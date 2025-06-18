import React, { useRef, useEffect } from 'react';
import { motion } from 'framer-motion';
import styles from './MinimalInput.module.scss';

interface MinimalInputProps {
  value: string | number;
  onChange: (value: string) => void;
  type?: 'text' | 'number' | 'currency' | 'url';
  placeholder?: string;
  autoFocus?: boolean;
  prefix?: string;
  suffix?: string;
  align?: 'left' | 'center' | 'right';
}

export const MinimalInput: React.FC<MinimalInputProps> = ({
  value,
  onChange,
  type = 'text',
  placeholder = '',
  autoFocus = false,
  prefix,
  suffix,
  align = 'left'
}) => {
  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    if (autoFocus && inputRef.current) {
      inputRef.current.focus();
    }
  }, [autoFocus]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const newValue = e.target.value;
    
    if (type === 'currency' || type === 'number') {
      // Allow only numbers and formatting characters
      const cleaned = newValue.replace(/[^0-9.,]/g, '');
      onChange(cleaned);
    } else {
      onChange(newValue);
    }
  };

  const formatDisplay = (val: string | number) => {
    if (type === 'currency' && val && val !== '') {
      const num = Number(String(val).replace(/[^0-9]/g, ''));
      return num.toLocaleString('en-US');
    }
    return val;
  };

  return (
    <div className={`${styles.container} ${styles[align]}`}>
      {prefix && <span className={styles.prefix}>{prefix}</span>}
      <input
        ref={inputRef}
        type="text"
        value={formatDisplay(value)}
        onChange={handleChange}
        placeholder={placeholder}
        className={styles.input}
        spellCheck="false"
        autoComplete="off"
      />
      {suffix && <span className={styles.suffix}>{suffix}</span>}
      <motion.div 
        className={styles.underline}
        initial={{ scaleX: 0 }}
        animate={{ scaleX: value ? 1 : 0 }}
        transition={{ duration: 0.6, ease: [0.25, 0, 0, 1] }}
      />
    </div>
  );
};