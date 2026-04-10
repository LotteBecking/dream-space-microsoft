import { useState, useEffect } from 'react'
import type { StudentExercise } from '@/types/lesson'
import { useLessonStore } from '@/store/lessonStore'
import Card from '@/components/ui/Card'
import PrimaryButton from '@/components/ui/PrimaryButton'

const TASKS = ['Getting ready for school', 'Making chocolate milk', 'Feeding a pet']
const MIN_STEPS = 6

function getStepWarning(text: string): string | null {
  if (!text.trim()) return null
  const words = text.trim().split(/\s+/)
  if (words.length < 3) return 'Can you be more specific?'
  if (/\band\b/i.test(text)) return 'This might be two actions — try splitting it.'
  return null
}

interface Props {
  exercise: StudentExercise
}

export default function WrittenExercise({ exercise }: Props) {
  const saveAnswer = useLessonStore((s) => s.saveAnswer)
  const markComplete = useLessonStore((s) => s.markExerciseComplete)
  const saved = useLessonStore((s) => s.exerciseAnswers[exercise.id])

  const initTask = saved?.type === 'written' ? saved.task : TASKS[0]
  const initSteps = saved?.type === 'written' ? saved.steps : Array(MIN_STEPS).fill('')

  const [task, setTask] = useState(initTask)
  const [steps, setSteps] = useState<string[]>(initSteps.length >= MIN_STEPS ? initSteps : Array(MIN_STEPS).fill(''))
  const [submitted, setSubmitted] = useState(false)

  useEffect(() => {
    saveAnswer(exercise.id, { type: 'written', task, steps })
  }, [task, steps, exercise.id, saveAnswer])

  const updateStep = (i: number, val: string) => {
    const next = [...steps]
    next[i] = val
    setSteps(next)
  }

  const addStep = () => setSteps((s) => [...s, ''])

  const removeStep = (i: number) => {
    if (steps.length <= MIN_STEPS) return
    setSteps((s) => s.filter((_, idx) => idx !== i))
  }

  const filledCount = steps.filter((s) => s.trim().length > 0).length
  const canSubmit = filledCount >= MIN_STEPS

  const handleSubmit = () => {
    if (!canSubmit) return
    markComplete(exercise.id)
    setSubmitted(true)
  }

  return (
    <div style={{ display: 'grid', gap: 16 }}>
      {/* Task selector */}
      <Card>
        <label style={{ fontWeight: 600, fontSize: 15, display: 'block', marginBottom: 8 }}>
          Choose your task:
        </label>
        <div style={{ display: 'grid', gap: 8 }}>
          {TASKS.map((t) => (
            <button
              key={t}
              onClick={() => setTask(t)}
              style={{
                padding: '10px 14px',
                borderRadius: 14,
                border: `2px solid ${task === t ? 'var(--color-blue)' : 'var(--color-line)'}`,
                background: task === t ? '#eef7ff' : '#fff',
                textAlign: 'left',
                fontSize: 15,
                color: 'var(--color-ink)',
                fontFamily: 'var(--font-fredoka)',
                cursor: 'pointer',
              }}
            >
              {t}
            </button>
          ))}
        </div>
      </Card>

      {/* Steps */}
      <Card>
        <div style={{ fontWeight: 600, fontSize: 15, marginBottom: 12 }}>
          Write your algorithm for: <em>{task}</em>
        </div>
        <div style={{ display: 'grid', gap: 10 }}>
          {steps.map((step, i) => {
            const warn = getStepWarning(step)
            return (
              <div key={i} style={{ display: 'flex', gap: 8, alignItems: 'flex-start' }}>
                <span
                  style={{
                    minWidth: 26,
                    height: 26,
                    borderRadius: 999,
                    background: 'var(--color-blue)',
                    color: '#fff',
                    display: 'grid',
                    placeItems: 'center',
                    fontSize: 13,
                    fontWeight: 700,
                    marginTop: 8,
                    flexShrink: 0,
                  }}
                >
                  {i + 1}
                </span>
                <div style={{ flex: 1 }}>
                  <input
                    type="text"
                    className={`step-input${warn ? ' warn' : ''}`}
                    placeholder={`Step ${i + 1} — one action only…`}
                    value={step}
                    onChange={(e) => updateStep(i, e.target.value)}
                    aria-label={`Step ${i + 1}`}
                  />
                  {warn && (
                    <div style={{ fontSize: 12, color: '#8a5b09', marginTop: 3 }}>⚠️ {warn}</div>
                  )}
                </div>
                {steps.length > MIN_STEPS && (
                  <button
                    onClick={() => removeStep(i)}
                    aria-label={`Remove step ${i + 1}`}
                    style={{
                      width: 28,
                      height: 28,
                      borderRadius: 999,
                      border: '1px solid #ddd',
                      background: '#fff',
                      color: '#999',
                      cursor: 'pointer',
                      marginTop: 7,
                      flexShrink: 0,
                    }}
                  >
                    ×
                  </button>
                )}
              </div>
            )
          })}
        </div>

        <button
          onClick={addStep}
          style={{
            marginTop: 12,
            padding: '8px 16px',
            borderRadius: 12,
            border: '2px dashed var(--color-line)',
            background: 'transparent',
            color: 'var(--color-muted)',
            fontSize: 14,
            cursor: 'pointer',
            width: '100%',
            fontFamily: 'var(--font-fredoka)',
          }}
        >
          + Add Step
        </button>

        <div
          style={{
            marginTop: 10,
            fontSize: 13,
            color: filledCount >= MIN_STEPS ? 'var(--color-green-dark)' : 'var(--color-muted)',
          }}
        >
          {filledCount}/{MIN_STEPS} minimum steps filled
        </div>
      </Card>

      {submitted ? (
        <div className="ds-success-banner">
          ✅ Algorithm submitted! You're thinking like a programmer!
        </div>
      ) : (
        <PrimaryButton onClick={handleSubmit} disabled={!canSubmit}>
          Submit Algorithm
        </PrimaryButton>
      )}
    </div>
  )
}
