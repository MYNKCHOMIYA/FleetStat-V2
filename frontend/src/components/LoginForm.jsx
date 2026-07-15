import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { Mail, Lock, Eye, EyeOff, Zap, ArrowRight } from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { useNavigate } from 'react-router-dom';
import { loginSchema } from '../lib/schemas';
import { FormField, Input, SubmitButton, AlertBanner } from './ui';

/* ── card animation ── */
const cardVariants = {
  hidden:  { opacity: 0, y: 32, scale: 0.96 },
  visible: {
    opacity: 1, y: 0, scale: 1,
    transition: { duration: 0.55, ease: [0.22, 1, 0.36, 1] },
  },
};

/* ── input row stagger ── */
const fieldVariants = {
  hidden:  { opacity: 0, y: 16 },
  visible: (i) => ({
    opacity: 1, y: 0,
    transition: { delay: 0.12 + i * 0.08, duration: 0.38, ease: [0.22, 1, 0.36, 1] },
  }),
};

export default function LoginForm({ onSwitchToRegister }) {
  const [showPw, setShowPw] = useState(false);
  const [apiError, setApiError] = useState('');
  const { login } = useAuth();
  const navigate  = useNavigate();

  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm({ resolver: zodResolver(loginSchema) });

  const onSubmit = async (data) => {
    setApiError('');
    try {
      await login(data.email, data.password);
      navigate('/dashboard');
    } catch (err) {
      const msg = err?.response?.data?.detail;
      setApiError(
        typeof msg === 'string' ? msg.trim() : 'Invalid email or password. Please try again.'
      );
    }
  };

  return (
    <motion.div
      className="w-full max-w-md mx-auto"
      variants={cardVariants}
      initial="hidden"
      animate="visible"
    >
      {/* Ambient glow behind card */}
      <div
        className="absolute inset-0 -z-10 opacity-30 blur-3xl rounded-3xl"
        style={{ background: 'radial-gradient(ellipse, rgba(59,130,246,0.5) 0%, transparent 70%)' }}
      />

      {/* Glass card */}
      <motion.div
        className="glass-card rounded-3xl p-8 sm:p-10 shadow-card"
        whileHover={{ y: -4, transition: { duration: 0.4 } }}
      >
        {/* Header */}
        <motion.div
          className="mb-8"
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.05, duration: 0.4 }}
        >
          {/* Brand mark */}
          <div className="flex items-center gap-3 mb-6">
            <div className="relative">
              <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-blue-500 to-violet-600 flex items-center justify-center shadow-ag-md">
                <svg viewBox="0 0 24 24" className="w-5 h-5 fill-white">
                  <path d="M20 8h-3V4H3c-1.1 0-2 .9-2 2v11h2c0 1.66 1.34 3 3 3s3-1.34 3-3h6c0 1.66 1.34 3 3 3s3-1.34 3-3h2v-5l-3-4zm-1.5 1.5 1.96 2.5H17V9.5h1.5zM6 18c-.55 0-1-.45-1-1s.45-1 1-1 1 .45 1 1-.45 1-1 1zm11 0c-.55 0-1-.45-1-1s.45-1 1-1 1 .45 1 1-.45 1-1 1z"/>
                </svg>
              </div>
              {/* Pulse ring */}
              <motion.div
                className="absolute inset-0 rounded-xl border border-blue-500/50"
                animate={{ scale: [1, 1.5], opacity: [0.5, 0] }}
                transition={{ duration: 2, repeat: Infinity, ease: 'easeOut' }}
              />
            </div>
            <div>
              <p className="font-display font-bold text-lg gradient-text tracking-tight">FleetStat</p>
              <p className="text-[10px] tracking-[0.18em] uppercase text-slate-500 font-medium">Management Platform</p>
            </div>
          </div>

          <h1 className="font-display text-3xl font-bold tracking-tight text-slate-50 mb-2">
            Welcome back
          </h1>
          <p className="text-slate-400 text-sm">
            Sign in to your account to continue
          </p>
        </motion.div>

        {/* Error banner */}
        <AlertBanner message={apiError} type="error" />

        {/* Form */}
        <form onSubmit={handleSubmit(onSubmit)} className="space-y-5" noValidate>

          <motion.div custom={0} variants={fieldVariants} initial="hidden" animate="visible">
            <FormField label="Email address" icon={Mail} error={errors.email?.message}>
              <Input
                type="email"
                placeholder="you@example.com"
                autoComplete="email"
                {...register('email')}
              />
            </FormField>
          </motion.div>

          <motion.div custom={1} variants={fieldVariants} initial="hidden" animate="visible">
            <FormField label="Password" icon={Lock} error={errors.password?.message}>
              <div className="relative">
                <Input
                  type={showPw ? 'text' : 'password'}
                  placeholder="••••••••"
                  autoComplete="current-password"
                  className="pr-11"
                  {...register('password')}
                />
                <motion.button
                  type="button"
                  className="absolute right-3 top-1/2 -translate-y-1/2 text-slate-500 hover:text-slate-300 transition-colors p-0.5"
                  onClick={() => setShowPw(v => !v)}
                  whileHover={{ scale: 1.1 }}
                  whileTap={{ scale: 0.9 }}
                >
                  <AnimatePresence mode="wait">
                    {showPw
                      ? <motion.div key="off" initial={{ opacity: 0, rotate: -15 }} animate={{ opacity: 1, rotate: 0 }} exit={{ opacity: 0 }}><EyeOff size={16} /></motion.div>
                      : <motion.div key="on"  initial={{ opacity: 0, rotate:  15 }} animate={{ opacity: 1, rotate: 0 }} exit={{ opacity: 0 }}><Eye     size={16} /></motion.div>
                    }
                  </AnimatePresence>
                </motion.button>
              </div>
            </FormField>
          </motion.div>

          <motion.div
            custom={2}
            variants={fieldVariants}
            initial="hidden"
            animate="visible"
          >
            <SubmitButton loading={isSubmitting}>
              Sign In
              <ArrowRight size={16} />
            </SubmitButton>
          </motion.div>
        </form>

        {/* Divider */}
        <div className="flex items-center gap-3 my-6">
          <div className="flex-1 h-px bg-slate-800" />
          <span className="text-xs text-slate-600 font-medium tracking-wide">OR</span>
          <div className="flex-1 h-px bg-slate-800" />
        </div>

        {/* Switch to Register */}
        <p className="text-center text-sm text-slate-500">
          Don't have an account?{' '}
          <button
            onClick={onSwitchToRegister}
            className="text-blue-400 hover:text-blue-300 font-semibold transition-colors hover:underline underline-offset-2"
          >
            Create one free
          </button>
        </p>
      </motion.div>
    </motion.div>
  );
}
