#!/usr/bin/env python3
"""Test if the model returns varied predictions or hardcoded results"""
import requests
import json

# Valid test data based on the API schema
test_data_1 = {
    "funding_stage": "series_a",
    "total_capital_raised_usd": 15000000,
    "cash_on_hand_usd": 8000000,
    "monthly_burn_usd": 400000,
    "annual_revenue_run_rate": 3000000,
    "revenue_growth_rate_percent": 150,
    "gross_margin_percent": 75,
    "ltv_cac_ratio": 3.5,
    "investor_tier_primary": "tier_1",
    "has_debt": False,
    "patent_count": 3,
    "network_effects_present": True,
    "has_data_moat": True,
    "regulatory_advantage_present": False,
    "tech_differentiation_score": 4.2,
    "switching_cost_score": 3.8,
    "brand_strength_score": 3.5,
    "scalability_score": 4.5,
    "product_stage": "growth",  # Fixed from "GA"
    "product_retention_30d": 0.85,
    "product_retention_90d": 0.75,
    "sector": "SaaS",
    "tam_size_usd": 50000000000,
    "sam_size_usd": 5000000000,
    "som_size_usd": 500000000,
    "market_growth_rate_percent": 25,
    "customer_count": 150,
    "customer_concentration_percent": 15,
    "user_growth_rate_percent": 20,
    "net_dollar_retention_percent": 125,
    "competition_intensity": 3,  # Fixed from "moderate"
    "competitors_named_count": 5,
    "dau_mau_ratio": 0.4,
    "founders_count": 3,
    "team_size_full_time": 45,
    "years_experience_avg": 12,
    "domain_expertise_years_avg": 8,
    "prior_startup_experience_count": 2,
    "prior_successful_exits_count": 1,
    "board_advisor_experience_score": 4,
    "advisors_count": 6,
    "team_diversity_percent": 40,
    "key_person_dependency": False  # Fixed from 2
}

# Create variations to test if model responds differently
test_data_2 = test_data_1.copy()
test_data_2.update({
    "funding_stage": "seed",
    "total_capital_raised_usd": 2000000,
    "cash_on_hand_usd": 1500000,
    "monthly_burn_usd": 100000,
    "annual_revenue_run_rate": 500000,
    "revenue_growth_rate_percent": 300,
    "customer_count": 20,
    "product_retention_30d": 0.65,
    "product_retention_90d": 0.45,
    "scalability_score": 3.0
})

test_data_3 = test_data_1.copy()
test_data_3.update({
    "funding_stage": "series_b",
    "total_capital_raised_usd": 50000000,
    "cash_on_hand_usd": 25000000,
    "monthly_burn_usd": 1000000,
    "annual_revenue_run_rate": 15000000,
    "revenue_growth_rate_percent": 80,
    "customer_count": 1000,
    "product_retention_30d": 0.90,
    "product_retention_90d": 0.85,
    "scalability_score": 5.0,
    "tech_differentiation_score": 5.0
})

# Test with poor metrics
test_data_4 = test_data_1.copy()
test_data_4.update({
    "funding_stage": "seed",
    "total_capital_raised_usd": 500000,
    "cash_on_hand_usd": 100000,
    "monthly_burn_usd": 50000,
    "annual_revenue_run_rate": 0,
    "revenue_growth_rate_percent": 0,
    "customer_count": 5,
    "product_retention_30d": 0.20,
    "product_retention_90d": 0.10,
    "scalability_score": 1.5,
    "tech_differentiation_score": 1.5,
    "founders_count": 1,
    "key_person_dependency": True
})

def test_predictions():
    """Test if predictions vary"""
    api_url = "http://localhost:8001/predict"
    
    test_cases = [
        ("High-growth Series A", test_data_1),
        ("Early-stage Seed", test_data_2),
        ("Mature Series B", test_data_3),
        ("Struggling Startup", test_data_4)
    ]
    
    results = []
    
    print("Testing API predictions with different startup profiles...\n")
    
    for name, data in test_cases:
        try:
            response = requests.post(api_url, json=data)
            
            if response.status_code == 200:
                result = response.json()
                prob = result['success_probability']
                
                print(f"{name}:")
                print(f"  Success Probability: {prob:.2%}")
                print(f"  Verdict: {result.get('verdict', 'N/A')}")
                print(f"  Risk Level: {result.get('risk_level', 'N/A')}")
                
                # Show pillar scores to see if they vary
                pillar_scores = result.get('pillar_scores', {})
                if pillar_scores:
                    print("  Pillar Scores:")
                    for pillar, score in pillar_scores.items():
                        print(f"    {pillar}: {score:.3f}")
                print()
                
                results.append(prob)
            else:
                print(f"Error for {name}: {response.status_code}")
                print(response.text[:500])
                print()
        except Exception as e:
            print(f"Exception for {name}: {e}")
    
    # Analyze results
    if results:
        unique_probs = len(set(results))
        print(f"\nUnique probability values: {unique_probs}/{len(results)}")
        
        if unique_probs == 1:
            print("⚠️  WARNING: All predictions returned the same probability!")
            print(f"All returned: {results[0]:.2%}")
            print("The model might be returning hardcoded values.")
        else:
            print("✅ Model appears to be working correctly - predictions vary with input.")
            print(f"Probability range: {min(results):.2%} - {max(results):.2%}")
            print(f"Standard deviation: {(max(results) - min(results)):.2%}")
            
            # Check if differences are meaningful
            if max(results) - min(results) < 0.1:
                print("\n⚠️  Warning: Probability range is very narrow (<10%)")
                print("Model might not be differentiating well between inputs")

if __name__ == "__main__":
    test_predictions()