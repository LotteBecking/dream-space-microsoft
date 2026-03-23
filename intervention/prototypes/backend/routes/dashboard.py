"""Teacher-dashboard HTML routes.

These replicate the existing teacher_dashboard_python views
but read from the SQLite database instead of JSON flat files.
"""

from flask import Blueprint, render_template, request

import models
from lesson_loader import load_lessons, search_lessons, get_lesson_by_id
import config

dashboard_bp = Blueprint('dashboard', __name__)

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
    lessons = _get_lessons()
    classes = models.get_all_classes()
    last_lesson_id = models.get_last_lesson()
    featured_lesson = lessons[0] if lessons else None

    last_lesson = None
    if last_lesson_id:
        last_lesson = get_lesson_by_id(lessons, last_lesson_id)

    total_students = sum(c['studentCount'] for c in classes)
    total_assignments = sum(c['activeAssignments'] for c in classes)
    avg_engagement = (
        round(sum(c['engagementRate'] for c in classes) / len(classes))
        if classes else 0
    )

    return render_template(
        'home.html',
        featured_lesson=featured_lesson,
        last_lesson=last_lesson,
        classes=classes,
        total_students=total_students,
        total_assignments=total_assignments,
        avg_engagement=avg_engagement,
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
