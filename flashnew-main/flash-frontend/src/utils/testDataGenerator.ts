// Test Data Generator for FLASH Platform
// Generates realistic random startup data for testing

import { StartupData } from '../types';

// Helper functions
const randomBetween = (min: number, max: number): number => {
  return Math.floor(Math.random() * (max - min + 1)) + min;
};

const randomFloat = (min: number, max: number, decimals: number = 2): number => {
  const value = Math.random() * (max - min) + min;
  return parseFloat(value.toFixed(decimals));
};

const randomChoice = <T>(array: T[]): T => {
  return array[Math.floor(Math.random() * array.length)];
};

// Define stage type
type FundingStage = 'pre_seed' | 'seed' | 'series_a' | 'series_b' | 'series_c';

// Stage-specific realistic ranges based on real-world data
const stageRanges: Record<FundingStage, {
  capital_raised: { min: number; max: number };
  cash_on_hand: { min: number; max: number };
  monthly_burn: { min: number; max: number };
  mrr: { min: number; max: number };
  team_size: { min: number; max: number };
  runway_months: { min: number; max: number };
  customer_count: { min: number; max: number };
  retention_30d: { min: number; max: number };
  tam_size: { min: number; max: number };
}> = {
  pre_seed: {
    capital_raised: { min: 50000, max: 500000 },
    cash_on_hand: { min: 30000, max: 400000 },
    monthly_burn: { min: 10000, max: 50000 },
    mrr: { min: 0, max: 5000 },
    team_size: { min: 2, max: 5 },
    runway_months: { min: 6, max: 12 },
    customer_count: { min: 0, max: 100 },
    retention_30d: { min: 0.20, max: 0.60 },
    tam_size: { min: 500000000, max: 5000000000 }
  },
  seed: {
    capital_raised: { min: 500000, max: 2000000 },
    cash_on_hand: { min: 300000, max: 1500000 },
    monthly_burn: { min: 30000, max: 150000 },
    mrr: { min: 5000, max: 50000 },
    team_size: { min: 4, max: 12 },
    runway_months: { min: 12, max: 18 },
    customer_count: { min: 10, max: 500 },
    retention_30d: { min: 0.30, max: 0.70 },
    tam_size: { min: 1000000000, max: 10000000000 }
  },
  series_a: {
    capital_raised: { min: 2000000, max: 15000000 },
    cash_on_hand: { min: 1500000, max: 10000000 },
    monthly_burn: { min: 100000, max: 500000 },
    mrr: { min: 50000, max: 250000 },
    team_size: { min: 10, max: 30 },
    runway_months: { min: 18, max: 24 },
    customer_count: { min: 50, max: 2000 },
    retention_30d: { min: 0.40, max: 0.80 },
    tam_size: { min: 5000000000, max: 50000000000 }
  },
  series_b: {
    capital_raised: { min: 15000000, max: 50000000 },
    cash_on_hand: { min: 10000000, max: 35000000 },
    monthly_burn: { min: 300000, max: 1000000 },
    mrr: { min: 250000, max: 1000000 },
    team_size: { min: 25, max: 100 },
    runway_months: { min: 18, max: 30 },
    customer_count: { min: 200, max: 5000 },
    retention_30d: { min: 0.50, max: 0.85 },
    tam_size: { min: 10000000000, max: 100000000000 }
  },
  series_c: {
    capital_raised: { min: 50000000, max: 150000000 },
    cash_on_hand: { min: 30000000, max: 100000000 },
    monthly_burn: { min: 500000, max: 2000000 },
    mrr: { min: 1000000, max: 5000000 },
    team_size: { min: 80, max: 300 },
    runway_months: { min: 24, max: 48 },
    customer_count: { min: 1000, max: 20000 },
    retention_30d: { min: 0.60, max: 0.90 },
    tam_size: { min: 20000000000, max: 200000000000 }
  }
};

// Generate data based on funding stage
export const generateTestStartupData = (): Partial<StartupData> => {
  // Pick a random funding stage
  const fundingStage = randomChoice<FundingStage>(['pre_seed', 'seed', 'series_a', 'series_b', 'series_c']);
  const ranges = stageRanges[fundingStage];
  
  // Generate stage-appropriate values
  const totalCapitalRaised = randomBetween(ranges.capital_raised.min, ranges.capital_raised.max);
  const cashOnHand = randomBetween(ranges.cash_on_hand.min, Math.min(ranges.cash_on_hand.max, totalCapitalRaised * 0.8));
  const monthlyBurn = randomBetween(ranges.monthly_burn.min, ranges.monthly_burn.max);
  const mrr = randomBetween(ranges.mrr.min, ranges.mrr.max);
  const annualRevenue = mrr * 12;
  
  // Calculate realistic runway
  const runwayMonths = cashOnHand / monthlyBurn;
  const burnMultiple = monthlyBurn > 0 && mrr > 0 ? randomFloat(1.5, 4.0) : 0;
  
  // Stage-appropriate team and experience
  const teamSize = randomBetween(ranges.team_size.min, ranges.team_size.max);
  const foundersCount = randomBetween(1, Math.min(4, Math.ceil(teamSize / 3)));
  
  // Experience correlates with stage
  const yearsExperience = fundingStage === 'pre_seed' ? randomBetween(2, 8) :
                          fundingStage === 'seed' ? randomBetween(3, 12) :
                          fundingStage === 'series_a' ? randomBetween(5, 15) :
                          randomBetween(8, 20);
  
  // Calculate TAM/SAM/SOM with realistic ratios
  const tam = randomBetween(ranges.tam_size.min, ranges.tam_size.max);
  const sam = tam * randomFloat(0.05, 0.20); // 5-20% of TAM
  const som = sam * randomFloat(0.05, 0.15); // 5-15% of SAM
  
  // Retention rates
  const retention30d = randomFloat(ranges.retention_30d.min, ranges.retention_30d.max);
  const retention90d = retention30d * randomFloat(0.6, 0.85); // 90d is 60-85% of 30d
  
  // Generate realistic growth rates based on stage
  const revenueGrowthRate = fundingStage === 'pre_seed' ? randomBetween(0, 100) :
                           fundingStage === 'seed' ? randomBetween(50, 200) :
                           fundingStage === 'series_a' ? randomBetween(80, 300) :
                           randomBetween(50, 150);
  
  const userGrowthRate = fundingStage === 'pre_seed' ? randomBetween(0, 50) :
                        fundingStage === 'seed' ? randomBetween(20, 100) :
                        randomBetween(30, 150);
  
  return {
    // Capital fields
    funding_stage: fundingStage, // Use the raw value (pre_seed, seed, etc.)
    total_capital_raised_usd: totalCapitalRaised,
    cash_on_hand_usd: cashOnHand,
    monthly_burn_usd: monthlyBurn,
    annual_revenue_run_rate: annualRevenue,
    revenue_growth_rate_percent: revenueGrowthRate,
    gross_margin_percent: randomBetween(40, 80), // Most software is 40-80%
    ltv_cac_ratio: randomFloat(0.8, 3.5),
    investor_tier_primary: fundingStage === 'pre_seed' ? randomChoice(['Angel']) :
                           fundingStage === 'seed' ? randomChoice(['Angel', 'Tier 3', 'Tier 2']) :
                           randomChoice(['Tier 1', 'Tier 2']),
    has_debt: Math.random() > 0.8, // 20% chance of debt
    runway_months: Math.round(runwayMonths),
    burn_multiple: burnMultiple,
    
    // Advantage fields
    patent_count: fundingStage === 'pre_seed' ? randomBetween(0, 2) :
                  fundingStage === 'seed' ? randomBetween(0, 5) :
                  randomBetween(1, 15),
    network_effects_present: Math.random() > 0.6,
    has_data_moat: Math.random() > 0.7,
    regulatory_advantage_present: Math.random() > 0.85,
    tech_differentiation_score: randomBetween(2, 5),
    switching_cost_score: randomBetween(2, 5),
    brand_strength_score: fundingStage === 'pre_seed' ? randomBetween(1, 3) :
                          fundingStage === 'seed' ? randomBetween(1, 4) :
                          randomBetween(2, 5),
    scalability_score: randomBetween(3, 5),
    product_stage: fundingStage === 'pre_seed' ? randomChoice(['MVP', 'Beta']) :
                   fundingStage === 'seed' ? randomChoice(['Beta', 'GA']) :
                   randomChoice(['GA', 'Mature']),
    product_retention_30d: retention30d,
    product_retention_90d: retention90d,
    
    // Market fields
    sector: randomChoice(['SaaS', 'Fintech', 'Healthcare', 'E-commerce', 'AI/ML', 'Marketplace', 'EdTech', 'PropTech']),
    tam_size_usd: Math.round(tam),
    sam_size_usd: Math.round(sam),
    som_size_usd: Math.round(som),
    market_growth_rate_percent: randomBetween(10, 40),
    customer_count: randomBetween(ranges.customer_count.min, ranges.customer_count.max),
    customer_concentration_percent: fundingStage === 'pre_seed' ? randomBetween(20, 80) :
                                   randomBetween(5, 40),
    user_growth_rate_percent: userGrowthRate,
    net_dollar_retention_percent: randomBetween(85, 125),
    competition_intensity: randomBetween(2, 4),
    competitors_named_count: randomBetween(3, 15),
    dau_mau_ratio: randomFloat(0.15, 0.65),
    
    // People fields
    founders_count: foundersCount,
    team_size_full_time: teamSize,
    years_experience_avg: yearsExperience,
    domain_expertise_years_avg: Math.max(1, yearsExperience - randomBetween(2, 5)),
    prior_startup_experience_count: Math.random() > 0.5 ? randomBetween(0, 3) : 0,
    prior_successful_exits_count: Math.random() > 0.8 ? randomBetween(0, 2) : 0,
    board_advisor_experience_score: fundingStage === 'pre_seed' ? randomBetween(1, 3) :
                                    fundingStage === 'seed' ? randomBetween(2, 4) :
                                    randomBetween(3, 5),
    advisors_count: fundingStage === 'pre_seed' ? randomBetween(0, 3) :
                    fundingStage === 'seed' ? randomBetween(1, 5) :
                    randomBetween(3, 10),
    team_diversity_percent: randomBetween(20, 60),
    key_person_dependency: Math.random() > 0.6
  };
};

// Generate specific test scenarios with realistic values
export const testScenarios = {
  bestCase: (): Partial<StartupData> => ({
    // Strong Series A startup
    funding_stage: 'series_a',
    total_capital_raised_usd: 12000000,
    cash_on_hand_usd: 9000000,
    monthly_burn_usd: 250000,
    annual_revenue_run_rate: 3000000, // $250k MRR
    revenue_growth_rate_percent: 180,
    gross_margin_percent: 75,
    ltv_cac_ratio: 3.2,
    investor_tier_primary: 'Tier 1',
    has_debt: false,
    runway_months: 36,
    burn_multiple: 2.5,
    patent_count: 4,
    network_effects_present: true,
    has_data_moat: true,
    regulatory_advantage_present: false,
    tech_differentiation_score: 4,
    switching_cost_score: 4,
    brand_strength_score: 3,
    scalability_score: 5,
    product_stage: 'GA',
    product_retention_30d: 0.75,
    product_retention_90d: 0.60,
    sector: 'SaaS',
    tam_size_usd: 15000000000, // $15B TAM
    sam_size_usd: 1500000000,  // $1.5B SAM
    som_size_usd: 150000000,   // $150M SOM
    market_growth_rate_percent: 25,
    customer_count: 800,
    customer_concentration_percent: 12,
    user_growth_rate_percent: 120,
    net_dollar_retention_percent: 115,
    competition_intensity: 3,
    competitors_named_count: 8,
    dau_mau_ratio: 0.45,
    founders_count: 2,
    team_size_full_time: 25,
    years_experience_avg: 12,
    domain_expertise_years_avg: 8,
    prior_startup_experience_count: 2,
    prior_successful_exits_count: 1,
    board_advisor_experience_score: 4,
    advisors_count: 5,
    team_diversity_percent: 40,
    key_person_dependency: false
  }),
  
  worstCase: (): Partial<StartupData> => ({
    // Struggling pre-seed startup
    funding_stage: 'pre_seed',
    total_capital_raised_usd: 75000,
    cash_on_hand_usd: 20000,
    monthly_burn_usd: 20000,
    annual_revenue_run_rate: 0,
    revenue_growth_rate_percent: 0,
    gross_margin_percent: 0,
    ltv_cac_ratio: 0,
    investor_tier_primary: 'Angel',
    has_debt: true,
    runway_months: 1,
    burn_multiple: 0,
    patent_count: 0,
    network_effects_present: false,
    has_data_moat: false,
    regulatory_advantage_present: false,
    tech_differentiation_score: 1,
    switching_cost_score: 1,
    brand_strength_score: 1,
    scalability_score: 2,
    product_stage: 'MVP',
    product_retention_30d: 0.15,
    product_retention_90d: 0.05,
    sector: 'E-commerce',
    tam_size_usd: 500000000,
    sam_size_usd: 25000000,
    som_size_usd: 1000000,
    market_growth_rate_percent: 5,
    customer_count: 3,
    customer_concentration_percent: 100,
    user_growth_rate_percent: -10,
    net_dollar_retention_percent: 70,
    competition_intensity: 5,
    competitors_named_count: 30,
    dau_mau_ratio: 0.05,
    founders_count: 1,
    team_size_full_time: 2,
    years_experience_avg: 2,
    domain_expertise_years_avg: 0,
    prior_startup_experience_count: 0,
    prior_successful_exits_count: 0,
    board_advisor_experience_score: 1,
    advisors_count: 0,
    team_diversity_percent: 0,
    key_person_dependency: true
  })
};