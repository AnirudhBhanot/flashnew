import React from 'react';
import { Icon } from '../design-system/components';
import styles from './EnhancedInsights.module.scss';

interface EnhancedInsightsProps {
  scores: {
    capital?: number;
    advantage?: number;
    market?: number;
    people?: number;
  };
  probability: number;
}

export const EnhancedInsights: React.FC<EnhancedInsightsProps> = ({ scores, probability }) => {
  const generateInsights = () => {
    const insights = [];
    
    // Capital insights
    if (scores.capital) {
      if (scores.capital >= 0.7) {
        insights.push({
          type: 'strength',
          category: 'Capital',
          text: 'Strong financial position with healthy runway and burn rate'
        });
      } else if (scores.capital < 0.4) {
        insights.push({
          type: 'risk',
          category: 'Capital',
          text: 'Limited runway may require immediate fundraising'
        });
      }
    }
    
    // Advantage insights
    if (scores.advantage) {
      if (scores.advantage >= 0.7) {
        insights.push({
          type: 'strength',
          category: 'Advantage',
          text: 'Clear competitive moat with strong differentiation'
        });
      } else if (scores.advantage < 0.4) {
        insights.push({
          type: 'risk',
          category: 'Advantage',
          text: 'Weak competitive positioning in a crowded market'
        });
      }
    }
    
    // Market insights
    if (scores.market) {
      if (scores.market >= 0.7) {
        insights.push({
          type: 'strength',
          category: 'Market',
          text: 'Large addressable market with strong growth potential'
        });
      } else if (scores.market < 0.4) {
        insights.push({
          type: 'risk',
          category: 'Market',
          text: 'Limited market opportunity or intense competition'
        });
      }
    }
    
    // People insights
    if (scores.people) {
      if (scores.people >= 0.7) {
        insights.push({
          type: 'strength',
          category: 'People',
          text: 'Experienced team with proven track record'
        });
      } else if (scores.people < 0.4) {
        insights.push({
          type: 'risk',
          category: 'People',
          text: 'Team lacks relevant experience or depth'
        });
      }
    }
    
    // Overall insights
    if (probability >= 0.7) {
      insights.push({
        type: 'overall',
        category: 'Overall',
        text: 'This startup shows strong fundamentals across multiple dimensions'
      });
    } else if (probability < 0.3) {
      insights.push({
        type: 'overall',
        category: 'Overall',
        text: 'Multiple risk factors suggest challenging path to success'
      });
    }
    
    return insights;
  };
  
  const generateRecommendations = () => {
    const recommendations = [];
    
    if (scores.capital && scores.capital < 0.5) {
      recommendations.push('Extend runway by reducing burn rate or raising additional capital');
    }
    
    if (scores.advantage && scores.advantage < 0.5) {
      recommendations.push('Focus on building stronger competitive advantages and IP protection');
    }
    
    if (scores.market && scores.market < 0.5) {
      recommendations.push('Refine go-to-market strategy and target customer segments');
    }
    
    if (scores.people && scores.people < 0.5) {
      recommendations.push('Strengthen team with experienced advisors or key hires');
    }
    
    if (probability >= 0.5 && probability < 0.7) {
      recommendations.push('Address identified weaknesses to improve success probability');
    }
    
    return recommendations;
  };
  
  const insights = generateInsights();
  const recommendations = generateRecommendations();
  
  return (
    <div className={styles.container}>
      {insights.length > 0 && (
        <div className={styles.section}>
          <h3 className={styles.sectionTitle}>
            <Icon name="sparkles" size={20} />
            Key Insights
          </h3>
          <div className={styles.insights}>
            {insights.map((insight, index) => (
              <div 
                key={index} 
                className={`${styles.insight} ${styles[insight.type]}`}
              >
                <Icon 
                  name={insight.type === 'strength' ? 'checkmark.circle' : 'exclamationmark.triangle'} 
                  size={16} 
                />
                <div>
                  <span className={styles.category}>{insight.category}:</span>
                  <span className={styles.text}>{insight.text}</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
      
      {recommendations.length > 0 && (
        <div className={styles.section}>
          <h3 className={styles.sectionTitle}>
            <Icon name="lightbulb" size={20} />
            Recommendations
          </h3>
          <ul className={styles.recommendations}>
            {recommendations.map((rec, index) => (
              <li key={index} className={styles.recommendation}>
                <Icon name="arrow.right" size={14} />
                <span>{rec}</span>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};