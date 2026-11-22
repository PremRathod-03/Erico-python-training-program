"""
Mini-Project 6: Simple To-Do App

A web application where users can add, view and delete tasks (plus mark them done).
- Flask for routing
- Jinja2 templating (base layout + index page)
- basic state management: tasks live in a Python list in memory
  (no database yet, so tasks reset when the server restarts)
- the session remembers the user's filter choice; flash messages give feedback

Run:  python app.py   ->  http://127.0.0.1:5001
"""
import os
from datetime import datetime
from itertools import count

from flask import Flask, abort, flash, redirect, render_template, request, session, url_for

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-only-change-me")

tasks: list[dict] = []          # in-memory "database"
_ids = count(1)
MAX_TITLE = 120
PRIORITIES = ("low", "medium", "high")


def add_task(title: str, priority: str = "medium") -> dict:
    task = {"id": next(_ids), "title": title, "priority": priority,
            "done": False, "created": datetime.now().strftime("%d %b %Y, %H:%M")}
    tasks.append(task)
    return task


def get_task(task_id: int) -> dict:
    task = next((t for t in tasks if t["id"] == task_id), None)
    if task is None:
        abort(404)
    return task


@app.route("/")
def index():
    show = request.args.get("show") or session.get("show", "all")
    if show not in ("all", "active", "done"):
        show = "all"
    session["show"] = show
    visible = [t for t in tasks
               if show == "all" or (show == "done") == t["done"]]
    stats = {"total": len(tasks), "done": sum(t["done"] for t in tasks)}
    return render_template("index.html", tasks=visible, show=show, stats=stats, priorities=PRIORITIES)


@app.post("/add")
def add():
    title = request.form.get("title", "").strip()
    priority = request.form.get("priority", "medium")
    if not title:
        flash("Task title cannot be empty.", "error")
    elif len(title) > MAX_TITLE:
        flash(f"Keep tasks under {MAX_TITLE} characters.", "error")
    elif priority not in PRIORITIES:
        flash("Invalid priority.", "error")
    else:
        add_task(title, priority)
        flash(f"Added “{title}”.", "success")
    return redirect(url_for("index"))


@app.post("/toggle/<int:task_id>")
def toggle(task_id):
    task = get_task(task_id)
    task["done"] = not task["done"]
    return redirect(url_for("index"))


@app.post("/delete/<int:task_id>")
def delete(task_id):
    task = get_task(task_id)
    tasks.remove(task)
    flash(f"Deleted “{task['title']}”.", "success")
    return redirect(url_for("index"))


@app.post("/clear-completed")
def clear_completed():
    removed = [t for t in tasks if t["done"]]
    for t in removed:
        tasks.remove(t)
    flash(f"Cleared {len(removed)} completed task(s).", "success")
    return redirect(url_for("index"))


@app.errorhandler(404)
def not_found(_error):
    flash("That task does not exist.", "error")
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True, port=5001)
