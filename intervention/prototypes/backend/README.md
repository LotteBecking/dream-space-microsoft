# Dream Space Backend

Unified Flask backend for both the **Teacher Dashboard** and the **Kids Learning App** prototypes. Uses SQLite for persistent storage and user tracking.

## Quick Start

```bash
# 1. Create a virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS / Linux

# 2. Install dependencies
pip install -r requirements.txt

# 3. Create tables and seed default data
python seed_db.py

# 4. Run the server
python app.py
```

The server starts at **http://localhost:5000**.

- **Teacher dashboard** — open http://localhost:5000/ in a browser.
- **REST API** — the `/api/` endpoints return JSON.

---

## Database

SQLite database stored at `backend/dreamspace.db`. Tables are created automatically on first run from [schema.sql](schema.sql).

### ID Conventions

| Entity | Format | Example |
|---|---|---|
| student_id | `student-N` | `student-1` |
| class_id | `class-N` | `class-3` |
| lesson_id | `lesson-N` | `lesson-8` |
| exercise_id | `exercise-N-N` | `exercise-4-2` |
| assignment_id | `assign-N` | `assign-1` |
| achievement_id | `ach-N` | `ach-2` |
| activity_id | `act-N` | `act-1` |

These formats are enforced by the backend validators and match the IDs already used in the Swift client.

---

## API Reference

### Teacher Dashboard API

| Method | Endpoint | Description |
|---|---|---|
| GET/POST | `/api/profile` | Teacher profile |
| GET | `/api/classes` | List classes |
| GET | `/api/classes/<class_id>` | Single class |
| POST | `/api/classes` | Create class |
| PUT | `/api/classes/<class_id>` | Update class |
| GET | `/api/classes/<class_id>/students` | Students in class |
| GET | `/api/students` | List students (optional `?class_id=`) |
| GET | `/api/students/<student_id>` | Single student |
| POST | `/api/students` | Create student |
| PUT | `/api/students/<student_id>` | Update student |
| POST | `/api/students/<student_id>/avatar` | Update avatar |
| GET | `/api/students/<student_id>/achievements` | Student achievements |
| POST | `/api/students/<student_id>/achievements` | Add achievement |
| GET | `/api/students/<student_id>/activity` | Activity log |
| POST | `/api/students/<student_id>/activity` | Log activity |
| GET | `/api/lessons` | List lessons (optional `?search=`) |
| GET | `/api/lessons/<lesson_id>` | Single lesson (full JSON) |
| GET | `/api/lessons/<lesson_id>/exercises` | Exercises for lesson |
| GET | `/api/assignments` | List assignments |
| GET | `/api/assignments/<assignment_id>` | Single assignment |
| POST | `/api/assignments` | Create assignment |
| PUT | `/api/assignments/<assignment_id>` | Update assignment |
| GET | `/api/achievements` | List all achievements |

### Kids Learning App API

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/kids/challenges` | List challenges (optional `?difficulty=&age=`) |
| GET | `/api/kids/challenges/daily` | Today's daily challenge (optional `?date=YYYY-MM-DD`) |
| GET | `/api/kids/challenges/<id>` | Single challenge |
| POST | `/api/kids/challenges/<id>/complete` | Submit answer |
| GET | `/api/kids/results/<member_id>` | Member's challenge results |
| GET | `/api/kids/teams` | List teams with members |
| GET | `/api/kids/teams/<team_id>` | Single team |
| GET | `/api/kids/teams/rankings` | Team leaderboard |
| GET | `/api/kids/members/rankings` | Individual leaderboard |
| POST | `/api/kids/teams/<team_id>/members` | Add team member |
| POST | `/api/kids/profile` | Create / update profile |
| GET | `/api/kids/profile/<member_id>` | Get profile |
| PUT | `/api/kids/profile/<member_id>` | Update profile |
| GET | `/api/kids/profile/<member_id>/stats` | Points, streak, accuracy |

### User Tracking API

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/tracking/event` | Log an event |
| GET | `/api/tracking/events` | Query events (optional `?user_type=&user_id=&event_type=&limit=`) |

**Event payload:**
```json
{
  "user_type": "student",
  "user_id": "student-1",
  "event_type": "lesson_started",
  "event_data": { "lesson_id": "lesson-3" },
  "session_id": "abc-123"
}
```

---

## Project Layout

```
backend/
├── app.py              # Flask application factory
├── config.py           # Paths and settings
├── database.py         # SQLite connection lifecycle
├── schema.sql          # Full database schema
├── models.py           # Query functions (all entities)
├── validators.py       # ID-format regex validators
├── lesson_loader.py    # Reads lesson JSON from teacher_dashboard
├── seed_db.py          # Populate DB with default data
├── requirements.txt
└── routes/
    ├── dashboard.py    # Teacher dashboard HTML pages
    ├── api.py          # Teacher / admin REST API
    ├── api_kids.py     # Kids learning app REST API
    └── api_tracking.py # Analytics event logging
```

The teacher-dashboard **templates** and **lesson-content JSON** files are read from `../teacher_dashboard_python/` so both projects share the same curriculum data.
