#!/usr/bin/env python3
"""Test if the API returns real model predictions or hardcoded values"""
import requests
import json
import random

# Test with different data to see if predictions vary
test_cases = [
    {
        "name": "High-performing startup",
        "data": {
            "founding_year": 2021,
            "funding_stage": "series_a",
            "total_funding": 15000000,
            "revenue": 5000000,
            "employee_count": 45,
            "founders_count": 3,
            "revenue_growth_rate_percent": 200,
            "customer_count": 500,
            "product_retention_30d": 0.85,
            "product_retention_90d": 0.75,
            "net_dollar_retention_percent": 130,
            "customer_concentration_percent": 15,
            "industry": "saas",
            "business_model": "subscription",
            "investor_tier_primary": "tier_1",
            "product_stage": "growth",
            "market_share_percent": 5,
            "competition_intensity": 3,
            "rule_of_40": 45,
            "scalability_score": 4.5,
            "differentiation_score": 4.0,
            "tech_novelty_score": 4.2,
            "ip_portfolio_score": 3.5,
            "ceo_experience_years": 12,
            "cto_experience_years": 10,
            "team_completeness_score": 4.5,
            "advisor_quality_score": 4.0,
            "key_person_dependency": False,
            "data_maturity_score": 4.0,
            "product_complexity_score": 3.5,
            "regulatory_compliance_score": 4.5,
            "total_addressable_market": 5000000000
        }
    },
    {
        "name": "Struggling startup",
        "data": {
            "founding_year": 2022,
            "funding_stage": "seed",
            "total_funding": 500000,
            "revenue": 50000,
            "employee_count": 5,
            "founders_count": 1,
            "revenue_growth_rate_percent": 50,
            "customer_count": 20,
            "product_retention_30d": 0.40,
            "product_retention_90d": 0.25,
            "net_dollar_retention_percent": 80,
            "customer_concentration_percent": 60,
            "industry": "other",
            "business_model": "marketplace",
            "investor_tier_primary": "none",
            "product_stage": "mvp",
            "market_share_percent": 0.1,
            "competition_intensity": 5,
            "rule_of_40": -20,
            "scalability_score": 2.0,
            "differentiation_score": 2.5,
            "tech_novelty_score": 2.0,
            "ip_portfolio_score": 1.5,
            "ceo_experience_years": 2,
            "cto_experience_years": 3,
            "team_completeness_score": 2.0,
            "advisor_quality_score": 1.5,
            "key_person_dependency": True,
            "data_maturity_score": 2.0,
            "product_complexity_score": 4.5,
            "regulatory_compliance_score": 2.5,
            "total_addressable_market": 100000000
        }
    },
    {
        "name": "Medium startup",
        "data": {
            "founding_year": 2020,
            "funding_stage": "series_b",
            "total_funding": 35000000,
            "revenue": 12000000,
            "employee_count": 120,
            "founders_count": 2,
            "revenue_growth_rate_percent": 100,
            "customer_count": 1000,
            "product_retention_30d": 0.65,
            "product_retention_90d": 0.55,
            "net_dollar_retention_percent": 105,
            "customer_concentration_percent": 25,
            "industry": "fintech",
            "business_model": "saas",
            "investor_tier_primary": "tier_2",
            "product_stage": "mature",
            "market_share_percent": 2.5,
            "competition_intensity": 4,
            "rule_of_40": 25,
            "scalability_score": 3.5,
            "differentiation_score": 3.0,
            "tech_novelty_score": 3.0,
            "ip_portfolio_score": 2.5,
            "ceo_experience_years": 8,
            "cto_experience_years": 6,
            "team_completeness_score": 3.5,
            "advisor_quality_score": 3.0,
            "key_person_dependency": False,
            "data_maturity_score": 3.5,
            "product_complexity_score": 3.0,
            "regulatory_compliance_score": 4.0,
            "total_addressable_market": 2000000000
        }
    }
]

def test_predictions():
    """Test if predictions vary with different inputs"""
    api_url = "http://localhost:8001/predict"
    results = []
    
    print("Testing API predictions with different startup profiles...\n")
    
    for test_case in test_cases:
        response = requests.post(api_url, json=test_case["data"])
        
        if response.status_code == 200:
            result = response.json()
            prob = result['success_probability']
            
            print(f"{test_case['name']}:")
            print(f"  Success Probability: {prob:.2%}")
            print(f"  Verdict: {result.get('verdict', 'N/A')}")
            print(f"  Risk Level: {result.get('risk_level', 'N/A')}")
            print(f"  Pillar Scores: {json.dumps(result.get('pillar_scores', {}), indent=4)}")
            print()
            
            results.append(prob)
        else:
            print(f"Error for {test_case['name']}: {response.status_code}")
            print(response.text)
    
    # Check if all probabilities are different
    unique_probs = len(set(results))
    print(f"\nUnique probability values: {unique_probs}/{len(results)}")
    
    if unique_probs == 1:
        print("⚠️  WARNING: All predictions returned the same probability!")
        print("The model might be returning hardcoded values.")
    else:
        print("✅ Model appears to be working correctly - predictions vary with input.")
        print(f"Probability range: {min(results):.2%} - {max(results):.2%}")

if __name__ == "__main__":
    test_predictions()