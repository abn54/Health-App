import test from 'node:test'
import assert from 'node:assert/strict'
import { Exercise, phraseCue } from '../src/engine.js'

test('all six cycles retain exact 4/6 boundaries without accumulated interval drift', () => {
  let t = 0; const e = new Exercise(() => t); e.start()
  for (let cycle = 0; cycle < 6; cycle++) {
    for (let count = 0; count < 10; count++) {
      t = cycle * 10000 + count * 1000
      const value = e.tick()
      assert.equal(value.phase, count < 4 ? 'Inhale' : 'Exhale')
      assert.equal(value.count, count < 4 ? count + 1 : count - 3)
      assert.equal(value.cycle, cycle + 1)
    }
  }
  t = 60020; e.tick(); assert.equal(e.state, 'completed')
  assert.equal(e.timing().assignment_duration_ms, 60020)
})

test('pause preserves the fraction of a count; overlapping support is excluded once', () => {
  let t = 0; const e = new Exercise(() => t); e.start()
  t = 1250; e.pause(); assert.equal(e.read().count, 2)
  t = 5250; assert.equal(e.read().elapsed, 1250)
  e.pause(); e.resume(); t = 5999; assert.equal(e.read().count, 2)
  t = 6000; assert.equal(e.read().count, 3)
  e.finish('stopped'); assert.equal(e.excluded, 4000)
  assert.equal(e.timing().assignment_duration_ms, 2000)
})

test('scheduling interruption includes app delay, without false completion or exclusion', () => {
  let t = 0; const e = new Exercise(() => t); e.start()
  t = 61000; e.tick(); assert.equal(e.state, 'interrupted')
  assert.equal(e.timing().assignment_duration_ms, 61000)
  assert.equal(e.timing().excluded_ms, 0)
})

test('End is immediate, and a terminal exercise does not resume', () => {
  let t = 0; const e = new Exercise(() => t); e.start(); t = 500; e.finish('stopped')
  e.resume(); assert.equal(e.state, 'stopped'); assert.equal(e.read().elapsed, 500)
})

test('a new session resets elapsed time and pause accounting', () => {
  let t = 0; const e = new Exercise(() => t); e.start(); t = 1000; e.pause(); t = 2000; e.finish('stopped')
  t = 3000; e.start(); assert.equal(e.read().elapsed, 0); assert.equal(e.excluded, 0)
  t = 4000; assert.equal(e.read().count, 2)
})

test('phrase cue is bounded and normalized; negations still match (documented limitation)', () => {
  assert.equal(phraseCue('I WANT   TO DIE'), true)
  assert.equal(phraseCue('I do not want to die'), true)
  assert.equal(phraseCue('I dyed a shirt'), false)
  assert.equal(phraseCue('kill myselfish'), false)
})
