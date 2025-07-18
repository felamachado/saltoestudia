import { defineConfig } from 'vite'

export default defineConfig({
  server: {
    allowedHosts: 'all',
    host: '0.0.0.0',
    port: 3000,
    strictPort: true,
    cors: true
  }
}) 