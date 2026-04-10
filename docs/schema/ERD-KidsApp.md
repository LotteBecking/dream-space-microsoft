# ERD — Kids App

> Student-facing tables only. See [[ERD-Full]] for the complete schema, [[ERD-TeacherDashboard]] for the teacher side.

```mermaid
erDiagram

    TEAMS {
        text team_id PK
        text name
        int total_points
        timestamp created_at
    }

    TEAM_MEMBERS {
        text member_id PK
        text team_id FK
        text name
        text avatar
        int points
    }

    USER_PROFILES {
        text member_id PK
        text name
        int age
        text team_id FK
        text avatar
        timestamp created_at
    }

    CHALLENGES {
        text challenge_id PK
        text title
        text description
        text difficulty
        text category
        int points
        text question
        text options
        int correct_answer
        text explanation
        text age_group
    }

    CHALLENGE_RESULTS {
        text id PK
        text member_id FK
        text challenge_id FK
        int completed
        int correct
        int points
        timestamp completed_date
    }

    ACCOUNTS {
        int id PK
        text email
        text role
        text display_name
        text student_id FK
    }

    AUTH_SESSIONS {
        text token PK
        int account_id FK
        timestamp expires_at
    }

    TEAMS ||--o{ TEAM_MEMBERS : "has members"
    TEAMS ||--o{ USER_PROFILES : "has profiles"

    USER_PROFILES }o--|| TEAMS : "in team"
    USER_PROFILES ||--o{ CHALLENGE_RESULTS : "has results"

    CHALLENGES ||--o{ CHALLENGE_RESULTS : "answered in"

    ACCOUNTS ||--o{ AUTH_SESSIONS : "has sessions"
```

---

## Notes

- `CHALLENGES.options` is stored as a JSON array string (e.g. `["Option A", "Option B", "Option C", "Option D"]`)
- `CHALLENGES.correct_answer` is a 0-based index into the `options` array
- `USER_PROFILES` and `TEAM_MEMBERS` share the same `member_id` — effectively 1:1
- Lesson completion in the kids app is tracked via Flask session (not persisted to DB directly)
