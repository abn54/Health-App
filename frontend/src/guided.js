import { Exercise } from './engine.js'

// Approved steps only. Inherit the same monotonic clock, pause/exit/interruption
// rules and 60-second limit. The model cannot provide or alter this sequence.
export class GuidedExercise extends Exercise {
  constructor(steps, clock = () => performance.now()) {
    super(clock)
    if (![4, 5].includes(steps.length)) throw new Error('Expected four or five approved steps')
    this.steps = steps
  }
  read() {
    const { elapsed } = super.read()
    const length = 60000 / this.steps.length
    const index = Math.min(this.steps.length - 1, Math.floor(elapsed / length))
    return { elapsed, step:index + 1, totalSteps:this.steps.length, ...this.steps[index], phase:this.steps[index].sense, remaining:Math.max(0, Math.ceil((length - (elapsed - index * length)) / 1000)) }
  }
}
