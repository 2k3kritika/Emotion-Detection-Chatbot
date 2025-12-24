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
