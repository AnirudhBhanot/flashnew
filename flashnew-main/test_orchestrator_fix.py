#!/usr/bin/env python3
"""Test script to verify orchestrator fix for weight distribution"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import pandas as pd
from models.unified_orchestrator_v3_integrated import UnifiedOrchestratorV3

def test_weight_distribution():
    """Test that weights are properly distributed"""
    
    # Test data - a startup with moderate metrics
    test_data = {
        'total_capital_raised_usd': 5000000,
        'cash_on_hand_usd': 3000000,
        'monthly_burn_usd': 200000,
        'runway_months': 15,
        'burn_multiple': 2.5,
        'annual_revenue_run_rate': 1000000,
        'revenue_growth_rate_percent': 100,
        'gross_margin_percent': 70,
        'customer_acquisition_cost_usd': 1000,
        'customer_lifetime_value_usd': 3000,
        'ltv_cac_ratio': 3.0,
        'product_retention_30d': 0.8,
        'product_retention_90d': 0.7,
        'dau_mau_ratio': 0.5,
        'user_growth_rate_percent': 50,
        'tam_size_usd': 10000000000,
        'sam_size_usd': 1000000000,
        'som_size_usd': 100000000,
        'customer_count': 100,
        'competitors_named_count': 5,
        'patent_count': 2,
        'proprietary_tech_score': 4,
        'switching_cost_score': 3,
        'brand_recognition_score': 2,
        'network_effects_present': 1,
        'has_data_moat': 1,
        'regulatory_advantage_present': 0,
        'founders_years_experience': 10,
        'founders_domain_expertise_score': 4,
        'founders_count': 2,
        'team_size_full_time': 20,
        'advisors_count': 3,
        'board_members_count': 5,
        'technical_leadership_score': 4,
        'sales_leadership_score': 3,
        'key_person_dependency': 0,
        'previous_startup_experience': 1,
        'investor_quality_score': 4,
        'has_debt': 0,
        'stage': 'Series A',
        'industry': 'SaaS',
        'business_model': 'B2B',
        'geographic_market': 'North America',
        'ai_product': 1
    }
    
    # Test with pattern system disabled
    print("Testing with pattern system DISABLED...")
    orchestrator_disabled = UnifiedOrchestratorV3("models/orchestrator_config_integrated_test_disabled.json")
    
    df = pd.DataFrame([test_data])
    result_disabled = orchestrator_disabled.predict(df)
    
    print(f"Success probability: {result_disabled['success_probability']:.2%}")
    print(f"Weights used: {result_disabled['weights_used']}")
    print(f"Sum of weights: {sum(result_disabled['weights_used'].values()):.2f}")
    print(f"Model predictions: {result_disabled['model_predictions']}")
    
    # Test with pattern system enabled
    print("\nTesting with pattern system ENABLED...")
    orchestrator_enabled = UnifiedOrchestratorV3()
    
    result_enabled = orchestrator_enabled.predict(df)
    
    print(f"Success probability: {result_enabled['success_probability']:.2%}")
    print(f"Weights used: {result_enabled['weights_used']}")
    print(f"Sum of weights: {sum(result_enabled['weights_used'].values()):.2f}")
    print(f"Model predictions: {result_enabled['model_predictions']}")
    
    # Compare results
    print("\nComparison:")
    print(f"Difference in predictions: {abs(result_enabled['success_probability'] - result_disabled['success_probability']):.2%}")
    
    # Verify weights sum to 1.0
    assert abs(sum(result_disabled['weights_used'].values()) - 1.0) < 0.001, "Disabled weights don't sum to 1.0!"
    assert abs(sum(result_enabled['weights_used'].values()) - 1.0) < 0.001, "Enabled weights don't sum to 1.0!"
    
    print("\n✅ All tests passed! Weights properly distributed.")

if __name__ == "__main__":
    # Create a test config with pattern disabled
    import json
    
    config = {
        "model_paths": {
            "dna_analyzer": "models/production_v45/dna_analyzer.pkl",
            "temporal_model": "models/production_v45/temporal_model.pkl",
            "industry_model": "models/production_v45/industry_model.pkl",
            "ensemble_model": "models/production_v45/ensemble_model.pkl",
            "pattern_ensemble": "models/pattern_success_models/pattern_ensemble_model.pkl"
        },
        "weights": {
            "camp_evaluation": 0.5,
            "pattern_analysis": 0.2,
            "industry_specific": 0.2,
            "temporal_prediction": 0.1
        },
        "pattern_system": {
            "enabled": False
        }
    }
    
    with open("models/orchestrator_config_integrated_test_disabled.json", "w") as f:
        json.dump(config, f, indent=2)
    
    test_weight_distribution()