"""Teams/Classes route — leaderboard with class and individual tabs."""

from flask import Blueprint, render_template, request, session, g
import services.api_client as api
from routes.auth import login_required

teams_bp = Blueprint("teams", __name__)


@teams_bp.route("/teams")
@login_required
def index():
    tab = request.args.get("tab", "classes")
    class_rankings, _ = api.get("/api/kids/teams/rankings")
    member_rankings, _ = api.get("/api/kids/members/rankings")

    if not isinstance(class_rankings, list):
        class_rankings = []
    if not isinstance(member_rankings, list):
        member_rankings = []

    # User's own class (from session or profile)
    user_class = {}
    user_class_rank = 0
    class_id = session.get("team_id")
    if not class_id:
        profile, _ = api.get(f"/api/kids/profile/{g.member_id}")
        class_id = profile.get("teamId") if profile else None

    if class_id:
        user_class, _ = api.get(f"/api/kids/teams/{class_id}")
        for i, c in enumerate(class_rankings):
            if c.get("id") == class_id:
                user_class_rank = i + 1
                break

    return render_template(
        "teams.html",
        tab=tab,
        class_rankings=class_rankings,
        member_rankings=member_rankings,
        user_class=user_class,
        user_class_rank=user_class_rank,
        offline=api.is_offline(),
    )
