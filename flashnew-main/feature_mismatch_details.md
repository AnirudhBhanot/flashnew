# Detailed Feature Mismatch Analysis

## Backend Feature Registry vs Frontend Assessment Store

### Core 45 Backend Features Breakdown

Based on `feature_registry.py`, the backend expects these 45 features in exact order:

#### Positions 0-6 (Capital/Revenue)
0. `funding_stage` ✓ Mapped from `companyInfo.stage`
1. `revenue_growth_rate` ❌ Hardcoded to 100%
2. `team_size_full_time` ✓ Mapped from `people.teamSize`
3. `total_capital_raised_usd` ✓ Mapped from `capital.totalFundingRaised`
4. `annual_recurring_revenue_millions` ❌ Not collected (different from ARR)
5. `annual_revenue_run_rate` ✓ Mapped from `capital.annualRevenueRunRate`
6. `burn_multiple` ⚠️ Incorrectly mapped from `ltvCacRatio`

#### Positions 7-17 (Market)
7. `market_tam_billions` ⚠️ Frontend has generic `marketSize`, not billions
8. `market_growth_rate` ✓ Mapped from `market.marketGrowthRate`
9. `market_competitiveness` ✓ Mapped from `market.competitionLevel`
10. `customer_acquisition_cost` ✓ Mapped from `market.customerAcquisitionCost`
11. `customer_lifetime_value` ❌ Not collected
12. `customer_growth_rate` ❌ Hardcoded to 100%
13. `net_revenue_retention` ❌ Hardcoded to 110%
14. `average_deal_size` ❌ Not collected
15. `sales_cycle_days` ❌ Not collected
16. `international_revenue_percent` ❌ Not collected
17. `target_enterprise` ❌ Not collected

#### Positions 18-26 (Product/Advantage)
18. `product_market_fit_score` ❌ Not collected
19. `technology_score` ⚠️ Derived from `moatStrength`
20. `scalability_score` ❌ Hardcoded to 4
21. `has_patent` ✓ Mapped from `advantage.hasPatents`
22. `research_development_percent` ❌ Not collected
23. `uses_ai_ml` ❌ Not collected
24. `cloud_native` ❌ Hardcoded to true
25. `mobile_first` ❌ Not collected
26. `platform_business` ❌ Not collected

#### Positions 27-35 (People)
27. `founder_experience_years` ⚠️ Scale value used instead of years
28. `repeat_founder` ⚠️ Boolean `previousStartups` not exact match
29. `technical_founder` ⚠️ Number collected, boolean expected
30. `employee_growth_rate` ❌ Not collected
31. `advisor_quality_score` ❌ Hardcoded to 3
32. `board_diversity_score` ❌ Not collected
33. `team_industry_experience` ⚠️ Scale value used instead of years
34. `key_person_dependency` ❌ Hardcoded to 3
35. `top_university_alumni` ❌ Not collected

#### Positions 36-44 (Additional)
36. `investor_tier_primary` ⚠️ Calculated from funding amount
37. `active_investors` ❌ Not collected
38. `cash_on_hand_months` ⚠️ Different from runway_months
39. `runway_months` ✓ Mapped from `capital.runwayMonths`
40. `time_to_next_funding` ❌ Not collected
41. `previous_exit` ⚠️ Number collected, boolean expected
42. `industry_connections` ❌ Not collected
43. `media_coverage` ❌ Not collected
44. `regulatory_risk` ❌ Not collected

## Critical Mismatches in API Transformation

Looking at `api.ts` `transformAssessmentToAPI()`:

### 1. Wrong Feature Mapping
```typescript
// WRONG: burn_multiple should NOT be ltv_cac_ratio
burn_multiple: Number(capital.ltvCacRatio) || 2.5,

// WRONG: These are different metrics in backend
tech_differentiation_score: advantage.moatStrength || 3,
switching_cost_score: advantage.moatStrength || 3,
```

### 2. Missing Backend Features From Registry
The transformation is missing these features that backend expects:
- `annual_recurring_revenue_millions` (position 4)
- `customer_lifetime_value` (position 11)
- `average_deal_size` (position 14)
- `sales_cycle_days` (position 15)
- `product_market_fit_score` (position 18)
- Many others...

### 3. Feature Name Mismatches
Backend registry uses different names than transformation:
- Registry: `revenue_growth_rate` → Transform: `revenue_growth_rate_percent`
- Registry: `market_tam_billions` → Transform: `tam_size_usd`
- Registry: `market_competitiveness` → Transform: `competition_intensity`
- Registry: `founder_experience_years` → Transform: `years_experience_avg`

### 4. Type Mismatches in Registry vs Transform
- Registry expects `technical_founder` as boolean
- Transform sends `technicalFounders` as number
- Registry expects `previous_exit` as boolean  
- Transform sends `prior_successful_exits_count` as number

## Data Flow Issues

1. **Frontend → API Transform**: Loses data through hardcoding
2. **API Transform → Backend**: Field names don't match registry
3. **Backend Registry**: Expects different types than provided

## Most Critical Fixes Needed

1. **Burn Multiple**: Currently using LTV:CAC ratio - completely wrong metric
2. **Revenue Metrics**: Missing ARR in millions, growth rate hardcoded
3. **Customer Metrics**: Missing CLV, deal size, sales cycle
4. **Product Metrics**: No PMF score, retention, or product stage input
5. **Field Names**: Transform doesn't match backend registry names
6. **Type Safety**: Booleans vs numbers inconsistent

## Recommended Immediate Actions

1. Fix `burn_multiple` calculation (should be net burn / net new ARR)
2. Add missing critical fields to frontend forms
3. Update API transformation to match exact registry field names
4. Ensure type consistency (boolean vs number)
5. Remove hardcoded values for collectable metrics