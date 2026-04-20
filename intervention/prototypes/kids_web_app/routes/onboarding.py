"""Onboarding wizard — runs after first login when profile has no team."""

from flask import Blueprint, render_template, request, session, redirect, url_for, g
import services.api_client as api
from routes.auth import login_required

onboarding_bp = Blueprint("onboarding", __name__)

AVATARS = [
    "🚀", "⭐", "🌙", "💻", "🎮", "🎯", "🔮", "🌈",
    "🦋", "🐉", "🦄", "🌸", "⚡", "🔥", "💎", "🎪",
    "🤖", "👾", "🎨", "🌺", "🏆", "🎓", "💡", "🌟",
    "🍀", "🦊", "🐼", "🦁", "🐬", "🦅",
]


@onboarding_bp.route("/onboarding", methods=["GET", "POST"])
@login_required
def index():
    classes, _ = api.get("/api/kids/teams")
    if not isinstance(classes, list):
        classes = []

    if request.method == "POST":
        nickname = request.form.get("name", g.user_name).strip()
        age = request.form.get("age", "")
        avatar = request.form.get("avatar", "🚀")
        class_code = request.form.get("class_code", "").strip().upper()
        class_id = request.form.get("class_id", "")

        member_id = g.member_id

        # Save profile
        api.post("/api/kids/profile", {
            "member_id": member_id,
            "name": nickname,
            "age": int(age) if age else None,
            "team_id": class_id or None,
            "avatar": avatar,
        })

        # Join class via code (connects to teacher dashboard)
        if class_code:
            api.post("/api/auth/join-class", {
                "student_id": member_id,
                "code": class_code,
            })

        # Join game class/team
        if class_id:
            api.post(f"/api/kids/teams/{class_id}/members", {
                "member_id": member_id,
                "name": nickname,
                "avatar": avatar,
                "points": 0,
            })

        # Persist in session
        session["avatar"] = avatar
        session["name"] = nickname
        session["team_id"] = class_id
        if class_code:
            session["class_code"] = class_code

        return redirect(url_for("dashboard.index"))

    return render_template(
        "onboarding.html",
        classes=classes,
        avatars=AVATARS,
        onboard_name=g.user_name,
        onboard_avatar="🚀",
    )
