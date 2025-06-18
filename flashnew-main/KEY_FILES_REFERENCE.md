# Key Files Reference - FLASH Platform
## Updated: June 3, 2025

## 🚀 Main Executable Files

### API Server (Use This!)
- **`api_server_unified_final.py`** - The working API server with all fixes
  ```bash
  DISABLE_AUTH=true python3 api_server_unified_final.py
  ```

### Startup Script
- **`start_flash.sh`** - Starts both API and frontend
  ```bash
  ./start_flash.sh
  ```

## 📊 Model Files

### Production Models (v45)
- `models/production_v45/dna_analyzer.pkl` - DNA pattern analyzer (99.36% AUC)
- `models/production_v45/temporal_model.pkl` - Temporal predictions (99.80% AUC)
- `models/production_v45/industry_model.pkl` - Industry-specific (99.80% AUC)
- `models/production_v45/ensemble_model.pkl` - Ensemble model
- `models/production_v45/feature_scaler.pkl` - Feature scaling

### Orchestrator
- `models/unified_orchestrator_v3_integrated.py` - Main prediction orchestrator (MODIFIED)

## 🧪 Testing Files

### Integration Tests
- `test_frontend_integration_noauth.py` - Full integration test suite
- `test_predict_simple.py` - Simple prediction test
- `test_direct_api.py` - Direct orchestrator testing

## 📝 Data Files

### Datasets
- `realistic_200k_dataset.csv` - 200k company training data
- `generate_realistic_200k_dataset.py` - Dataset generator

### Training Scripts
- `train_essential_models_200k.py` - Fast model training
- `train_models_realistic_200k.py` - Full training script

## 🔧 Configuration Files

### Core Config
- `feature_config.py` - Defines the 45 canonical features
- `config.py` - API configuration and settings
- `type_converter_simple.py` - Frontend to backend data conversion

## 📚 Documentation

### Main Docs
- `CLAUDE.md` - Main context file (UPDATED with V13)
- `CHANGES_DOCUMENTATION.md` - All changes from this session
- `KEY_FILES_REFERENCE.md` - This file

## 🚫 Deprecated Files (Don't Use)

- `api_server_unified.py` - Has validation issues
- `api_server.py` - Old version
- `api_server_*.py` - Various experimental versions

## 💡 Quick Commands

### Test API Health
```bash
curl http://localhost:8001/health | jq .
```

### Test Prediction
```bash
curl -X POST http://localhost:8001/predict \
  -H "Content-Type: application/json" \
  -d '{"total_capital_raised_usd": 5000000, "sector": "saas"}' | jq .
```

### Kill All Servers
```bash
pkill -f "api_server" && pkill -f "npm.*start"
```

### Check Ports
```bash
lsof -i :8001  # API server
lsof -i :3000  # Frontend
```