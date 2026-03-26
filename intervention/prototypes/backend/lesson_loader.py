"""Lesson content loader – reads JSON files from the teacher-dashboard
lesson_content directory."""

import json
from pathlib import Path


def load_lessons(content_dir, include_unpublished=False):
    """Load all lessons listed in manifest.json."""
    content_path = Path(content_dir)
    manifest_path = content_path / 'manifest.json'

    if not manifest_path.exists():
        return []

    with manifest_path.open('r', encoding='utf-8') as f:
        manifest = json.load(f)

    loaded = []
    for entry in manifest.get('lessons', []):
        if not include_unpublished and not entry.get('published', True):
            continue

        rel_path = entry.get('path')
        if not rel_path:
            continue

        lesson_file = content_path / rel_path
        if not lesson_file.exists():
            continue

        with lesson_file.open('r', encoding='utf-8') as f:
            lesson = json.load(f)

        lesson.setdefault('id', entry.get('id'))
        lesson.setdefault('title', entry.get('title', 'Untitled Lesson'))
        if 'level' not in lesson and entry.get('level'):
            lesson['level'] = entry['level']

        loaded.append(lesson)

    return loaded


def search_lessons(lessons, query):
    """Filter lessons by title or description (case-insensitive)."""
    q = query.lower().strip()
    if not q:
        return lessons
    return [
        l for l in lessons
        if q in l.get('title', '').lower()
        or q in l.get('description', '').lower()
    ]


def get_lesson_by_id(lessons, lesson_id):
    """Find a single lesson by its ID."""
    return next((l for l in lessons if l.get('id') == lesson_id), None)
