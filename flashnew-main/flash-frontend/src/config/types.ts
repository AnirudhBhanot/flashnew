/**
 * Configuration Type Definitions
 * Enterprise-grade type system for FLASH configuration management
 */

// Core configuration interface
export interface IConfiguration {
  version: string;
  environment: 'development' | 'staging' | 'production';
  features: IFeatureFlags;
  thresholds: IThresholds;
  defaults: IDefaults;
  ui: IUIConfiguration;
  business: IBusinessRules;
  messages: IMessages;
  experimental: IExperimentalFeatures;
}

// Feature flags for enabling/disabling features
export interface IFeatureFlags {
  llmRecommendations: boolean;
  industryBenchmarks: boolean;
  whatIfAnalysis: boolean;
  exportPDF: boolean;
  advancedMetrics: boolean;
  adminPanel: boolean;
  debugMode: boolean;
}

// Threshold configurations with stage/sector overrides
export interface IThresholds {
  success: ISuccessThresholds;
  risk: IRiskThresholds;
  performance: IPerformanceThresholds;
  metrics: IMetricThresholds;
}

export interface ISuccessThresholds {
  probability: IProbabilityThresholds;
  improvements: IImprovementThresholds;
  confidence: IConfidenceThresholds;
}

export interface IProbabilityThresholds {
  excellent: number;
  good: number;
  fair: number;
  poor: number;
  // Stage-specific overrides
  byStage?: {
    [stage: string]: {
      excellent: number;
      good: number;
      fair: number;
      poor: number;
    };
  };
  // Sector-specific overrides
  bySector?: {
    [sector: string]: {
      excellent: number;
      good: number;
      fair: number;
      poor: number;
    };
  };
}

export interface IImprovementThresholds {
  maxImprovement: number;
  perActionImprovement: number;
  milestoneActions: number[];
  algorithm: 'linear' | 'logarithmic' | 'exponential' | 'custom';
  // Custom calculation function
  calculateImprovement?: (current: number, actions: number, context?: IContext) => number;
}

export interface IConfidenceThresholds {
  veryHigh: number;
  high: number;
  moderate: number;
  low: number;
}

export interface IRiskThresholds {
  runway: {
    critical: number;
    warning: number;
    safe: number;
    comfortable: number;
    byStage?: Record<string, { critical: number; warning: number; safe: number; comfortable: number }>;
  };
  burnMultiple: {
    excellent: number;
    good: number;
    warning: number;
    critical: number;
    byStage?: Record<string, { excellent: number; good: number; warning: number; critical: number }>;
  };
  concentration: {
    low: number;
    medium: number;
    high: number;
    extreme: number;
  };
  churn: {
    excellent: number;
    good: number;
    warning: number;
    critical: number;
  };
}

export interface IPerformanceThresholds {
  revenue: {
    growth: {
      hypergrowth: number;
      high: number;
      moderate: number;
      low: number;
      byStage?: Record<string, { hypergrowth: number; high: number; moderate: number; low: number }>;
    };
  };
  ltv_cac: {
    excellent: number;
    good: number;
    fair: number;
    poor: number;
    bySector?: Record<string, { excellent: number; good: number; fair: number; poor: number }>;
  };
  grossMargin: {
    excellent: number;
    good: number;
    fair: number;
    poor: number;
    bySector?: Record<string, { excellent: number; good: number; fair: number; poor: number }>;
  };
}

export interface IMetricThresholds {
  team: {
    size: {
      minimum: number;
      optimal: number;
      maximum: number;
      byStage?: Record<string, { minimum: number; optimal: number; maximum: number }>;
    };
    experience: {
      junior: number;
      mid: number;
      senior: number;
      expert: number;
    };
    diversity: {
      low: number;
      moderate: number;
      high: number;
      excellent: number;
    };
  };
  market: {
    tam: {
      small: number;
      medium: number;
      large: number;
      huge: number;
    };
    competition: {
      low: number;
      medium: number;
      high: number;
      extreme: number;
    };
    growth: {
      declining: number;
      stable: number;
      growing: number;
      explosive: number;
    };
  };
  product: {
    nps: {
      poor: number;
      fair: number;
      good: number;
      excellent: number;
    };
    retention: {
      poor: number;
      fair: number;
      good: number;
      excellent: number;
    };
  };
}

// Default values for missing data
export interface IDefaults {
  confidence: number;
  probability: number;
  runway: number;
  burnMultiple: number;
  teamSize: number;
  experience: number;
  grossMargin: number;
  ltvCac: number;
  churnRate: number;
  nps: number;
}

// UI configuration for visual elements
export interface IUIConfiguration {
  animation: IAnimationConfig;
  charts: IChartConfig;
  colors: IColorConfig;
  layout: ILayoutConfig;
  numbers: INumberConfig;
  display: {
    emojis: {
      excellent: string;
      good: string;
      fair: string;
      poor: string;
    };
    limits: {
      strengths: number;
      risks: number;
      recommendations: number;
      patterns: number;
    };
  };
}

export interface IAnimationConfig {
  enabled: boolean;
  duration: {
    fast: number;
    normal: number;
    slow: number;
  };
  delay: {
    short: number;
    medium: number;
    long: number;
  };
  type: string;
  easing: string;
  reducedMotion: boolean;
  springConfig: {
    stiffness: number;
    damping: number;
    mass: number;
  };
}

export interface IChartConfig {
  radar: {
    radius: number;
    levels: number;
    pointRadius: number;
    labelOffset: number;
    strokeWidth: number;
    responsive: boolean;
  };
  colors: {
    success: string;
    warning: string;
    danger: string;
    info: string;
    neutral: string;
    gradients: boolean;
    opacity: {
      fill: number;
      stroke: number;
      hover: number;
    };
  };
}

export interface IColorConfig {
  brand: {
    primary: string;
    secondary: string;
    accent: string;
  };
  semantic: {
    success: string;
    warning: string;
    danger: string;
    info: string;
  };
  chart: {
    series: string[];
    background: string;
    grid: string;
  };
  text: {
    primary: string;
    secondary: string;
    disabled: string;
    inverse: string;
  };
  background: {
    primary: string;
    secondary: string;
    elevated: string;
    overlay: string;
  };
}

export interface ILayoutConfig {
  maxWidth: number;
  spacing: {
    xs: number;
    sm: number;
    md: number;
    lg: number;
    xl: number;
  };
  borderRadius: {
    sm: number;
    md: number;
    lg: number;
    full: number;
  };
  breakpoints: {
    mobile: number;
    tablet: number;
    desktop: number;
    wide: number;
  };
}

export interface INumberConfig {
  percentageDecimals: number;
  currencyDecimals: number;
  scoreDecimals: number;
  locale: string;
  currency: string;
}

// Business rules configuration
export interface IBusinessRules {
  scoring: IScoringRules;
  validation: IValidationRules;
  calculation: ICalculationRules;
  stageWeights: Record<string, Record<string, number>>;
  analysis: {
    modelWeights: Record<string, number>;
    successFactors: number;
    patternCount: number;
  };
  benchmarks: {
    revenue: Record<string, { p25: number; p50: number; p75: number }>;
    growth: Record<string, { p25: number; p50: number; p75: number }>;
  };
}

export interface IScoringRules {
  algorithm: 'weighted' | 'ml' | 'hybrid';
  weights: {
    camp: {
      capital: number;
      advantage: number;
      market: number;
      people: number;
    };
    models: {
      dna: number;
      temporal: number;
      industry: number;
      ensemble: number;
    };
  };
  adjustments: {
    stageMultipliers: Record<string, number>;
    sectorMultipliers: Record<string, number>;
  };
}

export interface IValidationRules {
  required: string[];
  ranges: Record<string, { min: number; max: number }>;
  patterns: Record<string, RegExp>;
  custom: Record<string, (value: any, context?: IContext) => boolean>;
}

export interface ICalculationRules {
  burnRate: (raised: number, runway: number) => number;
  ltvCac: (ltv: number, cac: number) => number;
  growthRate: (current: number, previous: number) => number;
  marketShare: (revenue: number, tam: number) => number;
}

// User-facing messages
export interface IMessages {
  success: {
    excellent: string;
    good: string;
    fair: string;
    poor: string;
  };
  risk: {
    low: string;
    medium: string;
    high: string;
    critical: string;
  };
  improvements: {
    available: string;
    completed: string;
    milestone: string;
  };
  errors: {
    validation: string;
    network: string;
    calculation: string;
    generic: string;
  };
  recommendations: {
    capital: string[];
    advantage: string[];
    market: string[];
    people: string[];
  };
}

// Experimental features configuration
export interface IExperimentalFeatures {
  enableMLWhatIf: boolean;
  enableStreaming: boolean;
  enableWebSockets: boolean;
  enableOfflineMode: boolean;
  enableBetaFeatures: boolean;
  experiments: Record<string, IExperiment>;
}

export interface IExperiment {
  id: string;
  name: string;
  enabled: boolean;
  rolloutPercentage: number;
  variants: IVariant[];
  targeting?: ITargetingRule[];
}

export interface IVariant {
  id: string;
  name: string;
  weight: number;
  config: Partial<IConfiguration>;
}

export interface ITargetingRule {
  attribute: string;
  operator: 'equals' | 'contains' | 'greater' | 'less' | 'in' | 'not_in';
  value: any;
}

// Context for configuration resolution
export interface IContext {
  stage?: string;
  sector?: string;
  userId?: string;
  companyId?: string;
  revenue?: number;
  teamSize?: number;
  [key: string]: any;
}

// Configuration change tracking
export interface IConfigChange {
  path: string;
  oldValue: any;
  newValue: any;
  timestamp: number;
  userId?: string;
  reason?: string;
}

// Configuration validation
export interface IConfigValidation {
  isValid: boolean;
  errors: IConfigError[];
  warnings: IConfigWarning[];
}

export interface IConfigError {
  path: string;
  message: string;
  value: any;
  rule: string;
}

export interface IConfigWarning {
  path: string;
  message: string;
  suggestion?: string;
}

// Type guards
export const isConfiguration = (obj: any): obj is IConfiguration => {
  return obj && 
    typeof obj.version === 'string' &&
    typeof obj.environment === 'string' &&
    typeof obj.features === 'object' &&
    typeof obj.thresholds === 'object';
};

export const isContext = (obj: any): obj is IContext => {
  return obj && typeof obj === 'object';
};

// Utility types
export type DeepPartial<T> = {
  [P in keyof T]?: T[P] extends object ? DeepPartial<T[P]> : T[P];
};

export type ConfigPath = string; // Dot notation path like 'thresholds.success.probability.good'

export type ConfigValue = string | number | boolean | object | null;

export type ConfigGetter<T = any> = (path: ConfigPath, defaultValue?: T, context?: IContext) => T;

export type ConfigSetter = (path: ConfigPath, value: ConfigValue) => void;

export type ConfigSubscriber = (config: IConfiguration, changes?: IConfigChange[]) => void;