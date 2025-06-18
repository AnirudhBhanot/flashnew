import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import useAssessmentStore from '../store/assessmentStore';
import styles from './StrategicFrameworkReport.module.scss';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8001';

interface FrameworkAnalysis {
  framework_id: string;
  framework_name: string;
  position: string;
  score: number;
  insights: string[];
  recommendations: string[];
  metrics?: any;
}

interface FrameworkRecommendation {
  framework_id: string;
  framework_name: string;
  relevance_score: number;
  reasoning: string;
}

export const StrategicFrameworkReport: React.FC = () => {
  const [analyses, setAnalyses] = useState<FrameworkAnalysis[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [selectedFramework, setSelectedFramework] = useState<string>('');
  const [recommendations, setRecommendations] = useState<FrameworkRecommendation[]>([]);
  
  const assessmentData = useAssessmentStore(state => state.data);
  const results = useAssessmentStore(state => state.results);

  useEffect(() => {
    if (assessmentData) {
      loadSmartFrameworkAnalyses();
    }
  }, [assessmentData]);

  const selectSmartFrameworks = (assessmentData: any, apiData: any) => {
    const stage = assessmentData.capital?.fundingStage || 'pre-seed';
    const sector = assessmentData.market?.sector || 'technology';
    const teamSize = Number(assessmentData.people?.fullTimeEmployees) || 1;
    const monthlyBurn = Number(assessmentData.capital?.monthlyBurn) || 0;
    const runway = Number(assessmentData.capital?.runwayMonths) || 0;
    const productStage = assessmentData.advantage?.productStage || 'concept';
    
    // Smart framework selection based on startup characteristics
    const frameworks: string[] = [];
    
    // Always include fundamental frameworks
    frameworks.push('bcg_matrix'); // For market position
    frameworks.push('swot_analysis'); // For comprehensive analysis
    
    // Stage-specific frameworks
    if (stage === 'pre-seed' || stage === 'seed') {
      frameworks.push('lean_canvas'); // For early stage planning
      frameworks.push('customer_development'); // For finding product-market fit
      frameworks.push('mom_test'); // For customer validation
    } else if (stage === 'series-a' || stage === 'series-b') {
      frameworks.push('ansoff_matrix'); // For growth strategy
      frameworks.push('growth_share_matrix'); // For portfolio decisions
      frameworks.push('okr_framework'); // For scaling operations
    } else {
      frameworks.push('balanced_scorecard'); // For mature operations
      frameworks.push('blue_ocean'); // For innovation
      frameworks.push('mckinsey_7s'); // For organizational alignment
    }
    
    // Challenge-specific frameworks
    if (runway < 6) {
      frameworks.push('unit_economics'); // For burn rate optimization
      frameworks.push('cash_flow_quadrant'); // For financial planning
    }
    
    if (teamSize < 10) {
      frameworks.push('agile_scrum'); // For small team efficiency
    } else {
      frameworks.push('organizational_culture'); // For team alignment
    }
    
    // Industry-specific frameworks
    if (sector === 'saas' || sector === 'software') {
      frameworks.push('saas_metrics'); // SaaS-specific KPIs
      frameworks.push('rule_of_40'); // SaaS growth efficiency
    } else if (sector === 'e-commerce' || sector === 'retail') {
      frameworks.push('customer_journey'); // For conversion optimization
      frameworks.push('rfm_analysis'); // For customer segmentation
    } else if (sector === 'healthcare' || sector === 'healthtech') {
      frameworks.push('patient_journey'); // Healthcare-specific
      frameworks.push('regulatory_compliance'); // For compliance
    }
    
    // Product stage frameworks
    if (productStage === 'concept' || productStage === 'mvp') {
      frameworks.push('design_thinking'); // For product development
    } else if (productStage === 'growth') {
      frameworks.push('growth_hacking'); // For rapid growth
    }
    
    // Competition frameworks
    frameworks.push('porters_five_forces'); // Always useful for competition
    
    // Return unique frameworks, limit to 8-10 for UI clarity
    return [...new Set(frameworks)].slice(0, 10);
  };

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
      product_stage: advantage.productStage || 'concept',
      proprietary_tech: advantage.proprietaryTech || false,
      patents_filed: Number(advantage.patentsFiled) || 0,
      monthly_active_users: Number(advantage.monthlyActiveUsers) || 0,
      market_size_usd: Number(market.tam) || 0,
      market_growth_rate_annual: Number(market.marketGrowthRate) || 15,
      competitor_count: Number(market.competitorCount) || 0,
      market_share_percentage: Number(market.marketShare) || (Number(market.som) && Number(market.sam) ? Number(market.som) / Number(market.sam) * 100 : 2.5),
      customer_acquisition_cost_usd: Number(market.customerAcquisitionCost) || 100,
      lifetime_value_usd: Number(market.lifetimeValue) || 300,
      team_size_full_time: Number(people.fullTimeEmployees) || 1,
      founders_industry_experience_years: Number(people.industryExperience) || 0,
      b2b_or_b2c: market.businessModel || 'b2c',
      sector: market.sector || 'other',
    };
  };

  const loadSmartFrameworkAnalyses = async () => {
    setIsLoading(true);
    const apiData = transformData(assessmentData);
    
    try {
      // Use intelligent framework selection based on startup stage and metrics
      const frameworkIds = selectSmartFrameworks(assessmentData, apiData);
      
      // Analyze with the selected frameworks
      const analyzeResponse = await fetch(`${API_URL}/api/frameworks/analyze`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          startup_data: apiData,
          framework_ids: frameworkIds
        })
      });

      if (analyzeResponse.ok) {
        const data = await analyzeResponse.json();
        setAnalyses(data.analyses || []);
        // Set first framework as selected
        if (data.analyses && data.analyses.length > 0) {
          setSelectedFramework(data.analyses[0].framework_id);
        }
      }
    } catch (error) {
      console.error('Error loading smart analyses:', error);
      // Fallback to default frameworks if smart selection fails
      loadDefaultFrameworks();
    } finally {
      setIsLoading(false);
    }
  };

  const loadDefaultFrameworks = async () => {
    const apiData = transformData(assessmentData);
    const frameworks = ['bcg_matrix', 'porters_five_forces', 'swot_analysis', 'ansoff_matrix'];
    
    try {
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
        setAnalyses(data.analyses || []);
        if (data.analyses && data.analyses.length > 0) {
          setSelectedFramework(data.analyses[0].framework_id);
        }
      }
    } catch (error) {
      console.error('Error loading default analyses:', error);
    }
  };

  const getFrameworkIcon = (frameworkId: string) => {
    // Generic icons based on framework category
    if (frameworkId.includes('matrix') || frameworkId.includes('grid')) {
      return (
        <svg viewBox="0 0 24 24" fill="none">
          <rect x="3" y="3" width="8" height="8" stroke="currentColor" strokeWidth="1.5"/>
          <rect x="13" y="3" width="8" height="8" stroke="currentColor" strokeWidth="1.5"/>
          <rect x="3" y="13" width="8" height="8" stroke="currentColor" strokeWidth="1.5"/>
          <rect x="13" y="13" width="8" height="8" stroke="currentColor" strokeWidth="1.5"/>
        </svg>
      );
    }
    if (frameworkId.includes('force') || frameworkId.includes('analysis')) {
      return (
        <svg viewBox="0 0 24 24" fill="none">
          <polygon points="12,2 22,8.5 18,20 6,20 2,8.5" stroke="currentColor" strokeWidth="1.5" fill="none"/>
          <circle cx="12" cy="12" r="3" stroke="currentColor" strokeWidth="1.5"/>
        </svg>
      );
    }
    if (frameworkId.includes('canvas') || frameworkId.includes('model')) {
      return (
        <svg viewBox="0 0 24 24" fill="none">
          <rect x="3" y="3" width="18" height="18" stroke="currentColor" strokeWidth="1.5" rx="2"/>
          <path d="M3 9h18M9 3v18M15 3v18" stroke="currentColor" strokeWidth="1.5"/>
        </svg>
      );
    }
    // Default icon
    return (
      <svg viewBox="0 0 24 24" fill="none">
        <path d="M12 2l2.09 6.26L21 9l-5.45 3.96L17 21l-5-3.72L7 21l1.45-8.04L3 9l6.91-.74L12 2z" stroke="currentColor" strokeWidth="1.5" fill="none"/>
      </svg>
    );
  };

  const getPositionColor = (position: string) => {
    const colors: Record<string, string> = {
      'Star': '#34C759',
      'Question Mark': '#FF9500',
      'Cash Cow': '#007AFF',
      'Dog': '#FF3B30',
      'Strong': '#34C759',
      'Moderate': '#FF9500',
      'Weak': '#FF3B30',
      'High Attractiveness': '#34C759',
      'Moderate Attractiveness': '#FF9500',
      'Low Attractiveness': '#FF3B30'
    };
    return colors[position] || '#86868B';
  };

  const selectedAnalysis = analyses.find(a => a.framework_id === selectedFramework);

  if (isLoading) {
    return (
      <div className={styles.container}>
        <div className={styles.loading}>
          <div className={styles.loadingIcon}>
            <div className={styles.spinner} />
          </div>
          <p>Analyzing strategic position...</p>
        </div>
      </div>
    );
  }

  return (
    <div className={styles.container}>
      <div className={styles.header}>
        <p>Intelligently selected frameworks based on your startup's specific situation</p>
      </div>

      <div className={styles.content}>
        {/* Framework Selector */}
        <div className={styles.frameworkSelector}>
          {analyses.map((analysis) => (
            <button
              key={analysis.framework_id}
              className={`${styles.frameworkTab} ${selectedFramework === analysis.framework_id ? styles.active : ''}`}
              onClick={() => setSelectedFramework(analysis.framework_id)}
            >
              <div className={styles.tabIcon}>
                {getFrameworkIcon(analysis.framework_id)}
              </div>
              <span>{analysis.framework_name}</span>
            </button>
          ))}
        </div>

        {/* Analysis Display */}
        <AnimatePresence mode="wait">
          {selectedAnalysis && (
            <motion.div
              key={selectedFramework}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              transition={{ duration: 0.3 }}
              className={styles.analysisContent}
            >
              {/* Position Card */}
              <div className={styles.positionCard}>
                <div className={styles.positionHeader}>
                  <h3>Current Position</h3>
                  <div 
                    className={styles.positionBadge}
                    style={{ backgroundColor: getPositionColor(selectedAnalysis.position) }}
                  >
                    {selectedAnalysis.position}
                  </div>
                </div>
                
                {/* Framework-specific visualization */}
                {selectedFramework === 'bcg_matrix' && selectedAnalysis.metrics && (
                  <div className={styles.metrics}>
                    <div className={styles.metric}>
                      <span className={styles.metricLabel}>Market Share</span>
                      <span className={styles.metricValue}>
                        {selectedAnalysis.metrics.absolute_market_share?.toFixed(1)}%
                      </span>
                    </div>
                    <div className={styles.metric}>
                      <span className={styles.metricLabel}>Market Growth</span>
                      <span className={styles.metricValue}>
                        {selectedAnalysis.metrics.market_growth_rate?.toFixed(0)}%
                      </span>
                    </div>
                  </div>
                )}

                {selectedFramework === 'porters_five_forces' && selectedAnalysis.metrics && (
                  <div className={styles.forcesList}>
                    {Object.entries(selectedAnalysis.metrics).map(([force, details]: any) => (
                      <div key={force} className={styles.forceItem}>
                        <span>{force.replace(/_/g, ' ').replace(/\b\w/g, (l: string) => l.toUpperCase())}</span>
                        <div className={styles.forceLevel} data-level={details.level?.toLowerCase()}>
                          {details.level}
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </div>

              {/* Key Insights */}
              <div className={styles.insightsSection}>
                <h3>Key Insights</h3>
                <div className={styles.insightsList}>
                  {selectedAnalysis.insights.map((insight, index) => (
                    <motion.div
                      key={index}
                      initial={{ opacity: 0, x: -20 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ delay: index * 0.1 }}
                      className={styles.insightItem}
                    >
                      <div className={styles.insightIcon}>
                        <div className={styles.insightDot} />
                      </div>
                      <p>{insight}</p>
                    </motion.div>
                  ))}
                </div>
              </div>

              {/* Strategic Recommendations */}
              <div className={styles.recommendationsSection}>
                <h3>Strategic Recommendations</h3>
                <div className={styles.recommendationsList}>
                  {selectedAnalysis.recommendations.map((rec, index) => (
                    <motion.div
                      key={index}
                      initial={{ opacity: 0, x: -20 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ delay: index * 0.1 }}
                      className={styles.recommendationItem}
                    >
                      <div className={styles.recommendationNumber}>{index + 1}</div>
                      <p>{rec}</p>
                    </motion.div>
                  ))}
                </div>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>

      {/* Summary Stats */}
      <div className={styles.summaryBar}>
        <div className={styles.summaryItem}>
          <span className={styles.summaryLabel}>Success Probability</span>
          <span className={styles.summaryValue}>
            {results ? `${Math.round((results.successProbability || 0) * 100)}%` : 'N/A'}
          </span>
        </div>
        <div className={styles.summaryItem}>
          <span className={styles.summaryLabel}>Primary Challenge</span>
          <span className={styles.summaryValue}>
            {results?.scores ? 
              Object.entries(results.scores)
                .sort(([,a], [,b]) => a - b)[0][0]
                .charAt(0).toUpperCase() + 
              Object.entries(results.scores)
                .sort(([,a], [,b]) => a - b)[0][0].slice(1)
              : 'N/A'
            }
          </span>
        </div>
        <div className={styles.summaryItem}>
          <span className={styles.summaryLabel}>Frameworks Analyzed</span>
          <span className={styles.summaryValue}>{analyses.length}</span>
        </div>
        {recommendations.length > 0 && (
          <div className={styles.summaryItem}>
            <span className={styles.summaryLabel}>AI Selected</span>
            <span className={styles.summaryValue}>✓</span>
          </div>
        )}
      </div>
    </div>
  );
};