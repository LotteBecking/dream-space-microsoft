"""REST API consumed by the iOS kids-learning app.

Covers: challenges, teams, user profiles, challenge results.
"""

import uuid
from datetime import date

from flask import Blueprint, request, jsonify

import models

kids_bp = Blueprint('kids', __name__, url_prefix='/api/kids')


# ── Challenges ─────────────────────────────────────────────────────

@kids_bp.route('/challenges', methods=['GET'])
def list_challenges():
    difficulty = request.args.get('difficulty')
    age = request.args.get('age', type=int)
    return jsonify(models.get_all_challenges(difficulty, age))


@kids_bp.route('/challenges/daily', methods=['GET'])
def daily_challenge():
    date_str = request.args.get('date', date.today().isoformat())
    challenge = models.get_daily_challenge(date_str)
    if not challenge:
        return jsonify({"error": "No challenges available"}), 404
    return jsonify(challenge)


@kids_bp.route('/challenges/<challenge_id>', methods=['GET'])
def get_challenge(challenge_id):
    c = models.get_challenge(challenge_id)
    if not c:
        return jsonify({"error": "Challenge not found"}), 404
    return jsonify(c)


@kids_bp.route('/challenges/<challenge_id>/complete', methods=['POST'])
def complete_challenge(challenge_id):
    data = request.get_json(silent=True) or {}
    member_id = data.get('member_id') or data.get('memberId', '')
    if not member_id:
        return jsonify({"error": "member_id is required"}), 400

    challenge = models.get_challenge(challenge_id)
    if not challenge:
        return jsonify({"error": "Challenge not found"}), 404

    correct = bool(data.get('correct', False))
    pts = challenge['points'] if correct else 0

    result_id = data.get('id', str(uuid.uuid4()))
    models.save_challenge_result({
        'id': result_id,
        'member_id': member_id,
        'challenge_id': challenge_id,
        'completed': 1,
        'correct': int(correct),
        'points': pts,
    })

    # Update team-member points
    if correct:
        models.update_member_points(member_id, pts)

    return jsonify({
        "success": True,
        "resultId": result_id,
        "correct": correct,
        "pointsAwarded": pts,
    }), 201


# ── Challenge results ─────────────────────────────────────────────

@kids_bp.route('/results/<member_id>', methods=['GET'])
def member_results(member_id):
    return jsonify(models.get_challenge_results(member_id))


# ── Teams ──────────────────────────────────────────────────────────

@kids_bp.route('/teams', methods=['GET'])
def list_teams():
    return jsonify(models.get_all_teams())


@kids_bp.route('/teams/<team_id>', methods=['GET'])
def get_team(team_id):
    t = models.get_team(team_id)
    if not t:
        return jsonify({"error": "Team not found"}), 404
    return jsonify(t)


@kids_bp.route('/teams/rankings', methods=['GET'])
def team_rankings():
    return jsonify(models.get_team_rankings())


@kids_bp.route('/members/rankings', methods=['GET'])
def member_rankings():
    return jsonify(models.get_member_rankings())


@kids_bp.route('/teams/<team_id>/members', methods=['POST'])
def add_member(team_id):
    data = request.get_json(silent=True) or {}
    mid = data.get('member_id') or data.get('memberId', '')
    if not mid:
        return jsonify({"error": "member_id is required"}), 400
    payload = {
        'member_id': mid,
        'name': data.get('name', ''),
        'avatar': data.get('avatar', ''),
        'points': data.get('points', 0),
    }
    models.add_team_member(team_id, payload)
    return jsonify({"success": True}), 201


# ── User profiles ─────────────────────────────────────────────────

@kids_bp.route('/profile', methods=['POST'])
def create_or_update_profile():
    data = request.get_json(silent=True) or {}
    mid = data.get('member_id') or data.get('memberId', '')
    if not mid:
        return jsonify({"error": "member_id is required"}), 400
    payload = {
        'member_id': mid,
        'name': data.get('name', ''),
        'age': data.get('age'),
        'team_id': data.get('team_id') or data.get('teamId', ''),
        'avatar': data.get('avatar', ''),
    }
    models.save_user_profile(payload)

    # Also ensure the member exists in team_members
    if payload['team_id']:
        existing_team = models.get_team(payload['team_id'])
        if existing_team:
            member_exists = any(
                m['id'] == mid for m in existing_team['members']
            )
            if not member_exists:
                models.add_team_member(payload['team_id'], {
                    'member_id': mid,
                    'name': payload['name'],
                    'avatar': payload['avatar'],
                    'points': 0,
                })

    return jsonify({"success": True, "memberId": mid}), 201


@kids_bp.route('/profile/<member_id>', methods=['GET'])
def get_profile(member_id):
    p = models.get_user_profile(member_id)
    if not p:
        return jsonify({"error": "Profile not found"}), 404
    return jsonify(p)


@kids_bp.route('/profile/<member_id>', methods=['PUT'])
def update_profile(member_id):
    data = request.get_json(silent=True) or {}
    data['member_id'] = member_id
    if 'teamId' in data:
        data['team_id'] = data.pop('teamId')
    models.save_user_profile(data)
    return jsonify({"success": True})


@kids_bp.route('/profile/<member_id>/stats', methods=['GET'])
def profile_stats(member_id):
    return jsonify(models.get_user_stats(member_id))
