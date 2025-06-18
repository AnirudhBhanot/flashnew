import React, { useState, useRef, useEffect } from 'react';
import { motion } from 'framer-motion';
import styles from './TextArea.module.scss';

export interface TextAreaProps {
  label: string;
  value: string;
  onChange: (value: string) => void;
  placeholder?: string;
  error?: string;
  helper?: string;
  disabled?: boolean;
  required?: boolean;
  floatingLabel?: boolean;
  rows?: number;
  maxLength?: number;
  showCount?: boolean;
  autoResize?: boolean;
  minRows?: number;
  maxRows?: number;
}

export const TextArea: React.FC<TextAreaProps> = ({
  label,
  value,
  onChange,
  placeholder = '',
  error,
  helper,
  disabled = false,
  required = false,
  floatingLabel = true,
  rows = 3,
  maxLength,
  showCount = false,
  autoResize = false,
  minRows = 3,
  maxRows = 10,
}) => {
  const [isFocused, setIsFocused] = useState(false);
  const [textAreaHeight, setTextAreaHeight] = useState('auto');
  const textAreaRef = useRef<HTMLTextAreaElement>(null);
  
  const shouldFloat = floatingLabel && (isFocused || value);
  
  useEffect(() => {
    if (autoResize && textAreaRef.current) {
      // Reset height to auto to get the correct scrollHeight
      setTextAreaHeight('auto');
      
      // Calculate new height
      const scrollHeight = textAreaRef.current.scrollHeight;
      const lineHeight = parseInt(getComputedStyle(textAreaRef.current).lineHeight);
      const minHeight = lineHeight * minRows;
      const maxHeight = lineHeight * maxRows;
      
      const newHeight = Math.min(Math.max(scrollHeight, minHeight), maxHeight);
      setTextAreaHeight(`${newHeight}px`);
    }
  }, [value, autoResize, minRows, maxRows]);
  
  const handleChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    const newValue = e.target.value;
    if (!maxLength || newValue.length <= maxLength) {
      onChange(newValue);
    }
  };
  
  const characterCount = value.length;
  const isOverLimit = maxLength && characterCount > maxLength;

  return (
    <div className={`${styles.container} ${disabled ? styles.disabled : ''}`}>
      {floatingLabel && (
        <label 
          className={`${styles.label} ${shouldFloat ? styles.floating : ''}`}
          htmlFor={label}
        >
          {label}
          {required && <span className={styles.required}>*</span>}
        </label>
      )}
      
      {!floatingLabel && (
        <label className={styles.staticLabel} htmlFor={label}>
          {label}
          {required && <span className={styles.required}>*</span>}
        </label>
      )}
      
      <div className={styles.textAreaWrapper}>
        <textarea
          ref={textAreaRef}
          id={label}
          className={`${styles.textArea} ${error ? styles.error : ''}`}
          value={value}
          onChange={handleChange}
          placeholder={isFocused || !floatingLabel ? placeholder : ''}
          onFocus={() => setIsFocused(true)}
          onBlur={() => setIsFocused(false)}
          disabled={disabled}
          rows={autoResize ? minRows : rows}
          style={autoResize ? { height: textAreaHeight, overflow: textAreaHeight === 'auto' ? 'hidden' : 'auto' } : {}}
        />
        
        {showCount && maxLength && (
          <div className={`${styles.counter} ${isOverLimit ? styles.overLimit : ''}`}>
            {characterCount}/{maxLength}
          </div>
        )}
      </div>
      
      {helper && !error && (
        <p className={styles.helper}>{helper}</p>
      )}
      
      {error && (
        <motion.p 
          className={styles.error}
          initial={{ opacity: 0, y: -5 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: -5 }}
        >
          {error}
        </motion.p>
      )}
    </div>
  );
};