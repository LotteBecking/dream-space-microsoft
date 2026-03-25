# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

DreamSpace is a digital coding intervention for kids consisting of four components that share a single SQLite database:

1. **Unified Flask Backend** (`prototypes/backend/`) — serves both the teacher dashboard HTML and the kids app REST API on port 5000
2. **Teacher Dashboard** (`prototypes/teacher_dashboard_python/`) — its templates, static assets, and lesson JSON files are served by the backend (not run standalone)
3. **Kids Learning iOS App** (`prototypes/kids_learning_app/`) — SwiftUI app that calls the backend REST API
4. **Kids Web App** (`kids_web_app/`) — Flask web app (port 5001) mirroring the iOS experience for browsers; proxies all data to the backend via HTTP

## Running the Backend

```bash
cd prototypes/backend
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python scripts/seed_db.py  # initialize/re-seed DB (add --force to wipe first)
python app.py              # starts Flask at http://localhost:5000
```

The backend reads lesson JSON from `../teacher_dashboard_python/data/lesson_content/` and serves HTML templates from `../teacher_dashboard_python/templates/`. These paths are configured in `config.py`.

## Running the iOS App

```bash
cd prototypes/kids_learning_app
xcodegen generate          # regenerates Xcode project from project.yml
open KidsCodingiOS.xcodeproj
# Select a simulator and run in Xcode
```

Default API base URL is `http://127.0.0.1:5000` (simulator). For a physical device on the same Wi-Fi, update the base URL in `APIService.swift` to the Mac's local IP.

## Architecture

### How the three components connect

```
Teacher Browser ──────────────────────────────────────────────┐
                                                               ▼
Kids iOS App ──── REST /api/kids/* ────► Flask Backend (5000) ◄─── HTML /dashboard/*
Kids Web App ──── REST /api/kids/* ──┘         │
(port 5001)                                    ▼
                                        SQLite (dreamspace.db)
                                               │
                                    lesson JSON files (teacher_dashboard_python/)
```

### Backend layer breakdown

| File | Role |
|------|------|
| `app.py` | Flask app factory; registers all route blueprints |
| `config.py` | Paths and env-var settings |
| `database.py` | `get_db()` / `init_db()` — SQLite connection per request |
| `models.py` | All query functions; returns camelCase dicts for API consumers |
| `validators.py` | Regex validators for every ID type |
| `db/schema.sql` | Authoritative schema — edit this, then re-run `scripts/seed_db.py --force` |
| `routes/dashboard.py` | Teacher dashboard HTML pages |
| `routes/api.py` | Teacher REST API |
| `routes/api_kids.py` | Kids app REST API |
| `routes/api_tracking.py` | Analytics event logging |
| `routes/api_auth.py` | Auth endpoints |
| `routes/api_progress.py` | Student progress tracking |

### iOS app layer breakdown

| File | Role |
|------|------|
| `Services/AppStore.swift` | Single `@MainActor ObservableObject` — all app state |
| `Services/APIService.swift` | Actor-based async/await HTTP client |
| `Models/AppModels.swift` | All `Codable` data structures |
| `Models/ChallengeData.swift` | Hardcoded challenge fallback + daily challenge logic |

The iOS app is **local-first**: state updates immediately in `AppStore`, then syncs to the server in the background. It gracefully degrades when the server is unreachable.

## ID Scheme — Keep Consistent Across Swift, Flask, and SQL

| Entity | Format | Regex |
|--------|--------|-------|
| student | `student-N` | `^student-[0-9]+$` |
| class | `class-N` | `^class-[0-9]+$` |
| lesson | `lesson-N` | `^lesson-[0-9]+$` |
| exercise | `exercise-N-N` | `^exercise-[0-9]+-[0-9]+$` |
| assignment | `assign-N` | `^assign-[0-9]+$` |
| achievement | `ach-N` | `^ach-[0-9]+$` |
| activity entry | `act-N` | `^act-[0-9]+$` |

- DB columns use `snake_case` names; frontend payloads use `camelCase` — mapping happens once in `models.py`
- Never reuse an ID value across entity types, even if the numbers overlap
- `validators.py` contains the regex checks — use them when accepting IDs from external input

## Running the Kids Web App

```bash
cd kids_web_app
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python app.py    # starts at http://localhost:5001 (backend must be on 5000)
```

Works in demo mode (static fallback data) if the backend is not running.

## Database

- Schema is in `prototypes/backend/db/schema.sql`; `database.py` auto-creates it on first startup
- All tables use `PRAGMA foreign_keys = ON`
- `models.py` is the only place that talks to the DB — don't write raw SQL in routes
- 20 tables total: teacher dashboard (12), kids app (6), auth/shared (2)
- **Full schema reference:** [`md-files/backend-database-schema-2026-03-24.md`](md-files/backend-database-schema-2026-03-24.md)
- **HTML visualization:** open `schema.html` in a browser (regenerate with `python generate_schema_html.py`)

## Lesson Content

Lessons live as JSON files in `prototypes/teacher_dashboard_python/data/lesson_content/lesson-N.json`. `lesson_loader.py` reads them at runtime. Both the teacher dashboard and the REST API serve content from these files — edit the JSON there to change lesson content.
