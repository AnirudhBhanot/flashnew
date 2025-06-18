import React, { useState } from 'react';
import { motion, AnimatePresence } from '../../../helpers/motion';
import classNames from 'classnames';
import { Icon } from '../Icon';
import styles from './DatePicker.module.scss';

export interface DatePickerProps {
  label: string;
  value: Date | null;
  onChange: (date: Date | null) => void;
  placeholder?: string;
  error?: string;
  helper?: string;
  disabled?: boolean;
  required?: boolean;
  min?: Date;
  max?: Date;
  size?: 'small' | 'medium' | 'large';
}

export const DatePicker: React.FC<DatePickerProps> = ({
  label,
  value,
  onChange,
  placeholder = 'Select date',
  error,
  helper,
  disabled = false,
  required = false,
  min,
  max,
  size = 'medium',
}) => {
  const [isFocused, setIsFocused] = useState(false);

  const formatDate = (date: Date | null): string => {
    if (!date) return '';
    return date.toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
    });
  };

  const formatDateForInput = (date: Date | null): string => {
    if (!date) return '';
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    return `${year}-${month}-${day}`;
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const dateString = e.target.value;
    if (dateString) {
      const newDate = new Date(dateString);
      if (!isNaN(newDate.getTime())) {
        onChange(newDate);
      }
    } else {
      onChange(null);
    }
  };

  const handleClear = () => {
    onChange(null);
  };

  const containerClass = classNames(
    styles.container,
    styles[size],
    {
      [styles.focused]: isFocused,
      [styles.hasValue]: !!value,
      [styles.hasError]: !!error,
      [styles.disabled]: disabled,
    }
  );

  return (
    <div className={containerClass}>
      <label className={styles.label}>
        {label}
        {required && <span className={styles.required}>*</span>}
      </label>
      
      <div className={styles.inputWrapper}>
        <div className={styles.dateDisplay}>
          {value ? formatDate(value) : placeholder}
        </div>
        
        <input
          type="date"
          value={formatDateForInput(value)}
          onChange={handleChange}
          onFocus={() => setIsFocused(true)}
          onBlur={() => setIsFocused(false)}
          disabled={disabled}
          min={min ? formatDateForInput(min) : undefined}
          max={max ? formatDateForInput(max) : undefined}
          className={styles.input}
          aria-label={label}
          aria-invalid={!!error}
        />
        
        <div className={styles.icons}>
          {value && !disabled && (
            <button
              type="button"
              className={styles.clearButton}
              onClick={handleClear}
              aria-label="Clear date"
            >
              <Icon name="xmark" size={16} />
            </button>
          )}
          <span className={styles.calendarIcon}>
            <Icon name="calendar" size={20} />
          </span>
        </div>
      </div>
      
      <AnimatePresence mode="wait">
        {error && (
          <motion.div
            className={styles.error}
            initial={{ opacity: 0, y: -4 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -4 }}
            transition={{ duration: 0.2 }}
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
          >
            {helper}
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};