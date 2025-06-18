// Test script to verify all 45 features are sent correctly
const testData = {
  companyInfo: {
    companyName: 'Test Startup Inc',
    website: 'https://teststartup.com',
    industry: 'saas',
    foundedDate: '2020-01-01T00:00:00.000Z',
    fundingStage: 'series_a',
    location: 'San Francisco, CA',
    description: 'AI-powered analytics platform'
  },
  capital: {
    totalCapitalRaisedUsd: '10000000',
    cashOnHandUsd: '7000000',
    monthlyBurnUsd: '250000',
    runwayMonths: '28',
    burnMultiple: '2.1',
    investorTierPrimary: 'tier_1',
    hasDebt: false
  },
  advantage: {
    patentCount: '3',
    networkEffectsPresent: true,
    hasDataMoat: true,
    regulatoryAdvantagePresent: false,
    techDifferentiationScore: 4,
    switchingCostScore: 3,
    brandStrengthScore: 3,
    scalabilityScore: 5
  },
  market: {
    sector: 'saas',
    tamSizeUsd: '50000000000',
    samSizeUsd: '5000000000',
    somSizeUsd: '500000000',
    marketGrowthRatePercent: '25',
    customerCount: '150',
    customerConcentrationPercent: '15',
    userGrowthRatePercent: '12',
    netDollarRetentionPercent: '115',
    competitionIntensity: 'medium',
    competitorsNamedCount: '7'
  },
  people: {
    foundersCount: '3',
    teamSizeFullTime: '45',
    yearsExperienceAvg: '12',
    domainExpertiseYearsAvg: '8',
    priorStartupExperienceCount: '2',
    priorSuccessfulExitsCount: '1',
    boardAdvisorExperienceScore: 4,
    advisorsCount: '5',
    teamDiversityPercent: '35',
    keyPersonDependency: false
  },
  product: {
    productStage: 'production',
    productRetention30d: '85',
    productRetention90d: '75',
    dauMauRatio: '45',
    annualRevenueRunRate: '3600000',
    revenueGrowthRatePercent: '150',
    grossMarginPercent: '82',
    ltvCacRatio: '3.5'
  }
};

// Transform function (copy from api.ts)
function transformAssessmentToAPI(data) {
  const {
    companyInfo = {},
    capital = {},
    advantage = {},
    market = {},
    people = {},
    product = {}
  } = data;

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
    competition_intensity: market.competitionIntensity || 'medium',
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

// Test the transformation
const apiData = transformAssessmentToAPI(testData);

// Check all 45 features
const expectedFeatures = [
  // Capital (7)
  'total_capital_raised_usd', 'cash_on_hand_usd', 'monthly_burn_usd', 
  'runway_months', 'burn_multiple', 'investor_tier_primary', 'has_debt',
  // Advantage (8)
  'patent_count', 'network_effects_present', 'has_data_moat', 
  'regulatory_advantage_present', 'tech_differentiation_score', 
  'switching_cost_score', 'brand_strength_score', 'scalability_score',
  // Market (11)
  'sector', 'tam_size_usd', 'sam_size_usd', 'som_size_usd', 
  'market_growth_rate_percent', 'customer_count', 'customer_concentration_percent',
  'user_growth_rate_percent', 'net_dollar_retention_percent', 
  'competition_intensity', 'competitors_named_count',
  // People (10)
  'founders_count', 'team_size_full_time', 'years_experience_avg',
  'domain_expertise_years_avg', 'prior_startup_experience_count',
  'prior_successful_exits_count', 'board_advisor_experience_score',
  'advisors_count', 'team_diversity_percent', 'key_person_dependency',
  // Product (9)
  'product_stage', 'product_retention_30d', 'product_retention_90d',
  'dau_mau_ratio', 'annual_revenue_run_rate', 'revenue_growth_rate_percent',
  'gross_margin_percent', 'ltv_cac_ratio', 'funding_stage'
];

console.log('=== FEATURE ALIGNMENT TEST ===\n');

// Check feature count
console.log(`Total features expected: ${expectedFeatures.length}`);
console.log(`Total features in payload: ${Object.keys(apiData).length}`);
console.log(`Match: ${expectedFeatures.length === Object.keys(apiData).length ? '✓' : '✗'}\n`);

// Check each feature
console.log('Feature Validation:');
let allPresent = true;
let nonDefaultCount = 0;

expectedFeatures.forEach(feature => {
  const present = feature in apiData;
  const value = apiData[feature];
  const isDefault = (
    value === 0 || 
    value === false || 
    value === 'tier_3' || 
    value === 'medium' || 
    value === 'mvp' || 
    value === 'seed' ||
    value === 3 ||
    value === 2.5
  );
  
  if (!isDefault) nonDefaultCount++;
  
  console.log(`${present ? '✓' : '✗'} ${feature}: ${value}${isDefault ? ' (default)' : ''}`);
  
  if (!present) allPresent = false;
});

console.log(`\n=== SUMMARY ===`);
console.log(`All features present: ${allPresent ? '✓' : '✗'}`);
console.log(`Features with actual data: ${nonDefaultCount}/${expectedFeatures.length}`);
console.log(`Data coverage: ${Math.round(nonDefaultCount / expectedFeatures.length * 100)}%`);

// Test actual API call
console.log('\n=== TESTING API ENDPOINT ===');

const fetch = require('node-fetch');

async function testAPI() {
  try {
    const response = await fetch('http://localhost:8001/predict', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(apiData)
    });
    
    const result = await response.json();
    
    console.log('\nAPI Response:');
    console.log(`Status: ${response.status}`);
    console.log(`Success Probability: ${result.success_probability}`);
    console.log(`Verdict: ${result.verdict}`);
    console.log(`CAMP Scores:`, result.camp_scores);
    
  } catch (error) {
    console.error('API Test Failed:', error.message);
  }
}

testAPI();