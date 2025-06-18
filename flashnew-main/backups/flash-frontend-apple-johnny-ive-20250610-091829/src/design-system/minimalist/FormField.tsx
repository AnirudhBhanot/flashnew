import React, { useRef, useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import styles from './FormField.module.scss';

interface FormFieldProps {
  question: string;
  helper?: string;
  children: React.ReactNode;
  isActive?: boolean;
  error?: string;
  onActivate?: () => void;
}

export const FormField: React.FC<FormFieldProps> = ({
  question,
  helper,
  children,
  isActive = false,
  error,
  onActivate
}) => {
  const [showHelper, setShowHelper] = useState(false);
  const fieldRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (isActive && fieldRef.current) {
      fieldRef.current.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
  }, [isActive]);

  return (
    <motion.div
      ref={fieldRef}
      className={styles.field}
      initial={{ opacity: 0 }}
      animate={{ 
        opacity: isActive ? 1 : 0.3,
        scale: isActive ? 1 : 0.98
      }}
      transition={{ duration: 0.6, ease: [0.25, 0, 0, 1] }}
      onClick={onActivate}
      onHoverStart={() => setShowHelper(true)}
      onHoverEnd={() => setShowHelper(false)}
    >
      <motion.h2 
        className={styles.question}
        animate={{ opacity: isActive ? 1 : 0.5 }}
      >
        {question}
      </motion.h2>
      
      <AnimatePresence>
        {helper && showHelper && !error && (
          <motion.p
            className={styles.helper}
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -10 }}
            transition={{ duration: 0.3 }}
          >
            {helper}
          </motion.p>
        )}
      </AnimatePresence>

      <motion.div 
        className={styles.input}
        animate={{ opacity: isActive ? 1 : 0.4 }}
      >
        {children}
      </motion.div>

      <AnimatePresence>
        {error && (
          <motion.p
            className={styles.error}
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -10 }}
            transition={{ duration: 0.3 }}
          >
            {error}
          </motion.p>
        )}
      </AnimatePresence>
    </motion.div>
  );
};