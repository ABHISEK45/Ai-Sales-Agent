from backend.analytics import generate_analytics
from backend.models import LeadState


def test_generate_analytics():
    lead = LeadState(
        configuration="3 BHK",
        budget="2 crore",
        interest_level="high",
        site_visit_status="booked",
    )

    analytics = generate_analytics(lead)

    assert analytics["configuration"] == "3 BHK"
    assert analytics["budget"] == "2 crore"
    assert analytics["interest_level"] == "high"
    assert analytics["site_visit_status"] == "booked"
    assert analytics["follow_up_required"] is False
    assert analytics["escalation_required"] is False