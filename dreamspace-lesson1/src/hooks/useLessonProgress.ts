import { useLessonStore } from '@/store/lessonStore'

export function useLessonProgress() {
  const completedExercises = useLessonStore((s) => s.completedExercises)
  const simulatorCompleted = useLessonStore((s) => s.simulatorCompleted)
  const getProgress = useLessonStore((s) => s.getProgress)

  const isExerciseComplete = (id: string) => completedExercises.includes(id)
  const allExercisesDone = completedExercises.length >= 3
  const progress = getProgress()

  return { completedExercises, simulatorCompleted, isExerciseComplete, allExercisesDone, progress }
}
