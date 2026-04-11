import type { Config } from 'tailwindcss'

export default {
  content: [
    './app/**/*.{js,ts,jsx,tsx,vue}',
    './components/**/*.{js,ts,jsx,tsx,vue}',
  ],
  theme: {
    extend: {},
  },
  plugins: [],
} satisfies Config