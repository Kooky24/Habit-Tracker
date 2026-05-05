import json
from pathlib import Path

STORAGE_FILE = Path(__file__).resolve().parents[1] / "data" / "habits.json"


def ensure_storage_file() -> None:
    STORAGE_FILE.parent.mkdir(parents=True, exist_ok=True)
    if not STORAGE_FILE.exists():
        STORAGE_FILE.write_text(json.dumps({"habits": []}, indent=2), encoding="utf-8")


def load_habits() -> dict:
    ensure_storage_file()
    try:
        return json.loads(STORAGE_FILE.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {"habits": []}


def save_habits(payload: dict) -> None:
    ensure_storage_file()
    STORAGE_FILE.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def get_habit_by_id(habit_id: str) -> dict | None:
    data = load_habits()
    return next((habit for habit in data.get("habits", []) if habit.get("id") == habit_id), None)


def add_habit(habit: dict) -> dict:
    data = load_habits()
    data.setdefault("habits", []).append(habit)
    save_habits(data)
    return habit


def update_habit(habit_id: str, updates: dict) -> dict | None:
    data = load_habits()
    for habit in data.get("habits", []):
        if habit.get("id") == habit_id:
            habit.update(updates)
            save_habits(data)
            return habit
    return None


def delete_habit(habit_id: str) -> bool:
    data = load_habits()
    habits = data.get("habits", [])
    filtered = [habit for habit in habits if habit.get("id") != habit_id]
    if len(filtered) == len(habits):
        return False
    data["habits"] = filtered
    save_habits(data)
    return True


def add_completion_date(habit_id: str, date_str: str) -> bool:
    data = load_habits()
    for habit in data.get("habits", []):
        if habit.get("id") == habit_id:
            completed = habit.setdefault("completed_dates", [])
            if date_str in completed:
                return False
            completed.append(date_str)
            completed.sort()
            save_habits(data)
            return True
    return False
