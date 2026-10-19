// One monotonic source. No setInterval count accumulation, API, or model authority.
export class Exercise {
  constructor(clock = () => performance.now()) { this.clock = clock; this.state = 'ready'; this.active = 0; this.excluded = 0; this.startAt = null; this.lastTick = null; this.pauseAt = null }
  start() { this.state = 'running'; this.active = 0; this.excluded = 0; this.pauseAt = null; this.endAt = null; this.startAt = this.clock(); this.anchor = this.startAt; this.lastTick = this.startAt; return this.read() }
  read() {
    const elapsed = this.state === 'running' ? this.active + this.clock() - this.anchor : this.active
    const bounded = Math.max(0, Math.min(60000, elapsed))
    const within = bounded % 10000
    return { elapsed: bounded, cycle: Math.min(6, Math.floor(bounded / 10000) + 1), phase: within < 4000 ? 'Inhale' : 'Exhale', count: Math.floor((within < 4000 ? within : within - 4000) / 1000) + 1, scale: within < 4000 ? 0.7 + 0.3 * within / 4000 : 1 - 0.3 * (within - 4000) / 6000 }
  }
  tick() {
    const t = this.clock()
    if (!['running', 'paused'].includes(this.state)) return this.read()
    if (t - this.lastTick > 2000) { this.finish('interrupted'); return this.read() }
    this.lastTick = t
    if (this.state === 'running' && this.active + t - this.anchor >= 60000) this.finish('completed')
    return this.read()
  }
  pause() { if (this.state !== 'running') return; this.active += this.clock() - this.anchor; this.pauseAt = this.clock(); this.state = 'paused' }
  resume() { if (this.state !== 'paused') return; const t = this.clock(); this.excluded += t - this.pauseAt; this.pauseAt = null; this.anchor = t; this.lastTick = t; this.state = 'running' }
  finish(status) { if (!['running', 'paused'].includes(this.state)) return; const t = this.clock(); if (this.state === 'running') this.active += t - this.anchor; else this.excluded += t - this.pauseAt; this.pauseAt = null; this.state = status; this.endAt = t }
  timing(renderedEnd = this.endAt) { const wall = renderedEnd - this.startAt; return { wall_ms: wall, excluded_ms: this.excluded, assignment_duration_ms: wall - this.excluded } }
}

export function phraseCue(text) {
  const normalized = text.normalize('NFKC').toLowerCase().replaceAll('’', "'").replace(/\s+/g, ' ').trim()
  return /\b(kill myself|end my life|hurt myself|want to die)\b/u.test(normalized)
}
