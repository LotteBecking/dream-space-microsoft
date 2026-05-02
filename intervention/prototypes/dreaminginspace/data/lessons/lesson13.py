"""Lesson 13: The Algorithm Race , Design & Optimise.
Track 3: Creation & Application | Dreaming in Space.
"""

LESSON = {
    "id": "lesson-13",
    "title": "The Algorithm Race",
    "description": (
        "Apply everything you\u2019ve learned to design, build, test, "
        "and improve an original algorithm for a real-world problem."
    ),
    "duration": 50,
    "level": "Intermediate",
    "age_group": "Ages 8-18",
    "color": "#b45309",
    "welcome": (
        "Final mission, Cadet! We need to sort 1,000 asteroids by size. "
        "We could do it one by one, or we could use a smart algorithm "
        "to do it in seconds! Great code doesn\u2019t just work \u2014 it "
        "works FAST. Now YOU design the solution!"
    ),
    "recap_msg": (
        "Algorithms are the secret recipes of the digital world. You "
        "planned, built, tested, and improved one from scratch. That\u2019s "
        "EXACTLY what software engineers do. You\u2019ve officially "
        "graduated from the Dreaming in Space academy!"
    ),
}

ROLE_MODEL = {
    "name": "Marian Croak",
    "years": "1955\u2013present",
    "intro": "Pioneered key Voice over IP (VoIP) technology \u2014 her patents made video calls possible for billions.",
    "detail": (
        "Marian holds over 200 patents. She designed algorithms that convert "
        "your voice into data packets and send them over the internet. "
        "Without her work, Zoom, FaceTime, and WhatsApp calls wouldn\u2019t exist."
    ),
}

VOCABULARY = [
    {"word": "Design", "definition": "Planning a solution before writing code"},
    {"word": "Pseudocode", "definition": "Writing your algorithm in plain language before real code"},
    {"word": "Edge Case", "definition": "An unusual input that might break your algorithm"},
    {"word": "Iterate", "definition": "Improve your solution by testing and refining it"},
]

OBJECTIVES = [
    "Choose a real-world problem and plan an algorithmic solution.",
    "Write a complete algorithm using all the concepts learned so far.",
    "Test your algorithm with different inputs and fix edge cases.",
]

EXERCISES = [
    {
        "id": 1,
        "title": "Choose & Plan",
        "type": "robot_commands",
        "difficulty": "Medium",
        "xp": 15,
        "description": (
            "Compare two ways to solve the same problem, then pick a challenge "
            "and plan which programming concepts you\u2019ll use."
        ),
        "beaver_msg": "Path A uses 10 lines of code. Path B uses 3 lines (with a loop). Which is the better algorithm?",
        "beaver_hint": "Shorter code is easier to read and faster to run. To find a number between 1 and 100, start at 50 and ask \u2018Higher or Lower?\u2019 \u2014 that\u2019s a Binary Search!",
        "command_set": [
            "Problem I\u2019m solving:",
            "Sub-tasks:",
            "Variables needed:",
            "Loops needed:",
            "Conditionals needed:",
            "Functions I\u2019ll write:",
        ],
        "scenarios": [
            {"label": "Route Planner \u2014 find the shortest path between two places", "hint": "Variables: start, end, distance. Loop: check each possible route. Conditional: is this route shorter?"},
            {"label": "Quiz Generator \u2014 create a quiz that tracks score and gives feedback", "hint": "Variables: questions (list), score, current_question. Loop: go through each question. Conditional: check answer."},
            {"label": "Playlist Organiser \u2014 sort and filter songs by mood, artist, or length", "hint": "Variables: songs (list), filter_mood. Loop: check each song. Conditional: does it match the filter?"},
        ],
        "min_steps": 5,
    },
    {
        "id": 2,
        "title": "Build Your Algorithm",
        "type": "robot_commands",
        "difficulty": "Hard",
        "xp": 25,
        "description": (
            "Write your complete algorithm. It must include at least: "
            "1 variable, 1 loop, 1 conditional, and 1 function."
        ),
        "beaver_msg": "Create a final algorithm to land the ship! Use a WHILE loop to check distance and a function to fire_thrusters().",
        "beaver_hint": "Start with the function definition. Example: while (distance > 0): if (speed > 10): fire_thrusters().",
        "command_set": [],
        "scenarios": [
            {"label": "Write your full algorithm for the problem you chose in Mission 1", "hint": "Use pseudocode. Include def, variables, LOOP, IF/ELSE, return."},
        ],
        "min_steps": 8,
    },
    {
        "id": 3,
        "title": "Test & Improve",
        "type": "robot_commands",
        "difficulty": "Hard",
        "xp": 25,
        "description": (
            "Test your algorithm with 3 different inputs. Find one edge "
            "case that breaks it. Fix it. Reflect on what was hardest."
        ),
        "beaver_msg": "Testing is how good algorithms become GREAT algorithms. Break it, then fix it!",
        "beaver_hint": "Try: a normal input, an extreme input (very big/small), and a weird input (empty, zero, negative). Find the one that fails.",
        "command_set": [
            "Test 1 (normal input):",
            "Result:",
            "Test 2 (extreme input):",
            "Result:",
            "Test 3 (edge case):",
            "What broke:",
            "My fix:",
            "Reflection \u2014 the hardest part was:",
        ],
        "scenarios": [
            {"label": "Test your algorithm from Mission 2 with 3 different inputs", "hint": "One normal, one extreme, one edge case. Fix anything that breaks."},
        ],
        "min_steps": 6,
    },
]

QUIZ = [
    {"question": "What is an edge case?", "options": ["The first line of code", "An unusual input that might break your algorithm", "A type of loop", "A function name"], "correct": 1},
    {"question": "Why should you plan before coding?", "options": ["It\u2019s a waste of time", "So you know what you\u2019re building before you build it", "Computers require plans", "It\u2019s optional"], "correct": 1},
    {"question": "What is pseudocode?", "options": ["Real Python code", "Writing your algorithm in plain language first", "A type of variable", "A programming language"], "correct": 1},
    {"question": "You tested your algorithm and it fails with empty input. What should you do?", "options": ["Ignore it", "Add a check: IF input is empty THEN handle it", "Delete the algorithm", "Tell the user not to do that"], "correct": 1},
]
