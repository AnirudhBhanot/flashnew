import React from 'react';
import { motion } from 'framer-motion';
import styles from './SuccessScoreMinimal.module.scss';

interface SuccessScoreMinimalProps {
  score: number;
  confidence?: string;
  companyName?: string;
}

export const SuccessScoreMinimal: React.FC<SuccessScoreMinimalProps> = ({ 
  score, 
  confidence = 'moderate',
  companyName 
}) => {
  const percentage = Math.round(score * 100);
  
  const getVerdict = () => {
    if (percentage >= 80) return 'Highly Recommended';
    if (percentage >= 60) return 'Recommended';
    if (percentage >= 40) return 'Conditional';
    return 'Not Recommended';
  };

  const getInsight = () => {
    if (percentage >= 80) return 'Exceptional potential for success';
    if (percentage >= 60) return 'Strong fundamentals with growth opportunity';
    if (percentage >= 40) return 'Moderate potential with key areas to address';
    return 'Significant challenges require attention';
  };

  return (
    <div className={styles.container}>
      {companyName && (
        <motion.h1 
          className={styles.companyName}
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
        >
          {companyName}
        </motion.h1>
      )}
      
      <motion.div
        className={styles.scoreContainer}
        initial={{ opacity: 0, scale: 0.9 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.8, delay: 0.2 }}
      >
        <div className={styles.percentageWrapper}>
          <span className={styles.percentage}>{percentage}</span>
          <span className={styles.percentSign}>%</span>
        </div>
        
        <div className={styles.label}>Success Probability</div>
      </motion.div>

      <motion.div
        className={styles.verdict}
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.6, delay: 0.4 }}
      >
        <div className={styles.verdictText}>{getVerdict()}</div>
        <div className={styles.insightText}>{getInsight()}</div>
      </motion.div>

      {confidence && (
        <motion.div
          className={styles.confidence}
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.6, delay: 0.6 }}
        >
          <span className={styles.confidenceLabel}>Confidence Level</span>
          <span className={styles.confidenceValue}>{confidence}</span>
        </motion.div>
      )}
    </div>
  );
};