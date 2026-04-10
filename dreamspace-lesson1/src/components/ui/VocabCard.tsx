import { useState } from 'react'
import type { VocabWord } from '@/types/lesson'

const ICONS: Record<string, string> = {
  Algorithm: '📋',
  Input: '📥',
  Output: '📤',
  Sequence: '🔢',
}

export default function VocabCard({ word, def }: VocabWord) {
  const [flipped, setFlipped] = useState(false)

  return (
    <div
      role="button"
      tabIndex={0}
      aria-label={`Vocabulary card: ${word}. Press to flip.`}
      onClick={() => setFlipped((f) => !f)}
      onKeyDown={(e) => (e.key === 'Enter' || e.key === ' ') && setFlipped((f) => !f)}
      style={{ height: 120, cursor: 'pointer', perspective: 800 }}
    >
      <div className={`vocab-card-inner${flipped ? ' flipped' : ''}`}>
        {/* Front */}
        <div
          className="vocab-card-face ds-card"
          style={{ background: 'rgba(255,255,255,0.96)', textAlign: 'center' }}
        >
          <div style={{ fontSize: 28 }}>{ICONS[word] ?? '💡'}</div>
          <div
            style={{
              fontFamily: 'var(--font-silkscreen)',
              fontSize: 13,
              color: 'var(--color-blue-dark)',
              marginTop: 6,
              lineHeight: 1.2,
            }}
          >
            {word}
          </div>
          <div style={{ fontSize: 10, color: 'var(--color-muted)', marginTop: 4 }}>tap to flip</div>
        </div>
        {/* Back */}
        <div
          className="vocab-card-face vocab-card-back ds-card"
          style={{ background: '#eef7ff', textAlign: 'center' }}
        >
          <div style={{ fontSize: 13, color: 'var(--color-ink)', lineHeight: 1.4 }}>{def}</div>
        </div>
      </div>
    </div>
  )
}
