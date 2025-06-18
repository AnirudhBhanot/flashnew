import React from 'react';
import { motion } from 'framer-motion';
import styles from './MinimalScale.module.scss';

interface MinimalScaleProps {
  value: number;
  onChange: (value: number) => void;
  min: number;
  max: number;
  labels?: { [key: number]: string };
}

export const MinimalScale: React.FC<MinimalScaleProps> = ({
  value,
  onChange,
  min,
  max,
  labels = {}
}) => {
  const steps = max - min + 1;
  const stepArray = Array.from({ length: steps }, (_, i) => min + i);

  return (
    <div className={styles.container}>
      <div className={styles.scale}>
        {stepArray.map((step) => (
          <button
            key={step}
            className={`${styles.step} ${value === step ? styles.active : ''}`}
            onClick={() => onChange(step)}
            type="button"
          >
            <motion.div
              className={styles.dot}
              animate={{ 
                scale: value === step ? 1.2 : 1,
                backgroundColor: value === step ? '#000' : '#d2d2d7'
              }}
              transition={{ duration: 0.3, ease: [0.25, 0, 0, 1] }}
            />
            {labels[step] && (
              <motion.span
                className={styles.label}
                animate={{ 
                  opacity: value === step ? 1 : 0.5,
                  fontWeight: value === step ? 500 : 400
                }}
              >
                {labels[step]}
              </motion.span>
            )}
          </button>
        ))}
      </div>
    </div>
  );
};