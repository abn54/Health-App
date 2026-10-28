<script setup>
import { nextTick, ref, watch } from 'vue'
import content from '../../../shared/help-content.json'
import { enhancedVoice } from '../audio.js'
const props = defineProps({
  messages: {type:Array,default:()=>[]}, mode:String, questionText:String,
  capabilities:Object, asking:Boolean, questionError:String, retryAvailable:Boolean,
  ready:Boolean, expanded:Boolean, popup:Boolean, profile:Object, profileError:String, profileBusy:Boolean, voices:Array, voiceURI:String, voiceRate:Number, autoRead:Boolean, audioState:Object,
})
const emit = defineEmits(['update:mode','update:questionText','update:expanded','ask','voice','auto-read','read','stop','rate','preview'])
const scrollArea = ref(null)
watch(() => props.messages.length, async () => {
  await nextTick()
  if (props.popup && scrollArea.value) scrollArea.value.scrollTop = scrollArea.value.scrollHeight
})
const sourceLabel = s => ({live:'Live local model',mock:'Mock response',fixed:'Fixed fallback'}[s] || s)
const sources = topic => (content.topics[topic]?.sources || []).map(id=>content.resources.find(r=>r.id===id)).filter(Boolean)
function sendOnEnter(event) {
  if (!event.isComposing && props.ready && !props.asking && !props.profileBusy && props.questionText.trim()) emit('ask',false)
}
function suggest(question) {
  emit('update:questionText',question)
  document.querySelector('#app-question')?.focus()
}
</script>

<template>
  <section class="card questions-card" :class="{'assistant-questions':popup}">
    <component :is="popup ? 'div' : 'details'" class="assistant-container" :open="expanded" @toggle="emit('update:expanded',$event.target.open)">
      <summary v-if="!popup"><span><strong>Questions, without the pressure.</strong><small>Optional · app help and reviewed general information</small></span><span aria-hidden="true">＋</span></summary>
      <div class="question-body">
        <div ref="scrollArea" class="assistant-scroll">
        <p>Use fictional questions. I can explain reviewed information, but I am not a therapist and cannot diagnose or provide treatment.</p>
        <details class="suggestion-disclosure" :open="!messages.length"><summary>Suggested questions</summary><div class="suggested-questions" role="group" aria-label="Suggested questions">
          <button v-for="q in content.suggestions" :key="q" :disabled="asking || profileBusy || !ready" @click="suggest(q)">{{ q }} <span aria-hidden="true">↗</span></button>
        </div></details>
        <details class="assistant-options"><summary>Reply &amp; voice options</summary><div class="assistant-options-body">
        <div class="mode-row"><label for="reply-mode">Reply mode <select id="reply-mode" :value="mode" :disabled="asking" @change="emit('update:mode',$event.target.value)"><option value="mock">Mock (default)</option><option value="live" :disabled="!capabilities.live_enabled">Live local model</option></select></label><small v-if="mode === 'live'">Local Ollama · this question and approved facts. Earlier messages stay in History. {{ capabilities.attempts }}/{{ capabilities.limit }} host attempts used.</small></div>
        <p class="assistant-context small-copy">{{ profileError ? 'Profile status unavailable. Check Your local profile before relying on saved choices.' : profile ? `${profile.reply_detail === 'brief' ? 'Brief reminders' : 'Standard explanations'} · saved practice context ${profile.use_history ? 'on' : 'off'}. Change or reset this in Your local profile on Practice.` : 'Loading optional profile choices… Practice and support remain available.' }} Profile and usage history stay outside the model; reviewed local rules tailor displayed replies.</p>
        <section class="assistant-audio" aria-labelledby="chatbot-voice-heading" :class="{'voice-playing':audioState.busy}">
          <div class="voice-heading"><h3 id="chatbot-voice-heading"><span aria-hidden="true">◖))</span> Chatbot voice</h3><span class="voice-state">{{ audioState.busy ? 'Playing' : autoRead ? 'Auto-read on' : 'Read when you choose' }}</span></div>
          <p id="voice-help" class="small-copy">Voice is only for chatbot replies. Enhanced voices appear first when your device offers them; novelty voices are hidden. Sound quality depends on the voices installed on your device.</p>
          <label for="assistant-voice">Reply voice</label><select id="assistant-voice" :value="voiceURI" :disabled="!voices.length" aria-describedby="voice-help" @change="emit('voice',$event.target.value)"><option v-if="!voices.length" value="">No suitable on-device English voice available</option><option v-for="v in voices" :key="v.voiceURI" :value="v.voiceURI">{{ v.name }} · {{ v.lang }}{{ enhancedVoice(v) ? ' · enhanced option' : '' }}</option></select>
          <label for="assistant-speed">Voice speed</label><select id="assistant-speed" :value="voiceRate" @change="emit('rate',$event.target.value)"><option :value=".85">Slower</option><option :value=".95">Relaxed (default)</option><option :value="1.05">Regular</option></select>
          <label class="audio-check" :class="{'auto-read-enabled':autoRead}"><input type="checkbox" :checked="autoRead" :disabled="!voices.length || !ready" @change="emit('auto-read',$event.target.checked)"> Read new replies aloud</label>
          <div class="voice-actions"><button class="voice-play" :disabled="!voices.length || !ready" @click="emit('preview')"><span aria-hidden="true">▶</span> Preview voice</button><button class="voice-stop" @click="emit('stop')"><span aria-hidden="true">■</span> Stop voice</button></div>
          <p class="small-copy" role="status">{{ audioState.message }}</p><p class="small-copy">Blue plays; red stops. Labels and symbols identify both actions. No microphone or recording. Auto-read resets off after reload. If you use a screen reader, leave auto-read off to avoid two voices.</p>
        </section>
        </div></details>
        <div class="conversation" role="log" aria-label="Assistant conversation" :aria-live="autoRead || audioState.busy ? 'off' : 'polite'" aria-relevant="additions">
          <div v-if="!messages.length" class="assistant-welcome"><span class="assistant-glyph" aria-hidden="true">✧</span><div><strong>A little clarity before you begin.</strong><p>Choose a question above or write your own. Asking is always optional.</p></div></div>
          <div v-for="(m,i) in messages" :key="i" class="message" :class="m.role"><small>{{ m.role === 'user' ? 'Fictional question' : sourceLabel(m.source) }}</small><p>{{ m.text }}</p><small v-if="m.reply_detail">{{ m.reply_detail === 'brief' ? 'Brief reply' : 'Standard reply' }} · {{ m.personalization_context?.history_used ? 'Explicit profile + saved practice context' : 'Saved reply-length choice; practice context not used' }}</small><button v-if="m.role === 'assistant'" class="read-reply voice-play" :aria-label="`Read assistant reply ${messages.slice(0,i+1).filter(m=>m.role === 'assistant').length} aloud`" :disabled="!voices.length || !ready" @click="emit('read',m.text)">Read reply aloud</button><small v-if="m.note">{{ m.note }}</small><div v-if="sources(m.reply_id).length" class="answer-sources"><a v-for="r in sources(m.reply_id)" :key="r.id" :href="r.url" target="_blank" rel="noopener noreferrer">{{ r.label }} ↗</a></div></div>
          <p v-if="asking" role="status">Getting an optional explanation…</p><p v-if="questionError" class="error" role="alert">{{ questionError }}</p><button v-if="retryAvailable && !asking && questionError && ready" @click="emit('ask',true)">Retry this question</button>
        </div>
        </div>
        <form class="chat-composer" @submit.prevent="emit('ask',false)">
          <label for="app-question">Your fictional question</label>
          <div class="composer-surface">
            <textarea id="app-question" :value="questionText" maxlength="500" rows="2" aria-describedby="question-help" placeholder="Ask mello about this practice…" :disabled="asking || profileBusy || !ready" @input="emit('update:questionText',$event.target.value)" @keydown.enter.exact.prevent="sendOnEnter" />
            <div class="composer-actions"><span class="composer-hint">App questions · your choice</span><button class="composer-voice" type="button" :aria-pressed="autoRead" :disabled="!voices.length || !ready" @click="emit('auto-read',!autoRead)"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 10v4m4-7v10m4-13v16m4-13v10m4-7v4" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg><span>Read replies</span></button><button v-if="audioState.busy" class="voice-stop composer-stop" type="button" @click="emit('stop')">Stop voice</button><button class="composer-send" :disabled="asking || profileBusy || !ready || !questionText.trim()" type="submit" aria-label="Send question"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 19V5m-6 6 6-6 6 6" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg></button></div>
          </div><small id="question-help">{{ questionText.length }}/500 · fictional inputs only · Enter to send, Shift+Enter for a new line.</small><p class="composer-voice-status" role="status">{{ audioState.busy ? audioState.message : autoRead ? 'Reply voice on. New replies will be read aloud.' : 'Reply voice off. Read or listen when you choose.' }}</p>
        </form>
      </div>
    </component>
  </section>
</template>
