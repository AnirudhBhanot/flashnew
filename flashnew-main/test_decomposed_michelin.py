#!/usr/bin/env python3
import requests
import json
import time

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
        "customer_count": 0
    },
    "include_financial_projections": True,
    "analysis_depth": "comprehensive"
}

print("Testing Decomposed Michelin Analysis...")
print("="*50)

# Test the new decomposed endpoint
url_decomposed = "http://localhost:8001/api/michelin/decomposed/analyze/phase1"
print(f"\nCalling decomposed endpoint: {url_decomposed}")

start_time = time.time()
response = requests.post(url_decomposed, json=test_data)
end_time = time.time()

print(f"Status Code: {response.status_code}")
print(f"Response Time: {end_time - start_time:.2f} seconds")

if response.status_code == 200:
    data = response.json()
    print("\n✅ Success! Response structure:")
    
    # Show executive summary
    print(f"\nExecutive Summary:")
    print(data['phase1']['executive_summary'])
    
    # Show BCG position
    print(f"\nBCG Position: {data['phase1']['bcg_matrix_analysis']['position']}")
    print(f"Strategic Implications: {data['phase1']['bcg_matrix_analysis']['strategic_implications']}")
    
    # Show Porter's Five Forces summary
    print(f"\nPorter's Five Forces:")
    for force, details in data['phase1']['porters_five_forces'].items():
        if isinstance(details, dict) and 'level' in details:
            print(f"- {force.replace('_', ' ').title()}: {details['level']}")
    
    # Show SWOT summary
    print(f"\nSWOT Analysis:")
    print(f"- Strengths: {len(data['phase1']['swot_analysis']['strengths'])} items")
    print(f"- Weaknesses: {len(data['phase1']['swot_analysis']['weaknesses'])} items")
    print(f"- Opportunities: {len(data['phase1']['swot_analysis']['opportunities'])} items")
    print(f"- Threats: {len(data['phase1']['swot_analysis']['threats'])} items")
    
    # Show a sample strength
    if data['phase1']['swot_analysis']['strengths']:
        strength = data['phase1']['swot_analysis']['strengths'][0]
        print(f"\nSample Strength: {strength['point']} - {strength['evidence']}")
    
else:
    print(f"\n❌ Error: {response.text}")

print("\n" + "="*50)
print("Now comparing with original endpoint...")
print("="*50)

# Compare with original endpoint
url_original = "http://localhost:8001/api/michelin/analyze/phase1"
print(f"\nCalling original endpoint: {url_original}")

start_time = time.time()
response2 = requests.post(url_original, json=test_data)
end_time = time.time()

print(f"Status Code: {response2.status_code}")
print(f"Response Time: {end_time - start_time:.2f} seconds")

if response2.status_code == 200:
    data2 = response2.json()
    print("\nOriginal endpoint executive summary:")
    print(data2['phase1']['executive_summary'][:200] + "...")