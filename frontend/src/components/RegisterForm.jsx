import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { User, Mail, Lock, Eye, EyeOff, Sparkles, CheckCircle2, ArrowRight } from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { registerSchema } from '../lib/schemas';
import { FormField, Input, SubmitButton, AlertBanner, PasswordStrength } from './ui';

const cardVariants = {
  hidden:  { opacity: 0, y: 32, scale: 0.96 },
  visible: {
    opacity: 1, y: 0, scale: 1,
    transition: { duration: 0.55, ease: [0.22, 1, 0.36, 1] },
  },
};

const fieldVariants = {
  hidden:  { opacity: 0, y: 16 },
  visible: (i) => ({
    opacity: 1, y: 0,
    transition: { delay: 0.10 + i * 0.07, duration: 0.36, ease: [0.22, 1, 0.36, 1] },
  }),
};

/* ── Success overlay ── */
function SuccessOverlay({ onDone }) {
  return (
    <motion.div
      className="absolute inset-0 z-20 flex flex-col items-center justify-center rounded-3xl bg-slate-900/95 backdrop-blur-xl"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.4 }}
    >
      <motion.div
        initial={{ scale: 0, rotate: -20 }}
        animate={{ scale: 1, rotate: 0 }}
        transition={{ delay: 0.1, type: 'spring', stiffness: 280, damping: 18 }}
        className="w-20 h-20 rounded-full bg-emerald-500/15 border border-emerald-500/30 flex items-center justify-center mb-5"
        style={{ boxShadow: '0 0 40px rgba(34,197,94,0.3)' }}
      >
        <CheckCircle2 size={36} className="text-emerald-400" />
      </motion.div>

      <motion.h3
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.25 }}
        className="font-display text-2xl font-bold text-slate-50 mb-2"
      >
        Account created!
      </motion.h3>

      <motion.p
        initial={{ opacity: 0, y: 8 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.33 }}
        className="text-slate-400 text-sm mb-8 text-center max-w-xs"
      >
        Your FleetStat account is ready. Sign in to get started.
      </motion.p>

      <motion.button
        initial={{ opacity: 0, y: 8 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.42 }}
        onClick={onDone}
        className="ag-btn-primary px-8 py-3 text-sm flex items-center gap-2"
        whileHover={{ scale: 1.03 }}
        whileTap={{ scale: 0.97 }}
      >
        Sign In Now <ArrowRight size={15} />
      </motion.button>
    </motion.div>
  );
}

export default function RegisterForm({ onSwitchToLogin }) {
  const [showPw, setShowPw]   = useState(false);
  const [apiError, setApiError] = useState('');
  const [success, setSuccess]   = useState(false);
  const [pwValue, setPwValue]   = useState('');
  const { register: registerUser } = useAuth();

  const {
    register,
    handleSubmit,
    watch,
    formState: { errors, isSubmitting },
  } = useForm({ resolver: zodResolver(registerSchema) });

  // Watch password for strength indicator
  const password = watch('password', '');

  const onSubmit = async (data) => {
    setApiError('');
    try {
      await registerUser(data.username, data.email, data.password);
      setSuccess(true);
    } catch (err) {
      const msg = err?.response?.data?.detail;
      setApiError(
        typeof msg === 'string' ? msg.trim() : 'Registration failed. This email may already be in use.'
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
      {/* Ambient glow */}
      <div
        className="absolute inset-0 -z-10 opacity-30 blur-3xl rounded-3xl"
        style={{ background: 'radial-gradient(ellipse, rgba(139,92,246,0.5) 0%, transparent 70%)' }}
      />

      <motion.div
        className="glass-card rounded-3xl p-8 sm:p-10 shadow-card relative overflow-hidden"
        whileHover={{ y: -4, transition: { duration: 0.4 } }}
      >
        {/* Success overlay */}
        <AnimatePresence>
          {success && <SuccessOverlay onDone={onSwitchToLogin} />}
        </AnimatePresence>

        {/* Header */}
        <motion.div
          className="mb-7"
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.05, duration: 0.4 }}
        >
          <div className="flex items-center gap-3 mb-6">
            <div className="relative">
              <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-violet-500 to-purple-600 flex items-center justify-center shadow-ag-md">
                <Sparkles size={18} className="text-white" />
              </div>
              <motion.div
                className="absolute inset-0 rounded-xl border border-violet-500/50"
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
            Create account
          </h1>
          <p className="text-slate-400 text-sm">
            Join FleetStat — it only takes a minute
          </p>
        </motion.div>

        {/* Error banner */}
        <AlertBanner message={apiError} type="error" />

        {/* Form */}
        <form onSubmit={handleSubmit(onSubmit)} className="space-y-4" noValidate>

          <motion.div custom={0} variants={fieldVariants} initial="hidden" animate="visible">
            <FormField label="Username" icon={User} error={errors.username?.message}>
              <Input
                type="text"
                placeholder="johndoe"
                autoComplete="username"
                {...register('username')}
              />
            </FormField>
          </motion.div>

          <motion.div custom={1} variants={fieldVariants} initial="hidden" animate="visible">
            <FormField label="Email address" icon={Mail} error={errors.email?.message}>
              <Input
                type="email"
                placeholder="you@example.com"
                autoComplete="email"
                {...register('email')}
              />
            </FormField>
          </motion.div>

          <motion.div custom={2} variants={fieldVariants} initial="hidden" animate="visible">
            <FormField label="Password" icon={Lock} error={errors.password?.message}>
              <div className="relative">
                <Input
                  type={showPw ? 'text' : 'password'}
                  placeholder="Min. 8 chars with uppercase & number"
                  autoComplete="new-password"
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
                      ? <motion.div key="off" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}><EyeOff size={16} /></motion.div>
                      : <motion.div key="on"  initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}><Eye     size={16} /></motion.div>
                    }
                  </AnimatePresence>
                </motion.button>
              </div>
              {/* Password strength */}
              <PasswordStrength password={password} />
            </FormField>
          </motion.div>

          <motion.div custom={3} variants={fieldVariants} initial="hidden" animate="visible" className="pt-1">
            <SubmitButton loading={isSubmitting}>
              Create Account
              <Sparkles size={15} />
            </SubmitButton>
          </motion.div>
        </form>

        {/* Divider */}
        <div className="flex items-center gap-3 my-6">
          <div className="flex-1 h-px bg-slate-800" />
          <span className="text-xs text-slate-600 font-medium tracking-wide">OR</span>
          <div className="flex-1 h-px bg-slate-800" />
        </div>

        <p className="text-center text-sm text-slate-500">
          Already have an account?{' '}
          <button
            onClick={onSwitchToLogin}
            className="text-blue-400 hover:text-blue-300 font-semibold transition-colors hover:underline underline-offset-2"
          >
            Sign in
          </button>
        </p>
      </motion.div>
    </motion.div>
  );
}
