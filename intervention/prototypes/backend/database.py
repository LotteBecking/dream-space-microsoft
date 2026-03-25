"""SQLite connection helpers for Flask."""

import os
import sqlite3

from flask import g

DATABASE_PATH = None  # set by init_app()


def get_db():
    """Return the per-request database connection."""
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE_PATH)
        g.db.row_factory = sqlite3.Row
        g.db.execute('PRAGMA foreign_keys = ON')
    return g.db


def close_db(_exc=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()


def init_db(app):
    """Create all tables from schema.sql if they don't exist."""
    schema_path = os.path.join(os.path.dirname(__file__), 'db', 'schema.sql')
    with app.app_context():
        db = get_db()
        with open(schema_path, 'r', encoding='utf-8') as f:
            db.executescript(f.read())
        db.commit()


def init_app(app):
    """Bind database lifecycle to the Flask app."""
    global DATABASE_PATH
    DATABASE_PATH = app.config['DATABASE_PATH']
    app.teardown_appcontext(close_db)
    init_db(app)
