import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { AnimatePresence } from '../design-system/components/AnimatePresenceWrapper';
import { Icon, Button } from '../design-system/components';
import { apiService } from '../services/api';
import styles from './LLMRecommendations.module.scss';

interface LLMRecommendationsProps {
  assessmentData: any;
  basicResults: any;
}

interface Recommendation {
  category: string;
  priority: string;
  recommendation: string;
  impact: string;
  effort: string;
  timeline: string;
}

export const LLMRecommendations: React.FC<LLMRecommendationsProps> = ({
  assessmentData,
  basicResults
}) => {
  const [isLoading, setIsLoading] = useState(false);
  const [recommendations, setRecommendations] = useState<Recommendation[]>([]);
  const [keyInsights, setKeyInsights] = useState<string[]>([]);
  const [actionItems, setActionItems] = useState<string[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [isExpanded, setIsExpanded] = useState(false);
  const [selectedCategory, setSelectedCategory] = useState<string | null>(null);

  const fetchRecommendations = async () => {
    setIsLoading(true);
    setError(null);
    
    try {
      const result = await apiService.getRecommendations(assessmentData, basicResults);
      setRecommendations(result.recommendations);
      setKeyInsights(result.key_insights);
      setActionItems(result.action_items);
      setIsExpanded(true);
    } catch (err) {
      console.error('Recommendations error:', err);
      setError('Failed to generate recommendations');
    } finally {
      setIsLoading(false);
    }
  };

  const categories = recommendations ? [...new Set(recommendations.map(r => r.category))] : [];
  const filteredRecommendations = selectedCategory && recommendations
    ? recommendations.filter(r => r.category === selectedCategory)
    : recommendations || [];

  const getPriorityColor = (priority: string) => {
    switch (priority.toLowerCase()) {
      case 'critical':
      case 'high':
        return styles.high;
      case 'medium':
        return styles.medium;
      case 'low':
        return styles.low;
      default:
        return '';
    }
  };

  const getEffortLevel = (effort: string) => {
    switch (effort.toLowerCase()) {
      case 'high':
        return { label: 'High Effort', icon: 'exclamationmark.triangle' };
      case 'medium':
        return { label: 'Medium Effort', icon: 'info.circle' };
      case 'low':
        return { label: 'Low Effort', icon: 'checkmark.circle' };
      default:
        return { label: effort, icon: 'circle' };
    }
  };

  return (
    <div className={styles.container}>
      {(!recommendations || recommendations.length === 0) && !isLoading && (
        <motion.div 
          className={styles.prompt}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
        >
          <div className={styles.promptIcon}>
            <Icon name="lightbulb" size={32} />
          </div>
          <h3 className={styles.promptTitle}>Get Personalized Recommendations</h3>
          <p className={styles.promptDescription}>
            Receive AI-powered, actionable recommendations specifically 
            tailored to your startup's unique situation and challenges.
          </p>
          <Button
            variant="primary"
            size="large"
            onClick={fetchRecommendations}
            loading={isLoading}
            icon={<Icon name="arrow.right" />}
          >
            Generate Recommendations
          </Button>
        </motion.div>
      )}

      {isLoading && (
        <motion.div 
          className={styles.loading}
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
        >
          <div className={styles.loadingIcon}>
            <Icon name="arrow.clockwise" size={32} />
          </div>
          <p>Generating personalized recommendations...</p>
        </motion.div>
      )}

      {error && (
        <motion.div 
          className={styles.error}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
        >
          <Icon name="exclamationmark.triangle" size={24} />
          <p>{error}</p>
          <Button
            variant="secondary"
            size="small"
            onClick={fetchRecommendations}
          >
            Try Again
          </Button>
        </motion.div>
      )}

      {recommendations && recommendations.length > 0 && (
        <AnimatePresence>
          {isExpanded && (
            <motion.div 
              className={styles.content}
              initial={{ opacity: 0, height: 0 }}
              animate={{ opacity: 1, height: 'auto' }}
              exit={{ opacity: 0, height: 0 }}
              transition={{ duration: 0.5 }}
            >
              {/* Key Insights */}
              {keyInsights && keyInsights.length > 0 && (
                <section className={styles.section}>
                  <h3 className={styles.sectionTitle}>
                    <Icon name="star" size={20} />
                    Key Insights
                  </h3>
                  <div className={styles.insights}>
                    {keyInsights.map((insight, index) => (
                      <motion.div
                        key={index}
                        className={styles.insight}
                        initial={{ opacity: 0, x: -20 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ delay: index * 0.1 }}
                      >
                        <Icon name="sparkles" size={16} />
                        <p>{insight}</p>
                      </motion.div>
                    ))}
                  </div>
                </section>
              )}

              {/* Category Filter */}
              {categories.length > 1 && (
                <div className={styles.categoryFilter}>
                  <Button
                    variant={selectedCategory === null ? 'primary' : 'secondary'}
                    size="small"
                    onClick={() => setSelectedCategory(null)}
                  >
                    All ({recommendations.length})
                  </Button>
                  {categories.map(category => (
                    <Button
                      key={category}
                      variant={selectedCategory === category ? 'primary' : 'secondary'}
                      size="small"
                      onClick={() => setSelectedCategory(category)}
                    >
                      {category} ({recommendations.filter(r => r.category === category).length})
                    </Button>
                  ))}
                </div>
              )}

              {/* Recommendations */}
              <section className={styles.section}>
                <h3 className={styles.sectionTitle}>
                  <Icon name="lightbulb" size={20} />
                  Strategic Recommendations
                </h3>
                <div className={styles.recommendations}>
                  {filteredRecommendations.map((rec, index) => (
                    <motion.div
                      key={index}
                      className={styles.recommendation}
                      initial={{ opacity: 0, y: 20 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ delay: index * 0.1 }}
                      layout
                    >
                      <div className={styles.recHeader}>
                        <span className={styles.recCategory}>{rec.category}</span>
                        <span className={`${styles.recPriority} ${getPriorityColor(rec.priority)}`}>
                          {rec.priority} Priority
                        </span>
                      </div>
                      
                      <h4 className={styles.recTitle}>{rec.recommendation}</h4>
                      
                      <div className={styles.recMetrics}>
                        <div className={styles.metric}>
                          <Icon name="chart.line.uptrend" size={16} />
                          <span className={styles.metricLabel}>Impact:</span>
                          <span className={styles.metricValue}>{rec.impact}</span>
                        </div>
                        
                        <div className={styles.metric}>
                          <Icon name={getEffortLevel(rec.effort).icon} size={16} />
                          <span className={styles.metricLabel}>Effort:</span>
                          <span className={styles.metricValue}>{getEffortLevel(rec.effort).label}</span>
                        </div>
                        
                        <div className={styles.metric}>
                          <Icon name="clock" size={16} />
                          <span className={styles.metricLabel}>Timeline:</span>
                          <span className={styles.metricValue}>{rec.timeline}</span>
                        </div>
                      </div>
                    </motion.div>
                  ))}
                </div>
              </section>

              {/* Action Items */}
              {actionItems && actionItems.length > 0 && (
                <section className={styles.section}>
                  <h3 className={styles.sectionTitle}>
                    <Icon name="checkmark.circle" size={20} />
                    Immediate Action Items
                  </h3>
                  <div className={styles.actionItems}>
                    {actionItems.map((item, index) => (
                      <motion.div
                        key={index}
                        className={styles.actionItem}
                        initial={{ opacity: 0, x: -20 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ delay: index * 0.1 }}
                      >
                        <div className={styles.actionNumber}>{index + 1}</div>
                        <p>{item}</p>
                      </motion.div>
                    ))}
                  </div>
                </section>
              )}
            </motion.div>
          )}
        </AnimatePresence>
      )}
    </div>
  );
};