# DreamSpace Microsoft - Capstone Project CSSci

Last updated: 27 March 2026

## Project Snapshot

This repository supports the DreamSpace intervention work across:

1. Student app development.
2. Teacher dashboard development.
3. Lesson and exercise design.
4. Exploratory data analysis.

## Current Team Work Division Guide

Use this shared plan so everyone can work in parallel and still integrate smoothly.

### 1. Project Goal

1. Build a system where kids can join classes by signup, or teachers can register kids manually.
2. Connect that system to the teacher dashboard.
3. Design high-quality lessons for teachers and linked student exercises.
4. Implement playable exercises in the app and track progress back to the dashboard.

### 2. Team Split

1. Backend Team (2 people): auth, class enrollment, student records, API, database.
2. Lesson Design Team (3 people): lesson structure, teacher guide, exercise briefs, UX text/content.
3. Exercise Developer (1 person): builds exercise logic and app-side integration.


### 4. Backend Team (2 People) Instructions

1. Choose stack:
2. Python backend: Flask or FastAPI.
3. SQL database: PostgreSQL preferred, SQLite fine for prototype.
4. Design core tables:
5. users: id, role, name, email, password_hash, created_at.
6. teachers: user_id, school_name.
7. students: user_id, avatar, age_group.
8. classes: id, teacher_id, class_name, class_code, created_at.
9. class_enrollments: class_id, student_id, joined_at, method.
10. lessons: id, title, topic, difficulty.
11. exercise_attempts: id, student_id, lesson_id, exercise_id, score, completed_at.
12. Build core endpoints:
13. teacher creates class.
14. student joins class by class_code.
15. teacher adds student manually.
16. get class roster.
17. get student progress by class.
18. get lesson completion stats for dashboard.
19. Add auth basics:
20. signup and login for teacher/student roles.
21. secure passwords.
22. role-based endpoint checks.
23. Data validation:
24. prevent duplicate enrollment.
25. prevent non-teacher class creation.
26. prevent invalid class codes.
27. Integration output for other teammates:
28. API documentation with sample request/response.
29. seeded test database.
30. Postman collection or simple test script.

### 5. Lesson Design Team (3 People) Instructions

1. Create a lesson template used for every lesson:
2. lesson title, age range, duration, difficulty.
3. teacher overview.
4. classroom setup.
5. step-by-step guide.
6. discussion prompts.
7. assessment criteria.
8. linked exercises list.
9. Divide content roles:
10. Person A: learning goals + teacher guide quality.
11. Person B: student exercise flow + difficulty progression.
12. Person C: dashboard presentation text + consistency review.
13. For each lesson, produce:
14. teacher view content.
15. student exercise brief with expected inputs/outputs.
16. completion criteria and scoring rule.
17. Design handoff package:
18. one structured JSON or table per lesson.
19. clear IDs for lesson and exercises.
20. edge-case notes for developer.
21. Quality checklist:
22. age-appropriate language.
23. objective matches exercise.
24. realistic timing.
25. at least one extension activity for faster students.

### 6. Exercise Developer (1 Person) Instructions

1. Start from lesson briefs and implement one exercise engine pattern first.
2. Build exercise modules with consistent interface:
3. load exercise by id.
4. validate answer/action.
5. return score and completion status.
6. save attempt to backend.
7. Implement MVP progression:
8. 2 easy, 2 medium, 1 hard exercise first.
9. Add progress sync:
10. send completion to backend after each exercise.
11. support retry and attempt history.
12. Add UX requirements:
13. clear instructions.
14. immediate feedback.
15. success and error states.
16. Keep exercise IDs exactly matching lesson design IDs.
17. Deliverables:
18. working exercise screens.
19. API integration for save/fetch progress.
20. short test checklist for each exercise.

### 7. Integration Contracts (Must Agree Early)

1. ID format: lesson-1, exercise-1-1 style.
2. Status values: not_started, in_progress, completed.
3. Score scale: 0 to 100.
4. Enrollment method values: self_signup or teacher_added.
5. API error format: success false plus message.
6. Timestamp format: ISO 8601.

### 8. Definition of Done Per Team

1. Backend done when signup, class join, teacher-add-student, and dashboard progress endpoints work with tests.
2. Lessons done when each lesson has complete teacher guide and mapped exercises with measurable outcomes.
3. Exercise done when students can complete exercise, receive feedback, and progress appears in dashboard.

## Repository Orientation

### data-analysis

- For exploratory data research only.
- Booking data is not stored in this repository.
- Booking data is stored securely on OneDrive.

### intervention

- Most recent builds are under `intervention/prototypes/`.
- This includes the Swift Xcode app and the teacher dashboard prototypes.
- Older versions are under `intervention/old/`.

## Quick Start

### Running iOS Prototypes (Xcode)

1. Install Xcode and iOS Simulator.
2. Clone this repository.
3. Open Xcode and open an existing project from `intervention/prototypes/`.
4. Choose a simulator device.
5. Press Run.

### Running Teacher Dashboard (Python prototype)

1. Go to `intervention/prototypes/teacher_dashboard_python/`.
2. Create or activate a virtual environment.
3. Install dependencies from `requirements.txt`.
4. Run `python app.py`.

## Current Priorities

1. Design more exercises across multiple levels.
2. Improve app UX quality.
3. Keep lesson IDs, exercise IDs, and backend payloads consistent across streams.
