/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,jsx,ts,tsx}'],
  darkMode: 'class',
  theme: {
    extend: {
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        display: ['"Space Grotesk"', 'Inter', 'sans-serif'],
        mono: ['"JetBrains Mono"', 'monospace'],
      },
      colors: {
        // Antigravity palette
        ag: {
          50:  '#f0f4ff',
          100: '#e0eaff',
          200: '#c0d5ff',
          300: '#93b7ff',
          400: '#608eff',
          500: '#3b6aff',
          600: '#1a45f5',
          700: '#1433e0',
          800: '#172bb5',
          900: '#192a8e',
          950: '#0f1a5e',
        },
        // Neon accents
        neon: {
          blue:   '#3b82f6',
          indigo: '#6366f1',
          violet: '#8b5cf6',
          purple: '#a855f7',
          cyan:   '#06b6d4',
          teal:   '#14b8a6',
          green:  '#22c55e',
          amber:  '#f59e0b',
          red:    '#ef4444',
        },
      },
      backgroundImage: {
        'ag-gradient': 'linear-gradient(135deg, #3b82f6 0%, #8b5cf6 50%, #6366f1 100%)',
        'ag-gradient-subtle': 'linear-gradient(135deg, rgba(59,130,246,0.15) 0%, rgba(139,92,246,0.1) 100%)',
        'space': 'radial-gradient(ellipse at top, #0f172a 0%, #020617 100%)',
        'card-glow': 'linear-gradient(145deg, rgba(59,130,246,0.08) 0%, rgba(139,92,246,0.05) 100%)',
      },
      boxShadow: {
        'ag-sm':  '0 0 15px rgba(59,130,246,0.15)',
        'ag-md':  '0 0 30px rgba(59,130,246,0.2), 0 8px 32px rgba(0,0,0,0.4)',
        'ag-lg':  '0 0 60px rgba(59,130,246,0.15), 0 20px 60px rgba(0,0,0,0.5)',
        'ag-xl':  '0 0 100px rgba(59,130,246,0.12), 0 32px 80px rgba(0,0,0,0.6)',
        'neon':   '0 0 20px rgba(59,130,246,0.5), 0 0 40px rgba(139,92,246,0.25)',
        'card':   '0 8px 32px rgba(0,0,0,0.5), 0 1px 0 rgba(255,255,255,0.06) inset',
        'input':  '0 0 0 3px rgba(59,130,246,0.15)',
        'float':  '0 20px 60px rgba(0,0,0,0.4), 0 0 40px rgba(59,130,246,0.08)',
        'levitate': '0 30px 80px rgba(0,0,0,0.5), 0 0 60px rgba(59,130,246,0.12)',
      },
      backdropBlur: {
        xs: '2px',
        '2xl': '32px',
        '3xl': '48px',
      },
      animation: {
        'pulse-slow': 'pulse 3s ease-in-out infinite',
        'drift-1': 'drift1 22s ease-in-out infinite',
        'drift-2': 'drift2 28s ease-in-out infinite',
        'drift-3': 'drift3 19s ease-in-out infinite',
        'drift-4': 'drift4 33s ease-in-out infinite',
        'shimmer': 'shimmer 2.5s linear infinite',
        'spin-slow': 'spin 3s linear infinite',
        'bounce-subtle': 'bounceSubtle 2s ease-in-out infinite',
        'glow': 'glow 2s ease-in-out infinite alternate',
        'float': 'float 6s ease-in-out infinite',
      },
      keyframes: {
        drift1: {
          '0%, 100%': { transform: 'translate(0,0) scale(1)' },
          '33%':       { transform: 'translate(40px,-50px) scale(1.08)' },
          '66%':       { transform: 'translate(-25px,35px) scale(0.95)' },
        },
        drift2: {
          '0%, 100%': { transform: 'translate(0,0) scale(1)' },
          '40%':       { transform: 'translate(-50px,30px) scale(1.06)' },
          '70%':       { transform: 'translate(30px,-40px) scale(0.97)' },
        },
        drift3: {
          '0%, 100%': { transform: 'translate(0,0) scale(1)' },
          '50%':       { transform: 'translate(20px,50px) scale(1.04)' },
        },
        drift4: {
          '0%, 100%': { transform: 'translate(0,0) scale(1)' },
          '30%':       { transform: 'translate(-30px,-20px) scale(1.05)' },
          '65%':       { transform: 'translate(40px,30px) scale(0.96)' },
        },
        shimmer: {
          '0%':   { backgroundPosition: '-1000px 0' },
          '100%': { backgroundPosition: '1000px 0' },
        },
        bounceSubtle: {
          '0%, 100%': { transform: 'translateY(0)' },
          '50%':       { transform: 'translateY(-6px)' },
        },
        glow: {
          '0%':   { boxShadow: '0 0 20px rgba(59,130,246,0.3)' },
          '100%': { boxShadow: '0 0 40px rgba(139,92,246,0.5), 0 0 80px rgba(59,130,246,0.2)' },
        },
        float: {
          '0%, 100%': { transform: 'translateY(0px)' },
          '50%':       { transform: 'translateY(-12px)' },
        },
      },
    },
  },
  plugins: [],
};
