from flask import Flask, render_template, request, jsonify
import json
import os
from datetime import datetime
from data.teacher_storage import (
    get_teacher_profile, save_teacher_profile,
    get_classes, save_classes,
    get_students, save_students,
    get_assignments, save_assignments,
    get_last_lesson, save_last_lesson
)
from data.lessons import lessons

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

DEFAULT_TEACHER_INSTRUCTIONS = {
    'setup': 'Prepare colorful blocks or printed pattern cards for hands-on activities',
    'steps': [
        'Start with the video introduction (5 min)',
        'Do a physical pattern activity with blocks (5 min)',
        'Discuss how patterns exist in nature and daily life (3 min)',
        'Guide students through the coding exercise (10 min)'
    ],
    'discussionPrompts': [
        'Where do you see patterns in your daily life?',
        'What makes a pattern a pattern?',
        'How could patterns help us write less code?'
    ],
    'tips': [
        'Use real-world examples that students can relate to',
        'Encourage students to create their own patterns',
        'Connect patterns to music or art for deeper engagement'
    ]
}


def normalize_lesson_detail(lesson):
    """Ensure lesson detail has the fields required by the tabbed detail template."""
    detail_lesson = dict(lesson)

    detail_lesson['learningObjectives'] = (
        lesson.get('learningObjectives')
        or lesson.get('objectives')
        or []
    )

    teacher_instructions = lesson.get('teacherInstructions') or {}
    detail_lesson['teacherInstructions'] = {
        'setup': teacher_instructions.get('setup') or DEFAULT_TEACHER_INSTRUCTIONS['setup'],
        'steps': teacher_instructions.get('steps') or DEFAULT_TEACHER_INSTRUCTIONS['steps'],
        'discussionPrompts': teacher_instructions.get('discussionPrompts') or DEFAULT_TEACHER_INSTRUCTIONS['discussionPrompts'],
        'tips': teacher_instructions.get('tips') or DEFAULT_TEACHER_INSTRUCTIONS['tips']
    }

    raw_exercises = lesson.get('studentExercises') or []
    normalized_exercises = []
    for index, exercise in enumerate(raw_exercises, start=1):
        normalized_exercises.append({
            'id': exercise.get('id', f"{lesson.get('id', 'lesson')}-exercise-{index}"),
            'title': exercise.get('title', f'Exercise {index}'),
            'description': exercise.get('description', 'Complete this exercise in the student app.'),
            'type': (exercise.get('type') or 'Coding').capitalize(),
            'difficulty': (exercise.get('difficulty') or lesson.get('level') or 'Beginner').capitalize()
        })

    detail_lesson['studentExercises'] = normalized_exercises
    detail_lesson['curriculumAlignment'] = lesson.get('curriculumAlignment') or []

    return detail_lesson

# Routes

@app.route('/')
def home():
    """Teacher dashboard home page"""
    classes = get_classes()
    last_lesson_id = get_last_lesson()
    featured_lesson = lessons[0] if lessons else None
    
    # Find last lesson
    last_lesson = None
    if last_lesson_id:
        last_lesson = next((l for l in lessons if l['id'] == last_lesson_id), None)
    
    # Calculate totals
    total_students = sum(c['studentCount'] for c in classes)
    total_assignments = sum(c['activeAssignments'] for c in classes)
    avg_engagement = round(sum(c['engagementRate'] for c in classes) / len(classes)) if classes else 0
    
    return render_template('home.html',
                         featured_lesson=featured_lesson,
                         last_lesson=last_lesson,
                         classes=classes,
                         total_students=total_students,
                         total_assignments=total_assignments,
                         avg_engagement=avg_engagement)

@app.route('/lessons')
def lesson_library():
    """Lesson library page"""
    search_query = request.args.get('search', '').lower()
    
    filtered_lessons = lessons
    if search_query:
        filtered_lessons = [l for l in lessons 
                           if search_query in l['title'].lower() 
                           or search_query in l['description'].lower()]
    
    return render_template('lessons/library.html', lessons=filtered_lessons, search_query=request.args.get('search', ''))

@app.route('/lessons/<lesson_id>')
def lesson_detail(lesson_id):
    """Single lesson detail page"""
    lesson = next((l for l in lessons if l['id'] == lesson_id), None)
    
    if not lesson:
        return "Lesson not found", 404
    
    # Save last viewed lesson
    save_last_lesson(lesson_id)

    lesson_detail_data = normalize_lesson_detail(lesson)
    return render_template('lessons/detail.html', lesson=lesson_detail_data)

@app.route('/classes')
def class_overview():
    """Class management overview"""
    classes = get_classes()
    return render_template('classes/overview.html', classes=classes)

@app.route('/students')
def student_list():
    """Student list and filters"""
    class_id = request.args.get('class')
    students = get_students()
    classes = get_classes()
    
    filtered_students = students
    if class_id:
        filtered_students = [s for s in students if s['classId'] == class_id]
    
    return render_template('students/list.html', 
                         students=filtered_students, 
                         classes=classes,
                         selected_class=class_id)

@app.route('/students/<student_id>')
def student_profile(student_id):
    """Detailed student progress page"""
    students = get_students()
    student = next((s for s in students if s['id'] == student_id), None)
    
    if not student:
        return "Student not found", 404
    
    return render_template('students/profile.html', student=student)

@app.route('/settings')
def profile():
    """Teacher profile settings"""
    profile = get_teacher_profile()
    return render_template('profile.html', profile=profile)

# API Routes

@app.route('/api/profile', methods=['GET', 'POST'])
def api_profile():
    if request.method == 'POST':
        data = request.json
        save_teacher_profile(data)
        return jsonify({"success": True})
    
    profile = get_teacher_profile()
    return jsonify(profile or {})

@app.route('/api/classes', methods=['GET'])
def api_classes():
    classes = get_classes()
    return jsonify(classes)

@app.route('/api/students', methods=['GET'])
def api_students():
    students = get_students()
    return jsonify(students)


@app.route('/api/students/<student_id>/avatar', methods=['POST'])
def api_update_student_avatar(student_id):
    data = request.json or {}
    avatar = (data.get('avatar') or '').strip()

    if not avatar:
        return jsonify({"success": False, "error": "Avatar is required"}), 400

    if len(avatar) > 8:
        return jsonify({"success": False, "error": "Avatar is too long"}), 400

    students = get_students()
    student = next((s for s in students if s['id'] == student_id), None)
    if not student:
        return jsonify({"success": False, "error": "Student not found"}), 404

    student['avatar'] = avatar
    save_students(students)

    return jsonify({"success": True, "studentId": student_id, "avatar": avatar})

if __name__ == '__main__':
    app.run(debug=True)
