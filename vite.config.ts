import { defineConfig } from 'vite'

// The demo-day deck is watched live through `tailscale serve` (https://*.ts.net), so the dev server
// must accept that host name.
export default defineConfig({
  server: {
    allowedHosts: ['.ts.net'],
  },
})
