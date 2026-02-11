from pathlib import Path
import joblib

from src.preprocessing.label_encoder import LabelEncoderWrapper
from src.preprocessing.text_cleaner import clean_text


class EmotionPredictor:
    def __init__(self):
        base = Path(__file__).resolve().parents[2]

        self.model = joblib.load(base / "models/emotion_classifier.pkl")
        self.vectorizer = joblib.load(base / "models/emotion_vectorizer.pkl")
        self.label_encoder = LabelEncoderWrapper.load(
            base / "data/processed/labels_encoded.pkl"
        )

    def predict(self, text: str) -> str:
        cleaned = clean_text(text)
        vec = self.vectorizer.transform([cleaned])
        encoded = self.model.predict(vec)[0]
        return self.label_encoder.inverse_transform([encoded])[0]
