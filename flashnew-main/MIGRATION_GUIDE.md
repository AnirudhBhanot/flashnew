# API Migration Guide

## Overview
The FLASH API has been consolidated into a single, unified version that integrates:
- All 45 canonical features
- Hierarchical pattern system (31 active patterns)
- Enhanced validation and error handling
- Comprehensive API endpoints

## Migration Steps

### 1. Update API Server
Replace references to old API servers:
- `api_server.py` → `api_server_final.py`
- `api_server_v2.py` → `api_server_final.py`

### 2. Update Imports
```python
# Old
from models.unified_orchestrator import UnifiedModelOrchestrator

# New
from models.unified_orchestrator_v3 import get_orchestrator
```

### 3. Feature Configuration
All features are now centralized in `feature_config.py`:
```python
from feature_config import ALL_FEATURES, validate_features
```

### 4. API Endpoints
The final API includes all endpoints:
- `/predict` - Enhanced predictions with patterns
- `/analyze` - Detailed analysis
- `/patterns` - Pattern management
- `/features` - Feature documentation

### 5. Running the Server
```bash
# Start the final API server
python3 api_server_final.py

# Default port: 8001
# Health check: http://localhost:8001/health
```

## Archived Files
Old versions have been moved to `archive/old_versions/` for reference.

## Feature Count
The system now uses exactly 45 features as defined in the dataset:
- Capital: 7 features
- Advantage: 8 features  
- Market: 11 features
- People: 10 features
- Product: 9 features

Total: 45 features
