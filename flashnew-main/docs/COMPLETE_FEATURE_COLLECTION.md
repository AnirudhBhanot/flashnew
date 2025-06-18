# Complete 45-Feature Collection Documentation

## Overview

The FLASH platform collects 45 features across 5 assessment pages to feed into the ML models for startup success prediction. This document details each feature, where it's collected, and how it's processed.

## Feature Breakdown by Category

### 1. CAPITAL_FEATURES (7 features) - `/assessment/capital`

| Feature | Field Name | Type | Notes |
|---------|------------|------|-------|
| total_capital_raised_usd | totalRaised | number | Total funding raised to date |
| cash_on_hand_usd | cashOnHand | number | Current cash balance |
| monthly_burn_usd | monthlyBurn | number | Monthly cash burn rate |
| runway_months | runway | number | **Auto-calculated**: cash_on_hand ÷ monthly_burn |
| burn_multiple | burnMultiple | number | **Auto-calculated**: monthly_burn ÷ monthly_revenue |
| investor_tier_primary | primaryInvestor | string | Tier 1/2/3, angel, none, etc. |
| has_debt | hasDebt | boolean | Converted to 0/1 for API |

### 2. ADVANTAGE_FEATURES (8 features) - `/assessment/advantage`

| Feature | Field Name | Type | Notes |
|---------|------------|------|-------|
| patent_count | patentCount | number | Number of patents filed/granted |
| network_effects_present | networkEffects | boolean | Toggle, converted to 0/1 |
| has_data_moat | hasDataMoat | boolean | Toggle, converted to 0/1 |
| regulatory_advantage_present | regulatoryAdvantage | boolean | Toggle, converted to 0/1 |
| tech_differentiation_score | techDifferentiation | number | Scale 1-5 |
| switching_cost_score | switchingCosts | number | Scale 1-5 |
| brand_strength_score | brandStrength | number | Scale 1-5 |
| scalability_score | scalability | number | Scale 1-5 |

### 3. MARKET_FEATURES (11 features) - `/assessment/market`

| Feature | Field Name | Type | Notes |
|---------|------------|------|-------|
| sector | sector | string | Industry sector dropdown |
| tam_size_usd | tam | number | Total Addressable Market |
| sam_size_usd | sam | number | **Auto-calculated**: 10% of TAM |
| som_size_usd | som | number | **Auto-calculated**: 1% of SAM |
| market_growth_rate_percent | marketGrowthRate | number | Annual growth % |
| customer_count | customerCount | number | Active customers |
| customer_concentration_percent | customerConcentration | number | Revenue from top customers % |
| user_growth_rate_percent | userGrowthRate | number | Monthly growth % |
| net_dollar_retention_percent | netDollarRetention | number | Revenue retention % |
| competition_intensity | competitionIntensity | number | Scale 1-5 |
| competitors_named_count | competitorCount | number | Direct competitors |

### 4. PEOPLE_FEATURES (10 features) - `/assessment/people`

| Feature | Field Name | Type | Notes |
|---------|------------|------|-------|
| founders_count | founderCount | number | Number of founders |
| team_size_full_time | teamSize | number | Full-time employees |
| years_experience_avg | avgExperience | number | Average years experience |
| domain_expertise_years_avg | domainExpertiseYears | number | Years in domain |
| prior_startup_experience_count | priorStartupCount | number | Previous startups |
| prior_successful_exits_count | priorExits | number | Successful exits |
| board_advisor_experience_score | boardAdvisorScore | number | Scale 1-5 |
| advisors_count | advisorCount | number | Number of advisors |
| team_diversity_percent | teamDiversity | number | Diversity percentage |
| key_person_dependency | keyPersonDependency | boolean | Toggle, converted to 0/1 |

### 5. PRODUCT_FEATURES (9 features) - Multiple Pages

| Feature | Field Name | Type | Collection Page | Notes |
|---------|------------|------|-----------------|-------|
| product_stage | productStage | string | Advantage | Dropdown selection |
| product_retention_30d | productRetention30d | number | Market | 30-day retention % |
| product_retention_90d | productRetention90d | number | Market | 90-day retention % |
| dau_mau_ratio | dauMauRatio | number | Market | Daily/Monthly active users % |
| annual_revenue_run_rate | annualRevenueRunRate | number | Capital | **Auto-calculated**: monthly_revenue × 12 |
| revenue_growth_rate_percent | revenueGrowthRate | number | Market | YoY growth % |
| gross_margin_percent | grossMargin | number | Market | Gross margin % |
| ltv_cac_ratio | ltvCacRatio | number | Market | LTV/CAC ratio |
| funding_stage | fundingStage | string | Capital | Pre-seed, Seed, Series A, etc. |

## Auto-Calculation Logic

### Financial Calculations (Capital Page)
```javascript
// Runway calculation
runway = Math.floor(cashOnHand / monthlyBurn)

// Burn multiple calculation  
burnMultiple = (monthlyBurn / monthlyRevenue).toFixed(2)

// Annual revenue run rate
annualRevenueRunRate = monthlyRevenue * 12
```

### Market Calculations (Market Page)
```javascript
// SAM calculation (10% of TAM)
sam = Math.round(tam * 0.1)

// SOM calculation (1% of SAM)
som = Math.round(sam * 0.01)
```

## Data Transformation

The `transformAssessmentToAPI` function in `services/api.ts` handles:

1. **Type Conversion**: Booleans to 0/1, strings to numbers
2. **Percentage Handling**: Some fields need division by 100 (retention rates)
3. **Mapping**: Frontend values to API-expected values
4. **Validation**: Ensures all 45 features are present

## Validation Rules

- Numeric fields accept 0 as valid (except where noted)
- Percentage fields typically range 0-100
- Scale fields range 1-5
- Required fields vary by page (defined in each component's validate function)

## Recent Updates (V24)

1. Added 10 missing product/market features to Market page
2. Fixed SAM/SOM auto-calculation with currency parsing
3. Removed "Add more details" toggle for consistent UX
4. Moved auto-calculated display to bottom of page
5. Achieved 100% feature collection coverage

## Testing Checklist

- [ ] All 45 features collected across pages
- [ ] Auto-calculations update in real-time
- [ ] SAM/SOM cannot be manually edited
- [ ] API receives all 45 features on submission
- [ ] Validation prevents submission with missing required fields
- [ ] Currency inputs handle formatting correctly