#!/usr/bin/env python3
"""
Test Phase 2 structure specifically
"""

import requests
import json
import time

# Wait for server
time.sleep(5)

test_data = {
    "startup_data": {
        "startup_name": "Test",
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

print("Testing Phase 2 structure...")
response = requests.post(
    "http://localhost:8001/api/michelin/analyze",
    json=test_data,
    headers={"Content-Type": "application/json"}
)

if response.status_code == 200:
    data = response.json()
    phase2 = data["phase2"]
    
    print("\nGrowth Scenarios:")
    for scenario in phase2["growth_scenarios"]:
        print(f"\n{scenario['name']}:")
        print(f"  - investment_required: {scenario.get('investment_required')} (type: {type(scenario.get('investment_required'))})")
        print(f"  - revenue_projection_3yr: {scenario.get('revenue_projection_3yr')} (type: {type(scenario.get('revenue_projection_3yr'))})")
        print(f"  - probability_of_success: {scenario.get('probability_of_success')} (type: {type(scenario.get('probability_of_success'))})")
        print(f"  - key_milestones: {len(scenario.get('key_milestones', []))} items")
        print(f"  - risks: {'✅' if 'risks' in scenario else '❌ MISSING'}")
        if 'risks' in scenario:
            print(f"    {scenario['risks']}")
            
    # Check expected numeric types
    print("\n\nType Validation:")
    scenario = phase2["growth_scenarios"][0]
    print(f"✅ investment_required is numeric: {isinstance(scenario.get('investment_required'), (int, float))}")
    print(f"✅ revenue_projection_3yr is numeric: {isinstance(scenario.get('revenue_projection_3yr'), (int, float))}")
    print(f"✅ probability_of_success is numeric: {isinstance(scenario.get('probability_of_success'), (int, float))}")
    print(f"✅ risks array exists: {'risks' in scenario}")
    
else:
    print(f"Error: {response.status_code}")