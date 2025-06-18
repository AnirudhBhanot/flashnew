import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import useAssessmentStore from '../store/assessmentStore';
import { Icon } from '../design-system/components';
import styles from './MichelinFrameworkAnalysis.module.scss';

// BCG Matrix Visualization Component
const BCGMatrixVisualization: React.FC<{ data: any }> = ({ data }) => {
  const { x, y, quadrant } = data.visualization_data || {};
  
  console.log('BCG Matrix data:', data);
  console.log('Visualization data:', data.visualization_data);
  console.log('Position - x:', x, 'y:', y, 'quadrant:', quadrant);
  console.log('Metrics:', data.metrics);
  
  // Calculate position in percentage (0-100)
  // BCG Matrix uses log scale for x-axis (relative market share)
  // x > 1 means market leader (right side), x < 1 means follower (left side)
  // We'll use a log scale mapping: 0.1x = 25%, 1x = 50%, 10x = 75%
  const marketShare = x || 0.1; // Default to 0.1 if no data
  const logX = Math.log10(Math.max(0.01, marketShare));
  const xPos = Math.min(95, Math.max(5, 50 + (logX * 25))); // This maps 0.1 to 25%, 1 to 50%, 10 to 75%
  
  // y is market growth rate (0-100%)
  // Map 0% growth to bottom (5%), 20% to middle (50%), 40%+ to top (95%)
  const growthRate = y || 10; // Default to 10% if no data
  const yPos = Math.min(95, Math.max(5, (growthRate / 40) * 90 + 5));
  
  console.log('Position calculation:', {
    marketShare,
    logX,
    xPos,
    growthRate,
    yPos
  });
  
  return (
    <div className={styles.bcgMatrix}>
      <div className={styles.matrixGrid}>
        <div className={styles.quadrant} data-quadrant="star">
          <span>Star</span>
          <p>High Growth, High Share</p>
        </div>
        <div className={styles.quadrant} data-quadrant="question">
          <span>Question Mark</span>
          <p>High Growth, Low Share</p>
        </div>
        <div className={styles.quadrant} data-quadrant="cash-cow">
          <span>Cash Cow</span>
          <p>Low Growth, High Share</p>
        </div>
        <div className={styles.quadrant} data-quadrant="dog">
          <span>Dog</span>
          <p>Low Growth, Low Share</p>
        </div>
        
        {/* Position indicator */}
        <motion.div 
          className={styles.position}
          initial={{ scale: 0 }}
          animate={{ 
            scale: 1,
            left: `${xPos}%`,
            bottom: `${yPos}%`
          }}
          transition={{ type: "spring", stiffness: 100 }}
        >
          <div className={styles.positionDot} />
          <span className={styles.positionLabel}>You</span>
        </motion.div>
      </div>
      
      <div className={styles.axisLabels}>
        <span className={styles.xLabel}>Relative Market Share →</span>
        <span className={styles.yLabel}>Market Growth Rate →</span>
      </div>
    </div>
  );
};

// Porter's Five Forces Visualization
const FiveForcesVisualization: React.FC<{ data: any }> = ({ data }) => {
  const forces = data.metrics || {};
  
  return (
    <div className={styles.fiveForces}>
      <div className={styles.forcesCenter}>
        <h4>Industry Attractiveness</h4>
        <p className={styles.overallScore}>{data.position}</p>
      </div>
      
      {Object.entries(forces).map(([force, details]: any) => (
        <div key={force} className={`${styles.force} ${styles[force]}`}>
          <h5>{force.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}</h5>
          <div className={styles.forceLevel} data-level={details.level?.toLowerCase()}>
            {details.level}
          </div>
          <div className={styles.forceScore}>
            <div 
              className={styles.scoreBar}
              style={{ width: `${(1 - details.score) * 100}%` }}
            />
          </div>
        </div>
      ))}
    </div>
  );
};

// SWOT Matrix Visualization
const SWOTVisualization: React.FC<{ data: any }> = ({ data }) => {
  const swot = data.visualization_data || {};
  
  return (
    <div className={styles.swotMatrix}>
      <div className={styles.swotQuadrant} data-type="strengths">
        <h5>Strengths</h5>
        <ul>
          {swot.strengths?.map((item: string, i: number) => (
            <li key={i}>{item}</li>
          ))}
        </ul>
      </div>
      <div className={styles.swotQuadrant} data-type="weaknesses">
        <h5>Weaknesses</h5>
        <ul>
          {swot.weaknesses?.map((item: string, i: number) => (
            <li key={i}>{item}</li>
          ))}
        </ul>
      </div>
      <div className={styles.swotQuadrant} data-type="opportunities">
        <h5>Opportunities</h5>
        <ul>
          {swot.opportunities?.map((item: string, i: number) => (
            <li key={i}>{item}</li>
          ))}
        </ul>
      </div>
      <div className={styles.swotQuadrant} data-type="threats">
        <h5>Threats</h5>
        <ul>
          {swot.threats?.map((item: string, i: number) => (
            <li key={i}>{item}</li>
          ))}
        </ul>
      </div>
    </div>
  );
};

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8001';

export const MichelinFrameworkAnalysis: React.FC = () => {
  const [activePhase, setActivePhase] = useState<'situation' | 'strategy' | 'execution'>('situation');
  const [analyses, setAnalyses] = useState<any>({
    situation: [],
    strategy: [],
    execution: []
  });
  const [isLoading, setIsLoading] = useState(true);
  
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
    
    console.log('Assessment data:', assessmentData);
    console.log('Market data:', assessmentData?.market);
    console.log('Transformed API data:', apiData);
    console.log('Market share calculation:', {
      marketShare: assessmentData?.market?.marketShare,
      som: assessmentData?.market?.som,
      tam: assessmentData?.market?.tam,
      calculated: Number(assessmentData?.market?.som) / Number(assessmentData?.market?.tam) * 100
    });
    console.log('Final market share:', apiData.market_share_percentage);
    console.log('Market growth:', apiData.market_growth_rate_annual);
    
    // Define frameworks for each phase
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

  const getVisualization = (framework: any) => {
    switch (framework.framework_id) {
      case 'bcg_matrix':
        return <BCGMatrixVisualization data={framework} />;
      case 'porters_five_forces':
        return <FiveForcesVisualization data={framework} />;
      case 'swot_analysis':
        return <SWOTVisualization data={framework} />;
      default:
        return null;
    }
  };

  const renderPhaseContent = () => {
    const phaseData = analyses[activePhase] || [];
    
    if (isLoading) {
      return (
        <div className={styles.loading}>
          <Icon name="arrow.trianglehead.clockwise" size={32} />
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
                  <Icon name="location.fill" size={16} />
                  <span>{analysis.position}</span>
                  {analysis.framework_id === 'bcg_matrix' && analysis.metrics && (
                    <span className={styles.subtext}>
                      ({analysis.metrics.absolute_market_share}% share, {analysis.metrics.market_growth_rate}% growth)
                    </span>
                  )}
                </div>
              </div>

              {/* Framework Visualization */}
              {getVisualization(analysis) && (
                <div className={styles.visualization}>
                  {getVisualization(analysis)}
                </div>
              )}

              {/* Key Insights */}
              <div className={styles.insights}>
                <h4>Key Insights</h4>
                <ul>
                  {analysis.insights.map((insight: string, i: number) => (
                    <li key={i}>
                      <Icon name="lightbulb.fill" size={16} />
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
                      <Icon name="arrow.right.circle.fill" size={16} />
                      <span>{rec}</span>
                    </li>
                  ))}
                </ul>
              </div>
            </motion.div>
          ))}
        </div>

        {/* Phase Summary */}
        {phaseData.length > 0 && (
          <div className={styles.phaseSummary}>
            <h3>
              {activePhase === 'situation' && 'Situation Summary'}
              {activePhase === 'strategy' && 'Strategic Direction'}
              {activePhase === 'execution' && 'Implementation Priorities'}
            </h3>
            <div className={styles.summaryContent}>
              {activePhase === 'situation' && (
                <>
                  <p>Based on our analysis using BCG Matrix, Porter's Five Forces, and SWOT:</p>
                  <ul>
                    <li>Market Position: {phaseData[0]?.position || 'Analyzing...'}</li>
                    <li>Industry Attractiveness: {phaseData[1]?.position || 'Analyzing...'}</li>
                    <li>Overall Assessment: {phaseData[2]?.position || 'Analyzing...'}</li>
                  </ul>
                </>
              )}
              {activePhase === 'strategy' && (
                <>
                  <p>Strategic options based on your current position:</p>
                  <ul>
                    {phaseData[0]?.recommendations.slice(0, 3).map((rec: string, i: number) => (
                      <li key={i}>{rec}</li>
                    ))}
                  </ul>
                </>
              )}
              {activePhase === 'execution' && (
                <>
                  <p>Key implementation priorities:</p>
                  <div className={styles.timeline}>
                    <div className={styles.phase}>
                      <h5>0-30 Days</h5>
                      <p>{phaseData[0]?.recommendations[0]}</p>
                    </div>
                    <div className={styles.phase}>
                      <h5>30-60 Days</h5>
                      <p>{phaseData[0]?.recommendations[1]}</p>
                    </div>
                    <div className={styles.phase}>
                      <h5>60-90 Days</h5>
                      <p>{phaseData[0]?.recommendations[2]}</p>
                    </div>
                  </div>
                </>
              )}
            </div>
          </div>
        )}
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
          <span className={styles.number}>1</span>
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
        >
          <span className={styles.number}>3</span>
          <div className={styles.phaseInfo}>
            <h4>How to Get There?</h4>
            <p>Implementation Plan</p>
          </div>
        </button>
      </div>

      {/* Phase Content */}
      {renderPhaseContent()}
    </div>
  );
};