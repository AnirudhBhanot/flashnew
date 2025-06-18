#!/usr/bin/env python3
"""Test the complete fix - normalized CAMP scores and correct verdicts"""

import requests
import json
import time

# Wait for server to start
time.sleep(3)

# Test 1: Terrible startup (should get low scores and FAIL)
terrible_startup = {
    "funding_stage": "pre_seed",
    "total_capital_raised_usd": 10000,
    "last_round_size_usd": 10000,
    "runway_months": 2,
    "burn_multiple": 10,
    "gross_margin_percent": -20,
    "revenue_growth_rate_percent": -50,
    
    "patent_count": 0,
    "proprietary_tech": 0,
    "network_effects_present": 0,
    "switching_costs_high": 0,
    "gross_margin_improvement_percent": -10,
    "technical_moat_score": 1,
    "time_to_revenue_months": 24,
    "scalability_score": 1,
    
    "tam_size_usd": 1000000,
    "sam_size_usd": 100000,
    "market_growth_rate_percent": 0,
    "market_maturity_score": 1,
    "competitive_intensity_score": 5,
    "customer_acquisition_cost_usd": 1000,
    "average_contract_value_usd": 100,
    "ltv_to_cac_ratio": 0.1,
    "payback_period_months": 99,
    "market_timing_score": 1,
    "regulatory_risk_score": 5,
    
    "team_size_full_time": 1,
    "technical_team_percent": 0,
    "founders_experience_score": 1,
    "advisors_score": 1,
    "board_strength_score": 1,
    "team_domain_expertise_score": 1,
    "previous_startup_experience": 0,
    "team_completeness_score": 1,
    "culture_fit_score": 1,
    "diversity_score": 0,
    
    "product_stage": "idea",
    "active_users": 0,
    "mrr_usd": 0,
    "feature_completeness_score": 1,
    "user_satisfaction_score": 1,
    "product_market_fit_score": 1,
    "innovation_score": 1,
    "time_to_market_score": 1,
    "iteration_speed_score": 1
}

# Test 2: Excellent startup (should get high scores and PASS)
excellent_startup = {
    "funding_stage": "series_a",
    "total_capital_raised_usd": 5000000,
    "last_round_size_usd": 3000000,
    "runway_months": 24,
    "burn_multiple": 1.2,
    "gross_margin_percent": 75,
    "revenue_growth_rate_percent": 200,
    
    "patent_count": 5,
    "proprietary_tech": 1,
    "network_effects_present": 1,
    "switching_costs_high": 1,
    "gross_margin_improvement_percent": 20,
    "technical_moat_score": 5,
    "time_to_revenue_months": 3,
    "scalability_score": 5,
    
    "tam_size_usd": 10000000000,
    "sam_size_usd": 1000000000,
    "market_growth_rate_percent": 50,
    "market_maturity_score": 4,
    "competitive_intensity_score": 2,
    "customer_acquisition_cost_usd": 100,
    "average_contract_value_usd": 10000,
    "ltv_to_cac_ratio": 4.5,
    "payback_period_months": 3,
    "market_timing_score": 5,
    "regulatory_risk_score": 1,
    
    "team_size_full_time": 25,
    "technical_team_percent": 80,
    "founders_experience_score": 5,
    "advisors_score": 5,
    "board_strength_score": 5,
    "team_domain_expertise_score": 5,
    "previous_startup_experience": 1,
    "team_completeness_score": 5,
    "culture_fit_score": 5,
    "diversity_score": 4,
    
    "product_stage": "growth",
    "active_users": 50000,
    "mrr_usd": 500000,
    "feature_completeness_score": 5,
    "user_satisfaction_score": 5,
    "product_market_fit_score": 5,
    "innovation_score": 5,
    "time_to_market_score": 5,
    "iteration_speed_score": 5
}

# Test 3: Borderline startup (around 50%)
borderline_startup = {
    "funding_stage": "seed",
    "total_capital_raised_usd": 500000,
    "last_round_size_usd": 500000,
    "runway_months": 12,
    "burn_multiple": 2.5,
    "gross_margin_percent": 50,
    "revenue_growth_rate_percent": 100,
    
    "patent_count": 1,
    "proprietary_tech": 1,
    "network_effects_present": 0,
    "switching_costs_high": 0,
    "gross_margin_improvement_percent": 10,
    "technical_moat_score": 3,
    "time_to_revenue_months": 6,
    "scalability_score": 3,
    
    "tam_size_usd": 500000000,
    "sam_size_usd": 50000000,
    "market_growth_rate_percent": 20,
    "market_maturity_score": 3,
    "competitive_intensity_score": 3,
    "customer_acquisition_cost_usd": 500,
    "average_contract_value_usd": 2000,
    "ltv_to_cac_ratio": 2.5,
    "payback_period_months": 9,
    "market_timing_score": 3,
    "regulatory_risk_score": 2,
    
    "team_size_full_time": 8,
    "technical_team_percent": 60,
    "founders_experience_score": 3,
    "advisors_score": 3,
    "board_strength_score": 3,
    "team_domain_expertise_score": 3,
    "previous_startup_experience": 0,
    "team_completeness_score": 3,
    "culture_fit_score": 3,
    "diversity_score": 3,
    
    "product_stage": "beta",
    "active_users": 1000,
    "mrr_usd": 10000,
    "feature_completeness_score": 3,
    "user_satisfaction_score": 3,
    "product_market_fit_score": 3,
    "innovation_score": 3,
    "time_to_market_score": 3,
    "iteration_speed_score": 3
}

base_url = "http://localhost:8001"

print("Testing complete fix with normalized CAMP scores...\n")

test_cases = [
    ("Terrible Startup", terrible_startup, "Should get FAIL"),
    ("Excellent Startup", excellent_startup, "Should get PASS or STRONG PASS"),
    ("Borderline Startup", borderline_startup, "Should get CONDITIONAL PASS or FAIL")
]

for name, data, expected in test_cases:
    print(f"\n{'='*60}")
    print(f"Testing: {name} - {expected}")
    print('='*60)
    
    response = requests.post(f"{base_url}/predict_enhanced", json=data)
    if response.ok:
        result = response.json()
        
        print(f"\nCAMP Scores:")
        for pillar, score in result['pillar_scores'].items():
            print(f"  {pillar.capitalize()}: {score:.1%}")
        
        print(f"\nSuccess Probability: {result['success_probability']:.1%}")
        print(f"Verdict: {result['verdict']}")
        
        # Check if verdict matches probability
        prob = result['success_probability']
        expected_verdict = "FAIL" if prob < 0.5 else ("CONDITIONAL PASS" if prob < 0.7 else "PASS")
        
        if result['verdict'] == expected_verdict:
            print("✅ Verdict matches probability threshold!")
        else:
            print(f"❌ Verdict mismatch: Expected {expected_verdict} based on {prob:.1%}")
    else:
        print(f"Error: {response.text}")

print("\n\n✅ Summary:")
print("- CAMP scores should now be properly normalized (0-100%)")
print("- Terrible startups should get low scores and FAIL")
print("- Excellent startups should get high scores and PASS")
print("- Verdicts should match probability thresholds")
print("- Pre-seed with 49.3% should now correctly show FAIL")