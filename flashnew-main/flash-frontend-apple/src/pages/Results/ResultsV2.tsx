import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import useAssessmentStore from '../../store/assessmentStore';
import { Button, Icon } from '../../design-system/components';
import styles from './ResultsV2.module.scss';

const ResultsV2: React.FC = () => {
  const navigate = useNavigate();
  const { results, resetAssessment, data } = useAssessmentStore();
  const [showDetails, setShowDetails] = useState(false);
  const [showScores, setShowScores] = useState(false);

  useEffect(() => {
    if (!results) {
      navigate('/');
    }
  }, [results, navigate]);

  if (!results) return null;

  const successProbability = Math.round((results.successProbability || 0) * 100);
  const scores = results.scores || {
    capital: 0,
    advantage: 0,
    market: 0,
    people: 0
  };

  const getVerdict = () => {
    if (successProbability >= 70) return 'Recommended';
    if (successProbability >= 50) return 'Promising';
    return 'High Risk';
  };

  const getVerdictDescription = () => {
    if (successProbability >= 70) {
      return 'Strong fundamentals. Proceed with confidence.';
    }
    if (successProbability >= 50) {
      return 'Good potential. Address key gaps first.';
    }
    return 'Significant challenges. Reconsider approach.';
  };

  return (
    <div className={styles.container}>
      {/* Minimal Navigation */}
      <nav className={styles.nav}>
        <button 
          className={styles.backButton}
          onClick={() => navigate('/')}
        >
          <Icon name="chevron.left" size={20} />
        </button>
      </nav>

      {/* Main Content */}
      <div className={styles.content}>
        {/* Hero Number */}
        <motion.div 
          className={styles.hero}
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 1 }}
        >
          <motion.div 
            className={styles.probability}
            initial={{ scale: 0.8, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            transition={{ delay: 0.2, duration: 0.8, type: "spring" }}
          >
            <span className={styles.number}>{successProbability}</span>
            <span className={styles.percent}>%</span>
          </motion.div>

          <motion.p 
            className={styles.label}
            initial={{ y: 20, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ delay: 0.5, duration: 0.6 }}
          >
            Success Probability
          </motion.p>

          <motion.div 
            className={styles.verdict}
            initial={{ y: 20, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ delay: 0.7, duration: 0.6 }}
          >
            <h2>{getVerdict()}</h2>
            <p>{getVerdictDescription()}</p>
          </motion.div>
        </motion.div>

        {/* Progressive Disclosure - Details */}
        <motion.div 
          className={styles.details}
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 1, duration: 0.6 }}
        >
          {!showDetails && (
            <button 
              className={styles.showMore}
              onClick={() => setShowDetails(true)}
            >
              View Analysis
            </button>
          )}

          <AnimatePresence>
            {showDetails && (
              <motion.div
                initial={{ height: 0, opacity: 0 }}
                animate={{ height: "auto", opacity: 1 }}
                exit={{ height: 0, opacity: 0 }}
                transition={{ duration: 0.6 }}
                className={styles.detailsContent}
              >
                {/* CAMP Scores - Minimal */}
                <div className={styles.scores}>
                  <h3>Key Metrics</h3>
                  <div className={styles.scoreGrid}>
                    <div className={styles.scoreItem}>
                      <span className={styles.scoreLabel}>Capital</span>
                      <span className={styles.scoreValue}>{Math.round(scores.capital * 100)}</span>
                    </div>
                    <div className={styles.scoreItem}>
                      <span className={styles.scoreLabel}>Advantage</span>
                      <span className={styles.scoreValue}>{Math.round(scores.advantage * 100)}</span>
                    </div>
                    <div className={styles.scoreItem}>
                      <span className={styles.scoreLabel}>Market</span>
                      <span className={styles.scoreValue}>{Math.round(scores.market * 100)}</span>
                    </div>
                    <div className={styles.scoreItem}>
                      <span className={styles.scoreLabel}>People</span>
                      <span className={styles.scoreValue}>{Math.round(scores.people * 100)}</span>
                    </div>
                  </div>
                </div>

                {/* Single Key Insight */}
                {results.insights && results.insights.length > 0 && (
                  <div className={styles.insight}>
                    <h3>Primary Insight</h3>
                    <p>{results.insights[0]}</p>
                  </div>
                )}

                {/* Minimal Actions */}
                <div className={styles.actions}>
                  <Button
                    variant="primary"
                    size="large"
                    onClick={() => setShowScores(!showScores)}
                  >
                    {showScores ? 'Hide' : 'View'} Full Report
                  </Button>
                </div>

                {/* Full Scores - Hidden by Default */}
                <AnimatePresence>
                  {showScores && (
                    <motion.div
                      initial={{ opacity: 0, y: 20 }}
                      animate={{ opacity: 1, y: 0 }}
                      exit={{ opacity: 0, y: 20 }}
                      transition={{ duration: 0.4 }}
                      className={styles.fullReport}
                    >
                      <div className={styles.reportSection}>
                        <h4>Detailed Analysis</h4>
                        <p className={styles.reportText}>
                          Your startup shows a {successProbability}% probability of success based on our comprehensive analysis. 
                          {successProbability >= 70 ? ' The fundamentals are strong, with particularly good scores in market opportunity and team composition.' : 
                           successProbability >= 50 ? ' There are promising indicators, but some areas need attention before moving forward.' :
                           ' Several critical areas need improvement before this venture can be considered investment-ready.'}
                        </p>
                      </div>

                      {results.recommendations && results.recommendations.length > 0 && (
                        <div className={styles.reportSection}>
                          <h4>Next Steps</h4>
                          <ol className={styles.recommendations}>
                            {results.recommendations.slice(0, 3).map((rec, index) => (
                              <li key={index}>{rec}</li>
                            ))}
                          </ol>
                        </div>
                      )}

                      <div className={styles.reportActions}>
                        <Button
                          variant="secondary"
                          size="medium"
                          icon={<Icon name="square.and.arrow.down" />}
                          onClick={() => {
                            const report = { 
                              date: new Date().toISOString(),
                              company: data.companyInfo?.companyName || 'Unknown',
                              successProbability,
                              scores,
                              verdict: getVerdict()
                            };
                            const blob = new Blob([JSON.stringify(report, null, 2)], { type: 'application/json' });
                            const url = URL.createObjectURL(blob);
                            const a = document.createElement('a');
                            a.href = url;
                            a.download = `flash-assessment-${new Date().toISOString().split('T')[0]}.json`;
                            a.click();
                            URL.revokeObjectURL(url);
                          }}
                        >
                          Export
                        </Button>
                        <Button
                          variant="text"
                          size="medium"
                          onClick={() => {
                            resetAssessment();
                            navigate('/');
                          }}
                        >
                          New Assessment
                        </Button>
                      </div>
                    </motion.div>
                  )}
                </AnimatePresence>
              </motion.div>
            )}
          </AnimatePresence>
        </motion.div>
      </div>
    </div>
  );
};

export default ResultsV2;