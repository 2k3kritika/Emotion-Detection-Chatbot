# app.py
# To run:
# pip install -r requirements.txt
# uvicorn src.app:app --reload

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uuid
from pathlib import Path

# Preprocessing & Models
from src.preprocessing.text_cleaner import clean_text
from src.intent_detection.predict_intent import IntentPredictor
from src.emotion_detection.emotion_predictor import EmotionPredictor

# Core logic
from src.context_manager.conversation_state import ConversationState
from src.response_engine.response_selector import ResponseSelector

# ----------- FastAPI Setup -----------
app = FastAPI(
    title="Emotion-Aware Chatbot API",
    description="An API for an emotion and intent aware chatbot",
    version="1.0.0"
)

# ----------- Base Path -----------
BASE_PATH = Path(__file__).resolve().parents[1]  # src/

# ----------- Initialize Components -----------
intent_predictor = IntentPredictor(
    model_path=BASE_PATH / "models" / "intent_classifier.pkl",
    vectorizer_path=BASE_PATH / "models" / "intent_vectorizer.pkl"
)

emotion_predictor = EmotionPredictor(
    model_path=BASE_PATH / "models" / "emotion_classifier.pkl",
    vectorizer_path=BASE_PATH / "models" / "emotion_vectorizer.pkl"
)

context_manager = ConversationState()
response_selector = ResponseSelector()  # automatically uses absolute path

# ----------- Request / Response Schemas -----------
class ChatRequest(BaseModel):
    message: str
    session_id: str | None = None

class ChatResponse(BaseModel):
    session_id: str
    intent: str
    emotion: str
    response: str

# ----------- Routes -----------
@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    if not request.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")

    # Session handling
    session_id = request.session_id or str(uuid.uuid4())
    context_manager.initialize_session(session_id)

    # Preprocessing
    cleaned_text = clean_text(request.message)

    # Predictions
    intent = intent_predictor.predict(request.message)
    emotion = emotion_predictor.predict(cleaned_text)  # fixed: pass string, not list

    # Context
    last_intent = context_manager.get_last_intent(session_id)

    # Response selection
    response = response_selector.select_response(
        intent=intent,
        emotion=emotion,
        last_intent=last_intent
    )

    # Update context
    context_manager.update_state(
        session_id=session_id,
        intent=intent,
        emotion=emotion,
        response=response
    )

    return ChatResponse(
        session_id=session_id,
        intent=intent,
        emotion=emotion,
        response=response
    )

@app.get("/")
def health_check():
    return {"status": "running", "message": "Emotion-Aware Chatbot API is alive"}
