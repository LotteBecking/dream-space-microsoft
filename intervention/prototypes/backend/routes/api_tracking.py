"""User-tracking / analytics API.

Every event is stored with a user_type, user_id, event_type, and an
arbitrary JSON payload so both the teacher dashboard and the kids app
can log behavioural data through one endpoint.
"""

from flask import Blueprint, request, jsonify

import models

tracking_bp = Blueprint('tracking', __name__, url_prefix='/api/tracking')


@tracking_bp.route('/event', methods=['POST'])
def log_event():
    data = request.get_json(silent=True) or {}

    required = ('user_type', 'user_id', 'event_type')
    # Accept camelCase too
    for camel, snake in [('userType', 'user_type'),
                         ('userId', 'user_id'),
                         ('eventType', 'event_type'),
                         ('eventData', 'event_data'),
                         ('sessionId', 'session_id')]:
        if camel in data:
            data.setdefault(snake, data.pop(camel))

    missing = [f for f in required if not data.get(f)]
    if missing:
        return jsonify({"error": f"Missing fields: {', '.join(missing)}"}), 400

    if data['user_type'] not in ('student', 'teacher'):
        return jsonify({"error": "user_type must be 'student' or 'teacher'"}), 400

    models.log_tracking_event(data)
    return jsonify({"success": True}), 201


@tracking_bp.route('/events', methods=['GET'])
def list_events():
    user_type = request.args.get('user_type') or request.args.get('userType')
    user_id = request.args.get('user_id') or request.args.get('userId')
    event_type = request.args.get('event_type') or request.args.get('eventType')
    limit = request.args.get('limit', 100, type=int)
    return jsonify(models.get_tracking_events(user_type, user_id,
                                              event_type, limit))
