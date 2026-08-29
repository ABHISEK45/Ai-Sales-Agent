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