"""Lesson 15: Staying Safe Online & What is AI?
Track 4: Digital World | Dreaming in Space.
"""

LESSON = {
    "id": "lesson-15",
    "title": "Staying Safe Online & What is AI?",
    "description": (
        "Learn to spot online risks, protect your accounts, and understand "
        "how artificial intelligence makes decisions all around you."
    ),
    "duration": 45,
    "level": "Beginner",
    "age_group": "Ages 8-18",
    "color": "#e11d48",
    "welcome": (
        "The internet is amazing, but not everyone online has good intentions. "
        "AND \u2014 AI is already in your pocket! Your phone\u2019s autocorrect, "
        "Spotify\u2019s recommendations, TikTok\u2019s For You page \u2014 that\u2019s "
        "all AI. Today you\u2019ll learn to stay safe AND understand the AI "
        "around you."
    ),
    "recap_msg": (
        "Think before you click. Protect your passwords. Don\u2019t share "
        "personal info with strangers. And remember: AI learns from data, "
        "not magic. Use it wisely, question it always!"
    ),
}

ROLE_MODEL = {
    "name": "Joy Buolamwini",
    "years": "1989\u2013present",
    "intro": "Researcher who discovered that facial recognition AI was biased against darker-skinned faces \u2014 and fought to fix it.",
    "detail": (
        "Joy showed the world that AI can be unfair if it\u2019s trained on "
        "biased data. Her work led to new laws and better AI systems. She "
        "proves that questioning technology makes it better for everyone."
    ),
}

VOCABULARY = [
    {"word": "Phishing", "definition": "A fake message that tricks you into giving away personal information"},
    {"word": "Password", "definition": "A secret word or phrase that protects your account"},
    {"word": "AI (Artificial Intelligence)", "definition": "Software that learns patterns from data to make decisions or predictions"},
    {"word": "Bias", "definition": "When AI treats some groups unfairly because of the data it was trained on"},
    {"word": "Privacy", "definition": "Your right to control who sees your personal information"},
]

OBJECTIVES = [
    "Spot a phishing attempt and explain the red flags.",
    "Create a strong password and explain what makes it strong.",
    "Explain what AI is and identify where it\u2019s used in everyday life.",
]

EXERCISES = [
    {
        "id": 1,
        "concept": {
            'title': 'Spot a Scam',
            'body': '<strong>Phishing</strong> is a fake message that tries to trick you into giving away passwords, money, or personal info. The clues are always there if you look closely &mdash; weird email addresses, urgency, and asks for things real companies never ask for.',
            'examples': [
                '🚨 <strong>Urgency</strong> &mdash; “Act now! 24 hours!”',
                '🔗 <strong>Weird link</strong> &mdash; <em>g00gle-support.xyz</em> is NOT google.com',
            ],
            'outro': 'Read each message and decide: real or fake?',
            'bg_from': '#fee2e2',
            'bg_to': '#fecaca',
            'border': '#ef4444',
        },
        "title": "Spot the Scam",
        "type": "read_conditional",
        "difficulty": "Easy",
        "xp": 10,
        "description": "Read each message and decide: is it real or a phishing scam?",
        "beaver_msg": "Scammers are sneaky! But they always leave clues. Look for spelling mistakes, urgency, and suspicious links.",
        "beaver_hint": "Red flags: misspelled company names, \u201cclick NOW or else,\u201d asking for passwords, weird email addresses.",
        "problems": [
            {
                "rule": "From: security@g00gle-support.xyz\nSubject: URGENT! Your account will be deleted!\n\nDear user, click this link immediately to verify your account or it will be permanently deleted in 24 hours.",
                "situation": "Is this email real or fake?",
                "options": ["Real \u2014 I should click the link", "Fake \u2014 the email address is suspicious and it uses urgency to scare me", "I\u2019m not sure", "Real \u2014 Google always emails like this"],
                "correct": 1,
            },
            {
                "rule": "From: noreply@school.edu\nSubject: Your school report is ready\n\nHi [Student Name], your end-of-term report is now available on the school portal. Log in at portal.school.edu to view it.",
                "situation": "Is this email real or fake?",
                "options": ["Fake", "Real \u2014 it uses the correct school domain and doesn\u2019t ask for a password", "Not sure", "Fake \u2014 all emails are scams"],
                "correct": 1,
            },
            {
                "rule": "A stranger messages you on a game:\n\u201cHey I work for the game company! Give me your password and I\u2019ll give you 1000 free coins!\u201d",
                "situation": "What should you do?",
                "options": ["Give them my password \u2014 free coins!", "Report and block \u2014 no real employee asks for passwords", "Ask for proof first", "Ignore but don\u2019t report"],
                "correct": 1,
            },
        ],
    },
    {
        "id": 2,
        "concept": {
            'title': 'What makes something AI?',
            'body': "<strong>AI</strong> is software that <strong>learns from examples</strong> instead of just following fixed rules. A calculator isn't AI &mdash; it follows exact instructions. But Spotify recommendations and Siri use AI because they learn from huge amounts of data!",
            'examples': [
                '🤖 <strong>AI</strong> &mdash; learns from data, gets better over time.',
                '⚙️ <strong>Not AI</strong> &mdash; follows fixed rules, behaves the same every time.',
            ],
            'bg_from': '#ede9fe',
            'bg_to': '#ddd6fe',
            'border': '#8b5cf6',
        },
        "title": "AI or Not AI?",
        "type": "grouping",
        "difficulty": "Medium",
        "xp": 15,
        "description": "Sort these technologies into AI or Not AI.",
        "beaver_msg": "AI learns from patterns in data. A calculator follows fixed rules. Can you tell the difference?",
        "beaver_hint": "AI = learns and improves from data. Not AI = follows the same fixed instructions every time.",
        "task_title": "Sort: AI or Not AI?",
        "jumbled_steps": [
            {"step": "Spotify recommending songs you might like", "group": "AI"},
            {"step": "A calculator adding 2 + 2", "group": "Not AI"},
            {"step": "Siri answering your questions", "group": "AI"},
            {"step": "An alarm clock ringing at 7am", "group": "Not AI"},
            {"step": "TikTok showing you videos based on what you watched", "group": "AI"},
            {"step": "A light switch turning on a lamp", "group": "Not AI"},
            {"step": "Google Translate converting English to Dutch", "group": "AI"},
            {"step": "A microwave timer counting down", "group": "Not AI"},
        ],
        "groups": ["AI", "Not AI"],
    },
    {
        "id": 3,
        "title": "What Would You Do?",
        "type": "robot_commands",
        "difficulty": "Medium",
        "xp": 20,
        "description": (
            "Three real-world scenarios about online safety and AI. "
            "For each one, explain what you would do and why."
        ),
        "beaver_msg": "There\u2019s no single right answer here \u2014 but there ARE smart choices. Think carefully!",
        "beaver_hint": "For each scenario: What\u2019s the risk? What\u2019s the smart action? Who should you tell?",
        "command_set": [],
        "scenarios": [
            {
                "label": "A stranger on social media asks for your home address to \u2018send you a prize.\u2019 What do you do?",
                "hint": "Never share personal info. Report the account. Tell a trusted adult.",
            },
            {
                "label": "An AI chatbot gives you homework answers that sound right but you\u2019re not sure they\u2019re correct. What do you do?",
                "hint": "AI can be wrong! Check the answers yourself. Use AI as a helper, not a replacement for thinking.",
            },
            {
                "label": "Your friend shares your embarrassing photo online without asking. What do you do?",
                "hint": "Ask them to take it down. If they won\u2019t, talk to a trusted adult. Everyone has a right to privacy.",
            },
        ],
        "min_steps": 3,
    },
]

QUIZ = [
    {"question": "What is phishing?", "options": ["A type of fishing", "A fake message that tricks you into giving away personal info", "A computer virus", "A social media app"], "correct": 1},
    {"question": "What makes a strong password?", "options": ["Your name and birthday", "The word \u2018password\u2019", "Long, with a mix of letters, numbers, and symbols", "Same as your username"], "correct": 2},
    {"question": "What is AI?", "options": ["A robot that looks like a human", "Software that learns patterns from data to make predictions", "A type of internet connection", "A programming language"], "correct": 1},
    {"question": "An AI gives you a wrong answer. Whose fault is it?", "options": ["Nobody\u2019s \u2014 AI is always right", "The AI\u2019s data or training was incomplete", "Your computer is broken", "The internet is slow"], "correct": 1},
]
