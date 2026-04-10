import { useNavigate } from 'react-router'
import { motion, AnimatePresence } from 'framer-motion'
import { useSimulatorStore } from '@/store/simulatorStore'
import { useLessonStore } from '@/store/lessonStore'
import type { SandwichState } from '@/services/executionEngine'
import StickyHeader from '@/components/layout/StickyHeader'
import Card from '@/components/ui/Card'
import PrimaryButton from '@/components/ui/PrimaryButton'

const HINTS = [
  'open bread bag',
  'take bread slice',
  'open peanut butter jar',
  'get knife',
  'spread peanut butter',
  'open jam jar',
  'spread jam',
  'place second slice',
  'serve',
]

function KitchenScene({ state }: { state: SandwichState }) {
  return (
    <div
      style={{
        background: 'linear-gradient(180deg,#f0f8ff,#e8f4ff)',
        border: '3px solid var(--color-line)',
        borderRadius: 22,
        padding: 16,
        marginBottom: 16,
      }}
    >
      <div style={{ textAlign: 'center', fontSize: 11, color: 'var(--color-muted)', marginBottom: 10 }}>
        🍳 KITCHEN COUNTER
      </div>
      <div
        style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(5, 1fr)',
          gap: 8,
          justifyItems: 'center',
        }}
      >
        {/* Bread bag */}
        <div className="kitchen-item">
          <motion.div
            className="item-emoji"
            animate={{ scale: state.breadBag === 'open' ? 1.1 : 1 }}
          >
            {state.breadBag === 'open' ? '🍞' : '🛍️'}
          </motion.div>
          <div className="item-label">
            Bread bag<br />{state.breadBag}
          </div>
        </div>
        {/* PB jar */}
        <div className="kitchen-item">
          <motion.div
            className="item-emoji"
            animate={{ rotate: state.pbJar === 'open' ? -15 : 0 }}
          >
            {state.pbJar === 'open' ? '🫙' : '🟤'}
          </motion.div>
          <div className="item-label">PB jar<br />{state.pbJar}</div>
        </div>
        {/* Jam jar */}
        <div className="kitchen-item">
          <motion.div
            className="item-emoji"
            animate={{ rotate: state.jamJar === 'open' ? -15 : 0 }}
          >
            {state.jamJar === 'open' ? '🍓' : '🔴'}
          </motion.div>
          <div className="item-label">Jam jar<br />{state.jamJar}</div>
        </div>
        {/* Knife */}
        <div className="kitchen-item">
          <motion.div
            className="item-emoji"
            animate={{ y: state.knifeLocation === 'hand' ? -6 : 0 }}
          >
            🔪
          </motion.div>
          <div className="item-label">{state.knifeLocation === 'hand' ? 'in hand' : 'on counter'}</div>
        </div>
        {/* Plate */}
        <div className="kitchen-item">
          <div className="item-emoji">
            {state.sandwichComplete
              ? '🥪'
              : state.breadSlices === 2
              ? state.jamApplied
                ? '🍞🍓'
                : state.pbApplied
                ? '🍞🟤'
                : '🍞🍞'
              : state.breadSlices === 1
              ? state.pbApplied
                ? '🟤'
                : '🍞'
              : '🍽️'}
          </div>
          <div className="item-label">plate</div>
        </div>
      </div>

      {/* State summary */}
      <div
        style={{
          marginTop: 10,
          display: 'flex',
          flexWrap: 'wrap',
          gap: 6,
          justifyContent: 'center',
        }}
      >
        {[
          { label: 'PB', done: state.pbApplied },
          { label: 'Jam', done: state.jamApplied },
          { label: '2 slices', done: state.breadSlices >= 2 },
          { label: 'Done!', done: state.sandwichComplete },
        ].map((s) => (
          <span
            key={s.label}
            style={{
              fontSize: 11,
              padding: '3px 8px',
              borderRadius: 999,
              background: s.done ? '#ecfff0' : '#f0f0f0',
              border: `1px solid ${s.done ? 'var(--color-green-dark)' : '#ddd'}`,
              color: s.done ? 'var(--color-green-dark)' : 'var(--color-muted)',
            }}
          >
            {s.done ? '✓' : '○'} {s.label}
          </span>
        ))}
      </div>
    </div>
  )
}

export default function SimulatorScreen() {
  const navigate = useNavigate()
  const {
    inputText, parseError, commands, executionLog,
    engineStatus, sandwichState, confusionCount,
    setInputText, addCommand, removeCommand, clearCommands, runAll, reset,
  } = useSimulatorStore()
  const setSimulatorCompleted = useLessonStore((s) => s.setSimulatorCompleted)

  const handleAddCommand = () => {
    addCommand()
  }

  const handleRunAll = () => {
    runAll()
    if (engineStatus === 'done') {
      setSimulatorCompleted(confusionCount)
    }
  }

  // After runAll, check if done
  const isDone = engineStatus === 'done'
  if (isDone) {
    setSimulatorCompleted(confusionCount)
  }

  return (
    <div className="ds-screen">
      <StickyHeader title="SIMULATOR" backTo="/" />

      <h2 style={{ fontFamily: 'var(--font-silkscreen)', fontSize: 16, color: 'var(--color-blue-dark)', marginBottom: 4 }}>
        PB&amp;J Sandwich Simulator
      </h2>
      <p style={{ fontSize: 13, color: 'var(--color-muted)', marginBottom: 16 }}>
        Type instructions to help the robot make a sandwich. Be precise — robots follow instructions literally!
      </p>

      <KitchenScene state={sandwichState} />

      {/* Command input */}
      <Card style={{ marginBottom: 14 }}>
        <div style={{ fontWeight: 700, fontSize: 14, marginBottom: 8 }}>Add an instruction:</div>
        <div style={{ display: 'flex', gap: 8 }}>
          <input
            type="text"
            className="step-input"
            style={{ flex: 1 }}
            placeholder='e.g. "open bread bag"'
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && handleAddCommand()}
            aria-label="Robot instruction"
          />
          <button
            onClick={handleAddCommand}
            style={{
              padding: '10px 14px',
              borderRadius: 14,
              border: 'none',
              background: 'var(--color-blue)',
              color: '#fff',
              fontFamily: 'var(--font-fredoka)',
              fontWeight: 700,
              cursor: 'pointer',
              whiteSpace: 'nowrap',
            }}
          >
            + Add
          </button>
        </div>
        {parseError && (
          <div style={{ marginTop: 6, fontSize: 12, color: '#c0392b' }}>❓ {parseError}</div>
        )}

        {/* Hint chips */}
        <div style={{ marginTop: 10, display: 'flex', flexWrap: 'wrap', gap: 6 }}>
          {HINTS.map((h) => (
            <button
              key={h}
              onClick={() => setInputText(h)}
              style={{
                fontSize: 11,
                padding: '4px 8px',
                borderRadius: 999,
                border: '1px solid var(--color-line)',
                background: '#f8fcff',
                color: 'var(--color-muted)',
                cursor: 'pointer',
                fontFamily: 'var(--font-fredoka)',
              }}
            >
              {h}
            </button>
          ))}
        </div>
      </Card>

      {/* Command queue */}
      {commands.length > 0 && (
        <Card style={{ marginBottom: 14 }}>
          <div style={{ fontWeight: 700, fontSize: 14, marginBottom: 8 }}>
            My Algorithm ({commands.length} step{commands.length !== 1 ? 's' : ''}):
          </div>
          <div style={{ display: 'grid', gap: 6 }}>
            {commands.map((cmd, i) => (
              <div
                key={cmd.id}
                style={{
                  display: 'flex',
                  gap: 8,
                  alignItems: 'center',
                  padding: '6px 10px',
                  borderRadius: 10,
                  background: '#f8fcff',
                  border: '1px solid var(--color-line)',
                }}
              >
                <span style={{ fontSize: 12, color: 'var(--color-muted)', minWidth: 18 }}>{i + 1}.</span>
                <span style={{ flex: 1, fontSize: 13 }}>{cmd.rawInput}</span>
                <button
                  onClick={() => removeCommand(cmd.id)}
                  aria-label={`Remove step ${i + 1}`}
                  style={{
                    width: 22,
                    height: 22,
                    borderRadius: 999,
                    border: '1px solid #ddd',
                    background: '#fff',
                    color: '#aaa',
                    cursor: 'pointer',
                    fontSize: 12,
                  }}
                >
                  ×
                </button>
              </div>
            ))}
          </div>
        </Card>
      )}

      {/* Controls */}
      <div style={{ display: 'grid', gap: 8, marginBottom: 16 }}>
        <PrimaryButton onClick={handleRunAll} disabled={commands.length === 0}>
          🤖 Run My Algorithm
        </PrimaryButton>
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 8 }}>
          <button className="ds-btn-secondary" onClick={clearCommands}>Clear All</button>
          <button className="ds-btn-secondary" onClick={reset}>Reset Kitchen</button>
        </div>
      </div>

      {/* Execution log */}
      {executionLog.length > 0 && (
        <Card variant="line" style={{ marginBottom: 16 }}>
          <div style={{ fontWeight: 700, fontSize: 14, marginBottom: 10 }}>Robot's Log:</div>
          {confusionCount > 0 && (
            <div style={{ fontSize: 12, color: 'var(--color-muted)', marginBottom: 8, fontStyle: 'italic' }}>
              🤔 Robot got confused {confusionCount} time{confusionCount !== 1 ? 's' : ''} — that's okay! Even Ada Lovelace had to debug.
            </div>
          )}
          <div style={{ display: 'grid', gap: 6 }}>
            <AnimatePresence>
              {executionLog.map((entry) => (
                <motion.div
                  key={entry.stepNumber}
                  className={`log-entry ${entry.result}`}
                  initial={{ y: 10, opacity: 0 }}
                  animate={{ y: 0, opacity: 1 }}
                  transition={{ delay: entry.stepNumber * 0.05 }}
                >
                  <strong>Step {entry.stepNumber}:</strong> {entry.message}
                </motion.div>
              ))}
            </AnimatePresence>
          </div>
        </Card>
      )}

      {/* Success */}
      {isDone && (
        <motion.div
          initial={{ scale: 0.9, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          style={{ marginBottom: 80 }}
        >
          <div className="ds-success-banner" style={{ textAlign: 'center', fontSize: 18 }}>
            🥪 Your algorithm worked!<br />The sandwich is ready!
          </div>
          <div style={{ height: 12 }} />
          <PrimaryButton onClick={() => navigate('/exercise/1')}>
            Continue to Exercise 1 →
          </PrimaryButton>
        </motion.div>
      )}

      <div style={{ height: 80 }} />
    </div>
  )
}
