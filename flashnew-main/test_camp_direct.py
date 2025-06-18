#!/usr/bin/env python3
"""
Test CAMP vs Success Probability alignment directly
"""

import sys
import numpy as np
import pandas as pd
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from models.unified_orchestrator_v3_fixed import create_orchestrator

def test_scenario(name, data):
    """Test a specific scenario"""
    print(f"\n{'='*60}")
    print(f"Testing: {name}")
    print(f"{'='*60}")
    
    # Create orchestrator
    orchestrator = create_orchestrator()
    
    # Make prediction
    result = orchestrator.predict(data)
    
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
    print(f"Verdict: {result.get('verdict', 'N/A')}")
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
        
        # Show model predictions
        print(f"\nModel Predictions:")
        for model, pred in result.get('model_predictions', {}).items():
            print(f"  {model}: {pred:.1%}")
    else:
        print(f"\n✅ Good alignment (difference: {diff:.1%})")
    
    return success_prob, avg_camp, result

def main():
    print("🔍 Testing CAMP vs Success Probability Alignment (Direct)")
    
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
        
        "High CAMP but critical runway": {
            "total_capital_raised_usd": 15000000,
            "cash_on_hand_usd": 500000,    # Very low cash
            "monthly_burn_usd": 600000,     # High burn
            "runway_months": 0.8,            # Less than 1 month!
            "burn_multiple": 12,             # Terrible efficiency
            "investor_tier_primary": "Tier 1",
            "has_debt": True,
            "patent_count": 8,
            "network_effects_present": True,
            "has_data_moat": True,
            "regulatory_advantage_present": True,
            "tech_differentiation_score": 5,
            "switching_cost_score": 5,
            "brand_strength_score": 5,
            "scalability_score": 5,
            "sector": "AI",
            "tam_size_usd": 30000000000,
            "sam_size_usd": 3000000000,
            "som_size_usd": 300000000,
            "market_growth_rate_percent": 55,
            "customer_count": 200,
            "customer_concentration_percent": 15,
            "user_growth_rate_percent": 40,
            "net_dollar_retention_percent": 130,
            "competition_intensity": 2,
            "competitors_named_count": 8,
            "founders_count": 3,
            "team_size_full_time": 70,
            "years_experience_avg": 14,
            "domain_expertise_years_avg": 11,
            "prior_startup_experience_count": 4,
            "prior_successful_exits_count": 2,
            "board_advisor_experience_score": 5,
            "advisors_count": 8,
            "strategic_partners_count": 6,
            "has_repeat_founder": True,
            "execution_risk_score": 1,
            "vertical_integration_score": 4,
            "time_to_market_advantage_years": 1.5,
            "partnership_leverage_score": 5,
            "company_age_months": 30,
            "cash_efficiency_score": 0.2,  # Very poor efficiency
            "operating_leverage_trend": -2,
            "predictive_modeling_score": 5
        }
    }
    
    results = []
    for name, data in scenarios.items():
        success_prob, avg_camp, full_result = test_scenario(name, data)
        results.append((name, success_prob, avg_camp))
    
    # Summary
    print(f"\n{'='*60}")
    print("📊 ALIGNMENT SUMMARY")
    print(f"{'='*60}")
    
    for name, success, camp in results:
        diff = abs(success - camp)
        status = "✅" if diff <= 0.3 else "⚠️"
        print(f"\n{status} {name}")
        print(f"   Success: {success:.1%}, CAMP: {camp:.1%}, Diff: {diff:.1%}")
    
    print("\n📝 Key Findings:")
    print("- CAMP scores are calculated as simple averages of normalized features")
    print("- Success probability comes from ML models trained on real patterns")
    print("- Misalignment is expected when critical factors (like runway) override high scores")
    print("- The ML models capture non-linear relationships that CAMP averages miss")

if __name__ == "__main__":
    main()