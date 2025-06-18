import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { configService } from '../../../services/LegacyConfigService';
import { DISPLAY_LIMITS } from '../../../config/constants';
import './BusinessInsights.css';

interface BusinessInsightsProps {
  keyInsights: string[];
  riskFactors?: string[];
  growthIndicators?: string[];
}

const translateToBusinessLanguage = (insight: string): {
  title: string;
  explanation: string;
  icon: string;
  type: 'positive' | 'negative' | 'neutral';
} => {
  const insightLower = insight.toLowerCase();
  
  // Financial insights
  if (insightLower.includes('burn') && insightLower.includes('high')) {
    return {
      title: 'Cash Efficiency Concern',
      explanation: 'The company is spending significantly more than it earns. This limits runway and increases dependency on external funding.',
      icon: '💸',
      type: 'negative'
    };
  }
  
  if (insightLower.includes('revenue growth') && insightLower.includes('strong')) {
    return {
      title: 'Rapid Revenue Growth',
      explanation: 'Revenue is growing faster than industry average, indicating strong product-market fit and customer demand.',
      icon: '📈',
      type: 'positive'
    };
  }
  
  if (insightLower.includes('runway') && (insightLower.includes('good') || insightLower.includes('strong'))) {
    return {
      title: 'Healthy Cash Position',
      explanation: 'The company has sufficient cash to operate for an extended period, reducing immediate funding pressure.',
      icon: '💰',
      type: 'positive'
    };
  }
  
  // Team insights
  if (insightLower.includes('experienced team') || insightLower.includes('strong team')) {
    return {
      title: 'Exceptional Team',
      explanation: 'The founding team has relevant experience and a track record of success, increasing execution probability.',
      icon: '🌟',
      type: 'positive'
    };
  }
  
  if (insightLower.includes('key person') || insightLower.includes('single founder')) {
    return {
      title: 'Team Risk',
      explanation: 'Heavy reliance on one person creates vulnerability. Building a strong leadership team should be a priority.',
      icon: '👤',
      type: 'negative'
    };
  }
  
  // Market insights
  if (insightLower.includes('large market') || insightLower.includes('tam')) {
    return {
      title: 'Significant Market Opportunity',
      explanation: 'The addressable market is large enough to support a billion-dollar company with room for multiple winners.',
      icon: '🌍',
      type: 'positive'
    };
  }
  
  if (insightLower.includes('competitive') || insightLower.includes('competition')) {
    return {
      title: 'Competitive Landscape',
      explanation: 'Multiple well-funded competitors exist. Success will depend on execution speed and differentiation.',
      icon: '🏁',
      type: 'neutral'
    };
  }
  
  // Product insights
  if (insightLower.includes('retention') && (insightLower.includes('high') || insightLower.includes('strong'))) {
    return {
      title: 'Strong Product Stickiness',
      explanation: 'Users continue using the product over time, indicating genuine value creation and product-market fit.',
      icon: '🎯',
      type: 'positive'
    };
  }
  
  if (insightLower.includes('churn') && insightLower.includes('high')) {
    return {
      title: 'Customer Retention Challenge',
      explanation: 'High customer turnover suggests product-market fit issues. Understanding why customers leave is critical.',
      icon: '📉',
      type: 'negative'
    };
  }
  
  // Default translation
  return {
    title: 'Key Insight',
    explanation: insight,
    icon: '💡',
    type: 'neutral'
  };
};

const getActionableRecommendation = (insight: any): string => {
  if (insight.title === 'Cash Efficiency Concern') {
    return 'Review unit economics and path to profitability. Consider revenue acceleration or cost reduction initiatives.';
  }
  if (insight.title === 'Team Risk') {
    return 'Prioritize hiring a co-founder or C-level executives. Document critical processes and knowledge.';
  }
  if (insight.title === 'Customer Retention Challenge') {
    return 'Conduct exit interviews with churned customers. Implement customer success program.';
  }
  if (insight.title === 'Competitive Landscape') {
    return 'Define clear differentiation. Focus on a specific customer segment or use case to dominate.';
  }
  return '';
};

export const BusinessInsights: React.FC<BusinessInsightsProps> = ({
  keyInsights,
  riskFactors = [],
  growthIndicators = []
}) => {
  const [config, setConfig] = useState<any>(null);

  useEffect(() => {
    configService.getAllConfig().then(setConfig);
  }, []);

  // Combine and translate all insights
  const allInsights = [
    ...keyInsights,
    ...riskFactors,
    ...growthIndicators
  ].slice(0, config?.displayLimits?.total_insights || 6); // Top insights
  
  const translatedInsights = allInsights.map(translateToBusinessLanguage);
  
  // Separate by type
  const positiveInsights = translatedInsights.filter(i => i.type === 'positive');
  const negativeInsights = translatedInsights.filter(i => i.type === 'negative');
  const neutralInsights = translatedInsights.filter(i => i.type === 'neutral');

  return (
    <div className="business-insights-container">
      <div className="insights-header">
        <h3>Business Analysis</h3>
        <p className="insights-subtitle">Key findings translated to business impact</p>
      </div>

      {positiveInsights.length > 0 && (
        <div className="insights-section strengths">
          <h4>💪 Strengths</h4>
          <div className="insights-grid">
            {positiveInsights.map((insight, index) => (
              <motion.div 
                key={index}
                className="insight-card positive"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.1 }}
              >
                <div className="insight-header">
                  <span className="insight-icon">{insight.icon}</span>
                  <h5>{insight.title}</h5>
                </div>
                <p className="insight-explanation">{insight.explanation}</p>
              </motion.div>
            ))}
          </div>
        </div>
      )}

      {negativeInsights.length > 0 && (
        <div className="insights-section challenges">
          <h4>⚠️ Challenges</h4>
          <div className="insights-grid">
            {negativeInsights.map((insight, index) => (
              <motion.div 
                key={index}
                className="insight-card negative"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.1 }}
              >
                <div className="insight-header">
                  <span className="insight-icon">{insight.icon}</span>
                  <h5>{insight.title}</h5>
                </div>
                <p className="insight-explanation">{insight.explanation}</p>
                {getActionableRecommendation(insight) && (
                  <div className="insight-action">
                    <span className="action-label">Action:</span>
                    <span className="action-text">{getActionableRecommendation(insight)}</span>
                  </div>
                )}
              </motion.div>
            ))}
          </div>
        </div>
      )}

      {neutralInsights.length > 0 && (
        <div className="insights-section considerations">
          <h4>🔍 Key Considerations</h4>
          <div className="insights-grid">
            {neutralInsights.map((insight, index) => (
              <motion.div 
                key={index}
                className="insight-card neutral"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.1 }}
              >
                <div className="insight-header">
                  <span className="insight-icon">{insight.icon}</span>
                  <h5>{insight.title}</h5>
                </div>
                <p className="insight-explanation">{insight.explanation}</p>
              </motion.div>
            ))}
          </div>
        </div>
      )}

      <motion.div 
        className="insights-summary"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.5 }}
      >
        <div className="summary-stats">
          <div className="stat">
            <span className="stat-value">{positiveInsights.length}</span>
            <span className="stat-label">Strengths</span>
          </div>
          <div className="stat">
            <span className="stat-value">{negativeInsights.length}</span>
            <span className="stat-label">Challenges</span>
          </div>
          <div className="stat">
            <span className="stat-value">{neutralInsights.length}</span>
            <span className="stat-label">Considerations</span>
          </div>
        </div>
      </motion.div>
    </div>
  );
};