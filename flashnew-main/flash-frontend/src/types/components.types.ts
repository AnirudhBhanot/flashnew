// Component-specific type definitions

import { StartupData, PredictionResult } from '../types';
import { ApiPredictionResult, EnrichedAnalysisData, ConfigField } from './api.types';

// Phase types for the application flow
export type AppPhase = 'landing' | 'collecting' | 'analyzing' | 'results';

// Props types for main components
export interface DataCollectionCAMPProps {
  onSubmit: (data: StartupData) => void;
  onBack?: () => void;
}

export interface HybridAnalysisPageProps {
  startupData: StartupData;
  onComplete: (results: EnrichedAnalysisData) => void;
  onBack: () => void;
}

export interface AnalysisResultsProps {
  data: EnrichedAnalysisData;
  onBack: () => void;
}

export interface HybridResultsProps {
  data: EnrichedAnalysisData;
}

// Investment memo types
export interface InvestmentMemoProps {
  data: EnrichedAnalysisData;
  onClose: () => void;
}

export interface MemoSection {
  title: string;
  content: string | string[];
  highlight?: boolean;
}

// Chart and visualization types
export interface CAMPRadarChartProps {
  scores: {
    capital: number;
    advantage: number;
    market: number;
    people: number;
  };
  thresholds?: {
    capital: number;
    advantage: number;
    market: number;
    people: number;
  };
  size?: number;
}

export interface ConfidenceVisualizationProps {
  probability: number;
  confidence: number;
  interval: {
    lower: number;
    upper: number;
  };
}

// Model contribution types
export interface ModelContribution {
  name: string;
  weight: number;
  prediction: number;
  contribution: number;
}

export interface ModelContributionsProps {
  contributions: Record<string, number>;
  finalPrediction: number;
}

// Pattern analysis types
export interface PatternInsight {
  pattern: string;
  confidence: number;
  description: string;
  implications: string[];
}

export interface PatternAnalysisProps {
  patterns: string[];
  insights: PatternInsight[];
}

// Dynamic prediction display types
export interface DynamicPredictionResult {
  success_probability: number;
  confidence_interval: {
    lower: number;
    upper: number;
    width: number;
  };
  verdict: string;
  verdict_confidence: string;
  uncertainty_level: string;
  factors: Array<{
    factor: string;
    impact: 'positive' | 'negative';
    strength: string;
    description: string;
  }>;
  warnings?: string[];
}

export interface DynamicPredictionDisplayProps {
  result: DynamicPredictionResult;
  onScenarioClick: () => void;
}

// Assessment component types
export interface BusinessInsightsProps {
  insights: string[];
  metrics: {
    marketFit: number;
    productReadiness: number;
    scalability: number;
  };
}

export interface RiskAssessmentProps {
  riskLevel: string;
  criticalFailures: string[];
  riskFactors: Array<{
    category: string;
    severity: 'high' | 'medium' | 'low';
    description: string;
  }>;
}

export interface InvestmentReadinessProps {
  verdict: string;
  confidence: number;
  readinessScore: number;
  keyStrengths: string[];
  areasForImprovement: string[];
}

// Configuration admin types
export interface ConfigurationAdminProps {
  onClose: () => void;
}

// Results router types
export interface ResultsRouterProps {
  results: ApiPredictionResult | EnrichedAnalysisData;
  onBack: () => void;
}

// Field error types
export type FieldErrors = Record<string, string>;

// CAMP pillar types
export interface CAMPPillar {
  name: string;
  icon: string;
  fields: string[];
}

export type CAMPPillarKey = 'capital' | 'advantage' | 'market' | 'people';