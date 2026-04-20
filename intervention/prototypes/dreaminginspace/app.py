"""Dreaming in Space -- Lesson 1 Flask app (student-facing).

Routes:
    /                       -- Home dashboard (resume, progress, path)
    /lesson/1/intro         -- Lesson intro (overview, vocab, role model)
    /simulator              -- PB&J sandwich simulator
    /exercise/<1|2|3>       -- Stepped exercises
    /review                 -- Recap/completion (includes Extensions)
    /challenge              -- Redirects to /review#extensions (folded)
    /api/simulator/command  -- JSON endpoint for JS-enhanced simulator
    /reset                  -- Clear session
"""

from flask import (
    Flask, render_template, request, session, redirect, url_for, jsonify,
)
import os
import random
import copy
from difflib import get_close_matches
from data.lesson_content import (
    LESSON, ROLE_MODEL, VOCABULARY, LEARNING_OBJECTIVES,
    EXERCISES, TEA_STEPS_CORRECT, CHALLENGES,
    INITIAL_SANDWICH_STATE, COMMAND_ALIASES, QUIZ_1,
)
from data.lesson2_robot_content import (
    LESSON_2_ROBOT, ROLE_MODEL_2_ROBOT, VOCABULARY_2_ROBOT,
    LEARNING_OBJECTIVES_2_ROBOT, EXERCISES_2_ROBOT, QUIZ_2_ROBOT,
)
from data.lesson2_content import (
    LESSON_2, ROLE_MODEL_2, VOCABULARY_2, LEARNING_OBJECTIVES_2,
    EXERCISES_2, QUIZ_2,
)
from data.lesson3_content import (
    LESSON_3, ROLE_MODEL_3, VOCABULARY_3, LEARNING_OBJECTIVES_3,
    EXERCISES_3, QUIZ_3,
)
from data.lesson4_content import (
    LESSON_4, ROLE_MODEL_4, VOCABULARY_4, LEARNING_OBJECTIVES_4,
    EXERCISES_4, QUIZ_4,
)
from data.lesson6_content import LESSON_6, ROLE_MODEL_6, VOCABULARY_6, OBJECTIVES_6, EXERCISES_6, QUIZ_6
from data.lesson7_content import LESSON_7, ROLE_MODEL_7, VOCABULARY_7, OBJECTIVES_7, EXERCISES_7, QUIZ_7
from data.lesson8_content import LESSON_8, ROLE_MODEL_8, VOCABULARY_8, OBJECTIVES_8, EXERCISES_8, QUIZ_8
from data.lesson9_content import LESSON_9, ROLE_MODEL_9, VOCABULARY_9, OBJECTIVES_9, EXERCISES_9, QUIZ_9
from data.lesson10_content import LESSON_10, ROLE_MODEL_10, VOCABULARY_10, OBJECTIVES_10, EXERCISES_10, QUIZ_10
from data.lesson11_content import LESSON_11, ROLE_MODEL_11, VOCABULARY_11, OBJECTIVES_11, EXERCISES_11, QUIZ_11
from data.lesson12_content import LESSON_12, ROLE_MODEL_12, VOCABULARY_12, OBJECTIVES_12, EXERCISES_12, QUIZ_12
from data.lesson13_content import LESSON_13, ROLE_MODEL_13, VOCABULARY_13, OBJECTIVES_13, EXERCISES_13, QUIZ_13
from data.lesson14_content import LESSON_14, ROLE_MODEL_14, VOCABULARY_14, OBJECTIVES_14, EXERCISES_14, QUIZ_14
from data.lesson15_content import LESSON_15, ROLE_MODEL_15, VOCABULARY_15, OBJECTIVES_15, EXERCISES_15, QUIZ_15
from data.lesson16_content import LESSON_16, ROLE_MODEL_16, VOCABULARY_16, OBJECTIVES_16, EXERCISES_16, QUIZ_16
from data.lesson17_content import LESSON_17, ROLE_MODEL_17, VOCABULARY_17, OBJECTIVES_17, EXERCISES_17, QUIZ_17
from data.lesson18_content import LESSON_18, ROLE_MODEL_18, VOCABULARY_18, OBJECTIVES_18, EXERCISES_18, QUIZ_18

# ---------------------------------------------------------------------------
# All-lessons registry (16 lessons across 4 tracks)
# ---------------------------------------------------------------------------
def _lesson(l, rm, v, o, ex, q=None):
    d = {"lesson": l, "role_model": rm, "vocabulary": v, "objectives": o, "exercises": ex}
    if q: d["quiz"] = q
    return d

ALL_LESSONS = {
    # Track 1: Foundations
    1:  _lesson(LESSON, ROLE_MODEL, VOCABULARY, LEARNING_OBJECTIVES, EXERCISES, QUIZ_1),
    2:  _lesson(LESSON_2_ROBOT, ROLE_MODEL_2_ROBOT, VOCABULARY_2_ROBOT, LEARNING_OBJECTIVES_2_ROBOT, EXERCISES_2_ROBOT, QUIZ_2_ROBOT),
    3:  _lesson(LESSON_2, ROLE_MODEL_2, VOCABULARY_2, LEARNING_OBJECTIVES_2, EXERCISES_2, QUIZ_2),
    4:  _lesson(LESSON_3, ROLE_MODEL_3, VOCABULARY_3, LEARNING_OBJECTIVES_3, EXERCISES_3, QUIZ_3),
    5:  _lesson(LESSON_4, ROLE_MODEL_4, VOCABULARY_4, LEARNING_OBJECTIVES_4, EXERCISES_4, QUIZ_4),
    # Track 2: Text-Based Coding
    6:  _lesson(LESSON_6, ROLE_MODEL_6, VOCABULARY_6, OBJECTIVES_6, EXERCISES_6, QUIZ_6),
    7:  _lesson(LESSON_7, ROLE_MODEL_7, VOCABULARY_7, OBJECTIVES_7, EXERCISES_7, QUIZ_7),
    8:  _lesson(LESSON_8, ROLE_MODEL_8, VOCABULARY_8, OBJECTIVES_8, EXERCISES_8, QUIZ_8),
    9:  _lesson(LESSON_9, ROLE_MODEL_9, VOCABULARY_9, OBJECTIVES_9, EXERCISES_9, QUIZ_9),
    # Track 3: Creation & Application
    10: _lesson(LESSON_10, ROLE_MODEL_10, VOCABULARY_10, OBJECTIVES_10, EXERCISES_10, QUIZ_10),
    11: _lesson(LESSON_11, ROLE_MODEL_11, VOCABULARY_11, OBJECTIVES_11, EXERCISES_11, QUIZ_11),
    12: _lesson(LESSON_12, ROLE_MODEL_12, VOCABULARY_12, OBJECTIVES_12, EXERCISES_12, QUIZ_12),
    13: _lesson(LESSON_13, ROLE_MODEL_13, VOCABULARY_13, OBJECTIVES_13, EXERCISES_13, QUIZ_13),
    # Track 4: Digital World
    14: _lesson(LESSON_14, ROLE_MODEL_14, VOCABULARY_14, OBJECTIVES_14, EXERCISES_14, QUIZ_14),
    15: _lesson(LESSON_15, ROLE_MODEL_15, VOCABULARY_15, OBJECTIVES_15, EXERCISES_15, QUIZ_15),
    16: _lesson(LESSON_16, ROLE_MODEL_16, VOCABULARY_16, OBJECTIVES_16, EXERCISES_16, QUIZ_16),
    17: _lesson(LESSON_17, ROLE_MODEL_17, VOCABULARY_17, OBJECTIVES_17, EXERCISES_17, QUIZ_17),
    18: _lesson(LESSON_18, ROLE_MODEL_18, VOCABULARY_18, OBJECTIVES_18, EXERCISES_18, QUIZ_18),
}
TOTAL_LESSONS = len(ALL_LESSONS)

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
        session["initialized"] = True

    completed = session.get("completed_exercises", [])
    all_done = len(completed) >= 3
    sim_done = session.get("simulator_completed", False)

    # Figure out the next resumable step for the Continue card.
    if not sim_done and not completed:
        resume = {"label": "Start lesson intro", "href": "/lesson/1/intro", "step": "intro"}
    elif not sim_done:
        resume = {"label": "Try the Simulator", "href": "/simulator", "step": "intro"}
    elif 1 not in completed:
        resume = {"label": "Exercise 1", "href": "/exercise/1", "step": "ex1"}
    elif 2 not in completed:
        resume = {"label": "Exercise 2", "href": "/exercise/2", "step": "ex2"}
    elif 3 not in completed:
        resume = {"label": "Exercise 3", "href": "/exercise/3", "step": "ex3"}
    else:
        resume = {"label": "Review & Recap", "href": "/review", "step": "recap"}

    return {
        "completed_exercises": completed,
        "progress_percent": round(len(completed) / 3 * 100),
        "simulator_completed": sim_done,
        "simulator_confusion_count": session.get("simulator_confusion_count", 0),
        "all_exercises_done": all_done,
        "resume": resume,
    }


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
    return render_template(
        "home.html",
        lesson=LESSON,
        progress=progress,
        all_lessons=ALL_LESSONS,
    )


@app.route("/lesson/1/intro")
def lesson_intro():
    progress = get_progress()
    return render_template(
        "lesson_intro.html",
        lesson=LESSON,
        role_model=ROLE_MODEL,
        vocabulary=VOCABULARY,
        objectives=LEARNING_OBJECTIVES,
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
            state = copy.deepcopy(INITIAL_SANDWICH_STATE)
            log = []
            confusion = 0
            for cmd_text in commands:
                result = process_user_command(cmd_text, state)
                log.append({"command": cmd_text, **result})
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
        "simulator.html",
        state=state,
        log=log,
        commands=commands,
        progress=progress,
    )


@app.route("/api/simulator/command", methods=["POST"])
def api_simulator_command():
    """JSON endpoint for JS-enhanced simulator interaction."""
    progress = get_progress()
    state = session.get("simulator_state", copy.deepcopy(INITIAL_SANDWICH_STATE))
    commands = session.get("simulator_commands", [])
    user_input = (request.json or {}).get("command", "").strip()
    if not user_input:
        return jsonify({"error": "No command provided"}), 400

    commands.append(user_input)

    state = copy.deepcopy(INITIAL_SANDWICH_STATE)
    log = []
    confusion = 0
    for cmd_text in commands:
        result = process_user_command(cmd_text, state)
        log.append({"command": cmd_text, **result})
        if result["type"] == "literal_interpretation":
            confusion += 1

    session["simulator_state"] = state
    session["simulator_log"] = log
    session["simulator_commands"] = commands
    session["simulator_confusion_count"] = confusion
    if state["sandwich_complete"]:
        session["simulator_completed"] = True
    session.modified = True

    return jsonify({
        "state": state,
        "log": log,
        "commands": commands,
        "confusion_count": confusion,
        "completed": state["sandwich_complete"],
    })


@app.route("/exercise/<int:num>", methods=["GET", "POST"])
def exercise(num):
    if num not in (1, 2, 3):
        return "Exercise not found", 404

    progress = get_progress()
    ex = EXERCISES[num - 1]
    error = None
    success = False

    if request.method == "POST":
        if num == 1:
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

        elif num == 2:
            order = request.form.getlist("order")
            if len(order) != 6:
                error = "Please put all 6 steps in order."
            else:
                submitted = [TEA_STEPS_CORRECT[int(i)] for i in order]
                session["exercise_answers"][str(num)] = submitted
                if submitted == TEA_STEPS_CORRECT:
                    if num not in session["completed_exercises"]:
                        session["completed_exercises"].append(num)
                    session.modified = True
                    success = True
                    progress = get_progress()
                else:
                    error = "Not quite right! Check the order and try again."

        elif num == 3:
            lunch_item = request.form.get("lunch_item", "").strip()
            steps = [
                request.form.get(f"step_{i}", "").strip()
                for i in range(1, 21)
            ]
            steps = [s for s in steps if s]
            allergy = request.form.get("allergy", "").strip()
            missing = request.form.get("missing_ingredient", "").strip()

            errors = []
            if not lunch_item:
                errors.append("Choose a lunch item.")
            if len(steps) < 6:
                errors.append("You need at least 6 steps.")
            if not allergy:
                errors.append("Add allergy safety instructions.")
            if not missing:
                errors.append("Add a rule for missing ingredients.")
            if errors:
                error = " ".join(errors)
            else:
                session["exercise_answers"][str(num)] = {
                    "lunch_item": lunch_item,
                    "steps": steps,
                    "allergy": allergy,
                    "missing_ingredient": missing,
                }
                if num not in session["completed_exercises"]:
                    session["completed_exercises"].append(num)
                session.modified = True
                success = True
                progress = get_progress()

    context = {
        "exercise": ex,
        "num": num,
        "progress": progress,
        "error": error,
        "success": success,
    }

    if num == 2:
        if "tea_shuffle" not in session:
            indices = list(range(6))
            random.shuffle(indices)
            session["tea_shuffle"] = indices
            session.modified = True
        context["tea_steps"] = TEA_STEPS_CORRECT
        context["shuffled_indices"] = session["tea_shuffle"]

    template = f"exercise{num}.html"
    return render_template(template, **context)


@app.route("/challenge")
def challenge():
    # Challenges are now folded into the recap page as "Extensions".
    return redirect(url_for("review") + "#extensions")


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
        "review.html",
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
        "lesson_home.html",
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
    error = None
    success = False

    if request.method == "POST":
        ex_type = ex.get("type", "written")

        if ex_type == "robot_maze":
            cmds = request.form.get("commands", "")
            if cmds:
                if ex_num not in lesson_data["completed_exercises"]:
                    lesson_data["completed_exercises"].append(ex_num)
                session["xp"] = session.get("xp", 0) + ex.get("xp", 10)
                session.modified = True
                success = True
                progress = get_lesson_progress(lesson_num)
            else:
                error = "Run your program and reach the goal first!"

        elif ex_type == "robot_commands":
            steps = [request.form.get(f"step_{i}", "").strip() for i in range(1, 21)]
            steps = [s for s in steps if s]
            min_steps = ex.get("min_steps", 5)
            if len(steps) < min_steps:
                error = f"Your robot needs at least {min_steps} commands. Keep going!"
            else:
                if ex_num not in lesson_data["completed_exercises"]:
                    lesson_data["completed_exercises"].append(ex_num)
                session["xp"] = session.get("xp", 0) + ex.get("xp", 10)
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
                    if ex_num not in lesson_data["completed_exercises"]:
                        lesson_data["completed_exercises"].append(ex_num)
                    session["xp"] = session.get("xp", 0) + ex.get("xp", 15)
                    session.modified = True
                    success = True
                    progress = get_lesson_progress(lesson_num)
                    _debug_result = result
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
                    session["xp"] = session.get("xp", 0) + ex.get("xp", 15)
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
                session["xp"] = session.get("xp", 0) + ex.get("xp", 20)
                session.modified = True
                success = True
                progress = get_lesson_progress(lesson_num)

        elif ex_type == "spot_loop":
            problems = ex.get("problems", [])
            all_filled = True
            for i in range(len(problems)):
                if not request.form.get(f"repeat_{i}", "").strip() or not request.form.get(f"count_{i}", "").strip():
                    all_filled = False
            if not all_filled:
                error = "Please answer both questions for each routine!"
            else:
                if ex_num not in lesson_data["completed_exercises"]:
                    lesson_data["completed_exercises"].append(ex_num)
                session["xp"] = session.get("xp", 0) + ex.get("xp", 10)
                session.modified = True
                success = True
                progress = get_lesson_progress(lesson_num)

        elif ex_type == "rewrite_loop":
            problems = ex.get("problems", [])
            all_filled = True
            for i in range(len(problems)):
                if not request.form.get(f"times_{i}", "").strip() or not request.form.get(f"body_{i}", "").strip():
                    all_filled = False
            if not all_filled:
                error = "Fill in the loop count AND the steps for each problem!"
            else:
                if ex_num not in lesson_data["completed_exercises"]:
                    lesson_data["completed_exercises"].append(ex_num)
                session["xp"] = session.get("xp", 0) + ex.get("xp", 15)
                session.modified = True
                success = True
                progress = get_lesson_progress(lesson_num)

        elif ex_type == "bug_hunt":
            bugs = ex.get("bugs", [])
            all_filled = True
            for i in range(len(bugs)):
                if not request.form.get(f"fix_{i}", "").strip():
                    all_filled = False
            if not all_filled:
                error = "Please write a fix for every bug!"
            else:
                if ex_num not in lesson_data["completed_exercises"]:
                    lesson_data["completed_exercises"].append(ex_num)
                session["xp"] = session.get("xp", 0) + ex.get("xp", 20)
                session.modified = True
                success = True
                progress = get_lesson_progress(lesson_num)

        elif ex_type == "read_conditional":
            problems = ex.get("problems", [])
            correct_count = 0
            for i, p in enumerate(problems):
                ans = request.form.get(f"q{i}")
                if ans is not None and int(ans) == p["correct"]:
                    correct_count += 1
            if correct_count < len(problems):
                error = f"You got {correct_count}/{len(problems)} correct. Try again!"
            else:
                if ex_num not in lesson_data["completed_exercises"]:
                    lesson_data["completed_exercises"].append(ex_num)
                session["xp"] = session.get("xp", 0) + ex.get("xp", 10)
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
                session["xp"] = session.get("xp", 0) + ex.get("xp", 15)
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
                session["xp"] = session.get("xp", 0) + ex.get("xp", 10)
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
                session["xp"] = session.get("xp", 0) + ex.get("xp", 15)
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
                session["xp"] = session.get("xp", 0) + ex.get("xp", 20)
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
    # Add debug result if MCQ bug hunt was submitted
    if "_debug_result" in dir() or "_debug_result" in locals():
        context["result"] = _debug_result

    # Template mapping
    TEMPLATE_MAP = {
        "robot_maze": "l2r_maze.html",
        "robot_commands": "l2r_commands.html",
        "robot_debug": "l_bug_hunt.html",
        "precision_rewrite": "l2r_precision.html",
        "spot_loop": "l2_spot_loop.html",
        "rewrite_loop": "l2_rewrite_loop.html",
        "bug_hunt": "l_bug_hunt.html",
        "read_conditional": "l3_read_conditional.html",
        "write_conditional": "l3_write_conditional.html",
        "grouping": "l4_grouping.html",
        "decompose": "l4_decompose.html",
        "ordering_dependencies": "l4_ordering.html",
    }
    ex_type = ex.get("type", "written")
    template = TEMPLATE_MAP.get(ex_type, "l_generic.html")
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
            session["xp"] = session.get("xp", 0) + 10
            session.modified = True
    return render_template("l_quiz.html", questions=quiz, lesson_num=lesson_num, lesson=lesson, result=result, progress=get_lesson_progress(lesson_num))


@app.route("/lesson/<int:lesson_num>/recap", methods=["GET", "POST"])
def lesson_recap(lesson_num):
    """Recap/rewards page for lessons 2+."""
    if lesson_num not in ALL_LESSONS or lesson_num == 1:
        return redirect(url_for("home"))
    info = ALL_LESSONS[lesson_num]
    progress = get_lesson_progress(lesson_num)
    recap_key = f"recap_{lesson_num}"
    recap_submitted = False
    recap_answer = session.get(recap_key, "")

    if request.method == "POST":
        reflection = request.form.get("reflection", "").strip()
        if reflection:
            session[recap_key] = reflection
            recap_answer = reflection
            recap_submitted = True
            session.modified = True

    if recap_answer:
        recap_submitted = True

    return render_template(
        "l_recap.html",
        lesson=info["lesson"],
        vocabulary=info["vocabulary"],
        objectives=info["objectives"],
        progress=progress,
        lesson_num=lesson_num,
        recap_submitted=recap_submitted,
        recap_answer=recap_answer,
    )


if __name__ == "__main__":
    app.run(debug=True, port=5004, use_reloader=False)
