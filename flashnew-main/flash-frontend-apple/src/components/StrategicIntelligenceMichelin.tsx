import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Icon } from '../design-system/components';
import { FrameworkImplementation } from './FrameworkImplementation';
import { MichelinLLMAnalysis } from './MichelinLLMAnalysis';
import { MichelinFrameworkAnalysisSimple } from './MichelinFrameworkAnalysisSimple';
import useAssessmentStore from '../store/assessmentStore';
import styles from './StrategicIntelligenceMichelin.module.scss';

interface FrameworkRecommendation {
  framework_id: string;
  framework_name: string;
  score: number;
  category: string;
  complexity: string;
  time_to_implement: string;
  description: string;
  why_recommended: string;
  key_benefits: string[];
  position?: string;
  key_insight?: string;
  urgency?: 'high' | 'medium' | 'low';
}

interface CompetitorData {
  name: string;
  fundingStage: string;
  marketShare: number;
  recentMoves: string[];
  strength: 'strong' | 'moderate' | 'weak';
}

interface StrategicOption {
  id: string;
  title: string;
  description: string;
  successRate: number;
  timeframe: string;
  requiredResources: string[];
  risks: string[];
  basedOn: string; // Which successful pattern
}

interface RoadmapItem {
  phase: '30-day' | '60-day' | '90-day';
  title: string;
  actions: string[];
  metrics: string[];
  resources: string[];
  dependencies: string[];
}

const FRAMEWORK_METADATA = {
  lean_startup: {
    icon: 'arrow.triangle.2.circlepath',
    gradient: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'
  },
  bcg_matrix: {
    icon: 'square.grid.2x2',
    gradient: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)'
  },
  porters_five_forces: {
    icon: 'shield.lefthalf.filled',
    gradient: 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)'
  },
  swot_analysis: {
    icon: 'square.split.2x2',
    gradient: 'linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)'
  },
  value_chain: {
    icon: 'link',
    gradient: 'linear-gradient(135deg, #fa709a 0%, #fee140 100%)'
  },
  business_model_canvas: {
    icon: 'rectangle.grid.3x2',
    gradient: 'linear-gradient(135deg, #30cfd0 0%, #330867 100%)'
  },
  blue_ocean_strategy: {
    icon: 'water.waves',
    gradient: 'linear-gradient(135deg, #a8edea 0%, #fed6e3 100%)'
  },
  ansoff_matrix: {
    icon: 'arrow.up.right.square',
    gradient: 'linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%)'
  },
  pestel_analysis: {
    icon: 'globe',
    gradient: 'linear-gradient(135deg, #a1c4fd 0%, #c2e9fb 100%)'
  },
  jobs_to_be_done: {
    icon: 'person.fill.checkmark',
    gradient: 'linear-gradient(135deg, #d299c2 0%, #fef9d7 100%)'
  }
};

export const StrategicIntelligenceMichelin: React.FC = () => {
  const [viewMode, setViewMode] = useState<'where-now' | 'where-go' | 'how-get-there'>('where-now');
  const [recommendations, setRecommendations] = useState<FrameworkRecommendation[]>([]);
  const [competitors, setCompetitors] = useState<CompetitorData[]>([]);
  const [strategicOptions, setStrategicOptions] = useState<StrategicOption[]>([]);
  const [roadmap, setRoadmap] = useState<RoadmapItem[]>([]);
  const [selectedFramework, setSelectedFramework] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [analysisMode, setAnalysisMode] = useState<'demo' | 'llm' | 'simple'>('simple');
  
  const assessmentData = useAssessmentStore(state => state.data);
  const results = useAssessmentStore(state => state.results);

  useEffect(() => {
    loadStrategicData();
  }, []);

  const loadStrategicData = async () => {
    setIsLoading(true);
    try {
      await Promise.all([
        loadFrameworkRecommendations(),
        loadCompetitorData(),
        loadStrategicOptions(),
        loadRoadmap()
      ]);
    } catch (error) {
      console.error('Error loading strategic data:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const loadFrameworkRecommendations = async () => {
    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 500));
    
    const mockRecommendations: FrameworkRecommendation[] = [
      {
        framework_id: 'bcg_matrix',
        framework_name: 'BCG Growth-Share Matrix',
        score: 0.95,
        category: 'Strategy',
        complexity: 'Intermediate',
        time_to_implement: '1-2 hours',
        description: 'Position your product portfolio based on market growth and share',
        why_recommended: 'Your high growth market (18% YoY) but low market share (3.2%) indicates critical strategic decisions needed',
        key_benefits: ['Clear strategic position', 'Investment prioritization', 'Portfolio decisions'],
        position: 'Question Mark',
        key_insight: 'High growth opportunity but requires significant investment to capture market share',
        urgency: 'high'
      },
      {
        framework_id: 'porters_five_forces',
        framework_name: "Porter's Five Forces",
        score: 0.88,
        category: 'Strategy',
        complexity: 'Advanced',
        time_to_implement: '2-3 hours',
        description: 'Analyze competitive forces shaping your industry',
        why_recommended: 'Multiple well-funded competitors and low barriers to entry threaten your position',
        key_benefits: ['Industry attractiveness', 'Competitive dynamics', 'Strategic positioning'],
        position: 'Moderate Attractiveness',
        key_insight: 'High competitive rivalry (4.2/5) suggests need for strong differentiation',
        urgency: 'high'
      }
    ];
    
    setRecommendations(mockRecommendations);
  };

  const loadCompetitorData = async () => {
    // Simulate loading competitor data
    await new Promise(resolve => setTimeout(resolve, 600));
    
    const mockCompetitors: CompetitorData[] = [
      {
        name: 'TechCorp Alpha',
        fundingStage: 'Series B',
        marketShare: 15.3,
        recentMoves: ['Raised $50M Series B', 'Launched enterprise product', 'Acquired DataSync Inc'],
        strength: 'strong'
      },
      {
        name: 'StartupBeta',
        fundingStage: 'Series A',
        marketShare: 8.7,
        recentMoves: ['Pivoted to B2B model', 'Partnership with Microsoft', 'Expanded to EU market'],
        strength: 'moderate'
      },
      {
        name: 'InnovateCo',
        fundingStage: 'Seed',
        marketShare: 3.1,
        recentMoves: ['MVP launch', 'Angel round closed', 'Hiring VP Sales'],
        strength: 'weak'
      }
    ];
    
    setCompetitors(mockCompetitors);
  };

  const loadStrategicOptions = async () => {
    // Simulate loading strategic options based on pattern analysis
    await new Promise(resolve => setTimeout(resolve, 700));
    
    const mockOptions: StrategicOption[] = [
      {
        id: 'vertical-focus',
        title: 'Vertical Market Focus',
        description: 'Narrow focus to healthcare vertical where early traction exists',
        successRate: 68,
        timeframe: '6-9 months',
        requiredResources: ['Domain expert hire', '$500K marketing budget', 'Product customization'],
        risks: ['Market size limitation', 'Longer sales cycles', 'Regulatory complexity'],
        basedOn: 'Pattern: B2B SaaS Vertical Success (n=47)'
      },
      {
        id: 'platform-play',
        title: 'Platform Ecosystem Strategy',
        description: 'Build API-first platform to enable third-party integrations',
        successRate: 45,
        timeframe: '12-18 months',
        requiredResources: ['Platform team (5 engineers)', '$2M development budget', 'Developer relations'],
        risks: ['High technical complexity', 'Slow initial adoption', 'Platform governance'],
        basedOn: 'Pattern: Platform Evolution (n=23)'
      },
      {
        id: 'geographic-expansion',
        title: 'Geographic Expansion',
        description: 'Expand to underserved APAC markets with localized approach',
        successRate: 52,
        timeframe: '9-12 months',
        requiredResources: ['Local team setup', '$1M expansion budget', 'Legal/compliance framework'],
        risks: ['Cultural barriers', 'Operational complexity', 'Currency fluctuations'],
        basedOn: 'Pattern: International Expansion Success (n=31)'
      }
    ];
    
    setStrategicOptions(mockOptions);
  };

  const loadRoadmap = async () => {
    // Simulate loading implementation roadmap
    await new Promise(resolve => setTimeout(resolve, 800));
    
    const mockRoadmap: RoadmapItem[] = [
      {
        phase: '30-day',
        title: 'Foundation & Quick Wins',
        actions: [
          'Hire VP Sales with healthcare experience',
          'Launch customer discovery interviews (n=50)',
          'Implement basic usage analytics',
          'Create healthcare-specific landing page'
        ],
        metrics: [
          '50 customer interviews completed',
          'VP Sales onboarded',
          'Analytics dashboard live',
          '20% increase in healthcare leads'
        ],
        resources: ['$150K budget', '2 engineers', '1 designer', 'CEO time (50%)'],
        dependencies: ['Board approval for VP hire', 'Engineering capacity']
      },
      {
        phase: '60-day',
        title: 'Market Validation & Product Fit',
        actions: [
          'Launch healthcare pilot program (10 customers)',
          'Build 3 healthcare-specific features',
          'Establish pricing model for vertical',
          'Create sales collateral and case studies'
        ],
        metrics: [
          '10 pilot customers onboarded',
          'NPS score >50',
          '3 features shipped',
          '2 case studies published'
        ],
        resources: ['$300K budget', '4 engineers', '1 product manager', 'Sales team (3)'],
        dependencies: ['Pilot customer commitments', 'Feature specifications complete']
      },
      {
        phase: '90-day',
        title: 'Scale & Optimize',
        actions: [
          'Scale to 50 healthcare customers',
          'Launch partner program with health systems',
          'Implement customer success function',
          'Raise Series A focused on vertical'
        ],
        metrics: [
          '$500K ARR from healthcare',
          '5 health system partnerships',
          'Churn <5% monthly',
          'Series A term sheet'
        ],
        resources: ['$500K budget', 'Full team (15 people)', 'Board support', 'Investor intros'],
        dependencies: ['Product-market fit validated', 'Scalable sales process']
      }
    ];
    
    setRoadmap(mockRoadmap);
  };

  const getScoreInterpretation = () => {
    if (!results) return { overall: 'Unknown', verdict: 'Insufficient data' };
    
    const prob = results.successProbability || 0;
    const scores = results.scores || { capital: 0, advantage: 0, market: 0, people: 0 };
    
    // Identify weakest dimension
    const dimensions = [
      { name: 'Capital', score: scores.capital },
      { name: 'Advantage', score: scores.advantage },
      { name: 'Market', score: scores.market },
      { name: 'People', score: scores.people }
    ];
    
    const weakest = dimensions.reduce((min, dim) => dim.score < min.score ? dim : min);
    const strongest = dimensions.reduce((max, dim) => dim.score > max.score ? dim : max);
    
    return {
      overall: `${Math.round(prob * 100)}% Success Probability`,
      verdict: prob >= 0.7 ? 'Strong Position' : prob >= 0.5 ? 'Developing Position' : 'Challenged Position',
      weakest: weakest.name,
      strongest: strongest.name,
      interpretation: `Your ${strongest.name} strength (${Math.round(strongest.score * 100)}%) is offset by ${weakest.name} weakness (${Math.round(weakest.score * 100)}%)`
    };
  };

  const getCompetitivePosition = () => {
    // Calculate relative position based on scores
    const marketScore = results?.scores?.market || 0;
    const advantageScore = results?.scores?.advantage || 0;
    
    if (marketScore > 0.7 && advantageScore > 0.7) return 'Market Leader';
    if (marketScore > 0.5 && advantageScore > 0.5) return 'Challenger';
    if (marketScore > 0.3 || advantageScore > 0.5) return 'Niche Player';
    return 'Follower';
  };

  const renderWhereAreWeNow = () => (
    <motion.div
      key="where-now"
      className={styles.tabContent}
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
    >
      {/* Situation Summary */}
      <div className={styles.situationSummary}>
        <h3>Current Strategic Position</h3>
        <div className={styles.positionGrid}>
          <div className={styles.positionCard}>
            <Icon name="gauge" size={32} />
            <h4>{getScoreInterpretation().overall}</h4>
            <p>{getScoreInterpretation().verdict}</p>
            <span className={styles.detail}>{getScoreInterpretation().interpretation}</span>
          </div>
          
          <div className={styles.positionCard}>
            <Icon name="person.3.fill" size={32} />
            <h4>Competitive Position</h4>
            <p>{getCompetitivePosition()}</p>
            <span className={styles.detail}>Among {competitors.length + 1} identified competitors</span>
          </div>
          
          <div className={styles.positionCard}>
            <Icon name="chart.line.uptrend.xyaxis" size={32} />
            <h4>Market Dynamics</h4>
            <p>High Growth, Low Share</p>
            <span className={styles.detail}>18% market growth, 3.2% current share</span>
          </div>
        </div>
      </div>

      {/* Competitive Landscape */}
      <div className={styles.competitiveLandscape}>
        <h3>Competitive Intelligence</h3>
        <div className={styles.competitorGrid}>
          {competitors.map((competitor, index) => (
            <motion.div
              key={competitor.name}
              className={styles.competitorCard}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: index * 0.1 }}
            >
              <div className={styles.competitorHeader}>
                <h4>{competitor.name}</h4>
                <span className={`${styles.strengthBadge} ${styles[competitor.strength]}`}>
                  {competitor.strength} threat
                </span>
              </div>
              
              <div className={styles.competitorStats}>
                <div className={styles.stat}>
                  <span className={styles.statLabel}>Stage</span>
                  <span className={styles.statValue}>{competitor.fundingStage}</span>
                </div>
                <div className={styles.stat}>
                  <span className={styles.statLabel}>Market Share</span>
                  <span className={styles.statValue}>{competitor.marketShare}%</span>
                </div>
              </div>
              
              <div className={styles.recentMoves}>
                <h5>Recent Moves</h5>
                <ul>
                  {competitor.recentMoves.map((move, i) => (
                    <li key={i}>{move}</li>
                  ))}
                </ul>
              </div>
            </motion.div>
          ))}
        </div>
      </div>

      {/* Framework Analysis Summary */}
      <div className={styles.frameworkSummary}>
        <h3>Strategic Framework Analysis</h3>
        <div className={styles.frameworkGrid}>
          {recommendations.slice(0, 3).map((framework, index) => (
            <motion.div
              key={framework.framework_id}
              className={styles.frameworkMini}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.1 }}
              onClick={() => setSelectedFramework(framework.framework_id)}
            >
              <div 
                className={styles.frameworkIcon}
                style={{ background: FRAMEWORK_METADATA[framework.framework_id]?.gradient }}
              >
                <Icon name={FRAMEWORK_METADATA[framework.framework_id]?.icon || 'square.grid.2x2'} size={24} />
              </div>
              <h4>{framework.framework_name}</h4>
              <p className={styles.position}>Position: <strong>{framework.position}</strong></p>
              <p className={styles.insight}>{framework.key_insight}</p>
              <div className={`${styles.urgency} ${styles[framework.urgency || 'medium']}`}>
                {framework.urgency} priority
              </div>
            </motion.div>
          ))}
        </div>
      </div>
    </motion.div>
  );

  const renderWhereToGo = () => (
    <motion.div
      key="where-go"
      className={styles.tabContent}
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
    >
      <div className={styles.strategicOptions}>
        <h3>Strategic Options Analysis</h3>
        <p className={styles.subtitle}>Based on pattern analysis of similar startups that succeeded</p>
        
        <div className={styles.optionsGrid}>
          {strategicOptions.map((option, index) => (
            <motion.div
              key={option.id}
              className={styles.optionCard}
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ delay: index * 0.15 }}
            >
              <div className={styles.optionHeader}>
                <h4>{option.title}</h4>
                <div className={styles.successRate}>
                  <span className={styles.rateValue}>{option.successRate}%</span>
                  <span className={styles.rateLabel}>Success Rate</span>
                </div>
              </div>
              
              <p className={styles.optionDescription}>{option.description}</p>
              
              <div className={styles.optionMeta}>
                <Icon name="clock" size={16} />
                <span>{option.timeframe}</span>
              </div>
              
              <div className={styles.optionDetails}>
                <div className={styles.detailSection}>
                  <h5>Required Resources</h5>
                  <ul>
                    {option.requiredResources.map((resource, i) => (
                      <li key={i}>{resource}</li>
                    ))}
                  </ul>
                </div>
                
                <div className={styles.detailSection}>
                  <h5>Key Risks</h5>
                  <ul>
                    {option.risks.map((risk, i) => (
                      <li key={i}>{risk}</li>
                    ))}
                  </ul>
                </div>
              </div>
              
              <div className={styles.patternBasis}>
                <Icon name="chart.bar.fill" size={14} />
                <span>{option.basedOn}</span>
              </div>
            </motion.div>
          ))}
        </div>
      </div>

      {/* Decision Matrix */}
      <div className={styles.decisionMatrix}>
        <h3>Strategic Decision Matrix</h3>
        <div className={styles.matrixContainer}>
          <div className={styles.matrixHeader}>
            <div></div>
            <div>Success Rate</div>
            <div>Time to Value</div>
            <div>Resource Intensity</div>
            <div>Risk Level</div>
          </div>
          {strategicOptions.map(option => (
            <div key={option.id} className={styles.matrixRow}>
              <div className={styles.optionName}>{option.title}</div>
              <div className={styles.matrixCell}>
                <div 
                  className={styles.matrixBar} 
                  style={{ width: `${option.successRate}%`, backgroundColor: getSuccessColor(option.successRate) }}
                />
              </div>
              <div className={styles.matrixCell}>{option.timeframe}</div>
              <div className={styles.matrixCell}>
                <span className={styles.resourceLevel}>
                  {option.requiredResources.length > 4 ? 'High' : option.requiredResources.length > 2 ? 'Medium' : 'Low'}
                </span>
              </div>
              <div className={styles.matrixCell}>
                <span className={styles.riskLevel}>
                  {option.risks.length > 3 ? 'High' : option.risks.length > 1 ? 'Medium' : 'Low'}
                </span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </motion.div>
  );

  const renderHowToGetThere = () => (
    <motion.div
      key="how-get-there"
      className={styles.tabContent}
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
    >
      <div className={styles.implementationRoadmap}>
        <h3>90-Day Implementation Roadmap</h3>
        <p className={styles.subtitle}>Actionable steps based on vertical focus strategy (highest success rate)</p>
        
        <div className={styles.roadmapTimeline}>
          {roadmap.map((phase, index) => (
            <motion.div
              key={phase.phase}
              className={styles.phaseCard}
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.2 }}
            >
              <div className={styles.phaseHeader}>
                <div className={styles.phaseTime}>{phase.phase}</div>
                <h4>{phase.title}</h4>
              </div>
              
              <div className={styles.phaseContent}>
                <div className={styles.phaseSection}>
                  <h5>Key Actions</h5>
                  <ul className={styles.actionList}>
                    {phase.actions.map((action, i) => (
                      <li key={i}>
                        <Icon name="checkmark.circle" size={16} />
                        <span>{action}</span>
                      </li>
                    ))}
                  </ul>
                </div>
                
                <div className={styles.phaseGrid}>
                  <div className={styles.phaseSection}>
                    <h5>Success Metrics</h5>
                    <ul className={styles.metricList}>
                      {phase.metrics.map((metric, i) => (
                        <li key={i}>{metric}</li>
                      ))}
                    </ul>
                  </div>
                  
                  <div className={styles.phaseSection}>
                    <h5>Resources Needed</h5>
                    <ul className={styles.resourceList}>
                      {phase.resources.map((resource, i) => (
                        <li key={i}>{resource}</li>
                      ))}
                    </ul>
                  </div>
                </div>
                
                {phase.dependencies.length > 0 && (
                  <div className={styles.dependencies}>
                    <h5>Dependencies</h5>
                    <div className={styles.dependencyList}>
                      {phase.dependencies.map((dep, i) => (
                        <span key={i} className={styles.dependency}>
                          <Icon name="link" size={12} />
                          {dep}
                        </span>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            </motion.div>
          ))}
        </div>
      </div>

      {/* Critical Success Factors */}
      <div className={styles.successFactors}>
        <h3>Critical Success Factors</h3>
        <div className={styles.factorGrid}>
          <div className={styles.factorCard}>
            <Icon name="person.fill.checkmark" size={32} />
            <h4>Healthcare Domain Expert</h4>
            <p>VP Sales hire with 10+ years healthcare experience is critical for credibility</p>
          </div>
          <div className={styles.factorCard}>
            <Icon name="speedometer" size={32} />
            <h4>Speed of Execution</h4>
            <p>First-mover advantage in healthcare vertical expires in 6-9 months</p>
          </div>
          <div className={styles.factorCard}>
            <Icon name="chart.line.uptrend.xyaxis" size={32} />
            <h4>Metrics Focus</h4>
            <p>Weekly tracking of pilot NPS and usage metrics for rapid iteration</p>
          </div>
          <div className={styles.factorCard}>
            <Icon name="dollarsign.circle" size={32} />
            <h4>Capital Efficiency</h4>
            <p>Achieve $500K ARR before Series A to maximize valuation</p>
          </div>
        </div>
      </div>
    </motion.div>
  );

  const getSuccessColor = (rate: number) => {
    if (rate >= 70) return '#10b981';
    if (rate >= 50) return '#f59e0b';
    return '#ef4444';
  };

  // Use LLM analysis if enabled
  if (analysisMode === 'llm') {
    return <MichelinLLMAnalysis />;
  }

  // Use simplified framework analysis without charts
  if (analysisMode === 'simple') {
    return <MichelinFrameworkAnalysisSimple />;
  }

  return (
    <div className={styles.container}>
      <div className={styles.header}>
        <div className={styles.titleSection}>
          <h2>Strategic Intelligence Report</h2>
          <p className={styles.subtitle}>
            Michelin-style strategic analysis for {assessmentData?.companyInfo?.companyName || 'your startup'}
          </p>
        </div>
        
        <div className={styles.controls}>
          <button
            className={`${styles.viewToggle} ${viewMode === 'where-now' ? styles.active : ''}`}
            onClick={() => setViewMode('where-now')}
          >
            <Icon name="location.circle" size={16} />
            Where Are We Now?
          </button>
          <button
            className={`${styles.viewToggle} ${viewMode === 'where-go' ? styles.active : ''}`}
            onClick={() => setViewMode('where-go')}
          >
            <Icon name="target" size={16} />
            Where Should We Go?
          </button>
          <button
            className={`${styles.viewToggle} ${viewMode === 'how-get-there' ? styles.active : ''}`}
            onClick={() => setViewMode('how-get-there')}
          >
            <Icon name="map" size={16} />
            How to Get There?
          </button>
        </div>
      </div>

      {isLoading ? (
        <div className={styles.loading}>
          <Icon name="arrow.clockwise" size={32} className={styles.spinner} />
          <p>Generating strategic intelligence report...</p>
        </div>
      ) : (
        <AnimatePresence mode="wait">
          {viewMode === 'where-now' && renderWhereAreWeNow()}
          {viewMode === 'where-go' && renderWhereToGo()}
          {viewMode === 'how-get-there' && renderHowToGetThere()}
        </AnimatePresence>
      )}

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
              initial={{ scale: 0.9, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              exit={{ scale: 0.9, opacity: 0 }}
              onClick={(e) => e.stopPropagation()}
            >
              <FrameworkImplementation 
                frameworkId={selectedFramework}
                onClose={() => setSelectedFramework(null)}
              />
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};

export default StrategicIntelligenceMichelin;