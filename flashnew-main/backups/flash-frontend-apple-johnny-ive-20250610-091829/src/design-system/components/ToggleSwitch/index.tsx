import React from 'react';
import { motion } from 'framer-motion';
import styles from './ToggleSwitch.module.scss';

export interface ToggleSwitchProps {
  label: string;
  value: boolean;
  onChange: (value: boolean) => void;
  disabled?: boolean;
  size?: 'small' | 'medium' | 'large';
  labelPosition?: 'left' | 'right';
  helper?: string;
}

export const ToggleSwitch: React.FC<ToggleSwitchProps> = ({
  label,
  value,
  onChange,
  disabled = false,
  size = 'medium',
  labelPosition = 'left',
  helper,
}) => {
  const handleToggle = () => {
    if (!disabled) {
      onChange(!value);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === ' ' || e.key === 'Enter') {
      e.preventDefault();
      handleToggle();
    }
  };

  const switchContent = (
    <div
      className={`${styles.switch} ${styles[size]} ${value ? styles.on : ''} ${disabled ? styles.disabled : ''}`}
      onClick={handleToggle}
      onKeyDown={handleKeyDown}
      role="switch"
      aria-checked={value}
      aria-label={label}
      tabIndex={disabled ? -1 : 0}
    >
      <motion.div
        className={styles.thumb}
        animate={{
          x: value ? '100%' : '0%',
        }}
        transition={{
          type: 'spring',
          stiffness: 500,
          damping: 30,
        }}
      />
    </div>
  );

  return (
    <div className={styles.container}>
      <div className={`${styles.wrapper} ${labelPosition === 'right' ? styles.rightLabel : ''}`}>
        {labelPosition === 'left' && (
          <label 
            className={styles.label}
            onClick={handleToggle}
          >
            {label}
          </label>
        )}
        
        {switchContent}
        
        {labelPosition === 'right' && (
          <label 
            className={styles.label}
            onClick={handleToggle}
          >
            {label}
          </label>
        )}
      </div>
      
      {helper && (
        <p className={styles.helper}>{helper}</p>
      )}
    </div>
  );
};