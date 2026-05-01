"""World: Fair Future Lab — system-testing lab game.
Track 5: Digital Missions | Dreaming in Space.
"""

WORLD = {
    "slug": "fair-future",
    "title": "Fair Future Lab",
    "tagline": "Change the rule. See what happens.",
    "description": "Test automated systems, spot unfairness, and repair the rules — but know when to escalate.",
    "color": "#0d9488",
    "color_light": "#2dd4bf",
    "icon": "sliders",
    "ct_skill": "Abstraction",
    "ct_skill_2": "Rule Testing",
    "recap": "You learned about algorithmic fairness in class. Now run the experiments.",
    "badge_name": "Lab Scientist",
    "badge_emoji": "🔬",
    "xp": 75,
    "missions": [
        {
            "id": 1,
            "title": "Run the System",
            "goal": "Watch the rule process inputs. Spot which rule causes unfair output.",
            "phase": "puzzle",
            "type": "pipeline",
        },
        {
            "id": 2,
            "title": "Repair Lab",
            "goal": "Change one rule. Compare before and after. Is it fairer now?",
            "phase": "fix",
            "type": "repair",
        },
        {
            "id": 3,
            "title": "The Hard Case",
            "goal": "Some outputs need a human — not an algorithm. Know when to escalate.",
            "phase": "twist",
            "type": "escalation",
        },
    ],
}

# --- Mission 1 & 2: Pipeline Systems ---
SYSTEMS = [
    {
        "id": "club_selection",
        "title": "School Club Selection System",
        "context": "A school uses an automated system to select students for the science club. Let's run it and see what happens.",
        "description": "The system reviews applications and decides who gets in.",
        "inputs": [
            {"name": "Amir", "emoji": "👦", "grade": "B", "essay_score": 7, "extracurricular": True, "note": "First-year student, strong essay"},
            {"name": "Priya", "emoji": "👧", "grade": "A", "essay_score": 8, "extracurricular": False, "note": "Top grades, focused student"},
            {"name": "Jake", "emoji": "👦", "grade": "C", "essay_score": 9, "extracurricular": True, "note": "Average grades but exceptional essay"},
            {"name": "Sofia", "emoji": "👧", "grade": "A", "essay_score": 6, "extracurricular": True, "note": "Great grades and sports captain"},
        ],
        "broken_rule": {
            "name": "Grade Filter",
            "description": "IF grade is NOT A → automatically rejected",
            "problem": "This rule rejects students before reading their essay or other qualities.",
        },
        "broken_outputs": [
            {"name": "Amir", "emoji": "👦", "result": "REJECTED", "reason": "Grade B — filtered out", "fair": False},
            {"name": "Priya", "emoji": "👧", "result": "ACCEPTED", "reason": "Grade A", "fair": True},
            {"name": "Jake", "emoji": "👦", "result": "REJECTED", "reason": "Grade C — filtered out", "fair": False},
            {"name": "Sofia", "emoji": "👧", "result": "ACCEPTED", "reason": "Grade A", "fair": True},
        ],
        "issue": "Amir and Jake have strong essays and extracurricular involvement — but they never get considered. The rule is too blunt.",
        "fix_options": [
            {
                "id": "remove_grade",
                "label": "Remove the grade filter entirely — assess all applicants",
                "rule_change": "All applicants reviewed on essay + involvement",
                "outputs": [
                    {"name": "Amir", "emoji": "👦", "result": "REVIEWED", "reason": "Essay 7/10 + extracurricular", "fair": True},
                    {"name": "Priya", "emoji": "👧", "result": "REVIEWED", "reason": "Essay 8/10, Grade A", "fair": True},
                    {"name": "Jake", "emoji": "👦", "result": "REVIEWED", "reason": "Essay 9/10 + extracurricular", "fair": True},
                    {"name": "Sofia", "emoji": "👧", "result": "REVIEWED", "reason": "Essay 6/10 + Grade A", "fair": True},
                ],
                "verdict": "Fairer — everyone gets considered. Not perfect (still needs a human reviewer).",
                "better": True,
            },
            {
                "id": "lower_grade",
                "label": "Lower grade threshold to C or above",
                "rule_change": "IF grade is NOT C or above → rejected",
                "outputs": [
                    {"name": "Amir", "emoji": "👦", "result": "REVIEWED", "reason": "Grade B meets new threshold", "fair": True},
                    {"name": "Priya", "emoji": "👧", "result": "REVIEWED", "reason": "Grade A", "fair": True},
                    {"name": "Jake", "emoji": "👦", "result": "REVIEWED", "reason": "Grade C meets new threshold", "fair": True},
                    {"name": "Sofia", "emoji": "👧", "result": "REVIEWED", "reason": "Grade A", "fair": True},
                ],
                "verdict": "More balanced — but still uses grade as a filter. Helps here, but could still exclude valid applicants.",
                "better": True,
            },
            {
                "id": "add_essay_weight",
                "label": "Add rule: high essay score (8+) overrides grade filter",
                "rule_change": "IF essay ≥ 8 → advance regardless of grade",
                "outputs": [
                    {"name": "Amir", "emoji": "👦", "result": "REJECTED", "reason": "Essay 7, Grade B — doesn't meet either threshold", "fair": False},
                    {"name": "Priya", "emoji": "👧", "result": "ACCEPTED", "reason": "Grade A + Essay 8", "fair": True},
                    {"name": "Jake", "emoji": "👦", "result": "ACCEPTED", "reason": "Essay 9 — override applied", "fair": True},
                    {"name": "Sofia", "emoji": "👧", "result": "ACCEPTED", "reason": "Grade A", "fair": True},
                ],
                "verdict": "Fairer for Jake — but Amir is still excluded despite a good overall profile. More balanced, not perfect.",
                "better": True,
            },
        ],
        "escalation_note": "Even the best rule here can't fully replace a human reviewer who reads the full application. Some decisions need human judgment.",
    },
    {
        "id": "loan_approval",
        "title": "Youth Grant Approval System",
        "context": "A community organisation uses an algorithm to approve small grants for student projects. Let's test it.",
        "description": "The system processes applications and outputs: Approved, Review, or Rejected.",
        "inputs": [
            {"name": "Keiko", "emoji": "👧", "postcode": "EC1", "project_score": 8, "school_type": "state", "note": "Strong project, state school"},
            {"name": "Marcus", "emoji": "👦", "postcode": "SW3", "project_score": 7, "school_type": "private", "note": "Good project, private school"},
            {"name": "Fatima", "emoji": "👧", "postcode": "E13", "project_score": 9, "school_type": "state", "note": "Excellent project, lower-income area"},
            {"name": "Leo", "emoji": "👦", "postcode": "W1", "project_score": 6, "school_type": "private", "note": "Average project, wealthy area"},
        ],
        "broken_rule": {
            "name": "Postcode Weighting",
            "description": "Applications from postcodes SW and W get +2 bonus points",
            "problem": "This rule gives higher-income areas a scoring advantage, which systematically disadvantages applicants from lower-income areas.",
        },
        "broken_outputs": [
            {"name": "Keiko", "emoji": "👧", "result": "REVIEW", "reason": "Score: 8 (no bonus)", "fair": False},
            {"name": "Marcus", "emoji": "👦", "result": "APPROVED", "reason": "Score: 9 (7 + SW bonus)", "fair": False},
            {"name": "Fatima", "emoji": "👧", "result": "APPROVED", "reason": "Score: 9 (no bonus, genuinely high)", "fair": True},
            {"name": "Leo", "emoji": "👦", "result": "APPROVED", "reason": "Score: 8 (6 + W bonus)", "fair": False},
        ],
        "issue": "Marcus and Leo's lower project scores are boosted by a postcode bonus — systematically favouring already-privileged applicants.",
        "fix_options": [
            {
                "id": "remove_postcode",
                "label": "Remove the postcode bonus entirely",
                "rule_change": "Score based on project quality only",
                "outputs": [
                    {"name": "Keiko", "emoji": "👧", "result": "APPROVED", "reason": "Score: 8 — now competitive", "fair": True},
                    {"name": "Marcus", "emoji": "👦", "result": "REVIEW", "reason": "Score: 7 — no bonus", "fair": True},
                    {"name": "Fatima", "emoji": "👧", "result": "APPROVED", "reason": "Score: 9 — highest", "fair": True},
                    {"name": "Leo", "emoji": "👦", "result": "REVIEW", "reason": "Score: 6 — no bonus", "fair": True},
                ],
                "verdict": "Much fairer. Project quality is what matters for a community grant — not where you live.",
                "better": True,
            },
            {
                "id": "reverse_bonus",
                "label": "Reverse the bonus: give +2 to lower-income postcodes instead",
                "rule_change": "Postcodes E, N, SE get +2 bonus points",
                "outputs": [
                    {"name": "Keiko", "emoji": "👧", "result": "APPROVED", "reason": "Score: 10 (8 + EC bonus)", "fair": True},
                    {"name": "Marcus", "emoji": "👦", "result": "REVIEW", "reason": "Score: 7 — no bonus", "fair": True},
                    {"name": "Fatima", "emoji": "👧", "result": "APPROVED", "reason": "Score: 11 (9 + E bonus)", "fair": True},
                    {"name": "Leo", "emoji": "👦", "result": "REVIEW", "reason": "Score: 6 — no bonus", "fair": True},
                ],
                "verdict": "This actively tries to correct existing inequality. Fairer in one way — but still uses a blunt postcode rule. Is postcode really the right proxy?",
                "better": True,
            },
            {
                "id": "human_review",
                "label": "Route all borderline applications to a human reviewer",
                "rule_change": "Scores 6–8 go to human review panel",
                "outputs": [
                    {"name": "Keiko", "emoji": "👧", "result": "HUMAN REVIEW", "reason": "Score 8 — borderline", "fair": True},
                    {"name": "Marcus", "emoji": "👦", "result": "HUMAN REVIEW", "reason": "Score 7 — borderline", "fair": True},
                    {"name": "Fatima", "emoji": "👧", "result": "APPROVED", "reason": "Score 9 — clearly strong", "fair": True},
                    {"name": "Leo", "emoji": "👦", "result": "HUMAN REVIEW", "reason": "Score 6 — borderline", "fair": True},
                ],
                "verdict": "Good approach. Automation handles clear cases; humans handle the grey areas. This is often the right architecture.",
                "better": True,
            },
        ],
        "escalation_note": "Some decisions are too important to automate fully. A grant affecting a student's opportunity deserves human oversight in close cases.",
    },
]

# --- Mission 3: Escalation Scenarios ---
ESCALATION_SCENARIOS = [
    {
        "id": "content_moderation",
        "title": "Content Moderation Flag",
        "context": "An automated content filter flags a student's history essay about a difficult historical event as 'inappropriate content'.",
        "rule_triggered": "IF post contains [list of flagged words] → auto-remove",
        "question": "What should happen next?",
        "options": [
            {
                "id": "auto_remove",
                "label": "Auto-remove it — rules are rules",
                "verdict": "Too blunt",
                "feedback": "Automated word lists can't understand context. A history essay discussing difficult events is very different from harmful content. Auto-removal without review causes real harm to students.",
                "correct": False,
            },
            {
                "id": "human_review",
                "label": "Send to a human reviewer before any action",
                "verdict": "Right approach",
                "feedback": "Correct. Context matters enormously here. A human reviewer can distinguish between a history essay and genuinely harmful content.",
                "correct": True,
            },
            {
                "id": "ignore_flag",
                "label": "Ignore the flag — the student's work should be protected",
                "verdict": "Too simple",
                "feedback": "Ignoring all flags defeats the purpose of moderation. The answer is human review, not ignoring flags entirely.",
                "correct": False,
            },
            {
                "id": "improve_rule",
                "label": "Improve the rule to understand context better",
                "verdict": "Good longer-term fix",
                "feedback": "Eventually yes — but right now this specific student needs their work reviewed fairly. Immediate action + longer-term rule improvement.",
                "correct": True,
            },
        ],
        "best": "human_review",
        "key_lesson": "Automated systems can't fully understand context. The more sensitive the decision, the more important human oversight becomes.",
    },
    {
        "id": "scholarship_tie",
        "title": "Scholarship Tie-Breaker",
        "context": "Two students have identical scores for a scholarship. The algorithm can't decide. A rule says: 'If tied, prefer the applicant from a more prestigious school.'",
        "question": "Should the algorithm apply the tie-breaker rule?",
        "options": [
            {
                "id": "apply_rule",
                "label": "Yes — apply the rule as programmed",
                "verdict": "Problematic",
                "feedback": "The tie-breaker rule encodes existing advantage. 'More prestigious school' often correlates with wealth, not merit. Automating this decision could entrench inequality.",
                "correct": False,
            },
            {
                "id": "send_to_human",
                "label": "Send both applications to a human committee",
                "verdict": "Best option",
                "feedback": "Correct. Tie-breaking in high-stakes decisions like scholarships deserves human judgment — not automated rules that might reinforce existing inequality.",
                "correct": True,
            },
            {
                "id": "random_select",
                "label": "Randomly select between the two",
                "verdict": "Arguably fairer than the rule",
                "feedback": "Better than applying a biased rule — but high-stakes decisions still benefit from human review rather than randomness.",
                "correct": False,
            },
            {
                "id": "award_both",
                "label": "Award the scholarship to both students",
                "verdict": "Creative but unrealistic",
                "feedback": "Nice idea — but usually there's one scholarship. The real answer is: this decision needs humans.",
                "correct": False,
            },
        ],
        "best": "send_to_human",
        "key_lesson": "When automated rules would encode bias or advantage, the right answer is often: send it to a human. Not every decision should be automated.",
    },
]
