// API Service for FLASH Apple UI - Complete 45-Metric Version
import { AssessmentData } from '../store/assessmentStore';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8001';
const API_KEY = process.env.REACT_APP_API_KEY || '';

// Helper to handle API errors
class APIError extends Error {
  constructor(public status: number, message: string, public data?: any) {
    super(message);
    this.name = 'APIError';
  }
}

// Helper for API calls
async function apiCall<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const url = `${API_BASE_URL}${endpoint}`;
  
  try {
    const headers: Record<string, string> = {
      'Content-Type': 'application/json',
      ...options.headers,
    };
    
    // Only add API key if it's configured
    if (API_KEY) {
      headers['X-API-Key'] = API_KEY;
    }
    
    const response = await fetch(url, {
      ...options,
      headers,
    });

    const data = await response.json();

    if (!response.ok) {
      throw new APIError(response.status, data.detail || 'API request failed', data);
    }

    return data;
  } catch (error) {
    if (error instanceof APIError) {
      throw error;
    }
    throw new Error(`Network error: ${error instanceof Error ? error.message : 'Unknown error'}`);
  }
}

// Transform assessment data to API format (complete 45-field version)
function transformAssessmentToAPI(data: AssessmentData): any {
  const {
    companyInfo = {},
    capital = {},
    advantage = {},
    market = {},
    product = {},
    people = {}
  } = data;

  // Calculate founding year from date
  const foundingYear = companyInfo.foundingDate ? 
    new Date(companyInfo.foundingDate).getFullYear() : 
    new Date().getFullYear();

  return {
    // Company Info (3 fields)
    company_name: companyInfo.companyName || '',
    industry: companyInfo.industry || '',
    founding_year: foundingYear,
    
    // Capital features (6 fields)
    funding_stage: capital.fundingStage || 'seed',
    total_funding: Number(capital.totalRaised) || 0,
    monthly_revenue: Number(capital.monthlyRevenue) || 0,
    burn_rate: Number(capital.monthlyBurn) || 0,
    runway_months: Number(capital.runway) || 12,
    has_revenue: Boolean(capital.hasRevenue),
    
    // Additional capital metrics (2 fields)
    burn_multiple: Number(capital.burnMultiple) || 0,
    ltv_cac_ratio: Number(capital.ltvCacRatio) || 0,
    
    // Market features (5 fields)
    sector: market.sector || 'other',
    market_size: Number(market.marketSize || market.tam) || 0,
    market_growth_rate: Number(market.marketGrowthRate || market.growthRate) / 100 || 0, // Convert percentage to decimal
    competition_level: Number(market.competitionLevel || market.competitionIntensity) || 3,
    market_risk_score: Number(market.marketRiskScore) || 3,
    
    // People features (8 fields)
    team_size: Number(people.teamSize) || 1,
    founder_experience: Number(people.founderExperience) || 5,
    technical_skill: Number(people.technicalSkill) || 5,
    business_skill: Number(people.businessSkill) || 5,
    industry_experience: Number(people.industryExperience) || 5,
    technical_founder: Boolean(people.hasTechnicalFounder || people.technicalSkill > 7),
    team_diversity_score: Number(people.teamDiversityScore) / 100 || 0.6, // Convert percentage to decimal
    team_experience_score: Number(people.teamExperienceScore) || 3.5,
    
    // Advantage features (6 fields)
    product_stage: advantage.productStage || 'mvp',
    moat_strength: Number(advantage.moatStrength) || 5,
    unique_advantage: advantage.uniqueAdvantage || '',
    patents_count: Number(advantage.patentCount) || 0,
    competitive_moat_score: Number(advantage.competitiveMoatScore) || 5,
    technology_score: Number(advantage.technologyScore) || 5,
    
    // Product metrics (15 fields)
    retention_rate_monthly: Number(product.retentionRate) / 100 || 0.85, // Convert percentage to decimal
    daily_active_users: Number(product.dailyActiveUsers) || 1000,
    monthly_active_users: Number(product.monthlyActiveUsers) || 10000,
    product_market_fit_score: Number(product.productMarketFitScore) || 3.5,
    feature_adoption_rate: Number(product.featureAdoptionRate) / 100 || 0.7, // Convert percentage to decimal
    user_engagement_score: Number(product.userEngagementScore) || 3.5,
    time_to_value_days: Number(product.timeToValueDays) || 7,
    product_stickiness: Number(product.productStickiness) / 100 || 0.3, // Convert percentage to decimal
    activation_rate: Number(product.activationRate) / 100 || 0.6, // Convert percentage to decimal
    customer_lifetime_value: Number(product.customerLifetimeValue) || 10000,
    average_deal_size: Number(product.averageDealSize) || 5000,
    customer_satisfaction_score: Number(product.customerSatisfactionScore) || 8,
    sales_cycle_days: Number(product.salesCycleDays) || 30,
    gross_margin: Number(product.grossMargin) / 100 || 0.7, // Convert percentage to decimal
    revenue_growth_rate: Number(product.revenueGrowthRate) / 100 || 1.0, // Convert percentage to decimal
    
    // Additional scores (3 fields)
    capital_efficiency_score: Number(product.capitalEfficiencyScore) || 3.5,
    execution_risk_score: Number(people.executionRiskScore) || 3,
    financial_risk_score: Number(market.financialRiskScore) || 3,
    
    // Business model score (1 field)
    business_model_score: Number(advantage.businessModelScore) || 5,
  };
}

// API Service methods
export const apiService = {
  // Export transformation function
  transformAssessmentToAPI,
  
  // Health check
  async health() {
    return apiCall<{ status: string; models_loaded: number }>('/health');
  },

  // Main prediction endpoint
  async predict(data: AssessmentData) {
    const apiData = transformAssessmentToAPI(data);
    return apiCall<{
      success_probability: number;
      verdict: string;
      confidence: string;
      risk_level: string;
      camp_scores: {
        capital: number;
        advantage: number;
        market: number;
        people: number;
      };
      insights?: string[];
      confidence_interval?: {
        lower: number;
        upper: number;
      };
    }>('/predict', {
      method: 'POST',
      body: JSON.stringify(apiData),
    });
  },

  // Enhanced analysis with LLM
  async analyze(data: AssessmentData) {
    const apiData = transformAssessmentToAPI(data);
    return apiCall<{
      status: string;
      analysis: {
        strengths: string[];
        weaknesses: string[];
        opportunities: string[];
        threats: string[];
        key_metrics: any;
        recommendations: string[];
        benchmark_comparison?: any;
        risk_factors: string[];
        growth_potential: any;
      };
    }>('/analyze', {
      method: 'POST',
      body: JSON.stringify(apiData),
    });
  },

  // LLM recommendations
  async getRecommendations(data: AssessmentData, results?: any) {
    const apiData = transformAssessmentToAPI(data);
    
    // Format the request according to backend expectations
    const requestData = {
      startup_data: apiData,
      scores: {
        capital: results?.scores?.capital || 0.5,
        advantage: results?.scores?.advantage || 0.5,
        market: results?.scores?.market || 0.5,
        people: results?.scores?.people || 0.5,
        success_probability: results?.successProbability || 0.5
      },
      verdict: results?.verdict || 'CONDITIONAL'
    };
    
    return apiCall<{
      recommendations: Array<{
        category: string;
        priority: string;
        recommendation: string;
        impact: string;
        effort: string;
        timeline: string;
      }>;
      key_insights: string[];
      action_items: string[];
    }>('/api/analysis/recommendations/dynamic', {
      method: 'POST',
      body: JSON.stringify(requestData),
    });
  },

  // Pattern analysis
  async getPatterns() {
    return apiCall<{
      patterns: Array<{
        name: string;
        description: string;
        success_rate: number;
        sample_size: number;
      }>;
    }>('/patterns');
  },

  // Investor profiles
  async getInvestorProfiles() {
    return apiCall<{
      profiles: Array<{
        name: string;
        type: string;
        focus_areas: string[];
        typical_check_size: string;
        stage_preference: string[];
      }>;
    }>('/investor_profiles');
  },

  // Metrics
  async getMetrics() {
    return apiCall<{
      total_predictions: number;
      average_success_rate: number;
      model_performance: any;
    }>('/metrics');
  },

  // Report generation
  async generateReport(data: AssessmentData) {
    const apiData = transformAssessmentToAPI(data);
    return apiCall<{
      report_id: string;
      status: string;
      download_url?: string;
    }>('/report/generate', {
      method: 'POST',
      body: JSON.stringify(apiData),
    });
  },
  
  // Validate data before submission
  async validateData(data: AssessmentData) {
    const apiData = transformAssessmentToAPI(data);
    
    // Basic validation
    const errors: string[] = [];
    
    // Check required Capital fields
    if (!apiData.funding_stage) {
      errors.push('Funding stage is required');
    }
    if (!apiData.total_funding && apiData.total_funding !== 0) {
      errors.push('Total funding is required');
    }
    if (!apiData.burn_rate && apiData.burn_rate !== 0) {
      errors.push('Monthly burn rate is required');
    }
    if (!apiData.runway_months) {
      errors.push('Runway is required');
    }
    
    // Check required Market fields
    if (!apiData.market_size || apiData.market_size === 0) {
      errors.push('Market size is required');
    }
    
    // Check required People fields
    if (!apiData.team_size || apiData.team_size === 0) {
      errors.push('Team size is required');
    }
    
    // Check required Advantage fields
    if (!apiData.product_stage) {
      errors.push('Product stage is required');
    }
    
    // Check if Product data exists
    if (!data.product) {
      errors.push('Product metrics are required');
    }
    
    return {
      valid: errors.length === 0,
      errors,
      data: apiData
    };
  },
  
  // Check API health
  async checkHealth() {
    try {
      const response = await this.health();
      return response.status === 'healthy';
    } catch (error) {
      return false;
    }
  },
  
  // Submit assessment (wrapper for predict)
  async submitAssessment(data: AssessmentData) {
    const prediction = await this.predict(data);
    
    // Transform response to match frontend expectations
    return {
      successProbability: prediction.success_probability,
      confidence: prediction.confidence,
      verdict: prediction.verdict,
      riskLevel: prediction.risk_level,
      scores: prediction.camp_scores,
      insights: prediction.insights || [],
      confidenceInterval: prediction.confidence_interval
    };
  },
  
  // Get detailed analysis (wrapper for analyze)
  async getDetailedAnalysis(data: AssessmentData) {
    const analysis = await this.analyze(data);
    return {
      status: analysis.status,
      detailedAnalysis: analysis.analysis
    };
  }
};