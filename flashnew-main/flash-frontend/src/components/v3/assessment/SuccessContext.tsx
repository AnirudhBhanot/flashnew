import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { configService } from '../../../services/LegacyConfigService';
import { SUCCESS_COMPARISONS, EXIT_TIMEFRAMES, DNA_PATTERN_EXAMPLES } from '../../../config/constants';
import './SuccessContext.css';

interface SuccessContextProps {
  successProbability: number;
  verdict: string;
  confidenceInterval?: [number, number];
  strength?: string;
  fundingStage?: string;
}

const getVerdictDetails = (verdict: string) => {
  const verdictMap: Record<string, {
    icon: string;
    color: string;
    message: string;
    recommendation: string;
  }> = {
    'STRONG PASS': {
      icon: '🚀',
      color: '#00C851',
      message: 'Exceptional investment opportunity',
      recommendation: 'Move quickly - this startup shows all the indicators of a potential unicorn'
    },
    'PASS': {
      icon: '✅',
      color: '#00C851',
      message: 'Solid investment candidate',
      recommendation: 'Proceed with standard due diligence process'
    },
    'CONDITIONAL PASS': {
      icon: '⚡',
      color: '#FFD93D',
      message: 'Promising with caveats',
      recommendation: 'Worth pursuing if key concerns can be addressed'
    },
    'FAIL': {
      icon: '⚠️',
      color: '#FF8800',
      message: 'Not recommended at this time',
      recommendation: 'Significant improvements needed before investment consideration'
    },
    'STRONG FAIL': {
      icon: '🔴',
      color: '#FF4444',
      message: 'High risk investment',
      recommendation: 'Fundamental issues make this investment unsuitable'
    }
  };

  return verdictMap[verdict] || verdictMap['FAIL'];
};

const getSuccessContext = (probability: number, stage?: string, config?: any) => {
  const comparisons = config?.successComparisons || SUCCESS_COMPARISONS;
  const exitTimeframes = config?.exitTimeframes || EXIT_TIMEFRAMES;
  const dnaExamples = config?.dnaPatternExamples || DNA_PATTERN_EXAMPLES;
  
  if (probability >= 0.80) {
    return {
      comparison: comparisons.top_5?.comparison || 'Top 5% of startups',
      similar: dnaExamples?.slice(0, 2) || ['Stripe at Series A', 'Airbnb at Series B'],
      likelihood: comparisons.top_5?.likelihood || 'Very likely to achieve 10x+ returns',
      timeframe: exitTimeframes.high?.timeframe || '3-5 years to major exit'
    };
  } else if (probability >= 0.65) {
    return {
      comparison: comparisons.top_10?.comparison || 'Top 10% of startups',
      similar: ['Notion at Seed', 'Figma at Series A'],
      likelihood: comparisons.top_10?.likelihood || 'Likely to achieve 5-10x returns',
      timeframe: exitTimeframes.medium_high?.timeframe || '4-6 years to exit'
    };
  } else if (probability >= 0.50) {
    return {
      comparison: comparisons.top_25?.comparison || 'Top 25% of startups',
      similar: ['Typical Series A SaaS companies'],
      likelihood: comparisons.top_25?.likelihood || 'Good chance of 3-5x returns',
      timeframe: exitTimeframes.medium?.timeframe || '5-7 years to exit'
    };
  } else {
    return {
      comparison: comparisons.average?.comparison || 'Average startup',
      similar: ['Early stage with significant challenges'],
      likelihood: comparisons.average?.likelihood || 'Modest returns expected',
      timeframe: exitTimeframes.low?.timeframe || '7+ years to potential exit'
    };
  }
};

const getConfidenceExplanation = (interval?: [number, number]) => {
  if (!interval) return 'Moderate confidence in prediction';
  
  const range = interval[1] - interval[0];
  if (range <= 0.1) {
    return 'High confidence - all indicators align';
  } else if (range <= 0.15) {
    return 'Good confidence - most factors agree';
  } else if (range <= 0.2) {
    return 'Moderate confidence - some uncertainty';
  } else {
    return 'Lower confidence - mixed signals';
  }
};

export const SuccessContext: React.FC<SuccessContextProps> = ({
  successProbability,
  verdict,
  confidenceInterval,
  strength,
  fundingStage
}) => {
  const [config, setConfig] = useState<any>(null);

  useEffect(() => {
    configService.getAllConfig().then(setConfig);
  }, []);

  const verdictDetails = getVerdictDetails(verdict);
  const successContext = getSuccessContext(successProbability, fundingStage, config);
  const confidenceExplanation = getConfidenceExplanation(confidenceInterval);

  return (
    <div className="success-context-container">
      <div className="verdict-section">
        <motion.div 
          className="verdict-badge"
          initial={{ scale: 0 }}
          animate={{ scale: 1 }}
          transition={{ type: "spring", stiffness: 200 }}
          style={{ borderColor: verdictDetails.color }}
        >
          <span className="verdict-icon">{verdictDetails.icon}</span>
          <h2 className="verdict-text" style={{ color: verdictDetails.color }}>
            {verdict}
          </h2>
        </motion.div>
        <p className="verdict-message">{verdictDetails.message}</p>
      </div>

      <div className="probability-section">
        <div className="probability-main">
          <motion.div 
            className="probability-circle"
            initial={{ scale: 0 }}
            animate={{ scale: 1 }}
            transition={{ delay: 0.2, type: "spring" }}
          >
            <svg viewBox="0 0 200 200">
              <circle
                cx="100"
                cy="100"
                r="90"
                fill="none"
                stroke="rgba(255, 255, 255, 0.1)"
                strokeWidth="10"
              />
              <motion.circle
                cx="100"
                cy="100"
                r="90"
                fill="none"
                stroke={successProbability >= 0.7 ? '#00C851' : successProbability >= 0.5 ? '#FFD93D' : '#FF8800'}
                strokeWidth="10"
                strokeLinecap="round"
                strokeDasharray={`${2 * Math.PI * 90}`}
                strokeDashoffset={`${2 * Math.PI * 90 * (1 - successProbability)}`}
                transform="rotate(-90 100 100)"
                initial={{ strokeDashoffset: `${2 * Math.PI * 90}` }}
                animate={{ strokeDashoffset: `${2 * Math.PI * 90 * (1 - successProbability)}` }}
                transition={{ duration: 1.5, ease: "easeOut" }}
              />
            </svg>
            <div className="probability-value">
              <span className="value">{Math.round(successProbability * 100)}</span>
              <span className="percent">%</span>
            </div>
          </motion.div>
          <div className="probability-details">
            <h3>Success Probability</h3>
            <p className="comparison">{successContext.comparison}</p>
            {confidenceInterval && (
              <div className="confidence-range">
                <span className="range-label">Range:</span>
                <span className="range-values">
                  {Math.round(confidenceInterval[0] * 100)}% - {Math.round(confidenceInterval[1] * 100)}%
                </span>
              </div>
            )}
            <p className="confidence-explanation">{confidenceExplanation}</p>
          </div>
        </div>
      </div>

      <div className="context-grid">
        <motion.div 
          className="context-card"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
        >
          <h4>📊 Similar Success Stories</h4>
          <ul>
            {successContext.similar.map((company: string, index: number) => (
              <li key={index}>{company}</li>
            ))}
          </ul>
        </motion.div>

        <motion.div 
          className="context-card"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4 }}
        >
          <h4>💰 Return Potential</h4>
          <p>{successContext.likelihood}</p>
          <p className="timeframe">{successContext.timeframe}</p>
        </motion.div>
      </div>

      <motion.div 
        className="recommendation-box"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.5 }}
        style={{ borderColor: verdictDetails.color }}
      >
        <span className="recommendation-icon">💡</span>
        <div>
          <h4>Investment Recommendation</h4>
          <p>{verdictDetails.recommendation}</p>
        </div>
      </motion.div>
    </div>
  );
};