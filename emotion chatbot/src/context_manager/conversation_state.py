class ConversationState:
    """
    Maintains short-term conversation context.
    """

    def __init__(self):
        self.previous_emotion = None
        self.previous_intent = None

    def update(self, emotion: str, intent: str):
        """
        Update the conversation state with current emotion and intent.
        """
        self.previous_emotion = emotion
        self.previous_intent = intent

    def get_state(self):
        """
        Return the current conversation state.
        """
        return {
            "previous_emotion": self.previous_emotion,
            "previous_intent": self.previous_intent
        }
