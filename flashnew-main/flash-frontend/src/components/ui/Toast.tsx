import React, { createContext, useContext, useState, useCallback } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import './Toast.css';

interface Toast {
  id: string;
  title: string;
  message?: string;
  type?: 'success' | 'error' | 'warning' | 'info';
  duration?: number;
  action?: {
    label: string;
    onClick: () => void;
  };
}

interface ToastContextType {
  toasts: Toast[];
  showToast: (toast: Omit<Toast, 'id'>) => void;
  hideToast: (id: string) => void;
}

const ToastContext = createContext<ToastContextType | undefined>(undefined);

export const useToast = () => {
  const context = useContext(ToastContext);
  if (!context) {
    throw new Error('useToast must be used within ToastProvider');
  }
  return context;
};

export const ToastProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [toasts, setToasts] = useState<Toast[]>([]);

  const showToast = useCallback((toast: Omit<Toast, 'id'>) => {
    const id = `toast-${Date.now()}-${Math.random()}`;
    const newToast = { ...toast, id };
    
    setToasts(prev => [...prev, newToast]);

    // Auto-hide after duration
    if (toast.duration !== 0) {
      setTimeout(() => {
        hideToast(id);
      }, toast.duration || 5000);
    }
  }, []);

  const hideToast = useCallback((id: string) => {
    setToasts(prev => prev.filter(toast => toast.id !== id));
  }, []);

  return (
    <ToastContext.Provider value={{ toasts, showToast, hideToast }}>
      {children}
      <ToastContainer toasts={toasts} hideToast={hideToast} />
    </ToastContext.Provider>
  );
};

interface ToastContainerProps {
  toasts: Toast[];
  hideToast: (id: string) => void;
}

const ToastContainer: React.FC<ToastContainerProps> = ({ toasts, hideToast }) => {
  return (
    <div className="toast-container">
      <AnimatePresence>
        {toasts.map((toast, index) => (
          <ToastItem
            key={toast.id}
            toast={toast}
            onClose={() => hideToast(toast.id)}
            index={index}
          />
        ))}
      </AnimatePresence>
    </div>
  );
};

interface ToastItemProps {
  toast: Toast;
  onClose: () => void;
  index: number;
}

const ToastItem: React.FC<ToastItemProps> = ({ toast, onClose, index }) => {
  const getIcon = () => {
    switch (toast.type) {
      case 'success':
        return '✓';
      case 'error':
        return '✕';
      case 'warning':
        return '⚠';
      case 'info':
      default:
        return 'ℹ';
    }
  };

  return (
    <motion.div
      className={`toast toast-${toast.type || 'info'}`}
      initial={{ opacity: 0, y: 50, scale: 0.3 }}
      animate={{ opacity: 1, y: 0, scale: 1 }}
      exit={{ opacity: 0, scale: 0.5, transition: { duration: 0.2 } }}
      transition={{
        type: "spring",
        stiffness: 500,
        damping: 40,
        delay: index * 0.05
      }}
      layout
    >
      <div className="toast-icon">
        <motion.span
          initial={{ scale: 0 }}
          animate={{ scale: 1 }}
          transition={{ delay: 0.2, type: "spring", stiffness: 500 }}
        >
          {getIcon()}
        </motion.span>
      </div>
      
      <div className="toast-content">
        <h4 className="toast-title">{toast.title}</h4>
        {toast.message && (
          <p className="toast-message">{toast.message}</p>
        )}
        {toast.action && (
          <button
            className="toast-action"
            onClick={() => {
              toast.action!.onClick();
              onClose();
            }}
          >
            {toast.action.label}
          </button>
        )}
      </div>
      
      <button className="toast-close" onClick={onClose}>
        <svg width="14" height="14" viewBox="0 0 14 14" fill="currentColor">
          <path d="M13 1L1 13M1 1L13 13" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
        </svg>
      </button>
      
      <motion.div 
        className="toast-progress"
        initial={{ scaleX: 1 }}
        animate={{ scaleX: 0 }}
        transition={{ duration: (toast.duration || 5000) / 1000, ease: "linear" }}
      />
    </motion.div>
  );
};

// Simple toast functions for quick use
export const toast = {
  success: (title: string, message?: string) => {
    const { showToast } = useToast();
    showToast({ title, message, type: 'success' });
  },
  error: (title: string, message?: string) => {
    const { showToast } = useToast();
    showToast({ title, message, type: 'error' });
  },
  warning: (title: string, message?: string) => {
    const { showToast } = useToast();
    showToast({ title, message, type: 'warning' });
  },
  info: (title: string, message?: string) => {
    const { showToast } = useToast();
    showToast({ title, message, type: 'info' });
  }
};