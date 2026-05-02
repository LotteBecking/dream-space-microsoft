"""Dreaming in Space -- Lesson 1 Flask app (student-facing).

Routes:
    /                       -- Home dashboard (resume, progress, path)
    /lesson/1/intro         -- Lesson intro (overview, vocab, role model)
    /simulator              -- PB&J sandwich simulator
    /exercise/<1|2|3>       -- Stepped exercises
    /review                 -- Recap/completion (includes Extensions)
    /reset                  -- Clear session
"""

from flask import (
    Flask, render_template, request, session, redirect, url_for,
)
import os
import random
import copy
from difflib import get_close_matches

# All lesson & world content is loaded via data/__init__.py
from data import ALL_LESSONS, ALL_WORLDS
from data.lessons.lesson1 import (
    LESSON, ROLE_MODEL, VOCABULARY, OBJECTIVES,
    EXERCISES, TEA_STEPS_CORRECT, TEA_STEPS_ALT, TASK_BLOCKS, CHALLENGES,
    INITIAL_SANDWICH_STATE, COMMAND_ALIASES,
    CHEF_LUNCH_ITEMS, CHEF_BLOCKS, CHEF_IF_CONDITIONS, CHEF_THEN_ACTIONS,
)

app = Flask(__name__)
app.secret_key = os.environ.get(
    "SECRET_KEY", "dreamspace-lesson1-dev-key-change-in-production"
)

# ---------------------------------------------------------------------------
# Session helpers
# ---------------------------------------------------------------------------

def get_progress():
    """Return (and lazily initialise) student progress stored in the session."""
    if "initialized" not in session:
        session["completed_exercises"] = []
        session["exercise_answers"] = {}
        session["exit_ticket_1"] = ""
        session["exit_ticket_2"] = ""
        session["simulator_completed"] = False
        session["simulator_confusion_count"] = 0
        session["simulator_state"] = copy.deepcopy(INITIAL_SANDWICH_STATE)
        session["simulator_log"] = []
        session["simulator_commands"] = []
        session["attempt_counts"] = {"1": 0, "2": 0, "3": 0}
        session["initialized"] = True

    # Backfill attempt_counts for older sessions
    if "attempt_counts" not in session:
        session["attempt_counts"] = {"1": 0, "2": 0, "3": 0}

    completed = session.get("completed_exercises", [])
    all_done = len(completed) >= 3
    sim_done = session.get("simulator_completed", False)

    # Figure out the next resumable step for the Continue card.
    if not sim_done and not completed:
        resume = {"label": "Start practicing", "href": "/simulator", "step": "intro"}
    elif not sim_done:
        resume = {"label": "Try the Simulator", "href": "/simulator", "step": "intro"}
    elif 1 not in completed:
        resume = {"label": "Mission 1: Sort the Steps", "href": "/exercise/1", "step": "ex1"}
    elif 2 not in completed:
        resume = {"label": "Mission 2: Write the Algorithm", "href": "/exercise/2", "step": "ex2"}
    elif 3 not in completed:
        resume = {"label": "Mission 3: Robot Chef", "href": "/exercise/3", "step": "ex3"}
    else:
        resume = {"label": "Claim your Rewards!", "href": "/review", "step": "recap"}

    return {
        "completed_exercises": completed,
        "progress_percent": round(len(completed) / 3 * 100),
        "simulator_completed": sim_done,
        "simulator_confusion_count": session.get("simulator_confusion_count", 0),
        "all_exercises_done": all_done,
        "resume": resume,
    }


# ---------------------------------------------------------------------------
# Universal XP & Achievement system (all lessons)
# ---------------------------------------------------------------------------

TRACK_1_LESSONS = [1, 2, 3, 4, 5]
XP_PER_EXERCISE = 25
XP_PER_QUIZ = 10
XP_PER_SIMULATOR = 25


def get_total_xp():
    """Calculate total XP earned across all lessons."""
    xp = 0
    # Lesson 1 (special)
    if session.get("simulator_completed"):
        xp += XP_PER_SIMULATOR
    xp += len(session.get("completed_exercises", [])) * XP_PER_EXERCISE
    # Lessons 2+
    for lnum in range(2, 19):
        key = f"lesson_{lnum}"
        if key in session:
            completed = session[key].get("completed_exercises", [])
            xp += len(completed) * XP_PER_EXERCISE
    # Quiz bonuses
    xp += session.get("quiz_bonuses", 0)
    return xp


def get_player_level(xp):
    """Calculate level from XP. Levels: 1 (0), 2 (100), 3 (250), 4 (500), 5 (800)."""
    thresholds = [(800, 5), (500, 4), (250, 3), (100, 2)]
    for threshold, level in thresholds:
        if xp >= threshold:
            return level
    return 1


def get_level_title(level):
    """Get title for a given level."""
    titles = {1: "Explorer", 2: "Coder", 3: "Developer", 4: "Engineer", 5: "Commander"}
    return titles.get(level, "Explorer")


def get_track1_progress():
    """Get completion stats for all Track 1 lessons."""
    stats = {}
    # Lesson 1
    l1_completed = session.get("completed_exercises", [])
    sim_done = session.get("simulator_completed", False)
    stats[1] = {
        "completed": len(l1_completed) >= 3 and sim_done,
        "exercises_done": len(l1_completed) + (1 if sim_done else 0),
        "total": 4,
        "title": "How Does a Computer Think?",
    }
    # Lessons 2-5
    lesson_titles = {
        2: "Give Your Robot Commands",
        3: "The Loop Station",
        4: "The If-Then Gates",
        5: "Break It Down",
    }
    for lnum in [2, 3, 4, 5]:
        key = f"lesson_{lnum}"
        completed = session.get(key, {}).get("completed_exercises", [])
        stats[lnum] = {
            "completed": len(completed) >= 3,
            "exercises_done": len(completed),
            "total": 3,
            "title": lesson_titles.get(lnum, ""),
        }
    return stats


ALL_ACHIEVEMENTS = [
    # Lesson 1
    {"id": "first_launch", "icon": "🚀", "title": "First Launch", "desc": "You completed the PB&J Simulator!"},
    {"id": "l1_champion", "icon": "🌟", "title": "Lesson 1 Champion", "desc": "All of Lesson 1 complete!"},
    # Lesson 2
    {"id": "robot_pilot", "icon": "🤖", "title": "Robot Pilot", "desc": "You can navigate and debug robots!"},
    # Lesson 3
    {"id": "loop_master", "icon": "🔄", "title": "Loop Master", "desc": "You've mastered loops and patterns!"},
    # Lesson 4
    {"id": "decision_maker", "icon": "🧠", "title": "Decision Maker", "desc": "You can write IF/THEN logic!"},
    # Lesson 5
    {"id": "architect", "icon": "🏗️", "title": "Architect", "desc": "You can break any problem down!"},
    # Track-wide
    {"id": "track1_complete", "icon": "🏆", "title": "Track 1 Complete", "desc": "All 5 Foundation lessons done!"},
    # Skill-based
    {"id": "first_try", "icon": "🎯", "title": "First Try!", "desc": "You nailed a mission on the first attempt!"},
    {"id": "perseverance", "icon": "💪", "title": "Never Give Up", "desc": "You kept trying and succeeded!"},
    {"id": "level_2", "icon": "⬆️", "title": "Level Up!", "desc": "You reached Level 2 — Coder!"},
    {"id": "level_3", "icon": "🚀", "title": "Developer", "desc": "You reached Level 3 — Developer!"},
    {"id": "level_5", "icon": "👑", "title": "Commander", "desc": "Maximum level — you are a Commander!"},
    {"id": "xp_100", "icon": "💎", "title": "Century Club", "desc": "You earned 100 XP!"},
    {"id": "xp_500", "icon": "🌠", "title": "Galaxy Brain", "desc": "You earned 500 XP!"},
    {"id": "quiz_ace", "icon": "📝", "title": "Quiz Ace", "desc": "You scored 100% on a quiz!"},
    {"id": "quiz_streak_3", "icon": "🔥", "title": "Quiz Streak", "desc": "Aced 3 quizzes in a row!"},
    {"id": "world_explorer", "icon": "🌍", "title": "World Explorer", "desc": "Cleared your first Digital World!"},
    {"id": "world_master", "icon": "🪐", "title": "World Master", "desc": "Cleared every Digital World!"},
]


def _all_lesson_attempts():
    """Yield (lesson_num, ex_num, attempts) over every lesson + exercise tracked."""
    # Lesson 1 attempts live at top-level for legacy reasons.
    for k, v in session.get("attempt_counts", {}).items():
        yield 1, k, v
    for ln in range(2, 19):
        ldata = session.get(f"lesson_{ln}", {})
        for k, v in ldata.get("attempt_counts", {}).items():
            yield ln, k, v


def check_new_achievements():
    """Check which achievements are newly earned and return them."""
    seen = set(session.get("seen_achievements", []))
    earned = set()

    # Lesson 1
    if session.get("simulator_completed"):
        earned.add("first_launch")
    l1_completed = session.get("completed_exercises", [])
    if len(l1_completed) >= 3:
        earned.add("l1_champion")

    # Lessons 2-5
    lesson_ach = {2: "robot_pilot", 3: "loop_master", 4: "decision_maker", 5: "architect"}
    all_track1_done = len(l1_completed) >= 3
    for lnum, ach_id in lesson_ach.items():
        key = f"lesson_{lnum}"
        completed = session.get(key, {}).get("completed_exercises", [])
        if len(completed) >= 3:
            earned.add(ach_id)
        else:
            all_track1_done = False

    if all_track1_done and session.get("simulator_completed"):
        earned.add("track1_complete")

    # Skill-based, now across ALL lessons
    completed_first_try = False
    perseverance_seen = False
    for ln, ex, atts in _all_lesson_attempts():
        # Was this exercise actually completed?
        if ln == 1:
            done = int(ex) in l1_completed
        else:
            done = int(ex) in session.get(f"lesson_{ln}", {}).get("completed_exercises", [])
        if done and atts == 1:
            completed_first_try = True
        if done and atts >= 3:
            perseverance_seen = True
    if completed_first_try:
        earned.add("first_try")
    if perseverance_seen:
        earned.add("perseverance")

    # XP-based
    xp = get_total_xp()
    if xp >= 100:
        earned.add("xp_100")
    if xp >= 500:
        earned.add("xp_500")
    lvl = get_player_level(xp)
    if lvl >= 2:
        earned.add("level_2")
    if lvl >= 3:
        earned.add("level_3")
    if lvl >= 5:
        earned.add("level_5")

    # Quiz ace, now per-lesson
    perfect_quizzes = set(session.get("quiz_perfect_lessons", []))
    if session.get("quiz_perfect"):
        # back-compat: legacy single flag still grants the achievement
        perfect_quizzes.add(0)
    if perfect_quizzes:
        earned.add("quiz_ace")
    if len(perfect_quizzes) >= 3:
        earned.add("quiz_streak_3")

    # Worlds
    worlds_done = 0
    for slug in ALL_WORLDS:
        wdata = session.get(f"world_{slug}", {})
        if len(wdata.get("completed_missions", [])) >= 3:
            worlds_done += 1
    if worlds_done >= 1:
        earned.add("world_explorer")
    if worlds_done >= len(ALL_WORLDS):
        earned.add("world_master")

    new_ids = earned - seen
    if new_ids:
        session["seen_achievements"] = list(earned)
        session.modified = True

    return [a for a in ALL_ACHIEVEMENTS if a["id"] in new_ids]


XP_LEVEL_THRESHOLDS = [0, 100, 250, 500, 800]

@app.context_processor
def inject_globals():
    """Make XP, level, achievements, and level-up info available in every template."""
    try:
        xp = get_total_xp()
        level = get_player_level(xp)
        # Calculate XP needed for next level
        next_threshold = XP_LEVEL_THRESHOLDS[level] if level < 5 else XP_LEVEL_THRESHOLDS[-1]
        xp_to_next = max(0, next_threshold - xp)
        prev_threshold = XP_LEVEL_THRESHOLDS[level - 1] if level > 1 else 0
        level_progress_pct = int(((xp - prev_threshold) / (next_threshold - prev_threshold)) * 100) if (next_threshold - prev_threshold) > 0 else 100
        next_level_title = get_level_title(min(level + 1, 5))
        return {
            "new_achievements": check_new_achievements() if "initialized" in session else [],
            "global_xp": xp,
            "global_level": level,
            "global_level_title": get_level_title(level),
            "xp_to_next_level": xp_to_next,
            "next_level": min(level + 1, 5),
            "next_level_title": next_level_title,
            "level_progress_pct": level_progress_pct,
            "xp_per_exercise": XP_PER_EXERCISE,
            "at_max_level": level >= 5,
        }
    except Exception:
        return {"new_achievements": [], "global_xp": 0, "global_level": 1, "global_level_title": "Explorer",
                "xp_to_next_level": 100, "next_level": 2, "next_level_title": "Coder",
                "level_progress_pct": 0, "xp_per_exercise": 25, "at_max_level": False}


# ---------------------------------------------------------------------------
# Simulator engine  (logic unchanged -- only UI is being redesigned)
# ---------------------------------------------------------------------------

ALL_ALIASES = []
for aliases in COMMAND_ALIASES.values():
    ALL_ALIASES.extend(aliases)


def parse_command(user_input: str):
    """Fuzzy-match *user_input* to a canonical command key, or return None."""
    text = user_input.strip().lower()
    if not text:
        return None

    for key, aliases in COMMAND_ALIASES.items():
        for alias in aliases:
            if alias == text:
                return key

    matches = get_close_matches(text, ALL_ALIASES, n=1, cutoff=0.55)
    if matches:
        for key, aliases in COMMAND_ALIASES.items():
            if matches[0] in aliases:
                return key
    return None


LITERAL_RESPONSES = [
    "I tried to '{cmd}' but I don't understand. I'm just a robot!",
    "'{cmd}'? My circuits are confused. Please use simpler words.",
    "Beep boop... '{cmd}' does not compute. Try being more specific!",
    "I stared at the bread and did nothing. '{cmd}' is not in my program.",
    "Error 404: instruction '{cmd}' not found in my recipe database.",
]


def execute_command(command_key: str, state: dict) -> dict:
    """Execute *command_key* against sandwich *state*."""
    s = state

    if command_key == "OPEN_BREAD_BAG":
        if s["bread_bag"] == "open":
            return {"type": "precondition_error",
                    "message": "The bread bag is already open."}
        s["bread_bag"] = "open"
        return {"type": "success", "message": "You opened the bread bag."}

    if command_key == "TAKE_BREAD_SLICE":
        if s["bread_bag"] != "open":
            return {"type": "precondition_error",
                    "message": "The bread bag is still closed! Open it first."}
        if s["bread_slices"] >= 2:
            return {"type": "precondition_error",
                    "message": "You already have 2 slices. That's enough!"}
        s["bread_slices"] += 1
        return {"type": "success",
                "message": f"You took bread slice #{s['bread_slices']}."}

    if command_key == "OPEN_PB_JAR":
        if s["pb_jar"] == "open":
            return {"type": "precondition_error",
                    "message": "The peanut butter jar is already open."}
        s["pb_jar"] = "open"
        return {"type": "success", "message": "You opened the peanut butter jar."}

    if command_key == "OPEN_JAM_JAR":
        if s["jam_jar"] == "open":
            return {"type": "precondition_error",
                    "message": "The jam jar is already open."}
        s["jam_jar"] = "open"
        return {"type": "success", "message": "You opened the jam jar."}

    if command_key == "GET_KNIFE":
        if s["knife_location"] == "hand":
            return {"type": "precondition_error",
                    "message": "You're already holding the knife."}
        s["knife_location"] = "hand"
        return {"type": "success", "message": "You picked up the knife."}

    if command_key == "APPLY_PB":
        errors = []
        if s["pb_jar"] != "open":
            errors.append("the peanut butter jar is closed")
        if s["knife_location"] != "hand":
            errors.append("you don't have the knife")
        if s["bread_slices"] < 1:
            errors.append("there's no bread on the plate")
        if s["pb_applied"]:
            errors.append("peanut butter is already on the bread")
        if errors:
            return {"type": "precondition_error",
                    "message": f"Can't spread peanut butter: {', '.join(errors)}."}
        s["pb_applied"] = True
        return {"type": "success",
                "message": "You spread peanut butter on the bread."}

    if command_key == "APPLY_JAM":
        errors = []
        if s["jam_jar"] != "open":
            errors.append("the jam jar is closed")
        if s["knife_location"] != "hand":
            errors.append("you don't have the knife")
        if s["bread_slices"] < 1:
            errors.append("there's no bread on the plate")
        if s["jam_applied"]:
            errors.append("jam is already on the bread")
        if errors:
            return {"type": "precondition_error",
                    "message": f"Can't spread jam: {', '.join(errors)}."}
        s["jam_applied"] = True
        return {"type": "success", "message": "You spread jam on the bread."}

    if command_key == "PLACE_SECOND_SLICE":
        if s["bread_slices"] < 2:
            return {"type": "precondition_error",
                    "message": "You need 2 slices of bread first."}
        if not s["pb_applied"] and not s["jam_applied"]:
            return {"type": "precondition_error",
                    "message": "You haven't spread anything on the bread yet!"}
        s["sandwich_complete"] = True
        return {"type": "success",
                "message": "You placed the second slice on top. The sandwich is assembled!"}

    if command_key == "SERVE":
        if not s["sandwich_complete"]:
            return {"type": "precondition_error",
                    "message": "The sandwich isn't complete yet!"}
        return {"type": "success",
                "message": "The sandwich is served! Great job, programmer!"}

    return {"type": "literal_interpretation",
            "message": "Unknown command."}


def process_user_command(user_input: str, state: dict) -> dict:
    """Parse and execute a user command. Returns result dict."""
    command_key = parse_command(user_input)
    if command_key is None:
        msg = random.choice(LITERAL_RESPONSES).format(cmd=user_input.strip())
        return {"type": "literal_interpretation", "message": msg}
    return execute_command(command_key, state)


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.route("/")
def home():
    progress = get_progress()

    # Universal XP tracking
    current_xp = get_total_xp()
    prev_xp = session.get("last_seen_xp", 0)
    xp_gained = max(0, current_xp - prev_xp)
    level = get_player_level(current_xp)
    prev_level = session.get("last_seen_level", 1)
    level_up = level > prev_level
    session["last_seen_xp"] = current_xp
    session["last_seen_level"] = level
    session.modified = True

    # Track 1 progress
    track1 = get_track1_progress()
    track1_lessons_done = sum(1 for s in track1.values() if s["completed"])
    track1_total_exercises = sum(s["exercises_done"] for s in track1.values())

    # Stars: 1 per completed lesson (5 total for Track 1)
    stars_earned = track1_lessons_done
    prev_stars = session.get("last_seen_stars", 0)
    stars_gained = max(0, stars_earned - prev_stars)
    session["last_seen_stars"] = stars_earned
    session.modified = True

    return render_template(
        "pages/home.html",
        lesson=LESSON,
        progress=progress,
        all_lessons=ALL_LESSONS,
        xp_gained=xp_gained,
        stars_gained=stars_gained,
        prev_xp=prev_xp,
        current_xp=current_xp,
        track1=track1,
        track1_lessons_done=track1_lessons_done,
        track1_total_exercises=track1_total_exercises,
        level_up=level_up,
    )


@app.route("/lesson/1/intro")
def lesson_intro():
    progress = get_progress()
    return render_template(
        "lesson1/intro.html",
        lesson=LESSON,
        role_model=ROLE_MODEL,
        vocabulary=VOCABULARY,
        objectives=OBJECTIVES,
        progress=progress,
    )


@app.route("/simulator", methods=["GET", "POST"])
def simulator():
    progress = get_progress()
    state = session.get("simulator_state", copy.deepcopy(INITIAL_SANDWICH_STATE))
    log = session.get("simulator_log", [])
    commands = session.get("simulator_commands", [])

    if request.method == "POST":
        action = request.form.get("action", "add")

        if action == "reset":
            session["simulator_state"] = copy.deepcopy(INITIAL_SANDWICH_STATE)
            session["simulator_log"] = []
            session["simulator_commands"] = []
            session["simulator_completed"] = False
            session["simulator_confusion_count"] = 0
            return redirect(url_for("simulator"))

        if action == "add":
            user_input = request.form.get("command", "").strip()
            if user_input:
                commands.append(user_input)
                session["simulator_commands"] = commands

        if action == "run":
            # If reordered commands were sent, use those instead
            reordered = request.form.getlist("cmd_order")
            if reordered:
                commands = reordered
                session["simulator_commands"] = commands
            state = copy.deepcopy(INITIAL_SANDWICH_STATE)
            log = []
            confusion = 0
            for cmd_text in commands:
                command_key = parse_command(cmd_text)
                result = process_user_command(cmd_text, state)
                log.append({"command": cmd_text, "command_key": command_key or "UNKNOWN", **result})
                if result["type"] == "literal_interpretation":
                    confusion += 1
            session["simulator_state"] = state
            session["simulator_log"] = log
            session["simulator_confusion_count"] = confusion
            if state["sandwich_complete"]:
                session["simulator_completed"] = True
            progress = get_progress()

        if action == "remove":
            idx = request.form.get("index")
            if idx is not None and idx.isdigit():
                idx = int(idx)
                if 0 <= idx < len(commands):
                    commands.pop(idx)
                    session["simulator_commands"] = commands

        session.modified = True
        return redirect(url_for("simulator"))

    return render_template(
        "pages/simulator.html",
        state=state,
        log=log,
        commands=commands,
        progress=progress,
    )


@app.route("/exercise/<int:num>", methods=["GET", "POST"])
def exercise(num):
    if num not in (1, 2, 3):
        return "Exercise not found", 404

    progress = get_progress()
    ex = EXERCISES[num - 1]
    error = None
    success = False

    if request.method == "POST":
        # Track attempt count
        attempts = session.get("attempt_counts", {"1": 0, "2": 0, "3": 0})
        attempts[str(num)] = attempts.get(str(num), 0) + 1
        session["attempt_counts"] = attempts
        session.modified = True

        if num == 1:
            # Sorting exercise (tea steps)
            order = request.form.getlist("order")
            if len(order) != 6:
                error = "Please put all 6 steps in order."
            else:
                submitted = [TEA_STEPS_CORRECT[int(i)] for i in order]
                session["exercise_answers"][str(num)] = submitted
                # Preserve user's submitted order for re-display
                session["tea_shuffle"] = [int(i) for i in order]
                if submitted == TEA_STEPS_CORRECT or submitted == TEA_STEPS_ALT:
                    if num not in session["completed_exercises"]:
                        session["completed_exercises"].append(num)
                    session.modified = True
                    success = True
                    progress = get_progress()
                else:
                    error = "Not quite right! The green ones are correct — fix the red ones."
                    session.modified = True

        elif num == 2:
            # Writing exercise (algorithm steps)
            steps = [
                request.form.get(f"step_{i}", "").strip()
                for i in range(1, 21)
            ]
            steps = [s for s in steps if s]
            if len(steps) < 6:
                error = "You need at least 6 steps. Keep going!"
            else:
                session["exercise_answers"][str(num)] = steps
                if num not in session["completed_exercises"]:
                    session["completed_exercises"].append(num)
                session.modified = True
                success = True
                progress = get_progress()

        elif num == 3:
            lunch_item = request.form.get("lunch_item", "").strip()
            steps = [
                request.form.get(f"step_{i}", "").strip()
                for i in range(1, 21)
            ]
            steps = [s for s in steps if s]
            allergy = request.form.get("allergy", "").strip()

            errors = []
            if not lunch_item:
                errors.append("Pick what to cook first!")
            if len(steps) < 6:
                errors.append("You need at least 6 cooking steps.")
            if not allergy:
                errors.append("Add at least one allergy safety rule.")
            if errors:
                error = " ".join(errors)
            else:
                session["exercise_answers"][str(num)] = {
                    "lunch_item": lunch_item,
                    "steps": steps,
                    "allergy": allergy,
                }
                if num not in session["completed_exercises"]:
                    session["completed_exercises"].append(num)
                session.modified = True
                success = True
                progress = get_progress()

    attempts = session.get("attempt_counts", {"1": 0, "2": 0, "3": 0})
    current_attempts = attempts.get(str(num), 0)

    context = {
        "exercise": ex,
        "num": num,
        "progress": progress,
        "error": error,
        "success": success,
        "attempts": current_attempts,
        "show_hint": current_attempts >= 2 and not success,
    }

    if num == 1:
        if "tea_shuffle" not in session:
            indices = list(range(6))
            random.shuffle(indices)
            session["tea_shuffle"] = indices
            session.modified = True
        context["tea_steps"] = TEA_STEPS_CORRECT
        context["shuffled_indices"] = session["tea_shuffle"]

    if num == 2:
        context["task_blocks"] = TASK_BLOCKS

    if num == 3:
        context["chef_items"] = CHEF_LUNCH_ITEMS
        context["chef_blocks"] = CHEF_BLOCKS
        context["chef_conditions"] = CHEF_IF_CONDITIONS
        context["chef_actions"] = CHEF_THEN_ACTIONS

    template = f"lesson1/exercise{num}.html"
    return render_template(template, **context)


@app.route("/review", methods=["GET", "POST"])
def review():
    progress = get_progress()
    success = False

    if request.method == "POST":
        session["exit_ticket_1"] = request.form.get("blank1", "").strip()
        session["exit_ticket_2"] = request.form.get("blank2", "").strip()
        session.modified = True
        if session["exit_ticket_1"] and session["exit_ticket_2"]:
            success = True

    return render_template(
        "lesson1/review.html",
        vocabulary=VOCABULARY,
        challenges=CHALLENGES,
        progress=progress,
        exit_ticket_1=session.get("exit_ticket_1", ""),
        exit_ticket_2=session.get("exit_ticket_2", ""),
        success=success,
    )


@app.route("/reset", methods=["POST"])
def reset():
    session.clear()
    return redirect(url_for("home"))


@app.route("/profile")
def profile():
    progress = get_progress()
    track1 = get_track1_progress()
    xp = get_total_xp()
    level = get_player_level(xp)
    attempts = session.get("attempt_counts", {"1": 0, "2": 0, "3": 0})
    completed = session.get("completed_exercises", [])

    # Build all achievements
    seen = set(session.get("seen_achievements", []))
    achievements = [
        {**a, "done": a["id"] in seen or _ach_earned(a["id"])}
        for a in ALL_ACHIEVEMENTS
    ]

    # Track 1 lesson stats
    lesson_stats = []
    for lnum in TRACK_1_LESSONS:
        s = track1[lnum]
        lesson_stats.append({
            "num": lnum,
            "title": s["title"],
            "completed": s["completed"],
            "exercises_done": s["exercises_done"],
            "total": s["total"],
        })

    track1_lessons_done = sum(1 for s in track1.values() if s["completed"])

    return render_template(
        "pages/profile.html",
        progress=progress,
        achievements=achievements,
        lesson_stats=lesson_stats,
        total_xp=xp,
        level=level,
        level_title=get_level_title(level),
        track1_lessons_done=track1_lessons_done,
        medals_earned=sum(1 for a in achievements if a["done"]),
        total_medals=len(achievements),
    )


def _ach_earned(ach_id):
    """Check if an achievement is currently earned (for profile display)."""
    l1 = session.get("completed_exercises", [])
    sim = session.get("simulator_completed", False)
    lesson_ach = {2: "robot_pilot", 3: "loop_master", 4: "decision_maker", 5: "architect"}

    if ach_id == "first_launch":
        return sim
    if ach_id == "l1_champion":
        return len(l1) >= 3
    if ach_id in lesson_ach.values():
        for lnum, aid in lesson_ach.items():
            if aid == ach_id:
                return len(session.get(f"lesson_{lnum}", {}).get("completed_exercises", [])) >= 3
    if ach_id == "track1_complete":
        return all(
            len(session.get(f"lesson_{n}", {}).get("completed_exercises", [])) >= 3
            for n in [2, 3, 4, 5]
        ) and len(l1) >= 3 and sim
    if ach_id == "first_try":
        # check L1 + every lesson 2+
        l1_atts = session.get("attempt_counts", {})
        if any(l1_atts.get(str(i), 99) == 1 for i in l1):
            return True
        for ln in range(2, 19):
            ldata = session.get(f"lesson_{ln}", {})
            done = ldata.get("completed_exercises", [])
            atts = ldata.get("attempt_counts", {})
            if any(atts.get(str(i), 99) == 1 for i in done):
                return True
        return False
    if ach_id == "perseverance":
        l1_atts = session.get("attempt_counts", {})
        if any(l1_atts.get(str(i), 0) >= 3 for i in l1):
            return True
        for ln in range(2, 19):
            ldata = session.get(f"lesson_{ln}", {})
            done = ldata.get("completed_exercises", [])
            atts = ldata.get("attempt_counts", {})
            if any(atts.get(str(i), 0) >= 3 for i in done):
                return True
        return False
    if ach_id == "xp_100":
        return get_total_xp() >= 100
    if ach_id == "xp_500":
        return get_total_xp() >= 500
    if ach_id == "level_2":
        return get_player_level(get_total_xp()) >= 2
    if ach_id == "level_3":
        return get_player_level(get_total_xp()) >= 3
    if ach_id == "level_5":
        return get_player_level(get_total_xp()) >= 5
    if ach_id == "quiz_ace":
        return session.get("quiz_perfect", False) or len(session.get("quiz_perfect_lessons", [])) > 0
    if ach_id == "quiz_streak_3":
        return len(session.get("quiz_perfect_lessons", [])) >= 3
    if ach_id == "world_explorer":
        for slug in ALL_WORLDS:
            if len(session.get(f"world_{slug}", {}).get("completed_missions", [])) >= 3:
                return True
        return False
    if ach_id == "world_master":
        return all(
            len(session.get(f"world_{slug}", {}).get("completed_missions", [])) >= 3
            for slug in ALL_WORLDS
        )
    return False


# ---------------------------------------------------------------------------
# Multi-lesson routes (Lessons 2-4, Track 1)
# ---------------------------------------------------------------------------

def get_lesson_progress(lesson_num):
    """Get progress for a specific lesson (2+)."""
    key = f"lesson_{lesson_num}"
    if key not in session:
        session[key] = {"completed_exercises": [], "exercise_answers": {}}
        session.modified = True
    data = session[key]
    completed = data.get("completed_exercises", [])
    return {
        "completed_exercises": completed,
        "progress_percent": round(len(completed) / 3 * 100) if 3 else 0,
        "all_exercises_done": len(completed) >= 3,
    }


@app.route("/lesson/<int:lesson_num>")
def lesson_home(lesson_num):
    """Home page for lessons 2+."""
    if lesson_num not in ALL_LESSONS or lesson_num == 1:
        return redirect(url_for("home"))
    info = ALL_LESSONS[lesson_num]
    progress = get_lesson_progress(lesson_num)
    return render_template(
        "lessons/home.html",
        lesson=info["lesson"],
        role_model=info["role_model"],
        vocabulary=info["vocabulary"],
        objectives=info["objectives"],
        progress=progress,
        lesson_num=lesson_num,
    )


@app.route("/lesson/<int:lesson_num>/exercise/<int:ex_num>", methods=["GET", "POST"])
def lesson_exercise(lesson_num, ex_num):
    """Exercise pages for lessons 2+."""
    if lesson_num not in ALL_LESSONS or lesson_num == 1:
        return redirect(url_for("home"))
    info = ALL_LESSONS[lesson_num]
    exercises = info["exercises"]
    if ex_num < 1 or ex_num > len(exercises):
        return "Exercise not found", 404

    progress = get_lesson_progress(lesson_num)
    ex = exercises[ex_num - 1]
    key = f"lesson_{lesson_num}"
    lesson_data = session.setdefault(key, {"completed_exercises": [], "exercise_answers": {}})
    if "attempt_counts" not in lesson_data:
        lesson_data["attempt_counts"] = {}
    error = None
    success = False
    _debug_result = None

    if request.method == "POST":
        ex_type = ex.get("type", "written")

        # Count this attempt against this exercise
        atts = lesson_data.setdefault("attempt_counts", {})
        atts[str(ex_num)] = atts.get(str(ex_num), 0) + 1
        session.modified = True

        if ex_type == "robot_maze":
            # Server-side enforcement: must have actually solved the maze (frontend
            # only sets `solved=1` when the JS reaches the goal cell).
            cmds = request.form.get("commands", "").strip()
            solved = request.form.get("solved", "").strip() == "1"
            min_steps = ex.get("min_steps", 1)
            cmd_count = len([c for c in cmds.split(",") if c.strip()]) if cmds else 0
            if not cmds:
                error = "Run your program and reach the goal first!"
            elif not solved:
                error = "Your robot didn't reach the goal yet — try a different path!"
            elif cmd_count < min_steps:
                error = f"You can do better — this maze needs at least {min_steps} moves!"
            else:
                if ex_num not in lesson_data["completed_exercises"]:
                    lesson_data["completed_exercises"].append(ex_num)
                session.modified = True
                success = True
                progress = get_lesson_progress(lesson_num)

        elif ex_type == "robot_commands":
            steps = [request.form.get(f"step_{i}", "").strip() for i in range(1, 21)]
            steps = [s for s in steps if s]
            min_steps = ex.get("min_steps", 5)
            if len(steps) < min_steps:
                error = f"Your robot needs at least {min_steps} commands. Keep going!"
            else:
                if ex_num not in lesson_data["completed_exercises"]:
                    lesson_data["completed_exercises"].append(ex_num)
                session.modified = True
                success = True
                progress = get_lesson_progress(lesson_num)

        elif ex_type == "robot_debug" or ex_type == "bug_hunt":
            bugs = ex.get("bugs", [])
            has_mcq = any("fixes" in b for b in bugs)

            if has_mcq:
                # MCQ mode: check radio selections
                all_answered = True
                correct_bugs = []
                answers = {}
                for i, bug in enumerate(bugs):
                    val = request.form.get(f"fix_{i}", "")
                    if val == "":
                        all_answered = False
                    else:
                        answers[str(i)] = int(val)
                        if int(val) == bug.get("correct_fix", -1):
                            correct_bugs.append(i)

                if not all_answered:
                    error = "Pick a fix for every bug before submitting!"
                else:
                    result = {"correct_bugs": correct_bugs, "answers": answers}
                    _debug_result = result
                    if len(correct_bugs) == len(bugs):
                        # All correct!
                        if ex_num not in lesson_data["completed_exercises"]:
                            lesson_data["completed_exercises"].append(ex_num)
                        session.modified = True
                        success = True
                        progress = get_lesson_progress(lesson_num)
                    else:
                        error = f"You got {len(correct_bugs)}/{len(bugs)} correct. The wrong ones are highlighted in red — try again!"
            else:
                # Textarea mode (fallback)
                all_filled = True
                for i in range(len(bugs)):
                    if not request.form.get(f"fix_{i}", "").strip():
                        all_filled = False
                if not all_filled:
                    error = "Please write a fix for every bug!"
                else:
                    if ex_num not in lesson_data["completed_exercises"]:
                        lesson_data["completed_exercises"].append(ex_num)
                    session.modified = True
                    success = True
                    progress = get_lesson_progress(lesson_num)

        elif ex_type == "precision_rewrite":
            vague = ex.get("vague_instructions", [])
            all_filled = True
            for i in range(len(vague)):
                steps = [request.form.get(f"rewrite_{i}_step_{j}", "").strip() for j in range(1, 10)]
                steps = [s for s in steps if s]
                if len(steps) < vague[i].get("min_steps", 3):
                    all_filled = False
            if not all_filled:
                error = "Each vague instruction needs enough precise steps. Keep going!"
            else:
                if ex_num not in lesson_data["completed_exercises"]:
                    lesson_data["completed_exercises"].append(ex_num)
                session.modified = True
                success = True
                progress = get_lesson_progress(lesson_num)

        elif ex_type == "spot_loop":
            problems = ex.get("problems", [])
            answers = {}
            correct_idxs = []
            for i, p in enumerate(problems):
                raw = request.form.get(f"count_{i}", "").strip()
                try:
                    val = int(raw)
                except (TypeError, ValueError):
                    val = None
                answers[str(i)] = val
                if val is not None and val == p.get("repeat_count"):
                    correct_idxs.append(i)
            unanswered = [i for i, p in enumerate(problems) if answers.get(str(i)) is None]
            _debug_result = {"answers": answers, "correct_idxs": correct_idxs}
            if unanswered:
                error = "Pick how many times the pattern repeats for every routine!"
            elif len(correct_idxs) < len(problems):
                error = f"You spotted {len(correct_idxs)}/{len(problems)} patterns. The wrong ones are highlighted — try again!"
            else:
                if ex_num not in lesson_data["completed_exercises"]:
                    lesson_data["completed_exercises"].append(ex_num)
                session.modified = True
                success = True
                progress = get_lesson_progress(lesson_num)

        elif ex_type == "rewrite_loop":
            problems = ex.get("problems", [])
            answers = {}
            correct_idxs = []
            for i, p in enumerate(problems):
                raw = request.form.get(f"times_{i}", "").strip()
                try:
                    val = int(raw)
                except (TypeError, ValueError):
                    val = None
                answers[str(i)] = val
                if val is not None and val == p.get("answer_times"):
                    correct_idxs.append(i)
            unanswered = [i for i, p in enumerate(problems) if answers.get(str(i)) is None]
            _debug_result = {"answers": answers, "correct_idxs": correct_idxs}
            if unanswered:
                error = "Pick the loop count for every problem!"
            elif len(correct_idxs) < len(problems):
                error = f"You got {len(correct_idxs)}/{len(problems)} loops right. Check the red ones!"
            else:
                if ex_num not in lesson_data["completed_exercises"]:
                    lesson_data["completed_exercises"].append(ex_num)
                session.modified = True
                success = True
                progress = get_lesson_progress(lesson_num)

        elif ex_type == "read_conditional":
            problems = ex.get("problems", [])
            answers = {}
            correct_idxs = []
            for i, p in enumerate(problems):
                raw = request.form.get(f"q{i}")
                try:
                    val = int(raw) if raw is not None else None
                except (TypeError, ValueError):
                    val = None
                answers[str(i)] = val
                if val is not None and val == p["correct"]:
                    correct_idxs.append(i)
            unanswered = [i for i, p in enumerate(problems) if answers.get(str(i)) is None]
            _debug_result = {"answers": answers, "correct_idxs": correct_idxs}
            if unanswered:
                error = "Pick an answer for every question!"
            elif len(correct_idxs) < len(problems):
                error = f"You got {len(correct_idxs)}/{len(problems)} right. The wrong ones are highlighted — try again!"
            else:
                if ex_num not in lesson_data["completed_exercises"]:
                    lesson_data["completed_exercises"].append(ex_num)
                session.modified = True
                success = True
                progress = get_lesson_progress(lesson_num)

        elif ex_type == "write_conditional":
            steps = [request.form.get(f"step_{i}", "").strip() for i in range(1, 21)]
            steps = [s for s in steps if s]
            if len(steps) < ex.get("min_lines", 3):
                error = f"Write at least {ex.get('min_lines', 3)} lines of IF/ELSE logic!"
            else:
                if ex_num not in lesson_data["completed_exercises"]:
                    lesson_data["completed_exercises"].append(ex_num)
                session.modified = True
                success = True
                progress = get_lesson_progress(lesson_num)

        elif ex_type == "grouping":
            items = ex.get("jumbled_steps", [])
            correct = sum(1 for i, item in enumerate(items) if request.form.get(f"group_{i}", "") == item["group"])
            if correct < len(items):
                error = f"You got {correct}/{len(items)} correct. Check the ones you're unsure about!"
            else:
                if ex_num not in lesson_data["completed_exercises"]:
                    lesson_data["completed_exercises"].append(ex_num)
                session.modified = True
                success = True
                progress = get_lesson_progress(lesson_num)

        elif ex_type == "decompose":
            subtasks = []
            for i in range(1, 5):
                name = request.form.get(f"subtask_name_{i}", "").strip()
                steps = [request.form.get(f"subtask_{i}_step_{j}", "").strip() for j in range(1, 4)]
                steps = [s for s in steps if s]
                if name and len(steps) >= ex.get("min_steps_per_subtask", 2):
                    subtasks.append({"name": name, "steps": steps})
            if len(subtasks) < ex.get("min_subtasks", 3):
                error = f"You need at least {ex.get('min_subtasks', 3)} sub-tasks with {ex.get('min_steps_per_subtask', 2)}+ steps each!"
            else:
                if ex_num not in lesson_data["completed_exercises"]:
                    lesson_data["completed_exercises"].append(ex_num)
                session.modified = True
                success = True
                progress = get_lesson_progress(lesson_num)

        elif ex_type == "ordering_dependencies":
            scenarios = ex.get("scenarios", [])
            all_correct = True
            for si, scenario in enumerate(scenarios):
                for ti, st in enumerate(scenario["subtasks"]):
                    val = request.form.get(f"order_{si}_{ti}", "")
                    if not val.isdigit() or int(val) != st["order"]:
                        all_correct = False
            if not all_correct:
                error = "Not quite right! Think about which steps depend on others."
            else:
                if ex_num not in lesson_data["completed_exercises"]:
                    lesson_data["completed_exercises"].append(ex_num)
                session.modified = True
                success = True
                progress = get_lesson_progress(lesson_num)

    session[key] = lesson_data
    session.modified = True

    context = {
        "exercise": ex,
        "num": ex_num,
        "lesson_num": lesson_num,
        "lesson": info["lesson"],
        "progress": progress,
        "error": error,
        "success": success,
        "total_exercises": len(exercises),
    }
    # Always pass debug result (None if not submitted)
    if _debug_result is not None:
        context["result"] = _debug_result

    # Template mapping
    TEMPLATE_MAP = {
        "robot_maze": "lessons/exercises/maze.html",
        "robot_commands": "lessons/exercises/commands.html",
        "robot_debug": "lessons/exercises/bug_hunt.html",
        "precision_rewrite": "lessons/exercises/precision.html",
        "spot_loop": "lessons/exercises/spot_loop.html",
        "rewrite_loop": "lessons/exercises/rewrite_loop.html",
        "bug_hunt": "lessons/exercises/bug_hunt.html",
        "read_conditional": "lessons/exercises/read_conditional.html",
        "write_conditional": "lessons/exercises/write_conditional.html",
        "grouping": "lessons/exercises/grouping.html",
        "decompose": "lessons/exercises/decompose.html",
        "ordering_dependencies": "lessons/exercises/ordering.html",
    }
    ex_type = ex.get("type", "written")
    template = TEMPLATE_MAP.get(ex_type, "lessons/exercises/generic.html")
    return render_template(template, **context)


@app.route("/lesson/<int:lesson_num>/quiz", methods=["GET", "POST"])
def lesson_quiz(lesson_num):
    """Quiz for lessons 2+."""
    if lesson_num not in ALL_LESSONS or lesson_num == 1:
        return redirect(url_for("home"))
    quiz = ALL_LESSONS[lesson_num].get("quiz", [])
    lesson = ALL_LESSONS[lesson_num]["lesson"]
    result = None
    if request.method == "POST":
        answers, wrong = [], []
        for i, q in enumerate(quiz):
            ans = request.form.get(f"q{i}")
            ans = int(ans) if ans is not None else -1
            answers.append(ans)
            if ans != q["correct"]:
                wrong.append(i)
        score = len(quiz) - len(wrong)
        result = {
            "score": score, "total": len(quiz),
            "percent": round(score / len(quiz) * 100) if quiz else 0,
            "answers": answers, "wrong": wrong,
        }
        if result["percent"] >= 75:
            # Award the quiz XP only once per lesson, not on every retry
            awarded = set(session.get("quiz_xp_awarded", []))
            if lesson_num not in awarded:
                session["quiz_bonuses"] = session.get("quiz_bonuses", 0) + XP_PER_QUIZ
                awarded.add(lesson_num)
                session["quiz_xp_awarded"] = list(awarded)
            session.modified = True
        if result["percent"] == 100:
            session["quiz_perfect"] = True
            perfect = set(session.get("quiz_perfect_lessons", []))
            perfect.add(lesson_num)
            session["quiz_perfect_lessons"] = list(perfect)
            session.modified = True
    return render_template("lessons/quiz.html", questions=quiz, lesson_num=lesson_num, lesson=lesson, result=result, progress=get_lesson_progress(lesson_num))


@app.route("/lesson/<int:lesson_num>/recap", methods=["GET", "POST"])
def lesson_recap(lesson_num):
    """Recap/rewards page for lessons 2+."""
    if lesson_num not in ALL_LESSONS or lesson_num == 1:
        return redirect(url_for("home"))
    info = ALL_LESSONS[lesson_num]
    progress = get_lesson_progress(lesson_num)
    recap_key = f"recap_{lesson_num}"
    recap_submitted = False
    recap_error = None
    recap_answer = session.get(recap_key, "")

    if request.method == "POST":
        reflection = request.form.get("reflection", "").strip()
        if len(reflection) < 8:
            recap_error = "Your reflection is a bit short — try writing at least one full sentence!"
            recap_answer = reflection  # keep what they typed so they can edit
        else:
            session[recap_key] = reflection
            recap_answer = reflection
            recap_submitted = True
            session.modified = True

    if recap_answer and not recap_error and request.method != "POST":
        recap_submitted = True

    return render_template(
        "lessons/recap.html",
        lesson=info["lesson"],
        vocabulary=info["vocabulary"],
        objectives=info["objectives"],
        progress=progress,
        lesson_num=lesson_num,
        recap_submitted=recap_submitted,
        recap_answer=recap_answer,
        recap_error=recap_error,
    )


# ---------------------------------------------------------------------------
# World routes (Track 5: Digital Missions)
# ---------------------------------------------------------------------------

def get_world_progress(slug):
    key = f"world_{slug}"
    if key not in session:
        session[key] = {"completed_missions": [], "tools_unlocked": []}
        session.modified = True
    data = session[key]
    completed = data.get("completed_missions", [])
    return {
        "completed_missions": completed,
        "progress_percent": round(len(completed) / 3 * 100),
        "all_done": len(completed) >= 3,
        "tools_unlocked": data.get("tools_unlocked", []),
    }


@app.route("/world/<slug>")
def world_home(slug):
    if slug not in ALL_WORLDS:
        return redirect(url_for("home"))
    info = ALL_WORLDS[slug]
    progress = get_world_progress(slug)
    return render_template(
        "worlds/hub.html",
        world=info["world"],
        world_data=info["data"],
        progress=progress,
        slug=slug,
    )


@app.route("/world/<slug>/mission/<int:n>", methods=["GET", "POST"])
def world_mission(slug, n):
    if slug not in ALL_WORLDS or n not in (1, 2, 3):
        return redirect(url_for("home"))
    info = ALL_WORLDS[slug]
    world = info["world"]
    progress = get_world_progress(slug)
    mission = world["missions"][n - 1]

    if request.method == "POST":
        # Require that the user actually played the mission (set by the
        # in-page submitMission helper). This blocks accidental direct POSTs
        # without forcing a particular score.
        if not request.form.get("played"):
            return redirect(url_for("world_mission", slug=slug, n=n))

        key = f"world_{slug}"
        wdata = session.setdefault(key, {"completed_missions": [], "tools_unlocked": []})
        if n not in wdata["completed_missions"]:
            wdata["completed_missions"].append(n)
        session[key] = wdata
        session.modified = True
        if n < 3:
            return redirect(url_for("world_mission", slug=slug, n=n + 1))
        return redirect(url_for("world_reward", slug=slug))

    extra = {}
    if slug == "data-defender":
        pool = info["data"]["scenarios"]
        picked = random.sample(pool, min(4, len(pool)))
        if n == 1:
            extra["picked_scenarios"] = picked
        elif n == 2:
            extra["trick_case"] = random.choice(info["data"]["trick_cases"])
        elif n == 3:
            extra["repair_task"] = info["data"]["repair_tasks"][0]
            extra["tools"] = info["data"]["tools"]
    elif slug == "city-fixer":
        if n == 1:
            extra["route"] = random.choice(info["data"]["routes"])
        elif n == 2:
            extra["tradeoff"] = random.choice(info["data"]["tradeoffs"])
        elif n == 3:
            extra["disruption"] = random.choice(info["data"]["disruptions"])
    elif slug == "truth-quest":
        if n in (1, 2):
            extra["case"] = random.choice(info["data"]["cases"])
        elif n == 3:
            extra["amb_case"] = random.choice(info["data"]["ambiguous"])
    elif slug == "fair-future":
        if n in (1, 2):
            extra["system"] = random.choice(info["data"]["systems"])
        elif n == 3:
            extra["escalation"] = random.choice(info["data"]["escalations"])
    elif slug == "build-for-good":
        if n == 1:
            extra["templates"] = info["data"]["templates"]
        elif n == 2:
            chosen_id = session.get(f"world_{slug}_template", info["data"]["templates"][0]["id"])
            tpl = next((t for t in info["data"]["templates"] if t["id"] == chosen_id), info["data"]["templates"][0])
            extra["template"] = tpl
            extra["all_blocks"] = info["data"]["blocks"]
        elif n == 3:
            extra["safety_checks"] = info["data"]["safety"]

    template_map = {
        "data-defender": "worlds/data_defender.html",
        "city-fixer": "worlds/city_fixer.html",
        "truth-quest": "worlds/truth_quest.html",
        "fair-future": "worlds/fair_future.html",
        "build-for-good": "worlds/build_good.html",
    }

    return render_template(
        template_map[slug],
        world=world,
        mission=mission,
        mission_num=n,
        progress=progress,
        slug=slug,
        **extra,
    )


@app.route("/world/<slug>/template-select", methods=["POST"])
def world_template_select(slug):
    template_id = request.form.get("template_id")
    if template_id:
        session[f"world_{slug}_template"] = template_id
        session.modified = True
    return redirect(url_for("world_mission", slug=slug, n=2))


@app.route("/world/<slug>/reward")
def world_reward(slug):
    if slug not in ALL_WORLDS:
        return redirect(url_for("home"))
    progress = get_world_progress(slug)
    world = ALL_WORLDS[slug]["world"]
    xp = session.get("xp", 0)
    return render_template(
        "worlds/reward.html",
        world=world,
        progress=progress,
        slug=slug,
        xp=xp,
    )


if __name__ == "__main__":
    app.run(debug=True, port=5004, use_reloader=False)
