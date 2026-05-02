"""Lesson 7: Function Factories — Reusable Instructions.
Track 2: Text-Based Coding | Dreaming in Space.
"""

LESSON = {
    "id": "lesson-7",
    "title": "Function Factories",
    "description": (
        "Learn to group instructions into a named function you can call "
        "anytime \u2014 like a recipe you use again and again."
    ),
    "duration": 45,
    "level": "Beginner",
    "age_group": "Ages 8-18",
    "color": "#0d9488",
    "welcome": (
        "We have a \u2018Landing Sequence\u2019 \u2014 fold wings, lower "
        "gear, slow down. Instead of listing those every time we land, I "
        "just call Landing_Sequence(). That\u2019s a Function! Build it "
        "once, use it whenever you need it \u2014 like power-ups for your code!"
    ),
    "recap_msg": (
        "Functions are like power-ups. You build them once, and use them "
        "whenever you need them! Parameters let you customise what they "
        "do each time. Every app, game, and website is built with functions!"
    ),
}

ROLE_MODEL = {
    "name": "Guido van Rossum",
    "years": "1956\u2013present",
    "intro": "Creator of Python \u2014 one of the most popular programming languages in the world.",
    "detail": (
        "Guido designed Python to be easy to read and write. He made functions "
        "simple so that beginners could start building useful programs quickly. "
        "Python is used by YouTube, Instagram, Spotify, and NASA."
    ),
}

VOCABULARY = [
    {"word": "Function", "definition": "A named block of code that does a specific job"},
    {"word": "Call", "definition": "Running a function by using its name followed by ()"},
    {"word": "Parameter", "definition": "Information you pass INTO a function to customise it"},
    {"word": "Return", "definition": "The result a function sends back when it\u2019s done"},
]

OBJECTIVES = [
    "Explain what a function is and why it saves time.",
    "Read a function and predict what it does when called.",
    "Write a simple function and call it with different inputs.",
]

EXERCISES = [
    {
        "id": 1,
        "concept": {
            'title': 'What is a Function?',
            'body': 'A <strong>function</strong> is a <strong>reusable power-up</strong>. You write the steps once, give it a name, then call it whenever you need it!',
            'examples': [
                '🔌 <strong>def shields_up():</strong> defines a function. <strong>shields_up()</strong> runs it.',
                '💪 Functions can take <strong>inputs</strong> (parameters) and give back a <strong>result</strong> (return).',
            ],
            'outro': 'Read each function below &mdash; what does it print or return?',
            'bg_from': '#fef3c7',
            'bg_to': '#fde68a',
            'border': '#f59e0b',
        },
        "title": "Name That Action",
        "type": "read_conditional",
        "difficulty": "Easy",
        "xp": 10,
        "description": "Read each function, then predict what happens when we call it.",
        "beaver_msg": "If we group fold_wings(), lower_gear(), and slow_down() \u2014 what should we name the function?",
        "beaver_hint": "A good function name tells you exactly what it does. Landing_Sequence, not Do_Stuff!",
        "problems": [
            {
                "rule": "def shields_up():\n  power = 100\n  print(\"Shields activated!\")\n\nshields_up()",
                "situation": "What gets printed?",
                "options": ["Nothing", "shields_up", "Shields activated!", "Error"],
                "correct": 2,
            },
            {
                "rule": "def calculate_fuel(distance, speed):\n  return distance / speed\n\ntrip = calculate_fuel(300, 50)",
                "situation": "What is \u2018trip\u2019?",
                "options": ["300", "50", "6", "350"],
                "correct": 2,
            },
            {
                "rule": "def scan_planet(name):\n  return \"Scanning: \" + name\n\nmsg = scan_planet(\"Mars\")",
                "situation": "What is \u2018msg\u2019?",
                "options": ["Scanning: name", "Scanning: Mars", "Mars", "scan_planet"],
                "correct": 1,
            },
            {
                "rule": "We group these commands:\n  fold_wings()\n  lower_gear()\n  slow_down()\nWhat should the function be called?",
                "situation": "Which name is best?",
                "options": ["Do_Stuff()", "Landing_Sequence()", "Potato()", "Function_1()"],
                "correct": 1,
            },
        ],
    },
    {
        "id": 2,
        "title": "Building the Bundle",
        "type": "robot_commands",
        "difficulty": "Medium",
        "xp": 15,
        "description": (
            "Build your own ship functions! Group commands into functions "
            "and call them with different values."
        ),
        "beaver_msg": "You\u2019re building your own tools now! Write it once, use it forever.",
        "beaver_hint": (
            "Start with def function_name(parameter): then write what it does "
            "inside. Don\u2019t forget return if it calculates something!"
        ),
        "command_set": [
            "def function_name(param):",
            "  return result",
            "function_name(value)",
        ],
        "scenarios": [
            {
                "label": "Write a function called \u2018refuel\u2019 that takes current_fuel and amount, and returns the total",
                "hint": "def refuel(current_fuel, amount): return current_fuel + amount",
            },
            {
                "label": "Write a function called \u2018is_safe_to_land\u2019 that takes altitude and returns True if it\u2019s below 100",
                "hint": "def is_safe_to_land(altitude): return altitude < 100",
            },
        ],
        "min_steps": 3,
    },
    {
        "id": 3,
        "title": "Emergency Function Call",
        "type": "precision_rewrite",
        "difficulty": "Medium",
        "xp": 20,
        "description": (
            "The ship is under attack! We already wrote defence functions. "
            "Spot the repeated code and refactor it into reusable functions."
        ),
        "beaver_msg": "The ship is under attack! We already wrote Shields_Up(). Type it below to activate!",
        "beaver_hint": "Find the repeated block, turn it into a function with a name, then call it.",
        "vague_instructions": [
            {
                "label": "Repeated shield activation code",
                "why_vague": (
                    "The code activates shields for 3 different sectors by copying "
                    "the same 4 lines each time. Write a function called activate_shield(sector) "
                    "and call it 3 times instead!"
                ),
                "min_steps": 4,
            },
            {
                "label": "Repeated scan & report",
                "why_vague": (
                    "The code scans 3 different planets the same way. "
                    "Make a function called scan_and_report(planet_name) and call it 3 times."
                ),
                "min_steps": 3,
            },
        ],
    },
]

QUIZ = [
    {"question": "What is a function?", "options": ["A type of variable", "A named block of code that does a specific job", "A loop", "An error"], "correct": 1},
    {"question": "What does \u2018calling\u2019 a function mean?", "options": ["Deleting it", "Writing it for the first time", "Running it by using its name", "Copying it"], "correct": 2},
    {"question": "What is a parameter?", "options": ["The function\u2019s name", "Information you pass into a function", "A bug", "A type of variable"], "correct": 1},
    {"question": "Why do programmers use functions?", "options": ["To make code longer", "To avoid writing the same code over and over", "To slow down the program", "To delete variables"], "correct": 1},
]
