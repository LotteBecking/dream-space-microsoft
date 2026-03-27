"""Teacher-dashboard HTML routes.

These replicate the existing teacher_dashboard_python views
but read from the SQLite database instead of JSON flat files.
"""

from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, session

import models
from lesson_loader import load_lessons, search_lessons, get_lesson_by_id
import config
from database import get_db
from auth import hash_password, verify_password, create_session

dashboard_bp = Blueprint('dashboard', __name__)


# ── Auth helpers ────────────────────────────────────────────────────

def _email_for(username):
    """Stable email derived from a legacy username."""
    return f"{username.strip().lower()}@teacher.local"


def _is_logged_in():
    return bool(session.get('user_username'))


# ── Auth pages & form handlers ──────────────────────────────────────

@dashboard_bp.route('/login', methods=['GET', 'POST'])
def login_page():
    if request.method == 'GET':
        return render_template('login.html')

    username = request.form.get('username', '').strip()
    password = request.form.get('password', '')

    if not username or not password:
        session['auth_error'] = 'Username and password are required.'
        return redirect(url_for('dashboard.login_page'))

    db = get_db()
    account = db.execute(
        'SELECT * FROM accounts WHERE email=?', (_email_for(username),)
    ).fetchone()

    if not account or not verify_password(password, account['password_hash']):
        session['auth_error'] = 'Invalid username or password.'
        return redirect(url_for('dashboard.login_page'))

    session['user_username'] = account['display_name']
    session['user_school'] = ''
    session.permanent = True
    return redirect(url_for('dashboard.home'))


@dashboard_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return redirect(url_for('dashboard.home'))

    username = request.form.get('username', '').strip()
    school = request.form.get('school', '').strip()
    password = request.form.get('password', '')
    confirm = request.form.get('confirm_password', '')

    if not username or not school or not password:
        session['auth_error'] = 'All fields are required.'
        return redirect(url_for('dashboard.home'))

    if len(password) < 8:
        session['auth_error'] = 'Password must be at least 8 characters.'
        return redirect(url_for('dashboard.home'))

    if password != confirm:
        session['auth_error'] = 'Passwords do not match.'
        return redirect(url_for('dashboard.home'))

    db = get_db()
    email = _email_for(username)

    if db.execute('SELECT 1 FROM accounts WHERE email=?', (email,)).fetchone():
        session['auth_error'] = 'Username already taken.'
        return redirect(url_for('dashboard.home'))

    cur = db.execute(
        'INSERT INTO teacher_profiles (name, email, school, avatar) VALUES (?,?,?,?)',
        (username, email, school, username[:2].upper())
    )
    teacher_id = cur.lastrowid

    db.execute(
        '''INSERT INTO accounts (email, password_hash, role, display_name, teacher_id)
           VALUES (?,?,?,?,?)''',
        (email, hash_password(password), 'teacher', username, teacher_id)
    )
    db.commit()

    session['user_username'] = username
    session['user_school'] = school
    session.permanent = True
    return redirect(url_for('dashboard.home'))


@dashboard_bp.route('/signup')
def signup_page():
    return render_template('signup.html')


@dashboard_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('dashboard.home'))


# Lesson JSON files are loaded once at import time; the list is refreshed on
# each request for simplicity (lessons are small and cached by the OS).
_lessons = None


def _get_lessons():
    global _lessons
    if _lessons is None:
        _lessons = load_lessons(config.LESSON_CONTENT_DIR)
    return _lessons


# ── helpers (copied from the original app.py) ──────────────────────

def _default_teacher_instructions(lesson):
    objectives = lesson.get('learningObjectives') or lesson.get('objectives') or []
    first_obj = objectives[0] if objectives else 'the core lesson objective'
    title = lesson.get('title', 'this lesson')
    return {
        'setup': f"Prepare the tools and examples needed to teach {title.lower()}.",
        'steps': [
            'Introduce the lesson goals and connect them to prior knowledge (5 min).',
            f"Demonstrate one core concept focused on {first_obj.lower()} (7 min).",
            'Guide students through a structured practice activity (10 min).',
            'Review outcomes, reflect, and assign the linked exercise (5 min).',
        ],
        'discussionPrompts': [
            f"What part of {title.lower()} feels easiest so far?",
            'What strategy helped you solve a challenge in this lesson?',
            'How could you apply this concept in a different project?',
        ],
        'tips': [
            'Model one example first, then shift quickly to guided practice.',
            'Use pair discussion before independent exercise work.',
            'End with a short reflection to reinforce retention.',
        ],
    }


def _normalize_lesson_detail(lesson):
    detail = dict(lesson)
    detail['learningObjectives'] = (
        lesson.get('learningObjectives')
        or lesson.get('objectives')
        or []
    )
    fallback = _default_teacher_instructions(lesson)
    ti = lesson.get('teacherInstructions') or {}
    detail['teacherInstructions'] = {
        'setup': ti.get('setup') or fallback['setup'],
        'steps': ti.get('steps') or fallback['steps'],
        'discussionPrompts': ti.get('discussionPrompts') or fallback['discussionPrompts'],
        'tips': ti.get('tips') or fallback['tips'],
    }
    raw_ex = lesson.get('studentExercises') or []
    normalized = []
    for idx, ex in enumerate(raw_ex, 1):
        normalized.append({
            'id': ex.get('id', f"{lesson.get('id', 'lesson')}-exercise-{idx}"),
            'title': ex.get('title', f'Exercise {idx}'),
            'description': ex.get('description', 'Complete this exercise in the student app.'),
            'type': (ex.get('type') or 'Coding').capitalize(),
            'difficulty': (ex.get('difficulty') or lesson.get('level') or 'Beginner').capitalize(),
        })
    detail['studentExercises'] = normalized
    detail['curriculumAlignment'] = lesson.get('curriculumAlignment') or []
    return detail


# ── routes ──────────────────────────────────────────────────────────

@dashboard_bp.route('/')
def home():
    logged_in = _is_logged_in()

    lessons = _get_lessons()
    classes = models.get_all_classes()
    last_lesson_id = models.get_last_lesson()
    featured_lesson = lessons[0] if lessons else None

    last_lesson = None
    if last_lesson_id:
        last_lesson = get_lesson_by_id(lessons, last_lesson_id)

    # Adjacent lesson navigation
    previous_lesson = None
    next_lesson = None
    if featured_lesson and lessons:
        idx = next((i for i, l in enumerate(lessons) if l.get('id') == featured_lesson.get('id')), 0)
        if idx > 0:
            previous_lesson = lessons[idx - 1]
        if idx < len(lessons) - 1:
            next_lesson = lessons[idx + 1]

    total_students = sum(c['studentCount'] for c in classes)
    total_assignments = sum(c['activeAssignments'] for c in classes)
    avg_engagement = (
        round(sum(c['engagementRate'] for c in classes) / len(classes))
        if classes else 0
    )

    # Leaderboard: top 3 students by progress
    class_name_by_id = {c['id']: c['name'] for c in classes}
    all_students = models.get_all_students() if logged_in else []
    top_students = sorted(
        all_students,
        key=lambda s: (s.get('progressPercentage', 0), s.get('challengesCompleted', 0)),
        reverse=True
    )[:3]
    leaderboard_students = [
        {**s, 'className': class_name_by_id.get(s.get('classId'), '')}
        for s in top_students
    ]

    # Popular challenges from activity logs
    challenge_counts = {}
    for s in all_students:
        for act in s.get('activityHistory', []):
            if act.get('type') == 'challenge' and act.get('success'):
                title = (act.get('title') or '').strip()
                if title:
                    challenge_counts[title] = challenge_counts.get(title, 0) + 1
    popular_challenges = [
        {'title': t, 'completedCount': c}
        for t, c in sorted(challenge_counts.items(), key=lambda x: x[1], reverse=True)[:5]
    ]

    # Day greeting
    hour = datetime.now().hour
    if hour < 12:
        day_greeting = 'Good morning'
    elif hour < 18:
        day_greeting = 'Good afternoon'
    else:
        day_greeting = 'Good evening'

    return render_template(
        'home.html',
        is_logged_in=logged_in,
        teacher_name=session.get('user_username', 'Teacher'),
        teacher_school=session.get('user_school', ''),
        teacher_class_label='Groep 7-8',
        day_greeting=day_greeting,
        featured_lesson=featured_lesson,
        featured_lesson_cover=None,
        last_lesson=last_lesson,
        previous_lesson=previous_lesson,
        next_lesson=next_lesson,
        classes=classes,
        total_students=total_students,
        total_assignments=total_assignments,
        avg_engagement=avg_engagement,
        leaderboard_students=leaderboard_students,
        popular_challenges=popular_challenges,
    )


@dashboard_bp.route('/lessons')
def lesson_library():
    lessons = _get_lessons()
    q = request.args.get('search', '')
    filtered = search_lessons(lessons, q) if q else lessons
    return render_template('lessons/library.html',
                           lessons=filtered, search_query=q)


@dashboard_bp.route('/lessons/<lesson_id>')
def lesson_detail(lesson_id):
    lessons = _get_lessons()
    lesson = get_lesson_by_id(lessons, lesson_id)
    if not lesson:
        return "Lesson not found", 404
    models.save_last_lesson(1, lesson_id)  # teacher_id=1 (default)
    return render_template('lessons/detail.html',
                           lesson=_normalize_lesson_detail(lesson))


@dashboard_bp.route('/classes')
def class_overview():
    return render_template('classes/overview.html',
                           classes=models.get_all_classes())


@dashboard_bp.route('/students')
def student_list():
    class_id = request.args.get('class')
    students = models.get_all_students(class_id)
    classes = models.get_all_classes()
    return render_template('students/list.html',
                           students=students,
                           classes=classes,
                           selected_class=class_id)


@dashboard_bp.route('/students/<student_id>')
def student_profile(student_id):
    student = models.get_student(student_id)
    if not student:
        return "Student not found", 404
    return render_template('students/profile.html', student=student)


@dashboard_bp.route('/settings')
def profile():
    return render_template('profile.html',
                           profile=models.get_teacher_profile())
