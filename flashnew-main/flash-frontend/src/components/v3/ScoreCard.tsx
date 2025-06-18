import React, { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import './ScoreCard.css';

interface ScoreCardProps {
  score: number;
  verdict: string;
  confidence: string;
  message: string;
  stage?: string;
  isLoading?: boolean;
}

export const ScoreCard: React.FC<ScoreCardProps> = ({
  score,
  verdict,
  confidence,
  message,
  stage = 'seed',
  isLoading = false
}) => {
  const [displayScore, setDisplayScore] = useState(0);

  useEffect(() => {
    if (!isLoading) {
      // Animate score counting up
      const duration = 1500;
      const startTime = Date.now();
      const animate = () => {
        const now = Date.now();
        const progress = Math.min((now - startTime) / duration, 1);
        const easeOutQuart = 1 - Math.pow(1 - progress, 4);
        const currentScore = Math.round(score * easeOutQuart);
        setDisplayScore(currentScore);
        
        if (progress < 1) {
          requestAnimationFrame(animate);
        }
      };
      requestAnimationFrame(animate);
    }
  }, [score, isLoading]);

  const getScoreColor = () => {
    if (score >= 75) return '#FFFFFF';
    if (score >= 60) return '#E8EAED';
    if (score >= 40) return '#9CA3AF';
    return '#6B7280';
  };

  const getVerdictColor = () => {
    const verdictUpper = verdict.toUpperCase();
    if (verdictUpper === 'PASS' || verdictUpper === 'EXCEPTIONAL') return '#00ff88';
    if (verdictUpper === 'CONDITIONAL') return '#ffaa00';
    return '#ff4444';
  };

  if (isLoading) {
    return (
      <div className="score-card-v2 loading">
        <div className="loading-pulse">
          <div className="pulse-ring"></div>
          <div className="pulse-ring"></div>
          <div className="pulse-ring"></div>
        </div>
      </div>
    );
  }

  return (
    <motion.div 
      className="score-card-v2"
      initial={{ opacity: 0, scale: 0.9 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ duration: 0.5, ease: [0.16, 1, 0.3, 1] }}
    >
      {/* Background Effects */}
      <div className="card-background">
        <div className="gradient-orb gradient-orb-1"></div>
        <div className="gradient-orb gradient-orb-2"></div>
        <div className="grid-pattern"></div>
      </div>

      {/* Main Content */}
      <div className="card-content">
        {/* Header Section */}
        <motion.div 
          className="card-header"
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2, duration: 0.6 }}
        >
          <h2 className="assessment-title">AI Assessment Results</h2>
          <div className="stage-badge">
            <span>{stage} Stage</span>
          </div>
        </motion.div>

        {/* Score Section */}
        <motion.div 
          className="score-section"
          initial={{ opacity: 0, scale: 0.8 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.3, duration: 0.8, ease: [0.34, 1.56, 0.64, 1] }}
        >
          <div className="score-display">
            <svg className="score-svg" viewBox="0 0 200 200">
              {/* Background circle */}
              <circle
                cx="100"
                cy="100"
                r="90"
                fill="none"
                stroke="rgba(255, 255, 255, 0.05)"
                strokeWidth="12"
              />
              
              {/* Progress circle */}
              <motion.circle
                cx="100"
                cy="100"
                r="90"
                fill="none"
                stroke={getScoreColor()}
                strokeWidth="12"
                strokeLinecap="round"
                strokeDasharray={`${2 * Math.PI * 90}`}
                strokeDashoffset={`${2 * Math.PI * 90 * (1 - displayScore / 100)}`}
                transform="rotate(-90 100 100)"
                initial={{ strokeDashoffset: 2 * Math.PI * 90 }}
                animate={{ strokeDashoffset: 2 * Math.PI * 90 * (1 - displayScore / 100) }}
                transition={{ duration: 1.5, ease: "easeOut" }}
                style={{
                  filter: `drop-shadow(0 0 20px ${getScoreColor()})`
                }}
              />

              {/* Decorative elements */}
              <circle cx="100" cy="10" r="3" fill={getScoreColor()} opacity="0.6">
                <animate attributeName="opacity" values="0.6;1;0.6" dur="2s" repeatCount="indefinite" />
              </circle>
            </svg>

            <div className="score-content">
              <motion.div 
                className="score-number"
                key={displayScore}
                initial={{ scale: 0.5, opacity: 0 }}
                animate={{ scale: 1, opacity: 1 }}
                transition={{ duration: 0.3 }}
              >
                {displayScore}
              </motion.div>
              <div className="score-label">Success Score</div>
            </div>
          </div>

          {/* Metrics Grid */}
          <div className="metrics-grid">
            <motion.div 
              className="metric-item"
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.5, duration: 0.5 }}
            >
              <div className="metric-icon verdict-icon-wrapper">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
                  <path d="M9 11L12 14L22 4" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                  <path d="M21 12V19C21 20.1046 20.1046 21 19 21H5C3.89543 21 3 20.1046 3 19V5C3 3.89543 3.89543 3 5 3H16" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                </svg>
              </div>
              <div className="metric-info">
                <div className="metric-value" style={{ color: getVerdictColor() }}>
                  {verdict}
                </div>
                <div className="metric-label">Verdict</div>
              </div>
            </motion.div>

            <motion.div 
              className="metric-item"
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.6, duration: 0.5 }}
            >
              <div className="metric-icon confidence-icon-wrapper">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
                  <circle cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="2"/>
                  <path d="M12 6V12L16 16" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
                </svg>
              </div>
              <div className="metric-info">
                <div className="metric-value">{confidence}</div>
                <div className="metric-label">Confidence</div>
              </div>
            </motion.div>
          </div>
        </motion.div>

        {/* Message Section */}
        <motion.div 
          className="message-section"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.7, duration: 0.6 }}
        >
          <p className="assessment-message">{message}</p>
          
          <div className="action-buttons">
            <button className="action-btn primary">
              <span>View Detailed Analysis</span>
              <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                <path d="M6 12L10 8L6 4" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
              </svg>
            </button>
            <button className="action-btn secondary">
              <span>Download Report</span>
              <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                <path d="M8 2V10M8 10L5 7M8 10L11 7M3 14H13" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
              </svg>
            </button>
          </div>
        </motion.div>

        {/* Bottom Pattern */}
        <div className="bottom-pattern">
          <svg width="100%" height="60" viewBox="0 0 600 60" preserveAspectRatio="none">
            <path 
              d="M0,30 Q150,10 300,30 T600,30 L600,60 L0,60 Z" 
              fill="url(#gradient)" 
              opacity="0.1"
            />
            <defs>
              <linearGradient id="gradient" x1="0%" y1="0%" x2="100%" y2="0%">
                <stop offset="0%" stopColor={getScoreColor()} />
                <stop offset="100%" stopColor="transparent" />
              </linearGradient>
            </defs>
          </svg>
        </div>
      </div>
    </motion.div>
  );
};