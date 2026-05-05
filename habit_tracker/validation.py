from datetime import datetime


DATE_FORMAT = "%Y-%m-%d"


def validate_date_string(date_str: str) -> str:
    try:
        datetime.strptime(date_str, DATE_FORMAT)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"Invalid date format: {date_str}. Expected YYYY-MM-DD.") from exc
    return date_str


def normalize_completed_dates(completed_dates: list[str]) -> list[str]:
    unique_dates = []
    seen = set()
    for date_str in completed_dates:
        validated = validate_date_string(date_str)
        if validated not in seen:
            unique_dates.append(validated)
            seen.add(validated)
    return sorted(unique_dates)


def validate_habit_payload(payload: dict) -> dict:
    if not isinstance(payload, dict):
        raise ValueError("Habit payload must be a dictionary.")

    name = payload.get("name")
    if not isinstance(name, str) or not name.strip():
        raise ValueError("Habit name must be a non-empty string.")

    category = payload.get("category")
    if not isinstance(category, str) or not category.strip():
        raise ValueError("Habit category must be a non-empty string.")

    created_at = payload.get("created_at")
    validate_date_string(created_at)

    description = payload.get("description")
    if description is None:
        description = ""
    elif not isinstance(description, str):
        raise ValueError("Habit description must be a string.")

    completed_dates = payload.get("completed_dates", [])
    if not isinstance(completed_dates, list):
        raise ValueError("completed_dates must be a list of date strings.")
    payload["completed_dates"] = normalize_completed_dates(completed_dates)

    return {
        "id": payload.get("id"),
        "name": name.strip(),
        "description": description.strip(),
        "category": category.strip(),
        "created_at": created_at,
        "completed_dates": payload["completed_dates"],
    }
