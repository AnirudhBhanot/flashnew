import React from 'react';
import { motion } from 'framer-motion';
import { useSuccessThresholds, useAnimationConfig, useNumberFormatter } from '../../hooks/useConfiguration';
import './DynamicPredictionDisplay.css';

interface PredictionResult {
  success_probability: number;
  confidence_interval: {
    lower: number;
    upper: number;
    width: number;
  };
  verdict: string;
  verdict_confidence: string;
  uncertainty_level: string;
  factors: Array<{
    factor: string;
    impact: 'positive' | 'negative';
    strength: string;
    description: string;
  }>;
  warnings?: string[];
}

interface Props {
  result: PredictionResult;
  onScenarioClick: () => void;
}

export const DynamicPredictionDisplay: React.FC<Props> = ({ result, onScenarioClick }) => {
  // Configuration hooks
  const successThresholds = useSuccessThresholds();
  const animationConfig = useAnimationConfig();
  const numberFormatter = useNumberFormatter();
  
  const probabilityPercent = Math.round(result.success_probability * 100);
  const lowerPercent = Math.round(result.confidence_interval.lower * 100);
  const upperPercent = Math.round(result.confidence_interval.upper * 100);
  
  // Dynamic color based on probability
  const color = successThresholds.getColor(result.success_probability);
  
  // Verdict styling
  const getVerdictClass = (verdict: string) => {
    const level = successThresholds.getLevel(result.success_probability);
    return `verdict-${level}`;
  };

  return (
    <div className="dynamic-prediction-display">
      {/* Main Probability Display */}
      <motion.div 
        className="probability-section"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: animationConfig.getDuration() / 1000 }}
      >
        <h2>Success Probability</h2>
        
        <div className="probability-main">
          <motion.div 
            className="probability-circle"
            style={{ borderColor: color }}
            initial={{ scale: 0 }}
            animate={{ scale: 1 }}
            transition={{ type: animationConfig.getType(), ...animationConfig.getSpring() }}
          >
            <motion.span 
              className="probability-value"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: animationConfig.getDelay(0.3) / 1000 }}
            >
              {numberFormatter.formatPercentage(result.success_probability, 0)}
            </motion.span>
          </motion.div>
          
          <div className="confidence-interval">
            <div className="interval-bar">
              <div 
                className="interval-range"
                style={{
                  left: `${lowerPercent}%`,
                  width: `${upperPercent - lowerPercent}%`,
                  backgroundColor: color + '40'
                }}
              />
              <div 
                className="interval-point"
                style={{
                  left: `${probabilityPercent}%`,
                  backgroundColor: color
                }}
              />
            </div>
            <div className="interval-labels">
              <span>0%</span>
              <span className="interval-text">
                {numberFormatter.formatPercentage(result.confidence_interval.lower, 0)} - {numberFormatter.formatPercentage(result.confidence_interval.upper, 0)} confidence interval
              </span>
              <span>100%</span>
            </div>
          </div>
        </div>
        
        <div className="confidence-meta">
          <div className="confidence-level">
            <span className="label">Confidence:</span>
            <span className={`value ${result.verdict_confidence.toLowerCase()}`}>
              {result.verdict_confidence}
            </span>
          </div>
          <div className="uncertainty-level">
            <span className="label">Uncertainty:</span>
            <span className={`value ${result.uncertainty_level}`}>
              {result.uncertainty_level.replace('_', ' ')}
            </span>
          </div>
        </div>
      </motion.div>

      {/* Verdict Section */}
      <motion.div 
        className="verdict-section"
        initial={{ opacity: 0, x: -20 }}
        animate={{ opacity: 1, x: 0 }}
        transition={{ delay: animationConfig.getDelay(0.2) / 1000, duration: animationConfig.getDuration() / 1000 }}
      >
        <h3>Investment Recommendation</h3>
        <div className={`verdict-display ${getVerdictClass(result.verdict)}`}>
          <span className="verdict-text">{result.verdict}</span>
          <span className="verdict-confidence">({result.verdict_confidence} confidence)</span>
        </div>
      </motion.div>

      {/* Key Factors */}
      <motion.div 
        className="factors-section"
        initial={{ opacity: 0, x: 20 }}
        animate={{ opacity: 1, x: 0 }}
        transition={{ delay: animationConfig.getDelay(0.4) / 1000, duration: animationConfig.getDuration() / 1000 }}
      >
        <h3>Key Factors</h3>
        <div className="factors-grid">
          {result.factors.map((factor, index) => (
            <motion.div 
              key={index}
              className={`factor-card ${factor.impact}`}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: animationConfig.getDelay(0.5 + index * 0.1) / 1000 }}
            >
              <div className="factor-header">
                <span className="factor-icon">
                  {factor.impact === 'positive' ? '✓' : '!'}
                </span>
                <span className="factor-name">{factor.factor}</span>
                <span className={`factor-strength ${factor.strength}`}>
                  {factor.strength}
                </span>
              </div>
              <p className="factor-description">{factor.description}</p>
            </motion.div>
          ))}
        </div>
      </motion.div>

      {/* Warnings */}
      {result.warnings && result.warnings.length > 0 && (
        <motion.div 
          className="warnings-section"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: animationConfig.getDelay(0.6) / 1000 }}
        >
          <h3>⚠️ Important Notes</h3>
          <ul className="warnings-list">
            {result.warnings.map((warning, index) => (
              <li key={index}>{warning}</li>
            ))}
          </ul>
        </motion.div>
      )}

      {/* Interactive What-If Button */}
      <motion.button 
        className="scenario-button"
        onClick={onScenarioClick}
        whileHover={{ scale: 1.05 }}
        whileTap={{ scale: 0.95 }}
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: animationConfig.getDelay(0.8) / 1000 }}
      >
        <span className="button-icon">🔮</span>
        Explore What-If Scenarios
      </motion.button>
    </div>
  );
};