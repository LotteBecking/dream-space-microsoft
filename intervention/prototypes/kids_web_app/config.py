"""Configuration for DreamSpace Kids Web App."""

import os
from pathlib import Path

# Backend API
API_BASE_URL = os.environ.get("API_BASE_URL", "http://localhost:5000")

# Flask
SECRET_KEY = os.environ.get("SECRET_KEY", "dreamspace-kids-dev-secret-2024")

# Lesson content (relative to this file's directory → sibling prototypes folder)
BASE_DIR = Path(__file__).parent
LESSON_DIR = BASE_DIR.parent / "teacher_dashboard_python" / "data" / "lesson_content"

# Optional: NewsAPI key (fallback source for tech news)
NEWSAPI_KEY = os.environ.get("NEWSAPI_KEY", "")

# Dev flag: set to True to skip onboarding redirect and always show the dashboard
SKIP_ONBOARDING = os.environ.get("SKIP_ONBOARDING", "true").lower() == "true"
