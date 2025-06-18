import React, { useState, useRef, useEffect } from 'react';
import { motion, AnimatePresence } from '../../../helpers/motion';
import classNames from 'classnames';
import { Icon } from '../Icon';
import styles from './TextField.module.scss';

export interface TextFieldProps {
  label: string;
  value: string;
  onChange: (value: string) => void;
  onBlur?: () => void;
  onFocus?: () => void;
  placeholder?: string;
  type?: 'text' | 'email' | 'password' | 'tel' | 'url' | 'number';
  error?: string;
  helper?: string;
  disabled?: boolean;
  required?: boolean;
  autoFocus?: boolean;
  autoComplete?: string;
  maxLength?: number;
  showCount?: boolean;
  icon?: React.ReactNode;
  clearable?: boolean;
  size?: 'small' | 'medium' | 'large';
  floatingLabel?: boolean;
}

export const TextField: React.FC<TextFieldProps> = ({
  label,
  value,
  onChange,
  onBlur,
  onFocus,
  placeholder,
  type = 'text',
  error,
  helper,
  disabled = false,
  required = false,
  autoFocus = false,
  autoComplete,
  maxLength,
  showCount = false,
  icon,
  clearable = true,
  size = 'medium',
  floatingLabel = true,
}) => {
  const [isFocused, setIsFocused] = useState(false);
  const [hasValue, setHasValue] = useState(!!value);
  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    setHasValue(!!value);
  }, [value]);

  const handleFocus = () => {
    setIsFocused(true);
    onFocus?.();
  };

  const handleBlur = () => {
    setIsFocused(false);
    onBlur?.();
  };

  const handleClear = () => {
    onChange('');
    inputRef.current?.focus();
  };

  const containerClass = classNames(
    styles.container,
    styles[size],
    {
      [styles.focused]: isFocused,
      [styles.hasValue]: hasValue,
      [styles.hasError]: !!error,
      [styles.disabled]: disabled,
      [styles.hasIcon]: !!icon,
      [styles.floatingLabel]: floatingLabel,
    }
  );

  const showClearButton = clearable && hasValue && !disabled;

  return (
    <div className={containerClass}>
      <div className={styles.inputWrapper}>
        {icon && <span className={styles.icon}>{icon}</span>}
        
        <input
          ref={inputRef}
          type={type}
          value={value}
          onChange={(e) => onChange(e.target.value)}
          onFocus={handleFocus}
          onBlur={handleBlur}
          placeholder={!floatingLabel ? placeholder : (isFocused || hasValue ? placeholder : '')}
          disabled={disabled}
          required={required}
          autoFocus={autoFocus}
          autoComplete={autoComplete}
          maxLength={maxLength}
          className={styles.input}
          aria-label={label}
          aria-invalid={!!error}
          aria-describedby={error ? `${label}-error` : helper ? `${label}-helper` : undefined}
        />
        
        <label className={styles.label}>
          {label}
          {required && <span className={styles.required}>*</span>}
        </label>
        
        <AnimatePresence>
          {showClearButton && (
            <motion.button
              type="button"
              className={styles.clearButton}
              onClick={handleClear}
              initial={{ opacity: 0, scale: 0.8 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0.8 }}
              transition={{ duration: 0.15 }}
              aria-label="Clear input"
            >
              <Icon name="xmark" size={16} />
            </motion.button>
          )}
        </AnimatePresence>
      </div>
      
      <AnimatePresence mode="wait">
        {error && (
          <motion.div
            className={styles.error}
            initial={{ opacity: 0, y: -4 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -4 }}
            transition={{ duration: 0.2 }}
            id={`${label}-error`}
          >
            <Icon name="info.circle" size={14} />
            {error}
          </motion.div>
        )}
        
        {helper && !error && (
          <motion.div
            className={styles.helper}
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            transition={{ duration: 0.2 }}
            id={`${label}-helper`}
          >
            {helper}
          </motion.div>
        )}
      </AnimatePresence>
      
      {showCount && maxLength && (
        <div className={styles.count}>
          {value.length}/{maxLength}
        </div>
      )}
    </div>
  );
};