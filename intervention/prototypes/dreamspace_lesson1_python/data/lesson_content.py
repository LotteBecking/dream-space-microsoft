"""Lesson 1 content: How Does a Computer Think? -- The PB&J Sandwich Algorithm.

Pedagogical design grounded in peer-reviewed research on computational thinking,
multiple learning styles, and developmentally appropriate CS education for ages 8-12.
"""

# ---------------------------------------------------------------------------
# Academic references underpinning this lesson
# ---------------------------------------------------------------------------

RESEARCH_REFERENCES = [
    {
        "id": "wing2006",
        "citation": (
            "Wing, J. M. (2006). Computational Thinking. "
            "Communications of the ACM, 49(3), 33\u201335."
        ),
        "doi": "10.1145/1118178.1118215",
        "relevance": (
            "Foundational argument that computational thinking\u2014including "
            "algorithmic reasoning and decomposition\u2014should be a fundamental "
            "skill for every child alongside reading, writing, and arithmetic."
        ),
    },
    {
        "id": "grover_pea2013",
        "citation": (
            "Grover, S. & Pea, R. (2013). Computational Thinking in K\u201312: "
            "A Review of the State of the Field. Educational Researcher, 42(1), 38\u201343."
        ),
        "doi": "10.3102/0013189X12463051",
        "relevance": (
            "Comprehensive review establishing that algorithmic thinking can be "
            "effectively taught to primary-age children through scaffolded, "
            "concrete activities before introducing formal programming."
        ),
    },
    {
        "id": "bell1998",
        "citation": (
            "Bell, T., Witten, I. H. & Fellows, M. (1998). Computer Science "
            "Unplugged: Off-line Activities and Games for All Ages. "
            "Canterbury, NZ: University of Canterbury."
        ),
        "relevance": (
            "Demonstrates that core CS concepts\u2014algorithms, sequencing, "
            "debugging\u2014can be learned through kinaesthetic, screen-free "
            "activities, supporting tactile and bodily-kinaesthetic learners."
        ),
    },
    {
        "id": "gardner1983",
        "citation": (
            "Gardner, H. (1983). Frames of Mind: The Theory of Multiple "
            "Intelligences. New York: Basic Books."
        ),
        "relevance": (
            "Multiple Intelligences theory supports designing activities that "
            "engage linguistic, logical-mathematical, spatial, bodily-kinaesthetic, "
            "and interpersonal intelligences so every learner has an entry point."
        ),
    },
    {
        "id": "fleming_mills1992",
        "citation": (
            "Fleming, N. D. & Mills, C. (1992). Not Another Inventory, Rather "
            "a Catalyst for Reflection. To Improve the Academy, 11, 137\u2013155."
        ),
        "relevance": (
            "Introduces the VARK model (Visual, Aural, Read/Write, Kinaesthetic) "
            "used here to ensure each lesson segment addresses at least two "
            "sensory modalities."
        ),
    },
    {
        "id": "kolb1984",
        "citation": (
            "Kolb, D. A. (1984). Experiential Learning: Experience as the "
            "Source of Learning and Development. Englewood Cliffs, NJ: Prentice Hall."
        ),
        "relevance": (
            "Experiential Learning Cycle (concrete experience \u2192 reflective "
            "observation \u2192 abstract conceptualisation \u2192 active experimentation) "
            "structures the lesson flow from the sandwich demo through reflection "
            "to independent algorithm writing."
        ),
    },
    {
        "id": "papert1980",
        "citation": (
            "Papert, S. (1980). Mindstorms: Children, Computers, and Powerful "
            "Ideas. New York: Basic Books."
        ),
        "relevance": (
            "Constructionism: children learn best by constructing personally "
            "meaningful artefacts. The sandwich algorithm and robot-chef tasks "
            "let students build their own executable instructions."
        ),
    },
    {
        "id": "vygotsky1978",
        "citation": (
            "Vygotsky, L. S. (1978). Mind in Society: The Development of Higher "
            "Psychological Processes. Cambridge, MA: Harvard University Press."
        ),
        "relevance": (
            "Zone of Proximal Development (ZPD) and scaffolding: exercises progress "
            "from guided (Easy) to independent (Medium/Hard), and pair work keeps "
            "tasks within each child\u2019s ZPD."
        ),
    },
    {
        "id": "bruner1966",
        "citation": (
            "Bruner, J. S. (1966). Toward a Theory of Instruction. "
            "Cambridge, MA: Harvard University Press."
        ),
        "relevance": (
            "Concrete\u2013Pictorial\u2013Abstract (CPA) progression: students manipulate "
            "real objects (sandwich demo), view visual simulations, then write "
            "abstract algorithm steps."
        ),
    },
    {
        "id": "piaget1973",
        "citation": (
            "Piaget, J. (1973). To Understand Is to Invent: The Future of "
            "Education. New York: Grossman Publishers."
        ),
        "relevance": (
            "Children aged 8\u201312 are in Piaget\u2019s Concrete Operational Stage; "
            "they reason logically about concrete events. Tangible algorithm tasks "
            "align with this developmental level."
        ),
    },
    {
        "id": "dweck2006",
        "citation": (
            "Dweck, C. S. (2006). Mindset: The New Psychology of Success. "
            "New York: Random House."
        ),
        "relevance": (
            "Growth-mindset framing: debugging is presented as \u2018improving\u2019 rather "
            "than \u2018failing,\u2019 encouraging persistence and a positive attitude "
            "toward iterative problem-solving."
        ),
    },
    {
        "id": "bers2018",
        "citation": (
            "Bers, M. U. (2018). Coding as a Playground: Programming and "
            "Computational Thinking in the Early Childhood Classroom. "
            "New York: Routledge."
        ),
        "relevance": (
            "Supports playful, low-floor/high-ceiling task design so young "
            "learners can enter at their own level while advanced students "
            "extend the same activity."
        ),
    },
]

# ---------------------------------------------------------------------------
# Pedagogical framework: how this lesson serves different learning styles
# ---------------------------------------------------------------------------

PEDAGOGICAL_FRAMEWORK = {
    "overview": (
        "This lesson is designed using a multi-modal, research-backed approach "
        "that addresses diverse learning styles. Every core concept is presented "
        "through at least three modalities (visual, auditory/verbal, read/write, "
        "and kinaesthetic) so that every child has an accessible entry point "
        "(Gardner, 1983; Fleming & Mills, 1992)."
    ),
    "learning_style_coverage": [
        {
            "style": "Visual / Spatial",
            "description": (
                "Interactive PB&J sandwich simulator with step-by-step visual "
                "feedback; colour-coded vocabulary flip cards; progress bar."
            ),
            "research_basis": ["gardner1983", "fleming_mills1992", "bruner1966"],
        },
        {
            "style": "Auditory / Verbal",
            "description": (
                "Whole-class discussion of \u2018what happened when we swapped steps?\u2019; "
                "partner comparison in the tea-sorting exercise; peer testing of "
                "algorithms by reading them aloud."
            ),
            "research_basis": ["gardner1983", "vygotsky1978"],
        },
        {
            "style": "Read / Write",
            "description": (
                "Writing numbered algorithms; vocabulary definitions; reading the "
                "Ada Lovelace role-model passage and reflecting on it."
            ),
            "research_basis": ["fleming_mills1992", "wing2006"],
        },
        {
            "style": "Kinaesthetic / Tactile",
            "description": (
                "Physical card-sorting activity (tea steps); hands-on sandwich "
                "demo (unplugged); dragging commands in the simulator."
            ),
            "research_basis": ["bell1998", "kolb1984", "papert1980"],
        },
        {
            "style": "Logical / Mathematical",
            "description": (
                "Sequencing constraints (\u2018which steps MUST come before others?\u2019); "
                "debugging flawed algorithms; generalising a sandwich algorithm "
                "to work for any input."
            ),
            "research_basis": ["wing2006", "grover_pea2013", "piaget1973"],
        },
        {
            "style": "Social / Interpersonal",
            "description": (
                "Pair work in Exercise 2 (compare sequences); peer-testing in "
                "the Extension challenge; group discussion of allergy-safety rules."
            ),
            "research_basis": ["vygotsky1978", "gardner1983"],
        },
    ],
    "design_principles": [
        {
            "principle": "Concrete \u2192 Pictorial \u2192 Abstract (CPA)",
            "application": (
                "Students first manipulate physical objects (sandwich ingredients), "
                "then interact with a visual simulator, then write abstract "
                "numbered-step algorithms."
            ),
            "reference": "bruner1966",
        },
        {
            "principle": "Experiential Learning Cycle",
            "application": (
                "Concrete Experience (sandwich demo) \u2192 Reflective Observation "
                "(class discussion) \u2192 Abstract Conceptualisation (vocabulary & "
                "definitions) \u2192 Active Experimentation (writing own algorithms)."
            ),
            "reference": "kolb1984",
        },
        {
            "principle": "Scaffolded Difficulty within the ZPD",
            "application": (
                "Exercises progress Easy \u2192 Easy \u2192 Medium, with pair support. "
                "Extension challenges provide a high ceiling without raising the floor."
            ),
            "reference": "vygotsky1978",
        },
        {
            "principle": "Constructionism",
            "application": (
                "Students build personally meaningful artefacts (their own "
                "algorithms for everyday tasks) rather than passively receiving "
                "instructions."
            ),
            "reference": "papert1980",
        },
        {
            "principle": "Growth Mindset & Debugging Culture",
            "application": (
                "Errors in the simulator are framed as \u2018the robot is confused\u2019 "
                "rather than \u2018you failed.\u2019 Iteration is celebrated."
            ),
            "reference": "dweck2006",
        },
        {
            "principle": "Unplugged-First CS Education",
            "application": (
                "Core concepts are introduced without screens (card sorting, "
                "verbal algorithms) before moving to the digital simulator, "
                "ensuring accessibility for all learners."
            ),
            "reference": "bell1998",
        },
        {
            "principle": "Low Floor, High Ceiling",
            "application": (
                "Every child can write a 6-step algorithm (low floor), while "
                "advanced learners generalise to variable-input algorithms and "
                "conditional logic (high ceiling)."
            ),
            "reference": "bers2018",
        },
    ],
}

# ---------------------------------------------------------------------------
# Core lesson metadata
# ---------------------------------------------------------------------------

LESSON = {
    "id": "lesson-1",
    "title": "Guide the Robot \u2014 The Maze Algorithm",
    "description": (
        "Students give step-by-step instructions to guide a robot through "
        "increasingly complex mazes. They discover that computers follow "
        "instructions exactly and that sequence determines the result."
    ),
    "duration": 60,
    "level": "Beginner",
    "age_group": "Ages 8-12",
    "welcome": "Guide your robot through the maze \u2014 think like Ada Lovelace!",
    "research_basis": (
        "Lesson structure follows Kolb\u2019s (1984) Experiential Learning Cycle and "
        "Bruner\u2019s (1966) CPA progression. Unplugged activities draw on Bell et al. "
        "(1998). Scaffolding follows Vygotsky\u2019s (1978) ZPD framework."
    ),
    "video_url": "",
}

ROLE_MODEL = {
    "name": "Ada Lovelace",
    "years": "1815\u20131852",
    "intro": "The world\u2019s first computer programmer \u2014 she wrote algorithms for a machine that didn\u2019t exist yet.",
    "detail": (
        "Ada was a mathematician who worked with inventor Charles Babbage on his "
        "Analytical Engine. She wrote detailed instructions for how it could calculate "
        "a complex mathematical sequence. Those instructions, written in 1843, are "
        "considered the world\u2019s first computer program. Presenting relatable role "
        "models supports the growth-mindset principle (Dweck, 2006) and helps "
        "students see themselves as capable computational thinkers (Wing, 2006)."
    ),
}

VOCABULARY = [
    {
        "word": "Algorithm",
        "definition": "A set of step-by-step instructions to solve a problem",
    },
    {
        "word": "Sequence",
        "definition": "The order of steps \u2014 changing the order changes the result",
    },
    {
        "word": "Instruction",
        "definition": "A single command that tells the robot what to do",
    },
    {
        "word": "Debug",
        "definition": "Finding and fixing mistakes in your program",
    },
]

LEARNING_OBJECTIVES = [
    "Give precise step-by-step instructions to guide a robot through a maze.",
    "Understand that the order (sequence) of instructions matters.",
    "Navigate around obstacles using a limited set of commands.",
    "Debug incorrect programs by testing, finding errors, and fixing them.",
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
        "learning_styles": ["Read/Write", "Logical/Mathematical"],
        "research_basis": (
            "Writing precise sequential instructions engages the read/write "
            "modality (Fleming & Mills, 1992) and logical-mathematical "
            "intelligence (Gardner, 1983). Choosing personally relevant tasks "
            "follows Papert\u2019s (1980) constructionist principle that learners "
            "build meaning through personally meaningful artefacts."
        ),
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
        "duration_minutes": 8,
        "learning_styles": ["Kinaesthetic/Tactile", "Social/Interpersonal", "Visual/Spatial"],
        "research_basis": (
            "Physical card manipulation is a classic CS Unplugged technique "
            "(Bell et al., 1998) that supports kinaesthetic learners. Partner "
            "comparison activates the social/interpersonal dimension "
            "(Gardner, 1983) and leverages Vygotsky\u2019s (1978) ZPD through peer "
            "dialogue. Concrete-to-abstract progression aligns with Bruner\u2019s "
            "(1966) CPA model and Piaget\u2019s (1973) Concrete Operational Stage."
        ),
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
        "duration_minutes": 10,
        "rules": [
            "Choose one lunch item from the school canteen menu.",
            "Write a precise step-by-step algorithm a robot chef could follow.",
            "Add safety instructions for students with allergies.",
            "Add a rule for what the robot should do if an ingredient runs out.",
            "Challenge: make your algorithm work for any sandwich type.",
        ],
        "learning_styles": ["Logical/Mathematical", "Read/Write", "Social/Interpersonal"],
        "research_basis": (
            "This extension provides a \u2018high ceiling\u2019 for advanced learners "
            "(Bers, 2018) while staying within the ZPD through scaffolded prompts "
            "(Vygotsky, 1978). Introducing conditional logic (\u2018if ingredient "
            "runs out\u2019) develops algorithmic thinking identified by Grover & Pea "
            "(2013) as age-appropriate for primary students. Peer testing "
            "activates interpersonal intelligence (Gardner, 1983)."
        ),
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
        "learning_styles": ["Logical/Mathematical", "Read/Write", "Social/Interpersonal"],
        "research_basis": (
            "Real-world safety constraints demand precise conditional logic, "
            "exercising the algorithmic thinking pillar of CT (Wing, 2006). "
            "Group peer-testing leverages social learning and the ZPD "
            "(Vygotsky, 1978). Writing step-by-step safety rules engages "
            "read/write learners (Fleming & Mills, 1992)."
        ),
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
        "learning_styles": ["Logical/Mathematical", "Read/Write", "Social/Interpersonal"],
        "research_basis": (
            "Iterating on a prior artefact mirrors the reflective observation "
            "and active experimentation stages of Kolb\u2019s (1984) cycle. "
            "Introducing conditional branching (\u2018IF \u2026 THEN\u2019) is identified by "
            "Grover & Pea (2013) as developmentally appropriate for ages 8\u201312. "
            "Debugging one\u2019s own work fosters a growth mindset (Dweck, 2006)."
        ),
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
        "learning_styles": ["Logical/Mathematical", "Visual/Spatial", "Read/Write"],
        "research_basis": (
            "Abstraction and generalisation are higher-order CT skills "
            "(Wing, 2006; Grover & Pea, 2013). Using placeholders moves "
            "students from concrete to abstract representation, following "
            "Bruner\u2019s (1966) CPA progression. This \u2018high-ceiling\u2019 task "
            "(Bers, 2018) lets advanced learners stretch while remaining "
            "within a constructionist framework (Papert, 1980)."
        ),
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
# Maze levels (Lesson 1 primary exercises)
# ---------------------------------------------------------------------------

MAZE_LEVELS = [
    {
        "id": 1,
        "title": "Level 1",
        "description": "Guide the robot through a simple 3\u00d73 maze with one obstacle.",
        "type": "maze",
        "difficulty": "Easy",
        "size": 3,
        "grid": [
            [0, 1, 0],
            [0, 0, 0],
            [0, 0, 0],
        ],
        "start": [0, 0],
        "goal": [2, 2],
        "start_direction": "right",
        "available_commands": ["forward", "turn_left", "turn_right"],
    },
    {
        "id": 2,
        "title": "Level 2",
        "description": "Navigate a 5\u00d75 maze with multiple obstacles and all commands.",
        "type": "maze",
        "difficulty": "Medium",
        "size": 5,
        "grid": [
            [0, 0, 0, 0, 0],
            [0, 1, 0, 1, 0],
            [0, 0, 0, 0, 0],
            [0, 1, 0, 0, 1],
            [0, 0, 0, 0, 0],
        ],
        "start": [0, 0],
        "goal": [4, 4],
        "start_direction": "right",
        "available_commands": ["forward", "backward", "turn_left", "turn_right"],
    },
    {
        "id": 3,
        "title": "Level 3",
        "description": "Master a challenging 7\u00d77 maze with many obstacles.",
        "type": "maze",
        "difficulty": "Hard",
        "size": 7,
        "grid": [
            [0, 0, 0, 1, 0, 0, 0],
            [0, 1, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [1, 0, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0],
            [0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
        ],
        "start": [0, 0],
        "goal": [6, 6],
        "start_direction": "right",
        "available_commands": ["forward", "backward", "turn_left", "turn_right"],
    },
]

QUIZ_QUESTIONS = [
    {
        "question": "What is an algorithm?",
        "options": [
            "A type of robot",
            "A set of step-by-step instructions to solve a problem",
            "A kind of maze",
            "A computer screen",
        ],
        "correct": 1,
    },
    {
        "question": "Why does the order of instructions matter?",
        "options": [
            "It doesn\u2019t matter at all",
            "Because robots are slow",
            "Because changing the order changes the result",
            "Because computers are expensive",
        ],
        "correct": 2,
    },
    {
        "question": "What does it mean to \u2018debug\u2019 a program?",
        "options": [
            "Remove insects from the computer",
            "Delete the program and start over",
            "Find and fix mistakes in the instructions",
            "Make the program run faster",
        ],
        "correct": 2,
    },
    {
        "question": "Your robot hit a wall. What should you do?",
        "options": [
            "Give up and try a different maze",
            "Check your instructions to find and fix the error",
            "Add more commands randomly",
            "Turn off the computer",
        ],
        "correct": 1,
    },
]
