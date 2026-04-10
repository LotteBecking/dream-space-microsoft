# Teacher

**App:** Teacher Dashboard
**Storage:** SQLite (`TEACHER_PROFILES`) + `data/store/teacher_profile.json`

## Fields

| Field | Type | Notes |
|-------|------|-------|
| `id` | INTEGER PK | Auto-increment |
| `name` | TEXT | Full name |
| `email` | TEXT | Login email |
| `school` | TEXT | School name |
| `avatar` | TEXT | 2–4 char initials used for display |
| `created_at` | TIMESTAMP | |
| `updated_at` | TIMESTAMP | |

## Relationships

- [[Account]] — a teacher has one or more accounts (role = `"teacher"`)
- [[Class]] — a teacher manages multiple classes (via assignments and dashboard)
- [[Lesson]] — tracks last viewed lesson via `LAST_VIEWED_LESSONS`

## JSON Store

The teacher dashboard also persists profile data locally at:
```
data/store/teacher_profile.json
```
```json
{
  "name": "string",
  "email": "string",
  "school": "string",
  "avatar": "string (2-4 chars)"
}
```

## Notes

- Avatar is initials (e.g. `"JL"`, `"KZE"`) — used in the dashboard header
- The teacher record is referenced by `LAST_VIEWED_LESSONS` with `teacher_id` (int FK)
