# train_emotion_model.py
import sys
from pathlib import Path
import os
import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from src.preprocessing.text_cleaner import clean_text
from src.preprocessing.label_encoder import LabelEncoderWrapper

# ----------- Paths -----------
ROOT_DIR = Path(__file__).resolve().parents[2]  # root
DATA_PATH = ROOT_DIR / "data/processed/cleaned_text.csv"  # matches preprocessing output
MODEL_PATH = ROOT_DIR / "models/emotion_classifier.pkl"
VECTORIZER_PATH = ROOT_DIR / "models/emotion_vectorizer.pkl"
LABEL_ENCODER_PATH = ROOT_DIR / "data/processed/labels_encoded.pkl"

def train_emotion_model():
    if not DATA_PATH.exists():
        raise FileNotFoundError(f"Cleaned emotion data not found at {DATA_PATH}")

    df = pd.read_csv(DATA_PATH)

    df["text"] = df["text"].apply(clean_text)
    X = df["text"]
    y = df["emotion"]

    # Encode labels
    le = LabelEncoderWrapper()
    le.fit(y.tolist())
    y_encoded = le.transform(y.tolist())
    le.save(LABEL_ENCODER_PATH)

    # Vectorize
    vectorizer = TfidfVectorizer()
    X_vec = vectorizer.fit_transform(X)

    # Train model
    model = LogisticRegression(max_iter=1000)
    model.fit(X_vec, y_encoded)

    # Save artifacts
    joblib.dump(model, MODEL_PATH)
    joblib.dump(vectorizer, VECTORIZER_PATH)

    print("Emotion model, vectorizer, and label encoder saved successfully.")

if __name__ == "__main__":
    train_emotion_model()
