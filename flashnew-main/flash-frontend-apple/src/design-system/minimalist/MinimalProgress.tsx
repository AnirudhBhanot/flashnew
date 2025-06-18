import React from 'react';
import { motion } from 'framer-motion';
import styles from './MinimalProgress.module.scss';

interface MinimalProgressProps {
  current: number;
  total: number;
  showSteps?: boolean;
}

export const MinimalProgress: React.FC<MinimalProgressProps> = ({
  current,
  total,
  showSteps = false
}) => {
  const progress = (current / total) * 100;

  return (
    <div className={styles.container}>
      <div className={styles.track}>
        <motion.div
          className={styles.fill}
          initial={{ width: 0 }}
          animate={{ width: `${progress}%` }}
          transition={{ duration: 0.8, ease: [0.25, 0, 0, 1] }}
        />
      </div>
      {showSteps && (
        <div className={styles.steps}>
          <span className={styles.current}>{current}</span>
          <span className={styles.separator}>/</span>
          <span className={styles.total}>{total}</span>
        </div>
      )}
    </div>
  );
};