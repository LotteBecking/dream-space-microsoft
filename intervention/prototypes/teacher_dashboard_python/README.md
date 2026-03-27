# Teacher Dashboard (Flask)

A teacher-facing dashboard for planning coding lessons, tracking student progress, and managing classes.

## Overview

This app provides:

- A home dashboard with quick lesson access, leaderboard, class metrics, and challenge insights
- A searchable lesson library and detailed lesson pages
- Student and class management views
- A basic account/settings page
- Local JSON-based storage for rapid prototyping

## Tech Stack

- Python 3.10+
- Flask
- Jinja2 templates
- Tailwind CSS (CDN)
- Font Awesome icons

## Project Structure

- app.py: main Flask app and routes
- requirements.txt: Python dependencies
- data/teacher_storage.py: local storage and auth helpers
- data/lessons.py: lesson loading/search utilities
- data/lesson_content/: lesson JSON files and manifest
- data/store/: runtime JSON storage (users, students, classes, last lesson)
- templates/: UI templates
- static/images/: lesson images and assets

## Features

- Authentication
- Register/login/logout flows using local user storage

- Dashboard
- Dynamic greeting and account context
- Featured lesson card with lesson cover support
- Podium-style top students leaderboard
- Most popular completed challenges panel
- Key metrics: total students, active assignments, average engagement

- Lessons
- Lesson library with search and track filtering
- Lesson detail pages with normalized teacher instructions
- Exercise and challenge presentation routes for classroom display

- Students and Classes
- Student list with class filter
- Student profile pages
- Class overview cards

## Getting Started

### 1. Clone and enter the project

```bash
git clone <your-repo-url>
cd dream-space-microsoft/intervention/prototypes/teacher_dashboard_python
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the app

```bash
python app.py
```

Open http://127.0.0.1:5000 in your browser.

## Default Data and Storage

The app uses local JSON/text storage in data/store.

- users.json: registered users
- students.json: student records
- classes.json: class records
- assignments.json: assignment records
- teacher_profile.json: profile defaults
- last_lesson.txt: recently opened lesson

If storage files are missing, defaults from data/teacher_storage.py are used.

## Important Notes

- This is a prototype-oriented implementation with local file storage.
- Passwords are SHA-256 hashed for development simplicity, not production security.
- For production, migrate to a proper database and stronger password hashing such as bcrypt or argon2.

## API Endpoints (Prototype)

- GET/POST /api/profile
- GET /api/classes
- GET /api/students
- POST /api/students/<student_id>/avatar

## Roadmap Ideas

- Add class/grade selection to registration
- Replace local storage with a relational database
- Add role-based access control
- Add tests and CI checks
- Add analytics from live student activity events

## License

Add your preferred license here, for example MIT.
