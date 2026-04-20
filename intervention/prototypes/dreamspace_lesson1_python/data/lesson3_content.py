"""Lesson 3 content: If This, Then That -- How Computers Make Decisions."""

LESSON_3 = {
    "id": "lesson-3",
    "title": "If This, Then That \u2014 How Computers Make Decisions",
    "description": (
        "Students learn conditionals, write IF/THEN/ELSE logic, and debug "
        "decision rules used in everyday technology. Combines all three CT "
        "building blocks: sequence, loops, and conditionals."
    ),
    "duration": 60,
    "level": "Beginner",
    "age_group": "Ages 8-12",
    "welcome": "Today we think like Katherine Johnson \u2014 the mathematician who kept astronauts safe with IF/THEN logic!",
    "research_basis": (
        "Completes the CT triad: Sequence \u2192 Loops \u2192 Conditionals. Grover & Pea "
        "(2013) identify conditionals as the third essential CT concept for primary "
        "learners. Physical warm-up follows Bell et al. (1998). Edge-case reasoning "
        "connects to Kapur\u2019s (2008) productive failure."
    ),
}

ROLE_MODEL_3 = {
    "name": "Katherine Johnson",
    "years": "1918\u20132020",
    "intro": (
        "NASA mathematician whose conditional calculations determined whether "
        "Apollo 11 would safely reach the Moon and return."
    ),
    "detail": (
        "Katherine wrote the equations that told the spacecraft: IF you are on this "
        "trajectory AND within this speed range, THEN fire the engine for exactly "
        "this many seconds, ELSE abort. Her conditionals were trusted over the "
        "computers \u2014 the astronauts\u2019 lives depended on her precision."
    ),
}

VOCABULARY_3 = [
    {"word": "Conditional", "definition": "A rule that only runs if a certain condition is true"},
    {"word": "IF", "definition": "The condition being checked"},
    {"word": "THEN", "definition": "What happens if the condition is true"},
    {"word": "ELSE", "definition": "What happens if the condition is not true"},
    {"word": "Boolean", "definition": "A value that is either true or false \u2014 nothing in between"},
]

LEARNING_OBJECTIVES_3 = [
    "Explain what a conditional is in plain language.",
    "Write a basic IF/THEN/ELSE rule and chain conditions with ELSE IF.",
    "Identify where conditional logic operates in technology used every day.",
    "Reason about edge cases and rule order in decision systems.",
]

EXERCISES_3 = [
    {
        "id": 1,
        "title": "Write the Conditional",
        "description": (
            "Choose one scenario and write full IF/THEN/ELSE logic with at "
            "least three connected conditions (IF, ELSE IF, ELSE)."
        ),
        "type": "written_conditional",
        "difficulty": "Easy",
        "duration_minutes": 8,
        "scenarios": [
            {
                "label": "A \u2014 Smart Alarm Clock",
                "detail": "Gentle music on weekdays, loud buzzer on Monday only, silence on weekends.",
            },
            {
                "label": "B \u2014 School Canteen Queue",
                "detail": (
                    "Pre-ordered meals first, then card, then cash; "
                    "if meal is out of stock, student goes to back of queue."
                ),
            },
            {
                "label": "C \u2014 Game Power-Up",
                "detail": (
                    "Red items add 10 points, gold items double current score, "
                    "grey items do nothing, black items end the game immediately."
                ),
            },
        ],
        "rules": [
            "Pick one scenario (A, B, or C).",
            "Write one connected IF / ELSE IF / ELSE chain \u2014 not separate IF statements.",
            "You must have at least: one IF, one ELSE IF, and one ELSE.",
            "Think about edge cases your rules might miss.",
        ],
        "min_steps": 3,
        "learning_styles": ["Read/Write", "Logical/Mathematical", "Interpersonal"],
        "research_basis": (
            "Wing (2006) identifies conditional logic as a pillar of CT. "
            "Grover & Pea (2013) confirm primary-age children can write IF/THEN/ELSE "
            "chains with concrete scenarios. Partner edge-case review leverages the "
            "ZPD (Vygotsky, 1978)."
        ),
    },
    {
        "id": 2,
        "title": "Fix the Broken Smart Home",
        "description": (
            "Identify bugs in three smart-home conditional systems and "
            "write corrected logic."
        ),
        "type": "bug_hunt",
        "difficulty": "Medium",
        "duration_minutes": 7,
        "bugs": [
            {
                "label": "Bug 1 \u2014 Heating Never Stops",
                "code": (
                    "IF temperature < 18\u00b0C\n"
                    "  THEN turn heating ON\n"
                    "(no ELSE rule exists)"
                ),
                "hint": "What happens when it reaches 18\u00b0C? The heating just stays on forever!",
            },
            {
                "label": "Bug 2 \u2014 Daylight Security Light",
                "code": (
                    "IF motion detected\n"
                    "  THEN turn light ON"
                ),
                "hint": "This turns on even in bright daylight. What condition is missing?",
            },
            {
                "label": "Bug 3 \u2014 47 Milk Alerts per Minute",
                "code": (
                    "LOOP FOREVER:\n"
                    "  IF milk is low\n"
                    "    THEN send alert to phone"
                ),
                "hint": "The alert sends every loop iteration! How do you send it only once?",
            },
        ],
        "learning_styles": ["Logical/Mathematical", "Visual/Spatial", "Interpersonal"],
        "research_basis": (
            "Kapur (2008) productive failure: engaging with broken systems before "
            "writing correct ones deepens understanding. Bug 3 connects loops (Lesson 2) "
            "with conditionals \u2014 Perkins & Salomon (1992) show cross-domain transfer is "
            "strongest when learners are prompted to make connections."
        ),
    },
    {
        "id": 3,
        "title": "Build a Smarter Traffic Light",
        "description": (
            "Design conditional rules for an adaptive traffic light using "
            "car-count sensors and emergency handling."
        ),
        "type": "written_extended",
        "difficulty": "Medium",
        "duration_minutes": 10,
        "fields": [
            {"name": "basic_rules", "label": "Write rules for green-light duration based on cars waiting", "type": "steps"},
            {"name": "emergency", "label": "Add a priority rule for ambulance detection", "type": "textarea"},
            {"name": "night_mode", "label": "What should happen at 3am when no cars are waiting?", "type": "textarea"},
            {"name": "side_effect", "label": "One risk where optimising one junction worsens another", "type": "textarea"},
        ],
        "learning_styles": ["Logical/Mathematical", "Visual/Spatial", "Read/Write"],
        "research_basis": (
            "High-ceiling task (Bers, 2018): basic rules are accessible, citywide "
            "interaction pushes toward systems thinking \u2014 a higher-order CT skill "
            "(Wing, 2006). Emergency-vehicle priority introduces interrupt logic, "
            "a bridge toward advanced programming (Grover & Pea, 2013)."
        ),
    },
]
