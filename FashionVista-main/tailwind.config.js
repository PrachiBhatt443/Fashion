module.exports = {
  content: [
    "./src/**/*.{html,js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        cream: '#f5f5f1',
        amber: '#FFB84D',
      },
      boxShadow: {
        'light': '0 4px 6px rgba(0, 0, 0, 0.1), 0 1px 3px rgba(0, 0, 0, 0.08)',
        '2xl': '0 20px 40px rgba(0, 0, 0, 0.2)',
      },
      textShadow: {
        'lg': '2px 2px 4px rgba(0, 0, 0, 0.3)',
        'md': '1px 1px 2px rgba(0, 0, 0, 0.25)',
      },
    },
  },
  plugins: [],
}
