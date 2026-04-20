"""Lessons route — grid and detail view from manifest.json."""

from flask import Blueprint, render_template, request, session, redirect, url_for, current_app, g
import services.api_client as api
from routes.auth import login_required

lessons_bp = Blueprint("lessons", __name__)

LEVEL_COLORS = {
    "Beginner": "green",
    "Intermediate": "yellow",
    "Advanced": "red",
}


@lessons_bp.route("/lessons")
@login_required
def list_lessons():
    lessons = current_app.config.get("LESSONS", [])
    completed = session.get("completed_lessons", [])
    for lesson in lessons:
        lesson["done"] = lesson["id"] in completed
        lesson["levelColor"] = LEVEL_COLORS.get(lesson.get("level", ""), "gray")
    return render_template("lessons/list.html", lessons=lessons, offline=api.is_offline())


@lessons_bp.route("/lessons/<lesson_id>")
@login_required
def detail(lesson_id):
    lessons_data = current_app.config.get("LESSONS_DATA", {})
    lesson = lessons_data.get(lesson_id)
    if not lesson:
        return redirect(url_for("lessons.list_lessons"))

    completed = session.get("completed_lessons", [])
    lesson["done"] = lesson_id in completed
    lesson["levelColor"] = LEVEL_COLORS.get(lesson.get("level", ""), "gray")

    return render_template("lessons/detail.html", lesson=lesson, offline=api.is_offline())


@lessons_bp.route("/lessons/<lesson_id>/complete", methods=["POST"])
@login_required
def complete(lesson_id):
    completed = session.get("completed_lessons", [])
    if lesson_id not in completed:
        completed.append(lesson_id)
        session["completed_lessons"] = completed
        session.modified = True
    return redirect(url_for("lessons.detail", lesson_id=lesson_id))
