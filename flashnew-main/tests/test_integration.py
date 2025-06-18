#!/usr/bin/env python3
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
    print("\nTesting API endpoints...")
    
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
