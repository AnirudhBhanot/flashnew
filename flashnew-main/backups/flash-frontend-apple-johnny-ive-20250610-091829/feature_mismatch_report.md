# Frontend-Backend Feature Mismatch Report

## Summary
The frontend and backend have significant mismatches in the features they expect. The backend expects exactly 45 features, but the frontend is collecting and sending different fields with different names and structures.

## Backend Expected Features (45 total)

### CAPITAL_FEATURES (7):
1. `total_capital_raised_usd`
2. `cash_on_hand_usd`
3. `monthly_burn_usd`
4. `runway_months`
5. `burn_multiple`
6. `investor_tier_primary`
7. `has_debt`

### ADVANTAGE_FEATURES (8):
1. `patent_count`
2. `network_effects_present`
3. `has_data_moat`
4. `regulatory_advantage_present`
5. `tech_differentiation_score`
6. `switching_cost_score`
7. `brand_strength_score`
8. `scalability_score`

### MARKET_FEATURES (11):
1. `sector`
2. `tam_size_usd`
3. `sam_size_usd`
4. `som_size_usd`
5. `market_growth_rate_percent`
6. `customer_count`
7. `customer_concentration_percent`
8. `user_growth_rate_percent`
9. `net_dollar_retention_percent`
10. `competition_intensity`
11. `competitors_named_count`

### PEOPLE_FEATURES (10):
1. `founders_count`
2. `team_size_full_time`
3. `years_experience_avg`
4. `domain_expertise_years_avg`
5. `prior_startup_experience_count`
6. `prior_successful_exits_count`
7. `board_advisor_experience_score`
8. `advisors_count`
9. `team_diversity_percent`
10. `key_person_dependency`

### PRODUCT_FEATURES (9):
1. `product_stage`
2. `product_retention_30d`
3. `product_retention_90d`
4. `dau_mau_ratio`
5. `annual_revenue_run_rate`
6. `revenue_growth_rate_percent`
7. `gross_margin_percent`
8. `ltv_cac_ratio`
9. `funding_stage`

## Frontend Current Implementation

### API Transformation (api.ts) sends 45 fields:
1. Company info (3): company_name, industry, founding_year
2. Capital (8): funding_stage, total_funding, monthly_revenue, burn_rate, runway_months, has_revenue, burn_multiple, ltv_cac_ratio
3. Market (5): sector, market_size, market_growth_rate, competition_level, market_risk_score
4. People (8): team_size, founder_experience, technical_skill, business_skill, industry_experience, technical_founder, team_diversity_score, team_experience_score
5. Advantage (6): product_stage, moat_strength, unique_advantage, patents_count, competitive_moat_score, technology_score
6. Product (15): retention_rate_monthly, daily_active_users, monthly_active_users, product_market_fit_score, feature_adoption_rate, user_engagement_score, time_to_value_days, product_stickiness, activation_rate, customer_lifetime_value, average_deal_size, customer_satisfaction_score, sales_cycle_days, gross_margin, revenue_growth_rate
7. Additional (3): capital_efficiency_score, execution_risk_score, financial_risk_score, business_model_score

## Critical Mismatches

### 1. Missing Backend Features (Not collected in frontend):
- `investor_tier_primary` - Capital form collects `primaryInvestor` but API doesn't send it
- `cash_on_hand_usd` - Capital form collects it but API doesn't send it
- `has_debt` - Capital form collects it but API doesn't send it
- `network_effects_present` - Advantage form collects it but API doesn't send it
- `has_data_moat` - Advantage form collects it but API doesn't send it
- `regulatory_advantage_present` - Advantage form collects it but API doesn't send it
- `tech_differentiation_score` - Advantage form collects it but API doesn't send it
- `switching_cost_score` - Advantage form collects it but API doesn't send it
- `brand_strength_score` - Advantage form collects it but API doesn't send it
- `scalability_score` - Advantage form collects it but API doesn't send it
- `tam_size_usd`, `sam_size_usd`, `som_size_usd` - Market form collects all three but API only sends `market_size`
- `customer_concentration_percent` - Market form collects it but API doesn't send it
- `net_dollar_retention_percent` - Market form collects it but API doesn't send it
- `competitors_named_count` - Market form collects `competitorCount` but API doesn't send it
- `founders_count` - People form collects it but API doesn't send it
- `years_experience_avg` - People form collects `avgExperience` but API doesn't send it
- `domain_expertise_years_avg` - People form collects it but API doesn't send it
- `prior_startup_experience_count` - People form collects it but API doesn't send it
- `prior_successful_exits_count` - People form collects it but API doesn't send it
- `board_advisor_experience_score` - People form collects it but API doesn't send it
- `advisors_count` - People form collects it but API doesn't send it
- `team_diversity_percent` - API sends `team_diversity_score` instead
- `key_person_dependency` - People form collects it but API doesn't send it
- `product_retention_30d`, `product_retention_90d` - People form collects them but API doesn't send them
- `dau_mau_ratio` - People form collects it but API doesn't send it
- `user_growth_rate_percent` - Market form collects it but API doesn't send it

### 2. Extra Frontend Fields (Not expected by backend):
- `company_name`, `industry`, `founding_year` (company info)
- `monthly_revenue`, `has_revenue` (not in backend features)
- `market_risk_score`, `competition_level` (backend expects `competition_intensity`)
- `founder_experience`, `technical_skill`, `business_skill`, `industry_experience`, `technical_founder`
- `moat_strength`, `unique_advantage`, `competitive_moat_score`, `technology_score`
- Many product metrics from Product.tsx form
- `capital_efficiency_score`, `execution_risk_score`, `financial_risk_score`, `business_model_score`

### 3. Name Mismatches:
- Frontend `total_funding` → Backend `total_capital_raised_usd`
- Frontend `burn_rate` → Backend `monthly_burn_usd`
- Frontend `patents_count` → Backend `patent_count`
- Frontend `market_size` → Backend expects `tam_size_usd`, `sam_size_usd`, `som_size_usd`
- Frontend `competition_level` → Backend `competition_intensity`
- Frontend `retention_rate_monthly` → Backend `product_retention_30d`

### 4. Data Type/Format Issues:
- Percentages: Frontend converts to decimals, backend expects percentages
- Boolean values: Frontend sends true/false, backend expects 0/1 for some fields

## Forms Collection vs API Sending Mismatch:
The forms are collecting many of the correct fields, but the API transformation function is not sending them. This is a critical issue where data is being collected but lost in translation.

## Recommendations:
1. Update the API transformation function to include all 45 backend features
2. Ensure proper field name mapping
3. Remove extra fields not expected by backend
4. Fix percentage/decimal conversions
5. Ensure boolean fields are properly formatted