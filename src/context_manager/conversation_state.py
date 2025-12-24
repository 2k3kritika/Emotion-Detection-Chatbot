"""
================================
FILE: conversation_state.py
================================
PURPOSE:
Maintains short-term memory of the conversation to ensure
emotionally consistent responses.

TASKS FOR THIS FILE:
1. Store previous emotion and intent.
2. Prevent abrupt emotional changes in replies.
3. Provide context to response selector.

EXPECTED OUTPUT:
- Input: current emotion and intent
- Output: updated conversation state object

CONNECTED TO:
- response_selector.py
- app.py

INTEGRATION NOTES:
- Should remain lightweight and fast.
- No persistence beyond session unless specified.

OWNER:
Logic Team

DO NOT:
- Store long-term data
- Add ML or NLP logic
================================
"""
