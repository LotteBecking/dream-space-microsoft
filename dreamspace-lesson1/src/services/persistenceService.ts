const NS = 'ds-l1-'

export const storage = {
  get<T>(key: string): T | null {
    try {
      const v = localStorage.getItem(NS + key)
      return v ? (JSON.parse(v) as T) : null
    } catch {
      return null
    }
  },
  set<T>(key: string, value: T): void {
    try {
      localStorage.setItem(NS + key, JSON.stringify(value))
    } catch {
      // ignore quota errors
    }
  },
  clear(key: string): void {
    localStorage.removeItem(NS + key)
  },
}
