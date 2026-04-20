"""Lesson 2 content: Don't Repeat Yourself -- Loops and Efficiency."""

LESSON_2 = {
    "id": "lesson-2",
    "title": "Don\u2019t Repeat Yourself \u2014 Loops and Efficiency",
    "description": (
        "Students learn what loops are, why they make code efficient, "
        "and how to debug looping bugs. Activities move from physical "
        "body-loops to written loop notation, supporting kinaesthetic "
        "and logical learners (Bell et al., 1998; Gardner, 1983)."
    ),
    "duration": 60,
    "level": "Beginner",
    "age_group": "Ages 8-12",
    "welcome": "Today we think like Grace Hopper \u2014 the queen of loops and the person who found the first real bug!",
    "research_basis": (
        "Builds on Lesson 1 sequences. Grover & Pea (2013) identify iteration "
        "as a key CT concept accessible to primary-age learners. Physical warm-up "
        "follows Bell et al. (1998). Debugging framed via Dweck (2006) growth mindset."
    ),
    "video_url": "",
}

ROLE_MODEL_2 = {
    "name": "Grace Hopper",
    "years": "1906\u20131992",
    "intro": (
        "Computer scientist and US Navy admiral who helped invent early "
        "programming languages \u2014 and discovered the first real computer bug "
        "(literally a moth stuck in a relay)."
    ),
    "detail": (
        "Grace Hopper found a moth causing errors in a computer and taped it "
        "into her notebook, writing \u2018First actual case of bug being found.\u2019 "
        "The words \u2018bug\u2019 and \u2018debug\u2019 come from her. She built tools so "
        "programmers never had to repeat themselves \u2014 just like loops."
    ),
}

VOCABULARY_2 = [
    {"word": "Loop", "definition": "An instruction that repeats a set of steps a set number of times"},
    {"word": "Iteration", "definition": "One single run through the loop"},
    {"word": "Bug", "definition": "An error in the code that causes the wrong output"},
    {"word": "Debug", "definition": "Finding and fixing a bug"},
    {"word": "Efficient", "definition": "Doing the most with the least effort"},
]

LEARNING_OBJECTIVES_2 = [
    "Explain what a loop is and why programmers use loops instead of repeating the same line many times.",
    "Identify repetition in everyday routines and technology examples.",
    "Use and explain key vocabulary: loop, iteration, bug, debug, efficient.",
    "Spot a bug in a loop and suggest a fix.",
]

EXERCISES_2 = [
    {
        "id": 1,
        "title": "Rewrite It with a Loop",
        "description": (
            "Rewrite the repeated hair-brushing algorithm using loops, then "
            "create a more complex loop for left/right/back sections."
        ),
        "type": "written_steps",
        "difficulty": "Easy",
        "duration_minutes": 8,
        "prompt": (
            "Here is a long algorithm:\n\n"
            "1. Move brush from top of head to bottom\n"
            "2. Move brush from top of head to bottom\n"
            "3. Move brush from top of head to bottom\n"
            "4. Move brush from top of head to bottom\n"
            "5. Move brush from top of head to bottom\n"
            "6. Move brush from top of head to bottom\n"
            "7. Move brush from top of head to bottom\n"
            "8. Move brush from top of head to bottom\n"
            "9. Move brush from top of head to bottom\n"
            "10. Move brush from top of head to bottom\n\n"
            "Rewrite it as a SHORT loop, then write a second version: "
            "brush left side, brush right side, brush back \u2014 repeat 3 times."
        ),
        "min_steps": 2,
        "rules": [
            "Your loop version must produce the same output as the long version.",
            "Use LOOP ___ TIMES: to start your loop.",
            "Write the steps inside the loop.",
            "Then write a second, more complex loop with 3 sections.",
        ],
        "learning_styles": ["Read/Write", "Logical/Mathematical"],
        "research_basis": (
            "Recognising repetition and expressing it as a loop is one of the first "
            "abstraction skills children develop (Grover & Pea, 2013). Transforming "
            "long-form to loop notation follows Bruner\u2019s (1966) CPA model."
        ),
    },
    {
        "id": 2,
        "title": "Spot the Bug",
        "description": (
            "Analyse three buggy loops and write fixes: classroom movement, "
            "infinite sugar, and fridge resource leak."
        ),
        "type": "bug_hunt",
        "difficulty": "Medium",
        "duration_minutes": 7,
        "bugs": [
            {
                "label": "Bug 1 \u2014 Classroom Chaos",
                "code": "LOOP 5 TIMES:\n  Stand up\n  Sit down\n  Lie on the floor",
                "hint": "Is \u2018Lie on the floor\u2019 a valid step inside this loop?",
            },
            {
                "label": "Bug 2 \u2014 Infinite Sugar",
                "code": "LOOP FOREVER:\n  Add one sugar to the coffee\n  Stir",
                "hint": "When should this loop stop? Add a stop condition.",
            },
            {
                "label": "Bug 3 \u2014 Fridge Leak",
                "code": "LOOP 3 TIMES:\n  Open fridge\n  Take out juice\n  Pour glass",
                "hint": "What happens to the fridge door after each iteration?",
            },
        ],
        "learning_styles": ["Logical/Mathematical", "Kinaesthetic/Tactile", "Interpersonal"],
        "research_basis": (
            "Kapur (2008) shows that \u2018productive failure\u2019 \u2014 engaging with broken "
            "code before solutions \u2014 produces deeper learning. Debugging framed "
            "via Dweck\u2019s (2006) growth mindset: bugs are normal, fixing them is the skill."
        ),
    },
    {
        "id": 3,
        "title": "Write a Loop for Your Life",
        "description": (
            "Choose a repeated real-life activity and model it as a loop with "
            "type, stop condition, and one possible bug plus fix."
        ),
        "type": "written_extended",
        "difficulty": "Medium",
        "duration_minutes": 10,
        "fields": [
            {"name": "activity", "label": "What repeated activity did you choose?", "type": "text"},
            {"name": "loop_type", "label": "Loop type (count, until, or forever)?", "type": "text"},
            {"name": "steps", "label": "Write the steps inside your loop", "type": "steps"},
            {"name": "stop_condition", "label": "What stops the loop?", "type": "textarea"},
            {"name": "bug_and_fix", "label": "One possible bug and your fix", "type": "textarea"},
        ],
        "learning_styles": ["Read/Write", "Logical/Mathematical", "Intrapersonal"],
        "research_basis": (
            "Papert\u2019s (1980) constructionism: students choose personally meaningful "
            "activities and model them computationally. Low-floor/high-ceiling principle "
            "(Bers, 2018): basic count loop is accessible, nested loops extend advanced learners."
        ),
    },
]
