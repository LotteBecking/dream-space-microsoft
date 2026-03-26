"""HTTP wrapper for all calls to the backend on port 5000.

Falls back to static mock data when the backend is unreachable,
so the capstone demo works without a running backend.
"""

import requests
from config import API_BASE_URL

# ── Offline flag ───────────────────────────────────────────────────
_backend_offline = False


def _headers(token=None):
    h = {"Content-Type": "application/json"}
    if token:
        h["Authorization"] = f"Bearer {token}"
    return h


def _is_dreamspace_response(r):
    """Return True only if the response looks like our Flask backend.
    Rejects AirTunes/ControlCenter on macOS port 5000 (returns 403, no JSON)."""
    ct = r.headers.get("Content-Type", "")
    server = r.headers.get("Server", "")
    # AirTunes/ControlCenter has no Content-Type and Server: AirTunes/...
    if "AirTunes" in server or "Apple" in server:
        return False
    return "application/json" in ct


def get(path, params=None, token=None):
    """GET API_BASE_URL + path. Returns (data_dict, status_code)."""
    global _backend_offline
    try:
        r = requests.get(
            API_BASE_URL + path,
            params=params,
            headers=_headers(token),
            timeout=5,
        )
        if not _is_dreamspace_response(r):
            raise requests.exceptions.ConnectionError("Not a DreamSpace backend")
        _backend_offline = False
        try:
            return r.json(), r.status_code
        except Exception:
            return {}, r.status_code
    except requests.exceptions.ConnectionError:
        _backend_offline = True
        return _mock_get(path, params), 200
    except Exception:
        _backend_offline = True
        return _mock_get(path, params), 200


def post(path, json=None, token=None):
    """POST API_BASE_URL + path. Returns (data_dict, status_code)."""
    global _backend_offline
    try:
        r = requests.post(
            API_BASE_URL + path,
            json=json or {},
            headers=_headers(token),
            timeout=5,
        )
        if not _is_dreamspace_response(r):
            raise requests.exceptions.ConnectionError("Not a DreamSpace backend")
        _backend_offline = False
        try:
            return r.json(), r.status_code
        except Exception:
            return {}, r.status_code
    except requests.exceptions.ConnectionError:
        _backend_offline = True
        return _mock_post(path, json), 201
    except Exception:
        _backend_offline = True
        return _mock_post(path, json), 201


def put(path, json=None, token=None):
    """PUT API_BASE_URL + path. Returns (data_dict, status_code)."""
    global _backend_offline
    try:
        r = requests.put(
            API_BASE_URL + path,
            json=json or {},
            headers=_headers(token),
            timeout=5,
        )
        if not _is_dreamspace_response(r):
            raise requests.exceptions.ConnectionError("Not a DreamSpace backend")
        _backend_offline = False
        try:
            return r.json(), r.status_code
        except Exception:
            return {}, r.status_code
    except requests.exceptions.ConnectionError:
        _backend_offline = True
        return {"success": True}, 200
    except Exception:
        _backend_offline = True
        return {"success": True}, 200


def is_offline():
    return _backend_offline


# ── Static mock data ───────────────────────────────────────────────

_MOCK_CHALLENGES = [
    {
        "id": "pattern-1", "title": "Pattern Recognition",
        "description": "Identify the next item in a sequence",
        "difficulty": "beginner", "category": "Patterns", "points": 10,
        "question": "What comes next? 🔴 🔵 🔴 🔵 🔴 ?",
        "options": ["🔴 Red", "🔵 Blue", "🟢 Green", "🟡 Yellow"],
        "correctAnswer": 1,
        "explanation": "The pattern alternates between red and blue.",
        "ageGroup": "8-12",
    },
    {
        "id": "sequence-1", "title": "Number Sequence",
        "description": "Find the pattern in numbers",
        "difficulty": "beginner", "category": "Logic", "points": 10,
        "question": "What number comes next? 2, 4, 6, 8, __",
        "options": ["9", "10", "11", "12"],
        "correctAnswer": 1,
        "explanation": "Each number increases by 2. 8 + 2 = 10!",
        "ageGroup": "8-12",
    },
    {
        "id": "variables-1", "title": "Variable Storage",
        "description": "Understanding variables",
        "difficulty": "intermediate", "category": "Variables", "points": 20,
        "question": "If x = 5 and y = 3, what is x + y?",
        "options": ["2", "8", "15", "53"],
        "correctAnswer": 1,
        "explanation": "Variables store values. 5 + 3 = 8.",
        "ageGroup": "12-15",
    },
    {
        "id": "recursion-1", "title": "Recursive Thinking",
        "description": "Understanding recursion",
        "difficulty": "advanced", "category": "Recursion", "points": 30,
        "question": "What is the factorial of 4? (4! = 4 × 3 × 2 × 1)",
        "options": ["10", "16", "24", "32"],
        "correctAnswer": 2,
        "explanation": "4 × 3 × 2 × 1 = 24",
        "ageGroup": "15-18",
    },
]

_MOCK_TEAMS = [
    {
        "id": "team-1", "name": "Class 3A", "totalPoints": 150,
        "members": [
            {"id": "m1", "name": "StarCoder", "avatar": "🚀", "points": 80},
            {"id": "m2", "name": "PixelWiz", "avatar": "⭐", "points": 70},
        ],
    },
    {
        "id": "team-2", "name": "Class 4B", "totalPoints": 120,
        "members": [
            {"id": "m3", "name": "ByteRunner", "avatar": "💻", "points": 60},
            {"id": "m4", "name": "NeonHack", "avatar": "🌟", "points": 60},
        ],
    },
    {
        "id": "team-3", "name": "Class 5C", "totalPoints": 90,
        "members": [
            {"id": "m5", "name": "QuantumQ", "avatar": "🌙", "points": 90},
        ],
    },
]


def _mock_get(path, params=None):
    if "/challenges/daily" in path:
        return _MOCK_CHALLENGES[0]
    if "/challenges" in path and "/" not in path.replace("/api/kids/challenges", ""):
        diff = (params or {}).get("difficulty")
        if diff:
            return [c for c in _MOCK_CHALLENGES if c["difficulty"] == diff]
        return _MOCK_CHALLENGES
    if "/challenges/" in path:
        cid = path.split("/")[-1]
        return next((c for c in _MOCK_CHALLENGES if c["id"] == cid), _MOCK_CHALLENGES[0])
    if "/teams/rankings" in path:
        return sorted(_MOCK_TEAMS, key=lambda t: t["totalPoints"], reverse=True)
    if "/members/rankings" in path:
        members = []
        for t in _MOCK_TEAMS:
            for m in t["members"]:
                members.append({**m, "teamName": t["name"]})
        return sorted(members, key=lambda m: m["points"], reverse=True)
    # Specific team by ID (e.g. /api/kids/teams/team-1) — must come before general /teams check
    if "/teams/" in path and "/members" not in path and "/rankings" not in path:
        tid = path.split("/")[-1]
        return next((t for t in _MOCK_TEAMS if t["id"] == tid), _MOCK_TEAMS[0])
    if "/teams" in path and "/members" not in path:
        return _MOCK_TEAMS
    if "/results/" in path:
        return []
    if "/profile/" in path and "/stats" in path:
        return {"totalPoints": 0, "streak": 0, "accuracy": 0}
    if "/profile/" in path:
        return {}   # empty dict → caller sees no teamId → triggers onboarding
    return {}


def _mock_post(path, data=None):
    if "/auth/login" in path or "/auth/signup" in path:
        name = (data or {}).get("name", "Demo Student")
        return {
            "success": True,
            "token": "demo-token",
            "role": "student",
            "studentId": "student-demo",
            "name": name,
        }
    if "/complete" in path:
        correct = (data or {}).get("correct", False)
        return {
            "success": True,
            "resultId": "mock-result",
            "correct": correct,
            "pointsAwarded": 10 if correct else 0,
        }
    if "/join-class" in path:
        return {"success": True, "classId": "class-demo"}
    return {"success": True}
