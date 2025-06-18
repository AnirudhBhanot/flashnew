import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Icon, Button } from '../design-system/components';
import { apiService } from '../services/api';
import styles from './EnhancedAnalysis.module.scss';

interface EnhancedAnalysisProps {
  assessmentData: any;
  basicResults: any;
}

export const EnhancedAnalysis: React.FC<EnhancedAnalysisProps> = ({
  assessmentData,
  basicResults
}) => {
  const [isLoading, setIsLoading] = useState(false);
  const [analysis, setAnalysis] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);
  const [isExpanded, setIsExpanded] = useState(false);

  const fetchEnhancedAnalysis = async () => {
    setIsLoading(true);
    setError(null);
    
    try {
      const result = await apiService.analyze(assessmentData);
      setAnalysis(result);
      setIsExpanded(true);
    } catch (err) {
      console.error('Enhanced analysis error:', err);
      setError('Failed to generate enhanced analysis');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className={styles.container}>
      {!analysis && !isLoading && (
        <motion.div 
          className={styles.prompt}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
        >
          <div className={styles.promptIcon}>
            <Icon name="sparkles" size={32} />
          </div>
          <h3 className={styles.promptTitle}>Get Deeper Insights</h3>
          <p className={styles.promptDescription}>
            Unlock AI-powered analysis with specific recommendations, 
            risk assessments, and actionable insights tailored to your startup.
          </p>
          <Button
            variant="primary"
            size="large"
            onClick={fetchEnhancedAnalysis}
            loading={isLoading}
            icon={<Icon name="arrow.right" />}
          >
            Generate Enhanced Analysis
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
          <p>Analyzing your startup with advanced AI models...</p>
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
            onClick={fetchEnhancedAnalysis}
          >
            Try Again
          </Button>
        </motion.div>
      )}

      {analysis && (
        <motion.div 
          className={styles.analysisContent}
          initial={{ opacity: 0, height: 0 }}
          animate={{ 
            opacity: isExpanded ? 1 : 0, 
            height: isExpanded ? 'auto' : 0 
          }}
          transition={{ duration: 0.5 }}
        >
          {/* Overall Assessment */}
          {analysis.overall_assessment && (
            <section className={styles.section}>
              <h3 className={styles.sectionTitle}>
                <Icon name="chart.line.uptrend" size={20} />
                Overall Assessment
              </h3>
              <p className={styles.assessment}>{analysis.overall_assessment}</p>
            </section>
          )}

          {/* Strengths */}
          {analysis.strengths && analysis.strengths.length > 0 && (
            <section className={styles.section}>
              <h3 className={styles.sectionTitle}>
                <Icon name="checkmark.circle" size={20} />
                Key Strengths
              </h3>
              <ul className={styles.list}>
                {analysis.strengths.map((strength: string, index: number) => (
                  <li key={index} className={styles.strengthItem}>
                    <Icon name="checkmark" size={16} />
                    {strength}
                  </li>
                ))}
              </ul>
            </section>
          )}

          {/* Risks */}
          {analysis.risks && analysis.risks.length > 0 && (
            <section className={styles.section}>
              <h3 className={styles.sectionTitle}>
                <Icon name="exclamationmark.triangle" size={20} />
                Risk Factors
              </h3>
              <ul className={styles.list}>
                {analysis.risks.map((risk: any, index: number) => (
                  <li key={index} className={styles.riskItem}>
                    <div className={styles.riskHeader}>
                      <Icon name="exclamationmark.circle" size={16} />
                      <span className={styles.riskTitle}>{risk.factor}</span>
                      <span className={`${styles.riskLevel} ${styles[risk.level]}`}>
                        {risk.level}
                      </span>
                    </div>
                    <p className={styles.riskDescription}>{risk.description}</p>
                  </li>
                ))}
              </ul>
            </section>
          )}

          {/* Recommendations */}
          {analysis.recommendations && analysis.recommendations.length > 0 && (
            <section className={styles.section}>
              <h3 className={styles.sectionTitle}>
                <Icon name="lightbulb" size={20} />
                Strategic Recommendations
              </h3>
              <div className={styles.recommendations}>
                {analysis.recommendations.map((rec: any, index: number) => (
                  <motion.div 
                    key={index} 
                    className={styles.recommendation}
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: index * 0.1 }}
                  >
                    <div className={styles.recHeader}>
                      <span className={styles.recNumber}>{index + 1}</span>
                      <h4 className={styles.recTitle}>{rec.title}</h4>
                      <span className={`${styles.recPriority} ${styles[rec.priority]}`}>
                        {rec.priority} priority
                      </span>
                    </div>
                    <p className={styles.recDescription}>{rec.description}</p>
                    {rec.impact && (
                      <p className={styles.recImpact}>
                        <strong>Expected Impact:</strong> {rec.impact}
                      </p>
                    )}
                  </motion.div>
                ))}
              </div>
            </section>
          )}

          {/* Market Opportunities */}
          {analysis.market_opportunities && analysis.market_opportunities.length > 0 && (
            <section className={styles.section}>
              <h3 className={styles.sectionTitle}>
                <Icon name="star" size={20} />
                Market Opportunities
              </h3>
              <ul className={styles.list}>
                {analysis.market_opportunities.map((opp: string, index: number) => (
                  <li key={index} className={styles.opportunityItem}>
                    <Icon name="arrow.right.circle" size={16} />
                    {opp}
                  </li>
                ))}
              </ul>
            </section>
          )}

          {/* Competitive Positioning */}
          {analysis.competitive_positioning && (
            <section className={styles.section}>
              <h3 className={styles.sectionTitle}>
                <Icon name="flag" size={20} />
                Competitive Positioning
              </h3>
              <p className={styles.positioning}>{analysis.competitive_positioning}</p>
            </section>
          )}

          {/* Next Steps */}
          {analysis.next_steps && analysis.next_steps.length > 0 && (
            <section className={styles.section}>
              <h3 className={styles.sectionTitle}>
                <Icon name="arrow.right.square" size={20} />
                Immediate Next Steps
              </h3>
              <ol className={styles.nextSteps}>
                {analysis.next_steps.map((step: string, index: number) => (
                  <li key={index}>{step}</li>
                ))}
              </ol>
            </section>
          )}
        </motion.div>
      )}
    </div>
  );
};