# API Server Architecture

## Current Structure (After Cleanup)

- `api_server.py` -> Symlink to `api_server_unified.py`
- `api_server_unified.py` -> Main unified API server with feature alignment

## Archived Versions

The following API server versions have been archived to `archive/api_servers/`:
- `api_server_v3.py` - Previous version 3
- `api_server_final.py` - Previous "final" version

## Key Improvements in Unified Server

1. **Feature Alignment**: Automatically handles models expecting different feature counts
2. **Consolidated Code**: Single source of truth for API logic
3. **Better Error Handling**: Comprehensive error messages and logging
4. **Pattern Integration**: Seamless pattern system integration
5. **Model Management**: Centralized model loading and prediction

## Usage

```bash
# Start the API server
python api_server.py

# Or directly
python api_server_unified.py
```

The server runs on port 8001 by default.
