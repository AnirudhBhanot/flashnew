#!/usr/bin/env python3
"""Debug why CAMP scores are so low"""

import requests
import json

# Test data from the failed test
test_data = {
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

# Make request to debug endpoint
print("Testing excellent Series A startup...")
print("Expected: High CAMP scores (60%+), High probability (70%+)\n")

response = requests.post("http://localhost:8001/predict_enhanced", json=test_data)
if response.ok:
    result = response.json()
    
    print("CAMP Scores:")
    for pillar, score in result['pillar_scores'].items():
        print(f"  {pillar}: {score:.1%}")
    
    avg_camp = sum(result['pillar_scores'].values()) / 4
    print(f"\nAverage CAMP: {avg_camp:.1%}")
    print(f"Success Probability: {result['success_probability']:.1%}")
    print(f"Verdict: {result['verdict']}")
    
    # Debug model predictions
    if 'model_predictions' in result:
        print("\nModel Predictions:")
        for model, pred in result['model_predictions'].items():
            print(f"  {model}: {pred:.1%}")
    
    # Check what's wrong
    print("\n⚠️ ISSUES:")
    print("- CAMP scores are much lower than expected")
    print("- This suggests the type converter is not mapping fields correctly")
    print("- Or the feature lists don't include all the fields we're sending")
else:
    print(f"Error: {response.text}")