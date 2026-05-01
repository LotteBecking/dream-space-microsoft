"""Lesson 16: Data All Around Us.
Track 4: Digital World | Dreaming in Space.
"""

LESSON = {
    "id": "lesson-16",
    "title": "Data All Around Us",
    "description": (
        "Learn to collect real-world data, represent it visually, spot "
        "trends, and communicate what the data is telling you."
    ),
    "duration": 45,
    "level": "Beginner",
    "age_group": "Ages 8-18",
    "color": "#0d9488",
    "welcome": (
        "Data is EVERYWHERE \u2014 the weather forecast, your step count, "
        "how many goals your team scored, the number of likes on a post. "
        "Today you\u2019ll become a data storyteller \u2014 someone who can "
        "look at numbers and find the story hiding inside!"
    ),
    "recap_msg": (
        "Data is just numbers until you organise it. Charts show patterns. "
        "Patterns tell stories. Stories drive decisions. You\u2019re now a "
        "data storyteller \u2014 the final lesson is COMPLETE!"
    ),
}

ROLE_MODEL = {
    "name": "Hans Rosling",
    "years": "1948\u20132017",
    "intro": "Made data come alive \u2014 his animated bubble charts showed the world how countries are really developing.",
    "detail": (
        "Hans believed that data should be fun and accessible to everyone. "
        "His presentations used simple charts to bust myths and change how "
        "millions of people understand the world."
    ),
}

VOCABULARY = [
    {"word": "Bar Chart", "definition": "Shows quantities as horizontal or vertical bars \u2014 great for comparing categories"},
    {"word": "Line Graph", "definition": "Shows how data changes over time with a connected line"},
    {"word": "Pie Chart", "definition": "Shows proportions as slices of a circle \u2014 must add up to 100%"},
    {"word": "Outlier", "definition": "A data point that\u2019s very different from the rest \u2014 worth investigating"},
]

OBJECTIVES = [
    "Read and interpret 3 types of charts (bar, line, pie).",
    "Collect data and choose the right chart type to represent it.",
    "Write 3 sentences describing what data shows, including a surprising finding.",
]

EXERCISES = [
    {
        "id": 1,
        "title": "Read the Chart",
        "type": "read_conditional",
        "difficulty": "Easy",
        "xp": 10,
        "description": "Look at each chart description and answer questions about what the data shows.",
        "beaver_msg": "Charts are pictures of data. Learn to read them and you can understand the world!",
        "beaver_hint": "Look at the title, the labels, the highest and lowest values, and any trends.",
        "problems": [
            {
                "rule": "BAR CHART \u2014 Favourite Sport:\nFootball: 35 students\nBasketball: 20 students\nSwimming: 15 students\nTennis: 10 students\nOther: 5 students",
                "situation": "How many more students chose football than basketball?",
                "options": ["10", "15", "20", "35"],
                "correct": 1,
            },
            {
                "rule": "LINE GRAPH \u2014 Temperature This Week:\nMon: 14\u00b0C, Tue: 16\u00b0C, Wed: 18\u00b0C, Thu: 15\u00b0C, Fri: 11\u00b0C",
                "situation": "On which day did the temperature drop the most?",
                "options": ["Tuesday to Wednesday", "Wednesday to Thursday", "Thursday to Friday", "Monday to Tuesday"],
                "correct": 2,
            },
            {
                "rule": "PIE CHART \u2014 How Students Get to School:\nWalk: 40%\nBike: 25%\nBus: 20%\nCar: 15%",
                "situation": "What percentage of students do NOT walk?",
                "options": ["40%", "60%", "25%", "75%"],
                "correct": 1,
            },
            {
                "rule": "BAR CHART \u2014 Books Read Per Month:\nJan: 2, Feb: 3, Mar: 2, Apr: 8, May: 3, Jun: 2",
                "situation": "April has 8 books while other months have 2-3. What is April?",
                "options": ["A trend", "The average", "An outlier \u2014 much higher than the rest", "Normal"],
                "correct": 2,
            },
        ],
    },
    {
        "id": 2,
        "title": "Collect & Visualise",
        "type": "robot_commands",
        "difficulty": "Medium",
        "xp": 15,
        "description": (
            "Design a mini data collection activity, make up realistic "
            "results, and choose the best chart type to show them."
        ),
        "beaver_msg": "You\u2019re a data scientist now! Collect, organise, and visualise.",
        "beaver_hint": "Step 1: What question? Step 2: What data? Step 3: Which chart type? Step 4: What does it show?",
        "command_set": [
            "My question:",
            "Data I collected:",
            "Chart type I\u2019d use (bar/line/pie) and why:",
            "One thing the data shows:",
        ],
        "scenarios": [
            {"label": "Survey: What\u2019s the most popular app in your class?", "hint": "e.g. TikTok: 12, YouTube: 8, Instagram: 5, WhatsApp: 10. Use a bar chart to compare."},
            {"label": "Track: How does your screen time change across a week?", "hint": "Mon-Sun hours. Use a line graph to show the trend. Weekend vs. weekday pattern?"},
        ],
        "min_steps": 4,
    },
    {
        "id": 3,
        "title": "Tell the Story",
        "type": "robot_commands",
        "difficulty": "Medium",
        "xp": 20,
        "description": (
            "Given a dataset, write 3 sentences: what the data shows, "
            "one surprising finding, and one action based on the data."
        ),
        "beaver_msg": "Data without a story is just numbers. Your job is to find the story and tell it clearly!",
        "beaver_hint": "Sentence 1: The main trend. Sentence 2: Something unexpected. Sentence 3: What should we DO about it?",
        "command_set": [
            "Sentence 1 \u2014 What the data shows:",
            "Sentence 2 \u2014 One surprising finding:",
            "Sentence 3 \u2014 One action based on the data:",
        ],
        "scenarios": [
            {
                "label": "School Water Fountain Usage:\nMorning break: 120 uses\nLunch: 200 uses\nAfternoon break: 80 uses\nAfter school: 30 uses",
                "hint": "Main trend: lunch is busiest. Surprise: after school is very low. Action: add a second fountain near the lunch area.",
            },
        ],
        "min_steps": 3,
    },
]

QUIZ = [
    {"question": "Which chart is best for comparing categories?", "options": ["Line graph", "Pie chart", "Bar chart", "Scatter plot"], "correct": 2},
    {"question": "What is an outlier?", "options": ["The average value", "A data point very different from the rest", "The most common value", "A type of chart"], "correct": 1},
    {"question": "Walk: 40%, Bike: 25%, Bus: 20%, Car: 15%. What chart shows this best?", "options": ["Bar chart", "Line graph", "Pie chart \u2014 it shows proportions of a whole", "Scatter plot"], "correct": 2},
    {"question": "Why is it important to tell a \u2018story\u2019 with data?", "options": ["It sounds fancy", "So people understand what the numbers mean and can take action", "Data doesn\u2019t need a story", "Only scientists tell data stories"], "correct": 1},
]
