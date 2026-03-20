"""Lesson content loader.

Storage model:
- `data/lesson_content/manifest.json` contains lesson ordering and metadata.
- Each lesson is stored in its own JSON file under `data/lesson_content/`.
"""

import json
from pathlib import Path

LESSON_CONTENT_DIR = Path(__file__).resolve().parent / "lesson_content"
MANIFEST_PATH = LESSON_CONTENT_DIR / "manifest.json"


def _load_manifest():
    if not MANIFEST_PATH.exists():
        return {"version": 1, "lessons": []}

    with MANIFEST_PATH.open("r", encoding="utf-8") as file:
        return json.load(file)


def load_lessons(include_unpublished=False):
    """Load lesson files based on manifest order."""
    manifest = _load_manifest()
    lesson_entries = manifest.get("lessons", [])
    loaded_lessons = []

    for entry in lesson_entries:
        if not include_unpublished and not entry.get("published", True):
            continue

        lesson_path_value = entry.get("path")
        if not lesson_path_value:
            continue

        lesson_path = LESSON_CONTENT_DIR / lesson_path_value
        if not lesson_path.exists():
            continue

        with lesson_path.open("r", encoding="utf-8") as file:
            lesson = json.load(file)

        if "id" not in lesson:
            lesson["id"] = entry.get("id")
        if "title" not in lesson:
            lesson["title"] = entry.get("title", "Untitled Lesson")
        if "level" not in lesson and entry.get("level"):
            lesson["level"] = entry.get("level")

        loaded_lessons.append(lesson)

    return loaded_lessons


lessons = load_lessons()


def search_lessons(query):
    """Search lessons by title or description."""
    query = query.lower().strip()
    if not query:
        return lessons

    return [
        lesson
        for lesson in lessons
        if query in lesson.get("title", "").lower()
        or query in lesson.get("description", "").lower()
    ]


def get_lesson_by_id(lesson_id):
    """Get a lesson by ID."""
    return next((lesson for lesson in lessons if lesson.get("id") == lesson_id), None)
