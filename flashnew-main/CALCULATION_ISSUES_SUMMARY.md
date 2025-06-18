# Flash Calculation Logic Issues - Comprehensive Analysis

## Executive Summary

The Flash application has critical issues with its calculation logic, resulting in hardcoded fallback values throughout the system. The main ML models (DNA analyzer and Pattern system) always return 0.5 due to feature name mismatches, making the system unable to differentiate between good and bad startups.

## Major Issues Identified

### 1. Feature Name Mismatch (CRITICAL)

**Frontend sends:**
- `founding_year`, `founder_experience_years`, `team_size`, `total_funding`
- `burn_rate`, `tam_size`, `revenue_growth_rate`

**Backend expects:**
- `total_capital_raised_usd`, `team_size_full_time`, `years_experience_avg`
- `monthly_burn_usd`, `tam_size_usd`, `revenue_growth_rate_percent`

**Impact:** DNA analyzer and Pattern system always fall back to 0.5

### 2. Hardcoded 0.5 Fallback Values

Location: `unified_orchestrator_v3.py`

```python
# DNA analyzer (lines 119-122)
except Exception as e:
    logger.error(f"DNA analyzer prediction failed: {e}")
    predictions["dna_analyzer"] = 0.5  # HARDCODED FALLBACK
    
# Pattern analysis (lines 133-135)
except Exception as e:
    logger.error(f"Pattern analysis failed: {e}")
    predictions["pattern_analysis"] = 0.5  # HARDCODED FALLBACK
```

### 3. No Financial Calculations Performed

**Missing calculations:**
- **LTV/CAC ratio**: Expected from frontend, not calculated
- **Runway months**: Expected from frontend, not calculated  
- **Burn multiple**: Expected from frontend, not calculated
- **Gross margin**: Not provided by frontend, not calculated

### 4. CAMP Score Calculations Are Oversimplified

Location: `unified_orchestrator_v3.py` (lines 247-272)

```python
# Current implementation - simple mean
camp_scores['capital_score'] = features[capital_cols].mean(axis=1).fillna(0.5)
```

**Issues:**
- Simple average of features, no domain logic
- Falls back to 0.5 if features missing
- No weighted calculations based on importance

### 5. Limited Score Range Due to Model Weights

```python
weights = {
    "camp_evaluation": 0.50,      # Always 0.5 (broken)
    "pattern_analysis": 0.25,     # Always 0.5 (broken)
    "industry_specific": 0.15,    # Works (0.48-0.51)
    "temporal_prediction": 0.10   # Works (0.27-0.61)
}
```

**Result:** Final scores limited to 0.375-0.625 range
- Only "CONDITIONAL PASS" or "CONDITIONAL FAIL" verdicts possible
- Cannot achieve "PASS" or "FAIL" verdicts

### 6. Frontend Displays Hardcoded Pillar Scores

Location: `api_server_unified.py` (lines 134-140)

```python
'pillar_scores': response.get('pillar_scores', {
    'capital': 0.5,    # HARDCODED
    'advantage': 0.5,  # HARDCODED
    'market': 0.5,     # HARDCODED
    'people': 0.5      # HARDCODED
})
```

## Calculations That DO Work

1. **Temporal features** (`unified_orchestrator_v3.py` lines 296-310)
   - `growth_momentum = revenue_growth * user_growth / 100`
   - `efficiency_trend = 1 / (1 + burn_multiple)`

2. **Model agreement** (line 169)
   - `model_agreement = 1 - np.std(model_values)`

3. **Pattern insights** (lines 369-400)
   - Business logic for string insights based on thresholds

## Test Results

From running `test_calculations.py`:

```
Full data 0.5 values:
  - dna_analyzer: 0.5 (likely fallback)
  - pattern_analysis: 0.5 (likely fallback)

Extreme data 0.5 values:
  - dna_analyzer: 0.5 (likely fallback)
  - pattern_analysis: 0.5 (likely fallback)
```

Even with extreme values (100x TAM, 20 patents, etc.), scores remain at 0.5.

## Recommendations

1. **Immediate Fixes:**
   - Create feature name mapping between frontend and backend
   - Implement actual financial calculations
   - Remove hardcoded fallback values

2. **Short-term:**
   - Retrain models with correct feature names
   - Implement proper CAMP score calculations with business logic
   - Add integration tests to catch feature mismatches

3. **Long-term:**
   - Redesign feature engineering pipeline
   - Implement domain-specific calculations for each pillar
   - Add monitoring for model performance

## Example of Proper Calculation Implementation

```python
def calculate_ltv_cac_ratio(customer_lifetime_value, customer_acquisition_cost):
    """Calculate LTV/CAC ratio with proper handling"""
    if customer_acquisition_cost <= 0:
        return 0  # Invalid CAC
    ratio = customer_lifetime_value / customer_acquisition_cost
    return min(ratio, 10)  # Cap at reasonable maximum

def calculate_runway_months(cash_on_hand, monthly_burn):
    """Calculate runway with proper handling"""
    if monthly_burn <= 0:
        return 120  # No burn = infinite runway (capped)
    return min(cash_on_hand / monthly_burn, 120)

def calculate_burn_multiple(annual_burn, net_new_arr):
    """Calculate burn multiple with proper handling"""
    if net_new_arr <= 0:
        return 20  # No growth = worst case (capped)
    return min(annual_burn / net_new_arr, 20)
```

## Conclusion

The Flash system is currently unable to perform meaningful startup evaluation due to:
1. Feature name mismatches causing 75% of model weight to default to 0.5
2. No actual financial calculations being performed
3. Hardcoded fallback values throughout the codebase
4. Frontend displaying static pillar scores

The system requires significant fixes to function as intended.