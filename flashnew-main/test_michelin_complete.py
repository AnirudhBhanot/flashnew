#!/usr/bin/env python3
"""
Complete test of Michelin API structure
"""

import requests
import json
import time

# Wait for server to start
print("Waiting for server to start...")
time.sleep(5)

# Test data
test_data = {
    "startup_data": {
        "startup_name": "Test Startup",
        "sector": "saas", 
        "funding_stage": "seed",
        "total_capital_raised_usd": 1000000,
        "cash_on_hand_usd": 500000,
        "market_size_usd": 1000000000,
        "market_growth_rate_annual": 20,
        "competitor_count": 5,
        "market_share_percentage": 0.1,
        "team_size_full_time": 10
    }
}

print("Testing Michelin API complete structure...")
print("=" * 80)

try:
    response = requests.post(
        "http://localhost:8001/api/michelin/analyze",
        json=test_data,
        headers={"Content-Type": "application/json"},
        timeout=10
    )

    if response.status_code == 200:
        data = response.json()
        
        # Check SWOT strategic_priorities
        print("Checking SWOT Analysis structure:")
        swot = data["phase1"]["swot_analysis"]
        
        print(f"  - Strengths: {len(swot['strengths'])} items")
        print(f"  - Weaknesses: {len(swot['weaknesses'])} items")
        print(f"  - Opportunities: {len(swot['opportunities'])} items")
        print(f"  - Threats: {len(swot['threats'])} items")
        
        if "strategic_priorities" in swot:
            print(f"  ✅ Strategic Priorities: {len(swot['strategic_priorities'])} items")
            for i, priority in enumerate(swot['strategic_priorities'][:3]):
                print(f"     {i+1}. {priority}")
        else:
            print("  ❌ Missing strategic_priorities")
        
        # Save full response
        with open("michelin_complete_response.json", "w") as f:
            json.dump(data, f, indent=2)
        print(f"\n✅ Full response saved to michelin_complete_response.json")
        
    else:
        print(f"❌ Error: {response.status_code}")
        print(response.text)
        
except Exception as e:
    print(f"❌ Connection error: {e}")
    print("Make sure the API server is running on port 8001")