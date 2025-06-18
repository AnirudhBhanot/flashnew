#!/usr/bin/env python3
"""
Test competition_intensity field conversion
"""

import requests
import json
import time

# Wait for server
time.sleep(5)

# Test data with competition_intensity as number (as frontend sends)
test_data = {
    "startup_name": "Test Corp",
    "funding_stage": "Series A", 
    "total_capital_raised_usd": 5000000,
    "team_size": 25,
    "competition_intensity": 3,  # Frontend sends as number
    "market_competition_level": "medium",
    "annual_revenue_run_rate": 1000000
}

print("Testing competition_intensity conversion...")
print(f"Sending competition_intensity as: {test_data['competition_intensity']} (type: {type(test_data['competition_intensity']).__name__})")

try:
    # Test regular endpoint
    response = requests.post("http://localhost:8001/predict", json=test_data)
    print(f"\n/predict endpoint - Status: {response.status_code}")
    
    if response.status_code == 200:
        print("✅ Success!")
        result = response.json()
        print(f"Probability: {result.get('success_probability', 0):.1%}")
    else:
        print("❌ Failed")
        print("Error:", response.text[:200])
    
    # Test enhanced endpoint
    response2 = requests.post("http://localhost:8001/predict_enhanced", json=test_data)
    print(f"\n/predict_enhanced endpoint - Status: {response2.status_code}")
    
    if response2.status_code == 200:
        print("✅ Success!")
    else:
        print("❌ Failed")
        if response2.status_code == 422:
            error = response2.json()
            if "detail" in error and isinstance(error["detail"], list):
                for err in error["detail"][:3]:
                    print(f"  - {err.get('loc', [])[-1]}: {err.get('msg')}")
        
except Exception as e:
    print(f"\nError: {e}")