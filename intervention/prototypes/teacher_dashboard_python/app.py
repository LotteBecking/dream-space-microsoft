from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import json
import os
import csv
from datetime import datetime
from data.teacher_storage import (
    get_teacher_profile, save_teacher_profile,
    get_classes, save_classes,
    get_students, save_students,
    get_assignments, save_assignments,
    get_last_lesson, save_last_lesson,
    register_user, verify_user
)
from data.lessons import lessons

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
app.secret_key = os.environ.get('SECRET_KEY', 'teacher-dashboard-dev-key-change-in-production')

# Cache for schools data
_schools_cache = None

def load_schools():
    """Load schools from CSV file with caching"""
    global _schools_cache
    if _schools_cache is not None:
        return _schools_cache
    
    schools = []
    schools_csv_path = os.path.join(os.path.dirname(__file__), 'data', 'schools.csv')
    
    try:
        with open(schools_csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row.get('School Name'):
                    schools.append(row['School Name'].strip())
    except Exception as e:
        print(f"Error loading schools: {e}")
        return []
    
    # Remove duplicates and sort
    _schools_cache = sorted(list(set(schools)))
    return _schools_cache

def build_default_teacher_instructions(lesson):
    """Generate lesson-specific fallback instructions when teacherInstructions are missing."""
    objectives = lesson.get('learningObjectives') or lesson.get('objectives') or []
    first_objective = objectives[0] if objectives else 'the core lesson objective'
    title = lesson.get('title', 'this lesson')

    return {
        'setup': f"Prepare the tools and examples needed to teach {title.lower()}.",
        'steps': [
            'Introduce the lesson goals and connect them to prior knowledge (5 min).',
            f"Demonstrate one core concept focused on {first_objective.lower()} (7 min).",
            'Guide students through a structured practice activity (10 min).',
            'Review outcomes, reflect, and assign the linked exercise (5 min).'
        ],
        'discussionPrompts': [
            f"What part of {title.lower()} feels easiest so far?",
            'What strategy helped you solve a challenge in this lesson?',
            'How could you apply this concept in a different project?'
        ],
        'tips': [
            'Model one example first, then shift quickly to guided practice.',
            'Use pair discussion before independent exercise work.',
            'End with a short reflection to reinforce retention.'
        ]
    }


def normalize_lesson_detail(lesson):
    """Ensure lesson detail has the fields required by the tabbed detail template."""
    detail_lesson = dict(lesson)
    detail_lesson['ageGroup'] = lesson.get('ageGroup') or 'Primary school (ages 8-12)'

    detail_lesson['learningObjectives'] = (
        lesson.get('learningObjectives')
        or lesson.get('objectives')
        or []
    )

    fallback_teacher_instructions = build_default_teacher_instructions(lesson)
    teacher_instructions = lesson.get('teacherInstructions') or {}
    detail_lesson['teacherInstructions'] = {
        'setup': teacher_instructions.get('setup') or fallback_teacher_instructions['setup'],
        'steps': teacher_instructions.get('steps') or fallback_teacher_instructions['steps'],
        'discussionPrompts': teacher_instructions.get('discussionPrompts') or fallback_teacher_instructions['discussionPrompts'],
        'tips': teacher_instructions.get('tips') or fallback_teacher_instructions['tips']
    }

    raw_exercises = lesson.get('studentExercises') or []
    normalized_exercises = []
    for index, exercise in enumerate(raw_exercises, start=1):
        description = exercise.get('description', 'Complete this exercise in the student app.')
        instructions = exercise.get('instructions') or [description]
        success_criteria = exercise.get('successCriteria') or [
            'Students can explain their approach clearly.',
            'Students can complete the task with precise steps.'
        ]

        normalized_exercises.append({
            'id': exercise.get('id', f"{lesson.get('id', 'lesson')}-exercise-{index}"),
            'title': exercise.get('title', f'Exercise {index}'),
            'description': description,
            'type': (exercise.get('type') or 'Coding').capitalize(),
            'difficulty': (exercise.get('difficulty') or lesson.get('level') or 'Beginner').capitalize(),
            'durationMinutes': exercise.get('durationMinutes') or 10,
            'displayMode': exercise.get('displayMode') or 'Whole class',
            'instructions': instructions,
            'materials': exercise.get('materials') or ['Paper and pencil'],
            'successCriteria': success_criteria
        })

    detail_lesson['studentExercises'] = normalized_exercises

    raw_challenges = lesson.get('studentChallenges') or []
    normalized_challenges = []
    for index, challenge in enumerate(raw_challenges, start=1):
        challenge_description = challenge.get('description', 'Complete this classroom challenge.')
        challenge_instructions = challenge.get('instructions') or [challenge_description]
        challenge_success_criteria = challenge.get('successCriteria') or [
            'Students can justify their algorithm design decisions.',
            'Students can revise instructions after testing.'
        ]

        normalized_challenges.append({
            'id': challenge.get('id', f"{lesson.get('id', 'lesson')}-challenge-{index}"),
            'title': challenge.get('title', f'Challenge {index}'),
            'description': challenge_description,
            'type': (challenge.get('type') or 'Challenge').capitalize(),
            'difficulty': (challenge.get('difficulty') or 'Medium').capitalize(),
            'durationMinutes': challenge.get('durationMinutes') or 10,
            'displayMode': challenge.get('displayMode') or 'Whole class',
            'instructions': challenge_instructions,
            'materials': challenge.get('materials') or ['Paper and pencil'],
            'successCriteria': challenge_success_criteria
        })

    detail_lesson['studentChallenges'] = normalized_challenges
    detail_lesson['curriculumAlignment'] = lesson.get('curriculumAlignment') or []

    return detail_lesson

# Routes

@app.route('/')
def home():
    """Teacher dashboard home page"""
    classes = get_classes()
    students = get_students()
    teacher_profile = get_teacher_profile()
    last_lesson_id = get_last_lesson()
    featured_lesson = lessons[0] if lessons else None
    
    # Find last lesson
    last_lesson = None
    if last_lesson_id:
        last_lesson = next((l for l in lessons if l['id'] == last_lesson_id), None)

    # If a lesson was viewed, make it the featured lesson for quick continuation.
    if last_lesson:
        featured_lesson = last_lesson

    previous_lesson = None
    next_lesson = None
    if lessons:
        lesson_index_by_id = {
            lesson.get('id'): index
            for index, lesson in enumerate(lessons)
            if lesson.get('id')
        }

        current_lesson_id = featured_lesson.get('id') if featured_lesson else None
        current_index = lesson_index_by_id.get(current_lesson_id, 0)

        if current_index > 0:
            previous_lesson = lessons[current_index - 1]
        if current_index < len(lessons) - 1:
            next_lesson = lessons[current_index + 1]

    class_name_by_id = {
        class_item.get('id'): class_item.get('name', 'Unknown class')
        for class_item in classes
    }
    top_students = sorted(
        students,
        key=lambda student: (
            student.get('progressPercentage', 0),
            student.get('challengesCompleted', 0)
        ),
        reverse=True
    )[:3]

    leaderboard_students = [
        {
            **student,
            'className': class_name_by_id.get(student.get('classId'), 'Unknown class')
        }
        for student in top_students
    ]

    challenge_completion_counts = {}
    for student in students:
        for activity in student.get('activityHistory', []):
            if activity.get('type') != 'challenge':
                continue
            if not activity.get('success', True):
                continue

            challenge_title = (activity.get('title') or '').strip()
            if not challenge_title:
                continue

            challenge_completion_counts[challenge_title] = challenge_completion_counts.get(challenge_title, 0) + 1

    popular_challenges = [
        {
            'title': challenge_title,
            'completedCount': completion_count
        }
        for challenge_title, completion_count in sorted(
            challenge_completion_counts.items(),
            key=lambda item: item[1],
            reverse=True
        )[:5]
    ]

    lesson_covers = {f'lesson-{i}': f'/static/images/lesson-{i}-cover.jpg' for i in range(1, 17)}

    featured_lesson_cover = None
    if featured_lesson:
        featured_lesson_cover = lesson_covers.get(featured_lesson.get('id'))

    current_hour = datetime.now().hour
    if current_hour < 12:
        day_greeting = 'Good morning'
    elif current_hour < 18:
        day_greeting = 'Good afternoon'
    else:
        day_greeting = 'Good evening'

    teacher_name = session.get('user_username') or teacher_profile.get('name') or 'Teacher'
    teacher_school = session.get('user_school') or teacher_profile.get('school') or 'School not set'
    teacher_class_label = session.get('user_class') or teacher_profile.get('class') or 'Class not set'
    
    # Calculate totals
    total_students = sum(c['studentCount'] for c in classes)
    total_assignments = sum(c['activeAssignments'] for c in classes)
    avg_engagement = round(sum(c['engagementRate'] for c in classes) / len(classes)) if classes else 0
    
    # Check if user is logged in
    is_logged_in = 'user_username' in session
    
    return render_template('home.html',
                         featured_lesson=featured_lesson,
                         last_lesson=last_lesson,
                         previous_lesson=previous_lesson,
                         next_lesson=next_lesson,
                         leaderboard_students=leaderboard_students,
                         popular_challenges=popular_challenges,
                         featured_lesson_cover=featured_lesson_cover,
                         day_greeting=day_greeting,
                         teacher_name=teacher_name,
                         teacher_school=teacher_school,
                         teacher_class_label=teacher_class_label,
                         classes=classes,
                         total_students=total_students,
                         total_assignments=total_assignments,
                         avg_engagement=avg_engagement,
                         is_logged_in=is_logged_in)

@app.route('/lessons')
def lesson_library():
    """Lesson library page"""
    if 'user_username' not in session:
        return redirect(url_for('home'))
    
    search_query = request.args.get('search', '').strip().lower()
    selected_track = request.args.get('track', 'all').strip().lower()
    valid_tracks = {'all', 'primary', 'highschool', 'tv'}

    if selected_track not in valid_tracks:
        selected_track = 'all'

    def lesson_number(lesson):
        lesson_id = lesson.get('id', '')
        if not lesson_id.startswith('lesson-'):
            return None
        try:
            return int(lesson_id.split('-', 1)[1])
        except (TypeError, ValueError):
            return None

    filtered_lessons = list(lessons)

    if selected_track == 'primary':
        filtered_lessons = [
            lesson for lesson in filtered_lessons
            if (lesson_number(lesson) or 0) <= 8
        ]
    elif selected_track == 'highschool':
        filtered_lessons = [
            lesson for lesson in filtered_lessons
            if (lesson_number(lesson) or 0) >= 9
        ]
    elif selected_track == 'tv':
        filtered_lessons = []

    if search_query:
        filtered_lessons = [
            lesson for lesson in filtered_lessons
            if search_query in lesson.get('title', '').lower()
            or search_query in lesson.get('description', '').lower()
        ]

    return render_template(
        'lessons/library.html',
        lessons=filtered_lessons,
        search_query=request.args.get('search', ''),
        selected_track=selected_track
    )

@app.route('/lessons/<lesson_id>')
def lesson_detail(lesson_id):
    """Single lesson detail page"""
    if 'user_username' not in session:
        return redirect(url_for('home'))
    
    lesson = next((l for l in lessons if l['id'] == lesson_id), None)
    
    if not lesson:
        return "Lesson not found", 404
    
    # Save last viewed lesson
    save_last_lesson(lesson_id)

    lesson_detail_data = normalize_lesson_detail(lesson)
    return render_template('lessons/detail.html', lesson=lesson_detail_data)


@app.route('/lessons/<lesson_id>/exercises/<exercise_id>')
def lesson_exercise_present(lesson_id, exercise_id):
    """Big-screen exercise presentation view for in-class use."""
    lesson = next((l for l in lessons if l['id'] == lesson_id), None)

    if not lesson:
        return "Lesson not found", 404

    lesson_detail_data = normalize_lesson_detail(lesson)
    exercises = lesson_detail_data.get('studentExercises') or []
    exercise = next((e for e in exercises if e.get('id') == exercise_id), None)

    if not exercise:
        return "Exercise not found", 404

    exercise_index = next((i for i, e in enumerate(exercises) if e.get('id') == exercise_id), 0)
    previous_exercise_id = exercises[exercise_index - 1]['id'] if exercise_index > 0 else None
    next_exercise_id = exercises[exercise_index + 1]['id'] if exercise_index < len(exercises) - 1 else None

    return render_template(
        'lessons/exercise_present.html',
        lesson=lesson_detail_data,
        exercise=exercise,
        exercise_index=exercise_index,
        exercise_count=len(exercises),
        previous_exercise_id=previous_exercise_id,
        next_exercise_id=next_exercise_id
    )


@app.route('/lessons/<lesson_id>/challenges/<challenge_id>')
def lesson_challenge_present(lesson_id, challenge_id):
    """Big-screen challenge presentation view for in-class use."""
    lesson = next((l for l in lessons if l['id'] == lesson_id), None)

    if not lesson:
        return "Lesson not found", 404

    lesson_detail_data = normalize_lesson_detail(lesson)
    challenges = lesson_detail_data.get('studentChallenges') or []
    challenge = next((c for c in challenges if c.get('id') == challenge_id), None)

    if not challenge:
        return "Challenge not found", 404

    challenge_index = next((i for i, c in enumerate(challenges) if c.get('id') == challenge_id), 0)
    previous_challenge_id = challenges[challenge_index - 1]['id'] if challenge_index > 0 else None
    next_challenge_id = challenges[challenge_index + 1]['id'] if challenge_index < len(challenges) - 1 else None

    return render_template(
        'lessons/challenge_present.html',
        lesson=lesson_detail_data,
        challenge=challenge,
        challenge_index=challenge_index,
        challenge_count=len(challenges),
        previous_challenge_id=previous_challenge_id,
        next_challenge_id=next_challenge_id
    )

@app.route('/classes')
def class_overview():
    """Class management overview"""
    if 'user_username' not in session:
        return redirect(url_for('home'))
    
    classes = get_classes()
    return render_template('classes/overview.html', classes=classes)

@app.route('/students')
def student_list():
    """Student list and filters"""
    if 'user_username' not in session:
        return redirect(url_for('home'))
    
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
    if 'user_username' not in session:
        return redirect(url_for('home'))
    
    students = get_students()
    student = next((s for s in students if s['id'] == student_id), None)
    
    if not student:
        return "Student not found", 404
    
    return render_template('students/profile.html', student=student)

@app.route('/settings')
def profile():
    """Teacher profile settings"""
    if 'user_username' not in session:
        return redirect(url_for('home'))

    stored_profile = get_teacher_profile() or {}
    username = session.get('user_username', '')
    school = session.get('user_school', '')
    email = session.get('user_email', '')

    profile = {
        'name': username or stored_profile.get('name', ''),
        'school': school or stored_profile.get('school', ''),
        'email': email or stored_profile.get('email', ''),
        'avatar': (username[:2].upper() if username else stored_profile.get('avatar', 'TD'))
    }

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

@app.route('/api/schools', methods=['GET'])
def api_get_schools():
    """API endpoint to get school suggestions based on search query"""
    query = request.args.get('q', '').strip().lower()
    
    schools = load_schools()
    
    if not query:
        return jsonify([])
    
    # Filter schools based on query
    matches = [school for school in schools if query in school.lower()]
    
    # Return top 10 matches
    return jsonify(matches[:10])

# Authentication Routes

@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration page"""
    # Show signup form on GET
    if request.method == 'GET':
        return render_template('signup.html')
    
    if request.method == 'POST':
        try:
            username = request.form.get('username', '').strip()
            school = request.form.get('school', '').strip()
            class_group = request.form.get('class', '').strip()
            email = request.form.get('email', '').strip()
            password = request.form.get('password', '').strip()
            confirm_password = request.form.get('confirm_password', '').strip()
            
            # Debug: Print what we're receiving
            print(f"DEBUG Registration - Email received: '{email}' (length: {len(email)})")
            print(f"DEBUG Form data keys: {list(request.form.keys())}")
            
            # Validation
            if not username:
                session['auth_error'] = 'Username is required'
                return redirect(url_for('home'))
            
            if not school:
                session['auth_error'] = 'School is required'
                return redirect(url_for('home'))
            
            if not class_group:
                session['auth_error'] = 'Age group is required'
                return redirect(url_for('home'))
            
            if not email:
                session['auth_error'] = 'Email is required'
                return redirect(url_for('home'))
            
            if not password:
                session['auth_error'] = 'Password is required'
                return redirect(url_for('home'))
            
            if len(password) < 8:
                session['auth_error'] = 'Password must be at least 8 characters'
                return redirect(url_for('home'))
            
            if password != confirm_password:
                session['auth_error'] = 'Passwords do not match'
                return redirect(url_for('home'))
            
            # Register user
            success, message = register_user(username, password, school, class_group, email)
            
            if success:
                # Auto-login after registration and store user info
                session['user_username'] = username
                session['user_email'] = email
                session['user_school'] = school
                session['user_class'] = class_group
                # Show success message
                session['auth_success'] = f'Welcome, {username}! You are now logged in.'
                return redirect(url_for('home'))
            else:
                session['auth_error'] = message
                return redirect(url_for('home'))
        except Exception as e:
            session['auth_error'] = f'An error occurred: {str(e)}'
            return redirect(url_for('home'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login page"""
    # Redirect GET requests to home (which shows the signup form)
    if request.method == 'GET':
        return redirect(url_for('home'))
    
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()
        
        print(f"DEBUG login route: Received email: '{email}', password length: {len(password)}")
        
        if not email or not password:
            session['auth_error'] = 'Email and password are required'
            session['show_login_form'] = True
        else:
            success, user_data = verify_user(email, password)
            
            print(f"DEBUG login route: verify_user returned success={success}, user_data={user_data}")
            
            if success and user_data:
                # Clear the show_login_form flag on successful login
                session.pop('show_login_form', None)
                # Store user data in session
                session['user_username'] = user_data.get('username', user_data.get('email', ''))
                session['user_email'] = user_data.get('email', '')
                session['user_school'] = user_data.get('school', '')
                session['user_class'] = user_data.get('class', '')
                session['is_logged_in'] = True
                print(f"DEBUG login route: User logged in successfully")
                return redirect(url_for('home'))
            else:
                session['auth_error'] = 'Invalid email or password'
                session['show_login_form'] = True
                print(f"DEBUG login route: Login failed")
        
        # Render signup form with login form visible and error message
        return render_template('signup.html')

@app.route('/logout')
def logout():
    """Logout user"""
    session.clear()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True, port=5001, use_reloader=False)
