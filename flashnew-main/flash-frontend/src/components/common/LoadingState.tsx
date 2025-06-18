import React from 'react';
import { motion } from 'framer-motion';
import './LoadingState.css';

interface LoadingStateProps {
  stage?: 'initializing' | 'analyzing' | 'preparing-results' | 'loading';
  progress?: number;
  message?: string;
  variant?: 'default' | 'inline' | 'overlay';
}

export const LoadingState: React.FC<LoadingStateProps> = ({ 
  stage = 'loading',
  progress,
  message,
  variant = 'default'
}) => {
  const messages = {
    'initializing': 'Preparing analysis models...',
    'analyzing': 'Analyzing startup metrics...',
    'preparing-results': 'Generating insights...',
    'loading': message || 'Loading...'
  };
  
  const displayMessage = messages[stage];
  
  // Simple DNA Helix Animation
  const DNAHelix: React.FC<{ progress?: number }> = ({ progress }) => (
    <div className="dna-helix-container">
      <motion.div
        className="dna-helix"
        animate={{ rotate: 360 }}
        transition={{ duration: 4, repeat: Infinity, ease: "linear" }}
      >
        {[...Array(8)].map((_, i) => (
          <div key={i} className="dna-pair" style={{ top: `${i * 12.5}%` }}>
            <div className="dna-node dna-node-left" />
            <div className="dna-connection" />
            <div className="dna-node dna-node-right" />
          </div>
        ))}
      </motion.div>
      {progress !== undefined && (
        <div className="dna-progress" style={{ height: `${progress}%` }} />
      )}
    </div>
  );
  
  if (variant === 'inline') {
    return (
      <motion.div 
        className="loading-state loading-state--inline"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        exit={{ opacity: 0 }}
      >
        <div className="loading-spinner" />
        <span className="loading-text">{displayMessage}</span>
      </motion.div>
    );
  }
  
  if (variant === 'overlay') {
    return (
      <motion.div 
        className="loading-state loading-state--overlay"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        exit={{ opacity: 0 }}
      >
        <div className="loading-overlay-content">
          <DNAHelix progress={progress} />
          <p className="loading-message">{displayMessage}</p>
          {progress !== undefined && (
            <div className="loading-progress">
              <div className="progress-track">
                <motion.div 
                  className="progress-fill"
                  initial={{ width: 0 }}
                  animate={{ width: `${progress}%` }}
                  transition={{ ease: "easeOut" }}
                />
              </div>
              <span className="progress-text">{Math.round(progress)}%</span>
            </div>
          )}
        </div>
      </motion.div>
    );
  }
  
  return (
    <motion.div 
      className="loading-state loading-state--default"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      role="status"
      aria-live="polite"
    >
      <div className="loading-animation">
        <DNAHelix progress={progress} />
      </div>
      
      <div className="loading-content">
        <h2>Analyzing with Realistic AI Models</h2>
        <p>{displayMessage}</p>
        
        {progress !== undefined && (
          <div className="progress-bar">
            <div 
              className="progress-fill"
              style={{ width: `${progress}%` }}
              role="progressbar"
              aria-valuenow={progress}
              aria-valuemin={0}
              aria-valuemax={100}
            />
          </div>
        )}
        
        <div className="loading-stats">
          <span>4 AI Models</span>
          <span>•</span>
          <span>100K Training Data</span>
          <span>•</span>
          <span>Honest Assessment</span>
        </div>
      </div>
    </motion.div>
  );
};

// Loading spinner component for buttons
export const ButtonLoader: React.FC = () => (
  <div className="button-loader">
    <div className="button-loader-dot" />
    <div className="button-loader-dot" />
    <div className="button-loader-dot" />
  </div>
);

// Skeleton loader for content
interface SkeletonProps {
  width?: string | number;
  height?: string | number;
  variant?: 'text' | 'rect' | 'circle';
  className?: string;
}

export const Skeleton: React.FC<SkeletonProps> = ({ 
  width = '100%', 
  height = 20, 
  variant = 'rect',
  className = ''
}) => {
  const variantClasses = {
    text: 'skeleton--text',
    rect: 'skeleton--rect',
    circle: 'skeleton--circle'
  };
  
  return (
    <div 
      className={`skeleton ${variantClasses[variant]} ${className}`}
      style={{ width, height }}
    >
      <div className="skeleton-shimmer" />
    </div>
  );
};