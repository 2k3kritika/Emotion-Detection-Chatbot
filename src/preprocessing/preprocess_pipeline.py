import os
from typing import Dict, Any, List
import importlib.util


def _load_local(name: str, filename: str):
    """Helper to import modules when running this file directly."""
    path = os.path.join(os.path.dirname(__file__), filename)
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# Import shared utilities (package mode or direct mode)
try:
    from .text_cleaner import clean_text
    from .label_encoder import LabelEncoderWrapper
except Exception:
    _tc = _load_local("text_cleaner", "text_cleaner.py")
    _le = _load_local("label_encoder", "label_encoder.py")
    clean_text = _tc.clean_text
    LabelEncoderWrapper = _le.LabelEncoderWrapper


# ---------- helper to load multiple emotion CSVs ----------

def _load_emotion_csvs(csv_paths: List[str]):
    """Load and clean multiple emotion CSV files, returning texts and labels.
    Each CSV is expected to have 'text' and 'emotion' (or equivalent) columns.
    """
    texts: List[str] = []
    emotions: List[str] = []

    # Try pandas; if unavailable or fails, fall back to csv.DictReader
    try:
        import pandas as pd

        frames = []
        for path in csv_paths:
            df = pd.read_csv(path)

            # Detect / standardize text column
            if "text" not in df.columns:
                possible = [c for c in df.columns if "text" in c.lower()]
                if possible:
                    df = df.rename(columns={possible[0]: "text"})

            # Detect / standardize emotion column
            if "emotion" not in df.columns:
                possible = [
                    c for c in df.columns
                    if "emotion" in c.lower() or "label" in c.lower()
                ]
                if possible:
                    df = df.rename(columns={possible[0]: "emotion"})

            if "text" not in df.columns or "emotion" not in df.columns:
                raise ValueError(
                    f"{path} must have 'text' and 'emotion' (or equivalent) columns"
                )

            # Clean text and drop empty rows
            df["text"] = df["text"].astype(str).apply(clean_text)
            df = df[df["text"].str.strip() != ""]

            frames.append(df[["text", "emotion"]])

        if not frames:
            return [], []

        all_df = pd.concat(frames, ignore_index=True)
        texts = all_df["text"].tolist()
        emotions = all_df["emotion"].tolist()
        return texts, emotions

    except Exception:
        import csv

        for path in csv_paths:
            with open(path, newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                fieldnames = reader.fieldnames or []

                # Detect text column
                if "text" in fieldnames:
                    text_field = "text"
                else:
                    possible = [c for c in fieldnames if "text" in c.lower()]
                    if not possible:
                        raise ValueError(f"Could not find a text column in {path}")
                    text_field = possible[0]

                # Detect emotion / label column
                if "emotion" in fieldnames:
                    label_field = "emotion"
                else:
                    possible = [
                        c for c in fieldnames
                        if "emotion" in c.lower() or "label" in c.lower()
                    ]
                    if not possible:
                        raise ValueError(
                            f"Could not find an emotion/label column in {path}"
                        )
                    label_field = possible[0]

                for row in reader:
                    t = clean_text(row.get(text_field, ""))
                    if t:
                        texts.append(t)
                        emotions.append(row.get(label_field, ""))

        return texts, emotions


# ---------- helper to load intent CSV ----------

def _load_intent_csv(intent_csv: str):
    """Load an almost-cleaned intent CSV and apply extra clean_text().
    Expects at least a text column and optionally an intent/label column.
    """
    texts: List[str] = []
    intents: List[str] = []

    try:
        import pandas as pd

        df = pd.read_csv(intent_csv)

        # Detect / standardize text column
        if "text" not in df.columns:
            possible = [c for c in df.columns if "text" in c.lower()]
            if possible:
                df = df.rename(columns={possible[0]: "text"})

        # Detect / standardize intent column (can be called intent/label/tag, etc.)
        intent_col = None
        for cand in ["intent", "label", "tag"]:
            if cand in df.columns:
                intent_col = cand
                break
        if intent_col is None:
            possible = [
                c for c in df.columns
                if "intent" in c.lower() or "label" in c.lower() or "tag" in c.lower()
            ]
            if possible:
                intent_col = possible[0]

        # Apply extra cleaning on text
        df["text"] = df["text"].astype(str).apply(clean_text)
        df = df[df["text"].str.strip() != ""]

        texts = df["text"].tolist()
        if intent_col is not None:
            intents = df[intent_col].astype(str).tolist()
        else:
            # If no intent column, use empty strings
            intents = ["" for _ in texts]

        return texts, intents

    except Exception:
        import csv

        with open(intent_csv, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            fieldnames = reader.fieldnames or []

            # Detect text column
            if "text" in fieldnames:
                text_field = "text"
            else:
                possible = [c for c in fieldnames if "text" in c.lower()]
                if not possible:
                    raise ValueError(f"Could not find a text column in {intent_csv}")
                text_field = possible[0]

            # Detect intent column
            intent_field = None
            for cand in ["intent", "label", "tag"]:
                if cand in fieldnames:
                    intent_field = cand
                    break
            if intent_field is None:
                possible = [
                    c for c in fieldnames
                    if "intent" in c.lower() or "label" in c.lower() or "tag" in c.lower()
                ]
                if possible:
                    intent_field = possible[0]

            for row in reader:
                t = clean_text(row.get(text_field, ""))
                if t:
                    texts.append(t)
                    if intent_field is not None:
                        intents.append(row.get(intent_field, ""))
                    else:
                        intents.append("")

        return texts, intents


# ---------- main preprocessing pipeline ----------

def preprocess_text(
    train_csv: str = "data/raw/train.csv",
    test_csv: str = "data/raw/test.csv",
    val_csv: str = "data/raw/val.csv",
    intent_csv: str = "data/raw/intent_raw.csv",
    out_dir: str = "data/processed",
) -> Dict[str, str]:
    """Run preprocessing pipeline for emotions (three CSVs) and intents (one CSV).

    - Reads train.csv, test.csv, val.csv.
    - Applies clean_text() to all emotion texts.
    - Saves merged result as cleaned_text_emotion.csv in out_dir.
    - Encodes emotion labels and saves labels_encoded.pkl.
    - Reads an almost-cleaned intent CSV, applies extra clean_text(),
      and saves cleaned_intent.csv.
    """
    os.makedirs(out_dir, exist_ok=True)

    # 1. Load and clean emotions from all splits
    texts, emotions = _load_emotion_csvs([train_csv, test_csv, val_csv])

    # 2. Save cleaned_text_emotion.csv
    cleaned_text_path = os.path.join(out_dir, "cleaned_text_emotion.csv")
    try:
        import pandas as pd

        out_df = pd.DataFrame({"text": texts, "emotion": emotions})
        out_df.to_csv(cleaned_text_path, index=False)
    except Exception:
        import csv

        with open(cleaned_text_path, "w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["text", "emotion"])
            for t, e in zip(texts, emotions):
                writer.writerow([t, e])

    # 3. Label encoding for emotions
    le = LabelEncoderWrapper()
    le.fit(emotions)
    le_path = os.path.join(out_dir, "labels_encoded.pkl")
    le.save(le_path)

    # 4. Load and further clean intent CSV
    intent_texts, intent_labels = _load_intent_csv(intent_csv)

    cleaned_intent_csv = os.path.join(out_dir, "cleaned_intent.csv")
    try:
        import pandas as pd

        df_intent = pd.DataFrame({"intent": intent_labels, "text": intent_texts})
        df_intent.to_csv(cleaned_intent_csv, index=False)
    except Exception:
        import csv

        with open(cleaned_intent_csv, "w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["intent", "text"])
            for lbl, txt in zip(intent_labels, intent_texts):
                writer.writerow([lbl, txt])

    return {
        "cleaned_text": cleaned_text_path,
        "cleaned_intent": cleaned_intent_csv,
        "label_encoder": le_path,
    }


# ---------- CLI entry point ----------

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Run preprocessing pipeline")
    parser.add_argument("--train", default="data/raw/train.csv")
    parser.add_argument("--test", default="data/raw/test.csv")
    parser.add_argument("--val", default="data/raw/val.csv")
    parser.add_argument("--intent_csv", default="data/raw/intent_raw.csv")
    parser.add_argument("--out", default="data/processed")
    args = parser.parse_args()

    result = preprocess_text(
        train_csv=args.train,
        test_csv=args.test,
        val_csv=args.val,
        intent_csv=args.intent_csv,
        out_dir=args.out,
    )
    print(result)
