# API Endpoint Mapping: Frontend vs Backend

## Frontend Configuration (from config.ts)

```typescript
API_BASE_URL: 'http://localhost:8001' (default)

ENDPOINTS: {
  PREDICT: '/predict',
  PREDICT_SIMPLE: '/predict_simple',
  PREDICT_ADVANCED: '/predict_advanced',
  PREDICT_ENHANCED: '/predict_enhanced',
  PATTERNS: '/patterns',
  PATTERN_DETAILS: '/patterns/{pattern_name}',
  ANALYZE_PATTERN: '/analyze_pattern',
  HEALTH: '/health',
  INVESTOR_PROFILES: '/investor_profiles'
}
```

## Backend Endpoints (from api_server.py)

### Implemented Endpoints:
1. **GET /** - Root endpoint
2. **POST /predict** - Standard prediction endpoint
3. **POST /predict_simple** - Alias for /predict
4. **POST /predict_enhanced** - Enhanced prediction with pattern analysis
5. **POST /predict_advanced** - Alias for /predict_enhanced
6. **GET /features** - Get feature documentation
7. **GET /patterns** - Get available patterns
8. **GET /patterns/{pattern_name}** - Get details for specific pattern
9. **POST /analyze_pattern** - Analyze patterns for a startup
10. **GET /investor_profiles** - Get sample investor profiles
11. **GET /system_info** - Get system information
12. **GET /health** - Health check endpoint

### Missing from Backend:
- **POST /explain** - Used by ExplainabilityPanel.tsx but not implemented

## Frontend API Usage Analysis

### 1. App.tsx (Main App)
- **Endpoint Used**: `/predict`
- **Method**: POST
- **Request Body**: StartupData object
- **Expected Response**:
  ```typescript
  {
    success_probability: number,
    confidence_interval: { lower: number, upper: number },
    verdict: string,
    strength_level: string,
    pillar_scores: {
      capital: number,
      advantage: number,
      market: number,
      people: number
    },
    risk_factors: string[],
    success_factors: string[],
    processing_time_ms: number,
    timestamp: string,
    model_version: string,
    pattern_insights?: string[],
    primary_patterns?: string[]
  }
  ```

### 2. AnalysisPage.tsx (V3)
- **Endpoints Used**: 
  - `/predict` (standard)
  - `/predict_enhanced` (when usePatternAPI=true)
  - `/predict_advanced` (when useAdvancedAPI=true)
- **Method**: POST
- **Data Transformation**: Yes (transforms funding_stage, investor_tier_primary, product_stage)
- **Error Handling**: Yes (catches and logs errors)

### 3. TestPage.tsx
- **Endpoint Used**: `/predict` (Note: Uses port 8000 instead of 8001)
- **Method**: POST
- **Error Handling**: Falls back to mock data on error

### 4. ExplainabilityPanel.tsx
- **Endpoint Used**: `/explain` ❌ NOT IMPLEMENTED IN BACKEND
- **Method**: POST
- **Expected Response**: Explanation data with plots and insights

## Request/Response Format Analysis

### Frontend StartupData Structure
The frontend sends all fields from the StartupData interface, including:
- Capital metrics (16 fields)
- Advantage metrics (11 fields)
- Market metrics (12 fields)
- People metrics (10 fields)
- Additional frontend fields (4 optional fields)

### Backend StartupData Model
The backend expects the same fields but with some differences:
- Ignores frontend-specific fields: `startup_name`, `hq_location`, `vertical`
- All fields have validation (Field constraints, ge/le limits)
- Some fields have default values

### Response Transformation
The backend transforms its response in `transform_response_for_frontend()`:
1. Calculates verdict based on success_probability
2. Adds confidence_interval based on confidence_score
3. Maps pillar_scores (defaults if not present)
4. Extracts risk_factors and success_factors from interpretation
5. Adds pattern insights if available

## Field Name Consistency Issues

### Port Inconsistency
- Config.ts: Uses port 8001
- TestPage.tsx: Uses port 8000
- **Issue**: TestPage will fail to connect

### Data Type Transformations
Frontend transforms certain fields before sending:
1. `funding_stage`: Converts to lowercase with underscores
2. `investor_tier_primary`: Maps to specific values (tier_1, tier_2, etc.)
3. `product_stage`: Converts to lowercase

### Missing Error Response Handling
Frontend components handle errors differently:
- App.tsx: Returns to collection state on error
- AnalysisPage.tsx: Logs error and shows message
- TestPage.tsx: Falls back to mock data
- ExplainabilityPanel.tsx: Sets error state

## Key Findings

### ✅ Working Endpoints:
1. `/predict` - Main analysis endpoint works correctly
2. `/predict_enhanced` - Pattern-enhanced prediction works
3. `/patterns` - Pattern listing works
4. `/health` - Health check works
5. `/investor_profiles` - Sample data works

### ❌ Issues Found:
1. **Missing /explain endpoint** - ExplainabilityPanel expects this but it's not implemented
2. **Port mismatch** - TestPage uses wrong port (8000 vs 8001)
3. **No standardized error response format** - Frontend expects different error formats
4. **Missing CORS for /explain** - Even if implemented, would need CORS support

### 🔄 Data Flow Issues:
1. Frontend sends optional fields that backend ignores
2. Backend provides default values for missing fields
3. Response transformation may lose some backend data
4. Pattern analysis data only included with enhanced endpoints

## Recommendations

1. **Implement /explain endpoint** in backend for ExplainabilityPanel
2. **Standardize port usage** across all frontend components
3. **Create consistent error response format**:
   ```json
   {
     "error": "string",
     "detail": "string",
     "status_code": number
   }
   ```
4. **Document required vs optional fields** clearly
5. **Add API versioning** for future compatibility
6. **Implement request/response logging** for debugging
7. **Add input validation error details** in responses

## Summary Table

| Endpoint | Frontend Usage | Backend Status | Issues |
|----------|---------------|----------------|---------|
| `/predict` | ✅ App.tsx, AnalysisPage.tsx, TestPage.tsx | ✅ Implemented | Port mismatch in TestPage |
| `/predict_simple` | ✅ Config defined | ✅ Implemented (alias) | None |
| `/predict_advanced` | ✅ AnalysisPage.tsx | ✅ Implemented (alias) | None |
| `/predict_enhanced` | ✅ AnalysisPage.tsx | ✅ Implemented | None |
| `/patterns` | ✅ Config defined | ✅ Implemented | None |
| `/patterns/{pattern_name}` | ✅ Config defined | ✅ Implemented | None |
| `/analyze_pattern` | ✅ Config defined | ✅ Implemented | None |
| `/health` | ✅ Config defined | ✅ Implemented | None |
| `/investor_profiles` | ✅ Config defined | ✅ Implemented | None |
| `/explain` | ❌ ExplainabilityPanel.tsx | ❌ NOT Implemented | Missing endpoint |
| `/features` | ❌ Not in config | ✅ Implemented | Config not updated |
| `/system_info` | ❌ Not in config | ✅ Implemented | Config not updated |
| `/` | ❌ Not used | ✅ Implemented | Root endpoint |

## Critical Action Items

1. **URGENT**: Implement `/explain` endpoint in backend or remove ExplainabilityPanel usage
2. **HIGH**: Fix port mismatch in TestPage.tsx (8000 → 8001)
3. **MEDIUM**: Update frontend config to include `/features` and `/system_info`
4. **LOW**: Consider removing unused endpoint aliases for clarity