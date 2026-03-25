"""Progress API: submit exercise attempts, query per-student and per-lesson progress."""

import json
from flask import Blueprint, request, jsonify, g

from database import get_db
from auth import require_auth, require_role
from validators import validate_id

progress_bp = Blueprint('progress', __name__, url_prefix='/api/progress')


# ── Submit exercise attempt (from app) ────────────────────────────

@progress_bp.route('/attempt', methods=['POST'])
@require_auth
@require_role('student')
def submit_attempt():
    """Record an exercise attempt.

    Body: {
        exercise_id, lesson_id, score (0-100), completed (bool),
        time_spent_sec, attempt_data (optional JSON object)
    }
    """
    data = request.get_json(silent=True) or {}
    student_id = g.account['student_id']
    if not student_id:
        return jsonify({"error": "No student profile linked"}), 400

    exercise_id = data.get('exercise_id') or data.get('exerciseId', '')
    lesson_id = data.get('lesson_id') or data.get('lessonId', '')

    if not validate_id(exercise_id, 'exercise_id'):
        return jsonify({"error": f"Invalid exercise_id: {exercise_id}"}), 400
    if not validate_id(lesson_id, 'lesson_id'):
        return jsonify({"error": f"Invalid lesson_id: {lesson_id}"}), 400

    score = data.get('score', 0)
    completed = int(data.get('completed', 0))
    time_spent = data.get('time_spent_sec', data.get('timeSpentSec', 0))
    attempt_data = data.get('attempt_data') or data.get('attemptData')

    db = get_db()
    cur = db.execute(
        '''INSERT INTO exercise_attempts
           (student_id, exercise_id, lesson_id, score, completed, time_spent_sec, attempt_data)
           VALUES (?,?,?,?,?,?,?)''',
        (student_id, exercise_id, lesson_id, score, completed, time_spent,
         json.dumps(attempt_data) if attempt_data else None))
    db.commit()

    _update_student_stats(student_id)

    return jsonify({
        "success": True,
        "attemptId": cur.lastrowid,
        "studentId": student_id,
    }), 201


# ── Batch sync (offline queue from app) ───────────────────────────

@progress_bp.route('/sync', methods=['POST'])
@require_auth
@require_role('student')
def sync_attempts():
    """Accept an array of queued attempts from an offline app.

    Body: { attempts: [ { exercise_id, lesson_id, score, completed,
                          time_spent_sec, attempt_data, timestamp } ] }
    """
    data = request.get_json(silent=True) or {}
    attempts = data.get('attempts', [])
    student_id = g.account['student_id']
    if not student_id:
        return jsonify({"error": "No student profile linked"}), 400

    db = get_db()
    saved = 0
    errors = []

    for i, a in enumerate(attempts):
        ex_id = a.get('exercise_id') or a.get('exerciseId', '')
        ls_id = a.get('lesson_id') or a.get('lessonId', '')
        if not validate_id(ex_id, 'exercise_id') or not validate_id(ls_id, 'lesson_id'):
            errors.append({"index": i, "error": "Invalid ID format"})
            continue
        ts = a.get('timestamp') or a.get('created_at')
        attempt_data = a.get('attempt_data') or a.get('attemptData')
        db.execute(
            '''INSERT INTO exercise_attempts
               (student_id, exercise_id, lesson_id, score, completed,
                time_spent_sec, attempt_data, created_at)
               VALUES (?,?,?,?,?,?,?,COALESCE(?,CURRENT_TIMESTAMP))''',
            (student_id, ex_id, ls_id,
             a.get('score', 0), int(a.get('completed', 0)),
             a.get('time_spent_sec', a.get('timeSpentSec', 0)),
             json.dumps(attempt_data) if attempt_data else None,
             ts))
        saved += 1

    db.commit()
    _update_student_stats(student_id)

    return jsonify({
        "success": True,
        "saved": saved,
        "errors": errors,
    }), 201


# ── Per-student progress (teacher dashboard) ──────────────────────

@progress_bp.route('/student/<student_id>', methods=['GET'])
@require_auth
def student_progress(student_id):
    """All exercise attempts for a student, grouped by lesson."""
    if not validate_id(student_id, 'student_id'):
        return jsonify({"error": "Invalid student_id"}), 400

    db = get_db()
    rows = db.execute(
        '''SELECT exercise_id, lesson_id,
                  MAX(score) AS best_score,
                  COUNT(*) AS attempt_count,
                  MAX(completed) AS ever_completed,
                  SUM(time_spent_sec) AS total_time,
                  MAX(created_at) AS last_attempt
           FROM exercise_attempts
           WHERE student_id = ?
           GROUP BY exercise_id, lesson_id
           ORDER BY lesson_id, exercise_id''',
        (student_id,)
    ).fetchall()

    lessons = {}
    for r in rows:
        lid = r['lesson_id']
        if lid not in lessons:
            lessons[lid] = []
        lessons[lid].append({
            'exerciseId': r['exercise_id'],
            'bestScore': r['best_score'],
            'attempts': r['attempt_count'],
            'completed': bool(r['ever_completed']),
            'totalTimeSec': r['total_time'],
            'lastAttempt': r['last_attempt'],
        })

    return jsonify({
        'studentId': student_id,
        'lessons': [
            {'lessonId': lid, 'exercises': exs}
            for lid, exs in lessons.items()
        ],
    })


# ── Per-lesson progress (class-wide view for teacher) ─────────────

@progress_bp.route('/lesson/<lesson_id>', methods=['GET'])
@require_auth
def lesson_progress(lesson_id):
    """Per-lesson breakdown: how each student in a class performed.

    Query param: ?class_id=class-1 (optional, filters by class)
    """
    if not validate_id(lesson_id, 'lesson_id'):
        return jsonify({"error": "Invalid lesson_id"}), 400

    class_id = request.args.get('class_id') or request.args.get('classId')

    db = get_db()

    if class_id:
        students = db.execute(
            'SELECT student_id, name FROM students WHERE class_id=? ORDER BY name',
            (class_id,)
        ).fetchall()
    else:
        students = db.execute(
            'SELECT student_id, name FROM students ORDER BY name'
        ).fetchall()

    result = []
    for s in students:
        sid = s['student_id']
        rows = db.execute(
            '''SELECT exercise_id,
                      MAX(score) AS best_score,
                      COUNT(*) AS attempt_count,
                      MAX(completed) AS ever_completed,
                      SUM(time_spent_sec) AS total_time,
                      MAX(created_at) AS last_attempt
               FROM exercise_attempts
               WHERE student_id=? AND lesson_id=?
               GROUP BY exercise_id
               ORDER BY exercise_id''',
            (sid, lesson_id)
        ).fetchall()

        result.append({
            'studentId': sid,
            'name': s['name'],
            'exercises': [{
                'exerciseId': r['exercise_id'],
                'bestScore': r['best_score'],
                'attempts': r['attempt_count'],
                'completed': bool(r['ever_completed']),
                'totalTimeSec': r['total_time'],
                'lastAttempt': r['last_attempt'],
            } for r in rows],
        })

    return jsonify({'lessonId': lesson_id, 'students': result})


# ── Class roster with progress summary ────────────────────────────

@progress_bp.route('/class/<class_id>', methods=['GET'])
@require_auth
def class_progress(class_id):
    """Class roster with per-student progress summaries."""
    if not validate_id(class_id, 'class_id'):
        return jsonify({"error": "Invalid class_id"}), 400

    db = get_db()
    students = db.execute(
        'SELECT * FROM students WHERE class_id=? ORDER BY name',
        (class_id,)
    ).fetchall()

    total_exercises = db.execute(
        'SELECT COUNT(*) AS c FROM exercises'
    ).fetchone()['c'] or 1

    result = []
    for s in students:
        sid = s['student_id']
        stats = db.execute(
            '''SELECT COUNT(DISTINCT exercise_id) AS exercises_done,
                      COUNT(*) AS total_attempts,
                      ROUND(AVG(score), 1) AS avg_score,
                      SUM(time_spent_sec) AS total_time,
                      MAX(created_at) AS last_attempt,
                      COUNT(DISTINCT lesson_id) AS lessons_touched
               FROM exercise_attempts WHERE student_id=?''',
            (sid,)
        ).fetchone()

        completed_exercises = db.execute(
            '''SELECT COUNT(DISTINCT exercise_id) AS c
               FROM exercise_attempts
               WHERE student_id=? AND completed=1''',
            (sid,)
        ).fetchone()['c']

        progress = round((completed_exercises / total_exercises) * 100)

        result.append({
            'studentId': sid,
            'name': s['name'],
            'avatar': s['avatar'],
            'progressPercentage': progress,
            'lessonsCompleted': stats['lessons_touched'] or 0,
            'exercisesCompleted': completed_exercises,
            'totalAttempts': stats['total_attempts'] or 0,
            'avgScore': stats['avg_score'] or 0,
            'totalTimeSec': stats['total_time'] or 0,
            'lastActivity': stats['last_attempt'],
        })

    return jsonify({'classId': class_id, 'students': result})


# ── Progress over time ────────────────────────────────────────────

@progress_bp.route('/student/<student_id>/timeline', methods=['GET'])
@require_auth
def student_timeline(student_id):
    """Day-by-day progress for a student (for graphs)."""
    if not validate_id(student_id, 'student_id'):
        return jsonify({"error": "Invalid student_id"}), 400

    db = get_db()
    rows = db.execute(
        '''SELECT DATE(created_at) AS day,
                  COUNT(*) AS attempts,
                  ROUND(AVG(score), 1) AS avg_score,
                  SUM(completed) AS completed,
                  SUM(time_spent_sec) AS time_sec
           FROM exercise_attempts
           WHERE student_id=?
           GROUP BY DATE(created_at)
           ORDER BY day''',
        (student_id,)
    ).fetchall()

    return jsonify({
        'studentId': student_id,
        'days': [{
            'date': r['day'],
            'attempts': r['attempts'],
            'avgScore': r['avg_score'],
            'completed': r['completed'],
            'timeSec': r['time_sec'],
        } for r in rows],
    })


# ── Internal helper ───────────────────────────────────────────────

def _update_student_stats(student_id):
    """Recalculate aggregate stats on the students row from exercise_attempts."""
    db = get_db()
    total_exercises = db.execute(
        'SELECT COUNT(*) AS c FROM exercises'
    ).fetchone()['c'] or 1

    completed_exercises = db.execute(
        '''SELECT COUNT(DISTINCT exercise_id) AS c
           FROM exercise_attempts
           WHERE student_id=? AND completed=1''',
        (student_id,)
    ).fetchone()['c']

    lessons_completed = db.execute(
        '''SELECT COUNT(DISTINCT lesson_id) AS c
           FROM exercise_attempts
           WHERE student_id=? AND completed=1''',
        (student_id,)
    ).fetchone()['c']

    progress = round((completed_exercises / total_exercises) * 100)

    db.execute(
        '''UPDATE students
           SET progress_percentage=?, lessons_completed=?,
               last_activity=CURRENT_TIMESTAMP, updated_at=CURRENT_TIMESTAMP
           WHERE student_id=?''',
        (progress, lessons_completed, student_id))
    db.commit()
