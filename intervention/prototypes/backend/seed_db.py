"""Populate dreamspace.db with the default data that ships with the
teacher-dashboard and kids-learning-app prototypes.

Usage:
    python seed_db.py          # creates / re-seeds the database
    python seed_db.py --force  # drops all data first
"""

import json
import sys
from app import create_app
from database import get_db

# ═══════════════════════════════════════════════════════════════════
#  Seed data – mirrors teacher_storage.py defaults & ChallengeData
# ═══════════════════════════════════════════════════════════════════

TEACHER_PROFILE = {
    'name': 'Sarah Johnson',
    'email': 'sarah.johnson@school.edu',
    'school': 'Kennedy Elementary School',
    'avatar': 'SJ',
}

CLASSES = [
    {'class_id': 'class-1', 'name': 'Class 4A', 'student_count': 24,
     'active_assignments': 3, 'engagement_rate': 87},
    {'class_id': 'class-2', 'name': 'Class 4B', 'student_count': 22,
     'active_assignments': 2, 'engagement_rate': 92},
    {'class_id': 'class-3', 'name': 'Class 5A', 'student_count': 20,
     'active_assignments': 4, 'engagement_rate': 78},
]

STUDENTS = [
    {'student_id': 'student-1',  'name': 'Emma Wilson',     'avatar': 'EW', 'class_id': 'class-1', 'progress_percentage': 75, 'challenges_completed': 12, 'lessons_completed': 5, 'last_activity': '2 hours ago', 'teacher_notes': 'Emma shows great promise. Very attentive during class.'},
    {'student_id': 'student-2',  'name': 'Liam Chen',       'avatar': 'LC', 'class_id': 'class-1', 'progress_percentage': 82, 'challenges_completed': 15, 'lessons_completed': 7, 'last_activity': '30 minutes ago', 'teacher_notes': 'Excellent progress. Helping other students.'},
    {'student_id': 'student-3',  'name': 'Marcus Brown',    'avatar': 'MB', 'class_id': 'class-1', 'progress_percentage': 45, 'challenges_completed': 6,  'lessons_completed': 2, 'last_activity': '1 day ago', 'teacher_notes': 'Needs additional support. Meeting scheduled.'},
    {'student_id': 'student-4',  'name': 'Sofia Garcia',    'avatar': 'SG', 'class_id': 'class-1', 'progress_percentage': 88, 'challenges_completed': 18, 'lessons_completed': 8, 'last_activity': '1 hour ago', 'teacher_notes': 'Outstanding student. Role model for others.'},
    {'student_id': 'student-5',  'name': 'James Park',      'avatar': 'JP', 'class_id': 'class-1', 'progress_percentage': 68, 'challenges_completed': 10, 'lessons_completed': 4, 'last_activity': '45 minutes ago', 'teacher_notes': 'Good progress. Enjoys visual learning.'},
    {'student_id': 'student-6',  'name': 'Olivia Martinez', 'avatar': 'OM', 'class_id': 'class-2', 'progress_percentage': 92, 'challenges_completed': 20, 'lessons_completed': 9, 'last_activity': '20 minutes ago', 'teacher_notes': 'Class leader in coding challenges.'},
    {'student_id': 'student-7',  'name': 'Noah Johnson',    'avatar': 'NJ', 'class_id': 'class-2', 'progress_percentage': 61, 'challenges_completed': 9,  'lessons_completed': 3, 'last_activity': '3 hours ago', 'teacher_notes': 'Progressing steadily. Prefers group work.'},
    {'student_id': 'student-8',  'name': 'Ava Taylor',      'avatar': 'AT', 'class_id': 'class-2', 'progress_percentage': 79, 'challenges_completed': 14, 'lessons_completed': 6, 'last_activity': '2 hours ago', 'teacher_notes': 'Consistent high quality work.'},
    {'student_id': 'student-9',  'name': 'Noah Lee',        'avatar': 'NL', 'class_id': 'class-2', 'progress_percentage': 55, 'challenges_completed': 7,  'lessons_completed': 2, 'last_activity': '5 hours ago', 'teacher_notes': 'Needs encouragement. New to coding.'},
    {'student_id': 'student-10', 'name': 'Grace Kim',       'avatar': 'GK', 'class_id': 'class-3', 'progress_percentage': 85, 'challenges_completed': 16, 'lessons_completed': 7, 'last_activity': '1 hour ago', 'teacher_notes': 'Creative problem solver.'},
    {'student_id': 'student-11', 'name': 'Henry Davis',     'avatar': 'HD', 'class_id': 'class-3', 'progress_percentage': 71, 'challenges_completed': 11, 'lessons_completed': 5, 'last_activity': '4 hours ago', 'teacher_notes': 'Making good progress.'},
]

ACHIEVEMENTS = [
    {'achievement_id': 'ach-1', 'name': 'First Steps',    'icon': 'star',      'description': 'Completed your first lesson'},
    {'achievement_id': 'ach-2', 'name': 'Quick Learner',   'icon': 'zap',       'description': 'Completed 5 lessons'},
    {'achievement_id': 'ach-3', 'name': 'Problem Solver',  'icon': 'lightbulb', 'description': 'Completed 10 challenges'},
]

STUDENT_ACHIEVEMENTS = [
    ('student-1',  'ach-1', '2024-01-15'),
    ('student-1',  'ach-2', '2024-02-20'),
    ('student-2',  'ach-1', '2024-01-10'),
    ('student-4',  'ach-1', '2024-01-05'),
    ('student-4',  'ach-2', '2024-02-15'),
    ('student-4',  'ach-3', '2024-03-01'),
    ('student-5',  'ach-1', '2024-01-20'),
    ('student-6',  'ach-1', '2024-01-02'),
    ('student-6',  'ach-2', '2024-02-08'),
    ('student-8',  'ach-1', '2024-01-12'),
    ('student-10', 'ach-1', '2024-01-08'),
]

ACTIVITY_LOG = [
    {'activity_id': 'act-1', 'student_id': 'student-1', 'activity_type': 'lesson',    'title': 'Loops & Sequences',   'activity_date': '2024-03-15', 'success': 1},
    {'activity_id': 'act-2', 'student_id': 'student-1', 'activity_type': 'challenge', 'title': 'Pattern Challenge',   'activity_date': '2024-03-10', 'success': 1},
    {'activity_id': 'act-3', 'student_id': 'student-2', 'activity_type': 'lesson',    'title': 'Variables & Data Types', 'activity_date': '2024-03-16', 'success': 1},
]

ASSIGNMENTS = [
    {'assignment_id': 'assign-1', 'lesson_id': 'lesson-1', 'class_id': 'class-1', 'assigned_date': '2024-03-10', 'due_date': '2024-03-17', 'completion_rate': 85},
    {'assignment_id': 'assign-2', 'lesson_id': 'lesson-2', 'class_id': 'class-1', 'assigned_date': '2024-03-12', 'due_date': '2024-03-19', 'completion_rate': 70},
]

LESSONS_META = [
    {'lesson_id': 'lesson-1', 'title': 'Introduction to Block Coding', 'description': 'Learn the basics of block-based programming.', 'duration': 15, 'level': 'Beginner', 'video_url': 'https://www.youtube.com/embed/MEzGyRb0LnY'},
    {'lesson_id': 'lesson-2', 'title': 'Loops & Sequences',            'description': 'Master loops and sequential execution.',       'duration': 20, 'level': 'Beginner'},
    {'lesson_id': 'lesson-3', 'title': 'Variables & Data Types',        'description': 'Store and manipulate different types of data.','duration': 25, 'level': 'Intermediate'},
    {'lesson_id': 'lesson-4', 'title': 'Conditionals & Decision Making','description': 'Make decisions with if-then-else logic.',     'duration': 30, 'level': 'Intermediate'},
    {'lesson_id': 'lesson-5', 'title': 'Functions & Procedures',        'description': 'Create reusable blocks of code.',             'duration': 25, 'level': 'Advanced'},
    {'lesson_id': 'lesson-6', 'title': 'Debugging & Problem Solving',   'description': 'Find and fix errors systematically.',         'duration': 20, 'level': 'Intermediate'},
    {'lesson_id': 'lesson-7', 'title': 'Game Development Basics',       'description': 'Build simple interactive games.',             'duration': 40, 'level': 'Advanced'},
    {'lesson_id': 'lesson-8', 'title': 'Arrays & Lists',                'description': 'Work with collections of data.',              'duration': 30, 'level': 'Advanced'},
]

EXERCISES = [
    # lesson-1
    {'exercise_id': 'exercise-1-1', 'lesson_id': 'lesson-1', 'title': 'Drag Your First Block',    'description': 'Drag a simple block and see what happens',            'difficulty': 'Easy',         'sort_order': 1},
    {'exercise_id': 'exercise-1-2', 'lesson_id': 'lesson-1', 'title': 'Create a Sequence',        'description': 'Connect multiple blocks in order',                    'difficulty': 'Easy',         'sort_order': 2},
    {'exercise_id': 'exercise-1-3', 'lesson_id': 'lesson-1', 'title': 'Build a Simple Program',   'description': 'Create a complete block program that moves a character','difficulty': 'Medium',       'sort_order': 3},
    # lesson-2
    {'exercise_id': 'exercise-2-1', 'lesson_id': 'lesson-2', 'title': 'Simple Loop',              'description': 'Create a loop that repeats an action',                'difficulty': 'Easy',         'sort_order': 1},
    {'exercise_id': 'exercise-2-2', 'lesson_id': 'lesson-2', 'title': 'Pattern with Loops',       'description': 'Use loops to create a repeating pattern',             'difficulty': 'Medium',       'sort_order': 2},
    {'exercise_id': 'exercise-2-3', 'lesson_id': 'lesson-2', 'title': 'Nested Loops',             'description': 'Create loops inside loops',                           'difficulty': 'Hard',         'sort_order': 3},
    # lesson-3
    {'exercise_id': 'exercise-3-1', 'lesson_id': 'lesson-3', 'title': 'Create Variables',         'description': 'Create and name your first variables',                'difficulty': 'Easy',         'sort_order': 1},
    {'exercise_id': 'exercise-3-2', 'lesson_id': 'lesson-3', 'title': 'Use Variables',            'description': 'Use variables in expressions',                        'difficulty': 'Medium',       'sort_order': 2},
    {'exercise_id': 'exercise-3-3', 'lesson_id': 'lesson-3', 'title': 'Multi-Variable Program',   'description': 'Build a program using multiple variables',            'difficulty': 'Hard',         'sort_order': 3},
    # lesson-4
    {'exercise_id': 'exercise-4-1', 'lesson_id': 'lesson-4', 'title': 'Simple If Statement',      'description': 'Create a basic if-then condition',                    'difficulty': 'Easy',         'sort_order': 1},
    {'exercise_id': 'exercise-4-2', 'lesson_id': 'lesson-4', 'title': 'If-Else Logic',            'description': 'Add else branches to handle both outcomes',           'difficulty': 'Medium',       'sort_order': 2},
    {'exercise_id': 'exercise-4-3', 'lesson_id': 'lesson-4', 'title': 'Game Logic',               'description': 'Use conditionals to control game behaviour',          'difficulty': 'Hard',         'sort_order': 3},
    # lesson-5
    {'exercise_id': 'exercise-5-1', 'lesson_id': 'lesson-5', 'title': 'Simple Function',          'description': 'Create your first function',                          'difficulty': 'Easy',         'sort_order': 1},
    {'exercise_id': 'exercise-5-2', 'lesson_id': 'lesson-5', 'title': 'Function with Parameters', 'description': 'Add parameters to make functions flexible',           'difficulty': 'Medium',       'sort_order': 2},
    {'exercise_id': 'exercise-5-3', 'lesson_id': 'lesson-5', 'title': 'Refactoring Code',         'description': 'Refactor repeated code into functions',               'difficulty': 'Hard',         'sort_order': 3},
    # lesson-6
    {'exercise_id': 'exercise-6-1', 'lesson_id': 'lesson-6', 'title': 'Find the Bug',             'description': 'Identify errors in a broken program',                 'difficulty': 'Easy',         'sort_order': 1},
    {'exercise_id': 'exercise-6-2', 'lesson_id': 'lesson-6', 'title': 'Debug Complex Program',    'description': 'Fix multiple bugs in a larger program',               'difficulty': 'Medium',       'sort_order': 2},
    {'exercise_id': 'exercise-6-3', 'lesson_id': 'lesson-6', 'title': 'Improve Efficiency',       'description': 'Make a working program run better',                   'difficulty': 'Hard',         'sort_order': 3},
    # lesson-7
    {'exercise_id': 'exercise-7-1', 'lesson_id': 'lesson-7', 'title': 'Create Simple Game',       'description': 'Build a basic interactive game',                      'difficulty': 'Medium',       'sort_order': 1},
    {'exercise_id': 'exercise-7-2', 'lesson_id': 'lesson-7', 'title': 'Add Game Features',        'description': 'Add scoring and levels to your game',                 'difficulty': 'Hard',         'sort_order': 2},
    {'exercise_id': 'exercise-7-3', 'lesson_id': 'lesson-7', 'title': 'Design Original Game',     'description': 'Design and build your own game from scratch',         'difficulty': 'Hard',         'sort_order': 3},
    # lesson-8
    {'exercise_id': 'exercise-8-1', 'lesson_id': 'lesson-8', 'title': 'Create Arrays',            'description': 'Create and populate arrays',                          'difficulty': 'Easy',         'sort_order': 1},
    {'exercise_id': 'exercise-8-2', 'lesson_id': 'lesson-8', 'title': 'Iterate Over Arrays',      'description': 'Loop through array elements',                         'difficulty': 'Medium',       'sort_order': 2},
    {'exercise_id': 'exercise-8-3', 'lesson_id': 'lesson-8', 'title': 'Manipulate Arrays',        'description': 'Add, remove, and sort array data',                    'difficulty': 'Hard',         'sort_order': 3},
]

# ── Kids-app data ──────────────────────────────────────────────────

TEAMS = [
    {'team_id': 'team-1', 'name': 'Code Warriors',     'total_points': 1250},
    {'team_id': 'team-2', 'name': 'Algorithm Wizards',  'total_points': 1180},
    {'team_id': 'team-3', 'name': 'Binary Builders',    'total_points': 1050},
    {'team_id': 'team-4', 'name': 'Logic Masters',      'total_points': 920},
]

TEAM_MEMBERS = [
    {'member_id': '1',  'team_id': 'team-1', 'name': 'Alex',   'avatar': '👦', 'points': 450},
    {'member_id': '2',  'team_id': 'team-1', 'name': 'Sam',    'avatar': '👧', 'points': 380},
    {'member_id': '3',  'team_id': 'team-1', 'name': 'Jordan', 'avatar': '🧒', 'points': 420},
    {'member_id': '4',  'team_id': 'team-2', 'name': 'Taylor', 'avatar': '👦', 'points': 410},
    {'member_id': '5',  'team_id': 'team-2', 'name': 'Morgan', 'avatar': '👧', 'points': 390},
    {'member_id': '6',  'team_id': 'team-2', 'name': 'Casey',  'avatar': '🧒', 'points': 380},
    {'member_id': '7',  'team_id': 'team-3', 'name': 'Riley',  'avatar': '👦', 'points': 360},
    {'member_id': '8',  'team_id': 'team-3', 'name': 'Quinn',  'avatar': '👧', 'points': 350},
    {'member_id': '9',  'team_id': 'team-3', 'name': 'Avery',  'avatar': '🧒', 'points': 340},
    {'member_id': '10', 'team_id': 'team-4', 'name': 'Jamie',  'avatar': '👦', 'points': 320},
    {'member_id': '11', 'team_id': 'team-4', 'name': 'Drew',   'avatar': '👧', 'points': 310},
    {'member_id': '12', 'team_id': 'team-4', 'name': 'Skyler', 'avatar': '🧒', 'points': 290},
]

CHALLENGES = [
    {'challenge_id': 'pattern-1',         'title': 'Pattern Recognition',  'description': 'Identify the next item in a sequence',  'difficulty': 'beginner',     'category': 'Patterns',         'points': 10, 'question': 'What comes next in this pattern? 🔴 🔵 🔴 🔵 🔴 ?', 'options': ['🔴 Red', '🔵 Blue', '🟢 Green', '🟡 Yellow'], 'correct_answer': 1, 'explanation': 'The pattern alternates between red and blue circles. After red comes blue!', 'age_group': '8-12'},
    {'challenge_id': 'sequence-1',        'title': 'Number Sequence',      'description': 'Find the pattern in numbers',           'difficulty': 'beginner',     'category': 'Logic',            'points': 10, 'question': 'What number comes next? 2, 4, 6, 8, __', 'options': ['9', '10', '11', '12'], 'correct_answer': 1, 'explanation': 'Each number increases by 2. After 8, we add 2 to get 10!', 'age_group': '8-12'},
    {'challenge_id': 'sorting-1',         'title': 'Sort the Animals',     'description': 'Understanding sorting algorithms',      'difficulty': 'beginner',     'category': 'Algorithms',       'points': 15, 'question': 'Which order sorts these animals by size (smallest to largest)? 🐘 🐕 🐁', 'options': ['🐘 🐕 🐁', '🐁 🐕 🐘', '🐕 🐁 🐘', '🐁 🐘 🐕'], 'correct_answer': 1, 'explanation': 'Mouse is smallest, dog is medium, elephant is largest!', 'age_group': '8-12'},
    {'challenge_id': 'loops-1',           'title': 'Repeat the Action',    'description': 'Understanding loops',                   'difficulty': 'beginner',     'category': 'Loops',            'points': 15, 'question': 'If you clap 3 times, then repeat that 2 times, how many claps total?', 'options': ['3', '5', '6', '9'], 'correct_answer': 2, 'explanation': 'You clap 3 times, twice. That\'s 3 + 3 = 6 claps!', 'age_group': '8-12'},
    {'challenge_id': 'variables-1',       'title': 'Variable Storage',     'description': 'Understanding variables',               'difficulty': 'intermediate', 'category': 'Variables',        'points': 20, 'question': 'If x = 5 and y = 3, what is x + y?', 'options': ['2', '8', '15', '53'], 'correct_answer': 1, 'explanation': 'Variables store values. We replace x with 5 and y with 3, then add: 5 + 3 = 8', 'age_group': '12-15'},
    {'challenge_id': 'conditionals-1',    'title': 'If-Then Thinking',     'description': 'Conditional logic',                     'difficulty': 'intermediate', 'category': 'Conditionals',     'points': 20, 'question': 'If temperature > 30°C, wear shorts. It\'s 32°C. What do you wear?', 'options': ['Jacket', 'Shorts', 'Sweater', 'Raincoat'], 'correct_answer': 1, 'explanation': 'Since 32 > 30 is true, the condition is met, so wear shorts!', 'age_group': '12-15'},
    {'challenge_id': 'functions-1',       'title': 'Function Magic',       'description': 'Understanding functions',               'difficulty': 'intermediate', 'category': 'Functions',        'points': 25, 'question': 'A function double(x) returns x * 2. What is double(7)?', 'options': ['7', '9', '14', '49'], 'correct_answer': 2, 'explanation': 'The function multiplies input by 2. So double(7) = 7 * 2 = 14', 'age_group': '12-15'},
    {'challenge_id': 'arrays-1',          'title': 'List Indexing',        'description': 'Working with arrays',                   'difficulty': 'intermediate', 'category': 'Data Structures',  'points': 25, 'question': 'fruits = ["apple", "banana", "cherry"]. What is fruits[1]?', 'options': ['apple', 'banana', 'cherry', 'error'], 'correct_answer': 1, 'explanation': 'Arrays start counting at 0! So [0]=apple, [1]=banana, [2]=cherry', 'age_group': '12-15'},
    {'challenge_id': 'recursion-1',       'title': 'Recursive Thinking',   'description': 'Understanding recursion',               'difficulty': 'advanced',     'category': 'Recursion',        'points': 30, 'question': 'What is the factorial of 4? (4! = 4 × 3 × 2 × 1)', 'options': ['10', '16', '24', '32'], 'correct_answer': 2, 'explanation': 'Factorial multiplies all numbers down to 1: 4 × 3 × 2 × 1 = 24', 'age_group': '15-18'},
    {'challenge_id': 'algorithms-1',      'title': 'Binary Search',        'description': 'Search algorithms',                     'difficulty': 'advanced',     'category': 'Algorithms',       'points': 30, 'question': 'How many steps max to find a number in a sorted list of 16 items using binary search?', 'options': ['4', '8', '16', '32'], 'correct_answer': 0, 'explanation': 'Binary search divides in half each time: 16→8→4→2→1 = 4 steps max!', 'age_group': '15-18'},
    {'challenge_id': 'complexity-1',      'title': 'Time Complexity',      'description': 'Algorithm efficiency',                  'difficulty': 'advanced',     'category': 'Optimization',     'points': 35, 'question': 'Which grows fastest as n increases: n, n², or 2ⁿ?', 'options': ['n', 'n²', '2ⁿ', 'All the same'], 'correct_answer': 2, 'explanation': 'Exponential (2ⁿ) grows much faster than polynomial (n²) or linear (n)!', 'age_group': '15-18'},
    {'challenge_id': 'data-structures-1', 'title': 'Stack Operations',     'description': 'Understanding stacks',                  'difficulty': 'advanced',     'category': 'Data Structures',  'points': 35, 'question': 'Push 5, Push 3, Pop, Push 7. What\'s on top of the stack?', 'options': ['5', '3', '7', 'Empty'], 'correct_answer': 2, 'explanation': 'Stack is LIFO (Last In First Out). After operations: [5, 7], so 7 is on top!', 'age_group': '15-18'},
]


# ═══════════════════════════════════════════════════════════════════
#  Seed runner
# ═══════════════════════════════════════════════════════════════════

def seed(force=False):
    app = create_app()
    with app.app_context():
        db = get_db()

        if force:
            tables = [r[0] for r in db.execute(
                "SELECT name FROM sqlite_master WHERE type='table'"
            ).fetchall()]
            for t in tables:
                if t != 'sqlite_sequence':
                    db.execute(f'DELETE FROM [{t}]')
            db.commit()
            print('Cleared all existing data.')

        # Teacher profile
        if not db.execute('SELECT 1 FROM teacher_profiles LIMIT 1').fetchone():
            db.execute(
                'INSERT INTO teacher_profiles (name,email,school,avatar) VALUES (?,?,?,?)',
                (TEACHER_PROFILE['name'], TEACHER_PROFILE['email'],
                 TEACHER_PROFILE['school'], TEACHER_PROFILE['avatar']))
            print('  + teacher profile')

        # Classes
        for c in CLASSES:
            if not db.execute('SELECT 1 FROM classes WHERE class_id=?', (c['class_id'],)).fetchone():
                db.execute(
                    'INSERT INTO classes (class_id,name,student_count,active_assignments,engagement_rate) VALUES (?,?,?,?,?)',
                    (c['class_id'], c['name'], c['student_count'],
                     c['active_assignments'], c['engagement_rate']))
        print('  + classes')

        # Students
        for s in STUDENTS:
            if not db.execute('SELECT 1 FROM students WHERE student_id=?', (s['student_id'],)).fetchone():
                db.execute(
                    '''INSERT INTO students
                       (student_id,name,avatar,class_id,progress_percentage,
                        challenges_completed,lessons_completed,last_activity,teacher_notes)
                       VALUES (?,?,?,?,?,?,?,?,?)''',
                    (s['student_id'], s['name'], s['avatar'], s['class_id'],
                     s['progress_percentage'], s['challenges_completed'],
                     s['lessons_completed'], s['last_activity'], s['teacher_notes']))
        print('  + students')

        # Achievements
        for a in ACHIEVEMENTS:
            if not db.execute('SELECT 1 FROM achievements WHERE achievement_id=?', (a['achievement_id'],)).fetchone():
                db.execute(
                    'INSERT INTO achievements (achievement_id,name,icon,description) VALUES (?,?,?,?)',
                    (a['achievement_id'], a['name'], a['icon'], a['description']))
        print('  + achievements')

        # Student achievements
        for sid, aid, dt in STUDENT_ACHIEVEMENTS:
            if not db.execute('SELECT 1 FROM student_achievements WHERE student_id=? AND achievement_id=?', (sid, aid)).fetchone():
                db.execute(
                    'INSERT INTO student_achievements (student_id,achievement_id,earned_date) VALUES (?,?,?)',
                    (sid, aid, dt))
        print('  + student achievements')

        # Activity log
        for a in ACTIVITY_LOG:
            if not db.execute('SELECT 1 FROM activity_log WHERE activity_id=?', (a['activity_id'],)).fetchone():
                db.execute(
                    'INSERT INTO activity_log (activity_id,student_id,activity_type,title,activity_date,success) VALUES (?,?,?,?,?,?)',
                    (a['activity_id'], a['student_id'], a['activity_type'],
                     a['title'], a['activity_date'], a['success']))
        print('  + activity log')

        # Lessons (metadata)
        for l in LESSONS_META:
            if not db.execute('SELECT 1 FROM lessons WHERE lesson_id=?', (l['lesson_id'],)).fetchone():
                db.execute(
                    'INSERT INTO lessons (lesson_id,title,description,duration,level,video_url) VALUES (?,?,?,?,?,?)',
                    (l['lesson_id'], l['title'], l.get('description', ''),
                     l.get('duration'), l.get('level'), l.get('video_url')))
        print('  + lessons')

        # Exercises
        for e in EXERCISES:
            if not db.execute('SELECT 1 FROM exercises WHERE exercise_id=?', (e['exercise_id'],)).fetchone():
                db.execute(
                    'INSERT INTO exercises (exercise_id,lesson_id,title,description,difficulty,sort_order) VALUES (?,?,?,?,?,?)',
                    (e['exercise_id'], e['lesson_id'], e['title'],
                     e['description'], e['difficulty'], e['sort_order']))
        print('  + exercises')

        # Assignments
        for a in ASSIGNMENTS:
            if not db.execute('SELECT 1 FROM assignments WHERE assignment_id=?', (a['assignment_id'],)).fetchone():
                db.execute(
                    'INSERT INTO assignments (assignment_id,lesson_id,class_id,assigned_date,due_date,completion_rate) VALUES (?,?,?,?,?,?)',
                    (a['assignment_id'], a['lesson_id'], a['class_id'],
                     a['assigned_date'], a['due_date'], a['completion_rate']))
        print('  + assignments')

        # Teams
        for t in TEAMS:
            if not db.execute('SELECT 1 FROM teams WHERE team_id=?', (t['team_id'],)).fetchone():
                db.execute(
                    'INSERT INTO teams (team_id,name,total_points) VALUES (?,?,?)',
                    (t['team_id'], t['name'], t['total_points']))
        print('  + teams')

        # Team members
        for m in TEAM_MEMBERS:
            if not db.execute('SELECT 1 FROM team_members WHERE member_id=?', (m['member_id'],)).fetchone():
                db.execute(
                    'INSERT INTO team_members (member_id,team_id,name,avatar,points) VALUES (?,?,?,?,?)',
                    (m['member_id'], m['team_id'], m['name'], m['avatar'], m['points']))
        print('  + team members')

        # Challenges
        for ch in CHALLENGES:
            if not db.execute('SELECT 1 FROM challenges WHERE challenge_id=?', (ch['challenge_id'],)).fetchone():
                db.execute(
                    '''INSERT INTO challenges
                       (challenge_id,title,description,difficulty,category,points,
                        question,options,correct_answer,explanation,age_group)
                       VALUES (?,?,?,?,?,?,?,?,?,?,?)''',
                    (ch['challenge_id'], ch['title'], ch['description'],
                     ch['difficulty'], ch['category'], ch['points'],
                     ch['question'], json.dumps(ch['options']),
                     ch['correct_answer'], ch['explanation'], ch['age_group']))
        print('  + challenges')

        db.commit()
        print('\nSeed complete ✓')


if __name__ == '__main__':
    force = '--force' in sys.argv
    seed(force)
