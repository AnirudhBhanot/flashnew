# Michelin Analysis Timeout Increase Summary

## Changes Made

### 1. Increased Timeouts in Hybrid Engine (`api_michelin_hybrid.py`)
- **DeepSeek availability test**: 5s → 10s
- **Full analysis timeout**: 60s → 120s (2 minutes)
- **Quick check timeout**: 15s → 30s

### 2. Optimized Prompts in LLM Analysis (`api_michelin_llm_analysis.py`)
- Made prompts more concise to reduce response size
- Changed from "comprehensive" to "CONCISE" analysis
- Reduced requirements:
  - BCG Matrix: From 2-3 paragraphs to 1-2 sentences
  - Porter's Five Forces: Simplified to High/Medium/Low ratings with 1 sentence
  - SWOT: Reduced from 3-4 points to 2-3 points each
  - Executive Summary: From 3 paragraphs to 2 paragraphs (max 150 words)

### 3. Improved JSON Handling
- Better truncation detection and repair
- Enhanced error recovery for partial JSON responses
- Added fallback structures when JSON parsing fails

## Expected Improvements

1. **Longer Wait Time**: System will now wait up to 2 minutes for DeepSeek responses
2. **Smaller Responses**: Concise prompts should result in smaller, complete JSON responses
3. **Better Success Rate**: Combination of longer timeout and smaller responses should improve reliability

## Testing

Test the updated endpoint with:
```bash
curl -X POST http://localhost:8001/api/michelin/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "startup_data": {
      "startup_name": "TechVenture AI",
      "sector": "artificial-intelligence",
      "funding_stage": "seed",
      "total_capital_raised_usd": 2000000,
      "cash_on_hand_usd": 1500000,
      "monthly_burn_usd": 75000,
      "runway_months": 20,
      "market_size_usd": 50000000000,
      "market_growth_rate_annual": 45,
      "competitor_count": 50,
      "market_share_percentage": 0.01,
      "team_size_full_time": 12,
      "customer_acquisition_cost_usd": 500,
      "lifetime_value_usd": 5000,
      "monthly_active_users": 1000,
      "product_stage": "beta",
      "proprietary_tech": true,
      "patents_filed": 3,
      "founders_industry_experience_years": 15,
      "b2b_or_b2c": "b2b",
      "burn_rate_usd": 75000,
      "investor_tier_primary": "tier_1",
      "annual_revenue_usd": 500000,
      "revenue_growth_rate": 150,
      "gross_margin": 80
    }
  }'
```

The system should now:
1. Wait longer for DeepSeek to respond (up to 2 minutes)
2. Generate more concise responses that fit within token limits
3. Successfully parse and return complete analysis