# Lesson data
lessons = [
    {
        'id': 'lesson-1',
        'title': 'Introduction to Block Coding',
        'description': 'Learn the basics of block-based programming with interactive visual blocks.',
        'duration': 15,
        'level': 'Beginner',
        'videoUrl': 'https://www.youtube.com/embed/MEzGyRb0LnY',
        'objectives': [
            'Understand what coding is',
            'Learn basic programming concepts',
            'Create your first program'
        ],
        'prerequisites': 'None',
        'materials': ['Computer', 'Code blocks environment'],
        'fullDescription': 'This foundational lesson introduces students to the world of coding using visual blocks. Students will learn how code works and create simple programs using drag-and-drop blocks.',
        'teacherGuide': 'Start by explaining what coding is and why it\'s important. Demonstrate how block-based coding works by dragging blocks, then ask students to try it themselves. Monitor progress and provide hints when needed. Celebrate successes to build confidence.',
        'studentExercises': [
            {'id': 'exercise-1-1', 'title': 'Drag Your First Block', 'description': 'Drag a simple block and see what happens', 'difficulty': 'Easy'},
            {'id': 'exercise-1-2', 'title': 'Create a Simple Sequence', 'description': 'Stack 3 blocks in order to create a sequence', 'difficulty': 'Easy'},
            {'id': 'exercise-1-3', 'title': 'Build Your First Program', 'description': 'Create a program that draws a shape', 'difficulty': 'Medium'}
        ]
    },
    {
        'id': 'lesson-2',
        'title': 'Loops & Sequences',
        'description': 'Master loops and sequential programming to create repeating patterns and efficient code.',
        'duration': 20,
        'level': 'Beginner',
        'videoUrl': 'https://www.youtube.com/embed/RMINSD7MmT4',
        'objectives': [
            'Understand loops',
            'Use repeat blocks',
            'Create sequential instructions'
        ],
        'prerequisites': 'Introduction to Block Coding',
        'materials': ['Computer', 'Code blocks environment'],
        'fullDescription': 'Learn how to use loops to repeat actions and create efficient programs. This lesson covers repeat blocks, sequences, and pattern creation.',
        'teacherGuide': 'Introduce the concept of repetition and loops. Show how using a repeat block is more efficient than copying the same block multiple times. Have students practice with simple 2-3 iteration loops, then gradually increase complexity. Visual demonstrations are key for understanding.',
        'studentExercises': [
            {'id': 'exercise-2-1', 'title': 'Create a Simple Loop', 'description': 'Use a repeat block to draw the same shape 4 times', 'difficulty': 'Easy'},
            {'id': 'exercise-2-2', 'title': 'Pattern Creation', 'description': 'Create a repeating pattern using loops', 'difficulty': 'Medium'},
            {'id': 'exercise-2-3', 'title': 'Nested Loops', 'description': 'Use loops within loops to create complex patterns', 'difficulty': 'Hard'}
        ]
    },
    {
        'id': 'lesson-3',
        'title': 'Variables & Data Types',
        'description': 'Explore variables and different data types to store and manipulate information.',
        'duration': 25,
        'level': 'Intermediate',
        'videoUrl': 'https://www.youtube.com/embed/G8hfAePjJv4',
        'objectives': [
            'Understand variables',
            'Learn about data types',
            'Store and retrieve information'
        ],
        'prerequisites': 'Loops & Sequences',
        'materials': ['Computer', 'Code blocks environment', 'Workbook'],
        'fullDescription': 'Dive deeper into programming by learning about variables and different data types. Understand how to store, retrieve, and manipulate data in your programs.',
        'teacherGuide': 'Use real-world analogies to explain variables (containers that hold information). Show how to create variables and change their values. Demonstrate different data types and why they matter. Have students create programs that use multiple variables.',
        'studentExercises': [
            {'id': 'exercise-3-1', 'title': 'Create Your First Variable', 'description': 'Create a variable and set its value', 'difficulty': 'Easy'},
            {'id': 'exercise-3-2', 'title': 'Using Variables', 'description': 'Use variables to store and display information', 'difficulty': 'Medium'},
            {'id': 'exercise-3-3', 'title': 'Building a Simple Program', 'description': 'Create a program that uses multiple variables', 'difficulty': 'Medium'}
        ]
    },
    {
        'id': 'lesson-4',
        'title': 'Conditionals & Decision Making',
        'description': 'Use if-statements and conditionals to make your programs make decisions.',
        'duration': 30,
        'level': 'Intermediate',
        'videoUrl': 'https://www.youtube.com/embed/lAKbCKwdv0s',
        'objectives': [
            'Understand conditional statements',
            'Use if-else blocks',
            'Create decision-making logic'
        ],
        'prerequisites': 'Variables & Data Types',
        'materials': ['Computer', 'Code blocks environment', 'Decision-making worksheet'],
        'fullDescription': 'Learn how to make your programs smart by using conditionals. Teach your code to make decisions based on different conditions.',
        'teacherGuide': 'Start with real-world decision-making examples. Explain if-then logic clearly. Show how to use if-else blocks. Have students debug programs with conditional logic. Emphasize that conditions must be true or false.',
        'studentExercises': [
            {'id': 'exercise-4-1', 'title': 'Simple If Statement', 'description': 'Create a program with a simple if statement', 'difficulty': 'Medium'},
            {'id': 'exercise-4-2', 'title': 'If-Else Logic', 'description': 'Use if-else to create two different outcomes', 'difficulty': 'Medium'},
            {'id': 'exercise-4-3', 'title': 'Game Logic', 'description': 'Create a simple game that uses conditionals', 'difficulty': 'Hard'}
        ]
    },
    {
        'id': 'lesson-5',
        'title': 'Functions & Procedures',
        'description': 'Create reusable blocks of code with functions to organize and simplify your programs.',
        'duration': 25,
        'level': 'Advanced',
        'videoUrl': 'https://www.youtube.com/embed/FOjESLx0fqU',
        'objectives': [
            'Understand functions',
            'Create reusable code blocks',
            'Organize complex programs'
        ],
        'prerequisites': 'Conditionals & Decision Making',
        'materials': ['Computer', 'Code blocks environment', 'Function templates'],
        'fullDescription': 'Master the art of writing reusable code by creating functions. Learn how to organize complex programs into manageable, reusable blocks.',
        'teacherGuide': 'Introduce functions by explaining the concept of reusable code. Show real-life examples of procedures. Demonstrate creating functions with parameters. Have students refactor repetitive code into functions. Emphasize code organization and reusability.',
        'studentExercises': [
            {'id': 'exercise-5-1', 'title': 'Create a Simple Function', 'description': 'Create your first function and call it', 'difficulty': 'Medium'},
            {'id': 'exercise-5-2', 'title': 'Functions with Parameters', 'description': 'Create functions that accept different parameters', 'difficulty': 'Hard'},
            {'id': 'exercise-5-3', 'title': 'Refactor Code', 'description': 'Rewrite repetitive code using functions', 'difficulty': 'Hard'}
        ]
    },
    {
        'id': 'lesson-6',
        'title': 'Debugging & Problem Solving',
        'description': 'Learn systematic approaches to find and fix errors in your code.',
        'duration': 20,
        'level': 'Intermediate',
        'videoUrl': 'https://www.youtube.com/embed/Z6p2TwjKr6g',
        'objectives': [
            'Identify common errors',
            'Use debugging techniques',
            'Solve problems systematically'
        ],
        'prerequisites': 'Loops & Sequences',
        'materials': ['Computer', 'Buggy code examples', 'Debugging checklist'],
        'fullDescription': 'Develop problem-solving skills by learning how to identify and fix errors in code. Understand common mistakes and how to debug programs effectively.',
        'teacherGuide': 'Normalize mistakes and emphasize that debugging is a normal part of programming. Teach systematic debugging techniques like adding print statements and testing small sections. Have students practice fixing buggy programs.',
        'studentExercises': [
            {'id': 'exercise-6-1', 'title': 'Find the Bug', 'description': 'Identify and fix a simple error in provided code', 'difficulty': 'Easy'},
            {'id': 'exercise-6-2', 'title': 'Debug a Program', 'description': 'Debug a more complex program with multiple issues', 'difficulty': 'Medium'},
            {'id': 'exercise-6-3', 'title': 'Problem Solving', 'description': 'Fix a program and improve its efficiency', 'difficulty': 'Hard'}
        ]
    },
    {
        'id': 'lesson-7',
        'title': 'Game Development Basics',
        'description': 'Create simple games using coding concepts and game design principles.',
        'duration': 40,
        'level': 'Advanced',
        'videoUrl': 'https://www.youtube.com/embed/7L7vQHIgKA4',
        'objectives': [
            'Understand game loops',
            'Create interactive gameplay',
            'Design simple games'
        ],
        'prerequisites': 'Functions & Procedures',
        'materials': ['Computer', 'Game development environment', 'Game design template'],
        'fullDescription': 'Bring coding to life by creating simple games. Learn game design principles and how to implement them using code.',
        'teacherGuide': 'Discuss game design fundamentals. Show examples of simple games. Demonstrate the game loop concept. Have students design their own game on paper first. Provide templates to speed up development. Celebrate creative solutions.',
        'studentExercises': [
            {'id': 'exercise-7-1', 'title': 'Create a Simple Game', 'description': 'Build a basic game with one mechanic', 'difficulty': 'Hard'},
            {'id': 'exercise-7-2', 'title': 'Add Game Features', 'description': 'Add scoring and levels to a game', 'difficulty': 'Hard'},
            {'id': 'exercise-7-3', 'title': 'Design Your Game', 'description': 'Create your own original game concept', 'difficulty': 'Expert'}
        ]
    },
    {
        'id': 'lesson-8',
        'title': 'Arrays & Lists',
        'description': 'Work with collections of data using arrays and lists.',
        'duration': 30,
        'level': 'Advanced',
        'videoUrl': 'https://www.youtube.com/embed/xT8qIIJwMzc',
        'objectives': [
            'Understand arrays and lists',
            'Iterate through collections',
            'Manipulate multiple data items'
        ],
        'prerequisites': 'Variables & Data Types',
        'materials': ['Computer', 'Code blocks environment', 'Array examples'],
        'fullDescription': 'Learn to work with collections of data using arrays and lists. Master iteration and manipulation of multiple data items.',
        'teacherGuide': 'Explain arrays as collections of similar items. Show how indexing works. Demonstrate iterating through arrays with loops. Practice common array operations like adding, removing, and searching. Relate arrays to real-world concepts like shopping lists.',
        'studentExercises': [
            {'id': 'exercise-8-1', 'title': 'Create an Array', 'description': 'Create an array and access its elements', 'difficulty': 'Medium'},
            {'id': 'exercise-8-2', 'title': 'Iterate Arrays', 'description': 'Loop through an array and perform operations', 'difficulty': 'Medium'},
            {'id': 'exercise-8-3', 'title': 'Array Manipulation', 'description': 'Create a program that adds, removes, and searches in arrays', 'difficulty': 'Hard'}
        ]
    }
]

def search_lessons(query):
    """Search lessons by title or description"""
    query = query.lower()
    return [l for l in lessons 
            if query in l['title'].lower() 
            or query in l['description'].lower()]

def get_lesson_by_id(lesson_id):
    """Get a lesson by ID"""
    return next((l for l in lessons if l['id'] == lesson_id), None)
