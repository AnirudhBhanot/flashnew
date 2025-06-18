/**
 * Migration Example: AnalysisResults Component
 * Shows how to migrate from hardcoded values to configuration system
 */

import React, { useState, useRef, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { createRoot } from 'react-dom/client';
import { InvestmentMemo } from './InvestmentMemo';
import { llmService } from '../../services/llmService';
import { getBenchmarksForSectorStage, calculatePercentile, extractBenchmarkValue } from '../../industry_benchmarks';

// NEW: Import configuration hooks
import { 
  useConfiguration, 
  useSuccessThresholds, 
  useImprovementCalculator,
  useAnimationConfig,
  useNumberFormatter,
  useMetricThreshold,
  useDefaults
} from '../../hooks/useConfiguration';

import './AnalysisResults.css';

interface AnalysisResultsProps {
  data: any;
  onExportPDF?: () => void;
}

export const AnalysisResults: React.FC<AnalysisResultsProps> = ({ data, onExportPDF }) => {
  // State management
  const [activeView, setActiveView] = useState<'overview' | 'camp' | 'insights' | 'recommendations'>('overview');
  const [expandedCAMP, setExpandedCAMP] = useState<string | null>(null);
  const [showQuickSummary, setShowQuickSummary] = useState(false);
  const [expandedMetrics, setExpandedMetrics] = useState<Set<string>>(new Set());
  const [simulatedImprovements, setSimulatedImprovements] = useState<Record<string, Set<string>>>(/* ... */);
  const [completedActions, setCompletedActions] = useState<Set<number>>(new Set());
  const [showGlossary, setShowGlossary] = useState<string | null>(null);
  
  // LLM Integration State
  const [llmRecommendations, setLlmRecommendations] = useState<any>(null);
  const [isLoadingLLM, setIsLoadingLLM] = useState(false);
  const [llmAvailable, setLlmAvailable] = useState(false);
  const [showAIBadge, setShowAIBadge] = useState(false);
  const [dynamicWhatIfResult, setDynamicWhatIfResult] = useState<any>(null);
  const [isLoadingWhatIf, setIsLoadingWhatIf] = useState(false);
  
  // NEW: Configuration hooks
  const { config, isFeatureEnabled } = useConfiguration();
  const successThresholds = useSuccessThresholds(data.funding_stage, data.sector);
  const improvementCalculator = useImprovementCalculator(data.success_probability || 0.5);
  const animationConfig = useAnimationConfig();
  const numberFormatter = useNumberFormatter();
  const defaults = useDefaults();
  
  // NEW: Get metric thresholds
  const burnThresholds = useMetricThreshold('burn', data.funding_stage, data.sector);
  const teamThresholds = useMetricThreshold('team.size', data.funding_stage, data.sector);
  const marketThresholds = useMetricThreshold('market.tam', data.funding_stage, data.sector);
  
  // Calculate derived metrics with defaults
  const successProbability = data.success_probability || defaults.probability;
  const confidenceScore = data.confidence_score || defaults.confidence;
  const verdict = data.verdict || 'CONDITIONAL PASS';
  const riskLevel = data.risk_level || 'MEDIUM';
  
  // Check LLM availability
  useEffect(() => {
    if (isFeatureEnabled('llmRecommendations')) {
      checkLLMAvailability();
    }
  }, [isFeatureEnabled]);
  
  // Fetch LLM recommendations when data changes
  useEffect(() => {
    if (data && llmAvailable && isFeatureEnabled('llmRecommendations')) {
      fetchLLMRecommendations();
    }
  }, [data, llmAvailable, isFeatureEnabled]);

  // Helper functions using configuration
  const getVerdictDisplay = (probability: number) => {
    const level = successThresholds.getLevel(probability);
    const message = successThresholds.getMessage(probability);
    const color = successThresholds.getColor(probability);
    
    return { 
      text: message,
      color,
      className: `verdict-${level}`
    };
  };

  const formatPercentage = (value: number) => numberFormatter.formatPercentage(value);
  const formatCurrency = (value: number) => numberFormatter.formatCurrency(value);

  const verdictInfo = getVerdictDisplay(successProbability);

  return (
    <div className="analysis-results">
      {/* Header Section */}
      <motion.div 
        className="results-header-section"
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: animationConfig.getDuration() / 1000 }}
      >
        {/* ... header content ... */}
      </motion.div>

      {/* Success Score Card */}
      <motion.div 
        className="success-score-card"
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ 
          delay: animationConfig.getDelay() / 1000,
          duration: animationConfig.getDuration() / 1000
        }}
      >
        <div className="score-left">
          <div className="verdict-display">
            <span className="verdict-emoji">{verdictInfo.emoji}</span>
            <h2 className={`verdict-text ${verdictInfo.className}`}>{verdictInfo.text}</h2>
          </div>
          <p className="verdict-description">
            {/* Use success messages from configuration */}
            {successThresholds.getMessage(successProbability)}
          </p>
          
          {/* Success meter with configured colors */}
          <div className="success-meter">
            <svg viewBox="0 0 200 200" className="meter-svg">
              <motion.circle
                cx="100" cy="100" r="85"
                fill="none"
                stroke={successThresholds.getColor(successProbability)}
                strokeWidth="20"
                // ... other props
              />
            </svg>
          </div>
        </div>
      </motion.div>

      {/* Business metric comparisons using configured thresholds */}
      <div className="performance-summary">
        <h2>Performance Summary</h2>
        <div className="summary-grid">
          <MetricCard
            icon="💰"
            title="Financial Health"
            metrics={[
              { 
                label: 'Revenue Growth', 
                value: formatPercentage(data.revenue_growth_rate_percent / 100 || 0),
                tooltip: 'Year-over-year revenue growth rate'
              },
              { 
                label: 'Burn Multiple', 
                value: `${(data.burn_multiple || defaults.burnMultiple).toFixed(1)}x`,
                tooltip: 'Cash burned divided by net new ARR'
              },
              { 
                label: 'Runway', 
                value: `${data.runway_months || defaults.runway} months`,
                tooltip: 'Months of operations remaining'
              }
            ]}
            // Use configured thresholds for insights
            insight={
              data.burn_multiple < burnThresholds.good 
                ? '✅ Efficient capital use' 
                : data.burn_multiple < burnThresholds.warning
                ? '📊 Monitor burn rate'
                : '⚠️ High burn rate'
            }
            cardData={data}
          />

          <MetricCard
            icon="📈"
            title="Market Position"
            metrics={[
              { 
                label: 'TAM Size', 
                value: formatCurrency(data.tam_size_usd || 0),
                tooltip: 'Total Addressable Market'
              },
              { 
                label: 'Market Growth', 
                value: formatPercentage(data.market_growth_rate / 100 || 0),
                tooltip: 'Annual growth rate of your target market'
              },
              { 
                label: 'Competition', 
                value: data.competition_intensity > marketThresholds.competition.high 
                  ? 'High' 
                  : data.competition_intensity > marketThresholds.competition.medium
                  ? 'Moderate'
                  : 'Low',
                tooltip: 'Competitive intensity in your market'
              }
            ]}
            insight={
              data.tam_size_usd > marketThresholds.tam.large 
                ? '✅ Large opportunity' 
                : data.tam_size_usd > marketThresholds.tam.medium
                ? '📊 Good market size'
                : '📊 Niche market'
            }
            cardData={data}
          />

          <MetricCard
            icon="👥"
            title="Team & Execution"
            metrics={[
              { 
                label: 'Team Size', 
                value: `${data.team_size_full_time || defaults.teamSize}`,
                tooltip: 'Number of full-time employees'
              },
              { 
                label: 'Avg Experience', 
                value: `${data.years_experience_avg || defaults.experience} years`,
                tooltip: 'Average years of relevant industry experience'
              },
              { 
                label: 'Key Hires', 
                value: data.team_size_full_time > teamThresholds.optimal ? 'Good' : 'Needed',
                tooltip: 'Assessment of whether key roles are filled'
              }
            ]}
            insight={
              data.years_experience_avg > config.thresholds.metrics.team.experience.senior 
                ? '✅ Experienced team' 
                : data.years_experience_avg > config.thresholds.metrics.team.experience.mid
                ? '📊 Growing team'
                : '📊 Building experience'
            }
            cardData={data}
          />
        </div>
      </div>

      {/* Improvement potential using configured calculator */}
      {activeView === 'recommendations' && (
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
              <span className="score">
                {formatPercentage(
                  Math.min(
                    successProbability + improvementCalculator(completedActions.size),
                    config.thresholds.success.probability.excellent
                  )
                )}
              </span>
            </div>
          </div>
          <p className="impact-note">
            {config.messages.improvements.available.replace(
              '{amount}',
              Math.round(improvementCalculator(completedActions.size) * 100).toString()
            )}
          </p>
        </div>
      )}

      {/* Progress tracker with configured milestones */}
      <div className="progress-tracker">
        <h3>Track Your Improvements</h3>
        
        <div className="progress-overview">
          <div className="actions-completed">
            <span className="number">{completedActions.size}</span>
            <span className="label">Actions Completed</span>
          </div>
          <div className="score-improvement">
            <span className="number">
              +{Math.floor(improvementCalculator(completedActions.size) * 100)}%
            </span>
            <span className="label">Score Improvement</span>
          </div>
          <div className="next-milestone">
            <span className="number">
              {Math.max(
                0, 
                config.thresholds.success.improvements.milestoneActions[0] - completedActions.size
              )}
            </span>
            <span className="label">Actions to Next Level</span>
          </div>
        </div>
      </div>

      {/* Export PDF if feature enabled */}
      {isFeatureEnabled('exportPDF') && (
        <button className="export-pdf-btn" onClick={handleExportPDF}>
          <span className="icon">📄</span>
          Export Report
        </button>
      )}
    </div>
  );
};

// MIGRATION SUMMARY:
// 
// 1. REPLACED HARDCODED VALUES:
//    - successProbability >= 0.65 → successThresholds.getLevel()
//    - formatPercentage with fixed decimals → numberFormatter.formatPercentage()
//    - burn_multiple < 2 → burnThresholds.good
//    - team_size > 20 → teamThresholds.optimal
//    - TAM > 50B → marketThresholds.tam.large
//    - Fixed improvement calculations → improvementCalculator()
//    - Animation durations → animationConfig.getDuration()
//
// 2. ADDED CONFIGURATION SUPPORT:
//    - Stage-aware thresholds (pre-seed vs Series A)
//    - Sector-aware thresholds (SaaS vs FinTech)
//    - Feature flags (exportPDF, llmRecommendations)
//    - Configurable messages and labels
//    - Dynamic defaults for missing data
//
// 3. BENEFITS:
//    - No more hardcoded business logic
//    - Easy A/B testing of thresholds
//    - Personalized experience by stage/sector
//    - Centralized configuration management
//    - Hot-reloadable without deployment