#!/usr/bin/env python3
"""
Script to verify frontend and backend configuration alignment for FLASH
"""

import json
import requests
from typing import Dict, Any, List, Tuple

# Configuration endpoints used by frontend
FRONTEND_CONFIG_ENDPOINTS = [
    "stage-weights",
    "model-performance", 
    "company-examples",
    "success-thresholds",
    "model-weights",
    "revenue-benchmarks",
    "company-comparables",
    "display-limits"
]

# API URLs
MAIN_API_URL = "http://localhost:8001"
CONFIG_API_URL = "http://localhost:8002"

def check_endpoint(base_url: str, endpoint: str) -> Tuple[bool, Any]:
    """Check if an endpoint exists and returns data"""
    try:
        response = requests.get(f"{base_url}/config/{endpoint}", timeout=5)
        if response.status_code == 200:
            return True, response.json()
        else:
            return False, f"Status: {response.status_code}"
    except requests.exceptions.ConnectionError:
        return False, "Connection refused"
    except Exception as e:
        return False, str(e)

def compare_data_structures(frontend_expected: Dict, backend_actual: Dict) -> List[str]:
    """Compare data structures and find mismatches"""
    issues = []
    
    # Check for missing keys
    frontend_keys = set(frontend_expected.keys())
    backend_keys = set(backend_actual.keys()) if isinstance(backend_actual, dict) else set()
    
    missing_in_backend = frontend_keys - backend_keys
    extra_in_backend = backend_keys - frontend_keys
    
    if missing_in_backend:
        issues.append(f"Missing keys in backend: {missing_in_backend}")
    if extra_in_backend:
        issues.append(f"Extra keys in backend: {extra_in_backend}")
    
    # Check data types
    for key in frontend_keys & backend_keys:
        if type(frontend_expected[key]) != type(backend_actual[key]):
            issues.append(f"Type mismatch for '{key}': frontend expects {type(frontend_expected[key])}, backend returns {type(backend_actual[key])}")
    
    return issues

def main():
    print("=== FLASH Frontend-Backend Configuration Alignment Check ===\n")
    
    # Check which API is providing config endpoints
    print("1. Checking Main API (port 8001):")
    main_api_working = False
    for endpoint in FRONTEND_CONFIG_ENDPOINTS:
        success, data = check_endpoint(MAIN_API_URL, endpoint)
        status = "✅" if success else "❌"
        print(f"   {status} /config/{endpoint}: {data if not success else 'OK'}")
        if success:
            main_api_working = True
    
    print("\n2. Checking Config API (port 8002):")
    config_api_working = False
    for endpoint in FRONTEND_CONFIG_ENDPOINTS:
        success, data = check_endpoint(CONFIG_API_URL, endpoint)
        status = "✅" if success else "❌"
        print(f"   {status} /config/{endpoint}: {data if not success else 'OK'}")
        if success:
            config_api_working = True
    
    # Determine which API the frontend should use
    print("\n3. Frontend Configuration:")
    print(f"   - Frontend expects config API at: {CONFIG_API_URL}")
    print(f"   - Frontend expects main API at: {MAIN_API_URL}")
    
    if config_api_working:
        print(f"   - Config API (port 8002) is {'✅ AVAILABLE' if config_api_working else '❌ NOT AVAILABLE'}")
    if main_api_working:
        print(f"   - Main API config endpoints (port 8001) are {'✅ AVAILABLE' if main_api_working else '❌ NOT AVAILABLE'}")
    
    # Check data format compatibility
    print("\n4. Data Format Compatibility Check:")
    
    # Expected data structures from frontend constants
    expected_structures = {
        "stage-weights": {
            "pre_seed": {"people": 0.40, "advantage": 0.30, "market": 0.20, "capital": 0.10}
        },
        "model-performance": {
            "dna_analyzer": {"accuracy": 0.7674, "name": "DNA Pattern Analyzer"},
            "overall_accuracy": 0.7717,
            "dataset_size": "100k"
        },
        "success-thresholds": {
            "STRONG_INVESTMENT": {
                "minProbability": 0.75,
                "text": "STRONG INVESTMENT OPPORTUNITY",
                "emoji": "🚀",
                "className": "strong-yes"
            }
        }
    }
    
    # Check actual vs expected for available endpoints
    base_url = CONFIG_API_URL if config_api_working else (MAIN_API_URL if main_api_working else None)
    
    if base_url:
        for endpoint, expected in expected_structures.items():
            success, actual = check_endpoint(base_url, endpoint)
            if success:
                issues = compare_data_structures(expected, actual)
                if issues:
                    print(f"\n   ⚠️  {endpoint}:")
                    for issue in issues:
                        print(f"      - {issue}")
                else:
                    print(f"\n   ✅ {endpoint}: Structure matches")
    else:
        print("   ❌ No API available to check data formats")
    
    # Recommendations
    print("\n5. Recommendations:")
    if not config_api_working and not main_api_working:
        print("   ❌ Neither API is providing config endpoints!")
        print("   - Start the config API server: python config_api_server.py")
        print("   - OR ensure main API includes config endpoints")
    elif config_api_working and not main_api_working:
        print("   ✅ Config API is running correctly on port 8002")
        print("   - Frontend will use the dedicated config service")
    elif main_api_working and not config_api_working:
        print("   ⚠️  Main API provides config endpoints but frontend expects port 8002")
        print("   - Update frontend to use main API for config")
        print("   - OR start the dedicated config API server")
    else:
        print("   ⚠️  Both APIs provide config endpoints - potential confusion")
        print("   - Ensure frontend uses only one source")
        print("   - Consider disabling config endpoints in main API")
    
    print("\n6. Environment Variables Check:")
    print("   - Frontend should set REACT_APP_CONFIG_API_URL=http://localhost:8002")
    print("   - Frontend should set REACT_APP_API_URL=http://localhost:8001")
    print("   - Or update configService.ts to use main API if config API not needed")

if __name__ == "__main__":
    main()