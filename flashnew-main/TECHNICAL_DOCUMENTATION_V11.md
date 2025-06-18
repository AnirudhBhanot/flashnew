# FLASH Technical Documentation V11
*Last Updated: May 31, 2025*

## System Overview

FLASH (Fast Learning and Assessment of Startup Health) is an AI-powered startup evaluation system that predicts success probability using the CAMP framework (Capital, Advantage, Market, People). The system has evolved through 11 major versions, achieving production-ready status with real trained models and sophisticated pattern recognition.

## Architecture Changes V11

### Major Updates from V10:

1. **Model Retraining with Consistent Features**
   - All models retrained with proper feature alignment
   - Fixed feature ordering issues across all model types
   - Improved discrimination power from -1.63% to 55.56%

2. **Enhanced Model Performance**
   - DNA Analyzer: 77.11% AUC
   - Temporal Model: 77.36% AUC
   - Industry Model: 77.17% AUC
   - Ensemble Model: 74.01% AUC
   - Average Performance: ~76.36% AUC

3. **Feature Alignment System**
   - DNA Model: 49 features (45 base + 4 CAMP scores)
   - Temporal Model: 48 features (45 base + 3 temporal features)
   - Industry Model: 45 features (base features only)
   - Ensemble Model: 3 features (model predictions)

4. **Production Model Management**
   - Consistent feature ordering saved with each model
   - Label encoders properly stored and loaded
   - Scalers maintained for proper preprocessing

## Integration Architecture

### API Server (`api_server_final_integrated.py`)
The consolidated API server includes all integration fixes:

```python
# Core endpoints
POST /predict          # Standard prediction with type conversion
POST /predict_simple   # Alias for frontend compatibility  
POST /predict_enhanced # Enhanced prediction with patterns
GET  /investor_profiles # Returns investor templates
GET  /patterns         # List all 31 patterns
GET  /patterns/{name}  # Pattern details
POST /analyze_pattern  # Pattern analysis
GET  /features        # Feature documentation
GET  /system_info     # System configuration
GET  /health          # Health check
```

### Type Conversion System (`type_converter.py`)
Handles all frontend-to-backend data transformations:

```python
# Boolean conversions
frontend: has_debt: true → backend: has_debt: 1
frontend: network_effects_present: false → backend: network_effects_present: 0

# String conversions  
frontend: funding_stage: "Pre-seed" → backend: funding_stage: "pre_seed"
frontend: investor_tier: "Tier 1" → backend: investor_tier: "tier_1"

# Default values for optional fields
runway_months: null → 12
burn_multiple: null → 2.0
```

### Response Transformation
Backend responses are transformed to match frontend expectations:

```python
# Backend format
{
    "success_probability": 0.72,
    "confidence_score": 0.85,
    "pattern_insights": {...}
}

# Transformed to frontend format
{
    "probability": 72,
    "confidence_interval": {"lower": 67, "upper": 77},
    "confidence_score": 85,
    "insights": {...}
}
```

## Machine Learning Models V11

### Model Architecture and Features

#### 1. DNA Pattern Analyzer (77.11% AUC)
- **Input Features**: 49 (45 base + 4 CAMP scores)
- **CAMP Score Calculation**:
  ```python
  capital_score = mean(funding_stage, total_capital_raised, cash_on_hand, 
                      monthly_burn, runway_months, investor_tier, has_debt)
  advantage_score = mean(patent_count, network_effects, has_data_moat,
                        regulatory_advantage, tech_differentiation,
                        switching_cost, brand_strength, scalability)
  market_score = mean(sector, tam_size, sam_size, som_size, market_growth,
                     customer_count, customer_concentration, user_growth,
                     net_dollar_retention, competition_intensity, competitors)
  people_score = mean(founders_count, team_size, years_experience,
                     domain_expertise, prior_startups, successful_exits,
                     board_experience, advisors, diversity, key_person)
  ```
- **Model Type**: LightGBM Classifier
- **Feature Ordering**: Stored in `dna_feature_order.pkl`

#### 2. Temporal Prediction Model (77.36% AUC)
- **Input Features**: 48 (45 base + 3 temporal)
- **Temporal Feature Engineering**:
  ```python
  growth_momentum = (revenue_growth * 0.4 + 
                    user_growth * 0.3 + 
                    net_dollar_retention * 0.3)
  
  efficiency_trend = (gross_margin * 0.5 + 
                     (100 - burn_multiple) * 0.3 + 
                     ltv_cac_ratio * 10 * 0.2)
  
  stage_velocity = (funding_stage * 0.5 + 
                   product_stage * 0.3 + 
                   log(revenue) / 20 * 0.2)
  ```
- **Model Type**: LightGBM Classifier
- **Feature Ordering**: Stored in `temporal_feature_order.pkl`

#### 3. Industry-Specific Model (77.17% AUC)
- **Input Features**: 45 (base features only)
- **Preprocessing**: StandardScaler normalization
- **Model Type**: XGBoost Classifier
- **Feature Ordering**: Stored in `industry_feature_order.pkl`
- **Scaler**: Stored in `industry_scaler.pkl`

#### 4. Ensemble Model (74.01% AUC)
- **Input Features**: 3 (predictions from DNA, Temporal, Industry)
- **Model Type**: GradientBoostingClassifier
- **Architecture**: Meta-learner combining model predictions
- **Weights**: Learned automatically during training

### Model Training Pipeline

```python
# 1. Load and prepare data
data = pd.read_csv('data/final_100k_dataset_45features.csv')

# 2. Encode categorical features
categorical_features = ['funding_stage', 'investor_tier_primary', 
                       'product_stage', 'sector']
for feature in categorical_features:
    data[feature] = label_encoder.fit_transform(data[feature])

# 3. Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# 4. Train individual models with proper feature preparation
# DNA: 45 base + 4 CAMP = 49 features
# Temporal: 45 base + 3 temporal = 48 features
# Industry: 45 base features with scaling

# 5. Train ensemble on model predictions
ensemble_features = np.column_stack([
    dna_predictions, temporal_predictions, industry_predictions
])
```

### Model Performance Metrics

```
Model               AUC    Features  Training Time
--------------------------------------------------
DNA Analyzer       77.11%     49        ~45 sec
Temporal Model     77.36%     48        ~35 sec
Industry Model     77.17%     45        ~40 sec
Ensemble Model     74.01%      3        ~10 sec
--------------------------------------------------
Average            76.36%              ~130 sec total
```

### Discrimination Power Analysis
- **Previous**: -1.63% (models couldn't distinguish success from failure)
- **Current**: 55.56% (clear separation between outcomes)
- **Success Cases**: Average probability 73.8%
- **Failure Cases**: Average probability 18.2%

## Pattern System Integration

### Pattern Architecture
- **Total Patterns**: 50+ defined, 31 active
- **Categories**: 8 master categories
- **Contribution**: 25% weight in final prediction
- **Detection**: Hierarchical classification system

### Pattern Categories:
1. **Unicorn DNA** (10 patterns)
2. **Death Valley** (6 patterns)
3. **Market Dynamics** (5 patterns)
4. **Execution Excellence** (4 patterns)
5. **Team Dynamics** (3 patterns)
6. **Financial Health** (2 patterns)
7. **Innovation Patterns** (1 pattern)
8. **Risk Patterns** (Multiple sub-patterns)

### Pattern Integration Flow:
```python
# 1. Base model predictions
base_prediction = orchestrator.predict(features)

# 2. Pattern detection and scoring
patterns = pattern_matcher.identify_patterns(features)
pattern_score = pattern_ensemble.predict(patterns)

# 3. Weighted combination
final_prediction = (base_prediction * 0.75 + 
                   pattern_score * 0.25)
```

## Frontend-Backend Contract

### Request Format:
```typescript
interface PredictionRequest {
  // Capital Features
  funding_stage: string;          // "Pre-seed", "Seed", etc.
  total_capital_raised_usd: number;
  cash_on_hand_usd: number;
  monthly_burn_usd: number;
  runway_months?: number;         // Optional, defaults to 12
  
  // Boolean fields (sent as boolean)
  has_debt: boolean;
  network_effects_present: boolean;
  has_data_moat: boolean;
  
  // Numeric fields
  scalability_score: number;      // 1-5 range
  burn_multiple?: number;         // Optional, defaults to 2.0
  
  // ... other features
}
```

### Response Format:
```typescript
interface PredictionResponse {
  probability: number;            // 0-100
  confidence_interval: {
    lower: number;
    upper: number;
  };
  confidence_score: number;       // 0-100
  
  verdict: {
    decision: "PASS" | "FAIL" | "CONDITIONAL PASS";
    strength: "Strong" | "Moderate" | "Weak";
    key_risks: string[];
    key_strengths: string[];
  };
  
  pillar_scores: {
    capital: number;
    advantage: number;
    market: number;
    people: number;
  };
  
  insights: {
    summary: string;
    strengths: string[];
    weaknesses: string[];
    recommendations: string[];
  };
  
  pattern_analysis?: {
    primary_pattern: string;
    pattern_score: number;
    similar_unicorns: string[];
    pattern_insights: string[];
  };
}
```

## Configuration Management

### Environment Variables:
```bash
# API Configuration
API_HOST=0.0.0.0
API_PORT=8001
LOG_LEVEL=INFO
ENABLE_PATTERNS=true
PATTERN_WEIGHT=0.25

# Model Paths
MODEL_PATH=models/production_v45
PATTERN_MODEL_PATH=models/pattern_models

# Feature Configuration
CANONICAL_FEATURES=45
ENABLE_FEATURE_VALIDATION=true
```

### Model Registry (`production_manifest.json`):
```json
{
  "version": "v45",
  "models": {
    "dna_analyzer": {
      "path": "models/production_v45/dna_analyzer.pkl",
      "features": 49,
      "auc": 0.7711,
      "type": "lightgbm"
    },
    "temporal_model": {
      "path": "models/production_v45/temporal_model.pkl",
      "features": 48,
      "auc": 0.7736,
      "type": "lightgbm"
    },
    "industry_model": {
      "path": "models/production_v45/industry_model.pkl",
      "features": 45,
      "auc": 0.7717,
      "type": "xgboost",
      "scaler": "models/production_v45/industry_scaler.pkl"
    },
    "ensemble_model": {
      "path": "models/production_v45/ensemble_model.pkl",
      "features": 3,
      "auc": 0.7401,
      "type": "gradient_boosting"
    }
  },
  "label_encoders": "models/production_v45/label_encoders.pkl",
  "feature_orders": {
    "dna": "models/production_v45/dna_feature_order.pkl",
    "temporal": "models/production_v45/temporal_feature_order.pkl",
    "industry": "models/production_v45/industry_feature_order.pkl"
  }
}
```

## Testing Strategy

### Integration Tests:
```python
# Test suite coverage
- Type conversion (boolean → integer)
- Feature alignment (45/48/49 features)
- Response transformation
- Pattern integration
- Error handling
- Edge cases (missing fields, invalid data)
```

### Model Validation Tests:
```python
# Discrimination power test
assert discrimination_power > 50.0  # Was -1.63%, now 55.56%

# Model agreement test
assert model_correlation > 0.65     # All pairs > 0.69

# Prediction range test
assert 0.0 <= prediction <= 1.0     # All predictions valid

# NaN check
assert nan_count == 0               # No missing predictions
```

### Performance Benchmarks:
- API Latency: < 900ms with patterns
- Model Loading: < 2 seconds
- Prediction Time: < 100ms per request
- Memory Usage: < 2GB for all models

## Deployment Guide

### Development:
```bash
# 1. Start API server
cd /Users/sf/Desktop/FLASH
python3 api_server_final_integrated.py

# 2. Start frontend
cd flash-frontend
npm start

# 3. Verify integration
python3 test_full_integration.py
```

### Production:
```bash
# 1. Build frontend
cd flash-frontend
npm run build

# 2. Start production server
gunicorn api_server_final_integrated:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8001

# 3. Serve frontend via nginx
server {
    listen 80;
    location / {
        root /var/www/flash-frontend/build;
    }
    location /api {
        proxy_pass http://localhost:8001;
    }
}
```

### Docker Deployment:
```dockerfile
# Backend Dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "api_server_final_integrated:app", "--host", "0.0.0.0", "--port", "8001"]

# Frontend Dockerfile  
FROM node:16-alpine as build
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/build /usr/share/nginx/html
```

## Monitoring and Logging

### Log Files:
- `api_final_integrated.log` - Main API server logs
- `pattern_analysis.log` - Pattern system diagnostics
- `model_performance.log` - Prediction metrics

### Key Metrics to Monitor:
1. **Prediction Distribution**: Should be 20-85% range
2. **Model Agreement**: Correlation > 0.65
3. **Discrimination Power**: > 50%
4. **API Response Time**: < 1 second
5. **Error Rate**: < 0.1%

### Health Check Endpoint:
```bash
curl http://localhost:8001/health

{
  "status": "healthy",
  "models_loaded": true,
  "pattern_system": "active",
  "discrimination_power": 55.56,
  "average_auc": 76.36,
  "uptime_seconds": 3600
}
```

## Troubleshooting

### Common Issues:

1. **Feature Mismatch Errors**
   - Symptom: "Expected 49 features, got 45"
   - Solution: Ensure proper feature preparation functions are used
   - Check: Feature order files are loaded correctly

2. **Low Discrimination Power**
   - Symptom: Similar probabilities for all predictions
   - Solution: Verify models are loaded from production_v45
   - Check: Label encoders are applied correctly

3. **Type Conversion Failures**
   - Symptom: "Invalid literal for int()"
   - Solution: Check type_converter.py is handling all fields
   - Debug: Log raw request data before conversion

4. **Pattern System Not Working**
   - Symptom: No pattern insights in response
   - Solution: Ensure ENABLE_PATTERNS=true
   - Check: Pattern models are loaded successfully

### Debug Commands:
```bash
# Check model files
ls -la models/production_v45/*.pkl

# Verify feature counts
python3 -c "import joblib; print(len(joblib.load('models/production_v45/dna_feature_order.pkl')))"

# Test model predictions
python3 test_retrained_models.py

# Check API logs
tail -f api_final_integrated.log | grep ERROR
```

## Performance Optimization

### Model Loading:
```python
# Lazy loading for faster startup
models = {}
def get_model(name):
    if name not in models:
        models[name] = joblib.load(f'models/production_v45/{name}.pkl')
    return models[name]
```

### Batch Predictions:
```python
# Process multiple startups efficiently
def batch_predict(startup_list):
    features = prepare_features_batch(startup_list)
    predictions = model.predict_proba(features)
    return process_results_batch(predictions)
```

### Caching Strategy:
- Cache model predictions for 5 minutes
- Cache pattern analysis for 15 minutes
- Use Redis for distributed caching in production

## Future Enhancements

### Planned for V12:
1. **AutoML Integration**: Automated model retraining
2. **Real-time Learning**: Update models with new data
3. **Explainable AI**: SHAP values for all predictions
4. **Multi-region Support**: Locale-specific models
5. **GraphQL API**: More flexible data queries

### Research Directions:
1. **Transformer Models**: For better pattern recognition
2. **Time Series Analysis**: Track startup evolution
3. **Network Effects**: Analyze founder/investor connections
4. **Market Timing**: Incorporate macro trends
5. **Competitive Intelligence**: Real-time market analysis

## Migration Guide

### From V10 to V11:
```bash
# 1. Backup current models
cp -r models/production_v45 models/backup_v10

# 2. Copy new models
cp -r models/production_v45_fixed/* models/production_v45/

# 3. Update configuration
export DISCRIMINATION_THRESHOLD=0.5  # Was 0.0

# 4. Restart services
systemctl restart flash-api
systemctl restart flash-frontend

# 5. Verify performance
python3 test_retrained_models.py
```

## API Examples

### Basic Prediction:
```bash
curl -X POST http://localhost:8001/predict \
  -H "Content-Type: application/json" \
  -d '{
    "funding_stage": "Seed",
    "total_capital_raised_usd": 2000000,
    "has_debt": false,
    "scalability_score": 4.5,
    ...
  }'
```

### Enhanced Prediction with Patterns:
```bash
curl -X POST http://localhost:8001/predict_enhanced \
  -H "Content-Type: application/json" \
  -d '{ ... startup data ... }'
```

### Pattern Analysis:
```bash
curl -X POST http://localhost:8001/analyze_pattern \
  -H "Content-Type: application/json" \
  -d '{
    "pattern_name": "unicorn_dna",
    "startup_data": { ... }
  }'
```

## Security Considerations

### Input Validation:
- All numeric fields checked for valid ranges
- String fields sanitized for SQL injection
- Request size limited to 1MB
- Rate limiting: 100 requests/minute per IP

### Model Protection:
- Models stored with restricted permissions
- No direct model file access via API
- Prediction logic isolated in secure containers
- Regular security audits of dependencies

## Conclusion

FLASH V11 represents a major milestone in the system's evolution, with dramatically improved discrimination power (from -1.63% to 55.56%) and consistent feature handling across all models. The system now reliably distinguishes between successful and failing startups with an average model performance of 76.36% AUC.

Key achievements in V11:
- ✅ Fixed feature alignment issues across all models
- ✅ Improved discrimination power by over 57 percentage points
- ✅ Maintained high model agreement (>69% correlation)
- ✅ Zero NaN predictions with robust error handling
- ✅ Production-ready with comprehensive testing

The system is now fully operational and ready for production deployment with real predictive power and reliable performance.

---

**Version**: 11.0  
**Last Updated**: May 31, 2025  
**Status**: Production Ready  
**Performance**: 76.36% Average AUC, 55.56% Discrimination Power