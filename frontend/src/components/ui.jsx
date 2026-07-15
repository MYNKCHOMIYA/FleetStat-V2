import { forwardRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { AlertCircle, CheckCircle2 } from 'lucide-react';

/* ── Animated Field wrapper (floating label + glow) ── */
export const FormField = forwardRef(function FormField(
  { label, icon: Icon, error, success, children, className = '' },
  _ref
) {
  return (
    <div className={`space-y-1.5 ${className}`}>
      {label && (
        <label className="flex items-center gap-1.5 text-xs font-semibold tracking-wider uppercase text-slate-400">
          {Icon && <Icon size={11} />}
          {label}
        </label>
      )}

      {/* Neon border wrapper */}
      <div className="relative group">
        {/* Gradient border glow on focus */}
        <div
          className="absolute -inset-[1px] rounded-xl opacity-0 group-focus-within:opacity-100 transition-opacity duration-300"
          style={{ background: 'linear-gradient(135deg, #3b82f6, #8b5cf6, #6366f1)', zIndex: 0 }}
        />

        {/* Inner wrapper */}
        <div className="relative z-10 rounded-xl overflow-hidden">
          {children}
        </div>
      </div>

      {/* Error / success feedback */}
      <AnimatePresence mode="wait">
        {error && (
          <motion.p
            key="error"
            initial={{ opacity: 0, y: -6, height: 0 }}
            animate={{ opacity: 1, y: 0, height: 'auto' }}
            exit={{    opacity: 0, y: -4, height: 0 }}
            transition={{ duration: 0.2 }}
            className="flex items-center gap-1.5 text-xs text-red-400 font-medium"
          >
            <AlertCircle size={12} className="flex-shrink-0" />
            {error}
          </motion.p>
        )}
        {!error && success && (
          <motion.p
            key="success"
            initial={{ opacity: 0, y: -6 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{    opacity: 0 }}
            className="flex items-center gap-1.5 text-xs text-emerald-400 font-medium"
          >
            <CheckCircle2 size={12} className="flex-shrink-0" />
            {success}
          </motion.p>
        )}
      </AnimatePresence>
    </div>
  );
});

/* ── Styled Input ── */
export const Input = forwardRef(function Input({ className = '', ...props }, ref) {
  return (
    <input
      ref={ref}
      className={`
        ag-input
        ${className}
      `}
      {...props}
    />
  );
});

/* ── Primary Submit Button ── */
export function SubmitButton({ loading, children, className = '', ...props }) {
  return (
    <motion.button
      type="submit"
      className={`
        ag-btn-primary w-full py-3.5 px-6 text-sm flex items-center justify-center gap-2.5
        ${className}
      `}
      whileHover={!loading ? { scale: 1.015, y: -1 } : {}}
      whileTap={!loading   ? { scale: 0.98  } : {}}
      transition={{ type: 'spring', stiffness: 400, damping: 20 }}
      disabled={loading}
      {...props}
    >
      <AnimatePresence mode="wait">
        {loading ? (
          <motion.span
            key="loader"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{    opacity: 0 }}
            className="flex items-center gap-2.5"
          >
            <Spinner />
            <span>Processing…</span>
          </motion.span>
        ) : (
          <motion.span
            key="label"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{    opacity: 0 }}
            className="flex items-center gap-2"
          >
            {children}
          </motion.span>
        )}
      </AnimatePresence>
    </motion.button>
  );
}

/* ── Inline spinner ── */
export function Spinner({ size = 16, className = '' }) {
  return (
    <motion.div
      className={`rounded-full border-2 border-white/20 border-t-white ${className}`}
      style={{ width: size, height: size, flexShrink: 0 }}
      animate={{ rotate: 360 }}
      transition={{ duration: 0.7, repeat: Infinity, ease: 'linear' }}
    />
  );
}

/* ── Alert toast / banner ── */
export function AlertBanner({ message, type = 'error', className = '' }) {
  const cfg = {
    error:   { bg: 'bg-red-500/10',     border: 'border-red-500/25',   text: 'text-red-400',    icon: AlertCircle   },
    success: { bg: 'bg-emerald-500/10', border: 'border-emerald-500/25', text: 'text-emerald-400', icon: CheckCircle2 },
    info:    { bg: 'bg-blue-500/10',    border: 'border-blue-500/25',   text: 'text-blue-400',   icon: AlertCircle   },
  }[type] || {};

  return (
    <AnimatePresence>
      {message && (
        <motion.div
          initial={{ opacity: 0, y: -10, height: 0, marginBottom: 0 }}
          animate={{ opacity: 1, y: 0, height: 'auto', marginBottom: 16 }}
          exit={{    opacity: 0, y: -6, height: 0, marginBottom: 0 }}
          transition={{ duration: 0.28 }}
          className={`
            flex items-start gap-2.5 px-4 py-3 rounded-xl
            border text-sm font-medium
            ${cfg.bg} ${cfg.border} ${cfg.text} ${className}
          `}
        >
          {cfg.icon && <cfg.icon size={15} className="flex-shrink-0 mt-0.5" />}
          <span>{message}</span>
        </motion.div>
      )}
    </AnimatePresence>
  );
}

/* ── Password strength indicator ── */
export function PasswordStrength({ password }) {
  const getStrength = (pw) => {
    let score = 0;
    if (!pw) return { score: 0, label: '', color: '' };
    if (pw.length >= 8) score++;
    if (/[A-Z]/.test(pw)) score++;
    if (/[0-9]/.test(pw)) score++;
    if (/[^A-Za-z0-9]/.test(pw)) score++;
    const map = [
      { label: 'Too short', color: 'bg-red-500'    },
      { label: 'Weak',      color: 'bg-orange-500' },
      { label: 'Fair',      color: 'bg-amber-500'  },
      { label: 'Good',      color: 'bg-blue-500'   },
      { label: 'Strong',    color: 'bg-emerald-500' },
    ];
    return { score, ...map[score] };
  };

  const s = getStrength(password);
  if (!password) return null;

  return (
    <div className="space-y-1.5 mt-1">
      <div className="flex gap-1">
        {[1,2,3,4].map(i => (
          <motion.div
            key={i}
            className={`h-1 flex-1 rounded-full transition-all duration-500 ${i <= s.score ? s.color : 'bg-slate-700'}`}
            initial={{ scaleX: 0 }}
            animate={{ scaleX: 1 }}
            transition={{ delay: i * 0.05 }}
          />
        ))}
      </div>
      <p className={`text-xs font-medium ${
        s.score <= 1 ? 'text-red-400' :
        s.score === 2 ? 'text-amber-400' :
        s.score === 3 ? 'text-blue-400' : 'text-emerald-400'
      }`}>{s.label}</p>
    </div>
  );
}
