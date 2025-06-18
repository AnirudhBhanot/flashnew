import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { AnimatePresence } from '../design-system/components/AnimatePresenceWrapper';
import { Icon } from '../design-system/components';
import styles from './AutoSaveIndicator.module.scss';

interface AutoSaveIndicatorProps {
  saving?: boolean;
  error?: boolean;
  lastSaved?: Date | null;
}

export const AutoSaveIndicator: React.FC<AutoSaveIndicatorProps> = ({
  saving = false,
  error = false,
  lastSaved
}) => {
  const [showSaved, setShowSaved] = useState(false);

  useEffect(() => {
    if (!saving && !error && lastSaved) {
      setShowSaved(true);
      const timer = setTimeout(() => setShowSaved(false), 3000);
      return () => clearTimeout(timer);
    }
  }, [saving, error, lastSaved]);

  const formatLastSaved = (date: Date) => {
    const now = new Date();
    const diff = now.getTime() - date.getTime();
    const seconds = Math.floor(diff / 1000);
    const minutes = Math.floor(seconds / 60);
    const hours = Math.floor(minutes / 60);

    if (seconds < 60) return 'Just now';
    if (minutes < 60) return `${minutes}m ago`;
    if (hours < 24) return `${hours}h ago`;
    return date.toLocaleDateString();
  };

  return (
    <AnimatePresence mode="wait">
      {saving && (
        <motion.div
          key="saving"
          className={styles.container}
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: -10 }}
          transition={{ duration: 0.2 }}
        >
          <div className={styles.spinner} />
          <span className={styles.text}>Saving...</span>
        </motion.div>
      )}

      {error && (
        <motion.div
          key="error"
          className={`${styles.container} ${styles.error}`}
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: -10 }}
          transition={{ duration: 0.2 }}
        >
          <Icon name="exclamationmark.triangle" size={16} />
          <span className={styles.text}>Save failed</span>
        </motion.div>
      )}

      {showSaved && lastSaved && !saving && !error && (
        <motion.div
          key="saved"
          className={`${styles.container} ${styles.success}`}
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: -10 }}
          transition={{ duration: 0.2 }}
        >
          <Icon name="checkmark" size={16} />
          <span className={styles.text}>
            Saved {formatLastSaved(lastSaved)}
          </span>
        </motion.div>
      )}
    </AnimatePresence>
  );
};