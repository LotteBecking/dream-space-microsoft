import { useState } from 'react'
import { useLessonProgress } from '@/hooks/useLessonProgress'
import StickyHeader from '@/components/layout/StickyHeader'
import SpeechBubble from '@/components/ui/SpeechBubble'
import Card from '@/components/ui/Card'
import PrimaryButton from '@/components/ui/PrimaryButton'

const COMBOS = [
  { breadType: 'rye', spreadA: 'hummus', spreadB: 'cucumber' },
  { breadType: 'sourdough', spreadA: 'butter', spreadB: 'cheese' },
]

export default function ChallengeScreen() {
  const { allExercisesDone } = useLessonProgress()

  const [inputs, setInputs] = useState({ breadType: '', spreadA: '', spreadB: '' })
  const [steps, setSteps] = useState([''])
  const [testCombo, setTestCombo] = useState<0 | 1 | null>(null)

  const updateInput = (key: keyof typeof inputs, val: string) =>
    setInputs((prev) => ({ ...prev, [key]: val }))

  const updateStep = (i: number, val: string) => {
    const next = [...steps]
    next[i] = val
    setSteps(next)
  }

  const addStep = () => setSteps((s) => [...s, ''])

  const substituteStep = (step: string, combo: { breadType: string; spreadA: string; spreadB: string }) =>
    step
      .replace(/BREAD_TYPE/gi, combo.breadType || inputs.breadType || 'BREAD_TYPE')
      .replace(/SPREAD_A/gi, combo.spreadA || inputs.spreadA || 'SPREAD_A')
      .replace(/SPREAD_B/gi, combo.spreadB || inputs.spreadB || 'SPREAD_B')

  if (!allExercisesDone) {
    return (
      <div className="ds-screen">
        <StickyHeader title="CHALLENGE" backTo="/exercise/3" />
        <div
          style={{
            textAlign: 'center',
            padding: '40px 20px',
            color: 'var(--color-muted)',
          }}
        >
          <div style={{ fontSize: 48 }}>🔒</div>
          <h2
            style={{
              fontFamily: 'var(--font-silkscreen)',
              fontSize: 16,
              color: 'var(--color-locked)',
              margin: '16px 0 8px',
            }}
          >
            LOCKED
          </h2>
          <p style={{ fontSize: 14 }}>Complete all 3 exercises to unlock the challenge.</p>
        </div>
      </div>
    )
  }

  return (
    <div className="ds-screen">
      <StickyHeader title="CHALLENGE" backTo="/exercise/3" />
      <SpeechBubble>
        Can you write one algorithm that works for ANY sandwich? Use placeholders!
      </SpeechBubble>

      <h2
        style={{
          fontFamily: 'var(--font-silkscreen)',
          fontSize: 14,
          color: 'var(--color-blue-dark)',
          marginBottom: 16,
        }}
      >
        One Algorithm for Any Sandwich
      </h2>

      {/* Input definitions */}
      <Card style={{ marginBottom: 14 }}>
        <div style={{ fontWeight: 700, fontSize: 14, marginBottom: 10 }}>Define your inputs:</div>
        {(['breadType', 'spreadA', 'spreadB'] as const).map((key) => (
          <div key={key} style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 8 }}>
            <span
              style={{
                fontFamily: 'var(--font-silkscreen)',
                fontSize: 11,
                color: 'var(--color-blue-dark)',
                minWidth: 80,
              }}
            >
              {key.toUpperCase()}:
            </span>
            <input
              type="text"
              className="step-input"
              style={{ flex: 1 }}
              placeholder={
                key === 'breadType' ? 'e.g. white, rye' : key === 'spreadA' ? 'e.g. peanut butter' : 'e.g. jam'
              }
              value={inputs[key]}
              onChange={(e) => updateInput(key, e.target.value)}
            />
          </div>
        ))}
      </Card>

      {/* Algorithm steps */}
      <Card style={{ marginBottom: 14 }}>
        <div style={{ fontWeight: 700, fontSize: 14, marginBottom: 4 }}>Your reusable algorithm:</div>
        <div style={{ fontSize: 12, color: 'var(--color-muted)', marginBottom: 10 }}>
          Use BREAD_TYPE, SPREAD_A, SPREAD_B as placeholders in your steps.
        </div>
        <div style={{ display: 'grid', gap: 8 }}>
          {steps.map((step, i) => (
            <div key={i} style={{ display: 'flex', gap: 8, alignItems: 'center' }}>
              <span
                style={{
                  minWidth: 22,
                  height: 22,
                  borderRadius: 999,
                  background: 'var(--color-purple)',
                  color: '#fff',
                  display: 'grid',
                  placeItems: 'center',
                  fontSize: 11,
                  fontWeight: 700,
                  flexShrink: 0,
                }}
              >
                {i + 1}
              </span>
              <input
                type="text"
                className="step-input"
                placeholder="e.g. spread SPREAD_A on BREAD_TYPE slice"
                value={step}
                onChange={(e) => updateStep(i, e.target.value)}
              />
            </div>
          ))}
        </div>
        <button
          onClick={addStep}
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
            width: '100%',
          }}
        >
          + Add Step
        </button>
      </Card>

      {/* Test combos */}
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 10, marginBottom: 14 }}>
        {COMBOS.map((combo, idx) => (
          <button
            key={idx}
            onClick={() => setTestCombo(idx as 0 | 1)}
            style={{
              padding: '10px 8px',
              borderRadius: 16,
              border: `2px solid ${testCombo === idx ? 'var(--color-blue)' : 'var(--color-line)'}`,
              background: testCombo === idx ? '#eef7ff' : '#fff',
              cursor: 'pointer',
              fontFamily: 'var(--font-fredoka)',
              fontSize: 13,
              color: 'var(--color-ink)',
            }}
          >
            Test Combo {idx + 1}<br />
            <span style={{ fontSize: 11, color: 'var(--color-muted)' }}>
              {combo.breadType} / {combo.spreadA} / {combo.spreadB}
            </span>
          </button>
        ))}
      </div>

      {testCombo !== null && steps.some((s) => s.trim()) && (
        <Card variant="line" style={{ marginBottom: 16 }}>
          <div style={{ fontWeight: 700, fontSize: 13, marginBottom: 8 }}>
            Result with Combo {testCombo + 1}:
          </div>
          <div style={{ display: 'grid', gap: 6 }}>
            {steps.filter((s) => s.trim()).map((step, i) => (
              <div key={i} style={{ fontSize: 13, padding: '6px 10px', borderRadius: 10, background: '#f8fcff' }}>
                <span style={{ color: 'var(--color-muted)', marginRight: 6 }}>{i + 1}.</span>
                <span
                  dangerouslySetInnerHTML={{
                    __html: substituteStep(step, COMBOS[testCombo]).replace(
                      /(rye|sourdough|hummus|cucumber|butter|cheese|peanut butter|jam)/gi,
                      '<strong style="color:var(--color-purple)">$1</strong>',
                    ),
                  }}
                />
              </div>
            ))}
          </div>
        </Card>
      )}

      <PrimaryButton onClick={() => alert('Challenge complete! Great generalisation!')}>
        Submit Challenge
      </PrimaryButton>
      <div style={{ height: 80 }} />
    </div>
  )
}
