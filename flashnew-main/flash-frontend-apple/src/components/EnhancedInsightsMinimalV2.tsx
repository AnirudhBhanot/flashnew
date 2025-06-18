import React from 'react';
import styles from './EnhancedInsightsMinimal.module.scss';

interface EnhancedInsightsMinimalProps {
  scores: {
    capital?: number;
    advantage?: number;
    market?: number;
    people?: number;
  };
  probability: number;
}

export const EnhancedInsightsMinimalV2: React.FC<EnhancedInsightsMinimalProps> = ({ scores, probability }) => {
  const generateInsights = () => {
    const insights = [];
    
    // Capital insights
    if (scores.capital) {
      if (scores.capital >= 0.7) {
        insights.push({
          category: 'Capital',
          text: 'Strong financial position with healthy runway and burn rate'
        });
      } else if (scores.capital < 0.4) {
        insights.push({
          category: 'Capital',
          text: 'Limited runway may require immediate fundraising'
        });
      }
    }
    
    // Advantage insights
    if (scores.advantage) {
      if (scores.advantage >= 0.7) {
        insights.push({
          category: 'Advantage',
          text: 'Clear competitive moat with strong differentiation'
        });
      } else if (scores.advantage < 0.4) {
        insights.push({
          category: 'Advantage',
          text: 'Weak competitive positioning in a crowded market'
        });
      }
    }
    
    // Market insights
    if (scores.market) {
      if (scores.market >= 0.7) {
        insights.push({
          category: 'Market',
          text: 'Large addressable market with strong growth potential'
        });
      } else if (scores.market < 0.4) {
        insights.push({
          category: 'Market',
          text: 'Limited market opportunity or intense competition'
        });
      }
    }
    
    // People insights
    if (scores.people) {
      if (scores.people >= 0.7) {
        insights.push({
          category: 'People',
          text: 'Experienced team with proven track record'
        });
      } else if (scores.people < 0.4) {
        insights.push({
          category: 'People',
          text: 'Team lacks relevant experience or depth'
        });
      }
    }
    
    // Overall insights
    if (probability >= 0.7) {
      insights.push({
        category: 'Overall',
        text: 'This startup shows strong fundamentals across multiple dimensions'
      });
    } else if (probability < 0.3) {
      insights.push({
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
          <h3 className={styles.sectionTitle}>Key Insights</h3>
          <div className={styles.insights}>
            {insights.map((insight, index) => (
              <div key={index} className={styles.insight}>
                <span className={styles.category}>{insight.category}</span>
                <span className={styles.text}>{insight.text}</span>
              </div>
            ))}
          </div>
        </div>
      )}
      
      {recommendations.length > 0 && (
        <div className={styles.section}>
          <h3 className={styles.sectionTitle}>Recommendations</h3>
          <ul className={styles.recommendations}>
            {recommendations.map((rec, index) => (
              <li key={index} className={styles.recommendation}>
                {rec}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};