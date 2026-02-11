import pytest

from src.emotion_detection.emotion_predictor import EmotionPredictor


def test_emotion_prediction_runs():
    predictor = EmotionPredictor(
        model_path="models/emotion_classifier.pkl"
    )

    # Minimal dummy input that matches your pipeline expectations
    # Adjust only if your model strictly requires vectors
    dummy_input = ["i am feeling very sad today"]

    emotion = predictor.predict(dummy_input)

    assert emotion is not None
    assert isinstance(emotion, str)
