#!/usr/bin/env python3
"""
Summary of CAMP vs Success Probability Issues
"""

print("""
🔍 CAMP vs Success Probability Alignment Issues Summary
======================================================

## Current Issues Found:

1. **Orchestrator Version Mismatch**
   - API uses: `unified_orchestrator_v3_integrated`
   - Tests used: `unified_orchestrator_v3_fixed`
   - Different normalization logic between versions

2. **CAMP Score Calculation Problems**
   - String features (investor_tier_primary, sector) cause type errors in normalization
   - CAMP scores returning 0% for all scenarios in fixed version
   - Normalization tries to clip string values as numeric

3. **Model Feature Mismatch**
   - DNA analyzer expects 45 features, gets 49 (includes 4 CAMP scores)
   - Temporal model expects 46 features, gets 48
   - Only industry model working correctly

4. **Response Structure Inconsistency**
   - Orchestrator returns: 'pillar_scores'
   - Tests expect: 'camp_analysis'
   - API transforms pillar_scores but doesn't rename to camp_analysis

5. **Missing CAMP Score Mapping**
   - API server doesn't map pillar_scores to camp_analysis
   - Frontend may expect camp_analysis field

## Root Cause:
The CAMP scores are calculated correctly in the integrated orchestrator, but:
- Feature normalization has bugs with string types
- Model training doesn't match current feature expectations
- Response field naming is inconsistent

## Recommended Fixes:

1. **Fix Normalization** (models/unified_orchestrator_v3_integrated.py)
   - Skip string features in normalization
   - Handle investor_tier and sector as categorical

2. **Update Model Features**
   - Retrain models with consistent feature counts
   - Or fix feature preparation to match trained models

3. **Standardize Response**
   - Add camp_analysis field to response
   - Map pillar_scores -> camp_analysis

4. **Test with API**
   - Create test that uses actual API endpoint
   - Verify CAMP scores are calculated and returned correctly
""")