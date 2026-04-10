# Kids App API

**Base:** `http://localhost:5001/api/`
**App:** `intervention/kids_web_app/`

See [[ERD-KidsApp]] for the underlying tables.

---

## Challenges

### `GET /api/kids/challenges`
Returns today's challenges for the student's age group. Fetched from external backend.

```json
[
  {
    "id": "challenge-1",
    "title": "string",
    "description": "string",
    "difficulty": "Easy | Medium | Hard",
    "category": "string",
    "points": 10,
    "question": "string",
    "options": ["Option A", "Option B", "Option C", "Option D"],
    "correctAnswer": 0,
    "explanation": "string",
    "ageGroup": "8-12"
  }
]
```

### `POST /challenges/<challenge_id>/complete`
Submit an answer. Returns feedback inline (redirect with flash).

Request body (form):
```
answer = 0  (0-based index)
```

---

## Teams

### `GET /api/kids/teams`
Returns team leaderboard.

```json
[
  {
    "id": "team-1",
    "name": "string",
    "totalPoints": 340,
    "members": [
      { "id": "member-1", "name": "string", "avatar": "string", "points": 120 }
    ]
  }
]
```

---

## User Profile

### `GET /api/kids/profile`
Returns the current student's profile.

```json
{
  "memberId": "member-1",
  "name": "string",
  "age": 11,
  "teamId": "team-1",
  "avatar": "string"
}
```

### `GET /api/kids/stats`
Returns the current student's challenge stats.

```json
{
  "totalPoints": 240,
  "completed": 18,
  "correct": 15,
  "accuracy": 83,
  "streak": 4
}
```

---

## Lessons (kids app)

### `GET /lessons`
Lesson grid — all 16 lessons with completion status (from Flask session).

### `GET /lessons/<lesson_id>`
Full lesson detail — renders exercises and challenges from [[LessonContent]] JSON.

### `POST /lessons/<lesson_id>/complete`
Mark lesson as complete (stores `lesson_id` in Flask session `completed_lessons`).

---

## News

### `GET /api/news`
Returns tech news items for the dashboard carousel.

```json
[
  {
    "title": "string",
    "summary": "string",
    "imageUrl": "string",
    "url": "string",
    "publishedAt": "2026-04-07"
  }
]
```
Falls back to sample data if the external news service is offline.

---

## Progress

### `POST /api/progress/attempt`
Record a student exercise attempt.

Request body:
```json
{
  "exerciseId": "exercise-1-1",
  "lessonId": "lesson-1",
  "score": 85,
  "completed": true,
  "timeSpentSec": 300,
  "attemptData": {}
}
```

---

## Notes

- Lesson completion is stored in the **Flask session** (`completed_lessons` list), not a database call per request
- Challenge answer submission uses a **form POST + redirect** pattern, not JSON
- The news carousel uses `carousel.js` — falls back to sample data when offline (`api.is_offline()`)
- `attemptData` in exercise attempts is an open JSON object — content varies by exercise type
