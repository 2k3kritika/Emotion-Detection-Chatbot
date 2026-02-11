# conversation_state.py
from typing import Dict, Optional
from datetime import datetime


class ConversationState:
    """
    Manages conversational context per session/user.
    """

    def __init__(self):
        # session_id -> state
        self.sessions: Dict[str, Dict] = {}

    def initialize_session(self, session_id: str) -> None:
        if session_id not in self.sessions:
            self.sessions[session_id] = {
                "last_intent": None,
                "last_emotion": None,
                "last_response": None,
                "history": [],
                "created_at": datetime.utcnow()
            }

    def update_state(
        self,
        session_id: str,
        intent: str,
        emotion: str,
        response: str
    ) -> None:
        self.initialize_session(session_id)

        self.sessions[session_id]["last_intent"] = intent
        self.sessions[session_id]["last_emotion"] = emotion
        self.sessions[session_id]["last_response"] = response

        self.sessions[session_id]["history"].append({
            "intent": intent,
            "emotion": emotion,
            "response": response,
            "timestamp": datetime.utcnow()
        })

    def get_last_intent(self, session_id: str) -> Optional[str]:
        return self.sessions.get(session_id, {}).get("last_intent")

    def get_last_emotion(self, session_id: str) -> Optional[str]:
        return self.sessions.get(session_id, {}).get("last_emotion")

    def get_history(self, session_id: str):
        return self.sessions.get(session_id, {}).get("history", [])

    def reset_session(self, session_id: str) -> None:
        if session_id in self.sessions:
            del self.sessions[session_id]
