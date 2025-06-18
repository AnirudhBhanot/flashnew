// API Service for FLASH - Fixed to match backend's 45 features
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

// Transform assessment data to match backend's exact 45 features
function transformAssessmentToAPI(data: AssessmentData): any {
  const {
    capital = {},
    advantage = {},
    market = {},
    people = {}
  } = data;

  return {
    // CAPITAL_FEATURES (7)
    total_capital_raised_usd: Number(capital.totalRaised) || 0,
    cash_on_hand_usd: Number(capital.cashOnHand) || 0,
    monthly_burn_usd: Number(capital.monthlyBurn) || 0,
    runway_months: Number(capital.runway) || 0,
    burn_multiple: Number(capital.burnMultiple) || 0,
    investor_tier_primary: capital.primaryInvestor || 'none',
    has_debt: capital.hasDebt ? 1 : 0,
    
    // ADVANTAGE_FEATURES (8)
    patent_count: Number(advantage.patentCount) || 0,
    network_effects_present: advantage.networkEffects ? 1 : 0,
    has_data_moat: advantage.hasDataMoat ? 1 : 0,
    regulatory_advantage_present: advantage.regulatoryAdvantage ? 1 : 0,
    tech_differentiation_score: Number(advantage.techDifferentiation) || 3,
    switching_cost_score: Number(advantage.switchingCosts) || 3,
    brand_strength_score: Number(advantage.brandStrength) || 3,
    scalability_score: Number(advantage.scalability) || 3,
    
    // MARKET_FEATURES (11)
    sector: market.sector || 'other',
    tam_size_usd: Number(market.tam) || 0,
    sam_size_usd: Number(market.sam) || 0,
    som_size_usd: Number(market.som) || 0,
    market_growth_rate_percent: Number(market.marketGrowthRate) || 0, // Already in percent
    customer_count: Number(market.customerCount) || 0,
    customer_concentration_percent: Number(market.customerConcentration) || 0, // Already in percent
    user_growth_rate_percent: Number(market.userGrowthRate) || 0, // Already in percent
    net_dollar_retention_percent: Number(market.netDollarRetention) || 100, // Already in percent
    competition_intensity: Number(market.competitionIntensity) || 3,
    competitors_named_count: Number(market.competitorCount) || 0,
    
    // PEOPLE_FEATURES (10)
    founders_count: Number(people.founderCount) || 1,
    team_size_full_time: Number(people.teamSize) || 1,
    years_experience_avg: Number(people.avgExperience) || 0,
    domain_expertise_years_avg: Number(people.domainExpertiseYears) || 0,
    prior_startup_experience_count: Number(people.priorStartupCount) || 0,
    prior_successful_exits_count: Number(people.priorExits) || 0,
    board_advisor_experience_score: Number(people.boardAdvisorScore) || 3,
    advisors_count: Number(people.advisorCount) || 0,
    team_diversity_percent: Number(people.teamDiversity) || 0, // Already in percent
    key_person_dependency: people.keyPersonDependency ? 1 : 0,
    
    // PRODUCT_FEATURES (9)
    product_stage: advantage.productStage || 'mvp', // Moved from advantage form
    product_retention_30d: Number(people.productRetention30d) / 100 || 0.5, // Convert percent to decimal
    product_retention_90d: Number(people.productRetention90d) / 100 || 0.3, // Convert percent to decimal
    dau_mau_ratio: Number(people.dauMauRatio) / 100 || 0.2, // Convert percent to decimal
    annual_revenue_run_rate: Number(capital.annualRevenueRunRate) || 0, // From capital form
    revenue_growth_rate_percent: Number(market.revenueGrowthRate) || 0, // Already in percent, from market form
    gross_margin_percent: Number(market.grossMargin) || 0, // Already in percent, from market form
    ltv_cac_ratio: Number(market.ltvCacRatio) || 0, // From market form
    funding_stage: capital.fundingStage || 'seed', // From capital form
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
    
    // Validate all 45 required fields
    const errors: string[] = [];
    const requiredFields = [
      // Capital
      'total_capital_raised_usd', 'cash_on_hand_usd', 'monthly_burn_usd', 
      'runway_months', 'investor_tier_primary', 'funding_stage',
      
      // Market
      'sector', 'tam_size_usd', 'sam_size_usd', 'som_size_usd',
      'market_growth_rate_percent', 'customer_count',
      
      // People
      'founders_count', 'team_size_full_time', 'years_experience_avg',
      'domain_expertise_years_avg',
      
      // Advantage
      'product_stage',
    ];
    
    for (const field of requiredFields) {
      if (apiData[field] === undefined || apiData[field] === null || 
          (typeof apiData[field] === 'number' && isNaN(apiData[field]))) {
        errors.push(`${field} is required`);
      }
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