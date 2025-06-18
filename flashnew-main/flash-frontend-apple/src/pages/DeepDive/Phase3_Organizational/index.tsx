import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Icon } from '../../../design-system/components';
import SevenSFramework from './SevenSFramework';
import styles from './index.module.scss';

const Phase3Organizational: React.FC = () => {
  const navigate = useNavigate();
  const [completionStatus, setCompletionStatus] = useState({
    sevenS: 0
  });

  useEffect(() => {
    // Check completion status
    const sevenSData = localStorage.getItem('sevenSFrameworkData');
    if (sevenSData) {
      const data = JSON.parse(sevenSData);
      // Calculate completion based on how many dimensions have been assessed
      const dimensions = ['strategy', 'structure', 'systems', 'sharedValues', 'style', 'staff', 'skills'];
      const assessed = dimensions.filter(dim => data[dim]?.current > 0 || data[dim]?.desired > 0).length;
      setCompletionStatus({
        sevenS: Math.round((assessed / dimensions.length) * 100)
      });
    }
  }, []);

  const overallCompletion = completionStatus.sevenS;

  return (
    <div className={styles.container}>
      <div className={styles.header}>
        <motion.button
          className={styles.backButton}
          onClick={() => navigate('/deep-dive')}
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
        >
          <Icon name="arrow.left" size={20} />
          Back to Deep Dive
        </motion.button>
        
        <h1>Phase 3: Organizational Readiness</h1>
        <p>Assess your organization's alignment and readiness for strategic execution</p>
        
        <div className={styles.progressSection}>
          <div className={styles.progressBar}>
            <motion.div
              className={styles.progressFill}
              initial={{ width: 0 }}
              animate={{ width: `${overallCompletion}%` }}
              transition={{ duration: 0.5 }}
            />
          </div>
          <span className={styles.progressText}>{overallCompletion}% Complete</span>
        </div>
      </div>

      <div className={styles.overview}>
        <div className={styles.introCard}>
          <Icon name="building.2" size={32} />
          <h2>McKinsey 7S Framework</h2>
          <p>
            The 7S Framework examines seven interdependent elements that determine organizational effectiveness. 
            When all elements are aligned, your organization is positioned for successful strategy execution.
          </p>
        </div>

        <div className={styles.elementsGrid}>
          <div className={styles.elementCategory}>
            <h3>Hard Elements</h3>
            <div className={styles.elements}>
              <div className={styles.element}>
                <Icon name="target" size={24} />
                <h4>Strategy</h4>
                <p>Plan to achieve competitive advantage</p>
              </div>
              <div className={styles.element}>
                <Icon name="square.grid.3x3" size={24} />
                <h4>Structure</h4>
                <p>How the organization is arranged</p>
              </div>
              <div className={styles.element}>
                <Icon name="gearshape.2" size={24} />
                <h4>Systems</h4>
                <p>Processes and procedures</p>
              </div>
            </div>
          </div>

          <div className={styles.elementCategory}>
            <h3>Soft Elements</h3>
            <div className={styles.elements}>
              <div className={styles.element}>
                <Icon name="heart" size={24} />
                <h4>Shared Values</h4>
                <p>Core beliefs and culture</p>
              </div>
              <div className={styles.element}>
                <Icon name="person.2" size={24} />
                <h4>Style</h4>
                <p>Leadership and management approach</p>
              </div>
              <div className={styles.element}>
                <Icon name="person.3" size={24} />
                <h4>Staff</h4>
                <p>Employees and capabilities</p>
              </div>
              <div className={styles.element}>
                <Icon name="star" size={24} />
                <h4>Skills</h4>
                <p>Core competencies and expertise</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className={styles.content}>
        <SevenSFramework />
      </div>

      <div className={styles.navigation}>
        <motion.button
          className={styles.navButton}
          onClick={() => navigate('/deep-dive/phase2')}
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
        >
          <Icon name="arrow.left" size={16} />
          Previous Phase
        </motion.button>
        
        {overallCompletion === 100 && (
          <motion.button
            className={styles.navButtonPrimary}
            onClick={() => navigate('/deep-dive/phase4')}
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
          >
            Continue to Phase 4
            <Icon name="arrow.right" size={16} />
          </motion.button>
        )}
      </div>
    </div>
  );
};

export default Phase3Organizational;