"""
================================
FILE: response_selector.py
================================
PURPOSE:
Selects the final chatbot response based on
predicted emotion, intent, and conversation context.

TASKS FOR THIS FILE:
1. Load response templates.
2. Match emotion and intent.
3. Randomly select an appropriate response.
4. Ensure tone matches emotional state.

EXPECTED OUTPUT:
- Input: emotion, intent, conversation context
- Output: One response string

CONNECTED TO:
- response_templates.json
- conversation_state.py
- app.py (caller)

INTEGRATION NOTES:
- This is where emotion-awareness actually happens.
- Output must always be a valid string.

OWNER:
Logic Team

DO NOT:
- Perform ML here
- Print or log excessively
================================
"""
