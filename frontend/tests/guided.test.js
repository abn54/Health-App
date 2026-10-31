import test from 'node:test'
import assert from 'node:assert/strict'
import exercises from '../../shared/exercises.json' with {type:'json'}
import { GuidedExercise } from '../src/guided.js'

for (const id of ['grounding','stop']) {
  test(`${id}: approved steps remain ordered across all 60 seconds`, () => {
    let now = 0
    const steps = exercises[id].steps, engine = new GuidedExercise(steps, () => now)
    engine.start()
    for (now = 0; now < 60000; now += 500) {
      const reading = engine.tick(), index = Math.floor(now / (60000 / steps.length))
      assert.equal(reading.title, steps[index].title)
      assert.equal(reading.step, index+1)
    }
    now = 60012; engine.tick()
    assert.equal(engine.state,'completed')
    assert.equal(engine.read().step,steps.length)
    assert.equal(engine.timing().assignment_duration_ms,60012)
  })
}
test('guided pause holds a step; resume excludes only the explicit pause', () => {
  let now=0; const engine=new GuidedExercise(exercises.grounding.steps,()=>now); engine.start()
  now=12500; engine.pause(); assert.equal(engine.read().step,2)
  now=18000; assert.equal(engine.read().elapsed,12500); engine.resume()
  now=19000; assert.equal(engine.read().step,2); engine.finish('stopped')
  assert.equal(engine.excluded,5500); assert.equal(engine.timing().assignment_duration_ms,13500)
})
test('guided hidden/scheduled interruption is partial, and End cannot resume', () => {
  let now=0; const engine=new GuidedExercise(exercises.stop.steps,()=>now); engine.start()
  now=3000;engine.tick();assert.equal(engine.state,'interrupted');assert.equal(engine.timing().excluded_ms,0)
  engine.resume();assert.equal(engine.state,'interrupted')
  engine.start();now=3200;engine.finish('stopped');engine.resume();assert.equal(engine.state,'stopped')
})
