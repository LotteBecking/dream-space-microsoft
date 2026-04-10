# Account

**App:** Both apps (authentication layer)
**Storage:** SQLite (`ACCOUNTS`, `AUTH_SESSIONS`)

## ACCOUNTS Fields

| Field | Type | Notes |
|-------|------|-------|
| `id` | INTEGER PK | Auto-increment |
| `email` | TEXT UNIQUE | Login email |
| `password_hash` | TEXT | SHA-256 hex hash |
| `role` | TEXT | `"student"` or `"teacher"` |
| `display_name` | TEXT | Name shown in UI |
| `student_id` | TEXT FK → [[Student]] | Null if role = teacher |
| `teacher_id` | INTEGER FK → [[Teacher]] | Null if role = student |
| `created_at` | TIMESTAMP | |

## AUTH_SESSIONS Fields

| Field | Type | Notes |
|-------|------|-------|
| `token` | TEXT PK | Unique session token |
| `account_id` | INTEGER FK → Account | |
| `created_at` | TIMESTAMP | |
| `expires_at` | TIMESTAMP | Session expiry |

## Relationships

- [[Student]] — a student account links to one student record
- [[Teacher]] — a teacher account links to one teacher profile
- `AUTH_SESSIONS` — an account can have many active sessions

## Teacher Dashboard Auth (separate)

The teacher dashboard also has a legacy JSON-based auth store:
```
data/store/users.json
```
```json
{
  "teacher@school.nl": {
    "username": "string",
    "email": "string",
    "school": "string",
    "class": "string",
    "password_hash": "sha256 hex",
    "created_at": "2026-01-01T00:00:00"
  }
}
```

## Notes

- Password is hashed with SHA-256 (not bcrypt) — consider upgrading for production
- Two separate auth systems exist: SQLite `ACCOUNTS` (kids app) and JSON `users.json` (teacher dashboard legacy)
- Session tokens are stored server-side in `AUTH_SESSIONS`, not just in the cookie
