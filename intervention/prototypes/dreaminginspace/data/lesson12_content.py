"""Lesson 12: Data & Decisions.
Track 3: Creation & Application | Dreaming in Space.
"""

LESSON_12 = {
    "id": "lesson-12",
    "title": "Data & Decisions",
    "description": (
        "Learn how to collect, organise, and use data to make smart "
        "decisions \u2014 just like YouTube recommendations and weather apps."
    ),
    "duration": 45,
    "level": "Intermediate",
    "age_group": "Ages 8-18",
    "color": "#0891b2",
    "welcome": (
        "Ever wondered how YouTube knows what video to suggest next? Or "
        "how a weather app predicts rain? They use DATA! Today you\u2019ll "
        "collect data, turn it into charts, and make decisions based on "
        "what the numbers tell you."
    ),
    "recap_msg": (
        "Data helps you make smarter decisions instead of just guessing. "
        "Collect it, organise it, look for patterns, and let the evidence "
        "guide your choices. You\u2019re a data-driven decision maker!"
    ),
}

ROLE_MODEL_12 = {
    "name": "Florence Nightingale",
    "years": "1820\u20131910",
    "intro": "Used data visualisation to save lives \u2014 her charts convinced the government to improve hospital conditions.",
    "detail": (
        "Florence collected data on how soldiers were dying and created "
        "innovative charts called polar area diagrams to show that most "
        "deaths were from infections, not wounds. Her data changed "
        "healthcare forever."
    ),
}

VOCABULARY_12 = [
    {"word": "Data", "definition": "Facts, numbers, or text that can be collected and analysed"},
    {"word": "Dataset", "definition": "A structured collection of related data"},
    {"word": "Chart", "definition": "A visual way to show data (bar chart, pie chart, line graph)"},
    {"word": "Trend", "definition": "A general direction that data is moving over time"},
]

OBJECTIVES_12 = [
    "Read data from a chart and answer questions about it.",
    "Collect and organise data into a simple table.",
    "Make a recommendation based on evidence from data.",
]

EXERCISES_12 = [
    {
        "id": 1,
        "title": "Read the Data",
        "type": "read_conditional",
        "difficulty": "Easy",
        "xp": 10,
        "description": "Look at the data and answer questions about what it shows.",
        "beaver_msg": "Data tells a story if you know how to read it. Let\u2019s find out what the numbers say!",
        "beaver_hint": "Look for the biggest, smallest, and any patterns. Compare the numbers.",
        "problems": [
            {
                "rule": "School Lunch Survey:\nPizza: 45 votes\nPasta: 30 votes\nSandwich: 15 votes\nSalad: 10 votes",
                "situation": "Which lunch is most popular?",
                "options": ["Pasta", "Pizza", "Sandwich", "Salad"],
                "correct": 1,
            },
            {
                "rule": "Daily Steps (Mon-Fri):\nMon: 8,000\nTue: 6,500\nWed: 9,200\nThu: 7,100\nFri: 4,300",
                "situation": "On which day were the most steps taken?",
                "options": ["Monday", "Tuesday", "Wednesday", "Friday"],
                "correct": 2,
            },
            {
                "rule": "App Downloads This Week:\nMon: 100\nTue: 150\nWed: 200\nThu: 250\nFri: 300",
                "situation": "What\u2019s the trend?",
                "options": ["Downloads are decreasing", "Downloads are staying the same", "Downloads are increasing by ~50 per day", "No pattern"],
                "correct": 2,
            },
        ],
    },
    {
        "id": 2,
        "title": "Collect & Organise",
        "type": "robot_commands",
        "difficulty": "Medium",
        "xp": 15,
        "description": (
            "You\u2019ve been asked to find out what drink the class prefers "
            "for a school event. Design a survey, record the results, and "
            "write a recommendation."
        ),
        "beaver_msg": "Good data starts with a good question! What do you want to find out?",
        "beaver_hint": "Step 1: Write the question. Step 2: List the options. Step 3: Record the counts. Step 4: Recommend the winner.",
        "command_set": [
            "Survey question:",
            "Options: A, B, C, D",
            "Results: A=?, B=?, C=?, D=?",
            "Recommendation: Based on the data...",
        ],
        "scenarios": [
            {"label": "Design a drink survey for a school event", "hint": "e.g. Water: 12, Juice: 18, Milk: 6, Smoothie: 9 \u2192 \u201cBuy mostly juice\u201d"},
            {"label": "Design a survey to decide which game to play at the party", "hint": "List 4 games, make up realistic votes, recommend based on data"},
        ],
        "min_steps": 4,
    },
    {
        "id": 3,
        "title": "Data-Driven Decision",
        "type": "robot_commands",
        "difficulty": "Hard",
        "xp": 20,
        "description": (
            "The school wants to reduce energy use. You have data on "
            "electricity usage per month. Analyse it and write 3 "
            "recommendations backed by evidence."
        ),
        "beaver_msg": "This is what real data scientists do \u2014 find the story in the numbers and make smart recommendations!",
        "beaver_hint": "Find the month with highest usage, identify the trend, and suggest WHY it might be happening and what to do.",
        "command_set": [
            "Highest month and why:",
            "Trend I noticed:",
            "Recommendation 1:",
            "Recommendation 2:",
            "Recommendation 3:",
        ],
        "scenarios": [
            {
                "label": "Monthly electricity (kWh): Sep=500, Oct=600, Nov=800, Dec=1000, Jan=1100, Feb=900, Mar=700",
                "hint": "Usage peaks in winter. Recommend: better insulation, turn off lights, use timers for heating.",
            },
        ],
        "min_steps": 5,
    },
]

QUIZ_12 = [
    {"question": "What is a trend in data?", "options": ["A popular fashion", "A general direction data is moving", "A type of chart", "An error"], "correct": 1},
    {"question": "Pizza: 40, Pasta: 25, Salad: 10. What should the canteen order most of?", "options": ["Salad", "Pasta", "Pizza", "All equal"], "correct": 2},
    {"question": "Why is data useful for making decisions?", "options": ["It looks nice", "It gives evidence so you\u2019re not just guessing", "It\u2019s required by law", "It isn\u2019t useful"], "correct": 1},
    {"question": "Who used data charts to improve hospitals?", "options": ["Ada Lovelace", "Florence Nightingale", "Grace Hopper", "Tim Berners-Lee"], "correct": 1},
]
