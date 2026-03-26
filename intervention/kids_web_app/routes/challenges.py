"""Challenges routes: list, detail, and complete."""

from flask import Blueprint, render_template, request, session, jsonify, g
import services.api_client as api
from routes.auth import login_required

challenges_bp = Blueprint("challenges", __name__)

CATEGORY_EMOJI = {
    "Patterns": "🔄", "Logic": "🧩", "Algorithms": "⚙️", "Loops": "🔁",
    "Variables": "📦", "Conditionals": "🔀", "Functions": "🎯",
    "Data Structures": "📊", "Recursion": "🌀", "Optimization": "⚡",
}

DIFFICULTY_COLORS = {
    "beginner": "green", "intermediate": "yellow", "advanced": "red",
}


@challenges_bp.route("/challenges")
@login_required
def list_challenges():
    difficulty = request.args.get("difficulty", "")
    params = {"difficulty": difficulty} if difficulty else {}
    challenges, _ = api.get("/api/kids/challenges", params=params)
    if not isinstance(challenges, list):
        challenges = []

    # Mark completed ones
    results, _ = api.get(f"/api/kids/results/{g.member_id}")
    completed_ids = set()
    if isinstance(results, list):
        completed_ids = {r["challengeId"] for r in results if r.get("completed")}

    for c in challenges:
        c["done"] = c.get("id") in completed_ids
        c["categoryEmoji"] = CATEGORY_EMOJI.get(c.get("category", ""), "🎮")
        c["difficultyColor"] = DIFFICULTY_COLORS.get(c.get("difficulty", ""), "gray")

    return render_template(
        "challenges/list.html",
        challenges=challenges,
        difficulty=difficulty,
        offline=api.is_offline(),
    )


@challenges_bp.route("/challenges/<challenge_id>")
@login_required
def detail(challenge_id):
    challenge, status = api.get(f"/api/kids/challenges/{challenge_id}")
    if status == 404:
        return render_template("challenges/list.html", challenges=[], difficulty="", offline=api.is_offline())
    challenge["categoryEmoji"] = CATEGORY_EMOJI.get(challenge.get("category", ""), "🎮")
    challenge["difficultyColor"] = DIFFICULTY_COLORS.get(challenge.get("difficulty", ""), "gray")

    # Check if already completed
    results, _ = api.get(f"/api/kids/results/{g.member_id}")
    already_done = False
    if isinstance(results, list):
        already_done = any(
            r.get("challengeId") == challenge_id and r.get("completed")
            for r in results
        )

    return render_template(
        "challenges/detail.html",
        challenge=challenge,
        already_done=already_done,
    )


@challenges_bp.route("/challenges/<challenge_id>/complete", methods=["POST"])
@login_required
def complete(challenge_id):
    data = request.get_json(silent=True) or {}
    correct = bool(data.get("correct", False))

    result, status = api.post(
        f"/api/kids/challenges/{challenge_id}/complete",
        {"member_id": g.member_id, "correct": correct},
    )
    return jsonify(result), status
