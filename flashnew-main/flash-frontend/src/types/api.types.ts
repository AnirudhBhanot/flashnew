// API-specific type definitions

import { StartupData, PredictionResult } from '../types';

// Base API response structure
export interface ApiResponse<T> {
  data?: T;
  error?: string;
  status: number;
}

// Extended prediction result from API
export interface ApiPredictionResult extends Omit<PredictionResult, 'verdict'> {
  success_probability: number;
  confidence_score: number;
  confidence_interval: {
    lower: number;
    upper: number;
    width: number;
  };
  verdict: string; // API can return more verdict types than the base interface
  verdict_confidence: string;
  risk_level: string;
  pillar_scores: {
    capital: number;
    advantage: number;
    market: number;
    people: number;
  };
  camp_scores?: {
    capital: number;
    advantage: number;
    market: number;
    people: number;
  };
  key_insights: string[];
  recommendations?: string[];
  
  // Advanced analysis fields
  model_components?: {
    base: number;
    patterns: number;
    stage: number;
    industry: number;
    camp_avg: number;
  };
  model_breakdown?: Record<string, number>;
  dominant_patterns?: string[];
  all_predictions?: {
    base: number;
    patterns: number;
    stage: number;
    industry: number;
    camp: number;
  };
  
  // Pattern analysis
  dna_pattern?: {
    pattern_type: string;
    confidence: number;
    characteristics: string[];
  };
  
  // Temporal predictions
  temporal_predictions?: {
    short_term: number;
    medium_term: number;
    long_term: number;
  };
  
  // Industry insights
  industry_insights?: {
    relative_performance: string;
    key_challenges: string[];
    opportunities: string[];
  };
  
  // Stage-specific insights
  stage_prediction?: {
    current_stage_fit: number;
    next_stage_readiness: number;
    key_milestones: string[];
  };
}

// Configuration API types
export interface ConfigField {
  key: string;
  value: string | number | boolean;
  type: 'string' | 'number' | 'boolean';
  category: string;
  description?: string;
  min?: number;
  max?: number;
}

export interface ConfigResponse {
  fields: ConfigField[];
  categories: string[];
  lastUpdated: string;
}

// Analysis enriched data
export interface EnrichedAnalysisData extends ApiPredictionResult {
  userInput: StartupData;
  timestamp: string;
  analysisId: string;
  funding_stage?: string;
  industry?: string;
  runway_months?: number;
  burn_multiple?: number;
  revenue_growth_rate_percent?: number;
  team_size_full_time?: number;
  years_experience_avg?: number;
  tam_size_usd?: number;
  current_arr?: number;
  ltv_cac_ratio?: number;
  net_dollar_retention_percent?: number;
  customer_concentration_percent?: number;
  last_round_raised_usd?: number;
  market_growth_rate?: number;
  competition_intensity?: number;
  has_patent?: boolean;
  technology_score?: number;
  scalability_score?: number;
  advisor_quality_score?: number;
  stage_fit?: string;
  industry_fit?: string;
}

// Form field configuration
export interface FieldConfig {
  label: string;
  type: 'text' | 'number' | 'select' | 'boolean';
  placeholder?: string;
  helper?: string;
  min?: number;
  max?: number;
  step?: number;
  options?: Array<{ value: string; label: string }>;
}