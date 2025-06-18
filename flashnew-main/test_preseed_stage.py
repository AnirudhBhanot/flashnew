import requests
import json

# Test with pre_seed stage
test_data = {
    # Capital Features
    "funding_stage": "pre_seed",  # This should be highlighted in the UI
    "total_capital_raised_usd": 100000,
    "last_round_size_usd": 100000,
    "runway_months": 12,
    "burn_multiple": 2.0,
    "gross_margin_percent": 60,
    "revenue_growth_rate_percent": 100,
    
    # Other required fields (simplified)
    "patent_count": 1,
    "proprietary_tech": 1,
    "network_effects_present": 0,
    "switching_costs_high": 0,
    "gross_margin_improvement_percent": 5,
    "technical_moat_score": 3,
    "time_to_revenue_months": 12,
    "scalability_score": 3,
    "tam_size_usd": 1000000000,
    "sam_size_usd": 100000000,
    "market_growth_rate_percent": 20,
    "market_maturity_score": 2,
    "competitive_intensity_score": 3,
    "customer_acquisition_cost_usd": 500,
    "average_contract_value_usd": 2000,
    "ltv_to_cac_ratio": 2.5,
    "payback_period_months": 12,
    "market_timing_score": 3,
    "regulatory_risk_score": 2,
    "team_size_full_time": 5,
    "technical_team_percent": 60,
    "founders_experience_score": 3,
    "advisors_score": 2,
    "board_strength_score": 2,
    "team_domain_expertise_score": 3,
    "previous_startup_experience": 0,
    "team_completeness_score": 3,
    "culture_fit_score": 3,
    "diversity_score": 3,
    "product_stage": "mvp",
    "active_users": 100,
    "mrr_usd": 5000,
    "feature_completeness_score": 2,
    "user_satisfaction_score": 3,
    "product_market_fit_score": 2,
    "innovation_score": 3,
    "time_to_market_score": 3,
    "iteration_speed_score": 4
}

# Test the API
url = "http://localhost:8001/predict_enhanced"
response = requests.post(url, json=test_data)

print("Status Code:", response.status_code)
print("\nResponse:")
result = response.json()

# Pretty print but limit the output
relevant_fields = {
    "success_probability": result.get("success_probability"),
    "verdict": result.get("verdict"),
    "funding_stage": result.get("funding_stage"),
    "pillar_scores": result.get("pillar_scores")
}

print(json.dumps(relevant_fields, indent=2))

if result.get("funding_stage") == "pre_seed":
    print("\n✅ SUCCESS: funding_stage is correctly set to 'pre_seed'")
else:
    print(f"\n❌ ERROR: funding_stage is '{result.get('funding_stage')}' but should be 'pre_seed'")