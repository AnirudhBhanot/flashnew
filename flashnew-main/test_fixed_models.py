#!/usr/bin/env python3
"""
Test the fixed models directly without API authentication
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.unified_orchestrator_v3_integrated import UnifiedOrchestratorV3
from feature_config import ALL_FEATURES
# Skip type converter for now
import pandas as pd
import numpy as np

# Test cases
test_cases = {
    "Strong Startup": {
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
        "location": "San Francisco"
    },
    "Average Startup": {
        "funding_stage": "seed",
        "monthly_burn_usd": 100000,
        "runway_months": 12,
        "revenue_usd": 50000,
        "revenue_growth_rate_percent": 20,
        "gross_margin_percent": 70,
        "customer_acquisition_cost_usd": 500,
        "lifetime_value_usd": 2000,
        "arr_usd": 600000,
        "market_size_usd": 1000000000,
        "market_growth_rate_percent": 25,
        "product_stage": "beta",
        "team_size": 8,
        "founder_experience_years": 10,
        "technical_team_percent": 50,
        "sales_team_percent": 25,
        "customer_churn_rate_percent": 5,
        "nps_score": 50,
        "cash_balance_usd": 1200000,
        "industry": "SaaS",
        "location": "San Francisco"
    }
}

def test_models():
    """Test the fixed models"""
    print("Loading orchestrator...")
    orchestrator = UnifiedOrchestratorV3()
    # type_converter = TypeConverter()
    
    print(f"\nLoaded models: {list(orchestrator.models.keys())}")
    print(f"Pattern system: {'Enabled' if orchestrator.pattern_system else 'Disabled'}")
    
    for test_name, raw_data in test_cases.items():
        print(f"\n{'='*60}")
        print(f"Testing: {test_name}")
        print(f"{'='*60}")
        
        # Use raw data directly
        backend_features = raw_data
        
        # Create DataFrame with all features
        features_dict = {k: backend_features.get(k, 0) for k in ALL_FEATURES}
        features_df = pd.DataFrame([features_dict])
        
        # Get prediction
        result = orchestrator.predict(features_df)
        
        print(f"\nOverall Success Probability: {result['success_probability']:.1%}")
        print(f"Verdict: {result['verdict']}")
        print(f"Model Agreement: {result['model_agreement']:.3f}")
        
        print("\nIndividual Model Predictions:")
        for model, pred in result['model_predictions'].items():
            print(f"  {model}: {pred:.1%}")
        
        print("\nWeighted Contributions:")
        predictions = result['model_predictions']
        weights = result['weights_used']
        
        total = 0
        for model_key in predictions:
            # Map model names to weight keys
            weight_key = model_key
            if model_key == 'dna_analyzer':
                weight_key = 'camp_evaluation'
            elif model_key == 'industry_specific':
                weight_key = 'industry_specific'
            elif model_key == 'temporal_prediction':
                weight_key = 'temporal_prediction'
            elif model_key == 'ensemble':
                weight_key = 'ensemble'
                
            if weight_key in weights:
                contribution = predictions[model_key] * weights[weight_key]
                print(f"  {model_key}: {predictions[model_key]:.1%} × {weights[weight_key]:.1%} = {contribution:.1%}")
                total += contribution
        
        print(f"\nTotal: {total:.1%} (should match {result['success_probability']:.1%})")
        
        # Calculate CAMP scores
        from camp_calculator import calculate_camp_scores
        camp_scores = calculate_camp_scores(features_dict)
        print(f"\nCAMP Scores: {camp_scores}")
        
        if 'camp_scores' in camp_scores:
            print("\nDetailed CAMP Scores:")
            for pillar, score in camp_scores['camp_scores'].items():
                print(f"  {pillar}: {score:.1%}")
            print(f"  Average: {np.mean(list(camp_scores['camp_scores'].values())):.1%}")

if __name__ == "__main__":
    test_models()