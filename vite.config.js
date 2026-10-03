import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// GitHub Pages project site: /pareto-final-project/
export default defineConfig({
  base: '/pareto-final-project/',
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
