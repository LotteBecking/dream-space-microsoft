# Exercise

**App:** Both apps
**ID format:** `exercise-{N}-{M}` (e.g. `exercise-1-1`, `exercise-3-2`)
**Storage:** JSON (inside [[LessonContent]] files) + SQLite (`EXERCISES`)

## SQLite Fields

| Field | Type | Notes |
|-------|------|-------|
| `exercise_id` | TEXT PK | Format: `exercise-{lessonN}-{exerciseM}` |
| `lesson_id` | TEXT FK → [[Lesson]] | |
| `title` | TEXT | |
| `description` | TEXT | |
| `difficulty` | TEXT | `Easy` / `Medium` / `Hard` |
| `exercise_type` | TEXT | See types below |
| `sort_order` | INTEGER | Display order within lesson |

## Exercise Types

| Type | Description | Extra JSON fields |
|------|-------------|-------------------|
| `Written` | Student types numbered algorithm steps | — |
| `Sorting` | Drag-and-drop sequence ordering | `sortableItems[]` |
| `Extension` | Sectioned free-text for fast finishers | `sections[]` |
| `Challenge` | Student challenges (harder, in-lesson) | — |
| `Coding` | Code writing exercise (future) | — |

## JSON Schema (inside lesson file)

```json
{
  "id": "exercise-1-1",
  "title": "string",
  "description": "string",
  "type": "Written | Sorting | Extension",
  "difficulty": "Easy | Medium | Hard",
  "durationMinutes": 10,
  "displayMode": "string",
  "materials": ["Webapp"],
  "instructions": ["string"],
  "successCriteria": ["string"],

  "sortableItems": [
    { "id": "tea-1", "text": "string", "position": 1 }
  ],

  "sections": [
    { "id": "basic", "label": "string", "placeholder": "string" }
  ]
}
```

## Relationships

- [[Lesson]] — belongs to one lesson (3–4 exercises per lesson)
- `EXERCISE_ATTEMPTS` — [[Student]] attempt records with score + timing

## Notes

- `sortableItems` only present on `type: "Sorting"` exercises (e.g. exercise-1-2)
- `sections` only present on `type: "Extension"` exercises (e.g. exercise-1-3)
- Interactive widgets in the kids webapp are driven by `ex.type` — see `detail.html` template
- Student work is saved to localStorage (keys: `ds-ex-<id>-steps`, `ds-ex-<id>-order`, etc.)
