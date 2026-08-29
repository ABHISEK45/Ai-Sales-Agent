from backend.models import LeadState


def generate_analytics(lead: LeadState) -> dict:
    """Generate structured analytics from the completed lead state."""

    return {
        "configuration": lead.configuration,
        "budget": lead.budget,
        "purchase_timeline": lead.purchase_timeline,
        "interest_level": lead.interest_level,
        "site_visit_status": lead.site_visit_status,
        "site_visit_date": lead.site_visit_date,
        "site_visit_time": lead.site_visit_time,
        "follow_up_required": lead.follow_up_required,
        "preferred_language": lead.preferred_language,
        "escalation_required": lead.escalation_required,
        "opted_out": lead.opted_out,
        "conversation_ended": lead.conversation_ended,
    }