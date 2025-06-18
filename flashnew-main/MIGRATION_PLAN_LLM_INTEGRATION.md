# LLM Integration Migration Plan for FLASH Platform

## Overview
This document outlines the migration from hardcoded analysis to dynamic LLM-powered insights using DeepSeek API.

## Phase 1: Foundation (Week 1)

### 1.1 Create LLM Integration Module
- [ ] Create `llm_analysis.py` with DeepSeek client
- [ ] Implement structured prompt templates
- [ ] Add response parsing and validation
- [ ] Create fallback mechanisms

### 1.2 Environment Setup
- [ ] Add DeepSeek API key to environment variables
- [ ] Update requirements.txt with necessary packages
- [ ] Create configuration for LLM settings

### 1.3 Initial Testing
- [ ] Test DeepSeek API connectivity
- [ ] Validate response formats
- [ ] Benchmark response times

## Phase 2: Backend Integration (Week 2)

### 2.1 New API Endpoints
Create the following endpoints in `api_server_unified.py`:

#### `/api/analysis/recommendations/dynamic`
- Generate personalized recommendations using LLM
- Input: startup data + CAMP scores
- Output: 3-5 actionable recommendations with timelines

#### `/api/analysis/whatif/dynamic`
- Calculate realistic impact predictions
- Input: startup data + proposed improvements
- Output: probability changes with confidence intervals

#### `/api/analysis/insights/market`
- Provide current market intelligence
- Input: industry + stage + metrics
- Output: market trends, comparisons, opportunities

#### `/api/analysis/competitors`
- Identify and analyze similar companies
- Input: startup profile
- Output: competitor landscape and positioning

### 2.2 Caching Strategy
- Implement Redis caching for LLM responses
- Cache key: hash of input parameters
- TTL: 24 hours for market insights, 1 hour for recommendations

### 2.3 Rate Limiting
- Implement rate limiting for LLM calls
- Default: 100 requests per minute per user
- Configurable via environment variables

## Phase 3: Frontend Migration (Week 3)

### 3.1 Update Components

#### AnalysisResults.tsx
```typescript
// Add new state
const [dynamicRecommendations, setDynamicRecommendations] = useState(null);
const [isLoadingDynamic, setIsLoadingDynamic] = useState(false);

// Add API call
const fetchDynamicRecommendations = async () => {
  try {
    const response = await apiClient.post('/analysis/recommendations/dynamic', {
      startup_data: data.userInput,
      scores: data.camp_scores,
      verdict: data.verdict
    });
    setDynamicRecommendations(response.data);
  } catch (error) {
    // Fallback to hardcoded
    console.warn('Dynamic recommendations failed, using fallback');
  }
};
```

#### What-If Scenarios
- Replace hardcoded impact calculations with API calls
- Show "AI-Powered" badge on dynamic predictions
- Implement smooth loading transitions

### 3.2 UI Enhancements
- Add loading skeletons for LLM content
- Show "AI Generated" badges
- Implement typewriter effect for recommendations
- Add refresh button for updated insights

### 3.3 Fallback Strategy
- Always check for dynamic content first
- Fall back to hardcoded if API fails
- Log fallback occurrences for monitoring

## Phase 4: Testing & Optimization (Week 4)

### 4.1 A/B Testing
- Run both hardcoded and LLM versions
- Compare user engagement metrics
- Measure recommendation quality

### 4.2 Performance Optimization
- Implement streaming responses for long content
- Parallel API calls where possible
- Optimize prompt engineering for speed

### 4.3 Quality Assurance
- Validate LLM outputs against business rules
- Ensure recommendations are actionable
- Check for hallucinations or irrelevant content

## Phase 5: Full Rollout (Week 5)

### 5.1 Gradual Migration
- Start with 10% of users
- Monitor error rates and performance
- Increase to 50%, then 100%

### 5.2 Documentation
- Update API documentation
- Create prompt engineering guide
- Document fallback behaviors

### 5.3 Monitoring
- Set up alerts for API failures
- Track LLM usage and costs
- Monitor response quality metrics

## Technical Implementation Details

### Prompt Templates

#### Recommendations Prompt
```python
recommendation_prompt = """
You are a startup advisor analyzing a {stage} {industry} company.

CAMP Scores:
- Capital: {capital_score}% (Financial health)
- Advantage: {advantage_score}% (Competitive moat)
- Market: {market_score}% (Market opportunity)
- People: {people_score}% (Team strength)

Key Metrics:
- Revenue: ${revenue}
- Growth Rate: {growth_rate}%
- Burn Rate: ${burn_rate}/month
- Runway: {runway_months} months

Overall Success Probability: {success_probability}%

Generate 3-5 specific, actionable recommendations to improve their fundability. 
Each recommendation should include:
1. What to do (specific action)
2. Why it matters (impact on funding)
3. How to do it (concrete steps)
4. Timeline (realistic timeframe)
5. Expected impact (quantified if possible)

Focus on their weakest areas first. Be specific to their industry and stage.
"""

#### What-If Scenario Prompt
```python
whatif_prompt = """
Analyze the impact of these improvements for a {stage} {industry} startup:

Current State:
{current_metrics}

Proposed Improvements:
{improvements}

Based on similar companies and market data, predict:
1. New success probability (with confidence interval)
2. Impact on each CAMP score
3. Timeline to see results
4. Potential risks or trade-offs
5. Most effective improvement to prioritize

Use realistic, data-driven predictions. Avoid over-optimistic estimates.
"""
```

### Error Handling

```python
class LLMAnalysisEngine:
    def __init__(self, api_key: str, fallback_enabled: bool = True):
        self.api_key = api_key
        self.fallback_enabled = fallback_enabled
        self.circuit_breaker = CircuitBreaker(
            failure_threshold=5,
            recovery_timeout=300,
            expected_exception=Exception
        )
    
    async def get_recommendations(self, data: dict) -> dict:
        try:
            # Try LLM first
            with self.circuit_breaker:
                return await self._llm_recommendations(data)
        except Exception as e:
            logger.error(f"LLM failed: {e}")
            if self.fallback_enabled:
                return self._fallback_recommendations(data)
            raise
```

### Cost Management

- **Token Limits**: Max 2000 tokens per request
- **Caching**: Cache common queries for 24 hours
- **Batching**: Batch similar requests when possible
- **Monitoring**: Track usage and costs daily

### Security Considerations

- Store API key in environment variables
- Sanitize all user inputs before sending to LLM
- Implement request signing for API calls
- Rate limit by user and IP
- Log all LLM interactions for audit

## Success Metrics

1. **Quality Metrics**
   - User satisfaction with recommendations (survey)
   - Recommendation relevance score (1-5)
   - Actionability of insights (% implemented)

2. **Performance Metrics**
   - API response time (<3 seconds)
   - Fallback rate (<5%)
   - Cache hit rate (>70%)

3. **Business Metrics**
   - User engagement increase
   - Premium feature adoption
   - Recommendation follow-through rate

## Rollback Plan

If issues arise:
1. Disable LLM endpoints via feature flag
2. Frontend automatically falls back to hardcoded
3. Investigate and fix issues
4. Re-enable with fixes

## Next Steps

1. Review and approve migration plan
2. Set up DeepSeek API account
3. Begin Phase 1 implementation
4. Schedule weekly progress reviews