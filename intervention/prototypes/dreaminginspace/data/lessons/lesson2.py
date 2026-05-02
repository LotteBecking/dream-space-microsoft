"""Lesson 2: Give Your Robot Commands , Precise Instructions & Algorithms.
Track 1: Foundations | Dreaming in Space.

Learners act as 'programmers' giving precise step-by-step commands to a 'robot'.
They discover that robots follow instructions exactly, with no common sense.
"""

LESSON = {
    "id": "lesson-2",
    "title": "Give Your Robot Commands",
    "description": (
        "Become a programmer! Give precise, step-by-step commands to a robot. "
        "Discover what happens when instructions are vague \u2014 and learn to debug."
    ),
    "duration": 45,
    "level": "Beginner",
    "age_group": "Ages 8-18",
    "color": "#0891b2",
    "welcome": (
        "Imagine you have a robot that does EXACTLY what you say \u2014 nothing more, "
        "nothing less. If you say \u2018pick up the pen\u2019 it might not know what a "
        "pen is! Today you\u2019ll learn to give commands so precise that even a "
        "robot can\u2019t get them wrong."
    ),
    "recap_msg": (
        "Robots don\u2019t think \u2014 they follow. If your instructions are clear "
        "and in the right order, the robot succeeds. If not, it fails. That\u2019s "
        "why precision matters in programming!"
    ),
}

ROLE_MODEL = {
    "name": "Reshma Saujani",
    "years": "1975\u2013present",
    "intro": (
        "Founder of Girls Who Code, an organisation that has taught computing "
        "to hundreds of thousands of young people around the world."
    ),
    "detail": (
        "Reshma believes everyone should learn to give computers clear instructions. "
        "She says: \u2018Bravery, not perfection\u2019 \u2014 it\u2019s okay to make mistakes "
        "as long as you debug and try again."
    ),
}

VOCABULARY = [
    {"word": "Command", "definition": "A single instruction that tells the robot what to do"},
    {"word": "Algorithm", "definition": "An ordered sequence of commands to complete a task"},
    {"word": "Bug", "definition": "A mistake in your instructions that causes the wrong result"},
    {"word": "Debug", "definition": "Finding and fixing bugs in your commands"},
    {"word": "Precision", "definition": "Being exact and clear \u2014 no guessing allowed"},
]

OBJECTIVES = [
    "Write precise step-by-step commands that a robot can follow exactly.",
    "Understand that robots have no common sense \u2014 they only do what they\u2019re told.",
    "Find and fix bugs when commands don\u2019t produce the expected result.",
]

# ---------------------------------------------------------------------------
# Exercises
# ---------------------------------------------------------------------------

EXERCISES = [
    {
        "id": 1,
        "title": "Navigate the Maze",
        "type": "robot_maze",
        "difficulty": "Easy",
        "xp": 15,
        "description": (
            "Guide your robot through the asteroid field to reach the goal! "
            "Queue up commands, then hit Run to watch your robot follow them."
        ),
        "beaver_msg": "Press the arrow buttons to queue up moves. Up moves the robot up, Right moves it right \u2014 simple!",
        "beaver_hint": (
            "Plan your path first! Count the squares. You can also use "
            "your keyboard arrow keys to add commands faster."
        ),
        "command_set": ["Up", "Down", "Left", "Right"],
        "scenarios": [],
        "min_steps": 5,
        "maze_level": 1,
    },
    {
        "id": 2,
        "title": "The Gauntlet",
        "type": "robot_maze",
        "difficulty": "Hard",
        "xp": 25,
        "description": (
            "A bigger, tougher maze! Dodge asteroids, avoid fire traps, "
            "and find the safest path to the goal. One wrong move and it\u2019s game over!"
        ),
        "beaver_msg": "This maze is HUGE! Watch out for fire traps \u2014 they destroy the robot instantly. Plan carefully!",
        "beaver_hint": (
            "Trace the path with your eyes first. Fire squares are just "
            "as deadly as walls. There\u2019s only one safe route!"
        ),
        "command_set": ["Up", "Down", "Left", "Right"],
        "scenarios": [],
        "min_steps": 15,
        "maze_level": 2,
    },
    {
        "id": 3,
        "title": "Spot the Bug",
        "type": "robot_debug",
        "difficulty": "Medium",
        "xp": 15,
        "description": "These command sequences have bugs! Read the code, see what went wrong, and pick the correct fix.",
        "beaver_msg": "The robot did exactly what it was told \u2014 but the result is wrong!",
        "beaver_hint": "Read each command step by step. Act it out in your head \u2014 where does it go wrong?",
        "bugs": [
            {
                "label": "Bug 1 \u2014 The Robot Walked Into a Wall",
                "code": (
                    "1. Move Forward  \u27a1\ufe0f\n"
                    "2. Move Forward  \u27a1\ufe0f\n"
                    "3. Move Forward  \u27a1\ufe0f\n"
                    "4. Move Forward  \u27a1\ufe0f\n"
                    "5. Move Forward  \u27a1\ufe0f"
                ),
                "diagram_what_should_happen": [
                    ["\U0001f916", "\u27a1\ufe0f", "\u27a1\ufe0f", "\u27a1\ufe0f", "\u2935\ufe0f", ""],
                    ["", "", "", "", "\u2b07\ufe0f", ""],
                    ["", "", "", "", "\U0001f3c1", ""],
                ],
                "diagram_labels": ["Start", "", "", "Turn Right here!", "", "Goal"],
                "diagram_what_actually_happened": [
                    ["\U0001f916", "\u27a1\ufe0f", "\u27a1\ufe0f", "\u27a1\ufe0f", "\u27a1\ufe0f", "\U0001f4a5"],
                ],
                "scenario": (
                    "The robot should go 3 steps forward, turn right, then 2 more "
                    "steps to reach the goal. But the code says go forward 5 times "
                    "\u2014 it never turns and crashes into the wall!"
                ),
                "hint": "After step 3, the robot needs to change direction. What command is missing?",
                "fixes": [
                    "Add \u2018Turn Right\u2019 after step 3",
                    "Remove step 4 and 5",
                    "Change all steps to Turn Left",
                    "Add \u2018Stop\u2019 at the end",
                ],
                "correct_fix": 0,
            },
            {
                "label": "Bug 2 \u2014 The Robot Dropped the Cup",
                "code": (
                    "1. Move Forward  \u27a1\ufe0f\n"
                    "2. Move Forward  \u27a1\ufe0f\n"
                    "3. Lower Arm     \u2b07\ufe0f\n"
                    "4. Lift Arm      \u2b06\ufe0f\n"
                    "5. Turn Right    \u2935\ufe0f"
                ),
                "diagram_what_should_happen": [
                    ["\U0001f916\u27a1\ufe0f", "\u27a1\ufe0f", "\u2615"],
                    ["", "Lower arm \u2b07\ufe0f", ""],
                    ["", "GRAB \u270a", ""],
                    ["", "Lift arm \u2b06\ufe0f", ""],
                ],
                "diagram_what_actually_happened": [
                    ["\U0001f916\u27a1\ufe0f", "\u27a1\ufe0f", "\u2615"],
                    ["", "Lower arm \u2b07\ufe0f", ""],
                    ["", "Lift arm \u2b06\ufe0f (empty!)", ""],
                    ["", "\U0001f44b Cup still on table!", ""],
                ],
                "scenario": (
                    "The robot walked to the cup and lowered its arm. "
                    "Then it lifted its arm \u2014 but the cup stayed on the table! "
                    "The robot forgot to close its fingers around the cup."
                ),
                "hint": "Look between step 3 and 4. The arm goes down and up but never grabs anything!",
                "fixes": [
                    "Remove step 3 (Lower Arm)",
                    "Add \u2018Close Fingers\u2019 between step 3 and 4",
                    "Change step 4 to \u2018Move Forward\u2019",
                    "Add \u2018Open Fingers\u2019 at the end",
                ],
                "correct_fix": 1,
            },
            {
                "label": "Bug 3 \u2014 The Robot Went the Wrong Way",
                "code": (
                    "1. Turn Left     \u2b05\ufe0f\n"
                    "2. Move Forward  \u27a1\ufe0f\n"
                    "3. Move Forward  \u27a1\ufe0f\n"
                    "4. Turn Left     \u2b05\ufe0f\n"
                    "5. Move Forward  \u27a1\ufe0f"
                ),
                "diagram_what_should_happen": [
                    ["", "", "\U0001f3c1"],
                    ["", "", "\u2b06\ufe0f"],
                    ["\U0001f916", "\u27a1\ufe0f", "\u2935\ufe0f"],
                ],
                "diagram_what_actually_happened": [
                    ["", "", ""],
                    ["", "", ""],
                    ["\u2b05\ufe0f", "\u2b05\ufe0f", "\U0001f916"],
                    ["\U0001f4a5 Wrong way!", "", ""],
                ],
                "scenario": (
                    "The robot should turn RIGHT first, go forward 2 steps, "
                    "turn LEFT, then go forward 1 step to reach the goal above. "
                    "But step 1 says Turn Left \u2014 so it went the completely wrong direction!"
                ),
                "hint": "Step 1 says Turn Left, but the correct direction is Turn Right!",
                "fixes": [
                    "Delete step 1 entirely",
                    "Change step 1 from \u2018Turn Left\u2019 to \u2018Turn Right\u2019",
                    "Swap step 1 and step 4",
                    "Add another Move Forward at the end",
                ],
                "correct_fix": 1,
            },
        ],
    },
]

QUIZ = [
    {
        "question": "Why can\u2019t you tell a robot to \u2018pick up the pen\u2019 in one command?",
        "options": [
            "Robots are too slow",
            "The robot doesn\u2019t know what \u2018pick up\u2019 means \u2014 it needs smaller steps",
            "Pens are too small for robots",
            "Robots can only move forward",
        ],
        "correct": 1,
    },
    {
        "question": "What is an algorithm?",
        "options": [
            "A type of robot",
            "A computer screen",
            "An ordered sequence of commands to complete a task",
            "A programming language",
        ],
        "correct": 2,
    },
    {
        "question": "Your robot hit a wall instead of turning. What happened?",
        "options": [
            "The robot is broken",
            "A Turn command is missing or in the wrong place",
            "The wall appeared suddenly",
            "Robots can\u2019t turn",
        ],
        "correct": 1,
    },
    {
        "question": "What does \u2018debugging\u2019 mean?",
        "options": [
            "Removing insects from a computer",
            "Turning the robot off and on",
            "Finding and fixing mistakes in your instructions",
            "Writing new code from scratch",
        ],
        "correct": 2,
    },
]
