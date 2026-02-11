# train_intent_model.py
import json
import pandas as pd
from pathlib import Path
import pickle

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# Optional: use the same text cleaner as other modules
from src.preprocessing.text_cleaner import clean_text

# -------------------- Paths --------------------
ROOT_DIR = Path(__file__).resolve().parents[2]  # root
JSON_PATH = ROOT_DIR / "data/processed/cleaned_intents.json"
CSV_PATH = ROOT_DIR / "data/processed/cleaned_intent.csv"  # optional record
VECTOR_PATH = ROOT_DIR / "models/intent_vectorizer.pkl"
MODEL_PATH = ROOT_DIR / "models/intent_classifier.pkl"

# -------------------- Load and Process JSON --------------------
with open(JSON_PATH, "r", encoding="utf-8") as f:
    intents = json.load(f)

rows = []
for intent_label, phrases in intents.items():
    for phrase in phrases:
        cleaned_phrase = clean_text(phrase)
        if cleaned_phrase:  # skip empty strings
            rows.append({"text": cleaned_phrase, "intent": intent_label})

if not rows:
    raise ValueError("No valid training data found in cleaned_intents.json")

df = pd.DataFrame(rows)

# Optional: save CSV for reference
df.to_csv(CSV_PATH, index=False)
print(f"Training data prepared with {len(df)} samples and {df['intent'].nunique()} intent classes.")
print(df['intent'].value_counts())

# -------------------- Train Model --------------------
X = df["text"]
y = df["intent"]

vectorizer = TfidfVectorizer()
X_vec = vectorizer.fit_transform(X)

model = LogisticRegression(max_iter=1000)
model.fit(X_vec, y)

# -------------------- Save Artifacts --------------------
VECTOR_PATH.parent.mkdir(parents=True, exist_ok=True)
MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)

with open(VECTOR_PATH, "wb") as f:
    pickle.dump(vectorizer, f)

with open(MODEL_PATH, "wb") as f:
    pickle.dump(model, f)

print("Intent model and vectorizer saved successfully.")
