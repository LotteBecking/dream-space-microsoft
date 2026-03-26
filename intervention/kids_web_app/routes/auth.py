"""Auth routes: login, signup, logout. Also provides @login_required decorator."""

import functools
from flask import (
    Blueprint, render_template, request, session,
    redirect, url_for, flash, g,
)
import services.api_client as api

auth_bp = Blueprint("auth", __name__)


# ── Decorator ──────────────────────────────────────────────────────

def login_required(f):
    @functools.wraps(f)
    def decorated(*args, **kwargs):
        if not session.get("token"):
            return redirect(url_for("auth.login"))
        g.token = session["token"]
        g.member_id = session.get("member_id", "")
        g.user_name = session.get("name", "Coder")
        g.user_avatar = session.get("avatar", "🚀")
        return f(*args, **kwargs)
    return decorated


# ── Login ──────────────────────────────────────────────────────────

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if session.get("token"):
        return redirect(url_for("dashboard.index"))

    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")

        data, status = api.post("/api/auth/login", {"email": email, "password": password})

        if status in (200, 201) and data.get("token"):
            _save_session(data)
            return _post_login_redirect(data)
        else:
            flash(data.get("error", "Login failed. Check your email and password."), "error")

    return render_template("auth/login.html")


# ── Signup ─────────────────────────────────────────────────────────

@auth_bp.route("/signup", methods=["GET", "POST"])
def signup():
    if session.get("token"):
        return redirect(url_for("dashboard.index"))

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")

        if not name or not email or not password:
            flash("All fields are required.", "error")
            return render_template("auth/signup.html")

        data, status = api.post("/api/auth/signup", {
            "name": name,
            "email": email,
            "password": password,
            "role": "student",
        })

        if status in (200, 201) and data.get("token"):
            _save_session(data)
            return _post_login_redirect(data)
        else:
            flash(data.get("error", "Signup failed. Try a different email."), "error")

    return render_template("auth/signup.html")


# ── Logout ─────────────────────────────────────────────────────────

@auth_bp.route("/logout")
def logout():
    token = session.get("token")
    if token:
        api.post("/api/auth/logout", token=token)
    session.clear()
    return redirect(url_for("auth.login"))


# ── Helpers ────────────────────────────────────────────────────────

def _save_session(data):
    session["token"] = data["token"]
    session["member_id"] = data.get("studentId", "")
    session["name"] = data.get("name", "Coder")
    session["avatar"] = session.get("avatar", "🚀")  # set during onboarding
    session.permanent = True


def _post_login_redirect(data):
    member_id = data.get("studentId", "")
    if not member_id:
        return redirect(url_for("dashboard.index"))

    profile, status = api.get(f"/api/kids/profile/{member_id}")
    # Also check session team_id (set during onboarding) for demo/offline mode
    if status == 404 or not (profile.get("teamId") or session.get("team_id")):
        return redirect(url_for("onboarding.index"))
    # Cache avatar from profile
    session["avatar"] = profile.get("avatar", "🚀")
    return redirect(url_for("dashboard.index"))
