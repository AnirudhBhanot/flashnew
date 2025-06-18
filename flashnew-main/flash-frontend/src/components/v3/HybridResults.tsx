import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { CAMPRadarChart } from './CAMPRadarChart';
import { HybridConfidenceVisualization } from './HybridConfidenceVisualization';
import { configService } from '../../services/LegacyConfigService';
import { MODEL_WEIGHTS, SCORE_COLORS } from '../../config/constants';
import './HybridResults.css';

interface HybridResultsProps {
  data: any;
}

export const HybridResults: React.FC<HybridResultsProps> = ({ data }) => {
  const [activeTab, setActiveTab] = useState<'overview' | 'models' | 'patterns' | 'recommendations'>('overview');
  const [expandedSection, setExpandedSection] = useState<string | null>(null);
  const [config, setConfig] = useState<any>(null);

  useEffect(() => {
    configService.getAllConfig().then(setConfig);
  }, []);
  

  // Helper functions
  const getScoreColor = (score: number) => {
    const colors = config?.scoreColors || SCORE_COLORS;
    
    if (score >= colors.excellent.min) return colors.excellent.color;
    if (score >= colors.good.min) return colors.good.color;
    if (score >= colors.fair.min) return colors.fair.color;
    return colors.poor.color;
  };

  const getVerdictClass = (verdict: string) => {
    const verdictMap: Record<string, string> = {
      'STRONG PASS': 'strong-pass',
      'PASS': 'pass',
      'CONDITIONAL PASS': 'conditional-pass',
      'CONDITIONAL FAIL': 'conditional-fail',
      'FAIL': 'fail',
      'STRONG FAIL': 'strong-fail'
    };
    return verdictMap[verdict] || 'neutral';
  };

  const getRiskClass = (risk: string) => {
    return risk.toLowerCase();
  };

  const formatPercentage = (value: number) => {
    return `${(value * 100).toFixed(1)}%`;
  };

  const getPatternIcon = (pattern: string) => {
    const icons: Record<string, string> = {
      'efficient_growth': '🚀',
      'market_leader': '👑',
      'vc_hypergrowth': '💰',
      'capital_efficient': '💎',
      'b2b_saas': '☁️',
      'product_led': '🎯',
      'bootstrap_profitable': '🌱',
      'ai_ml_core': '🤖',
      'platform_network': '🌐',
      'deep_tech': '🔬'
    };
    return icons[pattern] || '📊';
  };

  const getModelTypeIcon = (type: string) => {
    const icons: Record<string, string> = {
      'base': '🏗️',
      'patterns': '🧬',
      'stage': '📈',
      'industry': '🏭',
      'camp': '🎯'
    };
    return icons[type] || '📊';
  };

  return (
    <div className="hybrid-results">
      {/* Header with verdict */}
      <motion.div 
        className="results-header"
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
      >
        <div className={`verdict-badge ${getVerdictClass(data.verdict)}`}>
          <span className="verdict-icon">{data.verdict === 'PASS' || data.verdict === 'STRONG PASS' ? '✅' : '❌'}</span>
          <span className="verdict-text">{data.verdict}</span>
        </div>
        
        <div className="risk-indicator">
          <span className={`risk-badge ${getRiskClass(data.risk_level)}`}>
            {data.risk_level} RISK
          </span>
        </div>
      </motion.div>

      {/* Main Score Display */}
      <motion.div 
        className="main-score-section"
        initial={{ opacity: 0, scale: 0.9 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ delay: 0.1 }}
      >
        <div className="probability-display">
          <div className="probability-value" style={{ color: getScoreColor(data.success_probability || 0.5) }}>
            {formatPercentage(data.success_probability || 0.5)}
          </div>
          <div className="probability-label">Success Probability</div>
        </div>
        
        <div className="confidence-display">
          <HybridConfidenceVisualization 
            confidence={data.confidence_score || 0.85}
            predictions={{
              base: data.all_predictions?.base || data.success_probability || 0.5,
              patterns: data.all_predictions?.patterns || data.success_probability || 0.5,
              stage: data.all_predictions?.stage || data.success_probability || 0.5,
              industry: data.all_predictions?.industry || data.success_probability || 0.5,
              camp: data.all_predictions?.camp || data.success_probability || 0.5
            }}
          />
        </div>
      </motion.div>

      {/* Tab Navigation */}
      <motion.div 
        className="tab-navigation"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.2 }}
      >
        <button 
          className={`tab-button ${activeTab === 'overview' ? 'active' : ''}`}
          onClick={() => setActiveTab('overview')}
        >
          Overview
        </button>
        <button 
          className={`tab-button ${activeTab === 'models' ? 'active' : ''}`}
          onClick={() => setActiveTab('models')}
        >
          Model Analysis
        </button>
        <button 
          className={`tab-button ${activeTab === 'patterns' ? 'active' : ''}`}
          onClick={() => setActiveTab('patterns')}
        >
          Patterns
        </button>
        <button 
          className={`tab-button ${activeTab === 'recommendations' ? 'active' : ''}`}
          onClick={() => setActiveTab('recommendations')}
        >
          Recommendations
        </button>
      </motion.div>

      {/* Tab Content */}
      <AnimatePresence mode="wait">
        {activeTab === 'overview' && (
          <motion.div
            key="overview"
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: -20 }}
            className="tab-content"
          >
            {/* CAMP Scores */}
            <div className="camp-section">
              <h3>CAMP Framework Analysis</h3>
              <div className="camp-visualization">
                <CAMPRadarChart scores={data.pillar_scores} />
              </div>
              <div className="camp-breakdown">
                {Object.entries(data.pillar_scores).map(([key, value]) => (
                  <div key={key} className="camp-item">
                    <div className="camp-label">
                      <span className="camp-icon">{getModelTypeIcon(key)}</span>
                      <span className="camp-name">{key.charAt(0).toUpperCase() + key.slice(1)}</span>
                    </div>
                    <div className="camp-bar">
                      <motion.div 
                        className="camp-fill"
                        initial={{ width: 0 }}
                        animate={{ width: `${(value as number) * 100}%` }}
                        style={{ backgroundColor: getScoreColor(value as number) }}
                      />
                    </div>
                    <div className="camp-value">{formatPercentage(value as number)}</div>
                  </div>
                ))}
              </div>
            </div>

            {/* Key Insights */}
            {data.key_insights && data.key_insights.length > 0 && (
              <div className="insights-section">
                <h3>Key Insights</h3>
                <div className="insights-list">
                  {data.key_insights.map((insight: string, index: number) => (
                    <motion.div 
                      key={index}
                      className="insight-item"
                      initial={{ opacity: 0, x: -20 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ delay: index * 0.1 }}
                    >
                      <span className="insight-icon">💡</span>
                      <span className="insight-text">{insight}</span>
                    </motion.div>
                  ))}
                </div>
              </div>
            )}
          </motion.div>
        )}

        {activeTab === 'models' && (
          <motion.div
            key="models"
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: -20 }}
            className="tab-content"
          >
            <h3>Model Ensemble Breakdown</h3>
            <p className="section-description">
              Your startup was evaluated by {config?.modelInfo?.total_models || 29} specialized models across {config?.modelInfo?.categories || 5} categories
            </p>
            
            <div className="model-breakdown">
              {data.model_breakdown && Object.entries(data.model_breakdown).map(([model, score]) => (
                <div key={model} className="model-item">
                  <div className="model-header">
                    <span className="model-icon">{getModelTypeIcon(model.split('_')[0])}</span>
                    <span className="model-name">{model.replace(/_/g, ' ').toUpperCase()}</span>
                  </div>
                  <div className="model-score">
                    <div className="score-bar">
                      <motion.div 
                        className="score-fill"
                        initial={{ width: 0 }}
                        animate={{ width: `${(score as number) * 100}%` }}
                        style={{ backgroundColor: getScoreColor(score as number) }}
                      />
                    </div>
                    <span className="score-value">{formatPercentage(score as number)}</span>
                  </div>
                </div>
              ))}
            </div>

            <div className="model-summary">
              <h4>Model Categories</h4>
              <ul>
                {Object.entries(config?.modelWeights || MODEL_WEIGHTS).map(([key, value]: [string, any]) => (
                  <li key={key}>
                    <strong>{value.label} ({value.percentage}):</strong> {
                      key === 'base_analysis' ? 'Foundation models using contractual architecture' :
                      key === 'pattern_detection' ? 'Specialized models for startup archetypes' :
                      key === 'stage_factors' ? 'Funding stage-specific evaluation' :
                      key === 'industry_specific' ? 'Vertical-specific insights' :
                      'Framework refinement models'
                    }
                  </li>
                ))}
              </ul>
            </div>
          </motion.div>
        )}

        {activeTab === 'patterns' && (
          <motion.div
            key="patterns"
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: -20 }}
            className="tab-content"
          >
            <h3>Pattern Analysis</h3>
            
            {/* Dominant Patterns */}
            {data.patterns && data.patterns.length > 0 && (
              <div className="dominant-patterns">
                <h4>Dominant Patterns Detected</h4>
                <div className="pattern-list">
                  {data.patterns.map((pattern: string, index: number) => (
                    <motion.div 
                      key={pattern}
                      className="pattern-badge"
                      initial={{ opacity: 0, scale: 0.8 }}
                      animate={{ opacity: 1, scale: 1 }}
                      transition={{ delay: index * 0.1 }}
                    >
                      <span className="pattern-icon">{getPatternIcon(pattern)}</span>
                      <span className="pattern-name">
                        {pattern.replace(/_/g, ' ').split(' ').map(word => 
                          word.charAt(0).toUpperCase() + word.slice(1)
                        ).join(' ')}
                      </span>
                    </motion.div>
                  ))}
                </div>
              </div>
            )}

            {/* Stage & Industry Fit */}
            <div className="fit-analysis">
              <div className="fit-item">
                <h4>Stage Fit</h4>
                <div className={`fit-badge ${data.stage_fit?.includes('Strong') ? 'strong' : data.stage_fit?.includes('Moderate') ? 'moderate' : 'weak'}`}>
                  {data.stage_fit || 'Unknown'}
                </div>
              </div>
              
              <div className="fit-item">
                <h4>Industry Fit</h4>
                <div className={`fit-badge ${data.industry_fit?.includes('Strong') ? 'strong' : data.industry_fit?.includes('Moderate') ? 'moderate' : 'weak'}`}>
                  {data.industry_fit || 'Unknown'}
                </div>
              </div>
            </div>

            {/* Pattern Descriptions */}
            <div className="pattern-descriptions">
              <h4>What These Patterns Mean</h4>
              {data.patterns && data.patterns.map((pattern: string) => (
                <div key={pattern} className="pattern-description">
                  <h5>{pattern.replace(/_/g, ' ').split(' ').map(word => 
                    word.charAt(0).toUpperCase() + word.slice(1)
                  ).join(' ')}</h5>
                  <p>{getPatternDescription(pattern)}</p>
                </div>
              ))}
            </div>
          </motion.div>
        )}

        {activeTab === 'recommendations' && (
          <motion.div
            key="recommendations"
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: -20 }}
            className="tab-content"
          >
            <h3>Actionable Recommendations</h3>
            
            {data.recommendations && data.recommendations.length > 0 && (
              <div className="recommendations-list">
                {data.recommendations.map((rec: string, index: number) => (
                  <motion.div 
                    key={index}
                    className="recommendation-item"
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: index * 0.1 }}
                  >
                    <div className="rec-number">{index + 1}</div>
                    <div className="rec-content">
                      <p>{rec}</p>
                      <button 
                        className="rec-expand"
                        onClick={() => setExpandedSection(expandedSection === `rec-${index}` ? null : `rec-${index}`)}
                      >
                        {expandedSection === `rec-${index}` ? 'Less' : 'More'}
                      </button>
                    </div>
                  </motion.div>
                ))}
              </div>
            )}

            {/* CAMP-based recommendations */}
            <div className="camp-recommendations">
              <h4>CAMP Framework Improvements</h4>
              {Object.entries(data.pillar_scores).map(([pillar, score]) => {
                if ((score as number) < 0.6) {
                  return (
                    <div key={pillar} className="camp-rec-item">
                      <div className="camp-rec-header">
                        <span className="camp-icon">{getModelTypeIcon(pillar)}</span>
                        <span className="camp-name">{pillar.charAt(0).toUpperCase() + pillar.slice(1)}</span>
                        <span className="camp-score" style={{ color: getScoreColor(score as number) }}>
                          {formatPercentage(score as number)}
                        </span>
                      </div>
                      <p className="camp-rec-text">{getCampRecommendation(pillar, score as number)}</p>
                    </div>
                  );
                }
                return null;
              })}
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};

// Helper function for pattern descriptions
function getPatternDescription(pattern: string): string {
  const descriptions: Record<string, string> = {
    'efficient_growth': 'Your startup shows signs of sustainable growth with efficient capital utilization. This pattern is associated with long-term success and attractive unit economics.',
    'market_leader': 'You demonstrate characteristics of a potential market leader with strong competitive positioning and market share growth potential.',
    'vc_hypergrowth': 'Your metrics align with VC-backed hypergrowth companies. Focus on maintaining growth while managing burn rate.',
    'capital_efficient': 'Excellent capital efficiency metrics suggest strong fundamentals and potential for profitability.',
    'b2b_saas': 'Classic B2B SaaS metrics with recurring revenue and enterprise focus. Continue optimizing net revenue retention.',
    'product_led': 'Product-led growth indicators are strong. User adoption and retention are key success factors.',
    'bootstrap_profitable': 'Bootstrap mentality with path to profitability. This sustainable approach reduces dependency on external funding.',
    'ai_ml_core': 'AI/ML is core to your value proposition. Continue investing in R&D and technical talent.',
    'platform_network': 'Network effects are building. Focus on reaching critical mass for exponential growth.',
    'deep_tech': 'Deep technology focus requires patient capital but offers strong moats once commercialized.'
  };
  return descriptions[pattern] || 'This pattern indicates specific characteristics in your business model and growth trajectory.';
}

// Helper function for CAMP recommendations
function getCampRecommendation(pillar: string, score: number): string {
  const recommendations: Record<string, Record<string, string>> = {
    capital: {
      low: 'Improve burn multiple and extend runway. Consider revenue-based financing or bridge rounds.',
      medium: 'Optimize unit economics and focus on path to profitability.'
    },
    advantage: {
      low: 'Strengthen competitive moats through patents, network effects, or technical differentiation.',
      medium: 'Enhance product differentiation and build stronger barriers to entry.'
    },
    market: {
      low: 'Validate market size and growth. Consider pivoting to larger or faster-growing segments.',
      medium: 'Improve go-to-market strategy and expand addressable market.'
    },
    people: {
      low: 'Strengthen leadership team and add domain expertise. Consider experienced advisors.',
      medium: 'Focus on team scaling and culture. Add specialized talent in key areas.'
    }
  };
  
  const level = score < 0.4 ? 'low' : 'medium';
  return recommendations[pillar]?.[level] || 'Focus on improving this aspect of your business.';
}