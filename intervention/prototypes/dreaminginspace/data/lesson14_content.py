"""Lesson 14: How the Internet Works.
Track 4: Digital World | Dreaming in Space.
"""

LESSON_14 = {
    "id": "lesson-14",
    "title": "How the Internet Works",
    "description": (
        "Discover that the internet is a network of connected computers "
        "that send data in tiny packets using addresses and rules."
    ),
    "duration": 45,
    "level": "Beginner",
    "age_group": "Ages 8-18",
    "color": "#d97706",
    "welcome": (
        "When you send a message to a friend, it doesn\u2019t fly through "
        "the air in one piece! It gets broken into tiny packets, labelled "
        "with an address, and sent through a huge network of computers. "
        "Let\u2019s find out how!"
    ),
    "recap_msg": (
        "The internet is a network of networks. Data travels in packets "
        "with addresses. Protocols are the rules everyone follows. Now you "
        "know what happens every time you press Send!"
    ),
}

ROLE_MODEL_14 = {
    "name": "Vint Cerf",
    "years": "1943\u2013present",
    "intro": "Co-inventor of the internet \u2014 he designed TCP/IP, the rules that let all computers talk to each other.",
    "detail": (
        "Vint and his colleague Bob Kahn created the \u2018language\u2019 that "
        "every device on the internet speaks. Without TCP/IP, your phone "
        "couldn\u2019t talk to a server in another country."
    ),
}

VOCABULARY_14 = [
    {"word": "Network", "definition": "A group of connected computers that can share data"},
    {"word": "Packet", "definition": "A small chunk of data sent over the internet with an address label"},
    {"word": "IP Address", "definition": "A unique number that identifies every device on the internet"},
    {"word": "Protocol", "definition": "A set of rules that devices follow to communicate (e.g. HTTP, TCP)"},
]

OBJECTIVES_14 = [
    "Explain how data travels across the internet in packets.",
    "Describe what an IP address and a protocol are.",
    "Identify what happens when something goes wrong (packet loss, wrong address).",
]

EXERCISES_14 = [
    {
        "id": 1,
        "title": "Trace the Packet",
        "type": "read_conditional",
        "difficulty": "Easy",
        "xp": 10,
        "description": "Follow a message as it travels across the internet. Answer questions about each step.",
        "beaver_msg": "Imagine you\u2019re a tiny packet of data zooming through cables and routers!",
        "beaver_hint": "The message gets split into packets, each gets an address, they travel through routers, and reassemble at the destination.",
        "problems": [
            {
                "rule": "You send a photo to your friend.\nStep 1: Photo is split into 50 packets.\nStep 2: Each packet gets your friend\u2019s IP address.\nStep 3: Packets travel through multiple routers.\nStep 4: Packets arrive and reassemble into the photo.",
                "situation": "Why is the photo split into packets?",
                "options": ["To make it smaller", "So different parts can take different routes and arrive faster", "Because computers can only handle tiny files", "It isn\u2019t split"],
                "correct": 1,
            },
            {
                "rule": "Your computer: 192.168.1.5\nSchool router: 10.0.0.1\nGoogle server: 142.250.74.14",
                "situation": "What is 142.250.74.14?",
                "options": ["Your computer\u2019s name", "The school wifi password", "Google\u2019s IP address", "A phone number"],
                "correct": 2,
            },
            {
                "rule": "HTTP = rules for web pages\nHTTPS = secure version (encrypted)\nTCP = rules for reliable delivery",
                "situation": "You\u2019re buying something online. Which protocol should the website use?",
                "options": ["HTTP \u2014 it\u2019s faster", "HTTPS \u2014 it\u2019s encrypted and secure", "TCP only", "No protocol needed"],
                "correct": 1,
            },
        ],
    },
    {
        "id": 2,
        "title": "Address & Send",
        "type": "grouping",
        "difficulty": "Medium",
        "xp": 15,
        "description": "Match each part of the internet to its real-world equivalent.",
        "beaver_msg": "The internet works like the postal system! Let\u2019s match the pieces.",
        "beaver_hint": "IP address = home address, Packet = letter in an envelope, Router = post office, Protocol = postal rules.",
        "task_title": "Match Internet \u2194 Real World",
        "jumbled_steps": [
            {"step": "IP Address", "group": "Home address"},
            {"step": "Data Packet", "group": "Letter in envelope"},
            {"step": "Router", "group": "Post office sorting"},
            {"step": "Protocol (HTTP)", "group": "Postal rules"},
            {"step": "Server", "group": "Library / warehouse"},
            {"step": "Browser", "group": "You opening the letter"},
        ],
        "groups": ["Home address", "Letter in envelope", "Post office sorting", "Postal rules", "Library / warehouse", "You opening the letter"],
    },
    {
        "id": 3,
        "title": "What Could Go Wrong?",
        "type": "bug_hunt",
        "difficulty": "Medium",
        "xp": 20,
        "description": "Three internet problems have occurred. Diagnose each one and suggest a fix.",
        "beaver_msg": "The internet isn\u2019t perfect! Sometimes packets get lost, addresses are wrong, or servers go down.",
        "beaver_hint": "Think about what part of the system failed: the address? the route? the server? the connection?",
        "bugs": [
            {
                "label": "Problem 1 \u2014 Website won\u2019t load",
                "code": "You type www.example.com but get \u201cServer not found.\u201d\nYour wifi is connected.\nOther websites work fine.",
                "hint": "The website\u2019s server might be down, or the domain name (address) could be wrong. What would you check?",
            },
            {
                "label": "Problem 2 \u2014 Video keeps buffering",
                "code": "You\u2019re watching a video but it stops every 10 seconds.\nThe wifi signal shows 2 out of 5 bars.\nOther people in the house are also streaming.",
                "hint": "Not enough bandwidth \u2014 too many devices sharing the connection. Packets arrive too slowly.",
            },
            {
                "label": "Problem 3 \u2014 Email sent to wrong person",
                "code": "You sent a message to alex@school.com\nbut Alex never received it.\nYou check and see you typed aelx@school.com.",
                "hint": "Wrong address! Just like a letter sent to the wrong house. The IP/email address must be exact.",
            },
        ],
    },
]

QUIZ_14 = [
    {"question": "What is a data packet?", "options": ["A big file", "A small chunk of data with an address label", "A type of computer", "A wifi signal"], "correct": 1},
    {"question": "What does an IP address do?", "options": ["Speeds up the internet", "Identifies a device on the network", "Encrypts your data", "Blocks websites"], "correct": 1},
    {"question": "What is HTTPS?", "options": ["A programming language", "A secure protocol for web pages", "A type of computer", "A router"], "correct": 1},
    {"question": "A website won\u2019t load but wifi works. What\u2019s most likely wrong?", "options": ["Your keyboard", "The website\u2019s server is down", "You need a new computer", "The internet doesn\u2019t exist"], "correct": 1},
]
