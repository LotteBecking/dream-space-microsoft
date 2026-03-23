"""DreamSpace unified Flask backend.

Serves the teacher-dashboard HTML pages and provides REST API
endpoints for both the teacher dashboard and the kids learning app.
"""

from flask import Flask
from flask_cors import CORS

import config
import database
from routes.dashboard import dashboard_bp
from routes.api import api_bp
from routes.api_kids import kids_bp
from routes.api_tracking import tracking_bp
from routes.api_auth import auth_bp
from routes.api_progress import progress_bp


def create_app():
    app = Flask(
        __name__,
        template_folder=config.TEMPLATE_DIR,
    )
    app.config['SECRET_KEY'] = config.SECRET_KEY
    app.config['DATABASE_PATH'] = config.DATABASE_PATH
    app.config['JSON_SORT_KEYS'] = False

    # Allow the iOS client (and local dev tools) to call the API
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # Database setup (creates tables on first run)
    database.init_app(app)

    # Register blueprints
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(api_bp)
    app.register_blueprint(kids_bp)
    app.register_blueprint(tracking_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(progress_bp)

    return app


app = create_app()

if __name__ == '__main__':
    app.run(debug=config.DEBUG, port=5000)
