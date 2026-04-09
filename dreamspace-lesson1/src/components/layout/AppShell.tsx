import { Outlet, useLocation } from 'react-router'
import { AnimatePresence, motion } from 'framer-motion'
import BottomNav from './BottomNav'

export default function AppShell() {
  const location = useLocation()

  return (
    <div style={{ minHeight: '100vh', background: 'var(--color-cream)' }}>
      <div className="ds-backdrop" />
      <AnimatePresence mode="wait">
        <motion.div
          key={location.pathname}
          initial={{ x: 30, opacity: 0 }}
          animate={{ x: 0, opacity: 1 }}
          exit={{ x: -30, opacity: 0 }}
          transition={{ duration: 0.2, ease: 'easeOut' }}
        >
          <Outlet />
        </motion.div>
      </AnimatePresence>
      <BottomNav />
    </div>
  )
}
