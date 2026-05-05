from datetime import datetime, timedelta

from habit_tracker import storage, validation


DATE_FORMAT = "%Y-%m-%d"


def create_habit(habit_data: dict) -> dict:
    validated = validation.validate_habit_payload(habit_data)
    return storage.add_habit(validated)


def edit_habit(habit_id: str, updates: dict) -> dict | None:
    if "completed_dates" in updates:
        updates["completed_dates"] = validation.normalize_completed_dates(updates["completed_dates"])
    if "created_at" in updates:
        validation.validate_date_string(updates["created_at"])
    if "name" in updates and (not isinstance(updates["name"], str) or not updates["name"].strip()):
        raise ValueError("Habit name must be a non-empty string.")
    if "category" in updates and (not isinstance(updates["category"], str) or not updates["category"].strip()):
        raise ValueError("Habit category must be a non-empty string.")
    return storage.update_habit(habit_id, updates)


def delete_habit(habit_id: str) -> bool:
    return storage.delete_habit(habit_id)


def mark_habit_complete(habit_id: str, date_str: str) -> bool:
    validation.validate_date_string(date_str)
    return storage.add_completion_date(habit_id, date_str)


def _parse_dates(completed_dates: list[str]) -> list[datetime.date]:
    unique_dates = validation.normalize_completed_dates(completed_dates)
    return [datetime.strptime(date_str, DATE_FORMAT).date() for date_str in unique_dates]


def current_streak(completed_dates: list[str], reference_date: str) -> int:
    reference = datetime.strptime(validation.validate_date_string(reference_date), DATE_FORMAT).date()
    completed = set(_parse_dates(completed_dates))
    streak = 0
    current_day = reference
    while current_day in completed:
        streak += 1
        current_day -= timedelta(days=1)
    return streak


def best_streak(completed_dates: list[str]) -> int:
    dates = sorted(_parse_dates(completed_dates))
    if not dates:
        return 0

    best = 1
    current = 1
    for previous, current_date in zip(dates, dates[1:]):
        if current_date == previous + timedelta(days=1):
            current += 1
        else:
            best = max(best, current)
            current = 1
    return max(best, current)


def weekly_progress(completed_dates: list[str], reference_date: str) -> list[dict]:
    reference = datetime.strptime(validation.validate_date_string(reference_date), DATE_FORMAT).date()
    completed = {datetime.strptime(date_str, DATE_FORMAT).date() for date_str in validation.normalize_completed_dates(completed_dates)}
    result = []
    for offset in range(6, -1, -1):
        day = reference - timedelta(days=offset)
        result.append({"date": day.strftime(DATE_FORMAT), "completed": day in completed})
    return result
