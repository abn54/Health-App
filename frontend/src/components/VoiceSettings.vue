<script setup>
defineProps({ idPrefix:String, breathingSound:String, voices:Array, voiceURI:String, audioState:Object, active:Boolean })
const emit = defineEmits(['sound','voice','preview','stop'])
</script>
<template>
  <details class="voice-settings">
    <summary>Voice &amp; sound <small>Optional · off by default</small></summary>
    <div class="voice-body">
      <label :for="`${idPrefix}-sound`">Breathing sound</label>
      <select :id="`${idPrefix}-sound`" :value="breathingSound" @change="emit('sound',$event.target.value)"><option value="off">Off</option><option value="voice" :disabled="!voices.length">Spoken inhale / exhale</option><option value="tone">Soft tones</option></select>
      <p class="small-copy">One cue at each phase: “Inhale” or “Exhale.” Tones rise for inhale and fall for exhale. Changing sound during practice takes effect at the next phase.</p>
      <label :for="`${idPrefix}-voice`">On-device English voice</label>
      <select :id="`${idPrefix}-voice`" :value="voiceURI" :disabled="!voices.length" @change="emit('voice',$event.target.value)"><option v-if="!voices.length" value="">No local English voice available</option><option v-for="v in voices" :key="v.voiceURI" :value="v.voiceURI">{{ v.name }} ({{ v.lang }})</option></select>
      <div class="button-row"><button class="text-button" :disabled="!voices.length || active" @click="emit('preview')">Preview voice</button><button class="text-button" @click="emit('stop')">Stop audio</button></div>
      <p class="small-copy" role="status">{{ audioState.message }}</p>
      <p class="small-copy">No microphone or audio recording. Only on-device browser voices are offered. Availability and volume depend on your browser/device. Sound choices reset on reload.</p>
    </div>
  </details>
</template>
