"""Auth API: signup, login, logout, join class by code, teacher adds student."""

from flask import Blueprint, request, jsonify, g

import models
from database import get_db
from auth import (
    hash_password, verify_password, create_session, delete_session,
    require_auth, require_role, generate_class_code,
)
from validators import validate_id

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')


# ── Signup ─────────────────────────────────────────────────────────

@auth_bp.route('/signup', methods=['POST'])
def signup():
    """Create a new teacher or student account.

    Body: { email, password, name, role: "teacher"|"student" }
    Optional for student: { age }
    """
    data = request.get_json(silent=True) or {}
    email = (data.get('email') or '').strip().lower()
    password = data.get('password', '')
    name = (data.get('name') or '').strip()
    role = data.get('role', '')

    if not email or not password or not name:
        return jsonify({"error": "email, password, and name are required"}), 400
    if len(password) < 6:
        return jsonify({"error": "Password must be at least 6 characters"}), 400
    if role not in ('teacher', 'student'):
        return jsonify({"error": "role must be 'teacher' or 'student'"}), 400

    db = get_db()

    # Check for duplicate email
    if db.execute('SELECT 1 FROM accounts WHERE email=?', (email,)).fetchone():
        return jsonify({"error": "Email already registered"}), 409

    pw_hash = hash_password(password)
    teacher_id = None
    student_id = None

    if role == 'teacher':
        cur = db.execute(
            'INSERT INTO teacher_profiles (name, email, avatar) VALUES (?,?,?)',
            (name, email, name[:2].upper()))
        teacher_id = cur.lastrowid
    else:
        # Auto-generate next student_id
        row = db.execute(
            "SELECT student_id FROM students ORDER BY LENGTH(student_id) DESC, student_id DESC LIMIT 1"
        ).fetchone()
        if row:
            last_num = int(row['student_id'].split('-')[1])
            student_id = f"student-{last_num + 1}"
        else:
            student_id = "student-1"

        avatar = name[:2].upper()
        db.execute(
            '''INSERT INTO students
               (student_id, name, avatar, progress_percentage,
                challenges_completed, lessons_completed, last_activity, teacher_notes)
               VALUES (?,?,?,0,0,0,'','')''',
            (student_id, name, avatar))

    db.execute(
        '''INSERT INTO accounts (email, password_hash, role, display_name, teacher_id, student_id)
           VALUES (?,?,?,?,?,?)''',
        (email, pw_hash, role, name, teacher_id, student_id))
    db.commit()

    # Auto-login: create session
    account = db.execute('SELECT * FROM accounts WHERE email=?', (email,)).fetchone()
    token, expires = create_session(account['id'])

    return jsonify({
        "success": True,
        "token": token,
        "expires": expires,
        "role": role,
        "studentId": student_id,
        "teacherId": teacher_id,
        "name": name,
    }), 201


# ── Login ──────────────────────────────────────────────────────────

@auth_bp.route('/login', methods=['POST'])
def login():
    """Authenticate with email + password.

    Body: { email, password }
    Returns: { token, role, studentId|teacherId, name }
    """
    data = request.get_json(silent=True) or {}
    email = (data.get('email') or '').strip().lower()
    password = data.get('password', '')

    if not email or not password:
        return jsonify({"error": "email and password are required"}), 400

    db = get_db()
    account = db.execute(
        'SELECT * FROM accounts WHERE email=?', (email,)
    ).fetchone()

    if not account or not verify_password(password, account['password_hash']):
        return jsonify({"error": "Invalid email or password"}), 401

    token, expires = create_session(account['id'])

    return jsonify({
        "success": True,
        "token": token,
        "expires": expires,
        "role": account['role'],
        "studentId": account['student_id'],
        "teacherId": account['teacher_id'],
        "name": account['display_name'],
    })


# ── Logout ─────────────────────────────────────────────────────────

@auth_bp.route('/logout', methods=['POST'])
@require_auth
def logout():
    token = request.headers.get('Authorization', '')[7:]
    delete_session(token)
    return jsonify({"success": True})


# ── Who am I ───────────────────────────────────────────────────────

@auth_bp.route('/me', methods=['GET'])
@require_auth
def me():
    a = g.account
    return jsonify({
        "id": a['id'],
        "email": a['email'],
        "role": a['role'],
        "name": a['display_name'],
        "studentId": a['student_id'],
        "teacherId": a['teacher_id'],
    })


# ── Class codes (teacher creates, student joins) ─────────────────

@auth_bp.route('/class-code', methods=['POST'])
@require_auth
@require_role('teacher')
def create_class_code():
    """Generate a join code for a class.

    Body: { class_id }
    """
    data = request.get_json(silent=True) or {}
    class_id = data.get('class_id') or data.get('classId', '')
    if not validate_id(class_id, 'class_id'):
        return jsonify({"error": "Invalid class_id"}), 400

    if not models.get_class(class_id):
        return jsonify({"error": "Class not found"}), 404

    db = get_db()
    existing = db.execute(
        'SELECT code FROM class_codes WHERE class_id=?', (class_id,)
    ).fetchone()
    if existing:
        return jsonify({"success": True, "code": existing['code'], "classId": class_id})

    code = generate_class_code()
    db.execute(
        'INSERT INTO class_codes (code, class_id) VALUES (?,?)',
        (code, class_id))
    db.commit()

    return jsonify({"success": True, "code": code, "classId": class_id}), 201


@auth_bp.route('/join-class', methods=['POST'])
@require_auth
@require_role('student')
def join_class():
    """Student joins a class using a code.

    Body: { code }
    """
    data = request.get_json(silent=True) or {}
    code = (data.get('code') or '').strip().upper()
    if not code:
        return jsonify({"error": "code is required"}), 400

    db = get_db()
    row = db.execute(
        'SELECT class_id FROM class_codes WHERE code=?', (code,)
    ).fetchone()
    if not row:
        return jsonify({"error": "Invalid class code"}), 404

    class_id = row['class_id']
    student_id = g.account['student_id']
    if not student_id:
        return jsonify({"error": "Account has no student profile"}), 400

    db.execute(
        'UPDATE students SET class_id=?, updated_at=CURRENT_TIMESTAMP WHERE student_id=?',
        (class_id, student_id))
    count = db.execute(
        'SELECT COUNT(*) as c FROM students WHERE class_id=?', (class_id,)
    ).fetchone()['c']
    db.execute(
        'UPDATE classes SET student_count=? WHERE class_id=?',
        (count, class_id))
    db.commit()

    return jsonify({
        "success": True,
        "classId": class_id,
        "studentId": student_id,
    })


@auth_bp.route('/add-student-to-class', methods=['POST'])
@require_auth
@require_role('teacher')
def add_student_to_class():
    """Teacher directly adds a student to a class.

    Body: { student_id, class_id }
    """
    data = request.get_json(silent=True) or {}
    student_id = data.get('student_id') or data.get('studentId', '')
    class_id = data.get('class_id') or data.get('classId', '')

    if not validate_id(student_id, 'student_id'):
        return jsonify({"error": "Invalid student_id"}), 400
    if not validate_id(class_id, 'class_id'):
        return jsonify({"error": "Invalid class_id"}), 400

    if not models.get_student(student_id):
        return jsonify({"error": "Student not found"}), 404
    if not models.get_class(class_id):
        return jsonify({"error": "Class not found"}), 404

    db = get_db()
    db.execute(
        'UPDATE students SET class_id=?, updated_at=CURRENT_TIMESTAMP WHERE student_id=?',
        (class_id, student_id))
    count = db.execute(
        'SELECT COUNT(*) as c FROM students WHERE class_id=?', (class_id,)
    ).fetchone()['c']
    db.execute(
        'UPDATE classes SET student_count=? WHERE class_id=?',
        (count, class_id))
    db.commit()

    return jsonify({"success": True, "studentId": student_id, "classId": class_id})


@auth_bp.route('/class-code-lookup', methods=['GET'])
def class_code_lookup():
    """Look up an existing class code by class_id.

    Query param: ?classId=class-1
    """
    class_id = request.args.get('classId') or request.args.get('class_id', '')
    if not class_id:
        return jsonify({"error": "classId is required"}), 400

    db = get_db()
    row = db.execute(
        'SELECT code FROM class_codes WHERE class_id=?', (class_id,)
    ).fetchone()
    if not row:
        return jsonify({"code": None}), 200
    return jsonify({"code": row['code'], "classId": class_id})
