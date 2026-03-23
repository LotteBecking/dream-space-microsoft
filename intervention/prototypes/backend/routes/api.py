"""REST API for teacher-dashboard entities:
profiles, classes, students, assignments, lessons/exercises."""

from flask import Blueprint, request, jsonify

import models
from validators import validate_id
from lesson_loader import load_lessons, search_lessons, get_lesson_by_id
import config

api_bp = Blueprint('api', __name__, url_prefix='/api')


def _lessons():
    return load_lessons(config.LESSON_CONTENT_DIR)


# ── Teacher profile ────────────────────────────────────────────────

@api_bp.route('/profile', methods=['GET', 'POST'])
def profile():
    if request.method == 'POST':
        data = request.get_json(silent=True) or {}
        models.save_teacher_profile(data)
        return jsonify({"success": True})
    return jsonify(models.get_teacher_profile() or {})


# ── Classes ────────────────────────────────────────────────────────

@api_bp.route('/classes', methods=['GET'])
def list_classes():
    return jsonify(models.get_all_classes())


@api_bp.route('/classes/<class_id>', methods=['GET'])
def get_class(class_id):
    c = models.get_class(class_id)
    if not c:
        return jsonify({"error": "Class not found"}), 404
    return jsonify(c)


@api_bp.route('/classes', methods=['POST'])
def create_class():
    data = request.get_json(silent=True) or {}
    cid = data.get('class_id') or data.get('classId', '')
    if not validate_id(cid, 'class_id'):
        return jsonify({"error": f"Invalid class_id: {cid}"}), 400
    data['class_id'] = cid
    # Map camelCase payload → snake_case for DB
    data.setdefault('student_count', data.pop('studentCount', 0))
    data.setdefault('active_assignments', data.pop('activeAssignments', 0))
    data.setdefault('engagement_rate', data.pop('engagementRate', 0))
    models.create_class(data)
    return jsonify({"success": True, "classId": cid}), 201


@api_bp.route('/classes/<class_id>', methods=['PUT'])
def update_class(class_id):
    if not validate_id(class_id, 'class_id'):
        return jsonify({"error": "Invalid class_id"}), 400
    data = request.get_json(silent=True) or {}
    # camelCase → snake_case mapping
    if 'studentCount' in data:
        data['student_count'] = data.pop('studentCount')
    if 'activeAssignments' in data:
        data['active_assignments'] = data.pop('activeAssignments')
    if 'engagementRate' in data:
        data['engagement_rate'] = data.pop('engagementRate')
    models.update_class(class_id, data)
    return jsonify({"success": True})


@api_bp.route('/classes/<class_id>/students', methods=['GET'])
def class_students(class_id):
    return jsonify(models.get_all_students(class_id))


# ── Students ───────────────────────────────────────────────────────

@api_bp.route('/students', methods=['GET'])
def list_students():
    class_id = request.args.get('class_id') or request.args.get('classId')
    return jsonify(models.get_all_students(class_id))


@api_bp.route('/students/<student_id>', methods=['GET'])
def get_student(student_id):
    s = models.get_student(student_id)
    if not s:
        return jsonify({"error": "Student not found"}), 404
    return jsonify(s)


@api_bp.route('/students', methods=['POST'])
def create_student():
    data = request.get_json(silent=True) or {}
    sid = data.get('student_id') or data.get('studentId', '')
    if not validate_id(sid, 'student_id'):
        return jsonify({"error": f"Invalid student_id: {sid}"}), 400
    data['student_id'] = sid
    # camelCase → snake_case
    for camel, snake in [('classId', 'class_id'),
                         ('progressPercentage', 'progress_percentage'),
                         ('challengesCompleted', 'challenges_completed'),
                         ('lessonsCompleted', 'lessons_completed'),
                         ('lastActivity', 'last_activity'),
                         ('teacherNotes', 'teacher_notes')]:
        if camel in data:
            data.setdefault(snake, data.pop(camel))
    models.create_student(data)
    return jsonify({"success": True, "studentId": sid}), 201


@api_bp.route('/students/<student_id>', methods=['PUT'])
def update_student(student_id):
    if not validate_id(student_id, 'student_id'):
        return jsonify({"error": "Invalid student_id"}), 400
    data = request.get_json(silent=True) or {}
    for camel, snake in [('classId', 'class_id'),
                         ('progressPercentage', 'progress_percentage'),
                         ('challengesCompleted', 'challenges_completed'),
                         ('lessonsCompleted', 'lessons_completed'),
                         ('lastActivity', 'last_activity'),
                         ('teacherNotes', 'teacher_notes')]:
        if camel in data:
            data[snake] = data.pop(camel)
    models.update_student(student_id, data)
    return jsonify({"success": True})


@api_bp.route('/students/<student_id>/avatar', methods=['POST'])
def update_avatar(student_id):
    data = request.get_json(silent=True) or {}
    avatar = (data.get('avatar') or '').strip()
    if not avatar:
        return jsonify({"success": False, "error": "Avatar is required"}), 400
    if len(avatar) > 8:
        return jsonify({"success": False, "error": "Avatar is too long"}), 400
    if not models.update_student_avatar(student_id, avatar):
        return jsonify({"success": False, "error": "Student not found"}), 404
    return jsonify({"success": True, "studentId": student_id, "avatar": avatar})


# ── Student achievements ──────────────────────────────────────────

@api_bp.route('/students/<student_id>/achievements', methods=['GET'])
def student_achievements(student_id):
    return jsonify(models.get_student_achievements(student_id))


@api_bp.route('/students/<student_id>/achievements', methods=['POST'])
def add_achievement(student_id):
    if not validate_id(student_id, 'student_id'):
        return jsonify({"error": "Invalid student_id"}), 400
    data = request.get_json(silent=True) or {}
    ach_id = data.get('achievement_id') or data.get('achievementId', '')
    if not validate_id(ach_id, 'achievement_id'):
        return jsonify({"error": f"Invalid achievement_id: {ach_id}"}), 400
    earned = data.get('earned_date') or data.get('earnedDate', '')
    models.add_student_achievement(student_id, ach_id, earned)
    return jsonify({"success": True}), 201


# ── Student activity log ──────────────────────────────────────────

@api_bp.route('/students/<student_id>/activity', methods=['GET'])
def student_activity(student_id):
    limit = request.args.get('limit', 50, type=int)
    return jsonify(models.get_student_activity(student_id, limit))


@api_bp.route('/students/<student_id>/activity', methods=['POST'])
def add_activity(student_id):
    if not validate_id(student_id, 'student_id'):
        return jsonify({"error": "Invalid student_id"}), 400
    data = request.get_json(silent=True) or {}
    act_id = data.get('activity_id') or data.get('activityId', '')
    if not validate_id(act_id, 'activity_id'):
        return jsonify({"error": f"Invalid activity_id: {act_id}"}), 400
    payload = {
        'activity_id': act_id,
        'student_id': student_id,
        'activity_type': data.get('activity_type') or data.get('type', ''),
        'title': data.get('title', ''),
        'activity_date': data.get('activity_date') or data.get('date', ''),
        'success': data.get('success', 0),
    }
    models.add_activity(payload)
    return jsonify({"success": True}), 201


# ── Lessons (read-only from JSON, exercises from DB) ──────────────

@api_bp.route('/lessons', methods=['GET'])
def list_lessons():
    lessons = _lessons()
    q = request.args.get('search', '')
    if q:
        lessons = search_lessons(lessons, q)
    # Return lightweight list (no full teacher instructions)
    return jsonify([{
        'id': l.get('id'),
        'title': l.get('title'),
        'description': l.get('description'),
        'duration': l.get('duration'),
        'level': l.get('level'),
    } for l in lessons])


@api_bp.route('/lessons/<lesson_id>', methods=['GET'])
def get_lesson(lesson_id):
    lesson = get_lesson_by_id(_lessons(), lesson_id)
    if not lesson:
        return jsonify({"error": "Lesson not found"}), 404
    return jsonify(lesson)


@api_bp.route('/lessons/<lesson_id>/exercises', methods=['GET'])
def lesson_exercises(lesson_id):
    return jsonify(models.get_exercises(lesson_id))


# ── Assignments ────────────────────────────────────────────────────

@api_bp.route('/assignments', methods=['GET'])
def list_assignments():
    class_id = request.args.get('class_id') or request.args.get('classId')
    return jsonify(models.get_all_assignments(class_id))


@api_bp.route('/assignments/<assignment_id>', methods=['GET'])
def get_assignment(assignment_id):
    a = models.get_assignment(assignment_id)
    if not a:
        return jsonify({"error": "Assignment not found"}), 404
    return jsonify(a)


@api_bp.route('/assignments', methods=['POST'])
def create_assignment():
    data = request.get_json(silent=True) or {}
    aid = data.get('assignment_id') or data.get('assignmentId', '')
    if not validate_id(aid, 'assignment_id'):
        return jsonify({"error": f"Invalid assignment_id: {aid}"}), 400
    lid = data.get('lesson_id') or data.get('lessonId', '')
    if not validate_id(lid, 'lesson_id'):
        return jsonify({"error": f"Invalid lesson_id: {lid}"}), 400
    cid = data.get('class_id') or data.get('classId', '')
    if not validate_id(cid, 'class_id'):
        return jsonify({"error": f"Invalid class_id: {cid}"}), 400
    payload = {
        'assignment_id': aid,
        'lesson_id': lid,
        'class_id': cid,
        'assigned_date': data.get('assigned_date') or data.get('assignedDate', ''),
        'due_date': data.get('due_date') or data.get('dueDate', ''),
        'completion_rate': data.get('completion_rate',
                                    data.get('completionRate', 0)),
    }
    models.create_assignment(payload)
    return jsonify({"success": True, "assignmentId": aid}), 201


@api_bp.route('/assignments/<assignment_id>', methods=['PUT'])
def update_assignment(assignment_id):
    if not validate_id(assignment_id, 'assignment_id'):
        return jsonify({"error": "Invalid assignment_id"}), 400
    data = request.get_json(silent=True) or {}
    for camel, snake in [('lessonId', 'lesson_id'),
                         ('classId', 'class_id'),
                         ('assignedDate', 'assigned_date'),
                         ('dueDate', 'due_date'),
                         ('completionRate', 'completion_rate')]:
        if camel in data:
            data[snake] = data.pop(camel)
    models.update_assignment(assignment_id, data)
    return jsonify({"success": True})


# ── Achievements list ─────────────────────────────────────────────

@api_bp.route('/achievements', methods=['GET'])
def list_achievements():
    return jsonify(models.get_all_achievements())


# ── ID generation helpers ─────────────────────────────────────────

@api_bp.route('/next-id/<entity>', methods=['GET'])
def next_id(entity):
    """Return the next available ID for an entity type.
    Supported entities: class, assign."""
    from database import get_db
    db = get_db()
    if entity == 'class':
        row = db.execute(
            "SELECT class_id FROM classes ORDER BY class_id DESC LIMIT 1"
        ).fetchone()
        n = int(row['class_id'].split('-')[1]) + 1 if row else 1
        return jsonify({"nextId": f"class-{n}"})
    if entity == 'assign':
        row = db.execute(
            "SELECT assignment_id FROM assignments ORDER BY assignment_id DESC LIMIT 1"
        ).fetchone()
        n = int(row['assignment_id'].split('-')[1]) + 1 if row else 1
        return jsonify({"nextId": f"assign-{n}"})
    return jsonify({"error": "Unknown entity"}), 400
