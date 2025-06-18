#!/usr/bin/env python3
"""
Fix Critical Mismatches in FLASH Codebase
Addresses port, endpoint, and type mismatches
"""

import json
import re
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

def fix_port_configuration():
    """Standardize port configuration to 8001"""
    logger.info("Fixing port configuration...")
    
    # Update config.py
    config_file = Path('config.py')
    if config_file.exists():
        content = config_file.read_text()
        # Update API_PORT to 8001
        content = re.sub(r'API_PORT[:\s]*=\s*\d+', 'API_PORT = 8001', content)
        config_file.write_text(content)
        logger.info("✓ Updated config.py to use port 8001")
    
    # Check frontend config
    frontend_config = Path('flash-frontend/src/config.ts')
    if frontend_config.exists():
        content = frontend_config.read_text()
        if '8001' in content:
            logger.info("✓ Frontend already configured for port 8001")
        else:
            logger.warning("Frontend config needs manual update")

def create_endpoint_mapping():
    """Create endpoint mapping for missing endpoints"""
    logger.info("\nCreating endpoint mapping...")
    
    endpoint_code = '''
# Add these endpoint mappings to api_server_working.py

@app.route("/predict_simple", methods=["POST"])
async def predict_simple(request: Request):
    """Alias for /predict endpoint for frontend compatibility"""
    return await predict(request)

@app.route("/predict_advanced", methods=["POST"])
async def predict_advanced(request: Request):
    """Alias for /predict_enhanced endpoint for frontend compatibility"""
    return await predict_enhanced(request)

@app.route("/investor_profiles", methods=["GET"])
async def investor_profiles():
    """Return investor profile templates"""
    profiles = {
        "conservative": {
            "name": "Conservative Investor",
            "risk_tolerance": "low",
            "preferred_stages": ["series_b", "series_c"],
            "preferred_metrics": {
                "burn_multiple": {"max": 1.5},
                "runway_months": {"min": 18},
                "gross_margin_percent": {"min": 70}
            }
        },
        "aggressive": {
            "name": "Aggressive Growth Investor",
            "risk_tolerance": "high",
            "preferred_stages": ["seed", "series_a"],
            "preferred_metrics": {
                "revenue_growth_rate_percent": {"min": 100},
                "user_growth_rate_percent": {"min": 50}
            }
        },
        "balanced": {
            "name": "Balanced Investor",
            "risk_tolerance": "medium",
            "preferred_stages": ["series_a", "series_b"],
            "preferred_metrics": {
                "burn_multiple": {"max": 2.0},
                "ltv_cac_ratio": {"min": 3.0}
            }
        }
    }
    return {"profiles": profiles}
'''
    
    with open('endpoint_mappings.py', 'w') as f:
        f.write(endpoint_code)
    
    logger.info("✓ Created endpoint_mappings.py with missing endpoints")

def create_type_converter():
    """Create type conversion utilities"""
    logger.info("\nCreating type conversion utilities...")
    
    converter_code = '''#!/usr/bin/env python3
"""
Type Conversion Utilities
Handles frontend-backend type mismatches
"""

from typing import Dict, Any

# Boolean fields that frontend sends as true/false
BOOLEAN_FIELDS = [
    'has_debt',
    'network_effects_present',
    'has_data_moat',
    'regulatory_advantage_present',
    'key_person_dependency'
]

# Optional fields that need defaults
OPTIONAL_FIELDS = {
    'runway_months': 12,  # Default 12 months
    'burn_multiple': 2.0  # Default 2.0
}

# Fields to remove (not in backend)
EXTRA_FIELDS = [
    'team_cohesion_score',
    'hiring_velocity_score',
    'diversity_score',
    'technical_expertise_score'
]

def convert_frontend_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """Convert frontend data format to backend format"""
    converted = data.copy()
    
    # Convert booleans to 0/1
    for field in BOOLEAN_FIELDS:
        if field in converted:
            if isinstance(converted[field], bool):
                converted[field] = 1 if converted[field] else 0
            elif isinstance(converted[field], str):
                converted[field] = 1 if converted[field].lower() == 'true' else 0
    
    # Add defaults for optional fields
    for field, default in OPTIONAL_FIELDS.items():
        if field not in converted or converted[field] is None:
            converted[field] = default
    
    # Remove extra fields
    for field in EXTRA_FIELDS:
        converted.pop(field, None)
    
    # Ensure numeric fields are numbers
    numeric_fields = [
        'total_capital_raised_usd', 'cash_on_hand_usd', 'monthly_burn_usd',
        'annual_revenue_run_rate', 'revenue_growth_rate_percent',
        'gross_margin_percent', 'tam_size_usd', 'sam_size_usd', 'som_size_usd'
    ]
    
    for field in numeric_fields:
        if field in converted and isinstance(converted[field], str):
            try:
                converted[field] = float(converted[field])
            except ValueError:
                converted[field] = 0
    
    return converted

def convert_backend_response(response: Dict[str, Any]) -> Dict[str, Any]:
    """Convert backend response to frontend format"""
    # Ensure all expected fields are present
    if 'interpretation' in response:
        interp = response['interpretation']
        
        # Add any missing fields frontend expects
        if 'risk_color' not in interp:
            risk_level = interp.get('risk_level', 'MEDIUM')
            color_map = {'LOW': 'green', 'MEDIUM': 'yellow', 'HIGH': 'red'}
            interp['risk_color'] = color_map.get(risk_level, 'yellow')
        
        if 'verdict_detail' not in interp:
            interp['verdict_detail'] = 'Analysis complete'
    
    return response

# Add this to api_server imports and use in predict endpoint:
# from type_converter import convert_frontend_data, convert_backend_response
# 
# In predict endpoint:
# data = convert_frontend_data(await request.json())
# result = model_manager.predict_full(data)
# return convert_backend_response(result)
'''
    
    with open('type_converter.py', 'w') as f:
        f.write(converter_code)
    
    logger.info("✓ Created type_converter.py for data format conversion")

def create_env_example():
    """Create example environment configuration"""
    logger.info("\nCreating environment configuration template...")
    
    env_content = '''# FLASH Environment Configuration

# API Server Configuration
API_PORT=8001
API_HOST=0.0.0.0
LOG_LEVEL=INFO

# Frontend Configuration
REACT_APP_API_URL=http://localhost:8001
REACT_APP_ENV=development

# Model Configuration
MODEL_BASE_PATH=models/production_v45
PATTERN_MODEL_PATH=models/pattern_v2_simple

# Feature Configuration
FEATURE_COUNT=45
ENABLE_PATTERN_SYSTEM=true
PATTERN_WEIGHT=0.25

# CORS Configuration
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:3001

# Rate Limiting
RATE_LIMIT_PER_HOUR=100
RATE_LIMIT_PER_MINUTE=30
'''
    
    with open('.env.example', 'w') as f:
        f.write(env_content)
    
    logger.info("✓ Created .env.example template")

def verify_model_paths():
    """Verify and document actual model paths"""
    logger.info("\nVerifying model paths...")
    
    model_locations = {}
    
    # Check for model files
    model_patterns = ['*.pkl', '*.cbm', '*.json']
    model_dirs = ['models', 'models/production_v45', 'models/pattern_v2_simple',
                  'models/v2_enhanced', 'models/dna_analyzer']
    
    for model_dir in model_dirs:
        dir_path = Path(model_dir)
        if dir_path.exists():
            models_found = []
            for pattern in model_patterns:
                models_found.extend(list(dir_path.glob(pattern)))
            
            if models_found:
                model_locations[model_dir] = [m.name for m in models_found[:5]]  # First 5
                logger.info(f"✓ Found {len(models_found)} models in {model_dir}")
    
    # Save model inventory
    with open('model_inventory.json', 'w') as f:
        json.dump(model_locations, f, indent=2)
    
    logger.info("✓ Created model_inventory.json")

def create_integration_test():
    """Create integration test for frontend-backend communication"""
    logger.info("\nCreating integration test...")
    
    test_code = '''#!/usr/bin/env python3
"""
Frontend-Backend Integration Test
Tests data format compatibility
"""

import requests
import json
from type_converter import convert_frontend_data, BOOLEAN_FIELDS, OPTIONAL_FIELDS

API_URL = "http://localhost:8001"

def test_data_conversion():
    """Test frontend data format conversion"""
    print("Testing data conversion...")
    
    # Simulate frontend data
    frontend_data = {
        "funding_stage": "Series A",
        "has_debt": true,  # Boolean
        "network_effects_present": false,  # Boolean
        "runway_months": null,  # Optional, should get default
        "team_cohesion_score": 4,  # Extra field, should be removed
        "annual_revenue_run_rate": "1000000",  # String number
        # ... other required fields
    }
    
    # Convert
    backend_data = convert_frontend_data(frontend_data)
    
    # Verify conversions
    assert backend_data["has_debt"] == 1
    assert backend_data["network_effects_present"] == 0
    assert backend_data["runway_months"] == 12  # Default
    assert "team_cohesion_score" not in backend_data
    assert backend_data["annual_revenue_run_rate"] == 1000000.0
    
    print("✓ Data conversion test passed")

def test_api_endpoints():
    """Test all API endpoints"""
    print("\\nTesting API endpoints...")
    
    endpoints = [
        ("GET", "/health"),
        ("GET", "/patterns"),
        ("GET", "/investor_profiles"),
        ("POST", "/predict"),
        ("POST", "/predict_simple"),
        ("POST", "/predict_advanced"),
        ("POST", "/predict_enhanced")
    ]
    
    for method, endpoint in endpoints:
        try:
            if method == "GET":
                response = requests.get(f"{API_URL}{endpoint}")
            else:
                # Need valid test data for POST
                response = requests.post(f"{API_URL}{endpoint}", json={})
            
            if response.status_code in [200, 400, 422]:  # Valid responses
                print(f"✓ {method} {endpoint}: OK")
            else:
                print(f"✗ {method} {endpoint}: {response.status_code}")
        except Exception as e:
            print(f"✗ {method} {endpoint}: Connection failed")

if __name__ == "__main__":
    print("Frontend-Backend Integration Test")
    print("=" * 50)
    test_data_conversion()
    test_api_endpoints()
'''
    
    with open('test_integration.py', 'w') as f:
        f.write(test_code)
    
    logger.info("✓ Created test_integration.py")

def generate_fix_summary():
    """Generate summary of fixes applied"""
    summary = {
        "fixes_applied": {
            "port_configuration": "Standardized to port 8001",
            "endpoint_mappings": "Created aliases for missing endpoints",
            "type_conversion": "Added boolean and optional field handling",
            "environment_config": "Created .env.example template",
            "model_inventory": "Documented actual model locations",
            "integration_test": "Created test for data compatibility"
        },
        "files_created": [
            "endpoint_mappings.py",
            "type_converter.py",
            ".env.example",
            "model_inventory.json",
            "test_integration.py"
        ],
        "manual_steps_required": [
            "Add endpoint mappings to api_server_working.py",
            "Import and use type_converter in API endpoints",
            "Update frontend to handle boolean conversions",
            "Run integration tests to verify fixes"
        ]
    }
    
    with open('mismatch_fixes_summary.json', 'w') as f:
        json.dump(summary, f, indent=2)
    
    logger.info("\n✓ Created mismatch_fixes_summary.json")

def main():
    """Apply all critical fixes"""
    logger.info("="*60)
    logger.info("Fixing Critical Mismatches in FLASH Codebase")
    logger.info("="*60)
    
    # Apply fixes
    fix_port_configuration()
    create_endpoint_mapping()
    create_type_converter()
    create_env_example()
    verify_model_paths()
    create_integration_test()
    generate_fix_summary()
    
    logger.info("\n" + "="*60)
    logger.info("Fix Summary")
    logger.info("="*60)
    
    logger.info("\nFiles created:")
    logger.info("1. endpoint_mappings.py - Missing endpoint implementations")
    logger.info("2. type_converter.py - Data format conversion utilities")
    logger.info("3. .env.example - Environment configuration template")
    logger.info("4. model_inventory.json - Actual model file locations")
    logger.info("5. test_integration.py - Integration test suite")
    
    logger.info("\nNext steps:")
    logger.info("1. Add endpoint mappings to api_server_working.py")
    logger.info("2. Import type_converter in API server")
    logger.info("3. Update predict endpoints to use convert_frontend_data()")
    logger.info("4. Run: python test_integration.py")
    logger.info("5. Update frontend if needed based on test results")
    
    logger.info("\n✅ Critical mismatch fixes completed!")

if __name__ == "__main__":
    main()