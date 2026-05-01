"""Lesson 9: Bug Hunt in Orbit.
Track 2: Text-Based Coding | Dreaming in Space.
"""

LESSON = {
    "id": "lesson-9",
    "title": "Bug Hunt in Orbit",
    "description": (
        "Develop a systematic approach to finding and fixing errors in code. "
        "Learn the 3 types of bugs and how to squash them."
    ),
    "duration": 45,
    "level": "Beginner",
    "age_group": "Ages 8-18",
    "color": "#dc2626",
    "welcome": (
        "Gasp! The landing computer has a \u2018Bug\u2019 \u2014 that\u2019s "
        "just a fancy word for a mistake in code. Here\u2019s a secret: "
        "professional programmers spend MORE time debugging than writing "
        "new code! The best coders aren\u2019t the ones who never make "
        "mistakes \u2014 they\u2019re the ones who find and fix them FAST. "
        "Let\u2019s be detectives!"
    ),
    "recap_msg": (
        "Every great coder is a great bug hunter. You just cleared the "
        "ship\u2019s systems! Read the error, trace the code, check your "
        "variables, fix one thing at a time. You\u2019re a debugging detective!"
    ),
}

ROLE_MODEL = {
    "name": "Grace Hopper",
    "years": "1906\u20131992",
    "intro": "Found the world\u2019s first computer bug \u2014 literally a moth stuck inside a machine!",
    "detail": (
        "In 1947, Grace found a moth causing errors in the Harvard Mark II "
        "computer. She taped it into her logbook with the note \u2018First "
        "actual case of bug being found.\u2019 That\u2019s where the word "
        "\u2018debugging\u2019 comes from!"
    ),
}

VOCABULARY = [
    {"word": "Syntax Error", "definition": "A typo or grammar mistake in your code \u2014 the computer can\u2019t even read it"},
    {"word": "Logic Error", "definition": "The code runs but gives the WRONG result because the logic is flawed"},
    {"word": "Runtime Error", "definition": "The code crashes while running (e.g. dividing by zero)"},
    {"word": "Trace", "definition": "Following code line-by-line to track what each variable contains"},
]

OBJECTIVES = [
    "Identify the 3 types of bugs: syntax, logic, and runtime.",
    "Read an error message and use it to find the bug.",
    "Trace through code step-by-step to find where it goes wrong.",
]

EXERCISES = [
    {
        "id": 1,
        "title": "Spot the Bug Type",
        "type": "read_conditional",
        "difficulty": "Easy",
        "xp": 10,
        "description": "The ship\u2019s code is broken! Identify what TYPE of bug is causing each problem.",
        "beaver_msg": "Every bug has a personality! Syntax bugs are typos, logic bugs give wrong answers, runtime bugs crash mid-flight!",
        "beaver_hint": "Does it crash before running? (syntax) Crash while running? (runtime) Give the wrong answer? (logic)",
        "problems": [
            {
                "rule": "Move_Forward(50)",
                "situation": "The computer expects lowercase: move_forward(). Tiny change, big difference! What type of bug?",
                "options": ["Syntax error \u2014 wrong capitalisation", "Logic error", "Runtime error", "No bug"],
                "correct": 0,
            },
            {
                "rule": "fuel = input(\"Fuel level: \")\ncan_launch = fuel > 50",
                "situation": "Crew types \"80\" but gets an error. What type?",
                "options": ["Syntax error", "Logic error", "Runtime error \u2014 comparing text to a number", "No bug"],
                "correct": 2,
            },
            {
                "rule": "def calculate_orbit(distance, speed):\n  return distance + speed / 2\n\npath = calculate_orbit(100, 20)",
                "situation": "This returns 110 instead of 60. What type of bug?",
                "options": ["Syntax error", "Logic error \u2014 missing brackets around distance + speed", "Runtime error", "No bug"],
                "correct": 1,
            },
            {
                "rule": "crew = [\"Beaver\", \"Ada\", \"Turing\"]\ncaptain = crew[3]",
                "situation": "What happens when this runs?",
                "options": ["Prints Turing", "Syntax error", "Runtime error \u2014 index 3 doesn\u2019t exist", "Logic error"],
                "correct": 2,
            },
        ],
    },
    {
        "id": 2,
        "title": "Fix the Ship\u2019s Code",
        "type": "bug_hunt",
        "difficulty": "Medium",
        "xp": 15,
        "description": "The ship\u2019s programs are broken! Find the bug and write the fix.",
        "beaver_msg": "The robot is putting on shoes before socks \u2014 that\u2019s a logic bug! Let\u2019s fix these one by one.",
        "beaver_hint": "Trace through each line. The bug is where reality doesn\u2019t match what the code SHOULD do.",
        "bugs": [
            {
                "label": "Bug 1 \u2014 Shield Drain",
                "code": "shield_power = 100\ndamage = 25\nshield_power = shield_power + damage\nprint(\"Shields at:\", shield_power)",
                "hint": "The shields should go DOWN when hit, but they\u2019re going UP! Should it be + or - ?",
            },
            {
                "label": "Bug 2 \u2014 Airlock Access",
                "code": "access_code = \"ALPHA7\"\nuser_code = input(\"Code: \")\nif access_code = user_code:\n  print(\"Airlock open!\")",
                "hint": "One = means assign. Two == means compare. The airlock is getting confused!",
            },
            {
                "label": "Bug 3 \u2014 Landing Countdown",
                "code": "altitude = 1000\nwhile altitude > 0:\n  print(\"Altitude:\", altitude)\n  altitude = altitude + 100",
                "hint": "We\u2019re supposed to descend, but altitude keeps going UP! We\u2019ll fly into deep space forever!",
            },
        ],
    },
    {
        "id": 3,
        "title": "The Multi-Bug Mystery",
        "type": "bug_hunt",
        "difficulty": "Hard",
        "xp": 20,
        "description": (
            "This navigation program has 3 hidden bugs. Find ALL of them "
            "and explain what\u2019s wrong and how to fix each one."
        ),
        "beaver_msg": "This is the ultimate challenge! A real program with multiple bugs. Take it slow and be methodical.",
        "beaver_hint": "Go line by line. Check: are variables spelled correctly? Is the logic right? Are list indices valid?",
        "bugs": [
            {
                "label": "The Crew Roster",
                "code": (
                    "crew = [\"Beaver\", \"Ada\", \"Turing\"]\n"
                    "scores = [95, 42, 78]\n\n"
                    "for i in range(4):\n"
                    "  if scores[i] > 50:\n"
                    "    print(crew[i], \"is mission-ready!\")\n"
                    "  else:\n"
                    "    pritn(crew[i], \"needs more training\")"
                ),
                "hint": "There are 3 bugs: range(4) should be range(3), \u2018pritn\u2019 is a typo, and is 50 the right boundary? Ada scored 42 but the check is > 50 \u2014 should it be >= 50?",
            },
        ],
    },
]

QUIZ = [
    {"question": "What is a syntax error?", "options": ["Wrong logic", "A typo or grammar mistake in code", "The program is too slow", "A missing file"], "correct": 1},
    {"question": "pritn(\"hello\") \u2014 what type of bug?", "options": ["Logic error", "Runtime error", "Syntax error", "No bug"], "correct": 2},
    {"question": "A program runs but gives the wrong answer. What type of bug?", "options": ["Syntax error", "Logic error", "Runtime error", "No bug"], "correct": 1},
    {"question": "What\u2019s the FIRST thing you should do when debugging?", "options": ["Delete everything and start over", "Read the error message carefully", "Ask someone else to fix it", "Turn off the computer"], "correct": 1},
]
