import React, { useState, useRef, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import { useWizard } from '../../../features/wizard/WizardProvider';
import useAssessmentStore from '../../../store/assessmentStore';
import { MinimalProgress } from '../../../design-system/minimalist';
import { AutoSaveIndicator } from '../../../components/AutoSaveIndicator';
import { apiService } from '../../../services/api';
import styles from './ReviewMinimal.module.scss';

const ReviewMinimal: React.FC = () => {
  const { previousStep, data } = useWizard();
  const { submitAssessment, setResults } = useAssessmentStore();
  const navigate = useNavigate();
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [currentView, setCurrentView] = useState(0);
  const [showConfirmation, setShowConfirmation] = useState(false);
  const contentRef = useRef<HTMLDivElement>(null);

  // Key metrics calculation
  const getKeyMetrics = () => {
    const metrics = [];
    
    if (data.capital?.totalRaised) {
      const amount = typeof data.capital.totalRaised === 'string' 
        ? parseFloat(data.capital.totalRaised) 
        : data.capital.totalRaised;
      metrics.push({
        label: 'Total Raised',
        value: new Intl.NumberFormat('en-US', {
          style: 'currency',
          currency: 'USD',
          minimumFractionDigits: 0,
          maximumFractionDigits: 0,
          notation: amount >= 1000000 ? 'compact' : 'standard'
        }).format(amount)
      });
    }
    
    if (data.market?.tam) {
      const tam = typeof data.market.tam === 'string' 
        ? parseFloat(data.market.tam) 
        : data.market.tam;
      metrics.push({
        label: 'Market Size',
        value: new Intl.NumberFormat('en-US', {
          style: 'currency',
          currency: 'USD',
          minimumFractionDigits: 0,
          maximumFractionDigits: 0,
          notation: tam >= 1000000 ? 'compact' : 'standard'
        }).format(tam)
      });
    }
    
    if (data.people?.teamSize) {
      metrics.push({
        label: 'Team',
        value: `${data.people.teamSize} people`
      });
    }
    
    if (data.companyInfo?.stage) {
      metrics.push({
        label: 'Stage',
        value: data.companyInfo.stage.replace(/[-_]/g, ' ').replace(/\b\w/g, (l: string) => l.toUpperCase())
      });
    }
    
    return metrics;
  };

  const views = [
    {
      title: data.companyInfo?.companyName || 'Your Startup',
      subtitle: 'Everything looks ready',
      metrics: getKeyMetrics(),
      type: 'summary'
    },
    {
      title: 'Ready to submit?',
      subtitle: 'Your assessment will be analyzed',
      type: 'confirm'
    }
  ];

  const handleSubmit = async () => {
    setIsSubmitting(true);
    setError(null);
    
    try {
      submitAssessment();
      
      const prediction = await apiService.predict(data);
      
      setResults({
        successProbability: prediction.success_probability,
        confidence: prediction.confidence,
        scores: prediction.camp_scores,
        insights: prediction.insights,
        recommendations: []
      });
      
      navigate('/analysis');
    } catch (error) {
      console.error('Submission error:', error);
      setError(error instanceof Error ? error.message : 'Failed to submit assessment');
      setIsSubmitting(false);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && e.metaKey && !isSubmitting && currentView === 1) {
      handleSubmit();
    }
  };

  const nextView = () => {
    if (currentView < views.length - 1) {
      setCurrentView(currentView + 1);
    }
  };

  const prevView = () => {
    if (currentView > 0) {
      setCurrentView(currentView - 1);
    }
  };

  return (
    <div className={styles.page} onKeyDown={handleKeyDown}>
      <motion.nav 
        className={styles.nav}
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6, ease: [0.25, 0, 0, 1] }}
      >
        <button 
          className={styles.backButton}
          onClick={currentView === 0 ? previousStep : prevView}
          disabled={isSubmitting}
        >
          <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
            <path d="M12 4L6 10L12 16" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
          </svg>
        </button>
        
        <div className={styles.progress}>
          <MinimalProgress current={6} total={6} />
        </div>
        
        <div className={styles.placeholder} />
      </motion.nav>
      
      <div className={styles.content} ref={contentRef}>
        <AnimatePresence mode="wait">
          {views[currentView].type === 'summary' ? (
            <motion.div
              key="summary"
              className={styles.summaryView}
              initial={{ opacity: 0, y: 40 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -40 }}
              transition={{ duration: 0.8, ease: [0.25, 0, 0, 1] }}
            >
              <h1 className={styles.title}>{views[currentView].title}</h1>
              <p className={styles.subtitle}>{views[currentView].subtitle}</p>
              
              <div className={styles.metrics}>
                {views[currentView].metrics?.map((metric, index) => (
                  <motion.div
                    key={index}
                    className={styles.metric}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: index * 0.1, duration: 0.6 }}
                  >
                    <span className={styles.metricValue}>{metric.value}</span>
                    <span className={styles.metricLabel}>{metric.label}</span>
                  </motion.div>
                ))}
              </div>
              
              <motion.button
                className={styles.reviewButton}
                onClick={nextView}
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: 0.6, duration: 0.6 }}
              >
                Review & Submit
              </motion.button>
            </motion.div>
          ) : (
            <motion.div
              key="confirm"
              className={styles.confirmView}
              initial={{ opacity: 0, y: 40 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -40 }}
              transition={{ duration: 0.8, ease: [0.25, 0, 0, 1] }}
            >
              <h1 className={styles.title}>{views[currentView].title}</h1>
              <p className={styles.subtitle}>{views[currentView].subtitle}</p>
              
              {error && (
                <motion.div 
                  className={styles.error}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                >
                  <p>{error}</p>
                </motion.div>
              )}
              
              <motion.div
                className={styles.submitActions}
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: 0.4, duration: 0.6 }}
              >
                <button 
                  className={styles.submitButton}
                  onClick={handleSubmit}
                  disabled={isSubmitting}
                >
                  {isSubmitting ? (
                    <>
                      <div className={styles.spinner} />
                      <span>Analyzing...</span>
                    </>
                  ) : (
                    <>
                      Submit Assessment
                      <span className={styles.shortcut}>⌘ Enter</span>
                    </>
                  )}
                </button>
                
                <p className={styles.disclaimer}>
                  By submitting, you confirm all information is accurate
                </p>
              </motion.div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </div>
  );
};

export default ReviewMinimal;