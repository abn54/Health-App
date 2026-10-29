<script setup>
defineProps({ saved:Object, draft:Object, remembered:String, busy:Boolean, status:String, error:String })
const emit = defineEmits(['detail','history','save','reset','retry','reuse'])
const cueName = cue => cue === 'text' ? 'Text only' : cue === 'animated' ? 'Animated circle' : 'System default'
const statusName = status => ({completed:'Completed',stopped:'Stopped',interrupted:'Interrupted'}[status] || status)
const date = value => new Date(value).toLocaleString([], {dateStyle:'medium',timeStyle:'short'})
</script>
<template>
  <section class="card local-profile" aria-label="Your local profile">
    <details>
      <summary><span><strong>Your local profile</strong><small>{{ saved ? `${saved.reply_detail === 'brief' ? 'Brief' : 'Standard'} replies · saved practice context ${saved.use_history ? 'on' : 'off'}` : 'Optional choices · no account or personal story' }}</small></span><span aria-hidden="true">＋</span></summary>
      <div class="profile-body">
        <p>One profile on this local server, shared by anyone using it. Use an example profile for demos; no name, diagnosis or mood rating is needed.</p>
        <p class="small-copy">Remembered pacing cue: <strong>{{ cueName(remembered) }}</strong>. Change or reset it with the cue controls above.</p>
        <label for="profile-detail">Assistant reply length</label>
        <select id="profile-detail" :value="draft.reply_detail" :disabled="busy" @change="emit('detail',$event.target.value)"><option value="standard">Standard explanations</option><option value="brief">Brief reminders</option></select>
        <label class="audio-check"><input type="checkbox" :checked="draft.use_history" :disabled="busy" @change="emit('history',$event.target.checked)"> Use my cue and saved practice history in replies</label>
        <p class="small-copy">Off by default. When saved on, reviewed app replies can refer to your current/remembered cue and latest saved Completed, Stopped or Interrupted practice. No emotions, improvement or treatment needs are inferred. Raw history is not sent to the model.</p>
        <div class="button-row"><button class="secondary" :disabled="busy" @click="emit('save')">Save profile</button><button class="text-button" :disabled="busy" @click="emit('reset')">Reset profile</button></div>
        <p v-if="status" class="small-copy" role="status">{{ status }}</p>
        <p v-if="error" class="error" role="alert">{{ error }} <button class="text-button" :disabled="busy" @click="emit('retry')">Reload profile</button></p>
        <div v-if="saved?.use_history && !error" class="profile-history">
          <template v-if="saved.latest_practice"><strong>Most recent saved practice</strong><p>{{ statusName(saved.latest_practice.status) }} · {{ date(saved.latest_practice.started_at || saved.latest_practice.created_at) }}<br>Last recorded cue: {{ cueName(saved.latest_practice.cue) }}.</p><button v-if="saved.latest_practice.cue" class="text-button" :disabled="busy" @click="emit('reuse')">Use last practice cue for this visit</button><small>This copies a cue for review. It does not start, remember or resume an exercise.</small></template>
          <p v-else>No saved finished, stopped or interrupted practice yet. Questions alone are not exercise history.</p>
        </div>
        <p class="small-copy">Reset profile restores standard replies and turns saved context off; it keeps your cue and history. History’s Delete all removes local history, cue and profile choices. Voice choices reset on reload.</p>
      </div>
    </details>
  </section>
</template>
