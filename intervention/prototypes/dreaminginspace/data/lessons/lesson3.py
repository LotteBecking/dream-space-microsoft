"""Lesson 2: The Loop Station — Loops & Iteration.
Track 1: Foundations | Dreaming in Space.
"""

LESSON = {
    "id": "lesson-3",
    "title": "The Loop Station",
    "description": (
        "Learn that loops let you repeat instructions without rewriting them. "
        "Spot repetition, rewrite it as a loop, and debug broken loops."
    ),
    "duration": 45,
    "level": "Beginner",
    "age_group": "Ages 8-18",
    "color": "#059669",
    "welcome": (
        "Ugh, my paws are tired! I have to check 100 air vents on the "
        "ship. Instead of writing \u2018check\u2019 100 times, let\u2019s "
        "build a LOOP to do the heavy lifting. Loops are a programmer\u2019s "
        "shortcut \u2014 let\u2019s make our code shorter AND smarter!"
    ),
    "recap_msg": (
        "You mastered the Loop! Now you can handle thousands of tasks "
        "with just two lines of code. Always check: how many times? "
        "And does it stop? You\u2019re thinking like a real programmer now!"
    ),
}

ROLE_MODEL = {
    "name": "Donald Knuth",
    "years": "1938\u2013present",
    "intro": (
        "Computer scientist who wrote \u2018The Art of Computer Programming\u2019 "
        "\u2014 the definitive book on algorithms and how loops really work."
    ),
    "detail": (
        "Donald showed that even simple loops can solve incredibly complex "
        "problems. His books are used by programmers at Google, Microsoft, "
        "and NASA. He also created the TeX typesetting system that scientists "
        "use worldwide."
    ),
}

VOCABULARY = [
    {"word": "Loop", "definition": "An instruction that repeats a set of steps"},
    {"word": "Iteration", "definition": "One single run through the loop"},
    {"word": "Infinite Loop", "definition": "A loop that never stops \u2014 usually a bug!"},
    {"word": "Counter", "definition": "A number that tracks how many times the loop has run"},
]

OBJECTIVES = [
    "Explain what a loop is and why it\u2019s useful.",
    "Rewrite repeated instructions as a loop.",
    "Spot and fix bugs in broken loops.",
]

EXERCISES = [
    {
        "id": 1,
        "title": "The Pattern Finder",
        "type": "spot_loop",
        "difficulty": "Easy",
        "xp": 10,
        "description": "Look at these space station routines. Find the steps that repeat and say how many times.",
        "beaver_msg": "Look at this messy code: walk, check, walk, check. What\u2019s the repeating pattern?",
        "beaver_hint": "Count how many times the same action appears in a row.",
        "problems": [
            {
                "label": "Checking 4 solar panels",
                "steps": [
                    "Put on space gloves",
                    "Walk to panel", "Clean panel", "Check power output",
                    "Walk to panel", "Clean panel", "Check power output",
                    "Walk to panel", "Clean panel", "Check power output",
                    "Walk to panel", "Clean panel", "Check power output",
                    "Return to airlock",
                ],
                "repeat_count": 4,
                "answer_text": "Walk to panel, clean panel, check power output \u2014 repeats 4 times",
            },
            {
                "label": "Morning routine on the space station",
                "steps": [
                    "Wake up",
                    "Float to exercise bike", "Pedal for 10 min",
                    "Float to exercise bike", "Pedal for 10 min",
                    "Float to exercise bike", "Pedal for 10 min",
                    "Eat breakfast", "Brush teeth",
                ],
                "repeat_count": 3,
                "answer_text": "Float to exercise bike, pedal for 10 min \u2014 repeats 3 times",
            },
            {
                "label": "Loading cargo into the shuttle",
                "steps": [
                    "Open cargo door",
                    "Pick up crate", "Scan barcode", "Place in shuttle",
                    "Pick up crate", "Scan barcode", "Place in shuttle",
                    "Pick up crate", "Scan barcode", "Place in shuttle",
                    "Pick up crate", "Scan barcode", "Place in shuttle",
                    "Pick up crate", "Scan barcode", "Place in shuttle",
                    "Close cargo door",
                ],
                "repeat_count": 5,
                "answer_text": "Pick up crate, scan barcode, place in shuttle \u2014 repeats 5 times",
            },
        ],
    },
    {
        "id": 2,
        "title": "The Loop Builder",
        "type": "rewrite_loop",
        "difficulty": "Medium",
        "xp": 15,
        "description": "These mission logs are way too long! Rewrite each one using a LOOP.",
        "beaver_msg": "We have 4 solar panels. Drag the correct number into the \u2018Repeat\u2019 block so we don\u2019t miss any!",
        "beaver_hint": "Find the repeated section, count how many times, then wrap it in LOOP ___ TIMES.",
        "problems": [
            {
                "label": "Scanning for Asteroids",
                "long_code": (
                    "1. Point telescope north\n2. Take photo\n3. Log data\n"
                    "4. Point telescope east\n5. Take photo\n6. Log data\n"
                    "7. Point telescope south\n8. Take photo\n9. Log data\n"
                    "10. Point telescope west\n11. Take photo\n12. Log data"
                ),
                "answer_times": 4,
                "answer_body": "Point telescope [direction]\nTake photo\nLog data",
            },
            {
                "label": "Drawing a Square in Space",
                "long_code": (
                    "1. Fire thrusters forward\n2. Turn right 90\u00b0\n"
                    "3. Fire thrusters forward\n4. Turn right 90\u00b0\n"
                    "5. Fire thrusters forward\n6. Turn right 90\u00b0\n"
                    "7. Fire thrusters forward\n8. Turn right 90\u00b0"
                ),
                "answer_times": 4,
                "answer_body": "Fire thrusters forward\nTurn right 90\u00b0",
            },
            {
                "label": "Refuelling 3 Escape Pods",
                "long_code": (
                    "1. Connect fuel hose\n2. Fill tank to 100%\n3. Disconnect hose\n4. Run safety check\n"
                    "5. Connect fuel hose\n6. Fill tank to 100%\n7. Disconnect hose\n8. Run safety check\n"
                    "9. Connect fuel hose\n10. Fill tank to 100%\n11. Disconnect hose\n12. Run safety check"
                ),
                "answer_times": 3,
                "answer_body": "Connect fuel hose\nFill tank to 100%\nDisconnect hose\nRun safety check",
            },
        ],
    },
    {
        "id": 3,
        "title": "Infinite Loop Debug",
        "type": "bug_hunt",
        "difficulty": "Medium",
        "xp": 20,
        "description": "These ship loops have bugs! Find what\u2019s wrong and write the fix.",
        "beaver_msg": "Oh no! The alarm is stuck in an Infinite Loop! It\u2019s going off forever!",
        "beaver_hint": "Check: does it run the right number of times? Does it stop? Is anything missing?",
        "bugs": [
            {
                "label": "Bug 1 \u2014 Alarm Won\u2019t Stop",
                "code": "LOOP FOREVER:\n  sound_alarm()\n  flash_lights()",
                "hint": "The alarm is going off FOREVER! It should only beep 3 times. Change FOREVER to a number.",
            },
            {
                "label": "Bug 2 \u2014 Airlock Left Open",
                "code": "LOOP 5 TIMES:\n  Open airlock\n  Send out probe\n  Collect sample",
                "hint": "The airlock is left open 5 times! What step is missing at the end?",
            },
            {
                "label": "Bug 3 \u2014 Fuel Overflow",
                "code": "LOOP FOREVER:\n  add_fuel(10)\n  (tank capacity is 100)",
                "hint": "This keeps adding fuel forever and the tank will overflow! When should it stop?",
            },
        ],
    },
]

QUIZ = [
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
