import React, { useState, useRef, useEffect } from 'react';
import { motion, AnimatePresence } from '../../../helpers/motion';
import styles from './MultiSelect.module.scss';
import { Icon } from '../Icon';

interface Option {
  value: string;
  label: string;
}

export interface MultiSelectProps {
  label: string;
  placeholder?: string;
  value: string[];
  onChange: (value: string[]) => void;
  options: Option[];
  error?: string;
  helper?: string;
  disabled?: boolean;
  required?: boolean;
  floatingLabel?: boolean;
  maxSelections?: number;
}

export const MultiSelect: React.FC<MultiSelectProps> = ({
  label,
  placeholder = 'Select options',
  value = [],
  onChange,
  options,
  error,
  helper,
  disabled = false,
  required = false,
  floatingLabel = true,
  maxSelections,
}) => {
  const [isOpen, setIsOpen] = useState(false);
  const [searchTerm, setSearchTerm] = useState('');
  const containerRef = useRef<HTMLDivElement>(null);
  const searchRef = useRef<HTMLInputElement>(null);

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
    if (isOpen && searchRef.current) {
      searchRef.current.focus();
    }
  }, [isOpen]);

  const filteredOptions = options.filter(option =>
    option.label.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const toggleOption = (optionValue: string) => {
    const newValue = value.includes(optionValue)
      ? value.filter(v => v !== optionValue)
      : [...value, optionValue];
    
    if (maxSelections && newValue.length > maxSelections) {
      return;
    }
    
    onChange(newValue);
  };

  const removeOption = (optionValue: string, e: React.MouseEvent) => {
    e.stopPropagation();
    onChange(value.filter(v => v !== optionValue));
  };

  const selectedOptions = options.filter(opt => value.includes(opt.value));
  
  const displayValue = selectedOptions.length > 0
    ? `${selectedOptions.length} selected`
    : '';

  const shouldFloat = floatingLabel && (value.length > 0 || isOpen);

  return (
    <div 
      className={`${styles.container} ${disabled ? styles.disabled : ''}`}
      ref={containerRef}
    >
      {floatingLabel && (
        <label className={`${styles.label} ${shouldFloat ? styles.floating : ''}`}>
          {label}
          {required && <span className={styles.required}>*</span>}
        </label>
      )}
      
      {!floatingLabel && (
        <label className={styles.staticLabel}>
          {label}
          {required && <span className={styles.required}>*</span>}
        </label>
      )}
      
      <div
        className={`${styles.select} ${isOpen ? styles.open : ''} ${error ? styles.error : ''}`}
        onClick={() => !disabled && setIsOpen(!isOpen)}
      >
        <div className={styles.value}>
          {displayValue || <span className={styles.placeholder}>{placeholder}</span>}
        </div>
        <Icon 
          name={isOpen ? 'chevron.up' : 'chevron.down'} 
          size={16} 
          className={styles.chevron}
        />
      </div>
      
      {selectedOptions.length > 0 && (
        <div className={styles.tags}>
          {selectedOptions.map(option => (
            <motion.div
              key={option.value}
              className={styles.tag}
              initial={{ opacity: 0, scale: 0.8 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0.8 }}
              transition={{ duration: 0.2 }}
            >
              <span>{option.label}</span>
              <button
                type="button"
                onClick={(e) => removeOption(option.value, e)}
                className={styles.removeButton}
                disabled={disabled}
              >
                <Icon name="xmark" size={12} />
              </button>
            </motion.div>
          ))}
        </div>
      )}
      
      <AnimatePresence>
        {isOpen && (
          <motion.div
            className={styles.dropdown}
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -10 }}
            transition={{ duration: 0.2 }}
          >
            <div className={styles.searchWrapper}>
              <Icon name="magnifyingglass" size={16} className={styles.searchIcon} />
              <input
                ref={searchRef}
                type="text"
                className={styles.search}
                placeholder="Search options..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                onClick={(e) => e.stopPropagation()}
              />
            </div>
            
            <div className={styles.options}>
              {filteredOptions.length === 0 ? (
                <div className={styles.noOptions}>No options found</div>
              ) : (
                filteredOptions.map(option => {
                  const isSelected = value.includes(option.value);
                  const isDisabled = !isSelected && maxSelections && value.length >= maxSelections;
                  
                  return (
                    <motion.div
                      key={option.value}
                      className={`${styles.option} ${isSelected ? styles.selected : ''} ${isDisabled ? styles.optionDisabled : ''}`}
                      onClick={() => !isDisabled && toggleOption(option.value)}
                      whileHover={!isDisabled ? { backgroundColor: 'var(--apple-fill-quaternary)' } : {}}
                      whileTap={!isDisabled ? { scale: 0.98 } : {}}
                    >
                      <div className={styles.checkbox}>
                        {isSelected && <Icon name="checkmark" size={12} />}
                      </div>
                      <span>{option.label}</span>
                    </motion.div>
                  );
                })
              )}
            </div>
            
            {maxSelections && (
              <div className={styles.footer}>
                {value.length} / {maxSelections} selected
              </div>
            )}
          </motion.div>
        )}
      </AnimatePresence>
      
      {helper && !error && (
        <p className={styles.helper}>{helper}</p>
      )}
      
      {error && (
        <p className={styles.error}>{error}</p>
      )}
    </div>
  );
};