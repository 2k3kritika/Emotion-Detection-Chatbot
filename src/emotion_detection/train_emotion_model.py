"""
================================
FILE: train_emotion_model.py
================================
PURPOSE:
Trains the emotion classification model using processed data.

TASKS FOR THIS FILE:
1. Load cleaned_text.csv and encoded labels.
2. Train the emotion classification model.
3. Train or load the vectorizer.
4. Save trained model and vectorizer to /models.

EXPECTED OUTPUT:
- models/emotion_classifier.pkl
- models/vectorizer.pkl
- data/processed/labels_encoded.pkl (if generated here)

CONNECTED TO:
- text_cleaning.py
- cleaned_text.csv
- labels_encoded.pkl
- predict_emotion.py (consumer)

INTEGRATION NOTES:
- This file is executed manually, NOT during runtime.
- Output files must exist before running app.py.

OWNER:
ML Team

DO NOT:
- Import this file in app.py
- Add runtime chatbot logic
================================
"""
