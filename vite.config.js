import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// GitHub Pages project site: /Final-Project/
export default defineConfig({
  base: '/Final-Project/',
  plugins: [react()],
  build: {
    rollupOptions: {
      input: {
        index: 'index.html',
        qualified: 'qualified.html',
        thankyou: 'thank-you.html',
      },
    },
  },
})
