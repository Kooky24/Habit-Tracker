from datetime import date

from habit_tracker import logic, storage


def test_integration_save_reload_and_mark_complete(tmp_path, monkeypatch):
    temp_file = tmp_path / "habits.json"
    monkeypatch.setattr(storage, "STORAGE_FILE", temp_file)

    habit = {
        "id": "habit_001",
        "name": "Read",
        "description": "Read for 20 minutes",
        "category": "Study",
        "created_at": "2026-01-10",
        "completed_dates": [],
    }

    storage.add_habit(habit)

    loaded = storage.load_habits()
    assert loaded["habits"][0]["id"] == "habit_001"
    assert loaded["habits"][0]["completed_dates"] == []

    assert logic.mark_habit_complete("habit_001", "2026-01-10") is True

    reloaded = storage.load_habits()
    assert reloaded["habits"][0]["completed_dates"] == ["2026-01-10"]
