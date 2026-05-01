"""Lesson 11: Patterns & Abstraction.
Track 3: Creation & Application | Dreaming in Space.
"""

LESSON = {
    "id": "lesson-11",
    "title": "Patterns & Abstraction",
    "description": (
        "Spot patterns in problems and code, then abstract away the details "
        "to create general solutions that work for many situations."
    ),
    "duration": 45,
    "level": "Intermediate",
    "age_group": "Ages 8-18",
    "color": "#7c3aed",
    "welcome": (
        "Have you noticed that making tea and making hot chocolate are almost "
        "the SAME steps? Boil water, add ingredient, stir, serve. If you "
        "spot the pattern, you can write ONE solution for both. That\u2019s "
        "the superpower of abstraction!"
    ),
    "recap_msg": (
        "Patterns are everywhere. When you spot them, you can write one "
        "solution instead of many. Abstraction means focusing on what "
        "matters and hiding the details. Master this and you can solve "
        "any problem!"
    ),
}

ROLE_MODEL = {
    "name": "Alan Turing",
    "years": "1912\u20131954",
    "intro": "Father of computer science who showed that ANY computation can be broken into simple patterns.",
    "detail": (
        "Alan proved that a simple machine following patterns could solve "
        "any mathematical problem. His insight \u2014 that complex things "
        "are built from simple repeating patterns \u2014 is the foundation "
        "of all computing."
    ),
}

VOCABULARY = [
    {"word": "Pattern", "definition": "A repeating structure you can predict and reuse"},
    {"word": "Abstraction", "definition": "Removing unnecessary detail to focus on what matters"},
    {"word": "Generalise", "definition": "Taking a specific solution and making it work for many cases"},
    {"word": "Parameter", "definition": "A placeholder that gets replaced with a specific value"},
]

OBJECTIVES = [
    "Identify repeating patterns in sequences, data, and code.",
    "Generalise a specific algorithm to work with different inputs.",
    "Simplify complex code by abstracting repeated parts into functions.",
]

EXERCISES = [
    {
        "id": 1,
        "title": "Find the Pattern",
        "type": "read_conditional",
        "difficulty": "Easy",
        "xp": 10,
        "description": "Look at each sequence and identify what repeats. Predict the next item.",
        "beaver_msg": "Patterns are everywhere \u2014 in numbers, shapes, music, and code. Train your eyes to spot them!",
        "beaver_hint": "Ask: what stays the same? What changes? Is there a rule?",
        "problems": [
            {
                "rule": "2, 4, 6, 8, 10, ?",
                "situation": "What comes next?",
                "options": ["11", "12", "14", "20"],
                "correct": 1,
            },
            {
                "rule": "\u25a0 \u25cb \u25a0 \u25cb \u25a0 \u25cb ?",
                "situation": "What comes next?",
                "options": ["\u25a0 (square)", "\u25cb (circle)", "\u25b2 (triangle)", "Nothing"],
                "correct": 0,
            },
            {
                "rule": "move, turn, move, turn, move, turn, move, turn",
                "situation": "What shape does this make?",
                "options": ["A line", "A triangle", "A square", "A circle"],
                "correct": 2,
            },
            {
                "rule": "def greet_en(): print(\"Hello\")\ndef greet_nl(): print(\"Hallo\")\ndef greet_es(): print(\"Hola\")",
                "situation": "What\u2019s the pattern? How could you improve this?",
                "options": [
                    "No pattern",
                    "Same structure, different word \u2014 use one function with a parameter",
                    "Add more languages as separate functions",
                    "Delete them all"
                ],
                "correct": 1,
            },
        ],
    },
    {
        "id": 2,
        "title": "Generalise the Solution",
        "type": "precision_rewrite",
        "difficulty": "Medium",
        "xp": 15,
        "description": (
            "These two algorithms do almost the same thing. Write ONE "
            "generalised version that works for both using parameters."
        ),
        "beaver_msg": "Two similar recipes? Make ONE recipe with a blank for the ingredient!",
        "beaver_hint": "Find what\u2019s DIFFERENT between the two versions. That becomes a parameter.",
        "vague_instructions": [
            {
                "label": "make_tea() and make_coffee() \u2014 same steps, different drink",
                "why_vague": (
                    "Both: boil water, add [ingredient], stir, pour into cup. "
                    "Write ONE function make_hot_drink(ingredient) that works for both."
                ),
                "min_steps": 4,
            },
            {
                "label": "draw_square() and draw_triangle() \u2014 same concept, different sides",
                "why_vague": (
                    "Square: LOOP 4 TIMES: draw line, turn 90\u00b0. "
                    "Triangle: LOOP 3 TIMES: draw line, turn 120\u00b0. "
                    "Write draw_shape(sides, angle) that works for any regular shape."
                ),
                "min_steps": 3,
            },
        ],
    },
    {
        "id": 3,
        "title": "Abstract & Simplify",
        "type": "precision_rewrite",
        "difficulty": "Hard",
        "xp": 20,
        "description": (
            "This messy program has repeated patterns. Identify them, "
            "create functions, and rewrite it in fewer lines."
        ),
        "beaver_msg": "The ultimate test! Find patterns, extract functions, and make this code elegant.",
        "beaver_hint": "Look for blocks of code that appear more than once. Each one should become a function.",
        "vague_instructions": [
            {
                "label": "Simplify this 15-line program into ~6 lines",
                "why_vague": (
                    "The code calculates and prints a student\u2019s grade 3 times "
                    "with the same logic but different names/scores. "
                    "Extract a function grade_student(name, score) and call it 3 times."
                ),
                "min_steps": 5,
            },
        ],
    },
]

QUIZ = [
    {"question": "What is abstraction?", "options": ["Making code longer", "Removing unnecessary detail to focus on what matters", "A type of loop", "An error"], "correct": 1},
    {"question": "2, 4, 8, 16, 32 \u2014 what\u2019s the pattern?", "options": ["Add 2", "Double each time", "Add 4", "Random"], "correct": 1},
    {"question": "Why generalise a function?", "options": ["To make it harder", "So it works for many cases, not just one", "To use more memory", "It\u2019s not useful"], "correct": 1},
    {"question": "make_tea() and make_coffee() are similar. What should you do?", "options": ["Keep both", "Delete both", "Write one function with a parameter for the drink type", "Add more drinks as separate functions"], "correct": 2},
]
