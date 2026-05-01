"""World: Build for Good — guided creator sandbox.
Track 5: Digital Missions | Dreaming in Space.
"""

WORLD = {
    "slug": "build-for-good",
    "title": "Build for Good",
    "tagline": "Build something. Test it. Make it better.",
    "description": "Use a template, assemble logic blocks, test your build, and check it's safe before shipping.",
    "color": "#7c3aed",
    "color_light": "#a78bfa",
    "icon": "cpu",
    "ct_skill": "Decomposition",
    "ct_skill_2": "Logic Flow",
    "recap": "You learned how systems are designed in class. Now build one.",
    "badge_name": "Inventor",
    "badge_emoji": "🚀",
    "xp": 75,
    "missions": [
        {
            "id": 1,
            "title": "Choose Your Mission",
            "goal": "Pick a template. Define who it's for and what problem it solves.",
            "phase": "puzzle",
            "type": "template_chooser",
        },
        {
            "id": 2,
            "title": "Build & Test",
            "goal": "Assemble the logic. Run test cases. Fix what breaks.",
            "phase": "fix",
            "type": "builder",
        },
        {
            "id": 3,
            "title": "Safety Check",
            "goal": "Before you ship — check for exclusion, data overreach, and false results.",
            "phase": "twist",
            "type": "safety",
        },
    ],
}

# --- Mission 1: Templates ---
TEMPLATES = [
    {
        "id": "privacy_helper",
        "title": "Privacy Helper",
        "emoji": "🛡️",
        "description": "A tool that checks if an app is asking for too much data.",
        "user": "Anyone downloading a new app",
        "problem": "People often click 'Accept All' without checking what permissions they're granting.",
        "goal": "Warn users when a permission seems unnecessary for the app type.",
        "avoid": "Avoid storing user data. Avoid being too aggressive with warnings.",
        "blocks_needed": ["input", "check_rule", "output_warning", "output_ok"],
        "test_cases": [
            {"input": "Map app asks for location", "expected": "OK", "explanation": "Makes sense"},
            {"input": "Game asks for microphone", "expected": "WARNING", "explanation": "Unusual for a game"},
            {"input": "Notes app asks for full contacts", "expected": "WARNING", "explanation": "Way more than needed"},
        ],
    },
    {
        "id": "rumour_checker",
        "title": "Rumour Checker",
        "emoji": "🔍",
        "description": "A tool that helps you decide whether to share something from your group chat.",
        "user": "Students in a school group chat",
        "problem": "Rumours spread fast when people share without checking.",
        "goal": "Ask a few quick questions and give a recommendation: share, pause, or verify first.",
        "avoid": "Avoid being preachy. Avoid making the final decision for the user.",
        "blocks_needed": ["input", "check_source", "check_date", "output_recommendation"],
        "test_cases": [
            {"input": "Post has no source, all-caps title", "expected": "VERIFY FIRST", "explanation": "Red flags"},
            {"input": "Post from official school account", "expected": "OK TO SHARE", "explanation": "Trusted source"},
            {"input": "Screenshot from unknown account", "expected": "PAUSE", "explanation": "Can't verify"},
        ],
    },
    {
        "id": "wellbeing_check",
        "title": "Wellbeing Check-In",
        "emoji": "💙",
        "description": "A simple daily check-in tool that notices patterns and suggests resources.",
        "user": "Students who want to track how they're feeling",
        "problem": "It's easy to dismiss bad days — but patterns matter.",
        "goal": "Record mood input. Spot if someone has had multiple difficult days. Offer a resource, not a diagnosis.",
        "avoid": "Never diagnose. Never share data without permission. Never make the user feel judged.",
        "blocks_needed": ["input_mood", "store_pattern", "check_pattern", "output_support", "privacy_check"],
        "test_cases": [
            {"input": "Feeling fine today", "expected": "OK — logged", "explanation": "Normal day"},
            {"input": "Bad day — 3rd this week", "expected": "Offer support resource", "explanation": "Pattern detected"},
            {"input": "User asks to delete their data", "expected": "Data deleted immediately", "explanation": "Privacy requirement"},
        ],
    },
    {
        "id": "route_helper",
        "title": "Accessible Route Planner",
        "emoji": "🗺️",
        "description": "A route planner that prioritises accessibility, not just speed.",
        "user": "Wheelchair user or someone with mobility needs",
        "problem": "Standard route planners optimise for speed — but they often suggest routes with stairs or steep inclines.",
        "goal": "Find a route that avoids barriers, even if it takes longer.",
        "avoid": "Never suggest a route with stairs without warning. Prioritise access over speed.",
        "blocks_needed": ["input_start", "input_destination", "filter_barriers", "calculate_route", "output_route"],
        "test_cases": [
            {"input": "Route A: 5 min, has stairs", "expected": "Not recommended — stairs", "explanation": "Barrier present"},
            {"input": "Route B: 9 min, fully flat", "expected": "Recommended", "explanation": "Accessible option"},
            {"input": "No accessible route found", "expected": "Alert: no accessible route — suggest alternatives", "explanation": "Edge case"},
        ],
    },
]

# --- Logic Blocks available for building ---
ALL_BLOCKS = [
    # Input blocks
    {"id": "input", "category": "Input", "label": "User Input", "icon": "📥", "description": "Take input from the user", "color": "#3b82f6"},
    {"id": "input_mood", "category": "Input", "label": "Mood Input", "icon": "😊", "description": "Ask user how they're feeling", "color": "#3b82f6"},
    {"id": "input_start", "category": "Input", "label": "Start Location", "icon": "📍", "description": "Ask for start point", "color": "#3b82f6"},
    {"id": "input_destination", "category": "Input", "label": "Destination", "icon": "🏁", "description": "Ask for end point", "color": "#3b82f6"},

    # Decision blocks
    {"id": "check_rule", "category": "Decision", "label": "Check Rule", "icon": "⚖️", "description": "Apply a rule to the input", "color": "#8b5cf6"},
    {"id": "check_source", "category": "Decision", "label": "Check Source", "icon": "🔍", "description": "Evaluate if source is verified", "color": "#8b5cf6"},
    {"id": "check_date", "category": "Decision", "label": "Check Date", "icon": "📅", "description": "Is this recent information?", "color": "#8b5cf6"},
    {"id": "check_pattern", "category": "Decision", "label": "Check Pattern", "icon": "📊", "description": "Look for patterns over time", "color": "#8b5cf6"},
    {"id": "filter_barriers", "category": "Decision", "label": "Filter Barriers", "icon": "🚧", "description": "Remove routes with accessibility barriers", "color": "#8b5cf6"},
    {"id": "privacy_check", "category": "Decision", "label": "Privacy Check", "icon": "🔒", "description": "Check if data handling is appropriate", "color": "#8b5cf6"},

    # Process blocks
    {"id": "store_pattern", "category": "Repeat", "label": "Store & Track", "icon": "💾", "description": "Save data to find patterns", "color": "#f59e0b"},
    {"id": "calculate_route", "category": "Repeat", "label": "Calculate", "icon": "🔄", "description": "Run calculation or algorithm", "color": "#f59e0b"},

    # Output blocks
    {"id": "output_warning", "category": "Output", "label": "Warning", "icon": "⚠️", "description": "Show a warning to the user", "color": "#ef4444"},
    {"id": "output_ok", "category": "Output", "label": "All Clear", "icon": "✅", "description": "Tell the user it looks fine", "color": "#10b981"},
    {"id": "output_recommendation", "category": "Output", "label": "Recommendation", "icon": "💡", "description": "Give a suggested action", "color": "#10b981"},
    {"id": "output_support", "category": "Output", "label": "Support Resource", "icon": "💙", "description": "Offer a helpful resource link", "color": "#10b981"},
    {"id": "output_route", "category": "Output", "label": "Show Route", "icon": "🗺️", "description": "Display the recommended route", "color": "#10b981"},
]

# --- Mission 3: Safety Check Questions ---
SAFETY_CHECKS = [
    {
        "id": "exclusion",
        "question": "Could this tool exclude or disadvantage any group of users?",
        "icon": "👥",
        "options": [
            {"id": "no", "label": "No — it works equally for everyone", "prompt": "Think carefully — is there any group who might not be able to use it, or who it might not work as well for?"},
            {"id": "yes_fixed", "label": "Yes — but I've designed around it", "prompt": "Good awareness. Describe what you've done to address it."},
            {"id": "yes_unsolved", "label": "Yes — and it's still a problem", "prompt": "Honest. What would you need to fix in version 2?"},
            {"id": "unsure", "label": "Not sure", "prompt": "That's okay — uncertainty is honest. What test would help you find out?"},
        ],
    },
    {
        "id": "data",
        "question": "Does this tool collect more data than it needs?",
        "icon": "📊",
        "options": [
            {"id": "no", "label": "No — it only collects what's necessary", "prompt": "Great data minimisation. What's the minimum it truly needs?"},
            {"id": "yes_reduced", "label": "I reduced it during building", "prompt": "Good. What did you remove?"},
            {"id": "yes_problem", "label": "Yes — it asks for too much", "prompt": "Important to catch this. What can you remove in version 2?"},
        ],
    },
    {
        "id": "wrong_output",
        "question": "What happens if your tool gives a wrong result?",
        "icon": "⚠️",
        "options": [
            {"id": "low_risk", "label": "Low risk — no big harm if it's wrong", "prompt": "Why is it low risk? Being specific helps."},
            {"id": "medium_risk", "label": "Medium risk — could confuse or mislead", "prompt": "What safeguard could you add to reduce this?"},
            {"id": "high_risk", "label": "High risk — wrong result could cause real harm", "prompt": "High-risk outputs need a human review step or a clear disclaimer. What would you add?"},
        ],
    },
    {
        "id": "version2",
        "question": "What is ONE thing you'd improve in version 2?",
        "icon": "🚀",
        "type": "open_text",
        "placeholder": "e.g. 'I'd add a way for users to give feedback when the tool gets it wrong'",
        "min_length": 10,
    },
]
