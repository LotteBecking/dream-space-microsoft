"""Progress route."""

from flask import Blueprint, render_template, g
import services.api_client as api
from routes.auth import login_required

progress_bp = Blueprint("progress", __name__)

CATEGORY_EMOJI = {
    "Patterns": "🔄", "Logic": "🧩", "Algorithms": "⚙️", "Loops": "🔁",
    "Variables": "📦", "Conditionals": "🔀", "Functions": "🎯",
    "Data Structures": "📊", "Recursion": "🌀", "Optimization": "⚡",
}


@progress_bp.route("/progress")
@login_required
def index():
    member_id = g.member_id
    stats, _ = api.get(f"/api/kids/profile/{member_id}/stats")
    results, _ = api.get(f"/api/kids/results/{member_id}")

    if not isinstance(results, list):
        results = []

    # Enrich results with category emoji
    all_challenges, _ = api.get("/api/kids/challenges")
    challenge_map = {}
    if isinstance(all_challenges, list):
        challenge_map = {c["id"]: c for c in all_challenges}

    for r in results:
        cid = r.get("challengeId", "")
        c = challenge_map.get(cid, {})
        r["challengeTitle"] = c.get("title", cid)
        r["category"] = c.get("category", "Other")
        r["categoryEmoji"] = CATEGORY_EMOJI.get(r["category"], "🎮")
        r["points"] = c.get("points", 0) if r.get("correct") else 0

    # Category performance
    category_stats = {}
    for r in results:
        cat = r["category"]
        if cat not in category_stats:
            category_stats[cat] = {"total": 0, "correct": 0, "emoji": r["categoryEmoji"]}
        category_stats[cat]["total"] += 1
        if r.get("correct"):
            category_stats[cat]["correct"] += 1
    for cat in category_stats:
        t = category_stats[cat]["total"]
        c = category_stats[cat]["correct"]
        category_stats[cat]["pct"] = round((c / t) * 100) if t > 0 else 0

    # Achievements
    total_points = stats.get("totalPoints", 0) if isinstance(stats, dict) else 0
    streak = stats.get("streak", 0) if isinstance(stats, dict) else 0
    completed_count = sum(1 for r in results if r.get("completed"))
    correct_count = sum(1 for r in results if r.get("correct"))
    accuracy = round((correct_count / completed_count) * 100) if completed_count else 0

    achievements = [
        {"title": "First Steps", "desc": "Complete your first challenge", "icon": "🎯",
         "unlocked": len(results) > 0},
        {"title": "3-Day Streak", "desc": "Complete challenges 3 days in a row", "icon": "🔥",
         "unlocked": streak >= 3},
        {"title": "Week Warrior", "desc": "Maintain a 7-day streak", "icon": "⭐",
         "unlocked": streak >= 7},
        {"title": "Century Club", "desc": "Earn 100 points", "icon": "💯",
         "unlocked": total_points >= 100},
        {"title": "Perfect Score", "desc": "5 correct in a row with 100% accuracy", "icon": "🏆",
         "unlocked": accuracy == 100 and completed_count >= 5},
        {"title": "Challenge Master", "desc": "Complete 10 challenges", "icon": "🎓",
         "unlocked": completed_count >= 10},
    ]

    return render_template(
        "progress.html",
        stats=stats if isinstance(stats, dict) else {},
        results=results,
        category_stats=category_stats,
        achievements=achievements,
        completed_count=completed_count,
        accuracy=accuracy,
        offline=api.is_offline(),
    )
