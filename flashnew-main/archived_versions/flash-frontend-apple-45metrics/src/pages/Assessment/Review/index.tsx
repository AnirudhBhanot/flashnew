import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import { useWizard } from '../../../features/wizard/WizardProvider';
import useAssessmentStore from '../../../store/assessmentStore';
import { Button, Icon } from '../../../design-system/components';
import { apiService } from '../../../services/api';
import styles from './Review.module.scss';

const Review: React.FC = () => {
  const { previousStep, data } = useWizard();
  const { submitAssessment, setResults } = useAssessmentStore();
  const navigate = useNavigate();
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  
  const handleSubmit = async () => {
    setIsSubmitting(true);
    setError(null);
    
    try {
      // Mark assessment as submitted in store
      submitAssessment();
      
      // Submit to API for prediction
      console.log('Submitting assessment data:', data);
      const prediction = await apiService.predict(data);
      
      // Log the prediction response to debug
      console.log('API prediction response:', prediction);
      console.log('CAMP scores:', prediction.camp_scores);
      
      // Store results
      setResults({
        successProbability: prediction.success_probability,
        confidence: prediction.confidence,
        scores: prediction.camp_scores,
        insights: prediction.insights,
        recommendations: []
      });
      
      // Navigate to analysis page
      navigate('/analysis');
    } catch (error) {
      console.error('Submission error:', error);
      setError(error instanceof Error ? error.message : 'Failed to submit assessment');
      setIsSubmitting(false);
    }
  };
  
  const formatCurrency = (value: number | string | undefined) => {
    if (!value) return '$0';
    const num = typeof value === 'string' ? parseFloat(value) : value;
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0,
    }).format(num);
  };
  
  const formatPercent = (value: number | string | undefined) => {
    if (!value) return '0%';
    return `${value}%`;
  };

  return (
    <div className={styles.page}>
      <nav className={styles.nav}>
        <Button 
          variant="text" 
          size="small" 
          icon={<Icon name="chevron.left" />} 
          iconPosition="left"
          onClick={previousStep}
        >
          Back
        </Button>
      </nav>
      
      <div className={styles.content}>
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, ease: [0.2, 0, 0, 1] }}
        >
          <h1 className={styles.title}>Review Your Assessment</h1>
          <p className={styles.subtitle}>Please review your information before submitting</p>
          
          <div className={styles.sections}>
            {/* Company Information */}
            <motion.section 
              className={styles.section}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.1 }}
            >
              <h2 className={styles.sectionTitle}>Company Information</h2>
              <div className={styles.details}>
                <div className={styles.detail}>
                  <span className={styles.label}>Company Name</span>
                  <span className={styles.value}>{data.companyInfo?.companyName || 'Not provided'}</span>
                </div>
                <div className={styles.detail}>
                  <span className={styles.label}>Industry</span>
                  <span className={styles.value}>{data.companyInfo?.industry || 'Not provided'}</span>
                </div>
                <div className={styles.detail}>
                  <span className={styles.label}>Founded</span>
                  <span className={styles.value}>
                    {data.companyInfo?.foundedDate 
                      ? new Date(data.companyInfo.foundedDate).toLocaleDateString()
                      : 'Not provided'}
                  </span>
                </div>
                <div className={styles.detail}>
                  <span className={styles.label}>Stage</span>
                  <span className={styles.value}>{data.companyInfo?.stage || 'Not provided'}</span>
                </div>
              </div>
            </motion.section>
            
            {/* Capital & Financials */}
            <motion.section 
              className={styles.section}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.2 }}
            >
              <h2 className={styles.sectionTitle}>Capital & Financials</h2>
              <div className={styles.details}>
                <div className={styles.detail}>
                  <span className={styles.label}>Total Funding</span>
                  <span className={styles.value}>{formatCurrency(data.capital?.totalFundingRaised)}</span>
                </div>
                <div className={styles.detail}>
                  <span className={styles.label}>Monthly Burn</span>
                  <span className={styles.value}>{formatCurrency(data.capital?.monthlyBurnRate)}</span>
                </div>
                <div className={styles.detail}>
                  <span className={styles.label}>Runway</span>
                  <span className={styles.value}>{data.capital?.runwayMonths || 0} months</span>
                </div>
                <div className={styles.detail}>
                  <span className={styles.label}>Annual Revenue</span>
                  <span className={styles.value}>{formatCurrency(data.capital?.annualRevenueRunRate)}</span>
                </div>
              </div>
            </motion.section>
            
            {/* Competitive Advantage */}
            <motion.section 
              className={styles.section}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.3 }}
            >
              <h2 className={styles.sectionTitle}>Competitive Advantage</h2>
              <div className={styles.details}>
                <div className={styles.detail}>
                  <span className={styles.label}>Moat Strength</span>
                  <span className={styles.value}>{data.advantage?.moatStrength || 0}/10</span>
                </div>
                <div className={styles.detail}>
                  <span className={styles.label}>Key Advantages</span>
                  <span className={styles.value}>
                    {data.advantage?.advantages?.length || 0} selected
                  </span>
                </div>
                <div className={styles.detail}>
                  <span className={styles.label}>Patents</span>
                  <span className={styles.value}>
                    {data.advantage?.hasPatents ? `${data.advantage.patentCount || 0} patents` : 'No'}
                  </span>
                </div>
              </div>
            </motion.section>
            
            {/* Market Analysis */}
            <motion.section 
              className={styles.section}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.4 }}
            >
              <h2 className={styles.sectionTitle}>Market Analysis</h2>
              <div className={styles.details}>
                <div className={styles.detail}>
                  <span className={styles.label}>Market Size (TAM)</span>
                  <span className={styles.value}>{formatCurrency(data.market?.marketSize)}</span>
                </div>
                <div className={styles.detail}>
                  <span className={styles.label}>Growth Rate</span>
                  <span className={styles.value}>{formatPercent(data.market?.marketGrowthRate)}</span>
                </div>
                <div className={styles.detail}>
                  <span className={styles.label}>Competition</span>
                  <span className={styles.value}>{data.market?.competitionLevel || 0}/10</span>
                </div>
                <div className={styles.detail}>
                  <span className={styles.label}>Target Market</span>
                  <span className={styles.value}>{data.market?.targetMarket?.toUpperCase() || 'Not specified'}</span>
                </div>
              </div>
            </motion.section>
            
            {/* Team & Leadership */}
            <motion.section 
              className={styles.section}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.5 }}
            >
              <h2 className={styles.sectionTitle}>Team & Leadership</h2>
              <div className={styles.details}>
                <div className={styles.detail}>
                  <span className={styles.label}>Team Size</span>
                  <span className={styles.value}>{data.people?.teamSize || 0} people</span>
                </div>
                <div className={styles.detail}>
                  <span className={styles.label}>Founders</span>
                  <span className={styles.value}>{data.people?.foundersCount || 0} founders</span>
                </div>
                <div className={styles.detail}>
                  <span className={styles.label}>Industry Experience</span>
                  <span className={styles.value}>{data.people?.industryExperience || 0}/10</span>
                </div>
                <div className={styles.detail}>
                  <span className={styles.label}>Previous Exits</span>
                  <span className={styles.value}>
                    {data.people?.previousStartups ? `${data.people.previousExits || 0} exits` : 'First startup'}
                  </span>
                </div>
              </div>
            </motion.section>
          </div>
          
          <div className={styles.disclaimer}>
            <Icon name="info.circle" size={20} />
            <p>
              By submitting this assessment, you confirm that all information provided is accurate 
              to the best of your knowledge. The assessment results are for informational purposes only.
            </p>
          </div>
          
          {error && (
            <div className={styles.error}>
              <Icon name="exclamationmark.triangle" size={20} />
              <p>{error}</p>
            </div>
          )}
          
          <div className={styles.actions}>
            <Button 
              variant="secondary" 
              size="large"
              onClick={previousStep}
              disabled={isSubmitting}
            >
              Back to Edit
            </Button>
            <Button 
              variant="primary" 
              size="large"
              onClick={handleSubmit}
              disabled={isSubmitting}
              loading={isSubmitting}
            >
              {isSubmitting ? 'Submitting...' : 'Submit Assessment'}
            </Button>
          </div>
        </motion.div>
      </div>
    </div>
  );
};

export default Review;