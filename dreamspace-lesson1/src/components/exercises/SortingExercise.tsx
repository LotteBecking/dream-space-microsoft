import { useState, useEffect } from 'react'
import {
  DndContext,
  closestCenter,
  KeyboardSensor,
  PointerSensor,
  useSensor,
  useSensors,
  type DragEndEvent,
} from '@dnd-kit/core'
import {
  SortableContext,
  verticalListSortingStrategy,
  useSortable,
  arrayMove,
  sortableKeyboardCoordinates,
} from '@dnd-kit/sortable'
import { CSS } from '@dnd-kit/utilities'
import { motion, AnimatePresence } from 'framer-motion'
import type { StudentExercise, SortableItem } from '@/types/lesson'
import { useLessonStore } from '@/store/lessonStore'
import Card from '@/components/ui/Card'
import PrimaryButton from '@/components/ui/PrimaryButton'

function shuffle<T>(arr: T[]): T[] {
  const a = [...arr]
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1))
    ;[a[i], a[j]] = [a[j], a[i]]
  }
  return a
}

function SortableCard({
  item,
  result,
}: {
  item: SortableItem
  result: 'correct' | 'wrong' | null
}) {
  const { attributes, listeners, setNodeRef, transform, transition, isDragging } = useSortable({
    id: item.id,
  })

  const style = {
    transform: CSS.Transform.toString(transform),
    transition,
    opacity: isDragging ? 0.5 : 1,
  }

  return (
    <div ref={setNodeRef} style={style} {...attributes}>
      <div
        className={`sort-card${result === 'correct' ? ' correct' : result === 'wrong' ? ' wrong' : ''}`}
      >
        <span
          {...listeners}
          aria-label="drag handle"
          style={{ fontSize: 18, color: 'var(--color-muted)', cursor: 'grab', touchAction: 'none' }}
        >
          ⠿
        </span>
        <span style={{ flex: 1, fontSize: 15 }}>{item.text}</span>
        <AnimatePresence>
          {result && (
            <motion.span
              initial={{ scale: 0 }}
              animate={{ scale: 1 }}
              style={{ fontSize: 18 }}
            >
              {result === 'correct' ? '✅' : '❌'}
            </motion.span>
          )}
        </AnimatePresence>
      </div>
    </div>
  )
}

interface Props {
  exercise: StudentExercise
}

export default function SortingExercise({ exercise }: Props) {
  const items = exercise.sortableItems ?? []
  const saveAnswer = useLessonStore((s) => s.saveAnswer)
  const markComplete = useLessonStore((s) => s.markExerciseComplete)
  const saved = useLessonStore((s) => s.exerciseAnswers[exercise.id])

  const initOrder =
    saved?.type === 'sorting' ? saved.order : shuffle(items.map((i) => i.id))

  const [order, setOrder] = useState<string[]>(initOrder)
  const [results, setResults] = useState<Record<string, 'correct' | 'wrong'> | null>(null)
  const [attempts, setAttempts] = useState(0)
  const [completed, setCompleted] = useState(false)

  const sensors = useSensors(
    useSensor(PointerSensor),
    useSensor(KeyboardSensor, { coordinateGetter: sortableKeyboardCoordinates }),
  )

  useEffect(() => {
    saveAnswer(exercise.id, { type: 'sorting', order })
  }, [order, exercise.id, saveAnswer])

  const orderedItems = order.map((id) => items.find((i) => i.id === id)!).filter(Boolean)

  const handleDragEnd = (event: DragEndEvent) => {
    const { active, over } = event
    if (over && active.id !== over.id) {
      setOrder((ids) => {
        const oldIdx = ids.indexOf(active.id as string)
        const newIdx = ids.indexOf(over.id as string)
        return arrayMove(ids, oldIdx, newIdx)
      })
      setResults(null)
    }
  }

  const checkAnswer = () => {
    setAttempts((a) => a + 1)
    const res: Record<string, 'correct' | 'wrong'> = {}
    orderedItems.forEach((item, i) => {
      res[item.id] = item.position === i + 1 ? 'correct' : 'wrong'
    })
    setResults(res)
    const allCorrect = Object.values(res).every((r) => r === 'correct')
    if (allCorrect) {
      markComplete(exercise.id)
      setCompleted(true)
    }
  }

  const reshuffle = () => {
    setOrder(shuffle(items.map((i) => i.id)))
    setResults(null)
  }

  const correctCount = results ? Object.values(results).filter((r) => r === 'correct').length : 0

  return (
    <div style={{ display: 'grid', gap: 16 }}>
      <Card>
        <div style={{ fontSize: 14, color: 'var(--color-muted)', marginBottom: 12 }}>
          Drag the cards into the correct order, then tap <strong>Check my answer</strong>.
        </div>

        <DndContext sensors={sensors} collisionDetection={closestCenter} onDragEnd={handleDragEnd}>
          <SortableContext items={order} strategy={verticalListSortingStrategy}>
            <div style={{ display: 'grid', gap: 8 }}>
              {orderedItems.map((item) => (
                <SortableCard
                  key={item.id}
                  item={item}
                  result={results ? (results[item.id] ?? null) : null}
                />
              ))}
            </div>
          </SortableContext>
        </DndContext>

        {results && !completed && (
          <div style={{ marginTop: 12, fontSize: 14, color: 'var(--color-muted)' }}>
            {correctCount}/{items.length} in the right spot. Try again!
          </div>
        )}
      </Card>

      {completed ? (
        <div className="ds-success-banner">
          🎉 Perfect sequence! You understand that order matters in algorithms.
          <div style={{ marginTop: 8, fontSize: 13, fontWeight: 400 }}>
            Attempts: {attempts}
          </div>
        </div>
      ) : (
        <div style={{ display: 'grid', gap: 10 }}>
          <PrimaryButton onClick={checkAnswer}>Check my answer</PrimaryButton>
          <button className="ds-btn-secondary" onClick={reshuffle}>
            Shuffle again
          </button>
        </div>
      )}
    </div>
  )
}
