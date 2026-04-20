"""Lesson 3: If This, Then That — Conditionals & Decisions.
Track 1: Foundations | Dreaming in Space.
"""

LESSON_3 = {
    "id": "lesson-3",
    "title": "If This, Then That \u2014 Conditionals",
    "description": (
        "Learn that computers make decisions using IF/THEN/ELSE rules. "
        "Read conditional logic, write your own rules, and debug broken decision systems."
    ),
    "duration": 45,
    "level": "Beginner",
    "age_group": "Ages 8-18",
    "color": "#d97706",
    "welcome": (
        "Have you noticed your phone screen turns off by itself? Or that a "
        "game character takes damage in fire? That\u2019s because someone wrote a "
        "RULE. Today you\u2019ll learn to write rules like a programmer!"
    ),
    "recap_msg": (
        "A conditional is a decision rule. IF something is true, do this. "
        "ELSE, do that. You just learned how every app, game, and smart "
        "device thinks. Amazing!"
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
        "title": "Read the Rule",
        "type": "read_conditional",
        "difficulty": "Easy",
        "xp": 10,
        "description": "Read each IF/THEN/ELSE rule and predict what happens.",
        "beaver_msg": "Read the rule carefully. Is the condition true or false? Follow the right path!",
        "beaver_hint": "Check: is the IF condition true? If yes, follow THEN. If no, follow ELSE.",
        "problems": [
            {
                "rule": "IF temperature < 18\u00b0C THEN turn heating ON\nELSE turn heating OFF",
                "situation": "The temperature is 22\u00b0C.",
                "options": ["Turn heating ON", "Turn heating OFF", "Do nothing", "Check again"],
                "correct": 1,
            },
            {
                "rule": "IF player touches coin THEN score = score + 10\nELSE score stays the same",
                "situation": "The player walks past the coin without touching it.",
                "options": ["Score goes up by 10", "Score stays the same", "Score goes down", "Game ends"],
                "correct": 1,
            },
            {
                "rule": "IF it is raining THEN take umbrella\nELSE IF it is sunny THEN take sunglasses\nELSE take nothing",
                "situation": "It\u2019s a sunny day.",
                "options": ["Take umbrella", "Take sunglasses", "Take nothing", "Take both"],
                "correct": 1,
            },
            {
                "rule": "IF age >= 12 THEN show teen content\nELSE show kids content",
                "situation": "The user is 10 years old.",
                "options": ["Show teen content", "Show kids content", "Show nothing", "Ask again"],
                "correct": 1,
            },
        ],
    },
    {
        "id": 2,
        "title": "Write the Rule",
        "type": "write_conditional",
        "difficulty": "Medium",
        "xp": 15,
        "description": "Choose a scenario and write a complete IF/ELSE IF/ELSE chain.",
        "beaver_msg": "Now you\u2019re the rule-maker! Write a rule that handles every possibility.",
        "beaver_hint": "Make sure you have at least: one IF, one ELSE IF, and one ELSE.",
        "scenarios": [
            {
                "label": "A \u2014 Smart Alarm Clock",
                "detail": "Gentle music on weekdays, loud buzzer on Monday, silence on weekends.",
            },
            {
                "label": "B \u2014 Game Power-Ups",
                "detail": "Red items = +10 points, gold = double score, black = game over, else nothing.",
            },
            {
                "label": "C \u2014 School Canteen",
                "detail": "Pre-ordered meals first, then card, then cash. If sold out, back of queue.",
            },
        ],
        "min_lines": 3,
    },
    {
        "id": 3,
        "title": "Fix the Smart Home",
        "type": "bug_hunt",
        "difficulty": "Medium",
        "xp": 20,
        "description": "These smart-home systems have bugs! Find what\u2019s wrong and fix them.",
        "beaver_msg": "The house is going haywire! These rules are buggy \u2014 can you fix them?",
        "beaver_hint": "Look for missing conditions, wrong logic, or loops that interact badly.",
        "bugs": [
            {
                "label": "Bug 1 \u2014 Heating Never Stops",
                "code": "IF temperature < 18\u00b0C\n  THEN turn heating ON\n(no ELSE rule exists)",
                "hint": "What happens when the temperature reaches 18\u00b0C?",
            },
            {
                "label": "Bug 2 \u2014 Daylight Security Light",
                "code": "IF motion detected\n  THEN turn light ON",
                "hint": "This turns on even in bright daylight! What condition is missing?",
            },
            {
                "label": "Bug 3 \u2014 47 Milk Alerts per Minute",
                "code": "LOOP FOREVER:\n  IF milk is low\n    THEN send alert to phone",
                "hint": "The alert sends every loop iteration! How do you send it only once?",
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
