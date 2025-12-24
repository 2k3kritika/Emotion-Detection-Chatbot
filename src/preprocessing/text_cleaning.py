"""
================================
FILE: text_cleaning.py
================================
PURPOSE:
Provides a single, reusable text-cleaning pipeline used
for both training and inference.

TASKS FOR THIS FILE:
1. Clean raw user text (lowercase, punctuation removal, etc.).
2. Ensure identical preprocessing during training and prediction.
3. Expose a clean_text(text: str) function.

EXPECTED OUTPUT:
- Input: Raw string
- Output: Cleaned string (normalized text)

CONNECTED TO:
- data/processed/cleaned_text.csv (generation)
- train_emotion_model.py
- train_intent_model.py
- predict_emotion.py
- predict_intent.py

INTEGRATION NOTES:
- Any change here REQUIRES model retraining.
- This file is a single source of truth for text preprocessing.

OWNER:
ML Team

DO NOT:
- Add model logic
- Perform training here
- Change output format without informing team
================================
"""
