import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { configService } from '../../services/LegacyConfigService';
import { VALUATION_MULTIPLES, REVENUE_BENCHMARKS, BURN_BENCHMARKS, COMPANY_COMPARABLES } from '../../config/constants';
import './InvestmentMemo.css';

interface InvestmentMemoProps {
  data: any;
}

export const InvestmentMemo: React.FC<InvestmentMemoProps> = ({ data }) => {
  const [config, setConfig] = useState<any>(null);

  useEffect(() => {
    configService.getAllConfig().then(setConfig);
  }, []);

  // Helper functions
  const getVerdictDisplay = (probability: number) => {
    if (probability >= 0.75) return { text: 'STRONG BUY', class: 'strong-buy' };
    if (probability >= 0.65) return { text: 'BUY', class: 'buy' };
    if (probability >= 0.55) return { text: 'HOLD', class: 'hold' };
    if (probability >= 0.45) return { text: 'WATCH', class: 'watch' };
    return { text: 'PASS', class: 'pass' };
  };

  const getConfidenceDisplay = (confidence: number) => {
    if (confidence >= 0.8) return 'HIGH';
    if (confidence >= 0.6) return 'MEDIUM';
    return 'LOW';
  };

  const calculateValuation = (data: any) => {
    // Simple revenue multiple based on growth rate
    const arr = data.annual_revenue_run_rate || 2000000;
    const growthRate = data.revenue_growth_rate_percent || 100;
    
    const multiples = config?.valuationMultiples || VALUATION_MULTIPLES;
    
    let multiple = multiples.base; // Base multiple
    if (growthRate > 200) multiple = multiples.growth_200_plus;
    else if (growthRate > 150) multiple = multiples.growth_150_plus;
    else if (growthRate > 100) multiple = multiples.growth_100_plus;
    else if (growthRate > 50) multiple = multiples.growth_50_plus || multiples.base;
    
    const fairValue = (arr / 1000000) * multiple;
    return {
      low: Math.round(fairValue * 0.8),
      fair: Math.round(fairValue),
      high: Math.round(fairValue * 1.2)
    };
  };

  const generateInvestmentThesis = (data: any) => {
    const growth = data.revenue_growth_rate_percent || 0;
    const nrr = data.net_dollar_retention_percent || 100;
    const burnMultiple = data.burn_multiple || 2;
    
    let thesis = '';
    
    if (growth > 200 && burnMultiple < 2) {
      thesis = 'Exceptional growth efficiency in a large market. ';
    } else if (growth > 150) {
      thesis = 'Strong growth momentum with improving unit economics. ';
    } else if (burnMultiple < 1.5) {
      thesis = 'Capital efficient growth model approaching profitability. ';
    } else {
      thesis = 'Early-stage company with developing metrics. ';
    }
    
    if (nrr > 130) {
      thesis += 'Outstanding product-market fit evidenced by net revenue expansion. ';
    } else if (nrr > 110) {
      thesis += 'Solid customer retention with upsell potential. ';
    }
    
    thesis += `Operating in a $${Math.round((data.tam_size_usd || 10000000000) / 1000000000)}B market.`;
    
    return thesis;
  };

  const getComparableCompanies = (data: any): string[] => {
    const sector = data.sector || 'SaaS';
    const stage = data.funding_stage || 'Series A';
    
    const comparables = config?.companyComparables || COMPANY_COMPARABLES;
    
    return comparables[sector]?.[stage] || comparables['SaaS']?.[stage] || ['Similar high-growth companies'];
  };

  const getKeyMetrics = (data: any) => {
    return [
      {
        label: 'Annual Revenue',
        value: `$${((data.annual_revenue_run_rate || 0) / 1000000).toFixed(1)}M`,
        benchmark: 'On track',
        good: true
      },
      {
        label: 'Growth Rate',
        value: `${data.revenue_growth_rate_percent || 0}%`,
        benchmark: data.revenue_growth_rate_percent > (config?.performanceBenchmarks?.revenue_growth?.excellent || 150) ? 'Top 10%' : 'Top 25%',
        good: data.revenue_growth_rate_percent > (config?.performanceBenchmarks?.revenue_growth?.good || 100)
      },
      {
        label: 'Burn Multiple',
        value: (data.burn_multiple || 0).toFixed(1),
        benchmark: data.burn_multiple < 1.5 ? 'Excellent' : data.burn_multiple < 2 ? 'Good' : 'High',
        good: data.burn_multiple < 2
      },
      {
        label: 'Net Revenue Retention',
        value: `${data.net_dollar_retention_percent || 100}%`,
        benchmark: data.net_dollar_retention_percent > 120 ? 'Top tier' : 'Average',
        good: data.net_dollar_retention_percent > 110
      },
      {
        label: 'LTV:CAC Ratio',
        value: `${(data.ltv_cac_ratio || 3).toFixed(1)}:1`,
        benchmark: data.ltv_cac_ratio > 3 ? 'Healthy' : 'Needs work',
        good: data.ltv_cac_ratio > 3
      },
      {
        label: 'Runway',
        value: `${Math.round(data.runway_months || 12)} months`,
        benchmark: data.runway_months > 18 ? 'Strong' : 'Adequate',
        good: data.runway_months > 18
      }
    ];
  };

  const getStrengths = (data: any) => {
    const strengths = [];
    
    const benchmarks = config?.performanceBenchmarks || {};
    
    if (data.revenue_growth_rate_percent > 200) {
      strengths.push('Exceptional revenue growth (>200% YoY)');
    }
    if (data.burn_multiple < (benchmarks.burn_multiple?.excellent || 1.5)) {
      strengths.push('Capital efficient growth model');
    }
    if (data.net_dollar_retention_percent > 120) {
      strengths.push('Strong product-market fit with expansion');
    }
    if (data.team_size_full_time > 20 && data.years_experience_avg > 10) {
      strengths.push('Experienced team with domain expertise');
    }
    if (data.tam_size_usd > 10000000000) {
      strengths.push('Large addressable market opportunity');
    }
    
    return strengths.slice(0, config?.displayLimits?.strengths || 3);
  };

  const getRisks = (data: any) => {
    const risks = [];
    
    if (data.burn_multiple > 2) {
      risks.push('High burn rate relative to growth');
    }
    if (data.runway_months < 12) {
      risks.push('Limited runway requiring near-term funding');
    }
    if (data.customer_concentration_percent > 30) {
      risks.push('Customer concentration risk');
    }
    if (data.competition_intensity > 3) {
      risks.push('Intense competitive landscape');
    }
    if (!data.has_patent && !data.has_data_moat) {
      risks.push('Limited defensibility/moat');
    }
    
    return risks.slice(0, config?.displayLimits?.risks || 3);
  };

  const getActionableSteps = (data: any) => {
    const steps = [];
    
    if (data.burn_multiple > 2) {
      steps.push('Optimize burn rate to reach <1.5x within 6 months');
    }
    if (data.net_dollar_retention_percent < 110) {
      steps.push('Improve product stickiness and upsell motion');
    }
    if (data.runway_months < 18) {
      steps.push('Extend runway to 18-24 months');
    }
    if (data.ltv_cac_ratio < 3) {
      steps.push('Improve unit economics to achieve 3:1 LTV:CAC');
    }
    
    return steps.slice(0, config?.displayLimits?.action_steps || 3);
  };

  const getPatternIcon = (pattern: string) => {
    const icons: Record<string, string> = {
      'efficient_growth': '🚀',
      'market_leader': '👑',
      'vc_hypergrowth': '💰',
      'capital_efficient': '💎',
      'b2b_saas': '☁️',
      'product_led': '🎯',
      'bootstrap_profitable': '🌱',
      'ai_ml_core': '🤖',
      'platform_network': '🌐',
      'deep_tech': '🔬'
    };
    return icons[pattern] || '📊';
  };

  const getStageWeightings = (stage: string) => {
    const weightings: Record<string, Array<{label: string, weight: number}>> = {
      'Pre-seed': [
        { label: 'People & Team', weight: 40 },
        { label: 'Market Opportunity', weight: 30 },
        { label: 'Product Vision', weight: 20 },
        { label: 'Capital Efficiency', weight: 10 }
      ],
      'Seed': [
        { label: 'Product-Market Fit', weight: 35 },
        { label: 'Team Execution', weight: 25 },
        { label: 'Market Timing', weight: 25 },
        { label: 'Unit Economics', weight: 15 }
      ],
      'Series A': [
        { label: 'Growth Metrics', weight: 30 },
        { label: 'Market Expansion', weight: 30 },
        { label: 'Team Scaling', weight: 20 },
        { label: 'Capital Efficiency', weight: 20 }
      ],
      'Series B': [
        { label: 'Revenue Growth', weight: 40 },
        { label: 'Market Leadership', weight: 25 },
        { label: 'Operational Excellence', weight: 20 },
        { label: 'Path to Profitability', weight: 15 }
      ]
    };
    return weightings[stage] || weightings['Series A'];
  };

  const formatPercentage = (value: number) => {
    return `${(value * 100).toFixed(1)}%`;
  };

  const getCampScoreClass = (score: number) => {
    if (score >= 0.7) return 'excellent';
    if (score >= 0.6) return 'good';
    if (score >= 0.5) return 'average';
    return 'needs-work';
  };

  // Calculate all derived data
  const verdict = getVerdictDisplay(data.success_probability);
  const confidence = getConfidenceDisplay(data.confidence_score);
  const valuation = calculateValuation(data);
  const thesis = generateInvestmentThesis(data);
  const comparables = getComparableCompanies(data);
  const metrics = getKeyMetrics(data);
  const strengths = getStrengths(data);
  const risks = getRisks(data);
  const actionableSteps = getActionableSteps(data);

  return (
    <div className="investment-memo">
      {/* Header */}
      <motion.div 
        className="memo-header"
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
      >
        <div className="company-info">
          <h1>Investment Memo</h1>
          <div className="company-details">
            <span>{data.funding_stage || 'Series A'}</span>
            <span className="separator">•</span>
            <span>{data.sector || 'SaaS'}</span>
            <span className="separator">•</span>
            <span>${((data.annual_revenue_run_rate || 0) / 1000000).toFixed(1)}M ARR</span>
          </div>
        </div>
        <div className={`verdict-badge ${verdict.class}`}>
          <span className="verdict-text">{verdict.text}</span>
          <span className="confidence">Confidence: {confidence}</span>
        </div>
      </motion.div>

      {/* Investment Thesis */}
      <motion.section 
        className="thesis-section"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.1 }}
      >
        <h2>Investment Thesis</h2>
        <div className="thesis-box">
          <p>{thesis}</p>
          <div className="comparables">
            <span className="label">Similar success stories:</span>
            {comparables.map((comp: string, idx: number) => (
              <span key={idx} className="comparable">{comp}</span>
            ))}
          </div>
        </div>
      </motion.section>

      {/* Key Metrics Dashboard */}
      <motion.section 
        className="metrics-section"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.2 }}
      >
        <h2>Key Metrics</h2>
        <div className="metrics-grid">
          {metrics.map((metric, idx) => (
            <motion.div 
              key={idx}
              className={`metric-card ${metric.good ? 'good' : 'warning'}`}
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ delay: 0.3 + idx * 0.05 }}
            >
              <div className="metric-value">{metric.value}</div>
              <div className="metric-label">{metric.label}</div>
              <div className="metric-benchmark">{metric.benchmark}</div>
            </motion.div>
          ))}
        </div>
      </motion.section>

      {/* Strengths & Risks */}
      <motion.section 
        className="analysis-section"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.4 }}
      >
        <div className="strengths-risks">
          <div className="strengths">
            <h3>Key Strengths</h3>
            <ol>
              {strengths.map((strength, idx) => (
                <li key={idx}>{strength}</li>
              ))}
            </ol>
          </div>
          <div className="risks">
            <h3>Key Risks</h3>
            <ol>
              {risks.map((risk, idx) => (
                <li key={idx}>{risk}</li>
              ))}
            </ol>
          </div>
        </div>
      </motion.section>

      {/* CAMP Pillar Scores */}
      <motion.section 
        className="camp-scores-section"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.5 }}
      >
        <h2>CAMP Framework Analysis</h2>
        <div className="camp-grid-scores">
          <div className={`camp-score-card ${getCampScoreClass(data.camp_scores?.capital || 0.5)}`}>
            <div className="camp-score-icon">💰</div>
            <h3>Capital</h3>
            <div className="camp-score-value">{formatPercentage(data.camp_scores?.capital || 0.5)}</div>
            <p className="camp-score-desc">Financial health & efficiency</p>
            <div className="camp-metrics">
              <div className="metric-item">
                <span className="metric-name">Burn Multiple</span>
                <span className="metric-val">{(data.burn_multiple || 0).toFixed(1)}x</span>
              </div>
              <div className="metric-item">
                <span className="metric-name">Runway</span>
                <span className="metric-val">{Math.round(data.runway_months || 12)}mo</span>
              </div>
            </div>
          </div>

          <div className={`camp-score-card ${getCampScoreClass(data.camp_scores?.advantage || 0.5)}`}>
            <div className="camp-score-icon">⚡</div>
            <h3>Advantage</h3>
            <div className="camp-score-value">{formatPercentage(data.camp_scores?.advantage || 0.5)}</div>
            <p className="camp-score-desc">Competitive positioning</p>
            <div className="camp-metrics">
              <div className="metric-item">
                <span className="metric-name">Moat</span>
                <span className="metric-val">{data.has_patent ? 'Strong' : 'Building'}</span>
              </div>
              <div className="metric-item">
                <span className="metric-name">Tech Score</span>
                <span className="metric-val">{data.technology_score || 3}/5</span>
              </div>
            </div>
          </div>

          <div className={`camp-score-card ${getCampScoreClass(data.camp_scores?.market || 0.5)}`}>
            <div className="camp-score-icon">📈</div>
            <h3>Market</h3>
            <div className="camp-score-value">{formatPercentage(data.camp_scores?.market || 0.5)}</div>
            <p className="camp-score-desc">Market opportunity & fit</p>
            <div className="camp-metrics">
              <div className="metric-item">
                <span className="metric-name">TAM</span>
                <span className="metric-val">${Math.round((data.tam_size_usd || 10000000000) / 1000000000)}B</span>
              </div>
              <div className="metric-item">
                <span className="metric-name">Growth</span>
                <span className="metric-val">{data.revenue_growth_rate_percent || 100}%</span>
              </div>
            </div>
          </div>

          <div className={`camp-score-card ${getCampScoreClass(data.camp_scores?.people || 0.5)}`}>
            <div className="camp-score-icon">👥</div>
            <h3>People</h3>
            <div className="camp-score-value">{formatPercentage(data.camp_scores?.people || 0.5)}</div>
            <p className="camp-score-desc">Team strength & experience</p>
            <div className="camp-metrics">
              <div className="metric-item">
                <span className="metric-name">Team Size</span>
                <span className="metric-val">{data.team_size_full_time || 10}</span>
              </div>
              <div className="metric-item">
                <span className="metric-name">Experience</span>
                <span className="metric-val">{data.years_experience_avg || 5}yr</span>
              </div>
            </div>
          </div>
        </div>
      </motion.section>

      {/* Valuation */}
      <motion.section 
        className="valuation-section"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.55 }}
      >
        <h2>Valuation Range</h2>
        <div className="valuation-display">
          <div className="valuation-range">
            <div className="val-item low">
              <span className="val-label">Low</span>
              <span className="val-amount">${valuation.low}M</span>
            </div>
            <div className="val-item fair">
              <span className="val-label">Fair Value</span>
              <span className="val-amount">${valuation.fair}M</span>
            </div>
            <div className="val-item high">
              <span className="val-label">High</span>
              <span className="val-amount">${valuation.high}M</span>
            </div>
          </div>
          <div className="valuation-method">
            Based on revenue multiple analysis and growth rate
          </div>
        </div>
      </motion.section>

      {/* Next Steps */}
      <motion.section 
        className="next-steps-section"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.6 }}
      >
        <h2>Recommended Actions</h2>
        <div className="steps-list">
          {actionableSteps.map((step, idx) => (
            <div key={idx} className="step-item">
              <span className="step-number">{idx + 1}</span>
              <span className="step-text">{step}</span>
            </div>
          ))}
        </div>
      </motion.section>

      {/* Model Analysis Breakdown */}
      <motion.section 
        className="model-breakdown-section"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.7 }}
      >
        <h2>AI Analysis Breakdown</h2>
        <p className="section-subtitle">29 specialized models analyzed your startup</p>
        
        {/* Model Components */}
        <div className="model-components">
          <div className="component-card">
            <div className="component-header">
              <span className="component-icon">🏗️</span>
              <span className="component-name">Base Models</span>
              <span className="component-weight">35%</span>
            </div>
            <div className="component-score">
              {formatPercentage(data.model_components?.base || 0.5)}
            </div>
            <p className="component-desc">Foundation models using contractual architecture</p>
          </div>

          <div className="component-card">
            <div className="component-header">
              <span className="component-icon">🧬</span>
              <span className="component-name">Pattern Recognition</span>
              <span className="component-weight">25%</span>
            </div>
            <div className="component-score">
              {formatPercentage(data.model_components?.patterns || 0.5)}
            </div>
            <p className="component-desc">Identified startup DNA and growth patterns</p>
          </div>

          <div className="component-card">
            <div className="component-header">
              <span className="component-icon">📈</span>
              <span className="component-name">Stage Analysis</span>
              <span className="component-weight">15%</span>
            </div>
            <div className="component-score">
              {formatPercentage(data.model_components?.stage || 0.5)}
            </div>
            <p className="component-desc">{data.funding_stage || 'Series A'} specific evaluation</p>
          </div>

          <div className="component-card">
            <div className="component-header">
              <span className="component-icon">🏭</span>
              <span className="component-name">Industry Expertise</span>
              <span className="component-weight">15%</span>
            </div>
            <div className="component-score">
              {formatPercentage(data.model_components?.industry || 0.5)}
            </div>
            <p className="component-desc">{data.sector || 'SaaS'} vertical insights</p>
          </div>

          <div className="component-card">
            <div className="component-header">
              <span className="component-icon">🎯</span>
              <span className="component-name">CAMP Framework</span>
              <span className="component-weight">10%</span>
            </div>
            <div className="component-score">
              {formatPercentage(data.model_components?.camp_avg || 0.5)}
            </div>
            <p className="component-desc">Capital, Advantage, Market, People analysis</p>
          </div>
        </div>

        {/* Detected Patterns */}
        {data.patterns && data.patterns.length > 0 && (
          <div className="detected-patterns">
            <h3>Detected Patterns</h3>
            <div className="pattern-badges">
              {data.patterns.map((pattern: string, idx: number) => (
                <div key={idx} className="pattern-badge">
                  <span className="pattern-icon">{getPatternIcon(pattern)}</span>
                  <span className="pattern-name">
                    {pattern.replace(/_/g, ' ').split(' ').map(word => 
                      word.charAt(0).toUpperCase() + word.slice(1)
                    ).join(' ')}
                  </span>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Stage-Specific Weightings */}
        <div className="stage-weightings">
          <h3>Stage-Specific Focus: {data.funding_stage || 'Series A'}</h3>
          <div className="weighting-info">
            {getStageWeightings(data.funding_stage || 'Series A').map((item, idx) => (
              <div key={idx} className="weighting-item">
                <span className="weighting-label">{item.label}</span>
                <div className="weighting-bar">
                  <div 
                    className="weighting-fill" 
                    style={{ width: `${item.weight}%` }}
                  />
                </div>
                <span className="weighting-value">{item.weight}%</span>
              </div>
            ))}
          </div>
        </div>

        {/* Model Confidence */}
        <div className="model-confidence">
          <h3>Model Consensus</h3>
          <div className="confidence-meter">
            <div className="confidence-level" style={{ width: `${(data.confidence_score || 0.5) * 100}%` }}>
              <span className="confidence-label">
                {data.confidence_score >= 0.8 ? 'High Agreement' : 
                 data.confidence_score >= 0.6 ? 'Moderate Agreement' : 'Low Agreement'}
              </span>
            </div>
          </div>
          <p className="confidence-desc">
            {data.confidence_score >= 0.8 
              ? 'All models strongly agree on this assessment'
              : data.confidence_score >= 0.6
              ? 'Most models agree with some variation'
              : 'Models show significant variation in assessment'}
          </p>
        </div>
      </motion.section>

      {/* Print Button */}
      <button className="print-button no-print" onClick={() => window.print()}>
        <span className="icon">🖨️</span>
        Print Investment Memo
      </button>
    </div>
  );
};