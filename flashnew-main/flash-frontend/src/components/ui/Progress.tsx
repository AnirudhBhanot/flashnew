import React, { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import './Progress.css';

interface ProgressBarProps {
  value: number;
  max?: number;
  variant?: 'default' | 'success' | 'warning' | 'danger' | 'gradient';
  size?: 'small' | 'medium' | 'large';
  showLabel?: boolean;
  animated?: boolean;
  striped?: boolean;
  indeterminate?: boolean;
}

export const ProgressBar: React.FC<ProgressBarProps> = ({
  value,
  max = 100,
  variant = 'default',
  size = 'medium',
  showLabel = false,
  animated = true,
  striped = false,
  indeterminate = false
}) => {
  const [displayValue, setDisplayValue] = useState(0);
  const percentage = indeterminate ? 100 : (value / max) * 100;

  useEffect(() => {
    if (animated && !indeterminate) {
      const duration = 800;
      const startTime = Date.now();
      const animate = () => {
        const now = Date.now();
        const progress = Math.min((now - startTime) / duration, 1);
        const easeOutExpo = 1 - Math.pow(2, -10 * progress);
        const currentValue = percentage * easeOutExpo;
        setDisplayValue(currentValue);
        
        if (progress < 1) {
          requestAnimationFrame(animate);
        }
      };
      requestAnimationFrame(animate);
    } else {
      setDisplayValue(percentage);
    }
  }, [percentage, animated, indeterminate]);

  const progressClasses = [
    'progress',
    `progress-${size}`,
    striped && 'progress-striped',
    animated && striped && 'progress-animated'
  ].filter(Boolean).join(' ');

  const barClasses = [
    'progress-bar',
    `progress-bar-${variant}`,
    indeterminate && 'progress-bar-indeterminate'
  ].filter(Boolean).join(' ');

  return (
    <div className={progressClasses}>
      <motion.div
        className={barClasses}
        initial={{ width: 0 }}
        animate={{ width: `${displayValue}%` }}
        transition={{ duration: 0.8, ease: [0.16, 1, 0.3, 1] }}
      >
        {showLabel && !indeterminate && (
          <span className="progress-label">{Math.round(displayValue)}%</span>
        )}
      </motion.div>
    </div>
  );
};

interface CircularProgressProps {
  value: number;
  size?: number;
  strokeWidth?: number;
  variant?: 'default' | 'success' | 'warning' | 'danger';
  showLabel?: boolean;
  animated?: boolean;
}

export const CircularProgress: React.FC<CircularProgressProps> = ({
  value,
  size = 80,
  strokeWidth = 8,
  variant = 'default',
  showLabel = true,
  animated = true
}) => {
  const [displayValue, setDisplayValue] = useState(0);
  const radius = (size - strokeWidth) / 2;
  const circumference = radius * 2 * Math.PI;
  const offset = circumference - (displayValue / 100) * circumference;

  useEffect(() => {
    if (animated) {
      const duration = 1200;
      const startTime = Date.now();
      const animate = () => {
        const now = Date.now();
        const progress = Math.min((now - startTime) / duration, 1);
        const easeOutExpo = 1 - Math.pow(2, -10 * progress);
        const currentValue = value * easeOutExpo;
        setDisplayValue(currentValue);
        
        if (progress < 1) {
          requestAnimationFrame(animate);
        }
      };
      requestAnimationFrame(animate);
    } else {
      setDisplayValue(value);
    }
  }, [value, animated]);

  return (
    <div className="circular-progress" style={{ width: size, height: size }}>
      <svg width={size} height={size} className="circular-progress-svg">
        <circle
          className="circular-progress-bg"
          cx={size / 2}
          cy={size / 2}
          r={radius}
          strokeWidth={strokeWidth}
        />
        <motion.circle
          className={`circular-progress-bar circular-progress-bar-${variant}`}
          cx={size / 2}
          cy={size / 2}
          r={radius}
          strokeWidth={strokeWidth}
          strokeDasharray={circumference}
          initial={{ strokeDashoffset: circumference }}
          animate={{ strokeDashoffset: offset }}
          transition={{ duration: 1.2, ease: [0.16, 1, 0.3, 1] }}
        />
      </svg>
      {showLabel && (
        <motion.div 
          className="circular-progress-label"
          initial={{ scale: 0 }}
          animate={{ scale: 1 }}
          transition={{ delay: 0.5, duration: 0.3, type: "spring" }}
        >
          {Math.round(displayValue)}%
        </motion.div>
      )}
    </div>
  );
};

interface StepProgressProps {
  steps: string[];
  currentStep: number;
  variant?: 'default' | 'numbered';
}

export const StepProgress: React.FC<StepProgressProps> = ({
  steps,
  currentStep,
  variant = 'default'
}) => {
  return (
    <div className="step-progress">
      {steps.map((step, index) => {
        const isActive = index === currentStep;
        const isCompleted = index < currentStep;
        
        return (
          <React.Fragment key={index}>
            <motion.div
              className={`step ${isActive ? 'step-active' : ''} ${isCompleted ? 'step-completed' : ''}`}
              initial={{ scale: 0.8, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              transition={{ delay: index * 0.1 }}
            >
              <div className="step-indicator">
                {variant === 'numbered' ? (
                  <span className="step-number">{index + 1}</span>
                ) : (
                  isCompleted && <span className="step-check">✓</span>
                )}
              </div>
              <span className="step-label">{step}</span>
            </motion.div>
            {index < steps.length - 1 && (
              <div 
                className={`step-connector ${isCompleted ? 'step-connector-completed' : ''}`}
              />
            )}
          </React.Fragment>
        );
      })}
    </div>
  );
};

interface SkeletonProps {
  width?: string | number;
  height?: string | number;
  variant?: 'text' | 'rect' | 'circle';
  animation?: 'pulse' | 'wave';
}

export const Skeleton: React.FC<SkeletonProps> = ({
  width = '100%',
  height = 20,
  variant = 'rect',
  animation = 'pulse'
}) => {
  const skeletonClasses = [
    'skeleton',
    `skeleton-${variant}`,
    `skeleton-${animation}`
  ].join(' ');

  const style = {
    width: typeof width === 'number' ? `${width}px` : width,
    height: typeof height === 'number' ? `${height}px` : height,
  };

  return <div className={skeletonClasses} style={style} />;
};

interface LoadingDotsProps {
  size?: 'small' | 'medium' | 'large';
  color?: string;
}

export const LoadingDots: React.FC<LoadingDotsProps> = ({
  size = 'medium',
  color
}) => {
  return (
    <div className={`loading-dots loading-dots-${size}`}>
      {[0, 1, 2].map(index => (
        <motion.span
          key={index}
          className="loading-dot"
          style={{ backgroundColor: color }}
          animate={{
            y: [0, -10, 0],
            opacity: [0.5, 1, 0.5]
          }}
          transition={{
            duration: 1,
            repeat: Infinity,
            delay: index * 0.15,
            ease: "easeInOut"
          }}
        />
      ))}
    </div>
  );
};