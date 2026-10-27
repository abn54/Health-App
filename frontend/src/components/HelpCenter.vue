<script setup>
import { ref } from 'vue'
import content from '../../../shared/help-content.json'
defineProps({compact:Boolean})
const group = ref('practice')
const sources = topic => content.topics[topic].sources.map(id=>content.resources.find(r=>r.id===id))
</script>

<template>
  <section class="help-center" aria-labelledby="faq-heading">
    <div class="help-heading"><div><div class="eyebrow">A LITTLE CLARITY</div><h2 id="faq-heading">Good questions. Clear answers.</h2></div><span class="faq-count">{{ content.faqs.length }} quick answers</span></div>
    <p class="help-intro">No questionnaire to complete. Explore only what you want to know.</p>
    <div class="faq-filters" role="group" aria-label="FAQ topics"><button v-for="g in content.faq_groups" :key="g.id" :aria-pressed="group === g.id" @click="group=g.id">{{ g.label }}</button></div>
    <div class="faq-list"><details v-for="faq in content.faqs.filter(f=>f.group === group)" :key="faq.topic"><summary>{{ faq.question }}<span aria-hidden="true">＋</span></summary><p>{{ content.topics[faq.topic].answer }}</p><div v-if="sources(faq.topic).length" class="answer-sources"><a v-for="r in sources(faq.topic)" :key="r.id" :href="r.url" target="_blank" rel="noopener noreferrer">{{ r.label }} ↗</a></div></details></div>
    <details class="reading-disclosure"><summary><span>Explore the reading shelf<small>Source types and limits, shown upfront</small></span><span aria-hidden="true">↗</span></summary><p class="small-copy">External reading is optional. These sources do not validate this prototype or provide a personal assessment. Handbook text has not been supplied.</p><div class="reading-grid"><a v-for="r in content.resources" :key="r.id" :href="r.url" target="_blank" rel="noopener noreferrer" class="reading-card"><svg viewBox="0 0 48 48" fill="none" aria-hidden="true"><path v-if="r.icon === 'book'" d="M8 11h13l3 3 3-3h13v26H27l-3 3-3-3H8V11Zm16 3v26"/><path v-else-if="r.icon === 'leaf'" d="M10 34C7 14 24 8 39 9c0 17-9 31-26 28m1-3 17-17M19 29l-1-9m6 4h9"/><path v-else d="m24 6 17 18-17 18L7 24 24 6Zm6 12-12 4 1 10 11-14Z"/></svg><span class="reading-kind">{{ r.kind }}</span><h3>{{ r.title }} <span aria-hidden="true">↗</span></h3><p>{{ r.description }}</p><small>{{ r.label }}</small></a></div></details>
  </section>
</template>
