"""Lesson 3: The If-Then Gates — Conditionals & Decisions.
Track 1: Foundations | Dreaming in Space.
"""

LESSON_3 = {
    "id": "lesson-4",
    "title": "The If-Then Gates",
    "description": (
        "Learn that computers make decisions using IF/THEN/ELSE rules. "
        "Read conditional logic, write your own rules, and debug broken decision systems."
    ),
    "duration": 45,
    "level": "Beginner",
    "age_group": "Ages 8-18",
    "color": "#d97706",
    "welcome": (
        "The ship\u2019s computer needs to make decisions. IF the door is "
        "locked, THEN we need a key. IF the oxygen is low, THEN sound "
        "the alarm. Today you\u2019ll build \u2018Choice Gates\u2019 that "
        "make the ship think for itself!"
    ),
    "recap_msg": (
        "You gave the ship a brain! Now it can make smart choices based "
        "on what\u2019s happening around it. IF something is true, do this. "
        "ELSE, do that. Every app, game, and smart device thinks this way!"
    ),
}

ROLE_MODEL_3 = {
    "name": "Katherine Johnson",
    "years": "1918\u20132020",
    "intro": (
        "NASA mathematician whose conditional calculations determined "
        "whether Apollo 11 would safely reach the Moon and return."
    ),
    "detail": (
        "Katherine wrote equations that told the spacecraft: IF you are on "
        "this trajectory AND within this speed range, THEN fire the engine "
        "for exactly this many seconds, ELSE abort."
    ),
}

VOCABULARY_3 = [
    {"word": "Conditional", "definition": "A rule that only runs if a certain condition is true"},
    {"word": "IF", "definition": "The question the computer checks \u2014 true or false?"},
    {"word": "THEN", "definition": "What happens if the answer is yes (true)"},
    {"word": "ELSE", "definition": "What happens if the answer is no (false)"},
    {"word": "Boolean", "definition": "A value that is either true or false \u2014 nothing in between"},
]

LEARNING_OBJECTIVES_3 = [
    "Explain what a conditional is in plain language.",
    "Write IF/THEN/ELSE rules for real-world scenarios.",
    "Find and fix bugs in broken conditional logic.",
]

EXERCISES_3 = [
    {
        "id": 1,
        "title": "Open the Gate",
        "type": "read_conditional",
        "difficulty": "Easy",
        "xp": 10,
        "description": "The ship has \u2018Choice Gates\u2019 everywhere. Read each rule and predict what happens.",
        "beaver_msg": "The gate checks a condition. Is it TRUE or FALSE? Follow the right path!",
        "beaver_hint": "Check: is the IF condition true? If yes, follow THEN. If no, follow ELSE.",
        "problems": [
            {
                "rule": "IF battery_level < 20% THEN charge_ship()\nELSE keep_flying()",
                "situation": "Battery is at 85%.",
                "options": ["Charge the ship", "Keep flying", "Do nothing", "Emergency landing"],
                "correct": 1,
            },
            {
                "rule": "IF alien_spotted == True THEN say_hello()\nELSE keep_scanning()",
                "situation": "The radar shows an alien vessel nearby!",
                "options": ["Keep scanning", "Say hello", "Run away", "Turn off radar"],
                "correct": 1,
            },
            {
                "rule": "IF oxygen_level >= 100% THEN open_valve()\nELSE close_valve()",
                "situation": "Oxygen is at 100%.",
                "options": ["Open the valve", "Close the valve", "Do nothing", "Check again"],
                "correct": 0,
            },
            {
                "rule": "IF it_is_dark AND motion_detected THEN activate_lights()\nELSE lights_off()",
                "situation": "It\u2019s dark but nobody is moving.",
                "options": ["Activate lights", "Nothing \u2014 both conditions must be true", "Lights off", "Error"],
                "correct": 2,
            },
        ],
    },
    {
        "id": 2,
        "title": "The Emergency Script",
        "type": "write_conditional",
        "difficulty": "Medium",
        "xp": 15,
        "description": "The ship needs safety rules! Write IF/ELSE IF/ELSE chains for these emergencies.",
        "beaver_msg": "Write a rule: IF temperature is greater than 100, THEN activate_cooling()! You\u2019re saving the engines!",
        "beaver_hint": "Make sure you have at least: one IF, one ELSE IF, and one ELSE.",
        "scenarios": [
            {
                "label": "A \u2014 Engine Temperature Alert",
                "detail": "IF temp > 100\u00b0C THEN activate cooling. ELSE IF temp > 80\u00b0C THEN warning light. ELSE all clear.",
            },
            {
                "label": "B \u2014 Alien Encounter Protocol",
                "detail": "IF alien is friendly THEN trade resources. ELSE IF alien is neutral THEN observe. ELSE raise shields.",
            },
            {
                "label": "C \u2014 Landing Autopilot",
                "detail": "IF altitude < 100m AND speed < 50 THEN deploy landing gear. ELSE IF altitude < 500m THEN slow down. ELSE keep descending.",
            },
        ],
        "min_lines": 3,
    },
    {
        "id": 3,
        "title": "Fix the Ship\u2019s Brain",
        "type": "bug_hunt",
        "difficulty": "Medium",
        "xp": 20,
        "description": "The ship\u2019s decision systems have bugs! Fix them before something explodes!",
        "beaver_msg": "The ship is going haywire! These rules are buggy \u2014 can you fix them?",
        "beaver_hint": "Look for missing conditions, wrong logic, or loops that interact badly.",
        "bugs": [
            {
                "label": "Bug 1 \u2014 Heating Never Stops",
                "code": "IF temperature < 18\u00b0C\n  THEN turn heating ON\n(no ELSE rule exists)",
                "hint": "The heating turns on but never turns off! What happens when temp reaches 18\u00b0C?",
            },
            {
                "label": "Bug 2 \u2014 Shields in Safe Space",
                "code": "IF enemy_detected\n  THEN raise_shields()",
                "hint": "Shields go up when enemies appear but never come down! What ELSE is needed?",
            },
            {
                "label": "Bug 3 \u2014 999 Distress Signals Per Minute",
                "code": "LOOP FOREVER:\n  IF fuel_low == True\n    THEN send_distress_signal()",
                "hint": "The distress signal sends EVERY loop iteration! How do you send it only once?",
            },
        ],
    },
]

QUIZ_3 = [
    {
        "question": "What does a conditional do?",
        "options": [
            "Repeats code many times",
            "Stores information",
            "Makes a decision based on true or false",
            "Deletes data",
        ],
        "correct": 2,
    },
    {
        "question": "In IF/THEN/ELSE, what does ELSE mean?",
        "options": [
            "Do this if the condition is true",
            "Do this if the condition is false",
            "Always do this",
            "Skip everything",
        ],
        "correct": 1,
    },
    {
        "question": "What is a Boolean?",
        "options": [
            "A number between 0 and 100",
            "A value that is either true or false",
            "A type of loop",
            "A programming language",
        ],
        "correct": 1,
    },
    {
        "question": "IF it is dark AND motion detected THEN turn on light. It\u2019s dark but nobody is moving. What happens?",
        "options": [
            "Light turns on",
            "Nothing \u2014 both conditions must be true",
            "Light turns off",
            "An error occurs",
        ],
        "correct": 1,
    },
]
