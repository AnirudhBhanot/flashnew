import React, { useState, useRef } from 'react';
import { motion, AnimatePresence } from '../../../helpers/motion';
import classNames from 'classnames';
import { Icon } from '../Icon';
import styles from './NumberField.module.scss';

export interface NumberFieldProps {
  label: string;
  value: number | string;
  onChange: (value: number | string) => void;
  onBlur?: () => void;
  placeholder?: string;
  error?: string;
  helper?: string;
  disabled?: boolean;
  required?: boolean;
  min?: number;
  max?: number;
  step?: number;
  prefix?: string;
  suffix?: string;
  size?: 'small' | 'medium' | 'large';
  stepper?: boolean;
  currency?: boolean;
  allowDecimal?: boolean;
  decimalPlaces?: number;
}

export const NumberField: React.FC<NumberFieldProps> = ({
  label,
  value,
  onChange,
  onBlur,
  placeholder,
  error,
  helper,
  disabled = false,
  required = false,
  min,
  max,
  step = 1,
  prefix,
  suffix,
  size = 'medium',
  stepper = true,
  currency = false,
  allowDecimal = true,
  decimalPlaces = 2,
}) => {
  const [isFocused, setIsFocused] = useState(false);
  const inputRef = useRef<HTMLInputElement>(null);

  const formatNumber = (num: number | string): string => {
    if (typeof num === 'string' && num === '') return '';
    
    const numValue = typeof num === 'string' ? parseFloat(num) : num;
    if (isNaN(numValue)) return '';
    
    if (currency) {
      return new Intl.NumberFormat('en-US', {
        minimumFractionDigits: 0,
        maximumFractionDigits: decimalPlaces,
      }).format(numValue);
    }
    
    return numValue.toString();
  };

  const parseNumber = (input: string): number | string => {
    if (input === '') return '';
    
    // Remove formatting
    const cleaned = input.replace(/,/g, '');
    
    if (!allowDecimal) {
      return parseInt(cleaned) || 0;
    }
    
    const parsed = parseFloat(cleaned);
    return isNaN(parsed) ? '' : parsed;
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const input = e.target.value;
    const parsed = parseNumber(input);
    
    if (parsed === '' || (typeof parsed === 'number' && !isNaN(parsed))) {
      onChange(parsed);
    }
  };

  const handleIncrement = () => {
    const current = typeof value === 'string' ? 0 : value;
    const newValue = current + step;
    if (max === undefined || newValue <= max) {
      onChange(newValue);
    }
  };

  const handleDecrement = () => {
    const current = typeof value === 'string' ? 0 : value;
    const newValue = current - step;
    if (min === undefined || newValue >= min) {
      onChange(newValue);
    }
  };

  const containerClass = classNames(
    styles.container,
    styles[size],
    {
      [styles.focused]: isFocused,
      [styles.hasError]: !!error,
      [styles.disabled]: disabled,
      [styles.hasPrefix]: !!prefix,
      [styles.hasSuffix]: !!suffix,
      [styles.hasStepper]: stepper,
    }
  );

  const displayValue = isFocused ? value : formatNumber(value);

  return (
    <div className={containerClass}>
      <label className={styles.label}>
        {label}
        {required && <span className={styles.required}>*</span>}
      </label>
      
      <div className={styles.inputWrapper}>
        {prefix && <span className={styles.prefix}>{prefix}</span>}
        
        <input
          ref={inputRef}
          type="text"
          inputMode="decimal"
          value={displayValue}
          onChange={handleChange}
          onFocus={() => setIsFocused(true)}
          onBlur={() => {
            setIsFocused(false);
            onBlur?.();
          }}
          placeholder={placeholder}
          disabled={disabled}
          className={styles.input}
          aria-label={label}
          aria-invalid={!!error}
        />
        
        {suffix && <span className={styles.suffix}>{suffix}</span>}
        
        {stepper && !disabled && (
          <div className={styles.stepper}>
            <button
              type="button"
              className={styles.stepperButton}
              onClick={handleIncrement}
              disabled={max !== undefined && Number(value) >= max}
              aria-label="Increase value"
            >
              <Icon name="chevron.up" size={12} />
            </button>
            <button
              type="button"
              className={styles.stepperButton}
              onClick={handleDecrement}
              disabled={min !== undefined && Number(value) <= min}
              aria-label="Decrease value"
            >
              <Icon name="chevron.down" size={12} />
            </button>
          </div>
        )}
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

// Specialized currency field
export const CurrencyField: React.FC<Omit<NumberFieldProps, 'currency' | 'prefix'>> = (props) => {
  return <NumberField {...props} currency prefix="$" allowDecimal />;
};

// Specialized percentage field
export const PercentageField: React.FC<Omit<NumberFieldProps, 'suffix' | 'min' | 'max'>> = (props) => {
  return <NumberField {...props} suffix="%" min={0} max={100} />;
};