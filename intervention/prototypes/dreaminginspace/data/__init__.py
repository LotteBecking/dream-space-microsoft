"""Data package , dynamic lesson & world loader.

Every lesson file (lessons/lesson1.py … lessons/lesson18.py) exports:
    LESSON, ROLE_MODEL, VOCABULARY, OBJECTIVES, EXERCISES, QUIZ

This loader imports them all into ALL_LESSONS[1..18] so app.py only needs:
    from data import ALL_LESSONS, ALL_WORLDS
"""
import importlib

# ── Lessons ────────────────────────────────────────────────────────────────
ALL_LESSONS = {}
for n in list(range(1, 6)) + list(range(6, 19)):
    mod = importlib.import_module(f"data.lessons.lesson{n}")
    ALL_LESSONS[n] = {
        "lesson":     mod.LESSON,
        "role_model":  mod.ROLE_MODEL,
        "vocabulary":  mod.VOCABULARY,
        "objectives":  mod.OBJECTIVES,
        "exercises":   mod.EXERCISES,
        "quiz":        getattr(mod, "QUIZ", []),
    }

# ── Worlds (Track 5) ──────────────────────────────────────────────────────
from data.worlds.world_data_defender import WORLD as _WDD, PERMISSION_SCENARIOS, TRICK_CASES, REPAIR_TASKS, TOOLS as DD_TOOLS
from data.worlds.world_city_fixer    import WORLD as _WCF, ROUTES as CF_ROUTES, TRADEOFF_SCENARIOS, DISRUPTIONS
from data.worlds.world_truth_quest   import WORLD as _WTQ, CASES as TQ_CASES, AMBIGUOUS_CASES
from data.worlds.world_fair_future   import WORLD as _WFF, SYSTEMS as FF_SYSTEMS, ESCALATION_SCENARIOS
from data.worlds.world_build_good    import WORLD as _WBG, TEMPLATES as BG_TEMPLATES, ALL_BLOCKS, SAFETY_CHECKS

ALL_WORLDS = {
    "data-defender":  {"world": _WDD, "data": {"scenarios": PERMISSION_SCENARIOS, "trick_cases": TRICK_CASES, "repair_tasks": REPAIR_TASKS, "tools": DD_TOOLS}},
    "city-fixer":     {"world": _WCF, "data": {"routes": CF_ROUTES, "tradeoffs": TRADEOFF_SCENARIOS, "disruptions": DISRUPTIONS}},
    "truth-quest":    {"world": _WTQ, "data": {"cases": TQ_CASES, "ambiguous": AMBIGUOUS_CASES}},
    "fair-future":    {"world": _WFF, "data": {"systems": FF_SYSTEMS, "escalations": ESCALATION_SCENARIOS}},
    "build-for-good": {"world": _WBG, "data": {"templates": BG_TEMPLATES, "blocks": ALL_BLOCKS, "safety": SAFETY_CHECKS}},
}