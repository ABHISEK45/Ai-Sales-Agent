from backend.models import Session


class SessionManager:
    """Simple in-memory session manager."""

    def __init__(self):
        self.sessions: dict[str, Session] = {}

    def get_or_create(self, session_id: str) -> Session:
        if session_id not in self.sessions:
            self.sessions[session_id] = Session()

        return self.sessions[session_id]

    def save(self, session_id: str, session: Session) -> None:
        self.sessions[session_id] = session

    def delete(self, session_id: str) -> None:
        self.sessions.pop(session_id, None)