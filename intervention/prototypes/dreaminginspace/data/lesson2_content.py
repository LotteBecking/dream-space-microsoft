"""Lesson 2: Don't Repeat Yourself — Loops & Iteration.
Track 1: Foundations | Dreaming in Space.
"""

LESSON_2 = {
    "id": "lesson-2",
    "title": "Don\u2019t Repeat Yourself \u2014 Loops",
    "description": (
        "Learn that loops let you repeat instructions without rewriting them. "
        "Spot repetition, rewrite it as a loop, and debug broken loops."
    ),
    "duration": 45,
    "level": "Beginner",
    "age_group": "Ages 8-18",
    "color": "#059669",
    "welcome": (
        "Hey! Imagine I asked you to clap 100 times. Would you write "
        "\u2018clap\u2019 100 times? No way! Today we\u2019ll learn the "
        "programmer\u2019s shortcut \u2014 loops. Let\u2019s make our code "
        "shorter AND smarter."
    ),
    "recap_msg": (
        "A loop repeats steps so you don\u2019t have to. Always check: "
        "how many times? And does it stop? You\u2019re thinking like a "
        "real programmer now!"
    ),
}

ROLE_MODEL_2 = {
    "name": "Grace Hopper",
    "years": "1906\u20131992",
    "intro": (
        "Computer scientist and US Navy admiral who helped invent early "
        "programming languages \u2014 and found the first real computer bug "
        "(a moth stuck in a relay!)."
    ),
    "detail": (
        "Grace taped the moth into her notebook and wrote \u2018First "
        "actual case of bug being found.\u2019 The words \u2018bug\u2019 "
        "and \u2018debug\u2019 come from her."
    ),
}

VOCABULARY_2 = [
    {"word": "Loop", "definition": "An instruction that repeats a set of steps"},
    {"word": "Iteration", "definition": "One single run through the loop"},
    {"word": "Infinite Loop", "definition": "A loop that never stops \u2014 usually a bug!"},
    {"word": "Counter", "definition": "A number that tracks how many times the loop has run"},
]

LEARNING_OBJECTIVES_2 = [
    "Explain what a loop is and why it\u2019s useful.",
    "Rewrite repeated instructions as a loop.",
    "Spot and fix bugs in broken loops.",
]

EXERCISES_2 = [
    {
        "id": 1,
        "title": "Spot the Loop",
        "type": "spot_loop",
        "difficulty": "Easy",
        "xp": 10,
        "description": "Look at these routines. Find the steps that repeat and say how many times.",
        "beaver_msg": "Look for the pattern! Which steps happen over and over?",
        "beaver_hint": "Count how many times the same action appears in a row.",
        "problems": [
            {
                "label": "Brushing your teeth",
                "steps": [
                    "Pick up toothbrush", "Squeeze toothpaste",
                    "Brush top left", "Brush top right",
                    "Brush bottom left", "Brush bottom right",
                    "Brush top left", "Brush top right",
                    "Brush bottom left", "Brush bottom right",
                    "Rinse mouth", "Put toothbrush away",
                ],
                "repeat_count": 2,
                "answer_text": "Brush top left, top right, bottom left, bottom right \u2014 repeats 2 times",
            },
            {
                "label": "Setting the table for 4 people",
                "steps": [
                    "Get plates from cupboard",
                    "Place plate", "Place fork", "Place knife", "Place glass",
                    "Place plate", "Place fork", "Place knife", "Place glass",
                    "Place plate", "Place fork", "Place knife", "Place glass",
                    "Place plate", "Place fork", "Place knife", "Place glass",
                ],
                "repeat_count": 4,
                "answer_text": "Place plate, fork, knife, glass \u2014 repeats 4 times",
            },
            {
                "label": "Watering 3 plants",
                "steps": [
                    "Fill watering can",
                    "Walk to plant", "Pour water",
                    "Walk to plant", "Pour water",
                    "Walk to plant", "Pour water",
                    "Put watering can away",
                ],
                "repeat_count": 3,
                "answer_text": "Walk to plant, pour water \u2014 repeats 3 times",
            },
        ],
    },
    {
        "id": 2,
        "title": "Rewrite with a Loop",
        "type": "rewrite_loop",
        "difficulty": "Medium",
        "xp": 15,
        "description": "These algorithms are too long! Rewrite each one using a LOOP.",
        "beaver_msg": "Shrink this long code into a short loop!",
        "beaver_hint": "Find the repeated section, count how many times, then wrap it in LOOP ___ TIMES.",
        "problems": [
            {
                "label": "Jumping Jacks",
                "long_code": (
                    "1. Jump and spread arms\n2. Jump and close arms\n"
                    "3. Jump and spread arms\n4. Jump and close arms\n"
                    "5. Jump and spread arms\n6. Jump and close arms\n"
                    "7. Jump and spread arms\n8. Jump and close arms\n"
                    "9. Jump and spread arms\n10. Jump and close arms"
                ),
                "answer_times": 5,
                "answer_body": "Jump and spread arms\nJump and close arms",
            },
            {
                "label": "Drawing a Square",
                "long_code": (
                    "1. Draw line forward\n2. Turn right 90\u00b0\n"
                    "3. Draw line forward\n4. Turn right 90\u00b0\n"
                    "5. Draw line forward\n6. Turn right 90\u00b0\n"
                    "7. Draw line forward\n8. Turn right 90\u00b0"
                ),
                "answer_times": 4,
                "answer_body": "Draw line forward\nTurn right 90\u00b0",
            },
            {
                "label": "Stacking Pancakes",
                "long_code": (
                    "1. Pour batter\n2. Wait 2 min\n3. Flip\n4. Wait 1 min\n5. Plate\n"
                    "6. Pour batter\n7. Wait 2 min\n8. Flip\n9. Wait 1 min\n10. Plate\n"
                    "11. Pour batter\n12. Wait 2 min\n13. Flip\n14. Wait 1 min\n15. Plate"
                ),
                "answer_times": 3,
                "answer_body": "Pour batter\nWait 2 min\nFlip\nWait 1 min\nPlate",
            },
        ],
    },
    {
        "id": 3,
        "title": "Fix the Broken Loop",
        "type": "bug_hunt",
        "difficulty": "Medium",
        "xp": 20,
        "description": "These loops have bugs! Find what\u2019s wrong and write the fix.",
        "beaver_msg": "Uh oh, these loops are broken! Can you find what went wrong?",
        "beaver_hint": "Check: does it run the right number of times? Does it stop? Is anything missing?",
        "bugs": [
            {
                "label": "Bug 1 \u2014 Wrong Count",
                "code": "LOOP 3 TIMES:\n  Stand up\n  Sit down",
                "hint": "The teacher wanted 5 repetitions, not 3.",
            },
            {
                "label": "Bug 2 \u2014 Never Stops",
                "code": "LOOP FOREVER:\n  Add sugar to coffee\n  Stir",
                "hint": "This loop never stops! What condition should make it stop?",
            },
            {
                "label": "Bug 3 \u2014 Missing Step",
                "code": "LOOP 3 TIMES:\n  Open fridge\n  Take out juice\n  Pour glass",
                "hint": "The fridge door is left open 3 times! What step is missing?",
            },
        ],
    },
]

QUIZ_2 = [
    {
        "question": "What is a loop?",
        "options": [
            "A type of variable",
            "An instruction that repeats a set of steps",
            "A way to store data",
            "A kind of function",
        ],
        "correct": 1,
    },
    {
        "question": "How many times does this run? LOOP 4 TIMES: clap",
        "options": ["1 time", "3 times", "4 times", "Forever"],
        "correct": 2,
    },
    {
        "question": "What is an infinite loop?",
        "options": [
            "A very fast loop",
            "A loop that runs exactly 100 times",
            "A loop that never stops",
            "A loop inside another loop",
        ],
        "correct": 2,
    },
    {
        "question": "Why do programmers use loops?",
        "options": [
            "To make code longer",
            "To avoid repeating the same instructions",
            "To delete variables",
            "To make the computer slower",
        ],
        "correct": 1,
    },
]
