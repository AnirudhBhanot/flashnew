# Frontend LLM Integration Testing Guide

## Current Status (June 7, 2025)

### ✅ Backend Status
- API Server: Running on port 8001
- LLM Status: Operational (DeepSeek API)
- Response Time: ~15-20 seconds for AI features
- CORS: Properly configured for localhost:3000

### ✅ Recent Tests
1. **API Health Check**: `/api/analysis/status` returns operational
2. **Prediction Endpoint**: `/predict` working (52% probability for test data)
3. **LLM Recommendations**: Successfully generated personalized recommendations
4. **What-If Analysis**: Endpoint ready at `/api/analysis/whatif/dynamic`

## Testing Steps

### 1. Open Browser Console
```javascript
// In Chrome DevTools Console at http://localhost:3000
// Check for any CORS errors or failed requests
```

### 2. Test LLM Status from Frontend
```javascript
// Run this in browser console
fetch('http://localhost:8001/api/analysis/status')
  .then(r => r.json())
  .then(data => console.log('LLM Status:', data))
  .catch(err => console.error('Error:', err));

// Expected: {status: "operational", model: "deepseek-chat", ...}
```

### 3. Complete Analysis Flow
1. Navigate to http://localhost:3000
2. Click "Start Analysis"
3. Fill in data:
   - Funding Stage: Series A
   - Sector: SaaS
   - Team Size: 25
   - Revenue: $3M ARR
   - Growth Rate: 150%
   - Monthly Burn: $250k
4. Complete all sections
5. Submit analysis

### 4. Verify AI Features

#### A. In Recommendations Tab
- Look for "✨ AI-Powered Recommendations" badge
- Should see 3-5 specific recommendations
- Each with: Title, Why, How, Timeline, Impact

#### B. In CAMP Tab
1. Expand any pillar (e.g., People - currently lowest at 27%)
2. Select 2-3 improvements
3. Click "Get AI Analysis"
4. Should see:
   - AI Prediction percentage
   - Confidence interval
   - Timeline for improvements

### 5. Monitor Network Tab
- Filter by: `api/analysis`
- Should see:
  - `GET /api/analysis/status` (checking availability)
  - `POST /api/analysis/recommendations/dynamic` (after analysis)
  - `POST /api/analysis/whatif/dynamic` (when using What-If)

## Expected Results

### Success Indicators
1. **AI Badges**: ✨ icon appears on recommendations
2. **Loading States**: "Generating personalized recommendations..." spinner
3. **Response Time**: 15-20 seconds for AI features
4. **Content Quality**: Specific, contextual recommendations (not generic)

### Current Test Data Response
```json
{
  "recommendations": [
    {
      "title": "Hire experienced executives to strengthen leadership",
      "why": "Low People score indicates weak team composition...",
      "timeline": "3 months",
      "impact": "Increase People score to 60%+"
    }
  ]
}
```

## Troubleshooting

### If No AI Features Show
1. Check console for errors
2. Verify API is running: `lsof -i :8001`
3. Check `.env` file has DeepSeek key
4. Look at API logs: `tail -f api_server.log`

### Common Issues
- **CORS Error**: Already fixed with wildcard origins
- **Timeout**: Normal for AI features (15-20s)
- **Empty Recommendations**: Check if LLM status is operational

## Quick API Test Commands

```bash
# Test LLM Status
curl http://localhost:8001/api/analysis/status | jq

# Test Recommendations
curl -X POST http://localhost:8001/api/analysis/recommendations/dynamic \
  -H "Content-Type: application/json" \
  -d '{
    "startup_data": {"funding_stage": "series_a", "sector": "saas"},
    "scores": {"capital": 0.55, "advantage": 0.44, "market": 0.63, "people": 0.27},
    "verdict": "CONDITIONAL PASS"
  }' | jq

# Test What-If Analysis
curl -X POST http://localhost:8001/api/analysis/whatif/dynamic \
  -H "Content-Type: application/json" \
  -d '{
    "startup_data": {"funding_stage": "series_a"},
    "current_scores": {"capital": 0.55, "people": 0.27},
    "improvements": [
      {"id": "hire_vp", "description": "Hire VP Sales/Engineering"}
    ]
  }' | jq
```

## Current Configuration
- Frontend: http://localhost:3000
- API: http://localhost:8001
- LLM: DeepSeek API (operational)
- Redis: Not running (caching disabled)
- Models: production_v45_fixed (72.7% AUC)

---

Last tested: June 7, 2025, 7:19 AM
Status: Backend fully operational, frontend integration ready for testing