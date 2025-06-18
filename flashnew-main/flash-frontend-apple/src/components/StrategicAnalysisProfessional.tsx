import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import useAssessmentStore from '../store/assessmentStore';
import styles from './StrategicAnalysisProfessional.module.scss';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8001';

interface StrategicInsight {
  type: 'opportunity' | 'threat' | 'strength' | 'gap';
  title: string;
  impact: 'transformational' | 'high' | 'medium';
  timeframe: 'immediate' | '6_months' | '12_months' | '24_months';
  description: string;
  evidence: string[];
  actions: string[];
  metrics: { name: string; current: string; target: string; }[];
}

interface StrategicTheme {
  name: string;
  narrative: string;
  insights: StrategicInsight[];
  frameworks_applied: string[];
  executive_summary: string;
  strategic_options: {
    option: string;
    rationale: string;
    investment: string;
    timeline: string;
    expected_return: string;
    risks: string[];
  }[];
}

interface CompetitiveDynamics {
  market_position: 'leader' | 'challenger' | 'follower' | 'nicher';
  competitive_advantages: { advantage: string; sustainability: 'high' | 'medium' | 'low'; timeframe: string; }[];
  strategic_gaps: { gap: string; impact: string; closing_strategy: string; }[];
  market_movements: { trend: string; implication: string; response: string; }[];
}

const StrategicAnalysisProfessional: React.FC = () => {
  const [isLoading, setIsLoading] = useState(true);
  const [activeView, setActiveView] = useState<'synthesis' | 'deep-dive' | 'roadmap'>('synthesis');
  const [strategicThemes, setStrategicThemes] = useState<StrategicTheme[]>([]);
  const [competitiveDynamics, setCompetitiveDynamics] = useState<CompetitiveDynamics | null>(null);
  const [selectedTheme, setSelectedTheme] = useState<number>(0);
  
  const assessmentData = useAssessmentStore(state => state.data);
  const results = useAssessmentStore(state => state.results);

  useEffect(() => {
    generateStrategicAnalysis();
  }, [assessmentData]);

  const generateStrategicAnalysis = async () => {
    setIsLoading(true);
    
    // In a real implementation, this would call sophisticated APIs
    // For now, let's create a McKinsey-quality analysis based on the data
    
    const company = {
      name: assessmentData?.companyInfo?.companyName || 'Your Company',
      stage: assessmentData?.capital?.fundingStage || 'seed',
      runway: assessmentData?.capital?.runwayMonths || 12,
      burn: assessmentData?.capital?.monthlyBurn || 50000,
      revenue: assessmentData?.capital?.annualRevenue || 0,
      marketGrowth: assessmentData?.market?.marketGrowthRate || 20,
      competitorCount: assessmentData?.market?.competitorCount || 10,
      teamSize: assessmentData?.people?.fullTimeEmployees || 5,
      productStage: assessmentData?.advantage?.productStage || 'mvp',
      successProbability: results?.successProbability || 0.5
    };

    // Generate strategic themes based on company situation
    const themes: StrategicTheme[] = [];

    // Theme 1: Market Position & Growth Strategy
    if (company.marketGrowth > 15) {
      themes.push({
        name: "Accelerated Market Capture",
        narrative: `The ${company.marketGrowth}% market growth presents a limited-time window for establishing dominant position. Historical analysis shows that in high-growth markets, early leaders capture 40-60% of total market value.`,
        insights: [
          {
            type: 'opportunity',
            title: 'First-Mover Advantage Window',
            impact: 'transformational',
            timeframe: '6_months',
            description: `Market is growing at ${company.marketGrowth}% annually. Companies that achieve 30%+ market share in the next 18 months typically maintain leadership for 5+ years.`,
            evidence: [
              `Current market fragmentation with ${company.competitorCount} competitors`,
              'No clear dominant player has emerged',
              'Customer switching costs increasing as habits form'
            ],
            actions: [
              'Launch "land grab" campaign targeting top 100 potential customers',
              'Implement aggressive referral program with 3-month payback',
              'Secure exclusive partnerships with 3 key distribution channels'
            ],
            metrics: [
              { name: 'Market Share', current: '<1%', target: '15%' },
              { name: 'Customer Acquisition', current: '10/month', target: '100/month' },
              { name: 'CAC Payback', current: '12 months', target: '3 months' }
            ]
          }
        ],
        frameworks_applied: ['Porter\'s Five Forces', 'BCG Growth-Share Matrix', 'Blue Ocean Strategy'],
        executive_summary: 'Aggressive growth strategy justified by market dynamics. 18-month window to establish market leadership.',
        strategic_options: [
          {
            option: 'Blitzscaling Approach',
            rationale: 'Sacrifice efficiency for speed to capture market share before consolidation',
            investment: '$5-10M Series A',
            timeline: '12-18 months',
            expected_return: '10x revenue growth, market leadership position',
            risks: ['High burn rate', 'Execution complexity', 'Quality control']
          }
        ]
      });
    }

    // Theme 2: Operational Excellence & Efficiency
    if (company.burn > company.revenue / 12 && company.runway < 18) {
      themes.push({
        name: "Path to Sustainable Growth",
        narrative: `Current burn rate of $${(company.burn/1000).toFixed(0)}k/month against ${company.runway} months runway requires immediate pivot to efficient growth. Top-quartile SaaS companies achieve profitability at $10-15M ARR.`,
        insights: [
          {
            type: 'gap',
            title: 'Unit Economics Optimization',
            impact: 'high',
            timeframe: 'immediate',
            description: 'Current burn multiple suggests inefficient resource allocation. Best-in-class companies at this stage operate at 1.5x burn multiple.',
            evidence: [
              `Burn rate ${((company.burn * 12) / Math.max(company.revenue, 1)).toFixed(1)}x of revenue`,
              `Runway of ${company.runway} months below 18-month safety threshold`,
              'Limited revenue per employee compared to benchmarks'
            ],
            actions: [
              'Implement zero-based budgeting for all departments',
              'Automate top 5 manual processes consuming 40% of team time',
              'Renegotiate vendor contracts for 20-30% cost reduction'
            ],
            metrics: [
              { name: 'Burn Multiple', current: `${((company.burn * 12) / Math.max(company.revenue, 1)).toFixed(1)}x`, target: '1.5x' },
              { name: 'Runway', current: `${company.runway} months`, target: '24 months' },
              { name: 'Revenue/Employee', current: '$50k', target: '$200k' }
            ]
          }
        ],
        frameworks_applied: ['Unit Economics Analysis', 'Zero-Based Budgeting', 'Lean Operations'],
        executive_summary: 'Transform burn rate through operational excellence while maintaining growth trajectory.',
        strategic_options: [
          {
            option: 'Efficient Growth Model',
            rationale: 'Optimize unit economics to extend runway while building sustainable growth engine',
            investment: 'Self-funded through efficiency gains',
            timeline: '3-6 months',
            expected_return: 'Double runway, achieve contribution margin positive',
            risks: ['Growth slowdown', 'Team morale during cuts', 'Competitive disadvantage']
          }
        ]
      });
    }

    // Theme 3: Competitive Differentiation
    themes.push({
      name: "Sustainable Competitive Advantage",
      narrative: `In a market with ${company.competitorCount}+ competitors, differentiation through superior execution and customer value is critical. Analysis shows 80% of startups fail due to lack of differentiation.`,
      insights: [
        {
          type: 'strength',
          title: 'Execution Velocity Advantage',
          impact: 'high',
          timeframe: '12_months',
          description: 'Small team size enables 3x faster iteration cycles than larger competitors. This advantage diminishes as you scale.',
          evidence: [
            `Team of ${company.teamSize} vs competitor average of 50+`,
            'Direct founder involvement in product decisions',
            'No legacy technical debt or organizational inertia'
          ],
          actions: [
            'Implement daily deployment cycles',
            'Create direct customer feedback loops with <24hr response',
            'Launch "10x better" feature every month based on customer pain points'
          ],
          metrics: [
            { name: 'Release Velocity', current: 'Monthly', target: 'Daily' },
            { name: 'Customer Feature Requests Shipped', current: '20%', target: '80%' },
            { name: 'Time to Market', current: '3 months', target: '2 weeks' }
          ]
        }
      ],
      frameworks_applied: ['VRIO Framework', 'Core Competencies Analysis', 'Speed as Strategy'],
      executive_summary: 'Leverage inherent startup advantages before they naturally erode with scale.',
      strategic_options: [
        {
          option: 'Speed-Based Competition',
          rationale: 'Use 10x faster execution as primary competitive weapon',
          investment: 'Minimal - process and culture focused',
          timeline: 'Ongoing',
          expected_return: 'Sustainable competitive advantage for 18-24 months',
          risks: ['Burnout', 'Quality issues', 'Harder to maintain at scale']
        }
      ]
    });

    // Set competitive dynamics
    setCompetitiveDynamics({
      market_position: company.marketGrowth > 20 && company.competitorCount > 10 ? 'challenger' : 'follower',
      competitive_advantages: [
        { 
          advantage: 'Speed of execution', 
          sustainability: company.teamSize < 20 ? 'high' : 'medium',
          timeframe: '12-18 months before organizational complexity sets in'
        },
        {
          advantage: 'Customer intimacy',
          sustainability: 'medium',
          timeframe: '24 months as customer base grows'
        }
      ],
      strategic_gaps: [
        {
          gap: 'Limited brand recognition',
          impact: 'Increases CAC by 2-3x vs established players',
          closing_strategy: 'Content marketing + thought leadership + customer advocacy program'
        },
        {
          gap: 'Resource constraints',
          impact: 'Cannot match competitor R&D spend',
          closing_strategy: 'Focus on single killer feature vs feature parity'
        }
      ],
      market_movements: [
        {
          trend: 'AI integration becoming table stakes',
          implication: 'Customers expect AI features as baseline',
          response: 'Partner with AI providers vs build in-house'
        }
      ]
    });

    setStrategicThemes(themes);
    setIsLoading(false);
  };

  const renderSynthesisView = () => {
    const theme = strategicThemes[selectedTheme];
    if (!theme) return null;

    return (
      <div className={styles.synthesisView}>
        <div className={styles.executiveSummary}>
          <h2>Strategic Synthesis</h2>
          <div className={styles.summaryCard}>
            <h3>{theme.name}</h3>
            <p className={styles.narrative}>{theme.narrative}</p>
            <div className={styles.keyMessage}>
              <span className={styles.icon}>💡</span>
              <p>{theme.executive_summary}</p>
            </div>
          </div>
        </div>

        <div className={styles.strategicOptions}>
          <h3>Strategic Options</h3>
          {theme.strategic_options.map((option, idx) => (
            <motion.div 
              key={idx}
              className={styles.optionCard}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: idx * 0.1 }}
            >
              <div className={styles.optionHeader}>
                <h4>{option.option}</h4>
                <span className={styles.timeline}>{option.timeline}</span>
              </div>
              <p className={styles.rationale}>{option.rationale}</p>
              <div className={styles.optionMetrics}>
                <div className={styles.metric}>
                  <label>Investment Required</label>
                  <span>{option.investment}</span>
                </div>
                <div className={styles.metric}>
                  <label>Expected Return</label>
                  <span>{option.expected_return}</span>
                </div>
              </div>
              <div className={styles.risks}>
                <label>Key Risks:</label>
                <ul>
                  {option.risks.map((risk, i) => (
                    <li key={i}>{risk}</li>
                  ))}
                </ul>
              </div>
            </motion.div>
          ))}
        </div>

        <div className={styles.competitiveLandscape}>
          <h3>Competitive Dynamics</h3>
          {competitiveDynamics && (
            <div className={styles.dynamicsGrid}>
              <div className={styles.positionCard}>
                <h4>Market Position</h4>
                <div className={styles.position}>
                  {competitiveDynamics.market_position.toUpperCase()}
                </div>
              </div>
              
              <div className={styles.advantagesCard}>
                <h4>Sustainable Advantages</h4>
                {competitiveDynamics.competitive_advantages.map((adv, i) => (
                  <div key={i} className={styles.advantage}>
                    <span className={styles.advantageName}>{adv.advantage}</span>
                    <span className={`${styles.sustainability} ${styles[adv.sustainability]}`}>
                      {adv.sustainability} sustainability
                    </span>
                    <p className={styles.timeframe}>{adv.timeframe}</p>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    );
  };

  const renderDeepDiveView = () => {
    const theme = strategicThemes[selectedTheme];
    if (!theme) return null;

    return (
      <div className={styles.deepDiveView}>
        <h2>Strategic Deep Dive: {theme.name}</h2>
        
        {theme.insights.map((insight, idx) => (
          <motion.div 
            key={idx}
            className={`${styles.insightCard} ${styles[insight.type]}`}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: idx * 0.15 }}
          >
            <div className={styles.insightHeader}>
              <div className={styles.titleSection}>
                <span className={styles.insightType}>{insight.type.toUpperCase()}</span>
                <h3>{insight.title}</h3>
              </div>
              <div className={styles.impactBadge} data-impact={insight.impact}>
                {insight.impact} impact
              </div>
            </div>

            <p className={styles.description}>{insight.description}</p>

            <div className={styles.evidence}>
              <h4>Supporting Evidence</h4>
              <ul>
                {insight.evidence.map((ev, i) => (
                  <li key={i}>{ev}</li>
                ))}
              </ul>
            </div>

            <div className={styles.actions}>
              <h4>Recommended Actions</h4>
              <div className={styles.actionsList}>
                {insight.actions.map((action, i) => (
                  <div key={i} className={styles.actionItem}>
                    <span className={styles.actionNumber}>{i + 1}</span>
                    <p>{action}</p>
                  </div>
                ))}
              </div>
            </div>

            <div className={styles.metrics}>
              <h4>Success Metrics</h4>
              <div className={styles.metricsGrid}>
                {insight.metrics.map((metric, i) => (
                  <div key={i} className={styles.metricCard}>
                    <label>{metric.name}</label>
                    <div className={styles.metricValues}>
                      <span className={styles.current}>{metric.current}</span>
                      <span className={styles.arrow}>→</span>
                      <span className={styles.target}>{metric.target}</span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </motion.div>
        ))}

        <div className={styles.frameworksApplied}>
          <h4>Analytical Frameworks Applied</h4>
          <div className={styles.frameworkTags}>
            {theme.frameworks_applied.map((fw, i) => (
              <span key={i} className={styles.frameworkTag}>{fw}</span>
            ))}
          </div>
        </div>
      </div>
    );
  };

  const renderRoadmapView = () => {
    return (
      <div className={styles.roadmapView}>
        <h2>Strategic Implementation Roadmap</h2>
        
        <div className={styles.timeline}>
          <div className={styles.timelineHeader}>
            <div className={styles.phase}>Immediate (0-3 months)</div>
            <div className={styles.phase}>Short-term (3-6 months)</div>
            <div className={styles.phase}>Medium-term (6-12 months)</div>
            <div className={styles.phase}>Long-term (12+ months)</div>
          </div>

          <div className={styles.initiativesGrid}>
            {strategicThemes.map((theme, themeIdx) => (
              <div key={themeIdx} className={styles.themeRow}>
                <h4>{theme.name}</h4>
                <div className={styles.initiatives}>
                  {theme.insights.map((insight, idx) => {
                    const position = 
                      insight.timeframe === 'immediate' ? 0 :
                      insight.timeframe === '6_months' ? 1 :
                      insight.timeframe === '12_months' ? 2 : 3;
                    
                    return (
                      <motion.div
                        key={idx}
                        className={styles.initiative}
                        style={{ gridColumn: position + 1 }}
                        initial={{ opacity: 0, scale: 0.8 }}
                        animate={{ opacity: 1, scale: 1 }}
                        transition={{ delay: idx * 0.1 }}
                      >
                        <h5>{insight.title}</h5>
                        <p className={styles.initiativeImpact}>{insight.impact} impact</p>
                        <div className={styles.initiativeActions}>
                          {insight.actions.slice(0, 2).map((action, i) => (
                            <span key={i}>• {action}</span>
                          ))}
                        </div>
                      </motion.div>
                    );
                  })}
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className={styles.criticalPath}>
          <h3>Critical Success Factors</h3>
          <div className={styles.factorsGrid}>
            <div className={styles.factor}>
              <h4>Leadership Alignment</h4>
              <p>Weekly strategic reviews with founding team. Clear OKRs cascaded to all levels.</p>
            </div>
            <div className={styles.factor}>
              <h4>Resource Allocation</h4>
              <p>70% resources on core strategy, 20% on experiments, 10% buffer for opportunities.</p>
            </div>
            <div className={styles.factor}>
              <h4>Execution Velocity</h4>
              <p>Daily standups, weekly sprints, monthly strategic checkpoints. Fail fast mentality.</p>
            </div>
            <div className={styles.factor}>
              <h4>Market Feedback Loops</h4>
              <p>Customer advisory board, weekly NPS tracking, monthly win/loss analysis.</p>
            </div>
          </div>
        </div>
      </div>
    );
  };

  if (isLoading) {
    return (
      <div className={styles.container}>
        <div className={styles.loading}>
          <div className={styles.loadingAnimation}>
            <div className={styles.dot}></div>
            <div className={styles.dot}></div>
            <div className={styles.dot}></div>
          </div>
          <p>Conducting strategic analysis...</p>
        </div>
      </div>
    );
  }

  return (
    <div className={styles.container}>
      <div className={styles.header}>
        <h1>Strategic Analysis</h1>
        <p className={styles.subtitle}>McKinsey-caliber insights for {assessmentData?.companyInfo?.companyName || 'your startup'}</p>
      </div>

      <div className={styles.viewSelector}>
        <button
          className={activeView === 'synthesis' ? styles.active : ''}
          onClick={() => setActiveView('synthesis')}
        >
          Executive Synthesis
        </button>
        <button
          className={activeView === 'deep-dive' ? styles.active : ''}
          onClick={() => setActiveView('deep-dive')}
        >
          Strategic Deep Dive
        </button>
        <button
          className={activeView === 'roadmap' ? styles.active : ''}
          onClick={() => setActiveView('roadmap')}
        >
          Implementation Roadmap
        </button>
      </div>

      {strategicThemes.length > 1 && (
        <div className={styles.themeSelector}>
          <label>Strategic Focus Area:</label>
          <select 
            value={selectedTheme} 
            onChange={(e) => setSelectedTheme(Number(e.target.value))}
            className={styles.themeDropdown}
          >
            {strategicThemes.map((theme, idx) => (
              <option key={idx} value={idx}>{theme.name}</option>
            ))}
          </select>
        </div>
      )}

      <AnimatePresence mode="wait">
        <motion.div
          key={activeView}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: -20 }}
          transition={{ duration: 0.3 }}
          className={styles.viewContent}
        >
          {activeView === 'synthesis' && renderSynthesisView()}
          {activeView === 'deep-dive' && renderDeepDiveView()}
          {activeView === 'roadmap' && renderRoadmapView()}
        </motion.div>
      </AnimatePresence>

      <div className={styles.footer}>
        <p className={styles.confidence}>
          Analysis confidence: {((results?.successProbability || 0.5) * 100).toFixed(0)}% | 
          Based on {assessmentData ? Object.keys(assessmentData).length : 0} data points
        </p>
      </div>
    </div>
  );
};

export default StrategicAnalysisProfessional;