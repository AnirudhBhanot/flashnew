import React from 'react';
import { motion, HTMLMotionProps } from 'framer-motion';
import classNames from 'classnames';
import styles from './Button.module.scss';

export interface ButtonProps extends Omit<HTMLMotionProps<"button">, 'size'> {
  variant?: 'primary' | 'secondary' | 'text' | 'destructive';
  size?: 'small' | 'medium' | 'large';
  fullWidth?: boolean;
  loading?: boolean;
  icon?: React.ReactNode;
  iconPosition?: 'left' | 'right';
  children: React.ReactNode;
}

export const Button: React.FC<ButtonProps> = ({
  variant = 'primary',
  size = 'medium',
  fullWidth = false,
  loading = false,
  disabled = false,
  icon,
  iconPosition = 'right',
  children,
  className,
  ...props
}) => {
  const buttonClass = classNames(
    styles.button,
    styles[variant],
    styles[size],
    {
      [styles.fullWidth]: fullWidth,
      [styles.loading]: loading,
      [styles.disabled]: disabled || loading,
      [styles.hasIcon]: !!icon,
    },
    className
  );

  return (
    <motion.button
      className={buttonClass}
      disabled={disabled || loading}
      whileTap={{ scale: 0.97 }}
      whileHover={{ scale: disabled || loading ? 1 : 1.02 }}
      transition={{ duration: 0.1 }}
      {...props}
    >
      {loading && (
        <span className={styles.spinner}>
          <svg viewBox="0 0 20 20">
            <circle
              cx="10"
              cy="10"
              r="8"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeDasharray="50.265"
              strokeDashoffset="50.265"
            >
              <animate
                attributeName="stroke-dashoffset"
                values="50.265;0;-50.265"
                dur="1.4s"
                repeatCount="indefinite"
              />
            </circle>
          </svg>
        </span>
      )}
      {icon && iconPosition === 'left' && !loading && (
        <span className={styles.icon}>{icon}</span>
      )}
      <span className={styles.label}>{children}</span>
      {icon && iconPosition === 'right' && !loading && (
        <span className={styles.icon}>{icon}</span>
      )}
    </motion.button>
  );
};