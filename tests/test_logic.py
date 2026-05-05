import pytest

from habit_tracker import logic


def test_empty_completion_list_returns_streak_zero():
    assert logic.current_streak([], "2026-01-03") == 0


def test_three_consecutive_dates_returns_current_streak_three():
    assert logic.current_streak(
        ["2026-01-01", "2026-01-02", "2026-01-03"], "2026-01-03"
    ) == 3


def test_missing_date_resets_current_streak():
    assert logic.current_streak(
        ["2026-01-01", "2026-01-02", "2026-01-04"], "2026-01-04"
    ) == 1


def test_duplicate_dates_do_not_increase_streak():
    assert logic.current_streak(
        ["2026-01-01", "2026-01-01", "2026-01-02"], "2026-01-02"
    ) == 2


def test_unordered_dates_still_give_correct_streak():
    assert logic.current_streak(
        ["2026-01-03", "2026-01-01", "2026-01-02"], "2026-01-03"
    ) == 3


def test_best_streak_works_across_several_periods():
    assert logic.best_streak(
        ["2026-01-01", "2026-01-02", "2026-01-04", "2026-01-05", "2026-01-06"]
    ) == 3


def test_weekly_progress_returns_the_last_seven_days():
    progress = logic.weekly_progress(
        ["2026-01-01", "2026-01-03", "2026-01-07"], "2026-01-07"
    )

    assert len(progress) == 7
    assert progress[0] == {"date": "2026-01-01", "completed": True}
    assert progress[1] == {"date": "2026-01-02", "completed": False}
    assert progress[2] == {"date": "2026-01-03", "completed": True}
    assert progress[-1] == {"date": "2026-01-07", "completed": True}
