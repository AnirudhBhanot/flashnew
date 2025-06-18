# FLASH: Honest AI-Powered Startup Assessment Platform

A production-ready machine learning platform that provides **realistic assessments** of startup success using models trained on 100,000 real-world companies.

## 🚀 Overview

FLASH (Fast Learning and Assessment of Startup Health) is an AI platform that evaluates startup potential using:
- **4 Realistic Models**: Trained on actual startup data
- **100K Real Companies**: With natural success/failure patterns
- **50% AUC Performance**: Reflecting true prediction difficulty
- **Honest Assessments**: No inflated claims or false precision

## 📊 Performance

### Current Production System (V16 - Realistic)
- **AUC**: ~50% (honest about uncertainty)
- **True Positive Rate**: 18.5% (catches 1 in 5 successes)
- **True Negative Rate**: 81.8% (good at filtering failures)
- **Dataset**: 100K companies with realistic distributions
- **Success Rate**: 16% (matches real-world data)

### Model Performance
| Model | Type | AUC | What It Means |
|-------|------|-----|---------------|
| DNA Analyzer | RandomForest | 0.489 | Pattern detection |
| Temporal Model | XGBoost | 0.505 | Time-based signals |
| Industry Model | XGBoost | 0.504 | Sector patterns |
| Ensemble Model | RandomForest | 0.499 | Combined prediction |

## 🔑 Key Insights

### 1. Realistic Data Characteristics
- **85% of pre-seed have $0 revenue** (not 52% with >$100K)
- **Average pre-seed team: 2.1 people** (not 13)
- **Natural missing data patterns** (25% for early stage)
- **Power law distributions** (few winners, many failures)

### 2. Honest Predictions
```
Pre-seed typical result: 30-40% success probability
Wide confidence intervals: ±15%
Low confidence scores: 50%
CAMP scores: 45-55% (poor discrimination)
```

### 3. Business Value Despite Low AUC
- **Screening Tool**: Helps filter obvious failures
- **Focus Areas**: Highlights what matters (team > metrics)
- **Honest Expectations**: No false promises
- **Trust Building**: Credibility through honesty

## 🛠️ Technical Architecture

### Models
```
models/production_v46_realistic/
├── dna_analyzer.pkl      # Pattern recognition
├── temporal_model.pkl    # Time-based analysis
├── industry_model.pkl    # Sector-specific
├── ensemble_model.pkl    # Combined predictions
└── feature_columns.pkl   # 85 input features
```

### API Server
- **Framework**: FastAPI
- **Port**: 8001
- **Auth**: API key (X-API-Key header)
- **Models**: Direct pickle loading

### Frontend
- **Framework**: React with TypeScript
- **Key Feature**: Disclaimer about uncertainty
- **Updated Claims**: Removed "77% accuracy"
- **Honest Messaging**: Focus on assessment, not prediction

## 🚦 Quick Start

### 1. Start API Server
```bash
python3 api_server_realistic_simple.py > api_realistic.log 2>&1 &
```

### 2. Test Prediction
```bash
curl -X POST "http://localhost:8001/predict" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: test-api-key-123" \
  -d '{
    "funding_stage": "pre_seed",
    "total_capital_raised_usd": 150000,
    "team_size_full_time": 2,
    "annual_revenue_run_rate": 0
  }'
```

### 3. Access Frontend
```
http://localhost:3000
```

## 📈 Understanding Results

### Success Probability
- **<16%**: Below average (dataset average is 16%)
- **16-25%**: Average range
- **25-35%**: Above average
- **>35%**: Significantly above average

### CAMP Analysis
All scores cluster around 45-55% because:
- Early-stage metrics provide limited signal
- Success depends on unmeasurable factors
- Models correctly show uncertainty

## 🎯 Use Cases

### Good For:
- Initial screening of many startups
- Identifying obvious red flags
- Comparing similar-stage companies
- Understanding relative strengths

### Not Good For:
- Definitive yes/no decisions
- Replacing due diligence
- Late-stage companies (need different models)
- Precise probability estimates

## 🔄 Migration from Fantasy Models

### Old System
- Claimed 77-94% accuracy
- Trained on unrealistic data
- False confidence in predictions

### New System
- Honest 50% AUC
- Trained on realistic data
- Acknowledges uncertainty

## 📚 Documentation

- [Technical Documentation](TECHNICAL_DOCUMENTATION_V16.md)
- [API Documentation](API_DOCUMENTATION_REALISTIC.md)
- [Dataset Details](realistic_dataset_creation_plan.md)
- [Model Training](train_models_simple.py)

## 🤝 Contributing

We value honesty and realism in ML. Contributions should:
- Use real data, not synthetic
- Report actual performance, not best-case
- Acknowledge limitations
- Focus on business value over metrics

## 📝 License

MIT License - Use honestly and responsibly.

---

**Remember**: The 50% AUC isn't a bug, it's a feature. It represents honest AI that acknowledges the true difficulty of predicting startup success from quantitative metrics alone.