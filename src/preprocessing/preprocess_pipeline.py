import os
import json
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


# ---------- main preprocessing pipeline ----------

def preprocess_text(
    train_csv: str = "data/raw/train.csv",
    test_csv: str = "data/raw/test.csv",
    val_csv: str = "data/raw/val.csv",
    intents_json: str = "data/raw/Intent.json",
    out_dir: str = "data/processed",
) -> Dict[str, str]:
    """Run preprocessing pipeline for emotions (CSV) and intents (JSON).

    - Reads train.csv, test.csv, val.csv.
    - Applies clean_text() to all emotion texts.
    - Saves merged result as cleaned_text_emotion.csv in out_dir.
    - Encodes emotion labels and saves labels_encoded.pkl.
    - Reads Intent.json, cleans texts with clean_text(), saves cleaned_intent.csv.
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

    # 3. Label encoding
    le = LabelEncoderWrapper()
    le.fit(emotions)
    le_path = os.path.join(out_dir, "labels_encoded.pkl")
    le.save(le_path)

    # 4. Process intents with the same clean_text() and save as CSV
    with open(intents_json, "r", encoding="utf-8") as f:
        intents = json.load(f)

    rows: List[Dict[str, str]] = []

    # Adjust this loop if Intent.json has a different structure
    # Here we assume: { "intent_name": ["phrase1", "phrase2", ...], ... }
    for intent_name, phrases in intents.items():
        for p in phrases:
            cleaned = clean_text(p)
            if cleaned.strip():
                rows.append({"intent": intent_name, "text": cleaned})

    cleaned_intent_csv = os.path.join(out_dir, "cleaned_intent.csv")
    try:
        import pandas as pd

        intents_df = pd.DataFrame(rows)
        intents_df.to_csv(cleaned_intent_csv, index=False)
    except Exception:
        import csv

        with open(cleaned_intent_csv, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["intent", "text"])
            writer.writeheader()
            writer.writerows(rows)

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
    parser.add_argument("--intents", default="data/raw/Intent.json")
    parser.add_argument("--out", default="data/processed")
    args = parser.parse_args()

    result = preprocess_text(
        train_csv=args.train,
        test_csv=args.test,
        val_csv=args.val,
        intents_json=args.intents,
        out_dir=args.out,
    )
    print(result)
