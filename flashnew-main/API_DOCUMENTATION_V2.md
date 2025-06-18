# FLASH Platform API Documentation V2
## Complete ML Infrastructure Edition

### Version: 2.0.0
### Last Updated: June 4, 2025
### API Base URL: `http://localhost:8000`

---

## Table of Contents

1. [Overview](#overview)
2. [Authentication](#authentication)
3. [Core Prediction API](#core-prediction-api)
4. [Model Management API](#model-management-api)
5. [Monitoring API](#monitoring-api)
6. [Experimentation API](#experimentation-api)
7. [Data Models](#data-models)
8. [Error Handling](#error-handling)
9. [Rate Limiting](#rate-limiting)
10. [Examples](#examples)

---

## Overview

The FLASH ML Platform API provides enterprise-grade startup evaluation with:
- **Unified ML Orchestration**: 73 models working in harmony
- **Pattern Recognition**: 50+ startup patterns
- **Real-time Monitoring**: Performance tracking and alerts
- **A/B Testing**: Built-in experimentation framework
- **Model Versioning**: Blue-green deployment support

### Key Features
- 81%+ prediction accuracy
- <100ms response time (p50)
- 100+ requests per second capacity
- Complete model lifecycle management
- Real-time performance monitoring

---

## Authentication

The API supports two authentication methods:

### JWT Bearer Token
```http
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
```

### API Key
```http
X-API-Key: your-api-key-here
```

### Obtaining Credentials
```http
POST /auth/login
Content-Type: application/json

{
  "username": "user@example.com",
  "password": "secure-password"
}

Response:
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer",
  "expires_in": 1800
}
```

---

## Core Prediction API

### POST /predict
Generate comprehensive startup success prediction using all ML systems.

**Request:**
```http
POST /predict
Authorization: Bearer {token}
Content-Type: application/json

{
  "startup_name": "AI Innovation Inc",
  "funding_stage": "seed",
  "total_capital_raised_usd": 2000000,
  "team_size_full_time": 15,
  "annual_revenue_run_rate": 1500000,
  "revenue_growth_rate_percent": 250,
  "gross_margin_percent": 70,
  "ltv_cac_ratio": 3.5,
  "monthly_burn_usd": 150000,
  "cash_on_hand_usd": 1800000,
  "runway_months": 12,
  "customer_count": 150,
  "churn_rate_monthly_percent": 3,
  "dau_mau_ratio": 0.65,
  "investor_tier_primary": "tier_2",
  "founder_domain_expertise_yrs": 8,
  "prior_successful_exits": 1,
  "team_diversity_score": 8,
  "market_tam_usd": 50000000000,
  "market_growth_rate_percent": 35,
  "competition_intensity_score": 6,
  "product_stage": "scaling",
  "network_effects_score": 7,
  "has_debt": false,
  "has_revenue": true,
  "is_saas": true,
  "is_b2b": true,
  // ... additional features
}
```

**Response:**
```json
{
  "prediction": 0.823,
  "confidence": 0.91,
  "verdict": "STRONG_INVEST",
  "success_probability": 0.823,
  "risk_score": 0.177,
  "investment_recommendation": "Strong investment opportunity. High success probability with solid fundamentals.",
  
  "metadata": {
    "model_version": "unified_complete_v1",
    "prediction_timestamp": "2025-06-04T23:15:30.123Z",
    "latency_ms": 94.3,
    "models_used": ["production", "camp", "patterns", "stage", "industry"],
    "integrity_verified": true,
    "monitoring_active": true,
    "total_models_used": 73
  },
  
  "explanations": {
    "component_predictions": {
      "production": {
        "dna_analyzer": 0.78,
        "temporal": 0.82,
        "industry": 0.80,
        "ensemble": 0.79
      },
      "camp": {
        "capital": 0.81,
        "advantage": 0.88,
        "market": 0.84,
        "people": 0.79
      },
      "patterns": 0.87,
      "stage": 0.83,
      "industry_specific": 0.85
    },
    
    "patterns_detected": [
      "AI_ML_CORE",
      "B2B_ENTERPRISE", 
      "PLG_EFFICIENT",
      "VC_HYPERGROWTH"
    ],
    
    "camp_scores": {
      "capital": 0.81,
      "advantage": 0.88,
      "market": 0.84,
      "people": 0.79
    },
    
    "key_factors": [
      "Strong pattern match with successful AI/ML startups",
      "Exceptional advantage score indicating strong moat",
      "High market score with large TAM",
      "Efficient growth metrics (LTV/CAC > 3)",
      "Experienced team with prior exits"
    ]
  }
}
```

### POST /predict/batch
Process multiple startups in a single request (async).

**Request:**
```json
{
  "startups": [
    { /* startup 1 data */ },
    { /* startup 2 data */ },
    // ... up to 100 startups
  ]
}
```

**Response:**
```json
{
  "task_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "processing",
  "batch_size": 2,
  "estimated_completion": "2025-06-04T23:16:00Z"
}
```

---

## Model Management API

### GET /models/info
Get comprehensive information about loaded models.

**Response:**
```json
{
  "orchestrator_version": "complete_v1",
  "total_models": 73,
  "model_types": ["production", "camp", "patterns", "stage", "industry"],
  "configuration": {
    "adaptive_weighting": true,
    "confidence_threshold": 0.65,
    "enable_monitoring": true,
    "enable_integrity_check": true
  },
  "production_info": {
    "models": ["dna_analyzer", "temporal", "industry", "ensemble"],
    "average_auc": 0.727
  },
  "pattern_info": {
    "total_patterns": 50,
    "patterns": ["AI_ML_CORE", "B2B_ENTERPRISE", "..."],
    "average_auc": 0.87
  }
}
```

### GET /models/integrity
Check model integrity and security status.

**Response:**
```json
{
  "report_generated": "2025-06-04T23:15:00Z",
  "system_status": "healthy",
  "current_state": {
    "total_models": 133,
    "valid_models": 133,
    "invalid_models": 0,
    "missing_models": 0
  },
  "recent_failures": 0,
  "recommendations": []
}
```

### GET /models/versions
List model versions with filtering options.

**Query Parameters:**
- `model_type` (optional): Filter by model type
- `status` (optional): Filter by status (staging/production/archived)

**Response:**
```json
[
  {
    "version_id": "ensemble_v20250604_224800",
    "model_type": "ensemble",
    "created_at": "2025-06-04T22:48:00Z",
    "status": "production",
    "performance": {
      "accuracy": 0.727,
      "auc": 0.727,
      "precision": 0.70,
      "recall": 0.68
    }
  }
]
```

### POST /models/deploy
Deploy a new model version with specified strategy.

**Request:**
```json
{
  "model_path": "models/new_ensemble.pkl",
  "model_type": "ensemble",
  "performance_metrics": {
    "accuracy": 0.82,
    "auc": 0.83,
    "precision": 0.80,
    "recall": 0.78
  },
  "deployment_strategy": "blue_green"
}
```

**Response:**
```json
{
  "status": "deployed",
  "version": "ensemble_v20250604_231600",
  "model_type": "ensemble",
  "deployment_strategy": "blue_green",
  "rollback_version": "ensemble_v20250604_224800"
}
```

---

## Monitoring API

### GET /monitoring/performance
Get real-time performance metrics.

**Query Parameters:**
- `hours` (default: 24): Time window for metrics
- `model_type` (optional): Filter by model type

**Response:**
```json
{
  "unified_orchestrator_complete_v1": {
    "total_predictions": 1523,
    "avg_prediction": 0.712,
    "avg_confidence": 0.78,
    "avg_latency_ms": 95.3,
    "p95_latency_ms": 142.7,
    "accuracy": 0.815,
    "feedback_rate": 0.23
  }
}
```

### GET /monitoring/alerts
Get active system alerts.

**Response:**
```json
[
  {
    "alert_id": "alert_20250604_231000_1",
    "alert_type": "latency",
    "severity": "warning",
    "model_type": "orchestrator",
    "model_version": "complete_v1",
    "metric_name": "latency_ms",
    "current_value": 125.3,
    "threshold": 100,
    "timestamp": "2025-06-04T23:10:00Z",
    "resolved": false
  }
]
```

### POST /monitoring/alerts/{alert_id}/resolve
Resolve an active alert.

**Response:**
```json
{
  "alert_id": "alert_20250604_231000_1",
  "resolved": true,
  "resolution_timestamp": "2025-06-04T23:15:30Z"
}
```

### GET /monitoring/report
Get comprehensive performance report.

**Response:**
```json
{
  "generated_at": "2025-06-04T23:20:00Z",
  "monitoring_period_hours": 168,
  "summary": {
    /* Performance summary data */
  },
  "active_alerts": [],
  "experiments": {
    "active": 2,
    "completed": 5,
    "results": { /* Experiment results */ }
  },
  "system_health": {
    "score": 95,
    "status": "healthy",
    "factors": {
      "critical_alerts": 0,
      "high_alerts": 0,
      "total_alerts": 1
    }
  }
}
```

---

## Experimentation API

### POST /experiments/create
Create a new A/B test experiment.

**Request:**
```json
{
  "experiment_name": "pattern_weight_optimization",
  "model_a": "weights_v1",
  "model_b": "weights_v2",
  "traffic_split": 0.5,
  "min_samples": 1000
}
```

**Response:**
```json
{
  "status": "created",
  "experiment": "pattern_weight_optimization",
  "started_at": "2025-06-04T23:25:00Z"
}
```

### GET /experiments/results
Get experiment results.

**Query Parameters:**
- `experiment_name` (optional): Specific experiment

**Response:**
```json
{
  "pattern_weight_optimization": {
    "name": "pattern_weight_optimization",
    "model_a": "weights_v1",
    "model_b": "weights_v2",
    "status": "completed",
    "started_at": "2025-06-04T20:00:00Z",
    "completed_at": "2025-06-04T23:00:00Z",
    "winner": "model_b",
    "results": {
      "mean_a": 0.803,
      "mean_b": 0.821,
      "t_statistic": 2.45,
      "p_value": 0.014,
      "effect_size": 0.18,
      "relative_improvement": 0.0224
    }
  }
}
```

### POST /feedback
Submit actual outcome for prediction improvement.

**Request:**
```json
{
  "features_hash": "a1b2c3d4e5f6",
  "actual_outcome": 1.0
}
```

**Response:**
```json
{
  "status": "recorded",
  "features_hash": "a1b2c3d4e5f6",
  "feedback_timestamp": "2025-06-04T23:30:00Z"
}
```

---

## Data Models

### StartupData
Complete startup information model:

```python
{
  # Company Basics
  "startup_name": str,
  "founding_date": str,  # YYYY-MM-DD
  "funding_stage": str,  # pre_seed, seed, series_a, series_b, series_c_plus
  
  # Financial Metrics
  "total_capital_raised_usd": float,
  "cash_on_hand_usd": float,
  "monthly_burn_usd": float,
  "runway_months": float,
  "annual_revenue_run_rate": float,
  "revenue_growth_rate_percent": float,
  "gross_margin_percent": float,
  
  # Unit Economics
  "ltv_cac_ratio": float,
  "cac_usd": float,
  "payback_period_months": float,
  
  # Team Metrics
  "team_size_full_time": int,
  "team_diversity_score": int,  # 1-10
  "founder_domain_expertise_yrs": float,
  "prior_successful_exits": int,
  
  # Market Metrics
  "market_tam_usd": float,
  "market_sam_usd": float,
  "market_som_usd": float,
  "market_growth_rate_percent": float,
  "competition_intensity_score": int,  # 1-10
  
  # Product Metrics
  "product_stage": str,  # idea, mvp, beta, launched, scaling
  "customer_count": int,
  "churn_rate_monthly_percent": float,
  "nps_score": int,
  "dau_mau_ratio": float,
  "network_effects_score": int,  # 1-10
  
  # Boolean Flags
  "has_debt": bool,
  "has_revenue": bool,
  "is_saas": bool,
  "is_b2b": bool,
  "is_profitable": bool
}
```

---

## Error Handling

### Error Response Format
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input data",
    "details": {
      "field": "revenue_growth_rate_percent",
      "issue": "Value must be between -100 and 1000"
    }
  },
  "request_id": "req_550e8400",
  "timestamp": "2025-06-04T23:35:00Z"
}
```

### Common Error Codes
| Code | HTTP Status | Description |
|------|-------------|-------------|
| `VALIDATION_ERROR` | 400 | Invalid input data |
| `AUTHENTICATION_FAILED` | 401 | Invalid credentials |
| `RATE_LIMIT_EXCEEDED` | 429 | Too many requests |
| `MODEL_NOT_FOUND` | 404 | Requested model not found |
| `INTERNAL_ERROR` | 500 | Server error |
| `SERVICE_UNAVAILABLE` | 503 | ML system not ready |

---

## Rate Limiting

### Default Limits
- **Predictions**: 10 requests/minute per IP
- **Batch**: 1 request/minute per IP
- **Model Management**: 5 requests/minute per user
- **Monitoring**: 30 requests/minute per user

### Rate Limit Headers
```http
X-RateLimit-Limit: 10
X-RateLimit-Remaining: 7
X-RateLimit-Reset: 1622547900
```

---

## Examples

### Python Example
```python
import requests

# Setup
API_KEY = "your-api-key"
BASE_URL = "http://localhost:8000"

# Make prediction
headers = {"X-API-Key": API_KEY}
startup_data = {
    "startup_name": "TechCo",
    "funding_stage": "seed",
    "team_size_full_time": 10,
    "annual_revenue_run_rate": 1200000,
    # ... other fields
}

response = requests.post(
    f"{BASE_URL}/predict",
    json=startup_data,
    headers=headers
)

if response.status_code == 200:
    result = response.json()
    print(f"Success Probability: {result['prediction']:.1%}")
    print(f"Patterns: {', '.join(result['explanations']['patterns_detected'])}")
else:
    print(f"Error: {response.json()['error']['message']}")
```

### cURL Example
```bash
curl -X POST http://localhost:8000/predict \
  -H "X-API-Key: your-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "startup_name": "TechCo",
    "funding_stage": "seed",
    "team_size_full_time": 10,
    "annual_revenue_run_rate": 1200000
  }'
```

### JavaScript/TypeScript Example
```typescript
interface PredictionResponse {
  prediction: number;
  confidence: number;
  verdict: string;
  explanations: {
    patterns_detected: string[];
    camp_scores: Record<string, number>;
  };
}

async function predictStartupSuccess(startupData: any): Promise<PredictionResponse> {
  const response = await fetch('http://localhost:8000/predict', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-API-Key': 'your-api-key'
    },
    body: JSON.stringify(startupData)
  });
  
  if (!response.ok) {
    throw new Error(`API Error: ${response.statusText}`);
  }
  
  return response.json();
}
```

---

## Best Practices

1. **Always include all required fields** - Missing fields will result in validation errors
2. **Use appropriate data types** - Numbers should be floats/ints, not strings
3. **Handle rate limits gracefully** - Implement exponential backoff
4. **Monitor your usage** - Track API calls and performance metrics
5. **Cache predictions** - Same inputs will return same results
6. **Validate inputs client-side** - Reduce unnecessary API calls
7. **Use batch endpoints** - For processing multiple startups
8. **Submit feedback** - Help improve model accuracy

---

**Version**: 2.0.0  
**Last Updated**: June 4, 2025  
**Status**: Production Ready with ML Infrastructure ✅