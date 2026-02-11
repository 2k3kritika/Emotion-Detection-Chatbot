# emotion_predictor.py

from pathlib import Path
import joblib

from src.preprocessing.label_encoder import LabelEncoderWrapper
from src.preprocessing.text_cleaner import clean_text


class EmotionPredictor:
    def __init__(self, model_path=None, vectorizer_path=None, label_encoder_path=None):
        base = Path(__file__).resolve().parents[2]

        # Use paths passed in, otherwise default to original paths
        self.model = joblib.load(model_path or base / "models/emotion_classifier.pkl")
        self.vectorizer = joblib.load(vectorizer_path or base / "models/emotion_vectorizer.pkl")
        self.label_encoder = LabelEncoderWrapper.load(
            label_encoder_path or base / "data/processed/labels_encoded.pkl"
        )

    def predict(self, text: str) -> str:
        cleaned = clean_text(text)
        vec = self.vectorizer.transform([cleaned])
        encoded = self.model.predict(vec)[0]
        return self.label_encoder.inverse_transform([encoded])[0]
