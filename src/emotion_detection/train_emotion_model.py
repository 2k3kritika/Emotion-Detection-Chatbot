# src/emotion_detection/train_emotion_model.py

import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT_DIR))


import os
import joblib
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

from src.preprocessing.text_cleaner import clean_text
from src.preprocessing.label_encoder import LabelEncoderWrapper

DATA_PATH = "data/processed/cleaned_text_emotion.csv"
MODEL_PATH = "models/emotion_classifier.pkl"
VECTORIZER_PATH = "models/emotion_vectorizer.pkl"
LABEL_ENCODER_PATH = "data/processed/labels_encoded.pkl"


def train_emotion_model():
    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError("Cleaned emotion data not found")

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

    print("Emotion model, vectorizer, and labels saved.")


if __name__ == "__main__":
    train_emotion_model()
