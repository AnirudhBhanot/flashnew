#!/usr/bin/env python3
"""Test Investment Readiness component with CAMP categories"""

import requests
import json

# Test data with varied scores to see different readiness levels
test_data = {
    "funding_stage": "seed",
    "total_capital_raised_usd": 1500000,
    "last_round_size_usd": 1500000,
    "runway_months": 12,  # Low runway to trigger warning
    "burn_multiple": 2.5,
    "gross_margin_percent": 60,
    "revenue_growth_rate_percent": 150,
    
    # Advantage - High score
    "patent_count": 3,
    "proprietary_tech": 1,
    "network_effects_present": 1,
    "switching_costs_high": 1,
    "gross_margin_improvement_percent": 15,
    "technical_moat_score": 5,
    "time_to_revenue_months": 3,
    "scalability_score": 5,
    
    # Market - Medium score
    "tam_size_usd": 5000000000,
    "sam_size_usd": 500000000,
    "market_growth_rate_percent": 25,
    "market_maturity_score": 3,
    "competitive_intensity_score": 4,
    "customer_acquisition_cost_usd": 500,
    "average_contract_value_usd": 5000,
    "ltv_to_cac_ratio": 3.5,
    "payback_period_months": 8,
    "market_timing_score": 3,
    "regulatory_risk_score": 2,
    
    # People - Low score to show incomplete items
    "team_size_full_time": 5,
    "technical_team_percent": 60,
    "founders_experience_score": 2,
    "advisors_score": 2,
    "board_strength_score": 2,
    "team_domain_expertise_score": 2,
    "previous_startup_experience": 0,
    "team_completeness_score": 2,
    "culture_fit_score": 3,
    "diversity_score": 2,
    
    # Product
    "product_stage": "mvp",
    "active_users": 1000,
    "mrr_usd": 50000,
    "feature_completeness_score": 3,
    "user_satisfaction_score": 4,
    "product_market_fit_score": 3,
    "innovation_score": 4,
    "time_to_market_score": 4,
    "iteration_speed_score": 4
}

# Test API
base_url = "http://localhost:8001"
print("Testing Investment Readiness with CAMP categories...\n")

response = requests.post(f"{base_url}/predict_enhanced", json=test_data)
if response.ok:
    result = response.json()
    print("CAMP Scores (to show in Investment Readiness):")
    print(f"- Capital: {result['pillar_scores']['capital']:.0%}")
    print(f"- Advantage: {result['pillar_scores']['advantage']:.0%}")
    print(f"- Market: {result['pillar_scores']['market']:.0%}")
    print(f"- People: {result['pillar_scores']['people']:.0%}")
    print(f"\nSuccess Probability: {result['success_probability']:.1%}")
    print(f"Verdict: {result['verdict']}")
    
    if result.get('critical_failures'):
        print(f"\nCritical Failures: {result['critical_failures']}")
    if result.get('below_threshold'):
        print(f"Below Threshold: {result['below_threshold']}")
else:
    print(f"Error: {response.text}")

print("\n✅ Investment Readiness should now show:")
print("- Items grouped by CAMP categories")
print("- Each category with its name and business subtitle")
print("- Clear visual hierarchy with category sections")