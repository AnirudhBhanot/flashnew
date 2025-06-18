import requests
import json

# Test with different data values
test_data = {
    # Capital Features - Lower values
    "funding_stage": "pre_seed",
    "total_capital_raised_usd": 500000,
    "last_round_size_usd": 500000,
    "runway_months": 6,
    "burn_multiple": 3.0,
    "gross_margin_percent": 40,
    "revenue_growth_rate_percent": 50,
    
    # Advantage Features - Higher values
    "patent_count": 10,
    "proprietary_tech": 1,
    "network_effects_present": 1,
    "switching_costs_high": 1,
    "gross_margin_improvement_percent": 10,
    "technical_moat_score": 5,
    "time_to_revenue_months": 3,
    "scalability_score": 5,
    
    # Market Features
    "tam_size_usd": 10000000000,
    "sam_size_usd": 1000000000,
    "market_growth_rate_percent": 40,
    "market_maturity_score": 4,
    "competitive_intensity_score": 2,
    "customer_acquisition_cost_usd": 500,
    "average_contract_value_usd": 5000,
    "ltv_to_cac_ratio": 5.0,
    "payback_period_months": 6,
    "market_timing_score": 5,
    "regulatory_risk_score": 1,
    
    # People Features
    "team_size_full_time": 50,
    "technical_team_percent": 70,
    "founders_experience_score": 5,
    "advisors_score": 5,
    "board_strength_score": 5,
    "team_domain_expertise_score": 5,
    "previous_startup_experience": 1,
    "team_completeness_score": 5,
    "culture_fit_score": 5,
    "diversity_score": 4,
    
    # Product Features
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

# Test the API
url = "http://localhost:8001/predict"
response = requests.post(url, json=test_data)

print("Status Code:", response.status_code)
print("\nResponse:")
result = response.json()
print(json.dumps(result, indent=2))

# Check score values
if 'pillar_scores' in result:
    print("\n\nPillar Scores Analysis:")
    for pillar, score in result['pillar_scores'].items():
        print(f"{pillar}: {score:.3f} ({score * 100:.1f}%)")
        if score > 1:
            print(f"  ERROR: {pillar} score > 1!")
        if score < 0:
            print(f"  ERROR: {pillar} score < 0!")

print(f"\nSuccess Probability: {result['success_probability']:.3f} ({result['success_probability'] * 100:.1f}%)")