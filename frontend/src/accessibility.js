// Text for an assistive technology live region; never synthesized by the app.
export function exerciseAnnouncement(status, reading, mode = 'phase') {
  if (mode === 'off' || !['running','paused'].includes(status)) return ''
  if (status === 'paused') return `Exercise paused. Cycle ${reading.cycle} of 6, ${reading.phase.toLowerCase()}, count ${reading.count}. Resume or End exercise is your choice.`
  const length = reading.phase === 'Inhale' ? 4 : 6
  return mode === 'count' ? `${reading.phase}, ${reading.count} of ${length}.` : `Cycle ${reading.cycle} of 6. ${reading.phase} for ${length} one-second counts.`
}

// Apply the same explicit motion choice to stored, reused and active cues.
export function motionSafeCue(requested, reduceMotion) {
  return reduceMotion ? 'text' : requested
}
