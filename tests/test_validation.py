import pytest

from habit_tracker import validation


def test_invalid_date_strings_are_rejected():
    with pytest.raises(ValueError):
        validation.validate_date_string("2026-02-30")

    with pytest.raises(ValueError):
        validation.validate_date_string("bad-date")


def test_empty_habit_names_are_rejected():
    payload = {
        "id": "habit_001",
        "name": "",
        "description": "Read for 20 minutes",
        "category": "Study",
        "created_at": "2026-01-10",
        "completed_dates": [],
    }

    with pytest.raises(ValueError):
        validation.validate_habit_payload(payload)
