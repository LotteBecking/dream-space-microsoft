from __future__ import annotations

import sqlite3
from pathlib import Path

from flask import Flask, jsonify, render_template, request

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "ab_test.db"

app = Flask(__name__, template_folder=str(BASE_DIR), static_folder=str(BASE_DIR / "static"))


def get_db() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    with get_db() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS votes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                design TEXT NOT NULL CHECK (design IN ('A', 'B', 'C')),
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )


@app.get("/")
def vote_screen():
    return render_template("dashboard.html")


@app.get("/results")
def results_screen():
    return render_template("results.html")


@app.post("/api/vote")
def save_vote():
    payload = request.get_json(silent=True) or {}
    design = str(payload.get("design", "")).strip().upper()

    if design not in {"A", "B", "C"}:
        return jsonify({"error": "Design must be A, B, or C"}), 400

    with get_db() as conn:
        conn.execute("INSERT INTO votes (design) VALUES (?)", (design,))

    return jsonify({"ok": True, "saved": design})


@app.get("/api/results")
def get_results():
    votes = {"A": 0, "B": 0, "C": 0}

    with get_db() as conn:
        rows = conn.execute(
            "SELECT design, COUNT(*) AS count FROM votes GROUP BY design"
        ).fetchall()
        for row in rows:
            votes[row["design"]] = int(row["count"])

        last = conn.execute(
            "SELECT design FROM votes ORDER BY id DESC LIMIT 1"
        ).fetchone()

    total_votes = votes["A"] + votes["B"] + votes["C"]
    max_votes = max(votes.values())
    most_liked = [design for design, count in votes.items() if count == max_votes and count > 0]

    return jsonify(
        {
            "votes": votes,
            "favorite": last["design"] if last else None,
            "most_liked": most_liked,
            "total_votes": total_votes,
        }
    )


@app.post("/api/reset")
def reset_results():
    with get_db() as conn:
        conn.execute("DELETE FROM votes")

    return jsonify({"ok": True})


if __name__ == "__main__":
    init_db()
    app.run(debug=True, host="127.0.0.1", port=5001)
