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
        "title": "Sequence Sorting: Make Tea",
        "description": (
            "These six steps for making tea got mixed up! "
            "Drag them into the right order. Think about which step "
            "has to come before the next one."
        ),
        "type": "Sorting",
        "difficulty": "Easy",
        "xp": 15,
        "duration_minutes": 8,
    },
    {
        "id": 2,
        "title": "Write the Perfect Algorithm",
        "description": (
            "Write a numbered algorithm (at least 6 steps, one action per step) "
            "for one task: getting ready for school, making chocolate milk, or feeding a pet."
        ),
        "type": "Written",
        "difficulty": "Medium",
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
        "id": 3,
        "title": "Robot Chef Challenge",
        "description": (
            "Write an algorithm for a robot chef in the school canteen. "
            "Your goal: make it so precise that a robot with NO common sense "
            "can follow it perfectly — and handle allergies and missing ingredients too!"
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

# Steps 5 and 6 can be swapped — both are valid
TEA_STEPS_ALT = [
    "Boil the water",
    "Place the tea bag in the cup",
    "Pour the hot water into the cup",
    "Wait 3 minutes to steep",
    "Add milk or sugar if you like",
    "Remove the tea bag",
]

# ---------------------------------------------------------------------------
# Exercise 2: Pre-made action blocks per task (for the block builder)
# ---------------------------------------------------------------------------
TASK_BLOCKS = [
    # Task 0: Getting ready for school
    [
        {"emoji": "\U0001f514", "text": "Wake up when the alarm rings"},
        {"emoji": "\U0001f6cf\ufe0f", "text": "Get out of bed"},
        {"emoji": "\U0001f6bf", "text": "Take a shower"},
        {"emoji": "\U0001faa5", "text": "Brush your teeth"},
        {"emoji": "\U0001f9f4", "text": "Wash your face"},
        {"emoji": "\U0001f455", "text": "Put on your school uniform"},
        {"emoji": "\U0001f9e6", "text": "Put on your socks"},
        {"emoji": "\U0001f45f", "text": "Put on your shoes"},
        {"emoji": "\U0001f963", "text": "Pour cereal into a bowl"},
        {"emoji": "\U0001f95b", "text": "Pour milk into the bowl"},
        {"emoji": "\U0001f944", "text": "Eat your breakfast"},
        {"emoji": "\U0001f392", "text": "Pack your school bag"},
        {"emoji": "\U0001f4da", "text": "Check you have all your books"},
        {"emoji": "\U0001f9e5", "text": "Put on your coat"},
        {"emoji": "\U0001f6aa", "text": "Open the front door"},
        {"emoji": "\U0001f6b6", "text": "Walk to school"},
    ],
    # Task 1: Making chocolate milk
    [
        {"emoji": "\U0001f95b", "text": "Get a clean glass from the cupboard"},
        {"emoji": "\U0001f4e6", "text": "Open the fridge door"},
        {"emoji": "\U0001f95b", "text": "Take out the milk carton"},
        {"emoji": "\U0001f6aa", "text": "Close the fridge door"},
        {"emoji": "\U0001f36b", "text": "Get the chocolate powder from the shelf"},
        {"emoji": "\U0001f513", "text": "Open the chocolate powder lid"},
        {"emoji": "\U0001f95b", "text": "Pour milk into the glass"},
        {"emoji": "\U0001f944", "text": "Get a spoon from the drawer"},
        {"emoji": "\U0001f36b", "text": "Add 2 spoons of chocolate powder"},
        {"emoji": "\U0001f504", "text": "Stir with the spoon until mixed"},
        {"emoji": "\U0001f445", "text": "Taste the chocolate milk"},
        {"emoji": "\U0001f9f9", "text": "Wipe the counter clean"},
        {"emoji": "\U0001f4e6", "text": "Put the milk back in the fridge"},
        {"emoji": "\U0001f512", "text": "Close the chocolate powder lid"},
    ],
    # Task 2: Feeding a pet
    [
        {"emoji": "\U0001f550", "text": "Check the clock \u2014 is it feeding time?"},
        {"emoji": "\U0001f963", "text": "Get the food bowl from the floor"},
        {"emoji": "\U0001f6b0", "text": "Wash the food bowl with water"},
        {"emoji": "\U0001f4e6", "text": "Open the pet food bag"},
        {"emoji": "\U0001f944", "text": "Scoop one cup of food into the bowl"},
        {"emoji": "\U0001f963", "text": "Place the food bowl on the floor"},
        {"emoji": "\U0001f4a7", "text": "Check if the water bowl is empty"},
        {"emoji": "\U0001f6b0", "text": "Fill the water bowl with fresh water"},
        {"emoji": "\U0001f415", "text": "Call your pet to come and eat"},
        {"emoji": "\U0001f440", "text": "Watch your pet eat"},
        {"emoji": "\U0001f9f9", "text": "Clean up any spills on the floor"},
        {"emoji": "\U0001f4e6", "text": "Close and seal the pet food bag"},
        {"emoji": "\U0001f963", "text": "Pick up the empty food bowl"},
        {"emoji": "\U0001f6b0", "text": "Wash the food bowl for next time"},
    ],
]

# ---------------------------------------------------------------------------
# Exercise 3: Robot Chef data (lunch items, cooking blocks, IF/THEN pieces)
# ---------------------------------------------------------------------------
CHEF_LUNCH_ITEMS = [
    {"emoji": "\U0001f354", "name": "Burger", "color": "#fef3c7"},
    {"emoji": "\U0001f355", "name": "Pizza", "color": "#fce7f3"},
    {"emoji": "\U0001f32e", "name": "Tacos", "color": "#dbeafe"},
    {"emoji": "\U0001f95e", "name": "Pancakes", "color": "#fef2f2"},
]

CHEF_BLOCKS = [
    # Item 0: Burger
    [
        {"emoji": "\U0001f6bf", "text": "Wash hands with soap and water"},
        {"emoji": "\U0001f35e", "text": "Take a burger bun from the bag"},
        {"emoji": "\U0001f52a", "text": "Cut the bun in half"},
        {"emoji": "\U0001f7e1", "text": "Place the bottom bun on the plate"},
        {"emoji": "\U0001f356", "text": "Take a burger patty from the fridge"},
        {"emoji": "\U0001f525", "text": "Turn on the grill to medium heat"},
        {"emoji": "\U0001f356", "text": "Place the patty on the grill"},
        {"emoji": "\u23f3", "text": "Cook for 4 minutes on each side"},
        {"emoji": "\U0001f356", "text": "Place the cooked patty on the bun"},
        {"emoji": "\U0001f9c0", "text": "Add a slice of cheese on the patty"},
        {"emoji": "\U0001f345", "text": "Wash and slice a tomato"},
        {"emoji": "\U0001f345", "text": "Place a tomato slice on the cheese"},
        {"emoji": "\U0001f96c", "text": "Add a lettuce leaf on top"},
        {"emoji": "\U0001f35e", "text": "Place the top bun on the burger"},
        {"emoji": "\U0001f37d\ufe0f", "text": "Place burger on the serving tray"},
    ],
    # Item 1: Pizza
    [
        {"emoji": "\U0001f6bf", "text": "Wash hands with soap and water"},
        {"emoji": "\U0001f355", "text": "Take a pizza base from the fridge"},
        {"emoji": "\U0001f37d\ufe0f", "text": "Place the base on a baking tray"},
        {"emoji": "\U0001f345", "text": "Open the jar of tomato sauce"},
        {"emoji": "\U0001f944", "text": "Spread tomato sauce on the base"},
        {"emoji": "\U0001f9c0", "text": "Sprinkle grated cheese on top"},
        {"emoji": "\U0001f336\ufe0f", "text": "Add sliced peppers on the cheese"},
        {"emoji": "\U0001f33d", "text": "Add sweetcorn on top"},
        {"emoji": "\U0001f525", "text": "Turn on the oven to 200\u00b0C"},
        {"emoji": "\u23f3", "text": "Wait for the oven to heat up"},
        {"emoji": "\U0001f525", "text": "Put the tray in the oven"},
        {"emoji": "\u23f3", "text": "Bake for 12 minutes until golden"},
        {"emoji": "\U0001f9f4", "text": "Use oven gloves to take tray out"},
        {"emoji": "\U0001f52a", "text": "Cut the pizza into slices"},
        {"emoji": "\U0001f37d\ufe0f", "text": "Place pizza on the serving tray"},
    ],
    # Item 2: Tacos
    [
        {"emoji": "\U0001f6bf", "text": "Wash hands with soap and water"},
        {"emoji": "\U0001f356", "text": "Take the mince meat from the fridge"},
        {"emoji": "\U0001f525", "text": "Turn on the stove to medium heat"},
        {"emoji": "\U0001f373", "text": "Put a frying pan on the stove"},
        {"emoji": "\U0001f356", "text": "Add the mince to the pan"},
        {"emoji": "\U0001f944", "text": "Stir the mince until cooked"},
        {"emoji": "\U0001f9c2", "text": "Add taco seasoning and mix"},
        {"emoji": "\U0001f32e", "text": "Take taco shells from the box"},
        {"emoji": "\U0001f32e", "text": "Place shells on the plate"},
        {"emoji": "\U0001f944", "text": "Spoon the mince into each shell"},
        {"emoji": "\U0001f9c0", "text": "Sprinkle grated cheese on top"},
        {"emoji": "\U0001f96c", "text": "Add shredded lettuce"},
        {"emoji": "\U0001f345", "text": "Add diced tomatoes"},
        {"emoji": "\U0001f37d\ufe0f", "text": "Place tacos on the serving tray"},
        {"emoji": "\U0001f9f9", "text": "Wipe the counter clean"},
    ],
    # Item 3: Pancakes
    [
        {"emoji": "\U0001f6bf", "text": "Wash hands with soap and water"},
        {"emoji": "\U0001f963", "text": "Get a mixing bowl from the shelf"},
        {"emoji": "\U0001f95a", "text": "Crack two eggs into the bowl"},
        {"emoji": "\U0001f95b", "text": "Pour milk into the bowl"},
        {"emoji": "\U0001f33e", "text": "Add flour to the bowl"},
        {"emoji": "\U0001f944", "text": "Whisk until the batter is smooth"},
        {"emoji": "\U0001f525", "text": "Turn on the stove to medium heat"},
        {"emoji": "\U0001f373", "text": "Put a frying pan on the stove"},
        {"emoji": "\U0001f9c8", "text": "Add a little butter to the pan"},
        {"emoji": "\U0001f95e", "text": "Pour batter into the pan"},
        {"emoji": "\u23f3", "text": "Cook for 2 minutes until bubbles form"},
        {"emoji": "\U0001f95e", "text": "Flip the pancake over"},
        {"emoji": "\u23f3", "text": "Cook for 1 more minute"},
        {"emoji": "\U0001f95e", "text": "Slide pancake onto the plate"},
        {"emoji": "\U0001f37d\ufe0f", "text": "Add toppings and serve"},
    ],
]

CHEF_IF_CONDITIONS = [
    {"emoji": "\U0001f95c", "text": "student has a nut allergy"},
    {"emoji": "\U0001f9c0", "text": "student is allergic to dairy (milk, cheese)"},
    {"emoji": "\U0001f33e", "text": "student is allergic to gluten (bread, flour)"},
    {"emoji": "\U0001f95a", "text": "student is allergic to eggs"},
    {"emoji": "\U0001f346", "text": "student is vegetarian (no meat)"},
]

CHEF_THEN_ACTIONS = [
    {"emoji": "\U0001f6ab", "text": "skip that ingredient completely"},
    {"emoji": "\U0001f504", "text": "swap it for a safe ingredient instead"},
    {"emoji": "\u2705", "text": "check the allergy list on the wall first"},
    {"emoji": "\U0001f4e2", "text": "tell the teacher before cooking"},
    {"emoji": "\U0001f6d1", "text": "stop and ask what they can eat"},
    {"emoji": "\U0001f504", "text": "make a different dish instead"},
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
        "place bread on plate", "put bread on plate", "place bread slice",
        "place first slice", "put first slice",
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
