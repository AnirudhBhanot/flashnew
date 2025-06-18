"""
Test script for hierarchical models
Validates the new 45-feature hierarchical models
"""

import pandas as pd
import numpy as np
import joblib
from pathlib import Path
import json
from datetime import datetime

def test_hierarchical_models():
    """Test the hierarchical models with sample data"""
    
    print("Loading test data...")
    # Load a sample from the dataset
    df = pd.read_csv('data/final_100k_dataset_45features.csv', nrows=100)
    
    # Prepare features
    feature_cols = [col for col in df.columns if col not in [
        'startup_id', 'startup_name', 'success', 'founding_year', 'burn_multiple_calc'
    ]]
    
    X = df[feature_cols]
    y = df['success'].astype(int)
    
    # Check if models exist
    model_path = Path('models/hierarchical_45features')
    if not model_path.exists():
        print(f"❌ Model directory not found: {model_path}")
        print("Please run train_hierarchical_models_45features.py first")
        return
    
    print("\nTesting individual hierarchical models...")
    
    # Test Stage-Based Model
    try:
        stage_model = joblib.load(model_path / 'stage_hierarchical_model.pkl')
        stage_pred = stage_model.predict_proba(X)[:, 1]
        print(f"✅ Stage-Based Model - Predictions range: [{stage_pred.min():.3f}, {stage_pred.max():.3f}]")
    except Exception as e:
        print(f"❌ Stage-Based Model failed: {e}")
    
    # Test Temporal Model
    try:
        temporal_model = joblib.load(model_path / 'temporal_hierarchical_model.pkl')
        temporal_pred = temporal_model.predict_proba(X)[:, 1]
        print(f"✅ Temporal Model - Predictions range: [{temporal_pred.min():.3f}, {temporal_pred.max():.3f}]")
    except Exception as e:
        print(f"❌ Temporal Model failed: {e}")
    
    # Test Industry Model
    try:
        industry_model = joblib.load(model_path / 'industry_specific_model.pkl')
        industry_pred = industry_model.predict_proba(X)[:, 1]
        print(f"✅ Industry Model - Predictions range: [{industry_pred.min():.3f}, {industry_pred.max():.3f}]")
    except Exception as e:
        print(f"❌ Industry Model failed: {e}")
    
    # Test DNA Pattern Model
    try:
        dna_model = joblib.load(model_path / 'dna_pattern_model.pkl')
        dna_pred = dna_model.predict_proba(X)[:, 1]
        print(f"✅ DNA Pattern Model - Predictions range: [{dna_pred.min():.3f}, {dna_pred.max():.3f}]")
    except Exception as e:
        print(f"❌ DNA Pattern Model failed: {e}")
    
    # Test Meta Ensemble
    try:
        meta_ensemble = joblib.load(model_path / 'hierarchical_meta_ensemble.pkl')
        final_pred = meta_ensemble.predict_proba(
            np.column_stack([stage_pred, temporal_pred, industry_pred, dna_pred])
        )[:, 1]
        print(f"✅ Meta Ensemble - Predictions range: [{final_pred.min():.3f}, {final_pred.max():.3f}]")
    except Exception as e:
        print(f"❌ Meta Ensemble failed: {e}")
    
    # Load test results if available
    try:
        with open(model_path / 'test_results.json', 'r') as f:
            results = json.load(f)
        print(f"\n📊 Model Performance on Test Set:")
        print(f"   - AUC: {results['test_auc']:.3f}")
        print(f"   - Accuracy: {results['test_accuracy']:.3f}")
        print(f"   - Precision: {results['test_precision']:.3f}")
        print(f"   - Recall: {results['test_recall']:.3f}")
    except:
        print("\n⚠️  Test results file not found")
    
    # Test specific scenarios
    print("\n🧪 Testing specific scenarios...")
    
    # Test 1: Pre-seed startup
    test_preseed = X.iloc[0:1].copy()
    test_preseed['funding_stage'] = 'Pre-seed'
    test_preseed['total_capital_raised_usd'] = 100000
    test_preseed['team_size_full_time'] = 3
    
    try:
        preseed_pred = stage_model.predict_proba(test_preseed)[:, 1][0]
        print(f"   Pre-seed test: {preseed_pred:.3f} probability")
    except:
        print("   Pre-seed test: Failed")
    
    # Test 2: SaaS company
    test_saas = X.iloc[0:1].copy()
    test_saas['sector'] = 'SaaS'
    test_saas['net_dollar_retention_percent'] = 120
    test_saas['ltv_cac_ratio'] = 3.5
    
    try:
        saas_pred = industry_model.predict_proba(test_saas)[:, 1][0]
        print(f"   SaaS test: {saas_pred:.3f} probability")
    except:
        print("   SaaS test: Failed")
    
    print("\n✅ Testing complete!")


if __name__ == "__main__":
    test_hierarchical_models()