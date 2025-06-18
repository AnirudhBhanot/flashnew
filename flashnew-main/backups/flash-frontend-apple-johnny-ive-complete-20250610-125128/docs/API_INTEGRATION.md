# FLASH Frontend-Backend API Integration

## Overview
The FLASH frontend is fully integrated with the backend ML API server running on port 8001. The integration handles data transformation, API calls, and response mapping to ensure seamless communication between the React frontend and Python backend.

## Integration Status ✅
- **API Health Check**: Working
- **Prediction Endpoint**: Working 
- **Validation Endpoint**: Working
- **Data Transformation**: Working
- **Response Mapping**: Working

## Key Components

### 1. API Service (`src/services/api.ts`)
The main service layer that handles all API communication:
- Transforms frontend assessment data to backend format (45 required fields)
- Maps frontend industries/stages to backend enums
- Handles different response formats from the API
- Provides error handling and fallbacks

### 2. Data Transformation
The frontend collects data through the wizard and transforms it into the format expected by the ML models:

```typescript
// Frontend format
{
  companyInfo: { companyName, industry, stage, ... },
  capital: { totalFundingRaised, monthlyBurnRate, ... },
  market: { marketSize, marketGrowthRate, ... },
  people: { foundersCount, teamSize, ... },
  advantage: { patentCount, advantages, ... }
}

// Transformed to backend format (45 fields)
{
  total_capital_raised_usd: number,
  monthly_burn_usd: number,
  sector: string, // mapped from industry
  tam_size_usd: number,
  founders_count: number,
  // ... 40 more fields
}
```

### 3. API Endpoints Used
- `GET /health` - Check API server status
- `POST /predict` - Get success probability and CAMP scores
- `POST /validate` - Validate assessment data

### 4. Response Handling
The API returns different response formats which are normalized:
```javascript
// API Response
{
  success_probability: 0.491,
  camp_scores: { capital: 0.565, ... },
  verdict: "FAIL",
  strength_level: "Weak"
}

// Transformed for frontend
{
  successProbability: 0.491,
  scores: { capital: 0.565, ... },
  confidence: "Weak",
  verdict: "FAIL"
}
```

## Testing the Integration

1. **Ensure backend is running**:
   ```bash
   cd /Users/sf/Desktop/FLASH
   python3 api_server_unified.py
   ```

2. **Run the integration test**:
   ```bash
   cd /Users/sf/Desktop/FLASH/flash-frontend-apple
   node test-api-integration.js
   ```

3. **Test through the UI**:
   - Navigate to http://localhost:3001
   - Complete the assessment wizard
   - On the Analysis page, click "Get AI Analysis"
   - Results will be fetched from the real API

## Configuration

### Environment Variables
Set in `.env`:
```
REACT_APP_API_URL=http://localhost:8001
```

### Fallback Behavior
If the API is unavailable, the frontend falls back to mock data to ensure the UI remains functional during development.

## Troubleshooting

### Common Issues
1. **API not reachable**: Ensure the backend server is running on port 8001
2. **Validation errors**: Check that all required fields are being sent
3. **Sector mismatch**: The frontend industry must map to a valid backend sector

### Debugging
- Check browser console for API errors
- Run the test script to verify integration
- Check backend logs for detailed error messages

## Implementation Details

### Analysis Page Integration
The Analysis page (`src/pages/Analysis/index.tsx`) uses the API service:

```javascript
const callAPI = async () => {
  try {
    const isHealthy = await apiService.checkHealth();
    if (!isHealthy) throw new Error('API service is unavailable');
    
    const results = await apiService.getDetailedAnalysis(data);
    setResults(results);
    navigate('/results');
  } catch (err) {
    console.error('API call failed:', err);
    // Fallback to mock data
  }
};
```

### Current Limitations
1. The `/analyze` endpoint has issues - using `/predict` instead
2. Some fields use default values when not collected by the wizard
3. TypeScript strict mode causes warnings but doesn't affect functionality

## Next Steps
1. Implement remaining endpoints (`/analyze`, `/explain`)
2. Add real-time validation during wizard data entry
3. Implement batch prediction for multiple assessments
4. Add API response caching for better performance