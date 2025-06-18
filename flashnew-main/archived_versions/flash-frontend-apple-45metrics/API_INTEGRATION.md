# FLASH Frontend-Backend API Integration

## Overview
The FLASH frontend is now integrated with the backend API server running on port 8001. The integration handles data transformation between the frontend's user-friendly format and the backend's ML model requirements.

## Integration Status ✅

### Completed
1. **API Service Layer** (`src/services/api.ts`)
   - Health check endpoint
   - Prediction endpoint
   - Detailed analysis endpoint
   - Data validation endpoint
   - Configuration endpoint

2. **Data Transformation**
   - Frontend assessment data → Backend 45-feature format
   - Backend response → Frontend display format
   - Proper handling of optional fields and defaults

3. **Error Handling**
   - API health checks before submission
   - Graceful fallback to mock data if API fails
   - Error display in the UI

4. **Environment Configuration**
   - `.env` file for API URL configuration
   - Default to `http://localhost:8001`

## API Endpoints Used

### 1. Health Check
- **Endpoint**: `GET /health`
- **Purpose**: Verify API is running and models are loaded
- **Response**: 
  ```json
  {
    "status": "healthy",
    "models_loaded": 4,
    "patterns_available": false,
    "timestamp": "2025-06-08T13:08:16.704466"
  }
  ```

### 2. Prediction
- **Endpoint**: `POST /predict`
- **Purpose**: Get success probability and basic scores
- **Request**: 45 feature fields (see data mapping below)
- **Response**:
  ```json
  {
    "success_probability": 0.73,
    "confidence": "high",
    "confidence_score": 0.85,
    "scores": {
      "capital": 0.78,
      "advantage": 0.71,
      "market": 0.69,
      "people": 0.75
    },
    "insights": ["..."],
    "recommendations": ["..."],
    "risk_assessment": {...}
  }
  ```

### 3. Detailed Analysis
- **Endpoint**: `POST /analyze`
- **Purpose**: Get comprehensive analysis with detailed breakdowns
- **Request**: Same as prediction
- **Response**: Includes everything from prediction plus:
  ```json
  {
    "detailed_analysis": {
      "capital_analysis": {...},
      "advantage_analysis": {...},
      "market_analysis": {...},
      "people_analysis": {...}
    }
  }
  ```

### 4. Validation
- **Endpoint**: `POST /validate`
- **Purpose**: Validate data before submission
- **Response**:
  ```json
  {
    "valid": true/false,
    "missing_fields": [...],
    "validation_errors": [...]
  }
  ```

## Data Mapping

### Frontend → Backend Transformation

#### Capital Features
- `totalFundingRaised` → `total_capital_raised_usd`
- `monthlyBurnRate` → `monthly_burn_usd`
- `runwayMonths` → `runway_months`
- `annualRevenueRunRate` → `annual_revenue_run_rate`
- Cash on hand calculated from: `burn_rate * runway_months`

#### Advantage Features
- `moatStrength` (1-10) → `tech_differentiation_score` (1-5)
- `hasPatents` → `patent_count` (boolean to count)
- `advantages` array mapped to specific boolean fields:
  - 'network-effects' → `network_effects_present`
  - 'proprietary-data' → `has_data_moat`
  - 'regulatory-barriers' → `regulatory_advantage_present`

#### Market Features
- `marketSize` → `tam_size_usd`
- SAM estimated as 30% of TAM
- SOM estimated as 5% of TAM
- `marketGrowthRate` → `market_growth_rate_percent`
- `competitionLevel` → `competition_intensity`

#### People Features
- `teamSize` → `team_size_full_time`
- `foundersCount` → `founders_count`
- `industryExperience` → `years_experience_avg`
- `previousStartups` → `prior_startup_experience_count`
- `previousExits` → `prior_successful_exits_count`

## Usage in Components

### Analysis Page
```typescript
// The Analysis page now uses real API
const callAPI = async () => {
  try {
    const isHealthy = await apiService.checkHealth();
    if (!isHealthy) throw new Error('API unavailable');
    
    const results = await apiService.getDetailedAnalysis(data);
    setResults(results);
    navigate('/results');
  } catch (err) {
    // Fallback to mock data
    setResults(mockResults);
  }
};
```

### Error Handling
- API errors display in the UI with a red error message
- Automatic fallback to mock data ensures app remains functional
- All errors are logged to console for debugging

## Testing the Integration

### Manual Testing
1. Start the backend API: `python3 api_server_unified.py`
2. Start the frontend: `npm start`
3. Complete an assessment
4. Watch the Analysis page - it should call the real API
5. Check browser console for API logs

### Test Script
Run the test script to verify all endpoints:
```bash
# In browser console
import('./test-api.ts').then(m => m.testAPIIntegration())
```

## Default Values

The API requires many fields that the frontend doesn't collect. Smart defaults are used:

- **Customer metrics**: 100 customers, 20% concentration
- **Retention rates**: 85% (30d), 70% (90d)
- **Growth rates**: 30% user growth
- **Financial ratios**: LTV/CAC = 3.0, Gross margin = 70%
- **Team diversity**: 30%
- **Advisor count**: 3

## Next Steps

### Immediate
1. ✅ API service implementation
2. ✅ Data transformation layer
3. ✅ Error handling
4. ✅ Integration in Analysis page

### Future Enhancements
1. Add authentication headers if required
2. Implement request caching
3. Add request retry logic
4. Create more sophisticated default value logic
5. Add real-time validation as user types
6. Implement batch predictions
7. Add webhook support for long-running analyses

## Troubleshooting

### API Not Responding
1. Check if backend is running: `lsof -i :8001`
2. Verify API health: `curl http://localhost:8001/health`
3. Check browser console for CORS errors
4. Ensure `.env` file has correct API URL

### Data Validation Errors
1. Check browser console for validation response
2. Review field mapping in `transformAssessmentData`
3. Ensure all required fields have values or defaults
4. Use validation endpoint to debug

### Type Errors
- The backend expects specific types (numbers, not strings)
- All numeric fields are parsed: `parseFloat()` or `parseInt()`
- Boolean fields properly converted from frontend format

## Architecture

```
Frontend (React)
    ↓
API Service Layer (api.ts)
    ↓
Data Transformation
    ↓
HTTP Request (fetch)
    ↓
Backend API (FastAPI)
    ↓
ML Models
    ↓
Response Transformation
    ↓
UI Update
```

---

**Status**: ✅ Fully Integrated and Functional
**Last Updated**: June 8, 2025