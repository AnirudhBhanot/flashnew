import React from 'react';
import { motion } from 'framer-motion';
import './Card.css';

interface CardProps {
  children: React.ReactNode;
  className?: string;
  variant?: 'default' | 'elevated' | 'bordered' | 'gradient';
  interactive?: boolean;
  delay?: number;
  onClick?: () => void;
}

export const Card: React.FC<CardProps> = ({
  children,
  className = '',
  variant = 'default',
  interactive = false,
  delay = 0,
  onClick
}) => {
  const variants = {
    hidden: { 
      opacity: 0, 
      y: 20,
      scale: 0.95
    },
    visible: { 
      opacity: 1, 
      y: 0,
      scale: 1,
      transition: {
        duration: 0.5,
        delay,
        ease: [0.16, 1, 0.3, 1]
      }
    }
  };

  const hoverVariants = interactive ? {
    hover: {
      y: -4,
      scale: 1.02,
      transition: {
        duration: 0.3,
        ease: [0.16, 1, 0.3, 1]
      }
    }
  } : {};

  const cardClasses = [
    'card',
    `card-${variant}`,
    interactive && 'card-interactive',
    className
  ].filter(Boolean).join(' ');

  return (
    <motion.div
      className={cardClasses}
      variants={variants}
      initial="hidden"
      animate="visible"
      whileHover={interactive ? "hover" : undefined}
      whileTap={interactive ? { scale: 0.98 } : undefined}
      onClick={onClick}
    >
      {children}
    </motion.div>
  );
};

interface CardHeaderProps {
  children: React.ReactNode;
  icon?: React.ReactNode;
  action?: React.ReactNode;
}

export const CardHeader: React.FC<CardHeaderProps> = ({ children, icon, action }) => {
  return (
    <div className="card-header">
      <div className="card-header-content">
        {icon && <span className="card-header-icon">{icon}</span>}
        {children}
      </div>
      {action && <div className="card-header-action">{action}</div>}
    </div>
  );
};

interface CardBodyProps {
  children: React.ReactNode;
  padded?: boolean;
}

export const CardBody: React.FC<CardBodyProps> = ({ children, padded = true }) => {
  return (
    <div className={`card-body ${padded ? 'card-body-padded' : ''}`}>
      {children}
    </div>
  );
};

interface CardFooterProps {
  children: React.ReactNode;
  transparent?: boolean;
}

export const CardFooter: React.FC<CardFooterProps> = ({ children, transparent = false }) => {
  return (
    <div className={`card-footer ${transparent ? 'card-footer-transparent' : ''}`}>
      {children}
    </div>
  );
};

// Animated Card Group for staggered animations
interface CardGroupProps {
  children: React.ReactNode;
  stagger?: number;
}

export const CardGroup: React.FC<CardGroupProps> = ({ children, stagger = 0.1 }) => {
  return (
    <motion.div
      className="card-group"
      initial="hidden"
      animate="visible"
      variants={{
        visible: {
          transition: {
            staggerChildren: stagger
          }
        }
      }}
    >
      {children}
    </motion.div>
  );
};