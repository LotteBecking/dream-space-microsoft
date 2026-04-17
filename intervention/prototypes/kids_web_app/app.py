"""DreamSpace Kids Web App — Flask entry point, port 5001."""

import json
from pathlib import Path
from flask import Flask
from config import SECRET_KEY, LESSON_DIR

from routes.auth import auth_bp
from routes.dashboard import dashboard_bp
from routes.onboarding import onboarding_bp
from routes.challenges import challenges_bp
from routes.progress import progress_bp
from routes.teams import teams_bp
from routes.profile import profile_bp
from routes.lessons import lessons_bp
from routes.news import news_bp


def create_app():
    app = Flask(__name__)
    app.secret_key = SECRET_KEY
    app.config["SESSION_COOKIE_SAMESITE"] = "Lax"

    # ── Load lesson content at startup ────────────────────────────
    manifest_path = LESSON_DIR / "manifest.json"
    lessons_list = []
    lessons_data = {}

    if manifest_path.exists():
        with open(manifest_path) as f:
            manifest = json.load(f)
        lessons_list = manifest.get("lessons", [])

        for entry in lessons_list:
            lesson_path = LESSON_DIR / entry["path"]
            if lesson_path.exists():
                with open(lesson_path) as f:
                    data = json.load(f)
                lessons_data[entry["id"]] = data

    app.config["LESSONS"] = lessons_list
    app.config["LESSONS_DATA"] = lessons_data

    # ── Register blueprints ────────────────────────────────────────
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(onboarding_bp)
    app.register_blueprint(challenges_bp)
    app.register_blueprint(progress_bp)
    app.register_blueprint(teams_bp)
    app.register_blueprint(profile_bp)
    app.register_blueprint(lessons_bp)
    app.register_blueprint(news_bp)

    return app


if __name__ == "__main__":
    app = create_app()
    print("🚀 Dream Space Kids Web App running at http://localhost:5001")
    app.run(port=5001, debug=True)
