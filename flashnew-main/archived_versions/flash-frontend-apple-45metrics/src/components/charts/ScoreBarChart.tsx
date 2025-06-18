import React from 'react';
import { motion } from 'framer-motion';
import { Icon } from '../../design-system/components';
import styles from './ScoreBarChart.module.scss';

interface ScoreBarChartProps {
  scores: {
    name: string;
    value: number;
    icon?: string;
    description?: string;
  }[];
  maxValue?: number;
  showPercentage?: boolean;
}

export const ScoreBarChart: React.FC<ScoreBarChartProps> = ({
  scores,
  maxValue = 1,
  showPercentage = true
}) => {
  const getScoreColor = (value: number) => {
    if (value >= 0.8) return styles.excellent;
    if (value >= 0.6) return styles.good;
    if (value >= 0.4) return styles.fair;
    return styles.poor;
  };
  
  const getScoreLabel = (value: number) => {
    if (value >= 0.8) return 'Excellent';
    if (value >= 0.6) return 'Good';
    if (value >= 0.4) return 'Fair';
    return 'Needs Improvement';
  };
  
  return (
    <div className={styles.container}>
      {scores.map((score, index) => (
        <motion.div
          key={score.name}
          className={styles.scoreItem}
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: index * 0.1 }}
        >
          <div className={styles.header}>
            <div className={styles.titleGroup}>
              {score.icon && (
                <Icon name={score.icon} size={20} className={styles.icon} />
              )}
              <h4 className={styles.title}>{score.name}</h4>
            </div>
            <div className={styles.valueGroup}>
              <span className={`${styles.value} ${getScoreColor(score.value)}`}>
                {showPercentage ? `${Math.round(score.value * 100)}%` : score.value.toFixed(2)}
              </span>
              <span className={styles.label}>{getScoreLabel(score.value)}</span>
            </div>
          </div>
          
          <div className={styles.barContainer}>
            <div className={styles.barBackground}>
              <motion.div
                className={`${styles.barFill} ${getScoreColor(score.value)}`}
                initial={{ width: 0 }}
                animate={{ width: `${(score.value / maxValue) * 100}%` }}
                transition={{ 
                  duration: 1, 
                  delay: index * 0.1 + 0.3,
                  ease: [0.2, 0, 0, 1]
                }}
              />
            </div>
          </div>
          
          {score.description && (
            <p className={styles.description}>{score.description}</p>
          )}
        </motion.div>
      ))}
    </div>
  );
};