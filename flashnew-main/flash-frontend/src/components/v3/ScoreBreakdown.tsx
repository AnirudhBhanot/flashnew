import React from 'react';
import { motion } from 'framer-motion';
import './ScoreBreakdown.css';

interface BreakdownItem {
  name: string;
  weight: number;
  contribution: number;
  description?: string;
}

interface ScoreBreakdownProps {
  items: BreakdownItem[];
  totalScore: number;
}

export const ScoreBreakdown: React.FC<ScoreBreakdownProps> = ({ items, totalScore }) => {
  const getItemColor = (contribution: number) => {
    if (contribution >= 0.7) return 'var(--color-success)';
    if (contribution >= 0.5) return 'var(--color-primary)';
    if (contribution >= 0.3) return 'var(--color-warning)';
    return 'var(--color-danger)';
  };

  const formatName = (name: string) => {
    return name
      .replace(/_/g, ' ')
      .split(' ')
      .map(word => word.charAt(0).toUpperCase() + word.slice(1))
      .join(' ');
  };

  const sortedItems = [...items].sort((a, b) => b.contribution - a.contribution);

  return (
    <motion.div 
      className="score-breakdown"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.5, duration: 0.6 }}
    >
      <div className="breakdown-header">
        <h3>Score Breakdown</h3>
        <span className="breakdown-subtitle">How each model contributes to your {totalScore}% score</span>
      </div>

      <div className="breakdown-items">
        {sortedItems.map((item, index) => {
          const impact = item.weight * item.contribution * 100;
          const barWidth = (item.contribution * 100);
          
          return (
            <motion.div
              key={item.name}
              className="breakdown-item"
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.1 * index, duration: 0.4 }}
            >
              <div className="item-header">
                <div className="item-name-group">
                  <span className="item-name">{formatName(item.name)}</span>
                  <span className="item-weight">{(item.weight * 100).toFixed(0)}% weight</span>
                </div>
                <div className="item-score-group">
                  <span className="item-contribution" style={{ color: getItemColor(item.contribution) }}>
                    {(item.contribution * 100).toFixed(0)}%
                  </span>
                  <span className="item-impact">+{impact.toFixed(1)}pts</span>
                </div>
              </div>
              
              <div className="item-bar-container">
                <motion.div 
                  className="item-bar"
                  style={{ 
                    width: `${barWidth}%`,
                    backgroundColor: getItemColor(item.contribution)
                  }}
                  initial={{ width: 0 }}
                  animate={{ width: `${barWidth}%` }}
                  transition={{ 
                    delay: 0.3 + (0.1 * index), 
                    duration: 0.8,
                    ease: [0.34, 1.56, 0.64, 1]
                  }}
                />
                <div 
                  className="item-bar-background"
                  style={{ width: `${item.weight * 100}%` }}
                />
              </div>

              {item.description && (
                <p className="item-description">{item.description}</p>
              )}
            </motion.div>
          );
        })}
      </div>

      <motion.div 
        className="breakdown-summary"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.8, duration: 0.6 }}
      >
        <div className="summary-item">
          <span className="summary-label">Combined Score:</span>
          <span className="summary-value">{totalScore}%</span>
        </div>
        <div className="summary-explanation">
          <p>
            Each model analyzes different aspects of your startup. 
            The final score is a weighted combination of all model predictions.
          </p>
        </div>
      </motion.div>
    </motion.div>
  );
};