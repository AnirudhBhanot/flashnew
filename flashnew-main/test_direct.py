#!/usr/bin/env python3
"""
Direct test of API with minimal data
"""

import requests
import json
import time

# Wait for server
time.sleep(5)

# Minimal frontend data
data = {
    "startup_name": "Test Corp",
    "funding_stage": "Series A",
    "total_capital_raised_usd": 5000000,
    "technology_score": 85,  # This should be converted by type converter
    "scalability_score": 4,
    "team_size": 25
}

print("Testing API with minimal data:")
print(json.dumps(data, indent=2))

try:
    response = requests.post("http://localhost:8001/predict", json=data)
    print(f"\nStatus: {response.status_code}")
    
    if response.status_code == 200:
        print("✅ Success!")
        result = response.json()
        print(f"Probability: {result.get('success_probability', 0):.1%}")
    else:
        print("❌ Failed")
        print("Response:", response.text[:500])
        
except Exception as e:
    print(f"Error: {e}")