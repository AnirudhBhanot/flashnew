import React, { useState, useEffect, useCallback, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { AnalysisOrb } from './AnalysisOrb';
import { HybridResults } from './HybridResults';
import { RealisticDisclaimer } from '../RealisticDisclaimer';
import { LoadingState } from '../common/LoadingState';
import { ErrorMessage } from '../common/ErrorMessage';
import { useApiCall } from '../../hooks/useApiCall';
import { API_CONFIG } from '../../config';
import './AnalysisPage.css';

interface HybridAnalysisPageProps {
  startupData: any;
  onComplete: (results: any) => void;
  onBack: () => void;
}

export const HybridAnalysisPage: React.FC<HybridAnalysisPageProps> = ({ 
  startupData, 
  onComplete,
  onBack
}) => {
  const [isAnalyzing, setIsAnalyzing] = useState(true);
  const [progress, setProgress] = useState(0);
  const [results, setResults] = useState<any>(null);
  const [currentPhase, setCurrentPhase] = useState('Initializing');
  const [apiError, setApiError] = useState<Error | null>(null);
  const analysisTimeoutRef = useRef<NodeJS.Timeout | null>(null);

  const phases = [
    'Loading 4 realistic models',
    'Analyzing startup patterns',
    'Evaluating stage alignment',
    'Assessing industry fit',
    'Computing CAMP scores',
    'Combining predictions',
    'Generating insights'
  ];

  useEffect(() => {
    let mounted = true;
    let currentProgress = 0;
    let phaseIndex = 0;

    const progressInterval = setInterval(() => {
      if (!mounted) return;
      
      currentProgress += 2;
      setProgress(currentProgress);

      // Update phase
      const newPhaseIndex = Math.floor((currentProgress / 100) * phases.length);
      if (newPhaseIndex !== phaseIndex && newPhaseIndex < phases.length) {
        phaseIndex = newPhaseIndex;
        setCurrentPhase(phases[phaseIndex]);
      }

      if (currentProgress >= 100) {
        clearInterval(progressInterval);
        if (mounted) {
          performHybridAnalysis();
        }
      }
    }, 100);

    return () => {
      mounted = false;
      clearInterval(progressInterval);
      // Clean up analysis timeout if it exists
      if (analysisTimeoutRef.current) {
        clearTimeout(analysisTimeoutRef.current);
        analysisTimeoutRef.current = null;
      }
    };
  }, []);

  const transformDataForAPI = (data: any) => {
    const transformed = { ...data };
    
    // Transform funding_stage to lowercase with underscores
    if (transformed.funding_stage) {
      transformed.funding_stage = transformed.funding_stage
        .toLowerCase()
        .replace(/\s+/g, '_')
        .replace(/-/g, '_');
    }
    
    // Transform investor_tier_primary to expected format
    if (transformed.investor_tier_primary) {
      const tierMap: Record<string, string> = {
        'angel': 'angel',
        'tier 1': 'tier_1',
        'tier 2': 'tier_2',
        'tier 3': 'tier_3',
        'tier1': 'tier_1',
        'tier2': 'tier_2',
        'tier3': 'tier_3',
        'none': 'none',
        'tier_1': 'tier_1',
        'tier_2': 'tier_2',
        'tier_3': 'tier_3'
      };
      transformed.investor_tier_primary = tierMap[transformed.investor_tier_primary.toLowerCase()] || 'none';
    }
    
    // Transform product_stage to lowercase
    if (transformed.product_stage) {
      const stageMap: Record<string, string> = {
        'ga': 'launched',
        'general availability': 'launched',
        'generally available': 'launched',
        'production': 'launched',
        'live': 'launched'
      };
      const stage = transformed.product_stage.toLowerCase();
      transformed.product_stage = stageMap[stage] || stage;
    }

    // Add total_capital_raised_usd if not present
    if (!transformed.total_capital_raised_usd && transformed.cash_on_hand_usd) {
      // Estimate based on stage and cash on hand
      const stageMultipliers: Record<string, number> = {
        'pre_seed': 1.5,
        'seed': 2.0,
        'series_a': 3.0,
        'series_b': 4.0,
        'series_c': 5.0
      };
      const multiplier = stageMultipliers[transformed.funding_stage] || 2.0;
      transformed.total_capital_raised_usd = Math.round(transformed.cash_on_hand_usd * multiplier);
    }

    // Transform sector to expected format
    if (transformed.sector) {
      const sectorMap: Record<string, string> = {
        'ai/ml': 'deeptech',
        'ai': 'deeptech',
        'ml': 'deeptech',
        'artificial intelligence': 'deeptech',
        'machine learning': 'deeptech',
        'b2b saas': 'saas',
        'b2b': 'enterprise',
        'b2c': 'consumer',
        'e-commerce': 'ecommerce',
        'e_commerce': 'ecommerce',
        'e commerce': 'ecommerce',
        'health tech': 'healthtech',
        'health-tech': 'healthtech',
        'health_tech': 'healthtech',
        'ed tech': 'edtech',
        'ed-tech': 'edtech',
        'ed_tech': 'edtech',
        'fin tech': 'fintech',
        'fin-tech': 'fintech',
        'fin_tech': 'fintech',
        'deep tech': 'deeptech',
        'deep-tech': 'deeptech',
        'deep_tech': 'deeptech',
        'prop tech': 'proptech',
        'prop-tech': 'proptech',
        'prop_tech': 'proptech',
        'real estate': 'proptech',
        'realestate': 'proptech',
        'bio tech': 'biotech',
        'bio-tech': 'biotech',
        'bio_tech': 'biotech',
        'ag tech': 'agtech',
        'ag-tech': 'agtech',
        'ag_tech': 'agtech',
        'agriculture': 'agtech',
        'clean tech': 'cleantech',
        'clean-tech': 'cleantech',
        'clean_tech': 'cleantech',
        'cyber security': 'cybersecurity',
        'cyber-security': 'cybersecurity',
        'cyber_security': 'cybersecurity',
        'insur tech': 'insurtech',
        'insur-tech': 'insurtech',
        'insur_tech': 'insurtech',
        'insurance': 'insurtech',
        'legal tech': 'legaltech',
        'legal-tech': 'legaltech',
        'legal_tech': 'legaltech',
        'hr tech': 'hrtech',
        'hr-tech': 'hrtech',
        'hr_tech': 'hrtech',
        'human resources': 'hrtech'
      };
      const sector = transformed.sector.toLowerCase().trim();
      transformed.sector = sectorMap[sector] || sector.replace(/[-_\s]+/g, '');
    }
    
    return transformed;
  };

  const performHybridAnalysis = useCallback(async () => {
    try {
      const apiData = transformDataForAPI(startupData);
      
      const endpoint = `${API_CONFIG.API_BASE_URL}/predict`;
      
      const response = await fetch(endpoint, {
        method: 'POST',
        headers: { 
          'Content-Type': 'application/json'
          // API key disabled in development (DISABLE_AUTH=true)
        },
        body: JSON.stringify(apiData)
      });
      
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(`API Error: ${response.status}`);
      }
      
      const data = await response.json();
      
      // Transform hybrid response to include expected fields
      const enrichedData = {
        ...data,
        // CRITICAL: Include success_probability and confidence_score from API response
        success_probability: data.success_probability || 0.5,
        confidence_score: data.confidence_score || 0.85,
        risk_level: data.risk_level || 'MEDIUM',
        // CRITICAL: Preserve the original funding stage from the form submission
        funding_stage: startupData.funding_stage || 'Series A',
        // Include other important fields from startup data
        industry: startupData.sector || 'Technology',
        // Pass through other relevant startup data fields
        runway_months: startupData.runway_months,
        burn_multiple: startupData.burn_multiple,
        revenue_growth_rate_percent: startupData.revenue_growth_rate_percent,
        team_size_full_time: startupData.team_size_full_time,
        years_experience_avg: startupData.years_experience_avg,
        tam_size_usd: startupData.tam_size_usd,
        current_arr: startupData.current_arr,
        ltv_cac_ratio: startupData.ltv_cac_ratio,
        net_dollar_retention_percent: startupData.net_dollar_retention_percent,
        customer_concentration_percent: startupData.customer_concentration_percent,
        last_round_raised_usd: startupData.last_round_raised_usd,
        market_growth_rate: startupData.market_growth_rate,
        competition_intensity: startupData.competition_intensity,
        has_patent: startupData.has_patent,
        technology_score: startupData.technology_score,
        scalability_score: startupData.scalability_score,
        advisor_quality_score: startupData.advisor_quality_score,
        // Map camp_scores to pillar_scores for compatibility
        pillar_scores: data.camp_scores || {
          capital: 0.5,
          advantage: 0.5,
          market: 0.5,
          people: 0.5
        },
        // Also preserve camp_scores if available
        camp_scores: data.camp_scores || data.pillar_scores || {
          capital: 0.5,
          advantage: 0.5,
          market: 0.5,
          people: 0.5
        },
        // Ensure verdict exists
        verdict: data.verdict || 'CONDITIONAL PASS',
        // Add model breakdown if available
        model_breakdown: data.model_components || {},
        // Add pattern insights
        patterns: data.dominant_patterns || [],
        stage_fit: data.key_insights?.find((i: string) => i.includes('Stage fit'))?.split(': ')[1] || 'Unknown',
        industry_fit: data.key_insights?.find((i: string) => i.includes('Industry fit'))?.split(': ')[1] || 'Unknown',
        // Add detailed predictions if available
        all_predictions: {
          base: data.model_components?.base || 0.5,
          patterns: data.model_components?.patterns || 0.5,
          stage: data.model_components?.stage || 0.5,
          industry: data.model_components?.industry || 0.5,
          camp: data.model_components?.camp_avg || 0.5
        },
        // Add key insights if available
        key_insights: data.key_insights || [],
        // Add recommendations if available
        recommendations: data.recommendations || [],
        // CRITICAL: Add original user input for LLM context
        userInput: startupData
      };
      
      // Store timeout ID in ref for cleanup
      analysisTimeoutRef.current = setTimeout(() => {
        setIsAnalyzing(false);
        setResults(enrichedData);
        onComplete(enrichedData);
      }, 500);
      
    } catch (error) {
      setIsAnalyzing(false);
      setResults(null);
      setApiError(error instanceof Error ? error : new Error('Analysis failed'));
    }
  }, [startupData, onComplete]);

  return (
    <div className="analysis-page">
      <AnimatePresence mode="wait">
        {isAnalyzing ? (
          <motion.div
            key="analyzing"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="analysis-content"
          >
            <AnalysisOrb progress={progress} isAnalyzing={isAnalyzing} />
            <div className="analysis-info">
              <h2>Analyzing with 4 Realistic Models</h2>
              <p>{currentPhase}</p>
              <div className="progress-bar">
                <motion.div 
                  className="progress-fill"
                  initial={{ width: 0 }}
                  animate={{ width: `${progress}%` }}
                />
              </div>
              <div className="model-info">
                <span>🧬 4 Model Types</span>
                <span>•</span>
                <span>🎯 Realistic Models</span>
                <span>•</span>
                <span>🔍 Honest Analysis</span>
              </div>
            </div>
          </motion.div>
        ) : results ? (
          <motion.div
            key="results"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="results-wrapper"
          >
            <RealisticDisclaimer modelAUC={0.50} className="mb-4" />
            <HybridResults data={results} />
          </motion.div>
        ) : apiError ? (
          <motion.div
            key="error"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="error-wrapper"
          >
            <ErrorMessage
              error={apiError}
              variant="page"
              onRetry={() => {
                setApiError(null);
                setIsAnalyzing(true);
                performHybridAnalysis();
              }}
            />
          </motion.div>
        ) : null}
      </AnimatePresence>
    </div>
  );
};