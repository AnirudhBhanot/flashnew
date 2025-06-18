# Frontend vs Backend Feature Name Comparison

## Exact Matches ✅ (Already Correct)
These features have the same name in frontend and backend:

### Capital Features
- `funding_stage` ✅
- `total_capital_raised_usd` ✅
- `cash_on_hand_usd` ✅
- `monthly_burn_usd` ✅
- `annual_revenue_run_rate` ✅
- `revenue_growth_rate_percent` ✅
- `gross_margin_percent` ✅
- `ltv_cac_ratio` ✅
- `investor_tier_primary` ✅
- `has_debt` ✅

### Advantage Features
- `patent_count` ✅
- `network_effects_present` ✅
- `has_data_moat` ✅
- `regulatory_advantage_present` ✅
- `tech_differentiation_score` ✅
- `switching_cost_score` ✅
- `brand_strength_score` ✅
- `scalability_score` ✅
- `product_stage` ✅
- `product_retention_30d` ✅
- `product_retention_90d` ✅

### Market Features
- `sector` ✅
- `tam_size_usd` ✅
- `sam_size_usd` ✅
- `som_size_usd` ✅
- `market_growth_rate_percent` ✅
- `customer_count` ✅
- `customer_concentration_percent` ✅
- `user_growth_rate_percent` ✅
- `net_dollar_retention_percent` ✅
- `competition_intensity` ✅
- `competitors_named_count` ✅
- `dau_mau_ratio` ✅

### People Features
- `founders_count` ✅
- `team_size_full_time` ✅
- `years_experience_avg` ✅
- `domain_expertise_years_avg` ✅
- `prior_startup_experience_count` ✅
- `prior_successful_exits_count` ✅
- `board_advisor_experience_score` ✅
- `advisors_count` ✅
- `team_diversity_percent` ✅
- `key_person_dependency` ✅

## Missing Features ❌
Backend expects these but frontend doesn't collect:

### Capital Features
- `runway_months` (backend calculates from cash/burn)
- `burn_multiple` (backend calculates)

## Summary

**GOOD NEWS**: The frontend is already using the correct feature names! All 43 features that the frontend collects match exactly with the backend expectations.

The only 2 missing features are:
- `runway_months` - Can be calculated from cash_on_hand_usd / monthly_burn_usd
- `burn_multiple` - Can be calculated from burn rate and revenue growth

These are calculated fields that the backend can compute, not something the user needs to input.