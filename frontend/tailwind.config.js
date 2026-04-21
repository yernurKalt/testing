/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        brand: {
          50: "#f5f7ff",
          100: "#e9edff",
          200: "#c9d1ff",
          300: "#a3afff",
          400: "#7a86f7",
          500: "#5865f2",
          600: "#4752c4",
          700: "#3843a0",
          800: "#2c3581",
          900: "#1f2560",
        },
      },
      boxShadow: {
        soft: "0 8px 24px -12px rgba(15, 23, 42, 0.18)",
      },
    },
  },
  plugins: [],
};
