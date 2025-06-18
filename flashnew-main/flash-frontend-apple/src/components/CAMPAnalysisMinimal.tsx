import React from 'react';
import { motion } from 'framer-motion';
import styles from './CAMPAnalysisMinimal.module.scss';

interface CAMPAnalysisMinimalProps {
  scores: {
    capital: number;
    advantage: number;
    market: number;
    people: number;
  };
}

export const CAMPAnalysisMinimal: React.FC<CAMPAnalysisMinimalProps> = ({ scores }) => {
  const campItems = [
    {
      key: 'capital',
      label: 'Capital',
      description: 'Financial health & efficiency',
      value: scores.capital || 0
    },
    {
      key: 'advantage',
      label: 'Advantage',
      description: 'Competitive differentiation',
      value: scores.advantage || 0
    },
    {
      key: 'market',
      label: 'Market',
      description: 'Size & growth potential',
      value: scores.market || 0
    },
    {
      key: 'people',
      label: 'People',
      description: 'Team & execution capability',
      value: scores.people || 0
    }
  ];

  const getScoreQuality = (score: number) => {
    if (score >= 0.8) return 'Excellent';
    if (score >= 0.6) return 'Good';
    if (score >= 0.4) return 'Fair';
    return 'Needs Work';
  };

  return (
    <div className={styles.container}>
      <div className={styles.items}>
        {campItems.map((item, index) => {
          const percentage = Math.round(item.value * 100);
          const quality = getScoreQuality(item.value);
          
          return (
            <motion.div
              key={item.key}
              className={styles.item}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: index * 0.1 }}
            >
              <div className={styles.header}>
                <div className={styles.titleGroup}>
                  <h3 className={styles.title}>{item.label}</h3>
                  <p className={styles.description}>{item.description}</p>
                </div>
                <div className={styles.scoreGroup}>
                  <span className={styles.percentage}>{percentage}%</span>
                  <span className={styles.quality}>{quality}</span>
                </div>
              </div>
              
              <div className={styles.barContainer}>
                <motion.div
                  className={styles.bar}
                  initial={{ width: 0 }}
                  animate={{ width: `${percentage}%` }}
                  transition={{ 
                    duration: 1, 
                    delay: 0.3 + index * 0.1,
                    ease: [0.25, 0, 0, 1]
                  }}
                  style={{
                    opacity: 0.8 + (item.value * 0.2),
                  }}
                />
              </div>
            </motion.div>
          );
        })}
      </div>

      {/* Summary insight */}
      <motion.div
        className={styles.summary}
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.6, delay: 0.6 }}
      >
        <p className={styles.summaryText}>
          {scores.capital >= 0.7 && scores.people >= 0.7 
            ? 'Strong fundamentals with experienced team'
            : scores.market >= 0.7 && scores.advantage >= 0.7
            ? 'Excellent market opportunity with clear differentiation'
            : scores.capital < 0.5 || scores.people < 0.5
            ? 'Focus on strengthening core fundamentals'
            : 'Balanced profile with room for optimization'
          }
        </p>
      </motion.div>
    </div>
  );
};