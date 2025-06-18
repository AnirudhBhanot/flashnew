import { AssessmentData } from '../types/assessment';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8001';

// Core API call function with consistent error handling
async function apiCall<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const response = await fetch(`${API_URL}${endpoint}`, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({ detail: 'Unknown error' }));
    throw new Error(errorData.detail || `API error: ${response.status}`);
  }

  return response.json();
}

// Helper function to transform assessment data to API format
export function transformAssessmentToAPI(data: AssessmentData): any {
  // Extract form sections
  const capital = data.capital || {};
  const advantage = data.advantage || {};
  const market = data.market || {};
  const people = data.people || {};
  
  // Map investor tiers
  const mapInvestorTier = (tier: string): string => {
    const tierMap: { [key: string]: string } = {
      'Tier 1 VC': 'tier_1',
      'Tier 2 VC': 'tier_2',
      'Tier 3 VC': 'tier_3',
      'Angel': 'angel',
      'None': 'none',
      'tier1': 'tier_1',
      'tier2': 'tier_2',
      'tier3': 'tier_3',
      'angel': 'angel',
      'none': 'none',
      'university': 'university',
      'corporate': 'corporate',
      'government': 'government'
    };
    return tierMap[tier] || tier || 'none';
  };
  
  // Map sectors
  const mapSector = (sector: string): string => {
    const sectorMap: { [key: string]: string } = {
      'SaaS': 'saas',
      'E-commerce': 'ecommerce',
      'Marketplace': 'marketplace',
      'Fintech': 'fintech',
      'Healthtech': 'healthtech',
      'Healthcare': 'healthcare',
      'AI/ML': 'ai-ml',
      'ai-ml': 'ai-ml',
      'artificial-intelligence': 'ai-ml',
      'machine-learning': 'ai-ml',
      'Blockchain': 'blockchain',
      'blockchain': 'blockchain',
      'crypto': 'blockchain',
      'Crypto': 'blockchain',
      'Real Estate': 'real-estate',
      'real-estate': 'real-estate',
      'Transportation': 'transportation',
      'transportation': 'transportation',
      'Clean Tech': 'clean-tech',
      'clean-tech': 'clean-tech',
      'Deep Tech': 'deep-tech',
      'deep-tech': 'deep-tech',
      'Consumer': 'consumer',
      'Enterprise': 'enterprise',
      'B2B': 'b2b',
      'B2C': 'b2c',
      'Other': 'other'
    };
    return sectorMap[sector] || sector || 'other';
  };
  
  // Map product stages
  const mapProductStage = (stage: string): string => {
    const stageMap: { [key: string]: string } = {
      'Concept': 'concept',
      'MVP': 'mvp',
      'Beta': 'beta',
      'Live': 'launched',
      'Growing': 'scaling',
      'idea': 'concept',
      'research': 'mvp',
      'development': 'mvp',
      'alpha': 'beta',
      'live': 'launched',
      'scaling': 'scaling'
    };
    return stageMap[stage] || stage || 'mvp';
  };
  
  // Debug logging before transformation
  console.log('Raw data before transformation:', {
    capitalData: capital,
    marketData: market,
    peopleData: people,
    advantageData: advantage
  });
  
  // Build the 45-feature object in the exact order expected by the API
  const transformedData: any = {
    // CAPITAL_FEATURES (7)
    total_capital_raised_usd: Number(capital.totalRaised) || 0,
    cash_on_hand_usd: Number(capital.cashOnHand) || 0,
    monthly_burn_usd: Number(capital.monthlyBurn) || 0,
    runway_months: Number(capital.runway) || 0,
    burn_multiple: Number(capital.burnMultiple) || 0,
    investor_tier_primary: mapInvestorTier(capital.primaryInvestor || 'none'),
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
    sector: mapSector(market.sector || 'other'),
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
    product_stage: mapProductStage(advantage.productStage || 'mvp'), // From advantage form
    product_retention_30d: Number(market.productRetention30d) / 100 || 0.5, // Convert percent to decimal
    product_retention_90d: Number(market.productRetention90d) / 100 || 0.3, // Convert percent to decimal
    dau_mau_ratio: Number(market.dauMauRatio) / 100 || 0.2, // Convert percent to decimal
    annual_revenue_run_rate: Number(capital.annualRevenueRunRate) || 0, // From capital form
    revenue_growth_rate_percent: Number(market.revenueGrowthRate) || 0, // Already in percent, from market form
    gross_margin_percent: Number(market.grossMargin) || 0, // Already in percent, from market form
    ltv_cac_ratio: Number(market.ltvCacRatio) || 0, // From market form
    funding_stage: capital.fundingStage || 'seed', // From capital form
  };
  
  // Debug logging after transformation
  console.log('Transformed values:', {
    investor_tier_primary: transformedData.investor_tier_primary,
    sector: transformedData.sector,
    product_stage: transformedData.product_stage
  });
  
  return transformedData;
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
    
    // Log the transformed data to help debug
    console.log('API Data being sent:', apiData);
    console.log('API Data keys:', Object.keys(apiData).sort());
    console.log('Expected 45 features, sending:', Object.keys(apiData).length);
    
    // Check for any zero or missing critical values
    const missingFields = Object.entries(apiData).filter(([key, value]) => {
      if (typeof value === 'number' && value === 0) {
        // Some fields can legitimately be 0
        const canBeZero = ['has_debt', 'patent_count', 'network_effects_present', 'has_data_moat', 
                          'regulatory_advantage_present', 'key_person_dependency', 'ltv_cac_ratio',
                          'annual_revenue_run_rate', 'revenue_growth_rate_percent'];
        return !canBeZero.includes(key);
      }
      return value === null || value === undefined || value === '';
    });
    
    if (missingFields.length > 0) {
      console.warn('Fields with missing or zero values:', missingFields);
    }
    
    return apiCall<{
      success_probability: number;
      verdict: string;
      confidence: number;
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

  // Enhanced analysis endpoint
  async analyze(data: AssessmentData) {
    const apiData = transformAssessmentToAPI(data);
    return apiCall<{
      status: string;
      analysis: {
        strengths: string[];
        weaknesses: string[];
        opportunities: string[];
        threats: string[];
        recommendations: string[];
      };
    }>('/analyze', {
      method: 'POST',
      body: JSON.stringify(apiData),
    });
  },

  // Dynamic recommendations
  async getDynamicRecommendations(data: {
    assessment_data: AssessmentData;
    ml_results: any;
    startup_data?: AssessmentData;
    scores?: any;
  }) {
    const apiData = transformAssessmentToAPI(data.assessment_data);
    
    // Extract scores from ml_results if not provided
    const scores = data.scores || {
      capital: data.ml_results?.scores?.capital || 0,
      advantage: data.ml_results?.scores?.advantage || 0,
      market: data.ml_results?.scores?.market || 0,
      people: data.ml_results?.scores?.people || 0,
      success_probability: data.ml_results?.successProbability || 0
    };
    
    return apiCall<{
      recommendations: Array<{
        category: string;
        priority: string;
        action: string;
        impact: string;
        implementation_time: string;
        resources_required: string;
        expected_outcome: string;
        risk_factors: string[];
      }>;
      executive_summary: string;
      key_focus_areas: string[];
    }>('/api/analysis/recommendations/dynamic', {
      method: 'POST',
      body: JSON.stringify({
        startup_data: apiData,
        scores: scores,
        verdict: data.ml_results?.verdict
      }),
    });
  },

  // Market insights
  async getMarketInsights(data: {
    assessment_data: AssessmentData;
    sector: string;
  }) {
    const apiData = transformAssessmentToAPI(data.assessment_data);
    return apiCall<{
      market_insights: {
        trends: string[];
        opportunities: string[];
        threats: string[];
        competitive_landscape: any;
      };
      recommendations: string[];
    }>('/api/analysis/market-insights', {
      method: 'POST',
      body: JSON.stringify({
        assessment_data: apiData,
        sector: data.sector,
      }),
    });
  },

  // Competitor analysis
  async getCompetitorAnalysis(data: {
    assessment_data: AssessmentData;
    competitors: string[];
  }) {
    const apiData = transformAssessmentToAPI(data.assessment_data);
    return apiCall<{
      competitor_analysis: {
        strengths: any;
        weaknesses: any;
        market_position: any;
        strategies: any;
      };
      competitive_advantages: string[];
      recommendations: string[];
    }>('/api/analysis/competitor-analysis', {
      method: 'POST',
      body: JSON.stringify({
        assessment_data: apiData,
        competitors: data.competitors,
      }),
    });
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
      // CAPITAL_FEATURES (7)
      'total_capital_raised_usd', 'cash_on_hand_usd', 'monthly_burn_usd', 
      'runway_months', 'burn_multiple', 'investor_tier_primary', 'has_debt',
      
      // ADVANTAGE_FEATURES (8)
      'patent_count', 'network_effects_present', 'has_data_moat',
      'regulatory_advantage_present', 'tech_differentiation_score',
      'switching_cost_score', 'brand_strength_score', 'scalability_score',
      
      // MARKET_FEATURES (11)
      'sector', 'tam_size_usd', 'sam_size_usd', 'som_size_usd',
      'market_growth_rate_percent', 'customer_count', 'customer_concentration_percent',
      'user_growth_rate_percent', 'net_dollar_retention_percent',
      'competition_intensity', 'competitors_named_count',
      
      // PEOPLE_FEATURES (10)
      'founders_count', 'team_size_full_time', 'years_experience_avg',
      'domain_expertise_years_avg', 'prior_startup_experience_count',
      'prior_successful_exits_count', 'board_advisor_experience_score',
      'advisors_count', 'team_diversity_percent', 'key_person_dependency',
      
      // PRODUCT_FEATURES (9)
      'product_stage', 'product_retention_30d', 'product_retention_90d',
      'dau_mau_ratio', 'annual_revenue_run_rate', 'revenue_growth_rate_percent',
      'gross_margin_percent', 'ltv_cac_ratio', 'funding_stage',
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
  },

  // Deep Dive API Functions
  async analyzePhase1DeepDive(request: {
    porters_five_forces: {
      supplier_power: any;
      buyer_power: any;
      competitive_rivalry: any;
      threat_of_substitution: any;
      threat_of_new_entry: any;
    };
    internal_audit: {
      strengths: string[];
      weaknesses: string[];
      opportunities: string[];
      threats: string[];
    };
  }) {
    return apiCall<{
      competitive_position: any;
      strategic_gaps: any[];
      opportunities: any[];
      threats: any[];
      recommendations: any[];
      timestamp: string;
    }>('/api/analysis/deepdive/phase1/analysis', {
      method: 'POST',
      body: JSON.stringify(request),
    });
  },

  // Executive Framework Analysis
  async generateExecutiveFramework(request: {
    assessment_data: any;
    ml_results: any;
    analysis_depth: 'comprehensive' | 'focused';
    framework_level: 'senior-partner' | 'manager';
  }) {
    return apiCall<{
      report: any;
      status: string;
      confidence: number;
    }>('/api/analysis/executive-framework', {
      method: 'POST',
      body: JSON.stringify(request),
    });
  },
};

// Export individual functions for direct use
export const transformData = transformAssessmentToAPI;

export const getExecutiveFrameworkAnalysis = async (assessmentData: any): Promise<any> => {
  try {
    // Try deep analysis endpoint with intelligent framework selection
    const apiData = transformAssessmentToAPI(assessmentData);
    const response = await apiCall<any>('/api/frameworks/deep-analysis', {
      method: 'POST',
      body: JSON.stringify({
        startup_data: apiData,
        analysis_depth: 'comprehensive'
      }),
    });
    
    // Transform to executive format
    return {
      executiveSummary: response.executive_summary || {},
      situationAssessment: response.situation_assessment || {},
      strategicOptions: response.strategic_options || [],
      valueCreationWaterfall: response.value_drivers || [],
      competitiveDynamics: response.competitive_dynamics || [],
      implementationRoadmap: response.implementation_roadmap || [],
      financialProjections: response.financial_projections || {}
    };
  } catch (error) {
    console.error('Deep analysis not available, returning null for fallback');
    return null;
  }
};

export const getDeepFrameworkAnalysis = async (data: any): Promise<any> => {
  try {
    // Ensure data is properly formatted for the DeepSeek endpoint
    const requestData = data.startup_data ? data : { startup_data: data };
    
    const response = await apiCall<any>('/api/frameworks/deep-analysis', {
      method: 'POST',
      body: JSON.stringify(requestData),
    });
    
    return response;
  } catch (error) {
    console.error('Error getting deep framework analysis:', error);
    // Return null to allow the component to continue without LLM enhancements
    return null;
  }
};