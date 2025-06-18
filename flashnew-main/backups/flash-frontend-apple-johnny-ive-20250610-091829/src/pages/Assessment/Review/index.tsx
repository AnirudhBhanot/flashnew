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
                  <span className={styles.label}>Sector</span>
                  <span className={styles.value}>{data.companyInfo?.sector?.replace(/-/g, ' ').toUpperCase() || 'Not provided'}</span>
                </div>
                <div className={styles.detail}>
                  <span className={styles.label}>Stage</span>
                  <span className={styles.value}>{data.companyInfo?.stage?.replace(/-/g, ' ').toUpperCase() || 'Not provided'}</span>
                </div>
                <div className={styles.detail}>
                  <span className={styles.label}>Founded</span>
                  <span className={styles.value}>
                    {data.companyInfo?.foundingDate 
                      ? new Date(data.companyInfo.foundingDate).toLocaleDateString()
                      : 'Not provided'}
                  </span>
                </div>
                {data.companyInfo?.headquarters && (
                  <div className={styles.detail}>
                    <span className={styles.label}>Headquarters</span>
                    <span className={styles.value}>{data.companyInfo.headquarters}</span>
                  </div>
                )}
                {data.companyInfo?.website && (
                  <div className={styles.detail}>
                    <span className={styles.label}>Website</span>
                    <span className={styles.value}>{data.companyInfo.website}</span>
                  </div>
                )}
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
                  <span className={styles.label}>Total Raised</span>
                  <span className={styles.value}>{formatCurrency(data.capital?.totalRaised)}</span>
                </div>
                <div className={styles.detail}>
                  <span className={styles.label}>Cash on Hand</span>
                  <span className={styles.value}>{formatCurrency(data.capital?.cashOnHand)}</span>
                </div>
                <div className={styles.detail}>
                  <span className={styles.label}>Monthly Burn</span>
                  <span className={styles.value}>{formatCurrency(data.capital?.monthlyBurn)}</span>
                </div>
                <div className={styles.detail}>
                  <span className={styles.label}>Last Valuation</span>
                  <span className={styles.value}>{formatCurrency(data.capital?.lastValuation)}</span>
                </div>
                <div className={styles.detail}>
                  <span className={styles.label}>Funding Stage</span>
                  <span className={styles.value}>{data.capital?.fundingStage?.replace(/_/g, ' ').toUpperCase() || 'Not provided'}</span>
                </div>
                <div className={styles.detail}>
                  <span className={styles.label}>Annual Revenue Run Rate</span>
                  <span className={styles.value}>{formatCurrency(data.capital?.annualRevenueRunRate)}</span>
                </div>
                <div className={styles.detail}>
                  <span className={styles.label}>Primary Investor</span>
                  <span className={styles.value}>{data.capital?.primaryInvestor?.replace(/_/g, ' ').toUpperCase() || 'Not provided'}</span>
                </div>
                <div className={styles.detail}>
                  <span className={styles.label}>Has Debt</span>
                  <span className={styles.value}>{data.capital?.hasDebt ? 'Yes' : 'No'}</span>
                </div>
                {data.capital?.hasDebt && (
                  <div className={styles.detail}>
                    <span className={styles.label}>Debt Amount</span>
                    <span className={styles.value}>{formatCurrency(data.capital.debtAmount)}</span>
                  </div>
                )}
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
                  <span className={styles.label}>Patents</span>
                  <span className={styles.value}>{data.advantage?.patentCount || 0}</span>
                </div>
                <div className={styles.detail}>
                  <span className={styles.label}>Product Stage</span>
                  <span className={styles.value}>{data.advantage?.productStage?.replace(/_/g, ' ').toUpperCase() || 'Not provided'}</span>
                </div>
                <div className={styles.detail}>
                  <span className={styles.label}>Network Effects</span>
                  <span className={styles.value}>{data.advantage?.networkEffects ? 'Yes' : 'No'}</span>
                </div>
                <div className={styles.detail}>
                  <span className={styles.label}>Data Moat</span>
                  <span className={styles.value}>{data.advantage?.hasDataMoat ? 'Yes' : 'No'}</span>
                </div>
                <div className={styles.detail}>
                  <span className={styles.label}>Regulatory Advantage</span>
                  <span className={styles.value}>{data.advantage?.regulatoryAdvantage ? 'Yes' : 'No'}</span>
                </div>
                <div className={styles.detail}>
                  <span className={styles.label}>Brand Strength</span>
                  <span className={styles.value}>{data.advantage?.brandStrength || 0}/5</span>
                </div>
                <div className={styles.detail}>
                  <span className={styles.label}>Scalability</span>
                  <span className={styles.value}>{data.advantage?.scalability || 0}/5</span>
                </div>
                <div className={styles.detail}>
                  <span className={styles.label}>Switching Costs</span>
                  <span className={styles.value}>{data.advantage?.switchingCosts || 0}/5</span>
                </div>
                <div className={styles.detail}>
                  <span className={styles.label}>Tech Differentiation</span>
                  <span className={styles.value}>{data.advantage?.techDifferentiation || 0}/5</span>
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
                  <span className={styles.label}>TAM</span>
                  <span className={styles.value}>{formatCurrency(data.market?.tam)}</span>
                </div>
                <div className={styles.detail}>
                  <span className={styles.label}>SAM</span>
                  <span className={styles.value}>{formatCurrency(data.market?.sam)}</span>
                </div>
                <div className={styles.detail}>
                  <span className={styles.label}>SOM</span>
                  <span className={styles.value}>{formatCurrency(data.market?.som)}</span>
                </div>
                <div className={styles.detail}>
                  <span className={styles.label}>Market Growth Rate</span>
                  <span className={styles.value}>{formatPercent(data.market?.marketGrowthRate)}</span>
                </div>
                <div className={styles.detail}>
                  <span className={styles.label}>Customer Count</span>
                  <span className={styles.value}>{data.market?.customerCount || 0}</span>
                </div>
                <div className={styles.detail}>
                  <span className={styles.label}>User Growth Rate</span>
                  <span className={styles.value}>{formatPercent(data.market?.userGrowthRate)}</span>
                </div>
                <div className={styles.detail}>
                  <span className={styles.label}>Net Dollar Retention</span>
                  <span className={styles.value}>{formatPercent(data.market?.netDollarRetention)}</span>
                </div>
                <div className={styles.detail}>
                  <span className={styles.label}>Competitor Count</span>
                  <span className={styles.value}>{data.market?.competitorCount || 0}</span>
                </div>
                <div className={styles.detail}>
                  <span className={styles.label}>Competition Intensity</span>
                  <span className={styles.value}>{data.market?.competitionIntensity || 0}/5</span>
                </div>
                <div className={styles.detail}>
                  <span className={styles.label}>Customer Concentration</span>
                  <span className={styles.value}>{formatPercent(data.market?.customerConcentration)}</span>
                </div>
                <div className={styles.detail}>
                  <span className={styles.label}>Revenue Growth Rate</span>
                  <span className={styles.value}>{formatPercent(data.market?.revenueGrowthRate)}</span>
                </div>
                <div className={styles.detail}>
                  <span className={styles.label}>Gross Margin</span>
                  <span className={styles.value}>{formatPercent(data.market?.grossMargin)}</span>
                </div>
                <div className={styles.detail}>
                  <span className={styles.label}>LTV/CAC Ratio</span>
                  <span className={styles.value}>{data.market?.ltvCacRatio || 0}</span>
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
                  <span className={styles.label}>Founders</span>
                  <span className={styles.value}>{data.people?.founderCount || 0}</span>
                </div>
                <div className={styles.detail}>
                  <span className={styles.label}>Team Size</span>
                  <span className={styles.value}>{data.people?.teamSize || 0} people</span>
                </div>
                <div className={styles.detail}>
                  <span className={styles.label}>Domain Expertise</span>
                  <span className={styles.value}>{data.people?.domainExpertiseYears || 0} years</span>
                </div>
                <div className={styles.detail}>
                  <span className={styles.label}>Prior Startup Experience</span>
                  <span className={styles.value}>{data.people?.priorStartupCount || 0}</span>
                </div>
                <div className={styles.detail}>
                  <span className={styles.label}>Advisors</span>
                  <span className={styles.value}>{data.people?.advisorCount || 0}</span>
                </div>
                <div className={styles.detail}>
                  <span className={styles.label}>Board/Advisor Score</span>
                  <span className={styles.value}>{data.people?.boardAdvisorScore || 0}/5</span>
                </div>
                <div className={styles.detail}>
                  <span className={styles.label}>Avg Experience</span>
                  <span className={styles.value}>{data.people?.avgExperience || 0} years</span>
                </div>
                <div className={styles.detail}>
                  <span className={styles.label}>Prior Exits</span>
                  <span className={styles.value}>{data.people?.priorExits || 0}</span>
                </div>
                <div className={styles.detail}>
                  <span className={styles.label}>30-Day Retention</span>
                  <span className={styles.value}>{formatPercent(data.people?.productRetention30d)}</span>
                </div>
                <div className={styles.detail}>
                  <span className={styles.label}>90-Day Retention</span>
                  <span className={styles.value}>{formatPercent(data.people?.productRetention90d)}</span>
                </div>
                <div className={styles.detail}>
                  <span className={styles.label}>DAU/MAU Ratio</span>
                  <span className={styles.value}>{formatPercent(data.people?.dauMauRatio)}</span>
                </div>
                <div className={styles.detail}>
                  <span className={styles.label}>Team Diversity</span>
                  <span className={styles.value}>{formatPercent(data.people?.teamDiversity)}</span>
                </div>
                <div className={styles.detail}>
                  <span className={styles.label}>Key Person Dependency</span>
                  <span className={styles.value}>{data.people?.keyPersonDependency ? 'Yes' : 'No'}</span>
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