# FLASH Platform API Documentation

## Overview

The FLASH (Fast Learning and Assessment of Startup Health) platform provides advanced AI-powered startup evaluation using multiple specialized models. This documentation covers all modules, APIs, and integration points.

## Table of Contents

1. [API Endpoints](#api-endpoints)
2. [Module Documentation](#module-documentation)
3. [Data Models](#data-models)
4. [Integration Guide](#integration-guide)
5. [Error Handling](#error-handling)
6. [Examples](#examples)

---

## API Endpoints

### Base URL
```
http://localhost:8000
```

### Authentication
Currently, the API uses rate limiting (100 requests/hour per IP) but no authentication.

### Main Endpoints

#### 1. **POST /predict**
Predict startup success probability.

**Request Body:**
```json
{
  "funding_stage": "series_a",
  "total_capital_raised_usd": 5000000,
  "cash_on_hand_usd": 3000000,
  "monthly_burn_usd": 150000,
  "annual_revenue_run_rate": 1200000,
  "revenue_growth_rate_percent": 150,
  "gross_margin_percent": 65,
  "ltv_cac_ratio": 3.0,
  "investor_tier_primary": "tier_2",
  "has_debt": false,
  // ... (see StartupMetrics model for all fields)
}
```

**Response:**
```json
{
  "success_probability": 0.7235,
  "confidence_interval": {
    "lower": 0.6825,
    "upper": 0.7645
  },
  "pillar_scores": {
    "capital": 0.82,
    "advantage": 0.71,
    "market": 0.68,
    "people": 0.69
  },
  "insights": {
    "strengths": ["Strong revenue growth", "Good LTV/CAC ratio"],
    "weaknesses": ["High burn rate relative to revenue"],
    "recommendations": ["Focus on improving unit economics"]
  }
}
```

#### 2. **GET /health**
Check API health status.

**Response:**
```json
{
  "status": "healthy",
  "models_loaded": {
    "v2_ensemble": true,
    "stage_hierarchical": true,
    "dna_analyzer": true,
    "temporal": true,
    "industry_specific": true,
    "unified_orchestrator": true
  },
  "version": "2.0.0"
}
```

#### 3. **GET /model_performance**
Get model performance metrics.

**Response:**
```json
{
  "auc_score": 0.803,
  "accuracy": 0.742,
  "model_agreement": 0.856,
  "last_updated": "2024-12-20T10:30:00Z"
}
```

#### 4. **POST /optimize_weights**
Optimize model weights (requires validation dataset).

**Request Body:**
```json
{
  "validation_file": "data/validation_set.csv"
}
```

---

## Module Documentation

### 1. **StageHierarchicalModel** (`stage_hierarchical_models.py`)

Provides stage-specific predictions based on funding stage.

**Key Methods:**
- `load_models(model_path: str)` - Load stage-specific models
- `predict(X: pd.DataFrame)` - Make predictions with stage-based logic
- `get_stage_insights(stage: str)` - Get stage-specific insights

**Usage:**
```python
from stage_hierarchical_models import StageHierarchicalModel

model = StageHierarchicalModel()
model.load_models('models/stage_hierarchical')
result = model.predict(df)
```

### 2. **StartupDNAAnalyzer** (`dna_pattern_analysis.py`)

Analyzes startup "DNA" patterns for success prediction.

**Key Methods:**
- `analyze_dna(features: pd.DataFrame)` - Analyze startup DNA
- `get_pattern_description(pattern_id: int)` - Get pattern descriptions
- `load(model_path: str)` - Load DNA models

**DNA Components:**
- Growth DNA
- Tech DNA
- Market DNA
- Execution DNA

**Usage:**
```python
from dna_pattern_analysis import StartupDNAAnalyzer

analyzer = StartupDNAAnalyzer()
result = analyzer.analyze_dna(df)
```

### 3. **TemporalPredictionModel** (`temporal_models.py`)

Provides time-based predictions and trajectory analysis.

**Key Methods:**
- `predict_timeline(features: pd.DataFrame)` - Get temporal predictions
- `analyze_trajectory(features: pd.DataFrame)` - Analyze growth trajectory
- `get_survival_curve(features: pd.DataFrame)` - Calculate survival probabilities

**Time Horizons:**
- Short-term (0-6 months)
- Medium-term (6-18 months)
- Long-term (18+ months)

**Usage:**
```python
from temporal_models import TemporalPredictionModel

model = TemporalPredictionModel()
timeline = model.predict_timeline(df)
```

### 4. **IndustrySpecificModel** (`industry_specific_models.py`)

Industry-tailored predictions and benchmarking.

**Key Methods:**
- `predict(features: pd.DataFrame)` - Industry-specific prediction
- `get_industry_benchmarks(industry: str)` - Get industry benchmarks
- `compare_to_peers(features: pd.DataFrame)` - Peer comparison

**Supported Industries:**
- SaaS
- FinTech
- HealthTech
- E-commerce
- EdTech
- BioTech
- Cybersecurity
- Gaming
- Others

**Usage:**
```python
from industry_specific_models import IndustrySpecificModel

model = IndustrySpecificModel()
result = model.predict(df)
```

### 5. **OptimizedModelPipeline** (`model_improvements_fixed.py`)

Enhanced prediction pipeline with calibration and feature engineering.

**Key Methods:**
- `predict(X: pd.DataFrame)` - Make calibrated predictions
- `engineer_features(X: pd.DataFrame)` - Create advanced features
- `get_feature_importance()` - Get feature importance scores

**Enhancements:**
- Probability calibration
- Feature engineering
- Ensemble optimization

**Usage:**
```python
from model_improvements_fixed import OptimizedModelPipeline

pipeline = OptimizedModelPipeline()
predictions = pipeline.predict(df)
```

### 6. **FinalProductionEnsemble** (`final_ensemble_integration.py`)

Production-ready ensemble combining validated models.

**Key Methods:**
- `load_models()` - Load all ensemble models
- `predict(X: pd.DataFrame)` - Make ensemble predictions
- `get_model_weights()` - Get current model weights

**Model Weights:**
- Stage Hierarchical: 40%
- Temporal Hierarchical: 35%
- DNA Pattern: 25%

**Usage:**
```python
from final_ensemble_integration import FinalProductionEnsemble

ensemble = FinalProductionEnsemble()
ensemble.load_models()
result = ensemble.predict(df)
```

### 7. **FLASHExplainer** (`shap_explainer.py`)

Provides SHAP-based explanations for predictions.

**Key Methods:**
- `explain_prediction(features: pd.DataFrame)` - Get full explanation
- `generate_report_data(features: pd.DataFrame)` - Generate report
- `_generate_plots(explanations: Dict)` - Create visualizations

**Outputs:**
- Feature importance
- CAMP category breakdown
- Model consensus analysis
- Actionable insights

**Usage:**
```python
from shap_explainer import FLASHExplainer

explainer = FLASHExplainer()
explanation = explainer.explain_prediction(df)
```

---

## Data Models

### StartupMetrics (Input)

All features required for prediction:

**Capital Features (12):**
- `funding_stage`: Current funding stage (pre_seed|seed|series_a|series_b|series_c|growth)
- `total_capital_raised_usd`: Total capital raised
- `cash_on_hand_usd`: Current cash reserves
- `monthly_burn_usd`: Monthly burn rate
- `runway_months`: Months of runway (auto-calculated if not provided)
- `annual_revenue_run_rate`: ARR
- `revenue_growth_rate_percent`: Revenue growth rate
- `gross_margin_percent`: Gross margin
- `burn_multiple`: Burn multiple (auto-calculated if not provided)
- `ltv_cac_ratio`: LTV/CAC ratio
- `investor_tier_primary`: Primary investor tier (tier_1|tier_2|tier_3|none)
- `has_debt`: Has debt financing

**Advantage Features (11):**
- `patent_count`: Number of patents
- `network_effects_present`: Network effects present
- `has_data_moat`: Has data moat
- `regulatory_advantage_present`: Regulatory advantage
- `tech_differentiation_score`: Tech differentiation (1-5)
- `switching_cost_score`: Switching cost (1-5)
- `brand_strength_score`: Brand strength (1-5)
- `scalability_score`: Scalability (1-5)
- `product_stage`: Product stage (concept|mvp|beta|launch|growth|mature)
- `product_retention_30d`: 30-day retention
- `product_retention_90d`: 90-day retention

**Market Features (12):**
- `sector`: Industry sector
- `tam_size_usd`: Total addressable market
- `sam_size_usd`: Serviceable addressable market
- `som_size_usd`: Serviceable obtainable market
- `market_growth_rate_percent`: Market growth rate
- `customer_count`: Number of customers
- `customer_concentration_percent`: Customer concentration
- `user_growth_rate_percent`: User growth rate
- `net_dollar_retention_percent`: Net dollar retention
- `competition_intensity`: Competition intensity (1-5)
- `competitors_named_count`: Number of competitors
- `dau_mau_ratio`: DAU/MAU ratio

**People Features (10):**
- `founders_count`: Number of founders
- `team_size_full_time`: Full-time team size
- `years_experience_avg`: Average years experience
- `domain_expertise_years_avg`: Domain expertise years
- `prior_startup_experience_count`: Prior startup experience
- `prior_successful_exits_count`: Successful exits
- `board_advisor_experience_score`: Board/advisor score (1-5)
- `advisors_count`: Number of advisors
- `team_diversity_percent`: Team diversity percentage
- `key_person_dependency`: Key person dependency

### PredictionResponse (Output)

```python
{
    "success_probability": float,  # 0-1
    "confidence_interval": {
        "lower": float,
        "upper": float
    },
    "pillar_scores": {
        "capital": float,
        "advantage": float,
        "market": float,
        "people": float
    },
    "insights": {
        "strengths": List[str],
        "weaknesses": List[str],
        "recommendations": List[str]
    },
    "model_consensus": {
        "agreement": float,  # 0-1
        "std_deviation": float
    },
    "explanations": Dict  # Optional SHAP explanations
}
```

---

## Integration Guide

### Python Client Example

```python
import requests
import json

# Prepare data
startup_data = {
    "funding_stage": "series_a",
    "total_capital_raised_usd": 5000000,
    # ... all required fields
}

# Make prediction
response = requests.post(
    "http://localhost:8000/predict",
    json=startup_data
)

result = response.json()
print(f"Success Probability: {result['success_probability']:.2%}")
```

### JavaScript/TypeScript Example

```typescript
const startupData = {
  funding_stage: "series_a",
  total_capital_raised_usd: 5000000,
  // ... all required fields
};

const response = await fetch('http://localhost:8000/predict', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify(startupData),
});

const result = await response.json();
console.log(`Success Probability: ${(result.success_probability * 100).toFixed(1)}%`);
```

---

## Error Handling

### Common Error Codes

- `400 Bad Request`: Invalid input data
- `413 Request Entity Too Large`: Request exceeds 1MB
- `422 Unprocessable Entity`: Validation error
- `429 Too Many Requests`: Rate limit exceeded
- `500 Internal Server Error`: Server error

### Error Response Format

```json
{
  "detail": "Error message",
  "errors": [
    {
      "field": "funding_stage",
      "message": "Invalid value. Must be one of: pre_seed, seed, series_a, series_b, series_c, growth"
    }
  ]
}
```

---

## Examples

### 1. Basic Prediction

```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d @startup_data.json
```

### 2. With Python Requests

```python
import requests
import pandas as pd

# Load data
df = pd.read_csv('startup_data.csv')
startup = df.iloc[0].to_dict()

# Make prediction
response = requests.post(
    'http://localhost:8000/predict',
    json=startup
)

if response.status_code == 200:
    result = response.json()
    print(f"Success: {result['success_probability']:.1%}")
    print(f"Confidence: ±{(result['confidence_interval']['upper'] - result['confidence_interval']['lower'])/2:.1%}")
else:
    print(f"Error: {response.status_code}")
    print(response.json())
```

### 3. Batch Processing

```python
import asyncio
import aiohttp

async def predict_startup(session, startup_data):
    async with session.post('http://localhost:8000/predict', json=startup_data) as response:
        return await response.json()

async def batch_predict(startups):
    async with aiohttp.ClientSession() as session:
        tasks = [predict_startup(session, startup) for startup in startups]
        return await asyncio.gather(*tasks)

# Run batch predictions
startups = [...]  # List of startup data
results = asyncio.run(batch_predict(startups))
```

---

## Performance Considerations

1. **Rate Limiting**: 100 requests/hour per IP
2. **Request Size**: Maximum 1MB per request
3. **Response Time**: ~100-200ms per prediction
4. **Batch Size**: Recommend batches of 10-50 for optimal performance

---

## Deployment

### Docker

```bash
docker build -t flash-api .
docker run -p 8000:8000 flash-api
```

### Production Settings

```bash
python api_server.py --port 8000 --workers 4
```

---

## Support

For issues or questions:
- GitHub Issues: [Create an issue](https://github.com/flash-platform/issues)
- API Status: Check `/health` endpoint
- Logs: Check `logs/api.log`