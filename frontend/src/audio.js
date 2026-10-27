// Optional output only. Exercise owns time; no audio callback changes its state.
export class AudioOutput {
  constructor({ synth, Utterance, AudioContext, timer = (fn, delay) => setTimeout(fn, delay), clear = id => clearTimeout(id), changed = () => {} } = {}) {
    Object.assign(this, { synth, Utterance, AudioContext, timer, clear, changed })
    this.epoch = 0; this.voices = []; this.nodes = new Set(); this.state = { busy: false, message: 'Audio is off.' }
  }
  report(message, busy = false) { this.state = { message, busy }; this.changed(this.state) }
  refreshVoices() {
    try { this.voices = (this.synth?.getVoices() || []).filter(v => v.localService === true && /^en(?:[-_]|$)/i.test(v.lang)) }
    catch { this.voices = []; this.report('Voice discovery unavailable. Text and soft tones remain available.') }
    return this.voices
  }
  stop(message = 'Audio stopped.') {
    this.epoch += 1
    this.clear(this.waiting); this.waiting = null
    try { this.synth?.cancel() } catch { /* Text remains available. */ }
    for (const node of this.nodes) { try { node.stop() } catch {} }
    this.nodes.clear()
    this.report(message)
  }
  speak(text, { voiceURI, valid = () => true, phase = false, preview = false } = {}) {
    this.stop()
    const voice = this.voices.find(v => v.voiceURI === voiceURI) || this.voices[0]
    if (!this.synth || !this.Utterance || !voice) { this.report('No on-device English voice is available. Use text or soft tones.'); return false }
    if (!valid()) return false
    const epoch = this.epoch
    let utterance
    try {
      utterance = new this.Utterance(text)
      utterance.voice = voice; utterance.lang = voice.lang; utterance.rate = 1; utterance.volume = .8
    } catch { this.report('Voice playback unavailable. Text remains available.'); return false }
    const current = () => epoch === this.epoch
    utterance.onstart = () => {
      if (!current()) return
      if (!valid()) { this.stop('Late voice cue skipped. Follow the words and count.'); return }
      this.clear(this.waiting); this.waiting = null
      this.report(phase ? `Speaking: ${text}.` : preview ? 'Voice preview playing.' : 'Reading assistant reply aloud.', true)
    }
    utterance.onend = () => { if (current()) { this.clear(this.waiting); this.waiting = null; this.report(phase ? 'Waiting for the next phase.' : preview ? 'Voice preview finished.' : 'Read aloud finished.') } }
    utterance.onerror = () => { if (current()) this.stop('Voice playback unavailable. Text remains available.') }
    this.report('Starting voice…', true)
    this.waiting = this.timer(() => { if (current()) this.stop('Voice did not start in time. Text remains available.') }, phase ? 900 : 4000)
    try { this.synth.speak(utterance); return true }
    catch { this.stop('Voice playback unavailable. Text remains available.'); return false }
  }
  async unlock() {
    if (!this.AudioContext) { this.report('Soft tones are unavailable in this browser.'); return false }
    try {
      this.context ||= new this.AudioContext()
      if (this.context.state !== 'running') await this.context.resume()
      if (this.context.state !== 'running') throw new Error('Audio blocked')
      return true
    } catch { this.report('Sound could not start. Use the words and count.'); return false }
  }
  tone(phase) {
    this.stop()
    if (this.context?.state !== 'running') { this.report('Sound unavailable. Re-select Soft tones to try again.'); return false }
    try {
      const now = this.context.currentTime, oscillator = this.context.createOscillator(), gain = this.context.createGain()
      oscillator.type = 'sine'
      oscillator.frequency.setValueAtTime(phase === 'Inhale' ? 330 : 440, now)
      oscillator.frequency.exponentialRampToValueAtTime(phase === 'Inhale' ? 440 : 330, now + .4)
      gain.gain.setValueAtTime(0, now); gain.gain.linearRampToValueAtTime(.07, now + .04); gain.gain.exponentialRampToValueAtTime(.001, now + .45)
      oscillator.connect(gain); gain.connect(this.context.destination); this.nodes.add(oscillator)
      const epoch = this.epoch
      oscillator.onended = () => { this.nodes.delete(oscillator); oscillator.disconnect(); gain.disconnect(); if (epoch === this.epoch) this.report('Waiting for the next phase.') }
      oscillator.start(now); oscillator.stop(now + .5)
      this.report(`${phase} tone playing.`, true); return true
    } catch { this.stop('Sound unavailable. Use the words and count.'); return false }
  }
  dispose() { this.stop(); void this.context?.close().catch(() => {}) }
}

// Deduplicate phase cues; enabling/resuming mid-phase never queues a late instruction.
export class PhaseCues {
  reset() { this.key = null }
  skip(reading) { this.key = `${reading.cycle}:${reading.phase}` }
  take(reading) {
    const key = `${reading.cycle}:${reading.phase}`
    if (key === this.key) return false
    this.key = key
    return reading.elapsed < 60000 && (reading.elapsed % 10000 - (reading.phase === 'Exhale' ? 4000 : 0)) < 900
  }
}
