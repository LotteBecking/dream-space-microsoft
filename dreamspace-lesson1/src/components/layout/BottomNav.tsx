import { useNavigate, useLocation } from 'react-router'

const NAV_ITEMS = [
  { label: 'Lesson', icon: '🏠', path: '/' },
  { label: 'Simulator', icon: '🤖', path: '/simulator' },
  { label: 'Exercises', icon: '📝', path: '/exercise/1' },
  { label: 'Challenge', icon: '🏆', path: '/challenge' },
  { label: 'Review', icon: '📖', path: '/review' },
]

export default function BottomNav() {
  const navigate = useNavigate()
  const { pathname } = useLocation()

  const isActive = (path: string) => {
    if (path === '/') return pathname === '/'
    if (path === '/exercise/1') return pathname.startsWith('/exercise')
    return pathname === path
  }

  return (
    <nav className="bottom-nav" aria-label="Main navigation">
      <div className="bottom-nav-inner">
        {NAV_ITEMS.map((item) => (
          <button
            key={item.path}
            className={`nav-btn${isActive(item.path) ? ' active' : ''}`}
            onClick={() => navigate(item.path)}
            aria-current={isActive(item.path) ? 'page' : undefined}
          >
            <span style={{ fontSize: 18 }}>{item.icon}</span>
            {item.label}
          </button>
        ))}
      </div>
    </nav>
  )
}
