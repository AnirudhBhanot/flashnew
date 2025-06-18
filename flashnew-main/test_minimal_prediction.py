#!/usr/bin/env python3
"""
Test with minimal valid data
"""
import subprocess
import time
import requests
import json

# Start server
process = subprocess.Popen(
    ["python3", "api_server_unified.py"],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True
)
time.sleep(3)

# Minimal valid data with all 45 required fields
minimal_data = {
    # Capital (7)
    "total_capital_raised_usd": 1000000,
    "funding_stage": "seed",
    "cash_on_hand_usd": 500000,
    "monthly_burn_usd": 50000,
    "runway_months": 10,
    "burn_multiple": 2.0,
    "investor_tier_primary": "tier_2",
    
    # Advantage (8)
    "tech_differentiation_score": 3,
    "patent_count": 0,
    "has_strategic_partnerships": False,
    "switching_cost_score": 2,
    "has_network_effects": False,
    "brand_strength_score": 2,
    "scalability_score": 3,
    "regulatory_advantage_present": False,
    
    # Market (11)
    "total_addressable_market_usd": 1000000000,
    "serviceable_addressable_market_usd": 100000000,
    "serviceable_obtainable_market_usd": 10000000,
    "market_growth_rate_percent": 20,
    "sector": "saas",
    "user_growth_rate_percent": 50,
    "customers_count": 10,
    "net_promoter_score": 30,
    "payback_period_months": 12,
    "time_to_revenue_months": 6,
    "customer_acquisition_cost": 500,
    
    # People (10)
    "founders_count": 2,
    "team_size_full_time": 5,
    "years_experience_avg": 5,
    "domain_expertise_years_avg": 3,
    "prior_startup_experience_count": 0,
    "prior_successful_exits_count": 0,
    "board_advisor_experience_score": 2,
    "advisors_count": 1,
    "team_diversity_percent": 20,
    "key_person_dependency": True,
    
    # Product (9)
    "product_stage": "mvp",
    "product_retention_30d": 0.6,
    "product_retention_90d": 0.4,
    "dau_mau_ratio": 0.3,
    "annual_revenue_run_rate": 120000,
    "revenue_growth_rate_percent": 100,
    "gross_margin_percent": 60,
    "ltv_cac_ratio": 2.0,
    "net_dollar_retention_percent": 90,
    
    # Additional
    "competition_intensity": 3,
    "competitors_named_count": 5
}

print(f"Sending {len(minimal_data)} fields...")

try:
    response = requests.post(
        "http://localhost:8001/predict",
        json=minimal_data
    )
    
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print("✅ Success!")
        print(f"Probability: {result.get('success_probability', 'N/A'):.2%}")
        print(f"Verdict: {result.get('verdict')}")
    else:
        print(f"❌ Error: {response.text[:500]}")
        
except Exception as e:
    print(f"Request error: {e}")
finally:
    process.terminate()
    process.wait()