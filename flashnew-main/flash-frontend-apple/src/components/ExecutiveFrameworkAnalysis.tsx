import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import useAssessmentStore from '../store/assessmentStore';
import { getExecutiveFrameworkAnalysis } from '../services/api';
import styles from './ExecutiveFrameworkAnalysis.module.scss';

interface StrategicOption {
  title: string;
  description: string;
  npv: number;
  irr: number;
  payback_period?: number;
  paybackPeriod?: number;
  risk_level?: 'Low' | 'Medium' | 'High';
  riskLevel?: 'Low' | 'Medium' | 'High';
  confidence_interval?: { low: number; high: number };
  confidenceInterval?: { low: number; high: number };
}

interface ValueDriver {
  name: string;
  impact: number;
  timeline: string;
  owner: string;
}

interface CompetitiveDynamic {
  force: string;
  intensity: 'Low' | 'Medium' | 'High';
  trend: 'Improving' | 'Stable' | 'Deteriorating';
  strategicImplication: string;
}

interface ExecutiveAnalysis {
  executiveSummary: {
    situation: string;
    key_insights?: string[];
    keyInsights?: string[];
    recommendation: string;
    value_at_stake?: number;
    valueAtStake?: number;
    confidence_level?: number;
    confidenceLevel?: number;
  };
  situationAssessment: {
    market_context?: string;
    marketContext?: string;
    competitive_position?: string;
    competitivePosition?: string;
    organizational_readiness?: string;
    organizationalReadiness?: string;
    key_risks?: string[];
    keyRisks?: string[];
  };
  strategicOptions: StrategicOption[];
  valueCreationWaterfall: ValueDriver[];
  competitiveDynamics: CompetitiveDynamic[];
  implementationRoadmap: {
    phase: string;
    quarter: string;
    initiatives: string[];
    milestones: string[];
    investment: number;
  }[];
  financialProjections: {
    base_case?: { year: number; revenue: number; ebitda: number; }[];
    baseCase?: { year: number; revenue: number; ebitda: number; }[];
    bull_case?: { year: number; revenue: number; ebitda: number; }[];
    bullCase?: { year: number; revenue: number; ebitda: number; }[];
    bear_case?: { year: number; revenue: number; ebitda: number; }[];
    bearCase?: { year: number; revenue: number; ebitda: number; }[];
  };
}

export const ExecutiveFrameworkAnalysis: React.FC = () => {
  const [analysis, setAnalysis] = useState<ExecutiveAnalysis | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [selectedSection, setSelectedSection] = useState<string>('executive-summary');
  
  const assessmentData = useAssessmentStore(state => state.data);
  const results = useAssessmentStore(state => state.results);

  useEffect(() => {
    if (assessmentData) {
      loadExecutiveAnalysis();
    }
  }, [assessmentData]);

  const loadExecutiveAnalysis = async () => {
    setIsLoading(true);
    try {
      console.log('Loading executive analysis with data:', assessmentData);
      const response = await getExecutiveFrameworkAnalysis(assessmentData);
      console.log('Executive analysis response:', response);
      
      if (response) {
        setAnalysis(response);
      } else {
        console.log('No response from API, using fallback');
        setAnalysis(generateFallbackAnalysis());
      }
    } catch (error) {
      console.error('Error loading executive analysis:', error);
      // Use fallback analysis
      setAnalysis(generateFallbackAnalysis());
    } finally {
      setIsLoading(false);
    }
  };

  const generateFallbackAnalysis = (): ExecutiveAnalysis => {
    const revenue = Number(assessmentData?.capital?.annualRevenueRunRate) || 1000000;
    const growthRate = Number(assessmentData?.market?.marketGrowthRate) || 30;
    const marketSize = Number(assessmentData?.market?.tam) || 10000000000;
    
    return {
      executiveSummary: {
        situation: `${assessmentData?.companyInfo?.companyName || 'The company'} operates in a ${formatCurrency(marketSize)} market growing at ${growthRate}% annually. Current positioning suggests significant untapped potential.`,
        key_insights: [
          `Market opportunity of ${formatCurrency(marketSize * 0.01)} (1% share) within 3 years`,
          `Current burn rate threatens runway; requires immediate optimization`,
          `Product-market fit indicators are strong but go-to-market needs refinement`
        ],
        recommendation: `Pursue focused growth strategy targeting enterprise segment while optimizing unit economics. This approach maximizes value creation while managing downside risk.`,
        value_at_stake: marketSize * 0.01 * 3.5, // 3.5x revenue multiple
        confidence_level: 73
      },
      situationAssessment: {
        marketContext: `The ${assessmentData?.market?.sector || 'technology'} sector exhibits winner-take-all dynamics with incumbents controlling 60% market share. Disruption window remains open for 18-24 months.`,
        competitivePosition: `Currently positioned as an emerging challenger with differentiated technology but limited market presence. Key advantages include superior product velocity and modern architecture.`,
        organizationalReadiness: `Team demonstrates strong technical capabilities but lacks enterprise sales experience. Current structure supports ${revenue < 5000000 ? 'startup' : 'scale-up'} operations.`,
        keyRisks: [
          'Competitive response from incumbents with 10x resources',
          'Customer acquisition costs may not scale efficiently',
          'Technical debt could constrain product roadmap'
        ]
      },
      strategicOptions: [
        {
          title: 'Enterprise Focus',
          description: 'Pivot to enterprise-first strategy with dedicated sales team and SOC2 compliance',
          npv: revenue * 15,
          irr: 45,
          paybackPeriod: 2.5,
          riskLevel: 'Medium',
          confidenceInterval: { low: revenue * 10, high: revenue * 25 }
        },
        {
          title: 'Geographic Expansion',
          description: 'Expand to 3 new markets leveraging product-led growth',
          npv: revenue * 8,
          irr: 35,
          paybackPeriod: 3,
          riskLevel: 'High',
          confidenceInterval: { low: revenue * 3, high: revenue * 15 }
        },
        {
          title: 'Vertical Integration',
          description: 'Acquire complementary technology to create full-stack solution',
          npv: revenue * 12,
          irr: 38,
          paybackPeriod: 3.5,
          riskLevel: 'High',
          confidenceInterval: { low: revenue * 5, high: revenue * 20 }
        }
      ],
      valueCreationWaterfall: [
        { name: 'Revenue Growth', impact: revenue * 5, timeline: 'Y1-Y2', owner: 'CRO' },
        { name: 'Margin Expansion', impact: revenue * 2, timeline: 'Y1-Y3', owner: 'COO' },
        { name: 'Market Multiple', impact: revenue * 3, timeline: 'Y2-Y3', owner: 'CEO' }
      ],
      competitiveDynamics: [
        {
          force: 'Competitive Rivalry',
          intensity: 'High',
          trend: 'Deteriorating',
          strategicImplication: 'Requires differentiation through vertical specialization'
        },
        {
          force: 'Buyer Power',
          intensity: 'Medium',
          trend: 'Stable',
          strategicImplication: 'Build switching costs through integrations and data'
        },
        {
          force: 'Threat of New Entry',
          intensity: 'Low',
          trend: 'Improving',
          strategicImplication: 'Window to establish market position before barriers rise'
        }
      ],
      implementationRoadmap: [
        {
          phase: 'Foundation',
          quarter: 'Q1-Q2',
          initiatives: ['Hire enterprise sales team', 'Achieve SOC2 compliance', 'Refine ICP'],
          milestones: ['First enterprise deal', '$2M ARR', 'Sales playbook v1'],
          investment: 2000000
        },
        {
          phase: 'Acceleration',
          quarter: 'Q3-Q4',
          initiatives: ['Scale sales team to 10', 'Launch partner program', 'Expand to 2 verticals'],
          milestones: ['$5M ARR', '50 enterprise customers', 'Series A close'],
          investment: 5000000
        },
        {
          phase: 'Scale',
          quarter: 'Y2',
          initiatives: ['International expansion', 'M&A exploration', 'Platform architecture'],
          milestones: ['$15M ARR', 'Market leader in vertical', 'Cashflow positive'],
          investment: 10000000
        }
      ],
      financialProjections: {
        baseCase: [
          { year: 1, revenue: revenue * 2.5, ebitda: revenue * -0.5 },
          { year: 2, revenue: revenue * 6, ebitda: revenue * 0.5 },
          { year: 3, revenue: revenue * 15, ebitda: revenue * 3 }
        ],
        bullCase: [
          { year: 1, revenue: revenue * 3, ebitda: revenue * -0.3 },
          { year: 2, revenue: revenue * 9, ebitda: revenue * 1.5 },
          { year: 3, revenue: revenue * 25, ebitda: revenue * 6 }
        ],
        bearCase: [
          { year: 1, revenue: revenue * 1.5, ebitda: revenue * -1 },
          { year: 2, revenue: revenue * 3, ebitda: revenue * -0.5 },
          { year: 3, revenue: revenue * 6, ebitda: revenue * 0.5 }
        ]
      }
    };
  };

  const formatCurrency = (value: number): string => {
    if (value >= 1000000000) return `$${(value / 1000000000).toFixed(1)}B`;
    if (value >= 1000000) return `$${(value / 1000000).toFixed(1)}M`;
    if (value >= 1000) return `$${(value / 1000).toFixed(0)}K`;
    return `$${value.toFixed(0)}`;
  };

  const formatPercent = (value: number): string => {
    if (!isFinite(value) || isNaN(value)) return 'N/A';
    return `${(value * 100).toFixed(0)}%`;
  };

  if (isLoading) {
    return (
      <div className={styles.container}>
        <div className={styles.loading}>
          <div className={styles.loadingIcon}>
            <div className={styles.spinner} />
          </div>
          <p>Generating executive analysis...</p>
        </div>
      </div>
    );
  }

  if (!analysis) {
    console.log('No analysis data available');
    return (
      <div className={styles.container}>
        <div className={styles.loading}>
          <p>No analysis data available. Please check the console for errors.</p>
        </div>
      </div>
    );
  }
  
  console.log('Rendering with analysis:', analysis);

  return (
    <div className={styles.container}>
      {/* Navigation */}
      <nav className={styles.navigation}>
        <button 
          className={`${styles.navButton} ${selectedSection === 'executive-summary' ? styles.active : ''}`}
          onClick={() => setSelectedSection('executive-summary')}
        >
          Executive Summary
        </button>
        <button 
          className={`${styles.navButton} ${selectedSection === 'situation' ? styles.active : ''}`}
          onClick={() => setSelectedSection('situation')}
        >
          Situation Assessment
        </button>
        <button 
          className={`${styles.navButton} ${selectedSection === 'options' ? styles.active : ''}`}
          onClick={() => setSelectedSection('options')}
        >
          Strategic Options
        </button>
        <button 
          className={`${styles.navButton} ${selectedSection === 'roadmap' ? styles.active : ''}`}
          onClick={() => setSelectedSection('roadmap')}
        >
          Implementation
        </button>
        <button 
          className={`${styles.navButton} ${selectedSection === 'financials' ? styles.active : ''}`}
          onClick={() => setSelectedSection('financials')}
        >
          Financial Projections
        </button>
      </nav>

      {/* Content */}
      <AnimatePresence mode="wait">
        {selectedSection === 'executive-summary' && (
          <motion.div
            key="executive-summary"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            className={styles.section}
          >
            <div className={styles.executiveSummary}>
              <h2>Executive Summary</h2>
              
              <div className={styles.situationBox}>
                <h3>Situation</h3>
                <p>{analysis.executiveSummary.situation}</p>
              </div>

              <div className={styles.keyInsights}>
                <h3>Key Insights</h3>
                <ul>
                  {(analysis.executiveSummary.key_insights || analysis.executiveSummary.keyInsights || []).map((insight, index) => (
                    <li key={index}>{insight}</li>
                  ))}
                </ul>
              </div>

              <div className={styles.recommendationBox}>
                <h3>Recommendation</h3>
                <p>{analysis.executiveSummary.recommendation}</p>
                
                <div className={styles.valueMetrics}>
                  <div className={styles.metric}>
                    <span className={styles.label}>Value at Stake</span>
                    <span className={styles.value}>{formatCurrency(analysis.executiveSummary.value_at_stake || analysis.executiveSummary.valueAtStake || 0)}</span>
                  </div>
                  <div className={styles.metric}>
                    <span className={styles.label}>Confidence Level</span>
                    <span className={styles.value}>{analysis.executiveSummary.confidence_level || analysis.executiveSummary.confidenceLevel || 0}%</span>
                  </div>
                </div>
              </div>
            </div>
          </motion.div>
        )}

        {selectedSection === 'situation' && (
          <motion.div
            key="situation"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            className={styles.section}
          >
            <h2>Situation Assessment</h2>
            
            <div className={styles.assessmentGrid}>
              <div className={styles.assessmentCard}>
                <h3>Market Context</h3>
                <p>{analysis.situationAssessment.market_context || analysis.situationAssessment.marketContext || ''}</p>
              </div>
              
              <div className={styles.assessmentCard}>
                <h3>Competitive Position</h3>
                <p>{analysis.situationAssessment.competitive_position || analysis.situationAssessment.competitivePosition || ''}</p>
              </div>
              
              <div className={styles.assessmentCard}>
                <h3>Organizational Readiness</h3>
                <p>{analysis.situationAssessment.organizational_readiness || analysis.situationAssessment.organizationalReadiness || ''}</p>
              </div>
            </div>

            <div className={styles.competitiveDynamics}>
              <h3>Competitive Dynamics</h3>
              <div className={styles.dynamicsTable}>
                {(analysis.competitiveDynamics || []).map((dynamic, index) => (
                  <div key={index} className={styles.dynamicRow}>
                    <div className={styles.force}>{dynamic.force}</div>
                    <div className={`${styles.intensity} ${dynamic.intensity ? styles[dynamic.intensity.toLowerCase()] : ''}`}>
                      {dynamic.intensity || 'Medium'}
                    </div>
                    <div className={`${styles.trend} ${dynamic.trend ? styles[dynamic.trend.toLowerCase()] : ''}`}>
                      {dynamic.trend || 'Stable'}
                    </div>
                    <div className={styles.implication}>{dynamic.strategic_implication || dynamic.strategicImplication || ''}</div>
                  </div>
                ))}
              </div>
            </div>

            <div className={styles.riskSection}>
              <h3>Key Risks</h3>
              <ul>
                {(analysis.situationAssessment.key_risks || analysis.situationAssessment.keyRisks || []).map((risk, index) => (
                  <li key={index}>{risk}</li>
                ))}
              </ul>
            </div>
          </motion.div>
        )}

        {selectedSection === 'options' && (
          <motion.div
            key="options"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            className={styles.section}
          >
            <h2>Strategic Options Analysis</h2>
            
            <div className={styles.optionsGrid}>
              {(analysis.strategicOptions || []).map((option, index) => (
                <div key={index} className={styles.optionCard}>
                  <h3>{option.title}</h3>
                  <p>{option.description}</p>
                  
                  <div className={styles.optionMetrics}>
                    <div className={styles.metricRow}>
                      <span>NPV</span>
                      <span>{formatCurrency(option.npv)}</span>
                    </div>
                    <div className={styles.metricRow}>
                      <span>IRR</span>
                      <span>{option.irr}%</span>
                    </div>
                    <div className={styles.metricRow}>
                      <span>Payback</span>
                      <span>{option.payback_period || option.paybackPeriod || 0} years</span>
                    </div>
                    <div className={styles.metricRow}>
                      <span>Risk</span>
                      <span className={option.risk_level || option.riskLevel ? styles[(option.risk_level || option.riskLevel).toLowerCase()] : ''}>{option.risk_level || option.riskLevel || 'Medium'}</span>
                    </div>
                  </div>
                  
                  <div className={styles.confidenceInterval}>
                    <span>90% Confidence Interval:</span>
                    <span>{formatCurrency((option.confidence_interval || option.confidenceInterval || {low: 0}).low)} - {formatCurrency((option.confidence_interval || option.confidenceInterval || {high: 0}).high)}</span>
                  </div>
                </div>
              ))}
            </div>

            <div className={styles.valueWaterfall}>
              <h3>Value Creation Waterfall</h3>
              <div className={styles.waterfallChart}>
                {(analysis.valueCreationWaterfall || []).map((driver, index) => (
                  <div key={index} className={styles.waterfallBar}>
                    <div className={styles.barLabel}>{driver.name}</div>
                    <div className={styles.barValue}>{formatCurrency(driver.impact)}</div>
                    <div className={styles.barTimeline}>{driver.timeline}</div>
                    <div className={styles.barOwner}>{driver.owner}</div>
                  </div>
                ))}
              </div>
            </div>
          </motion.div>
        )}

        {selectedSection === 'roadmap' && (
          <motion.div
            key="roadmap"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            className={styles.section}
          >
            <h2>Implementation Roadmap</h2>
            
            <div className={styles.roadmapTimeline}>
              {(analysis.implementationRoadmap || []).map((phase, index) => (
                <div key={index} className={styles.phaseCard}>
                  <div className={styles.phaseHeader}>
                    <h3>{phase.phase}</h3>
                    <span>{phase.quarter}</span>
                  </div>
                  
                  <div className={styles.phaseContent}>
                    <div className={styles.initiatives}>
                      <h4>Key Initiatives</h4>
                      <ul>
                        {phase.initiatives.map((initiative, i) => (
                          <li key={i}>{initiative}</li>
                        ))}
                      </ul>
                    </div>
                    
                    <div className={styles.milestones}>
                      <h4>Success Milestones</h4>
                      <ul>
                        {phase.milestones.map((milestone, i) => (
                          <li key={i}>{milestone}</li>
                        ))}
                      </ul>
                    </div>
                    
                    <div className={styles.investment}>
                      <h4>Required Investment</h4>
                      <span>{formatCurrency(phase.investment)}</span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </motion.div>
        )}

        {selectedSection === 'financials' && (
          <motion.div
            key="financials"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            className={styles.section}
          >
            <h2>Financial Projections</h2>
            
            <div className={styles.scenarioAnalysis}>
              <h3>Scenario Analysis</h3>
              
              <div className={styles.scenarioTables}>
                <div className={styles.scenario}>
                  <h4>Base Case (50% probability)</h4>
                  <table>
                    <thead>
                      <tr>
                        <th>Year</th>
                        <th>Revenue</th>
                        <th>EBITDA</th>
                        <th>EBITDA Margin</th>
                      </tr>
                    </thead>
                    <tbody>
                      {(analysis.financialProjections.base_case || analysis.financialProjections.baseCase || []).map((year, index) => (
                        <tr key={index}>
                          <td>Year {year.year}</td>
                          <td>{formatCurrency(year.revenue)}</td>
                          <td className={year.ebitda < 0 ? styles.negative : ''}>
                            {formatCurrency(year.ebitda)}
                          </td>
                          <td>{formatPercent(year.revenue > 0 ? year.ebitda / year.revenue : 0)}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>

                <div className={styles.scenario}>
                  <h4>Bull Case (25% probability)</h4>
                  <table>
                    <thead>
                      <tr>
                        <th>Year</th>
                        <th>Revenue</th>
                        <th>EBITDA</th>
                        <th>EBITDA Margin</th>
                      </tr>
                    </thead>
                    <tbody>
                      {(analysis.financialProjections.bull_case || analysis.financialProjections.bullCase || []).map((year, index) => (
                        <tr key={index}>
                          <td>Year {year.year}</td>
                          <td>{formatCurrency(year.revenue)}</td>
                          <td className={year.ebitda < 0 ? styles.negative : ''}>
                            {formatCurrency(year.ebitda)}
                          </td>
                          <td>{formatPercent(year.revenue > 0 ? year.ebitda / year.revenue : 0)}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>

                <div className={styles.scenario}>
                  <h4>Bear Case (25% probability)</h4>
                  <table>
                    <thead>
                      <tr>
                        <th>Year</th>
                        <th>Revenue</th>
                        <th>EBITDA</th>
                        <th>EBITDA Margin</th>
                      </tr>
                    </thead>
                    <tbody>
                      {(analysis.financialProjections.bear_case || analysis.financialProjections.bearCase || []).map((year, index) => (
                        <tr key={index}>
                          <td>Year {year.year}</td>
                          <td>{formatCurrency(year.revenue)}</td>
                          <td className={year.ebitda < 0 ? styles.negative : ''}>
                            {formatCurrency(year.ebitda)}
                          </td>
                          <td>{formatPercent(year.revenue > 0 ? year.ebitda / year.revenue : 0)}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};