import React, { createContext, useContext, useState, useCallback, ReactNode } from 'react';
import { AnimatePresence, motion } from 'framer-motion';
import { Icon } from '../design-system/components';
import styles from './ErrorContext.module.scss';

interface ErrorMessage {
  id: string;
  message: string;
  type: 'error' | 'warning' | 'info';
  timestamp: number;
}

interface ErrorContextType {
  showError: (message: string, type?: 'error' | 'warning' | 'info') => void;
  clearError: (id: string) => void;
  clearAllErrors: () => void;
}

const ErrorContext = createContext<ErrorContextType | undefined>(undefined);

export const useError = () => {
  const context = useContext(ErrorContext);
  if (!context) {
    throw new Error('useError must be used within ErrorProvider');
  }
  return context;
};

interface ErrorProviderProps {
  children: ReactNode;
}

export const ErrorProvider: React.FC<ErrorProviderProps> = ({ children }) => {
  const [errors, setErrors] = useState<ErrorMessage[]>([]);

  const showError = useCallback((message: string, type: 'error' | 'warning' | 'info' = 'error') => {
    const id = `${Date.now()}-${Math.random()}`;
    const newError: ErrorMessage = {
      id,
      message,
      type,
      timestamp: Date.now()
    };
    
    setErrors(prev => [...prev, newError]);
    
    // Auto-dismiss after 5 seconds
    setTimeout(() => {
      clearError(id);
    }, 5000);
  }, []);

  const clearError = useCallback((id: string) => {
    setErrors(prev => prev.filter(error => error.id !== id));
  }, []);

  const clearAllErrors = useCallback(() => {
    setErrors([]);
  }, []);

  return (
    <ErrorContext.Provider value={{ showError, clearError, clearAllErrors }}>
      {children}
      <div className={styles.errorContainer}>
        <AnimatePresence>
          {errors.map((error) => (
            <motion.div
              key={error.id}
              className={`${styles.errorToast} ${styles[error.type]}`}
              initial={{ opacity: 0, y: -20, scale: 0.9 }}
              animate={{ opacity: 1, y: 0, scale: 1 }}
              exit={{ opacity: 0, y: -20, scale: 0.9 }}
              transition={{ duration: 0.3 }}
            >
              <Icon 
                name={error.type === 'error' ? 'exclamationmark.circle' : 
                      error.type === 'warning' ? 'exclamationmark.triangle' : 
                      'info.circle'} 
                size={20} 
              />
              <span className={styles.message}>{error.message}</span>
              <button 
                className={styles.closeButton}
                onClick={() => clearError(error.id)}
                aria-label="Dismiss"
              >
                <Icon name="xmark" size={16} />
              </button>
            </motion.div>
          ))}
        </AnimatePresence>
      </div>
    </ErrorContext.Provider>
  );
};