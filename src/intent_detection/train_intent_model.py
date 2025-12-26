# src/intent_detection/train_intent_model.py

import pandas as pd
import pickle

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

from src.preprocessing.text_cleaner import clean_text


INTENT_DATA_PATH = "data/processed/cleaned_intent.csv"
VECTOR_PATH = "models/intent_vectorizer.pkl"
MODEL_PATH = "models/intent_classifier.pkl"


def train_intent_model():
    # Load intent dataset
    df = pd.read_csv(INTENT_DATA_PATH)

    # debugging 
    print(df["intent"].value_counts())

    # Clean text
    df["text"] = df["text"].apply(clean_text)

    X = df["text"]
    y = df["intent"]

    # Vectorize text
    vectorizer = TfidfVectorizer()
    X_vec = vectorizer.fit_transform(X)

    # Train classifier
    model = LogisticRegression(max_iter=1000)
    model.fit(X_vec, y)

    # Save vectorizer and model
    with open(VECTOR_PATH, "wb") as f:
        pickle.dump(vectorizer, f)

    with open(MODEL_PATH, "wb") as f:
        pickle.dump(model, f)

    print("Intent model and vectorizer saved successfully.")


if __name__ == "__main__":
    train_intent_model()
