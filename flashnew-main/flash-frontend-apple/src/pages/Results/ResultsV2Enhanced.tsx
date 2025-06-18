import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { AnimatePresence } from '../../design-system/components/AnimatePresenceWrapper';
import { useNavigate } from 'react-router-dom';
import useAssessmentStore from '../../store/assessmentStore';
import { EnhancedInsightsMinimalV2 } from '../../components/EnhancedInsightsMinimalV2';
import { DeepDiveAnalysisMinimalV2 } from '../../components/DeepDiveAnalysisMinimalV2';
import { LLMRecommendationsMinimalV2 } from '../../components/LLMRecommendationsMinimalV2';
import { CAMPAnalysisMinimalV2 } from '../../components/CAMPAnalysisMinimalV2';
import { SuccessScoreMinimal } from '../../components/SuccessScoreMinimal';
import StrategicFrameworkAnalysis from '../../components/StrategicFrameworkAnalysis';
import { ExecutiveFrameworkAnalysis } from '../../components/ExecutiveFrameworkAnalysis';
import { MichelinStrategicAnalysis } from '../../components/MichelinStrategicAnalysis';
import styles from './ResultsV2Enhanced.module.scss';

interface SectionProps {
  title: string;
  isExpanded: boolean;
  onToggle: () => void;
  children: React.ReactNode;
}

const ExpandableSection: React.FC<SectionProps> = ({ title, isExpanded, onToggle, children }) => {
  return (
    <div className={styles.expandableSection}>
      <button className={styles.sectionHeader} onClick={onToggle}>
        <h3>{title}</h3>
        <motion.svg
          width="20"
          height="20"
          viewBox="0 0 20 20"
          animate={{ rotate: isExpanded ? 180 : 0 }}
          transition={{ duration: 0.3 }}
        >
          <path
            d="M5 7.5L10 12.5L15 7.5"
            stroke="currentColor"
            strokeWidth="1.5"
            strokeLinecap="round"
            strokeLinejoin="round"
            fill="none"
          />
        </motion.svg>
      </button>
      <AnimatePresence>
        {isExpanded && (
          <motion.div
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: 'auto', opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            transition={{ duration: 0.3 }}
            className={styles.sectionContent}
          >
            {children}
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};

const ResultsV2Enhanced: React.FC = () => {
  const navigate = useNavigate();
  const { results, data } = useAssessmentStore();
  const [expandedSections, setExpandedSections] = useState<string[]>([]);

  if (!results) {
    navigate('/');
    return null;
  }

  const toggleSection = (section: string) => {
    setExpandedSections(prev =>
      prev.includes(section)
        ? prev.filter(s => s !== section)
        : [...prev, section]
    );
  };

  const successProbability = Math.round((results.successProbability || 0) * 100);
  const scores = results.scores || { capital: 0, advantage: 0, market: 0, people: 0 };

  const getScoreColor = (score: number) => {
    if (score >= 0.8) return styles.excellent;
    if (score >= 0.6) return styles.good;
    if (score >= 0.4) return styles.fair;
    return styles.poor;
  };

  const getVerdict = () => {
    const prob = results.successProbability || 0;
    if (prob >= 0.8) return 'Highly Recommended';
    if (prob >= 0.6) return 'Recommended';
    if (prob >= 0.4) return 'Conditional';
    return 'Not Recommended';
  };

  return (
    <div className={styles.page}>
      {/* Navigation */}
      <nav className={styles.nav}>
        <button className={styles.backButton} onClick={() => navigate('/')}>
          <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
            <path
              d="M12 4L6 10L12 16"
              stroke="currentColor"
              strokeWidth="1.5"
              strokeLinecap="round"
              strokeLinejoin="round"
            />
          </svg>
        </button>
      </nav>

      {/* Main Content */}
      <div className={styles.content}>
        {/* Success Score Section - Always Visible */}
        <SuccessScoreMinimal 
          score={results.successProbability || 0}
          confidence={results.confidence}
          companyName={data.companyInfo?.companyName || 'Your Startup'}
        />

        {/* CAMP Analysis */}
        <ExpandableSection
          title="CAMP Framework Analysis"
          isExpanded={expandedSections.includes('camp')}
          onToggle={() => toggleSection('camp')}
        >
          <div style={{ padding: '24px 0' }}>
            <CAMPAnalysisMinimalV2 scores={scores} />
          </div>
        </ExpandableSection>

        {/* Enhanced Insights */}
        <ExpandableSection
          title="Key Insights"
          isExpanded={expandedSections.includes('insights')}
          onToggle={() => toggleSection('insights')}
        >
          <div style={{ padding: '24px 0' }}>
            <EnhancedInsightsMinimalV2 
              scores={scores}
              probability={results.successProbability || 0}
            />
          </div>
        </ExpandableSection>

        {/* Deep Dive Analysis */}
        <ExpandableSection
          title="Deep Dive Analysis"
          isExpanded={expandedSections.includes('deepdive')}
          onToggle={() => toggleSection('deepdive')}
        >
          <div style={{ padding: '24px 0' }}>
            <DeepDiveAnalysisMinimalV2 
              scores={scores}
              assessmentData={data}
              insights={results.insights || []}
            />
          </div>
        </ExpandableSection>

        {/* FLASH Intelligence */}
        <ExpandableSection
          title="FLASH Intelligence"
          isExpanded={expandedSections.includes('recommendations')}
          onToggle={() => toggleSection('recommendations')}
        >
          <div style={{ padding: '24px 0' }}>
            <LLMRecommendationsMinimalV2 
              assessmentData={data}
              basicResults={results}
            />
          </div>
        </ExpandableSection>

        {/* Strategic Framework Analysis */}
        <ExpandableSection
          title="Strategic Framework Analysis"
          isExpanded={expandedSections.includes('strategic')}
          onToggle={() => toggleSection('strategic')}
        >
          <div style={{ padding: '24px 0' }}>
            <StrategicFrameworkAnalysis />
          </div>
        </ExpandableSection>

        {/* FLASH Executive Report */}
        <ExpandableSection
          title="FLASH Executive Report"
          isExpanded={expandedSections.includes('executive')}
          onToggle={() => toggleSection('executive')}
        >
          <div style={{ padding: '24px 0' }}>
            <ExecutiveFrameworkAnalysis />
          </div>
        </ExpandableSection>

        {/* Michelin Strategic Analysis */}
        <ExpandableSection
          title="Michelin Strategic Analysis"
          isExpanded={expandedSections.includes('michelin')}
          onToggle={() => toggleSection('michelin')}
        >
          <div style={{ padding: '24px 0' }}>
            <MichelinStrategicAnalysis 
              startupData={{
                company_name: data.companyInfo?.companyName || 'Your Startup',
                annual_revenue_run_rate: data.capital?.annualRevenue || 0,
                monthly_burn_usd: data.capital?.monthlyBurn || 50000,
                runway_months: data.capital?.runwayMonths || 12,
                team_size_full_time: data.people?.teamSize || 5,
                customer_count: data.market?.customerCount || 0,
                tam_size_usd: data.market?.tamSize || 10000000000,
                sam_size_usd: data.market?.samSize || 1000000000,
                som_size_usd: data.market?.somSize || 100000000,
                sector: data.market?.sector || 'technology',
                funding_stage: data.capital?.fundingStage || 'seed',
                revenue_growth_rate_percent: data.market?.revenueGrowthRate || 0,
                market_growth_rate_percent: data.market?.marketGrowthRate || 20,
                competition_intensity: data.market?.competitionIntensity || 3,
                competitors_named_count: data.market?.competitorCount || 5,
                patent_count: data.advantage?.patentCount || 0,
                prior_exits: data.people?.priorExits || 0,
                domain_expertise_years: data.people?.domainExpertise || 0,
                product_stage: data.advantage?.productStage || 'beta',
                investor_tier: data.capital?.investorTier || 'tier_2',
                gross_margin: data.market?.grossMargin || 70,
                total_capital_raised: data.capital?.totalCapitalRaised || 1000000,
                cash_on_hand: data.capital?.cashOnHand || 500000
              }}
            />
          </div>
        </ExpandableSection>

        {/* Action Items */}
        <ExpandableSection
          title="Recommended Actions"
          isExpanded={expandedSections.includes('actions')}
          onToggle={() => toggleSection('actions')}
        >
          <div className={styles.actions}>
            <div className={styles.actionGrid}>
              <button className={styles.actionButton} onClick={() => navigate('/assessment/company')}>
                <span className={styles.actionText}>Update Assessment</span>
              </button>
              <button className={styles.actionButton} onClick={() => window.print()}>
                <span className={styles.actionText}>Export Report</span>
              </button>
              <button className={styles.actionButton} onClick={() => navigate('/')}>
                <span className={styles.actionText}>Start New</span>
              </button>
            </div>
          </div>
        </ExpandableSection>
      </div>
    </div>
  );
};

export default ResultsV2Enhanced;