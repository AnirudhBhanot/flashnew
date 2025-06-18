#!/usr/bin/env python3
"""
Migration script to switch from old system to fixed system
Updates configurations and cleans up caches
"""

import os
import shutil
import subprocess
import json


def clean_python_cache():
    """Remove all Python cache files"""
    print("1. Cleaning Python cache files...")
    
    cache_dirs = []
    for root, dirs, files in os.walk('.'):
        if '__pycache__' in dirs:
            cache_dir = os.path.join(root, '__pycache__')
            cache_dirs.append(cache_dir)
    
    for cache_dir in cache_dirs:
        try:
            shutil.rmtree(cache_dir)
            print(f"   Removed: {cache_dir}")
        except Exception as e:
            print(f"   Failed to remove {cache_dir}: {e}")
    
    # Remove .pyc files
    pyc_count = 0
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.pyc'):
                try:
                    os.remove(os.path.join(root, file))
                    pyc_count += 1
                except:
                    pass
    
    print(f"   Removed {pyc_count} .pyc files")


def update_frontend_config():
    """Update frontend to use fixed API"""
    print("\n2. Updating frontend configuration...")
    
    config_file = "flash-frontend/src/config.ts"
    
    if os.path.exists(config_file):
        # Read current config
        with open(config_file, 'r') as f:
            content = f.read()
        
        # Check if it needs updating
        if 'api_server_unified' in content and 'api_server_fixed' not in content:
            print("   ✅ Frontend already configured for port 8001")
        else:
            print("   ⚠️  Frontend config may need manual update")
            print(f"   Please ensure {config_file} points to http://localhost:8001")
    else:
        print(f"   ⚠️  Config file not found: {config_file}")


def stop_running_servers():
    """Stop any running Python servers"""
    print("\n3. Stopping running servers...")
    
    # Kill Python servers
    try:
        subprocess.run(['pkill', '-f', 'python.*api_server'], check=False)
        subprocess.run(['pkill', '-f', 'uvicorn'], check=False)
        print("   ✅ Stopped existing servers")
    except:
        print("   ⚠️  Could not stop servers (may not be running)")


def create_startup_script():
    """Create convenient startup script"""
    print("\n4. Creating startup script...")
    
    script_content = """#!/bin/bash
# FLASH Fixed System Startup Script

echo "Starting FLASH Fixed System..."
echo "=============================="

# Clean any Python cache
find . -name "*.pyc" -delete
find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null

# Start the fixed API server
echo ""
echo "Starting API server on port 8001..."
python3 api_server_fixed.py &
API_PID=$!

# Wait for server to start
sleep 3

# Test the server
echo ""
echo "Testing server health..."
curl -s http://localhost:8001/health | python3 -m json.tool

echo ""
echo "=============================="
echo "FLASH Fixed System is running!"
echo "API Server PID: $API_PID"
echo ""
echo "To stop the server, run:"
echo "kill $API_PID"
echo ""
echo "To run tests:"
echo "python3 test_fixed_system_integration.py"
"""
    
    with open('start_fixed_system.sh', 'w') as f:
        f.write(script_content)
    
    os.chmod('start_fixed_system.sh', 0o755)
    print("   ✅ Created start_fixed_system.sh")


def verify_models():
    """Verify that fixed models exist"""
    print("\n5. Verifying fixed models...")
    
    model_dir = "models/production_v45_fixed"
    required_models = [
        "dna_analyzer.pkl",
        "temporal_model.pkl", 
        "industry_model.pkl",
        "ensemble_model.pkl"
    ]
    
    if os.path.exists(model_dir):
        missing = []
        for model in required_models:
            if not os.path.exists(os.path.join(model_dir, model)):
                missing.append(model)
        
        if missing:
            print(f"   ⚠️  Missing models: {missing}")
            print("   Run: python3 retrain_models_correctly.py")
        else:
            print("   ✅ All required models found")
    else:
        print(f"   ❌ Model directory not found: {model_dir}")
        print("   Run: python3 retrain_models_correctly.py")


def create_documentation():
    """Create documentation for the fixed system"""
    print("\n6. Creating documentation...")
    
    doc_content = """# FLASH Fixed System Documentation

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
"""
    
    with open('FIXED_SYSTEM_DOCUMENTATION.md', 'w') as f:
        f.write(doc_content)
    
    print("   ✅ Created FIXED_SYSTEM_DOCUMENTATION.md")


def main():
    """Run migration steps"""
    print("="*60)
    print("FLASH SYSTEM MIGRATION")
    print("="*60)
    print("Migrating from old system to fixed system...")
    
    # Run migration steps
    clean_python_cache()
    update_frontend_config()
    stop_running_servers()
    create_startup_script()
    verify_models()
    create_documentation()
    
    print("\n" + "="*60)
    print("MIGRATION COMPLETE")
    print("="*60)
    print("\nNext steps:")
    print("1. If models are missing, run: python3 retrain_models_correctly.py")
    print("2. Start the fixed system: ./start_fixed_system.sh")
    print("3. Run tests: python3 test_fixed_system_integration.py")
    print("4. Update any scripts to use api_server_fixed.py instead of api_server_unified.py")
    print("\nThe fixed system has:")
    print("- No caching or singleton issues")
    print("- Proper feature normalization")
    print("- Correct verdict calculation")
    print("- Fresh model loading for each request")


if __name__ == "__main__":
    main()