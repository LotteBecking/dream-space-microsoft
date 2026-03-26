"""Authentication helpers: password hashing, session tokens, role checks."""

import hashlib
import secrets
from datetime import datetime, timedelta
from functools import wraps

from flask import request, jsonify, g

from database import get_db

SESSION_DURATION_HOURS = 72


# ── Password hashing (PBKDF2-SHA256 from stdlib, no extra deps) ──

def hash_password(password):
    """Hash a password using PBKDF2-SHA256 with a random salt."""
    salt = secrets.token_hex(16)
    dk = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100_000)
    return f"{salt}${dk.hex()}"


def verify_password(password, stored_hash):
    """Check a password against a stored PBKDF2 hash."""
    parts = stored_hash.split('$', 1)
    if len(parts) != 2:
        return False
    salt, expected = parts
    dk = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100_000)
    return secrets.compare_digest(dk.hex(), expected)


# ── Session tokens ────────────────────────────────────────────────

def create_session(account_id):
    """Create a new session token and store it in the DB."""
    token = secrets.token_urlsafe(32)
    expires = datetime.utcnow() + timedelta(hours=SESSION_DURATION_HOURS)
    db = get_db()
    db.execute(
        'INSERT INTO auth_sessions (token, account_id, expires_at) VALUES (?,?,?)',
        (token, account_id, expires.isoformat()))
    db.commit()
    return token, expires.isoformat()


def get_session_account(token):
    """Return the account row for a valid session token, or None."""
    db = get_db()
    row = db.execute(
        '''SELECT a.* FROM auth_sessions s
           JOIN accounts a ON s.account_id = a.id
           WHERE s.token = ? AND s.expires_at > ?''',
        (token, datetime.utcnow().isoformat())
    ).fetchone()
    return dict(row) if row else None


def delete_session(token):
    db = get_db()
    db.execute('DELETE FROM auth_sessions WHERE token = ?', (token,))
    db.commit()


# ── Decorators for route protection ──────────────────────────────

def require_auth(f):
    """Decorator: requires a valid Bearer token.  Sets g.account."""
    @wraps(f)
    def wrapper(*args, **kwargs):
        auth = request.headers.get('Authorization', '')
        if not auth.startswith('Bearer '):
            return jsonify({"error": "Authentication required"}), 401
        token = auth[7:]
        account = get_session_account(token)
        if not account:
            return jsonify({"error": "Invalid or expired token"}), 401
        g.account = account
        return f(*args, **kwargs)
    return wrapper


def require_role(role):
    """Decorator: requires a specific role (use after @require_auth)."""
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if g.account.get('role') != role:
                return jsonify({"error": f"Requires {role} role"}), 403
            return f(*args, **kwargs)
        return wrapper
    return decorator


def generate_class_code():
    """Generate a short, unique, human-readable class join code."""
    return secrets.token_urlsafe(6).replace('-', '').replace('_', '')[:8].upper()
