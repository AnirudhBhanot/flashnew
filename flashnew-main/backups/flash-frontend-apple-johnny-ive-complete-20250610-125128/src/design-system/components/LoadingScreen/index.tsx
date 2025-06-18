import React from 'react';
import { motion } from 'framer-motion';
import styles from './LoadingScreen.module.scss';

export const LoadingScreen: React.FC = () => {
  return (
    <div className={styles.container}>
      <motion.div
        className={styles.spinner}
        animate={{ rotate: 360 }}
        transition={{
          duration: 1,
          repeat: Infinity,
          ease: "linear"
        }}
      />
    </div>
  );
};