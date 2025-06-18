// Comprehensive Business Framework Database
// Designed with PhD-level rigor for startup analysis

export interface FrameworkMetadata {
  id: string;
  name: string;
  category: FrameworkCategory;
  description: string;
  complexity: 'basic' | 'intermediate' | 'advanced' | 'expert';
  timeToImplement: string;
  visualizationType: VisualizationType;
  analysisType: AnalysisType;
  dataRequirements: DataRequirement[];
  outputType: OutputType;
  academicOrigin?: string;
  yearIntroduced?: number;
  primaryUseCase: string;
  limitations: string[];
}

export enum FrameworkCategory {
  STRATEGY = 'Strategy',
  INNOVATION = 'Innovation',
  GROWTH = 'Growth',
  FINANCIAL = 'Financial',
  OPERATIONS = 'Operations',
  MARKETING = 'Marketing',
  PRODUCT = 'Product',
  LEADERSHIP = 'Leadership',
  ORGANIZATIONAL = 'Organizational',
  COMPETITIVE = 'Competitive',
  CUSTOMER = 'Customer',
  RISK = 'Risk',
  DIGITAL = 'Digital',
  SUSTAINABILITY = 'Sustainability'
}

export enum VisualizationType {
  MATRIX_2X2 = 'matrix_2x2',
  MATRIX_3X3 = 'matrix_3x3',
  QUADRANT = 'quadrant',
  RADAR = 'radar',
  FUNNEL = 'funnel',
  PYRAMID = 'pyramid',
  CANVAS = 'canvas',
  FORCE_DIAGRAM = 'force_diagram',
  FLOW_CHART = 'flow_chart',
  HEAT_MAP = 'heat_map',
  TIMELINE = 'timeline',
  TREE = 'tree',
  NETWORK = 'network',
  GAUGE = 'gauge',
  SCORE_CARD = 'score_card'
}

export enum AnalysisType {
  POSITIONING = 'positioning',
  SCORING = 'scoring',
  MAPPING = 'mapping',
  ASSESSMENT = 'assessment',
  COMPARISON = 'comparison',
  PRIORITIZATION = 'prioritization',
  SEGMENTATION = 'segmentation',
  EVALUATION = 'evaluation'
}

export enum DataRequirement {
  FINANCIAL = 'financial',
  MARKET = 'market',
  COMPETITIVE = 'competitive',
  OPERATIONAL = 'operational',
  CUSTOMER = 'customer',
  TEAM = 'team',
  PRODUCT = 'product',
  STRATEGIC = 'strategic'
}

export enum OutputType {
  POSITION = 'position',
  SCORE = 'score',
  RANKING = 'ranking',
  SEGMENTS = 'segments',
  PRIORITIES = 'priorities',
  GAPS = 'gaps',
  OPPORTUNITIES = 'opportunities',
  RISKS = 'risks'
}

// The Comprehensive Framework Database
export const BUSINESS_FRAMEWORKS: FrameworkMetadata[] = [
  // 1. Strategic Planning Frameworks
  {
    id: 'bcg_matrix',
    name: 'BCG Growth-Share Matrix',
    category: FrameworkCategory.STRATEGY,
    description: 'Portfolio analysis tool that categorizes business units or products based on market growth and relative market share',
    complexity: 'intermediate',
    timeToImplement: '2-3 hours',
    visualizationType: VisualizationType.MATRIX_2X2,
    analysisType: AnalysisType.POSITIONING,
    dataRequirements: [DataRequirement.MARKET, DataRequirement.FINANCIAL],
    outputType: OutputType.POSITION,
    academicOrigin: 'Boston Consulting Group',
    yearIntroduced: 1970,
    primaryUseCase: 'Portfolio management and resource allocation decisions',
    limitations: ['Oversimplifies complex markets', 'Ignores synergies between units']
  },
  {
    id: 'porters_five_forces',
    name: "Porter's Five Forces",
    category: FrameworkCategory.COMPETITIVE,
    description: 'Analyzes industry attractiveness and competitive intensity through five key forces',
    complexity: 'advanced',
    timeToImplement: '3-4 hours',
    visualizationType: VisualizationType.FORCE_DIAGRAM,
    analysisType: AnalysisType.ASSESSMENT,
    dataRequirements: [DataRequirement.MARKET, DataRequirement.COMPETITIVE],
    outputType: OutputType.SCORE,
    academicOrigin: 'Michael Porter, Harvard Business School',
    yearIntroduced: 1979,
    primaryUseCase: 'Industry analysis and competitive strategy formulation',
    limitations: ['Static view', 'Doesn\'t account for collaboration']
  },
  {
    id: 'swot_analysis',
    name: 'SWOT Analysis',
    category: FrameworkCategory.STRATEGY,
    description: 'Evaluates internal strengths/weaknesses and external opportunities/threats',
    complexity: 'basic',
    timeToImplement: '1-2 hours',
    visualizationType: VisualizationType.QUADRANT,
    analysisType: AnalysisType.ASSESSMENT,
    dataRequirements: [DataRequirement.STRATEGIC],
    outputType: OutputType.GAPS,
    yearIntroduced: 1960,
    primaryUseCase: 'Strategic planning and decision making',
    limitations: ['Subjective', 'No prioritization mechanism']
  },
  {
    id: 'pestel_analysis',
    name: 'PESTEL Analysis',
    category: FrameworkCategory.STRATEGY,
    description: 'Examines macro-environmental factors: Political, Economic, Social, Technological, Environmental, Legal',
    complexity: 'intermediate',
    timeToImplement: '3-4 hours',
    visualizationType: VisualizationType.RADAR,
    analysisType: AnalysisType.ASSESSMENT,
    dataRequirements: [DataRequirement.MARKET, DataRequirement.STRATEGIC],
    outputType: OutputType.RISKS,
    primaryUseCase: 'Environmental scanning and strategic planning',
    limitations: ['Time-consuming', 'Requires extensive research']
  },
  {
    id: 'ansoff_matrix',
    name: 'Ansoff Growth Matrix',
    category: FrameworkCategory.GROWTH,
    description: 'Strategic planning tool for identifying growth opportunities through market/product combinations',
    complexity: 'intermediate',
    timeToImplement: '2-3 hours',
    visualizationType: VisualizationType.MATRIX_2X2,
    analysisType: AnalysisType.POSITIONING,
    dataRequirements: [DataRequirement.MARKET, DataRequirement.PRODUCT],
    outputType: OutputType.OPPORTUNITIES,
    academicOrigin: 'Igor Ansoff',
    yearIntroduced: 1957,
    primaryUseCase: 'Growth strategy selection',
    limitations: ['Doesn\'t consider capability requirements']
  },
  {
    id: 'blue_ocean_strategy',
    name: 'Blue Ocean Strategy Canvas',
    category: FrameworkCategory.INNOVATION,
    description: 'Creates uncontested market space by reconstructing market boundaries',
    complexity: 'advanced',
    timeToImplement: '4-6 hours',
    visualizationType: VisualizationType.CANVAS,
    analysisType: AnalysisType.COMPARISON,
    dataRequirements: [DataRequirement.MARKET, DataRequirement.COMPETITIVE, DataRequirement.CUSTOMER],
    outputType: OutputType.OPPORTUNITIES,
    academicOrigin: 'INSEAD',
    yearIntroduced: 2005,
    primaryUseCase: 'Market creation and differentiation',
    limitations: ['Difficult to implement', 'Risk of market rejection']
  },
  {
    id: 'ge_mckinsey_matrix',
    name: 'GE-McKinsey Nine-Box Matrix',
    category: FrameworkCategory.STRATEGY,
    description: 'Portfolio analysis using industry attractiveness and business unit strength',
    complexity: 'advanced',
    timeToImplement: '4-5 hours',
    visualizationType: VisualizationType.MATRIX_3X3,
    analysisType: AnalysisType.POSITIONING,
    dataRequirements: [DataRequirement.MARKET, DataRequirement.COMPETITIVE, DataRequirement.FINANCIAL],
    outputType: OutputType.POSITION,
    yearIntroduced: 1970,
    primaryUseCase: 'Portfolio management and investment decisions',
    limitations: ['Complex scoring', 'Subjective weightings']
  },
  {
    id: 'balanced_scorecard',
    name: 'Balanced Scorecard',
    category: FrameworkCategory.ORGANIZATIONAL,
    description: 'Strategic management system linking strategy to operational metrics across four perspectives',
    complexity: 'expert',
    timeToImplement: '1-2 weeks',
    visualizationType: VisualizationType.SCORE_CARD,
    analysisType: AnalysisType.SCORING,
    dataRequirements: [DataRequirement.FINANCIAL, DataRequirement.CUSTOMER, DataRequirement.OPERATIONAL, DataRequirement.TEAM],
    outputType: OutputType.SCORE,
    academicOrigin: 'Kaplan & Norton, Harvard Business School',
    yearIntroduced: 1992,
    primaryUseCase: 'Strategy execution and performance management',
    limitations: ['Implementation complexity', 'Requires cultural change']
  },

  // 2. Innovation & Product Frameworks
  {
    id: 'lean_startup',
    name: 'Lean Startup Methodology',
    category: FrameworkCategory.INNOVATION,
    description: 'Build-Measure-Learn cycle for rapid validation and iteration',
    complexity: 'intermediate',
    timeToImplement: '2-4 weeks per cycle',
    visualizationType: VisualizationType.FLOW_CHART,
    analysisType: AnalysisType.EVALUATION,
    dataRequirements: [DataRequirement.PRODUCT, DataRequirement.CUSTOMER],
    outputType: OutputType.PRIORITIES,
    academicOrigin: 'Eric Ries',
    yearIntroduced: 2011,
    primaryUseCase: 'Product development and market validation',
    limitations: ['Not suitable for all industries', 'Can lead to local optima']
  },
  {
    id: 'business_model_canvas',
    name: 'Business Model Canvas',
    category: FrameworkCategory.STRATEGY,
    description: 'Visual template for developing and documenting business models',
    complexity: 'intermediate',
    timeToImplement: '3-4 hours',
    visualizationType: VisualizationType.CANVAS,
    analysisType: AnalysisType.MAPPING,
    dataRequirements: [DataRequirement.STRATEGIC, DataRequirement.OPERATIONAL],
    outputType: OutputType.GAPS,
    academicOrigin: 'Alexander Osterwalder',
    yearIntroduced: 2010,
    primaryUseCase: 'Business model design and innovation',
    limitations: ['High-level view', 'Lacks financial detail']
  },
  {
    id: 'value_proposition_canvas',
    name: 'Value Proposition Canvas',
    category: FrameworkCategory.CUSTOMER,
    description: 'Maps customer jobs, pains, and gains to product features and benefits',
    complexity: 'intermediate',
    timeToImplement: '2-3 hours',
    visualizationType: VisualizationType.CANVAS,
    analysisType: AnalysisType.MAPPING,
    dataRequirements: [DataRequirement.CUSTOMER, DataRequirement.PRODUCT],
    outputType: OutputType.GAPS,
    academicOrigin: 'Alexander Osterwalder',
    yearIntroduced: 2014,
    primaryUseCase: 'Product-market fit optimization',
    limitations: ['Requires deep customer understanding']
  },
  {
    id: 'jobs_to_be_done',
    name: 'Jobs to be Done Framework',
    category: FrameworkCategory.CUSTOMER,
    description: 'Focuses on customer motivations and desired outcomes rather than demographics',
    complexity: 'advanced',
    timeToImplement: '1-2 weeks',
    visualizationType: VisualizationType.TREE,
    analysisType: AnalysisType.SEGMENTATION,
    dataRequirements: [DataRequirement.CUSTOMER],
    outputType: OutputType.SEGMENTS,
    academicOrigin: 'Clayton Christensen, Harvard Business School',
    yearIntroduced: 2003,
    primaryUseCase: 'Innovation and product development',
    limitations: ['Requires extensive customer research']
  },
  {
    id: 'design_thinking',
    name: 'Design Thinking Process',
    category: FrameworkCategory.INNOVATION,
    description: 'Human-centered approach to innovation: Empathize, Define, Ideate, Prototype, Test',
    complexity: 'intermediate',
    timeToImplement: '4-8 weeks',
    visualizationType: VisualizationType.FLOW_CHART,
    analysisType: AnalysisType.EVALUATION,
    dataRequirements: [DataRequirement.CUSTOMER],
    outputType: OutputType.PRIORITIES,
    academicOrigin: 'Stanford d.school',
    primaryUseCase: 'Product innovation and problem solving',
    limitations: ['Time-intensive', 'Requires cultural shift']
  },
  {
    id: 'technology_adoption_lifecycle',
    name: 'Technology Adoption Lifecycle',
    category: FrameworkCategory.MARKETING,
    description: 'Categorizes customers into adoption segments: Innovators, Early Adopters, Early/Late Majority, Laggards',
    complexity: 'intermediate',
    timeToImplement: '2-3 hours',
    visualizationType: VisualizationType.TIMELINE,
    analysisType: AnalysisType.SEGMENTATION,
    dataRequirements: [DataRequirement.CUSTOMER, DataRequirement.MARKET],
    outputType: OutputType.SEGMENTS,
    academicOrigin: 'Everett Rogers',
    yearIntroduced: 1962,
    primaryUseCase: 'Go-to-market strategy and customer targeting',
    limitations: ['Assumes normal distribution']
  },

  // 3. Marketing & Growth Frameworks
  {
    id: 'aarrr_metrics',
    name: 'AARRR (Pirate) Metrics',
    category: FrameworkCategory.GROWTH,
    description: 'Funnel metrics: Acquisition, Activation, Retention, Referral, Revenue',
    complexity: 'basic',
    timeToImplement: '1-2 hours setup',
    visualizationType: VisualizationType.FUNNEL,
    analysisType: AnalysisType.SCORING,
    dataRequirements: [DataRequirement.CUSTOMER, DataRequirement.FINANCIAL],
    outputType: OutputType.SCORE,
    academicOrigin: 'Dave McClure, 500 Startups',
    yearIntroduced: 2007,
    primaryUseCase: 'Growth optimization and metrics tracking',
    limitations: ['Oversimplifies customer journey']
  },
  {
    id: 'growth_share_matrix',
    name: 'Growth-Share Matrix',
    category: FrameworkCategory.GROWTH,
    description: 'Analyzes growth opportunities based on market and capability development',
    complexity: 'intermediate',
    timeToImplement: '2-3 hours',
    visualizationType: VisualizationType.MATRIX_2X2,
    analysisType: AnalysisType.POSITIONING,
    dataRequirements: [DataRequirement.MARKET, DataRequirement.STRATEGIC],
    outputType: OutputType.OPPORTUNITIES,
    primaryUseCase: 'Growth strategy prioritization',
    limitations: ['Static view of dynamic markets']
  },
  {
    id: 'customer_journey_map',
    name: 'Customer Journey Mapping',
    category: FrameworkCategory.CUSTOMER,
    description: 'Visualizes customer interactions across all touchpoints',
    complexity: 'intermediate',
    timeToImplement: '1-2 weeks',
    visualizationType: VisualizationType.FLOW_CHART,
    analysisType: AnalysisType.MAPPING,
    dataRequirements: [DataRequirement.CUSTOMER],
    outputType: OutputType.GAPS,
    primaryUseCase: 'Customer experience optimization',
    limitations: ['Resource intensive to create']
  },
  {
    id: 'segmentation_targeting_positioning',
    name: 'STP Marketing Model',
    category: FrameworkCategory.MARKETING,
    description: 'Strategic approach to market segmentation, target selection, and positioning',
    complexity: 'intermediate',
    timeToImplement: '1-2 weeks',
    visualizationType: VisualizationType.MATRIX_3X3,
    analysisType: AnalysisType.SEGMENTATION,
    dataRequirements: [DataRequirement.MARKET, DataRequirement.CUSTOMER],
    outputType: OutputType.SEGMENTS,
    primaryUseCase: 'Market strategy development',
    limitations: ['Requires market research']
  },
  {
    id: 'brand_equity_pyramid',
    name: 'Brand Equity Pyramid',
    category: FrameworkCategory.MARKETING,
    description: 'Builds brand value through salience, performance, imagery, judgments, feelings, and resonance',
    complexity: 'advanced',
    timeToImplement: '2-3 weeks',
    visualizationType: VisualizationType.PYRAMID,
    analysisType: AnalysisType.ASSESSMENT,
    dataRequirements: [DataRequirement.CUSTOMER, DataRequirement.MARKET],
    outputType: OutputType.SCORE,
    academicOrigin: 'Kevin Lane Keller',
    yearIntroduced: 2001,
    primaryUseCase: 'Brand strategy and management',
    limitations: ['Long-term perspective needed']
  },

  // 4. Organizational & Leadership Frameworks
  {
    id: 'mckinsey_7s',
    name: 'McKinsey 7S Framework',
    category: FrameworkCategory.ORGANIZATIONAL,
    description: 'Analyzes organizational effectiveness through 7 interdependent elements',
    complexity: 'advanced',
    timeToImplement: '1-2 weeks',
    visualizationType: VisualizationType.NETWORK,
    analysisType: AnalysisType.ASSESSMENT,
    dataRequirements: [DataRequirement.ORGANIZATIONAL, DataRequirement.TEAM],
    outputType: OutputType.GAPS,
    academicOrigin: 'McKinsey & Company',
    yearIntroduced: 1980,
    primaryUseCase: 'Organizational change and alignment',
    limitations: ['Complex interdependencies']
  },
  {
    id: 'organizational_culture_assessment',
    name: 'Competing Values Framework',
    category: FrameworkCategory.ORGANIZATIONAL,
    description: 'Assesses organizational culture across flexibility/stability and internal/external focus',
    complexity: 'intermediate',
    timeToImplement: '1 week',
    visualizationType: VisualizationType.QUADRANT,
    analysisType: AnalysisType.ASSESSMENT,
    dataRequirements: [DataRequirement.TEAM],
    outputType: OutputType.POSITION,
    academicOrigin: 'Cameron & Quinn',
    yearIntroduced: 1999,
    primaryUseCase: 'Culture assessment and change',
    limitations: ['Self-reported data bias']
  },
  {
    id: 'kotter_8_step_change',
    name: "Kotter's 8-Step Change Model",
    category: FrameworkCategory.LEADERSHIP,
    description: 'Systematic approach to organizational transformation',
    complexity: 'expert',
    timeToImplement: '6-12 months',
    visualizationType: VisualizationType.FLOW_CHART,
    analysisType: AnalysisType.EVALUATION,
    dataRequirements: [DataRequirement.ORGANIZATIONAL],
    outputType: OutputType.PRIORITIES,
    academicOrigin: 'John Kotter, Harvard Business School',
    yearIntroduced: 1996,
    primaryUseCase: 'Large-scale organizational change',
    limitations: ['Linear approach', 'Time-consuming']
  },
  {
    id: 'leadership_grid',
    name: 'Blake-Mouton Leadership Grid',
    category: FrameworkCategory.LEADERSHIP,
    description: 'Plots leadership style based on concern for people vs. concern for results',
    complexity: 'basic',
    timeToImplement: '1-2 hours',
    visualizationType: VisualizationType.MATRIX_2X2,
    analysisType: AnalysisType.POSITIONING,
    dataRequirements: [DataRequirement.TEAM],
    outputType: OutputType.POSITION,
    yearIntroduced: 1964,
    primaryUseCase: 'Leadership development',
    limitations: ['Oversimplifies leadership complexity']
  },

  // 5. Financial & Performance Frameworks
  {
    id: 'dupont_analysis',
    name: 'DuPont Analysis',
    category: FrameworkCategory.FINANCIAL,
    description: 'Decomposes ROE into profitability, efficiency, and leverage components',
    complexity: 'intermediate',
    timeToImplement: '2-3 hours',
    visualizationType: VisualizationType.TREE,
    analysisType: AnalysisType.SCORING,
    dataRequirements: [DataRequirement.FINANCIAL],
    outputType: OutputType.SCORE,
    yearIntroduced: 1920,
    primaryUseCase: 'Financial performance analysis',
    limitations: ['Historical focus']
  },
  {
    id: 'economic_value_added',
    name: 'Economic Value Added (EVA)',
    category: FrameworkCategory.FINANCIAL,
    description: 'Measures true economic profit after cost of capital',
    complexity: 'advanced',
    timeToImplement: '3-4 hours',
    visualizationType: VisualizationType.GAUGE,
    analysisType: AnalysisType.SCORING,
    dataRequirements: [DataRequirement.FINANCIAL],
    outputType: OutputType.SCORE,
    academicOrigin: 'Stern Stewart & Co',
    yearIntroduced: 1991,
    primaryUseCase: 'Value creation measurement',
    limitations: ['Complex calculations']
  },
  {
    id: 'activity_based_costing',
    name: 'Activity-Based Costing (ABC)',
    category: FrameworkCategory.FINANCIAL,
    description: 'Assigns costs to products/services based on resource consumption',
    complexity: 'expert',
    timeToImplement: '2-4 weeks',
    visualizationType: VisualizationType.FLOW_CHART,
    analysisType: AnalysisType.MAPPING,
    dataRequirements: [DataRequirement.FINANCIAL, DataRequirement.OPERATIONAL],
    outputType: OutputType.GAPS,
    yearIntroduced: 1987,
    primaryUseCase: 'Cost management and pricing',
    limitations: ['Implementation complexity']
  },

  // 6. Operations & Process Frameworks
  {
    id: 'value_stream_mapping',
    name: 'Value Stream Mapping',
    category: FrameworkCategory.OPERATIONS,
    description: 'Visualizes material and information flow to identify waste',
    complexity: 'intermediate',
    timeToImplement: '1-2 weeks',
    visualizationType: VisualizationType.FLOW_CHART,
    analysisType: AnalysisType.MAPPING,
    dataRequirements: [DataRequirement.OPERATIONAL],
    outputType: OutputType.GAPS,
    primaryUseCase: 'Process optimization',
    limitations: ['Manufacturing focus']
  },
  {
    id: 'theory_of_constraints',
    name: 'Theory of Constraints',
    category: FrameworkCategory.OPERATIONS,
    description: 'Identifies and manages bottlenecks in systems',
    complexity: 'advanced',
    timeToImplement: '2-4 weeks',
    visualizationType: VisualizationType.FLOW_CHART,
    analysisType: AnalysisType.EVALUATION,
    dataRequirements: [DataRequirement.OPERATIONAL],
    outputType: OutputType.GAPS,
    academicOrigin: 'Eliyahu Goldratt',
    yearIntroduced: 1984,
    primaryUseCase: 'Throughput optimization',
    limitations: ['Single constraint focus']
  },
  {
    id: 'six_sigma_dmaic',
    name: 'Six Sigma DMAIC',
    category: FrameworkCategory.OPERATIONS,
    description: 'Define, Measure, Analyze, Improve, Control process improvement',
    complexity: 'expert',
    timeToImplement: '3-6 months',
    visualizationType: VisualizationType.FLOW_CHART,
    analysisType: AnalysisType.EVALUATION,
    dataRequirements: [DataRequirement.OPERATIONAL],
    outputType: OutputType.GAPS,
    academicOrigin: 'Motorola',
    yearIntroduced: 1986,
    primaryUseCase: 'Quality improvement',
    limitations: ['Resource intensive']
  },

  // 7. Digital & Technology Frameworks
  {
    id: 'digital_maturity_model',
    name: 'Digital Maturity Model',
    category: FrameworkCategory.DIGITAL,
    description: 'Assesses organization\'s digital capabilities across multiple dimensions',
    complexity: 'intermediate',
    timeToImplement: '1-2 weeks',
    visualizationType: VisualizationType.RADAR,
    analysisType: AnalysisType.ASSESSMENT,
    dataRequirements: [DataRequirement.OPERATIONAL, DataRequirement.STRATEGIC],
    outputType: OutputType.SCORE,
    primaryUseCase: 'Digital transformation planning',
    limitations: ['Rapid technology changes']
  },
  {
    id: 'platform_business_model',
    name: 'Platform Business Model Canvas',
    category: FrameworkCategory.DIGITAL,
    description: 'Adapted canvas for multi-sided platform businesses',
    complexity: 'advanced',
    timeToImplement: '3-4 hours',
    visualizationType: VisualizationType.CANVAS,
    analysisType: AnalysisType.MAPPING,
    dataRequirements: [DataRequirement.STRATEGIC, DataRequirement.CUSTOMER],
    outputType: OutputType.GAPS,
    primaryUseCase: 'Platform strategy design',
    limitations: ['Network effects complexity']
  },
  {
    id: 'api_business_model',
    name: 'API Business Model',
    category: FrameworkCategory.DIGITAL,
    description: 'Framework for API strategy and monetization',
    complexity: 'advanced',
    timeToImplement: '1-2 weeks',
    visualizationType: VisualizationType.CANVAS,
    analysisType: AnalysisType.MAPPING,
    dataRequirements: [DataRequirement.PRODUCT, DataRequirement.STRATEGIC],
    outputType: OutputType.OPPORTUNITIES,
    primaryUseCase: 'API strategy development',
    limitations: ['Technical complexity']
  },

  // 8. Risk & Compliance Frameworks
  {
    id: 'risk_matrix',
    name: 'Risk Impact/Probability Matrix',
    category: FrameworkCategory.RISK,
    description: 'Plots risks by likelihood and potential impact',
    complexity: 'basic',
    timeToImplement: '2-3 hours',
    visualizationType: VisualizationType.MATRIX_2X2,
    analysisType: AnalysisType.PRIORITIZATION,
    dataRequirements: [DataRequirement.STRATEGIC],
    outputType: OutputType.RISKS,
    primaryUseCase: 'Risk assessment and prioritization',
    limitations: ['Subjective assessments']
  },
  {
    id: 'scenario_planning',
    name: 'Scenario Planning Matrix',
    category: FrameworkCategory.RISK,
    description: 'Develops multiple future scenarios based on key uncertainties',
    complexity: 'expert',
    timeToImplement: '2-4 weeks',
    visualizationType: VisualizationType.MATRIX_2X2,
    analysisType: AnalysisType.EVALUATION,
    dataRequirements: [DataRequirement.STRATEGIC, DataRequirement.MARKET],
    outputType: OutputType.OPPORTUNITIES,
    academicOrigin: 'Shell',
    yearIntroduced: 1970,
    primaryUseCase: 'Strategic planning under uncertainty',
    limitations: ['Resource intensive']
  },

  // 9. Competitive & Market Analysis
  {
    id: 'competitive_profile_matrix',
    name: 'Competitive Profile Matrix',
    category: FrameworkCategory.COMPETITIVE,
    description: 'Compares company against competitors on critical success factors',
    complexity: 'intermediate',
    timeToImplement: '3-4 hours',
    visualizationType: VisualizationType.HEAT_MAP,
    analysisType: AnalysisType.COMPARISON,
    dataRequirements: [DataRequirement.COMPETITIVE, DataRequirement.MARKET],
    outputType: OutputType.RANKING,
    primaryUseCase: 'Competitive positioning analysis',
    limitations: ['Data availability']
  },
  {
    id: 'market_attractiveness_matrix',
    name: 'Market Attractiveness Matrix',
    category: FrameworkCategory.MARKET,
    description: 'Evaluates markets based on attractiveness and competitive position',
    complexity: 'intermediate',
    timeToImplement: '3-4 hours',
    visualizationType: VisualizationType.MATRIX_3X3,
    analysisType: AnalysisType.POSITIONING,
    dataRequirements: [DataRequirement.MARKET, DataRequirement.COMPETITIVE],
    outputType: OutputType.OPPORTUNITIES,
    primaryUseCase: 'Market entry decisions',
    limitations: ['Dynamic market conditions']
  },
  {
    id: 'perceptual_mapping',
    name: 'Perceptual Mapping',
    category: FrameworkCategory.MARKETING,
    description: 'Visualizes customer perceptions of brands/products on key attributes',
    complexity: 'intermediate',
    timeToImplement: '1-2 weeks',
    visualizationType: VisualizationType.QUADRANT,
    analysisType: AnalysisType.POSITIONING,
    dataRequirements: [DataRequirement.CUSTOMER, DataRequirement.COMPETITIVE],
    outputType: OutputType.POSITION,
    primaryUseCase: 'Brand positioning strategy',
    limitations: ['Requires customer research']
  },

  // 10. Innovation & Disruption Frameworks
  {
    id: 'disruptive_innovation',
    name: 'Disruptive Innovation Model',
    category: FrameworkCategory.INNOVATION,
    description: 'Identifies potential for low-end or new-market disruption',
    complexity: 'advanced',
    timeToImplement: '1-2 weeks',
    visualizationType: VisualizationType.TIMELINE,
    analysisType: AnalysisType.EVALUATION,
    dataRequirements: [DataRequirement.MARKET, DataRequirement.PRODUCT],
    outputType: OutputType.OPPORTUNITIES,
    academicOrigin: 'Clayton Christensen',
    yearIntroduced: 1997,
    primaryUseCase: 'Innovation strategy',
    limitations: ['Predictive challenges']
  },
  {
    id: 'innovation_ambition_matrix',
    name: 'Innovation Ambition Matrix',
    category: FrameworkCategory.INNOVATION,
    description: 'Balances innovation portfolio across core, adjacent, and transformational',
    complexity: 'intermediate',
    timeToImplement: '2-3 hours',
    visualizationType: VisualizationType.MATRIX_3X3,
    analysisType: AnalysisType.POSITIONING,
    dataRequirements: [DataRequirement.PRODUCT, DataRequirement.STRATEGIC],
    outputType: OutputType.PRIORITIES,
    primaryUseCase: 'Innovation portfolio management',
    limitations: ['Resource allocation complexity']
  },
  {
    id: 'ten_types_innovation',
    name: 'Ten Types of Innovation',
    category: FrameworkCategory.INNOVATION,
    description: 'Systematic approach to innovation across 10 distinct areas',
    complexity: 'advanced',
    timeToImplement: '1-2 weeks',
    visualizationType: VisualizationType.RADAR,
    analysisType: AnalysisType.ASSESSMENT,
    dataRequirements: [DataRequirement.STRATEGIC, DataRequirement.PRODUCT],
    outputType: OutputType.GAPS,
    academicOrigin: 'Doblin',
    yearIntroduced: 1998,
    primaryUseCase: 'Holistic innovation planning',
    limitations: ['Requires broad organizational view']
  },

  // 11. Customer & Market Frameworks
  {
    id: 'customer_lifetime_value',
    name: 'CLV/CAC Analysis',
    category: FrameworkCategory.CUSTOMER,
    description: 'Analyzes customer lifetime value against acquisition costs',
    complexity: 'intermediate',
    timeToImplement: '2-3 hours',
    visualizationType: VisualizationType.GAUGE,
    analysisType: AnalysisType.SCORING,
    dataRequirements: [DataRequirement.FINANCIAL, DataRequirement.CUSTOMER],
    outputType: OutputType.SCORE,
    primaryUseCase: 'Unit economics optimization',
    limitations: ['Prediction accuracy']
  },
  {
    id: 'nps_driver_analysis',
    name: 'NPS Driver Analysis',
    category: FrameworkCategory.CUSTOMER,
    description: 'Identifies key drivers of customer satisfaction and loyalty',
    complexity: 'intermediate',
    timeToImplement: '1-2 weeks',
    visualizationType: VisualizationType.TREE,
    analysisType: AnalysisType.EVALUATION,
    dataRequirements: [DataRequirement.CUSTOMER],
    outputType: OutputType.PRIORITIES,
    primaryUseCase: 'Customer experience improvement',
    limitations: ['Survey response bias']
  },
  {
    id: 'market_segmentation_matrix',
    name: 'Market Segmentation Matrix',
    category: FrameworkCategory.MARKET,
    description: 'Segments market based on needs and behaviors',
    complexity: 'intermediate',
    timeToImplement: '1-2 weeks',
    visualizationType: VisualizationType.MATRIX_3X3,
    analysisType: AnalysisType.SEGMENTATION,
    dataRequirements: [DataRequirement.CUSTOMER, DataRequirement.MARKET],
    outputType: OutputType.SEGMENTS,
    primaryUseCase: 'Target market selection',
    limitations: ['Data requirements']
  },

  // 12. Sustainability & ESG Frameworks
  {
    id: 'triple_bottom_line',
    name: 'Triple Bottom Line',
    category: FrameworkCategory.SUSTAINABILITY,
    description: 'Measures performance across People, Planet, and Profit',
    complexity: 'intermediate',
    timeToImplement: '1-2 weeks',
    visualizationType: VisualizationType.RADAR,
    analysisType: AnalysisType.SCORING,
    dataRequirements: [DataRequirement.STRATEGIC, DataRequirement.OPERATIONAL],
    outputType: OutputType.SCORE,
    yearIntroduced: 1994,
    primaryUseCase: 'Sustainability assessment',
    limitations: ['Measurement challenges']
  },
  {
    id: 'circular_economy_model',
    name: 'Circular Economy Model',
    category: FrameworkCategory.SUSTAINABILITY,
    description: 'Designs regenerative business models eliminating waste',
    complexity: 'advanced',
    timeToImplement: '2-4 weeks',
    visualizationType: VisualizationType.FLOW_CHART,
    analysisType: AnalysisType.MAPPING,
    dataRequirements: [DataRequirement.OPERATIONAL, DataRequirement.PRODUCT],
    outputType: OutputType.OPPORTUNITIES,
    primaryUseCase: 'Sustainable business model design',
    limitations: ['System complexity']
  },

  // 13. Strategic Tools
  {
    id: 'vrio_framework',
    name: 'VRIO Framework',
    category: FrameworkCategory.STRATEGY,
    description: 'Evaluates resources for sustainable competitive advantage',
    complexity: 'intermediate',
    timeToImplement: '2-3 hours',
    visualizationType: VisualizationType.SCORE_CARD,
    analysisType: AnalysisType.ASSESSMENT,
    dataRequirements: [DataRequirement.STRATEGIC, DataRequirement.OPERATIONAL],
    outputType: OutputType.SCORE,
    academicOrigin: 'Jay Barney',
    yearIntroduced: 1991,
    primaryUseCase: 'Resource-based strategy',
    limitations: ['Static analysis']
  },
  {
    id: 'strategic_group_mapping',
    name: 'Strategic Group Mapping',
    category: FrameworkCategory.COMPETITIVE,
    description: 'Maps competitors based on strategic dimensions',
    complexity: 'intermediate',
    timeToImplement: '3-4 hours',
    visualizationType: VisualizationType.QUADRANT,
    analysisType: AnalysisType.POSITIONING,
    dataRequirements: [DataRequirement.COMPETITIVE, DataRequirement.MARKET],
    outputType: OutputType.POSITION,
    primaryUseCase: 'Competitive analysis',
    limitations: ['Dimension selection']
  },
  {
    id: 'core_competence_analysis',
    name: 'Core Competence Analysis',
    category: FrameworkCategory.STRATEGY,
    description: 'Identifies unique organizational capabilities',
    complexity: 'intermediate',
    timeToImplement: '1-2 weeks',
    visualizationType: VisualizationType.TREE,
    analysisType: AnalysisType.ASSESSMENT,
    dataRequirements: [DataRequirement.STRATEGIC, DataRequirement.OPERATIONAL],
    outputType: OutputType.PRIORITIES,
    academicOrigin: 'Prahalad & Hamel',
    yearIntroduced: 1990,
    primaryUseCase: 'Strategic focus',
    limitations: ['Identification difficulty']
  },

  // 14. Product Management Frameworks
  {
    id: 'product_lifecycle',
    name: 'Product Lifecycle Analysis',
    category: FrameworkCategory.PRODUCT,
    description: 'Maps products through introduction, growth, maturity, and decline',
    complexity: 'basic',
    timeToImplement: '2-3 hours',
    visualizationType: VisualizationType.TIMELINE,
    analysisType: AnalysisType.POSITIONING,
    dataRequirements: [DataRequirement.PRODUCT, DataRequirement.MARKET],
    outputType: OutputType.POSITION,
    primaryUseCase: 'Product strategy planning',
    limitations: ['Prediction challenges']
  },
  {
    id: 'kano_model',
    name: 'Kano Model',
    category: FrameworkCategory.PRODUCT,
    description: 'Categorizes features by customer satisfaction impact',
    complexity: 'intermediate',
    timeToImplement: '1-2 weeks',
    visualizationType: VisualizationType.QUADRANT,
    analysisType: AnalysisType.PRIORITIZATION,
    dataRequirements: [DataRequirement.CUSTOMER, DataRequirement.PRODUCT],
    outputType: OutputType.PRIORITIES,
    academicOrigin: 'Noriaki Kano',
    yearIntroduced: 1984,
    primaryUseCase: 'Feature prioritization',
    limitations: ['Cultural differences']
  },
  {
    id: 'rice_prioritization',
    name: 'RICE Prioritization Framework',
    category: FrameworkCategory.PRODUCT,
    description: 'Scores features by Reach, Impact, Confidence, and Effort',
    complexity: 'basic',
    timeToImplement: '1-2 hours',
    visualizationType: VisualizationType.SCORE_CARD,
    analysisType: AnalysisType.PRIORITIZATION,
    dataRequirements: [DataRequirement.PRODUCT],
    outputType: OutputType.PRIORITIES,
    primaryUseCase: 'Feature prioritization',
    limitations: ['Estimation accuracy']
  },

  // 15. Network & Ecosystem Frameworks
  {
    id: 'ecosystem_mapping',
    name: 'Business Ecosystem Mapping',
    category: FrameworkCategory.STRATEGY,
    description: 'Maps relationships and value flows in business ecosystem',
    complexity: 'advanced',
    timeToImplement: '1-2 weeks',
    visualizationType: VisualizationType.NETWORK,
    analysisType: AnalysisType.MAPPING,
    dataRequirements: [DataRequirement.STRATEGIC, DataRequirement.MARKET],
    outputType: OutputType.OPPORTUNITIES,
    primaryUseCase: 'Partnership strategy',
    limitations: ['Ecosystem complexity']
  },
  {
    id: 'stakeholder_mapping',
    name: 'Stakeholder Power/Interest Grid',
    category: FrameworkCategory.ORGANIZATIONAL,
    description: 'Maps stakeholders by power and interest levels',
    complexity: 'basic',
    timeToImplement: '2-3 hours',
    visualizationType: VisualizationType.MATRIX_2X2,
    analysisType: AnalysisType.MAPPING,
    dataRequirements: [DataRequirement.STRATEGIC],
    outputType: OutputType.PRIORITIES,
    primaryUseCase: 'Stakeholder management',
    limitations: ['Dynamic relationships']
  },
  {
    id: 'network_effects_analysis',
    name: 'Network Effects Analysis',
    category: FrameworkCategory.DIGITAL,
    description: 'Analyzes direct, indirect, and cross-side network effects',
    complexity: 'advanced',
    timeToImplement: '1-2 weeks',
    visualizationType: VisualizationType.NETWORK,
    analysisType: AnalysisType.ASSESSMENT,
    dataRequirements: [DataRequirement.CUSTOMER, DataRequirement.PRODUCT],
    outputType: OutputType.SCORE,
    primaryUseCase: 'Platform strategy',
    limitations: ['Measurement complexity']
  }
];

// Helper function to get frameworks by category
export function getFrameworksByCategory(category: FrameworkCategory): FrameworkMetadata[] {
  return BUSINESS_FRAMEWORKS.filter(f => f.category === category);
}

// Helper function to get frameworks by complexity
export function getFrameworksByComplexity(complexity: string): FrameworkMetadata[] {
  return BUSINESS_FRAMEWORKS.filter(f => f.complexity === complexity);
}

// Helper function to get frameworks suitable for specific data availability
export function getFrameworksByDataRequirements(availableData: DataRequirement[]): FrameworkMetadata[] {
  return BUSINESS_FRAMEWORKS.filter(framework => 
    framework.dataRequirements.every(req => availableData.includes(req))
  );
}

// Helper function to get framework by ID
export function getFrameworkById(id: string): FrameworkMetadata | undefined {
  return BUSINESS_FRAMEWORKS.find(f => f.id === id);
}

// Get total framework count
export function getTotalFrameworkCount(): number {
  return BUSINESS_FRAMEWORKS.length;
}