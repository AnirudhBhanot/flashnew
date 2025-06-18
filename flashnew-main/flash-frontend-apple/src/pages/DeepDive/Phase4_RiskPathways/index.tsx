import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Icon } from '../../../design-system/components';
import ScenarioPlanning from './ScenarioPlanning';
import styles from './index.module.scss';

const Phase4RiskPathways: React.FC = () => {
  const navigate = useNavigate();
  const [completionStatus, setCompletionStatus] = useState({
    scenarioPlanning: 0
  });

  useEffect(() => {
    // Check completion status
    const scenarioData = localStorage.getItem('scenarioPlanningData');
    if (scenarioData) {
      const data = JSON.parse(scenarioData);
      // Calculate completion based on scenario completeness
      let completion = 0;
      
      // Check if scenarios have been customized
      if (data.scenarios && data.scenarios.length >= 3) {
        completion += 30;
      }
      
      // Check if sensitivity parameters have been adjusted
      if (data.sensitivityParams) {
        completion += 20;
      }
      
      // Check if Monte Carlo has been run
      if (data.monteCarloResults && data.monteCarloResults.length > 0) {
        completion += 25;
      }
      
      // Check if contingency plans exist
      if (data.contingencyPlans && data.contingencyPlans.length > 0) {
        completion += 25;
      }
      
      setCompletionStatus({
        scenarioPlanning: completion
      });
    }
  }, []);

  const overallCompletion = completionStatus.scenarioPlanning;

  const handleScenarioComplete = (data: any) => {
    // Save to localStorage
    localStorage.setItem('scenarioPlanningData', JSON.stringify(data));
    
    // Update completion status
    setCompletionStatus({
      scenarioPlanning: 100
    });
  };


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
        
        <h1>Phase 4: Risk-Weighted Pathways</h1>
        <p>Plan for multiple futures and make risk-informed strategic decisions</p>
        
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
          <Icon name="chart.line.uptrend.xyaxis" size={32} />
          <h2>Scenario Planning & Risk Analysis</h2>
          <p>
            Use Monte Carlo simulations and scenario planning to understand the range of possible outcomes 
            for your startup. Make strategic decisions based on probabilities, not just possibilities.
          </p>
        </div>

        <div className={styles.methodologyGrid}>
          <div className={styles.methodCard}>
            <Icon name="dice" size={24} />
            <h3>Monte Carlo Simulation</h3>
            <p>Run thousands of simulations to understand the probability distribution of outcomes</p>
          </div>
          
          <div className={styles.methodCard}>
            <Icon name="slider.horizontal.3" size={24} />
            <h3>Sensitivity Analysis</h3>
            <p>Identify which variables have the greatest impact on your success</p>
          </div>
          
          <div className={styles.methodCard}>
            <Icon name="tree" size={24} />
            <h3>Decision Trees</h3>
            <p>Map out strategic choices and their expected values</p>
          </div>
          
          <div className={styles.methodCard}>
            <Icon name="exclamationmark.shield" size={24} />
            <h3>Contingency Planning</h3>
            <p>Prepare action plans for different scenarios</p>
          </div>
        </div>

        <div className={styles.benefitsSection}>
          <h3>Why Scenario Planning Matters</h3>
          <div className={styles.benefits}>
            <div className={styles.benefit}>
              <Icon name="checkmark.circle.fill" size={20} />
              <span>Reduce uncertainty through probabilistic thinking</span>
            </div>
            <div className={styles.benefit}>
              <Icon name="checkmark.circle.fill" size={20} />
              <span>Make better resource allocation decisions</span>
            </div>
            <div className={styles.benefit}>
              <Icon name="checkmark.circle.fill" size={20} />
              <span>Prepare for multiple futures, not just one</span>
            </div>
            <div className={styles.benefit}>
              <Icon name="checkmark.circle.fill" size={20} />
              <span>Identify key risk factors and mitigation strategies</span>
            </div>
          </div>
        </div>
      </div>

      <div className={styles.content}>
        <ScenarioPlanning 
          onComplete={handleScenarioComplete}
          initialData={JSON.parse(localStorage.getItem('scenarioPlanningData') || '{}')}
        />
      </div>

      <div className={styles.navigation}>
        <motion.button
          className={styles.navButton}
          onClick={() => navigate('/deep-dive/phase3')}
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
        >
          <Icon name="arrow.left" size={16} />
          Previous Phase
        </motion.button>
        
        {overallCompletion >= 75 && (
          <motion.button
            className={styles.navButtonPrimary}
            onClick={() => navigate('/deep-dive/synthesis')}
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
          >
            Continue to Synthesis
            <Icon name="arrow.right" size={16} />
          </motion.button>
        )}
      </div>
    </div>
  );
};

export default Phase4RiskPathways;