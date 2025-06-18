#!/usr/bin/env python3
import requests
import json

# Test with minimal data first
minimal_data = {
    "startup_data": {
        "startup_name": "TestStartup",
        "sector": "technology",
        "funding_stage": "seed",
        "total_capital_raised_usd": 1000000,
        "cash_on_hand_usd": 800000,
        "monthly_burn_usd": 50000,
        "runway_months": 16,
        "team_size_full_time": 5,
        "market_size_usd": 10000000000,
        "market_growth_rate_annual": 25,
        "competitor_count": 150,
        "market_share_percentage": 0.1,
        "customer_acquisition_cost_usd": 1000,
        "lifetime_value_usd": 10000,
        "monthly_active_users": 100000,
        "product_stage": "beta",
        "proprietary_tech": False,
        "patents_filed": 0,
        "founders_industry_experience_years": 10,
        "b2b_or_b2c": "b2b",
        "burn_rate_usd": 50000,
        "investor_tier_primary": "tier_2",
        "customer_count": 0  # Add this missing field
    }
}

# Try calling the endpoint
url = "http://localhost:8001/api/michelin/analyze/phase1"
print("Testing with minimal data...")
print(json.dumps(minimal_data, indent=2))

response = requests.post(url, json=minimal_data)
print(f"\nStatus Code: {response.status_code}")
if response.status_code == 200:
    print("Success!")
    data = response.json()
    if 'phase1' in data and 'executive_summary' in data['phase1']:
        print(f"Executive Summary: {data['phase1']['executive_summary'][:100]}...")
else:
    print(f"Error: {response.text}")