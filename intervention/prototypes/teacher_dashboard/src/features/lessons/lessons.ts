export type DifficultyLevel = 'beginner' | 'intermediate' | 'advanced';
export type AgeGroup = '8-10' | '10-12' | '12-15' | '15-18';
export type Topic = 'patterns' | 'logic' | 'algorithms' | 'loops' | 'variables' | 'conditionals' | 'functions' | 'data-structures' | 'recursion' | 'optimization';

export interface Lesson {
  id: string;
  title: string;
  description: string;
  videoUrl: string;
  thumbnailUrl: string;
  duration: number; // in minutes
  difficulty: DifficultyLevel;
  ageGroup: AgeGroup;
  topic: Topic;
  learningObjectives: string[];
  teacherInstructions: {
    setup: string;
    steps: string[];
    discussionPrompts: string[];
    tips: string[];
  };
  studentExercises: {
    title: string;
    description: string;
    type: 'coding' | 'quiz' | 'project';
    difficulty: DifficultyLevel;
  }[];
  curriculumAlignment: string[];
}

export const lessons: Lesson[] = [
  {
    id: 'lesson-1',
    title: 'Introduction to Patterns',
    description: 'Learn how to recognize and create patterns in code',
    videoUrl: 'https://www.youtube.com/embed/dQw4w9WgXcQ',
    thumbnailUrl: 'https://images.unsplash.com/photo-1516116216624-53e697fedbea?w=400&h=225&fit=crop',
    duration: 15,
    difficulty: 'beginner',
    ageGroup: '8-10',
    topic: 'patterns',
    learningObjectives: [
      'Identify repeating patterns in sequences',
      'Create simple patterns using shapes and colors',
      'Understand how patterns relate to loops in programming'
    ],
    teacherInstructions: {
      setup: 'Prepare colorful blocks or printed pattern cards for hands-on activities',
      steps: [
        'Start with the video introduction (5 min)',
        'Do a physical pattern activity with blocks (5 min)',
        'Discuss how patterns exist in nature and daily life (3 min)',
        'Guide students through the coding exercise (10 min)'
      ],
      discussionPrompts: [
        'Where do you see patterns in your daily life?',
        'What makes a pattern a pattern?',
        'How could patterns help us write less code?'
      ],
      tips: [
        'Use real-world examples that students can relate to',
        'Encourage students to create their own patterns',
        'Connect patterns to music or art for deeper engagement'
      ]
    },
    studentExercises: [
      {
        title: 'Pattern Creator',
        description: 'Create your own pattern using emojis',
        type: 'coding',
        difficulty: 'beginner'
      },
      {
        title: 'Pattern Quiz',
        description: 'Identify the next item in various patterns',
        type: 'quiz',
        difficulty: 'beginner'
      }
    ],
    curriculumAlignment: ['SLO Digital Literacy 1.2', 'Computational Thinking Level 1']
  },
  {
    id: 'lesson-2',
    title: 'Understanding Loops',
    description: 'Discover how loops help us repeat actions efficiently',
    videoUrl: 'https://www.youtube.com/embed/dQw4w9WgXcQ',
    thumbnailUrl: 'https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=400&h=225&fit=crop',
    duration: 20,
    difficulty: 'beginner',
    ageGroup: '8-10',
    topic: 'loops',
    learningObjectives: [
      'Understand the concept of repetition in programming',
      'Identify when to use loops in problem-solving',
      'Create simple loops to automate repetitive tasks'
    ],
    teacherInstructions: {
      setup: 'Have the video ready and prepare simple loop examples on the board',
      steps: [
        'Watch the introduction video together (7 min)',
        'Demonstrate a physical loop activity (walk in circles) (3 min)',
        'Explain loop syntax using visual diagrams (5 min)',
        'Guide through the interactive loop exercise (8 min)'
      ],
      discussionPrompts: [
        'What activities do you repeat every day?',
        'How do loops save time when coding?',
        'Can you think of a situation where a loop would never end?'
      ],
      tips: [
        'Use hand motions to represent loop iterations',
        'Start with very simple examples',
        'Show the difference between doing something once vs. in a loop'
      ]
    },
    studentExercises: [
      {
        title: 'Loop Builder',
        description: 'Build loops to draw patterns',
        type: 'coding',
        difficulty: 'beginner'
      },
      {
        title: 'Loop Challenge',
        description: 'Solve problems using loops',
        type: 'quiz',
        difficulty: 'beginner'
      }
    ],
    curriculumAlignment: ['SLO Digital Literacy 2.1', 'Computational Thinking Level 2']
  },
  {
    id: 'lesson-3',
    title: 'Variables and Storage',
    description: 'Learn how to store and use information in your programs',
    videoUrl: 'https://www.youtube.com/embed/dQw4w9WgXcQ',
    thumbnailUrl: 'https://images.unsplash.com/photo-1515879218367-8466d910aaa4?w=400&h=225&fit=crop',
    duration: 25,
    difficulty: 'intermediate',
    ageGroup: '10-12',
    topic: 'variables',
    learningObjectives: [
      'Understand what variables are and why they are useful',
      'Create and modify variables in code',
      'Use variables to make programs more flexible'
    ],
    teacherInstructions: {
      setup: 'Prepare boxes and labels to demonstrate variable storage',
      steps: [
        'Start with the video explanation (8 min)',
        'Use physical boxes to demonstrate variable storage (5 min)',
        'Show how variables change during program execution (7 min)',
        'Practice with the interactive exercises (10 min)'
      ],
      discussionPrompts: [
        'What would happen if we couldn\'t store information?',
        'How is a variable like a labeled box?',
        'Why might we want to change a variable\'s value?'
      ],
      tips: [
        'Use relatable examples like game scores or player names',
        'Emphasize the difference between variable names and values',
        'Show common mistakes and how to fix them'
      ]
    },
    studentExercises: [
      {
        title: 'Variable Practice',
        description: 'Create and manipulate variables',
        type: 'coding',
        difficulty: 'intermediate'
      },
      {
        title: 'Variable Game',
        description: 'Build a simple game using variables',
        type: 'project',
        difficulty: 'intermediate'
      }
    ],
    curriculumAlignment: ['SLO Digital Literacy 3.1', 'Computational Thinking Level 3']
  },
  {
    id: 'lesson-4',
    title: 'Conditional Logic',
    description: 'Make decisions in code using if-then-else statements',
    videoUrl: 'https://www.youtube.com/embed/dQw4w9WgXcQ',
    thumbnailUrl: 'https://images.unsplash.com/photo-1517694712202-14dd9538aa97?w=400&h=225&fit=crop',
    duration: 30,
    difficulty: 'intermediate',
    ageGroup: '12-15',
    topic: 'conditionals',
    learningObjectives: [
      'Understand how programs make decisions',
      'Write conditional statements using if-else',
      'Combine multiple conditions using logical operators'
    ],
    teacherInstructions: {
      setup: 'Prepare flowchart materials and decision tree examples',
      steps: [
        'Watch the video introduction (10 min)',
        'Create a decision flowchart together (8 min)',
        'Demonstrate if-else syntax with live coding (7 min)',
        'Students practice with guided exercises (12 min)'
      ],
      discussionPrompts: [
        'How do you make decisions in everyday life?',
        'What happens when a condition is true vs. false?',
        'Can you think of situations with multiple conditions?'
      ],
      tips: [
        'Use everyday scenarios like weather decisions',
        'Draw flowcharts before writing code',
        'Practice reading conditions in plain language first'
      ]
    },
    studentExercises: [
      {
        title: 'Decision Maker',
        description: 'Write programs that make decisions',
        type: 'coding',
        difficulty: 'intermediate'
      },
      {
        title: 'Logic Puzzle',
        description: 'Solve complex conditional puzzles',
        type: 'quiz',
        difficulty: 'intermediate'
      }
    ],
    curriculumAlignment: ['SLO Digital Literacy 4.2', 'Computational Thinking Level 4']
  },
  {
    id: 'lesson-5',
    title: 'Functions and Modularity',
    description: 'Organize code into reusable functions',
    videoUrl: 'https://www.youtube.com/embed/dQw4w9WgXcQ',
    thumbnailUrl: 'https://images.unsplash.com/photo-1461749280684-dccba630e2f6?w=400&h=225&fit=crop',
    duration: 30,
    difficulty: 'advanced',
    ageGroup: '12-15',
    topic: 'functions',
    learningObjectives: [
      'Understand the purpose of functions in programming',
      'Create functions with parameters and return values',
      'Organize code using modular design principles'
    ],
    teacherInstructions: {
      setup: 'Prepare recipe cards as function analogies',
      steps: [
        'Start with the video lesson (10 min)',
        'Use recipe analogy to explain functions (5 min)',
        'Demonstrate function creation and calling (8 min)',
        'Guide students through function exercises (12 min)'
      ],
      discussionPrompts: [
        'Why is it useful to package code into functions?',
        'How are functions like recipes?',
        'What makes a good function?'
      ],
      tips: [
        'Start with very simple functions without parameters',
        'Emphasize the DRY principle (Don\'t Repeat Yourself)',
        'Show how functions make code easier to read and maintain'
      ]
    },
    studentExercises: [
      {
        title: 'Function Builder',
        description: 'Create your own useful functions',
        type: 'coding',
        difficulty: 'advanced'
      },
      {
        title: 'Calculator Project',
        description: 'Build a calculator using functions',
        type: 'project',
        difficulty: 'advanced'
      }
    ],
    curriculumAlignment: ['SLO Digital Literacy 5.1', 'Computational Thinking Level 5']
  },
  {
    id: 'lesson-6',
    title: 'Introduction to Algorithms',
    description: 'Learn what algorithms are and how to design them',
    videoUrl: 'https://www.youtube.com/embed/dQw4w9WgXcQ',
    thumbnailUrl: 'https://images.unsplash.com/photo-1542831371-29b0f74f9713?w=400&h=225&fit=crop',
    duration: 35,
    difficulty: 'advanced',
    ageGroup: '15-18',
    topic: 'algorithms',
    learningObjectives: [
      'Define what an algorithm is',
      'Analyze algorithm efficiency',
      'Design algorithms to solve specific problems'
    ],
    teacherInstructions: {
      setup: 'Prepare sorting cards and algorithm visualization tools',
      steps: [
        'Watch the comprehensive video (12 min)',
        'Perform physical sorting algorithm activity (8 min)',
        'Discuss algorithm efficiency and Big O notation (10 min)',
        'Practice designing algorithms (10 min)'
      ],
      discussionPrompts: [
        'What makes one algorithm better than another?',
        'How do algorithms impact our daily digital experiences?',
        'Can you think of a problem that needs an algorithm to solve?'
      ],
      tips: [
        'Use physical demonstrations for sorting algorithms',
        'Connect to real-world applications like search engines',
        'Encourage students to design their own algorithms'
      ]
    },
    studentExercises: [
      {
        title: 'Algorithm Design',
        description: 'Design an algorithm for a specific problem',
        type: 'coding',
        difficulty: 'advanced'
      },
      {
        title: 'Sorting Challenge',
        description: 'Implement and compare sorting algorithms',
        type: 'project',
        difficulty: 'advanced'
      }
    ],
    curriculumAlignment: ['SLO Digital Literacy 6.1', 'Computational Thinking Level 6']
  },
  {
    id: 'lesson-7',
    title: 'Data Structures Basics',
    description: 'Explore different ways to organize and store data',
    videoUrl: 'https://www.youtube.com/embed/dQw4w9WgXcQ',
    thumbnailUrl: 'https://images.unsplash.com/photo-1504868584819-f8e8b4b6d7e3?w=400&h=225&fit=crop',
    duration: 30,
    difficulty: 'advanced',
    ageGroup: '15-18',
    topic: 'data-structures',
    learningObjectives: [
      'Understand different types of data structures',
      'Choose appropriate data structures for specific problems',
      'Implement basic data structures like arrays and lists'
    ],
    teacherInstructions: {
      setup: 'Prepare visual aids showing different data structures',
      steps: [
        'Begin with the video introduction (10 min)',
        'Use visual diagrams to explain structures (8 min)',
        'Demonstrate array and list operations (7 min)',
        'Students practice with exercises (10 min)'
      ],
      discussionPrompts: [
        'Why do we need different data structures?',
        'What are the trade-offs between different structures?',
        'How does data organization affect program performance?'
      ],
      tips: [
        'Use physical containers to represent different structures',
        'Start with arrays before moving to more complex structures',
        'Show real-world examples of where each structure is used'
      ]
    },
    studentExercises: [
      {
        title: 'Data Structure Explorer',
        description: 'Work with different data structures',
        type: 'coding',
        difficulty: 'advanced'
      },
      {
        title: 'Contact Book Project',
        description: 'Build a contact book using appropriate data structures',
        type: 'project',
        difficulty: 'advanced'
      }
    ],
    curriculumAlignment: ['SLO Digital Literacy 6.2', 'Computational Thinking Level 6']
  },
  {
    id: 'lesson-8',
    title: 'Recursion Fundamentals',
    description: 'Understand how functions can call themselves',
    videoUrl: 'https://www.youtube.com/embed/dQw4w9WgXcQ',
    thumbnailUrl: 'https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?w=400&h=225&fit=crop',
    duration: 35,
    difficulty: 'advanced',
    ageGroup: '15-18',
    topic: 'recursion',
    learningObjectives: [
      'Understand the concept of recursive functions',
      'Identify base cases and recursive cases',
      'Solve problems using recursive thinking'
    ],
    teacherInstructions: {
      setup: 'Prepare Russian nesting dolls or mirrors for recursion demonstration',
      steps: [
        'Watch the video with recursion examples (12 min)',
        'Demonstrate recursion using physical props (8 min)',
        'Draw recursion tree diagrams together (8 min)',
        'Practice with simple recursive problems (12 min)'
      ],
      discussionPrompts: [
        'How is recursion different from loops?',
        'Why do we need a base case?',
        'What happens if we forget the base case?'
      ],
      tips: [
        'Start with very simple examples like countdown',
        'Draw call stack diagrams to visualize recursion',
        'Warn about infinite recursion and stack overflow'
      ]
    },
    studentExercises: [
      {
        title: 'Recursive Problems',
        description: 'Solve classic recursive problems',
        type: 'coding',
        difficulty: 'advanced'
      },
      {
        title: 'Fractal Art',
        description: 'Create fractal patterns using recursion',
        type: 'project',
        difficulty: 'advanced'
      }
    ],
    curriculumAlignment: ['SLO Digital Literacy 7.1', 'Computational Thinking Level 7']
  }
];

export function getLessonsByDifficulty(difficulty: DifficultyLevel): Lesson[] {
  return lessons.filter(l => l.difficulty === difficulty);
}

export function getLessonsByAgeGroup(ageGroup: AgeGroup): Lesson[] {
  return lessons.filter(l => l.ageGroup === ageGroup);
}

export function getLessonsByTopic(topic: Topic): Lesson[] {
  return lessons.filter(l => l.topic === topic);
}

export function searchLessons(query: string): Lesson[] {
  const lowerQuery = query.toLowerCase();
  return lessons.filter(l => 
    l.title.toLowerCase().includes(lowerQuery) ||
    l.description.toLowerCase().includes(lowerQuery) ||
    l.topic.toLowerCase().includes(lowerQuery)
  );
}
