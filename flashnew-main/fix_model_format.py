#!/usr/bin/env python3
"""
Fix model format issues by re-saving with correct joblib version
"""

import joblib
import pickle
import os

def fix_models():
    """Re-save models in compatible format"""
    
    print("Fixing model format issues...")
    
    # Load the new models
    try:
        rf_model = joblib.load('models/production_real_data/random_forest_model.pkl')
        xgb_model = joblib.load('models/production_real_data/xgboost_model.pkl')
        scaler = joblib.load('models/production_real_data/feature_scaler.pkl')
        
        print("✅ Loaded new models successfully")
        
        # Save in production format with pickle protocol 4 for compatibility
        joblib.dump(rf_model, 'models/production_v45/dna_analyzer.pkl', protocol=4)
        joblib.dump(xgb_model, 'models/production_v45/temporal_model.pkl', protocol=4)
        joblib.dump(xgb_model, 'models/production_v45/industry_model.pkl', protocol=4)
        joblib.dump(rf_model, 'models/production_v45/ensemble_model.pkl', protocol=4)
        joblib.dump(scaler, 'models/production_v45/feature_scaler.pkl', protocol=4)
        
        print("✅ Re-saved models in compatible format")
        
        # Test loading
        test_model = joblib.load('models/production_v45/dna_analyzer.pkl')
        print("✅ Test load successful")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    fix_models()