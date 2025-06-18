import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import useAssessmentStore from '../store/assessmentStore';
// import { Icon } from '../design-system/components';
import styles from './MichelinLLMAnalysis.module.scss';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8001';

interface PhaseAnalysis {
  phase_name: string;
  frameworks: {
    framework_name: string;
    analysis: string;
    key_insights: string[];
  }[];
  summary: string;
}

interface MichelinAnalysis {
  executive_briefing: string;
  phase_1: PhaseAnalysis;
  phase_2: PhaseAnalysis;
  phase_3: PhaseAnalysis;
  strategic_recommendations: string[];
  immediate_next_steps: string[];
}

export const MichelinLLMAnalysis: React.FC = () => {
  const [activePhase, setActivePhase] = useState<'situation' | 'strategy' | 'execution'>('situation');
  const [analysis, setAnalysis] = useState<MichelinAnalysis | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  
  const assessmentData = useAssessmentStore(state => state.data);
  
  console.log('MichelinLLMAnalysis rendering, assessmentData:', assessmentData);

  useEffect(() => {
    if (assessmentData) {
      loadAnalysis();
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
      market_growth_rate_annual: Number(market.marketGrowthRate) || 0,
      competitor_count: Number(market.competitorCount) || 0,
      market_share_percentage: Number(market.marketShare) || (Number(market.som) / Number(market.tam) * 100) || 0.5,
      customer_acquisition_cost_usd: Number(market.customerAcquisitionCost) || Number(capital.monthlyBurn) / Math.max(1, Number(market.customerCount)) || 100,
      lifetime_value_usd: Number(market.lifetimeValue) || Number(market.ltvCacRatio) * 100 || 300,
      team_size_full_time: Number(people.fullTimeEmployees) || 1,
      founders_industry_experience_years: Number(people.industryExperience) || 0,
      b2b_or_b2c: market.businessModel || 'b2c',
      sector: market.sector || 'other',
      geographical_focus: 'domestic',
      revenue_growth_rate: Number(market.revenueGrowthRate) || 0,
      gross_margin: Number(market.grossMargin) || 0,
      net_promoter_score: 0,
      technology_readiness_level: advantage.productStage === 'launched' ? 8 : 5,
      has_strategic_partnerships: false,
      customer_concentration: Number(market.customerConcentration) || 0,
      annual_revenue_usd: 0,
      key_metrics: {
        customer_count: Number(market.customerCount) || 0,
        churn_rate: 0,
        average_contract_value: 0
      }
    };
  };

  const loadAnalysis = async () => {
    setIsLoading(true);
    setError(null);
    
    try {
      const apiData = transformData(assessmentData);
      
      const response = await fetch(`${API_URL}/api/michelin/analyze`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(apiData)
      });

      if (!response.ok) {
        throw new Error(`Analysis failed: ${response.statusText}`);
      }

      const data = await response.json();
      setAnalysis(data);
    } catch (error) {
      console.error('Error loading Michelin analysis:', error);
      setError('Failed to load strategic analysis. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const renderPhaseContent = () => {
    if (isLoading) {
      return (
        <div className={styles.loading}>
          <div style={{ fontSize: '32px', marginBottom: '16px' }}>⏳</div>
          <p>Generating strategic analysis using AI...</p>
        </div>
      );
    }

    if (error) {
      return (
        <div className={styles.error}>
          <div style={{ fontSize: '32px', marginBottom: '16px', color: '#ef4444' }}>⚠️</div>
          <p>{error}</p>
          <button onClick={loadAnalysis} className={styles.retryButton}>
            Try Again
          </button>
        </div>
      );
    }

    if (!analysis) return null;

    const phaseData = activePhase === 'situation' ? analysis.phase1 
                    : activePhase === 'strategy' ? analysis.phase2 
                    : analysis.phase3;

    // Check if phaseData exists
    if (!phaseData) {
      return (
        <div style={{ padding: '48px', textAlign: 'center', color: '#424245' }}>
          <p>No data available for this phase</p>
        </div>
      );
    }

    return (
      <div className={styles.phaseContent}>
        <div className={styles.phaseHeader}>
          <h2 style={{ color: '#1d1d1f' }}>{phaseData.phase_name || 'Phase Analysis'}</h2>
          <p className={styles.phaseSummary}>{phaseData.summary || 'Loading summary...'}</p>
        </div>

        <div className={styles.frameworkAnalyses}>
          {phaseData.frameworks && phaseData.frameworks.length > 0 ? (
            phaseData.frameworks.map((framework, index) => (
              <div
                key={framework.framework_name || index}
                className={styles.frameworkSection}
                style={{ marginBottom: '24px' }}
              >
                <div className={styles.frameworkHeader}>
                  <h3 style={{ color: '#1d1d1f' }}>{framework.framework_name || 'Framework'}</h3>
                </div>

                <div className={styles.analysisText}>
                  {framework.analysis ? framework.analysis.split('\n\n').map((paragraph, i) => (
                    <p key={i} style={{ color: '#424245', marginBottom: '16px' }}>{paragraph}</p>
                  )) : <p>No analysis available</p>}
                </div>

                {framework.key_insights && framework.key_insights.length > 0 && (
                  <div className={styles.keyInsights} style={{ marginTop: '24px', paddingTop: '24px', borderTop: '1px solid #d2d2d7' }}>
                    <h4 style={{ color: '#1d1d1f', marginBottom: '16px' }}>Key Insights</h4>
                    <ul style={{ listStyle: 'none', padding: 0 }}>
                      {framework.key_insights.map((insight, i) => (
                        <li key={i} style={{ display: 'flex', alignItems: 'flex-start', marginBottom: '12px' }}>
                          <span style={{ marginRight: '8px', color: '#f5a623' }}>💡</span>
                          <span style={{ color: '#424245' }}>{insight}</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            ))
          ) : (
            <p style={{ color: '#424245' }}>No framework analysis available</p>
          )}
        </div>

        {/* Show recommendations on execution phase */}
        {activePhase === 'execution' && analysis && (
          <div className={styles.recommendations} style={{ background: '#f5f5f7', padding: '32px', borderRadius: '16px', marginTop: '32px' }}>
            <h3 style={{ color: '#1d1d1f', marginBottom: '24px' }}>Strategic Recommendations</h3>
            <div className={styles.recommendationsList}>
              {analysis.strategic_recommendations && analysis.strategic_recommendations.map((rec, i) => (
                <div key={i} className={styles.recommendation} style={{ display: 'flex', alignItems: 'flex-start', marginBottom: '16px' }}>
                  <span style={{ marginRight: '12px', color: '#007aff' }}>→</span>
                  <p style={{ color: '#424245' }}>{rec}</p>
                </div>
              ))}
            </div>

            <h3 style={{ color: '#1d1d1f', marginTop: '32px', marginBottom: '24px' }}>Immediate Next Steps</h3>
            <div className={styles.nextSteps}>
              {analysis.immediate_next_steps && analysis.immediate_next_steps.map((step, i) => (
                <div key={i} className={styles.step} style={{ display: 'flex', alignItems: 'flex-start', marginBottom: '16px' }}>
                  <span className={styles.stepNumber} style={{ 
                    display: 'inline-flex', 
                    alignItems: 'center', 
                    justifyContent: 'center',
                    width: '32px', 
                    height: '32px', 
                    background: '#007aff', 
                    color: 'white', 
                    borderRadius: '50%', 
                    marginRight: '16px',
                    flexShrink: 0 
                  }}>{i + 1}</span>
                  <p style={{ color: '#424245' }}>{step}</p>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    );
  };

  return (
    <div className={styles.container}>
      <h1 style={{ color: '#1d1d1f', marginBottom: '24px' }}>Strategic Intelligence Report</h1>
      
      {/* Executive Briefing */}
      {analysis && !isLoading && (
        <motion.div 
          className={styles.executiveBriefing}
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
        >
          <h2>Executive Briefing</h2>
          <p>{analysis.executive_briefing}</p>
        </motion.div>
      )}

      {/* Phase Navigation */}
      <div className={styles.phaseNav}>
        <button
          className={`${styles.phaseButton} ${activePhase === 'situation' ? styles.active : ''}`}
          onClick={() => setActivePhase('situation')}
          disabled={isLoading}
        >
          <span className={styles.number}>1</span>
          <div className={styles.phaseInfo}>
            <h4>Where Are We Now?</h4>
            <p>Current Position Analysis</p>
          </div>
        </button>
        
        <div className={styles.phaseSeparator} />
        
        <button
          className={`${styles.phaseButton} ${activePhase === 'strategy' ? styles.active : ''}`}
          onClick={() => setActivePhase('strategy')}
          disabled={isLoading}
        >
          <span className={styles.number}>2</span>
          <div className={styles.phaseInfo}>
            <h4>Where Should We Go?</h4>
            <p>Strategic Options</p>
          </div>
        </button>
        
        <div className={styles.phaseSeparator} />
        
        <button
          className={`${styles.phaseButton} ${activePhase === 'execution' ? styles.active : ''}`}
          onClick={() => setActivePhase('execution')}
          disabled={isLoading}
        >
          <span className={styles.number}>3</span>
          <div className={styles.phaseInfo}>
            <h4>How to Get There?</h4>
            <p>Implementation Roadmap</p>
          </div>
        </button>
      </div>

      {/* Phase Content */}
      {!isLoading && !analysis && !error && (
        <div style={{ textAlign: 'center', padding: '48px', color: '#424245' }}>
          <p>Click here to load the strategic analysis</p>
          <button 
            onClick={loadAnalysis} 
            style={{ 
              marginTop: '16px', 
              padding: '12px 24px', 
              background: '#007aff', 
              color: 'white', 
              border: 'none', 
              borderRadius: '8px', 
              cursor: 'pointer' 
            }}
          >
            Load Analysis
          </button>
        </div>
      )}
      
      <AnimatePresence mode="wait">
        {renderPhaseContent()}
      </AnimatePresence>
    </div>
  );
};