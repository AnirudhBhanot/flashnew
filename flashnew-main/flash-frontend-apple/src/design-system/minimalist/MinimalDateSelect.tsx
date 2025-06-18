import React, { useState, useRef, useEffect } from 'react';
import { motion } from 'framer-motion';
import { AnimatePresence } from '../components/AnimatePresenceWrapper';
import styles from './MinimalSelect.module.scss'; // Use the exact same styles as MinimalSelect

interface Option {
  value: string;
  label: string;
  description?: string;
  date: Date;
}

interface MinimalDateSelectProps {
  value: Date | null;
  onChange: (date: Date | null) => void;
  placeholder?: string;
}

export const MinimalDateSelect: React.FC<MinimalDateSelectProps> = ({
  value,
  onChange,
  placeholder = 'Select month and year'
}) => {
  const [isOpen, setIsOpen] = useState(false);
  const containerRef = useRef<HTMLDivElement>(null);

  // Generate options for the last 10 years
  const generateOptions = (): Option[] => {
    const options: Option[] = [];
    const currentDate = new Date();
    const currentYear = currentDate.getFullYear();
    const currentMonth = currentDate.getMonth();
    
    // Generate from current date backwards for 10 years
    for (let year = currentYear; year >= currentYear - 10; year--) {
      const startMonth = year === currentYear ? currentMonth : 11;
      const endMonth = 0;
      
      for (let month = startMonth; month >= endMonth; month--) {
        const date = new Date(year, month, 1);
        const label = date.toLocaleDateString('en-US', { month: 'short', year: 'numeric' });
        
        options.push({
          value: date.toISOString(),
          label: label,
          description: `Founded ${label}`,
          date: date
        });
      }
    }
    
    return options;
  };

  const options = generateOptions();

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (containerRef.current && !containerRef.current.contains(event.target as Node)) {
        setIsOpen(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const formatDate = (date: Date | null) => {
    if (!date) return '';
    return date.toLocaleDateString('en-US', { month: 'short', year: 'numeric' });
  };

  const selectedValue = value ? formatDate(value) : '';

  return (
    <div ref={containerRef} className={styles.container}>
      <motion.button
        className={styles.trigger}
        onClick={() => setIsOpen(!isOpen)}
        whileTap={{ scale: 0.98 }}
      >
        <span className={value ? styles.value : styles.placeholder}>
          {selectedValue || placeholder}
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
                className={`${styles.option} ${selectedValue === option.label ? styles.selected : ''}`}
                onClick={() => {
                  onChange(option.date);
                  setIsOpen(false);
                }}
                whileHover={{ backgroundColor: '#f5f5f7' }}
                whileTap={{ scale: 0.98 }}
              >
                <span className={styles.optionLabel}>{option.label}</span>
                <span className={styles.optionDescription}>{option.description}</span>
              </motion.button>
            ))}
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};