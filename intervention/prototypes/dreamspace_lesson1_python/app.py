"""DreamSpace Lessons 1-3 -- Flask web app for students (ages 8-12)."""
from __future__ import annotations

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
    INITIAL_SANDWICH_STATE, COMMAND_ALIASES,
    RESEARCH_REFERENCES, PEDAGOGICAL_FRAMEWORK,
    MAZE_LEVELS, QUIZ_QUESTIONS,
)
from data.lesson2_content import (
    LESSON_2, ROLE_MODEL_2, VOCABULARY_2, LEARNING_OBJECTIVES_2, EXERCISES_2,
)
from data.lesson3_content import (
    LESSON_3, ROLE_MODEL_3, VOCABULARY_3, LEARNING_OBJECTIVES_3, EXERCISES_3,
)

# ---------------------------------------------------------------------------
# All-lessons registry
# ---------------------------------------------------------------------------
ALL_LESSONS = {
    1: {
        "lesson": LESSON,
        "role_model": ROLE_MODEL,
        "vocabulary": VOCABULARY,
        "objectives": LEARNING_OBJECTIVES,
        "exercises": MAZE_LEVELS,
    },
    2: {
        "lesson": LESSON_2,
        "role_model": ROLE_MODEL_2,
        "vocabulary": VOCABULARY_2,
        "objectives": LEARNING_OBJECTIVES_2,
        "exercises": EXERCISES_2,
    },
    3: {
        "lesson": LESSON_3,
        "role_model": ROLE_MODEL_3,
        "vocabulary": VOCABULARY_3,
        "objectives": LEARNING_OBJECTIVES_3,
        "exercises": EXERCISES_3,
    },
}

app = Flask(__name__)
app.secret_key = os.environ.get(
    "SECRET_KEY", "dreamspace-lesson1-dev-key-change-in-production"
)

# ---------------------------------------------------------------------------
# Session helpers
# ---------------------------------------------------------------------------

def get_progress(lesson_num=1):
    """Return (and lazily initialise) student progress for a lesson."""
    key = f"lesson_{lesson_num}"
    if key not in session:
        session[key] = {
            "completed_exercises": [],
            "exercise_answers": {},
        }
        session.modified = True

    # Lesson 1 also has simulator state
    if lesson_num == 1 and "initialized" not in session:
        session["exit_ticket_1"] = ""
        session["exit_ticket_2"] = ""
        session["simulator_completed"] = False
        session["simulator_confusion_count"] = 0
        session["simulator_state"] = copy.deepcopy(INITIAL_SANDWICH_STATE)
        session["simulator_log"] = []
        session["simulator_commands"] = []
        session["initialized"] = True

    data = session.get(key, {"completed_exercises": [], "exercise_answers": {}})
    completed = data.get("completed_exercises", [])
    return {
        "completed_exercises": completed,
        "progress_percent": round(len(completed) / 3 * 100),
        "simulator_completed": session.get("simulator_completed", False),
        "simulator_confusion_count": session.get("simulator_confusion_count", 0),
        "all_exercises_done": len(completed) >= 3,
    }


def get_overall_progress():
    """Return progress across all lessons."""
    total = 0
    for ln in (1, 2, 3):
        key = f"lesson_{ln}"
        data = session.get(key, {"completed_exercises": []})
        total += len(data.get("completed_exercises", []))
    return {
        "total_completed": total,
        "total_exercises": 9,
        "progress_percent": round(total / 9 * 100),
    }


# ---------------------------------------------------------------------------
# Simulator engine
# ---------------------------------------------------------------------------

ALL_ALIASES = []
for aliases in COMMAND_ALIASES.values():
    ALL_ALIASES.extend(aliases)


def parse_command(user_input: str) -> str | None:
    """Fuzzy-match *user_input* to a canonical command key, or return None."""
    text = user_input.strip().lower()
    if not text:
        return None

    # Exact substring match first
    for key, aliases in COMMAND_ALIASES.items():
        for alias in aliases:
            if alias == text:
                return key

    # Fuzzy match
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
    """Execute *command_key* against sandwich *state*.

    Returns ``{"type": "success"|"precondition_error"|"literal_interpretation",
               "message": str}``.
    """
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
    """Lesson picker / landing page."""
    overall = get_overall_progress()
    lessons = []
    for ln in (1, 2, 3):
        info = ALL_LESSONS[ln]
        prog = get_progress(ln)
        lessons.append({
            "num": ln,
            "lesson": info["lesson"],
            "role_model": info["role_model"],
            "progress": prog,
        })
    return render_template("home.html", lessons=lessons, overall=overall)


@app.route("/lesson/<int:lesson_num>")
def lesson_home(lesson_num):
    """Home page for a specific lesson."""
    if lesson_num not in ALL_LESSONS:
        return "Lesson not found", 404
    info = ALL_LESSONS[lesson_num]
    progress = get_progress(lesson_num)
    return render_template(
        "lesson_home.html",
        lesson=info["lesson"],
        role_model=info["role_model"],
        vocabulary=info["vocabulary"],
        objectives=info["objectives"],
        progress=progress,
        lesson_num=lesson_num,
    )


@app.route("/simulator", methods=["GET", "POST"])
def simulator():
    progress = get_progress(1)
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
            # Reset state and replay all commands
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
            progress = get_progress(1)

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
    progress = get_progress(1)
    state = session.get("simulator_state", copy.deepcopy(INITIAL_SANDWICH_STATE))
    commands = session.get("simulator_commands", [])
    user_input = (request.json or {}).get("command", "").strip()
    if not user_input:
        return jsonify({"error": "No command provided"}), 400

    commands.append(user_input)

    # Replay all commands from scratch
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
    """Legacy route — redirects to lesson 1 exercises."""
    return redirect(url_for("lesson_exercise", lesson_num=1, ex_num=num))


@app.route("/lesson/<int:lesson_num>/exercise/<int:ex_num>", methods=["GET", "POST"])
def lesson_exercise(lesson_num, ex_num):
    if lesson_num not in ALL_LESSONS:
        return "Lesson not found", 404
    info = ALL_LESSONS[lesson_num]
    exercises = info["exercises"]
    if ex_num < 1 or ex_num > len(exercises):
        return "Exercise not found", 404

    progress = get_progress(lesson_num)
    ex = exercises[ex_num - 1]
    lesson_data = session.setdefault(f"lesson_{lesson_num}",
                                     {"completed_exercises": [], "exercise_answers": {}})
    error = None
    success = False

    if request.method == "POST":
        ex_type = ex.get("type", "written_steps")

        if ex_type in ("written_steps", "written_conditional"):
            steps = [
                request.form.get(f"step_{i}", "").strip()
                for i in range(1, 21)
            ]
            steps = [s for s in steps if s]
            min_steps = ex.get("min_steps", 2)
            if len(steps) < min_steps:
                error = f"You need at least {min_steps} steps. Keep going!"
            else:
                lesson_data["exercise_answers"][str(ex_num)] = steps
                if ex_num not in lesson_data["completed_exercises"]:
                    lesson_data["completed_exercises"].append(ex_num)
                session.modified = True
                success = True
                progress = get_progress(lesson_num)

        elif ex_type == "bug_hunt":
            fixes = []
            bugs = ex.get("bugs", [])
            all_filled = True
            for i in range(len(bugs)):
                fix = request.form.get(f"fix_{i}", "").strip()
                fixes.append(fix)
                if not fix:
                    all_filled = False
            if not all_filled:
                error = "Please write a fix for every bug!"
            else:
                lesson_data["exercise_answers"][str(ex_num)] = fixes
                if ex_num not in lesson_data["completed_exercises"]:
                    lesson_data["completed_exercises"].append(ex_num)
                session.modified = True
                success = True
                progress = get_progress(lesson_num)

        elif ex_type == "written_extended":
            fields = ex.get("fields", [])
            answers = {}
            errors = []
            for field in fields:
                name = field["name"]
                if field["type"] == "steps":
                    val = [
                        request.form.get(f"{name}_{i}", "").strip()
                        for i in range(1, 21)
                    ]
                    val = [v for v in val if v]
                    if len(val) < 2:
                        errors.append(f"Write at least 2 steps for \u2018{field['label']}\u2019.")
                    answers[name] = val
                else:
                    val = request.form.get(name, "").strip()
                    if not val:
                        errors.append(f"Please fill in \u2018{field['label']}\u2019.")
                    answers[name] = val
            if errors:
                error = " ".join(errors)
            else:
                lesson_data["exercise_answers"][str(ex_num)] = answers
                if ex_num not in lesson_data["completed_exercises"]:
                    lesson_data["completed_exercises"].append(ex_num)
                session.modified = True
                success = True
                progress = get_progress(lesson_num)

        # Lesson 1 sorting exercise (special case)
        elif ex_type == "Sorting":
            order = request.form.getlist("order")
            if len(order) != 6:
                error = "Please put all 6 steps in order."
            else:
                submitted = [TEA_STEPS_CORRECT[int(i)] for i in order]
                lesson_data["exercise_answers"][str(ex_num)] = submitted
                if submitted == TEA_STEPS_CORRECT:
                    if ex_num not in lesson_data["completed_exercises"]:
                        lesson_data["completed_exercises"].append(ex_num)
                    session.modified = True
                    success = True
                    progress = get_progress(lesson_num)
                else:
                    error = "Not quite right! Check the order and try again."

        # Lesson 1 original written types
        elif ex_type == "Written":
            steps = [
                request.form.get(f"step_{i}", "").strip()
                for i in range(1, 21)
            ]
            steps = [s for s in steps if s]
            if len(steps) < 6:
                error = "You need at least 6 steps. Keep going!"
            else:
                lesson_data["exercise_answers"][str(ex_num)] = steps
                if ex_num not in lesson_data["completed_exercises"]:
                    lesson_data["completed_exercises"].append(ex_num)
                session.modified = True
                success = True
                progress = get_progress(lesson_num)

        elif ex_type == "Extension":
            lunch_item = request.form.get("lunch_item", "").strip()
            steps = [
                request.form.get(f"step_{i}", "").strip()
                for i in range(1, 21)
            ]
            steps = [s for s in steps if s]
            allergy = request.form.get("allergy", "").strip()
            missing = request.form.get("missing_ingredient", "").strip()
            errs = []
            if not lunch_item:
                errs.append("Choose a lunch item.")
            if len(steps) < 6:
                errs.append("You need at least 6 steps.")
            if not allergy:
                errs.append("Add allergy safety instructions.")
            if not missing:
                errs.append("Add a rule for missing ingredients.")
            if errs:
                error = " ".join(errs)
            else:
                lesson_data["exercise_answers"][str(ex_num)] = {
                    "lunch_item": lunch_item, "steps": steps,
                    "allergy": allergy, "missing_ingredient": missing,
                }
                if ex_num not in lesson_data["completed_exercises"]:
                    lesson_data["completed_exercises"].append(ex_num)
                session.modified = True
                success = True
                progress = get_progress(lesson_num)

    session[f"lesson_{lesson_num}"] = lesson_data
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

    # Lesson 1 exercise 2 sorting needs shuffled indices
    if lesson_num == 1 and ex_num == 2:
        if "tea_shuffle" not in session:
            indices = list(range(6))
            random.shuffle(indices)
            session["tea_shuffle"] = indices
            session.modified = True
        context["tea_steps"] = TEA_STEPS_CORRECT
        context["shuffled_indices"] = session["tea_shuffle"]

    # Choose template based on exercise type
    ex_type = ex.get("type", "written_steps")
    if ex_type == "maze":
        return render_template("maze.html", level=ex, lesson_num=lesson_num, progress=progress)
    elif lesson_num == 1:
        template = f"exercise{ex_num}.html"
    elif ex_type == "bug_hunt":
        template = "exercise_bug_hunt.html"
    elif ex_type == "written_extended":
        template = "exercise_extended.html"
    elif ex_type == "written_conditional":
        template = "exercise_conditional.html"
    else:
        template = "exercise_written.html"

    return render_template(template, **context)


@app.route("/lesson/<int:lesson_num>/challenge")
def lesson_challenge(lesson_num):
    if lesson_num != 1:
        return redirect(url_for("lesson_home", lesson_num=lesson_num))
    progress = get_progress(1)
    return render_template(
        "challenge.html",
        challenges=CHALLENGES,
        progress=progress,
        lesson_num=1,
    )


@app.route("/challenge")
def challenge():
    return redirect(url_for("lesson_challenge", lesson_num=1))


@app.route("/api/maze/complete", methods=["POST"])
def api_maze_complete():
    """Mark a maze level as complete (called from JS)."""
    data = request.json or {}
    lesson_num = data.get("lesson", 1)
    level = data.get("level", 1)
    steps = data.get("steps", 0)

    key = f"lesson_{lesson_num}"
    lesson_data = session.setdefault(key, {"completed_exercises": [], "exercise_answers": {}})
    if level not in lesson_data["completed_exercises"]:
        lesson_data["completed_exercises"].append(level)
    lesson_data["exercise_answers"][str(level)] = {"steps": steps}
    session.modified = True

    return jsonify({"success": True})


@app.route("/lesson/<int:lesson_num>/quiz", methods=["GET", "POST"])
def lesson_quiz(lesson_num):
    """Quiz page after completing maze levels."""
    if lesson_num != 1:
        return redirect(url_for("lesson_home", lesson_num=lesson_num))

    result = None
    if request.method == "POST":
        answers = []
        wrong = []
        for i, q in enumerate(QUIZ_QUESTIONS):
            ans = request.form.get(f"q{i}")
            ans = int(ans) if ans is not None else -1
            answers.append(ans)
            if ans != q["correct"]:
                wrong.append(i)
        score = len(QUIZ_QUESTIONS) - len(wrong)
        result = {
            "score": score,
            "total": len(QUIZ_QUESTIONS),
            "percent": round(score / len(QUIZ_QUESTIONS) * 100),
            "answers": answers,
            "wrong": wrong,
        }

    return render_template(
        "lesson1_quiz.html",
        questions=QUIZ_QUESTIONS,
        lesson_num=lesson_num,
        result=result,
    )


@app.route("/review", methods=["GET", "POST"])
def review():
    progress = get_progress(1)
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
        progress=progress,
        exit_ticket_1=session.get("exit_ticket_1", ""),
        exit_ticket_2=session.get("exit_ticket_2", ""),
        success=success,
    )


@app.route("/reset", methods=["POST"])
def reset():
    session.clear()
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True, port=5004, use_reloader=False)
