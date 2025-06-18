#!/usr/bin/env python3
"""
Debug individual model predictions to understand the scoring issue
"""

import json
import requests
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.unified_orchestrator_v3_integrated import UnifiedOrchestratorV3
from feature_config import ALL_FEATURES
import pandas as pd
import numpy as np

# Test data
test_data = {
    "funding_stage": "series_a",
    "monthly_burn_usd": 200000,
    "runway_months": 24,
    "revenue_usd": 500000,
    "revenue_growth_rate_percent": 40,
    "gross_margin_percent": 80,
    "customer_acquisition_cost_usd": 200,
    "lifetime_value_usd": 5000,
    "arr_usd": 6000000,
    "market_size_usd": 10000000000,
    "market_growth_rate_percent": 50,
    "product_stage": "growth",
    "team_size": 25,
    "founder_experience_years": 15,
    "technical_team_percent": 60,
    "sales_team_percent": 20,
    "customer_churn_rate_percent": 2,
    "nps_score": 80,
    "cash_balance_usd": 4800000,
    "industry": "SaaS",
    "location": "San Francisco",
    # Add additional features with default values
    "burn_multiple": 0.4,  # burn/revenue
    "ltv_cac_ratio": 25,  # 5000/200
    "monthly_recurring_revenue_usd": 500000,
    "customer_count": 1000,
    "average_contract_value_usd": 5000,
    "sales_cycle_days": 30,
    "marketing_spend_percent": 20,
    "r_and_d_spend_percent": 40,
    "gross_burn_rate_usd": 200000,
    "net_burn_rate_usd": -300000,  # negative means making money
    "months_since_last_funding": 12,
    "total_funding_usd": 10000000,
    "valuation_usd": 50000000,
    "employee_growth_rate_percent": 50,
    "revenue_per_employee_usd": 240000,
    "has_patents": True,
    "has_strategic_partnerships": True,
    "international_revenue_percent": 20,
    "regulatory_compliance_status": "compliant",
    "data_security_certifications": True,
    "scalability_score": 4,
    "time_to_revenue_months": 6,
    "competitive_advantage_score": 4,
    "market_share_percent": 5,
    "partnership_score": 4,
    "product_market_fit_score": 4,
    "advisor_score": 4,
    "board_experience_score": 4,
    "previous_exit_experience": True,
    "technical_debt_score": 2,  # lower is better
    "code_quality_score": 4,
    "infrastructure_scalability_score": 4,
    "cybersecurity_score": 4,
    "innovation_score": 4
}

def debug_orchestrator():
    """Debug the orchestrator predictions directly"""
    print("Loading orchestrator...")
    orchestrator = UnifiedOrchestratorV3()
    
    print(f"\nLoaded models: {list(orchestrator.models.keys())}")
    print(f"Configured weights: {orchestrator.config['weights']}")
    print(f"Pattern system enabled: {orchestrator.pattern_system is not None}")
    
    # Prepare features
    features_dict = {k: test_data.get(k, 0) for k in ALL_FEATURES}
    features_df = pd.DataFrame([features_dict])
    
    print(f"\nFeatures shape: {features_df.shape}")
    print(f"Features columns: {len(features_df.columns)}")
    
    # Get prediction
    print("\nGetting prediction...")
    try:
        result = orchestrator.predict(features_df)
        
        print("\nPrediction Result:")
        print(f"Success Probability: {result['success_probability']:.1%}")
        print(f"Verdict: {result['verdict']}")
        print(f"Model Agreement: {result['model_agreement']:.3f}")
        
        print("\nIndividual Model Predictions:")
        for model, pred in result['model_predictions'].items():
            print(f"  {model}: {pred:.1%}")
        
        print("\nWeights Used:")
        for component, weight in result['weights_used'].items():
            print(f"  {component}: {weight:.1%}")
        
        # Calculate weighted contributions
        print("\nWeighted Contributions to Final Score:")
        predictions = result['model_predictions']
        weights = result['weights_used']
        
        total_contribution = 0
        for key in ['dna_analyzer', 'pattern_analysis', 'industry_specific', 'temporal_prediction']:
            model_key = key
            weight_key = key
            
            # Map model names to weight names
            if key == 'dna_analyzer':
                weight_key = 'camp_evaluation'
            elif key == 'pattern_analysis' and key not in predictions:
                continue  # Skip if pattern analysis is disabled
                
            if model_key in predictions and weight_key in weights:
                contribution = predictions[model_key] * weights[weight_key]
                print(f"  {key}: {predictions[model_key]:.1%} × {weights[weight_key]:.1%} = {contribution:.1%}")
                total_contribution += contribution
        
        print(f"\nTotal (should match success probability): {total_contribution:.1%}")
        
        # Test with direct model calls
        print("\n\nDirect Model Testing:")
        print("-" * 50)
        
        for model_name, model in orchestrator.models.items():
            try:
                if hasattr(model, 'predict_proba'):
                    # Prepare features based on model type
                    if model_name == 'dna_analyzer':
                        model_features = orchestrator._prepare_dna_features(features_df)
                    elif model_name == 'temporal_model':
                        model_features = orchestrator._prepare_temporal_features(features_df)
                    else:
                        model_features = features_df
                    
                    pred = model.predict_proba(model_features)[:, 1][0]
                    print(f"{model_name}: {pred:.1%}")
                else:
                    print(f"{model_name}: No predict_proba method")
            except Exception as e:
                print(f"{model_name}: Error - {str(e)}")
        
    except Exception as e:
        print(f"Error during prediction: {e}")
        import traceback
        traceback.print_exc()

def test_camp_calculation():
    """Test CAMP score calculation directly"""
    print("\n\nTesting CAMP Calculation:")
    print("-" * 50)
    
    try:
        from camp_calculator import CAMPCalculator
        calculator = CAMPCalculator()
        
        # Prepare features
        features = {k: test_data.get(k, 0) for k in ALL_FEATURES}
        
        # Calculate CAMP scores
        camp_result = calculator.calculate_camp_scores(features, test_data['funding_stage'])
        
        print("CAMP Scores:")
        for pillar, score in camp_result['scores'].items():
            print(f"  {pillar}: {score:.1%}")
        
        print(f"\nWeighted CAMP Score: {camp_result['weighted_score']:.1%}")
        
    except Exception as e:
        print(f"Error calculating CAMP scores: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_orchestrator()
    test_camp_calculation()