# FLASH API Documentation - Realistic Models

**Version**: 2.0  
**Base URL**: `http://localhost:8001`  
**Last Updated**: June 6, 2025

## Overview

The FLASH API provides realistic startup success predictions using machine learning models trained on 100,000 companies with real-world characteristics. The API emphasizes honest assessment over false precision.

## Authentication

All endpoints (except `/health`) require API key authentication.

### Headers
```
X-API-Key: your-api-key
Content-Type: application/json
```

### Valid API Keys
- `test-api-key-123` (Development)
- `demo-api-key-456` (Demo)

## Endpoints

### 1. Health Check

```http
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "models_loaded": true,
  "timestamp": "2025-06-06T14:22:26.978240"
}
```

### 2. Make Prediction

```http
POST /predict
```

**Request Body:**
```json
{
  "funding_stage": "pre_seed",
  "sector": "AI/ML",
  "total_capital_raised_usd": 150000,
  "cash_on_hand_usd": 120000,
  "monthly_burn_usd": 15000,
  "runway_months": 8,
  "annual_revenue_run_rate": 0,
  "team_size_full_time": 2,
  "founders_count": 2,
  "years_experience_avg": 5,
  "customer_count": 0,
  "tam_size_usd": 5000000000,
  "market_growth_rate_percent": 40,
  // ... additional fields
}
```

**Response:**
```json
{
  "success_probability": 0.347,
  "confidence_score": 0.5,
  "confidence_interval": {
    "lower": 0.197,
    "upper": 0.497
  },
  "verdict": "PASS",
  "verdict_strength": "medium",
  "risk_level": "Medium Risk",
  "camp_analysis": {
    "capital": 0.45,
    "advantage": 0.45,
    "market": 0.47,
    "people": 0.53
  },
  "risk_factors": [
    "Early-stage prediction is highly uncertain"
  ],
  "success_factors": [
    "Based on limited quantitative signals"
  ],
  "processing_time_ms": 183.96,
  "timestamp": "2025-06-06T14:54:13.201615",
  "model_version": "realistic-v46",
  "investment_recommendation": "PASS"
}
```

### 3. Get Model Features

```http
GET /features
```

**Response:**
```json
{
  "total_features": 85,
  "model_auc": 0.499,
  "key_insights": [
    "Market growth rate most important",
    "Team experience matters",
    "Revenue/customers have low signal for early stage"
  ]
}
```

### 4. Get Configuration

```http
GET /config/{config_type}
```

**Config Types:**
- `success-thresholds`
- `model-performance`
- `all`

**Example Response (`/config/success-thresholds`):**
```json
{
  "pre_seed": 0.10,
  "seed": 0.22,
  "series_a": 0.38,
  "series_b": 0.52,
  "note": "Based on realistic success rates"
}
```

## Field Definitions

### Required Fields

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| funding_stage | string | Current funding stage | "pre_seed", "seed", "series_a" |
| sector | string | Industry sector | "AI/ML", "SaaS", "Fintech" |
| total_capital_raised_usd | float | Total funding raised | 150000 |
| team_size_full_time | int | Number of full-time employees | 2 |
| founders_count | int | Number of founders | 2 |

### Optional Fields

All other fields are optional and will use defaults if not provided.

## Understanding Results

### Success Probability
- **0-10%**: Strong Fail
- **10-16%**: Fail (below average)
- **16-25%**: Conditional Pass
- **25-35%**: Pass
- **35%+**: Strong Pass

Note: 16% is the overall average success rate in the dataset.

### Confidence Score
Always 0.5 (50%) reflecting the inherent uncertainty in early-stage prediction.

### CAMP Analysis
All scores typically range from 45-55% due to limited discriminatory power of quantitative metrics for early-stage companies.

## Model Information

### Current Models
- **DNA Analyzer**: RandomForest, AUC 0.489
- **Temporal Model**: XGBoost, AUC 0.505
- **Industry Model**: XGBoost, AUC 0.504
- **Ensemble Model**: RandomForest, AUC 0.499

### Average Performance
- **AUC**: 0.499 (~50%)
- **TPR**: 18.5%
- **TNR**: 81.8%

### Why 50% AUC?
This reflects the true difficulty of predicting early-stage startup success from quantitative metrics alone. The models are honest about uncertainty rather than overfitting to spurious patterns.

## Rate Limits

Currently no rate limits are enforced, but please be reasonable:
- Development: 100 requests/minute
- Production: Would implement proper rate limiting

## Error Responses

### 401 Unauthorized
```json
{
  "detail": "Invalid or missing API key"
}
```

### 422 Validation Error
```json
{
  "detail": [
    {
      "loc": ["body", "funding_stage"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error message"
}
```

## Migration from V1

### Key Changes
1. **Port**: Now 8001 (was 8000)
2. **Models**: Realistic models with 50% AUC (was 73%+)
3. **Confidence**: Always 0.5 (was artificially high)
4. **CAMP Scores**: 45-55% range (was exactly 50%)

### Backwards Compatibility
The API maintains the same request/response structure for easy migration.

## Example Implementation

### Python
```python
import requests

url = "http://localhost:8001/predict"
headers = {
    "X-API-Key": "test-api-key-123",
    "Content-Type": "application/json"
}

data = {
    "funding_stage": "pre_seed",
    "sector": "AI/ML",
    "total_capital_raised_usd": 150000,
    # ... other fields
}

response = requests.post(url, json=data, headers=headers)
result = response.json()
print(f"Success Probability: {result['success_probability']:.1%}")
```

### JavaScript
```javascript
const response = await fetch('http://localhost:8001/predict', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'X-API-Key': 'test-api-key-123'
  },
  body: JSON.stringify({
    funding_stage: 'pre_seed',
    sector: 'AI/ML',
    total_capital_raised_usd: 150000,
    // ... other fields
  })
});

const result = await response.json();
console.log(`Success Probability: ${(result.success_probability * 100).toFixed(1)}%`);
```

## Best Practices

1. **Understand Limitations**: The 50% AUC reflects real uncertainty
2. **Focus on Relative Scores**: Compare against stage averages
3. **Consider Confidence Intervals**: ±15% range is significant
4. **Use for Screening**: Not definitive prediction
5. **Complement with Qualitative**: Metrics alone aren't sufficient

## Support

For issues or questions:
- GitHub: https://github.com/anthropics/claude-code/issues
- Documentation: This file
- Model Details: See TECHNICAL_DOCUMENTATION_V16.md