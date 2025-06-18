import React, { useState, useRef } from 'react';
import './Button.css';

interface RippleProps {
  x: number;
  y: number;
  size: number;
}

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'ghost' | 'danger';
  size?: 'small' | 'medium' | 'large';
  loading?: boolean;
  icon?: React.ReactNode;
  children: React.ReactNode;
}

export const Button: React.FC<ButtonProps> = ({
  variant = 'primary',
  size = 'medium',
  loading = false,
  icon,
  children,
  className = '',
  disabled,
  onClick,
  ...props
}) => {
  const [ripples, setRipples] = useState<RippleProps[]>([]);
  const buttonRef = useRef<HTMLButtonElement>(null);

  const createRipple = (event: React.MouseEvent<HTMLButtonElement>) => {
    const button = buttonRef.current;
    if (!button) return;

    const rect = button.getBoundingClientRect();
    const size = Math.max(rect.width, rect.height);
    const x = event.clientX - rect.left - size / 2;
    const y = event.clientY - rect.top - size / 2;

    const newRipple = { x, y, size };
    setRipples(prev => [...prev, newRipple]);

    // Remove ripple after animation
    setTimeout(() => {
      setRipples(prev => prev.slice(1));
    }, 600);
  };

  const handleClick = (event: React.MouseEvent<HTMLButtonElement>) => {
    createRipple(event);
    if (onClick && !loading && !disabled) {
      onClick(event);
    }
  };

  const classes = [
    'btn',
    `btn-${variant}`,
    `btn-${size}`,
    loading && 'btn-loading',
    disabled && 'btn-disabled',
    className
  ].filter(Boolean).join(' ');

  return (
    <button
      ref={buttonRef}
      className={classes}
      disabled={disabled || loading}
      onClick={handleClick}
      {...props}
    >
      <span className="btn-content">
        {icon && <span className="btn-icon">{icon}</span>}
        <span className="btn-text">{children}</span>
      </span>
      
      {loading && (
        <span className="btn-loader">
          <span className="btn-loader-spinner" />
        </span>
      )}
      
      <span className="btn-ripple-container">
        {ripples.map((ripple, index) => (
          <span
            key={index}
            className="btn-ripple"
            style={{
              left: ripple.x,
              top: ripple.y,
              width: ripple.size,
              height: ripple.size,
            }}
          />
        ))}
      </span>
    </button>
  );
};