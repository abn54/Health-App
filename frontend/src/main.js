import { createApp } from 'vue'
import App from './App.vue'
import './style.css'
createApp(App).mount('#app')

if (import.meta.env.DEV && new URLSearchParams(location.search).has('a11y-review')) {
  import('../tests/browser-audit.js')
}
