// Chatbot output only. Breathing never invokes speech or Web Audio.
const novelty = /\b(albert|bad news|bahh|bells|boing|bubbles|cellos|fred|good news|grandma|grandpa|jester|junior|kathy|organ|ralph|superstar|trinoids|whisper|wobble|zarvox)\b/i
export const enhancedVoice = voice => /premium|enhanced|natural|neural|siri/i.test(voice.name || '')
export function replyVoices(voices) {
  const preferred = ['samantha','daniel','karen','moira','tessa','rishi']
  const rank = v => enhancedVoice(v) ? -100 : preferred.findIndex(n => (v.name || '').toLowerCase().startsWith(n)) < 0 ? 50 : preferred.findIndex(n => (v.name || '').toLowerCase().startsWith(n))
  return voices.filter(v => v.localService === true && /^en(?:[-_]|$)/i.test(v.lang) && !novelty.test(v.name || ''))
    .sort((a,b) => rank(a)-rank(b) || (a.name || '').localeCompare(b.name || ''))
}
export class AudioOutput {
  constructor({ synth, Utterance, timer = (fn, delay) => setTimeout(fn, delay), clear = id => clearTimeout(id), changed = () => {} } = {}) {
    Object.assign(this, { synth, Utterance, timer, clear, changed })
    this.epoch = 0; this.voices = []; this.state = { busy:false, message:'Chatbot voice is off.' }
  }
  report(message, busy = false) { this.state = {message,busy}; this.changed(this.state) }
  refreshVoices() {
    try { this.voices = replyVoices(this.synth?.getVoices() || []) }
    catch { this.voices = []; this.report('Voice discovery unavailable. Replies remain readable as text.') }
    return this.voices
  }
  stop(message = 'Chatbot voice stopped.') {
    this.epoch += 1; this.clear(this.waiting); this.waiting = null
    try { this.synth?.cancel() } catch { /* Text remains available. */ }
    this.report(message)
  }
  speak(text, {voiceURI, rate = .95, valid = () => true, preview = false} = {}) {
    this.stop()
    const voice = this.voices.find(v => v.voiceURI === voiceURI) || this.voices[0]
    if (!this.synth || !this.Utterance || !voice) { this.report('No suitable on-device English voice is available. Replies remain readable as text.'); return false }
    if (!valid()) return false
    const epoch = this.epoch
    let utterance
    try {
      utterance = new this.Utterance(text)
      utterance.voice = voice; utterance.lang = voice.lang
      utterance.rate = [.85,.95,1.05].includes(rate) ? rate : .95
      utterance.pitch = 1; utterance.volume = .8
    } catch { this.report('Voice playback unavailable. Text remains available.'); return false }
    const current = () => epoch === this.epoch
    utterance.onstart = () => {
      if (!current()) return
      if (!valid()) { this.stop('Playback cancelled. Replies remain readable as text.'); return }
      this.clear(this.waiting); this.waiting = null
      this.report(preview ? 'Voice preview playing.' : 'Reading assistant reply aloud.', true)
    }
    utterance.onend = () => { if (current()) { this.clear(this.waiting); this.waiting = null; this.report(preview ? 'Voice preview finished.' : 'Read aloud finished.') } }
    utterance.onerror = () => { if (current()) this.stop('Voice playback unavailable. Text remains available.') }
    this.report('Starting chatbot voice…', true)
    this.waiting = this.timer(() => { if (current()) this.stop('Voice did not start in time. Text remains available.') }, 4000)
    try { this.synth.speak(utterance); return true }
    catch { this.stop('Voice playback unavailable. Text remains available.'); return false }
  }
  dispose() { this.stop() }
}
