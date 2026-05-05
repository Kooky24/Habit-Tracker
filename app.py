from datetime import date
from uuid import uuid4

from flask import Flask, abort, redirect, render_template, request, url_for

from habit_tracker import logic, storage, validation

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True


def generate_habit_id() -> str:
    return f"habit_{uuid4().hex[:8]}"


def build_habit_summary(habit: dict) -> dict:
    today = date.today().isoformat()
    return {
        **habit,
        "current_streak": logic.current_streak(habit.get("completed_dates", []), today),
        "best_streak": logic.best_streak(habit.get("completed_dates", [])),
        "weekly_progress": logic.weekly_progress(habit.get("completed_dates", []), today),
    }


@app.route("/")
def index():
    data = storage.load_habits()
    habits = [build_habit_summary(habit) for habit in data.get("habits", [])]
    return render_template("index.html", habits=habits)


@app.route("/habits/new", methods=["GET", "POST"])
def create_habit():
    if request.method == "POST":
        payload = {
            "id": generate_habit_id(),
            "name": request.form.get("name", "").strip(),
            "description": request.form.get("description", "").strip(),
            "category": request.form.get("category", "").strip(),
            "created_at": date.today().isoformat(),
            "completed_dates": [],
        }
        validated = validation.validate_habit_payload(payload)
        storage.add_habit(validated)
        return redirect(url_for("index"))

    return render_template("create_habit.html")


@app.route("/habits/<habit_id>/edit", methods=["GET", "POST"])
def edit_habit(habit_id: str):
    habit = storage.get_habit_by_id(habit_id)
    if habit is None:
        abort(404)

    if request.method == "POST":
        updates = {
            "name": request.form.get("name", "").strip(),
            "description": request.form.get("description", "").strip(),
            "category": request.form.get("category", "").strip(),
            "created_at": request.form.get("created_at", habit.get("created_at")),
        }
        logic.edit_habit(habit_id, updates)
        return redirect(url_for("index"))

    return render_template("edit_habit.html", habit=habit)


@app.route("/habits/<habit_id>/delete", methods=["POST"])
def delete_habit(habit_id: str):
    if not storage.delete_habit(habit_id):
        abort(404)
    return redirect(url_for("index"))


@app.route("/habits/<habit_id>/complete", methods=["POST"])
def complete_habit(habit_id: str):
    today = date.today().isoformat()
    if not logic.mark_habit_complete(habit_id, today):
        # If duplicate completion or missing habit, still redirect to stay idempotent.
        return redirect(url_for("index"))
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
