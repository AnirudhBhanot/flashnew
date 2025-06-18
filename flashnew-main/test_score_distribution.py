#!/usr/bin/env python3
"""
Test score distribution with various startup profiles
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.unified_orchestrator_v3_integrated import UnifiedOrchestratorV3
from feature_config import ALL_FEATURES
from camp_calculator import calculate_camp_scores
import pandas as pd
import numpy as np

# Test cases with different quality levels
test_cases = {
    "Unicorn Profile": {
        "funding_stage": "Series_C",
        "monthly_burn_usd": 500000,
        "runway_months": 36,
        "annual_revenue_run_rate": 50000000,
        "revenue_growth_rate_percent": 80,
        "gross_margin_percent": 85,
        "customer_acquisition_cost_usd": 100,
        "lifetime_value_usd": 10000,
        "ltv_cac_ratio": 100,
        "tam_size_usd": 50000000000,
        "market_growth_rate_percent": 60,
        "product_stage": "Growth",
        "team_size_full_time": 100,
        "founders_previous_experience_score": 5,
        "technical_team_percent": 40,
        "customer_churn_rate_percent": 1,
        "nps_score": 90,
        "cash_on_hand_usd": 18000000,
        "total_capital_raised_usd": 50000000,
        "investor_tier_primary": "Tier_1",
        "sector": "SaaS",
        "network_effects_present": True,
        "has_data_moat": True,
        "patent_count": 20,
        "burn_multiple": 0.12,
        "product_retention_90d": 0.95,
        "user_growth_rate_percent": 100,
        "annual_marketing_spend_usd": 5000000,
        "product_market_fit_score": 5,
        "founders_count": 3,
        "advisors_count": 10,
        "board_experience_score": 5,
        "competitive_advantage_score": 5,
    },
    "Strong Series A": {
        "funding_stage": "Series_A",
        "monthly_burn_usd": 200000,
        "runway_months": 24,
        "annual_revenue_run_rate": 6000000,
        "revenue_growth_rate_percent": 60,
        "gross_margin_percent": 80,
        "customer_acquisition_cost_usd": 200,
        "lifetime_value_usd": 5000,
        "ltv_cac_ratio": 25,
        "tam_size_usd": 10000000000,
        "market_growth_rate_percent": 50,
        "product_stage": "Growth",
        "team_size_full_time": 25,
        "founders_previous_experience_score": 4,
        "technical_team_percent": 60,
        "customer_churn_rate_percent": 2,
        "nps_score": 80,
        "cash_on_hand_usd": 4800000,
        "total_capital_raised_usd": 10000000,
        "investor_tier_primary": "Tier_1",
        "sector": "SaaS",
        "network_effects_present": True,
        "has_data_moat": True,
        "patent_count": 5,
        "burn_multiple": 0.4,
        "product_retention_90d": 0.85,
        "user_growth_rate_percent": 70,
        "annual_marketing_spend_usd": 1000000,
        "product_market_fit_score": 4,
        "founders_count": 2,
        "advisors_count": 5,
        "board_experience_score": 4,
        "competitive_advantage_score": 4,
    },
    "Average Seed": {
        "funding_stage": "Seed",
        "monthly_burn_usd": 100000,
        "runway_months": 12,
        "annual_revenue_run_rate": 600000,
        "revenue_growth_rate_percent": 30,
        "gross_margin_percent": 70,
        "customer_acquisition_cost_usd": 500,
        "lifetime_value_usd": 2000,
        "ltv_cac_ratio": 4,
        "tam_size_usd": 1000000000,
        "market_growth_rate_percent": 25,
        "product_stage": "Beta",
        "team_size_full_time": 8,
        "founders_previous_experience_score": 3,
        "technical_team_percent": 50,
        "customer_churn_rate_percent": 5,
        "nps_score": 50,
        "cash_on_hand_usd": 1200000,
        "total_capital_raised_usd": 2000000,
        "investor_tier_primary": "Tier_2",
        "sector": "SaaS",
        "network_effects_present": False,
        "has_data_moat": False,
        "patent_count": 0,
        "burn_multiple": 2,
        "product_retention_90d": 0.70,
        "user_growth_rate_percent": 30,
        "annual_marketing_spend_usd": 200000,
        "product_market_fit_score": 3,
        "founders_count": 2,
        "advisors_count": 2,
        "board_experience_score": 3,
        "competitive_advantage_score": 3,
    },
    "Struggling Startup": {
        "funding_stage": "Seed",
        "monthly_burn_usd": 150000,
        "runway_months": 6,
        "annual_revenue_run_rate": 120000,
        "revenue_growth_rate_percent": 10,
        "gross_margin_percent": 50,
        "customer_acquisition_cost_usd": 1000,
        "lifetime_value_usd": 1500,
        "ltv_cac_ratio": 1.5,
        "tam_size_usd": 100000000,
        "market_growth_rate_percent": 10,
        "product_stage": "MVP",
        "team_size_full_time": 5,
        "founders_previous_experience_score": 2,
        "technical_team_percent": 40,
        "customer_churn_rate_percent": 10,
        "nps_score": 30,
        "cash_on_hand_usd": 900000,
        "total_capital_raised_usd": 1000000,
        "investor_tier_primary": "Tier_3",
        "sector": "SaaS",
        "network_effects_present": False,
        "has_data_moat": False,
        "patent_count": 0,
        "burn_multiple": 15,
        "product_retention_90d": 0.50,
        "user_growth_rate_percent": 10,
        "annual_marketing_spend_usd": 100000,
        "product_market_fit_score": 2,
        "founders_count": 2,
        "advisors_count": 1,
        "board_experience_score": 2,
        "competitive_advantage_score": 2,
    },
    "Pre-Revenue Startup": {
        "funding_stage": "Pre_Seed",
        "monthly_burn_usd": 50000,
        "runway_months": 10,
        "annual_revenue_run_rate": 0,
        "revenue_growth_rate_percent": 0,
        "gross_margin_percent": 0,
        "customer_acquisition_cost_usd": 0,
        "lifetime_value_usd": 0,
        "ltv_cac_ratio": 0,
        "tam_size_usd": 500000000,
        "market_growth_rate_percent": 20,
        "product_stage": "Concept",
        "team_size_full_time": 3,
        "founders_previous_experience_score": 2,
        "technical_team_percent": 66,
        "customer_churn_rate_percent": 0,
        "nps_score": 0,
        "cash_on_hand_usd": 500000,
        "total_capital_raised_usd": 500000,
        "investor_tier_primary": "Tier_3",
        "sector": "SaaS",
        "network_effects_present": False,
        "has_data_moat": False,
        "patent_count": 0,
        "burn_multiple": 0,
        "product_retention_90d": 0,
        "user_growth_rate_percent": 0,
        "annual_marketing_spend_usd": 0,
        "product_market_fit_score": 1,
        "founders_count": 2,
        "advisors_count": 0,
        "board_experience_score": 1,
        "competitive_advantage_score": 1,
    }
}

def test_models():
    """Test the fixed models"""
    print("Loading orchestrator...")
    orchestrator = UnifiedOrchestratorV3()
    
    print(f"\nLoaded models: {list(orchestrator.models.keys())}")
    
    results = []
    
    for test_name, raw_data in test_cases.items():
        print(f"\n{'='*60}")
        print(f"Testing: {test_name}")
        print(f"{'='*60}")
        
        # Create DataFrame with all features
        features_dict = {k: raw_data.get(k, 0) for k in ALL_FEATURES}
        features_df = pd.DataFrame([features_dict])
        
        # Get prediction
        result = orchestrator.predict(features_df)
        
        print(f"\nOverall Success Probability: {result['success_probability']:.1%}")
        print(f"Verdict: {result['verdict']}")
        
        print("\nIndividual Model Predictions:")
        for model, pred in result['model_predictions'].items():
            print(f"  {model}: {pred:.1%}")
        
        # Calculate CAMP scores
        camp_scores = calculate_camp_scores(features_dict)
        if 'camp_scores' in camp_scores:
            camp_avg = np.mean(list(camp_scores['camp_scores'].values()))
            print(f"\nCAMP Average: {camp_avg:.1%}")
            for pillar, score in camp_scores['camp_scores'].items():
                print(f"  {pillar}: {score:.1%}")
        
        results.append({
            'profile': test_name,
            'success_prob': result['success_probability'],
            'dna': result['model_predictions'].get('dna_analyzer', 0),
            'industry': result['model_predictions'].get('industry_specific', 0),
            'temporal': result['model_predictions'].get('temporal_prediction', 0),
            'ensemble': result['model_predictions'].get('ensemble', 0),
            'camp_avg': camp_avg if 'camp_scores' in camp_scores else 0
        })
    
    # Summary
    print("\n" + "="*80)
    print("SCORE DISTRIBUTION SUMMARY")
    print("="*80)
    print(f"{'Profile':<25} {'Success':<10} {'DNA':<10} {'Industry':<10} {'Temporal':<10} {'CAMP Avg':<10}")
    print("-"*80)
    
    for r in results:
        print(f"{r['profile']:<25} {r['success_prob']:<10.1%} {r['dna']:<10.1%} {r['industry']:<10.1%} {r['temporal']:<10.1%} {r['camp_avg']:<10.1%}")
    
    # Check distribution
    probs = [r['success_prob'] for r in results]
    print(f"\nMin probability: {min(probs):.1%}")
    print(f"Max probability: {max(probs):.1%}")
    print(f"Range: {max(probs) - min(probs):.1%}")

if __name__ == "__main__":
    test_models()