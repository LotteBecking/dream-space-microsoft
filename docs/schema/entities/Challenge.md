# Challenge

**App:** Kids App
**ID format:** `challenge-{N}` (e.g. `challenge-1`)
**Storage:** SQLite (`CHALLENGES`)

## Fields

| Field | Type | Notes |
|-------|------|-------|
| `challenge_id` | TEXT PK | Format: `challenge-{N}` |
| `title` | TEXT | |
| `description` | TEXT | |
| `difficulty` | TEXT | `Easy` / `Medium` / `Hard` |
| `category` | TEXT | e.g. `"Algorithms"`, `"Patterns"`, `"Ethics"` |
| `points` | INTEGER | Points awarded for correct answer |
| `question` | TEXT | The question shown to the student |
| `options` | TEXT | JSON array string: `["A","B","C","D"]` |
| `correct_answer` | INTEGER | 0-based index into `options` |
| `explanation` | TEXT | Shown after answering |
| `age_group` | TEXT | e.g. `"8-12"`, `"12-15"`, `"15-18"` |

## Relationships

- `CHALLENGE_RESULTS` — result records per [[Team]] member (via [[User Profile]])

## Notes

- `options` is stored as a raw JSON string in SQLite — parse with `json.loads()` before use
- `correct_answer` is **0-indexed** (i.e. `0` = first option, `3` = fourth option)
- Challenges are distinct from `studentChallenges` in lesson JSON — those are open-ended written tasks, these are multiple-choice daily quizzes
- The kids webapp fetches challenges from `/api/kids/challenges` (external backend API), not from this SQLite table directly

## API Response Shape

```json
{
  "id": "challenge-1",
  "title": "string",
  "description": "string",
  "difficulty": "Easy",
  "category": "Algorithms",
  "points": 10,
  "question": "string",
  "options": ["A", "B", "C", "D"],
  "correctAnswer": 0,
  "explanation": "string",
  "ageGroup": "8-12"
}
```
