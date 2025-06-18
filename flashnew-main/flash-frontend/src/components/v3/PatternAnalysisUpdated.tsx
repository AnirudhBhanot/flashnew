import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Card, CardHeader, CardBody } from '../ui/Card';
import { ProgressBar, CircularProgress } from '../ui/Progress';
import { useStaggerAnimation } from '../../hooks/useScrollAnimation';
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
  const staggerChildren = useStaggerAnimation(patternData?.tags.length || 0);
  
  if (!patternData) {
    return null;
  }

  const getCategoryVariant = (category: string) => {
    const variants: Record<string, 'success' | 'warning' | 'danger' | 'default'> = {
      'efficient_growth': 'success',
      'high_burn_growth': 'warning',
      'technical_innovation': 'default',
      'market_driven': 'default',
      'bootstrap_profitable': 'success',
      'struggling_pivot': 'danger',
      'vertical_specific': 'warning'
    };
    return variants[category] || 'default';
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
            <motion.div 
              key={index} 
              className="breakdown-item"
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.3 + index * 0.1 }}
            >
              <div className="breakdown-header">
                <span className="breakdown-label">{item.label}</span>
                <span className="breakdown-value">{Math.round(item.value * 100)}%</span>
              </div>
              <ProgressBar
                value={item.value * 100}
                variant={item.value > 0.7 ? 'success' : item.value > 0.5 ? 'warning' : 'default'}
                animated
                striped
              />
            </motion.div>
          )
        )}
      </div>
    );
  };

  const renderPatternTags = (tags: string[]) => {
    return (
      <div className="pattern-tags">
        {tags.map((tag, index) => (
          <motion.span
            key={index}
            className="pattern-tag"
            initial={{ opacity: 0, scale: 0.8 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: staggerChildren.getDelay(index) }}
            whileHover={{ scale: 1.05 }}
          >
            {tag}
          </motion.span>
        ))}
      </div>
    );
  };

  const renderPatternCard = (pattern: PatternMatch, isPrimary: boolean = false) => {
    const variant = getCategoryVariant(pattern.category);
    
    return (
      <Card
        variant={isPrimary ? 'gradient' : 'bordered'}
        interactive
        onClick={() => setExpandedSection(pattern.name)}
        className={`pattern-card ${isPrimary ? 'primary' : ''}`}
      >
        <CardHeader
          icon={
            <CircularProgress
              value={pattern.confidence * 100}
              size={48}
              strokeWidth={4}
              variant={variant}
              showLabel={false}
            />
          }
          action={
            <motion.div 
              className="expand-icon"
              animate={{ rotate: expandedSection === pattern.name ? 180 : 0 }}
            >
              ▼
            </motion.div>
          }
        >
          <div className="pattern-header-content">
            <h3>{formatPatternName(pattern.name)}</h3>
            <p className={`confidence-label ${getConfidenceClass(pattern.confidence)}`}>
              {Math.round(pattern.confidence * 100)}% Match
            </p>
          </div>
        </CardHeader>

        <AnimatePresence>
          {expandedSection === pattern.name && (
            <motion.div
              initial={{ height: 0, opacity: 0 }}
              animate={{ height: 'auto', opacity: 1 }}
              exit={{ height: 0, opacity: 0 }}
            >
              <CardBody>
                {renderMatchBreakdown(pattern.match_breakdown)}
                
                <div className="pattern-stats">
                  <div className="stat-item">
                    <span className="stat-label">Expected Success Rate</span>
                    <span className="stat-value">
                      {Math.round(pattern.expected_success_rate * 100)}%
                    </span>
                  </div>
                </div>

                {pattern.similar_companies.length > 0 && (
                  <div className="similar-companies">
                    <h4>Similar Companies:</h4>
                    <div className="company-list">
                      {pattern.similar_companies.map((company, idx) => (
                        <motion.span
                          key={idx}
                          className="company-chip"
                          initial={{ opacity: 0, scale: 0.8 }}
                          animate={{ opacity: 1, scale: 1 }}
                          transition={{ delay: idx * 0.05 }}
                          whileHover={{ scale: 1.05 }}
                        >
                          {company}
                        </motion.span>
                      ))}
                    </div>
                  </div>
                )}

                {pattern.gaps.length > 0 && (
                  <div className="pattern-gaps">
                    <h4>Key Gaps:</h4>
                    <ul>
                      {pattern.gaps.map((gap, idx) => (
                        <motion.li
                          key={idx}
                          initial={{ opacity: 0, x: -20 }}
                          animate={{ opacity: 1, x: 0 }}
                          transition={{ delay: idx * 0.1 }}
                        >
                          {gap}
                        </motion.li>
                      ))}
                    </ul>
                  </div>
                )}

                {pattern.recommendations.length > 0 && (
                  <div className="pattern-recommendations">
                    <h4>Recommendations:</h4>
                    <ul>
                      {pattern.recommendations.map((rec, idx) => (
                        <motion.li
                          key={idx}
                          initial={{ opacity: 0, x: -20 }}
                          animate={{ opacity: 1, x: 0 }}
                          transition={{ delay: idx * 0.1 }}
                          className="recommendation-item"
                        >
                          {rec}
                        </motion.li>
                      ))}
                    </ul>
                  </div>
                )}
              </CardBody>
            </motion.div>
          )}
        </AnimatePresence>
      </Card>
    );
  };

  return (
    <div className="pattern-analysis">
      <motion.div
        className="analysis-header"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
      >
        <h2>Pattern Recognition Analysis</h2>
        {patternAdjustedProbability !== undefined && (
          <div className="adjusted-probability">
            <span className="label">Pattern-Adjusted Success:</span>
            <span className="value">
              {Math.round(patternAdjustedProbability * 100)}%
            </span>
          </div>
        )}
      </motion.div>

      {/* Primary Pattern */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.2 }}
      >
        {renderPatternCard(patternData.primary_pattern, true)}
      </motion.div>

      {/* Secondary Patterns */}
      {patternData.secondary_patterns.length > 0 && (
        <motion.div
          className="secondary-patterns"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.4 }}
        >
          <h3>Alternative Patterns</h3>
          <div className="patterns-grid">
            {patternData.secondary_patterns.map((pattern, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.5 + index * 0.1 }}
              >
                {renderPatternCard(pattern)}
              </motion.div>
            ))}
          </div>
        </motion.div>
      )}

      {/* Pattern Tags */}
      {patternData.tags.length > 0 && (
        <Card variant="bordered" className="tags-card">
          <CardBody>
            <h4>Startup Characteristics</h4>
            {renderPatternTags(patternData.tags)}
          </CardBody>
        </Card>
      )}

      {/* Evolution Insights */}
      <Card variant="elevated" className="evolution-card">
        <CardHeader>
          <h3>Evolution Path</h3>
          <span className="current-stage">
            {formatPatternName(patternData.evolution.current_stage)} Stage
          </span>
        </CardHeader>
        <CardBody>
          <div className="evolution-paths">
            <h4>Likely Evolution Patterns:</h4>
            {patternData.evolution.next_patterns.map((path, index) => (
              <motion.div
                key={index}
                className="evolution-path"
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.3 + index * 0.1 }}
              >
                <div className="path-header">
                  <span className="path-name">{formatPatternName(path.pattern)}</span>
                  <span className="path-probability">
                    {Math.round(path.probability * 100)}%
                  </span>
                </div>
                <ProgressBar
                  value={path.probability * 100}
                  variant={path.probability > 0.5 ? 'success' : 'default'}
                  animated
                />
              </motion.div>
            ))}
          </div>

          <div className="pattern-quality">
            <h4>Pattern Quality Metrics:</h4>
            <div className="quality-metrics">
              <div className="metric">
                <span className="metric-label">Stability</span>
                <CircularProgress
                  value={patternData.pattern_quality.stability * 100}
                  size={60}
                  variant={patternData.pattern_quality.stability > 0.7 ? 'success' : 'warning'}
                />
              </div>
              <div className="metric">
                <span className="metric-label">Uniqueness</span>
                <CircularProgress
                  value={patternData.pattern_quality.uniqueness * 100}
                  size={60}
                  variant={patternData.pattern_quality.uniqueness > 0.7 ? 'success' : 'warning'}
                />
              </div>
            </div>
          </div>
        </CardBody>
      </Card>
    </div>
  );
};