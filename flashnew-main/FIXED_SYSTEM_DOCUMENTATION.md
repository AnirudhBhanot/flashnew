# FLASH Fixed System Documentation

## Overview
The FLASH Fixed System is a complete rewrite that eliminates all shortcuts, patches, and caching issues from the original system.

## Key Improvements

### 1. No Global State
- Orchestrator created fresh for each request
- No singleton pattern
- No module-level caching

### 2. Proper Feature Normalization
- All features normalized to 0-1 range
- Consistent handling of monetary values, percentages, scores
- Special handling for inverse metrics (burn_multiple, customer_concentration)

### 3. Fixed Model Loading
- Models loaded from disk for each request
- No persistent state between requests
- Clear model directory structure

### 4. Correct Verdict Calculation
- Based on probability thresholds
- < 50%: FAIL
- 50-65%: CONDITIONAL PASS
- 65-80%: PASS
- > 80%: STRONG PASS

## Usage

### Starting the System
```bash
./start_fixed_system.sh
```

### Running Tests
```bash
python3 test_fixed_system_integration.py
```

### API Endpoints
- POST /predict - Main prediction endpoint
- POST /predict_enhanced - Same as /predict
- GET /health - Health check
- GET /config/stage-weights - Stage-specific CAMP weights
- GET /validate - List required features

## Architecture

### Components
1. **api_server_fixed.py** - Fixed API server without caching
2. **unified_orchestrator_v3_fixed.py** - Fixed orchestrator
3. **models/production_v45_fixed/** - Retrained models

### Data Flow
1. Frontend sends data to API
2. API creates fresh orchestrator
3. Orchestrator normalizes features
4. Models make predictions
5. Results combined and returned

## Testing

The integration tests verify:
- Terrible startups get < 35% and FAIL
- Mediocre startups get 40-55% and FAIL/CONDITIONAL PASS
- Excellent startups get > 65% and PASS

## Troubleshooting

### High predictions for bad startups
1. Verify models are from production_v45_fixed
2. Check feature normalization
3. Ensure no caching is occurring

### Server won't start
1. Check port 8001 is free
2. Clean Python cache
3. Verify all dependencies installed

### Tests failing
1. Ensure models are properly trained
2. Check API server is using fixed version
3. Verify no old processes running
