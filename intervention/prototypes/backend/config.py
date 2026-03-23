import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Database
DATABASE_PATH = os.path.join(BASE_DIR, 'dreamspace.db')

# Lesson content lives in the teacher-dashboard prototype
LESSON_CONTENT_DIR = os.path.normpath(os.path.join(
    BASE_DIR, '..', 'teacher_dashboard_python', 'data', 'lesson_content'
))

# Reuse teacher-dashboard templates
TEMPLATE_DIR = os.path.normpath(os.path.join(
    BASE_DIR, '..', 'teacher_dashboard_python', 'templates'
))

# Flask
SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
DEBUG = os.environ.get('FLASK_DEBUG', '1') == '1'
