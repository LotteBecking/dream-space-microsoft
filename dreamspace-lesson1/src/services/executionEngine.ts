export interface SandwichState {
  breadBag: 'closed' | 'open'
  breadSlices: number
  pbJar: 'closed' | 'open'
  jamJar: 'closed' | 'open'
  pbApplied: boolean
  jamApplied: boolean
  sandwichComplete: boolean
  knifeLocation: 'counter' | 'hand'
}

export const INITIAL_SANDWICH_STATE: SandwichState = {
  breadBag: 'closed',
  breadSlices: 0,
  pbJar: 'closed',
  jamJar: 'closed',
  pbApplied: false,
  jamApplied: false,
  sandwichComplete: false,
  knifeLocation: 'counter',
}

export type CommandType =
  | 'OPEN_BREAD_BAG'
  | 'TAKE_BREAD_SLICE'
  | 'OPEN_PB_JAR'
  | 'OPEN_JAM_JAR'
  | 'GET_KNIFE'
  | 'APPLY_PB'
  | 'APPLY_JAM'
  | 'PLACE_SECOND_SLICE'
  | 'SERVE'

export interface Command {
  id: string
  type: CommandType
  rawInput: string
}

export type LogEntryResult = 'success' | 'precondition_error' | 'literal_interpretation'

export interface LogEntry {
  stepNumber: number
  command: Command
  result: LogEntryResult
  message: string
  stateAfter: SandwichState
}

export type ParseResult =
  | { ok: true; command: Command }
  | { ok: false; suggestion: string }

// Alias table — maps natural language to command types
const ALIASES: Record<CommandType, string[]> = {
  OPEN_BREAD_BAG: ['open bread bag', 'open the bread', 'open bag', 'open bread', 'tear the bag', 'unseal'],
  TAKE_BREAD_SLICE: ['take bread', 'take a slice', 'get bread', 'remove bread', 'take out bread', 'grab bread', 'take slice'],
  OPEN_PB_JAR: ['open peanut butter', 'open pb', 'open the peanut butter', 'unscrew peanut butter', 'open pb jar'],
  OPEN_JAM_JAR: ['open jam', 'open the jam', 'unscrew jam', 'open jam jar'],
  GET_KNIFE: ['get knife', 'pick up knife', 'grab knife', 'take knife', 'take the knife', 'get the knife', 'pick knife'],
  APPLY_PB: ['spread peanut butter', 'apply peanut butter', 'spread pb', 'put peanut butter on', 'add peanut butter', 'use peanut butter'],
  APPLY_JAM: ['spread jam', 'apply jam', 'put jam on', 'add jam', 'use jam', 'spread the jam'],
  PLACE_SECOND_SLICE: ['place second slice', 'put second slice', 'close sandwich', 'put bread on top', 'add second slice', 'place top slice', 'top with bread'],
  SERVE: ['serve', 'done', 'finish', 'complete', 'plate it', 'serve sandwich'],
}

export function parseCommand(input: string): ParseResult {
  const normalized = input.toLowerCase().trim()
  for (const [type, aliases] of Object.entries(ALIASES) as [CommandType, string[]][]) {
    if (aliases.some(a => normalized.includes(a))) {
      return {
        ok: true,
        command: { id: crypto.randomUUID(), type, rawInput: input },
      }
    }
  }
  // Find closest suggestion by word overlap
  let best = ''
  let bestScore = 0
  const inputWords = new Set(normalized.split(/\s+/))
  for (const aliases of Object.values(ALIASES)) {
    for (const alias of aliases) {
      const aliasWords = alias.split(/\s+/)
      const score = aliasWords.filter(w => inputWords.has(w)).length
      if (score > bestScore) {
        bestScore = score
        best = alias
      }
    }
  }
  const suggestion = best ? `Did you mean: "${best}"?` : 'Try: "open bread bag", "get knife", "spread peanut butter"…'
  return { ok: false, suggestion }
}

export function executeStep(
  cmd: Command,
  state: SandwichState,
  stepNumber: number,
): { log: LogEntry; newState: SandwichState } {
  const make = (
    result: LogEntryResult,
    message: string,
    nextState: SandwichState,
  ): { log: LogEntry; newState: SandwichState } => ({
    log: { stepNumber, command: cmd, result, message, stateAfter: nextState },
    newState: nextState,
  })

  switch (cmd.type) {
    case 'OPEN_BREAD_BAG':
      if (state.breadBag === 'open')
        return make('precondition_error', 'The bread bag is already open.', state)
      return make('success', 'I opened the bread bag.', { ...state, breadBag: 'open' })

    case 'TAKE_BREAD_SLICE':
      if (state.breadBag === 'closed')
        return make(
          'literal_interpretation',
          'I tried to take bread from the closed bag. My hand got stuck. The bag is still closed.',
          state,
        )
      if (state.breadSlices >= 2)
        return make('precondition_error', 'There are already 2 slices out. I do not know where to put another.', state)
      return make('success', `I took 1 bread slice. There are now ${state.breadSlices + 1} slice(s) out.`, {
        ...state,
        breadSlices: state.breadSlices + 1,
      })

    case 'OPEN_PB_JAR':
      if (state.pbJar === 'open')
        return make('precondition_error', 'The peanut butter jar is already open.', state)
      return make('success', 'I unscrewed the peanut butter jar lid.', { ...state, pbJar: 'open' })

    case 'OPEN_JAM_JAR':
      if (state.jamJar === 'open')
        return make('precondition_error', 'The jam jar is already open.', state)
      return make('success', 'I unscrewed the jam jar lid.', { ...state, jamJar: 'open' })

    case 'GET_KNIFE':
      if (state.knifeLocation === 'hand')
        return make('precondition_error', 'I am already holding the knife.', state)
      return make('success', 'I picked up the knife.', { ...state, knifeLocation: 'hand' })

    case 'APPLY_PB':
      if (state.pbJar === 'closed')
        return make(
          'literal_interpretation',
          'I pressed the knife against the closed peanut butter lid. No peanut butter came out.',
          state,
        )
      if (state.knifeLocation !== 'hand')
        return make(
          'precondition_error',
          'I do not have the knife in my hand. You forgot to tell me to get the knife.',
          state,
        )
      if (state.breadSlices === 0)
        return make(
          'literal_interpretation',
          'There is no bread. I spread peanut butter on the empty plate.',
          { ...state, pbApplied: true },
        )
      return make('success', 'I spread peanut butter on the bread slice.', { ...state, pbApplied: true })

    case 'APPLY_JAM':
      if (state.jamJar === 'closed')
        return make(
          'literal_interpretation',
          'I tried to spread jam but the jar is still closed. I poked the lid.',
          state,
        )
      if (state.knifeLocation !== 'hand')
        return make(
          'precondition_error',
          'I do not have the knife. You need to tell me to get the knife first.',
          state,
        )
      if (!state.pbApplied)
        return make('success', 'I spread jam on the bread (no peanut butter layer yet though!).', {
          ...state,
          jamApplied: true,
        })
      return make('success', 'I spread jam on top of the peanut butter.', { ...state, jamApplied: true })

    case 'PLACE_SECOND_SLICE':
      if (state.breadSlices < 1)
        return make('precondition_error', 'There is no first bread slice yet. Take a slice first.', state)
      if (state.breadSlices >= 2)
        return make('precondition_error', 'There are already 2 slices. The sandwich is stacked.', state)
      return make('success', 'I placed the second bread slice on top.', {
        ...state,
        breadSlices: 2,
      })

    case 'SERVE': {
      const isComplete = state.breadSlices === 2 && state.pbApplied && state.jamApplied
      if (!isComplete)
        return make(
          'precondition_error',
          'The sandwich is not ready yet. Make sure you have 2 slices of bread with peanut butter and jam.',
          state,
        )
      return make('success', '🥪 Sandwich complete! Serving now. Your algorithm worked!', {
        ...state,
        sandwichComplete: true,
      })
    }
  }
}

export function runSequence(
  cmds: Command[],
  initialState: SandwichState,
): { logs: LogEntry[]; finalState: SandwichState; isComplete: boolean } {
  let state = { ...initialState }
  const logs: LogEntry[] = []
  for (let i = 0; i < cmds.length; i++) {
    const { log, newState } = executeStep(cmds[i], state, i + 1)
    logs.push(log)
    state = newState
  }
  return { logs, finalState: state, isComplete: state.sandwichComplete }
}
