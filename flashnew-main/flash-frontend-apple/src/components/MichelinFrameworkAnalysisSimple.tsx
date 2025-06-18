import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import useAssessmentStore from '../store/assessmentStore';
import styles from './MichelinFrameworkAnalysisSimple.module.scss';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8001';

// Custom minimalist icons for Jony Ive aesthetic
const LocationIcon = () => (
  <svg width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M10 10.5C11.1046 10.5 12 9.60457 12 8.5C12 7.39543 11.1046 6.5 10 6.5C8.89543 6.5 8 7.39543 8 8.5C8 9.60457 8.89543 10.5 10 10.5Z" stroke="currentColor" strokeWidth="1.5"/>
    <path d="M10 17C10 17 15 13.5 15 8.5C15 5.73858 12.7614 3.5 10 3.5C7.23858 3.5 5 5.73858 5 8.5C5 13.5 10 17 10 17Z" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
  </svg>
);

const LightbulbIcon = () => (
  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M12 2C8.13401 2 5 5.13401 5 9C5 11.3719 6.13623 13.4784 7.875 14.7396V17C7.875 17.5523 8.32272 18 8.875 18H15.125C15.6773 18 16.125 17.5523 16.125 17V14.7396C17.8638 13.4784 19 11.3719 19 9C19 5.13401 15.866 2 12 2Z" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
    <path d="M9 21H15" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round"/>
    <path d="M10 18V21" stroke="currentColor" strokeWidth="1.5"/>
    <path d="M14 18V21" stroke="currentColor" strokeWidth="1.5"/>
  </svg>
);

const ArrowRightIcon = () => (
  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <circle cx="12" cy="12" r="9" stroke="currentColor" strokeWidth="1.5"/>
    <path d="M10.5 8.5L14 12L10.5 15.5" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
  </svg>
);

const LoadingIcon = () => (
  <svg width="48" height="48" viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
    <circle cx="24" cy="24" r="20" stroke="currentColor" strokeWidth="2" strokeOpacity="0.2"/>
    <path d="M24 4C35.0457 4 44 12.9543 44 24" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
  </svg>
);

export const MichelinFrameworkAnalysisSimple: React.FC = () => {
  const [activePhase, setActivePhase] = useState<'situation' | 'strategy' | 'execution'>('situation');
  const [analyses, setAnalyses] = useState<any>({
    situation: [],
    strategy: [],
    execution: []
  });
  const [isLoading, setIsLoading] = useState(false);
  
  const assessmentData = useAssessmentStore(state => state.data);

  useEffect(() => {
    if (assessmentData) {
      loadAnalyses();
    }
  }, [assessmentData]);

  const transformData = (data: any) => {
    const { capital = {}, advantage = {}, market = {}, people = {}, companyInfo = {} } = data;
    
    return {
      startup_name: companyInfo.companyName || 'Startup',
      total_capital_raised_usd: Number(capital.totalRaised) || 0,
      cash_on_hand_usd: Number(capital.cashOnHand) || 0,
      monthly_burn_usd: Number(capital.monthlyBurn) || 0,
      runway_months: Number(capital.runwayMonths) || 0,
      funding_stage: capital.fundingStage || 'pre_seed',
      investor_tier_primary: capital.primaryInvestor || 'none',
      burn_rate_usd: Number(capital.monthlyBurn) || 0,
      product_stage: advantage.productStage || 'concept',
      proprietary_tech: advantage.proprietaryTech || false,
      patents_filed: Number(advantage.patentsFiled) || 0,
      monthly_active_users: Number(advantage.monthlyActiveUsers) || 0,
      market_size_usd: Number(market.tam) || 0,
      market_growth_rate_annual: Number(market.marketGrowthRate) || 15,
      competitor_count: Number(market.competitorCount) || 0,
      market_share_percentage: Number(market.marketShare) || (Number(market.som) && Number(market.sam) ? Number(market.som) / Number(market.sam) * 100 : 2.5),
      customer_acquisition_cost_usd: Number(market.customerAcquisitionCost) || Number(capital.monthlyBurn) / Math.max(1, Number(market.customerCount)) || 100,
      lifetime_value_usd: Number(market.lifetimeValue) || Number(market.ltvCacRatio) * 100 || 300,
      team_size_full_time: Number(people.fullTimeEmployees) || 1,
      founders_industry_experience_years: Number(people.industryExperience) || 0,
      b2b_or_b2c: market.businessModel || 'b2c',
      sector: market.sector || 'other',
    };
  };

  const loadAnalyses = async () => {
    setIsLoading(true);
    const apiData = transformData(assessmentData);
    
    const phaseFrameworks = {
      situation: ['bcg_matrix', 'porters_five_forces', 'swot_analysis'],
      strategy: ['ansoff_matrix', 'blue_ocean', 'value_chain'],
      execution: ['lean_canvas', 'balanced_scorecard', 'okr_framework']
    };

    try {
      // Load all phases
      for (const [phase, frameworks] of Object.entries(phaseFrameworks)) {
        const response = await fetch(`${API_URL}/api/frameworks/analyze`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            startup_data: apiData,
            framework_ids: frameworks
          })
        });

        if (response.ok) {
          const data = await response.json();
          setAnalyses(prev => ({
            ...prev,
            [phase]: data.analyses || []
          }));
        }
      }
    } catch (error) {
      console.error('Error loading analyses:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const renderPhaseContent = () => {
    const phaseData = analyses[activePhase] || [];
    
    if (isLoading) {
      return (
        <div className={styles.loading}>
          <LoadingIcon />
          <p>Analyzing your business...</p>
        </div>
      );
    }

    return (
      <div className={styles.phaseContent}>
        <div className={styles.phaseHeader}>
          <h2>
            {activePhase === 'situation' && 'Where Are We Now?'}
            {activePhase === 'strategy' && 'Where Should We Go?'}
            {activePhase === 'execution' && 'How to Get There?'}
          </h2>
          <p>
            {activePhase === 'situation' && 'Understanding our current position through strategic frameworks'}
            {activePhase === 'strategy' && 'Identifying strategic options and opportunities'}
            {activePhase === 'execution' && 'Creating actionable implementation plans'}
          </p>
        </div>

        <div className={styles.frameworkAnalyses}>
          {phaseData.map((analysis: any, index: number) => (
            <motion.div
              key={analysis.framework_id}
              className={styles.frameworkSection}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.2 }}
            >
              <div className={styles.frameworkHeader}>
                <h3>{analysis.framework_name}</h3>
                <div className={styles.position}>
                  <LocationIcon />
                  <span>{analysis.position}</span>
                  {analysis.metrics && (
                    <span className={styles.subtext}>
                      {analysis.framework_id === 'bcg_matrix' && 
                        `(${analysis.metrics.absolute_market_share?.toFixed(1) || '0'}% share, ${analysis.metrics.market_growth_rate?.toFixed(0) || '0'}% growth)`
                      }
                      {analysis.framework_id === 'porters_five_forces' && 
                        `(Industry Attractiveness: ${((1 - (analysis.score || 0)) * 100).toFixed(0)}%)`
                      }
                      {analysis.framework_id === 'swot_analysis' && 
                        `(${analysis.metrics.strength_count || 0} strengths, ${analysis.metrics.weakness_count || 0} weaknesses)`
                      }
                    </span>
                  )}
                </div>
              </div>

              {/* Text-based analysis content */}
              <div className={styles.analysisContent}>
                {/* For SWOT, show lists */}
                {analysis.framework_id === 'swot_analysis' && analysis.visualization_data && (
                  <div className={styles.swotTextContent}>
                    <div className={styles.swotSection}>
                      <h4>Strengths</h4>
                      <ul>
                        {analysis.visualization_data.strengths?.map((item: string, i: number) => (
                          <li key={i}>{item}</li>
                        ))}
                      </ul>
                    </div>
                    <div className={styles.swotSection}>
                      <h4>Weaknesses</h4>
                      <ul>
                        {analysis.visualization_data.weaknesses?.map((item: string, i: number) => (
                          <li key={i}>{item}</li>
                        ))}
                      </ul>
                    </div>
                    <div className={styles.swotSection}>
                      <h4>Opportunities</h4>
                      <ul>
                        {analysis.visualization_data.opportunities?.map((item: string, i: number) => (
                          <li key={i}>{item}</li>
                        ))}
                      </ul>
                    </div>
                    <div className={styles.swotSection}>
                      <h4>Threats</h4>
                      <ul>
                        {analysis.visualization_data.threats?.map((item: string, i: number) => (
                          <li key={i}>{item}</li>
                        ))}
                      </ul>
                    </div>
                  </div>
                )}

                {/* For Five Forces, show force levels */}
                {analysis.framework_id === 'porters_five_forces' && analysis.metrics && (
                  <div className={styles.forcesTextContent}>
                    {Object.entries(analysis.metrics).map(([force, details]: any) => (
                      <div key={force} className={styles.forceItem}>
                        <span className={styles.forceName}>
                          {force.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}:
                        </span>
                        <span className={styles.forceLevel}>
                          {details.level} ({(details.score * 100).toFixed(0)}%)
                        </span>
                      </div>
                    ))}
                  </div>
                )}

                {/* For BCG Matrix, show position details */}
                {analysis.framework_id === 'bcg_matrix' && analysis.metrics && (
                  <div className={styles.bcgTextContent}>
                    <p>
                      <strong>Position:</strong> {analysis.position}
                    </p>
                    <p>
                      <strong>Market Share:</strong> {analysis.metrics.absolute_market_share?.toFixed(1)}%
                    </p>
                    <p>
                      <strong>Market Growth:</strong> {analysis.metrics.market_growth_rate?.toFixed(0)}% annually
                    </p>
                    <p>
                      <strong>Relative Market Share:</strong> {analysis.metrics.relative_market_share?.toFixed(2)}x
                    </p>
                  </div>
                )}
              </div>

              {/* Key Insights */}
              <div className={styles.insights}>
                <h4>Key Insights</h4>
                <ul>
                  {analysis.insights.map((insight: string, i: number) => (
                    <li key={i}>
                      <LightbulbIcon />
                      <span>{insight}</span>
                    </li>
                  ))}
                </ul>
              </div>

              {/* Strategic Recommendations */}
              <div className={styles.recommendations}>
                <h4>Recommendations</h4>
                <ul>
                  {analysis.recommendations.map((rec: string, i: number) => (
                    <li key={i}>
                      <ArrowRightIcon />
                      <span>{rec}</span>
                    </li>
                  ))}
                </ul>
              </div>
            </motion.div>
          ))}
        </div>
      </div>
    );
  };

  return (
    <div className={styles.container}>
      {/* Phase Navigation */}
      <div className={styles.phaseNav}>
        <button
          className={`${styles.phaseButton} ${activePhase === 'situation' ? styles.active : ''}`}
          onClick={() => setActivePhase('situation')}
        >
          <div className={styles.numberWrapper}>
            <span className={styles.number}>1</span>
          </div>
          <div className={styles.phaseInfo}>
            <h4>Where Are We Now?</h4>
            <p>Situation Analysis</p>
          </div>
        </button>
        
        <div className={styles.phaseSeparator} />
        
        <button
          className={`${styles.phaseButton} ${activePhase === 'strategy' ? styles.active : ''}`}
          onClick={() => setActivePhase('strategy')}
        >
          <div className={styles.numberWrapper}>
            <span className={styles.number}>2</span>
          </div>
          <div className={styles.phaseInfo}>
            <h4>Where Should We Go?</h4>
            <p>Strategic Options</p>
          </div>
        </button>
        
        <div className={styles.phaseSeparator} />
        
        <button
          className={`${styles.phaseButton} ${activePhase === 'execution' ? styles.active : ''}`}
          onClick={() => setActivePhase('execution')}
        >
          <div className={styles.numberWrapper}>
            <span className={styles.number}>3</span>
          </div>
          <div className={styles.phaseInfo}>
            <h4>How to Get There?</h4>
            <p>Implementation Plan</p>
          </div>
        </button>
      </div>

      {/* Phase Content */}
      <motion.div
        key={activePhase}
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        exit={{ opacity: 0, y: -20 }}
        transition={{ duration: 0.6, ease: [0.23, 1, 0.32, 1] }}
      >
        {renderPhaseContent()}
      </motion.div>
    </div>
  );
};