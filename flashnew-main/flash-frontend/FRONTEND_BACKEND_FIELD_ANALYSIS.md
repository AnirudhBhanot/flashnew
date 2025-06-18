# Frontend-Backend Field Analysis for FLASH Platform

## Summary of Findings

### Frontend Fields (DataCollectionCAMP Component)
The frontend collects exactly **45 fields** organized into the CAMP framework:

#### Capital (10 fields)
1. funding_stage
2. total_capital_raised_usd
3. cash_on_hand_usd
4. monthly_burn_usd
5. annual_revenue_run_rate
6. revenue_growth_rate_percent
7. gross_margin_percent
8. ltv_cac_ratio
9. investor_tier_primary
10. has_debt

#### Advantage (11 fields)
1. patent_count
2. network_effects_present
3. has_data_moat
4. regulatory_advantage_present
5. tech_differentiation_score
6. switching_cost_score
7. brand_strength_score
8. scalability_score
9. product_stage
10. product_retention_30d
11. product_retention_90d

#### Market (12 fields)
1. sector
2. tam_size_usd
3. sam_size_usd
4. som_size_usd
5. market_growth_rate_percent
6. customer_count
7. customer_concentration_percent
8. user_growth_rate_percent
9. net_dollar_retention_percent
10. competition_intensity
11. competitors_named_count
12. dau_mau_ratio

#### People (10 fields)
1. founders_count
2. team_size_full_time
3. years_experience_avg
4. domain_expertise_years_avg
5. prior_startup_experience_count
6. prior_successful_exits_count
7. board_advisor_experience_score
8. advisors_count
9. team_diversity_percent
10. key_person_dependency

### Additional/Calculated Fields (2 fields)
1. runway_months (calculated from cash_on_hand_usd / monthly_burn_usd)
2. burn_multiple (hardcoded to 2, noted as "will be calculated server-side")

**Total: 45 core fields + 2 calculated fields = 47 fields sent to backend**

## Key Transformations and Issues

### 1. Percentage to Decimal Conversion
The frontend converts these fields from percentage (0-100) to decimal (0-1):
- product_retention_30d
- product_retention_90d  
- scalability_score

**ISSUE**: scalability_score should NOT be converted as it's a 1-5 score, not a percentage.

### 2. Field Name Consistency
All field names match exactly between frontend and types.ts - no discrepancies found.

### 3. Enum Value Mismatches
Several fields have inconsistent enum values:

**funding_stage**:
- Frontend: ['Pre-seed', 'Seed', 'Series A', 'Series B', 'Series C']
- Test data uses: ['pre_seed', 'seed', 'series_a', 'series_b']

**investor_tier_primary**:
- Frontend: ['Tier 1', 'Tier 2', 'Tier 3', 'Angel']
- Test data uses: ['tier_1', 'tier_2', 'tier_3', 'none']

**product_stage**:
- Frontend: ['MVP', 'Beta', 'GA', 'Mature']
- Test data uses: ['mvp', 'beta', 'growth', 'mature']

### 4. Data Type Issues
The worst case test scenario has incorrect data types:
- scalability_score: 10 (should be 1-5)
- product_retention_30d: 10 (should be 0-1 after conversion)
- product_retention_90d: 2 (should be 0-1 after conversion)

### 5. Missing Backend Validation
Without access to the backend code, we cannot verify:
- If the backend expects the same 45 fields
- If field names match exactly
- If the backend expects percentages or decimals
- If enum values are validated/transformed

## Recommendations

1. **Fix scalability_score conversion** - Remove it from percentage conversion logic
2. **Standardize enum values** - Use consistent casing (prefer lowercase with underscores)
3. **Fix test data generator** - Ensure all values respect their constraints
4. **Add field validation** - Validate data before sending to API
5. **Document API contract** - Create clear documentation of expected field formats
6. **Add backend field list** - Need to verify backend expectations match frontend

## API Request Format
The frontend sends data to `/predict` endpoint with:
```json
{
  // All 45 fields from above
  "runway_months": <calculated>,
  "burn_multiple": 2
}
```

## Next Steps
To complete this analysis, we need:
1. Access to backend code to verify field expectations
2. API documentation showing expected request/response format
3. Validation rules for each field
4. Clear mapping of any field transformations