"""Lesson 4: Break It Down — Decomposition & Planning.
Track 1: Foundations | Dreaming in Space.
"""

LESSON = {
    "id": "lesson-4",
    "title": "Break It Down \u2014 Decomposition",
    "description": (
        "Learn to split a big problem into smaller, manageable parts "
        "and solve each one step by step."
    ),
    "duration": 45,
    "level": "Beginner",
    "age_group": "Ages 8-18",
    "color": "#7c3aed",
    "welcome": (
        "Imagine building a house. You wouldn\u2019t do everything at once! "
        "You\u2019d start with the foundation, then walls, then roof. "
        "That\u2019s decomposition \u2014 breaking big problems into small steps."
    ),
    "recap_msg": (
        "Decomposition means breaking big problems into smaller parts. "
        "Solve each part, connect them, and the big problem is solved. "
        "Every programmer does this, every day!"
    ),
}

ROLE_MODEL = {
    "name": "Margaret Hamilton",
    "years": "1936\u2013present",
    "intro": (
        "Software engineer who led the team that wrote the Apollo 11 "
        "flight software \u2014 she coined the term \u2018software engineering.\u2019"
    ),
    "detail": (
        "Margaret\u2019s team broke the incredibly complex problem of flying "
        "to the Moon into thousands of smaller software modules. Each handled "
        "one job \u2014 navigation, life support, communications."
    ),
}

VOCABULARY = [
    {"word": "Decomposition", "definition": "Breaking a big problem into smaller, manageable parts"},
    {"word": "Sub-task", "definition": "One smaller piece of the bigger problem"},
    {"word": "Dependency", "definition": "When one sub-task must be done before another can start"},
    {"word": "Planning", "definition": "Deciding what to do, in what order, before you start"},
]

OBJECTIVES = [
    "Break a complex task into smaller sub-tasks.",
    "Identify which sub-tasks depend on each other.",
    "Create a plan that connects sub-tasks in the right order.",
]

EXERCISES = [
    {
        "id": 1,
        "title": "Spot the Sub-tasks",
        "type": "grouping",
        "difficulty": "Easy",
        "xp": 10,
        "description": "This list of steps is a jumbled mess! Sort them into groups that belong together.",
        "beaver_msg": "This list is a mess! Can you sort these steps into groups that belong together?",
        "beaver_hint": "Read each step and ask: what bigger task does this belong to?",
        "task_title": "Getting Ready for a School Trip",
        "jumbled_steps": [
            {"step": "Pack lunch into bag", "group": "Packing"},
            {"step": "Put on shoes", "group": "Getting dressed"},
            {"step": "Eat breakfast", "group": "Breakfast"},
            {"step": "Pack notebook and pencils", "group": "Packing"},
            {"step": "Brush teeth", "group": "Getting dressed"},
            {"step": "Check the weather", "group": "Getting dressed"},
            {"step": "Put on jacket if cold", "group": "Getting dressed"},
            {"step": "Pour cereal and milk", "group": "Breakfast"},
            {"step": "Pack water bottle", "group": "Packing"},
            {"step": "Walk to bus stop", "group": "Travel"},
            {"step": "Check bus timetable", "group": "Travel"},
            {"step": "Wait for bus", "group": "Travel"},
        ],
        "groups": ["Breakfast", "Getting dressed", "Packing", "Travel"],
    },
    {
        "id": 2,
        "title": "Decompose It Yourself",
        "type": "decompose",
        "difficulty": "Medium",
        "xp": 15,
        "description": "Pick a big task and break it into sub-tasks. Write 3\u20135 steps for each.",
        "beaver_msg": "Your turn! Break this big challenge into smaller pieces.",
        "beaver_hint": "Think: what are the main parts? Then write the steps for each part.",
        "task_options": [
            {"label": "Organise a Classroom Science Fair"},
            {"label": "Plan a Birthday Party"},
            {"label": "Build a Simple Website"},
        ],
        "min_subtasks": 3,
        "min_steps_per_subtask": 2,
    },
    {
        "id": 3,
        "title": "Connect the Pieces",
        "type": "ordering_dependencies",
        "difficulty": "Medium",
        "xp": 20,
        "description": "These sub-tasks are broken down, but some must happen before others. Put them in order!",
        "beaver_msg": "Some pieces must happen first! Can you figure out the right order?",
        "beaver_hint": "Ask: can I do this step WITHOUT finishing another step first?",
        "scenarios": [
            {
                "label": "Making a Video for School",
                "subtasks": [
                    {"task": "Write the script", "order": 1},
                    {"task": "Film the scenes", "order": 2},
                    {"task": "Edit the video", "order": 3},
                    {"task": "Add music and titles", "order": 4},
                    {"task": "Show to the class", "order": 5},
                ],
            },
            {
                "label": "Planting a Garden",
                "subtasks": [
                    {"task": "Choose what to plant", "order": 1},
                    {"task": "Buy seeds and soil", "order": 2},
                    {"task": "Prepare the ground", "order": 3},
                    {"task": "Plant the seeds", "order": 4},
                    {"task": "Water regularly", "order": 5},
                ],
            },
        ],
    },
]

QUIZ = [
    {
        "question": "What is decomposition?",
        "options": [
            "Making code run faster",
            "Breaking a big problem into smaller parts",
            "Deleting old code",
            "A type of loop",
        ],
        "correct": 1,
    },
    {
        "question": "Why is decomposition useful?",
        "options": [
            "It makes problems harder",
            "Smaller parts are easier to understand and solve",
            "It uses more memory",
            "It only works for maths problems",
        ],
        "correct": 1,
    },
    {
        "question": "What is a dependency between sub-tasks?",
        "options": [
            "Two tasks that have nothing in common",
            "When one task must finish before another can start",
            "A bug in the code",
            "A type of variable",
        ],
        "correct": 1,
    },
    {
        "question": "You\u2019re making a sandwich. Which must happen FIRST?",
        "options": [
            "Eat the sandwich",
            "Spread butter on bread",
            "Get bread from the bag",
            "Put the two slices together",
        ],
        "correct": 2,
    },
]
