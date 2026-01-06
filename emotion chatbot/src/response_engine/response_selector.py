import json
import random
from pathlib import Path


class ResponseSelector:
    """
    Selects emotion-aware responses based on intent and context.
    """

    def __init__(self, template_path: str = None):
        if template_path is None:
            base_path = Path(__file__).resolve().parent
            template_path = base_path / "response_templates.json"

        with open(template_path, "r", encoding="utf-8") as file:
            self.templates = json.load(file)

    def select_response(self, emotion: str, intent: str, context_state: dict) -> str:
        """
        Select an appropriate response using emotion, intent and context.
        """

        # Fallbacks
        emotion_templates = self.templates.get(emotion)
        if not emotion_templates:
            return "I'm here to help you. Could you please tell me more?"

        intent_responses = emotion_templates.get(intent)
        if not intent_responses:
            return "I understand. Can you explain a bit more?"

        # Avoid repetition if same emotion + intent repeats
        if (
            context_state.get("previous_emotion") == emotion and
            context_state.get("previous_intent") == intent and
            len(intent_responses) > 1
        ):
            return random.choice(intent_responses[1:])

        return random.choice(intent_responses)
