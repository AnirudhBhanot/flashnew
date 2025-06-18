import requests
import json

# Test data with all required fields
test_data = {
    # Capital Features
    "funding_stage": "series_a",
    "total_capital_raised_usd": 5000000,
    "last_round_size_usd": 3000000,
    "runway_months": 18,
    "burn_multiple": 1.5,
    "gross_margin_percent": 70,
    "revenue_growth_rate_percent": 150,
    
    # Advantage Features
    "patent_count": 3,
    "proprietary_tech": 1,
    "network_effects_present": 1,
    "switching_costs_high": 1,
    "gross_margin_improvement_percent": 5,
    "technical_moat_score": 4,
    "time_to_revenue_months": 6,
    "scalability_score": 4,
    
    # Market Features
    "tam_size_usd": 5000000000,
    "sam_size_usd": 500000000,
    "market_growth_rate_percent": 25,
    "market_maturity_score": 3,
    "competitive_intensity_score": 3,
    "customer_acquisition_cost_usd": 1000,
    "average_contract_value_usd": 10000,
    "ltv_to_cac_ratio": 3.5,
    "payback_period_months": 12,
    "market_timing_score": 4,
    "regulatory_risk_score": 2,
    
    # People Features
    "team_size_full_time": 25,
    "technical_team_percent": 60,
    "founders_experience_score": 4,
    "advisors_score": 3,
    "board_strength_score": 3,
    "team_domain_expertise_score": 4,
    "previous_startup_experience": 1,
    "team_completeness_score": 4,
    "culture_fit_score": 4,
    "diversity_score": 3,
    
    # Product Features
    "product_stage": "growth",
    "active_users": 10000,
    "mrr_usd": 100000,
    "feature_completeness_score": 4,
    "user_satisfaction_score": 4,
    "product_market_fit_score": 4,
    "innovation_score": 4,
    "time_to_market_score": 4,
    "iteration_speed_score": 4
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
        print(f"{pillar}: {score} ({score * 100:.1f}%)")
        if score > 1:
            print(f"  WARNING: {pillar} score > 1!")
        if score < 0:
            print(f"  WARNING: {pillar} score < 0!")

if 'success_probability' in result:
    prob = result['success_probability']
    print(f"\nSuccess Probability: {prob} ({prob * 100:.1f}%)")
    if prob > 1:
        print("  WARNING: Success probability > 1!")
    if prob < 0:
        print("  WARNING: Success probability < 0!")