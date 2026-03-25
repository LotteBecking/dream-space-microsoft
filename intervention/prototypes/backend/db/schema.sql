-- DreamSpace Backend Schema
-- All IDs follow the project-wide naming convention:
--   student-N, class-N, lesson-N, exercise-N-N, assign-N, ach-N, act-N

PRAGMA foreign_keys = ON;

-- ────────────────────────────────────────────
-- Teacher dashboard tables
-- ────────────────────────────────────────────

CREATE TABLE IF NOT EXISTS teacher_profiles (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    name            TEXT    NOT NULL,
    email           TEXT,
    school          TEXT,
    avatar          TEXT,
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS classes (
    class_id            TEXT    PRIMARY KEY,
    name                TEXT    NOT NULL,
    student_count       INTEGER DEFAULT 0,
    active_assignments  INTEGER DEFAULT 0,
    engagement_rate     INTEGER DEFAULT 0,
    created_at          TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS students (
    student_id          TEXT    PRIMARY KEY,
    name                TEXT    NOT NULL,
    avatar              TEXT,
    class_id            TEXT    REFERENCES classes(class_id),
    progress_percentage INTEGER DEFAULT 0,
    challenges_completed INTEGER DEFAULT 0,
    lessons_completed   INTEGER DEFAULT 0,
    last_activity       TEXT,
    teacher_notes       TEXT    DEFAULT '',
    created_at          TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at          TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS achievements (
    achievement_id  TEXT PRIMARY KEY,
    name            TEXT NOT NULL,
    icon            TEXT,
    description     TEXT
);

CREATE TABLE IF NOT EXISTS student_achievements (
    student_id      TEXT NOT NULL REFERENCES students(student_id),
    achievement_id  TEXT NOT NULL REFERENCES achievements(achievement_id),
    earned_date     TEXT,
    PRIMARY KEY (student_id, achievement_id)
);

CREATE TABLE IF NOT EXISTS activity_log (
    activity_id     TEXT PRIMARY KEY,
    student_id      TEXT NOT NULL REFERENCES students(student_id),
    activity_type   TEXT NOT NULL,
    title           TEXT,
    activity_date   TEXT,
    success         INTEGER DEFAULT 0,
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS lessons (
    lesson_id   TEXT PRIMARY KEY,
    title       TEXT NOT NULL,
    description TEXT,
    duration    INTEGER,
    level       TEXT,
    video_url   TEXT,
    published   INTEGER DEFAULT 1,
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS exercises (
    exercise_id     TEXT PRIMARY KEY,
    lesson_id       TEXT NOT NULL REFERENCES lessons(lesson_id),
    title           TEXT NOT NULL,
    description     TEXT,
    difficulty      TEXT,
    exercise_type   TEXT DEFAULT 'Coding',
    sort_order      INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS assignments (
    assignment_id   TEXT PRIMARY KEY,
    lesson_id       TEXT NOT NULL REFERENCES lessons(lesson_id),
    class_id        TEXT NOT NULL REFERENCES classes(class_id),
    assigned_date   TEXT,
    due_date        TEXT,
    completion_rate INTEGER DEFAULT 0,
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS last_viewed_lessons (
    teacher_id  INTEGER NOT NULL REFERENCES teacher_profiles(id),
    lesson_id   TEXT    NOT NULL REFERENCES lessons(lesson_id),
    viewed_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (teacher_id)
);

-- ────────────────────────────────────────────
-- Kids-app tables (challenges / teams)
-- ────────────────────────────────────────────

CREATE TABLE IF NOT EXISTS teams (
    team_id       TEXT    PRIMARY KEY,
    name          TEXT    NOT NULL,
    total_points  INTEGER DEFAULT 0,
    created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS team_members (
    member_id   TEXT PRIMARY KEY,
    team_id     TEXT NOT NULL REFERENCES teams(team_id),
    name        TEXT NOT NULL,
    avatar      TEXT,
    points      INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS user_profiles (
    member_id   TEXT PRIMARY KEY,
    name        TEXT NOT NULL,
    age         INTEGER,
    team_id     TEXT REFERENCES teams(team_id),
    avatar      TEXT,
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS challenges (
    challenge_id    TEXT    PRIMARY KEY,
    title           TEXT    NOT NULL,
    description     TEXT,
    difficulty      TEXT    NOT NULL,
    category        TEXT,
    points          INTEGER DEFAULT 0,
    question        TEXT,
    options         TEXT,           -- JSON array stored as TEXT
    correct_answer  INTEGER,
    explanation     TEXT,
    age_group       TEXT
);

CREATE TABLE IF NOT EXISTS challenge_results (
    id              TEXT PRIMARY KEY,
    member_id       TEXT NOT NULL REFERENCES user_profiles(member_id),
    challenge_id    TEXT NOT NULL REFERENCES challenges(challenge_id),
    completed       INTEGER DEFAULT 0,
    correct         INTEGER DEFAULT 0,
    points          INTEGER DEFAULT 0,
    completed_date  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ────────────────────────────────────────────
-- User tracking / analytics
-- ────────────────────────────────────────────

CREATE TABLE IF NOT EXISTS user_tracking (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    user_type   TEXT NOT NULL,       -- 'student' | 'teacher'
    user_id     TEXT NOT NULL,
    event_type  TEXT NOT NULL,
    event_data  TEXT,                -- JSON stored as TEXT
    session_id  TEXT,
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ────────────────────────────────────────────
-- Authentication & progress tables
-- ────────────────────────────────────────────

CREATE TABLE IF NOT EXISTS accounts (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    email           TEXT    NOT NULL UNIQUE,
    password_hash   TEXT    NOT NULL,
    role            TEXT    NOT NULL DEFAULT 'student',   -- 'student' | 'teacher'
    display_name    TEXT,
    student_id      TEXT    REFERENCES students(student_id),
    teacher_id      INTEGER REFERENCES teacher_profiles(id),
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS auth_sessions (
    token       TEXT    PRIMARY KEY,
    account_id  INTEGER NOT NULL REFERENCES accounts(id),
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at  TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS class_codes (
    code        TEXT    PRIMARY KEY,
    class_id    TEXT    NOT NULL REFERENCES classes(class_id),
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS exercise_attempts (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id      TEXT    NOT NULL REFERENCES students(student_id),
    exercise_id     TEXT    NOT NULL REFERENCES exercises(exercise_id),
    lesson_id       TEXT    NOT NULL REFERENCES lessons(lesson_id),
    score           INTEGER DEFAULT 0,
    completed       INTEGER DEFAULT 0,
    time_spent_sec  INTEGER DEFAULT 0,
    attempt_data    TEXT,                -- JSON stored as TEXT
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ────────────────────────────────────────────
-- Indexes
-- ────────────────────────────────────────────

CREATE INDEX IF NOT EXISTS idx_students_class       ON students(class_id);
CREATE INDEX IF NOT EXISTS idx_stu_ach_student       ON student_achievements(student_id);
CREATE INDEX IF NOT EXISTS idx_activity_student      ON activity_log(student_id);
CREATE INDEX IF NOT EXISTS idx_exercises_lesson      ON exercises(lesson_id);
CREATE INDEX IF NOT EXISTS idx_assignments_class     ON assignments(class_id);
CREATE INDEX IF NOT EXISTS idx_assignments_lesson    ON assignments(lesson_id);
CREATE INDEX IF NOT EXISTS idx_team_members_team     ON team_members(team_id);
CREATE INDEX IF NOT EXISTS idx_challenge_res_member  ON challenge_results(member_id);
CREATE INDEX IF NOT EXISTS idx_tracking_user         ON user_tracking(user_type, user_id);
CREATE INDEX IF NOT EXISTS idx_tracking_event        ON user_tracking(event_type);
CREATE INDEX IF NOT EXISTS idx_tracking_session      ON user_tracking(session_id);

CREATE INDEX IF NOT EXISTS idx_accounts_email       ON accounts(email);
CREATE INDEX IF NOT EXISTS idx_accounts_student      ON accounts(student_id);
CREATE INDEX IF NOT EXISTS idx_accounts_teacher      ON accounts(teacher_id);
CREATE INDEX IF NOT EXISTS idx_auth_sessions_account ON auth_sessions(account_id);
CREATE INDEX IF NOT EXISTS idx_auth_sessions_expires ON auth_sessions(expires_at);
CREATE INDEX IF NOT EXISTS idx_class_codes_class     ON class_codes(class_id);
CREATE INDEX IF NOT EXISTS idx_attempts_student      ON exercise_attempts(student_id);
CREATE INDEX IF NOT EXISTS idx_attempts_exercise     ON exercise_attempts(exercise_id);
CREATE INDEX IF NOT EXISTS idx_attempts_lesson       ON exercise_attempts(lesson_id);
CREATE INDEX IF NOT EXISTS idx_attempts_created      ON exercise_attempts(created_at);
