from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.agent import NorthstarAgent, SessionManager
from backend.models import ChatRequest, ChatResponse


app = FastAPI(
    title="Northstar AI Sales Agent",
    description="AI-powered conversational sales agent for Northstar One.",
    version="1.0.0",
)


# Allow the frontend to communicate with the backend during development.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


session_manager = SessionManager()
agent = NorthstarAgent()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    session = session_manager.get_or_create(request.session_id)

    response = agent.chat(
        session=session,
        user_message=request.message,
    )

    session_manager.save(request.session_id, session)

    return ChatResponse(
        response=response,
        lead_state=session.lead,
    )