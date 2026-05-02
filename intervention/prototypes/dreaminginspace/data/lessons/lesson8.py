"""Lesson 8: The Cargo Hold , Lists & Collections.
Track 2: Text-Based Coding | Dreaming in Space.
"""

LESSON = {
    "id": "lesson-8",
    "title": "The Cargo Hold",
    "description": (
        "Learn that lists store multiple items in order \u2014 like a cargo "
        "manifest, a crew roster, or a mission log."
    ),
    "duration": 45,
    "level": "Beginner",
    "age_group": "Ages 8-18",
    "color": "#c026d3",
    "welcome": (
        "The ship\u2019s cargo hold has crates of supplies, crew names, "
        "and mission logs \u2014 they\u2019re all LISTS! Your Spotify "
        "playlist and Minecraft inventory work the same way. Today you\u2019ll "
        "learn how computers store collections and let you add, remove, "
        "and find things inside them."
    ),
    "recap_msg": (
        "Lists store multiple items in order. Each item has a position "
        "number (index, starting at 0). You can add, remove, and look up "
        "items. The ship\u2019s cargo hold is now perfectly organised!"
    ),
}

ROLE_MODEL = {
    "name": "Fei-Fei Li",
    "years": "1976\u2013present",
    "intro": "AI researcher who built ImageNet \u2014 a list of 14 million labelled images that changed how computers see.",
    "detail": (
        "Fei-Fei organised millions of photos into lists and categories "
        "so AI could learn to recognise objects. Without her massive list, "
        "modern AI image recognition wouldn\u2019t exist."
    ),
}

VOCABULARY = [
    {"word": "List", "definition": "An ordered collection of items stored together"},
    {"word": "Index", "definition": "The position number of an item in a list (starts at 0)"},
    {"word": "Append", "definition": "Add a new item to the end of a list"},
    {"word": "Remove", "definition": "Take an item out of a list"},
]

OBJECTIVES = [
    "Create a list and access items by their index number.",
    "Add and remove items from a list.",
    "Predict what a list contains after a series of operations.",
]

EXERCISES = [
    {
        "id": 1,
        "title": "Read the List",
        "type": "read_conditional",
        "difficulty": "Easy",
        "xp": 10,
        "description": "Look at each list and answer questions about what\u2019s inside.",
        "beaver_msg": "Lists are numbered starting from 0, not 1! That trips everyone up at first.",
        "beaver_hint": "Count from 0: the first item is index 0, the second is index 1, and so on.",
        "problems": [
            {
                "rule": "planets = [\"Mercury\", \"Venus\", \"Earth\", \"Mars\"]",
                "situation": "What is planets[2]?",
                "options": ["Mercury", "Venus", "Earth", "Mars"],
                "correct": 2,
            },
            {
                "rule": "snacks = [\"apple\", \"crisps\", \"cookie\", \"banana\"]",
                "situation": "What is snacks[0]?",
                "options": ["crisps", "apple", "cookie", "banana"],
                "correct": 1,
            },
            {
                "rule": "scores = [85, 92, 78, 95, 88]",
                "situation": "How many items are in this list?",
                "options": ["4", "5", "6", "95"],
                "correct": 1,
            },
            {
                "rule": "colours = [\"red\", \"blue\", \"green\"]\ncolours.append(\"yellow\")",
                "situation": "What does the list look like now?",
                "options": [
                    "[\"red\", \"blue\", \"green\"]",
                    "[\"yellow\", \"red\", \"blue\", \"green\"]",
                    "[\"red\", \"blue\", \"green\", \"yellow\"]",
                    "[\"red\", \"yellow\", \"green\"]"
                ],
                "correct": 2,
            },
        ],
    },
    {
        "id": 2,
        "title": "Build & Modify",
        "type": "robot_commands",
        "difficulty": "Medium",
        "xp": 15,
        "description": (
            "Create a shopping list, add items, remove one, and access "
            "a specific item by its index."
        ),
        "beaver_msg": "Think of it like a real shopping list \u2014 you can add items, cross them off, and check what\u2019s at position 3!",
        "beaver_hint": "Use .append(\"item\") to add, .remove(\"item\") to delete, and list[number] to access.",
        "command_set": [
            "my_list = [\"item1\", \"item2\"]",
            "my_list.append(\"new_item\")",
            "my_list.remove(\"item1\")",
            "print(my_list[0])",
        ],
        "scenarios": [
            {
                "label": "Create a playlist with 3 songs, add a 4th, then remove the 2nd one",
                "hint": "Start with playlist = [\"song1\", \"song2\", \"song3\"], then append and remove.",
            },
            {
                "label": "Create a high scores list [100, 85, 72], add score 95, then print the highest",
                "hint": "scores.append(95), then print(scores[0]) if sorted, or find the max.",
            },
        ],
        "min_steps": 4,
    },
    {
        "id": 3,
        "title": "List Detective",
        "type": "read_conditional",
        "difficulty": "Medium",
        "xp": 20,
        "description": "Trace through these programs and predict what the list contains at the end.",
        "beaver_msg": "Be a detective! Track every change to the list line by line.",
        "beaver_hint": "After each line, write down the full list. The final version is your answer.",
        "problems": [
            {
                "rule": "names = [\"Ali\", \"Bella\", \"Carlos\"]\nnames.append(\"Dina\")\nnames.remove(\"Bella\")",
                "situation": "What is the list now?",
                "options": [
                    "[\"Ali\", \"Carlos\", \"Dina\"]",
                    "[\"Ali\", \"Bella\", \"Carlos\", \"Dina\"]",
                    "[\"Dina\", \"Ali\", \"Carlos\"]",
                    "[\"Ali\", \"Carlos\"]"
                ],
                "correct": 0,
            },
            {
                "rule": "queue = [\"Emma\", \"Finn\", \"Grace\"]\nfirst = queue[0]\nqueue.remove(first)\nqueue.append(\"Hassan\")",
                "situation": "What is queue now?",
                "options": [
                    "[\"Finn\", \"Grace\", \"Hassan\"]",
                    "[\"Emma\", \"Finn\", \"Grace\", \"Hassan\"]",
                    "[\"Hassan\", \"Finn\", \"Grace\"]",
                    "[\"Finn\", \"Grace\"]"
                ],
                "correct": 0,
            },
            {
                "rule": "inventory = [\"sword\", \"shield\", \"potion\"]\ninventory[1] = \"magic staff\"\ninventory.append(\"potion\")",
                "situation": "What is inventory[1]?",
                "options": ["sword", "shield", "magic staff", "potion"],
                "correct": 2,
            },
        ],
    },
]

QUIZ = [
    {"question": "What index is the FIRST item in a list?", "options": ["1", "0", "-1", "First"], "correct": 1},
    {"question": "What does .append() do?", "options": ["Removes the last item", "Adds an item to the end", "Sorts the list", "Clears the list"], "correct": 1},
    {"question": "fruits = [\"apple\", \"banana\", \"cherry\"]. What is fruits[1]?", "options": ["apple", "banana", "cherry", "Error"], "correct": 1},
    {"question": "Why are lists useful?", "options": ["They store one item", "They store multiple items in order", "They only work with numbers", "They delete data"], "correct": 1},
]
