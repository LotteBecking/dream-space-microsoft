import { create } from 'zustand'
import { persist, createJSONStorage } from 'zustand/middleware'

type WrittenAnswer = { type: 'written'; task: string; steps: string[] }
type SortingAnswer = { type: 'sorting'; order: string[] }
type ExtensionAnswer = { type: 'extension'; sections: Record<string, string[]> }
export type ExerciseAnswer = WrittenAnswer | SortingAnswer | ExtensionAnswer

const TOTAL_EXERCISES = 3

interface LessonState {
  completedExercises: string[]
  exerciseAnswers: Record<string, ExerciseAnswer>
  exitTicketAnswer: string
  simulatorCompleted: boolean
  simulatorConfusionCount: number
  markExerciseComplete: (id: string) => void
  saveAnswer: (id: string, answer: ExerciseAnswer) => void
  setExitTicket: (answer: string) => void
  setSimulatorCompleted: (confusionCount: number) => void
  getProgress: () => number
}

export const useLessonStore = create<LessonState>()(
  persist(
    (set, get) => ({
      completedExercises: [],
      exerciseAnswers: {},
      exitTicketAnswer: '',
      simulatorCompleted: false,
      simulatorConfusionCount: 0,

      markExerciseComplete: (id) =>
        set((s) => ({
          completedExercises: s.completedExercises.includes(id)
            ? s.completedExercises
            : [...s.completedExercises, id],
        })),

      saveAnswer: (id, answer) =>
        set((s) => ({ exerciseAnswers: { ...s.exerciseAnswers, [id]: answer } })),

      setExitTicket: (answer) => set({ exitTicketAnswer: answer }),

      setSimulatorCompleted: (confusionCount) =>
        set({ simulatorCompleted: true, simulatorConfusionCount: confusionCount }),

      getProgress: () => {
        const done = get().completedExercises.length
        return Math.round((done / TOTAL_EXERCISES) * 100)
      },
    }),
    {
      name: 'ds-l1-lesson',
      storage: createJSONStorage(() => localStorage),
    },
  ),
)
