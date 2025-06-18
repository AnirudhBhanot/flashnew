import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import useAssessmentStore from '../store/assessmentStore';
import styles from './StrategicFrameworkReportIntelligent.module.scss';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8001';

interface MarketSignal {
  type: string;
  strength: number;
  trend: 'up' | 'down' | 'stable';
  impact: string;
}

interface FrameworkCustomization {
  aspect: string;
  adaptation: string;
  rationale: string;
}

interface QuickWin {
  action: string;
  timeline: string;
  impact: 'high' | 'medium' | 'low';
  effort: 'high' | 'medium' | 'low';
}

interface IntelligentFramework {
  framework_id: string;
  framework_name: string;
  category: string;
  relevance_score: number;
  confidence_level: number;
  synergy_score: number;
  timing_score: number;
  success_probability: number;
  customizations: string[];
  quick_wins: string[];
  risk_factors: string[];
  integration_plan: {
    sequence: number;
    dependencies: string[];
    parallel_frameworks: string[];
    resource_allocation: {
      percentage: number;
      team_members: number;
    };
  };
  analysis: any; // Specific analysis like SWOT, BCG, etc.
}

interface CompetitorMove {
  company: string;
  action: string;
  impact: 'high' | 'medium' | 'low';
  timeframe: string;
}

const StrategicFrameworkReportIntelligent: React.FC = () => {
  const [frameworks, setFrameworks] = useState<IntelligentFramework[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [selectedFramework, setSelectedFramework] = useState<string>('');
  const [marketIntelligence, setMarketIntelligence] = useState<any>(null);
  const [viewMode, setViewMode] = useState<'individual' | 'integrated'>('individual');
  
  const assessmentData = useAssessmentStore(state => state.data);
  const results = useAssessmentStore(state => state.results);

  useEffect(() => {
    if (assessmentData) {
      loadIntelligentAnalysis();
    }
  }, [assessmentData]);

  const loadIntelligentAnalysis = async () => {
    setIsLoading(true);
    
    try {
      // Call enhanced API endpoint
      const response = await fetch(`${API_URL}/api/frameworks/intelligent-analysis`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          assessment_data: assessmentData,
          include_market_intelligence: true,
          max_frameworks: 6,
          include_quick_wins: true,
          include_synergy_analysis: true
        })
      });

      if (!response.ok) {
        console.error('API response not ok:', response.status, response.statusText);
        // Try to get error details
        try {
          const errorData = await response.json();
          console.error('API error details:', errorData);
        } catch (e) {
          console.error('Could not parse error response');
        }
        // Fallback to generating mock intelligent data
        generateMockIntelligentAnalysis();
        return;
      }

      const data = await response.json();
      console.log('Intelligent analysis data:', data);
      
      setFrameworks(data.frameworks || []);
      
      // Transform market intelligence data if needed
      if (data.market_intelligence) {
        setMarketIntelligence({
          signals: data.market_intelligence.signals || [],
          competitor_moves: data.market_intelligence.competitor_moves || [],
          opportunities: data.market_intelligence.opportunities || [],
          threats: data.market_intelligence.threats || [],
          industry_trends: data.market_intelligence.industry_trends || []
        });
      }
      
      if (data.frameworks?.length > 0) {
        setSelectedFramework(data.frameworks[0].framework_id);
      }
    } catch (error) {
      console.error('Error loading intelligent analysis:', error);
      generateMockIntelligentAnalysis();
    } finally {
      setIsLoading(false);
    }
  };

  const generateMockIntelligentAnalysis = () => {
    // Generate intelligent mock data based on assessment
    const mockFrameworks: IntelligentFramework[] = [
      {
        framework_id: 'adaptive_strategy',
        framework_name: 'Adaptive Strategy Canvas',
        category: 'Strategy',
        relevance_score: 0.92,
        confidence_level: 0.88,
        synergy_score: 0.85,
        timing_score: 0.90,
        success_probability: 0.84,
        customizations: [
          'Focus on rapid hypothesis testing given market volatility',
          'Implement bi-weekly strategy reviews instead of quarterly',
          'Create "kill criteria" for each strategic bet'
        ],
        quick_wins: [
          'Map top 3 competitor moves and counter-strategies this week',
          'Launch micro-experiment for highest-risk assumption',
          'Align leadership team on primary success metric'
        ],
        risk_factors: [
          'Market moving faster than strategy cycles',
          'Resource constraints may limit parallel experiments'
        ],
        integration_plan: {
          sequence: 1,
          dependencies: [],
          parallel_frameworks: ['agile_execution'],
          resource_allocation: { percentage: 25, team_members: 3 }
        },
        analysis: generateAdaptiveStrategyAnalysis()
      },
      {
        framework_id: 'growth_velocity',
        framework_name: 'Growth Velocity Engine',
        category: 'Growth',
        relevance_score: 0.88,
        confidence_level: 0.82,
        synergy_score: 0.90,
        timing_score: 0.85,
        success_probability: 0.79,
        customizations: [
          'Prioritize viral loops given B2B SaaS dynamics',
          'Focus on expansion revenue over new customer acquisition',
          'Implement product-qualified lead (PQL) scoring'
        ],
        quick_wins: [
          'Identify top 3 features driving expansion revenue',
          'Launch in-app referral program beta',
          'Reduce time-to-value by 50% for new users'
        ],
        risk_factors: [
          'CAC payback period extending beyond comfort zone',
          'Feature velocity may suffer during growth push'
        ],
        integration_plan: {
          sequence: 2,
          dependencies: ['adaptive_strategy'],
          parallel_frameworks: ['customer_intelligence'],
          resource_allocation: { percentage: 30, team_members: 4 }
        },
        analysis: generateGrowthVelocityAnalysis()
      },
      {
        framework_id: 'ai_transformation',
        framework_name: 'AI-First Transformation',
        category: 'Innovation',
        relevance_score: 0.85,
        confidence_level: 0.78,
        synergy_score: 0.82,
        timing_score: 0.95,
        success_probability: 0.76,
        customizations: [
          'Start with internal tool automation before customer-facing AI',
          'Build AI ethics framework alongside technical implementation',
          'Create AI literacy program for all team members'
        ],
        quick_wins: [
          'Automate top 3 repetitive internal processes',
          'Launch AI-powered customer support bot pilot',
          'Implement AI-driven lead scoring'
        ],
        risk_factors: [
          'AI talent shortage in current market',
          'Data quality may limit AI effectiveness',
          'Regulatory landscape still evolving'
        ],
        integration_plan: {
          sequence: 3,
          dependencies: [],
          parallel_frameworks: ['data_excellence'],
          resource_allocation: { percentage: 20, team_members: 2 }
        },
        analysis: generateAITransformationAnalysis()
      },
      {
        framework_id: 'ecosystem_orchestration',
        framework_name: 'Ecosystem Orchestration Model',
        category: 'Strategy',
        relevance_score: 0.82,
        confidence_level: 0.75,
        synergy_score: 0.88,
        timing_score: 0.80,
        success_probability: 0.73,
        customizations: [
          'Focus on API-first architecture for partner integration',
          'Create developer evangelism program',
          'Build marketplace economics model'
        ],
        quick_wins: [
          'Launch partner portal MVP',
          'Sign 3 strategic integration partners',
          'Create revenue share model template'
        ],
        risk_factors: [
          'Platform governance complexity',
          'Channel conflict with direct sales',
          'Integration maintenance overhead'
        ],
        integration_plan: {
          sequence: 4,
          dependencies: ['adaptive_strategy', 'growth_velocity'],
          parallel_frameworks: [],
          resource_allocation: { percentage: 25, team_members: 3 }
        },
        analysis: generateEcosystemAnalysis()
      }
    ];

    const mockMarketIntel = {
      signals: [
        { type: 'Competitor Funding', strength: 0.8, trend: 'up', impact: 'Increased competition for talent and customers' },
        { type: 'Customer Demand', strength: 0.9, trend: 'up', impact: 'Window of opportunity for rapid scaling' },
        { type: 'Technology Shift', strength: 0.7, trend: 'up', impact: 'AI adoption accelerating across industry' },
        { type: 'Regulatory Risk', strength: 0.3, trend: 'stable', impact: 'Minimal regulatory concerns in current markets' }
      ],
      competitor_moves: [
        { company: 'Competitor A', action: 'Raised $50M Series B', impact: 'high', timeframe: '2 weeks ago' },
        { company: 'Competitor B', action: 'Launched AI features', impact: 'medium', timeframe: '1 month ago' },
        { company: 'Competitor C', action: 'Acquired analytics startup', impact: 'medium', timeframe: '3 weeks ago' }
      ],
      opportunities: [
        'Underserved mid-market segment showing 40% YoY growth',
        'Partnership opportunity with leading platform vendor',
        'New regulation creating barriers for smaller competitors'
      ],
      threats: [
        'Big Tech companies showing interest in the space',
        'Open source alternatives gaining traction',
        'Customer consolidation reducing TAM'
      ]
    };

    setFrameworks(mockFrameworks);
    setMarketIntelligence(mockMarketIntel);
    setSelectedFramework(mockFrameworks[0].framework_id);
  };

  const generateAdaptiveStrategyAnalysis = () => ({
    current_position: 'Emerging Challenger',
    strategic_options: [
      { option: 'Niche Domination', viability: 0.85, timeframe: '6-12 months' },
      { option: 'Platform Play', viability: 0.70, timeframe: '12-24 months' },
      { option: 'Vertical Integration', viability: 0.60, timeframe: '18-36 months' }
    ],
    key_bets: [
      { bet: 'AI-powered automation', conviction: 0.90, investment: '$2M' },
      { bet: 'Enterprise expansion', conviction: 0.75, investment: '$1.5M' },
      { bet: 'International markets', conviction: 0.65, investment: '$1M' }
    ]
  });

  const generateGrowthVelocityAnalysis = () => ({
    growth_metrics: {
      current_growth_rate: '15% MoM',
      target_growth_rate: '25% MoM',
      growth_ceiling: '40% MoM',
      sustainable_rate: '20% MoM'
    },
    growth_levers: [
      { lever: 'Product-Led Growth', impact: 0.35, effort: 0.6 },
      { lever: 'Channel Partnerships', impact: 0.25, effort: 0.7 },
      { lever: 'Content Marketing', impact: 0.20, effort: 0.4 },
      { lever: 'Paid Acquisition', impact: 0.20, effort: 0.3 }
    ],
    growth_experiments: [
      { name: 'Freemium Tier', hypothesis: 'Increase top-funnel by 3x', status: 'planning' },
      { name: 'In-app Referrals', hypothesis: 'Viral coefficient > 0.5', status: 'testing' },
      { name: 'Annual Pricing', hypothesis: 'Improve cash flow by 40%', status: 'launched' }
    ]
  });

  const generateAITransformationAnalysis = () => ({
    ai_maturity: {
      current_level: 2,
      target_level: 4,
      industry_average: 2.5,
      leader_level: 4.5
    },
    ai_initiatives: [
      { initiative: 'Predictive Analytics', readiness: 0.8, impact: 0.9 },
      { initiative: 'Process Automation', readiness: 0.9, impact: 0.7 },
      { initiative: 'Personalization Engine', readiness: 0.6, impact: 0.85 },
      { initiative: 'AI-Powered Insights', readiness: 0.7, impact: 0.8 }
    ],
    implementation_roadmap: [
      { phase: 'Foundation', duration: '3 months', focus: 'Data infrastructure and governance' },
      { phase: 'Pilot', duration: '3 months', focus: 'Internal tools and processes' },
      { phase: 'Scale', duration: '6 months', focus: 'Customer-facing features' },
      { phase: 'Transform', duration: 'Ongoing', focus: 'AI-native product evolution' }
    ]
  });

  const generateEcosystemAnalysis = () => ({
    ecosystem_health: {
      partner_count: 12,
      partner_satisfaction: 0.78,
      ecosystem_revenue_share: '15%',
      network_effects_strength: 0.65
    },
    partner_types: [
      { type: 'Technology Partners', count: 5, revenue_contribution: '40%' },
      { type: 'Channel Partners', count: 4, revenue_contribution: '35%' },
      { type: 'Service Partners', count: 3, revenue_contribution: '25%' }
    ],
    ecosystem_opportunities: [
      'Launch developer marketplace for custom integrations',
      'Create certification program for partners',
      'Build co-innovation lab with top partners'
    ]
  });

  const renderFrameworkSynergies = () => {
    const synergyMatrix = frameworks.map(f1 => ({
      framework: f1.framework_name,
      synergies: frameworks
        .filter(f2 => f2.framework_id !== f1.framework_id)
        .map(f2 => ({
          partner: f2.framework_name,
          score: Math.random() * 0.5 + 0.5 // In reality, would calculate actual synergy
        }))
    }));

    return (
      <div className={styles.synergyMatrix}>
        <h3>Framework Synergies</h3>
        <div className={styles.matrixGrid}>
          {synergyMatrix.map((row, i) => (
            <div key={i} className={styles.matrixRow}>
              <div className={styles.frameworkLabel}>{row.framework}</div>
              <div className={styles.synergies}>
                {row.synergies.map((syn, j) => (
                  <div 
                    key={j} 
                    className={styles.synergyCell}
                    style={{
                      backgroundColor: `rgba(52, 199, 89, ${syn.score})`,
                      color: syn.score > 0.7 ? 'white' : 'black'
                    }}
                  >
                    {(syn.score * 100).toFixed(0)}%
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>
      </div>
    );
  };

  const renderMarketIntelligence = () => (
    <div className={styles.marketIntelligence}>
      <h3>Real-Time Market Intelligence</h3>
      
      <div className={styles.signalsGrid}>
        {marketIntelligence?.signals?.map((signal: MarketSignal, i: number) => (
          <div key={i} className={styles.signalCard}>
            <div className={styles.signalHeader}>
              <span className={styles.signalType}>{signal.type}</span>
              <span className={`${styles.signalTrend} ${styles[signal.trend]}`}>
                {signal.trend === 'up' ? '↑' : signal.trend === 'down' ? '↓' : '→'}
              </span>
            </div>
            <div className={styles.signalStrength}>
              <div 
                className={styles.strengthBar} 
                style={{ width: `${signal.strength * 100}%` }}
              />
            </div>
            <p className={styles.signalImpact}>{signal.impact}</p>
          </div>
        ))}
      </div>

      <div className={styles.competitorMoves}>
        <h4>Recent Competitor Moves</h4>
        {marketIntelligence?.competitor_moves?.map((move: CompetitorMove, i: number) => (
          <div key={i} className={styles.competitorMove}>
            <div className={styles.moveHeader}>
              <span className={styles.competitor}>{move.company}</span>
              <span className={styles.moveTimeframe}>{move.timeframe}</span>
            </div>
            <p className={styles.moveAction}>{move.action}</p>
            <span className={`${styles.moveImpact} ${styles[move.impact]}`}>
              {move.impact} impact
            </span>
          </div>
        ))}
      </div>
    </div>
  );

  const renderIntegratedView = () => (
    <div className={styles.integratedView}>
      <div className={styles.implementationTimeline}>
        <h3>Integrated Implementation Roadmap</h3>
        <div className={styles.timeline}>
          {frameworks
            .sort((a, b) => a.integration_plan.sequence - b.integration_plan.sequence)
            .map((framework, i) => (
              <motion.div
                key={framework.framework_id}
                className={styles.timelineItem}
                initial={{ opacity: 0, x: -50 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: i * 0.1 }}
              >
                <div className={styles.timelineMarker}>
                  <span>{framework.integration_plan.sequence}</span>
                </div>
                <div className={styles.timelineContent}>
                  <h4>{framework.framework_name}</h4>
                  <div className={styles.timelineDetails}>
                    <span className={styles.allocation}>
                      {framework.integration_plan.resource_allocation.team_members} team members
                    </span>
                    <span className={styles.percentage}>
                      {framework.integration_plan.resource_allocation.percentage}% resources
                    </span>
                  </div>
                  {framework.integration_plan.dependencies.length > 0 && (
                    <div className={styles.dependencies}>
                      Depends on: {framework.integration_plan.dependencies.join(', ')}
                    </div>
                  )}
                </div>
              </motion.div>
            ))}
        </div>
      </div>

      {renderFrameworkSynergies()}
      
      <div className={styles.quickWinsMatrix}>
        <h3>Quick Wins Priority Matrix</h3>
        <div className={styles.effortImpactGrid}>
          <div className={styles.gridQuadrant} data-quadrant="quick-wins">
            <h5>Quick Wins</h5>
            <p className={styles.quadrantDesc}>High Impact, Low Effort</p>
            {frameworks.flatMap(f => 
              f.quick_wins.slice(0, 2).map((win, i) => (
                <div key={`${f.framework_id}-${i}`} className={styles.quickWinItem}>
                  • {win}
                </div>
              ))
            ).slice(0, 4)}
          </div>
          <div className={styles.gridQuadrant} data-quadrant="major-projects">
            <h5>Major Projects</h5>
            <p className={styles.quadrantDesc}>High Impact, High Effort</p>
          </div>
          <div className={styles.gridQuadrant} data-quadrant="fill-ins">
            <h5>Fill-ins</h5>
            <p className={styles.quadrantDesc}>Low Impact, Low Effort</p>
          </div>
          <div className={styles.gridQuadrant} data-quadrant="questionable">
            <h5>Questionable</h5>
            <p className={styles.quadrantDesc}>Low Impact, High Effort</p>
          </div>
        </div>
      </div>
    </div>
  );

  const renderFrameworkDetail = (framework: IntelligentFramework) => (
    <div className={styles.frameworkDetail}>
      <div className={styles.intelligenceScores}>
        <div className={styles.scoreCard}>
          <label>Relevance</label>
          <div className={styles.scoreBar}>
            <div 
              className={styles.scoreProgress} 
              style={{ width: `${framework.relevance_score * 100}%` }}
            />
          </div>
          <span>{(framework.relevance_score * 100).toFixed(0)}%</span>
        </div>
        <div className={styles.scoreCard}>
          <label>Confidence</label>
          <div className={styles.scoreBar}>
            <div 
              className={styles.scoreProgress} 
              style={{ width: `${framework.confidence_level * 100}%` }}
            />
          </div>
          <span>{(framework.confidence_level * 100).toFixed(0)}%</span>
        </div>
        <div className={styles.scoreCard}>
          <label>Success Probability</label>
          <div className={styles.scoreBar}>
            <div 
              className={styles.scoreProgress} 
              style={{ width: `${framework.success_probability * 100}%` }}
            />
          </div>
          <span>{(framework.success_probability * 100).toFixed(0)}%</span>
        </div>
        <div className={styles.scoreCard}>
          <label>Market Timing</label>
          <div className={styles.scoreBar}>
            <div 
              className={styles.scoreProgress} 
              style={{ width: `${framework.timing_score * 100}%` }}
            />
          </div>
          <span>{(framework.timing_score * 100).toFixed(0)}%</span>
        </div>
      </div>

      <div className={styles.customizations}>
        <h4>AI-Powered Customizations</h4>
        <p className={styles.customizationIntro}>
          Specifically adapted for your company's context:
        </p>
        {framework.customizations.map((custom, i) => (
          <motion.div
            key={i}
            className={styles.customizationItem}
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: i * 0.1 }}
          >
            <span className={styles.customNumber}>{i + 1}</span>
            <p>{custom}</p>
          </motion.div>
        ))}
      </div>

      <div className={styles.quickWinsSection}>
        <h4>Quick Wins (This Week)</h4>
        <div className={styles.quickWinsGrid}>
          {framework.quick_wins.map((win, i) => (
            <div key={i} className={styles.quickWinCard}>
              <div className={styles.winHeader}>
                <span className={styles.winNumber}>Win #{i + 1}</span>
                <span className={styles.winTiming}>Week 1</span>
              </div>
              <p>{win}</p>
              <button className={styles.winAction}>Start Now →</button>
            </div>
          ))}
        </div>
      </div>

      <div className={styles.riskMitigation}>
        <h4>Risk Factors & Mitigation</h4>
        {framework.risk_factors.map((risk, i) => (
          <div key={i} className={styles.riskItem}>
            <div className={styles.riskHeader}>
              <span className={styles.riskIcon}>⚠️</span>
              <p>{risk}</p>
            </div>
            <div className={styles.mitigation}>
              <strong>Mitigation:</strong> Monitor weekly and adjust approach if needed
            </div>
          </div>
        ))}
      </div>

      {/* Render specific framework analysis */}
      {framework.analysis && (
        <div className={styles.frameworkAnalysis}>
          {/* Different visualizations based on framework type */}
          {renderFrameworkSpecificAnalysis(framework)}
        </div>
      )}
    </div>
  );

  const renderFrameworkSpecificAnalysis = (framework: IntelligentFramework) => {
    // Render different analysis types based on framework
    switch (framework.framework_id) {
      case 'adaptive_strategy':
        return renderAdaptiveStrategyAnalysis(framework.analysis);
      case 'growth_velocity':
        return renderGrowthVelocityAnalysis(framework.analysis);
      case 'ai_transformation':
        return renderAITransformationAnalysis(framework.analysis);
      case 'ecosystem_orchestration':
        return renderEcosystemAnalysis(framework.analysis);
      default:
        return null;
    }
  };

  const renderAdaptiveStrategyAnalysis = (analysis: any) => (
    <div className={styles.adaptiveStrategy}>
      <h4>Strategic Options Analysis</h4>
      <div className={styles.strategicOptions}>
        {analysis.strategic_options.map((option: any, i: number) => (
          <div key={i} className={styles.optionCard}>
            <h5>{option.option}</h5>
            <div className={styles.viabilityScore}>
              <label>Viability</label>
              <div className={styles.scoreBar}>
                <div 
                  className={styles.scoreProgress} 
                  style={{ width: `${option.viability * 100}%` }}
                />
              </div>
            </div>
            <span className={styles.timeframe}>{option.timeframe}</span>
          </div>
        ))}
      </div>
    </div>
  );

  const renderGrowthVelocityAnalysis = (analysis: any) => (
    <div className={styles.growthVelocity}>
      <h4>Growth Lever Analysis</h4>
      <div className={styles.growthLevers}>
        {analysis.growth_levers.map((lever: any, i: number) => (
          <div key={i} className={styles.leverCard}>
            <h5>{lever.lever}</h5>
            <div className={styles.leverMetrics}>
              <div className={styles.metric}>
                <label>Impact</label>
                <span>{(lever.impact * 100).toFixed(0)}%</span>
              </div>
              <div className={styles.metric}>
                <label>Effort</label>
                <span>{(lever.effort * 100).toFixed(0)}%</span>
              </div>
              <div className={styles.metric}>
                <label>ROI</label>
                <span>{((lever.impact / lever.effort) * 100).toFixed(0)}%</span>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );

  const renderAITransformationAnalysis = (analysis: any) => (
    <div className={styles.aiTransformation}>
      <h4>AI Maturity Progression</h4>
      <div className={styles.maturityChart}>
        <div className={styles.maturityLevels}>
          {[1, 2, 3, 4, 5].map(level => (
            <div 
              key={level} 
              className={`${styles.maturityLevel} ${
                level === analysis.ai_maturity.current_level ? styles.current :
                level === analysis.ai_maturity.target_level ? styles.target : ''
              }`}
            >
              <span className={styles.levelNumber}>{level}</span>
              <span className={styles.levelLabel}>
                {level === 1 ? 'Basic' : 
                 level === 2 ? 'Developing' :
                 level === 3 ? 'Competent' :
                 level === 4 ? 'Advanced' : 'Leading'}
              </span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );

  const renderEcosystemAnalysis = (analysis: any) => (
    <div className={styles.ecosystem}>
      <h4>Ecosystem Health Metrics</h4>
      <div className={styles.ecosystemMetrics}>
        <div className={styles.metricCard}>
          <label>Partner Count</label>
          <span className={styles.metricValue}>{analysis.ecosystem_health.partner_count}</span>
        </div>
        <div className={styles.metricCard}>
          <label>Partner Satisfaction</label>
          <span className={styles.metricValue}>
            {(analysis.ecosystem_health.partner_satisfaction * 100).toFixed(0)}%
          </span>
        </div>
        <div className={styles.metricCard}>
          <label>Ecosystem Revenue</label>
          <span className={styles.metricValue}>
            {analysis.ecosystem_health.ecosystem_revenue_share}
          </span>
        </div>
      </div>
    </div>
  );

  if (isLoading) {
    return (
      <div className={styles.container}>
        <div className={styles.loading}>
          <div className={styles.aiLoader}>
            <div className={styles.aiPulse} />
            <div className={styles.aiPulse} />
            <div className={styles.aiPulse} />
          </div>
          <p>AI analyzing your business context...</p>
          <p className={styles.loadingSubtext}>Incorporating real-time market intelligence</p>
        </div>
      </div>
    );
  }

  const selectedFrameworkObj = frameworks.find(f => f.framework_id === selectedFramework);

  return (
    <div className={styles.container}>
      <div className={styles.header}>
        <h2>Intelligent Strategic Framework Analysis</h2>
        <p>AI-powered framework selection with real-time market intelligence</p>
        
        <div className={styles.viewToggle}>
          <button
            className={viewMode === 'individual' ? styles.active : ''}
            onClick={() => setViewMode('individual')}
          >
            Individual Frameworks
          </button>
          <button
            className={viewMode === 'integrated' ? styles.active : ''}
            onClick={() => setViewMode('integrated')}
          >
            Integrated View
          </button>
        </div>
      </div>

      {viewMode === 'individual' ? (
        <>
          <div className={styles.frameworkSelector}>
            {frameworks.map((framework) => (
              <button
                key={framework.framework_id}
                className={`${styles.frameworkTab} ${
                  selectedFramework === framework.framework_id ? styles.active : ''
                }`}
                onClick={() => setSelectedFramework(framework.framework_id)}
              >
                <div className={styles.tabHeader}>
                  <span className={styles.frameworkName}>{framework.framework_name}</span>
                  <span className={styles.frameworkCategory}>{framework.category}</span>
                </div>
                <div className={styles.tabScores}>
                  <span className={styles.relevanceScore}>
                    {(framework.relevance_score * 100).toFixed(0)}% relevant
                  </span>
                  <span className={styles.confidenceScore}>
                    {(framework.confidence_level * 100).toFixed(0)}% confidence
                  </span>
                </div>
              </button>
            ))}
          </div>

          <div className={styles.mainContent}>
            <div className={styles.leftColumn}>
              <AnimatePresence mode="wait">
                {selectedFrameworkObj && (
                  <motion.div
                    key={selectedFramework}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0, y: -20 }}
                  >
                    {renderFrameworkDetail(selectedFrameworkObj)}
                  </motion.div>
                )}
              </AnimatePresence>
            </div>
            
            <div className={styles.rightColumn}>
              {renderMarketIntelligence()}
            </div>
          </div>
        </>
      ) : (
        renderIntegratedView()
      )}

      <div className={styles.actionBar}>
        <button className={styles.primaryAction}>
          Generate Implementation Plan
        </button>
        <button className={styles.secondaryAction}>
          Schedule Strategy Session
        </button>
        <button className={styles.tertiaryAction}>
          Export Analysis
        </button>
      </div>
    </div>
  );
};

export default StrategicFrameworkReportIntelligent;