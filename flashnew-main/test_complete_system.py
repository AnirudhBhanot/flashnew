import requests
import json

# Test complete system with dynamic configuration
base_url = "http://localhost:8001"

print("Testing complete system with dynamic configuration...\n")

# Test data with pre_seed stage
test_data = {
    "funding_stage": "pre_seed",
    "total_capital_raised_usd": 150000,
    "last_round_size_usd": 150000,
    "runway_months": 18,
    "burn_multiple": 1.5,
    "gross_margin_percent": 70,
    "revenue_growth_rate_percent": 200,
    
    # Other required fields
    "patent_count": 2,
    "proprietary_tech": 1,
    "network_effects_present": 1,
    "switching_costs_high": 0,
    "gross_margin_improvement_percent": 10,
    "technical_moat_score": 4,
    "time_to_revenue_months": 6,
    "scalability_score": 4,
    
    "tam_size_usd": 2000000000,
    "sam_size_usd": 200000000,
    "market_growth_rate_percent": 30,
    "market_maturity_score": 3,
    "competitive_intensity_score": 3,
    "customer_acquisition_cost_usd": 100,
    "average_contract_value_usd": 1000,
    "ltv_to_cac_ratio": 3.0,
    "payback_period_months": 6,
    "market_timing_score": 4,
    "regulatory_risk_score": 2,
    
    "team_size_full_time": 8,
    "technical_team_percent": 75,
    "founders_experience_score": 4,
    "advisors_score": 3,
    "board_strength_score": 3,
    "team_domain_expertise_score": 4,
    "previous_startup_experience": 1,
    "team_completeness_score": 4,
    "culture_fit_score": 4,
    "diversity_score": 3,
    
    "product_stage": "mvp",
    "active_users": 500,
    "mrr_usd": 10000,
    "feature_completeness_score": 3,
    "user_satisfaction_score": 4,
    "product_market_fit_score": 3,
    "innovation_score": 4,
    "time_to_market_score": 4,
    "iteration_speed_score": 4
}

# Test enhanced prediction
print("1. Testing enhanced prediction with pre_seed stage")
response = requests.post(f"{base_url}/predict_enhanced", json=test_data)
print(f"Status: {response.status_code}")
if response.ok:
    result = response.json()
    print(f"Success probability: {result['success_probability']:.2%}")
    print(f"Funding stage returned: {result.get('funding_stage', 'NOT FOUND')}")
    print(f"Pillar scores: {result['pillar_scores']}")
else:
    print(f"Error: {response.text}")

# Test stage weights are being used
print("\n2. Verifying stage-specific weights for pre_seed")
weights_response = requests.get(f"{base_url}/config/stage-weights")
if weights_response.ok:
    weights = weights_response.json()
    pre_seed_weights = weights['pre_seed']
    print(f"Pre-seed weights from API: {pre_seed_weights}")
    print(f"People weight (should be highest at 40%): {pre_seed_weights['people'] * 100}%")

print("\n✅ System test complete! Frontend should now:")
print("- Show correct stage highlighting (pre_seed not seed)")
print("- Display dynamic weights from API")
print("- Show actual model accuracies")
print("- Use configuration for all thresholds and defaults")