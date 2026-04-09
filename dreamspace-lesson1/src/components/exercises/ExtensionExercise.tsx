import { useState, useEffect } from 'react'
import type { StudentExercise } from '@/types/lesson'
import { useLessonStore } from '@/store/lessonStore'
import Card from '@/components/ui/Card'
import PrimaryButton from '@/components/ui/PrimaryButton'

interface Props {
  exercise: StudentExercise
}

export default function ExtensionExercise({ exercise }: Props) {
  const sections = exercise.sections ?? []
  const saveAnswer = useLessonStore((s) => s.saveAnswer)
  const markComplete = useLessonStore((s) => s.markExerciseComplete)
  const saved = useLessonStore((s) => s.exerciseAnswers[exercise.id])

  const initSections: Record<string, string[]> =
    saved?.type === 'extension'
      ? saved.sections
      : Object.fromEntries(sections.map((s) => [s.id, ['']]))

  const [sectionSteps, setSectionSteps] = useState<Record<string, string[]>>(initSections)
  const [submitted, setSubmitted] = useState(false)
  const [open, setOpen] = useState<Record<string, boolean>>(
    Object.fromEntries(sections.map((s, i) => [s.id, i === 0])),
  )

  useEffect(() => {
    saveAnswer(exercise.id, { type: 'extension', sections: sectionSteps })
  }, [sectionSteps, exercise.id, saveAnswer])

  const updateStep = (sectionId: string, idx: number, val: string) => {
    setSectionSteps((prev) => {
      const steps = [...(prev[sectionId] ?? [''])]
      steps[idx] = val
      return { ...prev, [sectionId]: steps }
    })
  }

  const addStep = (sectionId: string) => {
    setSectionSteps((prev) => ({ ...prev, [sectionId]: [...(prev[sectionId] ?? []), ''] }))
  }

  const canSubmit = sections.every((s) =>
    (sectionSteps[s.id] ?? []).some((step) => step.trim().length > 0),
  )

  const handleSubmit = () => {
    if (!canSubmit) return
    markComplete(exercise.id)
    setSubmitted(true)
  }

  return (
    <div style={{ display: 'grid', gap: 14 }}>
      {sections.map((section) => (
        <Card key={section.id}>
          <button
            onClick={() => setOpen((o) => ({ ...o, [section.id]: !o[section.id] }))}
            style={{
              width: '100%',
              display: 'flex',
              justifyContent: 'space-between',
              alignItems: 'center',
              background: 'none',
              border: 'none',
              padding: 0,
              cursor: 'pointer',
              fontFamily: 'var(--font-fredoka)',
            }}
          >
            <span style={{ fontWeight: 700, fontSize: 16, color: 'var(--color-blue-dark)' }}>
              {section.label}
            </span>
            <span style={{ color: 'var(--color-muted)' }}>{open[section.id] ? '▲' : '▼'}</span>
          </button>

          {open[section.id] && (
            <div style={{ marginTop: 12 }}>
              <div style={{ display: 'grid', gap: 8 }}>
                {(sectionSteps[section.id] ?? ['']).map((step, idx) => (
                  <div key={idx} style={{ display: 'flex', gap: 8, alignItems: 'center' }}>
                    <span
                      style={{
                        minWidth: 24,
                        height: 24,
                        borderRadius: 999,
                        background: 'var(--color-purple)',
                        color: '#fff',
                        display: 'grid',
                        placeItems: 'center',
                        fontSize: 12,
                        fontWeight: 700,
                        flexShrink: 0,
                      }}
                    >
                      {idx + 1}
                    </span>
                    <input
                      type="text"
                      className="step-input"
                      placeholder={section.placeholder}
                      value={step}
                      onChange={(e) => updateStep(section.id, idx, e.target.value)}
                      aria-label={`${section.label} step ${idx + 1}`}
                    />
                  </div>
                ))}
              </div>
              <button
                onClick={() => addStep(section.id)}
                style={{
                  marginTop: 10,
                  padding: '7px 14px',
                  borderRadius: 12,
                  border: '2px dashed var(--color-line)',
                  background: 'transparent',
                  color: 'var(--color-muted)',
                  fontSize: 13,
                  cursor: 'pointer',
                  fontFamily: 'var(--font-fredoka)',
                }}
              >
                + Add Step
              </button>
            </div>
          )}
        </Card>
      ))}

      {submitted ? (
        <div className="ds-success-banner">✅ Robot Chef algorithm saved!</div>
      ) : (
        <PrimaryButton onClick={handleSubmit} disabled={!canSubmit}>
          Save Robot Chef Algorithm
        </PrimaryButton>
      )}
    </div>
  )
}
