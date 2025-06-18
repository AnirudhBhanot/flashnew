#!/usr/bin/env python3
"""
Test API response format
"""

import requests
import json
import time

# Wait for server
time.sleep(5)

# Simple test data
data = {
    "startup_name": "Test Corp",
    "funding_stage": "Series A",
    "total_capital_raised_usd": 5000000,
    "team_size": 25,
    "annual_revenue_run_rate": 1000000,
    "market_size_billions": 10,
    "technology_score": 80,
    "scalability_score": 4
}

print("Testing API response format...")

try:
    response = requests.post("http://localhost:8001/predict", json=data)
    
    if response.status_code == 200:
        result = response.json()
        print("\n✅ API Response:")
        print(json.dumps(result, indent=2))
        
        # Check what fields are present
        print("\n📋 Fields in response:")
        for key in result.keys():
            print(f"  - {key}: {type(result[key]).__name__}")
            
        # Check specifically for pillar_scores
        if 'pillar_scores' in result:
            print("\n✅ pillar_scores found:")
            print(json.dumps(result['pillar_scores'], indent=2))
        else:
            print("\n❌ pillar_scores NOT found")
            
        if 'camp_scores' in result:
            print("\n📊 camp_scores found:")
            print(json.dumps(result['camp_scores'], indent=2))
            
    else:
        print(f"\n❌ Error: {response.status_code}")
        print(response.text[:500])
        
except Exception as e:
    print(f"\n❌ Error: {e}")