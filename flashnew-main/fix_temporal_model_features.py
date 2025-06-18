#!/usr/bin/env python3
"""
Fix for temporal model expecting 46 features instead of 45
"""

import joblib
import numpy as np
from pathlib import Path

# Check what the temporal model expects
temporal_model_path = Path("models/production_v45_fixed/temporal_model.pkl")
if temporal_model_path.exists():
    temporal_model = joblib.load(temporal_model_path)
    
    print("Temporal Model Information:")
    print(f"Model type: {type(temporal_model)}")
    
    if hasattr(temporal_model, 'n_features_in_'):
        print(f"Expected features: {temporal_model.n_features_in_}")
    
    if hasattr(temporal_model, 'feature_names_in_'):
        print(f"Feature names: {len(temporal_model.feature_names_in_)} features")
        print("Feature list:")
        for i, f in enumerate(temporal_model.feature_names_in_):
            print(f"  {i}: {f}")
    
    # Check feature order file
    feature_order_path = Path("models/production_v45_fixed/temporal_feature_order.pkl")
    if feature_order_path.exists():
        feature_order = joblib.load(feature_order_path)
        print(f"\nFeature order file has {len(feature_order)} features")
        
        # Compare with expected 45
        from feature_config import ALL_FEATURES
        print(f"\nExpected canonical features: {len(ALL_FEATURES)}")
        
        # Find differences
        extra_in_model = set(feature_order) - set(ALL_FEATURES)
        missing_in_model = set(ALL_FEATURES) - set(feature_order)
        
        if extra_in_model:
            print(f"\nExtra features in model: {extra_in_model}")
        if missing_in_model:
            print(f"\nMissing features in model: {missing_in_model}")
else:
    print("Temporal model not found at expected path")

# Check other models for comparison
print("\n\nChecking other models:")
for model_name in ['dna_analyzer', 'industry_model', 'ensemble_model']:
    model_path = Path(f"models/production_v45_fixed/{model_name}.pkl")
    if model_path.exists():
        model = joblib.load(model_path)
        if hasattr(model, 'n_features_in_'):
            print(f"{model_name}: expects {model.n_features_in_} features")