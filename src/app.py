"""
================================
FILE: app.py
================================
PURPOSE:
Main entry point of the chatbot application.
Acts as the orchestrator connecting all modules.

TASKS FOR THIS FILE:
1. Accept user input.
2. Call text preprocessing.
3. Call emotion prediction.
4. Call intent prediction.
5. Update conversation context.
6. Call response selector.
7. Output final chatbot response.

EXPECTED OUTPUT:
- Input: User message (string)
- Output: Chatbot reply (string)

CONNECTED TO:
- text_cleaning.py
- predict_emotion.py
- predict_intent.py
- conversation_state.py
- response_selector.py
- logger.py

INTEGRATION NOTES:
- This file should NOT contain ML logic.
- Keep logic linear and readable.
- Any module change must reflect here.

OWNER:
Integration Team

DO NOT:
- Train models
- Hardcode responses
- Add heavy logic
================================
"""
