"""
================================
FILE: predict_intent.py
================================
PURPOSE:
Predicts the intent of user input during chatbot runtime.

TASKS FOR THIS FILE:
1. Load intent_classifier.pkl.
2. Load intent_vectorizer.pkl.
3. Apply preprocessing identical to training.
4. Predict intent label from text input.
5. Return a standardized intent string.

EXPECTED OUTPUT:
- Input: Raw user text
- Output: Intent label (e.g., greeting, help, complaint)

CONNECTED TO:
- text_cleaner.py
- intent_classifier.pkl
- intent_vectorizer.pkl
- app.py (caller)
- response_selector.py (consumer)

INTEGRATION NOTES:
- Output labels MUST match response_templates.json
- Do not retrain models here

OWNER:
ML Team / Logic Team
================================
"""

import pickle
from pathlib import Path

from src.preprocessing.text_cleaner import clean_text


class IntentPredictor:
    """
    Loads trained intent model and vectorizer
    and predicts intent from raw user text.
    """

    def __init__(
        self,
        model_path: str = "models/intent_classifier.pkl",
        vectorizer_path: str = "models/intent_vectorizer.pkl",
    ):
        # Resolve absolute paths safely
        base_path = Path(__file__).resolve().parents[2]

        model_path = base_path / model_path
        vectorizer_path = base_path / vectorizer_path

        if not model_path.exists():
            raise FileNotFoundError(f"Intent model not found at {model_path}")

        if not vectorizer_path.exists():
            raise FileNotFoundError(f"Intent vectorizer not found at {vectorizer_path}")

        with open(vectorizer_path, "rb") as f:
            self.vectorizer = pickle.load(f)

        with open(model_path, "rb") as f:
            self.model = pickle.load(f)

    def predict(self, text: str) -> str:
        """
        Predict intent from raw user text.
        """

        if not isinstance(text, str) or not text.strip():
            return "fallback"

        cleaned_text = clean_text(text)
        vectorized_text = self.vectorizer.transform([cleaned_text])
        intent = self.model.predict(vectorized_text)[0]

        return intent


# Optional CLI testing (won't interfere with API)
if __name__ == "__main__":
    predictor = IntentPredictor()

    while True:
        user_input = input("User: ")
        print("Predicted intent:", predictor.predict(user_input))
