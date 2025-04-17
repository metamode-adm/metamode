/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './src/frontend/templates/**/*.html',
    './src/frontend/static/js/**/*.js',
  ],
  safelist: [
    'bg-red-600', 'hover:bg-red-700', 'bg-gray-200', 'hover:bg-gray-300',
    'text-white', 'text-gray-800', 'px-4', 'py-2', 'rounded', 'font-medium', 'font-semibold',
  ],
  theme: {
    extend: {
      keyframes: {
        flame: {
          '0%, 100%': { filter: 'brightness(1) saturate(1)' },
          '50%': { filter: 'brightness(1.4) saturate(1.5)' },
        },
      },
      animation: {
        flame: 'flame 1.8s ease-in-out infinite',
      },
    },
  },
  plugins: [],
}
;