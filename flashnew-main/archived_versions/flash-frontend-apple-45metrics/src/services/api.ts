// API Service for FLASH Apple UI - Aligned with Backend Features
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

// Transform assessment data to API format (45 features) - Direct mapping
function transformAssessmentToAPI(data: AssessmentData): any {
  const {
    companyInfo = {},
    capital = {},
    advantage = {},
    market = {},
    people = {},
    product = {}
  } = data;

  // Direct mapping of all 45 backend features
  return {
    // Capital features (7)
    total_capital_raised_usd: Number(capital.totalCapitalRaisedUsd) || 0,
    cash_on_hand_usd: Number(capital.cashOnHandUsd) || 0,
    monthly_burn_usd: Number(capital.monthlyBurnUsd) || 0,
    runway_months: Number(capital.runwayMonths) || 0,
    burn_multiple: Number(capital.burnMultiple) || 2.5,
    investor_tier_primary: capital.investorTierPrimary || 'tier_3',
    has_debt: Boolean(capital.hasDebt),
    
    // Advantage features (8)
    patent_count: Number(advantage.patentCount) || 0,
    network_effects_present: Boolean(advantage.networkEffectsPresent),
    has_data_moat: Boolean(advantage.hasDataMoat),
    regulatory_advantage_present: Boolean(advantage.regulatoryAdvantagePresent),
    tech_differentiation_score: Number(advantage.techDifferentiationScore) || 3,
    switching_cost_score: Number(advantage.switchingCostScore) || 3,
    brand_strength_score: Number(advantage.brandStrengthScore) || 3,
    scalability_score: Number(advantage.scalabilityScore) || 3,
    
    // Market features (11)
    sector: market.sector || companyInfo.industry || 'saas',
    tam_size_usd: Number(market.tamSizeUsd) || 0,
    sam_size_usd: Number(market.samSizeUsd) || 0,
    som_size_usd: Number(market.somSizeUsd) || 0,
    market_growth_rate_percent: Number(market.marketGrowthRatePercent) || 0,
    customer_count: Number(market.customerCount) || 0,
    customer_concentration_percent: Number(market.customerConcentrationPercent) || 20,
    user_growth_rate_percent: Number(market.userGrowthRatePercent) || 0,
    net_dollar_retention_percent: Number(market.netDollarRetentionPercent) || 100,
    competition_intensity: market.competitionIntensity === 'low' ? 2 : market.competitionIntensity === 'high' ? 4 : 3,
    competitors_named_count: Number(market.competitorsNamedCount) || 0,
    
    // People features (10)
    founders_count: Number(people.foundersCount) || 1,
    team_size_full_time: Number(people.teamSizeFullTime) || 1,
    years_experience_avg: Number(people.yearsExperienceAvg) || 0,
    domain_expertise_years_avg: Number(people.domainExpertiseYearsAvg) || 0,
    prior_startup_experience_count: Number(people.priorStartupExperienceCount) || 0,
    prior_successful_exits_count: Number(people.priorSuccessfulExitsCount) || 0,
    board_advisor_experience_score: Number(people.boardAdvisorExperienceScore) || 3,
    advisors_count: Number(people.advisorsCount) || 0,
    team_diversity_percent: Number(people.teamDiversityPercent) || 30,
    key_person_dependency: Boolean(people.keyPersonDependency),
    
    // Product features (9)
    product_stage: product.productStage || 'mvp',
    product_retention_30d: Number(product.productRetention30d) / 100 || 0.7,
    product_retention_90d: Number(product.productRetention90d) / 100 || 0.5,
    dau_mau_ratio: Number(product.dauMauRatio) / 100 || 0.4,
    annual_revenue_run_rate: Number(product.annualRevenueRunRate) || 0,
    revenue_growth_rate_percent: Number(product.revenueGrowthRatePercent) || 0,
    gross_margin_percent: Number(product.grossMarginPercent) || 70,
    ltv_cac_ratio: Number(product.ltvCacRatio) || 3,
    funding_stage: companyInfo.fundingStage || 'seed'
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
    
    // Check required fields
    if (!apiData.total_capital_raised_usd && apiData.total_capital_raised_usd !== 0) {
      errors.push('Total capital raised is required');
    }
    if (!apiData.monthly_burn_usd && apiData.monthly_burn_usd !== 0) {
      errors.push('Monthly burn rate is required');
    }
    if (!apiData.tam_size_usd || apiData.tam_size_usd === 0) {
      errors.push('Total addressable market is required');
    }
    if (!apiData.founders_count || apiData.founders_count === 0) {
      errors.push('Number of founders is required');
    }
    if (!apiData.team_size_full_time || apiData.team_size_full_time === 0) {
      errors.push('Team size is required');
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