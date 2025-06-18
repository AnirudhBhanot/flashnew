#!/usr/bin/env python3
"""
Simple test for the predict endpoint
"""

import requests
import json

# Minimal valid data
data = {
    "total_capital_raised_usd": 5000000,
    "cash_on_hand_usd": 3000000,
    "monthly_burn_usd": 200000,
    "investor_tier_primary": "tier_1",
    "has_debt": False,
    "patent_count": 3,
    "network_effects_present": True,
    "has_data_moat": True,
    "regulatory_advantage_present": False,
    "tech_differentiation_score": 4,
    "switching_cost_score": 3,
    "brand_strength_score": 3,
    "scalability_score": 4,
    "sector": "saas",
    "tam_size_usd": 10000000000,
    "sam_size_usd": 1000000000,
    "som_size_usd": 100000000,
    "market_growth_rate_percent": 30,
    "customer_count": 100,
    "customer_concentration_percent": 20,
    "user_growth_rate_percent": 25,
    "net_dollar_retention_percent": 120,
    "competition_intensity": 3,
    "competitors_named_count": 10,
    "founders_count": 2,
    "team_size_full_time": 25,
    "years_experience_avg": 10,
    "domain_expertise_years_avg": 8,
    "prior_startup_experience_count": 2,
    "prior_successful_exits_count": 1,
    "board_advisor_experience_score": 4,
    "advisors_count": 5,
    "team_diversity_percent": 40,
    "key_person_dependency": False,
    "product_stage": "growth",
    "product_retention_30d": 0.80,
    "product_retention_90d": 0.65,
    "dau_mau_ratio": 0.5,
    "annual_revenue_run_rate": 2000000,
    "revenue_growth_rate_percent": 150,
    "gross_margin_percent": 75,
    "ltv_cac_ratio": 3.5,
    "funding_stage": "series_a"
}

print("Testing prediction endpoint...")
print(f"Sending {len(data)} fields")

response = requests.post(
    "http://localhost:8001/predict",
    json=data,
    headers={"Content-Type": "application/json"}
)

print(f"\nStatus: {response.status_code}")
if response.status_code == 200:
    result = response.json()
    print(f"Success Probability: {result.get('success_probability', 0):.1%}")
    print(f"Verdict: {result.get('verdict', 'N/A')}")
else:
    print(f"Error: {response.text}")
    
    # Try to parse error details
    try:
        error_data = response.json()
        if 'details' in error_data:
            print("\nError details:")
            for detail in error_data['details']:
                print(f"  - {detail.get('msg', 'Unknown error')}")
                print(f"    Location: {detail.get('loc', [])}")
                if 'input' in detail:
                    print(f"    Input: {detail['input']}")
    except:
        pass