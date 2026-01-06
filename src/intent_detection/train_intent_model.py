"""
================================
FILE: train_intent_model.py
================================
PURPOSE:
Trains the intent classification model used to understand
what the user wants (greeting, question, complaint, etc.).

TASKS FOR THIS FILE:
1. Load processed intent training data.
2. Apply the same preprocessing used elsewhere.
3. Train an intent classification model.
4. Save the trained model to the models directory.

EXPECTED OUTPUT:
- models/intent_classifier.pkl
- data/processed/labels_encoded.pkl (if intent labels are encoded here)

CONNECTED TO:
- text_cleaning.py
- tokenizer.py
- intents.json
- predict_intent.py (consumer)

INTEGRATION NOTES:
- This script is run manually.
- Must NOT be imported into app.py.
- Output model must exist before chatbot runtime.

OWNER:
ML Team

DO NOT:
- Add chatbot runtime logic
- Print excessive debug output
================================
"""
