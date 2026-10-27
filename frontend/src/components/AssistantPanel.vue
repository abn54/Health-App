<script setup>
import content from '../../../shared/help-content.json'
const props = defineProps({
  messages: {type:Array,default:()=>[]}, mode:String, questionText:String,
  capabilities:Object, asking:Boolean, questionError:String, retryAvailable:Boolean,
  ready:Boolean, expanded:Boolean, popup:Boolean, voices:Array, voiceURI:String, autoRead:Boolean, audioState:Object,
})
const emit = defineEmits(['update:mode','update:questionText','update:expanded','ask','voice','auto-read','read','stop'])
const sourceLabel = s => ({live:'Live local model',mock:'Mock response',fixed:'Fixed fallback'}[s] || s)
const sources = topic => (content.topics[topic]?.sources || []).map(id=>content.resources.find(r=>r.id===id)).filter(Boolean)
function suggest(question) {
  emit('update:questionText',question)
  document.querySelector('#app-question')?.focus()
}
</script>

<template>
  <section class="card questions-card" :class="{'assistant-questions':popup}">
    <details :open="expanded" @toggle="emit('update:expanded',$event.target.open)">
      <summary><span><strong>Questions, without the pressure.</strong><small>Optional · app help and reviewed general information</small></span><span aria-hidden="true">＋</span></summary>
      <div class="question-body">
        <p>Use fictional questions. I can explain reviewed information, but I am not a therapist and cannot diagnose or provide treatment.</p>
        <details class="suggestion-disclosure" :open="!messages.length"><summary>Suggested questions</summary><div class="suggested-questions" role="group" aria-label="Suggested questions">
          <button v-for="q in content.suggestions" :key="q" :disabled="asking || !ready" @click="suggest(q)">{{ q }} <span aria-hidden="true">↗</span></button>
        </div></details>
        <div class="mode-row"><label for="reply-mode">Reply mode <select id="reply-mode" :value="mode" :disabled="asking" @change="emit('update:mode',$event.target.value)"><option value="mock">Mock (default)</option><option value="live" :disabled="!capabilities.live_enabled">Live local model</option></select></label><small v-if="mode === 'live'">Local Ollama · this question and approved facts. Earlier messages stay in History. {{ capabilities.attempts }}/{{ capabilities.limit }} host attempts used.</small></div>
        <div class="assistant-audio">
          <label for="assistant-voice">Reply voice</label><select id="assistant-voice" :value="voiceURI" :disabled="!voices.length" @change="emit('voice',$event.target.value)"><option v-if="!voices.length" value="">No on-device English voice available</option><option v-for="v in voices" :key="v.voiceURI" :value="v.voiceURI">{{ v.name }} ({{ v.lang }})</option></select>
          <label class="audio-check"><input type="checkbox" :checked="autoRead" :disabled="!voices.length || !ready" @change="emit('auto-read',$event.target.checked)"> Read new replies aloud</label>
          <button class="text-button" @click="emit('stop')">Stop audio</button>
          <p class="small-copy" role="status">{{ audioState.message }}</p><p class="small-copy">Optional on-device speech · no microphone or recording. Off again after reload.</p>
        </div>
        <div class="conversation" role="log" aria-label="Assistant conversation" aria-live="polite" aria-relevant="additions">
          <div v-if="!messages.length" class="assistant-welcome"><span class="assistant-glyph" aria-hidden="true">✧</span><div><strong>A little clarity before you begin.</strong><p>Choose a question above or write your own. Asking is always optional.</p></div></div>
          <div v-for="(m,i) in messages" :key="i" class="message" :class="m.role"><small>{{ m.role === 'user' ? 'Fictional question' : sourceLabel(m.source) }}</small><p>{{ m.text }}</p><button v-if="m.role === 'assistant'" class="read-reply text-button" :disabled="!voices.length || !ready" @click="emit('read',m.text)">Read reply aloud</button><small v-if="m.note">{{ m.note }}</small><div v-if="sources(m.reply_id).length" class="answer-sources"><a v-for="r in sources(m.reply_id)" :key="r.id" :href="r.url" target="_blank" rel="noopener noreferrer">{{ r.label }} ↗</a></div></div>
          <p v-if="asking" role="status">Getting an optional explanation…</p><p v-if="questionError" class="error" role="alert">{{ questionError }}</p><button v-if="retryAvailable && !asking && questionError && ready" @click="emit('ask',true)">Retry this question</button>
        </div>
        <form @submit.prevent="emit('ask',false)"><label for="app-question">Your fictional question</label><div class="input-row"><input id="app-question" :value="questionText" maxlength="500" placeholder="What would you like to know about this practice?" :disabled="asking || !ready" @input="emit('update:questionText',$event.target.value)"><button class="primary" :disabled="asking || !ready || !questionText.trim()" type="submit">Ask →</button></div><small>{{ questionText.length }}/500 characters · fictional inputs only</small></form>
      </div>
    </details>
  </section>
</template>
