import React from 'react';
import { motion } from 'framer-motion';
import { Button, Icon } from '../design-system/components';
import useAssessmentStore from '../store/assessmentStore';
import styles from './ProgressRecovery.module.scss';

interface ProgressRecoveryProps {
  onContinue: () => void;
  onStartNew: () => void;
}

export const ProgressRecovery: React.FC<ProgressRecoveryProps> = ({
  onContinue,
  onStartNew
}) => {
  const { getCompletionStatus, data } = useAssessmentStore();
  const status = getCompletionStatus();
  
  const getSectionName = () => {
    if (!data.capital) return 'Capital & Financials';
    if (!data.advantage) return 'Competitive Advantage';
    if (!data.market) return 'Market Analysis';
    if (!data.people) return 'Team & Leadership';
    return 'Review';
  };
  
  return (
    <motion.div
      className={styles.container}
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
    >
      <div className={styles.icon}>
        <Icon name="arrow.clockwise" size={32} />
      </div>
      
      <h2 className={styles.title}>Welcome back!</h2>
      <p className={styles.subtitle}>
        You have an assessment in progress
      </p>
      
      <div className={styles.progress}>
        <div className={styles.progressBar}>
          <motion.div
            className={styles.progressFill}
            initial={{ width: 0 }}
            animate={{ width: `${status.percentage}%` }}
            transition={{ duration: 0.8, ease: 'easeOut' }}
          />
        </div>
        <p className={styles.progressText}>
          {status.completedSteps} of {status.totalSteps} sections completed
        </p>
      </div>
      
      <div className={styles.info}>
        <div className={styles.infoItem}>
          <Icon name="building" size={20} />
          <span>{data.companyInfo?.companyName || 'Your Company'}</span>
        </div>
        <div className={styles.infoItem}>
          <Icon name="arrow.right" size={20} />
          <span>Next: {getSectionName()}</span>
        </div>
      </div>
      
      <div className={styles.actions}>
        <Button
          variant="primary"
          size="large"
          onClick={onContinue}
          fullWidth
        >
          Continue Assessment
        </Button>
        <Button
          variant="secondary"
          size="large"
          onClick={onStartNew}
          fullWidth
        >
          Start New Assessment
        </Button>
      </div>
    </motion.div>
  );
};