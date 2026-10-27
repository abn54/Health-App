import test from 'node:test'
import assert from 'node:assert/strict'
import { AudioOutput, PhaseCues } from '../src/audio.js'
import { Exercise } from '../src/engine.js'

function fixture(voices = [{voiceURI:'local',lang:'en-US',localService:true}]) {
  const spoken = [], timers = new Map(); let id = 0, cancelled = 0
  const output = new AudioOutput({
    synth:{getVoices:()=>voices,cancel:()=>cancelled++,speak:u=>spoken.push(u)},
    Utterance:class { constructor(text) { this.text = text } },
    timer:fn=>{ timers.set(++id,fn); return id },clear:id=>timers.delete(id),
  })
  output.refreshVoices()
  return {output,spoken,timers,cancelled:()=>cancelled}
}
test('only on-device English voices can speak, with truthful unavailable fallback', () => {
  const {output,spoken} = fixture([{voiceURI:'cloud',lang:'en-US',localService:false},{voiceURI:'fr',lang:'fr-FR',localService:true}])
  assert.equal(output.speak('Inhale'),false); assert.equal(spoken.length,0)
  assert.match(output.state.message,/No on-device/)
})
test('speech lifecycle reports browser events; Stop invalidates all stale callbacks', () => {
  const {output,spoken,timers} = fixture()
  output.speak('Approved reply'); const first = spoken[0]
  assert.equal(timers.size,1); first.onstart(); assert.equal(timers.size,0); assert.equal(output.state.busy,true)
  output.stop(); first.onend(); first.onerror(); assert.equal(output.state.message,'Audio stopped.')
  output.speak('Next reply'); spoken[1].onstart(); spoken[1].onend()
  assert.equal(output.state.message,'Read aloud finished.'); assert.equal(output.state.busy,false)
})
test('late phase startup is cancelled rather than speaking a stale instruction', () => {
  const {output,spoken,timers,cancelled} = fixture(); let valid = true
  output.speak('Inhale',{phase:true,valid:()=>valid}); valid = false; spoken[0].onstart()
  assert.match(output.state.message,/Late voice cue skipped/); assert.equal(timers.size,0); assert.equal(cancelled(),2)
})
test('blocked speech times out; stale timer cannot cancel subsequent speech', () => {
  const {output,spoken,timers} = fixture()
  output.speak('Inhale',{phase:true}); const stale = [...timers.values()][0]
  output.speak('Exhale',{phase:true}); stale(); assert.equal(output.state.message,'Starting voice…')
  const current = [...timers.values()][0]; current(); assert.match(output.state.message,/did not start/)
  spoken[1].onstart(); assert.match(output.state.message,/did not start/)
})
test('synchronous speech errors do not throw or claim successful playback', () => {
  const {output} = fixture(); output.synth.speak = () => { throw new Error('blocked') }
  assert.equal(output.speak('Inhale'),false); assert.match(output.state.message,/unavailable/)
})
test('phase cues deduplicate all counts, skip late phases and start again only after reset', () => {
  const cues = new PhaseCues(); cues.reset(); const seen = []
  for (let elapsed = 0; elapsed <= 60000; elapsed += 100) {
    const r = {elapsed,cycle:Math.min(6,Math.floor(elapsed/10000)+1),phase:elapsed%10000<4000?'Inhale':'Exhale'}
    if (cues.take(r)) seen.push([r.cycle,r.phase,elapsed])
  }
  assert.equal(seen.length,12); assert.deepEqual(seen.at(-1),[6,'Exhale',54000])
  cues.reset(); assert.equal(cues.take({elapsed:1500,cycle:1,phase:'Inhale'}),false)
  cues.reset(); cues.skip({cycle:1,phase:'Exhale'})
  assert.equal(cues.take({elapsed:4400,cycle:1,phase:'Exhale'}),false)
  assert.equal(cues.take({elapsed:10010,cycle:2,phase:'Inhale'}),true)
})
test('speech failure/timeout leaves the single exercise clock and 4/6 completion unchanged', () => {
  let now = 0; const exercise = new Exercise(()=>now), {output,timers} = fixture(); exercise.start()
  output.speak('Inhale',{phase:true}); [...timers.values()][0]()
  for (now = 1000; now <= 60000; now += 1000) exercise.tick()
  assert.equal(exercise.state,'completed'); assert.equal(exercise.timing().assignment_duration_ms,60000)
  assert.equal(exercise.excluded,0)
})
test('soft tones handle missing or blocked audio without claiming playback', async () => {
  const missing = new AudioOutput(); assert.equal(await missing.unlock(),false)
  assert.equal(missing.tone('Inhale'),false)
  const blocked = new AudioOutput({AudioContext:class { constructor(){this.state='suspended'} async resume(){throw new Error('blocked')} }})
  assert.equal(await blocked.unlock(),false); assert.match(blocked.state.message,/could not start/)
})
test('tone nodes cancel immediately and stale end does not overwrite Stop', async () => {
  let stopCalls = 0, lastNode
  const output = new AudioOutput({AudioContext:class {
    constructor(){this.state='running';this.currentTime=0;this.destination={}}
    createOscillator(){return lastNode={frequency:{setValueAtTime(){},exponentialRampToValueAtTime(){}},connect(){},disconnect(){},start(){},stop(){stopCalls++}}}
    createGain(){return {gain:{setValueAtTime(){},linearRampToValueAtTime(){},exponentialRampToValueAtTime(){}},connect(){},disconnect(){}}}
  }})
  assert.equal(await output.unlock(),true); assert.equal(output.tone('Exhale'),true)
  assert.equal(output.state.busy,true); output.stop(); lastNode.onended()
  assert.equal(stopCalls,2); assert.equal(output.state.message,'Audio stopped.'); assert.equal(output.nodes.size,0)
})
test('a voice object rejected by the browser falls back to text without escaping the handler', () => {
  const {output} = fixture()
  output.Utterance = class { set voice(value) { throw new TypeError('rejected voice') } }
  assert.equal(output.speak('Inhale'),false); assert.match(output.state.message,/unavailable/)
})
test('voice discovery failure is contained and explicit local selection is respected', () => {
  const a={voiceURI:'a',lang:'en-US',localService:true}, b={voiceURI:'b',lang:'en-GB',localService:true}
  const {output,spoken}=fixture([a,b]); output.speak('Approved reply',{voiceURI:'b'})
  assert.equal(spoken[0].voice,b)
  output.synth.getVoices=()=>{throw new Error('unavailable')}
  assert.deepEqual(output.refreshVoices(),[]); assert.match(output.state.message,/discovery unavailable/)
})
