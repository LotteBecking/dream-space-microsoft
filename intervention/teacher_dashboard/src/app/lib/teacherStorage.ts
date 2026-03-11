export interface TeacherProfile {
  name: string;
  email: string;
  school: string;
  avatar: string;
}

export interface Student {
  id: string;
  name: string;
  avatar: string;
  classId: string;
  progressPercentage: number;
  challengesCompleted: number;
  lessonsCompleted: number;
  lastActivity: string;
  achievements: Achievement[];
  activityHistory: ActivityEntry[];
  teacherNotes: string;
}

export interface Achievement {
  id: string;
  name: string;
  icon: string;
  earnedDate: string;
}

export interface ActivityEntry {
  id: string;
  type: 'lesson' | 'challenge' | 'achievement';
  title: string;
  date: string;
  success: boolean;
}

export interface Class {
  id: string;
  name: string;
  studentCount: number;
  activeAssignments: number;
  engagementRate: number;
  students: string[]; // student IDs
}

export interface Assignment {
  id: string;
  lessonId: string;
  classId: string;
  assignedDate: string;
  dueDate: string;
  completionRate: number;
}

const STORAGE_KEYS = {
  TEACHER_PROFILE: 'teacher_profile',
  CLASSES: 'teacher_classes',
  STUDENTS: 'teacher_students',
  ASSIGNMENTS: 'teacher_assignments',
  LAST_LESSON: 'teacher_last_lesson'
};

// Teacher Profile
export function saveTeacherProfile(profile: TeacherProfile): void {
  localStorage.setItem(STORAGE_KEYS.TEACHER_PROFILE, JSON.stringify(profile));
}

export function getTeacherProfile(): TeacherProfile | null {
  const data = localStorage.getItem(STORAGE_KEYS.TEACHER_PROFILE);
  return data ? JSON.parse(data) : null;
}

// Classes
export function getClasses(): Class[] {
  const data = localStorage.getItem(STORAGE_KEYS.CLASSES);
  if (data) {
    return JSON.parse(data);
  }

  // Default mock classes
  const defaultClasses: Class[] = [
    {
      id: 'class-1',
      name: 'Class 4A',
      studentCount: 24,
      activeAssignments: 3,
      engagementRate: 87,
      students: ['student-1', 'student-2', 'student-3', 'student-4', 'student-5']
    },
    {
      id: 'class-2',
      name: 'Class 4B',
      studentCount: 22,
      activeAssignments: 2,
      engagementRate: 92,
      students: ['student-6', 'student-7', 'student-8', 'student-9']
    },
    {
      id: 'class-3',
      name: 'Class 5A',
      studentCount: 26,
      activeAssignments: 4,
      engagementRate: 78,
      students: ['student-10', 'student-11', 'student-12']
    }
  ];

  localStorage.setItem(STORAGE_KEYS.CLASSES, JSON.stringify(defaultClasses));
  return defaultClasses;
}

export function addClass(newClass: Class): void {
  const classes = getClasses();
  classes.push(newClass);
  localStorage.setItem(STORAGE_KEYS.CLASSES, JSON.stringify(classes));
}

// Students
export function getStudents(): Student[] {
  const data = localStorage.getItem(STORAGE_KEYS.STUDENTS);
  if (data) {
    return JSON.parse(data);
  }

  // Default mock students
  const defaultStudents: Student[] = [
    {
      id: 'student-1',
      name: 'Emma de Vries',
      avatar: '👧',
      classId: 'class-1',
      progressPercentage: 78,
      challengesCompleted: 15,
      lessonsCompleted: 4,
      lastActivity: new Date(Date.now() - 2 * 60 * 60 * 1000).toISOString(),
      achievements: [
        { id: 'ach-1', name: 'Pattern Master', icon: '🎯', earnedDate: new Date(Date.now() - 5 * 24 * 60 * 60 * 1000).toISOString() },
        { id: 'ach-2', name: 'Loop Hero', icon: '🔄', earnedDate: new Date(Date.now() - 3 * 24 * 60 * 60 * 1000).toISOString() }
      ],
      activityHistory: [
        { id: 'act-1', type: 'lesson', title: 'Understanding Loops', date: new Date(Date.now() - 2 * 60 * 60 * 1000).toISOString(), success: true },
        { id: 'act-2', type: 'challenge', title: 'Loop Challenge', date: new Date(Date.now() - 1 * 24 * 60 * 60 * 1000).toISOString(), success: true }
      ],
      teacherNotes: 'Very engaged student, excels at pattern recognition'
    },
    {
      id: 'student-2',
      name: 'Lucas van Berg',
      avatar: '👦',
      classId: 'class-1',
      progressPercentage: 92,
      challengesCompleted: 22,
      lessonsCompleted: 6,
      lastActivity: new Date(Date.now() - 5 * 60 * 60 * 1000).toISOString(),
      achievements: [
        { id: 'ach-1', name: 'Pattern Master', icon: '🎯', earnedDate: new Date(Date.now() - 7 * 24 * 60 * 60 * 1000).toISOString() },
        { id: 'ach-2', name: 'Loop Hero', icon: '🔄', earnedDate: new Date(Date.now() - 6 * 24 * 60 * 60 * 1000).toISOString() },
        { id: 'ach-3', name: 'Variable Wizard', icon: '✨', earnedDate: new Date(Date.now() - 2 * 24 * 60 * 60 * 1000).toISOString() }
      ],
      activityHistory: [
        { id: 'act-3', type: 'lesson', title: 'Variables and Storage', date: new Date(Date.now() - 5 * 60 * 60 * 1000).toISOString(), success: true },
        { id: 'act-4', type: 'achievement', title: 'Variable Wizard', date: new Date(Date.now() - 2 * 24 * 60 * 60 * 1000).toISOString(), success: true }
      ],
      teacherNotes: 'Top performer, helps other students'
    },
    {
      id: 'student-3',
      name: 'Sophie Bakker',
      avatar: '👧',
      classId: 'class-1',
      progressPercentage: 64,
      challengesCompleted: 12,
      lessonsCompleted: 3,
      lastActivity: new Date(Date.now() - 1 * 24 * 60 * 60 * 1000).toISOString(),
      achievements: [
        { id: 'ach-1', name: 'Pattern Master', icon: '🎯', earnedDate: new Date(Date.now() - 4 * 24 * 60 * 60 * 1000).toISOString() }
      ],
      activityHistory: [
        { id: 'act-5', type: 'lesson', title: 'Introduction to Patterns', date: new Date(Date.now() - 1 * 24 * 60 * 60 * 1000).toISOString(), success: true }
      ],
      teacherNotes: 'Needs extra support with conditional logic'
    },
    {
      id: 'student-4',
      name: 'Daan Jansen',
      avatar: '👦',
      classId: 'class-1',
      progressPercentage: 85,
      challengesCompleted: 18,
      lessonsCompleted: 5,
      lastActivity: new Date(Date.now() - 3 * 60 * 60 * 1000).toISOString(),
      achievements: [
        { id: 'ach-1', name: 'Pattern Master', icon: '🎯', earnedDate: new Date(Date.now() - 8 * 24 * 60 * 60 * 1000).toISOString() },
        { id: 'ach-2', name: 'Loop Hero', icon: '🔄', earnedDate: new Date(Date.now() - 5 * 24 * 60 * 60 * 1000).toISOString() }
      ],
      activityHistory: [
        { id: 'act-6', type: 'lesson', title: 'Conditional Logic', date: new Date(Date.now() - 3 * 60 * 60 * 1000).toISOString(), success: true }
      ],
      teacherNotes: 'Creative problem solver'
    },
    {
      id: 'student-5',
      name: 'Lotte Peters',
      avatar: '👧',
      classId: 'class-1',
      progressPercentage: 71,
      challengesCompleted: 14,
      lessonsCompleted: 4,
      lastActivity: new Date(Date.now() - 8 * 60 * 60 * 1000).toISOString(),
      achievements: [
        { id: 'ach-1', name: 'Pattern Master', icon: '🎯', earnedDate: new Date(Date.now() - 6 * 24 * 60 * 60 * 1000).toISOString() },
        { id: 'ach-2', name: 'Loop Hero', icon: '🔄', earnedDate: new Date(Date.now() - 4 * 24 * 60 * 60 * 1000).toISOString() }
      ],
      activityHistory: [
        { id: 'act-7', type: 'challenge', title: 'Loop Builder', date: new Date(Date.now() - 8 * 60 * 60 * 1000).toISOString(), success: true }
      ],
      teacherNotes: 'Consistent progress, attentive in class'
    }
  ];

  localStorage.setItem(STORAGE_KEYS.STUDENTS, JSON.stringify(defaultStudents));
  return defaultStudents;
}

export function getStudentsByClass(classId: string): Student[] {
  const students = getStudents();
  return students.filter(s => s.classId === classId);
}

export function getStudentById(studentId: string): Student | null {
  const students = getStudents();
  return students.find(s => s.id === studentId) || null;
}

export function updateStudentNotes(studentId: string, notes: string): void {
  const students = getStudents();
  const student = students.find(s => s.id === studentId);
  if (student) {
    student.teacherNotes = notes;
    localStorage.setItem(STORAGE_KEYS.STUDENTS, JSON.stringify(students));
  }
}

// Assignments
export function getAssignments(): Assignment[] {
  const data = localStorage.getItem(STORAGE_KEYS.ASSIGNMENTS);
  if (data) {
    return JSON.parse(data);
  }
  return [];
}

export function createAssignment(assignment: Assignment): void {
  const assignments = getAssignments();
  assignments.push(assignment);
  localStorage.setItem(STORAGE_KEYS.ASSIGNMENTS, JSON.stringify(assignments));
}

// Last viewed lesson
export function saveLastLesson(lessonId: string): void {
  localStorage.setItem(STORAGE_KEYS.LAST_LESSON, lessonId);
}

export function getLastLesson(): string | null {
  return localStorage.getItem(STORAGE_KEYS.LAST_LESSON);
}
