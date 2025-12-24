"""
================================
FILE: predict_emotion.py
================================
PURPOSE:
Predicts the emotion of user input during chatbot runtime.

TASKS FOR THIS FILE:
1. Load emotion_classifier.pkl and vectorizer.pkl.
2. Apply the same preprocessing as training.
3. Predict emotion label from user input.
4. Return a standardized emotion string.

EXPECTED OUTPUT:
- Input: Raw user text
- Output: One emotion label (e.g., sad, angry, happy, neutral)

CONNECTED TO:
- text_cleaning.py
- tokenizer.py (if used)
- emotion_classifier.pkl
- vectorizer.pkl
- app.py (caller)

INTEGRATION NOTES:
- This module is a runtime dependency.
- Output format must remain stable for response engine.

OWNER:
ML Team / Integration Team

DO NOT:
- Retrain models here
- Print debug output in production
================================
"""
