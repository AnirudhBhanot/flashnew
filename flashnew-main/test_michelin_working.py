#!/usr/bin/env python3
"""
Test the working Michelin API endpoint
"""

import requests
import json

# Test with simplified data
test_data = {
    "startup_data": {
        "startup_name": "TechVenture AI",
        "sector": "artificial-intelligence",
        "funding_stage": "seed",
        "annual_revenue_usd": 500000,
        "runway_months": 20,
        "team_size_full_time": 12,
        "market_size_usd": 50000000000,
        "competitor_count": 8
    }
}

print("Testing Working Michelin API...")
print("=" * 80)

# Test the working endpoint
response = requests.post(
    "http://localhost:8001/api/michelin-working/analyze",
    json=test_data,
    headers={"Content-Type": "application/json"},
    timeout=30
)

print(f"Status: {response.status_code}")

if response.status_code == 200:
    print("✅ Success! Working endpoint is functional")
    data = response.json()
    
    print(f"\nCompany: {data.get('startup_name', 'Unknown')}")
    print(f"\nExecutive Briefing:")
    print("-" * 40)
    print(data.get('executive_briefing', 'No briefing')[:500].strip() + "...")
    
    if 'key_recommendations' in data:
        print(f"\nKey Recommendations:")
        print("-" * 40)
        for i, rec in enumerate(data['key_recommendations'][:3], 1):
            print(f"{i}. {rec}")
    
    # Save full response
    with open("michelin_working_response.json", "w") as f:
        json.dump(data, f, indent=2)
    print(f"\n✅ Full response saved to michelin_working_response.json")
else:
    print(f"❌ Error: {response.text}")

# Also test frontend integration
print("\n" + "=" * 80)
print("Testing frontend-compatible endpoint...")

# Use the exact same data structure as frontend
frontend_data = {
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

# Update the frontend component to use the working endpoint
print("\nTo use in frontend, update MichelinStrategicAnalysis.tsx:")
print("Change: '/api/michelin/analyze'")
print("To: '/api/michelin-working/analyze'")
print("\nThis endpoint provides immediate responses without DeepSeek dependencies.")