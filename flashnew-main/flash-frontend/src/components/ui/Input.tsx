import React, { useState, useRef, useEffect } from 'react';
import './Input.css';

interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
  success?: boolean;
  floatingLabel?: boolean;
  icon?: React.ReactNode;
  onClear?: () => void;
}

export const Input: React.FC<InputProps> = ({
  label,
  error,
  success,
  floatingLabel = true,
  icon,
  onClear,
  className = '',
  onFocus,
  onBlur,
  onChange,
  value,
  ...props
}) => {
  const [isFocused, setIsFocused] = useState(false);
  const [hasValue, setHasValue] = useState(!!value);
  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    setHasValue(!!value);
  }, [value]);

  const handleFocus = (e: React.FocusEvent<HTMLInputElement>) => {
    setIsFocused(true);
    if (onFocus) onFocus(e);
  };

  const handleBlur = (e: React.FocusEvent<HTMLInputElement>) => {
    setIsFocused(false);
    if (onBlur) onBlur(e);
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setHasValue(!!e.target.value);
    if (onChange) onChange(e);
  };

  const handleClear = () => {
    if (onClear) onClear();
    if (inputRef.current) {
      inputRef.current.focus();
    }
  };

  const inputClasses = [
    'input',
    error && 'input-error',
    success && 'input-success',
    isFocused && 'input-focused',
    hasValue && 'input-has-value',
    icon && 'input-with-icon',
    className
  ].filter(Boolean).join(' ');

  const wrapperClasses = [
    'input-wrapper',
    floatingLabel && 'input-floating-label',
    error && 'input-wrapper-error',
    success && 'input-wrapper-success'
  ].filter(Boolean).join(' ');

  return (
    <div className={wrapperClasses}>
      {icon && <span className="input-icon">{icon}</span>}
      
      <input
        ref={inputRef}
        className={inputClasses}
        value={value}
        onFocus={handleFocus}
        onBlur={handleBlur}
        onChange={handleChange}
        placeholder={!floatingLabel ? label : ' '}
        {...props}
      />
      
      {floatingLabel && label && (
        <label className="input-label">
          {label}
        </label>
      )}
      
      {hasValue && onClear && (
        <button
          type="button"
          className="input-clear"
          onClick={handleClear}
          tabIndex={-1}
        >
          <svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor">
            <path d="M12.5 3.5L3.5 12.5M3.5 3.5L12.5 12.5" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
          </svg>
        </button>
      )}
      
      {(error || success) && (
        <div className="input-feedback">
          {error && (
            <>
              <svg className="input-feedback-icon" width="16" height="16" viewBox="0 0 16 16">
                <circle cx="8" cy="8" r="7" fill="none" stroke="currentColor" strokeWidth="2"/>
                <path d="M8 5v3M8 10v1" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
              </svg>
              <span className="input-feedback-text">{error}</span>
            </>
          )}
          {success && !error && (
            <>
              <svg className="input-feedback-icon" width="16" height="16" viewBox="0 0 16 16">
                <circle cx="8" cy="8" r="7" fill="none" stroke="currentColor" strokeWidth="2"/>
                <path d="M5 8l2 2 4-4" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
              </svg>
              <span className="input-feedback-text">Valid input</span>
            </>
          )}
        </div>
      )}
    </div>
  );
};