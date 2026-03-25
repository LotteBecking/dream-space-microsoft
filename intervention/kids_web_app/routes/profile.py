"""Profile route — view and edit user profile."""

from flask import Blueprint, render_template, request, session, redirect, url_for, flash, g
import services.api_client as api
from routes.auth import login_required
from routes.onboarding import AVATARS

profile_bp = Blueprint("profile", __name__)


@profile_bp.route("/profile", methods=["GET", "POST"])
@login_required
def index():
    member_id = g.member_id
    teams, _ = api.get("/api/kids/teams")
    if not isinstance(teams, list):
        teams = []

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        age = request.form.get("age", "")
        avatar = request.form.get("avatar", "🚀")
        team_id = request.form.get("team_id", "")

        api.put(f"/api/kids/profile/{member_id}", {
            "name": name,
            "age": int(age) if age else None,
            "avatar": avatar,
            "teamId": team_id,
        })

        session["avatar"] = avatar
        session["name"] = name
        flash("Profile updated!", "success")
        return redirect(url_for("profile.index"))

    profile, _ = api.get(f"/api/kids/profile/{member_id}")
    stats, _ = api.get(f"/api/kids/profile/{member_id}/stats")
    if not isinstance(profile, dict):
        profile = {}
    if not isinstance(stats, dict):
        stats = {}

    # Find team name
    team_name = ""
    if profile.get("teamId"):
        team, _ = api.get(f"/api/kids/teams/{profile['teamId']}")
        team_name = team.get("name", "") if isinstance(team, dict) else ""

    return render_template(
        "profile.html",
        profile=profile,
        stats=stats,
        teams=teams,
        team_name=team_name,
        avatars=AVATARS,
        edit=request.args.get("edit") == "1",
        offline=api.is_offline(),
    )
