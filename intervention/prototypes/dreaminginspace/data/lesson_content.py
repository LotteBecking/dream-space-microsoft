"""Lesson 1 content: How Does a Computer Think? The PB&J Sandwich Algorithm."""

LESSON = {
    "id": "lesson-1",
    "title": "How Does a Computer Think? The PB&J Sandwich Lesson",
    "description": "Students discover that computers follow exact step-by-step instructions, and that sequence determines the result.",
    "duration": 60,
    "level": "Beginner",
    "age_group": "Ages 8-18",
    "color": "#7c3aed",
    "welcome": "Today we learn to think like Ada Lovelace, the world\u2019s first programmer!",
    "recap_msg": (
        "Computers follow instructions exactly \u2014 one step at a time, in order. "
        "If the steps are wrong or unclear, the output is wrong. That\u2019s why "
        "precision and sequence matter in every program!"
    ),
}

ROLE_MODEL = {
    "name": "Ada Lovelace",
    "years": "1815\u20131852",
    "intro": (
        "Ada Lovelace became the world\u2019s first programmer in 1843 by writing the first algorithm "
        "for the Analytical Engine, an early idea for a computer that could follow step-by-step "
        "instructions to solve math problems automatically."
    ),
    "detail": (
        "Ada wrote detailed instructions for how Charles Babbage\u2019s Analytical "
        "Engine could calculate a complex mathematical sequence called Bernoulli "
        "numbers. Those instructions, written in 1843, are considered the world\u2019s "
        "first computer program \u2014 for a machine that hadn\u2019t even been built yet!"
    ),
}

VOCABULARY = [
    {"word": "Algorithm", "definition": "A set of step-by-step instructions"},
    {"word": "Input", "definition": "What goes in (ingredients, data, commands)"},
    {"word": "Output", "definition": "What comes out (the sandwich, the result, the route)"},
    {"word": "Sequence", "definition": "The order of steps"},
]

LEARNING_OBJECTIVES = [
    "Explain in their own words that a computer follows instructions exactly, one step at a time.",
    "Describe why sequence matters by showing how changing the order changes the outcome.",
    "Use key vocabulary correctly: algorithm, input, output, and sequence.",
    "Debug unclear instructions by testing and improving a written algorithm.",
]

EXERCISES = [
    {
        "id": 1,
        "title": "Write the Perfect Algorithm",
        "description": (
            "Write a numbered algorithm (at least 6 steps, one action per step) "
            "for one task: getting ready for school, making chocolate milk, or feeding a pet."
        ),
        "type": "Written",
        "difficulty": "Easy",
        "xp": 10,
        "duration_minutes": 10,
        "task_options": [
            "Getting ready for school in the morning",
            "Making a glass of chocolate milk",
            "Feeding a pet",
        ],
        "rules": [
            "Each step must be numbered.",
            "Each step must be one action only.",
            "The algorithm must have at least 6 steps.",
            "A robot that cannot guess must be able to follow it.",
        ],
    },
    {
        "id": 2,
        "title": "Sequence Sorting: Make Tea",
        "description": (
            "Order six shuffled instruction cards into a logical sequence, "
            "compare with a partner, and discuss where sequence is fixed versus flexible."
        ),
        "type": "Sorting",
        "difficulty": "Easy",
        "xp": 15,
        "duration_minutes": 8,
    },
    {
        "id": 3,
        "title": "Extension: Robot Chef Algorithm",
        "description": (
            "Write a canteen robot algorithm for one lunch item, then extend it "
            "with allergy safety and missing-ingredient handling."
        ),
        "type": "Extension",
        "difficulty": "Medium",
        "xp": 20,
        "duration_minutes": 10,
        "rules": [
            "Choose one lunch item from the school canteen menu.",
            "Write a precise step-by-step algorithm a robot chef could follow.",
            "Add safety instructions for students with allergies.",
            "Add a rule for what the robot should do if an ingredient runs out.",
            "Challenge: make your algorithm work for any sandwich type.",
        ],
    },
]

TEA_STEPS_CORRECT = [
    "Boil the water",
    "Place the tea bag in the cup",
    "Pour the hot water into the cup",
    "Wait 3 minutes to steep",
    "Remove the tea bag",
    "Add milk or sugar if you like",
]

CHALLENGES = [
    {
        "id": "challenge-1-1",
        "title": "Allergy-Safe Robot Chef",
        "description": "Design a robot-chef algorithm that safely handles a food allergy without using common sense.",
        "difficulty": "Medium",
        "duration_minutes": 10,
        "instructions": [
            "Choose one canteen food item.",
            "Write a step-by-step robot algorithm for preparing it.",
            "Add explicit allergy checks before handling ingredients.",
            "Include safe fallback steps if risky ingredients appear.",
            "Test your algorithm by having another group try to follow it literally.",
        ],
    },
    {
        "id": "challenge-1-2",
        "title": "What If an Ingredient Runs Out?",
        "description": "Improve your algorithm with a decision path for missing ingredients during preparation.",
        "difficulty": "Medium",
        "duration_minutes": 8,
        "instructions": [
            "Take an algorithm you already wrote.",
            "Pick one ingredient that could run out halfway.",
            "Add precise steps for what the robot does next.",
            "Include at least one IF-style instruction in plain language.",
            "Run a peer test to see whether the updated logic works.",
        ],
    },
    {
        "id": "challenge-1-3",
        "title": "One Algorithm for Any Sandwich",
        "description": "Generalise from one sandwich to a reusable algorithm that works with different inputs.",
        "difficulty": "Hard",
        "duration_minutes": 10,
        "instructions": [
            "Rewrite your sandwich algorithm so it does not name specific spreads.",
            "Use placeholders like SPREAD A and SPREAD B.",
            "Define input choices at the top (bread type, spread 1, spread 2).",
            "Keep the action steps specific and in order.",
            "Test with two different ingredient combinations.",
        ],
    },
]

# ---------------------------------------------------------------------------
# Simulator data
# ---------------------------------------------------------------------------

INITIAL_SANDWICH_STATE = {
    "bread_bag": "closed",
    "bread_slices": 0,
    "pb_jar": "closed",
    "jam_jar": "closed",
    "pb_applied": False,
    "jam_applied": False,
    "sandwich_complete": False,
    "knife_location": "counter",
}

COMMAND_ALIASES = {
    "OPEN_BREAD_BAG": [
        "open bread bag", "open the bread", "open bag", "open bread",
        "tear the bag", "unseal", "open the bag",
    ],
    "TAKE_BREAD_SLICE": [
        "take bread", "take a slice", "get bread", "remove bread",
        "take out bread", "grab bread", "take slice", "take bread slice",
    ],
    "OPEN_PB_JAR": [
        "open peanut butter", "open pb", "open the peanut butter",
        "unscrew peanut butter", "open pb jar", "open peanut butter jar",
    ],
    "OPEN_JAM_JAR": [
        "open jam", "open the jam", "unscrew jam", "open jam jar",
    ],
    "GET_KNIFE": [
        "get knife", "pick up knife", "grab knife", "take knife",
        "take the knife", "get the knife", "pick knife",
    ],
    "APPLY_PB": [
        "spread peanut butter", "apply peanut butter", "spread pb",
        "put peanut butter on", "add peanut butter", "use peanut butter",
        "apply pb",
    ],
    "APPLY_JAM": [
        "spread jam", "apply jam", "put jam on", "add jam",
        "use jam", "spread the jam",
    ],
    "PLACE_SECOND_SLICE": [
        "place second slice", "put second slice", "close sandwich",
        "put bread on top", "add second slice", "place top slice",
        "top with bread",
    ],
    "SERVE": [
        "serve", "done", "finish", "complete", "plate it",
        "serve sandwich",
    ],
}

# ---------------------------------------------------------------------------
# Quiz
# ---------------------------------------------------------------------------

QUIZ_1 = [
    {
        "question": "What is an algorithm?",
        "options": [
            "A type of computer",
            "A set of step-by-step instructions to complete a task",
            "A kind of sandwich",
            "A programming language",
        ],
        "correct": 1,
    },
    {
        "question": "Why does the ORDER of instructions matter?",
        "options": [
            "It doesn\u2019t matter at all",
            "Because computers like things alphabetical",
            "Because changing the order changes the result",
            "Because code runs backwards",
        ],
        "correct": 2,
    },
    {
        "question": "What is the OUTPUT of a sandwich algorithm?",
        "options": [
            "The bread and ingredients",
            "The instructions you wrote",
            "The finished sandwich",
            "The knife",
        ],
        "correct": 2,
    },
    {
        "question": "A robot followed your instructions exactly but the sandwich is wrong. Whose fault is it?",
        "options": [
            "The robot\u2019s fault \u2014 it should have known better",
            "Nobody\u2019s fault",
            "The programmer\u2019s fault \u2014 the instructions were wrong",
            "The bread\u2019s fault",
        ],
        "correct": 2,
    },
]
