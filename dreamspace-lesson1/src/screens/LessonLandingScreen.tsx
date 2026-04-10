import { useState } from 'react'
import { useNavigate } from 'react-router'
import { motion, AnimatePresence } from 'framer-motion'
import lessonData from '@/data/lesson-1.json'
import type { Lesson } from '@/types/lesson'
import SpeechBubble from '@/components/ui/SpeechBubble'
import PixelChip from '@/components/ui/PixelChip'
import Card from '@/components/ui/Card'
import VocabCard from '@/components/ui/VocabCard'
import PrimaryButton from '@/components/ui/PrimaryButton'
import { useLessonProgress } from '@/hooks/useLessonProgress'

const lesson = lessonData as Lesson

export default function LessonLandingScreen() {
  const navigate = useNavigate()
  const { progress } = useLessonProgress()
  const [objectivesOpen, setObjectivesOpen] = useState(false)

  return (
    <div className="ds-screen">
      <SpeechBubble>
        Today we learn to think like Ada Lovelace — the world's first programmer! 🤖
      </SpeechBubble>

      <div style={{ marginBottom: 16 }}>
        <PixelChip>LESSON 1</PixelChip>
      </div>

      {/* Title */}
      <h1
        style={{
          fontFamily: 'var(--font-silkscreen)',
          fontSize: 18,
          color: 'var(--color-blue-dark)',
          lineHeight: 1.3,
          marginBottom: 6,
        }}
      >
        {lesson.title}
      </h1>
      <p style={{ color: 'var(--color-muted)', fontSize: 14, marginBottom: 20 }}>
        {lesson.description}
      </p>

      {/* Progress */}
      <Card style={{ marginBottom: 16 }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: 14, marginBottom: 6 }}>
          <span>Progress</span>
          <span style={{ color: 'var(--color-blue-dark)', fontWeight: 600 }}>{progress}%</span>
        </div>
        <div className="ds-progress-track">
          <span className="ds-progress-fill" style={{ width: `${progress}%` }} />
        </div>
      </Card>

      {/* Role model */}
      <Card style={{ marginBottom: 16, background: 'linear-gradient(135deg,#f2ebff,#eef7ff)' }}>
        <div style={{ display: 'flex', gap: 12, alignItems: 'center' }}>
          <div
            style={{
              width: 54,
              height: 54,
              borderRadius: 18,
              background: 'var(--color-purple)',
              display: 'grid',
              placeItems: 'center',
              fontSize: 28,
              flexShrink: 0,
            }}
          >
            👩‍💻
          </div>
          <div>
            <div style={{ fontWeight: 700, fontSize: 16 }}>{lesson.roleModelOfDay.name}</div>
            <div style={{ fontSize: 12, color: 'var(--color-muted)' }}>{lesson.roleModelOfDay.years}</div>
            <div style={{ fontSize: 13, color: 'var(--color-ink)', marginTop: 4, lineHeight: 1.4 }}>
              {lesson.roleModelOfDay.intro}
            </div>
          </div>
        </div>
      </Card>

      {/* Vocabulary grid */}
      <div style={{ marginBottom: 6 }}>
        <div style={{ fontWeight: 700, fontSize: 16, marginBottom: 12 }}>Key Words</div>
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 10 }}>
          {lesson.vocabulary.map((v) => (
            <VocabCard key={v.word} {...v} />
          ))}
        </div>
      </div>

      {/* Learning objectives accordion */}
      <Card style={{ margin: '16px 0' }} variant="line">
        <button
          onClick={() => setObjectivesOpen((o) => !o)}
          style={{
            width: '100%',
            display: 'flex',
            justifyContent: 'space-between',
            background: 'none',
            border: 'none',
            cursor: 'pointer',
            fontFamily: 'var(--font-fredoka)',
            fontSize: 15,
            fontWeight: 700,
            color: 'var(--color-ink)',
            padding: 0,
          }}
        >
          🎯 What you'll learn
          <span>{objectivesOpen ? '▲' : '▼'}</span>
        </button>
        <AnimatePresence>
          {objectivesOpen && (
            <motion.ul
              initial={{ height: 0, opacity: 0 }}
              animate={{ height: 'auto', opacity: 1 }}
              exit={{ height: 0, opacity: 0 }}
              transition={{ duration: 0.2 }}
              style={{ margin: '10px 0 0 18px', padding: 0, overflow: 'hidden' }}
            >
              {lesson.learningObjectives.map((obj, i) => (
                <li key={i} style={{ fontSize: 14, color: 'var(--color-muted)', marginBottom: 6, lineHeight: 1.4 }}>
                  {obj}
                </li>
              ))}
            </motion.ul>
          )}
        </AnimatePresence>
      </Card>

      {/* Spacer for fixed footer */}
      <div style={{ height: 80 }} />

      {/* Fixed CTA */}
      <div className="ds-footer-cta">
        <div className="ds-footer-cta-inner">
          <PrimaryButton onClick={() => navigate('/simulator')}>
            Start the Simulator →
          </PrimaryButton>
        </div>
      </div>
    </div>
  )
}
