"""
================================
FILE: test_responses.py
================================
PURPOSE:
Validates that the chatbot selects correct responses
based on emotion, intent, and context.

TASKS FOR THIS FILE:
1. Test response selection logic.
2. Ensure emotion + intent mapping works correctly.
3. Verify fallback responses exist for edge cases.

EXPECTED OUTPUT:
- Test pass/fail results.
- Assertion errors if response logic breaks.

CONNECTED TO:
- response_selector.py
- response_templates.json
- conversation_state.py

INTEGRATION NOTES:
- This test ensures the chatbot sounds human.
- If this fails, the bot may reply incorrectly.

OWNER:
Testing Team

DO NOT:
- Modify response templates here
- Hardcode responses inside tests
================================
"""
