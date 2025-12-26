"""
================================
FILE: predict_intent.py
================================
PURPOSE:
Predicts the intent of user input during chatbot runtime.

TASKS FOR THIS FILE:
1. Load intent_classifier.pkl.
2. Apply preprocessing identical to training.
3. Predict intent label from text input.
4. Return a standardized intent string.

EXPECTED OUTPUT:
- Input: Raw user text
- Output: Intent label (e.g., greeting, question, complaint)

CONNECTED TO:
- text_cleaning.py
- tokenizer.py
- intent_classifier.pkl
- app.py (caller)
- response_selector.py (consumer)

INTEGRATION NOTES:
- Output labels must match response_templates.json.
- Any change here affects response logic.

OWNER:
ML Team / Logic Team

DO NOT:
- Retrain models here
- Change label names casually
================================
"""


# src/intent_detection/predict_intent.py

import pickle
from src.preprocessing.text_cleaner import clean_text

VECTOR_PATH = "models/intent_vectorizer.pkl"
MODEL_PATH = "models/intent_classifier.pkl"


with open(VECTOR_PATH, "rb") as f:
    vectorizer = pickle.load(f)

with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)


def predict_intent(text: str) -> str:
    cleaned = clean_text(text)
    vectorized = vectorizer.transform([cleaned])
    intent = model.predict(vectorized)[0]
    return intent


if __name__ == "__main__":
    while True:
        user_input = input("User: ")
        print("Predicted intent:", predict_intent(user_input))
