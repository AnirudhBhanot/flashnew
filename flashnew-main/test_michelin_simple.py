#!/usr/bin/env python3
"""
Simple test for Michelin API to debug the parsing issue
"""

import requests
import json

# Test with minimal required fields
test_data = {
    "startup_data": {
        "startup_name": "Test Startup",
        "sector": "technology",
        "funding_stage": "seed",
        "total_capital_raised_usd": 1000000,
        "cash_on_hand_usd": 500000,
        "market_size_usd": 10000000000,
        "market_growth_rate_annual": 30,
        "competitor_count": 5,
        "market_share_percentage": 0.1,
        "team_size_full_time": 10,
        "customer_count": 10,
        "customer_acquisition_cost_usd": 1000,
        "lifetime_value_usd": 10000,
        "monthly_active_users": 1000,
        "proprietary_tech": True,
        "patents_filed": 1,
        "founders_industry_experience_years": 5,
        "b2b_or_b2c": "b2b",
        "burn_rate_usd": 50000,
        "monthly_burn_usd": 50000,
        "runway_months": 10,
        "product_stage": "beta",
        "investor_tier_primary": "tier_2"
    },
    "analysis_depth": "quick"  # Try quick analysis first
}

print("Testing Michelin API with minimal data...")
print("Using 'quick' analysis depth for faster response")

response = requests.post(
    "http://localhost:8001/api/michelin/analyze",
    json=test_data,
    headers={"Content-Type": "application/json"},
    timeout=60
)

print(f"\nStatus: {response.status_code}")
if response.status_code == 200:
    print("✅ Success!")
    data = response.json()
    print(f"\nStartup: {data.get('startup_name', 'Unknown')}")
    print(f"Executive Briefing Preview: {data.get('executive_briefing', '')[:200]}...")
    
    # Save full response
    with open("michelin_test_response.json", "w") as f:
        json.dump(data, f, indent=2)
    print("\nFull response saved to michelin_test_response.json")
else:
    print(f"❌ Error: {response.text}")