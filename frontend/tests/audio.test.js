import test from 'node:test'
import assert from 'node:assert/strict'
import { AudioOutput, replyVoices } from '../src/audio.js'

function fixture(voices = [{name:'Samantha',voiceURI:'local',lang:'en-US',localService:true}]) {
  const spoken = [], timers = new Map(); let id = 0, cancelled = 0
  const output = new AudioOutput({synth:{getVoices:()=>voices,cancel:()=>cancelled++,speak:u=>spoken.push(u)},Utterance:class { constructor(text) { this.text = text } },timer:fn=>{ timers.set(++id,fn); return id },clear:id=>timers.delete(id)})
  output.refreshVoices(); return {output,spoken,timers,cancelled:()=>cancelled}
}
test('reply choices exclude remote/non-English/novelty voices and rank enhanced options first', () => {
  const v=(name,localService=true,lang='en-US')=>({name,voiceURI:name,localService,lang})
  const choices=replyVoices([v('Fred'),v('Daniel'),v('Cloud Neural',false),v('Samantha'),v('Other'),v('Siri Enhanced'),v('Claire',true,'fr-FR'),v('Bad News'),v('Kathy')])
  assert.deepEqual(choices.map(v=>v.name),['Siri Enhanced','Samantha','Daniel','Other'])
})
test('no suitable voice has a truthful text fallback without a speech attempt', () => {
  const {output,spoken}=fixture([{name:'Cloud',voiceURI:'remote',lang:'en-US',localService:false}])
  assert.equal(output.speak('Approved reply'),false); assert.equal(spoken.length,0); assert.match(output.state.message,/No suitable/)
})
test('speech lifecycle and Stop invalidate stale callbacks', () => {
  const {output,spoken,timers}=fixture(); output.speak('Approved reply'); const first=spoken[0]
  assert.equal(timers.size,1); first.onstart(); assert.equal(timers.size,0); assert.equal(output.state.busy,true)
  output.stop(); first.onend(); first.onerror(); assert.equal(output.state.message,'Chatbot voice stopped.')
  output.speak('Next reply'); spoken[1].onstart(); spoken[1].onend(); assert.equal(output.state.message,'Read aloud finished.')
})
test('speech awaiting startup is cancelled if practice/navigation makes it invalid', () => {
  const {output,spoken,timers}=fixture(); let valid=true
  output.speak('Approved reply',{valid:()=>valid}); valid=false; spoken[0].onstart()
  assert.match(output.state.message,/Playback cancelled/); assert.equal(timers.size,0)
})
test('blocked speech times out and stale timer cannot cancel later output', () => {
  const {output,spoken,timers}=fixture(); output.speak('First reply'); const stale=[...timers.values()][0]
  output.speak('Second reply'); stale(); assert.equal(output.state.message,'Starting chatbot voice…')
  ;[...timers.values()][0](); assert.match(output.state.message,/did not start/)
  spoken[1].onstart(); assert.match(output.state.message,/did not start/)
})
test('browser speech and rejected voice errors are contained', () => {
  const {output}=fixture(); output.synth.speak=()=>{throw new Error('blocked')}
  assert.equal(output.speak('Reply'),false)
  output.Utterance=class {set voice(value){throw new TypeError('rejected')}}
  assert.equal(output.speak('Reply'),false); assert.match(output.state.message,/unavailable/)
})
test('selected on-device voice, controlled speed and preview labels reach browser speech', () => {
  const a={name:'Samantha',voiceURI:'a',lang:'en-US',localService:true},b={name:'Daniel',voiceURI:'b',lang:'en-GB',localService:true}
  const {output,spoken}=fixture([a,b]); output.speak('Preview',{voiceURI:'b',rate:.85,preview:true})
  assert.equal(spoken[0].voice,b); assert.equal(spoken[0].rate,.85); assert.equal(spoken[0].pitch,1)
  spoken[0].onstart(); assert.equal(output.state.message,'Voice preview playing.')
  spoken[0].onend(); assert.equal(output.state.message,'Voice preview finished.')
  output.speak('Reply',{rate:99}); assert.equal(spoken[1].rate,.95)
})
test('voice discovery failure remains explicit', () => {
  const {output}=fixture(); output.synth.getVoices=()=>{throw new Error('blocked')}
  assert.deepEqual(output.refreshVoices(),[]); assert.match(output.state.message,/discovery unavailable/)
})
