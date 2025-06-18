import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { apiService } from '../services/api';
import styles from './LLMRecommendationsMinimal.module.scss';

interface LLMRecommendationsMinimalProps {
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

export const LLMRecommendationsMinimalV2: React.FC<LLMRecommendationsMinimalProps> = ({
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
      // Prepare the request in the format the API expects
      const scores = {
        capital: basicResults.scores?.capital || 0,
        advantage: basicResults.scores?.advantage || 0,
        market: basicResults.scores?.market || 0,
        people: basicResults.scores?.people || 0,
        success_probability: basicResults.successProbability || 0
      };
      
      const result = await apiService.getDynamicRecommendations({
        assessment_data: assessmentData,
        ml_results: basicResults,
        startup_data: assessmentData,
        scores: scores
      });
      
      console.log('FLASH Intelligence API Response:', result);
      
      // Map the API response to our component structure
      const mappedRecommendations = result.recommendations.map(rec => ({
        category: rec.category || 'General',
        priority: rec.priority || 'Medium',
        recommendation: rec.action || rec.recommendation || 'No description',
        impact: rec.impact || 'Not specified',
        effort: rec.resources_required || rec.effort || 'Not specified',
        timeline: rec.implementation_time || rec.timeline || 'Not specified'
      }));
      
      setRecommendations(mappedRecommendations);
      setKeyInsights(result.key_focus_areas || result.key_insights || []);
      
      // Create more meaningful action items from recommendations
      const actions = result.recommendations.map((rec, idx) => 
        rec.action || rec.recommendation || `Action ${idx + 1}`
      );
      setActionItems(actions);
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

  return (
    <div className={styles.container}>
      {(!recommendations || recommendations.length === 0) && !isLoading && (
        <motion.div 
          className={styles.prompt}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
        >
          <h3 className={styles.promptTitle}>Activate FLASH Intelligence</h3>
          <p className={styles.promptDescription}>
            Get intelligent, data-driven insights from FLASH's advanced 
            assessment engine tailored to your startup's unique profile.
          </p>
          <button
            className={styles.generateButton}
            onClick={fetchRecommendations}
            disabled={isLoading}
          >
            Generate FLASH Insights
          </button>
        </motion.div>
      )}

      {isLoading && (
        <motion.div 
          className={styles.loading}
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
        >
          <p>FLASH Intelligence analyzing your startup...</p>
        </motion.div>
      )}

      {error && (
        <motion.div 
          className={styles.error}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
        >
          <p>{error}</p>
          <button
            className={styles.retryButton}
            onClick={fetchRecommendations}
          >
            Try Again
          </button>
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
                  <h3 className={styles.sectionTitle}>Key Insights</h3>
                  <div className={styles.insights}>
                    {keyInsights.map((insight, index) => (
                      <motion.div
                        key={index}
                        className={styles.insight}
                        initial={{ opacity: 0, x: -20 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ delay: index * 0.1 }}
                      >
                        {insight}
                      </motion.div>
                    ))}
                  </div>
                </section>
              )}

              {/* Category Filter */}
              {categories.length > 1 && (
                <div className={styles.categoryFilter}>
                  <button
                    className={`${styles.filterButton} ${selectedCategory === null ? styles.active : ''}`}
                    onClick={() => setSelectedCategory(null)}
                  >
                    All ({recommendations.length})
                  </button>
                  {categories.map(category => (
                    <button
                      key={category}
                      className={`${styles.filterButton} ${selectedCategory === category ? styles.active : ''}`}
                      onClick={() => setSelectedCategory(category)}
                    >
                      {category} ({recommendations.filter(r => r.category === category).length})
                    </button>
                  ))}
                </div>
              )}

              {/* Recommendations */}
              <section className={styles.section}>
                <h3 className={styles.sectionTitle}>Strategic Recommendations</h3>
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
                        <span className={styles.recPriority}>
                          {rec.priority} Priority
                        </span>
                      </div>
                      
                      <h4 className={styles.recTitle}>{rec.recommendation}</h4>
                      
                      <div className={styles.recMetrics}>
                        <div className={styles.metric}>
                          <span className={styles.metricLabel}>Impact:</span>
                          <span className={styles.metricValue}>{rec.impact}</span>
                        </div>
                        
                        <div className={styles.metric}>
                          <span className={styles.metricLabel}>Effort:</span>
                          <span className={styles.metricValue}>{rec.effort}</span>
                        </div>
                        
                        <div className={styles.metric}>
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
                  <h3 className={styles.sectionTitle}>Immediate Action Items</h3>
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