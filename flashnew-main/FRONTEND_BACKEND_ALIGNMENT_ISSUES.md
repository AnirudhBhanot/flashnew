# Frontend-Backend Alignment Issues Report

## Executive Summary
This report details the alignment issues between the FLASH frontend and backend, focusing on API endpoints, port configuration, data structures, CAMP score calculations, and error handling.

## 1. PORT CONFIGURATION ✅ ALIGNED
- **Frontend**: Expects port 8001 (config.ts line 7)
- **Backend**: Runs on port 8001 (api_server.py line 360)
- **Status**: CORRECTLY ALIGNED

## 2. API ENDPOINTS MISALIGNMENT ⚠️

### Backend Available Endpoints (api_server.py)
- `/` - Root endpoint
- `/predict` - Standard prediction
- `/predict_simple` - Alias for /predict
- `/predict_enhanced` - Enhanced prediction with pattern analysis
- `/predict_advanced` - Alias for /predict_enhanced
- `/features` - Feature documentation
- `/patterns` - Available patterns
- `/patterns/{pattern_name}` - Pattern details
- `/analyze_pattern` - Pattern analysis
- `/investor_profiles` - Sample investor profiles
- `/system_info` - System information
- `/health` - Health check

### Frontend Expected Endpoints (config.ts)
- `PREDICT: '/predict'` ✅
- `PREDICT_SIMPLE: '/predict_simple'` ✅
- `PREDICT_ADVANCED: '/predict_advanced'` ✅
- `PREDICT_ENHANCED: '/predict_enhanced'` ✅
- `PATTERNS: '/patterns'` ✅
- `PATTERN_DETAILS: '/patterns/{pattern_name}'` ✅
- `ANALYZE_PATTERN: '/analyze_pattern'` ✅
- `HEALTH: '/health'` ✅
- `INVESTOR_PROFILES: '/investor_profiles'` ✅

**Status**: All endpoints are properly aligned.

## 3. METHOD CALL MISMATCH 🔴 CRITICAL

### Issue: predict_enhanced Method Not Found
- **Location**: api_server.py line 176, 206
- **Problem**: The API server calls `orchestrator.predict_enhanced(features)` but the UnifiedOrchestratorV3 class only has a `predict()` method, not `predict_enhanced()`
- **Impact**: This will cause a runtime error when any prediction endpoint is called

### Fix Required:
Either:
1. Add `predict_enhanced` method to UnifiedOrchestratorV3, or
2. Change API server to call `predict()` instead of `predict_enhanced()`

## 4. DATA STRUCTURE ALIGNMENT

### Frontend to Backend Transformation (type_converter_clean.py)
The TypeConverter properly handles:
- Boolean fields conversion (has_debt, network_effects_present, etc.)
- Optional fields with defaults (runway_months: 12.0, burn_multiple: 2.0, etc.)
- Removal of frontend-only fields (startup_name, hq_location, vertical)
- Type conversions for numeric and string fields
- Special conversions for investor_tier_primary and funding_stage

### Frontend Data Transformation (AnalysisPage.tsx lines 72-108)
- Transforms funding_stage to lowercase with underscores
- Maps investor_tier_primary correctly
- Maintains scalability_score as 1-5 range

**Status**: Data transformations are properly aligned.

## 5. CAMP SCORE CALCULATIONS ⚠️ WARNING

### Backend CAMP Score Calculation (unified_orchestrator_v3.py lines 243-272)
The orchestrator calculates CAMP scores by:
1. Averaging relevant features for each pillar
2. Using 0.5 as fallback if no features available
3. Adding these as additional features for DNA analyzer

### Issues:
1. **Simplistic Calculation**: CAMP scores are simple averages of raw feature values
2. **No Normalization**: Features aren't normalized before averaging
3. **Missing Features**: If features are missing, defaults to 0.5

### Frontend CAMP Score Handling
- Expects pillar_scores in response (WorldClassResults.tsx line 209)
- Backend provides fallback values if missing (api_server.py lines 134-139):
  ```python
  'pillar_scores': response.get('pillar_scores', {
      'capital': 0.5,
      'advantage': 0.5,
      'market': 0.5,
      'people': 0.5
  })
  ```

**Issue**: The predict() method in orchestrator doesn't return pillar_scores, only the API transformation adds them as fallbacks.

## 6. HARDCODED VALUES AND FALLBACKS ⚠️

### Frontend Hardcoded Values:
1. **Temporal predictions fallback to 0.5** (WorldClassResults.tsx lines 488-496)
2. **CAMP score fallbacks** handled by backend transformation

### Backend Hardcoded Values:
1. **CAMP score fallback**: 0.5 for missing features (orchestrator lines 249, 257, 265, 272)
2. **API response fallback CAMP scores**: All default to 0.5 (api_server.py lines 135-139)
3. **Model prediction fallbacks**: 0.5 when models fail (orchestrator lines 121, 135, 147, 159)

## 7. ERROR HANDLING 🔴 NEEDS IMPROVEMENT

### Frontend Error Handling (AnalysisPage.tsx):
- Catches API errors and logs them (line 153)
- Shows error state UI (lines 196-205)
- Validates response format (lines 143-151)

### Backend Error Handling:
- Individual model failures fallback to 0.5 predictions
- General exception returns error response with 0.5 probability
- API endpoints return HTTP 500 with error details

### Issues:
1. **Silent Failures**: Model failures default to 0.5 without clear indication
2. **No Pillar Scores**: When predict() runs successfully, it doesn't return pillar_scores
3. **Misleading Success**: Failed predictions still return "valid" results

## 8. MISSING RESPONSE FIELDS 🔴

The orchestrator's predict() method returns:
```python
{
    "success_probability": float,
    "confidence_score": float,
    "verdict": str,
    "verdict_strength": str,
    "model_predictions": dict,
    "model_agreement": float,
    "weights_used": dict,
    "pattern_insights": list
}
```

But the frontend expects (via transform_response_for_frontend):
```python
{
    'success_probability': float,
    'confidence_interval': dict,
    'verdict': str,
    'strength_level': str,
    'pillar_scores': dict,  # MISSING from orchestrator
    'risk_factors': list,
    'success_factors': list,
    'processing_time_ms': int,
    'timestamp': str,
    'model_version': str,
    'pattern_insights': list (optional),
    'primary_patterns': list (optional)
}
```

## RECOMMENDATIONS

### Immediate Fixes Required:

1. **Fix predict_enhanced method call** (CRITICAL):
   - Either rename orchestrator.predict() to predict_enhanced()
   - Or change API calls from predict_enhanced() to predict()

2. **Add pillar_scores to orchestrator response**:
   - Calculate and return actual CAMP scores from the model
   - Don't rely on API transformation fallbacks

3. **Improve CAMP score calculation**:
   - Normalize features before averaging
   - Use proper weights instead of simple average
   - Return actual calculated scores, not fallbacks

4. **Better error handling**:
   - Return clear error states instead of 0.5 fallbacks
   - Include which models failed in the response
   - Add model health status to responses

5. **Add missing response fields**:
   - Include confidence_interval calculation
   - Add risk_factors and success_factors extraction
   - Include processing_time_ms tracking

### Code Locations for Fixes:

1. **api_server.py line 176, 206**: Change `predict_enhanced` to `predict`
2. **unified_orchestrator_v3.py line 180**: Add pillar_scores to result dict
3. **unified_orchestrator_v3.py lines 243-272**: Improve CAMP calculation logic
4. **api_server.py lines 134-139**: Remove hardcoded fallback CAMP scores
5. **unified_orchestrator_v3.py lines 96-195**: Add proper error states instead of fallbacks