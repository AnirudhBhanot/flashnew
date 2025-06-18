#!/usr/bin/env python3
"""
Test the fixed models to ensure they work correctly
"""

import pandas as pd
import numpy as np
from pathlib import Path
import sys
import json

# Add the models directory to the path
sys.path.append(str(Path(__file__).parent))

# Import the orchestrator
from models.unified_orchestrator_v3_integrated import UnifiedOrchestratorV3

def create_test_data():
    """Create test data with all required features"""
    from feature_config import ALL_FEATURES, CATEGORICAL_FEATURES
    
    # Create a sample startup
    test_data = {
        # Capital features
        'total_capital_raised_usd': 5000000,
        'cash_on_hand_usd': 3000000,
        'monthly_burn_usd': 150000,
        'runway_months': 20,
        'burn_multiple': 2.5,
        'investor_tier_primary': 'Tier_2',
        'has_debt': False,
        
        # Advantage features
        'patent_count': 3,
        'network_effects_present': True,
        'has_data_moat': True,
        'regulatory_advantage_present': False,
        'tech_differentiation_score': 4,
        'switching_cost_score': 3,
        'brand_strength_score': 3,
        'scalability_score': 4,
        
        # Market features
        'sector': 'SaaS',
        'tam_size_usd': 10000000000,
        'sam_size_usd': 1000000000,
        'som_size_usd': 100000000,
        'market_growth_rate_percent': 25,
        'customer_count': 100,
        'customer_concentration_percent': 15,
        'user_growth_rate_percent': 50,
        'net_dollar_retention_percent': 110,
        'competition_intensity': 3,
        'competitors_named_count': 5,
        'dau_mau_ratio': 0.4,
        
        # People features
        'founders_count': 2,
        'team_size_full_time': 25,
        'years_experience_avg': 10,
        'domain_expertise_years_avg': 8,
        'prior_startup_experience_count': 2,
        'prior_successful_exits_count': 1,
        'board_advisor_experience_score': 4,
        'advisors_count': 4,
        'team_diversity_percent': 40,
        'key_person_dependency': False,
        
        # Product features
        'product_stage': 'Growth',
        'product_retention_30d': 0.85,
        'product_retention_90d': 0.75,
        
        # Financial features
        'annual_revenue_run_rate': 2400000,
        'revenue_growth_rate_percent': 150,
        'gross_margin_percent': 75,
        'ltv_cac_ratio': 3.5,
        
        # Stage
        'funding_stage': 'Series_A'
    }
    
    return pd.DataFrame([test_data])

def test_individual_models():
    """Test each model individually"""
    import joblib
    
    print("\n=== Testing Individual Models ===\n")
    
    models_path = Path("models/production_v45_fixed")
    test_data = create_test_data()
    
    # Test DNA Analyzer (45 features)
    print("1. Testing DNA Analyzer (expects 45 features)...")
    try:
        dna_model = joblib.load(models_path / "dna_analyzer.pkl")
        dna_pred = dna_model.predict_proba(test_data)[:, 1]
        print(f"   ✓ DNA Analyzer prediction: {dna_pred[0]:.4f}")
    except Exception as e:
        print(f"   ✗ DNA Analyzer failed: {e}")
    
    # Test Industry Model (45 features)
    print("\n2. Testing Industry Model (expects 45 features)...")
    try:
        industry_model = joblib.load(models_path / "industry_model.pkl")
        industry_pred = industry_model.predict_proba(test_data)[:, 1]
        print(f"   ✓ Industry Model prediction: {industry_pred[0]:.4f}")
    except Exception as e:
        print(f"   ✗ Industry Model failed: {e}")
    
    # Test Temporal Model (46 features - needs burn_efficiency)
    print("\n3. Testing Temporal Model (expects 46 features)...")
    try:
        temporal_model = joblib.load(models_path / "temporal_model.pkl")
        # Add burn_efficiency
        temporal_data = test_data.copy()
        temporal_data['burn_efficiency'] = (temporal_data['annual_revenue_run_rate'] / 12) / temporal_data['monthly_burn_usd']
        temporal_pred = temporal_model.predict_proba(temporal_data)[:, 1]
        print(f"   ✓ Temporal Model prediction: {temporal_pred[0]:.4f}")
    except Exception as e:
        print(f"   ✗ Temporal Model failed: {e}")
    
    # Test Ensemble Model (3 features - predictions from other models)
    print("\n4. Testing Ensemble Model (expects 3 prediction features)...")
    try:
        ensemble_model = joblib.load(models_path / "ensemble_model.pkl")
        ensemble_data = pd.DataFrame({
            'dna_probability': [0.7],
            'temporal_probability': [0.65],
            'industry_probability': [0.75]
        })
        ensemble_pred = ensemble_model.predict_proba(ensemble_data)[:, 1]
        print(f"   ✓ Ensemble Model prediction: {ensemble_pred[0]:.4f}")
    except Exception as e:
        print(f"   ✗ Ensemble Model failed: {e}")

def test_orchestrator():
    """Test the full orchestrator"""
    print("\n\n=== Testing Unified Orchestrator ===\n")
    
    try:
        # Create orchestrator instance
        orchestrator = UnifiedOrchestratorV3()
        
        # Get model info
        info = orchestrator.get_model_info()
        print("Models loaded:", info['models_loaded'])
        print("Pattern system enabled:", info['pattern_system'])
        print("Weights:", json.dumps(info['weights'], indent=2))
        
        # Create test data
        test_data = create_test_data()
        
        # Make prediction
        print("\nMaking prediction with orchestrator...")
        result = orchestrator.predict(test_data)
        
        print("\n=== Orchestrator Results ===")
        print(f"Success Probability: {result['success_probability']:.4f}")
        print(f"Confidence Score: {result['confidence_score']:.4f}")
        print(f"Verdict: {result['verdict']} ({result['verdict_strength']})")
        print(f"Model Agreement: {result['model_agreement']:.4f}")
        
        print("\nIndividual Model Predictions:")
        for model, pred in result['model_predictions'].items():
            print(f"  - {model}: {pred:.4f}")
        
        print("\nWeights Used:")
        for component, weight in result['weights_used'].items():
            print(f"  - {component}: {weight:.2f}")
        
        # Check for any zero predictions
        zero_predictions = [model for model, pred in result['model_predictions'].items() if pred == 0.0]
        if zero_predictions:
            print(f"\n⚠️  WARNING: The following models returned 0%: {zero_predictions}")
        else:
            print(f"\n✅ All models returned non-zero predictions!")
        
    except Exception as e:
        print(f"\n❌ Orchestrator test failed: {e}")
        import traceback
        traceback.print_exc()

def main():
    """Run all tests"""
    print("Testing FLASH Model Fixes")
    print("=" * 50)
    
    # Test individual models first
    test_individual_models()
    
    # Test the orchestrator
    test_orchestrator()
    
    print("\n" + "=" * 50)
    print("Testing complete!")

if __name__ == "__main__":
    main()