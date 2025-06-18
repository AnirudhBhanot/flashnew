# LLM Integration Quick Start Guide

## 1. Backend Setup

### Install Dependencies
```bash
pip install -r requirements_llm.txt
```

### Set Environment Variables
```bash
# Add to your .env file
export DEEPSEEK_API_KEY="sk-f68b7148243e4663a31386a5ea6093cf"
export REDIS_URL="redis://localhost:6379"  # Optional
export LLM_CACHE_TTL=3600  # 1 hour
```

### Update API Server
Add these lines to `api_server_unified.py`:

```python
# Import LLM endpoints
from api_llm_endpoints import llm_router, shutdown_llm_engine

# Add router to app
app.include_router(llm_router)

# Add shutdown handler
@app.on_event("shutdown")
async def shutdown():
    await shutdown_llm_engine()
```

### Test the Integration
```bash
# Start the API server
python api_server_unified.py

# Test LLM status
curl http://localhost:8001/api/analysis/status

# Test recommendations
curl -X POST http://localhost:8001/api/analysis/recommendations/dynamic \
  -H "Content-Type: application/json" \
  -d '{
    "startup_data": {
      "funding_stage": "Series A",
      "sector": "SaaS",
      "annual_revenue_run_rate": 2000000
    },
    "scores": {
      "capital": 0.6,
      "advantage": 0.7,
      "market": 0.8,
      "people": 0.65,
      "success_probability": 0.7
    }
  }'
```

## 2. Frontend Setup

### Install the LLM Service
The `llmService.ts` file is already created. Import it where needed:

```typescript
import { llmService } from '../services/llmService';
```

### Update AnalysisResults Component

#### Step 1: Add State
```typescript
const [llmRecommendations, setLlmRecommendations] = useState(null);
const [isLoadingLLM, setIsLoadingLLM] = useState(false);
const [llmAvailable, setLlmAvailable] = useState(false);
```

#### Step 2: Check Availability
```typescript
useEffect(() => {
  llmService.isAvailable().then(setLlmAvailable);
}, []);
```

#### Step 3: Fetch Dynamic Content
```typescript
useEffect(() => {
  if (data && llmAvailable) {
    fetchLLMRecommendations();
  }
}, [data, llmAvailable]);
```

#### Step 4: Update UI
Add AI badges and loading states as shown in the integration example.

## 3. Testing the Integration

### Backend Tests
```python
# test_llm_integration.py
import asyncio
from llm_analysis import LLMAnalysisEngine

async def test_recommendations():
    engine = LLMAnalysisEngine()
    
    result = await engine.get_recommendations(
        {"funding_stage": "Seed", "sector": "SaaS"},
        {"capital": 0.6, "advantage": 0.7, "market": 0.8, "people": 0.65, "success_probability": 0.7}
    )
    
    print("Recommendations:", result)
    await engine.close()

asyncio.run(test_recommendations())
```

### Frontend Tests
Open the browser console and run:
```javascript
// Test LLM service
const status = await llmService.checkStatus();
console.log('LLM Status:', status);

// Test recommendations
const recs = await llmService.getRecommendations(
  {funding_stage: 'Seed', sector: 'SaaS'},
  {capital: 0.6, advantage: 0.7, market: 0.8, people: 0.65, success_probability: 0.7}
);
console.log('Recommendations:', recs);
```

## 4. Gradual Rollout

### Phase 1: Shadow Mode (Week 1)
- Enable LLM calls but don't show to users
- Log and compare with static recommendations
- Monitor performance and accuracy

### Phase 2: Beta Users (Week 2)
- Enable for 10% of users
- Add feature flag: `REACT_APP_LLM_ENABLED=true`
- Collect feedback

### Phase 3: Full Rollout (Week 3)
- Enable for all users
- Keep fallback mechanism active
- Monitor costs and usage

## 5. Monitoring

### Add Logging
```python
# In api_llm_endpoints.py
logger.info(f"LLM call: {analysis_type} for {sector} {stage}")
logger.info(f"Response time: {response_time}ms")
logger.info(f"Cache hit: {cache_hit}")
```

### Track Metrics
- API response times
- Cache hit rates
- Fallback rates
- Token usage
- Cost per analysis

### Set Up Alerts
- Response time > 5 seconds
- Error rate > 5%
- Daily cost > $X

## 6. Cost Optimization

### Caching Strategy
- Cache recommendations for 1 hour
- Cache market insights for 24 hours
- Use Redis for distributed caching

### Token Optimization
- Limit prompts to essential information
- Use structured outputs (JSON)
- Set max_tokens appropriately

### Rate Limiting
- Implement per-user rate limits
- Queue requests during peak times
- Use circuit breakers for failures

## 7. Troubleshooting

### Common Issues

#### "LLM unavailable, using fallback"
- Check API key is correct
- Verify network connectivity
- Check DeepSeek API status

#### Slow Response Times
- Check Redis connection
- Reduce prompt complexity
- Enable response streaming

#### Inconsistent Results
- Review prompt templates
- Add validation for LLM outputs
- Increase temperature for variety

## 8. Next Steps

1. **Enhance Prompts**: Continuously improve prompt engineering based on results
2. **Add More Features**: Competitor analysis, market reports, etc.
3. **Fine-tuning**: Consider fine-tuning models on your specific data
4. **A/B Testing**: Compare LLM vs static recommendations
5. **User Feedback**: Add thumbs up/down for recommendations

## Security Notes

- Never commit API keys to git
- Sanitize all user inputs
- Implement rate limiting
- Monitor for prompt injection
- Regular security audits

## Support

For issues or questions:
- Check logs in `api_server.log`
- Review LLM responses in Redis cache
- Contact DeepSeek support for API issues