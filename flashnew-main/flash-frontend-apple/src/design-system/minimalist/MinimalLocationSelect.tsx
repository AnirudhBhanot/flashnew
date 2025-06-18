import React, { useState, useRef, useEffect } from 'react';
import { motion } from 'framer-motion';
import { AnimatePresence } from '../components/AnimatePresenceWrapper';
import styles from './MinimalSelect.module.scss'; // Use the same styles!

interface Option {
  value: string;
  label: string;
  description?: string;
}

interface MinimalLocationSelectProps {
  value: string;
  onChange: (value: string) => void;
  placeholder?: string;
}

export const MinimalLocationSelect: React.FC<MinimalLocationSelectProps> = ({
  value,
  onChange,
  placeholder = 'Select location'
}) => {
  const [isOpen, setIsOpen] = useState(false);
  const containerRef = useRef<HTMLDivElement>(null);

  const options: Option[] = [
    // United States
    { value: 'San Francisco, CA', label: 'San Francisco, CA', description: 'Bay Area, United States' },
    { value: 'New York, NY', label: 'New York, NY', description: 'East Coast, United States' },
    { value: 'Austin, TX', label: 'Austin, TX', description: 'Texas, United States' },
    { value: 'Boston, MA', label: 'Boston, MA', description: 'Massachusetts, United States' },
    { value: 'Seattle, WA', label: 'Seattle, WA', description: 'Pacific Northwest, United States' },
    { value: 'Los Angeles, CA', label: 'Los Angeles, CA', description: 'Southern California, United States' },
    { value: 'Chicago, IL', label: 'Chicago, IL', description: 'Midwest, United States' },
    { value: 'Denver, CO', label: 'Denver, CO', description: 'Colorado, United States' },
    { value: 'Miami, FL', label: 'Miami, FL', description: 'Florida, United States' },
    { value: 'Atlanta, GA', label: 'Atlanta, GA', description: 'Georgia, United States' },
    { value: 'Portland, OR', label: 'Portland, OR', description: 'Oregon, United States' },
    { value: 'Washington, DC', label: 'Washington, DC', description: 'Capital, United States' },
    
    // International
    { value: 'London, UK', label: 'London, UK', description: 'United Kingdom' },
    { value: 'Paris, France', label: 'Paris, France', description: 'Europe' },
    { value: 'Berlin, Germany', label: 'Berlin, Germany', description: 'Europe' },
    { value: 'Toronto, Canada', label: 'Toronto, Canada', description: 'North America' },
    { value: 'Vancouver, Canada', label: 'Vancouver, Canada', description: 'North America' },
    { value: 'Singapore', label: 'Singapore', description: 'Southeast Asia' },
    { value: 'Tokyo, Japan', label: 'Tokyo, Japan', description: 'Asia Pacific' },
    { value: 'Sydney, Australia', label: 'Sydney, Australia', description: 'Asia Pacific' },
    { value: 'Tel Aviv, Israel', label: 'Tel Aviv, Israel', description: 'Middle East' },
    { value: 'Dubai, UAE', label: 'Dubai, UAE', description: 'Middle East' },
    { value: 'Mumbai, India', label: 'Mumbai, India', description: 'South Asia' },
    { value: 'Bangalore, India', label: 'Bangalore, India', description: 'South Asia' },
    { value: 'São Paulo, Brazil', label: 'São Paulo, Brazil', description: 'South America' },
    { value: 'Mexico City, Mexico', label: 'Mexico City, Mexico', description: 'North America' },
    { value: 'Remote', label: 'Remote', description: 'Distributed team' },
    { value: 'Other', label: 'Other', description: 'Not listed above' },
  ];

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
          {selectedOption?.label || value || placeholder}
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