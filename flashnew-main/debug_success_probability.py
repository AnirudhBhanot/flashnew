#!/usr/bin/env python3
"""Debug script to understand why success_probability returns 1.0"""

import sys
import json
import numpy as np
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from models.unified_orchestrator_v3_integrated import UnifiedOrchestratorV3
from type_converter_simple import TypeConverter
from feature_config import ALL_FEATURES

# Create test data
test_data = {
    "company_stage": "seed",
    "funding_stage": "seed",
    "total_capital_raised_usd": 1000000,
    "cash_on_hand_usd": 800000,
    "monthly_burn_usd": 50000,
    "runway_months": 16,
    "team_size_full_time": 5,
    "founders_count": 2,
    "years_experience_avg": 8,
    "sector": "fintech",
    "tam_size_usd": 10000000000,
    "customer_count": 100,
    "product_stage": "mvp",
    "annual_revenue_run_rate": 120000
}

print("Initializing orchestrator...")
orchestrator = UnifiedOrchestratorV3()

# Check loaded models
print(f"\nLoaded models: {list(orchestrator.models.keys())}")
print(f"Pattern system loaded: {orchestrator.pattern_system is not None}")
print(f"Config weights: {orchestrator.config.get('weights', {})}")

# Convert data
type_converter = TypeConverter()
features = type_converter.convert_frontend_to_backend(test_data)

# Get canonical features
canonical_features = {k: features.get(k, 0) for k in ALL_FEATURES}

# Get prediction
print("\nMaking prediction...")
result = orchestrator.predict(canonical_features)

print("\nPrediction Result:")
print(f"Success Probability: {result.get('success_probability', 'N/A')}")
print(f"Confidence Score: {result.get('confidence_score', 'N/A')}")
print(f"Verdict: {result.get('verdict', 'N/A')}")

if 'model_predictions' in result:
    print("\nIndividual Model Predictions:")
    for model, pred in result.get('model_predictions', {}).items():
        print(f"  {model}: {pred:.4f}")

if 'weights_used' in result:
    print("\nWeights Used:")
    for component, weight in result.get('weights_used', {}).items():
        print(f"  {component}: {weight}")

# Calculate what the weighted sum should be
if 'model_predictions' in result and 'weights_used' in result:
    print("\nDebug Calculation:")
    predictions = result['model_predictions']
    weights = result['weights_used']
    
    weighted_sum = 0
    for component, weight in weights.items():
        # Map component names to prediction keys
        pred_key_map = {
            'camp_evaluation': 'dna_analyzer',
            'pattern_analysis': 'pattern_analysis',
            'industry_specific': 'industry_specific', 
            'temporal_prediction': 'temporal_prediction'
        }
        
        pred_key = pred_key_map.get(component)
        if pred_key and pred_key in predictions:
            contribution = predictions[pred_key] * weight
            weighted_sum += contribution
            print(f"  {component}: {predictions[pred_key]:.4f} * {weight} = {contribution:.4f}")
        else:
            print(f"  {component}: NOT FOUND (weight={weight})")
    
    print(f"\nCalculated weighted sum: {weighted_sum:.4f}")
    print(f"Reported success_probability: {result.get('success_probability', 'N/A')}")
    
    # Check if they match
    if abs(weighted_sum - result.get('success_probability', 0)) > 0.001:
        print("\nWARNING: Mismatch between calculated and reported probability!")