import { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import lessonData from '@/data/lesson-1.json'
import type { Lesson } from '@/types/lesson'
import { useLessonStore } from '@/store/lessonStore'
import { useLessonProgress } from '@/hooks/useLessonProgress'
import StickyHeader from '@/components/layout/StickyHeader'
import VocabCard from '@/components/ui/VocabCard'
import Card from '@/components/ui/Card'
import PrimaryButton from '@/components/ui/PrimaryButton'

const lesson = lessonData as Lesson

export default function VocabReviewScreen() {
  const setExitTicket = useLessonStore((s) => s.setExitTicket)
  const simulatorConfusionCount = useLessonStore((s) => s.simulatorConfusionCount)
  const { completedExercises, progress } = useLessonProgress()

  const [ticketA, setTicketA] = useState('')
  const [ticketB, setTicketB] = useState('')
  const [submitted, setSubmitted] = useState(false)

  const handleSubmit = () => {
    setExitTicket(`precise/exact because computers cannot: ${ticketB || '…'}`)
    setSubmitted(true)
  }

  return (
    <div className="ds-screen">
      <StickyHeader title="REVIEW" backTo="/challenge" />

      <h2
        style={{
          fontFamily: 'var(--font-silkscreen)',
          fontSize: 16,
          color: 'var(--color-blue-dark)',
          marginBottom: 16,
        }}
      >
        Vocab Review
      </h2>

      {/* Vocab flip cards */}
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 10, marginBottom: 20 }}>
        {lesson.vocabulary.map((v) => (
          <VocabCard key={v.word} {...v} />
        ))}
      </div>

      {/* Exit ticket */}
      <Card style={{ marginBottom: 16 }}>
        <div style={{ fontWeight: 700, fontSize: 15, marginBottom: 12 }}>Exit Ticket</div>
        <p style={{ fontSize: 14, color: 'var(--color-muted)', marginBottom: 14, lineHeight: 1.5 }}>
          An algorithm needs to be{' '}
          <input
            type="text"
            placeholder="______"
            value={ticketA}
            onChange={(e) => setTicketA(e.target.value)}
            style={{
              display: 'inline-block',
              width: 100,
              border: 'none',
              borderBottom: '2px solid var(--color-blue)',
              background: 'transparent',
              fontSize: 14,
              fontFamily: 'var(--font-fredoka)',
              color: 'var(--color-ink)',
              padding: '2px 4px',
              outline: 'none',
            }}
            aria-label="First blank"
          />{' '}
          because computers cannot{' '}
          <input
            type="text"
            placeholder="______"
            value={ticketB}
            onChange={(e) => setTicketB(e.target.value)}
            style={{
              display: 'inline-block',
              width: 100,
              border: 'none',
              borderBottom: '2px solid var(--color-blue)',
              background: 'transparent',
              fontSize: 14,
              fontFamily: 'var(--font-fredoka)',
              color: 'var(--color-ink)',
              padding: '2px 4px',
              outline: 'none',
            }}
            aria-label="Second blank"
          />
          .
        </p>

        {!submitted ? (
          <PrimaryButton onClick={handleSubmit} disabled={!ticketA.trim() || !ticketB.trim()}>
            Submit Exit Ticket
          </PrimaryButton>
        ) : (
          <div className="ds-success-banner">
            Thanks! Great reflection. 🌟
          </div>
        )}
      </Card>

      {/* Completion celebration */}
      <AnimatePresence>
        {submitted && (
          <motion.div
            initial={{ scale: 0.8, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            transition={{ type: 'spring', stiffness: 260, damping: 20 }}
          >
            <Card
              style={{
                textAlign: 'center',
                background: 'linear-gradient(135deg,#eef7ff,#f2ebff)',
                marginBottom: 16,
              }}
            >
              <div style={{ fontSize: 48 }}>🥪🤖🎉</div>
              <h2
                style={{
                  fontFamily: 'var(--font-silkscreen)',
                  fontSize: 18,
                  color: 'var(--color-blue-dark)',
                  margin: '12px 0 8px',
                }}
              >
                Lesson 1 Complete!
              </h2>

              <div style={{ display: 'grid', gap: 8, margin: '16px 0', textAlign: 'left' }}>
                <div
                  style={{
                    display: 'flex',
                    justifyContent: 'space-between',
                    fontSize: 14,
                    padding: '8px 12px',
                    borderRadius: 12,
                    background: 'rgba(255,255,255,0.7)',
                  }}
                >
                  <span>Exercises done</span>
                  <strong>{completedExercises.length}/3</strong>
                </div>
                <div
                  style={{
                    display: 'flex',
                    justifyContent: 'space-between',
                    fontSize: 14,
                    padding: '8px 12px',
                    borderRadius: 12,
                    background: 'rgba(255,255,255,0.7)',
                  }}
                >
                  <span>Overall progress</span>
                  <strong>{progress}%</strong>
                </div>
                {simulatorConfusionCount > 0 && (
                  <div
                    style={{
                      display: 'flex',
                      justifyContent: 'space-between',
                      fontSize: 14,
                      padding: '8px 12px',
                      borderRadius: 12,
                      background: 'rgba(255,255,255,0.7)',
                    }}
                  >
                    <span>Robot confusions</span>
                    <strong>{simulatorConfusionCount} (great debugging!)</strong>
                  </div>
                )}
              </div>

              <PrimaryButton onClick={() => window.scrollTo({ top: 0, behavior: 'smooth' })}>
                Back to Start
              </PrimaryButton>
            </Card>
          </motion.div>
        )}
      </AnimatePresence>

      <div style={{ height: 80 }} />
    </div>
  )
}
