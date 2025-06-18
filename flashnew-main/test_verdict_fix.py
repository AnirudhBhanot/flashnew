#!/usr/bin/env python3
"""Test the verdict fix for pre-seed with low scores"""

import requests
import json

# Test data for pre-seed with intentionally low scores
test_data = {
    "funding_stage": "pre_seed",
    "total_capital_raised_usd": 50000,
    "last_round_size_usd": 50000,
    "runway_months": 6,  # Low runway
    "burn_multiple": 5.0,  # High burn
    "gross_margin_percent": 30,  # Low margin
    "revenue_growth_rate_percent": 50,
    
    # Low scores across the board to get < 50% probability
    "patent_count": 0,
    "proprietary_tech": 0,
    "network_effects_present": 0,
    "switching_costs_high": 0,
    "gross_margin_improvement_percent": 0,
    "technical_moat_score": 1,
    "time_to_revenue_months": 24,
    "scalability_score": 2,
    
    "tam_size_usd": 100000000,  # Small TAM
    "sam_size_usd": 10000000,
    "market_growth_rate_percent": 10,
    "market_maturity_score": 2,
    "competitive_intensity_score": 5,  # High competition
    "customer_acquisition_cost_usd": 1000,
    "average_contract_value_usd": 500,  # CAC > ACV!
    "ltv_to_cac_ratio": 0.5,  # Bad ratio
    "payback_period_months": 24,
    "market_timing_score": 2,
    "regulatory_risk_score": 4,
    
    "team_size_full_time": 2,
    "technical_team_percent": 50,
    "founders_experience_score": 1,
    "advisors_score": 1,
    "board_strength_score": 1,
    "team_domain_expertise_score": 1,
    "previous_startup_experience": 0,
    "team_completeness_score": 1,
    "culture_fit_score": 2,
    "diversity_score": 1,
    
    "product_stage": "idea",
    "active_users": 0,
    "mrr_usd": 0,
    "feature_completeness_score": 1,
    "user_satisfaction_score": 1,
    "product_market_fit_score": 1,
    "innovation_score": 2,
    "time_to_market_score": 2,
    "iteration_speed_score": 2
}

# Test API
base_url = "http://localhost:8001"
print("Testing verdict fix for low-scoring pre-seed startup...\n")

response = requests.post(f"{base_url}/predict_enhanced", json=test_data)
if response.ok:
    result = response.json()
    print(f"Success Probability: {result['success_probability']:.1%}")
    print(f"Verdict: {result['verdict']}")
    print(f"\n✅ Expected: FAIL for probability < 50%")
    print(f"✅ Actual: {result['verdict']}")
    
    # Check if verdict matches expected
    prob = result['success_probability']
    expected_verdict = "FAIL" if prob < 0.5 else ("CONDITIONAL PASS" if prob < 0.7 else "PASS")
    
    if result['verdict'] == expected_verdict:
        print(f"\n🎉 VERDICT IS NOW CORRECT!")
    else:
        print(f"\n❌ VERDICT MISMATCH: Expected {expected_verdict}, got {result['verdict']}")
else:
    print(f"Error: {response.text}")