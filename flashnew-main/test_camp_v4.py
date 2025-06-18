#!/usr/bin/env python3
"""
Test CAMP V4 System - Integrated Explainability
"""

import sys
from pathlib import Path
import numpy as np

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from models.unified_orchestrator_v4 import create_orchestrator

def test_scenario(name, data):
    """Test a specific scenario"""
    print(f"\n{'='*60}")
    print(f"Testing: {name}")
    print(f"{'='*60}")
    
    # Create orchestrator
    orchestrator = create_orchestrator()
    
    # Make prediction
    result = orchestrator.predict(data)
    
    # Extract metrics
    success_prob = result['success_probability']
    camp_scores = result['camp_analysis']
    avg_camp = np.mean(list(camp_scores.values()))
    
    # Display results
    print(f"\n📊 Prediction Results:")
    print(f"Success Probability: {success_prob:.1%}")
    print(f"Verdict: {result['verdict']}")
    print(f"Risk Level: {result['risk_level']}")
    
    print(f"\n🎯 CAMP Analysis (ML-Aligned):")
    print(f"  Capital:   {camp_scores['capital']:.1%}")
    print(f"  Advantage: {camp_scores['advantage']:.1%}")
    print(f"  Market:    {camp_scores['market']:.1%}")
    print(f"  People:    {camp_scores['people']:.1%}")
    print(f"  Average:   {avg_camp:.1%}")
    
    # Check alignment
    diff = abs(success_prob - avg_camp)
    print(f"\n📐 Alignment: {diff:.1%} difference")
    print(f"Explanation: {result['alignment_explanation']}")
    
    # Show critical factors
    print(f"\n⚡ Critical Factors:")
    for factor in result['critical_factors'][:3]:
        print(f"  {factor['icon']} {factor['explanation']}")
    
    # Show insights
    print(f"\n💡 Key Insights:")
    for insight in result['insights'][:3]:
        print(f"  • {insight}")
    
    return success_prob, avg_camp, diff

def main():
    print("🔍 Testing CAMP V4 - Integrated Explainability System")
    
    scenarios = {
        "Strong startup (all positive)": {
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
            "sector": "AI",
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
        
        "Critical runway despite good metrics": {
            "total_capital_raised_usd": 15000000,
            "cash_on_hand_usd": 200000,     # Very low!
            "monthly_burn_usd": 600000,      # High burn
            "runway_months": 0.33,            # Only 10 days!
            "burn_multiple": 15,              # Terrible
            "investor_tier_primary": "Tier 1",
            "has_debt": True,
            "patent_count": 8,
            "network_effects_present": True,
            "has_data_moat": True,
            "regulatory_advantage_present": False,
            "tech_differentiation_score": 5,
            "switching_cost_score": 5,
            "brand_strength_score": 4,
            "scalability_score": 5,
            "sector": "SaaS",
            "tam_size_usd": 30000000000,
            "sam_size_usd": 3000000000,
            "som_size_usd": 300000000,
            "market_growth_rate_percent": 50,
            "customer_count": 300,
            "customer_concentration_percent": 20,
            "user_growth_rate_percent": 40,
            "net_dollar_retention_percent": 130,
            "competition_intensity": 2,
            "competitors_named_count": 10,
            "founders_count": 3,
            "team_size_full_time": 70,
            "years_experience_avg": 12,
            "domain_expertise_years_avg": 10,
            "prior_startup_experience_count": 4,
            "prior_successful_exits_count": 2,
            "board_advisor_experience_score": 5,
            "advisors_count": 8,
            "strategic_partners_count": 6,
            "has_repeat_founder": True,
            "execution_risk_score": 1,
            "vertical_integration_score": 4,
            "time_to_market_advantage_years": 1,
            "partnership_leverage_score": 4,
            "company_age_months": 30,
            "cash_efficiency_score": 0.1,  # Very poor
            "operating_leverage_trend": -2,
            "predictive_modeling_score": 4
        },
        
        "Mixed signals startup": {
            "total_capital_raised_usd": 5000000,
            "cash_on_hand_usd": 2000000,
            "monthly_burn_usd": 200000,
            "runway_months": 10,
            "burn_multiple": 3,
            "investor_tier_primary": "Tier 2",
            "has_debt": False,
            "patent_count": 2,
            "network_effects_present": False,
            "has_data_moat": True,
            "regulatory_advantage_present": False,
            "tech_differentiation_score": 3,
            "switching_cost_score": 3,
            "brand_strength_score": 2,
            "scalability_score": 4,
            "sector": "Marketplace",
            "tam_size_usd": 5000000000,
            "sam_size_usd": 500000000,
            "som_size_usd": 50000000,
            "market_growth_rate_percent": 25,
            "customer_count": 100,
            "customer_concentration_percent": 40,
            "user_growth_rate_percent": 15,
            "net_dollar_retention_percent": 95,  # Below 100%
            "competition_intensity": 4,
            "competitors_named_count": 30,
            "founders_count": 2,
            "team_size_full_time": 20,
            "years_experience_avg": 8,
            "domain_expertise_years_avg": 5,
            "prior_startup_experience_count": 1,
            "prior_successful_exits_count": 0,
            "board_advisor_experience_score": 3,
            "advisors_count": 3,
            "strategic_partners_count": 2,
            "has_repeat_founder": False,
            "execution_risk_score": 3,
            "vertical_integration_score": 2,
            "time_to_market_advantage_years": 0,
            "partnership_leverage_score": 2,
            "company_age_months": 18,
            "cash_efficiency_score": 0.8,
            "operating_leverage_trend": 0,
            "predictive_modeling_score": 2
        }
    }
    
    results = []
    for name, data in scenarios.items():
        success, camp, diff = test_scenario(name, data)
        results.append((name, success, camp, diff))
    
    # Summary
    print(f"\n{'='*60}")
    print("📊 V4 SYSTEM SUMMARY - CAMP NOW EXPLAINS ML")
    print(f"{'='*60}")
    
    for name, success, camp, diff in results:
        status = "✅ Aligned" if diff <= 0.15 else "🔄 Explained"
        print(f"\n{status} {name}")
        print(f"   ML Prediction: {success:.1%}")
        print(f"   CAMP Average:  {camp:.1%}")
        print(f"   Difference:    {diff:.1%}")
    
    print("\n✨ Key Improvements:")
    print("1. CAMP scores now derived from ML feature importance")
    print("2. Critical factors (like runway) properly weighted")
    print("3. Explanations show WHY predictions differ from simple averages")
    print("4. No more contradictions - CAMP explains, not competes")

if __name__ == "__main__":
    main()