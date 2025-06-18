# Frontend-Backend Feature Mismatch Analysis Report

## Executive Summary

A comprehensive analysis of the FLASH platform reveals significant mismatches between frontend data collection and backend feature expectations. Only **11% (5 out of 45)** of the backend's core features are correctly mapped and collected from the frontend, severely impacting the ML models' ability to make accurate predictions.

## Current State

### Backend System
- **Total Core Features**: 45 features organized by CAMP framework
- **Feature Source**: Defined in `feature_config.py` and `core/feature_registry.py`
- **Categories**: Capital (7), Advantage (8), Market (11), People (10), Product (9)

### Frontend System (flash-frontend-apple)
- **Total Fields Collected**: ~30 actual user inputs
- **Total Fields Sent**: 140+ (most are hardcoded)
- **Categories**: Company Info, Capital, Market, People, Advantage

## Critical Mismatches by Category

### 1. Features Not Collected at All (26 features)
These backend features have no corresponding frontend input and are hardcoded:

**Product Features (100% missing)**
- `retention_rate_monthly` (hardcoded: 0.85)
- `daily_active_users` (hardcoded: 1000)
- `monthly_active_users` (hardcoded: 10000)
- `product_market_fit_score` (hardcoded: 3.5)
- `feature_adoption_rate` (hardcoded: 0.7)
- `user_engagement_score` (hardcoded: 3.5)
- `time_to_value_days` (hardcoded: 7)
- `product_stickiness` (hardcoded: 0.3)
- `activation_rate` (hardcoded: 0.6)

**Customer Metrics (100% missing)**
- `customer_lifetime_value` (hardcoded: 10000)
- `average_deal_size` (hardcoded: 5000)
- `customer_satisfaction_score` (hardcoded: 8)
- `sales_cycle_days` (hardcoded: 30)

**Financial Metrics (partially missing)**
- `gross_margin` (hardcoded: 0.7)
- `revenue_growth_rate` (hardcoded: 1.0)
- `capital_efficiency_score` (hardcoded: 3.5)

**Team & Risk Metrics**
- `team_diversity_score` (hardcoded: 0.6)
- `team_experience_score` (hardcoded: 3.5)
- `execution_risk_score` (hardcoded: 3)
- `market_risk_score` (hardcoded: 3)
- `financial_risk_score` (hardcoded: 3)

### 2. Incorrectly Mapped Features (10 features)

| Backend Feature | Frontend Field | Issue |
|----------------|----------------|--------|
| `burn_multiple` | `ltv_cac_ratio` | Completely different metrics |
| `technical_founder` | `technicalSkill` | Boolean expected, number provided |
| `founding_team_size` | Derived from `teamSize` | Should be separate field |
| `prior_startup_experience` | `founderExperience` | Years vs 1-10 scale |
| `competitive_moat_score` | `moatStrength` | Multiple scores use same value |
| `technology_score` | `moatStrength` | Redundant mapping |
| `business_model_score` | `moatStrength` | Redundant mapping |
| `founder_expertise_years` | `founderExperience` | Scale vs actual years |

### 3. Name Mismatches (15+ instances)

**Backend → Frontend → API Transformation**
- `market_tam_billions` → `marketSize` → `tam_size` 
- `revenue_monthly` → `monthlyRevenue` → `monthly_revenue`
- `founding_year` → `foundingDate` → Calculated value
- `has_revenue` → Not collected → Derived boolean

### 4. Type Mismatches

| Field | Backend Type | Frontend Type | Issue |
|-------|--------------|---------------|--------|
| `technical_founder` | boolean | number (1-10) | Type conversion error |
| `burn_multiple` | float (ratio) | float (different metric) | Wrong calculation |
| Scores | 1-5 scale | 1-10 scale | Scale mismatch |
| `founding_year` | integer | date string | Format conversion |

### 5. Structural Differences

**Backend Structure**: Flat 45 features
```python
{
    "revenue_monthly": 50000,
    "burn_rate": 100000,
    "team_size": 10,
    ...
}
```

**Frontend Structure**: Nested categories
```javascript
{
    company_info: { name, industry, ... },
    capital_metrics: { monthly_revenue, burn_rate, ... },
    market_metrics: { tam_size, ... },
    ...
}
```

## Impact Analysis

### 1. Model Performance
- Models trained on 45 features receive mostly hardcoded values
- Real user input only affects ~11% of model features
- Predictions likely based more on defaults than actual company data

### 2. User Experience
- Users fill detailed forms but most data is ignored
- False sense of comprehensive analysis
- Results may not reflect actual company situation

### 3. Data Quality
- 58% of features use hardcoded values
- Loss of variance in critical features
- Models cannot distinguish between different companies effectively

## Recommended Fixes

### Immediate Priority (Critical)
1. **Fix burn_multiple calculation**
   - Current: Uses LTV/CAC ratio
   - Should be: Net burn / Net new ARR

2. **Add missing product metrics section**
   - User retention rates
   - DAU/MAU metrics
   - Product-market fit indicators

3. **Fix type conversions**
   - Boolean fields should use toggle switches
   - Align score scales (1-5 vs 1-10)

### High Priority
1. **Add financial metrics collection**
   - Gross margin
   - Revenue growth rate
   - Capital efficiency metrics

2. **Expand team metrics**
   - Diversity scores
   - Experience breakdowns
   - Risk assessments

3. **Customer metrics section**
   - Lifetime value
   - Satisfaction scores
   - Sales metrics

### Medium Priority
1. **Align field names across systems**
2. **Remove hardcoded defaults**
3. **Add validation for data consistency**

## Technical Implementation Notes

The mismatch occurs in the API transformation layer (`api_server_unified.py`), where frontend data is mapped to backend features. The transformation function attempts to derive 45 features from ~30 inputs, resulting in extensive use of default values.

### Current Flow
1. Frontend collects data in nested structure
2. API flattens and transforms data
3. Missing fields get hardcoded values
4. Backend receives mostly static data

### Recommended Flow
1. Expand frontend to collect all 45 core features
2. Direct field mapping without complex transformations
3. Clear indication of optional vs required fields
4. Validation at each layer

## Conclusion

The current system has a fundamental disconnect between what users input and what the ML models receive. This significantly impacts the platform's ability to provide accurate, personalized startup assessments. Addressing these mismatches should be the top priority for improving FLASH's predictive capabilities.