import React from 'react';
import { motion } from 'framer-motion';
import './ConfidenceVisualization.css';

interface ConfidenceVisualizationProps {
  successProbability: number;
  confidenceInterval?: {
    lower: number;
    upper: number;
  };
  modelConfidence?: number;
  riskLevel: string;
  verdict: string;
  scoreLabel?: string; // Optional custom label for the score
}

export const ConfidenceVisualization: React.FC<ConfidenceVisualizationProps> = ({
  successProbability,
  confidenceInterval,
  modelConfidence,
  riskLevel,
  verdict,
  scoreLabel = 'Success Probability' // Default to 'Success Probability'
}) => {
  const percentage = Math.round(successProbability * 100);
  const confidence = modelConfidence || (confidenceInterval ? 
    1 - (confidenceInterval.upper - confidenceInterval.lower) : 0.85);
  
  const getVerdictColor = () => {
    switch (verdict) {
      case 'PASS':
      case 'STRONG PASS':
        return '#00C896';
      case 'CONDITIONAL PASS':
        return '#FF9500';
      case 'FAIL':
      case 'STRONG FAIL':
        return '#FF3B30';
      default:
        return '#007AFF';
    }
  };

  const getRiskColor = () => {
    if (riskLevel.includes('Low')) return '#00C896';
    if (riskLevel.includes('Medium-Low')) return '#52C41A';
    if (riskLevel.includes('Medium-High')) return '#FF9500';
    if (riskLevel.includes('High')) return '#FF3B30';
    return '#FFA500';
  };

  const confidencePercentage = Math.round(confidence * 100);

  return (
    <div className="confidence-viz">
      {/* Main Score Display */}
      <div className="score-section">
        <div className="score-circle">
          <svg viewBox="0 0 200 200" className="score-svg">
            {/* Background circle */}
            <circle
              cx="100"
              cy="100"
              r="90"
              fill="none"
              stroke="rgba(255, 255, 255, 0.1)"
              strokeWidth="12"
            />
            
            {/* Confidence interval arc (if available) */}
            {confidenceInterval && (
              <motion.path
                d={describeArc(100, 100, 90, 
                  confidenceInterval.lower * 360, 
                  confidenceInterval.upper * 360)}
                fill="none"
                stroke="rgba(255, 255, 255, 0.2)"
                strokeWidth="24"
                initial={{ pathLength: 0 }}
                animate={{ pathLength: 1 }}
                transition={{ duration: 1, ease: "easeOut" }}
              />
            )}
            
            {/* Success probability arc */}
            <motion.circle
              cx="100"
              cy="100"
              r="90"
              fill="none"
              stroke={getVerdictColor()}
              strokeWidth="12"
              strokeLinecap="round"
              strokeDasharray={`${successProbability * 565.48} 565.48`}
              transform="rotate(-90 100 100)"
              initial={{ strokeDasharray: "0 565.48" }}
              animate={{ strokeDasharray: `${successProbability * 565.48} 565.48` }}
              transition={{ duration: 1.5, ease: "easeOut" }}
            />
          </svg>
          
          <div className="score-content">
            <motion.div 
              className="score-percentage"
              initial={{ opacity: 0, scale: 0.5 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ delay: 0.5, duration: 0.5 }}
            >
              {percentage}%
            </motion.div>
            <div className="score-label">{scoreLabel}</div>
          </div>
        </div>
      </div>

      {/* Confidence & Risk Indicators */}
      <div className="confidence-details">
        <motion.div 
          className="confidence-card"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.7 }}
        >
          <div className="card-header">
            <span className="card-icon">🛡️</span>
            <span className="card-title">Model Confidence</span>
          </div>
          <div className="confidence-bar">
            <motion.div 
              className="confidence-fill"
              style={{ backgroundColor: confidencePercentage > 80 ? '#00C896' : '#FF9500' }}
              initial={{ width: 0 }}
              animate={{ width: `${confidencePercentage}%` }}
              transition={{ duration: 1, delay: 0.9 }}
            />
          </div>
          <div className="confidence-value">{confidencePercentage}% certain</div>
        </motion.div>

        <motion.div 
          className="risk-card"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.8 }}
        >
          <div className="card-header">
            <span className="card-icon">⚡</span>
            <span className="card-title">Risk Assessment</span>
          </div>
          <div 
            className="risk-level"
            style={{ color: getRiskColor() }}
          >
            {riskLevel}
          </div>
        </motion.div>

        <motion.div 
          className="verdict-card"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.9 }}
        >
          <div className="card-header">
            <span className="card-icon">🎯</span>
            <span className="card-title">Investment Verdict</span>
          </div>
          <div 
            className="verdict-text"
            style={{ color: getVerdictColor() }}
          >
            {verdict}
          </div>
        </motion.div>
      </div>

      {/* Confidence Interval Visualization */}
      {confidenceInterval && (
        <motion.div 
          className="interval-section"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 1 }}
        >
          <div className="interval-label">Confidence Interval</div>
          <div className="interval-bar">
            <div 
              className="interval-range"
              style={{
                left: `${confidenceInterval.lower * 100}%`,
                width: `${(confidenceInterval.upper - confidenceInterval.lower) * 100}%`
              }}
            >
              <span className="interval-lower">{Math.round(confidenceInterval.lower * 100)}%</span>
              <span className="interval-upper">{Math.round(confidenceInterval.upper * 100)}%</span>
            </div>
            <div 
              className="interval-marker"
              style={{ left: `${successProbability * 100}%` }}
            />
          </div>
        </motion.div>
      )}
    </div>
  );
};

// Helper function to create SVG arc path
function describeArc(x: number, y: number, radius: number, startAngle: number, endAngle: number) {
  const start = polarToCartesian(x, y, radius, endAngle);
  const end = polarToCartesian(x, y, radius, startAngle);
  const largeArcFlag = endAngle - startAngle <= 180 ? "0" : "1";
  
  return [
    "M", start.x, start.y, 
    "A", radius, radius, 0, largeArcFlag, 0, end.x, end.y
  ].join(" ");
}

function polarToCartesian(centerX: number, centerY: number, radius: number, angleInDegrees: number) {
  const angleInRadians = (angleInDegrees - 90) * Math.PI / 180.0;
  return {
    x: centerX + (radius * Math.cos(angleInRadians)),
    y: centerY + (radius * Math.sin(angleInRadians))
  };
}