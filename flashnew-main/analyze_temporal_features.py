#!/usr/bin/env python3
"""Analyze temporal feature order"""

import joblib
from feature_config import ALL_FEATURES

try:
    features = joblib.load('models/production_v45_fixed/temporal_feature_order.pkl')
    print(f'Temporal feature order has {len(features)} features')
    print('\nLast 10 features:', features[-10:])
    
    # Find extra features not in canonical 45
    extra = [f for f in features if f not in ALL_FEATURES and f != 'burn_efficiency']
    print(f'\nExtra features beyond canonical 45 + burn_efficiency: {extra}')
    
    # Check if all canonical features are present
    missing = [f for f in ALL_FEATURES if f not in features]
    print(f'\nMissing canonical features: {missing}')
    
except Exception as e:
    print(f'Error: {e}')