# Teacher Dashboard API

**Base:** `http://localhost:5002/api/`
**App:** `intervention/prototypes/teacher_dashboard_python/app.py`

See [[TeacherDashboard ERD|ERD-TeacherDashboard]] for the underlying tables.

---

## Classes

### `GET /api/classes`
Returns all classes.

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

## Students

### `GET /api/students`
Returns all students.

### `GET /api/students/<student_id>`
Returns one student with full detail.

```json
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
    { "id": "ach-1", "name": "string", "icon": "🏆", "earnedDate": "2026-03-01" }
  ],
  "activityHistory": [
    { "id": "act-1", "type": "lesson", "title": "string", "date": "2026-04-06", "success": true }
  ]
}
```

### `PATCH /api/students/<student_id>`
Update teacher notes or other mutable fields.

---

## Lessons

### `GET /api/lessons`
Returns lesson list (lightweight — no slides/exercises).

```json
[
  { "id": "lesson-1", "title": "string", "description": "string", "duration": 60, "level": "Beginner" }
]
```

### `GET /api/lessons/<lesson_id>`
Returns full lesson JSON (same structure as [[LessonContent]] file).

### `POST /api/lessons/<lesson_id>/last-viewed`
Marks lesson as last viewed by the current teacher.

---

## Assignments

### `GET /api/assignments`
Returns all assignments.

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

### `POST /api/assignments`
Create a new assignment.

### `DELETE /api/assignments/<assignment_id>`
Remove an assignment.

---

## Teacher Profile

### `GET /api/profile`
Returns teacher profile.

```json
{ "name": "string", "email": "string", "school": "string", "avatar": "JL" }
```

### `PUT /api/profile`
Update teacher profile.

---

## Progress

### `GET /api/progress/class/<class_id>`
Class-level progress summary.

```json
{
  "classId": "class-1",
  "students": [
    {
      "studentId": "student-1",
      "name": "string",
      "avatar": "string",
      "progressPercentage": 60,
      "lessonsCompleted": 4,
      "exercisesCompleted": 12,
      "totalAttempts": 20,
      "avgScore": 78.5,
      "totalTimeSec": 3600,
      "lastActivity": "2026-04-06"
    }
  ]
}
```

### `GET /api/progress/student/<student_id>`
Per-student exercise attempt history.

```json
{
  "studentId": "student-1",
  "lessons": [
    {
      "lessonId": "lesson-1",
      "exercises": [
        {
          "exerciseId": "exercise-1-1",
          "bestScore": 90,
          "attempts": 2,
          "completed": true,
          "totalTimeSec": 480,
          "lastAttempt": "2026-04-05T09:30:00"
        }
      ]
    }
  ]
}
```
