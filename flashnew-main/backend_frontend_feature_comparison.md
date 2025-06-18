# Backend vs Frontend Feature Comparison

## Summary
- **Backend**: 45 core features defined in `feature_config.py` and `feature_registry.py`
- **Frontend**: ~30 input fields collected across 5 sections, transformed to 45 backend features

## 1. Backend Features Missing in Frontend

These backend features have NO direct frontend input field and are either:
- Hardcoded in the transformation
- Calculated/derived
- Given default values

### Capital Features
- `cash_on_hand_usd` - Estimated as 70% of total funding raised
- `has_debt` - Always set to `false`
- `investor_tier_primary` - Calculated based on total funding amount

### Advantage Features  
- `brand_strength_score` - Hardcoded to `3`
- `scalability_score` - Hardcoded to `4`
- `switching_cost_score` - Derived from `moatStrength`
- `tech_differentiation_score` - Derived from `moatStrength`

### Market Features
- `tam_size_usd` - Frontend only collects generic `marketSize`
- `sam_size_usd` - Calculated as 10% of market size
- `som_size_usd` - Calculated as 1% of market size
- `customer_count` - Hardcoded to `100`
- `customer_concentration_percent` - Hardcoded to `20`
- `user_growth_rate_percent` - Hardcoded to `100`
- `net_dollar_retention_percent` - Hardcoded to `110`
- `competitors_named_count` - Hardcoded to `5`

### People Features
- `years_experience_avg` - Uses `industryExperience` scale (1-10) instead
- `domain_expertise_years_avg` - Also uses `industryExperience`
- `prior_startup_experience_count` - Boolean in frontend, converted to count
- `board_advisor_experience_score` - Hardcoded to `3`
- `team_diversity_percent` - Hardcoded to `30%`
- `key_person_dependency` - Hardcoded to `false`

### Product Features
- `product_stage` - Hardcoded to `'beta'`
- `product_retention_30d` - Hardcoded to `0.7`
- `product_retention_90d` - Hardcoded to `0.5`  
- `dau_mau_ratio` - Hardcoded to `0.4`
- `revenue_growth_rate_percent` - Hardcoded to `100`

## 2. Frontend Features Not in Backend

These are collected in frontend but not used or transformed differently:

### Company Info Section (not in backend 45 features)
- `companyName`
- `website`
- `foundedDate`
- `location`
- `description`

### Capital Section
- Frontend combines all funding stages into `totalFundingRaised`

### Market Section
- `goToMarketStrategy` - Text field not used
- `marketTiming` - Scale not mapped to backend

### People Section
- `teamCulture` - Scale not used
- `keyRoles` - Array of roles not used
- `teamWeaknesses` - Text field not used

### Advantage Section
- `uniqueAdvantage` - Text description not used

## 3. Name Mismatches

| Backend Feature | Frontend Field | Notes |
|-----------------|----------------|-------|
| `sector` | `industry` | Direct mapping |
| `funding_stage` | `stage` | Direct mapping |
| `total_capital_raised_usd` | `totalFundingRaised` | Direct mapping |
| `monthly_burn_usd` | `monthlyBurnRate` | Direct mapping |
| `annual_revenue_run_rate` | `annualRevenueRunRate` | Direct mapping |
| `gross_margin_percent` | `grossMargin` | Direct mapping |
| `ltv_cac_ratio` | `ltvCacRatio` | Direct mapping |
| `patent_count` | `patentCount` | Direct mapping |
| `network_effects_present` | Derived from `advantages` array | Check if 'network' in array |
| `has_data_moat` | Derived from `advantages` array | Check if 'data' in array |
| `regulatory_advantage_present` | Derived from `advantages` array | Check if 'regulatory' in array |
| `market_growth_rate_percent` | `marketGrowthRate` | Direct mapping |
| `competition_intensity` | `competitionLevel` | Direct mapping |
| `team_size_full_time` | `teamSize` | Direct mapping |
| `founders_count` | `foundersCount` | Direct mapping |
| `prior_successful_exits_count` | `previousExits` | Direct mapping |
| `advisors_count` | `advisorsCount` | Direct mapping |

## 4. Type Mismatches

### Scale to Score Conversions
Frontend uses 1-10 scales, backend expects 1-5 scores:
- `industryExperience` (1-10 scale) → `years_experience_avg` (expects years)
- `moatStrength` (1-10) → multiple scores (1-5)
- `competitionLevel` (1-10) → `competition_intensity` (1-5)
- `differentiationLevel` (1-10) → not directly used

### Boolean to Count Conversions
- `previousStartups` (boolean) → `prior_startup_experience_count` (number)
- `hasPatents` (boolean) → used to conditionally set `patent_count`

### Different Units
- Frontend `marketSize` is generic, backend splits into TAM/SAM/SOM
- Frontend collects single market size, backend needs three different values

## 5. Structural Differences

### Data Organization
1. **Frontend**: Organized by UI sections (CompanyInfo, Capital, Advantage, Market, People)
2. **Backend**: Organized by CAMP framework + Product features

### Missing Validation
Frontend doesn't validate:
- Ranges for scores (should be 1-5 not 1-10)
- Percentage fields (0-100 bounds)
- Realistic value ranges for metrics

### Calculation Logic
Many backend features are calculated/estimated rather than collected:
- Runway calculation exists in frontend but also estimated in transform
- Cash on hand is estimated as 70% of funding
- Market sizes (SAM/SOM) calculated from TAM
- Many scores defaulted rather than derived

## Critical Issues to Fix

1. **Data Loss**: Many nuanced backend features are hardcoded instead of collected
2. **Scale Misalignment**: Frontend 1-10 scales don't map cleanly to backend 1-5 scores
3. **Missing Core Metrics**: No way to input product metrics, retention rates, DAU/MAU
4. **Oversimplification**: Complex features like team diversity, key person risk not captured
5. **Default Value Overuse**: Too many features use static defaults instead of user input

## Recommendations

1. Add frontend fields for critical missing metrics:
   - Product retention rates
   - Customer metrics (count, concentration)
   - Detailed market sizing (TAM/SAM/SOM)
   - Team diversity percentage
   - Cash on hand separate from funding raised

2. Align scoring scales between frontend (1-10) and backend (1-5)

3. Add calculated fields in frontend for:
   - Burn multiple
   - Investor tier determination
   - Market size breakdowns

4. Remove unused frontend fields or map them to backend features

5. Add proper validation for all numeric ranges and percentages