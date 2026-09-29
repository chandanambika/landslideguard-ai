/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        hazard: {
          low: '#10B981',
          moderate: '#F59E0B',
          high: '#F97316',
          critical: '#EF4444',
        }
      }
    },
  },
  plugins: [],
}
