import React from 'react';
import { motion } from 'framer-motion';
import { Card } from '../ui/Card';
import './ScoreCardV17.css';

interface ScoreCardV17Props {
  score: number;
  verdict: string;
  confidence: number;
  message: string;
  stage: string;
}

export const ScoreCardV17: React.FC<ScoreCardV17Props> = ({
  score,
  verdict,
  confidence,
  message,
  stage
}) => {
  const getVerdictColor = () => {
    if (verdict === 'PASS') return 'var(--color-success)';
    if (verdict === 'MAYBE') return 'var(--color-warning)';
    return 'var(--color-error)';
  };

  const getConfidenceLevel = () => {
    if (confidence >= 0.8) return 'High';
    if (confidence >= 0.6) return 'Moderate';
    return 'Low';
  };

  const getScoreStatus = () => {
    if (score >= 65) return { label: 'Strong', color: 'var(--color-success)' };
    if (score >= 50) return { label: 'Promising', color: 'var(--color-warning)' };
    return { label: 'Needs Work', color: 'var(--color-error)' };
  };

  const scoreStatus = getScoreStatus();

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
    >
      <Card variant="bordered" className="score-card-v17">
        <div className="score-header">
          <h2>AI Assessment Results</h2>
          <div className="stage-badge">
            {stage} Stage Evaluation
          </div>
        </div>

        <div className="score-content">
          <div className="score-main">
            <motion.div 
              className="score-value"
              initial={{ scale: 0 }}
              animate={{ scale: 1 }}
              transition={{ delay: 0.2, type: "spring", stiffness: 200 }}
            >
              <span className="score-number">{Math.round(score)}</span>
              <span className="score-percent">%</span>
            </motion.div>
            
            <div className="score-label">Success Probability</div>
            
            <motion.div 
              className="score-status"
              style={{ color: scoreStatus.color }}
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.4 }}
            >
              {scoreStatus.label}
            </motion.div>
          </div>

          <div className="score-details">
            <motion.div 
              className="verdict-section"
              initial={{ x: -20, opacity: 0 }}
              animate={{ x: 0, opacity: 1 }}
              transition={{ delay: 0.3 }}
            >
              <div className="detail-label">Investment Verdict</div>
              <div 
                className="verdict-value"
                style={{ color: getVerdictColor() }}
              >
                {verdict}
              </div>
            </motion.div>

            <motion.div 
              className="confidence-section"
              initial={{ x: -20, opacity: 0 }}
              animate={{ x: 0, opacity: 1 }}
              transition={{ delay: 0.4 }}
            >
              <div className="detail-label">Model Confidence</div>
              <div className="confidence-value">
                <div className="confidence-bar">
                  <motion.div 
                    className="confidence-fill"
                    initial={{ width: 0 }}
                    animate={{ width: `${confidence * 100}%` }}
                    transition={{ delay: 0.6, duration: 0.8 }}
                    style={{
                      background: confidence >= 0.8 
                        ? 'var(--color-success)' 
                        : confidence >= 0.6 
                        ? 'var(--color-warning)' 
                        : 'var(--color-error)'
                    }}
                  />
                </div>
                <span className="confidence-text">{getConfidenceLevel()}</span>
              </div>
            </motion.div>
          </div>
        </div>

        <motion.div 
          className="score-message"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.5 }}
        >
          <p>{message}</p>
        </motion.div>

        <motion.div 
          className="score-footer"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.6 }}
        >
          <div className="insight-icon">
            <svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor">
              <circle cx="8" cy="8" r="8" opacity="0.2" />
              <circle cx="8" cy="8" r="3" />
            </svg>
          </div>
          <span>AI-powered analysis based on 4 specialized models</span>
        </motion.div>
      </Card>
    </motion.div>
  );
};