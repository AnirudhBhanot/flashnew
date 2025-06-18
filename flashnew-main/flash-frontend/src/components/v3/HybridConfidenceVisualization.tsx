import React from 'react';
import { motion } from 'framer-motion';
import './HybridConfidenceVisualization.css';

interface HybridConfidenceVisualizationProps {
  confidence: number;
  predictions: {
    base: number;
    patterns: number;
    stage: number;
    industry: number;
    camp: number;
  };
}

export const HybridConfidenceVisualization: React.FC<HybridConfidenceVisualizationProps> = ({ 
  confidence, 
  predictions 
}) => {
  const getModelIcon = (model: string) => {
    const icons: Record<string, string> = {
      base: '🏗️',
      patterns: '🧬',
      stage: '📈',
      industry: '🏭',
      camp: '🎯'
    };
    return icons[model] || '📊';
  };

  const getModelLabel = (model: string) => {
    const labels: Record<string, string> = {
      base: 'Foundation',
      patterns: 'Patterns',
      stage: 'Stage',
      industry: 'Industry',
      camp: 'CAMP'
    };
    return labels[model] || model;
  };

  const getModelDescription = (model: string) => {
    const descriptions: Record<string, string> = {
      base: 'Core contractual models',
      patterns: 'Startup archetype analysis',
      stage: 'Funding stage optimization',
      industry: 'Vertical-specific insights',
      camp: 'Framework refinement'
    };
    return descriptions[model] || '';
  };

  const getConfidenceLevel = (confidence: number) => {
    if (confidence >= 0.8) return { level: 'Very High', color: '#00C851' };
    if (confidence >= 0.7) return { level: 'High', color: '#33B5E5' };
    if (confidence >= 0.6) return { level: 'Moderate', color: '#FF8800' };
    if (confidence >= 0.5) return { level: 'Low', color: '#FF6F00' };
    return { level: 'Very Low', color: '#FF4444' };
  };

  const { level: confidenceLevel, color: confidenceColor } = getConfidenceLevel(confidence);

  // Calculate model agreement
  const modelValues = Object.values(predictions);
  const avgPrediction = modelValues.reduce((a, b) => a + b, 0) / modelValues.length;
  const variance = modelValues.reduce((sum, val) => sum + Math.pow(val - avgPrediction, 2), 0) / modelValues.length;
  const agreement = 1 - Math.sqrt(variance);

  return (
    <div className="hybrid-confidence-viz">
      <div className="confidence-header">
        <h4>Model Confidence Analysis</h4>
        <div className="confidence-score" style={{ color: confidenceColor }}>
          {(confidence * 100).toFixed(0)}%
          <span className="confidence-label">{confidenceLevel}</span>
        </div>
      </div>

      <div className="model-predictions">
        {Object.entries(predictions).map(([model, value], index) => (
          <motion.div 
            key={model}
            className="model-prediction-item"
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: index * 0.1 }}
          >
            <div className="model-info">
              <span className="model-icon">{getModelIcon(model)}</span>
              <div className="model-details">
                <span className="model-name">{getModelLabel(model)}</span>
                <span className="model-desc">{getModelDescription(model)}</span>
              </div>
            </div>
            <div className="model-value">
              <div className="value-bar">
                <motion.div 
                  className="value-fill"
                  initial={{ width: 0 }}
                  animate={{ width: `${value * 100}%` }}
                  transition={{ duration: 0.8, delay: index * 0.1 }}
                  style={{ 
                    backgroundColor: value >= 0.7 ? '#00C851' : 
                                   value >= 0.5 ? '#33B5E5' : 
                                   value >= 0.3 ? '#FF8800' : '#FF4444'
                  }}
                />
              </div>
              <span className="value-text">{(value * 100).toFixed(1)}%</span>
            </div>
          </motion.div>
        ))}
      </div>

      <div className="agreement-section">
        <div className="agreement-metric">
          <span className="metric-label">Model Agreement</span>
          <span className="metric-value" style={{ color: agreement > 0.8 ? '#00C851' : agreement > 0.6 ? '#FF8800' : '#FF4444' }}>
            {(agreement * 100).toFixed(0)}%
          </span>
        </div>
        <div className="agreement-bar">
          <motion.div 
            className="agreement-fill"
            initial={{ width: 0 }}
            animate={{ width: `${agreement * 100}%` }}
            transition={{ duration: 0.8 }}
            style={{ 
              backgroundColor: agreement > 0.8 ? '#00C851' : agreement > 0.6 ? '#FF8800' : '#FF4444'
            }}
          />
        </div>
      </div>

      <div className="confidence-insights">
        <h5>Confidence Factors</h5>
        <ul>
          {agreement > 0.8 && <li>✅ High model consensus</li>}
          {agreement <= 0.8 && agreement > 0.6 && <li>⚠️ Moderate model agreement</li>}
          {agreement <= 0.6 && <li>❌ Low model consensus</li>}
          {confidence > 0.8 && <li>✅ Strong prediction confidence</li>}
          {Math.max(...modelValues) > 0.7 && <li>✅ At least one strong signal</li>}
          {Math.min(...modelValues) < 0.3 && <li>⚠️ Some models show concern</li>}
        </ul>
      </div>
    </div>
  );
};