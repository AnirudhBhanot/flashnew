// Test to verify all 45 features are correctly mapped
import { apiService } from './services/api';
import { AssessmentData } from './store/assessmentStore';

const testData: AssessmentData = {
  companyInfo: {
    companyName: 'Test Corp',
    sector: 'saas',
    website: 'https://test.com',
    headquarters: 'San Francisco',
    description: 'Test company',
    foundingDate: '2020-01-01'
  },
  capital: {
    totalRaised: 1000000,
    cashOnHand: 500000,
    monthlyBurn: 50000,
    runway: 10,
    burnMultiple: 2,
    primaryInvestor: 'tier_1',
    hasDebt: true,
    debtAmount: 100000,
    fundingStage: 'series_a',
    annualRevenueRunRate: 600000,
    monthlyRevenue: 50000,
    hasRevenue: true,
    lastValuation: 10000000
  },
  advantage: {
    productStage: 'mvp',
    patentCount: 2,
    networkEffects: true,
    hasDataMoat: true,
    regulatoryAdvantage: false,
    techDifferentiation: 4,
    switchingCosts: 3,
    brandStrength: 3,
    scalability: 4,
    uniqueAdvantage: 'Test advantage'
  },
  market: {
    sector: 'saas',
    tam: 1000000000,
    sam: 100000000,
    som: 10000000,
    marketGrowthRate: 25,
    customerCount: 100,
    customerConcentration: 20,
    userGrowthRate: 50,
    netDollarRetention: 120,
    competitionIntensity: 3,
    competitorCount: 5,
    revenueGrowthRate: 100,
    grossMargin: 80,
    ltvCacRatio: 3
  },
  people: {
    founderCount: 2,
    teamSize: 10,
    avgExperience: 10,
    domainExpertiseYears: 5,
    priorStartupCount: 1,
    priorExits: 0,
    boardAdvisorScore: 4,
    advisorCount: 3,
    teamDiversity: 40,
    keyPersonDependency: false
  },
  product: {
    dailyActiveUsers: 1000,
    monthlyActiveUsers: 5000,
    retentionRate: 85,
    productRetention30d: 60,
    productRetention90d: 40,
    dauMauRatio: 20,
    productMarketFitScore: 3.5,
    featureAdoptionRate: 70,
    userEngagementScore: 3.5,
    timeToValueDays: 7,
    productStickiness: 20,
    activationRate: 60,
    customerLifetimeValue: 10000,
    averageDealSize: 1000,
    customerSatisfactionScore: 8,
    salesCycleDays: 30,
    grossMargin: 80,
    revenueGrowthRate: 100,
    capitalEfficiencyScore: 3.5
  }
};

export function testFeatureMapping() {
  console.log('Testing Feature Mapping...\n');
  
  // Transform the data
  const transformedData = apiService.transformAssessmentToAPI(testData);
  
  // Expected 45 features
  const expectedFeatures = [
    // CAPITAL_FEATURES (7)
    'total_capital_raised_usd',
    'cash_on_hand_usd',
    'monthly_burn_usd',
    'runway_months',
    'burn_multiple',
    'investor_tier_primary',
    'has_debt',
    
    // ADVANTAGE_FEATURES (8)
    'patent_count',
    'network_effects_present',
    'has_data_moat',
    'regulatory_advantage_present',
    'tech_differentiation_score',
    'switching_cost_score',
    'brand_strength_score',
    'scalability_score',
    
    // MARKET_FEATURES (11)
    'sector',
    'tam_size_usd',
    'sam_size_usd',
    'som_size_usd',
    'market_growth_rate_percent',
    'customer_count',
    'customer_concentration_percent',
    'user_growth_rate_percent',
    'net_dollar_retention_percent',
    'competition_intensity',
    'competitors_named_count',
    
    // PEOPLE_FEATURES (10)
    'founders_count',
    'team_size_full_time',
    'years_experience_avg',
    'domain_expertise_years_avg',
    'prior_startup_experience_count',
    'prior_successful_exits_count',
    'board_advisor_experience_score',
    'advisors_count',
    'team_diversity_percent',
    'key_person_dependency',
    
    // PRODUCT_FEATURES (9)
    'product_stage',
    'product_retention_30d',
    'product_retention_90d',
    'dau_mau_ratio',
    'annual_revenue_run_rate',
    'revenue_growth_rate_percent',
    'gross_margin_percent',
    'ltv_cac_ratio',
    'funding_stage'
  ];
  
  console.log('Checking all 45 features...\n');
  
  let missingFeatures = [];
  let incorrectValues = [];
  
  for (const feature of expectedFeatures) {
    if (!(feature in transformedData)) {
      missingFeatures.push(feature);
    } else if (transformedData[feature] === undefined || transformedData[feature] === null) {
      incorrectValues.push(`${feature}: ${transformedData[feature]}`);
    }
  }
  
  // Check for extra features
  const extraFeatures = Object.keys(transformedData).filter(
    key => !expectedFeatures.includes(key)
  );
  
  // Report results
  console.log(`Total features expected: ${expectedFeatures.length}`);
  console.log(`Total features found: ${Object.keys(transformedData).length}`);
  console.log(`Missing features: ${missingFeatures.length}`);
  console.log(`Features with null/undefined: ${incorrectValues.length}`);
  console.log(`Extra features: ${extraFeatures.length}`);
  
  if (missingFeatures.length > 0) {
    console.log('\n❌ Missing features:', missingFeatures);
  }
  
  if (incorrectValues.length > 0) {
    console.log('\n⚠️  Features with null/undefined values:', incorrectValues);
  }
  
  if (extraFeatures.length > 0) {
    console.log('\n⚠️  Extra features found:', extraFeatures);
  }
  
  if (missingFeatures.length === 0 && incorrectValues.length === 0 && extraFeatures.length === 0) {
    console.log('\n✅ All 45 features are correctly mapped!');
    
    // Show sample of transformed values
    console.log('\nSample transformed values:');
    console.log('- investor_tier_primary:', transformedData.investor_tier_primary);
    console.log('- sector:', transformedData.sector);
    console.log('- product_stage:', transformedData.product_stage);
    console.log('- product_retention_30d:', transformedData.product_retention_30d);
    console.log('- product_retention_90d:', transformedData.product_retention_90d);
    console.log('- dau_mau_ratio:', transformedData.dau_mau_ratio);
  }
}

// Run the test
testFeatureMapping();