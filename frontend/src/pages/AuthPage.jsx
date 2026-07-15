import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import AuthLayout from '../components/AuthLayout';
import LoginForm from '../components/LoginForm';
import RegisterForm from '../components/RegisterForm';

const pageVariants = {
  enter:  (dir) => ({ opacity: 0, x: dir > 0 ?  60 : -60, scale: 0.97 }),
  center: {
    opacity: 1, x: 0, scale: 1,
    transition: { duration: 0.4, ease: [0.22, 1, 0.36, 1] },
  },
  exit:   (dir) => ({
    opacity: 0, x: dir > 0 ? -60 : 60, scale: 0.97,
    transition: { duration: 0.28 },
  }),
};

export default function AuthPage() {
  const [view, setView] = useState('login'); // 'login' | 'register'
  const [dir,  setDir]  = useState(1);

  const go = (next) => {
    if (next === view) return;
    setDir(next === 'register' ? 1 : -1);
    setView(next);
  };

  return (
    <AuthLayout>
      {/* Top bar */}
      <div className="absolute top-0 left-0 right-0 flex items-center justify-between px-6 py-4 z-20">
        {/* Logo wordmark */}
        <div className="flex items-center gap-2">
          <div className="w-7 h-7 rounded-lg bg-gradient-to-br from-blue-500 to-violet-600 flex items-center justify-center">
            <svg viewBox="0 0 24 24" className="w-4 h-4 fill-white">
              <path d="M20 8h-3V4H3c-1.1 0-2 .9-2 2v11h2c0 1.66 1.34 3 3 3s3-1.34 3-3h6c0 1.66 1.34 3 3 3s3-1.34 3-3h2v-5l-3-4zm-1.5 1.5 1.96 2.5H17V9.5h1.5zM6 18c-.55 0-1-.45-1-1s.45-1 1-1 1 .45 1 1-.45 1-1 1zm11 0c-.55 0-1-.45-1-1s.45-1 1-1 1 .45 1 1-.45 1-1 1z"/>
            </svg>
          </div>
          <span className="font-display font-bold text-sm gradient-text">FleetStat V2</span>
        </div>

        {/* Tab switcher pill */}
        <div className="flex items-center gap-1 bg-slate-900/70 border border-slate-700/50 backdrop-blur-xl rounded-xl p-1">
          {['login', 'register'].map(tab => (
            <button
              key={tab}
              onClick={() => go(tab)}
              className={`
                relative px-4 py-1.5 rounded-lg text-xs font-semibold transition-all duration-200
                ${view === tab ? 'text-white' : 'text-slate-500 hover:text-slate-300'}
              `}
            >
              {view === tab && (
                <motion.div
                  layoutId="auth-tab-indicator"
                  className="absolute inset-0 rounded-lg bg-gradient-to-r from-blue-600 to-violet-600"
                  style={{ zIndex: -1 }}
                  transition={{ type: 'spring', stiffness: 400, damping: 30 }}
                />
              )}
              {tab === 'login' ? 'Sign In' : 'Register'}
            </button>
          ))}
        </div>
      </div>

      {/* Main form area */}
      <div className="flex items-center justify-center min-h-screen px-4 sm:px-6 pt-16">
        <div className="w-full max-w-md relative">
          <AnimatePresence mode="wait" custom={dir}>
            <motion.div
              key={view}
              custom={dir}
              variants={pageVariants}
              initial="enter"
              animate="center"
              exit="exit"
            >
              {view === 'login' ? (
                <LoginForm    onSwitchToRegister={() => go('register')} />
              ) : (
                <RegisterForm onSwitchToLogin={() => go('login')} />
              )}
            </motion.div>
          </AnimatePresence>
        </div>
      </div>

      {/* Bottom legal */}
      <div className="absolute bottom-4 left-0 right-0 text-center">
        <p className="text-xs text-slate-700">
          © 2025 FleetStat V2 &middot; Fleet Management Platform
        </p>
      </div>
    </AuthLayout>
  );
}
