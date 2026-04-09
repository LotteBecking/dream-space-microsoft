# Lesson

**App:** Both apps
**ID format:** `lesson-{N}` (e.g. `lesson-1` through `lesson-16`)
**Storage:** JSON files (`data/lesson_content/lesson-{N}.json`) + SQLite (`LESSONS`) + manifest

## SQLite Fields

| Field | Type | Notes |
|-------|------|-------|
| `lesson_id` | TEXT PK | Format: `lesson-{N}` |
| `title` | TEXT | |
| `description` | TEXT | Short description |
| `duration` | INTEGER | Minutes |
| `level` | TEXT | `Beginner` / `Intermediate` / `Advanced` |
| `video_url` | TEXT | Optional supplementary video |
| `published` | INTEGER | Boolean: 1 = live, 0 = draft |
| `created_at` | TIMESTAMP | |

## Relationships

- [[Exercise]] — a lesson has 3–4 exercises
- [[Assignment]] — a lesson can be assigned to one or more [[Class]] groups
- `EXERCISE_ATTEMPTS` — attempt history from [[Student]] records
- `LAST_VIEWED_LESSONS` — tracks which lesson each [[Teacher]] last opened

## JSON File Structure

Full rich content lives in `lesson-{N}.json`. See [[LessonContent]] for the complete schema.

Key top-level fields:
```
id, title, description, duration, level, ageGroup, imageUrl,
roleModelOfDay, vocabulary[], learningObjectives[], prerequisites,
materials[], fullDescription, teacherInstructions{},
curriculumAlignment[], teacherGuide,
studentExercises[], studentChallenges[], lessonSlides[]
```

## 16 Lessons

| # | Title | Level |
|---|-------|-------|
| 1 | How Does a Computer Think? The PB&J Sandwich Lesson | Beginner |
| 2 | Don't Repeat Yourself — Loops and Efficiency | Beginner |
| 3 | If This, Then That — How Computers Make Decisions | Intermediate |
| 4 | Memory Boxes — How Computers Remember Things | Intermediate |
| 5 | Teaching the Machine — What AI Actually Is | Advanced |
| 6 | Secrets and Codes — How Computers Keep Information Safe | Intermediate |
| 7 | Build Something Real — Design Thinking and Your First Prototype | Advanced |
| 8 | Who Is Technology For? Ethics, Fairness, and Responsibility | Advanced |
| 9 | Why Does Your Phone Freeze? — Efficiency | Intermediate |
| 10 | How Do Computers Make Secure Decisions? — Cybersecurity | Intermediate |
| 11 | How Do Computers Handle Massive Data? — Climate Crisis | Intermediate |
| 12 | How Do Large Teams Build Software? — Black Boxes | Intermediate |
| 13 | How Do Systems Prioritise? — Queues, Stacks, Triage | Intermediate |
| 14 | How Do Computers Learn? — Training the Fraud Detector | Intermediate |
| 15 | Can Data Be Unfair? — Auditing Algorithms for Bias | Intermediate |
| 16 | How Do We Solve Real Problems? — The Tech for Good Pitch | Intermediate |

## Notes

- The manifest at `data/lesson_content/manifest.json` lists all lessons with `id`, `title`, `level`, `path`, `published`
- The kids webapp loads lessons at startup into `app.config["LESSONS_DATA"]` (dict keyed by lesson ID)
- Rich content (slides, exercises, role models) lives only in the JSON files, not SQLite
