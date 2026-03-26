# Teacher Dashboard (Python)

> **Note:** This folder's templates and lesson content are **served by the unified backend** (`prototypes/backend/app.py`), not run standalone. The `app.py` in this folder is legacy and should not be run directly.
>
> To run the teacher dashboard:
> ```bash
> cd prototypes/backend
> python app.py   # serves dashboard at http://localhost:5000
> ```

This folder contains the Jinja2 templates, lesson JSON content, and static assets for the teacher-facing dashboard.

## What's in here

- `templates/` — Jinja2 HTML templates rendered by `backend/app.py`
- `data/lesson_content/` — 16 lesson JSON files (`lesson-1.json` … `lesson-16.json`) + `manifest.json`
- `static/images/` — Lesson thumbnail images and SVGs
- `data/lessons.py`, `data/teacher_storage.py` — Legacy data utilities (superseded by `backend/models.py`)

## Lesson Content

Lessons live as JSON files in `data/lesson_content/lesson-N.json`. Both the teacher dashboard and the kids app (iOS + web) read lesson content from these files. Edit the JSON here to change lesson content.

## Features

- Teacher dashboard home
- Lesson library with search
- Lesson detail view
- Class overview and management
- Student list with filtering
- Student progress profiles
- Teacher settings / profile
