import type { Config } from "tailwindcss";

export default {
  content: [
    "./app/**/*.{js,ts,jsx,tsx,vue}",
    "./components/**/*.{js,ts,jsx,tsx,vue}",
    "./pages/**/*.{js,ts,jsx,tsx,vue}",
    "./layouts/**/*.{js,ts,jsx,tsx,vue}",
  ],
  darkMode: "class",
  theme: {
    extend: {},
  },
  plugins: [],
  safelist: [
    "bg-blue-500",
    "bg-violet-500",
    "bg-green-500",
    "bg-red-500",
    "bg-orange-500",
  ],
} satisfies Config;
