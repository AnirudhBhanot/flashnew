import React from 'react';
import { motion } from 'framer-motion';
import './ScoreComparison.css';

interface ScoreComparisonProps {
  score: number;
  stage: string;
  percentileData?: {
    p10: number;
    p25: number;
    p50: number;
    p75: number;
    p90: number;
  };
}

export const ScoreComparison: React.FC<ScoreComparisonProps> = ({ 
  score, 
  stage,
  percentileData = {
    p10: 35,
    p25: 45,
    p50: 55,
    p75: 65,
    p90: 75
  }
}) => {
  const getPercentile = (score: number) => {
    if (score >= percentileData.p90) return 90;
    if (score >= percentileData.p75) return 75;
    if (score >= percentileData.p50) return 50;
    if (score >= percentileData.p25) return 25;
    if (score >= percentileData.p10) return 10;
    return 5;
  };

  const percentile = getPercentile(score);
  
  const segments = [
    { 
      label: 'Significant improvements needed', 
      range: '0-45%', 
      color: 'var(--color-danger)',
      description: 'Needs major work across multiple areas'
    },
    { 
      label: 'Moderate adjustments required', 
      range: '45-55%', 
      color: 'var(--color-warning)',
      description: 'Shows promise but requires attention'
    },
    { 
      label: 'Above average performance', 
      range: '55-65%', 
      color: 'var(--color-primary)',
      description: 'Strong fundamentals with room to grow'
    },
    { 
      label: 'Exceptional', 
      range: '65-75%', 
      color: 'var(--color-success)',
      description: 'Excellent fundamentals'
    },
    { 
      label: 'Exceptional', 
      range: '75%+', 
      color: 'var(--color-success)',
      description: 'Top tier performance'
    }
  ];

  const getSegmentIndex = (score: number) => {
    if (score < 45) return 0;
    if (score < 55) return 1;
    if (score < 65) return 2;
    if (score < 75) return 3;
    return 4;
  };

  const currentSegment = segments[getSegmentIndex(score)];
  const scorePosition = Math.min(Math.max(score, 0), 100);

  return (
    <motion.div 
      className="score-comparison"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.4, duration: 0.6 }}
    >
      <div className="comparison-header">
        <h3>How Your Score Compares</h3>
        <span className="info-icon" title="Based on our database of similar startups">ⓘ</span>
      </div>

      {/* Distribution Curve Visualization */}
      <div className="distribution-container">
        <svg viewBox="0 0 400 200" className="distribution-svg">
          {/* Background gradient */}
          <defs>
            <linearGradient id="curveGradient" x1="0%" y1="0%" x2="100%" y2="0%">
              <stop offset="0%" stopColor="var(--color-danger)" stopOpacity="0.2" />
              <stop offset="45%" stopColor="var(--color-warning)" stopOpacity="0.2" />
              <stop offset="65%" stopColor="var(--color-primary)" stopOpacity="0.2" />
              <stop offset="100%" stopColor="var(--color-success)" stopOpacity="0.2" />
            </linearGradient>
          </defs>

          {/* Bell curve path */}
          <motion.path
            d="M 20,180 Q 100,20 200,20 T 380,180"
            fill="url(#curveGradient)"
            stroke="var(--color-border-primary)"
            strokeWidth="2"
            initial={{ pathLength: 0, opacity: 0 }}
            animate={{ pathLength: 1, opacity: 1 }}
            transition={{ duration: 1.5, ease: "easeOut" }}
          />

          {/* Percentile markers */}
          {Object.entries(percentileData).map(([key, value], index) => (
            <g key={key}>
              <line
                x1={value * 4}
                y1="180"
                x2={value * 4}
                y2="170"
                stroke="var(--color-text-tertiary)"
                strokeWidth="1"
              />
              <text
                x={value * 4}
                y="195"
                textAnchor="middle"
                fill="var(--color-text-tertiary)"
                fontSize="10"
              >
                {key.replace('p', '')}%
              </text>
            </g>
          ))}

          {/* Your position marker */}
          <motion.g
            initial={{ y: -50, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ delay: 0.8, duration: 0.6, ease: [0.34, 1.56, 0.64, 1] }}
          >
            <line
              x1={scorePosition * 4}
              y1="0"
              x2={scorePosition * 4}
              y2="180"
              stroke={currentSegment.color}
              strokeWidth="2"
              strokeDasharray="4 2"
            />
            <circle
              cx={scorePosition * 4}
              cy="100"
              r="6"
              fill={currentSegment.color}
            />
            <text
              x={scorePosition * 4}
              y="30"
              textAnchor="middle"
              fill={currentSegment.color}
              fontSize="14"
              fontWeight="600"
            >
              You
            </text>
          </motion.g>
        </svg>

        {/* Score segments */}
        <div className="score-segments">
          {segments.map((segment, index) => (
            <motion.div
              key={index}
              className={`segment ${getSegmentIndex(score) === index ? 'active' : ''}`}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.1 * index, duration: 0.4 }}
            >
              <div className="segment-header">
                <span className="segment-label">{segment.label}</span>
                <span className="segment-range">{segment.range}</span>
              </div>
              <div className="segment-bar" style={{ backgroundColor: segment.color }} />
            </motion.div>
          ))}
        </div>
      </div>

      {/* Context Information */}
      <motion.div 
        className="comparison-context"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 1, duration: 0.6 }}
      >
        <div className="context-item">
          <span className="context-label">Your Percentile:</span>
          <span className="context-value" style={{ color: currentSegment.color }}>
            Top {100 - percentile}%
          </span>
        </div>
        <div className="context-item">
          <span className="context-label">Assessment for:</span>
          <span className="context-value">{stage} Stage</span>
        </div>
        <div className="context-item full-width">
          <p className="context-description">{currentSegment.description}</p>
        </div>
      </motion.div>
    </motion.div>
  );
};