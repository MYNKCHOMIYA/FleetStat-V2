import { motion } from 'framer-motion';
import { Sun, Moon } from 'lucide-react';
import { useTheme } from '../context/ThemeContext';
import styles from './ThemeToggle.module.css';

export default function ThemeToggle() {
  const { theme, toggle } = useTheme();
  const dark = theme === 'dark';

  return (
    <motion.button
      className={styles.toggle}
      onClick={toggle}
      whileHover={{ scale: 1.08 }}
      whileTap={{ scale: 0.93 }}
      aria-label={`Switch to ${dark ? 'light' : 'dark'} mode`}
      title={`Switch to ${dark ? 'light' : 'dark'} mode`}
    >
      <motion.div
        className={styles.track}
        animate={{ backgroundColor: dark ? '#1e2235' : '#dbeafe' }}
        transition={{ duration: 0.35 }}
      >
        <motion.div
          className={styles.thumb}
          animate={{ x: dark ? 2 : 26, backgroundColor: dark ? '#3b82f6' : '#f59e0b' }}
          transition={{ type: 'spring', stiffness: 400, damping: 28 }}
        >
          <motion.div
            animate={{ rotate: dark ? 0 : 180, opacity: 1 }}
            transition={{ duration: 0.3 }}
          >
            {dark ? (
              <Moon size={11} color="#fff" />
            ) : (
              <Sun size={11} color="#fff" />
            )}
          </motion.div>
        </motion.div>
      </motion.div>
    </motion.button>
  );
}
