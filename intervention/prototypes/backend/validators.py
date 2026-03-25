"""ID-format validators matching the project-wide naming convention.

Regex patterns
--------------
student_id   : ^student-[0-9]+$
class_id     : ^class-[0-9]+$
lesson_id    : ^lesson-[0-9]+$
exercise_id  : ^exercise-[0-9]+-[0-9]+$
assignment_id: ^assign-[0-9]+$
achievement_id: ^ach-[0-9]+$
activity_id  : ^act-[0-9]+$
"""

import re

ID_PATTERNS = {
    'student_id':    re.compile(r'^student-[0-9]+$'),
    'class_id':      re.compile(r'^class-[0-9]+$'),
    'lesson_id':     re.compile(r'^lesson-[0-9]+$'),
    'exercise_id':   re.compile(r'^exercise-[0-9]+-[0-9]+$'),
    'assignment_id': re.compile(r'^assign-[0-9]+$'),
    'achievement_id': re.compile(r'^ach-[0-9]+$'),
    'activity_id':   re.compile(r'^act-[0-9]+$'),
}


def validate_id(value, id_type):
    """Return *True* when *value* matches the expected format for *id_type*."""
    pattern = ID_PATTERNS.get(id_type)
    if pattern is None:
        return False
    return bool(pattern.match(str(value)))


def require_valid_id(value, id_type):
    """Validate and return *value*, or raise ``ValueError``."""
    if not validate_id(value, id_type):
        expected = ID_PATTERNS[id_type].pattern if id_type in ID_PATTERNS else 'unknown'
        raise ValueError(
            f"Invalid {id_type}: '{value}'. Expected format: {expected}"
        )
    return value
