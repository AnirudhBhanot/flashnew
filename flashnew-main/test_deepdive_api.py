#!/usr/bin/env python3
import requests
import json

# Test the Deep Dive Phase 1 API endpoint
url = "http://localhost:8001/api/analysis/deepdive/phase1/analysis"

# Sample request data
data = {
    "porters_five_forces": {
        "supplier_power": {
            "rating": "Medium",
            "factors": ["Limited suppliers", "High switching costs"],
            "score": 6.5
        },
        "buyer_power": {
            "rating": "High",
            "factors": ["Many alternatives", "Low switching costs"],
            "score": 7.8
        },
        "competitive_rivalry": {
            "rating": "High",
            "factors": ["Many competitors", "Similar offerings"],
            "score": 8.2
        },
        "threat_of_substitution": {
            "rating": "Medium",
            "factors": ["Some alternatives exist"],
            "score": 5.5
        },
        "threat_of_new_entry": {
            "rating": "Low",
            "factors": ["High barriers to entry", "Capital requirements"],
            "score": 3.2
        }
    },
    "internal_audit": {
        "strengths": ["Strong team", "Good technology"],
        "weaknesses": ["Limited marketing", "Small sales team"],
        "opportunities": ["Growing market", "New partnerships"],
        "threats": ["Economic uncertainty", "Regulatory changes"]
    }
}

print("Testing Deep Dive Phase 1 API endpoint...")
print(f"URL: {url}")
print(f"Request data: {json.dumps(data, indent=2)[:200]}...")
print("\n" + "="*50 + "\n")

try:
    response = requests.post(url, json=data)
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print("✓ Success! Got response:")
        print(json.dumps(result, indent=2))
        
        # Check if it's using fallback or AI
        if result.get('type') == 'fallback':
            print("\n⚠️  Note: Using fallback data (LLM call failed)")
        else:
            print("\n✓ Using AI-generated analysis")
            
    else:
        print(f"✗ Error: {response.status_code}")
        print(f"Response: {response.text}")
        
except Exception as e:
    print(f"✗ Request failed: {e}")
    print("Make sure the API server is running on port 8001")