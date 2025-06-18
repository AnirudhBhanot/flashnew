import React, { useState, useRef, useEffect } from 'react';
import { motion } from 'framer-motion';
import { AnimatePresence } from '../components/AnimatePresenceWrapper';
import styles from './MinimalSelect.module.scss';

interface Option {
  value: string;
  label: string;
  description?: string;
}

interface MinimalSelectProps {
  value: string;
  onChange: (value: string) => void;
  options: Option[];
  placeholder?: string;
}

export const MinimalSelect: React.FC<MinimalSelectProps> = ({
  value,
  onChange,
  options,
  placeholder = 'Select an option'
}) => {
  const [isOpen, setIsOpen] = useState(false);
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (containerRef.current && !containerRef.current.contains(event.target as Node)) {
        setIsOpen(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const selectedOption = options.find(opt => opt.value === value);

  return (
    <div ref={containerRef} className={styles.container}>
      <motion.button
        className={styles.trigger}
        onClick={() => setIsOpen(!isOpen)}
        whileTap={{ scale: 0.98 }}
      >
        <span className={value ? styles.value : styles.placeholder}>
          {selectedOption?.label || placeholder}
        </span>
        <motion.svg
          width="24"
          height="24"
          viewBox="0 0 24 24"
          fill="none"
          animate={{ rotate: isOpen ? 180 : 0 }}
          transition={{ duration: 0.3 }}
        >
          <path
            d="M6 9L12 15L18 9"
            stroke="currentColor"
            strokeWidth="1.5"
            strokeLinecap="round"
            strokeLinejoin="round"
          />
        </motion.svg>
      </motion.button>

      <AnimatePresence>
        {isOpen && (
          <motion.div
            className={styles.dropdown}
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            transition={{ duration: 0.3, ease: [0.25, 0, 0, 1] }}
          >
            {options.map((option) => (
              <motion.button
                key={option.value}
                className={`${styles.option} ${value === option.value ? styles.selected : ''}`}
                onClick={() => {
                  onChange(option.value);
                  setIsOpen(false);
                }}
                whileHover={{ backgroundColor: '#f5f5f7' }}
                whileTap={{ scale: 0.98 }}
              >
                <span className={styles.optionLabel}>{option.label}</span>
                {option.description && (
                  <span className={styles.optionDescription}>{option.description}</span>
                )}
              </motion.button>
            ))}
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};