# FLASH Frontend-Backend Field Analysis Report

## Executive Summary
A comprehensive analysis of the FLASH frontend wizard reveals significant mismatches between the frontend data collection fields and backend API expectations. While the frontend collects data across the CAMP framework (Capital, Advantage, Market, People), there are critical differences in field names, data types, and API structure.

## Frontend Data Collection (DataCollectionCAMP.tsx)

### Fields Collected by the Frontend Wizard

#### Capital Fields (7 fields)
1. `funding_stage` - Select: ['Pre-seed', 'Seed', 'Series A', 'Series B', 'Series C']
2. `total_capital_raised_usd` - Number
3. `cash_on_hand_usd` - Number
4. `monthly_burn_usd` - Number
5. `annual_revenue_run_rate` - Number
6. `revenue_growth_rate_percent` - Number (-100 to 1000)
7. `gross_margin_percent` - Number (-100 to 100)
8. `ltv_cac_ratio` - Number (0 to 100)
9. `investor_tier_primary` - Select: ['Tier 1', 'Tier 2', 'Tier 3', 'Angel']
10. `has_debt` - Boolean

#### Advantage Fields (11 fields)
1. `patent_count` - Number
2. `network_effects_present` - Boolean
3. `has_data_moat` - Boolean
4. `regulatory_advantage_present` - Boolean
5. `tech_differentiation_score` - Number (1-5)
6. `switching_cost_score` - Number (1-5)
7. `brand_strength_score` - Number (1-5)
8. `scalability_score` - Number (1-5)
9. `product_stage` - Select: ['MVP', 'Beta', 'GA', 'Mature']
10. `product_retention_30d` - Number (0-100%) - **Converted to decimal in frontend**
11. `product_retention_90d` - Number (0-100%) - **Converted to decimal in frontend**

#### Market Fields (12 fields)
1. `sector` - Text (free form)
2. `tam_size_usd` - Number
3. `sam_size_usd` - Number
4. `som_size_usd` - Number
5. `market_growth_rate_percent` - Number (-50 to 200)
6. `customer_count` - Number
7. `customer_concentration_percent` - Number (0-100)
8. `user_growth_rate_percent` - Number (-100 to 1000)
9. `net_dollar_retention_percent` - Number (0-300)
10. `competition_intensity` - Number (1-5)
11. `competitors_named_count` - Number
12. `dau_mau_ratio` - Number (0-1)

#### People Fields (10 fields)
1. `founders_count` - Number (1-10)
2. `team_size_full_time` - Number
3. `years_experience_avg` - Number (0-50)
4. `domain_expertise_years_avg` - Number (0-50)
5. `prior_startup_experience_count` - Number
6. `prior_successful_exits_count` - Number
7. `board_advisor_experience_score` - Number (1-5)
8. `advisors_count` - Number
9. `team_diversity_percent` - Number (0-100)
10. `key_person_dependency` - Boolean

### Additional Frontend Processing
- `runway_months` - Calculated: cash_on_hand_usd / monthly_burn_usd (capped at 60)
- `burn_multiple` - Set to 2 (placeholder, calculated server-side)

## Backend API Expectations

### API Server Models
The backend has **two different data models**:

#### 1. api_server.py StartupData Model (Old format - 46 fields)
This appears to be an older format with different field names:
- Uses fields like `founding_year`, `founder_experience_years`, `team_size`
- Has different structure than frontend sends
- Not aligned with CAMP framework

#### 2. feature_config.py (45 features - Current format)
This is the canonical feature set that aligns with frontend:
- Total: 45 features
- Capital: 7 features
- Advantage: 8 features  
- Market: 11 features
- People: 10 features
- Product: 9 features (includes some overlap)

## Critical Mismatches

### 1. 🔴 API Endpoint Mismatch
**Frontend expects:**
- `/predict_simple`
- `/predict_advanced` 
- `/predict_enhanced`

**Backend provides:**
- `/predict` (standard)
- `/predict_enhanced` (with patterns)
- `/predict_advanced` (alias for enhanced)

### 2. 🔴 Data Type Mismatches
**Frontend sends:**
- Booleans as `true/false`
- Retention rates as percentages (0-100)

**Backend expects:**
- Booleans as 0/1
- Retention rates as decimals (0-1)

**Affected fields:**
- `has_debt`
- `network_effects_present`
- `has_data_moat`
- `regulatory_advantage_present`
- `key_person_dependency`

### 3. 🟡 Field Naming Transformations
**Frontend transformations needed:**
- `funding_stage`: Spaces to underscores, lowercase
- `investor_tier_primary`: 'Angel' → 'none', add underscores
- `product_stage`: Convert to lowercase

### 4. 🟡 Missing Type Converter
The backend references `TypeConverter` class that doesn't exist, causing potential runtime errors.

### 5. 🟡 Frontend-Only Fields
The frontend types.ts includes fields not used:
- `team_cohesion_score?`
- `hiring_velocity_score?`
- `diversity_score?`
- `technical_expertise_score?`

## Data Flow Analysis

### Frontend → API Flow
1. User fills CAMP forms in `DataCollectionCAMP.tsx`
2. Data validated and transformed:
   - Retention percentages → decimals
   - Calculated fields added
3. Sent to `AnalysisPage.tsx`
4. `transformDataForAPI()` applies transformations:
   - funding_stage formatting
   - investor_tier mapping
   - product_stage lowercase
5. POST to API endpoint

### API Processing
1. API receives data
2. **Missing**: TypeConverter should transform booleans
3. Data passed to UnifiedOrchestratorV3
4. Response transformed for frontend

## Required Fixes

### Immediate (Critical)
1. **Create TypeConverter class**:
```python
class TypeConverter:
    def convert_frontend_to_backend(self, data):
        # Convert booleans to 0/1
        # Remove extra fields
        # Ensure all 45 features present
```

2. **Add missing endpoints** or update frontend config

3. **Fix boolean handling** in API

### Short-term
1. Align StartupData models between files
2. Document field transformations
3. Add validation for all 45 features

### Long-term
1. Generate TypeScript types from backend
2. Create single source of truth for fields
3. Add integration tests

## Summary
The frontend collects the correct 45 features across CAMP pillars, but several transformation and type conversion issues prevent smooth API communication. The most critical issue is the missing TypeConverter implementation and boolean type mismatches.

## Validation Checklist
- [ ] All 45 features collected ✅
- [ ] Boolean conversion working ❌
- [ ] Endpoint alignment ❌
- [ ] Type converter implemented ❌
- [ ] Field transformations documented ⚠️
- [ ] Retention rates converted correctly ✅
- [ ] Funding stage formatting ✅
- [ ] Investor tier mapping ✅