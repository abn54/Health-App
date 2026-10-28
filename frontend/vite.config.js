import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
export default defineConfig({ plugins: [vue()], server: { host: '127.0.0.1', proxy: { '/api': process.env.MELLO_REVIEW_API || 'http://127.0.0.1:8000' } } })
