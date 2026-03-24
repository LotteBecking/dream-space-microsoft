"""Dashboard route — the main landing page after login."""

from flask import Blueprint, render_template, session, redirect, url_for, g
import services.api_client as api
from routes.auth import login_required
import config

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/")
@login_required
def index():
    member_id = g.member_id

    # Parallel data fetching
    daily, _ = api.get("/api/kids/challenges/daily")
    stats, _ = api.get(f"/api/kids/profile/{member_id}/stats")
    profile, pstatus = api.get(f"/api/kids/profile/{member_id}")

    # Redirect to onboarding if no team set (check session fallback for demo mode)
    team_id = profile.get("teamId") or session.get("team_id")
    if not config.SKIP_ONBOARDING and (pstatus == 404 or not team_id):
        return redirect(url_for("onboarding.index"))

    # Fetch user's team details
    team = {}
    team_rank = 0
    if team_id:
        team, _ = api.get(f"/api/kids/teams/{team_id}")
        rankings, _ = api.get("/api/kids/teams/rankings")
        if isinstance(rankings, list):
            for i, t in enumerate(rankings):
                if t.get("id") == team_id:
                    team_rank = i + 1
                    break

    return render_template(
        "dashboard.html",
        daily=daily,
        stats=stats,
        profile=profile,
        team=team,
        team_rank=team_rank,
        offline=api.is_offline(),
    )
