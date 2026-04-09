# Class

**App:** Teacher Dashboard
**ID format:** `class-{N}` (e.g. `class-1`)
**Storage:** SQLite (`CLASSES`) + `data/store/classes.json`

## Fields

| Field | Type | Notes |
|-------|------|-------|
| `class_id` | TEXT PK | Format: `class-{N}` |
| `name` | TEXT | Display name (e.g. "6B", "Groep 7") |
| `student_count` | INTEGER | Cached count of enrolled students |
| `active_assignments` | INTEGER | Count of open assignments |
| `engagement_rate` | INTEGER | 0–100 percentage |
| `created_at` | TIMESTAMP | |

## Relationships

- [[Student]] — a class has many students
- [[Assignment]] — a class has many assignments
- `CLASS_CODES` — a class has one or more join codes for student enrolment

## JSON Store

```
data/store/classes.json
```
```json
[
  {
    "id": "class-1",
    "name": "string",
    "studentCount": 25,
    "activeAssignments": 2,
    "engagementRate": 78,
    "students": ["student-1", "student-2", "..."]
  }
]
```

## Notes

- `student_count` and `engagement_rate` are denormalised/cached — may be recalculated
- Join codes (`CLASS_CODES`) let students self-enrol
