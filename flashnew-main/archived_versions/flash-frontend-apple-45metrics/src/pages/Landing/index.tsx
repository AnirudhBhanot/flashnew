import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import { Button } from '../../design-system/components/Button';
import { Icon } from '../../design-system/components/Icon';
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

  return (
    <div className={styles.landing}>
      {/* Navigation */}
      <nav className={styles.nav}>
        <div className={styles.navContent}>
          <h1 className={styles.logo}>FLASH</h1>
          <div className={styles.navActions}>
            <Button variant="text" size="small">About</Button>
            <Button variant="text" size="small">Sign In</Button>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className={styles.hero}>
        {showRecovery ? (
          <div className={styles.recoveryContainer}>
            <ProgressRecovery
              onContinue={handleContinue}
              onStartNew={handleStartNew}
            />
          </div>
        ) : (
          <>
            <div className={styles.heroContent}>
              <motion.div
                initial={{ opacity: 0, y: 30 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.8, ease: [0.2, 0, 0, 1] }}
              >
                <h1 className={styles.title}>
                  Know Your Startup's{' '}
                  <span className={styles.gradient}>True Potential</span>
                </h1>
                
                <p className={styles.subtitle}>
                  Get an honest assessment powered by machine learning
                  and validated by analyzing 100,000+ startups
                </p>
                
                <div className={styles.actions}>
                  <Button
                    variant="primary"
                    size="large"
                    onClick={() => navigate('/assessment/company')}
                    icon={<Icon name="arrow.right" />}
                  >
                    Begin Assessment
                  </Button>
                  
                  <Button 
                    variant="secondary" 
                    size="large"
                    icon={<Icon name="play.circle" />}
                    iconPosition="left"
                  >
                    Watch Demo
                  </Button>
                </div>
              </motion.div>
            </div>
            
            <motion.div 
              className={styles.heroVisual}
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ duration: 1, delay: 0.2, ease: [0.2, 0, 0, 1] }}
            >
              {/* Placeholder for 3D visualization */}
              <div className={styles.visualPlaceholder}>
                <div className={styles.orb} />
              </div>
            </motion.div>
          </>
        )}
      </section>

      {/* Features Section */}
      <section className={styles.features}>
        <div className={styles.container}>
          <h2 className={styles.sectionTitle}>Why FLASH is Different</h2>
          
          <div className={styles.featureGrid}>
            <FeatureCard
              icon="brain"
              title="Honest Predictions"
              description="No sugar-coating. Real probabilities based on real data."
              delay={0.1}
            />
            
            <FeatureCard
              icon="chart.line.uptrend"
              title="Pattern Recognition"
              description="Identifies which of 50+ success patterns match your startup."
              delay={0.2}
            />
            
            <FeatureCard
              icon="building.2"
              title="Industry Specific"
              description="Tailored insights for SaaS, FinTech, HealthTech, and more."
              delay={0.3}
            />
            
            <FeatureCard
              icon="sparkles"
              title="Actionable Insights"
              description="Get specific recommendations, not generic advice."
              delay={0.4}
            />
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className={styles.cta}>
        <div className={styles.container}>
          <motion.div 
            className={styles.ctaCard}
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, ease: [0.2, 0, 0, 1] }}
            viewport={{ once: true }}
          >
            <h2 className={styles.ctaTitle}>Ready to see the truth?</h2>
            <p className={styles.ctaSubtitle}>
              Takes 5 minutes. No signup required.
            </p>
            <Button
              variant="primary"
              size="large"
              onClick={() => navigate('/assessment/company')}
            >
              Start Free Assessment
            </Button>
          </motion.div>
        </div>
      </section>
    </div>
  );
};

interface FeatureCardProps {
  icon: string;
  title: string;
  description: string;
  delay: number;
}

const FeatureCard: React.FC<FeatureCardProps> = ({ icon, title, description, delay }) => {
  return (
    <motion.div
      className={styles.featureCard}
      initial={{ opacity: 0, y: 20 }}
      whileInView={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, delay, ease: [0.2, 0, 0, 1] }}
      viewport={{ once: true }}
      whileHover={{ y: -4 }}
    >
      <div className={styles.featureIcon}>
        <Icon name={icon} size={28} />
      </div>
      <h3 className={styles.featureTitle}>{title}</h3>
      <p className={styles.featureDescription}>{description}</p>
    </motion.div>
  );
};

export default Landing;