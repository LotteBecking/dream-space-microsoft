# Teacher Dashboard JSON Storage Files

**Location:** `intervention/prototypes/teacher_dashboard_python/data/store/`

These files are the teacher dashboard's local persistence layer — read/written by `data/teacher_storage.py`.

See [[Teacher]], [[Class]], [[Student]] for the SQLite schema counterparts.

---

## `teacher_profile.json`

```json
{
  "name": "string",
  "email": "string",
  "school": "string",
  "avatar": "string (2-4 char initials)"
}
```

---

## `classes.json`

```json
[
  {
    "id": "class-1",
    "name": "string",
    "studentCount": 25,
    "activeAssignments": 2,
    "engagementRate": 78,
    "students": ["student-1", "student-2"]
  }
]
```

---

## `students.json`

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
      {
        "id": "ach-1",
        "name": "string",
        "icon": "🏆",
        "earnedDate": "2026-03-01"
      }
    ],
    "activityHistory": [
      {
        "id": "act-1",
        "type": "lesson | challenge",
        "title": "string",
        "date": "2026-04-06",
        "success": true
      }
    ]
  }
]
```

---

## `assignments.json`

```json
[
  {
    "id": "assign-1",
    "lessonId": "lesson-1",
    "classId": "class-1",
    "assignedDate": "2026-04-01",
    "dueDate": "2026-04-10",
    "completionRate": 64
  }
]
```

---

## `users.json`

Legacy authentication store (teacher login only):

```json
{
  "teacher@school.nl": {
    "username": "string",
    "email": "string",
    "school": "string",
    "class": "string",
    "password_hash": "sha256 hex string",
    "created_at": "2026-01-01T00:00:00"
  }
}
```

Key is `email.lower()`.

---

## `last_lesson.txt`

Plain text — contains the ID of the last lesson the teacher viewed:

```
lesson-4
```

---

## Notes

- All these files are read and written by `data/teacher_storage.py`
- There is intentional overlap between this JSON store and the SQLite `TEACHER_PROFILES`, `CLASSES`, `STUDENTS` tables — the JSON store was the original implementation, SQLite was added later
- The `users.json` auth store is separate from the SQLite `ACCOUNTS` table used by the kids app
