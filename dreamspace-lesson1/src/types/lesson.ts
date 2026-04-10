export type ExerciseType = 'Written' | 'Sorting' | 'Extension'
export type Difficulty = 'Easy' | 'Medium' | 'Hard'

export interface VocabWord {
  word: string
  def: string
}

export interface RoleModel {
  name: string
  years: string
  intro: string
}

export interface SortableItem {
  id: string
  text: string
  position: number
}

export interface ExerciseSection {
  id: string
  label: string
  placeholder: string
}

export interface StudentExercise {
  id: string
  title: string
  description: string
  type: ExerciseType
  difficulty: Difficulty
  durationMinutes: number
  displayMode: string
  materials: string[]
  instructions: string[]
  successCriteria: string[]
  sortableItems?: SortableItem[]
  sections?: ExerciseSection[]
}

export interface StudentChallenge {
  id: string
  title: string
  description: string
  type: string
  difficulty: Difficulty
  durationMinutes: number
  displayMode: string
  materials: string[]
  instructions: string[]
  successCriteria: string[]
}

export interface Lesson {
  id: string
  title: string
  description: string
  duration: number
  level: string
  ageGroup: string
  roleModelOfDay: RoleModel
  vocabulary: VocabWord[]
  learningObjectives: string[]
  materials: string[]
  studentExercises: StudentExercise[]
  studentChallenges: StudentChallenge[]
}
