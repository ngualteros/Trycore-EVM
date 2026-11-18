import { defineConfig, mergeConfig } from 'vite'
import config from './vite.config.js'

export default defineConfig(({ mode }) => mergeConfig(config({ mode }), {
  test: { include: ['src/test/reference.live.jsx'] },
  // This fixed URL must be the Vite instance proxying the isolated helper server.
  define: { 'import.meta.env.VITE_API_BASE_URL': JSON.stringify('http://127.0.0.1:5174') },
}))
