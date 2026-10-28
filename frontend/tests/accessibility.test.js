import test from 'node:test'
import assert from 'node:assert/strict'
import { exerciseAnnouncement } from '../src/accessibility.js'

test('phase announcements contain cycle, direction and prescribed duration, without every-frame chatter', () => {
  const r={cycle:2,phase:'Inhale',count:1}
  assert.equal(exerciseAnnouncement('running',r),'Cycle 2 of 6. Inhale for 4 one-second counts.')
  assert.equal(exerciseAnnouncement('running',{...r,count:4}),exerciseAnnouncement('running',r))
  assert.equal(exerciseAnnouncement('running',{cycle:6,phase:'Exhale',count:1}),'Cycle 6 of 6. Exhale for 6 one-second counts.')
})
test('optional count announcements are concise and respect different phase lengths', () => {
  assert.equal(exerciseAnnouncement('running',{cycle:1,phase:'Inhale',count:4},'count'),'Inhale, 4 of 4.')
  assert.equal(exerciseAnnouncement('running',{cycle:6,phase:'Exhale',count:6},'count'),'Exhale, 6 of 6.')
})
test('paused state offers explicit resume/end; announcements can be switched off', () => {
  const r={cycle:3,phase:'Exhale',count:2}
  assert.match(exerciseAnnouncement('paused',r),/Exercise paused.*Cycle 3 of 6, exhale, count 2.*Resume or End/)
  assert.equal(exerciseAnnouncement('paused',r,'off'),'')
  for(const state of ['ready','completed','stopped','interrupted']) assert.equal(exerciseAnnouncement(state,r),'')
})
