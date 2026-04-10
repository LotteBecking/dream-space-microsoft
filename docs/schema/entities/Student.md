# Student

**App:** Teacher Dashboard + Kids App (shared record)
**ID format:** `student-{N}` (e.g. `student-5`)
**Storage:** SQLite (`STUDENTS`) + `data/store/students.json`

## Fields

| Field | Type | Notes |
|-------|------|-------|
| `student_id` | TEXT PK | Format: `student-{N}` |
| `name` | TEXT | Display name |
| `avatar` | TEXT | Avatar initials or identifier |
| `class_id` | TEXT FK → [[Class]] | |
| `progress_percentage` | INTEGER | 0–100, overall progress |
| `challenges_completed` | INTEGER | Cumulative count |
| `lessons_completed` | INTEGER | Cumulative count |
| `last_activity` | TEXT | ISO timestamp of last action |
| `teacher_notes` | TEXT | Free-text notes from teacher |
| `created_at` | TIMESTAMP | |
| `updated_at` | TIMESTAMP | |

## Relationships

- [[Class]] — belongs to one class
- [[Account]] — has one login account (role = `"student"`)
- `STUDENT_ACHIEVEMENTS` — junction table to [[Achievement]] records
- `ACTIVITY_LOG` — timestamped history of lesson/challenge activity
- `EXERCISE_ATTEMPTS` — attempt records linking to [[Exercise]] and [[Lesson]]

## JSON Store

```
data/store/students.json
```
```json
[
  {
    "id": "student-1",
    "name": "string",
    "avatar": "string",
    "classId": "class-1",
    "progressPercentage": 60,
    "challengesCompleted": 12,
    "lessonsCompleted": 4,
    "lastActivity": "2026-04-07T10:30:00",
    "teacherNotes": "string",
    "achievements": [
      { "id": "ach-1", "name": "string", "icon": "🏆", "earnedDate": "2026-03-01" }
    ],
    "activityHistory": [
      { "id": "act-1", "type": "lesson", "title": "string", "date": "2026-04-06", "success": true }
    ]
  }
]
```

## Notes

- `progress_percentage` is computed/cached — not calculated live from attempts
- `teacher_notes` is visible only in teacher dashboard, not to the student
- `activity_history` is embedded in the JSON store but normalised into `ACTIVITY_LOG` in SQLite
