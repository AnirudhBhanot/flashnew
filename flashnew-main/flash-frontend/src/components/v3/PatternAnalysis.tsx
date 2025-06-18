import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import './PatternAnalysis.css';

interface PatternMatch {
  name: string;
  confidence: number;
  category: string;
  expected_success_rate: number;
  similar_companies: string[];
  match_breakdown: {
    camp_match?: number;
    feature_match?: number;
    statistical_match?: number;
  };
  gaps: string[];
  recommendations: string[];
}

interface PatternAnalysisData {
  primary_pattern: PatternMatch;
  secondary_patterns: PatternMatch[];
  pattern_mixture: Record<string, number>;
  tags: string[];
  evolution: {
    current_stage: string;
    next_patterns: Array<{
      pattern: string;
      probability: number;
    }>;
  };
  pattern_quality: {
    stability: number;
    uniqueness: number;
  };
  success_modifier: number;
}

interface PatternAnalysisProps {
  patternData?: PatternAnalysisData;
  patternAdjustedProbability?: number;
}

export const PatternAnalysis: React.FC<PatternAnalysisProps> = ({ 
  patternData, 
  patternAdjustedProbability 
}) => {
  const [expandedSection, setExpandedSection] = useState<string | null>('primary');
  
  if (!patternData) {
    return null;
  }

  const getCategoryColor = (category: string) => {
    const colors: Record<string, string> = {
      'efficient_growth': '#00C851',
      'high_burn_growth': '#FF8800',
      'technical_innovation': '#33B5E5',
      'market_driven': '#AA66CC',
      'bootstrap_profitable': '#00C851',
      'struggling_pivot': '#FF4444',
      'vertical_specific': '#FFBB33'
    };
    return colors[category] || '#666';
  };

  const getConfidenceClass = (confidence: number) => {
    if (confidence >= 0.8) return 'very-high';
    if (confidence >= 0.6) return 'high';
    if (confidence >= 0.4) return 'medium';
    return 'low';
  };

  const formatPatternName = (name: string) => {
    return name
      .split('_')
      .map(word => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase())
      .join(' ');
  };

  const renderMatchBreakdown = (breakdown: PatternMatch['match_breakdown']) => {
    const items = [
      { label: 'CAMP Match', value: breakdown.camp_match },
      { label: 'Feature Match', value: breakdown.feature_match },
      { label: 'Statistical Match', value: breakdown.statistical_match }
    ];

    return (
      <div className="match-breakdown">
        {items.map((item, index) => 
          item.value !== undefined && (
            <div key={index} className="breakdown-item">
              <span className="breakdown-label">{item.label}</span>
              <div className="breakdown-bar">
                <motion.div 
                  className="breakdown-fill"
                  initial={{ width: 0 }}
                  animate={{ width: `${item.value * 100}%` }}
                  transition={{ delay: 0.3 + index * 0.1 }}
                />
              </div>
              <span className="breakdown-value">{(item.value * 100).toFixed(0)}%</span>
            </div>
          )
        )}
      </div>
    );
  };

  const renderPatternTags = (tags: string[]) => {
    const tagCategories = {
      growth: ['hypergrowth', 'steady_growth', 'stagnant', 'declining'],
      efficiency: ['capital_efficient', 'high_burn', 'break_even', 'profitable'],
      position: ['market_leader', 'fast_follower', 'niche_player', 'struggling'],
      tech: ['ai_enabled', 'mobile_first', 'api_first', 'hardware_component'],
      risk: ['high_risk', 'moderate_risk', 'low_risk']
    };

    const getTagCategory = (tag: string) => {
      for (const [category, categoryTags] of Object.entries(tagCategories)) {
        if (categoryTags.includes(tag)) return category;
      }
      return 'other';
    };

    return (
      <div className="pattern-tags">
        {tags.map((tag, index) => (
          <motion.span 
            key={tag}
            className={`pattern-tag tag-${getTagCategory(tag)}`}
            initial={{ opacity: 0, scale: 0.8 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 0.05 * index }}
          >
            {tag.replace(/_/g, ' ')}
          </motion.span>
        ))}
      </div>
    );
  };

  return (
    <motion.div 
      className="pattern-analysis-container"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6 }}
    >
      <h2 className="pattern-title">
        <span className="pattern-icon">🧬</span>
        Startup DNA Pattern Analysis
      </h2>

      {/* Pattern-Adjusted Probability */}
      {patternAdjustedProbability !== undefined && (
        <div className="pattern-adjusted-probability">
          <div className="probability-comparison">
            <div className="probability-item">
              <span className="prob-label">Pattern-Enhanced</span>
              <span className="prob-value enhanced">
                {(patternAdjustedProbability * 100).toFixed(1)}%
              </span>
            </div>
            <div className="modifier-indicator">
              <span className="modifier-value">
                {patternData.success_modifier > 1 ? '+' : ''}
                {((patternData.success_modifier - 1) * 100).toFixed(0)}%
              </span>
              <span className="modifier-label">Pattern Impact</span>
            </div>
          </div>
        </div>
      )}

      {/* Primary Pattern */}
      <motion.div 
        className={`pattern-section primary ${expandedSection === 'primary' ? 'expanded' : ''}`}
        onClick={() => setExpandedSection(expandedSection === 'primary' ? null : 'primary')}
      >
        <div className="pattern-header">
          <div className="pattern-info">
            <h3 className="pattern-name">
              {formatPatternName(patternData.primary_pattern.name)}
            </h3>
            <span 
              className="pattern-category"
              style={{ backgroundColor: getCategoryColor(patternData.primary_pattern.category) }}
            >
              {formatPatternName(patternData.primary_pattern.category)}
            </span>
            <span className={`pattern-confidence ${getConfidenceClass(patternData.primary_pattern.confidence)}`}>
              {(patternData.primary_pattern.confidence * 100).toFixed(0)}% Match
            </span>
          </div>
          <motion.div 
            className="expand-icon"
            animate={{ rotate: expandedSection === 'primary' ? 180 : 0 }}
          >
            ▼
          </motion.div>
        </div>

        <AnimatePresence>
          {expandedSection === 'primary' && (
            <motion.div 
              className="pattern-details"
              initial={{ height: 0, opacity: 0 }}
              animate={{ height: 'auto', opacity: 1 }}
              exit={{ height: 0, opacity: 0 }}
            >
              <div className="success-rate">
                <span className="rate-label">Expected Success Rate:</span>
                <span className="rate-value">
                  {(patternData.primary_pattern.expected_success_rate * 100).toFixed(0)}%
                </span>
              </div>

              {renderMatchBreakdown(patternData.primary_pattern.match_breakdown)}

              <div className="similar-companies">
                <h4>Similar Successful Companies:</h4>
                <div className="company-list">
                  {patternData.primary_pattern.similar_companies.map((company, index) => (
                    <span key={index} className="company-tag">{company}</span>
                  ))}
                </div>
              </div>

              {patternData.primary_pattern.gaps.length > 0 && (
                <div className="pattern-gaps">
                  <h4>Areas for Improvement:</h4>
                  <ul>
                    {patternData.primary_pattern.gaps.map((gap, index) => (
                      <li key={index}>{gap}</li>
                    ))}
                  </ul>
                </div>
              )}

              {patternData.primary_pattern.recommendations.length > 0 && (
                <div className="pattern-recommendations">
                  <h4>Specific Recommendations:</h4>
                  <ul>
                    {patternData.primary_pattern.recommendations.map((rec, index) => (
                      <li key={index}>{rec}</li>
                    ))}
                  </ul>
                </div>
              )}
            </motion.div>
          )}
        </AnimatePresence>
      </motion.div>

      {/* Pattern Tags */}
      {patternData.tags.length > 0 && (
        <div className="pattern-tags-section">
          <h4>Startup Characteristics:</h4>
          {renderPatternTags(patternData.tags)}
        </div>
      )}

      {/* Evolution Insights */}
      <motion.div 
        className={`pattern-section evolution ${expandedSection === 'evolution' ? 'expanded' : ''}`}
        onClick={() => setExpandedSection(expandedSection === 'evolution' ? null : 'evolution')}
      >
        <div className="pattern-header">
          <h3>Evolution Path</h3>
          <span className="current-stage">{formatPatternName(patternData.evolution.current_stage)} Stage</span>
          <motion.div 
            className="expand-icon"
            animate={{ rotate: expandedSection === 'evolution' ? 180 : 0 }}
          >
            ▼
          </motion.div>
        </div>

        <AnimatePresence>
          {expandedSection === 'evolution' && (
            <motion.div 
              className="pattern-details"
              initial={{ height: 0, opacity: 0 }}
              animate={{ height: 'auto', opacity: 1 }}
              exit={{ height: 0, opacity: 0 }}
            >
              <div className="evolution-paths">
                <h4>Likely Evolution Patterns:</h4>
                {patternData.evolution.next_patterns.map((path, index) => (
                  <div key={index} className="evolution-path">
                    <span className="path-name">{formatPatternName(path.pattern)}</span>
                    <div className="path-probability">
                      <div className="probability-bar">
                        <motion.div 
                          className="probability-fill"
                          initial={{ width: 0 }}
                          animate={{ width: `${path.probability * 100}%` }}
                          transition={{ delay: 0.3 + index * 0.1 }}
                        />
                      </div>
                      <span className="probability-text">
                        {(path.probability * 100).toFixed(0)}%
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </motion.div>

      {/* Secondary Patterns */}
      {patternData.secondary_patterns.length > 0 && (
        <motion.div 
          className={`pattern-section secondary ${expandedSection === 'secondary' ? 'expanded' : ''}`}
          onClick={() => setExpandedSection(expandedSection === 'secondary' ? null : 'secondary')}
        >
          <div className="pattern-header">
            <h3>Secondary Pattern Matches</h3>
            <motion.div 
              className="expand-icon"
              animate={{ rotate: expandedSection === 'secondary' ? 180 : 0 }}
            >
              ▼
            </motion.div>
          </div>

          <AnimatePresence>
            {expandedSection === 'secondary' && (
              <motion.div 
                className="pattern-details"
                initial={{ height: 0, opacity: 0 }}
                animate={{ height: 'auto', opacity: 1 }}
                exit={{ height: 0, opacity: 0 }}
              >
                {patternData.secondary_patterns.map((pattern, index) => (
                  <div key={index} className="secondary-pattern">
                    <span className="pattern-name">{formatPatternName(pattern.name)}</span>
                    <span className={`pattern-confidence ${getConfidenceClass(pattern.confidence)}`}>
                      {(pattern.confidence * 100).toFixed(0)}%
                    </span>
                  </div>
                ))}
              </motion.div>
            )}
          </AnimatePresence>
        </motion.div>
      )}

      {/* Pattern Quality Indicators */}
      <div className="pattern-quality">
        <div className="quality-indicator">
          <span className="quality-label">Pattern Stability</span>
          <div className="quality-bar">
            <motion.div 
              className="quality-fill"
              initial={{ width: 0 }}
              animate={{ width: `${patternData.pattern_quality.stability * 100}%` }}
              style={{ 
                backgroundColor: patternData.pattern_quality.stability > 0.7 ? '#00C851' : '#FF8800' 
              }}
            />
          </div>
          <span className="quality-value">
            {(patternData.pattern_quality.stability * 100).toFixed(0)}%
          </span>
        </div>
        <div className="quality-indicator">
          <span className="quality-label">Pattern Uniqueness</span>
          <div className="quality-bar">
            <motion.div 
              className="quality-fill"
              initial={{ width: 0 }}
              animate={{ width: `${patternData.pattern_quality.uniqueness * 100}%` }}
              style={{ 
                backgroundColor: patternData.pattern_quality.uniqueness > 0.7 ? '#33B5E5' : '#FF8800' 
              }}
            />
          </div>
          <span className="quality-value">
            {(patternData.pattern_quality.uniqueness * 100).toFixed(0)}%
          </span>
        </div>
      </div>
    </motion.div>
  );
};