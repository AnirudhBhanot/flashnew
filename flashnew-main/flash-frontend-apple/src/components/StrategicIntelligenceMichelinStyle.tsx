import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import useAssessmentStore from '../store/assessmentStore';
import { Icon } from '../design-system/components';
import styles from './StrategicIntelligenceMichelinStyle.module.scss';

interface FrameworkAnalysis {
  framework_id: string;
  framework_name: string;
  category: string;
  position: string;
  score: number;
  insights: string[];
  recommendations: string[];
  metrics: any;
  visualization_data: any;
}

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8001';

// Transform assessment data to API format
const transformAssessmentToAPI = (data: any) => {
  const { capital = {}, advantage = {}, market = {}, people = {}, companyInfo = {} } = data;
  
  return {
    startup_name: companyInfo.companyName || 'Unknown Startup',
    total_capital_raised_usd: Number(capital.totalRaised) || 0,
    cash_on_hand_usd: Number(capital.cashOnHand) || 0,
    monthly_burn_usd: Number(capital.monthlyBurn) || 0,
    runway_months: Number(capital.runwayMonths) || 0,
    funding_stage: capital.fundingStage || 'pre_seed',
    investor_tier_primary: capital.primaryInvestor || 'none',
    product_stage: advantage.productStage || 'concept',
    proprietary_tech: advantage.proprietaryTech || false,
    patents_filed: Number(advantage.patentsFiled) || 0,
    monthly_active_users: Number(advantage.monthlyActiveUsers) || 0,
    market_size_usd: Number(market.totalAddressableMarket) || 0,
    market_growth_rate_annual: Number(market.marketGrowthRate) || 0,
    competitor_count: Number(market.competitorCount) || 0,
    market_share_percentage: Number(market.marketShare) || 0,
    customer_acquisition_cost_usd: Number(market.customerAcquisitionCost) || 0,
    lifetime_value_usd: Number(market.lifetimeValue) || 0,
    team_size_full_time: Number(people.fullTimeEmployees) || 1,
    founders_industry_experience_years: Number(people.industryExperience) || 0,
    b2b_or_b2c: market.businessModel || 'b2c',
    sector: market.sector || 'other',
  };
};

export const StrategicIntelligenceMichelinStyle: React.FC = () => {
  const [viewMode, setViewMode] = useState<'where-now' | 'where-go' | 'how-get-there'>('where-now');
  const [situationAnalyses, setSituationAnalyses] = useState<FrameworkAnalysis[]>([]);
  const [strategyAnalyses, setStrategyAnalyses] = useState<FrameworkAnalysis[]>([]);
  const [executionAnalyses, setExecutionAnalyses] = useState<FrameworkAnalysis[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [selectedFramework, setSelectedFramework] = useState<FrameworkAnalysis | null>(null);
  
  const assessmentData = useAssessmentStore(state => state.data);
  const results = useAssessmentStore(state => state.results);

  useEffect(() => {
    if (assessmentData && results) {
      loadFrameworkAnalyses();
    }
  }, [assessmentData, results]);

  const loadFrameworkAnalyses = async () => {
    setIsLoading(true);
    try {
      const apiData = transformAssessmentToAPI(assessmentData);
      console.log('Transformed API data:', apiData);
      console.log('Market share:', apiData.market_share_percentage);
      console.log('Market growth:', apiData.market_growth_rate_annual);
      
      // Load analyses for each phase
      await Promise.all([
        loadPhaseAnalysis('situation', setSituationAnalyses, apiData),
        loadPhaseAnalysis('strategy', setStrategyAnalyses, apiData),
        loadPhaseAnalysis('execution', setExecutionAnalyses, apiData)
      ]);
    } catch (error) {
      console.error('Error loading framework analyses:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const loadPhaseAnalysis = async (phase: string, setSetter: any, apiData: any) => {
    try {
      const response = await fetch(`${API_URL}/api/frameworks/analyze-phase`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          startup_data: apiData,
          phase: phase,
          max_frameworks: 3
        }),
      });

      if (response.ok) {
        const data = await response.json();
        setSetter(data.analyses || []);
      }
    } catch (error) {
      console.error(`Error loading ${phase} analysis:`, error);
      // Fallback to specific frameworks if phase analysis fails
      loadSpecificFrameworks(phase, setSetter, apiData);
    }
  };

  const loadSpecificFrameworks = async (phase: string, setSetter: any, apiData: any) => {
    // Define frameworks for each phase (Michelin-style approach)
    const phaseFrameworks = {
      situation: ['porters_five_forces', 'swot_analysis', 'bcg_matrix'],
      strategy: ['ansoff_matrix', 'blue_ocean', 'jobs_to_be_done'],
      execution: ['lean_canvas', 'value_chain', 'balanced_scorecard']
    };

    const frameworks = phaseFrameworks[phase as keyof typeof phaseFrameworks] || [];
    
    try {
      const response = await fetch(`${API_URL}/api/frameworks/analyze`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          startup_data: apiData,
          framework_ids: frameworks
        }),
      });

      if (response.ok) {
        const data = await response.json();
        setSetter(data.analyses || []);
      }
    } catch (error) {
      console.error(`Error loading specific frameworks for ${phase}:`, error);
    }
  };

  const renderFrameworkCard = (analysis: FrameworkAnalysis, index: number) => (
    <motion.div
      key={analysis.framework_id}
      className={styles.frameworkCard}
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: index * 0.1 }}
      onClick={() => setSelectedFramework(analysis)}
    >
      <div className={styles.frameworkHeader}>
        <h4>{analysis.framework_name}</h4>
        <span className={styles.category}>{analysis.category}</span>
      </div>
      
      <div className={styles.positionBadge}>
        <Icon name="location.fill" size={16} />
        <span>{analysis.position}</span>
      </div>
      
      <div className={styles.score}>
        <div className={styles.scoreBar}>
          <motion.div 
            className={styles.scoreFill}
            initial={{ width: 0 }}
            animate={{ width: `${analysis.score * 100}%` }}
            transition={{ delay: index * 0.1 + 0.3, duration: 0.8 }}
          />
        </div>
        <span>{Math.round(analysis.score * 100)}%</span>
      </div>
      
      <div className={styles.insights}>
        <h5>Key Insights</h5>
        <ul>
          {analysis.insights.slice(0, 2).map((insight, i) => (
            <li key={i}>{insight}</li>
          ))}
        </ul>
      </div>
      
      <button className={styles.viewDetails}>
        View Full Analysis
        <Icon name="chevron.right" size={16} />
      </button>
    </motion.div>
  );

  const renderWhereAreWeNow = () => (
    <div className={styles.phaseContent}>
      <div className={styles.phaseHeader}>
        <h3>Situation Analysis</h3>
        <p>Understanding our current strategic position through business frameworks</p>
      </div>
      
      {isLoading ? (
        <div className={styles.loading}>
          <Icon name="arrow.trianglehead.clockwise" size={32} />
          <p>Analyzing your startup...</p>
        </div>
      ) : (
        <div className={styles.analysisGrid}>
          {situationAnalyses.map((analysis, index) => 
            renderFrameworkCard(analysis, index)
          )}
        </div>
      )}
      
      {situationAnalyses.length > 0 && (
        <div className={styles.summary}>
          <h4>Situation Summary</h4>
          <div className={styles.consensusPosition}>
            <Icon name="target" size={24} />
            <div>
              <h5>Overall Position</h5>
              <p>{situationAnalyses[0]?.position || 'Analyzing...'}</p>
            </div>
          </div>
        </div>
      )}
    </div>
  );

  const renderWhereToGo = () => (
    <div className={styles.phaseContent}>
      <div className={styles.phaseHeader}>
        <h3>Strategic Direction</h3>
        <p>Identifying opportunities and setting strategic goals</p>
      </div>
      
      {isLoading ? (
        <div className={styles.loading}>
          <Icon name="arrow.trianglehead.clockwise" size={32} />
          <p>Generating strategic options...</p>
        </div>
      ) : (
        <div className={styles.analysisGrid}>
          {strategyAnalyses.map((analysis, index) => 
            renderFrameworkCard(analysis, index)
          )}
        </div>
      )}
      
      {strategyAnalyses.length > 0 && (
        <div className={styles.strategicOptions}>
          <h4>Recommended Strategic Directions</h4>
          <div className={styles.optionsList}>
            {strategyAnalyses.flatMap(a => a.recommendations.slice(0, 2)).map((rec, i) => (
              <motion.div
                key={i}
                className={styles.option}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: i * 0.1 }}
              >
                <Icon name="arrow.right.circle.fill" size={20} />
                <span>{rec}</span>
              </motion.div>
            ))}
          </div>
        </div>
      )}
    </div>
  );

  const renderHowToGetThere = () => (
    <div className={styles.phaseContent}>
      <div className={styles.phaseHeader}>
        <h3>Implementation Roadmap</h3>
        <p>Execution frameworks to achieve strategic goals</p>
      </div>
      
      {isLoading ? (
        <div className={styles.loading}>
          <Icon name="arrow.trianglehead.clockwise" size={32} />
          <p>Building implementation plan...</p>
        </div>
      ) : (
        <div className={styles.analysisGrid}>
          {executionAnalyses.map((analysis, index) => 
            renderFrameworkCard(analysis, index)
          )}
        </div>
      )}
      
      {executionAnalyses.length > 0 && (
        <div className={styles.roadmap}>
          <h4>Implementation Priorities</h4>
          <div className={styles.timeline}>
            {['30 Days', '60 Days', '90 Days'].map((phase, index) => (
              <motion.div
                key={phase}
                className={styles.timelinePhase}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.2 }}
              >
                <div className={styles.phaseLabel}>{phase}</div>
                <div className={styles.phaseActions}>
                  {executionAnalyses[index]?.recommendations.slice(0, 2).map((rec, i) => (
                    <div key={i} className={styles.action}>
                      <Icon name="checkmark.circle" size={16} />
                      <span>{rec}</span>
                    </div>
                  ))}
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      )}
    </div>
  );

  return (
    <div className={styles.container}>
      {/* Tab Navigation */}
      <div className={styles.tabNav}>
        <button
          className={`${styles.tab} ${viewMode === 'where-now' ? styles.active : ''}`}
          onClick={() => setViewMode('where-now')}
        >
          <Icon name="location" size={20} />
          <span>Where Are We Now?</span>
        </button>
        <button
          className={`${styles.tab} ${viewMode === 'where-go' ? styles.active : ''}`}
          onClick={() => setViewMode('where-go')}
        >
          <Icon name="flag" size={20} />
          <span>Where Should We Go?</span>
        </button>
        <button
          className={`${styles.tab} ${viewMode === 'how-get-there' ? styles.active : ''}`}
          onClick={() => setViewMode('how-get-there')}
        >
          <Icon name="map" size={20} />
          <span>How to Get There?</span>
        </button>
      </div>

      {/* Content */}
      <AnimatePresence mode="wait">
        <motion.div
          key={viewMode}
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          className={styles.content}
        >
          {viewMode === 'where-now' && renderWhereAreWeNow()}
          {viewMode === 'where-go' && renderWhereToGo()}
          {viewMode === 'how-get-there' && renderHowToGetThere()}
        </motion.div>
      </AnimatePresence>

      {/* Framework Detail Modal */}
      <AnimatePresence>
        {selectedFramework && (
          <motion.div
            className={styles.modal}
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={() => setSelectedFramework(null)}
          >
            <motion.div
              className={styles.modalContent}
              initial={{ scale: 0.9, y: 20 }}
              animate={{ scale: 1, y: 0 }}
              exit={{ scale: 0.9, y: 20 }}
              onClick={(e) => e.stopPropagation()}
            >
              <button 
                className={styles.closeButton}
                onClick={() => setSelectedFramework(null)}
              >
                <Icon name="xmark" size={24} />
              </button>
              
              <h3>{selectedFramework.framework_name}</h3>
              
              <div className={styles.detailSection}>
                <h4>Position & Score</h4>
                <div className={styles.positionDetail}>
                  <span className={styles.position}>{selectedFramework.position}</span>
                  <span className={styles.score}>{Math.round(selectedFramework.score * 100)}%</span>
                </div>
              </div>
              
              <div className={styles.detailSection}>
                <h4>Analysis Insights</h4>
                <ul>
                  {selectedFramework.insights.map((insight, i) => (
                    <li key={i}>{insight}</li>
                  ))}
                </ul>
              </div>
              
              <div className={styles.detailSection}>
                <h4>Recommendations</h4>
                <ul>
                  {selectedFramework.recommendations.map((rec, i) => (
                    <li key={i}>{rec}</li>
                  ))}
                </ul>
              </div>
              
              {selectedFramework.visualization_data && (
                <div className={styles.detailSection}>
                  <h4>Framework Metrics</h4>
                  <pre className={styles.metrics}>
                    {JSON.stringify(selectedFramework.metrics, null, 2)}
                  </pre>
                </div>
              )}
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};