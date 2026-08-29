from backend.agent import SessionManager


def test_session_creation():
    manager = SessionManager()

    session = manager.get_or_create("test-session")

    assert session.gemini_interaction_id is None
    assert session.lead.configuration is None
    assert session.lead.budget is None


def test_session_persistence():
    manager = SessionManager()

    session = manager.get_or_create("test-session")

    session.lead.configuration = "3 BHK"
    session.lead.budget = "₹2 crore"

    manager.save("test-session", session)

    retrieved = manager.get_or_create("test-session")

    assert retrieved.lead.configuration == "3 BHK"
    assert retrieved.lead.budget == "₹2 crore"