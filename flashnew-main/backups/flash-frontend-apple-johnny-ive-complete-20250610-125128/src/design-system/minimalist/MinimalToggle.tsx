import React from 'react';
import { motion } from 'framer-motion';
import styles from './MinimalToggle.module.scss';

interface MinimalToggleProps {
  value: boolean;
  onChange: (value: boolean) => void;
  label: string;
}

export const MinimalToggle: React.FC<MinimalToggleProps> = ({
  value,
  onChange,
  label
}) => {
  return (
    <button
      className={styles.container}
      onClick={() => onChange(!value)}
      type="button"
    >
      <span className={styles.label}>{label}</span>
      <motion.div
        className={styles.toggle}
        animate={{ backgroundColor: value ? '#34c759' : '#e5e5e7' }}
        transition={{ duration: 0.3 }}
      >
        <motion.div
          className={styles.thumb}
          animate={{ x: value ? 28 : 0 }}
          transition={{ type: 'spring', stiffness: 500, damping: 30 }}
        />
      </motion.div>
    </button>
  );
};