# DreamSpace Database Schema

## Entity Relationship Diagram

```mermaid
erDiagram
    CLASS {
        string class_id PK "^class-[0-9]+$"
        string name
        int student_count
        int active_assignments
        int engagement_rate
    }

    STUDENT {
        string student_id PK "^student-[0-9]+$"
        string name
        string avatar
        string class_id FK
        int progress_percentage
        int challenges_completed
        int lessons_completed
        string last_activity
        string teacher_notes
    }

    LESSON {
        string lesson_id PK "^lesson-[0-9]+$"
        string title
        string description
        int duration
        string level
        string video_url
    }

    EXERCISE {
        string exercise_id PK "^exercise-[0-9]+-[0-9]+$"
        string lesson_id FK
        string title
        string description
        string difficulty
        string exercise_type
        int sort_order
    }

    ASSIGNMENT {
        string assignment_id PK "^assign-[0-9]+$"
        string lesson_id FK
        string class_id FK
        string assigned_date
        string due_date
        int completion_rate
    }

    ACHIEVEMENT {
        string achievement_id PK "^ach-[0-9]+$"
        string name
        string icon
        string description
    }

    ACTIVITY_ENTRY {
        string activity_id PK "^act-[0-9]+$"
        string student_id FK
        string activity_type
        string title
        string activity_date
        int success
    }

    STUDENT_ACHIEVEMENT {
        string student_id FK
        string achievement_id FK
        string earned_date
    }

    CLASS ||--o{ STUDENT : "has"
    LESSON ||--o{ EXERCISE : "contains"
    LESSON ||--o{ ASSIGNMENT : "assigned via"
    CLASS ||--o{ ASSIGNMENT : "receives"
    STUDENT ||--o{ ACTIVITY_ENTRY : "logs"
    STUDENT ||--o{ STUDENT_ACHIEVEMENT : "earns"
    ACHIEVEMENT ||--o{ STUDENT_ACHIEVEMENT : "awarded in"
```

## ID Patterns

| Entity | Example | Regex |
|--------|---------|-------|
| student | `student-1` | `^student-[0-9]+$` |
| class | `class-1` | `^class-[0-9]+$` |
| lesson | `lesson-1` | `^lesson-[0-9]+$` |
| exercise | `exercise-1-1` | `^exercise-[0-9]+-[0-9]+$` |
| assignment | `assign-1` | `^assign-[0-9]+$` |
| achievement | `ach-1` | `^ach-[0-9]+$` |
| activity entry | `act-1` | `^act-[0-9]+$` |
