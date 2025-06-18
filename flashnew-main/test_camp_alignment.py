#!/usr/bin/env python3
"""
Test CAMP vs Success Probability alignment
"""

import requests
import json
import sys

def test_scenario(name, data):
    """Test a specific scenario"""
    print(f"\n{'='*60}")
    print(f"Testing: {name}")
    print(f"{'='*60}")
    
    # Make prediction
    response = requests.post('http://localhost:8001/predict', json=data)
    
    if response.status_code != 200:
        print(f"❌ Error: {response.status_code}")
        print(response.text)
        return
    
    result = response.json()
    
    # Extract key metrics
    success_prob = result.get('success_probability', 0)
    camp_scores = result.get('camp_analysis', {})
    
    # Calculate average CAMP score
    camp_values = [
        camp_scores.get('capital', 0),
        camp_scores.get('advantage', 0),
        camp_scores.get('market', 0),
        camp_scores.get('people', 0)
    ]
    avg_camp = sum(camp_values) / 4
    
    # Display results
    print(f"\n📊 Results:")
    print(f"Success Probability: {success_prob:.1%}")
    print(f"Average CAMP Score: {avg_camp:.1%}")
    print(f"\nCAMP Breakdown:")
    print(f"  Capital:   {camp_scores.get('capital', 0):.1%}")
    print(f"  Advantage: {camp_scores.get('advantage', 0):.1%}")
    print(f"  Market:    {camp_scores.get('market', 0):.1%}")
    print(f"  People:    {camp_scores.get('people', 0):.1%}")
    
    # Check alignment
    diff = abs(success_prob - avg_camp)
    if diff > 0.3:  # More than 30% difference
        print(f"\n⚠️  WARNING: Large misalignment detected!")
        print(f"   Difference: {diff:.1%}")
    else:
        print(f"\n✅ Good alignment (difference: {diff:.1%})")
    
    return success_prob, avg_camp

def main():
    print("🔍 Testing CAMP vs Success Probability Alignment")
    
    # Test scenarios
    scenarios = {
        "Strong startup (all high)": {
            "total_capital_raised_usd": 20000000,
            "cash_on_hand_usd": 15000000,
            "monthly_burn_usd": 500000,
            "runway_months": 30,
            "burn_multiple": 1.2,
            "investor_tier_primary": "Tier 1",
            "has_debt": False,
            "patent_count": 10,
            "network_effects_present": True,
            "has_data_moat": True,
            "regulatory_advantage_present": True,
            "tech_differentiation_score": 5,
            "switching_cost_score": 5,
            "brand_strength_score": 5,
            "scalability_score": 5,
            "sector": "SaaS",
            "tam_size_usd": 50000000000,
            "sam_size_usd": 5000000000,
            "som_size_usd": 500000000,
            "market_growth_rate_percent": 60,
            "customer_count": 1000,
            "customer_concentration_percent": 10,
            "user_growth_rate_percent": 50,
            "net_dollar_retention_percent": 140,
            "competition_intensity": 2,
            "competitors_named_count": 5,
            "founders_count": 3,
            "team_size_full_time": 80,
            "years_experience_avg": 15,
            "domain_expertise_years_avg": 12,
            "prior_startup_experience_count": 5,
            "prior_successful_exits_count": 3,
            "board_advisor_experience_score": 5,
            "advisors_count": 10,
            "strategic_partners_count": 8,
            "has_repeat_founder": True,
            "execution_risk_score": 1,
            "vertical_integration_score": 4,
            "time_to_market_advantage_years": 2,
            "partnership_leverage_score": 5,
            "company_age_months": 36,
            "cash_efficiency_score": 1.8,
            "operating_leverage_trend": 2,
            "predictive_modeling_score": 4
        },
        
        "Weak startup (all low)": {
            "total_capital_raised_usd": 500000,
            "cash_on_hand_usd": 100000,
            "monthly_burn_usd": 50000,
            "runway_months": 2,
            "burn_multiple": 8,
            "investor_tier_primary": "No Tier",
            "has_debt": True,
            "patent_count": 0,
            "network_effects_present": False,
            "has_data_moat": False,
            "regulatory_advantage_present": False,
            "tech_differentiation_score": 1,
            "switching_cost_score": 1,
            "brand_strength_score": 1,
            "scalability_score": 2,
            "sector": "Services",
            "tam_size_usd": 10000000,
            "sam_size_usd": 1000000,
            "som_size_usd": 100000,
            "market_growth_rate_percent": 5,
            "customer_count": 10,
            "customer_concentration_percent": 80,
            "user_growth_rate_percent": -10,
            "net_dollar_retention_percent": 70,
            "competition_intensity": 5,
            "competitors_named_count": 50,
            "founders_count": 1,
            "team_size_full_time": 3,
            "years_experience_avg": 2,
            "domain_expertise_years_avg": 1,
            "prior_startup_experience_count": 0,
            "prior_successful_exits_count": 0,
            "board_advisor_experience_score": 1,
            "advisors_count": 0,
            "strategic_partners_count": 0,
            "has_repeat_founder": False,
            "execution_risk_score": 5,
            "vertical_integration_score": 1,
            "time_to_market_advantage_years": -1,
            "partnership_leverage_score": 1,
            "company_age_months": 6,
            "cash_efficiency_score": 0.2,
            "operating_leverage_trend": -2,
            "predictive_modeling_score": 1
        },
        
        "Mixed signals (high CAMP, risky fundamentals)": {
            "total_capital_raised_usd": 15000000,
            "cash_on_hand_usd": 1000000,  # Low cash despite high raise
            "monthly_burn_usd": 800000,   # Very high burn
            "runway_months": 1.25,         # Critical runway
            "burn_multiple": 10,           # Terrible efficiency
            "investor_tier_primary": "Tier 1",
            "has_debt": True,
            "patent_count": 8,
            "network_effects_present": True,
            "has_data_moat": True,
            "regulatory_advantage_present": False,
            "tech_differentiation_score": 5,
            "switching_cost_score": 4,
            "brand_strength_score": 4,
            "scalability_score": 5,
            "sector": "DeepTech",
            "tam_size_usd": 20000000000,
            "sam_size_usd": 2000000000,
            "som_size_usd": 200000000,
            "market_growth_rate_percent": 45,
            "customer_count": 50,
            "customer_concentration_percent": 60,  # High concentration risk
            "user_growth_rate_percent": 15,
            "net_dollar_retention_percent": 95,   # Below 100%
            "competition_intensity": 4,
            "competitors_named_count": 20,
            "founders_count": 2,
            "team_size_full_time": 60,
            "years_experience_avg": 12,
            "domain_expertise_years_avg": 10,
            "prior_startup_experience_count": 3,
            "prior_successful_exits_count": 1,
            "board_advisor_experience_score": 4,
            "advisors_count": 6,
            "strategic_partners_count": 4,
            "has_repeat_founder": True,
            "execution_risk_score": 4,
            "vertical_integration_score": 3,
            "time_to_market_advantage_years": 0.5,
            "partnership_leverage_score": 3,
            "company_age_months": 24,
            "cash_efficiency_score": 0.3,
            "operating_leverage_trend": -1,
            "predictive_modeling_score": 3
        }
    }
    
    results = []
    for name, data in scenarios.items():
        success_prob, avg_camp = test_scenario(name, data)
        results.append((name, success_prob, avg_camp))
    
    # Summary
    print(f"\n{'='*60}")
    print("📊 ALIGNMENT SUMMARY")
    print(f"{'='*60}")
    
    for name, success, camp in results:
        diff = abs(success - camp)
        status = "✅" if diff <= 0.3 else "⚠️"
        print(f"{status} {name}")
        print(f"   Success: {success:.1%}, CAMP: {camp:.1%}, Diff: {diff:.1%}")
    
if __name__ == "__main__":
    main()