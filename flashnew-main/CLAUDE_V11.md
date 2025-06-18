# FLASH Platform - Context for Claude V11

## Project Overview
FLASH (Fast Learning and Assessment of Startup Health) is an advanced AI platform for evaluating startup success probability using the CAMP framework (Capital, Advantage, Market, People). The system uses **real trained models** achieving ~76% accuracy with 55.56% discrimination power.

## Latest Updates (May 31, 2025 - V11)
- **DISCRIMINATION POWER FIXED**: Improved from -1.63% to 55.56%!
- **Model Retraining Complete**: All models retrained with consistent feature handling
- **Feature Alignment Resolved**: Models properly handle 45/48/49 features
- **Production Models Updated**: All models in production_v45 directory
- **High Model Agreement**: Correlations between models > 69%
- **Zero NaN Predictions**: Robust error handling ensures valid outputs

## Critical Performance Improvements (V11)
- **DNA Analyzer**: 77.11% AUC (49 features: 45 base + 4 CAMP)
- **Temporal Model**: 77.36% AUC (48 features: 45 base + 3 temporal)
- **Industry Model**: 77.17% AUC (45 features: base only)
- **Ensemble Model**: 74.01% AUC (3 features: model predictions)
- **Average Performance**: 76.36% AUC
- **Discrimination Power**: 55.56% (was -1.63%)

## Key Technical Details

### API Server (Fully Integrated)
#### Final Integrated API (api_server_final_integrated.py) - Port 8001
- **Type Conversion**: Automatic handling of frontend data formats
- **Response Transformation**: Backend → Frontend format mapping
- **Pattern Support**: Full integration with 31 active patterns (25% weight)
- **Feature Alignment**: Handles models expecting 45/48/49 features
- **All Endpoints Working**:
  - `/predict` - Standard prediction with type conversion
  - `/predict_simple` - Alias for frontend compatibility
  - `/predict_advanced` - Alias to `/predict_enhanced`
  - `/predict_enhanced` - Enhanced with pattern analysis
  - `/investor_profiles` - Returns 3 investor templates
  - `/patterns` - List all 31 patterns
  - `/patterns/{name}` - Pattern details
  - `/analyze_pattern` - Pattern analysis
  - `/features` - Feature documentation
  - `/system_info` - System configuration
  - `/health` - Health check

### Real Model Performance (production_v45)
- **Success Cases**: Mean probability = 73.8%
- **Failure Cases**: Mean probability = 18.2%
- **Clear Separation**: 55.56% discrimination between outcomes
- **Model Agreement**: All correlations > 0.69
- **No NaN Values**: 100% valid predictions

### Feature Engineering Details

#### DNA Analyzer Features (49 total)
```python
# 45 base features + 4 CAMP scores
capital_score = mean([funding_stage, total_capital_raised, cash_on_hand, 
                     monthly_burn, runway_months, investor_tier, has_debt])
advantage_score = mean([patent_count, network_effects, has_data_moat,
                       regulatory_advantage, tech_differentiation,
                       switching_cost, brand_strength, scalability])
market_score = mean([sector, tam_size, sam_size, som_size, market_growth,
                    customer_count, customer_concentration, user_growth,
                    net_dollar_retention, competition_intensity, competitors])
people_score = mean([founders_count, team_size, years_experience,
                    domain_expertise, prior_startups, successful_exits,
                    board_experience, advisors, diversity, key_person])
```

#### Temporal Model Features (48 total)
```python
# 45 base features + 3 temporal features
growth_momentum = (revenue_growth * 0.4 + user_growth * 0.3 + ndr * 0.3)
efficiency_trend = (gross_margin * 0.5 + (100-burn_multiple) * 0.3 + ltv_cac * 0.2)
stage_velocity = (funding_stage * 0.5 + product_stage * 0.3 + log(revenue) * 0.2)
```

#### Industry Model Features (45 total)
- Uses base features only with StandardScaler normalization

### Frontend Architecture
- **Version 3 (Active)**: Apple-inspired dark theme
  - Business View: Non-technical stakeholder focused
  - Technical View: Data-rich analysis for experts
- **Key Components**:
  - `AppV3.tsx`: Main app with dark theme
  - `WorldClassResults.tsx`: Premium results display
  - `ConfidenceVisualization.tsx`: Trust-building metrics
  - `CAMPRadarChart.tsx`: Interactive CAMP analysis

### Model Training Commands
```bash
# Train all models with consistent features (recommended)
python train_all_models_45features.py

# Train individual models
python train_ensemble_model_only.py  # Just ensemble

# Test model performance
python test_retrained_models.py
```

### Testing
- **API Tests**: `tests/test_api.py`
- **Integration Tests**: `test_full_integration.py`
- **Model Tests**: `test_retrained_models.py`
- **Run All**: `pytest tests/ -v --cov=. --cov-report=html`

## Common Commands

```bash
# Start INTEGRATED API server (port 8001) - V11 with all fixes
cd /Users/sf/Desktop/FLASH && python3 api_server_final_integrated.py

# Run frontend
cd flash-frontend && npm start

# Test model predictions
python test_retrained_models.py

# Check discrimination power
python test_integrated_system.py

# Train models (if needed)
python train_all_models_45features.py

# Check logs
tail -f api_final_integrated.log
tail -f flash-frontend/react.log

# Kill running servers
pkill -f "python.*api_server"
```

## Important Files

### Core System (V11)
- `api_server_final_integrated.py`: MAIN API server with all integrations
- `type_converter.py`: Frontend→Backend data conversion
- `models/unified_orchestrator_v3.py`: Orchestrator with pattern system
- `feature_config.py`: Canonical 45-feature definitions
- `test_retrained_models.py`: Model performance verification
- `TECHNICAL_DOCUMENTATION_V11.md`: Latest complete documentation

### Model Files (All Real - No Placeholders!)
- `models/production_v45/dna_analyzer.pkl`: DNA analyzer (77.11% AUC)
- `models/production_v45/temporal_model.pkl`: Temporal model (77.36% AUC)
- `models/production_v45/industry_model.pkl`: Industry model (77.17% AUC)
- `models/production_v45/ensemble_model.pkl`: Ensemble model (74.01% AUC)
- `models/production_v45/label_encoders.pkl`: Categorical encoders
- `models/production_v45/*_feature_order.pkl`: Feature ordering for each model
- `models/production_v45/industry_scaler.pkl`: Preprocessing scaler

### Pattern System
- `ml_core/models/pattern_definitions.py`: 50+ pattern definitions
- `ml_core/models/pattern_matcher_v2.py`: Advanced pattern matching
- `models/pattern_models/`: 31 trained pattern models

## Key Features (V11)
1. **Strong Discrimination**: 55.56% separation between success/failure
2. **High Accuracy**: ~76% average AUC across all models
3. **45 Canonical Features**: Standardized across all components
4. **31 Active Patterns**: Contributing 25% to final prediction
5. **Model Consensus**: High agreement (>69%) between models
6. **Robust Predictions**: Zero NaN values, all predictions valid
7. **Fast Training**: ~2 minutes for all models
8. **Full Integration**: Features, models, and patterns working together
9. **Production Ready**: All systems properly configured
10. **Business/Technical Views**: Dual interface for different audiences
11. **Trust Building**: Confidence intervals and model transparency
12. **Interactive Visualizations**: CAMP radar chart, progress tracking

## Development Guidelines (V11)
- **Start the right server**: `python3 api_server_final_integrated.py`
- **Test predictions**: `python3 test_retrained_models.py`
- **Check discrimination**: Should be ~55% (was -1.63%)
- **Model agreement**: All correlations should be > 0.65
- **Port**: Always use 8001 (configured everywhere)
- **Frontend data**: Can send booleans, nulls, extra fields - all handled
- **Response format**: Automatically transformed to frontend expectations
- **Pattern system**: Integrated with 25% weight
- **Logs**: Check `api_final_integrated.log` for issues

## Performance Expectations (V11)
- **Current AUC**: 76.36% average
- **Discrimination**: 55.56% (dramatically improved!)
- **Success Probability Mean**: 73.8% for successful startups
- **Failure Probability Mean**: 18.2% for failed startups
- **Latency**: <900ms with pattern analysis
- **Model Agreement**: >69% correlation between all models
- **Training Time**: ~2 minutes for all models
- **Pattern Detection**: 31 patterns across 8 categories

## Model Performance Summary

### Individual Models
| Model | AUC | Features | Purpose |
|-------|-----|----------|---------|
| DNA Analyzer | 77.11% | 49 | CAMP score analysis |
| Temporal | 77.36% | 48 | Time-based patterns |
| Industry | 77.17% | 45 | Sector-specific insights |
| Ensemble | 74.01% | 3 | Meta-learning combination |

### Discrimination Analysis
| Metric | Before (V10) | After (V11) | Improvement |
|--------|--------------|-------------|-------------|
| Success Mean | 41.7% | 73.8% | +32.1pp |
| Failure Mean | 43.3% | 18.2% | -25.1pp |
| Discrimination | -1.63% | 55.56% | +57.19pp |

## Frontend-Backend Feature Alignment
- **45 Core Features**: Perfect match between frontend and backend
- **CAMP Distribution**: 
  - Capital: 7 features
  - Advantage: 8 features
  - Market: 11 features
  - People: 10 features
  - Product: 9 features
- **Data Transformations**: Handled in type_converter.py
- **Field Conversions**:
  - funding_stage: "Pre-seed" → "pre_seed"
  - investor_tier_primary: "Tier 1" → "tier_1"
  - scalability_score: 1-5 range (not percentage)
  - booleans: true/false → 1/0

## V11 Major Fixes - Discrimination Power Restored!
1. **Feature Ordering**: Fixed inconsistent feature ordering ✅
2. **Model Retraining**: All models retrained with proper alignment ✅
3. **Discrimination Power**: Improved from -1.63% to 55.56% ✅
4. **Prediction Validity**: Zero NaN predictions ✅
5. **Model Agreement**: All correlations > 69% ✅
6. **Production Ready**: All models deployed successfully ✅

## Documentation (Updated V11)
- **[TECHNICAL_DOCUMENTATION_V11.md](TECHNICAL_DOCUMENTATION_V11.md)** - LATEST with V11 improvements
- **[IMPLEMENTATION_COMPLETE_SUMMARY.md](IMPLEMENTATION_COMPLETE_SUMMARY.md)** - Integration details
- **[MASTER_DOCUMENTATION.md](MASTER_DOCUMENTATION.md)** - Comprehensive system docs
- **[PATTERN_SYSTEM_SUMMARY.md](PATTERN_SYSTEM_SUMMARY.md)** - Pattern implementation

## Important Notes
- All placeholder models have been replaced
- Models now show strong discrimination (55.56%)
- System can clearly distinguish between success and failure
- Production models are in `models/production_v45/`
- Frontend has 3 versions - V3 is the active Apple-inspired design
- Pattern system adds additional predictive power

## Quick Reference - Model Status

```bash
# Verify discrimination power
python test_retrained_models.py | grep "Discrimination:"
# Should show: Discrimination: 55.56%

# Check model files
ls -la models/production_v45/*.pkl

# Verify model performance
cat models/production_v45/ensemble_metadata.json

# Test live predictions
curl -X POST http://localhost:8001/predict -H "Content-Type: application/json" -d @test_startup.json
```

---
**Last Updated**: 2025-05-31
**Version**: V11
**Status**: PRODUCTION READY
**Average Performance**: 76.36% AUC
**Discrimination Power**: 55.56% (FIXED!)
**UI Version**: V3 Apple-Inspired Dark Theme
**Feature Count**: 45 canonical features
**Pattern Count**: 31 active patterns