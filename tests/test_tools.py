from backend.tools import book_site_visit


def test_successful_site_visit_booking():
    result = book_site_visit("Saturday", "11:00 AM")

    assert result["status"] == "success"
    assert result["date"] == "Saturday"
    assert result["time"] == "11:00 AM"


def test_failed_site_visit_booking():
    result = book_site_visit("Saturday", "2:00 PM")

    assert result["status"] == "failed"
    assert result["date"] == "Saturday"
    assert result["time"] == "2:00 PM"