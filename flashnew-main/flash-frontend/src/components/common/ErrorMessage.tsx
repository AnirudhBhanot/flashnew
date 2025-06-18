import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import './ErrorMessage.css';

interface ErrorMessageProps {
  error: string | Error | null;
  onRetry?: () => void;
  onDismiss?: () => void;
  variant?: 'inline' | 'toast' | 'page';
  className?: string;
}

export const ErrorMessage: React.FC<ErrorMessageProps> = ({
  error,
  onRetry,
  onDismiss,
  variant = 'inline',
  className = ''
}) => {
  if (!error) return null;
  
  const errorMessage = typeof error === 'string' ? error : error.message;
  
  // Provide user-friendly error messages
  const getUserFriendlyMessage = (msg: string): string => {
    if (msg.includes('Network') || msg.includes('fetch')) {
      return 'Unable to connect to the server. Please check your internet connection and try again.';
    }
    if (msg.includes('404')) {
      return 'The requested resource was not found. Please try again later.';
    }
    if (msg.includes('500') || msg.includes('Internal Server Error')) {
      return 'Our servers are experiencing issues. Please try again in a few moments.';
    }
    if (msg.includes('timeout')) {
      return 'The request took too long to complete. Please try again.';
    }
    if (msg.includes('API Error')) {
      return 'There was an error processing your request. Please try again.';
    }
    return msg || 'An unexpected error occurred. Please try again.';
  };
  
  const friendlyMessage = getUserFriendlyMessage(errorMessage);
  
  if (variant === 'toast') {
    return (
      <AnimatePresence>
        <motion.div
          className={`error-toast ${className}`}
          initial={{ opacity: 0, y: 50, scale: 0.9 }}
          animate={{ opacity: 1, y: 0, scale: 1 }}
          exit={{ opacity: 0, y: 20, scale: 0.9 }}
          role="alert"
          aria-live="assertive"
        >
          <div className="error-toast-content">
            <div className="error-toast-icon">⚠️</div>
            <div className="error-toast-message">
              <h4>Error</h4>
              <p>{friendlyMessage}</p>
            </div>
            {onDismiss && (
              <button
                className="error-toast-dismiss"
                onClick={onDismiss}
                aria-label="Dismiss error"
              >
                ×
              </button>
            )}
          </div>
          {onRetry && (
            <button className="error-toast-retry" onClick={onRetry}>
              Try Again
            </button>
          )}
        </motion.div>
      </AnimatePresence>
    );
  }
  
  if (variant === 'page') {
    return (
      <motion.div
        className={`error-page ${className}`}
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        exit={{ opacity: 0 }}
      >
        <div className="error-page-content">
          <div className="error-page-icon">😔</div>
          <h2>Something went wrong</h2>
          <p>{friendlyMessage}</p>
          <div className="error-page-actions">
            {onRetry && (
              <button className="error-button primary" onClick={onRetry}>
                Try Again
              </button>
            )}
            <button 
              className="error-button secondary" 
              onClick={() => window.location.href = '/'}
            >
              Go Home
            </button>
          </div>
        </div>
      </motion.div>
    );
  }
  
  // Default inline variant
  return (
    <motion.div
      className={`error-inline ${className}`}
      initial={{ opacity: 0, height: 0 }}
      animate={{ opacity: 1, height: 'auto' }}
      exit={{ opacity: 0, height: 0 }}
      role="alert"
    >
      <div className="error-inline-content">
        <span className="error-inline-icon">⚠️</span>
        <span className="error-inline-message">{friendlyMessage}</span>
      </div>
      {onRetry && (
        <button className="error-inline-retry" onClick={onRetry}>
          Retry
        </button>
      )}
    </motion.div>
  );
};

// Error boundary component
interface ErrorBoundaryState {
  hasError: boolean;
  error: Error | null;
}

export class ErrorBoundary extends React.Component<
  { children: React.ReactNode; fallback?: React.ReactNode },
  ErrorBoundaryState
> {
  state: ErrorBoundaryState = {
    hasError: false,
    error: null
  };
  
  static getDerivedStateFromError(error: Error): ErrorBoundaryState {
    return { hasError: true, error };
  }
  
  componentDidCatch(error: Error, errorInfo: React.ErrorInfo) {
    // Log to error reporting service
    console.error('Error caught by boundary:', error, errorInfo);
    
    // Send to analytics if available
    if (typeof window !== 'undefined' && (window as any).gtag) {
      (window as any).gtag('event', 'exception', {
        description: error.toString(),
        fatal: false
      });
    }
  }
  
  handleReset = () => {
    this.setState({ hasError: false, error: null });
  };
  
  render() {
    if (this.state.hasError) {
      if (this.props.fallback) {
        return <>{this.props.fallback}</>;
      }
      
      return (
        <ErrorMessage
          error={this.state.error}
          variant="page"
          onRetry={this.handleReset}
        />
      );
    }
    
    return this.props.children;
  }
}