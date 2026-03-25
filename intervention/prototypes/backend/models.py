"""Query functions for every entity in the DreamSpace database.

All public helpers fetch the connection via ``get_db()`` so callers never
need to pass one.  Return values are plain dicts / lists of dicts whose
keys match the camelCase names the templates and the Swift client expect.
"""

import json
from datetime import datetime, timedelta

from database import get_db

# ─── generic helpers ────────────────────────────────────────────────

def _row(row):
    return dict(row) if row else None


def _rows(rows):
    return [dict(r) for r in rows]


# ═══════════════════════════════════════════════════════════════════
#  TEACHER PROFILES
# ═══════════════════════════════════════════════════════════════════

def get_teacher_profile(teacher_id=1):
    row = get_db().execute(
        'SELECT * FROM teacher_profiles WHERE id = ?', (teacher_id,)
    ).fetchone()
    return _row(row)


def save_teacher_profile(data, teacher_id=1):
    db = get_db()
    exists = db.execute(
        'SELECT 1 FROM teacher_profiles WHERE id = ?', (teacher_id,)
    ).fetchone()
    if exists:
        db.execute(
            '''UPDATE teacher_profiles
               SET name=?, email=?, school=?, avatar=?, updated_at=CURRENT_TIMESTAMP
               WHERE id=?''',
            (data.get('name'), data.get('email'),
             data.get('school'), data.get('avatar'), teacher_id))
    else:
        db.execute(
            'INSERT INTO teacher_profiles (name, email, school, avatar) VALUES (?,?,?,?)',
            (data.get('name'), data.get('email'),
             data.get('school'), data.get('avatar')))
    db.commit()


def get_last_lesson(teacher_id=1):
    row = get_db().execute(
        'SELECT lesson_id FROM last_viewed_lessons WHERE teacher_id = ?',
        (teacher_id,)
    ).fetchone()
    return row['lesson_id'] if row else None


def save_last_lesson(teacher_id, lesson_id):
    db = get_db()
    db.execute(
        '''INSERT INTO last_viewed_lessons (teacher_id, lesson_id, viewed_at)
           VALUES (?, ?, CURRENT_TIMESTAMP)
           ON CONFLICT(teacher_id)
           DO UPDATE SET lesson_id=excluded.lesson_id,
                         viewed_at=CURRENT_TIMESTAMP''',
        (teacher_id, lesson_id))
    db.commit()


# ═══════════════════════════════════════════════════════════════════
#  CLASSES
# ═══════════════════════════════════════════════════════════════════

def get_all_classes():
    db = get_db()
    rows = db.execute('SELECT * FROM classes ORDER BY class_id').fetchall()
    result = []
    for row in rows:
        c = _row(row)
        stu = db.execute(
            'SELECT student_id FROM students WHERE class_id = ?',
            (c['class_id'],)
        ).fetchall()
        result.append({
            'id': c['class_id'],
            'name': c['name'],
            'studentCount': c['student_count'],
            'activeAssignments': c['active_assignments'],
            'engagementRate': c['engagement_rate'],
            'students': [r['student_id'] for r in stu],
        })
    return result


def get_class(class_id):
    db = get_db()
    row = db.execute(
        'SELECT * FROM classes WHERE class_id = ?', (class_id,)
    ).fetchone()
    if not row:
        return None
    c = _row(row)
    stu = db.execute(
        'SELECT student_id FROM students WHERE class_id = ?',
        (class_id,)
    ).fetchall()
    return {
        'id': c['class_id'],
        'name': c['name'],
        'studentCount': c['student_count'],
        'activeAssignments': c['active_assignments'],
        'engagementRate': c['engagement_rate'],
        'students': [r['student_id'] for r in stu],
    }


def create_class(data):
    db = get_db()
    db.execute(
        '''INSERT INTO classes
           (class_id, name, student_count, active_assignments, engagement_rate)
           VALUES (?,?,?,?,?)''',
        (data['class_id'], data['name'],
         data.get('student_count', 0),
         data.get('active_assignments', 0),
         data.get('engagement_rate', 0)))
    db.commit()


def update_class(class_id, data):
    db = get_db()
    sets, vals = [], []
    for col in ('name', 'student_count', 'active_assignments', 'engagement_rate'):
        if col in data:
            sets.append(f'{col}=?')
            vals.append(data[col])
    if sets:
        vals.append(class_id)
        db.execute(
            f'UPDATE classes SET {", ".join(sets)} WHERE class_id=?', vals)
        db.commit()


# ═══════════════════════════════════════════════════════════════════
#  STUDENTS
# ═══════════════════════════════════════════════════════════════════

def get_all_students(class_id=None):
    db = get_db()
    if class_id:
        rows = db.execute(
            'SELECT * FROM students WHERE class_id=? ORDER BY student_id',
            (class_id,)
        ).fetchall()
    else:
        rows = db.execute(
            'SELECT * FROM students ORDER BY student_id'
        ).fetchall()
    return [_build_student(r) for r in rows]


def get_student(student_id):
    row = get_db().execute(
        'SELECT * FROM students WHERE student_id=?', (student_id,)
    ).fetchone()
    return _build_student(row) if row else None


def _build_student(row):
    """Convert a students row + related data into the camelCase dict
    expected by templates and API consumers."""
    db = get_db()
    s = _row(row)
    sid = s['student_id']

    ach = db.execute(
        '''SELECT sa.achievement_id, a.name, a.icon, sa.earned_date
           FROM student_achievements sa
           JOIN achievements a ON sa.achievement_id = a.achievement_id
           WHERE sa.student_id = ?''', (sid,)
    ).fetchall()

    acts = db.execute(
        '''SELECT activity_id, activity_type, title, activity_date, success
           FROM activity_log WHERE student_id = ?
           ORDER BY activity_date DESC''', (sid,)
    ).fetchall()

    return {
        'id': sid,
        'name': s['name'],
        'avatar': s['avatar'],
        'classId': s['class_id'],
        'progressPercentage': s['progress_percentage'],
        'challengesCompleted': s['challenges_completed'],
        'lessonsCompleted': s['lessons_completed'],
        'lastActivity': s['last_activity'],
        'teacherNotes': s['teacher_notes'],
        'achievements': [
            {'id': r['achievement_id'], 'name': r['name'],
             'icon': r['icon'], 'earnedDate': r['earned_date']}
            for r in ach
        ],
        'activityHistory': [
            {'id': r['activity_id'], 'type': r['activity_type'],
             'title': r['title'], 'date': r['activity_date'],
             'success': bool(r['success'])}
            for r in acts
        ],
    }


def create_student(data):
    db = get_db()
    db.execute(
        '''INSERT INTO students
           (student_id, name, avatar, class_id, progress_percentage,
            challenges_completed, lessons_completed, last_activity, teacher_notes)
           VALUES (?,?,?,?,?,?,?,?,?)''',
        (data['student_id'], data['name'], data.get('avatar', ''),
         data.get('class_id'), data.get('progress_percentage', 0),
         data.get('challenges_completed', 0), data.get('lessons_completed', 0),
         data.get('last_activity', ''), data.get('teacher_notes', '')))
    db.commit()


def update_student(student_id, data):
    db = get_db()
    allowed = ('name', 'avatar', 'class_id', 'progress_percentage',
               'challenges_completed', 'lessons_completed',
               'last_activity', 'teacher_notes')
    sets, vals = [], []
    for col in allowed:
        if col in data:
            sets.append(f'{col}=?')
            vals.append(data[col])
    if sets:
        sets.append('updated_at=CURRENT_TIMESTAMP')
        vals.append(student_id)
        db.execute(
            f'UPDATE students SET {", ".join(sets)} WHERE student_id=?', vals)
        db.commit()


def update_student_avatar(student_id, avatar):
    db = get_db()
    cur = db.execute(
        'UPDATE students SET avatar=?, updated_at=CURRENT_TIMESTAMP WHERE student_id=?',
        (avatar, student_id))
    db.commit()
    return cur.rowcount > 0


# ═══════════════════════════════════════════════════════════════════
#  ACHIEVEMENTS
# ═══════════════════════════════════════════════════════════════════

def get_all_achievements():
    rows = get_db().execute(
        'SELECT * FROM achievements ORDER BY achievement_id'
    ).fetchall()
    return [{'id': r['achievement_id'], 'name': r['name'],
             'icon': r['icon'], 'description': r['description']}
            for r in rows]


def add_student_achievement(student_id, achievement_id, earned_date):
    db = get_db()
    db.execute(
        '''INSERT OR IGNORE INTO student_achievements
           (student_id, achievement_id, earned_date) VALUES (?,?,?)''',
        (student_id, achievement_id, earned_date))
    db.commit()


def get_student_achievements(student_id):
    rows = get_db().execute(
        '''SELECT sa.achievement_id, a.name, a.icon, sa.earned_date
           FROM student_achievements sa
           JOIN achievements a ON sa.achievement_id = a.achievement_id
           WHERE sa.student_id = ?''', (student_id,)
    ).fetchall()
    return [{'id': r['achievement_id'], 'name': r['name'],
             'icon': r['icon'], 'earnedDate': r['earned_date']}
            for r in rows]


# ═══════════════════════════════════════════════════════════════════
#  ACTIVITY LOG
# ═══════════════════════════════════════════════════════════════════

def add_activity(data):
    db = get_db()
    db.execute(
        '''INSERT INTO activity_log
           (activity_id, student_id, activity_type, title, activity_date, success)
           VALUES (?,?,?,?,?,?)''',
        (data['activity_id'], data['student_id'], data['activity_type'],
         data.get('title', ''), data.get('activity_date', ''),
         int(data.get('success', 0))))
    db.commit()


def get_student_activity(student_id, limit=50):
    rows = get_db().execute(
        '''SELECT * FROM activity_log
           WHERE student_id=? ORDER BY activity_date DESC LIMIT ?''',
        (student_id, limit)
    ).fetchall()
    return [{'id': r['activity_id'], 'type': r['activity_type'],
             'title': r['title'], 'date': r['activity_date'],
             'success': bool(r['success'])} for r in rows]


# ═══════════════════════════════════════════════════════════════════
#  EXERCISES  (stored in DB, linked to lesson JSON files)
# ═══════════════════════════════════════════════════════════════════

def get_exercises(lesson_id=None):
    db = get_db()
    if lesson_id:
        rows = db.execute(
            'SELECT * FROM exercises WHERE lesson_id=? ORDER BY sort_order',
            (lesson_id,)
        ).fetchall()
    else:
        rows = db.execute(
            'SELECT * FROM exercises ORDER BY lesson_id, sort_order'
        ).fetchall()
    return [{'id': r['exercise_id'], 'lessonId': r['lesson_id'],
             'title': r['title'], 'description': r['description'],
             'difficulty': r['difficulty'], 'type': r['exercise_type']}
            for r in rows]


# ═══════════════════════════════════════════════════════════════════
#  ASSIGNMENTS
# ═══════════════════════════════════════════════════════════════════

def get_all_assignments(class_id=None):
    db = get_db()
    if class_id:
        rows = db.execute(
            'SELECT * FROM assignments WHERE class_id=? ORDER BY assigned_date',
            (class_id,)
        ).fetchall()
    else:
        rows = db.execute(
            'SELECT * FROM assignments ORDER BY assigned_date'
        ).fetchall()
    return [_fmt_assignment(r) for r in rows]


def get_assignment(assignment_id):
    row = get_db().execute(
        'SELECT * FROM assignments WHERE assignment_id=?', (assignment_id,)
    ).fetchone()
    return _fmt_assignment(row) if row else None


def _fmt_assignment(row):
    a = _row(row)
    return {
        'id': a['assignment_id'],
        'lessonId': a['lesson_id'],
        'classId': a['class_id'],
        'assignedDate': a['assigned_date'],
        'dueDate': a['due_date'],
        'completionRate': a['completion_rate'],
    }


def create_assignment(data):
    db = get_db()
    db.execute(
        '''INSERT INTO assignments
           (assignment_id, lesson_id, class_id, assigned_date, due_date, completion_rate)
           VALUES (?,?,?,?,?,?)''',
        (data['assignment_id'], data['lesson_id'], data['class_id'],
         data.get('assigned_date', ''), data.get('due_date', ''),
         data.get('completion_rate', 0)))
    db.commit()


def update_assignment(assignment_id, data):
    db = get_db()
    allowed = ('lesson_id', 'class_id', 'assigned_date', 'due_date', 'completion_rate')
    sets, vals = [], []
    for col in allowed:
        if col in data:
            sets.append(f'{col}=?')
            vals.append(data[col])
    if sets:
        vals.append(assignment_id)
        db.execute(
            f'UPDATE assignments SET {", ".join(sets)} WHERE assignment_id=?', vals)
        db.commit()


# ═══════════════════════════════════════════════════════════════════
#  TEAMS  (kids-app gamification)
# ═══════════════════════════════════════════════════════════════════

def get_all_teams():
    db = get_db()
    rows = db.execute(
        'SELECT * FROM teams ORDER BY total_points DESC'
    ).fetchall()
    result = []
    for row in rows:
        t = _row(row)
        members = db.execute(
            'SELECT * FROM team_members WHERE team_id=? ORDER BY points DESC',
            (t['team_id'],)
        ).fetchall()
        result.append({
            'id': t['team_id'],
            'name': t['name'],
            'totalPoints': t['total_points'],
            'members': [
                {'id': m['member_id'], 'name': m['name'],
                 'avatar': m['avatar'], 'points': m['points']}
                for m in members
            ],
        })
    return result


def get_team(team_id):
    db = get_db()
    row = db.execute(
        'SELECT * FROM teams WHERE team_id=?', (team_id,)
    ).fetchone()
    if not row:
        return None
    t = _row(row)
    members = db.execute(
        'SELECT * FROM team_members WHERE team_id=? ORDER BY points DESC',
        (team_id,)
    ).fetchall()
    return {
        'id': t['team_id'],
        'name': t['name'],
        'totalPoints': t['total_points'],
        'members': [
            {'id': m['member_id'], 'name': m['name'],
             'avatar': m['avatar'], 'points': m['points']}
            for m in members
        ],
    }


def add_team_member(team_id, data):
    db = get_db()
    db.execute(
        'INSERT INTO team_members (member_id, team_id, name, avatar, points) VALUES (?,?,?,?,?)',
        (data['member_id'], team_id, data['name'],
         data.get('avatar', ''), data.get('points', 0)))
    _recalc_team(team_id)
    db.commit()


def update_member_points(member_id, points_to_add):
    db = get_db()
    db.execute(
        'UPDATE team_members SET points = points + ? WHERE member_id=?',
        (points_to_add, member_id))
    row = db.execute(
        'SELECT team_id FROM team_members WHERE member_id=?', (member_id,)
    ).fetchone()
    if row:
        _recalc_team(row['team_id'])
    db.commit()


def _recalc_team(team_id):
    db = get_db()
    row = db.execute(
        'SELECT COALESCE(SUM(points),0) AS total FROM team_members WHERE team_id=?',
        (team_id,)
    ).fetchone()
    db.execute(
        'UPDATE teams SET total_points=? WHERE team_id=?',
        (row['total'], team_id))


def get_team_rankings():
    rows = get_db().execute(
        'SELECT * FROM teams ORDER BY total_points DESC'
    ).fetchall()
    return [{'id': r['team_id'], 'name': r['name'],
             'totalPoints': r['total_points']} for r in rows]


def get_member_rankings():
    rows = get_db().execute(
        '''SELECT tm.member_id, tm.name, tm.avatar, tm.points,
                  t.name AS team_name, t.team_id
           FROM team_members tm
           JOIN teams t ON tm.team_id = t.team_id
           ORDER BY tm.points DESC'''
    ).fetchall()
    return [{'id': r['member_id'], 'name': r['name'], 'avatar': r['avatar'],
             'points': r['points'], 'teamName': r['team_name'],
             'teamId': r['team_id']} for r in rows]


# ═══════════════════════════════════════════════════════════════════
#  CHALLENGES
# ═══════════════════════════════════════════════════════════════════

def get_all_challenges(difficulty=None, age=None):
    db = get_db()
    query = 'SELECT * FROM challenges'
    params = []
    conds = []
    if difficulty:
        conds.append('difficulty = ?')
        params.append(difficulty)
    if age is not None:
        # Age groups stored as "8-12", "12-15", "15-18"
        conds.append(
            '''(
                CAST(SUBSTR(age_group, 1, INSTR(age_group, '-') - 1) AS INTEGER) <= ?
                AND CAST(SUBSTR(age_group, INSTR(age_group, '-') + 1) AS INTEGER) >= ?
            )'''
        )
        params.extend([age, age])
    if conds:
        query += ' WHERE ' + ' AND '.join(conds)
    query += ' ORDER BY challenge_id'
    rows = db.execute(query, params).fetchall()
    return [_fmt_challenge(r) for r in rows]


def get_challenge(challenge_id):
    row = get_db().execute(
        'SELECT * FROM challenges WHERE challenge_id=?', (challenge_id,)
    ).fetchone()
    return _fmt_challenge(row) if row else None


def _fmt_challenge(row):
    c = _row(row)
    return {
        'id': c['challenge_id'],
        'title': c['title'],
        'description': c['description'],
        'difficulty': c['difficulty'],
        'category': c['category'],
        'points': c['points'],
        'question': c['question'],
        'options': json.loads(c['options']) if c['options'] else [],
        'correctAnswer': c['correct_answer'],
        'explanation': c['explanation'],
        'ageGroup': c['age_group'],
    }


def get_daily_challenge(date_str):
    """Pick a deterministic challenge for a given date string (YYYY-MM-DD).

    Mirrors the Swift ``ChallengeData.dailyChallenge(for:)`` logic which uses
    the ordinal day-of-year modulo the number of challenges.
    """
    db = get_db()
    ids = db.execute(
        'SELECT challenge_id FROM challenges ORDER BY challenge_id'
    ).fetchall()
    if not ids:
        return None
    try:
        dt = datetime.strptime(date_str, '%Y-%m-%d')
        day_of_year = dt.timetuple().tm_yday
    except ValueError:
        day_of_year = 1
    index = day_of_year % len(ids)
    return get_challenge(ids[index]['challenge_id'])


# ═══════════════════════════════════════════════════════════════════
#  CHALLENGE RESULTS
# ═══════════════════════════════════════════════════════════════════

def get_challenge_results(member_id):
    rows = get_db().execute(
        'SELECT * FROM challenge_results WHERE member_id=? ORDER BY completed_date DESC',
        (member_id,)
    ).fetchall()
    return [{'id': r['id'], 'challengeId': r['challenge_id'],
             'completed': bool(r['completed']), 'correct': bool(r['correct']),
             'points': r['points'], 'date': r['completed_date']}
            for r in rows]


def save_challenge_result(data):
    db = get_db()
    db.execute(
        '''INSERT INTO challenge_results
           (id, member_id, challenge_id, completed, correct, points)
           VALUES (?,?,?,?,?,?)''',
        (data['id'], data['member_id'], data['challenge_id'],
         int(data.get('completed', 1)), int(data.get('correct', 0)),
         data.get('points', 0)))
    db.commit()


# ═══════════════════════════════════════════════════════════════════
#  USER PROFILES  (kids-app accounts)
# ═══════════════════════════════════════════════════════════════════

def get_user_profile(member_id):
    row = get_db().execute(
        'SELECT * FROM user_profiles WHERE member_id=?', (member_id,)
    ).fetchone()
    if not row:
        return None
    p = _row(row)
    return {
        'memberId': p['member_id'],
        'name': p['name'],
        'age': p['age'],
        'teamId': p['team_id'],
        'avatar': p['avatar'],
    }


def save_user_profile(data):
    db = get_db()
    db.execute(
        '''INSERT INTO user_profiles (member_id, name, age, team_id, avatar)
           VALUES (?,?,?,?,?)
           ON CONFLICT(member_id) DO UPDATE
           SET name=excluded.name, age=excluded.age,
               team_id=excluded.team_id, avatar=excluded.avatar,
               updated_at=CURRENT_TIMESTAMP''',
        (data['member_id'], data['name'], data.get('age'),
         data.get('team_id'), data.get('avatar', '')))
    db.commit()


def get_user_stats(member_id):
    results = get_db().execute(
        'SELECT * FROM challenge_results WHERE member_id=? ORDER BY completed_date',
        (member_id,)
    ).fetchall()
    total_pts = sum(r['points'] for r in results if r['correct'])
    completed = sum(1 for r in results if r['completed'])
    correct = sum(1 for r in results if r['correct'])
    accuracy = round((correct / completed) * 100) if completed else 0

    # streak – consecutive days with at least one completed result
    streak = 0
    if results:
        completed_dates = set()
        for r in results:
            if r['completed']:
                try:
                    dt = datetime.fromisoformat(
                        str(r['completed_date']).replace('Z', '+00:00'))
                    completed_dates.add(dt.date())
                except (ValueError, AttributeError):
                    pass
        today = datetime.now().date()
        for i in range(365):
            day = today - timedelta(days=i)
            if day in completed_dates:
                streak += 1
            elif i > 0:
                break

    return {
        'totalPoints': total_pts,
        'completed': completed,
        'correct': correct,
        'accuracy': accuracy,
        'streak': streak,
    }


# ═══════════════════════════════════════════════════════════════════
#  USER TRACKING / ANALYTICS
# ═══════════════════════════════════════════════════════════════════

def log_tracking_event(data):
    db = get_db()
    db.execute(
        '''INSERT INTO user_tracking
           (user_type, user_id, event_type, event_data, session_id)
           VALUES (?,?,?,?,?)''',
        (data['user_type'], data['user_id'], data['event_type'],
         json.dumps(data.get('event_data', {})),
         data.get('session_id')))
    db.commit()


def get_tracking_events(user_type=None, user_id=None,
                        event_type=None, limit=100):
    db = get_db()
    query = 'SELECT * FROM user_tracking'
    params, conds = [], []
    if user_type:
        conds.append('user_type=?'); params.append(user_type)
    if user_id:
        conds.append('user_id=?'); params.append(user_id)
    if event_type:
        conds.append('event_type=?'); params.append(event_type)
    if conds:
        query += ' WHERE ' + ' AND '.join(conds)
    query += ' ORDER BY created_at DESC LIMIT ?'
    params.append(limit)
    rows = db.execute(query, params).fetchall()
    return [{
        'id': r['id'],
        'userType': r['user_type'],
        'userId': r['user_id'],
        'eventType': r['event_type'],
        'eventData': json.loads(r['event_data']) if r['event_data'] else {},
        'sessionId': r['session_id'],
        'createdAt': r['created_at'],
    } for r in rows]
