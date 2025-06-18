#!/usr/bin/env python3
import requests
import json

# Test data
test_data = {
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
        "geographical_focus": "domestic",
        "revenue_growth_rate": -10,
        "gross_margin": 70,
        "net_promoter_score": 0,
        "technology_readiness_level": 5,
        "has_strategic_partnerships": False,
        "customer_concentration": 0,
        "annual_revenue_usd": 0,
        "customer_count": 0
    },
    "include_financial_projections": True,
    "analysis_depth": "comprehensive"
}

# Call the API
url = "http://localhost:8001/api/michelin/analyze/phase1"
response = requests.post(url, json=test_data)

print(f"Status Code: {response.status_code}")
print(f"Response Headers: {dict(response.headers)}")

if response.status_code == 200:
    data = response.json()
    print("\nResponse Structure:")
    print(json.dumps(data, indent=2))
    
    # Check executive summary
    if 'phase1' in data and 'executive_summary' in data['phase1']:
        print(f"\nExecutive Summary: {data['phase1']['executive_summary'][:100]}...")
else:
    print(f"Error: {response.text}")