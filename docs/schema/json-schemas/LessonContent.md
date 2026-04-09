# Lesson Content JSON Schema

**Files:** `intervention/prototypes/teacher_dashboard_python/data/lesson_content/lesson-{N}.json`
**Count:** 16 files (lesson-1 through lesson-16)
**Index:** `manifest.json` in the same folder

See [[Lesson]] and [[Exercise]] for the SQLite counterparts.

---

## Top-Level Structure

```json
{
  "id": "lesson-1",
  "title": "string",
  "description": "string",
  "duration": 60,
  "level": "Beginner | Intermediate | Advanced",
  "ageGroup": "Groep 5-8 (ages 8-12)",
  "imageUrl": "/static/images/lesson-1-placeholder.svg",

  "roleModelOfDay": { ... },
  "vocabulary": [ ... ],
  "learningObjectives": [ "string" ],
  "prerequisites": "string",
  "materials": [ "string" ],
  "fullDescription": "string",
  "teacherInstructions": { ... },
  "curriculumAlignment": [ "string" ],
  "teacherGuide": "string",

  "studentExercises": [ ... ],
  "studentChallenges": [ ... ],
  "lessonSlides": [ ... ]
}
```

---

## `roleModelOfDay`

```json
{
  "name": "Ada Lovelace",
  "years": "1815–1852",
  "intro": "string — one sentence bio"
}
```

---

## `vocabulary[]`

```json
[
  { "word": "Algorithm", "def": "A set of step-by-step instructions" }
]
```

---

## `teacherInstructions`

```json
{
  "setup": "string — what to prepare before class",
  "steps": [
    "Phase 1 (0-3 min): string",
    "Phase 2 (3-10 min): string"
  ],
  "discussionPrompts": [ "string" ],
  "tips": [ "string" ]
}
```

---

## `studentExercises[]`

Base fields (all types):

```json
{
  "id": "exercise-1-1",
  "title": "string",
  "description": "string",
  "type": "Written | Sorting | Extension",
  "difficulty": "Easy | Medium | Hard",
  "durationMinutes": 10,
  "displayMode": "Individual then pairs",
  "materials": ["Webapp"],
  "instructions": [ "string" ],
  "successCriteria": [ "string" ]
}
```

**Extra field for `type: "Sorting"`:**

```json
"sortableItems": [
  { "id": "tea-1", "text": "Boil the water", "position": 1 }
]
```
Items are stored in **correct order** — the webapp JS shuffles them for the student.

**Extra field for `type: "Extension"`:**

```json
"sections": [
  {
    "id": "basic",
    "label": "Basic Algorithm",
    "placeholder": "Step by step — what does the robot do first?"
  },
  { "id": "allergy", "label": "Allergy Safety Rules", "placeholder": "..." },
  { "id": "missing", "label": "Missing Ingredient Rules", "placeholder": "..." }
]
```

---

## `studentChallenges[]`

Harder, open-ended tasks (different from the MC [[Challenge]] entity in the kids app):

```json
{
  "id": "challenge-1-1",
  "title": "string",
  "description": "string",
  "type": "Challenge",
  "difficulty": "Medium | Hard",
  "durationMinutes": 10,
  "displayMode": "Pairs or small groups",
  "materials": ["Webapp"],
  "instructions": [ "string" ],
  "successCriteria": [ "string" ]
}
```

---

## `lessonSlides[]`

16 slide objects per lesson, used by the teacher presentation view:

```json
{
  "id": "slide-1-1",
  "phase": "string",
  "time": "0-3 min",
  "title": "string",
  "colour": "#hex",
  "whatToSay": "string",
  "whatToDo": "string",
  "conversationStarter": "string"
}
```
Some slides include additional fields: `realWorldConnection`, `vocabularyFocus`, `exerciseInstructions`.

---

## `manifest.json`

```json
{
  "version": 1,
  "lessons": [
    {
      "id": "lesson-1",
      "title": "string",
      "level": "Beginner",
      "path": "lesson-1.json",
      "published": true
    }
  ]
}
```
