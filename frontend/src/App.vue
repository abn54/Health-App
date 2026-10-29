<script setup>
import { computed, nextTick, onMounted, onUnmounted, ref, watch } from 'vue'
import { Exercise, phraseCue } from './engine.js'
import { AudioOutput } from './audio.js'
import { exerciseAnnouncement } from './accessibility.js'
import AssistantPanel from './components/AssistantPanel.vue'
import LocalProfile from './components/LocalProfile.vue'
import HelpCenter from './components/HelpCenter.vue'
import RhythmGuide from './components/RhythmGuide.vue'
import PauseIllustration from './components/PauseIllustration.vue'
import helpContent from '../../shared/help-content.json'

const reduced = matchMedia('(prefers-reduced-motion: reduce)')
const cue = ref(reduced.matches ? 'text' : 'animated')
const remembered = ref(null), prefStatus = ref(''), view = ref('ready'), support = ref(false)
const status = ref('ready'), reading = ref({ elapsed: 0, cycle: 1, phase: 'Inhale', count: 1, scale: .7 })
const current = ref(null), saved = ref('No session started'), pendingSave = ref(false), appError = ref('')
const history = ref([]), selected = ref(null), historyError = ref(''), deleteConfirm = ref(false)
const questionText = ref(''), messages = ref([]), asking = ref(false), questionError = ref(''), mode = ref('mock')
const capabilities = ref({ live_enabled: false, review_tools: false, attempts: 0, limit: 50 })
const simulateModel = ref(false), simulateSave = ref(false), retryTurn = ref(null), assistantOpen = ref(false)
const assistantPopup = ref(false)
const profileSaved = ref(null), profileDraft = ref({reply_detail:'standard',use_history:false}), profileBusy = ref(false), profileStatus = ref(''), profileError = ref('')
let profileRequest = 0, profileTouched = false
let popupReturnFocus
const replySources = topic => (helpContent.topics[topic]?.sources || []).map(id=>helpContent.resources.find(r=>r.id===id)).filter(Boolean)
const engine = new Exercise()
const voices = ref([]), voiceURI = ref(''), voiceRate = ref(.95), autoRead = ref(false)
const highContrast = ref(matchMedia('(prefers-contrast: more)').matches), largeText = ref(false), screenReaderUpdates = ref('phase')
const exerciseLiveText = computed(() => exerciseAnnouncement(status.value, reading.value, screenReaderUpdates.value))
watch([highContrast, largeText], ([contrast, large]) => {
  document.documentElement.classList.toggle('higher-contrast', contrast)
  document.documentElement.classList.toggle('larger-text', large)
}, {immediate:true})
const audioState = ref({ busy:false, message:'Chatbot voice is off.' }), audioObservations = ref([])
const audio = new AudioOutput({ synth:window.speechSynthesis, Utterance:window.SpeechSynthesisUtterance, changed:state => {
  audioState.value = state
  if (capabilities.value.review_tools) {
    audioObservations.value.push({at:Math.round(performance.now()),message:state.message})
    if (audioObservations.value.length > 80) audioObservations.value.shift()
  }
} })
function refreshVoices() {
  voices.value = audio.refreshVoices()
  if (!voices.value.some(v => v.voiceURI === voiceURI.value)) voiceURI.value = voices.value[0]?.voiceURI || ''
  if (!voices.value.length) autoRead.value = false
}
function stopAudio(message = 'Chatbot voice stopped.') { audio.stop(message) }
function muteAudio() { autoRead.value = false; stopAudio('Chatbot voice stopped. Automatic reading is off.') }
function setVoice(value) { stopAudio(); voiceURI.value = value }
function setVoiceRate(value) { stopAudio(); voiceRate.value = Number(value) }
function setAutoRead(value) { autoRead.value = value; if (!value) stopAudio('Automatic reading turned off.') }
function readReply(text) {
  if (active.value || support.value || document.hidden) return
  audio.speak(text, {voiceURI:voiceURI.value,rate:voiceRate.value, valid:() => !active.value && !support.value && !document.hidden})
}
function previewVoice() {
  if (active.value) return
  audio.speak('Hi, I am mello’s app assistant. You can listen to my replies or read them as text.', {preview:true,voiceURI:voiceURI.value,rate:voiceRate.value, valid:() => !active.value && !support.value && !document.hidden})
}
watch(view, () => {
  stopAudio()
  if (view.value !== 'exercise') nextTick(() => document.querySelector('main h1')?.focus())
}, {flush:'sync'})
const active = computed(() => ['running', 'paused'].includes(status.value))
const terminal = computed(() => ['completed', 'stopped', 'interrupted'].includes(status.value))
const title = computed(() => ({completed:'Six cycles complete.',stopped:'Exercise ended.',interrupted:'Exercise interrupted.'}[status.value] || ''))
let headerObserver
let raf, readyAt = performance.now(), token = 0, saving = false, saveRequested = false, finalizing = false, cueTouched = false
const stamp = () => new Date().toISOString()
const frame = () => new Promise(resolve => requestAnimationFrame(resolve))
const label = s => ({draft:'Not started',running:'In progress',paused:'Paused',completed:'Completed',stopped:'Stopped',interrupted:'Interrupted'}[s] || s)
const seconds = ms => ms == null ? 'Not recorded' : `${(ms / 1000).toFixed(2)} s`
const date = value => new Date(value).toLocaleString([], { dateStyle:'medium', timeStyle:'short' })
const chatDate = value => new Date(value).toLocaleString([], {dateStyle:'medium',timeStyle:'long'})
const sourceLabel = source => ({live:'Live local model',mock:'Prepared reply',fixed:'Fixed fallback'}[source] || source)

async function api(path, options = {}) {
  const controller = new AbortController()
  const timeout = setTimeout(() => controller.abort(), 11000)
  try {
    const response = await fetch('/api' + path, { ...options, headers: { 'Content-Type':'application/json' }, signal:controller.signal })
    if (!response.ok) throw new Error(`Request failed (${response.status})`)
    return await response.json()
  } finally { clearTimeout(timeout) }
}
async function refreshProfile(syncDraft = false) {
  if (profileBusy.value) return
  const request = ++profileRequest
  try {
    const loaded = await api('/profile')
    if (request !== profileRequest) return
    profileSaved.value = loaded
    if (syncDraft && !profileTouched) { profileDraft.value = {reply_detail:loaded.reply_detail,use_history:loaded.use_history}; profileStatus.value = 'Profile loaded from local storage.' }
    profileError.value = ''
  } catch { if (request !== profileRequest) return; profileError.value = 'Profile could not refresh. The last loaded choices may be out of date; practice and support remain available.' }
}
function editProfileDetail(value) { profileTouched = true; profileDraft.value.reply_detail = value }
function editProfileHistory(value) { profileTouched = true; profileDraft.value.use_history = value }
function reloadProfile() { profileTouched = false; void refreshProfile(true) }
async function saveProfile(reset = false) {
  if (profileBusy.value || asking.value) return
  profileRequest += 1
  profileBusy.value = true; profileStatus.value = 'Saving profile…'
  const desired = reset === true ? {reply_detail:'standard',use_history:false} : {...profileDraft.value}
  try {
    const loaded = await api('/profile',{method:'PUT',body:JSON.stringify(desired)})
    profileTouched = false
    profileSaved.value = loaded; profileDraft.value = {reply_detail:loaded.reply_detail,use_history:loaded.use_history}
    profileStatus.value = reset === true ? 'Profile reset locally. Standard replies; saved context off.' : 'Profile saved locally. New replies use these choices.'
    profileError.value = ''
  } catch { profileStatus.value = 'Profile not confirmed saved. Reload before relying on a change.'; profileError.value = 'The profile save could not be confirmed.' }
  finally { profileBusy.value = false }
}
function reuseLastPracticeCue() {
  if (active.value || profileError.value || !profileSaved.value?.latest_practice?.cue) return
  changeCue(profileSaved.value.latest_practice.cue)
  profileStatus.value = 'Last practice cue copied for this visit; not remembered. Start remains your choice.'
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
  if (!pendingSave.value && terminal.value) void refreshProfile()
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
  stopAudio()
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
function pause() { if (status.value !== 'running') return; stopAudio('Chatbot voice stopped while practice is paused.'); engine.pause(); status.value = 'paused'; event('pause'); queueSave() }
function resume() { if (status.value !== 'paused') return; engine.resume(); status.value = 'running'; event('resume'); queueSave() }
async function finish(kind, reason = '') {
  if (!active.value || finalizing) return
  finalizing = true
  stopAudio('Chatbot voice stopped.')
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
function visibility() { if (document.hidden) { stopAudio('Page hidden. Chatbot voice stopped.'); if (active.value) void finish('interrupted', 'Page hidden or left') } }
function pagehide() { stopAudio(); if (active.value) { engine.finish('interrupted'); status.value = 'interrupted' } /* Next page recovers last persisted state; unload writes are not promised. */ }
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
  stopAudio('Crisis support opened. Chatbot voice stopped.')
  if (support.value) return
  if (status.value === 'running') pause()
  if (active.value) { event('support_open'); queueSave() }
  support.value = true
  nextTick(() => document.querySelector('#support-heading')?.focus())
}
function closeSupport() {
  support.value = false
  if (active.value) { event('support_close'); queueSave() }
  nextTick(() => document.querySelector(assistantPopup.value ? '#popup-support-control' : '#support-control')?.focus())
}
function trapSupport(e) {
  if (e.key === 'Escape') { closeSupport(); return }
  if (e.key !== 'Tab') return
  const nodes = [...e.currentTarget.querySelectorAll('button,a[href]')].filter(n => !n.disabled)
  if (e.shiftKey && (document.activeElement === nodes[0] || document.activeElement.id === 'support-heading')) { e.preventDefault(); nodes.at(-1)?.focus() }
  else if (!e.shiftKey && document.activeElement === nodes.at(-1)) { e.preventDefault(); nodes[0]?.focus() }
}
async function openHistory() {
  stopAudio()
  if (status.value === 'running') pause()
  if (active.value) { event('history_open'); queueSave() }
  view.value = 'history'; selected.value = null; historyError.value = ''
  try { history.value = await api('/sessions') } catch { historyError.value = 'History could not load. Retry when the local server is available.' }
}
function returnExercise() { if (view.value === 'history' && active.value) { event('history_close'); queueSave() }; view.value = 'exercise' }
function openAssistant() {
  stopAudio()
  if (status.value === 'running') pause()
  if (view.value === 'history' && active.value) { event('history_close'); queueSave() }
  if (terminal.value && !pendingSave.value && !asking.value && !finalizing) ready()
  void refreshProfile()
  view.value = 'assistant'; assistantOpen.value = true
  nextTick(() => document.querySelector(status.value === 'ready' ? '#app-question' : '#assistant-heading')?.focus())
}
function openAssistantPopup() {
  stopAudio()
  void refreshProfile()
  popupReturnFocus = document.activeElement
  if (status.value === 'running') pause()
  assistantPopup.value = true; assistantOpen.value = true
  nextTick(() => document.querySelector('#assistant-popup-heading')?.focus())
}
function closeAssistantPopup() {
  stopAudio('Assistant closed. Chatbot voice stopped.')
  assistantPopup.value = false
  nextTick(() => {
    if (popupReturnFocus?.isConnected) popupReturnFocus.focus()
    else document.querySelector('#assistant-launcher')?.focus()
  })
}
function newPopupQuestions() {
  ready(); assistantOpen.value = true
  nextTick(() => document.querySelector('#app-question')?.focus())
}
function trapPopup(e) {
  if (support.value) return
  if (e.key === 'Escape') { e.preventDefault(); closeAssistantPopup(); return }
  if (e.key !== 'Tab') return
  const nodes = [...e.currentTarget.querySelectorAll('button,a[href],input,select,summary')].filter(n => !n.disabled && n.getClientRects().length && ![...n.closest('.assistant-popup').querySelectorAll('details:not([open])')].some(d => d.contains(n) && n !== d.querySelector(':scope > summary')))
  if (e.shiftKey && (document.activeElement === nodes[0] || document.activeElement.id === 'assistant-popup-heading')) { e.preventDefault(); nodes.at(-1)?.focus() }
  else if (!e.shiftKey && document.activeElement === nodes.at(-1)) { e.preventDefault(); nodes[0]?.focus() }
}
function ready(discard = false) {
  const leaveUnsaved = discard === true
  if (active.value || finalizing || (!leaveUnsaved && (pendingSave.value || asking.value))) return
  if (leaveUnsaved) { token += 1; saveRequested = false; pendingSave.value = false; retryTurn.value = null; questionError.value = '' }
  stopAudio(); void refreshProfile()
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
  current.value = Object.fromEntries(Object.entries(selected.value).filter(([key]) => !['messages','last_chat_at'].includes(key)))
  messages.value = selected.value.messages.map(m => ({role:m.role,text:m.content,...m.metadata}))
  status.value = 'ready'; view.value = 'ready'; saved.value = 'Saved locally'; selected.value = null; readyAt = performance.now()
}
async function deleteSession(id) {
  if (active.value || asking.value || pendingSave.value) return
  try { await api(`/sessions/${id}`, {method:'DELETE'}); if (current.value?.id === id) { current.value = null; status.value = 'ready'; messages.value = [] }; selected.value = null; await openHistory(); await refreshProfile() }
  catch { historyError.value = 'Deletion failed; the saved record may still exist.' }
}
async function deleteAll() {
  if (active.value || pendingSave.value || asking.value) return
  try { await api('/local-data',{method:'DELETE'}); deleteConfirm.value = false; history.value = []; selected.value = null; current.value = null; status.value = 'ready'; messages.value = []; remembered.value = null; cue.value = reduced.matches ? 'text' : 'animated'; saved.value = 'No session started'; profileTouched = false; await refreshProfile(true) }
  catch { historyError.value = 'Deletion failed; local data may still exist.' }
}
async function ask(retry = false) {
  if (asking.value || profileBusy.value || status.value !== 'ready') return
  const text = retry ? retryTurn.value?.question : questionText.value.trim()
  if (!text) return
  if (phraseCue(text)) openSupport()
  if (!current.value) { newSession(); queueSave() }
  const turn = retry ? retryTurn.value : {turn_id:crypto.randomUUID(),question:text,cue:cue.value,mode:mode.value,simulate_failure:simulateModel.value}
  const thisToken = token, audioEpoch = audio.epoch
  if (!retry) messages.value.push({role:'user',text})
  questionText.value = ''; asking.value = true; questionError.value = ''; retryTurn.value = turn
  try {
    await waitForSave()
    const response = await api(`/sessions/${current.value.id}/messages`, {method:'POST',body:JSON.stringify(turn)})
    if (thisToken === token && !active.value) { messages.value.push({role:'assistant',...response}); if (response.rule_id) openSupport(); else if (autoRead.value && audioEpoch === audio.epoch) readReply(response.text) }
    retryTurn.value = null
    capabilities.value = await api('/health').catch(() => capabilities.value)
  } catch {
    if (thisToken === token && !active.value) questionError.value = 'The optional explanation is unavailable. You can still start or open Crisis support. This turn is not confirmed saved; retry or review History.'
  } finally { asking.value = false }
}

onMounted(async () => {
  if ('ResizeObserver' in window) {
    headerObserver = new ResizeObserver(entries => document.documentElement.style.setProperty('--header-offset', `${entries[0].target.getBoundingClientRect().height + 12}px`))
    const header = document.querySelector('.sidebar')
    if (header) headerObserver.observe(header)
  }
  refreshVoices(); window.speechSynthesis?.addEventListener('voiceschanged', refreshVoices)
  void refreshProfile(true)
  raf = requestAnimationFrame(loop)
  document.addEventListener('visibilitychange', visibility); window.addEventListener('pagehide', pagehide); reduced.addEventListener('change', motionChange)
  try {
    await api('/recover', {method:'POST'})
    const [prefs, health] = await Promise.all([api('/preferences'),api('/health')])
    capabilities.value = health; remembered.value = prefs.cue
    if (prefs.cue && !cueTouched && status.value === 'ready') cue.value = prefs.cue
  } catch { appError.value = 'Local server unavailable. Exercise and Crisis support still work; saving needs the server.' }
})
onUnmounted(() => { headerObserver?.disconnect(); document.documentElement.style.removeProperty('--header-offset'); document.documentElement.classList.remove('higher-contrast','larger-text'); audio.dispose(); window.speechSynthesis?.removeEventListener('voiceschanged', refreshVoices); cancelAnimationFrame(raf); document.removeEventListener('visibilitychange', visibility); window.removeEventListener('pagehide', pagehide); reduced.removeEventListener('change', motionChange) })
</script>

<template>
  <div class="app-shell" :inert="support || assistantPopup || undefined">
    <a class="skip-link" href="#main-content">Skip to main content</a>
    <header class="sidebar">
      <a class="brand" href="#" @click.prevent="active ? returnExercise() : view = 'ready'" aria-label="mello home"><svg class="brand-mark" viewBox="0 0 40 40" aria-hidden="true"><path d="M20 21c-18 0-17-17-8-17 7 0 8 8 8 17Zm0 0c0-18 17-17 17-8 0 7-8 8-17 8Zm0 0c18 0 17 17 8 17-7 0-8-8-8-17Zm0 0c0 18-17 17-17 8 0-7 8-8 17-8Z" fill="currentColor"/></svg><span class="brand-copy">mello<small>a little space to pause</small></span></a>
      <nav aria-label="Main navigation">
        <button :aria-current="view === 'ready' || view === 'exercise' ? 'page' : undefined" :class="{selected:view === 'ready' || view === 'exercise'}" @click="active ? returnExercise() : view = 'ready'"><span aria-hidden="true">◌</span> {{ active ? 'Your exercise' : 'Practice' }}<span class="nav-arrow">↗</span></button>
        <button :class="{selected:view === 'assistant'}" :aria-current="view === 'assistant' ? 'page' : undefined" @click="openAssistant"><span aria-hidden="true">✧</span> AI assistant<span class="nav-arrow" aria-hidden="true">↗</span></button>
        <button :aria-current="view === 'history' ? 'page' : undefined" :class="{selected:view === 'history'}" @click="openHistory"><span aria-hidden="true">▤</span> Session history<span class="nav-arrow">↗</span></button>
      </nav>
      <div class="header-actions"><button id="support-control" class="support-button" @click="openSupport"><span aria-hidden="true">✚</span> Crisis support</button></div>
    </header>
    <div class="main-shell">
      <main id="main-content" tabindex="-1">
      <div class="context-header"><span class="eyebrow">{{ view === 'history' ? 'YOUR SAVED RECORDS' : view === 'assistant' ? 'YOUR OPTIONAL APP ASSISTANT' : 'A LITTLE ROOM TO PRACTICE' }}</span><span class="local-label"><i></i> Local coursework prototype</span></div>
      <div class="coursework-notice"><span class="notice-dot"></span> Coursework prototype · demo use only. Not therapy, diagnosis, or human monitoring.</div>

        <details class="accessibility-tools"><summary>Accessibility options</summary><div class="accessibility-body"><p>Use a keyboard or screen reader throughout. Color is always paired with words. These choices apply to this visit.</p><label><input v-model="highContrast" type="checkbox"> Higher contrast</label><label><input v-model="largeText" type="checkbox"> Larger text</label><label for="screen-reader-updates">Screen-reader breathing updates</label><select id="screen-reader-updates" v-model="screenReaderUpdates"><option value="phase">Phase and cycle</option><option value="count">Each count</option><option value="off">Off</option></select><small>Breathing has no app-generated voice or sounds. Your screen reader can read these updates in its own voice. Announcements may lag; Pause and End are always available. Chatbot voice is separate and optional.</small></div></details>
        <div class="sr-only" role="status" aria-live="polite" aria-atomic="true">{{ exerciseLiveText }}</div>
        <template v-if="view === 'history'">
          <div class="page-heading"><div><div class="eyebrow">A RECORD, WITHOUT A SCORE</div><h1 tabindex="-1">Session history<span>.</span></h1><p>Review saved sessions and when you last chatted. Dates and times use this device’s time zone.</p></div><button class="secondary" @click="active ? returnExercise() : view = 'ready'">{{ active ? 'Return to paused exercise' : 'Back to practice' }} →</button></div>
          <div v-if="active" class="banner">Your exercise is paused. Returning does not resume it.<div><button @click="returnExercise">Return to exercise</button><button @click="finish('stopped')">End exercise</button></div></div>
          <div v-if="historyError" class="error" role="alert">{{ historyError }} <button @click="openHistory">Retry history</button></div>
          <div class="history-layout">
            <section class="card history-list" aria-label="Saved sessions">
              <h2>On this computer <span class="pill">{{ history.length }}</span></h2>
              <p v-if="!history.length">No saved sessions yet.</p>
              <button v-for="item in history" :key="item.id" class="history-row" :class="{chosen:selected?.id === item.id}" @click="selectSession(item.id)"><span><strong>{{ label(item.status) }}</strong><small>Started <time :datetime="item.created_at">{{ date(item.created_at) }}</time></small><small v-if="item.last_chat_at" class="last-chat">Last chatted <time :datetime="item.last_chat_at">{{ chatDate(item.last_chat_at) }}</time></small><small v-else>No chat in this session</small></span><span>{{ seconds(item.assignment_duration_ms) }} ↗</span></button>
            </section>
            <section v-if="selected" class="card history-detail" aria-label="Session detail">
              <div class="eyebrow">PACED BREATHING · {{ selected.content_version }}</div><h2>{{ label(selected.status) }}</h2>
              <p class="session-dates">Started <time :datetime="selected.created_at">{{ date(selected.created_at) }}</time><br><template v-if="selected.last_chat_at">Last chatted <time :datetime="selected.last_chat_at">{{ chatDate(selected.last_chat_at) }}</time></template><template v-else>No chat in this session</template></p><code class="record-id">{{ selected.id }}</code>
              <dl><div><dt>Initial cue</dt><dd>{{ selected.cue_initial || 'Not started' }}</dd></div><div><dt>{{ selected.status === 'interrupted' ? 'Last recorded cue' : 'Final cue' }}</dt><dd>{{ selected.cue_final || 'Not started' }}</dd></div><div><dt>Exercise duration</dt><dd>{{ seconds(selected.assignment_duration_ms) }}</dd></div><div><dt>Wall time / excluded pauses</dt><dd>{{ seconds(selected.wall_ms) }} / {{ seconds(selected.excluded_ms) }}</dd></div><div><dt>Entry and setup</dt><dd>{{ seconds(selected.setup_ms) }}</dd></div></dl>
              <p v-if="selected.status === 'interrupted'">Partial record. A missing final time is unknown, not a completed exercise.</p>
              <div class="button-row"><button v-if="selected.cue_final" class="secondary" :disabled="active || pendingSave || asking" @click="reuse">Use this cue next time</button><button v-if="selected.status === 'draft'" class="secondary" :disabled="active || pendingSave || asking" @click="reopenDraft">Continue these questions</button><button class="text-button danger" :disabled="active || pendingSave || asking" @click="deleteSession(selected.id)">Delete this session</button></div>
              <h3>Saved conversation</h3><p v-if="selected.messages.length" class="small-copy">Message times are shown in this device’s time zone.</p><p v-if="!selected.messages.length">No questions were submitted.</p>
              <div v-for="m in selected.messages" :key="m.id" class="message" :class="m.role"><small>{{ m.role === 'user' ? 'You' : sourceLabel(m.metadata.source) }}</small><time class="message-time" :datetime="m.created_at">{{ chatDate(m.created_at) }}</time><p>{{ m.content }}</p><small v-if="m.metadata.reply_id">{{ m.metadata.reply_id }} · {{ m.metadata.prompt_version }}</small><small v-if="m.metadata.reply_detail">{{ m.metadata.reply_detail === 'brief' ? 'Brief reply' : 'Standard reply' }} · {{ m.metadata.personalization_context?.history_used ? 'Explicit profile + saved practice context' : 'Saved reply-length choice; practice context not used' }}</small><small v-if="m.metadata.note">{{ m.metadata.note }}</small><div class="answer-sources"><a v-for="r in replySources(m.metadata.reply_id)" :key="r.id" :href="r.url" target="_blank" rel="noopener noreferrer">{{ r.label }} ↗</a></div></div>
              <details><summary>Recorded events ({{ selected.events.length }})</summary><ol><li v-for="e in selected.events" :key="e.id">{{ e.type }} · {{ seconds(e.elapsed_ms) }} <span v-if="Object.keys(e.details).length">{{ e.details }}</span></li></ol></details>
            </section>
            <div v-else class="history-empty"><span>↖</span><h2>Choose a saved session.</h2><p>Its timing, settings, and conversation appear here.</p></div>
          </div>
          <div class="delete-all"><button class="text-button danger" :disabled="active || pendingSave || asking" @click="deleteConfirm = !deleteConfirm">Delete all local history and preferences</button><div v-if="deleteConfirm" class="banner">This removes local records, cue and profile choices. Model-attempt accounting is retained.<div><button @click="deleteConfirm = false">Cancel</button><button @click="deleteAll">Confirm delete all</button></div></div></div>
        </template>
        <template v-else-if="view === 'assistant'">
          <div class="page-heading"><div><div class="eyebrow">OPTIONAL QUESTIONS, AT YOUR PACE</div><h1 id="assistant-heading" tabindex="-1">AI assistant<span>.</span></h1><p>Ask about pacing, controls, settings, and saved history.</p></div><button class="secondary" @click="active ? returnExercise() : view = 'ready'">{{ active ? 'Return to paused exercise' : 'Back to practice' }} →</button></div>
          <div v-if="active" class="banner">Your exercise is paused at cycle {{ reading.cycle }}, {{ reading.phase.toLowerCase() }} count {{ reading.count }}. End it before asking new questions, or return to continue.<div><button @click="returnExercise">Return to exercise</button><button @click="finish('stopped')">End exercise</button></div></div>
          <div v-else-if="terminal" class="banner">{{ pendingSave ? 'Finish saving this session before starting new questions.' : 'This session has ended. You can start new questions or return to its summary.' }}<div><button @click="returnExercise">Return to summary</button><button :disabled="pendingSave || asking || finalizing" @click="openAssistant">Start new questions</button></div></div>
        </template>
        <template v-else-if="status === 'ready'">
          <div class="page-heading ready-heading"><div class="hero-copy"><span class="welcome-pill"><span aria-hidden="true">✳</span> A small pause starts here</span><h1 tabindex="-1">Take a little<br><em>breathing room.</em></h1><p>One simple practice. A minute at your pace.<br>No writing, no score, and your choice to stop.</p></div><PauseIllustration /></div>
          <div class="practice-grid">
            <section class="practice-card">
              <div class="card-top"><span class="pill"><span aria-hidden="true">◌</span> THE BREATHING PRACTICE</span><span class="duration">60 seconds</span></div>
              <div class="practice-description"><h2>In, out.<br>One count at a time.</h2><p>Four counts in. Six counts out.<br>Follow the words, with or without motion.</p></div>
              <button class="primary start-button" @click="start">Start 60-second exercise <span aria-hidden="true">→</span></button><small class="card-footnote">No question or model response needed to start.</small>
              <div class="preview-orbit"><div class="preview-circle"><span>4 <i>/</i> 6</span><small>INHALE / EXHALE</small></div><span class="orbit-label">SIX CYCLES · ONE SECOND PER COUNT</span></div>
              <RhythmGuide />
            </section>
            <div class="side-stack"><section class="card settings-card"><div class="eyebrow">A LITTLE MORE YOU</div><h2>Your pace. Your cue.</h2><p>Same rhythm. A different way to follow it.</p><div class="cue-options" role="group" aria-label="Pacing cue"><button :aria-pressed="cue === 'animated'" @click="changeCue('animated')"><span>◯</span><strong>Animated circle</strong><small>Movement + words</small></button><button :aria-pressed="cue === 'text'" @click="changeCue('text')"><span>Aa</span><strong>Text only</strong><small>Words + count</small></button></div><p class="small-copy">{{ remembered ? `Remembered setting: ${remembered === 'text' ? 'Text only' : 'Animated circle'}.` : 'Nothing remembered. Your system motion setting is the default.' }} You can change the cue during the exercise.</p><div class="button-row"><button class="text-button" @click="remember">Remember this choice</button><button v-if="remembered" class="text-button" @click="resetPreference">Reset preference</button></div><p v-if="prefStatus" role="status" class="small-copy">{{ prefStatus }}</p></section>
            <section class="about-card"><span class="tiny-spark" aria-hidden="true">☼</span><div><h3>A practice, without a score.</h3><p>There is no rating to enter and no outcome to prove. History records only what happened in this prototype.</p></div></section></div>
          </div>
        </template>
        <template v-else>
          <section v-if="active" class="exercise-panel" :data-phase="status === 'paused' ? 'paused' : reading.phase.toLowerCase()" aria-label="Active exercise"><div class="exercise-top"><span class="eyebrow">{{ status === 'paused' ? 'PAUSED · YOUR CHOICE TO CONTINUE' : 'FOLLOW THE WORDS AND COUNT' }}</span><span class="pill">Cycle {{ reading.cycle }} of 6</span></div><div class="phase-key" role="group" aria-label="Phase colors"><span :class="{current:status === 'running' && reading.phase === 'Inhale'}"><i class="phase-dot inhale-dot"></i> Inhale · 4</span><span :class="{current:status === 'running' && reading.phase === 'Exhale'}"><i class="phase-dot exhale-dot"></i> Exhale · 6</span></div><div class="exercise-space"><div v-if="cue === 'animated'" class="breathing-orbit" :style="{'--breath-scale':reading.scale}" aria-hidden="true"><div></div></div><div class="instruction"><span class="phase-tag">{{ status === 'paused' ? 'Your place is held' : reading.phase === 'Inhale' ? 'Expand · green cue' : 'Release · blue cue' }}</span><h1 id="exercise-heading" tabindex="-1">{{ status === 'paused' ? 'Paused' : reading.phase }}</h1><div class="count">{{ reading.count }}<span> / {{ reading.phase === 'Inhale' ? 4 : 6 }}</span></div><p>{{ status === 'paused' ? `Holding ${reading.phase.toLowerCase()}, count ${reading.count}.` : reading.phase === 'Inhale' ? 'Four counts in.' : 'Six counts out.' }}</p></div></div><div class="cycle-dots" aria-hidden="true"><span v-for="n in 6" :key="n" :class="{passed:n < reading.cycle,current:n === reading.cycle}"></span></div><progress max="60000" :value="reading.elapsed" aria-label="Exercise progress" :aria-valuetext="`Cycle ${reading.cycle} of 6, ${reading.phase.toLowerCase()}, count ${reading.count}`"></progress><div class="exercise-controls"><button v-if="status === 'running'" class="primary" @click="pause">Ⅱ Pause</button><button v-else class="primary" @click="resume">Resume →</button><button class="secondary" @click="finish('stopped')">End exercise</button></div><div class="cue-inline"><label for="active-cue">Pacing cue</label><select id="active-cue" :value="cue" @change="changeCue($event.target.value)"><option value="animated">Animated circle</option><option value="text">Text only</option></select><small>Changing the cue keeps your place.</small></div></section>
          <section v-else class="summary-panel"><span class="summary-icon">{{ status === 'completed' ? '✓' : '◌' }}</span><div class="eyebrow">{{ label(status) }} · PACED BREATHING</div><h1 id="summary-heading" tabindex="-1">{{ title }}</h1><p>{{ status === 'completed' ? 'The planned sequence has finished. Stay here as long as you like.' : status === 'interrupted' ? 'The page was hidden or scheduling stopped. Review your settings before starting a new exercise.' : 'This is a partial session. You can review it or return when you choose.' }}</p><div class="timing-grid"><div><strong>{{ seconds(current?.assignment_duration_ms) }}</strong><span>{{ status === 'completed' ? 'Measured exercise' : 'Partial exercise time' }}</span></div><div><strong>{{ seconds(current?.setup_ms) }}</strong><span>Entry and setup</span></div><div><strong>{{ seconds(current?.excluded_ms) }}</strong><span>User pause / support</span></div></div><p class="small-copy">Timing includes application and render delays. Explicit pause and support intervals are excluded once. Interrupted sessions do not establish completion.</p><div class="button-row"><button class="primary" :disabled="pendingSave || asking || finalizing" @click="ready">Return to ready →</button><button class="secondary" @click="openHistory">Review saved history</button></div><div v-if="pendingSave" class="unsaved-exit"><p class="small-copy">You can leave without waiting for a save. Unsaved changes may be lost; records already saved remain in History.</p><button class="secondary" @click="ready(true)">Leave without saving</button></div></section>
        </template>
        <LocalProfile v-if="status === 'ready' && (view === 'ready' || view === 'assistant')" :saved="profileSaved" :draft="profileDraft" :remembered="remembered" :busy="profileBusy || asking" :status="profileStatus" :error="profileError" @detail="editProfileDetail" @history="editProfileHistory" @save="saveProfile()" @reset="saveProfile(true)" @retry="reloadProfile" @reuse="reuseLastPracticeCue" />
        <AssistantPanel v-if="!assistantPopup && (view === 'assistant' || (view === 'ready' && status === 'ready'))" v-model:mode="mode" v-model:question-text="questionText" v-model:expanded="assistantOpen" :messages="messages" :capabilities="capabilities" :profile="profileSaved" :profile-error="profileError" :profile-busy="profileBusy" :asking="asking" :question-error="questionError" :retry-available="!!retryTurn" :ready="status === 'ready'" :voices="voices" :voice-u-r-i="voiceURI" :voice-rate="voiceRate" :auto-read="autoRead" :audio-state="audioState" @voice="setVoice" @rate="setVoiceRate" @preview="previewVoice" @auto-read="setAutoRead" @read="readReply" @stop="muteAudio" @ask="ask" />
        <HelpCenter v-if="view === 'assistant' || (view === 'ready' && status === 'ready')" />
        <div class="save-bar" role="status" :aria-live="active ? 'off' : 'polite'"><span :class="['save-dot',{unsaved:pendingSave}]"></span>{{ saved }} <button v-if="pendingSave" @click="retrySave">Retry save</button></div><p v-if="appError" class="small-copy error">{{ appError }}</p>
        <details v-if="capabilities.review_tools" class="review-tools"><summary>Coursework review tools</summary><p>Deliberate failure simulations for fictional verification. They never disable exercise or Crisis support.</p><label><input v-model="simulateModel" type="checkbox"> Simulate optional model failure</label><label><input v-model="simulateSave" type="checkbox"> Simulate session-save failure</label><details class="audio-observations"><summary>Audio playback observations (browser events, not an audio recording)</summary><ol><li v-for="(entry,i) in audioObservations" :key="i">{{ entry.at }} ms · {{ entry.message }}</li></ol></details><small>Model: {{ capabilities.model }} · host run: {{ capabilities.test_run_id }} · attempts: {{ capabilities.attempts }}/{{ capabilities.limit }}. Mock remains the default.</small></details>
      </main><footer>MELLO / A COURSEWORK SKILLS PROTOTYPE<span>YOUR CHOICE TO START. YOUR CHOICE TO STOP.</span></footer>
    </div>
    <div class="assistant-dock" role="region" aria-label="Assistant shortcut"><span>A little help, when you choose.</span><button id="assistant-launcher" class="assistant-launcher" aria-label="Ask the assistant" title="Ask the assistant" aria-haspopup="dialog" :aria-expanded="assistantPopup" @click="openAssistantPopup"><svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M20 11.5a8 8 0 0 1-8 8H5l-3 2v-10a9 9 0 0 1 18 0Z" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/><path d="m12 7 1.1 2.9L16 11l-2.9 1.1L12 15l-1.1-2.9L8 11l2.9-1.1L12 7Z" fill="currentColor"/></svg></button></div>
  </div>
  <div v-if="assistantPopup" class="assistant-scrim" :inert="support || undefined" @keydown="trapPopup">
    <section class="assistant-popup" role="dialog" aria-modal="true" aria-labelledby="assistant-popup-heading" aria-describedby="assistant-popup-description">
      <div class="assistant-popup-top"><div><span class="eyebrow">A LITTLE CLARITY, WHEN YOU WANT IT</span><h2 id="assistant-popup-heading" tabindex="-1"><span aria-hidden="true">✧</span> AI assistant</h2></div><button class="popup-close" aria-label="Close assistant" @click="closeAssistantPopup">×</button></div>
      <div class="assistant-popup-tools"><p id="assistant-popup-description">Coursework prototype · app assistant</p><button id="popup-support-control" class="support-button" @click="openSupport">Crisis support</button></div>
      <div v-if="active" class="banner">Your exercise is paused at {{ reading.phase.toLowerCase() }} count {{ reading.count }}. Close this window to return; Resume remains your choice.<div><button @click="returnExercise(); closeAssistantPopup()">Return to exercise</button><button @click="finish('stopped'); closeAssistantPopup()">End exercise</button></div></div>
      <div v-else-if="terminal" class="banner">This session has ended.<div><button :disabled="pendingSave || asking || finalizing" @click="newPopupQuestions">Start new questions</button><button @click="closeAssistantPopup">Return to summary</button></div></div>
      <AssistantPanel v-model:mode="mode" v-model:question-text="questionText" v-model:expanded="assistantOpen" :messages="messages" :capabilities="capabilities" :profile="profileSaved" :profile-error="profileError" :profile-busy="profileBusy" :asking="asking" :question-error="questionError" :retry-available="!!retryTurn" :ready="status === 'ready'" :voices="voices" :voice-u-r-i="voiceURI" :voice-rate="voiceRate" :auto-read="autoRead" :audio-state="audioState" @voice="setVoice" @rate="setVoiceRate" @preview="previewVoice" @auto-read="setAutoRead" @read="readReply" @stop="muteAudio" popup @ask="ask" />
      <div class="popup-save"><span role="status">{{ saved }}</span><button v-if="pendingSave" @click="retrySave">Retry save</button><button @click="closeAssistantPopup">Close assistant →</button></div>
    </section>
  </div>
  <div v-if="support" class="modal-scrim" @keydown="trapSupport"><section class="support-panel" role="dialog" aria-modal="true" aria-labelledby="support-heading"><div class="eyebrow">AVAILABLE INDEPENDENTLY OF THE APP SERVER</div><h1 id="support-heading" tabindex="-1">Crisis support</h1><p>This coursework prototype cannot respond to a crisis or connect you to a person. Nobody monitors this app.</p><div class="resource-card"><span class="pill">UNITED STATES</span><h2>988 Suicide &amp; Crisis Lifeline</h2><p><a href="tel:988?oai_link_source=model_response_hotline">Call 988</a><a href="sms:988?oai_link_source=model_response_hotline">Text 988</a></p><a href="https://988lifeline.org/chat/?oai_link_source=model_response_hotline" target="_blank" rel="noopener noreferrer">Open Lifeline chat ↗</a><p class="small-copy">Outside the United States, use the crisis or emergency resources for your location. This app does not determine your location.</p></div><p v-if="active">Your exercise is paused. Return leaves it paused; use Resume when you choose.</p><p v-if="status === 'interrupted'">Your exercise was interrupted while this panel was open.</p><div class="button-row"><button class="primary" @click="closeSupport">Return to prototype</button><button v-if="active" class="secondary" @click="finish('stopped'); closeSupport()">End exercise</button></div></section></div>
</template>
