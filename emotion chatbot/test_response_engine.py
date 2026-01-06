from src.context_manager.conversation_state import ConversationState
from src.response_engine.response_selector import ResponseSelector

def main():
    state = ConversationState()
    selector = ResponseSelector()

    # Example input (normally comes from other teams)
    emotion = "sad"
    intent = "complaint"

    response = selector.select_response(
        emotion=emotion,
        intent=intent,
        context_state=state.get_state()
    )

    print("Bot Response:")
    print(response)

    # Update context after response
    state.update(emotion, intent)

if __name__ == "__main__":
    main()
