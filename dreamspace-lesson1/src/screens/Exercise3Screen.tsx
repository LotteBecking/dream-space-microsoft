import lessonData from '@/data/lesson-1.json'
import type { Lesson } from '@/types/lesson'
import StickyHeader from '@/components/layout/StickyHeader'
import SpeechBubble from '@/components/ui/SpeechBubble'
import PixelChip from '@/components/ui/PixelChip'
import ExtensionExercise from '@/components/exercises/ExtensionExercise'

const lesson = lessonData as Lesson
const exercise = lesson.studentExercises[2]

export default function Exercise3Screen() {
  return (
    <div className="ds-screen">
      <StickyHeader title="EXERCISE 3" backTo="/exercise/2" />
      <SpeechBubble>Design a robot chef algorithm — handle allergies and missing ingredients too!</SpeechBubble>
      <div style={{ marginBottom: 12 }}>
        <PixelChip>{exercise.difficulty.toUpperCase()} · {exercise.durationMinutes} MIN</PixelChip>
      </div>
      <h2 style={{ fontFamily: 'var(--font-silkscreen)', fontSize: 15, color: 'var(--color-blue-dark)', marginBottom: 8 }}>
        {exercise.title}
      </h2>
      <p style={{ fontSize: 14, color: 'var(--color-muted)', marginBottom: 16 }}>{exercise.description}</p>
      <ExtensionExercise exercise={exercise} />
      <div style={{ height: 80 }} />
    </div>
  )
}
