/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      blur: {
        xs: '1px', // This creates a "blur-xs" class with a 1px blur
      },
    },
  },
  plugins: [
    require('@tailwindcss/typography')
  ],
};
