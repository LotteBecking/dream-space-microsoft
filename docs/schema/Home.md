# Dream Space — Data Schema Overview

> Open this folder (`docs/schema/`) as an Obsidian vault. Use **Graph View** (Cmd+G) to see entity relationships. Mermaid diagrams render inline in the ERD notes.

---

## Two Apps, One Data Model

The project consists of two Flask apps sharing overlapping data:

| App | Path | Port | Purpose |
|-----|------|------|---------|
| **Kids Webapp** | `intervention/kids_web_app/` | 5001 | Students — lessons, challenges, teams |
| **Teacher Dashboard** | `intervention/prototypes/teacher_dashboard_python/` | 5002 | Teachers — classes, students, assignments |

---

## ERD Diagrams

- [[ERD-Full]] — All 20 tables in one diagram
- [[ERD-TeacherDashboard]] — Teacher-side tables only
- [[ERD-KidsApp]] — Kids app tables only

---

## Entities

### Teacher Dashboard

| Entity | ID Format | Storage | Note |
|--------|-----------|---------|------|
| [[Teacher]] | `teacher-{N}` (int) | SQLite + JSON | Teacher profile |
| [[Class]] | `class-{N}` | SQLite + JSON | Group of students |
| [[Student]] | `student-{N}` | SQLite + JSON | Individual student record |
| [[Lesson]] | `lesson-{N}` | JSON files | 16 lessons, file-based |
| [[Exercise]] | `exercise-{N}-{M}` | JSON + SQLite | 3–4 per lesson |

### Kids App

| Entity | ID Format | Storage | Note |
|--------|-----------|---------|------|
| [[Team]] | `team-{N}` | SQLite | Competitive group |
| [[Challenge]] | `challenge-{N}` | SQLite | Daily MC questions |
| [[Account]] | integer PK | SQLite | Auth, role: student/teacher |

---

## JSON Schemas

- [[LessonContent]] — Schema for `lesson-{N}.json` files
- [[StorageFiles]] — Teacher dashboard local JSON file store

---

## API Reference

- [[TeacherAPI]] — Teacher dashboard endpoints
- [[KidsAPI]] — Kids app endpoints

---

## ID Naming Conventions

| Entity | Format | Example |
|--------|--------|---------|
| Student | `student-{N}` | `student-5` |
| Class | `class-{N}` | `class-1` |
| Lesson | `lesson-{N}` | `lesson-1` through `lesson-16` |
| Exercise | `exercise-{N}-{M}` | `exercise-1-1` |
| Assignment | `assign-{N}` | `assign-3` |
| Achievement | `ach-{N}` | `ach-2` |
| Activity | `act-{N}` | `act-10` |
| Challenge | `challenge-{N}` | `challenge-4` |
| Team | `team-{N}` | `team-2` |

---

## Database

- **Engine:** SQLite
- **Tables:** 20 total
- **Foreign key constraints:** enabled
- **JSON columns:** `challenges.options`, `exercise_attempts.attempt_data`, `user_tracking.event_data`
