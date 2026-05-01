"""Lesson 10: Build a Simple Game.
Track 3: Creation & Application | Dreaming in Space.
"""

LESSON = {
    "id": "lesson-10",
    "title": "Build a Simple Game",
    "description": (
        "Combine everything you\u2019ve learned \u2014 variables, loops, "
        "conditionals, functions \u2014 to design and build a simple game."
    ),
    "duration": 50,
    "level": "Intermediate",
    "age_group": "Ages 8-18",
    "color": "#059669",
    "welcome": (
        "You\u2019ve learned algorithms, loops, conditionals, variables, "
        "functions, lists, and debugging. Now let\u2019s put it ALL together "
        "and build a GAME! It won\u2019t be Fortnite, but it\u2019ll be YOURS."
    ),
    "recap_msg": (
        "You just designed a game! Every game is made of the same building "
        "blocks: variables for data, loops for repetition, conditionals for "
        "decisions, and functions for organisation. You\u2019re a game designer!"
    ),
}

ROLE_MODEL = {
    "name": "Roberta Williams",
    "years": "1953\u2013present",
    "intro": "Pioneer of graphic adventure games \u2014 she created King\u2019s Quest, one of the first story-driven computer games.",
    "detail": (
        "Roberta proved that games could tell stories and be creative, not just "
        "about high scores. She designed game logic with variables, conditionals, "
        "and puzzles \u2014 the same building blocks you\u2019ve been learning."
    ),
}

VOCABULARY = [
    {"word": "Game Loop", "definition": "The main loop that runs every frame: check input, update state, draw screen"},
    {"word": "State", "definition": "All the current data in your game (score, position, health, etc.)"},
    {"word": "Event", "definition": "Something that happens (a key press, a collision, a timer)"},
    {"word": "Win Condition", "definition": "The rule that decides when the player wins"},
]

OBJECTIVES = [
    "Design a game by identifying the variables, loops, and conditionals needed.",
    "Implement a basic game loop with scoring and win/lose conditions.",
    "Add a new feature to an existing game and test it.",
]

EXERCISES = [
    {
        "id": 1,
        "title": "Design the Rules",
        "type": "robot_commands",
        "difficulty": "Easy",
        "xp": 10,
        "description": (
            "Before coding, every game needs a DESIGN. Pick a game concept "
            "and list: what variables do you need? What loops run? What "
            "conditionals trigger events?"
        ),
        "beaver_msg": "Every great game starts with a plan! Think about what data your game needs to track.",
        "beaver_hint": "Think: score (variable), game loop (repeat), collision check (conditional), game over (function).",
        "command_set": ["Variables needed:", "Loops needed:", "Conditionals needed:", "Win condition:"],
        "scenarios": [
            {"label": "Coin Collector \u2014 player moves, collects coins, avoids enemies", "hint": "score, player_x, player_y, coins_left, game_over"},
            {"label": "Quiz Show \u2014 answer questions, earn points, 3 lives", "hint": "score, lives, question_number, time_remaining"},
        ],
        "min_steps": 5,
    },
    {
        "id": 2,
        "title": "Build the Core",
        "type": "robot_commands",
        "difficulty": "Medium",
        "xp": 20,
        "description": (
            "Write the pseudocode for your game\u2019s core loop. Include: "
            "player action, score update, and a win/lose check."
        ),
        "beaver_msg": "Now turn your design into code! Write the game loop step by step.",
        "beaver_hint": "LOOP FOREVER: get input, update position, check collisions, update score, check win/lose, draw screen.",
        "command_set": [
            "LOOP FOREVER:",
            "  get player input",
            "  update position",
            "  IF player touches coin: score = score + 1",
            "  IF score >= 10: print(\"You win!\")",
            "  IF lives <= 0: print(\"Game over!\")",
        ],
        "scenarios": [
            {"label": "Write the complete game loop for your chosen game", "hint": "Start with LOOP FOREVER: then handle input, update, check, and draw."},
        ],
        "min_steps": 6,
    },
    {
        "id": 3,
        "title": "Add a Feature",
        "type": "robot_commands",
        "difficulty": "Medium",
        "xp": 25,
        "description": (
            "Your basic game works! Now add ONE new feature: a timer, "
            "a power-up, a new enemy type, or a difficulty level."
        ),
        "beaver_msg": "Game designers always add features after the core works. Pick ONE and make it great!",
        "beaver_hint": "Pick ONE feature. Write what variables it needs, what conditional triggers it, and how it changes the game.",
        "command_set": ["New feature name:", "New variables needed:", "New conditionals:", "How it changes gameplay:"],
        "scenarios": [
            {"label": "Add a speed power-up that makes the player move 2x faster for 5 seconds", "hint": "speed_boost = True, boost_timer = 5, IF boost_timer > 0: speed = speed * 2"},
            {"label": "Add a timer that ends the game after 60 seconds", "hint": "time_left = 60, every second: time_left = time_left - 1, IF time_left <= 0: game over"},
        ],
        "min_steps": 4,
    },
]

QUIZ = [
    {"question": "What is a game loop?", "options": ["A loop that plays music", "The main loop that runs every frame of the game", "A type of controller", "A cheat code"], "correct": 1},
    {"question": "What type of data does \u2018score = 0\u2019 create?", "options": ["A function", "A loop", "A variable", "A conditional"], "correct": 2},
    {"question": "IF player touches enemy THEN lose a life. What is this?", "options": ["A loop", "A variable", "A function", "A conditional"], "correct": 3},
    {"question": "Why should you design before you code?", "options": ["It\u2019s a waste of time", "So you know what variables, loops, and rules you need", "Computers require it", "It\u2019s optional"], "correct": 1},
]
