import React, { useState, useRef, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { createRoot } from 'react-dom/client';
import { InvestmentMemo } from './InvestmentMemo';
import { ScoreCard } from './ScoreCard';
import { ScoreCardV17 } from './ScoreCardV17';
import { IndustryBenchmarksV17 } from './IndustryBenchmarksV17';
import { PerformanceSummaryV17 } from './PerformanceSummaryV17';
import StrategicIntelligence from './assessment/StrategicIntelligence';
import { configService } from '../../services/LegacyConfigService';
import { llmService } from '../../services/llmService';
import { getBenchmarksForSectorStage, calculatePercentile, extractBenchmarkValue } from '../../industry_benchmarks';
import { 
  useConfiguration, 
  useSuccessThresholds, 
  useImprovementCalculator,
  useAnimationConfig,
  useNumberFormatter,
  useMetricThreshold,
  useStageAwareThreshold,
  useDefaults,
  useConfigValue
} from '../../hooks/useConfiguration';
import './AnalysisResults.css';

interface AnalysisResultsProps {
  data: any;
  onExportPDF?: () => void;
}

export const AnalysisResults: React.FC<AnalysisResultsProps> = ({ data, onExportPDF }) => {
  const [activeView, setActiveView] = useState<'overview' | 'camp' | 'insights' | 'recommendations' | 'strategic'>('overview');
  const [expandedCAMP, setExpandedCAMP] = useState<string | null>(null);
  const [showQuickSummary, setShowQuickSummary] = useState(false);
  const [expandedMetrics, setExpandedMetrics] = useState<Set<string>>(new Set());
  const [simulatedImprovements, setSimulatedImprovements] = useState<Record<string, Set<string>>>({
    capital: new Set(),
    advantage: new Set(),
    market: new Set(),
    people: new Set()
  });
  const [completedActions, setCompletedActions] = useState<Set<number>>(new Set());
  const [showGlossary, setShowGlossary] = useState<string | null>(null);
  const printRef = useRef<HTMLDivElement>(null);
  const [legacyConfig, setLegacyConfig] = useState<any>(null);
  const printTimeoutRefs = useRef<NodeJS.Timeout[]>([]);
  
  // LLM Integration State
  const [llmRecommendations, setLlmRecommendations] = useState<any>(null);
  const [isLoadingLLM, setIsLoadingLLM] = useState(false);
  const [llmAvailable, setLlmAvailable] = useState(false);
  const [showAIBadge, setShowAIBadge] = useState(false);
  const [dynamicWhatIfResult, setDynamicWhatIfResult] = useState<any>(null);
  const [isLoadingWhatIf, setIsLoadingWhatIf] = useState(false);
  
  // Configuration hooks
  const { config, isFeatureEnabled } = useConfiguration();
  const successThresholds = useSuccessThresholds(data.funding_stage, data.sector);
  const improvementCalculator = useImprovementCalculator(data.success_probability || 0.5);
  const animationConfig = useAnimationConfig();
  const numberFormatter = useNumberFormatter();
  const defaults = useDefaults();
  
  // Get metric thresholds
  const burnThresholds = useStageAwareThreshold('thresholds.risk.burnMultiple', data.funding_stage, data.sector) || {};
  const teamThresholds = useStageAwareThreshold('thresholds.metrics.team.size', data.funding_stage, data.sector) || {};
  const experienceThresholds = useConfigValue('thresholds.metrics.team.experience') || {};
  // const marketThresholds = useMetricThreshold('market', data.funding_stage, data.sector);

  // Load configuration on mount
  useEffect(() => {
    configService.getAllConfig().then(setLegacyConfig);
    
    // Check LLM availability
    checkLLMAvailability();
    
    // Cleanup print timeouts on unmount
    return () => {
      printTimeoutRefs.current.forEach(timeout => clearTimeout(timeout));
      printTimeoutRefs.current = [];
    };
  }, []);
  
  // Fetch LLM recommendations when data changes
  useEffect(() => {
    if (data && llmAvailable) {
      fetchLLMRecommendations();
    }
  }, [data, llmAvailable]);

  // Helper function for toggling metric expansion
  const toggleMetricExpansion = (metricId: string) => {
    setExpandedMetrics(prev => {
      const newSet = new Set(prev);
      if (newSet.has(metricId)) {
        newSet.delete(metricId);
      } else {
        newSet.add(metricId);
      }
      return newSet;
    });
  };

  // Handle PDF export
  const handleExportPDF = () => {
    const printContainer = document.createElement('div');
    printContainer.style.position = 'absolute';
    printContainer.style.left = '-9999px';
    printContainer.style.top = '0';
    printContainer.className = 'print-only-container';
    document.body.appendChild(printContainer);

    const root = createRoot(printContainer);
    root.render(<InvestmentMemo data={data} />);
    
    const timeout1 = setTimeout(() => {
      window.print();
      const timeout2 = setTimeout(() => {
        root.unmount();
        document.body.removeChild(printContainer);
      }, 100);
      printTimeoutRefs.current.push(timeout2);
    }, 100);
    printTimeoutRefs.current.push(timeout1);
  };
  
  // LLM Integration Functions
  const checkLLMAvailability = async () => {
    try {
      const available = await llmService.isAvailable();
      setLlmAvailable(available);
    } catch (error) {
      console.error('Failed to check LLM availability:', error);
      setLlmAvailable(false);
    }
  };
  
  const fetchLLMRecommendations = async () => {
    setIsLoadingLLM(true);
    try {
      const scores = {
        capital: data.camp_scores?.capital || data.pillar_scores?.capital || 0.5,
        advantage: data.camp_scores?.advantage || data.pillar_scores?.advantage || 0.5,
        market: data.camp_scores?.market || data.pillar_scores?.market || 0.5,
        people: data.camp_scores?.people || data.pillar_scores?.people || 0.5,
        success_probability: data.success_probability || 0.5
      };
      
      const response = await llmService.getRecommendations(
        data.userInput || {},
        scores,
        data.verdict
      );
      
      if (response.type === 'ai_generated') {
        setLlmRecommendations(response.recommendations);
        setShowAIBadge(true);
      }
    } catch (error) {
      console.error('Failed to fetch LLM recommendations:', error);
      // Fall back to static recommendations
    } finally {
      setIsLoadingLLM(false);
    }
  };
  
  const calculateDynamicWhatIf = async (improvements: any[]) => {
    const currentScores = {
      capital: data.camp_scores?.capital || data.pillar_scores?.capital || 0.5,
      advantage: data.camp_scores?.advantage || data.pillar_scores?.advantage || 0.5,
      market: data.camp_scores?.market || data.pillar_scores?.market || 0.5,
      people: data.camp_scores?.people || data.pillar_scores?.people || 0.5,
      success_probability: data.success_probability || 0.5
    };
    
    if (!llmAvailable) {
      // Return current scores unchanged
      return {
        new_probability: { value: data.success_probability || 0.5 },
        new_scores: currentScores
      };
    }
    
    setIsLoadingWhatIf(true);
    try {
      
      const whatIfResult = await llmService.analyzeWhatIf(
        data.userInput || {},
        currentScores,
        improvements
      );
      
      setDynamicWhatIfResult(whatIfResult);
      return whatIfResult;
    } catch (error) {
      console.error('Dynamic what-if failed:', error);
      // Return current scores unchanged
      return {
        new_probability: { value: data.success_probability || 0.5 },
        new_scores: currentScores
      };
    } finally {
      setIsLoadingWhatIf(false);
    }
  };

  // Calculate derived metrics
  const successProbability = data.success_probability || 0.5;
  const confidenceScore = data.confidence_score || 0.5;
  const verdict = data.verdict || 'CONDITIONAL PASS';
  const riskLevel = data.risk_level || 'MEDIUM';
  

  // Helper functions
  const getVerdictDisplay = (probability: number) => {
    const level = successThresholds.getLevel(probability);
    const message = successThresholds.getMessage(probability);
    const emoji = successThresholds.getEmoji(probability);
    const className = successThresholds.getClassName(probability);
    
    return {
      text: message,
      emoji: emoji,
      class: className
    };
  };

  const getSuccessColor = (probability: number) => {
    return successThresholds.getColor(probability);
  };

  const formatPercentage = (value: number) => `${(value * 100).toFixed(0)}%`;

  const verdictInfo = getVerdictDisplay(successProbability);

  // Term Tooltip Component
  const TermTooltip: React.FC<{term: string, definition: string}> = ({term, definition}) => {
    const [showTooltip, setShowTooltip] = useState(false);
    
    return (
      <span className="term-tooltip-wrapper">
        <span 
          className="term-highlight"
          onMouseEnter={() => setShowTooltip(true)}
          onMouseLeave={() => setShowTooltip(false)}
        >
          {term}
        </span>
        {showTooltip && (
          <motion.div 
            className="tooltip-content"
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
          >
            <h5>{term}</h5>
            <p>{definition}</p>
          </motion.div>
        )}
      </span>
    );
  };

  // Metric Card Component
  const MetricCard: React.FC<{
    icon: string;
    title: string;
    metrics: Array<{label: string, value: string, tooltip: string}>;
    insight: string;
    cardData: any;
  }> = ({ icon, title, metrics, insight, cardData }) => {
    const cardId = title.toLowerCase().replace(/\s+/g, '-');
    const isExpanded = expandedMetrics.has(cardId);
    
    return (
      <div className="summary-card metric-card-expandable">
        <span className="summary-icon">{icon}</span>
        <h3>{title}</h3>
        <div className="summary-metrics">
          {metrics.map((metric, idx) => (
            <div key={idx} className="metric-row">
              <span>
                <TermTooltip term={metric.label} definition={metric.tooltip} />:
              </span>
              <strong>{metric.value}</strong>
            </div>
          ))}
        </div>
        <p className="summary-insight">{insight}</p>
        
        <button 
          className="expand-indicator"
          onClick={() => toggleMetricExpansion(cardId)}
        >
          {isExpanded ? '− Less Details' : '+ More Details'}
        </button>
        
        {isExpanded && (
          <motion.div 
            className="metric-details"
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
          >
            <div className="calculation-breakdown">
              <h5>How we calculated this:</h5>
              {title === 'Financial Health' && (
                <>
                  <div className="formula">
                    Burn Multiple = Net Burn ÷ Net New ARR
                  </div>
                  <div className="components">
                    <div className="component">
                      <span>Monthly Burn:</span>
                      <span>${((cardData.last_round_raised_usd || 10000000) / (Math.round(cardData.runway_months) || 12) / 1000).toFixed(0)}k</span>
                    </div>
                    <div className="component">
                      <span>Monthly New ARR:</span>
                      <span>${((cardData.current_arr || 1000000) * (cardData.revenue_growth_rate_percent || 100) / 100 / 12 / 1000).toFixed(0)}k</span>
                    </div>
                  </div>
                </>
              )}
            </div>
          </motion.div>
        )}
      </div>
    );
  };

  // Get stage-specific weights using actual CAMP framework
  const getStageWeights = () => {
    const stage = data.funding_stage || 'Series A';
    
    // Map funding stage to the format used in CAMP framework
    const stageKey = stage.toLowerCase().replace(/\s+/g, '_').replace('-', '_');
    
    // Use configuration or fallback to constants
    const campWeights = legacyConfig?.stageWeights || config.business.stageWeights;
    
    const weights = campWeights[stageKey] || campWeights.series_a;
    
    // Convert CAMP weights to display format
    const campDescriptions: Record<string, string> = {
      capital: 'Financial efficiency, burn rate, and path to profitability',
      advantage: 'Competitive moat, differentiation, and defensibility',
      market: 'TAM size, growth rate, and market capture potential',
      people: 'Team experience, execution capability, and leadership'
    };
    
    // Sort by weight descending
    return Object.entries(weights)
      .sort(([,a], [,b]) => (b as number) - (a as number))
      .map(([pillar, weight]) => ({
        area: pillar.charAt(0).toUpperCase() + pillar.slice(1),
        weight: Math.round((weight as number) * 100),
        description: campDescriptions[pillar as string]
      }));
  };

  // CAMP explanations
  const getCampExplanation = (pillar: string) => {
    const explanations: Record<string, { title: string, description: string, factors: string[] }> = {
      capital: {
        title: 'Capital Efficiency',
        description: 'How effectively you use capital to generate growth',
        factors: [
          'Burn Multiple: Cash burned per dollar of revenue growth',
          'Runway: Months of operations with current cash',
          'LTV/CAC Ratio: Customer value vs acquisition cost',
          'Gross Margins: Revenue after direct costs'
        ]
      },
      advantage: {
        title: 'Competitive Advantage',
        description: 'Your unique position and defensibility in the market',
        factors: [
          'Product Differentiation: Unique features and value prop',
          'Technical Moat: Patents, proprietary tech, or data',
          'Network Effects: Value increases with more users',
          'Brand Recognition: Market awareness and reputation'
        ]
      },
      market: {
        title: 'Market Opportunity',
        description: 'Size and growth potential of your target market',
        factors: [
          'TAM Size: Total addressable market in dollars',
          'Market Growth Rate: Annual market expansion',
          'Market Share: Your current and potential share',
          'Market Timing: Readiness for your solution'
        ]
      },
      people: {
        title: 'Team Strength',
        description: 'Quality and experience of your team',
        factors: [
          'Founder Experience: Years in industry/startups',
          'Team Completeness: Coverage of key roles',
          'Advisory Board: Quality of advisors',
          'Culture & Retention: Employee satisfaction'
        ]
      }
    };
    return explanations[pillar] || { title: '', description: '', factors: [] };
  };

  return (
    <div className="analysis-results">
      {/* Page Background Effects */}
      <div className="page-background-effects">
        <div className="gradient-orb page-orb-1"></div>
        <div className="gradient-orb page-orb-2"></div>
        <div className="gradient-orb page-orb-3"></div>
        <div className="page-grid-pattern"></div>
      </div>

      {/* Header Section */}
      <motion.div 
        className="results-header-section"
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
      >
        <div className="results-title">
          <h1>Your Startup Assessment Results</h1>
          <p className="subtitle">Comprehensive analysis based on {config.business.analysis.successFactors} success factors</p>
        </div>
        <button className="export-pdf-btn" onClick={handleExportPDF}>
          <svg className="icon" width="20" height="20" viewBox="0 0 20 20" fill="none">
            <path d="M11.5 2.5H4C3.17 2.5 2.5 3.17 2.5 4V16C2.5 16.83 3.17 17.5 4 17.5H16C16.83 17.5 17.5 16.83 17.5 16V8.5L11.5 2.5Z" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
            <path d="M11.5 2.5V8.5H17.5" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
            <path d="M10 13.5L10 10.5M10 10.5L8 12.5M10 10.5L12 12.5" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
          </svg>
          Export Report
        </button>
      </motion.div>

      {/* Quick Summary Card */}
      <motion.div 
        className="quick-summary-card"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.05 }}
      >
        <div className="summary-header">
          <span className="icon">📋</span>
          <h3>Assessment Summary</h3>
          <button 
            className="expand-btn"
            onClick={() => setShowQuickSummary(!showQuickSummary)}
          >
            {showQuickSummary ? 'Hide Details' : 'View Details'}
          </button>
        </div>
        {showQuickSummary && (
          <motion.div 
            className="summary-content"
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
          >
            <div className="summary-item">
              <span className="label">Assessment Type:</span>
              <span className="value">{data.funding_stage || 'Series A'} Stage Startup</span>
            </div>
            <div className="summary-item">
              <span className="label">Industry:</span>
              <span className="value">{data.industry || 'Technology'}</span>
            </div>
            <div className="summary-item">
              <span className="label">Analysis Date:</span>
              <span className="value">{new Date().toLocaleDateString()}</span>
            </div>
            <div className="summary-item">
              <span className="label">Confidence Level:</span>
              <span className="value">{
                confidenceScore >= config.thresholds.success.confidence.high ? 'High' : 
                confidenceScore >= config.thresholds.success.confidence.moderate ? 'Moderate' : 
                'Low'
              }</span>
            </div>
          </motion.div>
        )}
      </motion.div>

      {/* Success Score Card - New Design */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.1 }}
        style={{ 
          margin: '48px auto',
          width: '100%',
          display: 'flex',
          justifyContent: 'center'
        }}
      >
        <ScoreCard
        score={successProbability * 100}
        verdict={data.verdict || 'PASS'}
        confidence={
          confidenceScore >= config.thresholds.success.confidence.high ? 'High' : 
          confidenceScore >= config.thresholds.success.confidence.moderate ? 'Moderate' : 
          'Low'
        }
        message={
          successProbability >= 0.65 
            ? "Your startup demonstrates strong fundamentals across multiple dimensions. The AI models show high confidence in your potential for success."
            : successProbability >= 0.50
            ? "Your startup shows promise but has areas that need attention. Focus on the recommendations below to improve your success probability."
            : "Your startup needs significant improvements in key areas. Use this analysis to identify and address critical gaps."
        }
        stage={formatStageName(data.funding_stage)}
      />
      </motion.div>

      {/* View Toggle */}
      <motion.div 
        className="view-toggle"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.2 }}
      >
        <button 
          className={`view-btn ${activeView === 'overview' ? 'active' : ''}`}
          onClick={() => setActiveView('overview')}
        >
          <svg className="btn-icon" width="20" height="20" viewBox="0 0 20 20" fill="none">
            <rect x="3" y="10" width="4" height="7" rx="1" fill="currentColor"/>
            <rect x="8" y="6" width="4" height="11" rx="1" fill="currentColor"/>
            <rect x="13" y="3" width="4" height="14" rx="1" fill="currentColor"/>
          </svg>
          Overview
        </button>
        <button 
          className={`view-btn ${activeView === 'camp' ? 'active' : ''}`}
          onClick={() => setActiveView('camp')}
        >
          <svg className="btn-icon" width="20" height="20" viewBox="0 0 20 20" fill="none">
            <circle cx="10" cy="10" r="7" stroke="currentColor" strokeWidth="2" fill="none"/>
            <circle cx="10" cy="10" r="3" fill="currentColor"/>
            <path d="M10 1V5M10 15V19M1 10H5M15 10H19" stroke="currentColor" strokeWidth="2"/>
          </svg>
          CAMP Analysis
        </button>
        <button 
          className={`view-btn ${activeView === 'insights' ? 'active' : ''}`}
          onClick={() => setActiveView('insights')}
        >
          <svg className="btn-icon" width="20" height="20" viewBox="0 0 20 20" fill="none">
            <path d="M10 2C7.79 2 6 3.79 6 6C6 7.89 7.29 9.48 9 9.87V14C9 14.55 9.45 15 10 15C10.55 15 11 14.55 11 14V9.87C12.71 9.48 14 7.89 14 6C14 3.79 12.21 2 10 2Z" fill="currentColor"/>
            <path d="M9 17H11V18H9V17Z" fill="currentColor"/>
          </svg>
          Key Insights
        </button>
        <button 
          className={`view-btn ${activeView === 'recommendations' ? 'active' : ''}`}
          onClick={() => setActiveView('recommendations')}
        >
          <svg className="btn-icon" width="20" height="20" viewBox="0 0 20 20" fill="none">
            <path d="M4 16L2 18V7L4 9L7 6L10 9L13 6L16 9L19 6V17L16 14L13 17L10 14L7 17L4 14" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
            <path d="M2 7L7 2M13 2L18 7" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
          </svg>
          Action Plan
        </button>
        <button 
          className={`view-btn ${activeView === 'strategic' ? 'active' : ''}`}
          onClick={() => setActiveView('strategic')}
        >
          <svg className="btn-icon" width="20" height="20" viewBox="0 0 20 20" fill="none">
            <path d="M10 2L12 7H18L13 10L15 15L10 12L5 15L7 10L2 7H8L10 2Z" fill="currentColor"/>
          </svg>
          Strategic Intel
        </button>
      </motion.div>

      {/* Content Area */}
      <AnimatePresence mode="wait">
        {activeView === 'overview' && (
          <motion.div
            key="overview"
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: -20 }}
            className="view-content"
          >
            {/* Stage-Specific Weights - Matching ScoreCard Design */}
            <motion.div 
              className="stage-weights-card"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, ease: [0.16, 1, 0.3, 1] }}
            >
              <div className="stage-weights-header">
                <h2>What Matters Most at {formatStageName(data.funding_stage)} Stage</h2>
                <p className="section-desc">Our AI adjusts its analysis based on your stage. Here's what we prioritized:</p>
              </div>
              
              {/* Educational Panel with ScoreCard styling */}
              <motion.div 
                className="education-panel-v2"
                initial={{ opacity: 0, scale: 0.95 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ delay: 0.2, duration: 0.6 }}
              >
                <div className="panel-header-v2">
                  <span className="panel-icon">
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
                      <path d="M12 3C9.24 3 7 5.24 7 8C7 10.22 8.39 12.11 10.31 12.78C10.73 12.92 11 13.33 11 13.78V18C11 18.55 11.45 19 12 19C12.55 19 13 18.55 13 18V13.78C13 13.33 13.27 12.92 13.69 12.78C15.61 12.11 17 10.22 17 8C17 5.24 14.76 3 12 3Z" fill="currentColor"/>
                      <path d="M11 20H13V21H11V20Z" fill="currentColor"/>
                    </svg>
                  </span>
                  <h4>Why This Matters</h4>
                </div>
                <div className="panel-content-v2">
                  <p>At the {formatStageName(data.funding_stage)} stage, investors typically look for:</p>
                  <ul className="key-expectations-v2">
                    {getStageExpectations(data.funding_stage).map((expectation, idx) => (
                      <motion.li 
                        key={idx}
                        initial={{ opacity: 0, x: -20 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ delay: 0.3 + idx * 0.1 }}
                      >
                        <span className="check-icon">✓</span>
                        {expectation}
                      </motion.li>
                    ))}
                  </ul>
                </div>
              </motion.div>
              
              <div className="stage-weights-grid-v2">
                {getStageWeights().map((weight, idx) => (
                  <motion.div 
                    key={idx}
                    className="stage-weight-item"
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.4 + idx * 0.1, duration: 0.6, ease: [0.16, 1, 0.3, 1] }}
                  >
                    <div className="weight-circle-container">
                      <motion.div 
                        className="weight-circle-background"
                        initial={{ scale: 0.8, opacity: 0 }}
                        animate={{ scale: 1, opacity: 1 }}
                        transition={{ delay: 0.5 + idx * 0.1, duration: 0.8 }}
                      />
                      <motion.div 
                        className="weight-circle"
                        style={{
                          background: `conic-gradient(
                            from -135deg,
                            ${getSuccessColor(weight.weight / 100)} 0deg,
                            ${getSuccessColor(weight.weight / 100)} ${(weight.weight / 100) * 270 - 135 + 135}deg,
                            var(--color-background-tertiary) ${(weight.weight / 100) * 270 - 135 + 135}deg
                          )`
                        }}
                        initial={{ rotate: -90 }}
                        animate={{ rotate: 0 }}
                        transition={{ delay: 0.6 + idx * 0.1, duration: 1.2, ease: [0.34, 1.56, 0.64, 1] }}
                      >
                        <div className="weight-circle-inner">
                          <motion.div 
                            className="weight-value"
                            initial={{ scale: 0 }}
                            animate={{ scale: 1 }}
                            transition={{ delay: 0.8 + idx * 0.1, duration: 0.6, ease: [0.34, 1.56, 0.64, 1] }}
                          >
                            <span className="weight-number">{weight.weight}</span>
                            <span className="weight-percent">%</span>
                          </motion.div>
                        </div>
                      </motion.div>
                    </div>
                    <div className="weight-details">
                      <h4 className="weight-area">{weight.area}</h4>
                      <p className="weight-description">{weight.description}</p>
                    </div>
                  </motion.div>
                ))}
              </div>
            </motion.div>

            {/* Performance Summary */}
            <PerformanceSummaryV17 data={data} />

            {/* Detected Patterns */}
            {data.patterns && data.patterns.length > 0 && (
              <div className="patterns-section">
                <h2>Startup DNA Patterns Detected</h2>
                <p className="section-desc">We identified these characteristics in your startup:</p>
                <div className="patterns-grid">
                  {data.patterns.map((pattern: string, idx: number) => (
                    <motion.div 
                      key={pattern}
                      className="pattern-card"
                      initial={{ opacity: 0, scale: 0.9 }}
                      animate={{ opacity: 1, scale: 1 }}
                      transition={{ delay: 0.1 * idx }}
                    >
                      <span className="pattern-icon">{getPatternIcon(pattern)}</span>
                      <h4>{formatPatternName(pattern)}</h4>
                      <p>{getPatternDescription(pattern)}</p>
                    </motion.div>
                  ))}
                </div>
              </div>
            )}

            {/* Industry Benchmarks */}
            <IndustryBenchmarksV17 
              sector={data.sector || data.industry || 'Fintech'}
              stage={data.funding_stage || 'Series A'}
              benchmarks={getIndustryBenchmarks(data).map(benchmark => ({
                metric: benchmark.metric,
                value: benchmark.yourValue || 0,
                unit: benchmark.unit,
                percentile: benchmark.yourPercentile,
                p25: extractBenchmarkValue(benchmark.p25),
                p50: extractBenchmarkValue(benchmark.p50),
                p75: extractBenchmarkValue(benchmark.p75),
                description: benchmark.description
              }))}
            />
          </motion.div>
        )}

        {activeView === 'camp' && (
          <motion.div
            key="camp"
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: -20 }}
            className="view-content"
          >
            <motion.div 
              className="camp-detailed-v2"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, ease: [0.16, 1, 0.3, 1] }}
            >
              <div className="camp-header">
                <h2>CAMP Framework Deep Dive</h2>
                <p className="section-desc">
                  The CAMP framework evaluates four critical dimensions of startup success. 
                  Click on each pillar to understand your score.
                </p>
              </div>

              <div className="camp-pillars-grid">
                {['capital', 'advantage', 'market', 'people'].map((pillar) => {
                  const score = data.camp_scores?.[pillar] || data.pillar_scores?.[pillar] || 0.5;
                  const explanation = getCampExplanation(pillar);
                  const isExpanded = expandedCAMP === pillar;

                  return (
                    <motion.div 
                      key={pillar}
                      className={`camp-pillar-card ${isExpanded ? 'expanded' : ''}`}
                      initial={{ opacity: 0, y: 20 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ delay: 0.1 * ['capital', 'advantage', 'market', 'people'].indexOf(pillar), duration: 0.6, ease: [0.16, 1, 0.3, 1] }}
                      onClick={() => setExpandedCAMP(isExpanded ? null : pillar)}
                    >
                      {/* Score Ring Section */}
                      <div className="pillar-score-section">
                        <div className="score-ring-container">
                          <motion.div 
                            className="score-ring-background"
                            initial={{ scale: 0.8, opacity: 0 }}
                            animate={{ scale: 1, opacity: 1 }}
                            transition={{ delay: 0.2 + 0.1 * ['capital', 'advantage', 'market', 'people'].indexOf(pillar), duration: 0.8 }}
                          />
                          <motion.div 
                            className="score-ring"
                            style={{
                              background: `conic-gradient(
                                from -135deg,
                                ${getSuccessColor(score)} 0deg,
                                ${getSuccessColor(score)} ${(score * 270) - 135 + 135}deg,
                                var(--color-background-tertiary) ${(score * 270) - 135 + 135}deg
                              )`
                            }}
                            initial={{ rotate: -90 }}
                            animate={{ rotate: 0 }}
                            transition={{ delay: 0.3 + 0.1 * ['capital', 'advantage', 'market', 'people'].indexOf(pillar), duration: 1.2, ease: [0.34, 1.56, 0.64, 1] }}
                          >
                            <div className="score-ring-inner">
                              <motion.div 
                                className="score-value"
                                initial={{ scale: 0 }}
                                animate={{ scale: 1 }}
                                transition={{ delay: 0.5 + 0.1 * ['capital', 'advantage', 'market', 'people'].indexOf(pillar), duration: 0.6, ease: [0.34, 1.56, 0.64, 1] }}
                              >
                                <span className="score-number">{Math.round(score * 100)}</span>
                                <span className="score-percent">%</span>
                              </motion.div>
                            </div>
                          </motion.div>
                        </div>
                        
                        <div className="pillar-info">
                          <div className="pillar-header">
                            <span className="pillar-icon">
                              {pillar === 'capital' ? (
                                <svg width="32" height="32" viewBox="0 0 32 32" fill="none">
                                  <path d="M16 2C8.268 2 2 8.268 2 16s6.268 14 14 14 14-6.268 14-14S23.732 2 16 2zm1.5 21.5v2a.5.5 0 01-.5.5h-2a.5.5 0 01-.5-.5v-2a5 5 0 01-3.5-4.5.5.5 0 01.5-.5h1.79a.5.5 0 01.5.43A2.5 2.5 0 0016 21.5h2a1.5 1.5 0 000-3h-4a3.5 3.5 0 010-7V9.5a.5.5 0 01.5-.5h2a.5.5 0 01.5.5v2a5 5 0 013.5 4.5.5.5 0 01-.5.5h-1.79a.5.5 0 01-.5-.43A2.5 2.5 0 0016 13.5h-2a1.5 1.5 0 000 3h4a3.5 3.5 0 010 7z" fill="currentColor"/>
                                </svg>
                              ) : pillar === 'advantage' ? (
                                <svg width="32" height="32" viewBox="0 0 32 32" fill="none">
                                  <path d="M11 2L7 12h6l-2 18 14-18h-8l4-10z" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                                </svg>
                              ) : pillar === 'market' ? (
                                <svg width="32" height="32" viewBox="0 0 32 32" fill="none">
                                  <path d="M4 26L12 18L18 24L28 14M28 14H22M28 14V20" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                                </svg>
                              ) : (
                                <svg width="32" height="32" viewBox="0 0 32 32" fill="none">
                                  <circle cx="16" cy="8" r="4" stroke="currentColor" strokeWidth="2"/>
                                  <path d="M6 26c0-5.523 4.477-10 10-10s10 4.477 10 10" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
                                </svg>
                              )}
                            </span>
                            <h3>{explanation.title}</h3>
                          </div>
                          <p className="pillar-description">{explanation.description}</p>
                          <div className="pillar-status">
                            <span className="status-badge" data-status={score >= 0.7 ? 'excellent' : score >= 0.5 ? 'good' : score >= 0.3 ? 'warning' : 'critical'}>
                              {score >= 0.7 ? 'EXCELLENT' : 
                               score >= 0.5 ? 'GOOD' : 
                               score >= 0.3 ? 'NEEDS IMPROVEMENT' : 'CRITICAL'}
                            </span>
                          </div>
                        </div>
                      </div>
                      
                      <button className="expand-button" onClick={(e) => { e.stopPropagation(); setExpandedCAMP(isExpanded ? null : pillar); }}>
                        <span>{isExpanded ? 'Less Details' : 'More Details'}</span>
                        <svg width="16" height="16" viewBox="0 0 16 16" className={`expand-arrow ${isExpanded ? 'expanded' : ''}`}>
                          <path d="M4 6l4 4 4-4" stroke="currentColor" strokeWidth="2" fill="none" />
                        </svg>
                      </button>

                      {isExpanded && (
                        <motion.div 
                          className="pillar-details"
                          initial={{ opacity: 0, height: 0 }}
                          animate={{ opacity: 1, height: 'auto' }}
                          exit={{ opacity: 0, height: 0 }}
                        >
                          <h4>Key Factors Analyzed:</h4>
                          <ul className="factors-list">
                            {explanation.factors.map((factor, idx) => (
                              <li key={idx}>{factor}</li>
                            ))}
                          </ul>
                          
                          <div className="pillar-metrics">
                            <h4>Your Metrics:</h4>
                            {getPillarMetrics(pillar, data).map((metric, idx) => (
                              <div key={idx} className="metric-display">
                                <span className="metric-label">{metric.label}:</span>
                                <span className="metric-value">{metric.value}</span>
                                <span className={`metric-status ${metric.status}`}>
                                  {metric.status === 'good' ? '✓' : metric.status === 'warning' ? '!' : '✗'}
                                </span>
                              </div>
                            ))}
                          </div>

                          {/* What-If Analysis */}
                          <div className="camp-pillar-interactive">
                            <h4>What-If Analysis</h4>
                            <p>
                              {llmAvailable ? (
                                <>
                                  <span className="ai-indicator">
                                    <svg width="16" height="16" viewBox="0 0 16 16" fill="none" style={{display: 'inline-block', verticalAlign: 'middle', marginRight: '4px'}}>
                                      <path d="M8 2C5.79 2 4 3.79 4 6v4c0 2.21 1.79 4 4 4s4-1.79 4-4V6c0-2.21-1.79-4-4-4z" fill="currentColor"/>
                                      <circle cx="6" cy="6" r="1" fill="white"/>
                                      <circle cx="10" cy="6" r="1" fill="white"/>
                                      <path d="M6 10h4" stroke="white" strokeWidth="1" strokeLinecap="round"/>
                                    </svg>
                                  </span>AI-powered predictions based on real startup data
                                </>
                              ) : (
                                'See how improvements would affect your score:'
                              )}
                            </p>
                            
                            <div className="improvement-simulator">
                              {getImprovementOptions(pillar).map((option) => (
                                <div key={option.id} className="improvement-option">
                                  <label>
                                    <input 
                                      type="checkbox" 
                                      checked={simulatedImprovements[pillar].has(option.id)}
                                      onChange={(e) => {
                                        const newSimulated = { ...simulatedImprovements };
                                        if (e.target.checked) {
                                          newSimulated[pillar].add(option.id);
                                        } else {
                                          newSimulated[pillar].delete(option.id);
                                        }
                                        setSimulatedImprovements(newSimulated);
                                      }}
                                    />
                                    <span className="option-text">{option.description}</span>
                                    <span className="impact-preview">+{option.impact}%</span>
                                  </label>
                                </div>
                              ))}
                            </div>
                            
                            <div className="simulated-score">
                              <span>Potential Score:</span>
                              <motion.span 
                                className="score-value"
                                animate={{ 
                                  color: calculateSimulatedScore(pillar, score, simulatedImprovements[pillar]) > score ? '#00c851' : '#ffffff' 
                                }}
                              >
                                {formatPercentage(calculateSimulatedScore(pillar, score, simulatedImprovements[pillar]))}
                              </motion.span>
                            </div>
                            
                            {llmAvailable && simulatedImprovements[pillar].size > 0 && (
                              <button 
                                className="analyze-with-ai-btn"
                                onClick={async () => {
                                  const improvements = Array.from(simulatedImprovements[pillar]).map(id => {
                                    const option = getImprovementOptions(pillar).find(opt => opt.id === id);
                                    return { id, description: option?.description || id };
                                  });
                                  await calculateDynamicWhatIf(improvements);
                                }}
                                disabled={isLoadingWhatIf}
                              >
                                {isLoadingWhatIf ? 'Analyzing...' : 'Get AI Analysis'}
                              </button>
                            )}
                            
                            {dynamicWhatIfResult && (
                              <div className="ai-whatif-results">
                                <div className="ai-prediction">
                                  <strong>AI Prediction:</strong> {(dynamicWhatIfResult.new_probability.value * 100).toFixed(0)}% 
                                  <span className="confidence-interval">
                                    ({(dynamicWhatIfResult.new_probability.lower * 100).toFixed(0)}-{(dynamicWhatIfResult.new_probability.upper * 100).toFixed(0)}%)
                                  </span>
                                </div>
                                <div className="timeline">Timeline: {dynamicWhatIfResult.timeline}</div>
                              </div>
                            )}
                          </div>

                          <div className="improvement-tips">
                            <h4>How to Improve:</h4>
                            {getImprovementTips(pillar, score, config).map((tip, idx) => (
                              <p key={idx} className="tip">• {tip}</p>
                            ))}
                          </div>
                        </motion.div>
                      )}
                    </motion.div>
                  );
                })}
              </div>
            </motion.div>

            {/* CAMP Score Comparison - Updated Design */}
            <motion.div 
              className="camp-comparison-v2"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.5, duration: 0.6 }}
            >
                <h3>Your CAMP Profile vs. Successful Startups</h3>
                <div className="comparison-chart-v2">
                  <div className="comparison-header">
                    <span>Pillar</span>
                    <span>Your Score</span>
                    <span>Target for {formatStageName(data.funding_stage)}</span>
                    <span>Gap</span>
                  </div>
                  {['capital', 'advantage', 'market', 'people'].map((pillar) => {
                    const score = data.camp_scores?.[pillar] || data.pillar_scores?.[pillar] || 0.5;
                    const target = getTargetScore(pillar, data.funding_stage);
                    const gap = score - target;
                    
                    return (
                      <div key={pillar} className="comparison-row">
                        <span className="pillar-name">{getCampExplanation(pillar).title}</span>
                        <span className="your-score" style={{ color: getSuccessColor(score) }}>
                          {formatPercentage(score)}
                        </span>
                        <span className="target-score">{formatPercentage(target)}</span>
                        <span className={`gap ${gap >= 0 ? 'positive' : 'negative'}`}>
                          {gap >= 0 ? '+' : ''}{formatPercentage(Math.abs(gap))}
                        </span>
                      </div>
                    );
                  })}
                </div>
              </motion.div>
          </motion.div>
        )}

        {activeView === 'insights' && (
          <motion.div
            key="insights"
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: -20 }}
            className="view-content"
          >
            <div className="insights-section">
              <h2>Key Insights from Your Analysis</h2>
              
              {/* Strengths */}
              <div className="insight-category strengths">
                <h3>
                  <span className="category-icon">
                    <svg width="28" height="28" viewBox="0 0 28 28" fill="none">
                      <path d="M21 10C21 10 19.5 8.5 16 8.5C13.5 8.5 12 10 12 10M12 10V5C12 3.34 10.66 2 9 2C7.34 2 6 3.34 6 5V17L3.5 14.5C2.67 13.67 1.33 13.67 0.5 14.5C-0.17 15.17 -0.17 16.33 0.5 17L6 22.5C7.5 24 9.5 25 12 25H17C20.31 25 23 22.31 23 19V14C23 11.79 21.21 10 19 10H21Z" fill="currentColor"/>
                    </svg>
                  </span>
                  Your Strengths
                </h3>
                <div className="insights-list">
                  {getStrengths(data, config, burnThresholds, teamThresholds, experienceThresholds).map((strength, idx) => (
                    <motion.div 
                      key={idx}
                      className="insight-item positive"
                      initial={{ opacity: 0, x: -20 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ delay: 0.1 * idx }}
                    >
                      <span className="insight-bullet">
                        <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                          <circle cx="10" cy="10" r="9" fill="#00c851"/>
                          <path d="M6 10L9 13L14 8" stroke="white" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                        </svg>
                      </span>
                      <div className="insight-content">
                        <h4>{strength.title}</h4>
                        <p>{strength.description}</p>
                      </div>
                    </motion.div>
                  ))}
                </div>
              </div>

              {/* Areas for Improvement */}
              <div className="insight-category improvements">
                <h3>
                  <span className="category-icon">
                    <svg width="28" height="28" viewBox="0 0 28 28" fill="none">
                      <circle cx="14" cy="14" r="10" stroke="currentColor" strokeWidth="2" fill="none"/>
                      <circle cx="14" cy="14" r="4" fill="currentColor"/>
                      <path d="M14 2V6M14 22V26M2 14H6M22 14H26" stroke="currentColor" strokeWidth="2"/>
                    </svg>
                  </span>
                  Areas for Improvement
                </h3>
                <div className="insights-list">
                  {getImprovements(data, config, burnThresholds).map((improvement, idx) => (
                    <motion.div 
                      key={idx}
                      className="insight-item warning"
                      initial={{ opacity: 0, x: -20 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ delay: 0.1 * idx }}
                    >
                      <span className="insight-bullet">
                        <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                          <circle cx="10" cy="10" r="9" fill="#ff8800"/>
                          <path d="M10 6V11M10 14H10.01" stroke="white" strokeWidth="2" strokeLinecap="round"/>
                        </svg>
                      </span>
                      <div className="insight-content">
                        <h4>{improvement.title}</h4>
                        <p>{improvement.description}</p>
                        <span className="impact-label">Impact: {improvement.impact}</span>
                      </div>
                    </motion.div>
                  ))}
                </div>
              </div>

              {/* Critical Risks */}
              <div className="insight-category risks">
                <h3>
                  <span className="category-icon">
                    <svg width="28" height="28" viewBox="0 0 28 28" fill="none">
                      <path d="M12 3L2 21h20L12 3z" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" fill="none"/>
                      <path d="M12 9v6M12 18h.01" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
                    </svg>
                  </span>
                  Critical Risks to Address
                </h3>
                <div className="insights-list">
                  {getRisks(data, config).map((risk, idx) => (
                    <motion.div 
                      key={idx}
                      className="insight-item negative"
                      initial={{ opacity: 0, x: -20 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ delay: 0.1 * idx }}
                    >
                      <span className="insight-bullet">
                        <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                          <circle cx="10" cy="10" r="9" fill="#ff4444"/>
                          <path d="M7 7L13 13M13 7L7 13" stroke="white" strokeWidth="2" strokeLinecap="round"/>
                        </svg>
                      </span>
                      <div className="insight-content">
                        <h4>{risk.title}</h4>
                        <p>{risk.description}</p>
                        <div className="mitigation-box">
                          <strong>Mitigation:</strong> {risk.mitigation}
                        </div>
                      </div>
                    </motion.div>
                  ))}
                </div>
              </div>

              {/* Market Timing */}
              <div className="market-timing">
                <h3>Market Timing Assessment</h3>
                <div className="timing-indicator">
                  <div className="timing-scale">
                    <span className="early">Too Early</span>
                    <span className="optimal">Optimal</span>
                    <span className="late">Too Late</span>
                  </div>
                  <div className="timing-pointer" style={{ left: `${getMarketTiming(data)}%` }}>
                    <svg className="pointer-icon" width="24" height="24" viewBox="0 0 24 24" fill="none">
                      <path d="M12 2L7 10H17L12 2Z" fill="currentColor"/>
                    </svg>
                  </div>
                </div>
                <p className="timing-explanation">
                  {getMarketTiming(data) < 30 ? 'Market may not be ready for your solution yet. Focus on education and early adopters.' :
                   getMarketTiming(data) > 70 ? 'Market is mature with established players. Focus on differentiation and niche segments.' :
                   'Good market timing! The market is ready for innovation and new solutions.'}
                </p>
              </div>
            </div>
          </motion.div>
        )}

        {activeView === 'recommendations' && (
          <motion.div
            key="recommendations"
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: -20 }}
            className="view-content"
          >
            <div className="recommendations-section">
              <h2>Your Personalized Action Plan</h2>
              <p className="section-desc">
                Based on your analysis, here are specific actions to improve your success probability. 
                We've prioritized them by impact and urgency.
              </p>

              {/* Success Probability Impact */}
              <div className="probability-impact">
                <h3>Potential Success Score Improvement</h3>
                <div className="impact-visualization">
                  <div className="current-score">
                    <span className="label">Current</span>
                    <span className="score">{formatPercentage(successProbability)}</span>
                  </div>
                  <div className="arrow">→</div>
                  <div className="potential-score">
                    <span className="label">Potential</span>
                    <span className="score">{formatPercentage(Math.min(successProbability + 0.15, 0.85))}</span>
                  </div>
                </div>
                <p className="impact-note">
                  By implementing these recommendations, you could improve your success score by up to 15 percentage points.
                </p>
              </div>

              {/* AI-Powered Badge */}
              {showAIBadge && (
                <div className="ai-badge-container">
                  <span className="ai-badge">
                    <span className="ai-icon">
                      <svg width="18" height="18" viewBox="0 0 18 18" fill="none">
                        <path d="M9 2L7.17 7.17L2 9l5.17 1.83L9 16l1.83-5.17L16 9l-5.17-1.83L9 2z" fill="currentColor"/>
                        <path d="M4.5 4.5L3.5 6.5L1.5 7.5L3.5 8.5L4.5 10.5L5.5 8.5L7.5 7.5L5.5 6.5L4.5 4.5z" fill="currentColor" opacity="0.7"/>
                        <path d="M13.5 13.5L12.5 15.5L10.5 16.5L12.5 17.5L13.5 19.5L14.5 17.5L16.5 16.5L14.5 15.5L13.5 13.5z" fill="currentColor" opacity="0.7"/>
                      </svg>
                    </span>
                    AI-Powered Recommendations
                  </span>
                </div>
              )}
              
              {/* Prioritized Recommendations */}
              <div className="recommendations-list">
                {isLoadingLLM ? (
                  <div className="llm-loading">
                    <div className="loading-spinner" />
                    <p>Generating personalized recommendations...</p>
                  </div>
                ) : (
                  getRecommendations(data, llmRecommendations).map((rec, idx) => (
                  <motion.div 
                    key={idx}
                    className={`recommendation-card priority-${rec.priority.toLowerCase()}`}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.1 * idx }}
                  >
                    <div className="rec-header">
                      <div className="rec-number">{idx + 1}</div>
                      <div className="rec-title-section">
                        <h3>{rec.title}</h3>
                        <div className="rec-tags">
                          <span className="priority-tag">{rec.priority}</span>
                          <span className="timeline-tag">{rec.timeline}</span>
                          <span className="impact-tag">+{rec.impact}%</span>
                        </div>
                      </div>
                    </div>

                    <p className="rec-description">{rec.description}</p>

                    <div className="rec-details">
                      <div className="action-steps">
                        <h4>Specific Actions:</h4>
                        <ol>
                          {rec.actions.map((action: string, actionIdx: number) => (
                            <li key={actionIdx}>{action}</li>
                          ))}
                        </ol>
                      </div>

                      <div className="success-metrics">
                        <h4>Success Metrics:</h4>
                        <ul>
                          {rec.metrics.map((metric: string, metricIdx: number) => (
                            <li key={metricIdx}>{metric}</li>
                          ))}
                        </ul>
                      </div>
                    </div>

                    <div className="rec-footer">
                      <div className="affected-scores">
                        <span className="label">Improves:</span>
                        {rec.affects.map((pillar: string, pillarIdx: number) => (
                          <span key={pillarIdx} className="affected-pillar">
                            {pillar === 'capital' ? (
                              <svg width="16" height="16" viewBox="0 0 16 16" fill="none" style={{display: 'inline-block', verticalAlign: 'middle', marginRight: '4px'}}>
                                <circle cx="8" cy="8" r="6" stroke="currentColor" strokeWidth="1.5" fill="none"/>
                                <path d="M8 5v6M6 7h4M6 9h4" stroke="currentColor" strokeWidth="1.5"/>
                              </svg>
                            ) : pillar === 'advantage' ? (
                              <svg width="16" height="16" viewBox="0 0 16 16" fill="none" style={{display: 'inline-block', verticalAlign: 'middle', marginRight: '4px'}}>
                                <path d="M6 2L4 8h3L6 14l6-8h-3l2-4z" fill="currentColor"/>
                              </svg>
                            ) : pillar === 'market' ? (
                              <svg width="16" height="16" viewBox="0 0 16 16" fill="none" style={{display: 'inline-block', verticalAlign: 'middle', marginRight: '4px'}}>
                                <path d="M2 12L6 8l3 3 5-5M11 4h3v3" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
                              </svg>
                            ) : (
                              <svg width="16" height="16" viewBox="0 0 16 16" fill="none" style={{display: 'inline-block', verticalAlign: 'middle', marginRight: '4px'}}>
                                <circle cx="8" cy="5" r="2" stroke="currentColor" strokeWidth="1.5"/>
                                <path d="M3 13c0-2.76 2.24-5 5-5s5 2.24 5 5" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round"/>
                              </svg>
                            )}
                            {getCampExplanation(pillar).title}
                          </span>
                        ))}
                      </div>
                      <div className="action-buttons">
                        <button 
                          className={`mark-complete-btn ${completedActions.has(idx) ? 'completed' : ''}`}
                          onClick={() => {
                            const newCompleted = new Set(completedActions);
                            if (completedActions.has(idx)) {
                              newCompleted.delete(idx);
                            } else {
                              newCompleted.add(idx);
                            }
                            setCompletedActions(newCompleted);
                          }}
                        >
                          <span className="icon">
                            {completedActions.has(idx) ? (
                              <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                                <rect x="2" y="2" width="12" height="12" rx="2" fill="currentColor"/>
                                <path d="M5 8L7 10L11 6" stroke="white" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                              </svg>
                            ) : (
                              <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                                <rect x="2" y="2" width="12" height="12" rx="2" stroke="currentColor" strokeWidth="2" fill="none"/>
                              </svg>
                            )}
                          </span>
                          {completedActions.has(idx) ? 'Completed' : 'Mark as Complete'}
                        </button>
                      </div>
                    </div>
                  </motion.div>
                )))}
              </div>

              {/* Progress Tracker */}
              <div className="progress-tracker">
                <h3>Track Your Improvements</h3>
                
                <div className="progress-overview">
                  <div className="actions-completed">
                    <span className="number">{completedActions.size}</span>
                    <span className="label">Actions Completed</span>
                  </div>
                  <div className="score-improvement">
                    <span className="number">+{Math.floor(completedActions.size * 2)}%</span>
                    <span className="label">Score Improvement</span>
                  </div>
                  <div className="next-milestone">
                    <span className="number">{Math.max(0, 3 - completedActions.size)}</span>
                    <span className="label">Actions to Next Level</span>
                  </div>
                </div>
                
                <button className="schedule-followup">
                  <span className="icon">
                    <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                      <rect x="2" y="3" width="12" height="11" rx="2" stroke="currentColor" strokeWidth="2"/>
                      <path d="M5 1V5M11 1V5" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
                      <path d="M2 6H14" stroke="currentColor" strokeWidth="2"/>
                      <rect x="5" y="8" width="2" height="2" fill="currentColor"/>
                      <rect x="9" y="8" width="2" height="2" fill="currentColor"/>
                      <rect x="5" y="11" width="2" height="2" fill="currentColor"/>
                    </svg>
                  </span>
                  Schedule 30-Day Re-Assessment
                </button>
              </div>

              {/* Next Steps */}
              <div className="next-steps">
                <h3>Your Next 30 Days</h3>
                <div className="timeline">
                  <div className="timeline-item">
                    <div className="timeline-marker">Week 1</div>
                    <div className="timeline-content">
                      <h4>Quick Wins</h4>
                      <p>Focus on the highest priority items that can be implemented immediately.</p>
                    </div>
                  </div>
                  <div className="timeline-item">
                    <div className="timeline-marker">Week 2-3</div>
                    <div className="timeline-content">
                      <h4>Build Momentum</h4>
                      <p>Start implementing medium-priority items and track early metrics.</p>
                    </div>
                  </div>
                  <div className="timeline-item">
                    <div className="timeline-marker">Week 4</div>
                    <div className="timeline-content">
                      <h4>Measure & Adjust</h4>
                      <p>Review progress, measure impact, and adjust your approach.</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </motion.div>
        )}

        {activeView === 'strategic' && (
          <motion.div
            key="strategic"
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: -20 }}
            className="view-content strategic-view"
          >
            <StrategicIntelligence analysisData={data} />
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};

// Helper functions
function formatModelName(model: string): string {
  const names: Record<string, string> = {
    'dna_analyzer': 'DNA Pattern Analysis',
    'temporal_predictor': 'Time-Based Factors',
    'industry_model': 'Industry Specific',
    'ensemble': 'Base Analysis',
    'stage_predictor': 'Stage Factors'
  };
  return names[model] || model.split('_').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ');
}

function getModelDescription(model: string): string {
  const descriptions: Record<string, string> = {
    'dna_analyzer': 'Identifies patterns from successful startups in similar domains',
    'temporal_predictor': 'Analyzes time-based trends and market timing factors',
    'temporal_model': 'Evaluates growth trajectory and timing indicators',
    'industry_model': 'Sector-specific insights and competitive positioning',
    'ensemble': 'Combines multiple models for balanced assessment',
    'ensemble_model': 'Unified analysis from all model perspectives',
    'stage_predictor': 'Stage-appropriate metrics and expectations',
    'dna': 'Pattern recognition from successful startup DNA',
    'temporal': 'Time-series analysis of growth and momentum',
    'industry': 'Industry benchmarks and competitive landscape',
    'stage': 'Stage-specific success factors and milestones'
  };
  return descriptions[model] || 'Advanced ML analysis of startup metrics';
}

function formatBenchmarkValue(metric: string, value: number): string {
  if (metric.toLowerCase().includes('growth') || metric.toLowerCase().includes('percent')) {
    return `${Math.round(value)}%`;
  }
  if (metric.toLowerCase().includes('multiple') || metric.toLowerCase().includes('ratio')) {
    return `${value.toFixed(1)}x`;
  }
  if (metric.toLowerCase().includes('size') || metric.toLowerCase().includes('employees')) {
    return Math.round(value).toString();
  }
  if (metric.toLowerCase().includes('months')) {
    return `${Math.round(value)} months`;
  }
  return value.toFixed(1);
}

function getStageExpectations(stage: string): string[] {
  const expectations: Record<string, string[]> = {
    'Pre-seed': [
      'Strong founder-market fit and domain expertise',
      'Clear problem identification with customer validation',
      'Initial product concept or MVP in development',
      'Small but dedicated founding team'
    ],
    'Seed': [
      'Working product with early customer adoption',
      'Initial revenue or strong user engagement metrics',
      'Product-market fit signals and customer feedback loops',
      'Core team in place with key technical roles filled'
    ],
    'Series A': [
      'Consistent revenue growth (>100% YoY typical)',
      'Proven unit economics and scalable go-to-market',
      'Expanding team with department heads',
      'Clear path to profitability within 24-36 months'
    ],
    'Series B': [
      'Market leadership position or clear path to it',
      'Efficient growth metrics (LTV/CAC > 3x)',
      'Mature operations and processes',
      'International expansion or product line extension'
    ]
  };
  return expectations[stage] || expectations['Series A'];
}

function getPatternIcon(pattern: string): React.ReactElement {
  const icons: Record<string, React.ReactElement> = {
    'efficient_growth': (
      <svg width="40" height="40" viewBox="0 0 40 40" fill="none">
        <path d="M10 30L8 35V15L10 20L15 15L20 20L25 15L30 20L35 15V30L30 25L25 30L20 25L15 30L10 25" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
        <path d="M8 15L18 5M22 5L32 15" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
      </svg>
    ),
    'market_leader': (
      <svg width="40" height="40" viewBox="0 0 40 40" fill="none">
        <path d="M20 5L25 15H35L27.5 21L30 31L20 25L10 31L12.5 21L5 15H15L20 5Z" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
        <circle cx="20" cy="15" r="3" fill="currentColor"/>
      </svg>
    ),
    'vc_hypergrowth': (
      <svg width="40" height="40" viewBox="0 0 40 40" fill="none">
        <circle cx="20" cy="20" r="15" stroke="currentColor" strokeWidth="2" fill="none"/>
        <path d="M20 10v20M15 15h10M15 25h10" stroke="currentColor" strokeWidth="2"/>
        <path d="M10 20C10 14.5 14.5 10 20 10M30 20C30 25.5 25.5 30 20 30" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
      </svg>
    ),
    'capital_efficient': (
      <svg width="40" height="40" viewBox="0 0 40 40" fill="none">
        <path d="M20 5L10 15V25L20 35L30 25V15L20 5Z" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
        <path d="M20 15V25M15 20H25" stroke="currentColor" strokeWidth="2"/>
      </svg>
    ),
    'b2b_saas': (
      <svg width="40" height="40" viewBox="0 0 40 40" fill="none">
        <path d="M10 25C10 15 15 10 20 10C25 10 30 15 30 25M10 25C10 28 12 30 15 30H25C28 30 30 28 30 25M10 25V30H30V25" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
        <circle cx="15" cy="20" r="2" fill="currentColor"/>
        <circle cx="25" cy="20" r="2" fill="currentColor"/>
      </svg>
    ),
    'product_led': (
      <svg width="40" height="40" viewBox="0 0 40 40" fill="none">
        <circle cx="20" cy="20" r="15" stroke="currentColor" strokeWidth="2" fill="none"/>
        <circle cx="20" cy="20" r="5" fill="currentColor"/>
        <path d="M20 5V10M20 30V35M5 20H10M30 20H35" stroke="currentColor" strokeWidth="2"/>
      </svg>
    ),
    'bootstrap_profitable': (
      <svg width="40" height="40" viewBox="0 0 40 40" fill="none">
        <path d="M20 35C20 35 10 30 10 20C10 15 15 10 20 10C25 10 30 15 30 20C30 30 20 35 20 35Z" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
        <path d="M20 15V25M15 20H25" stroke="currentColor" strokeWidth="2"/>
      </svg>
    ),
    'ai_ml_core': (
      <svg width="40" height="40" viewBox="0 0 40 40" fill="none">
        <rect x="10" y="10" width="20" height="20" rx="4" stroke="currentColor" strokeWidth="2"/>
        <circle cx="15" cy="15" r="2" fill="currentColor"/>
        <circle cx="25" cy="15" r="2" fill="currentColor"/>
        <path d="M15 25h10" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
        <path d="M5 15h5M30 15h5M20 5v5M20 30v5" stroke="currentColor" strokeWidth="2"/>
      </svg>
    ),
    'platform_network': (
      <svg width="40" height="40" viewBox="0 0 40 40" fill="none">
        <circle cx="20" cy="10" r="3" stroke="currentColor" strokeWidth="2"/>
        <circle cx="10" cy="25" r="3" stroke="currentColor" strokeWidth="2"/>
        <circle cx="30" cy="25" r="3" stroke="currentColor" strokeWidth="2"/>
        <circle cx="20" cy="30" r="3" stroke="currentColor" strokeWidth="2"/>
        <path d="M20 13V27M17 11L13 23M23 11L27 23" stroke="currentColor" strokeWidth="2"/>
      </svg>
    ),
    'deep_tech': (
      <svg width="40" height="40" viewBox="0 0 40 40" fill="none">
        <circle cx="20" cy="20" r="12" stroke="currentColor" strokeWidth="2" fill="none"/>
        <path d="M20 8C20 8 15 13 15 20C15 27 20 32 20 32M20 8C20 8 25 13 25 20C25 27 20 32 20 32" stroke="currentColor" strokeWidth="2"/>
        <path d="M8 20H32" stroke="currentColor" strokeWidth="2"/>
        <circle cx="20" cy="20" r="3" fill="currentColor"/>
      </svg>
    )
  };
  return icons[pattern] || (
    <svg width="40" height="40" viewBox="0 0 40 40" fill="none">
      <rect x="5" y="25" width="6" height="10" rx="1" fill="currentColor"/>
      <rect x="14" y="20" width="6" height="15" rx="1" fill="currentColor"/>
      <rect x="23" y="15" width="6" height="20" rx="1" fill="currentColor"/>
      <rect x="32" y="10" width="6" height="25" rx="1" fill="currentColor"/>
    </svg>
  );
}

function formatPatternName(pattern: string): string {
  return pattern.replace(/_/g, ' ').split(' ').map(word => 
    word.charAt(0).toUpperCase() + word.slice(1)
  ).join(' ');
}

function getPatternDescription(pattern: string): string {
  const descriptions: Record<string, string> = {
    'efficient_growth': 'Growing rapidly while maintaining low burn rate',
    'market_leader': 'Positioned to dominate your market segment',
    'vc_hypergrowth': 'Classic venture-backed growth trajectory',
    'capital_efficient': 'Achieving more with less capital',
    'b2b_saas': 'Strong B2B SaaS fundamentals',
    'product_led': 'Product drives organic growth',
    'bootstrap_profitable': 'Path to profitability without heavy funding',
    'ai_ml_core': 'AI/ML as core value proposition',
    'platform_network': 'Building network effects',
    'deep_tech': 'Advanced technology innovation'
  };
  return descriptions[pattern] || 'Unique pattern detected in your business model';
}

function getPillarMetrics(pillar: string, data: any): Array<{label: string, value: string, status: string}> {
  const metrics: Record<string, Array<{label: string, value: string, status: string}>> = {
    capital: [
      {
        label: 'Burn Multiple',
        value: `${(data.burn_multiple || 0).toFixed(1)}x`,
        status: data.burn_multiple < 1.5 ? 'good' : data.burn_multiple < 2.5 ? 'warning' : 'bad'
      },
      {
        label: 'Runway',
        value: `${Math.round(data.runway_months || 12)} months`,
        status: data.runway_months > 18 ? 'good' : data.runway_months > 12 ? 'warning' : 'bad'
      },
      {
        label: 'LTV/CAC',
        value: `${(data.ltv_cac_ratio || 3).toFixed(1)}:1`,
        status: data.ltv_cac_ratio > 3 ? 'good' : data.ltv_cac_ratio > 2 ? 'warning' : 'bad'
      }
    ],
    advantage: [
      {
        label: 'Tech Score',
        value: `${data.technology_score || 3}/5`,
        status: data.technology_score >= 4 ? 'good' : data.technology_score >= 3 ? 'warning' : 'bad'
      },
      {
        label: 'Has Patent',
        value: data.has_patent ? 'Yes' : 'No',
        status: data.has_patent ? 'good' : 'warning'
      },
      {
        label: 'Differentiation',
        value: data.scalability_score >= 4 ? 'Strong' : 'Moderate',
        status: data.scalability_score >= 4 ? 'good' : 'warning'
      }
    ],
    market: [
      {
        label: 'TAM',
        value: `$${Math.round((data.tam_size_usd || 10000000000) / 1000000000)}B`,
        status: data.tam_size_usd > 50000000000 ? 'good' : data.tam_size_usd > 10000000000 ? 'warning' : 'bad'
      },
      {
        label: 'Growth Rate',
        value: `${data.revenue_growth_rate_percent || 0}%`,
        status: data.revenue_growth_rate_percent > 150 ? 'good' : data.revenue_growth_rate_percent > 50 ? 'warning' : 'bad'
      },
      {
        label: 'Market Growth',
        value: `${data.market_growth_rate || 15}%`,
        status: data.market_growth_rate > 20 ? 'good' : data.market_growth_rate > 10 ? 'warning' : 'bad'
      }
    ],
    people: [
      {
        label: 'Team Size',
        value: `${data.team_size_full_time || 10}`,
        status: data.team_size_full_time > 20 ? 'good' : data.team_size_full_time > 10 ? 'warning' : 'bad'
      },
      {
        label: 'Experience',
        value: `${data.years_experience_avg || 5} years`,
        status: data.years_experience_avg > 10 ? 'good' : data.years_experience_avg > 5 ? 'warning' : 'bad'
      },
      {
        label: 'Advisor Quality',
        value: `${data.advisor_quality_score || 3}/5`,
        status: data.advisor_quality_score >= 4 ? 'good' : data.advisor_quality_score >= 3 ? 'warning' : 'bad'
      }
    ]
  };
  return metrics[pillar] || [];
}

function getImprovementTips(pillar: string, score: number, config?: any): string[] {
  if (score >= 0.7) {
    return ['Maintain current performance', 'Look for optimization opportunities', 'Share best practices with other areas'];
  }
  
  const tips = config?.messages?.recommendations?.[pillar as keyof typeof config.messages.recommendations] || 
    ['Focus on improving core metrics'];
  return Array.isArray(tips) ? tips : [tips];
}

function formatStageName(stage: string): string {
  if (!stage) return 'Seed';
  
  // Handle different formats
  const normalized = stage.toLowerCase().replace(/_/g, ' ');
  
  // Capitalize properly
  return normalized.split(' ').map(word => 
    word === 'a' || word === 'b' ? word.toUpperCase() : 
    word.charAt(0).toUpperCase() + word.slice(1)
  ).join(' ');
}

function getTargetScore(pillar: string, stage: string): number {
  const targets: Record<string, Record<string, number>> = {
    'pre_seed': { capital: 0.40, advantage: 0.45, market: 0.50, people: 0.45 },
    'seed': { capital: 0.55, advantage: 0.60, market: 0.70, people: 0.65 },
    'series_a': { capital: 0.70, advantage: 0.75, market: 0.75, people: 0.80 },
    'series_b': { capital: 0.80, advantage: 0.85, market: 0.85, people: 0.90 }
  };
  
  // Normalize stage name to match our keys
  const normalizedStage = stage?.toLowerCase().replace(/[\s-]+/g, '_') || 'seed';
  
  // Return stage-specific targets or default targets for seed stage
  return targets[normalizedStage]?.[pillar] || targets['seed']?.[pillar] || 0.6;
}

function getStrengths(data: any, config: any, burnThresholds: any, teamThresholds: any, experienceThresholds: any): Array<{title: string, description: string}> {
  // Use real strengths from API if available
  if (data.key_insights?.strengths && data.key_insights.strengths.length > 0) {
    return data.key_insights.strengths;
  }
  
  // Fallback to basic analysis
  const strengths = [];
  
  if (data.revenue_growth_rate_percent && config.thresholds.performance?.revenue?.growth?.high && 
      data.revenue_growth_rate_percent > config.thresholds.performance.revenue.growth.high * 100) {
    strengths.push({
      title: 'Exceptional Revenue Growth',
      description: `Your ${data.revenue_growth_rate_percent}% growth rate puts you in the top 10% of startups at your stage.`
    });
  }
  
  if (data.burn_multiple && burnThresholds.excellent && data.burn_multiple < burnThresholds.excellent) {
    strengths.push({
      title: 'Capital Efficient Operations',
      description: 'Your burn multiple shows excellent financial discipline and sustainable growth.'
    });
  }
  
  if (data.net_dollar_retention_percent && config.thresholds.metrics?.retention?.excellent &&
      data.net_dollar_retention_percent > config.thresholds.metrics.retention.excellent * 100) {
    strengths.push({
      title: 'Strong Product-Market Fit',
      description: 'High net revenue retention indicates customers love your product and are expanding usage.'
    });
  }
  
  if (data.team_size_full_time && teamThresholds.optimal && 
      data.years_experience_avg && experienceThresholds.senior &&
      data.team_size_full_time > teamThresholds.optimal && 
      data.years_experience_avg > experienceThresholds.senior) {
    strengths.push({
      title: 'Experienced Team',
      description: 'Your team has the experience and scale to execute on your vision.'
    });
  }
  
  return strengths.length > 0 ? strengths : [{
    title: 'Building Momentum',
    description: 'Continue focusing on core metrics to build your strengths.'
  }];
}

function getImprovements(data: any, config: any, burnThresholds: any): Array<{title: string, description: string, impact: string}> {
  // Use real improvements from API if available
  if (data.key_insights?.improvements && data.key_insights.improvements.length > 0) {
    return data.key_insights.improvements;
  }
  
  // Fallback to basic analysis
  const improvements = [];
  
  if (data.burn_multiple && burnThresholds.critical && data.burn_multiple > burnThresholds.critical) {
    improvements.push({
      title: 'Optimize Burn Rate',
      description: 'Your current burn multiple suggests inefficient capital usage.',
      impact: 'High'
    });
  }
  
  if (data.ltv_cac_ratio && config.thresholds.performance?.ltv_cac?.good &&
      data.ltv_cac_ratio < config.thresholds.performance.ltv_cac.good) {
    improvements.push({
      title: 'Improve Unit Economics',
      description: 'Focus on either increasing customer lifetime value or reducing acquisition costs.',
      impact: 'High'
    });
  }
  
  if (data.runway_months && config.thresholds.risk?.runway?.warning &&
      data.runway_months < config.thresholds.risk.runway.warning) {
    improvements.push({
      title: 'Extend Runway',
      description: 'Limited runway creates fundraising pressure and reduces negotiation leverage.',
      impact: 'Critical'
    });
  }
  
  return improvements;
}

function getRisks(data: any, config: any): Array<{title: string, description: string, mitigation: string}> {
  // Use real risks from API if available
  if (data.key_insights?.risks && data.key_insights.risks.length > 0) {
    return data.key_insights.risks;
  }
  
  // Fallback to basic analysis
  const risks = [];
  
  // Add basic risk if no API risks available
  if (risks.length === 0 && !data.key_insights?.risks) {
    // Basic runway risk check
    if (data.runway_months && data.runway_months < 6) {
      risks.push({
        title: 'Limited Runway',
        description: `With ${Math.round(data.runway_months)} months of runway, fundraising should be a priority.`,
        mitigation: 'Begin fundraising process immediately or reduce burn rate.'
      });
    }
  }
  
  // Customer concentration check - commented out as threshold not in config
  // if (data.customer_concentration_percent && config.thresholds.risk?.customerConcentration?.warning &&
  //     data.customer_concentration_percent > config.thresholds.risk.customerConcentration.warning) {
  //   risks.push({
  //     title: 'Customer Concentration Risk',
  //     description: `${data.customer_concentration_percent}% of revenue from top customers creates vulnerability.`,
  //     mitigation: 'Diversify customer base and implement retention strategies for key accounts.'
  //   });
  // }
  
  if (data.competition_intensity && config.thresholds.metrics?.competition?.high &&
      data.competition_intensity > config.thresholds.metrics.competition.high) {
    risks.push({
      title: 'Competitive Pressure',
      description: 'High competition may compress margins and increase customer acquisition costs.',
      mitigation: 'Focus on differentiation and building customer switching costs.'
    });
  }
  
  return risks;
}

function getMarketTiming(data: any): number {
  // Calculate market timing based on various factors
  let timing = 50; // Start at optimal
  
  if (data.market_growth_rate > 30) timing -= 20; // Fast growth = earlier
  if (data.market_growth_rate < 10) timing += 20; // Slow growth = later
  if (data.competition_intensity > 3) timing += 15; // High competition = later
  
  return Math.max(0, Math.min(100, timing));
}

function getIndustryBenchmarks(data: any): Array<any> {
  const benchmarks = [];
  
  // Get sector and stage specific benchmarks
  const sector = data.sector || data.industry || 'default';
  const stage = data.funding_stage || 'seed';
  const sectorBenchmarks = getBenchmarksForSectorStage(sector, stage);
  
  // Revenue Growth benchmark
  const revenueGrowth = data.revenue_growth_rate_percent || 0;
  const revenueBenchmark = sectorBenchmarks.revenue_growth;
  const revenueP25 = extractBenchmarkValue(revenueBenchmark.p25);
  const revenueP50 = extractBenchmarkValue(revenueBenchmark.p50);
  const revenueP75 = extractBenchmarkValue(revenueBenchmark.p75);
  
  benchmarks.push({
    metric: revenueBenchmark.metric,
    description: revenueBenchmark.description,
    p25: revenueBenchmark.p25,
    p50: revenueBenchmark.p50,
    p75: revenueBenchmark.p75,
    yourValue: revenueGrowth,
    unit: '%',
    yourPercentile: calculatePercentile(revenueGrowth, revenueP25, revenueP50, revenueP75)
  });
  
  // Burn Multiple benchmark
  const burnMultiple = data.burn_multiple || 2;
  const burnBenchmark = sectorBenchmarks.burn_multiple;
  const burnP25 = extractBenchmarkValue(burnBenchmark.p25);
  const burnP50 = extractBenchmarkValue(burnBenchmark.p50);
  const burnP75 = extractBenchmarkValue(burnBenchmark.p75);
  
  benchmarks.push({
    metric: burnBenchmark.metric,
    description: burnBenchmark.description,
    p25: burnBenchmark.p25,
    p50: burnBenchmark.p50,
    p75: burnBenchmark.p75,
    yourValue: burnMultiple,
    unit: 'x',
    yourPercentile: calculatePercentile(burnMultiple, burnP25, burnP50, burnP75, true) // inverse for burn
  });
  
  // Team Size benchmark
  const teamSize = data.team_size_full_time || 10;
  const teamBenchmark = sectorBenchmarks.team_size;
  const teamP25 = extractBenchmarkValue(teamBenchmark.p25);
  const teamP50 = extractBenchmarkValue(teamBenchmark.p50);
  const teamP75 = extractBenchmarkValue(teamBenchmark.p75);
  
  benchmarks.push({
    metric: teamBenchmark.metric,
    description: teamBenchmark.description,
    p25: teamBenchmark.p25,
    p50: teamBenchmark.p50,
    p75: teamBenchmark.p75,
    yourValue: teamSize,
    unit: '',
    yourPercentile: calculatePercentile(teamSize, teamP25, teamP50, teamP75)
  });
  
  // LTV/CAC benchmark
  const ltvCac = data.ltv_cac_ratio || 3;
  const ltvBenchmark = sectorBenchmarks.ltv_cac;
  const ltvP25 = extractBenchmarkValue(ltvBenchmark.p25);
  const ltvP50 = extractBenchmarkValue(ltvBenchmark.p50);
  const ltvP75 = extractBenchmarkValue(ltvBenchmark.p75);
  
  benchmarks.push({
    metric: ltvBenchmark.metric,
    description: ltvBenchmark.description,
    p25: ltvBenchmark.p25,
    p50: ltvBenchmark.p50,
    p75: ltvBenchmark.p75,
    yourValue: ltvCac,
    unit: 'x',
    yourPercentile: calculatePercentile(ltvCac, ltvP25, ltvP50, ltvP75)
  });
  
  // Gross Margin / Take Rate benchmark
  const grossMargin = data.gross_margin_percent || 
                     (sector === 'marketplace' ? data.take_rate_percent : 0) || 60;
  const marginBenchmark = sectorBenchmarks.gross_margin;
  const marginP25 = extractBenchmarkValue(marginBenchmark.p25);
  const marginP50 = extractBenchmarkValue(marginBenchmark.p50);
  const marginP75 = extractBenchmarkValue(marginBenchmark.p75);
  
  benchmarks.push({
    metric: marginBenchmark.metric,
    description: marginBenchmark.description,
    p25: marginBenchmark.p25,
    p50: marginBenchmark.p50,
    p75: marginBenchmark.p75,
    yourValue: grossMargin,
    unit: '%',
    yourPercentile: calculatePercentile(grossMargin, marginP25, marginP50, marginP75)
  });
  
  // Runway benchmark
  const runwayMonths = Math.round(data.runway_months || 12);
  const runwayBenchmark = sectorBenchmarks.runway_months;
  const runwayP25 = extractBenchmarkValue(runwayBenchmark.p25);
  const runwayP50 = extractBenchmarkValue(runwayBenchmark.p50);
  const runwayP75 = extractBenchmarkValue(runwayBenchmark.p75);
  
  benchmarks.push({
    metric: runwayBenchmark.metric,
    description: runwayBenchmark.description,
    p25: runwayBenchmark.p25,
    p50: runwayBenchmark.p50,
    p75: runwayBenchmark.p75,
    yourValue: runwayMonths,
    unit: 'months',
    yourPercentile: calculatePercentile(runwayMonths, runwayP25, runwayP50, runwayP75)
  });
  
  return benchmarks;
}

function calculateTeamSizePercentile(size: number, stage: string): number {
  const benchmarks: Record<string, {p25: number, p50: number, p75: number}> = {
    'Pre-seed': { p25: 2, p50: 4, p75: 8 },
    'Seed': { p25: 5, p50: 10, p75: 20 },
    'Series A': { p25: 15, p50: 30, p75: 60 },
    'Series B': { p25: 40, p50: 80, p75: 150 }
  };
  
  const stageBenchmarks = benchmarks[stage] || benchmarks['Series A'];
  
  if (size < stageBenchmarks.p25) return 20;
  if (size < stageBenchmarks.p50) return 35 + (size - stageBenchmarks.p25) / (stageBenchmarks.p50 - stageBenchmarks.p25) * 15;
  if (size < stageBenchmarks.p75) return 50 + (size - stageBenchmarks.p50) / (stageBenchmarks.p75 - stageBenchmarks.p50) * 25;
  return Math.min(85, 75 + (size - stageBenchmarks.p75) / stageBenchmarks.p75 * 10);
}

function getImprovementOptions(pillar: string): Array<{id: string, description: string, impact: number}> {
  const options: Record<string, Array<{id: string, description: string, impact: number}>> = {
    capital: [
      { id: 'reduce_burn', description: 'Reduce burn rate by 20%', impact: 5 },
      { id: 'improve_ltv', description: 'Increase LTV by 30%', impact: 4 },
      { id: 'extend_runway', description: 'Extend runway to 18+ months', impact: 3 },
      { id: 'optimize_cac', description: 'Reduce CAC by 25%', impact: 4 }
    ],
    advantage: [
      { id: 'file_patent', description: 'File provisional patent', impact: 3 },
      { id: 'increase_nps', description: 'Improve NPS to 50+', impact: 4 },
      { id: 'add_features', description: 'Launch 3 unique features', impact: 5 },
      { id: 'build_moat', description: 'Create data/network moat', impact: 6 }
    ],
    market: [
      { id: 'expand_tam', description: 'Expand to adjacent market', impact: 4 },
      { id: 'accelerate_growth', description: 'Double growth rate', impact: 6 },
      { id: 'capture_share', description: 'Reach 5% market share', impact: 5 },
      { id: 'partnerships', description: 'Sign 2 strategic partnerships', impact: 3 }
    ],
    people: [
      { id: 'hire_vp', description: 'Hire VP Sales/Engineering', impact: 4 },
      { id: 'advisory_board', description: 'Add 3 industry advisors', impact: 3 },
      { id: 'team_growth', description: 'Grow team by 50%', impact: 4 },
      { id: 'retention', description: 'Achieve 90%+ retention', impact: 3 }
    ]
  };
  return options[pillar] || [];
}

function calculateSimulatedScore(pillar: string, currentScore: number, improvements: Set<string>): number {
  let simulatedScore = currentScore;
  const options = getImprovementOptions(pillar);
  
  improvements.forEach(improvementId => {
    const option = options.find(o => o.id === improvementId);
    if (option) {
      simulatedScore += option.impact / 100;
    }
  });
  
  return Math.min(simulatedScore, 0.95); // Cap at 95%
}

function getRecommendations(data: any, llmRecs?: any): Array<any> {
  // Use LLM recommendations if available
  if (llmRecs && llmRecs.length > 0) {
    return llmService.formatRecommendations(llmRecs);
  }
  
  // Use real recommendations from API if available
  if (data.recommendations && data.recommendations.length > 0) {
    return data.recommendations.map((rec: any, idx: number) => ({
      priority: rec.priority || 'MEDIUM',
      title: rec.title,
      description: rec.description,
      impact: rec.impact || 5,
      timeline: rec.timeline || '90 days',
      actions: rec.actions || [],
      metrics: rec.success_metrics || [],
      affects: rec.affected_areas || ['capital']
    }));
  }
  
  // Fallback to basic recommendations if API doesn't provide them
  const recommendations = [];
  
  if (data.burn_multiple > 2) {
    recommendations.push({
      priority: 'CRITICAL',
      title: 'Reduce Burn Rate to Sustainable Levels',
      description: 'Your burn multiple indicates you\'re spending too much relative to growth. This is the #1 risk to address.',
      impact: 8,
      timeline: '30 days',
      actions: [
        'Conduct expense audit and cut non-essential costs',
        'Renegotiate major vendor contracts',
        'Focus resources on highest ROI activities',
        'Consider revenue-based financing vs dilutive equity'
      ],
      metrics: [
        'Achieve burn multiple < 2.0',
        'Extend runway to 18+ months',
        'Maintain or increase growth rate'
      ],
      affects: ['capital']
    });
  }
  
  if (data.net_dollar_retention_percent < 110) {
    recommendations.push({
      priority: 'HIGH',
      title: 'Improve Customer Retention & Expansion',
      description: 'Increasing retention is the fastest path to improving unit economics and growth efficiency.',
      impact: 6,
      timeline: '90 days',
      actions: [
        'Implement customer success program',
        'Create upsell/cross-sell playbooks',
        'Build product features that increase stickiness',
        'Establish quarterly business reviews with key accounts'
      ],
      metrics: [
        'Reach 110%+ net dollar retention',
        'Reduce monthly churn below 5%',
        'Increase average contract value by 20%'
      ],
      affects: ['capital', 'market']
    });
  }
  
  if (data.team_size_full_time < 20 && data.revenue_growth_rate_percent > 100) {
    recommendations.push({
      priority: 'MEDIUM',
      title: 'Scale Your Team Strategically',
      description: 'Your growth rate requires additional talent to maintain momentum and quality.',
      impact: 5,
      timeline: '60 days',
      actions: [
        'Hire VP Sales or VP Engineering (based on biggest gap)',
        'Build customer success function',
        'Add 2-3 senior individual contributors',
        'Engage executive search firm for key roles'
      ],
      metrics: [
        'Fill 3+ key positions',
        'Maintain culture fit (>80% satisfaction)',
        'Increase velocity without increasing burn multiple'
      ],
      affects: ['people', 'advantage']
    });
  }
  
  return recommendations;
}