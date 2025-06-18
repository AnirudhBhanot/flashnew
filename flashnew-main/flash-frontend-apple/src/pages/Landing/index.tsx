import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import { ProgressRecovery } from '../../components/ProgressRecovery';
import useAssessmentStore from '../../store/assessmentStore';
import styles from './Landing.module.scss';

const Landing: React.FC = () => {
  const navigate = useNavigate();
  const { data, getCompletionStatus, resetAssessment } = useAssessmentStore();
  const [showRecovery, setShowRecovery] = useState(false);
  
  useEffect(() => {
    // Check if there's saved progress
    const status = getCompletionStatus();
    if (status.completedSteps > 0 && !status.isComplete) {
      setShowRecovery(true);
    }
  }, [getCompletionStatus]);
  
  const handleContinue = () => {
    // Navigate to the next incomplete section
    if (!data.companyInfo) {
      navigate('/assessment/company');
    } else if (!data.capital) {
      navigate('/assessment/capital');
    } else if (!data.advantage) {
      navigate('/assessment/advantage');
    } else if (!data.market) {
      navigate('/assessment/market');
    } else if (!data.people) {
      navigate('/assessment/people');
    } else {
      navigate('/assessment/review');
    }
  };
  
  const handleStartNew = () => {
    resetAssessment();
    setShowRecovery(false);
    navigate('/assessment/company');
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLDivElement>) => {
    if (e.key === 'Enter') {
      e.preventDefault();
      if (showRecovery) {
        handleContinue();
      } else {
        navigate('/assessment/company');
      }
    }
  };

  return (
    <div className={styles.page} onKeyDown={handleKeyDown}>
      {/* Minimal Navigation */}
      <motion.nav 
        className={styles.nav}
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 1, ease: [0.25, 0, 0, 1] }}
      >
        <motion.h1 
          className={styles.logo}
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ 
            duration: 0.8,
            delay: 0.2,
            ease: [0.25, 0, 0, 1]
          }}
        >
          FLASH
        </motion.h1>
      </motion.nav>

      {/* Hero Section */}
      <section className={styles.hero}>
        {showRecovery ? (
          <motion.div 
            className={styles.recoveryContainer}
            initial={{ opacity: 0, y: 40 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, ease: [0.25, 0, 0, 1] }}
          >
            <ProgressRecovery
              onContinue={handleContinue}
              onStartNew={handleStartNew}
            />
          </motion.div>
        ) : (
          <motion.div 
            className={styles.heroContent}
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 1.2, ease: [0.25, 0, 0, 1] }}
          >
            <motion.h1 
              className={styles.title}
              initial={{ opacity: 0, y: 60 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 1, delay: 0.2, ease: [0.25, 0, 0, 1] }}
            >
              Know your startup's
              <br />
              true potential
            </motion.h1>
            
            <motion.p 
              className={styles.subtitle}
              initial={{ opacity: 0, y: 40 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 1, delay: 0.4, ease: [0.25, 0, 0, 1] }}
            >
              An honest assessment powered by data from 100,000+ startups
            </motion.p>
            
            <motion.div 
              className={styles.action}
              initial={{ opacity: 0, y: 40 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 1, delay: 0.6, ease: [0.25, 0, 0, 1] }}
            >
              <button
                className={styles.startButton}
                onClick={() => navigate('/assessment/company')}
              >
                Begin
                <span className={styles.shortcut}>Press Enter</span>
              </button>
            </motion.div>
          </motion.div>
        )}
      </section>
    </div>
  );
};

export default Landing;