import json
import os
from pathlib import Path
from datetime import datetime

# Data directory
DATA_DIR = Path(__file__).parent / 'store'
DATA_DIR.mkdir(exist_ok=True)

STORAGE_KEYS = {
    'TEACHER_PROFILE': DATA_DIR / 'teacher_profile.json',
    'CLASSES': DATA_DIR / 'classes.json',
    'STUDENTS': DATA_DIR / 'students.json',
    'ASSIGNMENTS': DATA_DIR / 'assignments.json',
    'LAST_LESSON': DATA_DIR / 'last_lesson.txt'
}

# Default data
DEFAULT_TEACHER_PROFILE = {
    'name': 'Sarah Johnson',
    'email': 'sarah.johnson@school.edu',
    'school': 'Kennedy Elementary School',
    'avatar': 'SJ'
}

DEFAULT_CLASSES = [
    {
        'id': 'class-1',
        'name': 'Class 4A',
        'studentCount': 24,
        'activeAssignments': 3,
        'engagementRate': 87,
        'students': ['student-1', 'student-2', 'student-3', 'student-4', 'student-5']
    },
    {
        'id': 'class-2',
        'name': 'Class 4B',
        'studentCount': 22,
        'activeAssignments': 2,
        'engagementRate': 92,
        'students': ['student-6', 'student-7', 'student-8', 'student-9']
    },
    {
        'id': 'class-3',
        'name': 'Class 5A',
        'studentCount': 20,
        'activeAssignments': 4,
        'engagementRate': 78,
        'students': ['student-10', 'student-11']
    }
]

DEFAULT_STUDENTS = [
    {
        'id': 'student-1',
        'name': 'Emma Wilson',
        'avatar': 'EW',
        'classId': 'class-1',
        'progressPercentage': 75,
        'challengesCompleted': 12,
        'lessonsCompleted': 5,
        'lastActivity': '2 hours ago',
        'achievements': [
            {'id': 'ach-1', 'name': 'First Steps', 'icon': 'star', 'earnedDate': '2024-01-15'},
            {'id': 'ach-2', 'name': 'Quick Learner', 'icon': 'zap', 'earnedDate': '2024-02-20'}
        ],
        'activityHistory': [
            {'id': 'act-1', 'type': 'lesson', 'title': 'Loops & Sequences', 'date': '2024-03-15', 'success': True},
            {'id': 'act-2', 'type': 'challenge', 'title': 'Pattern Challenge', 'date': '2024-03-10', 'success': True}
        ],
        'teacherNotes': 'Emma shows great promise. Very attentive during class.'
    },
    {
        'id': 'student-2',
        'name': 'Liam Chen',
        'avatar': 'LC',
        'classId': 'class-1',
        'progressPercentage': 82,
        'challengesCompleted': 15,
        'lessonsCompleted': 7,
        'lastActivity': '30 minutes ago',
        'achievements': [
            {'id': 'ach-1', 'name': 'First Steps', 'icon': 'star', 'earnedDate': '2024-01-10'}
        ],
        'activityHistory': [
            {'id': 'act-1', 'type': 'lesson', 'title': 'Variables & Data Types', 'date': '2024-03-16', 'success': True}
        ],
        'teacherNotes': 'Excellent progress. Helping other students.'
    },
    {
        'id': 'student-3',
        'name': 'Marcus Brown',
        'avatar': 'MB',
        'classId': 'class-1',
        'progressPercentage': 45,
        'challengesCompleted': 6,
        'lessonsCompleted': 2,
        'lastActivity': '1 day ago',
        'achievements': [],
        'activityHistory': [],
        'teacherNotes': 'Needs additional support. Meeting scheduled.'
    },
    {
        'id': 'student-4',
        'name': 'Sofia Garcia',
        'avatar': 'SG',
        'classId': 'class-1',
        'progressPercentage': 88,
        'challengesCompleted': 18,
        'lessonsCompleted': 8,
        'lastActivity': '1 hour ago',
        'achievements': [
            {'id': 'ach-1', 'name': 'First Steps', 'icon': 'star', 'earnedDate': '2024-01-05'},
            {'id': 'ach-2', 'name': 'Quick Learner', 'icon': 'zap', 'earnedDate': '2024-02-15'},
            {'id': 'ach-3', 'name': 'Problem Solver', 'icon': 'lightbulb', 'earnedDate': '2024-03-01'}
        ],
        'activityHistory': [],
        'teacherNotes': 'Outstanding student. Role model for others.'
    },
    {
        'id': 'student-5',
        'name': 'James Park',
        'avatar': 'JP',
        'classId': 'class-1',
        'progressPercentage': 68,
        'challengesCompleted': 10,
        'lessonsCompleted': 4,
        'lastActivity': '45 minutes ago',
        'achievements': [
            {'id': 'ach-1', 'name': 'First Steps', 'icon': 'star', 'earnedDate': '2024-01-20'}
        ],
        'activityHistory': [],
        'teacherNotes': 'Good progress. Enjoys visual learning.'
    },
    {
        'id': 'student-6',
        'name': 'Olivia Martinez',
        'avatar': 'OM',
        'classId': 'class-2',
        'progressPercentage': 92,
        'challengesCompleted': 20,
        'lessonsCompleted': 9,
        'lastActivity': '20 minutes ago',
        'achievements': [
            {'id': 'ach-1', 'name': 'First Steps', 'icon': 'star', 'earnedDate': '2024-01-02'},
            {'id': 'ach-2', 'name': 'Quick Learner', 'icon': 'zap', 'earnedDate': '2024-02-08'}
        ],
        'activityHistory': [],
        'teacherNotes': 'Class leader in coding challenges.'
    },
    {
        'id': 'student-7',
        'name': 'Noah Johnson',
        'avatar': 'NJ',
        'classId': 'class-2',
        'progressPercentage': 61,
        'challengesCompleted': 9,
        'lessonsCompleted': 3,
        'lastActivity': '3 hours ago',
        'achievements': [],
        'activityHistory': [],
        'teacherNotes': 'Progressing steadily. Prefers group work.'
    },
    {
        'id': 'student-8',
        'name': 'Ava Taylor',
        'avatar': 'AT',
        'classId': 'class-2',
        'progressPercentage': 79,
        'challengesCompleted': 14,
        'lessonsCompleted': 6,
        'lastActivity': '2 hours ago',
        'achievements': [
            {'id': 'ach-1', 'name': 'First Steps', 'icon': 'star', 'earnedDate': '2024-01-12'}
        ],
        'activityHistory': [],
        'teacherNotes': 'Consistent high quality work.'
    },
    {
        'id': 'student-9',
        'name': 'Noah Lee',
        'avatar': 'NL',
        'classId': 'class-2',
        'progressPercentage': 55,
        'challengesCompleted': 7,
        'lessonsCompleted': 2,
        'lastActivity': '5 hours ago',
        'achievements': [],
        'activityHistory': [],
        'teacherNotes': 'Needs encouragement. New to coding.'
    },
    {
        'id': 'student-10',
        'name': 'Grace Kim',
        'avatar': 'GK',
        'classId': 'class-3',
        'progressPercentage': 85,
        'challengesCompleted': 16,
        'lessonsCompleted': 7,
        'lastActivity': '1 hour ago',
        'achievements': [
            {'id': 'ach-1', 'name': 'First Steps', 'icon': 'star', 'earnedDate': '2024-01-08'}
        ],
        'activityHistory': [],
        'teacherNotes': 'Creative problem solver.'
    },
    {
        'id': 'student-11',
        'name': 'Henry Davis',
        'avatar': 'HD',
        'classId': 'class-3',
        'progressPercentage': 71,
        'challengesCompleted': 11,
        'lessonsCompleted': 5,
        'lastActivity': '4 hours ago',
        'achievements': [],
        'activityHistory': [],
        'teacherNotes': 'Making good progress.'
    }
]

DEFAULT_ASSIGNMENTS = [
    {
        'id': 'assign-1',
        'lessonId': 'lesson-1',
        'classId': 'class-1',
        'assignedDate': '2024-03-10',
        'dueDate': '2024-03-17',
        'completionRate': 85
    },
    {
        'id': 'assign-2',
        'lessonId': 'lesson-2',
        'classId': 'class-1',
        'assignedDate': '2024-03-12',
        'dueDate': '2024-03-19',
        'completionRate': 70
    }
]

# Teacher Profile
def get_teacher_profile():
    """Get teacher profile from storage"""
    if STORAGE_KEYS['TEACHER_PROFILE'].exists():
        with open(STORAGE_KEYS['TEACHER_PROFILE'], 'r') as f:
            return json.load(f)
    return DEFAULT_TEACHER_PROFILE

def save_teacher_profile(profile):
    """Save teacher profile to storage"""
    with open(STORAGE_KEYS['TEACHER_PROFILE'], 'w') as f:
        json.dump(profile, f, indent=2)

# Classes
def get_classes():
    """Get classes from storage"""
    if STORAGE_KEYS['CLASSES'].exists():
        with open(STORAGE_KEYS['CLASSES'], 'r') as f:
            return json.load(f)
    return DEFAULT_CLASSES

def save_classes(classes):
    """Save classes to storage"""
    with open(STORAGE_KEYS['CLASSES'], 'w') as f:
        json.dump(classes, f, indent=2)

# Students
def get_students():
    """Get students from storage"""
    if STORAGE_KEYS['STUDENTS'].exists():
        with open(STORAGE_KEYS['STUDENTS'], 'r') as f:
            return json.load(f)
    return DEFAULT_STUDENTS

def save_students(students):
    """Save students to storage"""
    with open(STORAGE_KEYS['STUDENTS'], 'w') as f:
        json.dump(students, f, indent=2)

# Assignments
def get_assignments():
    """Get assignments from storage"""
    if STORAGE_KEYS['ASSIGNMENTS'].exists():
        with open(STORAGE_KEYS['ASSIGNMENTS'], 'r') as f:
            return json.load(f)
    return DEFAULT_ASSIGNMENTS

def save_assignments(assignments):
    """Save assignments to storage"""
    with open(STORAGE_KEYS['ASSIGNMENTS'], 'w') as f:
        json.dump(assignments, f, indent=2)

# Last Lesson
def get_last_lesson():
    """Get last viewed lesson ID"""
    if STORAGE_KEYS['LAST_LESSON'].exists():
        with open(STORAGE_KEYS['LAST_LESSON'], 'r') as f:
            return f.read().strip()
    return None

def save_last_lesson(lesson_id):
    """Save last viewed lesson ID"""
    with open(STORAGE_KEYS['LAST_LESSON'], 'w') as f:
        f.write(lesson_id)
