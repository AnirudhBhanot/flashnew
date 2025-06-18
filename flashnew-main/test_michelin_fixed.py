#!/usr/bin/env python3
"""
Test the fixed Michelin API endpoint
"""

import requests
import json

# Test with the fixed endpoint
test_data = {
    "startup_data": {
        "startup_name": "TechVenture AI",
        "sector": "artificial-intelligence",
        "funding_stage": "seed",
        "total_capital_raised_usd": 2000000,
        "cash_on_hand_usd": 1500000,
        "market_size_usd": 50000000000,
        "market_growth_rate_annual": 45,
        "competitor_count": 8,
        "market_share_percentage": 0.01,
        "team_size_full_time": 12,
        "customer_count": 25,
        "customer_acquisition_cost_usd": 1000,
        "lifetime_value_usd": 10000,
        "monthly_active_users": 5000,
        "proprietary_tech": True,
        "patents_filed": 2,
        "founders_industry_experience_years": 8,
        "b2b_or_b2c": "b2b",
        "burn_rate_usd": 75000,
        "monthly_burn_usd": 75000,
        "runway_months": 20,
        "product_stage": "beta",
        "investor_tier_primary": "tier_2",
        "revenue_growth_rate": 150,
        "gross_margin": 70,
        "annual_revenue_usd": 500000
    },
    "analysis_depth": "comprehensive"
}

print("Testing Fixed Michelin API...")
print("=" * 80)

# Test the fixed endpoint
response = requests.post(
    "http://localhost:8001/api/michelin-fixed/analyze",
    json=test_data,
    headers={"Content-Type": "application/json"},
    timeout=60
)

print(f"Status: {response.status_code}")

if response.status_code == 200:
    print("✅ Success! Fixed endpoint is working")
    data = response.json()
    
    print(f"\nCompany: {data.get('startup_name', 'Unknown')}")
    print(f"\nExecutive Briefing:")
    print("-" * 40)
    print(data.get('executive_briefing', 'No briefing')[:500] + "...")
    
    if 'key_recommendations' in data:
        print(f"\nKey Recommendations:")
        print("-" * 40)
        for i, rec in enumerate(data['key_recommendations'][:3], 1):
            print(f"{i}. {rec}")
    
    # Save full response
    with open("michelin_fixed_response.json", "w") as f:
        json.dump(data, f, indent=2)
    print(f"\n✅ Full response saved to michelin_fixed_response.json")
else:
    print(f"❌ Error: {response.text}")

# Also test if the original endpoint works now
print("\n" + "=" * 80)
print("Testing original endpoint with fixes...")

response2 = requests.post(
    "http://localhost:8001/api/michelin/analyze",
    json=test_data,
    headers={"Content-Type": "application/json"},
    timeout=60
)

print(f"Original endpoint status: {response2.status_code}")
if response2.status_code == 200:
    print("✅ Original endpoint is also working now!")
else:
    print("❌ Original endpoint still has issues")