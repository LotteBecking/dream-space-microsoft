"""Lesson 18: Prompt Pilot — Talking to AI.
Track 4: The Digital World | Dreaming in Space.
"""

LESSON_18 = {
    "id": "lesson-18",
    "title": "Prompt Pilot",
    "description": (
        "Learn to communicate with AI effectively. Discover why context, "
        "specificity, and structure make all the difference."
    ),
    "duration": 45,
    "level": "Intermediate",
    "age_group": "Ages 8-18",
    "color": "#0ea5e9",
    "welcome": (
        "The Ship\u2019s AI is a bit literal. If you ask for \u2018food,\u2019 "
        "it might give you a bowl of screws! AI is a powerful co-pilot, "
        "but it needs clear, detailed instructions \u2014 just like code. "
        "Today you\u2019ll learn the art of \u2018Prompt Engineering.\u2019"
    ),
    "recap_msg": (
        "AI is your co-pilot, but YOU are the Captain. Clear prompts = "
        "better results. Give it a role, a tone, and specific details. "
        "The more context you provide, the smarter the AI becomes!"
    ),
}

ROLE_MODEL_18 = {
    "name": "Timnit Gebru",
    "years": "1982\u2013present",
    "intro": "AI ethics researcher who fights to make AI fair, transparent, and safe for everyone.",
    "detail": (
        "Timnit co-authored groundbreaking research showing that large "
        "AI models can have hidden biases. She founded the DAIR Institute "
        "to ensure AI serves all communities, not just the privileged few. "
        "She reminds us: AI is only as good as the humans who guide it."
    ),
}

VOCABULARY_18 = [
    {"word": "Prompt", "definition": "The instruction or question you give to an AI system"},
    {"word": "Context", "definition": "Background information that helps the AI understand what you want"},
    {"word": "Specificity", "definition": "Being precise about what you need \u2014 details matter!"},
    {"word": "Hallucination", "definition": "When AI confidently makes up incorrect information"},
]

OBJECTIVES_18 = [
    "Explain why specific prompts get better AI results than vague ones.",
    "Improve a vague prompt by adding context, role, and constraints.",
    "Identify when AI output might be wrong and needs human verification.",
]

EXERCISES_18 = [
    {
        "id": 1,
        "title": "Context is Queen",
        "type": "read_conditional",
        "difficulty": "Easy",
        "xp": 10,
        "description": "Compare prompts and pick the one that will get the best result from AI.",
        "beaver_msg": "We want the AI to write a poem about the moon. Which prompt is better?",
        "beaver_hint": "Giving the AI a \u2018Role\u2019 (space traveller) and a \u2018Tone\u2019 (funny) gets much better results.",
        "problems": [
            {
                "rule": "You want a poem about the moon.",
                "situation": "Which prompt will get the best result?",
                "options": [
                    "Write a poem.",
                    "Write a short, funny poem about the moon for a space traveller.",
                    "Moon poem now.",
                    "Write something.",
                ],
                "correct": 1,
            },
            {
                "rule": "You want help with a coding bug.",
                "situation": "Which prompt helps the AI most?",
                "options": [
                    "Fix my code.",
                    "My code doesn\u2019t work, help!",
                    "I\u2019m getting a \u2018SyntaxError\u2019 on line 4 of my Python script. Can you find the bug?",
                    "Code broken. What do?",
                ],
                "correct": 2,
            },
            {
                "rule": "You want a picture of a spaceship.",
                "situation": "Which prompt gives the most useful result?",
                "options": [
                    "Spaceship.",
                    "Draw something cool.",
                    "A shiny red spaceship flying through Saturn\u2019s rings at sunset, digital art style.",
                    "Make art.",
                ],
                "correct": 2,
            },
            {
                "rule": "The AI says \u2018The Eiffel Tower is in London.\u2019",
                "situation": "What should you do?",
                "options": [
                    "Trust it \u2014 AI is always right",
                    "Check the fact yourself \u2014 AI can \u2018hallucinate\u2019 wrong answers",
                    "Ask the AI again and it\u2019ll fix itself",
                    "Ignore it",
                ],
                "correct": 1,
            },
        ],
    },
    {
        "id": 2,
        "title": "The Prompt Fixer",
        "type": "robot_commands",
        "difficulty": "Medium",
        "xp": 15,
        "description": (
            "These prompts are too vague! Rewrite each one by adding "
            "a role, tone, audience, and specific details."
        ),
        "beaver_msg": "Adding adjectives and context helps the AI \u2018visualise\u2019 your goal!",
        "beaver_hint": "Formula: [Role] + [Task] + [Details] + [Constraints]. Example: \u2018You are a friendly teacher. Explain loops to a 10-year-old in 3 sentences.\u2019",
        "command_set": [
            "Role: You are a...",
            "Task: Please...",
            "Details: It should include...",
            "Constraints: Keep it under...",
        ],
        "scenarios": [
            {
                "label": "Improve: \u2018Write a story.\u2019 \u2192 Add character, setting, genre, length, audience",
                "hint": "e.g. \u2018You are a children\u2019s author. Write a 200-word adventure story about a space beaver exploring a crystal cave on Mars.\u2019",
            },
            {
                "label": "Improve: \u2018Explain coding.\u2019 \u2192 Add audience, analogy, format, length",
                "hint": "e.g. \u2018Explain what a variable is to an 8-year-old. Use a labelled box analogy. Keep it under 50 words.\u2019",
            },
        ],
        "min_steps": 4,
    },
    {
        "id": 3,
        "title": "AI Fact-Checker",
        "type": "read_conditional",
        "difficulty": "Medium",
        "xp": 20,
        "description": "The AI gave us some answers. Some are right, some are \u2018hallucinations.\u2019 Can you spot which ones to trust?",
        "beaver_msg": "Providing the specific error message is the \u2018Secret Sauce\u2019 of prompt engineering!",
        "beaver_hint": "If it sounds too specific or confident about something you can\u2019t verify, double-check it!",
        "problems": [
            {
                "rule": "AI says: \u2018Python was created by Guido van Rossum in 1991.\u2019",
                "situation": "Should you trust this?",
                "options": ["Yes \u2014 this is a well-known, verifiable fact", "No \u2014 AI always lies", "Maybe \u2014 but still check", "Ignore it"],
                "correct": 0,
            },
            {
                "rule": "AI says: \u2018The function sort_list() was invented by Ada Lovelace in 1843.\u2019",
                "situation": "Is this likely accurate?",
                "options": [
                    "Yes \u2014 Ada was a pioneer",
                    "No \u2014 sort_list() is a modern function name, not from 1843. This is a hallucination.",
                    "Maybe \u2014 who knows?",
                    "Ask the AI to confirm",
                ],
                "correct": 1,
            },
            {
                "rule": "You asked AI to write a quiz about loops. It generated 4 questions.",
                "situation": "What should you do before using them?",
                "options": [
                    "Use them immediately",
                    "Check each answer is correct \u2014 AI can generate plausible but wrong answers",
                    "Delete them and write your own",
                    "AI quizzes are always perfect",
                ],
                "correct": 1,
            },
        ],
    },
]

QUIZ_18 = [
    {"question": "What is a \u2018prompt\u2019 in AI?", "options": ["A type of code", "The instruction you give to an AI", "A bug", "A password"], "correct": 1},
    {"question": "Which prompt is better?", "options": ["\u2018Write something.\u2019", "\u2018Write a 100-word funny story about a robot dog for kids aged 8.\u2019", "\u2018Help.\u2019", "\u2018Do stuff.\u2019"], "correct": 1},
    {"question": "What is an AI \u2018hallucination\u2019?", "options": ["When AI sees images", "When AI confidently makes up wrong information", "When AI crashes", "When AI is too slow"], "correct": 1},
    {"question": "Why should you ALWAYS check AI output?", "options": ["AI is never wrong", "AI can generate plausible but incorrect information", "It\u2019s a waste of time", "Only experts need to check"], "correct": 1},
]
