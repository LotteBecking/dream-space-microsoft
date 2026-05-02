"""Lesson 17: The Encryption Code , Cybersecurity Basics.
Track 4: The Digital World | Dreaming in Space.
"""

LESSON = {
    "id": "lesson-17",
    "title": "The Encryption Code",
    "description": (
        "Learn how encryption keeps data safe. Crack a Caesar cipher, "
        "build strong passwords, and understand how digital locks work."
    ),
    "duration": 45,
    "level": "Intermediate",
    "age_group": "Ages 8-18",
    "color": "#6d28d9",
    "welcome": (
        "We\u2019re sending our location to Earth, but we don\u2019t want "
        "space pirates to see it! We need to \u2018Encrypt\u2019 it \u2014 "
        "which is like a secret digital handshake. Today you\u2019ll learn "
        "to lock and unlock data like a real codebreaker!"
    ),
    "recap_msg": (
        "Cybersecurity is about keeping the \u2018bad bots\u2019 out and "
        "your data safe! Encryption scrambles messages so only the right "
        "people can read them. Strong passwords and digital keys protect "
        "everything from your game accounts to space missions."
    ),
}

ROLE_MODEL = {
    "name": "Claude Shannon",
    "years": "1916\u20132001",
    "intro": "Father of Information Theory \u2014 he proved that any message can be sent secretly using maths.",
    "detail": (
        "Claude showed that encryption can be mathematically unbreakable "
        "if you use a key that\u2019s as long as the message and never reuse it. "
        "His 1949 paper \u2018Communication Theory of Secrecy Systems\u2019 is the "
        "foundation of all modern cybersecurity."
    ),
}

VOCABULARY = [
    {"word": "Encryption", "definition": "Scrambling data so only the right person can read it"},
    {"word": "Cipher", "definition": "A method for converting readable text into coded text"},
    {"word": "Key", "definition": "The secret value used to encrypt or decrypt a message"},
    {"word": "Password", "definition": "A secret word or phrase that proves your identity"},
]

OBJECTIVES = [
    "Explain what encryption is and why it keeps data safe.",
    "Encrypt and decrypt a message using a simple cipher.",
    "Identify what makes a strong password versus a weak one.",
]

EXERCISES = [
    {
        "id": 1,
        "title": "The Caesar Cipher",
        "type": "read_conditional",
        "difficulty": "Easy",
        "xp": 10,
        "description": "Crack the code! In a Caesar Cipher, every letter shifts by a number. If the key is +1, A becomes B, B becomes C, etc.",
        "beaver_msg": "If our \u2018Key\u2019 is +1, then A becomes B. What does the word \u2018CAT\u2019 become?",
        "beaver_hint": "Shift each letter forward by the key number. A\u2192B, B\u2192C, C\u2192D...",
        "problems": [
            {
                "rule": "Caesar Cipher with Key = +1\nA\u2192B, B\u2192C, C\u2192D ...",
                "situation": "Encrypt the word \u2018CAT\u2019",
                "options": ["DBU", "BZS", "CAT", "DCU"],
                "correct": 0,
            },
            {
                "rule": "Caesar Cipher with Key = +3\nA\u2192D, B\u2192E, C\u2192F ...",
                "situation": "Encrypt the word \u2018HI\u2019",
                "options": ["KL", "HI", "IJ", "GH"],
                "correct": 0,
            },
            {
                "rule": "Caesar Cipher with Key = +1\nEncrypted message: \u2018TQBDF\u2019",
                "situation": "Decrypt it (shift back by 1)",
                "options": ["URCEG", "SPACE", "TQBDF", "ROACE"],
                "correct": 1,
            },
            {
                "rule": "Someone sends: \u2018PHHW PH DW WKH DLUORFN\u2019\nYou know the key is +3.",
                "situation": "What does the first word \u2018PHHW\u2019 decrypt to?",
                "options": ["MEET", "HELP", "STOP", "FIND"],
                "correct": 0,
            },
        ],
    },
    {
        "id": 2,
        "title": "Password Protector",
        "type": "read_conditional",
        "difficulty": "Medium",
        "xp": 15,
        "description": "A space pirate\u2019s computer can guess easy passwords in seconds. Which passwords are strong enough to protect the ship?",
        "beaver_msg": "Mixing capital letters, numbers, and symbols makes encryption MUCH stronger!",
        "beaver_hint": "Longer passwords with mixed characters are exponentially harder to crack.",
        "problems": [
            {
                "rule": "Which password is strongest?",
                "situation": "Choose the hardest to crack:",
                "options": ["password123", "SpaceBeaver1", "B3av3r!_Sky7", "12345678"],
                "correct": 2,
            },
            {
                "rule": "A hacker\u2019s computer can guess 1 billion passwords per second.",
                "situation": "Which takes longest to crack?",
                "options": ["6-letter lowercase (abc...)", "8-character mixed (Aa1!...)", "10-digit number", "Your pet\u2019s name"],
                "correct": 1,
            },
            {
                "rule": "Why should you NEVER reuse passwords?",
                "situation": "What\u2019s the risk?",
                "options": [
                    "It\u2019s fine \u2014 one password is easier to remember",
                    "If one site is hacked, ALL your accounts are exposed",
                    "Websites don\u2019t allow it",
                    "It makes your computer slower",
                ],
                "correct": 1,
            },
        ],
    },
    {
        "id": 3,
        "title": "The Secure Key",
        "type": "robot_commands",
        "difficulty": "Medium",
        "xp": 20,
        "description": (
            "To read the Captain\u2019s log, you need to match the \u2018Private "
            "Key\u2019 to the \u2018Encrypted Lock.\u2019 Design your own "
            "encryption system and write a secret message!"
        ),
        "beaver_msg": "Access Granted! Encryption ensures only the right people see the right data.",
        "beaver_hint": "Pick a key number, shift every letter, and write the encrypted version. Then swap with a friend to decrypt!",
        "command_set": [
            "My secret message:",
            "My key number:",
            "Encrypted version:",
            "How to decrypt:",
        ],
        "scenarios": [
            {
                "label": "Create a secret message using a Caesar Cipher with key = +4",
                "hint": "Write your message, then shift every letter forward by 4. A\u2192E, B\u2192F, etc.",
            },
            {
                "label": "Design a stronger cipher: use a different key for odd and even positions",
                "hint": "Example: odd letters shift +2, even letters shift +5. Much harder to crack!",
            },
        ],
        "min_steps": 4,
    },
]

QUIZ = [
    {"question": "What does encryption do?", "options": ["Deletes data", "Scrambles data so only the right person can read it", "Makes files bigger", "Speeds up the computer"], "correct": 1},
    {"question": "In a Caesar Cipher with key +2, what does \u2018AB\u2019 become?", "options": ["CD", "BA", "AC", "ZA"], "correct": 0},
    {"question": "Which password is weakest?", "options": ["Tr0ub4dor&3", "123456", "C@ptain_B3aver!", "Nebula#2026x"], "correct": 1},
    {"question": "Why is encryption important?", "options": ["It makes websites look nice", "It protects private data from hackers", "It\u2019s only for spies", "It isn\u2019t important"], "correct": 1},
]
