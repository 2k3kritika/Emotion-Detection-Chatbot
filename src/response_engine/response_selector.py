import json
import random
from typing import Optional
from pathlib import Path

class ResponseSelector:
    """
    Selects responses based on intent, emotion, and conversation context.
    """

    def __init__(self, templates_path: str = None):
        # Use default path relative to this file if none provided
        if templates_path is None:
            base = Path(__file__).resolve().parents[1]  # points to src/response_engine
            templates_path = base / "response_templates.json"

        templates_path = Path(templates_path)

        if not templates_path.exists():
            raise FileNotFoundError(
                f"Response templates not found at {templates_path}"
            )

        with open(templates_path, "r", encoding="utf-8") as f:
            self.templates = json.load(f)

    def select_response(
        self,
        intent: str,
        emotion: str,
        last_intent: Optional[str] = None
    ) -> str:
        """
        Select an appropriate response.

        Priority:
        1. intent + emotion
        2. intent only
        3. fallback
        """

        # 1️⃣ Intent + Emotion
        intent_block = self.templates.get(intent, {})
        emotion_responses = intent_block.get(emotion)

        if emotion_responses:
            return random.choice(emotion_responses)

        # 2️⃣ Intent only (neutral fallback)
        neutral_responses = intent_block.get("neutral")
        if neutral_responses:
            return random.choice(neutral_responses)

        # 3️⃣ Absolute fallback
        fallback = self.templates.get("fallback", {}).get("neutral", [])
        if fallback:
            return random.choice(fallback)

        return "I'm not sure how to respond to that right now."
