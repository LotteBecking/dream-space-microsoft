import { create } from 'zustand'
import type { Command, LogEntry, SandwichState } from '@/services/executionEngine'
import {
  INITIAL_SANDWICH_STATE,
  runSequence,
  parseCommand,
} from '@/services/executionEngine'

type EngineStatus = 'idle' | 'running' | 'done' | 'error'

interface SimulatorState {
  inputText: string
  parseError: string | null
  commands: Command[]
  executionLog: LogEntry[]
  engineStatus: EngineStatus
  sandwichState: SandwichState
  confusionCount: number
  setInputText: (t: string) => void
  addCommand: () => void
  removeCommand: (id: string) => void
  clearCommands: () => void
  runAll: () => void
  reset: () => void
}

export const useSimulatorStore = create<SimulatorState>((set, get) => ({
  inputText: '',
  parseError: null,
  commands: [],
  executionLog: [],
  engineStatus: 'idle',
  sandwichState: { ...INITIAL_SANDWICH_STATE },
  confusionCount: 0,

  setInputText: (t) => set({ inputText: t, parseError: null }),

  addCommand: () => {
    const { inputText, commands } = get()
    if (!inputText.trim()) return
    const result = parseCommand(inputText.trim())
    if (!result.ok) {
      set({ parseError: result.suggestion })
      return
    }
    set({ commands: [...commands, result.command], inputText: '', parseError: null })
  },

  removeCommand: (id) =>
    set((s) => ({ commands: s.commands.filter((c) => c.id !== id) })),

  clearCommands: () =>
    set({ commands: [], executionLog: [], engineStatus: 'idle', parseError: null }),

  runAll: () => {
    const { commands } = get()
    if (commands.length === 0) return
    set({ engineStatus: 'running' })
    const { logs, finalState, isComplete } = runSequence(commands, INITIAL_SANDWICH_STATE)
    const confusion = logs.filter(
      (l) => l.result === 'literal_interpretation' || l.result === 'precondition_error',
    ).length
    set({
      executionLog: logs,
      sandwichState: finalState,
      engineStatus: isComplete ? 'done' : 'error',
      confusionCount: confusion,
    })
  },

  reset: () =>
    set({
      inputText: '',
      parseError: null,
      commands: [],
      executionLog: [],
      engineStatus: 'idle',
      sandwichState: { ...INITIAL_SANDWICH_STATE },
      confusionCount: 0,
    }),
}))
