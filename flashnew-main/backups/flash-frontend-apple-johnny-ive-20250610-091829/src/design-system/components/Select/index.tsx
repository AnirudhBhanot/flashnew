import React, { useState, useRef, useEffect } from 'react';
import { motion, AnimatePresence } from '../../../helpers/motion';
import classNames from 'classnames';
import { Icon } from '../Icon';
import styles from './Select.module.scss';

export interface SelectOption {
  value: string;
  label: string;
  disabled?: boolean;
}

export interface SelectProps {
  label: string;
  value: string;
  onChange: (value: string) => void;
  options: SelectOption[];
  placeholder?: string;
  error?: string;
  helper?: string;
  disabled?: boolean;
  required?: boolean;
  size?: 'small' | 'medium' | 'large';
  fullWidth?: boolean;
}

export const Select: React.FC<SelectProps> = ({
  label,
  value,
  onChange,
  options,
  placeholder = 'Select an option',
  error,
  helper,
  disabled = false,
  required = false,
  size = 'medium',
  fullWidth = true,
}) => {
  const [isOpen, setIsOpen] = useState(false);
  const [highlightedIndex, setHighlightedIndex] = useState(-1);
  const containerRef = useRef<HTMLDivElement>(null);
  const buttonRef = useRef<HTMLButtonElement>(null);
  const listRef = useRef<HTMLUListElement>(null);

  const selectedOption = options.find(opt => opt.value === value);

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (containerRef.current && !containerRef.current.contains(event.target as Node)) {
        setIsOpen(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  useEffect(() => {
    if (isOpen && highlightedIndex >= 0 && listRef.current) {
      const highlightedElement = listRef.current.children[highlightedIndex] as HTMLElement;
      if (highlightedElement) {
        highlightedElement.scrollIntoView({ block: 'nearest' });
      }
    }
  }, [highlightedIndex, isOpen]);

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (disabled) return;

    switch (e.key) {
      case 'Enter':
      case ' ':
        e.preventDefault();
        if (isOpen && highlightedIndex >= 0) {
          const option = options[highlightedIndex];
          if (!option.disabled) {
            onChange(option.value);
            setIsOpen(false);
          }
        } else {
          setIsOpen(!isOpen);
        }
        break;
      case 'ArrowDown':
        e.preventDefault();
        if (!isOpen) {
          setIsOpen(true);
        } else {
          setHighlightedIndex(prev => {
            const next = prev + 1;
            return next >= options.length ? 0 : next;
          });
        }
        break;
      case 'ArrowUp':
        e.preventDefault();
        if (!isOpen) {
          setIsOpen(true);
        } else {
          setHighlightedIndex(prev => {
            const next = prev - 1;
            return next < 0 ? options.length - 1 : next;
          });
        }
        break;
      case 'Escape':
        setIsOpen(false);
        break;
    }
  };

  const handleSelect = (option: SelectOption) => {
    if (!option.disabled) {
      onChange(option.value);
      setIsOpen(false);
      setHighlightedIndex(-1);
    }
  };

  const containerClass = classNames(
    styles.container,
    styles[size],
    {
      [styles.fullWidth]: fullWidth,
      [styles.disabled]: disabled,
      [styles.hasError]: !!error,
      [styles.isOpen]: isOpen,
    }
  );

  return (
    <div className={containerClass} ref={containerRef}>
      <label className={styles.label}>
        {label}
        {required && <span className={styles.required}>*</span>}
      </label>
      
      <button
        ref={buttonRef}
        type="button"
        className={styles.trigger}
        onClick={() => !disabled && setIsOpen(!isOpen)}
        onKeyDown={handleKeyDown}
        disabled={disabled}
        aria-label={label}
        aria-haspopup="listbox"
        aria-expanded={isOpen}
        aria-invalid={!!error}
      >
        <span className={styles.value}>
          {selectedOption ? selectedOption.label : placeholder}
        </span>
        <motion.span 
          className={styles.arrow}
          animate={{ rotate: isOpen ? 180 : 0 }}
          transition={{ duration: 0.2 }}
        >
          <Icon name="chevron.down" size={16} />
        </motion.span>
      </button>
      
      <AnimatePresence>
        {isOpen && (
          <motion.ul
            ref={listRef}
            className={styles.dropdown}
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -10 }}
            transition={{ duration: 0.2, ease: [0.2, 0, 0, 1] }}
            role="listbox"
            aria-label={label}
          >
            {options.map((option, index) => (
              <li
                key={option.value}
                className={classNames(styles.option, {
                  [styles.selected]: option.value === value,
                  [styles.highlighted]: index === highlightedIndex,
                  [styles.disabled]: option.disabled,
                })}
                onClick={() => handleSelect(option)}
                onMouseEnter={() => setHighlightedIndex(index)}
                role="option"
                aria-selected={option.value === value}
                aria-disabled={option.disabled}
              >
                {option.label}
                {option.value === value && (
                  <Icon name="checkmark" size={16} />
                )}
              </li>
            ))}
          </motion.ul>
        )}
      </AnimatePresence>
      
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

// Option component for use in JSX
export const Option: React.FC<{ value: string; children: React.ReactNode }> = ({ children }) => {
  // This component is only for JSX syntax, actual rendering is handled by Select
  return null;
};