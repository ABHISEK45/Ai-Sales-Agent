AVAILABLE_SLOTS = {
    "11:00 AM",
    "3:00 PM",
}


def book_site_visit(date: str, time: str) -> dict:
    """
    Simulate booking a Northstar One site visit.

    The mock booking system accepts a small set of predefined
    time slots so we can demonstrate both success and failure.
    """

    if time not in AVAILABLE_SLOTS:
        return {
            "status": "failed",
            "date": date,
            "time": time,
            "message": "The requested time slot is unavailable.",
        }

    return {
        "status": "success",
        "date": date,
        "time": time,
        "message": "Site visit booked successfully.",
    }


BOOK_SITE_VISIT_TOOL = {
    "type": "function",
    "name": "book_site_visit",
    "description": (
        "Book a site visit for Northstar One. "
        "Use this only after the customer has provided "
        "both a preferred date and time."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "date": {
                "type": "string",
                "description": "Preferred site visit date.",
            },
            "time": {
                "type": "string",
                "description": "Preferred site visit time.",
            },
        },
        "required": ["date", "time"],
    },
}
UPDATE_LEAD_TOOL = {
    "type": "function",
    "name": "update_lead",
    "description": (
        "Update customer lead information when the customer provides "
        "new information. Only include fields explicitly stated or "
        "clearly implied by the customer's current message. "
        "Do not invent information."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "name": {
                "type": "string",
                "description": "Customer's name, if provided.",
            },
            "configuration": {
                "type": "string",
                "description": "Preferred property configuration, such as 2 BHK or 3 BHK.",
            },
            "budget": {
                "type": "string",
                "description": "Customer's stated budget.",
            },
            "purchase_timeline": {
                "type": "string",
                "description": "Customer's stated purchase timeline.",
            },
            "interest_level": {
                "type": "string",
                "description": "Customer's demonstrated level of purchase interest.",
            },
            "follow_up_required": {
                "type": "boolean",
                "description": "Whether the customer explicitly requests follow-up.",
            },
            "preferred_language": {
                "type": "string",
                "description": "Customer's preferred language if explicitly stated.",
            },
        },
    },
}