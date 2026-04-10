import { useNavigate } from 'react-router'
import { useLessonProgress } from '@/hooks/useLessonProgress'

interface Props {
  title: string
  backTo?: string
}

export default function StickyHeader({ title, backTo }: Props) {
  const navigate = useNavigate()
  const { progress } = useLessonProgress()

  return (
    <div className="ds-topbar">
      <button
        className="ds-circle-btn"
        onClick={() => (backTo ? navigate(backTo) : navigate(-1))}
        aria-label="Go back"
      >
        ←
      </button>
      <div className="ds-progress-track" role="progressbar" aria-valuenow={progress} aria-valuemin={0} aria-valuemax={100}>
        <span className="ds-progress-fill" style={{ width: `${progress}%` }} />
      </div>
      <span
        style={{
          fontFamily: 'var(--font-silkscreen)',
          fontSize: 11,
          color: 'var(--color-blue-dark)',
          whiteSpace: 'nowrap',
          letterSpacing: '0.05em',
        }}
      >
        {title}
      </span>
    </div>
  )
}
