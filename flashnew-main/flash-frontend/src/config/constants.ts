/**
 * Central configuration for all application constants
 * These values should eventually come from a backend API or environment variables
 */

// Stage-specific CAMP weights
export const STAGE_WEIGHTS = {
  pre_seed: {
    people: 0.40,
    advantage: 0.30,
    market: 0.20,
    capital: 0.10
  },
  seed: {
    people: 0.30,
    advantage: 0.30,
    market: 0.25,
    capital: 0.15
  },
  series_a: {
    market: 0.30,
    people: 0.25,
    advantage: 0.25,
    capital: 0.20
  },
  series_b: {
    market: 0.35,
    capital: 0.25,
    advantage: 0.20,
    people: 0.20
  },
  series_c: {
    capital: 0.35,
    market: 0.30,
    people: 0.20,
    advantage: 0.15
  },
  growth: {
    capital: 0.35,
    market: 0.30,
    people: 0.20,
    advantage: 0.15
  }
};

// Model performance metrics (should come from API)
export const MODEL_PERFORMANCE = {
  dna_analyzer: { accuracy: 0.7674, name: "DNA Pattern Analyzer" },
  temporal_predictor: { accuracy: 0.7732, name: "Temporal Predictor" },
  industry_model: { accuracy: 0.7744, name: "Industry-Specific Model" },
  ensemble_model: { accuracy: 0.7700, name: "Ensemble Model" },
  pattern_matcher: { accuracy: 0.7700, name: "Pattern Matcher" },
  meta_learner: { accuracy: 0.7681, name: "Meta Learner" },
  overall_accuracy: 0.499,
  dataset_size: "100k"
};

// Score thresholds
export const SCORE_THRESHOLDS = {
  high: 0.8,
  medium: 0.6,
  low: 0.4,
  default_score: 0.5,
  default_confidence: 0.85,
  success_high: 0.7,
  success_medium: 0.5,
  success_low: 0.3
};

// Risk assessment thresholds
export const RISK_THRESHOLDS = {
  runway_months_critical: 3,
  runway_months_warning: 6,
  burn_multiple_high: 3,
  revenue_concentration_high: 0.3, // 30%
  churn_rate_high: 0.2, // 20%
  ltv_cac_low: 3
};

// Time periods for predictions
export const TIME_PERIODS = {
  short_term_months: 6,
  medium_term_months: 12,
  long_term_months: 18
};

// Company examples (should rotate or come from API)
export const COMPANY_EXAMPLES = {
  pre_seed: {
    company: "Airbnb",
    story: "Airbnb's founders were rejected by many VCs, but their persistence and execution skills turned a simple idea into a $75B company."
  },
  seed: {
    company: "Stripe",
    story: "Stripe succeeded because the Collison brothers (team) built dramatically better payment APIs (advantage) than existing solutions."
  },
  series_a: {
    company: "Uber",
    story: "Uber raised Series A after proving the ride-sharing market was massive and their model could scale beyond San Francisco."
  },
  series_b: {
    company: "DoorDash",
    story: "DoorDash's Series B focused on their path to market leadership and improving delivery economics."
  },
  series_c: {
    company: "Spotify",
    story: "Spotify's later rounds focused heavily on improving gross margins and reducing customer acquisition costs."
  },
  growth: {
    company: "Canva",
    story: "Canva maintained high growth while achieving profitability, making it attractive for growth investors."
  }
};

// Verdict configurations
export const VERDICT_CONFIG = {
  STRONG_PASS: {
    icon: '🚀',
    className: 'verdict-strong-pass',
    color: '#00C851',
    message: 'Exceptional opportunity',
    minProbability: 0.85
  },
  PASS: {
    icon: '✅',
    className: 'verdict-pass',
    color: '#00C851',
    message: 'Strong investment potential',
    minProbability: 0.7
  },
  CONDITIONAL_PASS: {
    icon: '⚡',
    className: 'verdict-conditional',
    color: '#FFD93D',
    message: 'Promising with conditions',
    minProbability: 0.5
  },
  FAIL: {
    icon: '⚠️',
    className: 'verdict-fail',
    color: '#FF8800',
    message: 'Significant improvements needed',
    minProbability: 0.3
  },
  STRONG_FAIL: {
    icon: '🔴',
    className: 'verdict-strong-fail',
    color: '#FF4444',
    message: 'Not ready for investment',
    minProbability: 0
  }
};

// Success probability thresholds and messages
export const SUCCESS_THRESHOLDS = {
  STRONG_INVESTMENT: {
    minProbability: 0.75,
    text: 'STRONG INVESTMENT OPPORTUNITY',
    emoji: '🚀',
    className: 'strong-yes'
  },
  PROMISING: {
    minProbability: 0.65,
    text: 'PROMISING OPPORTUNITY',
    emoji: '✨',
    className: 'yes'
  },
  CONDITIONAL: {
    minProbability: 0.55,
    text: 'PROCEED WITH CONDITIONS',
    emoji: '📊',
    className: 'conditional'
  },
  NEEDS_IMPROVEMENT: {
    minProbability: 0.45,
    text: 'NEEDS IMPROVEMENT',
    emoji: '🔧',
    className: 'needs-work'
  },
  NOT_READY: {
    minProbability: 0,
    text: 'NOT READY FOR INVESTMENT',
    emoji: '⚠️',
    className: 'not-ready'
  }
};

// Score color thresholds
export const SCORE_COLORS = {
  excellent: { min: 0.7, color: '#FFFFFF' },
  good: { min: 0.55, color: '#E8EAED' },
  fair: { min: 0.45, color: '#9CA3AF' },
  poor: { min: 0, color: '#6B7280' }
};

// Score range descriptions
export const SCORE_RANGES = [
  { min: 0, max: 45, label: '0-45%', className: 'poor', description: 'Needs significant improvement' },
  { min: 45, max: 55, label: '45-55%', className: 'fair', description: 'Shows potential with work' },
  { min: 55, max: 65, label: '55-65%', className: 'good', description: 'Strong foundation' },
  { min: 65, max: 75, label: '65-75%', className: 'excellent', description: 'Very promising' },
  { min: 75, max: 100, label: '75-100%', className: 'exceptional', description: 'Top tier opportunity' }
];

// Model weights configuration
export const MODEL_WEIGHTS = {
  base_analysis: { weight: 0.35, label: 'Base Analysis', percentage: '35%' },
  pattern_detection: { weight: 0.25, label: 'Pattern Detection', percentage: '25%' },
  stage_factors: { weight: 0.15, label: 'Stage Factors', percentage: '15%' },
  industry_specific: { weight: 0.15, label: 'Industry Specific', percentage: '15%' },
  camp_framework: { weight: 0.10, label: 'CAMP Framework', percentage: '10%' }
};

// Revenue growth benchmarks by stage
export const REVENUE_BENCHMARKS = {
  'pre_seed': { p25: '0%', p50: '0%', p75: '100%', threshold: 0 },
  'seed': { p25: '50%', p50: '150%', p75: '300%', threshold: 50 },
  'series_a': { p25: '100%', p50: '200%', p75: '400%', threshold: 100 },
  'series_b': { p25: '100%', p50: '200%', p75: '400%', threshold: 150 },
  'series_c': { p25: '75%', p50: '150%', p75: '300%', threshold: 100 },
  'growth': { p25: '50%', p50: '100%', p75: '200%', threshold: 75 }
};

// Burn multiple benchmarks
export const BURN_BENCHMARKS = {
  p25: '3.0x',
  p50: '2.0x',
  p75: '1.2x',
  excellent: 1.5,
  good: 2.0,
  warning: 2.5,
  critical: 3.0
};

// Valuation multiples based on growth
export const VALUATION_MULTIPLES = {
  base: 5,
  growth_200_plus: 10,
  growth_150_plus: 8,
  growth_100_plus: 6,
  growth_50_plus: 4
};

// Display limits
export const DISPLAY_LIMITS = {
  insights: 3,
  recommendations: 2,
  similar_companies: 3,
  strengths: 3,
  risks: 3,
  action_steps: 3,
  total_insights: 6
};

// Exit timeframes based on probability
export const EXIT_TIMEFRAMES = {
  high: { min: 0.80, timeframe: '3-5 years to major exit' },
  medium_high: { min: 0.65, timeframe: '4-6 years to exit' },
  medium: { min: 0.50, timeframe: '5-7 years to exit' },
  low: { min: 0, timeframe: '7+ years to potential exit' }
};

// Action plan timelines
export const ACTION_TIMELINES = {
  immediate: '30 days',
  short_term: '60 days',
  medium_term: '90 days',
  long_term: '6 months'
};

// Milestone timelines
export const MILESTONE_TIMELINES = {
  immediate: '0-3 months',
  short_term: '3-6 months',
  medium_term: '6-12 months',
  long_term: '12-24 months'
};

// Model counts and dataset info
export const MODEL_INFO = {
  total_models: 4,
  categories: 5,
  success_factors: 45,
  training_time: '56 seconds',
  dataset_size: '100k Real Startups'
};

// Retention period definitions
export const RETENTION_PERIODS = {
  short: { days: 30, label: '30-Day Retention (%)' },
  medium: { days: 90, label: '90-Day Retention (%)' },
  long: { days: 180, label: '180-Day Retention (%)' }
};

// Funding stage options
export const FUNDING_STAGE_OPTIONS = [
  { value: 'pre_seed', label: 'Pre-seed' },
  { value: 'seed', label: 'Seed' },
  { value: 'series_a', label: 'Series A' },
  { value: 'series_b', label: 'Series B' },
  { value: 'series_c', label: 'Series C' }
];

// Confidence interval calculations
export const CONFIDENCE_INTERVAL = {
  multiplier: 0.2,
  default_lower_bound: 0.05,
  default_upper_bound: 0.05
};

// Pattern analysis colors
export const PATTERN_COLORS = {
  growth: '#00C851',
  efficiency: '#E8EAED',
  market: '#FF8800',
  team: '#AA66CC',
  product: '#FFD93D',
  traction: '#00C896',
  risk: '#FF4444',
  other: '#78909C'
};

// Default values
export const DEFAULT_VALUES = {
  success_probability: 0.5,
  confidence_score: 0.85,
  risk_level: 'medium',
  funding_stage: 'seed',
  tam_size: 0,
  market_growth_rate: 0,
  runway_months: 12,
  burn_multiple: 2.0
};

// Model consensus thresholds
export const CONSENSUS_THRESHOLDS = {
  very_high: 0.85,
  high: 0.70,
  moderate: 0.50,
  low: 0
};

// Risk indicator positions (percentages)
export const RISK_INDICATOR_POSITIONS = {
  low: 87.5,
  medium: 62.5,
  high: 37.5,
  critical: 12.5
};

// Field validation configurations
export const FIELD_VALIDATION = {
  revenue_growth_rate_percent: { min: -100, max: 1000, placeholder: '100' },
  gross_margin_percent: { min: -100, max: 100, placeholder: '70' },
  ltv_cac_ratio: { min: 0, max: 100, step: 0.1, placeholder: '3' },
  customer_concentration_percent: { min: 0, max: 100, default: 20 },
  team_diversity_percent: { min: 0, max: 100, default: 40 },
  runway_months: { min: 0, max: 60, default: 12 },
  burn_multiple: { min: 0, max: 10, step: 0.1, default: 2 }
};

// Company comparables by sector and stage
export const COMPANY_COMPARABLES = {
  'SaaS': {
    'Series A': ['Slack at Series A ($340M → $28B)', 'Zoom at Series A ($30M → $100B)'],
    'Series B': ['Datadog at Series B ($94M → $40B)', 'Monday.com at Series B ($84M → $7B)']
  },
  'AI/ML': {
    'Series A': ['Hugging Face at Series A ($40M → $2B)', 'Scale AI at Series A ($100M → $7B)'],
    'Series B': ['Anthropic at Series B ($124M → $5B)', 'Cohere at Series B ($125M → $2B)']
  },
  'FinTech': {
    'Series A': ['Square at Series A ($10M → $100B)', 'Stripe at Series A ($2M → $95B)'],
    'Series B': ['Robinhood at Series B ($110M → $11B)', 'Coinbase at Series B ($75M → $85B)']
  },
  'HealthTech': {
    'Series A': ['Oscar Health at Series A ($30M → $7B)', 'Flatiron Health at Series A ($8M → $1.9B)'],
    'Series B': ['Tempus at Series B ($70M → $8B)', 'Ro at Series B ($88M → $7B)']
  },
  'E-commerce': {
    'Series A': ['Warby Parker at Series A ($12M → $3B)', 'Casper at Series A ($15M → $1.1B)'],
    'Series B': ['Glossier at Series B ($24M → $1.8B)', 'Allbirds at Series B ($17M → $1.7B)']
  }
};

// Investor tier options
export const INVESTOR_TIERS = [
  { value: 'tier_1', label: 'Tier 1', description: 'Top-tier VCs (Sequoia, a16z, etc.)' },
  { value: 'tier_2', label: 'Tier 2', description: 'Established VCs with strong track record' },
  { value: 'tier_3', label: 'Tier 3', description: 'Emerging VCs and regional funds' },
  { value: 'angel', label: 'Angel', description: 'Angel investors and syndicates' },
  { value: 'none', label: 'None', description: 'No institutional investors yet' }
];

// Industry sectors
export const INDUSTRY_SECTORS = [
  { value: 'saas', label: 'SaaS' },
  { value: 'ai_ml', label: 'AI/ML' },
  { value: 'fintech', label: 'FinTech' },
  { value: 'healthtech', label: 'HealthTech' },
  { value: 'ecommerce', label: 'E-commerce' },
  { value: 'marketplace', label: 'Marketplace' },
  { value: 'consumer', label: 'Consumer' },
  { value: 'enterprise', label: 'Enterprise' },
  { value: 'other', label: 'Other' }
];

// Temporal prediction periods
export const TEMPORAL_PERIODS = {
  short: { months: 6, label: '6 months' },
  medium: { months: 12, label: '12 months' },
  long: { months: 18, label: '18+ months' }
};

// Success comparison tiers
export const SUCCESS_COMPARISONS = {
  top_5: { min: 0.80, comparison: 'Top 5% of startups', likelihood: 'Very likely to achieve 10x+ returns' },
  top_10: { min: 0.65, comparison: 'Top 10% of startups', likelihood: 'Likely to achieve 5-10x returns' },
  top_25: { min: 0.50, comparison: 'Top 25% of startups', likelihood: 'Good chance of 3-5x returns' },
  average: { min: 0, comparison: 'Average startup', likelihood: 'Modest returns expected' }
};

// DNA pattern example companies
export const DNA_PATTERN_EXAMPLES = [
  'Stripe at Series A',
  'Airbnb at Series B',
  'Uber at Series A',
  'Slack at Seed',
  'Zoom at Series B',
  'Datadog at Series A'
];

// Profitability timeframes
export const PROFITABILITY_TIMEFRAMES = {
  aggressive: '12-18 months',
  moderate: '18-24 months',
  conservative: '24-36 months',
  extended: '36+ months'
};

// Performance benchmark thresholds
export const PERFORMANCE_BENCHMARKS = {
  revenue_growth: {
    excellent: 150,
    good: 100,
    fair: 50,
    poor: 0
  },
  burn_multiple: {
    excellent: 1.5,
    good: 2.0,
    fair: 2.5,
    poor: 3.0
  },
  ltv_cac: {
    excellent: 3.0,
    good: 2.0,
    fair: 1.5,
    poor: 1.0
  },
  gross_margin: {
    excellent: 80,
    good: 70,
    fair: 60,
    poor: 50
  }
};