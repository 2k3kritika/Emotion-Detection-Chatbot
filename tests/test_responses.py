from src.response_engine.response_selector import ResponseSelector


def test_valid_intent_and_emotion():
    selector = ResponseSelector(
        templates_path="src/response_engine/response_templates.json"
    )

    response = selector.select_response(
        intent="greeting",
        emotion="happy"
    )

    assert response is not None
    assert isinstance(response, str)
    assert len(response) > 0


def test_unknown_intent_fallback():
    selector = ResponseSelector(
        templates_path="src/response_engine/response_templates.json"
    )

    response = selector.select_response(
        intent="unknown_intent",
        emotion="neutral"
    )

    assert response is not None
    assert isinstance(response, str)


def test_missing_emotion_fallback():
    selector = ResponseSelector(
        templates_path="src/response_engine/response_templates.json"
    )

    response = selector.select_response(
        intent="greeting",
        emotion="nonexistent_emotion"
    )

    assert response is not None
    assert isinstance(response, str)
