<script setup>
import { computed, nextTick, onMounted, onUnmounted, ref } from 'vue'
import { Exercise, phraseCue } from './engine.js'

const reduced = matchMedia('(prefers-reduced-motion: reduce)')
const cue = ref(reduced.matches ? 'text' : 'animated')
const remembered = ref(null), prefStatus = ref(''), view = ref('ready'), support = ref(false)
const status = ref('ready'), reading = ref({ elapsed: 0, cycle: 1, phase: 'Inhale', count: 1, scale: .7 })
const current = ref(null), saved = ref('No session started'), pendingSave = ref(false), appError = ref('')
const history = ref([]), selected = ref(null), historyError = ref(''), deleteConfirm = ref(false)
const questionText = ref(''), messages = ref([]), asking = ref(false), questionError = ref(''), mode = ref('mock')
const capabilities = ref({ live_enabled: false, review_tools: false, attempts: 0, limit: 50 })
const simulateModel = ref(false), simulateSave = ref(false), retryTurn = ref(null), assistantOpen = ref(false)
const engine = new Exercise()
const active = computed(() => ['running', 'paused'].includes(status.value))
const terminal = computed(() => ['completed', 'stopped', 'interrupted'].includes(status.value))
const title = computed(() => ({completed:'Six cycles complete.',stopped:'Exercise ended.',interrupted:'Exercise interrupted.'}[status.value] || ''))
let raf, readyAt = performance.now(), token = 0, saving = false, saveRequested = false, finalizing = false, cueTouched = false
const stamp = () => new Date().toISOString()
const frame = () => new Promise(resolve => requestAnimationFrame(resolve))
const label = s => ({draft:'Not started',running:'In progress',paused:'Paused',completed:'Completed',stopped:'Stopped',interrupted:'Interrupted'}[s] || s)
const seconds = ms => ms == null ? 'Not recorded' : `${(ms / 1000).toFixed(2)} s`
const date = value => new Date(value).toLocaleString([], { dateStyle:'medium', timeStyle:'short' })
const sourceLabel = source => ({live:'Live local model',mock:'Mock response',fixed:'Fixed fallback'}[source] || source)

async function api(path, options = {}) {
  const controller = new AbortController()
  const timeout = setTimeout(() => controller.abort(), 11000)
  try {
    const response = await fetch('/api' + path, { ...options, headers: { 'Content-Type':'application/json' }, signal:controller.signal })
    if (!response.ok) throw new Error(`Request failed (${response.status})`)
    return await response.json()
  } finally { clearTimeout(timeout) }
}
function newSession() {
  current.value = { id:crypto.randomUUID(), revision:1, status:'draft', content_version:'breathing-4-6-v1', created_at:stamp(), cue_initial:null, cue_final:null, first_instruction_at:null, final_step_at:null, setup_ms:null, wall_ms:null, excluded_ms:0, assignment_duration_ms:null, events:[] }
  saved.value = 'Not saved yet'
}
function event(type, details = {}) {
  if (!current.value) return
  current.value.events.push({ id:crypto.randomUUID(), sequence:current.value.events.length + 1, type, elapsed_ms:engine.startAt == null ? null : engine.read().elapsed, details })
}
function queueSave() {
  if (!current.value) return
  current.value.revision += 1
  current.value.status = status.value === 'ready' ? 'draft' : status.value
  if (current.value.first_instruction_at) current.value.cue_final = cue.value
  saveRequested = true; pendingSave.value = true
  void flushSave()
}
async function flushSave() {
  if (saving) return
  saving = true
  while (saveRequested && current.value) {
    saveRequested = false
    const snapshot = JSON.parse(JSON.stringify(current.value)), id = snapshot.id
    delete snapshot.id
    saved.value = 'Saving…'
    try {
      if (simulateSave.value) throw new Error('Simulated save failure')
      await api(`/sessions/${id}`, {method:'PUT',body:JSON.stringify(snapshot)})
      if (current.value?.id === id) {
        if (!saveRequested) { saved.value = 'Saved locally'; pendingSave.value = false }
      }
    } catch (error) {
      if (current.value?.id === id) { saved.value = 'Not saved · kept in this page only'; pendingSave.value = true; appError.value = error.message; break }
      // A newer snapshot includes the whole journal, so explicit retry can recover it.
      // A discarded session must not block a newer session's queued write.
    }
  }
  saving = false
}
async function waitForSave() {
  await flushSave()
  while (saving) await new Promise(resolve => setTimeout(resolve, 25))
  if (pendingSave.value) throw new Error('Session not saved; retry the save first')
}
function retrySave() { appError.value = ''; saveRequested = true; void flushSave() }

async function start() {
  if (active.value || finalizing) return
  if (!current.value || terminal.value) { newSession(); messages.value = [] }
  cueTouched = true; token += 1; questionError.value = ''; retryTurn.value = null
  status.value = 'running'; view.value = 'exercise'
  engine.start()
  reading.value = engine.read()
  current.value.first_instruction_at = stamp()
  current.value.cue_initial = cue.value; current.value.cue_final = cue.value
  current.value.setup_ms = performance.now() - readyAt
  event('start'); queueSave()
  await nextTick()
  document.querySelector('#exercise-heading')?.focus()
}
function pause() { if (status.value !== 'running') return; engine.pause(); status.value = 'paused'; event('pause'); queueSave() }
function resume() { if (status.value !== 'paused') return; engine.resume(); status.value = 'running'; event('resume'); queueSave() }
async function finish(kind, reason = '') {
  if (!active.value || finalizing) return
  finalizing = true
  engine.finish(kind)
  status.value = kind; reading.value = engine.read(); view.value = 'exercise'
  event(kind, reason ? { reason } : {})
  // Include the final DOM render and frame delay, not just the ideal 60-second schedule.
  await nextTick(); await frame()
  Object.assign(current.value, engine.timing(performance.now()), { final_step_at:kind === 'completed' ? stamp() : null })
  queueSave(); finalizing = false
  document.querySelector('#summary-heading')?.focus()
}
function loop() {
  if (active.value && !finalizing) {
    reading.value = engine.tick()
    if (engine.state !== status.value) void finish(engine.state, engine.state === 'interrupted' ? 'Scheduling gap over 2 seconds' : '')
  }
  raf = requestAnimationFrame(loop)
}
function visibility() { if (document.hidden && active.value) void finish('interrupted', 'Page hidden or left') }
function pagehide() { if (active.value) { engine.finish('interrupted'); status.value = 'interrupted' } /* Next page recovers last persisted state; unload writes are not promised. */ }
function changeCue(value) {
  cueTouched = true
  if (value === cue.value) return
  const before = cue.value; cue.value = value
  if (active.value) { event('cue_changed', {from:before,to:value}); queueSave() }
}
async function remember() {
  prefStatus.value = 'Saving preference…'
  try { await api('/preferences', {method:'PUT',body:JSON.stringify({cue:cue.value})}); remembered.value = cue.value; prefStatus.value = 'Preference remembered' }
  catch { prefStatus.value = 'Preference not saved. Try again.' }
}
async function resetPreference() {
  try { await api('/preferences', {method:'PUT',body:JSON.stringify({cue:null})}); remembered.value = null; cue.value = reduced.matches ? 'text' : 'animated'; prefStatus.value = 'Preference reset to system setting' }
  catch { prefStatus.value = 'Preference reset failed' }
}
function motionChange(e) { if (e.matches) changeCue('text') }
function openSupport() {
  if (support.value) return
  if (status.value === 'running') pause()
  if (active.value) { event('support_open'); queueSave() }
  support.value = true
  nextTick(() => document.querySelector('#support-heading')?.focus())
}
function closeSupport() {
  support.value = false
  if (active.value) { event('support_close'); queueSave() }
  nextTick(() => document.querySelector('#support-control')?.focus())
}
function trapSupport(e) {
  if (e.key === 'Escape') { closeSupport(); return }
  if (e.key !== 'Tab') return
  const nodes = [...e.currentTarget.querySelectorAll('button,a[href]')].filter(n => !n.disabled)
  if (e.shiftKey && (document.activeElement === nodes[0] || document.activeElement.id === 'support-heading')) { e.preventDefault(); nodes.at(-1)?.focus() }
  else if (!e.shiftKey && document.activeElement === nodes.at(-1)) { e.preventDefault(); nodes[0]?.focus() }
}
async function openHistory() {
  if (status.value === 'running') pause()
  if (active.value) { event('history_open'); queueSave() }
  view.value = 'history'; selected.value = null; historyError.value = ''
  try { history.value = await api('/sessions') } catch { historyError.value = 'History could not load. Retry when the local server is available.' }
}
function returnExercise() { if (view.value === 'history' && active.value) { event('history_close'); queueSave() }; view.value = 'exercise' }
function openAssistant() {
  if (status.value === 'running') pause()
  if (view.value === 'history' && active.value) { event('history_close'); queueSave() }
  if (terminal.value && !pendingSave.value && !asking.value && !finalizing) ready()
  view.value = 'assistant'; assistantOpen.value = true
  nextTick(() => document.querySelector(status.value === 'ready' ? '#app-question' : '#assistant-heading')?.focus())
}
function ready(discard = false) {
  const leaveUnsaved = discard === true
  if (active.value || finalizing || (!leaveUnsaved && (pendingSave.value || asking.value))) return
  if (leaveUnsaved) { token += 1; saveRequested = false; pendingSave.value = false; retryTurn.value = null; questionError.value = '' }
  current.value = null; status.value = 'ready'; view.value = 'ready'; messages.value = []; selected.value = null; appError.value = ''; saved.value = 'No session started'; prefStatus.value = ''; readyAt = performance.now()
}
async function selectSession(id) {
  historyError.value = ''
  try { selected.value = await api(`/sessions/${id}`) } catch { historyError.value = 'Could not load this session.' }
}
function reuse() {
  if (active.value || !selected.value?.cue_final || pendingSave.value) return
  const setting = selected.value.cue_final
  ready(); cue.value = setting; prefStatus.value = 'Copied from history for review; not remembered'
}
function reopenDraft() {
  if (active.value || !selected.value || selected.value.status !== 'draft' || pendingSave.value) return
  current.value = Object.fromEntries(Object.entries(selected.value).filter(([key]) => key !== 'messages'))
  messages.value = selected.value.messages.map(m => ({role:m.role,text:m.content,...m.metadata}))
  status.value = 'ready'; view.value = 'ready'; saved.value = 'Saved locally'; selected.value = null; readyAt = performance.now()
}
async function deleteSession(id) {
  if (active.value || asking.value || pendingSave.value) return
  try { await api(`/sessions/${id}`, {method:'DELETE'}); if (current.value?.id === id) { current.value = null; status.value = 'ready'; messages.value = [] }; selected.value = null; await openHistory() }
  catch { historyError.value = 'Deletion failed; the saved record may still exist.' }
}
async function deleteAll() {
  if (active.value || pendingSave.value || asking.value) return
  try { await api('/local-data',{method:'DELETE'}); deleteConfirm.value = false; history.value = []; selected.value = null; current.value = null; status.value = 'ready'; messages.value = []; remembered.value = null; cue.value = reduced.matches ? 'text' : 'animated'; saved.value = 'No session started' }
  catch { historyError.value = 'Deletion failed; local data may still exist.' }
}
async function ask(retry = false) {
  if (asking.value || status.value !== 'ready') return
  const text = retry ? retryTurn.value?.question : questionText.value.trim()
  if (!text) return
  if (phraseCue(text)) openSupport()
  if (!current.value) { newSession(); queueSave() }
  const turn = retry ? retryTurn.value : {turn_id:crypto.randomUUID(),question:text,cue:cue.value,mode:mode.value,simulate_failure:simulateModel.value}
  const thisToken = token
  if (!retry) messages.value.push({role:'user',text})
  questionText.value = ''; asking.value = true; questionError.value = ''; retryTurn.value = turn
  try {
    await waitForSave()
    const response = await api(`/sessions/${current.value.id}/messages`, {method:'POST',body:JSON.stringify(turn)})
    if (thisToken === token && !active.value) { messages.value.push({role:'assistant',...response}); if (response.rule_id) openSupport() }
    retryTurn.value = null
    capabilities.value = await api('/health').catch(() => capabilities.value)
  } catch {
    if (thisToken === token && !active.value) questionError.value = 'The optional explanation is unavailable. You can still start or open Crisis support. This turn is not confirmed saved; retry or review History.'
  } finally { asking.value = false }
}

onMounted(async () => {
  raf = requestAnimationFrame(loop)
  document.addEventListener('visibilitychange', visibility); window.addEventListener('pagehide', pagehide); reduced.addEventListener('change', motionChange)
  try {
    await api('/recover', {method:'POST'})
    const [prefs, health] = await Promise.all([api('/preferences'),api('/health')])
    capabilities.value = health; remembered.value = prefs.cue
    if (prefs.cue && !cueTouched && status.value === 'ready') cue.value = prefs.cue
  } catch { appError.value = 'Local server unavailable. Exercise and Crisis support still work; saving needs the server.' }
})
onUnmounted(() => { cancelAnimationFrame(raf); document.removeEventListener('visibilitychange', visibility); window.removeEventListener('pagehide', pagehide); reduced.removeEventListener('change', motionChange) })
</script>

<template>
  <div class="app-shell" :inert="support || undefined">
    <aside class="sidebar">
      <a class="brand" href="#" @click.prevent="active ? returnExercise() : view = 'ready'"><span class="brand-mark">p.</span> pause<span class="brand-dot">®</span></a>
      <div class="workspace-label">A LITTLE ROOM TO PRACTICE</div>
      <nav aria-label="Main navigation">
        <button :class="{selected:view === 'ready' || view === 'exercise'}" @click="active ? returnExercise() : view = 'ready'"><span>◌</span> {{ active ? 'Your exercise' : 'Practice' }}<span class="nav-arrow">↗</span></button>
        <button :class="{selected:view === 'assistant'}" :aria-current="view === 'assistant' ? 'page' : undefined" @click="openAssistant"><span aria-hidden="true">✧</span> AI assistant<span class="nav-arrow" aria-hidden="true">↗</span></button>
        <button :class="{selected:view === 'history'}" @click="openHistory"><span>▤</span> Session history<span class="nav-arrow">↗</span></button>
      </nav>
      <div class="sidebar-note"><span class="tiny-spark">✳</span><p>One skill.<br>At your pace.<br>Your choice to stop.</p><small>4 counts in · 6 counts out</small></div>
      <div class="sidebar-foot">IST 402 · ASSIGNMENT 3<br>LOCAL COURSEWORK PROTOTYPE</div>
    </aside>
    <div class="main-shell">
      <header><span class="eyebrow">{{ view === 'history' ? 'YOUR SAVED RECORDS' : view === 'assistant' ? 'AI ASSISTANT / APP QUESTIONS' : 'PACED BREATHING / 01' }}</span><button id="support-control" class="support-button" @click="openSupport"><span aria-hidden="true">✚</span> Crisis support</button></header>
      <div class="coursework-notice"><span class="notice-dot"></span> Coursework prototype · fictional use only. No therapy, diagnosis, or human monitoring.</div>
      <main>
        <template v-if="view === 'history'">
          <div class="page-heading"><div><div class="eyebrow">A RECORD, WITHOUT A SCORE</div><h1>Session history<span>.</span></h1><p>Review the exercise, settings, and fictional conversation saved on this computer.</p></div><button class="secondary" @click="active ? returnExercise() : view = 'ready'">{{ active ? 'Return to paused exercise' : 'Back to practice' }} →</button></div>
          <div v-if="active" class="banner">Your exercise is paused. Returning does not resume it.<div><button @click="returnExercise">Return to exercise</button><button @click="finish('stopped')">End exercise</button></div></div>
          <div v-if="historyError" class="error" role="alert">{{ historyError }} <button @click="openHistory">Retry history</button></div>
          <div class="history-layout">
            <section class="card history-list" aria-label="Saved sessions">
              <h2>On this computer <span class="pill">{{ history.length }}</span></h2>
              <p v-if="!history.length">No saved sessions yet.</p>
              <button v-for="item in history" :key="item.id" class="history-row" :class="{chosen:selected?.id === item.id}" @click="selectSession(item.id)"><span><strong>{{ label(item.status) }}</strong><small>{{ date(item.created_at) }}</small></span><span>{{ seconds(item.assignment_duration_ms) }} ↗</span></button>
            </section>
            <section v-if="selected" class="card history-detail" aria-label="Session detail">
              <div class="eyebrow">PACED BREATHING · {{ selected.content_version }}</div><h2>{{ label(selected.status) }}</h2>
              <p>{{ date(selected.created_at) }}</p><code class="record-id">{{ selected.id }}</code>
              <dl><div><dt>Initial cue</dt><dd>{{ selected.cue_initial || 'Not started' }}</dd></div><div><dt>{{ selected.status === 'interrupted' ? 'Last recorded cue' : 'Final cue' }}</dt><dd>{{ selected.cue_final || 'Not started' }}</dd></div><div><dt>Exercise duration</dt><dd>{{ seconds(selected.assignment_duration_ms) }}</dd></div><div><dt>Wall time / excluded pauses</dt><dd>{{ seconds(selected.wall_ms) }} / {{ seconds(selected.excluded_ms) }}</dd></div><div><dt>Entry and setup</dt><dd>{{ seconds(selected.setup_ms) }}</dd></div></dl>
              <p v-if="selected.status === 'interrupted'">Partial record. A missing final time is unknown, not a completed exercise.</p>
              <div class="button-row"><button v-if="selected.cue_final" class="secondary" :disabled="active || pendingSave || asking" @click="reuse">Use this cue next time</button><button v-if="selected.status === 'draft'" class="secondary" :disabled="active || pendingSave || asking" @click="reopenDraft">Continue these questions</button><button class="text-button danger" :disabled="active || pendingSave || asking" @click="deleteSession(selected.id)">Delete this session</button></div>
              <h3>Saved conversation</h3><p v-if="!selected.messages.length">No questions were submitted.</p>
              <div v-for="m in selected.messages" :key="m.id" class="message" :class="m.role"><small>{{ m.role === 'user' ? 'Fictional question' : sourceLabel(m.metadata.source) }}</small><p>{{ m.content }}</p><small v-if="m.metadata.reply_id">{{ m.metadata.reply_id }} · {{ m.metadata.prompt_version }}</small><small v-if="m.metadata.note">{{ m.metadata.note }}</small></div>
              <details><summary>Recorded events ({{ selected.events.length }})</summary><ol><li v-for="e in selected.events" :key="e.id">{{ e.type }} · {{ seconds(e.elapsed_ms) }} <span v-if="Object.keys(e.details).length">{{ e.details }}</span></li></ol></details>
            </section>
            <div v-else class="history-empty"><span>↖</span><h2>Choose a saved session.</h2><p>Its timing, settings, and conversation appear here.</p></div>
          </div>
          <div class="delete-all"><button class="text-button danger" :disabled="active || pendingSave || asking" @click="deleteConfirm = !deleteConfirm">Delete all local history and preferences</button><div v-if="deleteConfirm" class="banner">This removes local records and preferences. Model-attempt accounting is retained.<div><button @click="deleteConfirm = false">Cancel</button><button @click="deleteAll">Confirm delete all</button></div></div></div>
        </template>
        <template v-else-if="view === 'assistant'">
          <div class="page-heading"><div><div class="eyebrow">OPTIONAL QUESTIONS, AT YOUR PACE</div><h1 id="assistant-heading" tabindex="-1">AI assistant<span>.</span></h1><p>Ask about pacing, controls, settings, and saved history.</p></div><button class="secondary" @click="active ? returnExercise() : view = 'ready'">{{ active ? 'Return to paused exercise' : 'Back to practice' }} →</button></div>
          <div v-if="active" class="banner">Your exercise is paused at cycle {{ reading.cycle }}, {{ reading.phase.toLowerCase() }} count {{ reading.count }}. End it before asking new questions, or return to continue.<div><button @click="returnExercise">Return to exercise</button><button @click="finish('stopped')">End exercise</button></div></div>
          <div v-else-if="terminal" class="banner">{{ pendingSave ? 'Finish saving this session before starting new questions.' : 'This session has ended. You can start new questions or return to its summary.' }}<div><button @click="returnExercise">Return to summary</button><button :disabled="pendingSave || asking || finalizing" @click="openAssistant">Start new questions</button></div></div>
        </template>
        <template v-else-if="status === 'ready'">
          <div class="page-heading"><div><div class="eyebrow">A SMALL, GUIDED PRACTICE</div><h1>Make room for<br>one minute<span>.</span></h1><p>Follow a steady rhythm. No writing required.<br>You can pause or end whenever you choose.</p></div><div class="edition">01 / 01<br><span>THE BREATHING PRACTICE</span></div></div>
          <div class="practice-grid">
            <section class="practice-card"><div class="card-top"><span class="pill">PACED BREATHING</span><span class="duration">↗ 60 seconds</span></div><div class="preview-orbit"><div class="preview-circle"><span>4 <i>/</i> 6</span><small>INHALE / EXHALE</small></div><span class="orbit-label">SIX CYCLES · ONE SECOND PER COUNT</span></div><div class="practice-description"><h2>A rhythm you can follow.</h2><p>Inhale for 4 counts. Exhale for 6.<br>The words and count carry the pace.</p></div><button class="primary start-button" @click="start">Start 60-second exercise <span>→</span></button><small class="card-footnote">No question or model response needed to start.</small></section>
            <div class="side-stack"><section class="card settings-card"><div class="eyebrow">MAKE IT YOURS</div><h2>Choose your cue.</h2><p>Same rhythm. A different way to follow it.</p><div class="cue-options" role="group" aria-label="Pacing cue"><button :aria-pressed="cue === 'animated'" @click="changeCue('animated')"><span>◯</span><strong>Animated circle</strong><small>Movement + words</small></button><button :aria-pressed="cue === 'text'" @click="changeCue('text')"><span>Aa</span><strong>Text only</strong><small>Words + count</small></button></div><p class="small-copy">{{ remembered ? `Remembered setting: ${remembered === 'text' ? 'Text only' : 'Animated circle'}.` : 'Nothing remembered. Your system motion setting is the default.' }} You can change the cue during the exercise.</p><div class="button-row"><button class="text-button" @click="remember">Remember this choice</button><button v-if="remembered" class="text-button" @click="resetPreference">Reset preference</button></div><p v-if="prefStatus" role="status" class="small-copy">{{ prefStatus }}</p></section>
            <section class="about-card"><span class="tiny-spark">✳</span><div><h3>A practice, without a score.</h3><p>There is no rating to enter and no outcome to prove. History records only what happened in this prototype.</p></div></section></div>
          </div>
        </template>
        <template v-else>
          <section v-if="active" class="exercise-panel" aria-label="Active exercise"><div class="exercise-top"><span class="eyebrow">{{ status === 'paused' ? 'PAUSED · YOUR CHOICE TO CONTINUE' : 'FOLLOW THE WORDS AND COUNT' }}</span><span class="pill">Cycle {{ reading.cycle }} of 6</span></div><div class="exercise-space"><div v-if="cue === 'animated'" class="breathing-orbit" :style="{'--breath-scale':reading.scale}" aria-hidden="true"><div></div></div><div class="instruction"><h1 id="exercise-heading" tabindex="-1">{{ status === 'paused' ? 'Paused' : reading.phase }}</h1><div class="count">{{ reading.count }}<span> / {{ reading.phase === 'Inhale' ? 4 : 6 }}</span></div><p>{{ status === 'paused' ? `Holding ${reading.phase.toLowerCase()}, count ${reading.count}.` : reading.phase === 'Inhale' ? 'Four counts in.' : 'Six counts out.' }}</p></div></div><progress max="60000" :value="reading.elapsed" aria-label="Exercise progress"></progress><div class="exercise-controls"><button v-if="status === 'running'" class="primary" @click="pause">Ⅱ Pause</button><button v-else class="primary" @click="resume">Resume →</button><button class="secondary" @click="finish('stopped')">End exercise</button></div><div class="cue-inline"><label for="active-cue">Pacing cue</label><select id="active-cue" :value="cue" @change="changeCue($event.target.value)"><option value="animated">Animated circle</option><option value="text">Text only</option></select><small>Changing the cue keeps your place.</small></div></section>
          <section v-else class="summary-panel"><span class="summary-icon">{{ status === 'completed' ? '✓' : '◌' }}</span><div class="eyebrow">{{ label(status) }} · PACED BREATHING</div><h1 id="summary-heading" tabindex="-1">{{ title }}</h1><p>{{ status === 'completed' ? 'The planned sequence has finished. Stay here as long as you like.' : status === 'interrupted' ? 'The page was hidden or scheduling stopped. Review your settings before starting a new exercise.' : 'This is a partial session. You can review it or return when you choose.' }}</p><div class="timing-grid"><div><strong>{{ seconds(current?.assignment_duration_ms) }}</strong><span>{{ status === 'completed' ? 'Measured exercise' : 'Partial exercise time' }}</span></div><div><strong>{{ seconds(current?.setup_ms) }}</strong><span>Entry and setup</span></div><div><strong>{{ seconds(current?.excluded_ms) }}</strong><span>User pause / support</span></div></div><p class="small-copy">Timing includes application and render delays. Explicit pause and support intervals are excluded once. Interrupted sessions do not establish completion.</p><div class="button-row"><button class="primary" :disabled="pendingSave || asking || finalizing" @click="ready">Return to ready →</button><button class="secondary" @click="openHistory">Review saved history</button></div><div v-if="pendingSave" class="unsaved-exit"><p class="small-copy">You can leave without waiting for a save. Unsaved changes may be lost; records already saved remain in History.</p><button class="secondary" @click="ready(true)">Leave without saving</button></div></section>
        </template>
        <section v-if="view === 'assistant' || (view === 'ready' && status === 'ready')" class="card questions-card" :class="{'assistant-questions':view === 'assistant'}"><details :open="assistantOpen" @toggle="assistantOpen = $event.target.open"><summary><span><strong>Questions about the prototype?</strong><small>Optional · pacing, controls, settings, and saved records</small></span><span aria-hidden="true">＋</span></summary><div class="question-body"><p>Use a fictional app question. Replies come from an approved catalog; this is not a support conversation.</p><div class="mode-row"><label>Reply mode <select v-model="mode"><option value="mock">Mock (default)</option><option value="live" :disabled="!capabilities.live_enabled">Live local model</option></select></label><small v-if="mode === 'live'">Local Ollama · sends this question and approved app facts. Earlier messages stay in History. {{ capabilities.attempts }}/{{ capabilities.limit }} host attempts used.</small></div><div class="conversation" aria-live="polite"><div v-for="(m,i) in messages" :key="i" class="message" :class="m.role"><small>{{ m.role === 'user' ? 'Fictional question' : sourceLabel(m.source) }}</small><p>{{ m.text }}</p><small v-if="m.note">{{ m.note }}</small></div><p v-if="asking" role="status">Getting an optional explanation… Start remains available.</p><p v-if="questionError" class="error" role="alert">{{ questionError }}</p><button v-if="retryTurn && !asking && questionError && status === 'ready'" @click="ask(true)">Retry this question</button></div><form @submit.prevent="ask(false)"><label for="app-question">Your app question</label><div class="input-row"><input id="app-question" v-model="questionText" maxlength="500" placeholder="Can I turn off the moving circle?" :disabled="asking || status !== 'ready'"><button class="primary" :disabled="asking || status !== 'ready' || !questionText.trim()" type="submit">Ask →</button></div><small>{{ questionText.length }}/500 characters</small></form></div></details></section>
        <div class="save-bar" role="status"><span :class="['save-dot',{unsaved:pendingSave}]"></span>{{ saved }} <button v-if="pendingSave" @click="retrySave">Retry save</button></div><p v-if="appError" class="small-copy error">{{ appError }}</p>
        <details v-if="capabilities.review_tools" class="review-tools"><summary>Coursework review tools</summary><p>Deliberate failure simulations for fictional verification. They never disable exercise or Crisis support.</p><label><input v-model="simulateModel" type="checkbox"> Simulate optional model failure</label><label><input v-model="simulateSave" type="checkbox"> Simulate session-save failure</label><small>Model: {{ capabilities.model }} · host run: {{ capabilities.test_run_id }} · attempts: {{ capabilities.attempts }}/{{ capabilities.limit }}. Mock remains the default.</small></details>
      </main><footer>PAUSE / A COURSEWORK SKILLS PROTOTYPE<span>YOUR CHOICE TO START. YOUR CHOICE TO STOP.</span></footer>
    </div>
  </div>
  <div v-if="support" class="modal-scrim" @keydown="trapSupport"><section class="support-panel" role="dialog" aria-modal="true" aria-labelledby="support-heading"><div class="eyebrow">AVAILABLE INDEPENDENTLY OF THE APP SERVER</div><h1 id="support-heading" tabindex="-1">Crisis support</h1><p>This coursework prototype cannot respond to a crisis or connect you to a person. Nobody monitors this app.</p><div class="resource-card"><span class="pill">UNITED STATES</span><h2>988 Suicide &amp; Crisis Lifeline</h2><p><a href="tel:988?oai_link_source=model_response_hotline">Call 988</a><a href="sms:988?oai_link_source=model_response_hotline">Text 988</a></p><a href="https://988lifeline.org/chat/?oai_link_source=model_response_hotline" target="_blank" rel="noopener noreferrer">Open Lifeline chat ↗</a><p class="small-copy">Outside the United States, use the crisis or emergency resources for your location. This app does not determine your location.</p></div><p v-if="active">Your exercise is paused. Return leaves it paused; use Resume when you choose.</p><p v-if="status === 'interrupted'">Your exercise was interrupted while this panel was open.</p><div class="button-row"><button class="primary" @click="closeSupport">Return to prototype</button><button v-if="active" class="secondary" @click="finish('stopped'); closeSupport()">End exercise</button></div></section></div>
</template>
