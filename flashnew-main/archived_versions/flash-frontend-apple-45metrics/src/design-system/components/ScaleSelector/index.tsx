import React from 'react';
import { motion } from 'framer-motion';
import classNames from 'classnames';
import styles from './ScaleSelector.module.scss';

export interface ScaleSelectorProps {
  label: string;
  value: number;
  onChange: (value: number) => void;
  min?: number;
  max?: number;
  step?: number;
  labels?: Record<number, string>;
  showValue?: boolean;
  showLabels?: boolean;
  error?: string;
  helper?: string;
  disabled?: boolean;
  required?: boolean;
  size?: 'small' | 'medium' | 'large';
}

export const ScaleSelector: React.FC<ScaleSelectorProps> = ({
  label,
  value,
  onChange,
  min = 1,
  max = 10,
  step = 1,
  labels,
  showValue = true,
  showLabels = true,
  error,
  helper,
  disabled = false,
  required = false,
  size = 'medium',
}) => {
  const steps = [];
  for (let i = min; i <= max; i += step) {
    steps.push(i);
  }

  const getLabel = (num: number): string | undefined => {
    if (!labels) return undefined;
    return labels[num];
  };

  const containerClass = classNames(
    styles.container,
    styles[size],
    {
      [styles.hasError]: !!error,
      [styles.disabled]: disabled,
    }
  );

  const getScaleColor = (num: number): string => {
    const percentage = ((num - min) / (max - min)) * 100;
    if (percentage <= 33) return 'var(--apple-red)';
    if (percentage <= 66) return 'var(--apple-orange)';
    return 'var(--apple-green)';
  };

  return (
    <div className={containerClass}>
      <div className={styles.header}>
        <label className={styles.label}>
          {label}
          {required && <span className={styles.required}>*</span>}
        </label>
        {showValue && (
          <span className={styles.currentValue} style={{ color: getScaleColor(value) }}>
            {value}
          </span>
        )}
      </div>
      
      <div className={styles.scale}>
        {steps.map((num) => {
          const isSelected = value === num;
          const label = getLabel(num);
          
          return (
            <motion.button
              key={num}
              type="button"
              className={classNames(styles.step, {
                [styles.selected]: isSelected,
                [styles.disabled]: disabled,
              })}
              onClick={() => !disabled && onChange(num)}
              disabled={disabled}
              whileHover={!disabled ? { scale: 1.1 } : {}}
              whileTap={!disabled ? { scale: 0.95 } : {}}
              transition={{ duration: 0.1 }}
            >
              <span 
                className={styles.stepNumber}
                style={{ 
                  backgroundColor: isSelected ? getScaleColor(num) : undefined,
                  borderColor: isSelected ? getScaleColor(num) : undefined,
                }}
              >
                {num}
              </span>
              {showLabels && label && (
                <span className={styles.stepLabel}>{label}</span>
              )}
            </motion.button>
          );
        })}
      </div>
      
      {showLabels && labels && (
        <div className={styles.labelRow}>
          {Object.entries(labels).map(([key, label]) => (
            <div key={key} className={styles.labelItem}>
              <span className={styles.labelKey}>{key}</span>
              <span className={styles.labelText}>{label}</span>
            </div>
          ))}
        </div>
      )}
      
      {error && (
        <div className={styles.error}>
          {error}
        </div>
      )}
      
      {helper && !error && (
        <div className={styles.helper}>
          {helper}
        </div>
      )}
    </div>
  );
};