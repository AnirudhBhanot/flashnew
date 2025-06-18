#!/usr/bin/env python3
"""Test the complete system fix - normalized CAMP scores, retrained models, correct verdicts"""

import requests
import json
import time

# Wait for server
time.sleep(3)

# Test cases including the specific pre-seed case mentioned
test_cases = [
    {
        "name": "Pre-seed with 49.3% Expected",
        "data": {
            "funding_stage": "pre_seed",
            "total_capital_raised_usd": 150000,
            "last_round_size_usd": 150000,
            "runway_months": 10,
            "burn_multiple": 3,
            "gross_margin_percent": 45,
            "revenue_growth_rate_percent": 80,
            
            "patent_count": 1,
            "proprietary_tech": 0,
            "network_effects_present": 0,
            "switching_costs_high": 0,
            "gross_margin_improvement_percent": 5,
            "technical_moat_score": 2,
            "time_to_revenue_months": 9,
            "scalability_score": 3,
            
            "tam_size_usd": 500000000,
            "sam_size_usd": 50000000,
            "market_growth_rate_percent": 15,
            "market_maturity_score": 3,
            "competitive_intensity_score": 4,
            "customer_acquisition_cost_usd": 800,
            "average_contract_value_usd": 2000,
            "ltv_to_cac_ratio": 2.0,
            "payback_period_months": 12,
            "market_timing_score": 3,
            "regulatory_risk_score": 3,
            
            "team_size_full_time": 4,
            "technical_team_percent": 50,
            "founders_experience_score": 2,
            "advisors_score": 2,
            "board_strength_score": 2,
            "team_domain_expertise_score": 2,
            "previous_startup_experience": 0,
            "team_completeness_score": 2,
            "culture_fit_score": 3,
            "diversity_score": 2,
            
            "product_stage": "mvp",
            "active_users": 100,
            "mrr_usd": 2000,
            "feature_completeness_score": 2,
            "user_satisfaction_score": 3,
            "product_market_fit_score": 2,
            "innovation_score": 3,
            "time_to_market_score": 3,
            "iteration_speed_score": 3
        },
        "expected": "Should be around 49% and get FAIL"
    },
    {
        "name": "Terrible Startup",
        "data": {
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
        },
        "expected": "Should get < 30% and FAIL"
    },
    {
        "name": "Excellent Series A",
        "data": {
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
        },
        "expected": "Should get > 70% and PASS"
    }
]

base_url = "http://localhost:8001"
print("Testing complete system fix with retrained models...\n")

for test in test_cases:
    print(f"\n{'='*60}")
    print(f"Testing: {test['name']}")
    print(f"Expected: {test['expected']}")
    print('='*60)
    
    response = requests.post(f"{base_url}/predict_enhanced", json=test['data'])
    if response.ok:
        result = response.json()
        
        # Display CAMP scores
        print(f"\nCAMP Scores (normalized):")
        camp_avg = 0
        for pillar, score in result['pillar_scores'].items():
            print(f"  {pillar.capitalize()}: {score:.1%}")
            camp_avg += score
        camp_avg /= 4
        print(f"  Average: {camp_avg:.1%}")
        
        # Display prediction results
        print(f"\nSuccess Probability: {result['success_probability']:.1%}")
        print(f"Verdict: {result['verdict']}")
        
        # Check if verdict matches probability
        prob = result['success_probability']
        if prob < 0.5:
            expected_verdict = "FAIL"
        elif prob < 0.7:
            expected_verdict = "CONDITIONAL PASS"
        elif prob < 0.8:
            expected_verdict = "PASS"
        else:
            expected_verdict = "STRONG PASS"
        
        # Verdict check
        verdict_match = "✅" if result['verdict'] == expected_verdict else "❌"
        print(f"{verdict_match} Verdict {'matches' if verdict_match == '✅' else 'should be'} {expected_verdict}")
        
        # Check if it's reasonable
        if camp_avg < 0.4 and prob > 0.5:
            print("⚠️ WARNING: Low CAMP average but high success probability!")
        elif camp_avg > 0.6 and prob < 0.5:
            print("⚠️ WARNING: High CAMP average but low success probability!")
        else:
            print("✅ Success probability aligns with CAMP scores")
            
    else:
        print(f"Error: {response.text}")

print("\n\n" + "="*60)
print("SUMMARY")
print("="*60)
print("Expected behavior:")
print("- Pre-seed with ~49% CAMP average → ~49% probability → FAIL verdict")
print("- Terrible startup → < 30% probability → FAIL verdict")
print("- Excellent startup → > 70% probability → PASS verdict")
print("\nThe system should now properly discriminate between good and bad startups!")