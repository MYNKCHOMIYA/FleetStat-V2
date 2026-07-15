import { Navigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { motion } from 'framer-motion';

export default function ProtectedRoute({ children }) {
  const { user, loading } = useAuth();

  if (loading) {
    return (
      <div style={{
        minHeight: '100vh',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        background: 'var(--bg-base)',
      }}>
        <motion.div
          style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 20 }}
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
        >
          {/* Animated fleet icon spinner */}
          <motion.div
            style={{
              width: 56, height: 56,
              background: 'linear-gradient(135deg, var(--accent), var(--accent-2))',
              borderRadius: 14,
              display: 'flex', alignItems: 'center', justifyContent: 'center',
              boxShadow: '0 0 30px var(--accent-glow)',
            }}
            animate={{ rotate: [0, 0, 180, 180, 360], scale: [1, 1.1, 1.1, 1, 1] }}
            transition={{ duration: 1.6, repeat: Infinity, ease: 'easeInOut' }}
          >
            <svg width="30" height="30" viewBox="0 0 24 24" fill="white">
              <path d="M20 8h-3V4H3c-1.1 0-2 .9-2 2v11h2c0 1.66 1.34 3 3 3s3-1.34 3-3h6c0 1.66 1.34 3 3 3s3-1.34 3-3h2v-5l-3-4zm-1.5 1.5 1.96 2.5H17V9.5h1.5zM6 18c-.55 0-1-.45-1-1s.45-1 1-1 1 .45 1 1-.45 1-1 1zm11 0c-.55 0-1-.45-1-1s.45-1 1-1 1 .45 1 1-.45 1-1 1z"/>
            </svg>
          </motion.div>

          <div style={{ display: 'flex', gap: 6 }}>
            {[0, 1, 2].map(i => (
              <motion.div
                key={i}
                style={{ width: 8, height: 8, background: 'var(--accent)', borderRadius: '50%' }}
                animate={{ y: [0, -10, 0] }}
                transition={{ duration: 0.8, delay: i * 0.15, repeat: Infinity, ease: 'easeInOut' }}
              />
            ))}
          </div>

          <motion.p
            style={{ color: 'var(--text-muted)', fontSize: 14 }}
            animate={{ opacity: [0.5, 1, 0.5] }}
            transition={{ duration: 2, repeat: Infinity }}
          >
            Loading FleetStat…
          </motion.p>
        </motion.div>
      </div>
    );
  }

  return user ? children : <Navigate to="/" replace />;
}
