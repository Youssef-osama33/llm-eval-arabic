import type { Config } from "tailwindcss";

const config: Config = {
  content: ["./src/**/*.{js,ts,jsx,tsx,mdx}"],
  theme: {
    extend: {
      fontFamily: {
        mono:   ["Courier Prime", "monospace"],
        arabic: ["Scheherazade New", "serif"],
        display:["Cinzel", "serif"],
      },
      colors: {
        gold:   "#d4a843",
        crimson:"#8b1a1a",
      },
      animation: {
        "fadeUp":  "fadeUp 0.4s ease both",
        "slideIn": "slideIn 0.3s ease both",
      },
      keyframes: {
        fadeUp:  { from: { opacity: "0", transform: "translateY(20px)" }, to: { opacity: "1", transform: "translateY(0)" } },
        slideIn: { from: { opacity: "0", transform: "translateX(-10px)" }, to: { opacity: "1", transform: "translateX(0)" } },
      },
    },
  },
  plugins: [],
};

export default config;
