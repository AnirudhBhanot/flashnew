// Strategic Framework Database - 500+ Business Frameworks
// PhD-level comprehensive framework repository

export enum FrameworkCategory {
  STRATEGY = 'Strategy',
  INNOVATION = 'Innovation',
  GROWTH = 'Growth',
  FINANCIAL = 'Financial',
  OPERATIONAL = 'Operations',
  MARKETING = 'Marketing',
  PRODUCT = 'Product',
  LEADERSHIP = 'Leadership',
  ORGANIZATIONAL = 'Organizational',
  TRANSFORMATION = 'Transformation',
  COMPETITIVE = 'Competitive Analysis',
  CUSTOMER = 'Customer Analysis',
  RISK = 'Risk Management',
  TECHNOLOGY = 'Technology',
  SUSTAINABILITY = 'Sustainability'
}

export enum VisualizationType {
  MATRIX_2X2 = 'matrix_2x2',
  MATRIX_3X3 = 'matrix_3x3',
  CANVAS = 'canvas',
  PYRAMID = 'pyramid',
  FUNNEL = 'funnel',
  SPIDER = 'spider',
  FLOWCHART = 'flowchart',
  TIMELINE = 'timeline',
  QUADRANT = 'quadrant',
  HEATMAP = 'heatmap',
  FORCE_FIELD = 'force_field',
  VALUE_CHAIN = 'value_chain',
  ECOSYSTEM_MAP = 'ecosystem_map',
  JOURNEY_MAP = 'journey_map',
  SCORECARD = 'scorecard'
}

export interface FrameworkOrigin {
  author: string;
  year: number;
  source: string;
  academicPaper?: string;
  company?: string; // McKinsey, BCG, etc.
}

export interface FrameworkApplicability {
  stages: string[]; // ['pre_seed', 'seed', 'series_a', etc.]
  industries: string[]; // ['saas', 'marketplace', 'fintech', etc.]
  companySize: {
    min: number; // employees
    max: number;
  };
  situations: string[]; // ['growth', 'turnaround', 'pivot', 'scale', etc.]
  geographies?: string[]; // ['global', 'us', 'europe', 'asia', etc.]
}

export interface MetricRequirement {
  flashField: string; // Maps to FLASH 45 features
  alternativeFields?: string[]; // Fallback fields
  importance: 'required' | 'recommended' | 'optional';
  description: string;
}

export interface CalculationStep {
  id: string;
  name: string;
  formula: string; // Mathematical formula or logic
  inputs: string[]; // References to metrics or previous steps
  output: string; // Variable name for result
  unit?: string; // %, $, score, etc.
}

export interface InterpretationRule {
  condition: string; // e.g., "score > 7"
  position: string; // e.g., "Market Leader"
  description: string;
  implications: string[];
  recommendations: string[];
}

export interface VisualizationConfig {
  type: VisualizationType;
  axes?: {
    x: { label: string; min: number; max: number; };
    y: { label: string; min: number; max: number; };
    z?: { label: string; min: number; max: number; };
  };
  segments?: Array<{
    id: string;
    label: string;
    description: string;
    color?: string;
  }>;
  customConfig?: any; // Framework-specific visualization data
}

export interface CaseExample {
  company: string;
  industry: string;
  stage: string;
  situation: string;
  application: string;
  outcome: string;
  keyLearning: string;
}

export interface RelatedFramework {
  id: string;
  relationship: 'complementary' | 'alternative' | 'prerequisite' | 'advanced';
  description: string;
}

export interface Framework {
  id: string;
  name: string;
  category: FrameworkCategory;
  subcategory?: string;
  description: string;
  purpose: string;
  
  origin: FrameworkOrigin;
  applicability: FrameworkApplicability;
  
  methodology: {
    overview: string;
    requiredMetrics: MetricRequirement[];
    calculationSteps: CalculationStep[];
    interpretationRules: InterpretationRule[];
    timeToComplete: string; // "5 minutes", "30 minutes", etc.
  };
  
  visualization: VisualizationConfig;
  
  insights: {
    whenMostPowerful: string;
    limitations: string[];
    commonMisuses: string[];
    bestPractices: string[];
    academicValidation?: string;
  };
  
  implementation: {
    prerequisites: string[];
    steps: string[];
    deliverables: string[];
    typicalDuration: string;
    requiredResources: string[];
  };
  
  relatedFrameworks: RelatedFramework[];
  cases: CaseExample[];
  
  metadata: {
    popularity: number; // 1-10
    complexity: 'basic' | 'intermediate' | 'advanced' | 'expert';
    evidenceStrength: 'theoretical' | 'empirical' | 'proven';
    lastUpdated: Date;
    tags: string[];
  };
}

// Core Frameworks Collection (we'll expand to 500+)
export const frameworksDatabase: Framework[] = [
  {
    id: 'bcg_growth_share_matrix',
    name: 'BCG Growth-Share Matrix',
    category: FrameworkCategory.STRATEGY,
    subcategory: 'Portfolio Analysis',
    description: 'Analyzes business units or products based on market growth and relative market share',
    purpose: 'Determine resource allocation and strategic direction for different business units',
    
    origin: {
      author: 'Bruce Henderson',
      year: 1970,
      source: 'Boston Consulting Group',
      company: 'BCG'
    },
    
    applicability: {
      stages: ['seed', 'series_a', 'series_b', 'growth', 'mature'],
      industries: ['all'],
      companySize: { min: 10, max: 100000 },
      situations: ['portfolio_management', 'resource_allocation', 'strategic_planning']
    },
    
    methodology: {
      overview: 'Plot business units on a 2x2 matrix based on relative market share (x-axis) and market growth rate (y-axis)',
      requiredMetrics: [
        {
          flashField: 'market_growth_rate_percent',
          importance: 'required',
          description: 'Annual growth rate of the market'
        },
        {
          flashField: 'revenue_growth_rate_percent',
          alternativeFields: ['annual_revenue_run_rate'],
          importance: 'required',
          description: 'Company revenue for market share calculation'
        },
        {
          flashField: 'tam_size_usd',
          alternativeFields: ['sam_size_usd'],
          importance: 'recommended',
          description: 'Total market size for share calculation'
        }
      ],
      calculationSteps: [
        {
          id: 'market_share',
          name: 'Calculate Relative Market Share',
          formula: '(company_revenue / market_leader_revenue) * 100',
          inputs: ['annual_revenue_run_rate', 'competitor_data'],
          output: 'relative_market_share',
          unit: '%'
        },
        {
          id: 'position',
          name: 'Determine Matrix Position',
          formula: 'IF(market_share > 50 AND growth > 10, "Star", IF(market_share > 50 AND growth <= 10, "Cash Cow", IF(market_share <= 50 AND growth > 10, "Question Mark", "Dog")))',
          inputs: ['relative_market_share', 'market_growth_rate_percent'],
          output: 'bcg_position',
          unit: 'category'
        }
      ],
      interpretationRules: [
        {
          condition: 'bcg_position === "Star"',
          position: 'Star',
          description: 'High growth market with dominant position',
          implications: [
            'Requires heavy investment to maintain position',
            'Future cash cow as market matures',
            'Focus on maintaining market leadership'
          ],
          recommendations: [
            'Invest aggressively in growth',
            'Defend market position',
            'Build competitive moats'
          ]
        },
        {
          condition: 'bcg_position === "Question Mark"',
          position: 'Question Mark',
          description: 'High growth market but weak position',
          implications: [
            'Requires investment decision',
            'High risk, high reward',
            'Resource intensive'
          ],
          recommendations: [
            'Decide: invest heavily or divest',
            'Focus on specific market segments',
            'Build partnerships for quick growth'
          ]
        }
      ],
      timeToComplete: '15 minutes'
    },
    
    visualization: {
      type: VisualizationType.MATRIX_2X2,
      axes: {
        x: { label: 'Relative Market Share', min: 0, max: 10 },
        y: { label: 'Market Growth Rate (%)', min: -5, max: 30 }
      },
      segments: [
        { id: 'star', label: 'Star', description: 'High Growth, High Share', color: '#FFD700' },
        { id: 'question_mark', label: 'Question Mark', description: 'High Growth, Low Share', color: '#FF6B6B' },
        { id: 'cash_cow', label: 'Cash Cow', description: 'Low Growth, High Share', color: '#4ECDC4' },
        { id: 'dog', label: 'Dog', description: 'Low Growth, Low Share', color: '#95A5A6' }
      ]
    },
    
    insights: {
      whenMostPowerful: 'Multi-product companies deciding resource allocation',
      limitations: [
        'Assumes market share correlates with profitability',
        'Ignores synergies between units',
        'Static view of dynamic markets'
      ],
      commonMisuses: [
        'Using for single-product startups',
        'Ignoring industry-specific factors',
        'Over-simplifying complex markets'
      ],
      bestPractices: [
        'Combine with other strategic tools',
        'Consider market definition carefully',
        'Update positions regularly'
      ],
      academicValidation: 'Widely studied but criticized for oversimplification (Day, 1977)'
    },
    
    implementation: {
      prerequisites: [
        'Clear market definition',
        'Competitor revenue data',
        'Market growth statistics'
      ],
      steps: [
        'Define market boundaries',
        'Gather market and competitor data',
        'Calculate positions',
        'Plot on matrix',
        'Develop strategic recommendations'
      ],
      deliverables: [
        'BCG matrix visualization',
        'Strategic recommendations by unit',
        'Resource allocation plan'
      ],
      typicalDuration: '1-2 weeks',
      requiredResources: ['Market research', 'Financial data', 'Strategic planning team']
    },
    
    relatedFrameworks: [
      {
        id: 'ge_mckinsey_matrix',
        relationship: 'alternative',
        description: 'More nuanced with 9 cells instead of 4'
      },
      {
        id: 'ansoff_matrix',
        relationship: 'complementary',
        description: 'Helps determine growth strategy for each position'
      }
    ],
    
    cases: [
      {
        company: 'Apple',
        industry: 'Technology',
        stage: 'Mature',
        situation: 'iPhone as Cash Cow, Apple Watch as Question Mark',
        application: 'Resource allocation between product lines',
        outcome: 'Continued iPhone investment while building Watch ecosystem',
        keyLearning: 'Cash cows can fund question marks'
      }
    ],
    
    metadata: {
      popularity: 9,
      complexity: 'intermediate',
      evidenceStrength: 'proven',
      lastUpdated: new Date('2024-01-01'),
      tags: ['portfolio', 'strategy', 'classic', 'resource-allocation']
    }
  },
  
  // Porter's Five Forces
  {
    id: 'porters_five_forces',
    name: "Porter's Five Forces",
    category: FrameworkCategory.COMPETITIVE,
    description: 'Analyzes competitive intensity and attractiveness of an industry',
    purpose: 'Understand industry structure and competitive dynamics',
    
    origin: {
      author: 'Michael Porter',
      year: 1979,
      source: 'Harvard Business Review',
      academicPaper: 'How Competitive Forces Shape Strategy'
    },
    
    applicability: {
      stages: ['all'],
      industries: ['all'],
      companySize: { min: 1, max: 1000000 },
      situations: ['market_entry', 'strategic_planning', 'competitive_analysis']
    },
    
    methodology: {
      overview: 'Evaluate five competitive forces that shape industry competition',
      requiredMetrics: [
        {
          flashField: 'competition_intensity',
          importance: 'required',
          description: 'Direct competitive rivalry'
        },
        {
          flashField: 'switching_cost_score',
          importance: 'required',
          description: 'Customer switching costs'
        },
        {
          flashField: 'regulatory_advantage_present',
          importance: 'recommended',
          description: 'Barriers to entry'
        }
      ],
      calculationSteps: [
        {
          id: 'competitive_rivalry',
          name: 'Assess Competitive Rivalry',
          formula: 'competition_intensity * (1 + (competitors_count / 10))',
          inputs: ['competition_intensity', 'competitors_named_count'],
          output: 'rivalry_score',
          unit: 'score'
        }
      ],
      interpretationRules: [
        {
          condition: 'average_force > 7',
          position: 'Highly Challenging Industry',
          description: 'Industry faces intense pressure on all fronts',
          implications: ['Low profitability potential', 'Need for strong differentiation'],
          recommendations: ['Consider niche positioning', 'Build switching costs']
        }
      ],
      timeToComplete: '30 minutes'
    },
    
    visualization: {
      type: VisualizationType.SPIDER,
      customConfig: {
        forces: ['Competitive Rivalry', 'Buyer Power', 'Supplier Power', 'Threat of Substitutes', 'Threat of New Entry']
      }
    },
    
    insights: {
      whenMostPowerful: 'Evaluating new market entry or major strategic shifts',
      limitations: ['Static analysis', 'Ignores complementors', 'Less relevant for platform businesses'],
      commonMisuses: ['Focusing on forces in isolation', 'Ignoring industry evolution'],
      bestPractices: ['Update regularly', 'Consider sixth force (complementors)', 'Combine with value chain analysis']
    },
    
    implementation: {
      prerequisites: ['Industry knowledge', 'Competitor analysis', 'Supply chain understanding'],
      steps: ['Map industry players', 'Score each force', 'Identify key pressure points', 'Develop mitigation strategies'],
      deliverables: ['Five forces spider diagram', 'Industry attractiveness score', 'Strategic recommendations'],
      typicalDuration: '2-4 weeks',
      requiredResources: ['Industry experts', 'Market research', 'Competitor intelligence']
    },
    
    relatedFrameworks: [
      {
        id: 'value_chain_analysis',
        relationship: 'complementary',
        description: 'Identifies where to build competitive advantage'
      }
    ],
    
    cases: [
      {
        company: 'Netflix',
        industry: 'Streaming',
        stage: 'Growth',
        situation: 'Entering content production',
        application: 'Analyzed supplier power (content creators) and competitive rivalry',
        outcome: 'Decision to become content producer to reduce supplier power',
        keyLearning: 'Vertical integration can address unfavorable forces'
      }
    ],
    
    metadata: {
      popularity: 10,
      complexity: 'intermediate',
      evidenceStrength: 'proven',
      lastUpdated: new Date('2024-01-01'),
      tags: ['competitive-analysis', 'industry-analysis', 'classic']
    }
  }
  
  // We'll add 498+ more frameworks...
];

// Helper functions for framework operations
export function getFrameworkById(id: string): Framework | undefined {
  return frameworksDatabase.find(f => f.id === id);
}

export function getFrameworksByCategory(category: FrameworkCategory): Framework[] {
  return frameworksDatabase.filter(f => f.category === category);
}

export function searchFrameworks(query: string): Framework[] {
  const lowerQuery = query.toLowerCase();
  return frameworksDatabase.filter(f => 
    f.name.toLowerCase().includes(lowerQuery) ||
    f.description.toLowerCase().includes(lowerQuery) ||
    f.tags.some(tag => tag.toLowerCase().includes(lowerQuery))
  );
}

export function getFrameworksForStage(stage: string): Framework[] {
  return frameworksDatabase.filter(f => 
    f.applicability.stages.includes(stage) || 
    f.applicability.stages.includes('all')
  );
}

export function getFrameworksForSituation(situation: string): Framework[] {
  return frameworksDatabase.filter(f => 
    f.applicability.situations.includes(situation)
  );
}

// Intelligent framework matching based on startup data
export interface FrameworkMatch {
  framework: Framework;
  relevanceScore: number;
  dataCompleteness: number;
  rationale: string;
}

export function matchFrameworksToStartup(
  startupData: any,
  maxResults: number = 10
): FrameworkMatch[] {
  const matches = frameworksDatabase.map(framework => {
    const relevance = calculateRelevance(framework, startupData);
    const completeness = calculateDataCompleteness(framework, startupData);
    const rationale = generateRationale(framework, startupData, relevance);
    
    return {
      framework,
      relevanceScore: relevance,
      dataCompleteness: completeness,
      rationale
    };
  });
  
  return matches
    .filter(m => m.relevanceScore > 0.3 && m.dataCompleteness > 0.5)
    .sort((a, b) => b.relevanceScore - a.relevanceScore)
    .slice(0, maxResults);
}

function calculateRelevance(framework: Framework, data: any): number {
  let score = 0;
  
  // Stage match (30%)
  if (framework.applicability.stages.includes(data.funding_stage) || 
      framework.applicability.stages.includes('all')) {
    score += 0.3;
  }
  
  // Industry match (20%)
  if (framework.applicability.industries.includes(data.sector) ||
      framework.applicability.industries.includes('all')) {
    score += 0.2;
  }
  
  // Situation match (30%)
  const situation = inferSituation(data);
  const situationMatch = framework.applicability.situations.some(s => 
    situation.includes(s)
  );
  if (situationMatch) score += 0.3;
  
  // Company size match (10%)
  const { min, max } = framework.applicability.companySize;
  if (data.team_size_full_time >= min && data.team_size_full_time <= max) {
    score += 0.1;
  }
  
  // Complexity match (10%)
  const complexityScore = matchComplexity(framework.metadata.complexity, data);
  score += complexityScore * 0.1;
  
  return score;
}

function calculateDataCompleteness(framework: Framework, data: any): number {
  const required = framework.methodology.requiredMetrics.filter(m => 
    m.importance === 'required'
  );
  
  if (required.length === 0) return 1;
  
  const available = required.filter(metric => {
    const hasMain = data[metric.flashField] !== undefined && data[metric.flashField] !== null;
    const hasAlternative = metric.alternativeFields?.some(field => 
      data[field] !== undefined && data[field] !== null
    );
    return hasMain || hasAlternative;
  });
  
  return available.length / required.length;
}

function inferSituation(data: any): string[] {
  const situations = [];
  
  // Growth situation
  if (data.revenue_growth_rate_percent > 100) situations.push('growth');
  if (data.revenue_growth_rate_percent > 200) situations.push('hypergrowth');
  
  // Scale situation
  if (data.team_size_full_time > 50) situations.push('scale');
  
  // Efficiency situation
  if (data.burn_multiple && data.burn_multiple > 2) situations.push('efficiency');
  
  // Market situation
  if (data.competition_intensity > 7) situations.push('competitive_pressure');
  
  // Pivot situation
  if (data.product_retention_30d < 20) situations.push('pivot');
  
  return situations;
}

function matchComplexity(complexity: string, data: any): number {
  // Match framework complexity to company maturity
  const maturityScore = (
    (data.team_size_full_time / 100) +
    (data.funding_stage === 'series_b' ? 1 : data.funding_stage === 'series_a' ? 0.7 : 0.3)
  ) / 2;
  
  if (complexity === 'basic' && maturityScore < 0.3) return 1;
  if (complexity === 'intermediate' && maturityScore >= 0.3 && maturityScore < 0.7) return 1;
  if (complexity === 'advanced' && maturityScore >= 0.7) return 1;
  
  return 0.5; // Partial match
}

function generateRationale(framework: Framework, data: any, score: number): string {
  const reasons = [];
  
  if (framework.applicability.stages.includes(data.funding_stage)) {
    reasons.push(`Designed for ${data.funding_stage} stage companies`);
  }
  
  const situation = inferSituation(data);
  const matchingSituations = framework.applicability.situations.filter(s => 
    situation.includes(s)
  );
  if (matchingSituations.length > 0) {
    reasons.push(`Addresses your ${matchingSituations.join(', ')} challenges`);
  }
  
  if (score > 0.8) {
    reasons.push('Highly relevant to your current context');
  }
  
  return reasons.join('. ');
}