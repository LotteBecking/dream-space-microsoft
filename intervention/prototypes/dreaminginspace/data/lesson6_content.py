"""Lesson 6: Variable Vaults — Storing Information.
Track 2: Text-Based Coding | Dreaming in Space.
"""

LESSON_6 = {
    "id": "lesson-6",
    "title": "Variable Vaults",
    "description": (
        "Learn that variables are like labelled boxes that store data. "
        "Create them, change them, and predict what happens."
    ),
    "duration": 45,
    "level": "Beginner",
    "age_group": "Ages 8-18",
    "color": "#2563eb",
    "welcome": (
        "Let\u2019s talk about \u2018Variables.\u2019 Think of them as "
        "labelled boxes where we store information we might need later "
        "\u2014 like our fuel levels, oxygen supply, or how many Space "
        "Crystals we\u2019ve collected! Without variables, the ship would "
        "have total amnesia."
    ),
    "recap_msg": (
        "Variables keep our data organised. You can read them, change "
        "them, and use them in calculations. Without them, the ship "
        "would forget everything! Every program starts here."
    ),
}

ROLE_MODEL_6 = {
    "name": "Tim Berners-Lee",
    "years": "1955\u2013present",
    "intro": "Inventor of the World Wide Web \u2014 every website you visit uses variables to remember who you are.",
    "detail": (
        "When you log into a website, your username is stored in a variable. "
        "Tim built the system that makes this possible for billions of people."
    ),
}

VOCABULARY_6 = [
    {"word": "Variable", "definition": "A named container that stores a piece of data"},
    {"word": "Value", "definition": "The data stored inside a variable (a number, text, etc.)"},
    {"word": "Assign", "definition": "Put a value into a variable using = "},
    {"word": "Update", "definition": "Change the value stored in a variable"},
]

OBJECTIVES_6 = [
    "Explain what a variable is using a real-world analogy.",
    "Create variables and assign values to them.",
    "Predict what a variable contains after a series of changes.",
]

EXERCISES_6 = [
    {
        "id": 1,
        "title": "Label Logic",
        "type": "read_conditional",
        "difficulty": "Easy",
        "xp": 10,
        "description": "Read the ship\u2019s code and predict what each variable vault contains.",
        "beaver_msg": "We need to store the ship\u2019s current speed. Which box label makes the most sense so we don\u2019t get confused later?",
        "beaver_hint": "Read each line top to bottom. When you see = it means \u2018put this value in the vault.\u2019",
        "problems": [
            {
                "rule": "fuel_level = 50\noxygen = 98\nship_speed = 300",
                "situation": "We found a fuel tank! What should fuel_level be after fuel_level = fuel_level + 20?",
                "options": ["50", "20", "70", "Error"],
                "correct": 2,
            },
            {
                "rule": "crystals = 0\ncrystals = crystals + 1\ncrystals = crystals + 1\ncrystals = crystals + 1",
                "situation": "How many Space Crystals do we have?",
                "options": ["0", "1", "3", "4"],
                "correct": 2,
            },
            {
                "rule": "captain_name = \"Space Beaver\"\ncrew_size = 4\nmission = \"Explore Nebula\"",
                "situation": "Which variable stores the number of crew members?",
                "options": ["captain_name", "crew_size", "mission", "4"],
                "correct": 1,
            },
            {
                "rule": "greeting = \"Hello\"\nplanet = \"Mars\"\nmessage = greeting + \" from \" + planet",
                "situation": "What does \u2018message\u2019 contain?",
                "options": ["Hello", "Mars", "Hello from Mars", "greeting planet"],
                "correct": 2,
            },
        ],
    },
    {
        "id": 2,
        "title": "The Data Update",
        "type": "robot_commands",
        "difficulty": "Medium",
        "xp": 15,
        "description": (
            "The ship\u2019s systems need updating! Create variables to track "
            "fuel, oxygen, crystals, and crew \u2014 then update them as events happen."
        ),
        "beaver_msg": "We just found a fuel tank! Drag the +20 block to the variable to update our total. Refuelled and ready!",
        "beaver_hint": "Write one variable per line like: fuel_level = 50",
        "command_set": [
            "fuel_level = 50",
            "oxygen = 100",
            "crystals = 0",
            "crew = 4",
            "ship_speed = 200",
        ],
        "scenarios": [
            {
                "label": "Set up the ship: fuel (50), oxygen (100), crystals (0), speed (200)",
                "hint": "Use = to assign each value. Numbers don\u2019t need quotes.",
            },
            {
                "label": "Asteroid hit! Fuel drops by 15, we find 3 crystals, one crew member is rescued (+1)",
                "hint": "fuel_level = fuel_level - 15, crystals = crystals + 3, crew = crew + 1",
            },
        ],
        "min_steps": 4,
    },
    {
        "id": 3,
        "title": "The Scorekeeper",
        "type": "read_conditional",
        "difficulty": "Medium",
        "xp": 20,
        "description": "Trace through these ship programs and predict what the variables contain at the end.",
        "beaver_msg": "Be a detective! Track every change to the vault line by line.",
        "beaver_hint": "Write down each variable\u2019s value after every line. The last value wins.",
        "problems": [
            {
                "rule": "shields = 100\ndamage = 35\nshields = shields - damage\nrepair = 10\nshields = shields + repair",
                "situation": "What is \u2018shields\u2019 now?",
                "options": ["100", "65", "75", "35"],
                "correct": 2,
            },
            {
                "rule": "distance = 1000\nspeed = 50\ntime = distance / speed",
                "situation": "What is \u2018time\u2019?",
                "options": ["1000", "50", "20", "50000"],
                "correct": 2,
            },
            {
                "rule": "price = 10\ndiscount = 3\nfinal_price = price - discount\nprice = 20",
                "situation": "What is \u2018final_price\u2019?",
                "options": ["7", "17", "20", "10"],
                "correct": 0,
            },
        ],
    },
]

QUIZ_6 = [
    {"question": "What is a variable?", "options": ["A type of loop", "A named container that stores data", "A kind of robot", "A website"], "correct": 1},
    {"question": "What does score = score + 10 do?", "options": ["Creates a new variable called 10", "Adds 10 to whatever score currently is", "Deletes the score", "Nothing"], "correct": 1},
    {"question": "name = \"Alex\". What type of data is stored?", "options": ["A number", "A boolean", "Text (a string)", "A list"], "correct": 2},
    {"question": "x = 5, then x = 8. What is x?", "options": ["5", "8", "13", "Error"], "correct": 1},
]
