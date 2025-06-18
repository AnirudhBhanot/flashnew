#!/usr/bin/env python3
"""
Debug feature mismatch issue
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from models.unified_orchestrator_v3_integrated import UnifiedOrchestratorV3
from type_converter_simple import TypeConverter
from feature_config import ALL_FEATURES
import numpy as np

# Initialize components
orchestrator = UnifiedOrchestratorV3()
type_converter = TypeConverter()

# Minimal test data
test_data = {
    "total_capital_raised_usd": 5000000,
    "funding_stage": "series_a",
    "sector": "saas",
    "team_size_full_time": 25,
    "product_stage": "growth"
}

print("🔍 Debugging Feature Mismatch")
print("=" * 60)

# Convert
backend_data = type_converter.convert_frontend_to_backend(test_data)
canonical_features = {k: backend_data.get(k, 0) for k in ALL_FEATURES}

print(f"\n1. Canonical features expected: {len(ALL_FEATURES)}")
print(f"2. Features after conversion: {len(canonical_features)}")

# Check what the orchestrator is doing
print("\n3. Checking orchestrator feature preparation...")

# Prepare features array
features_array = np.array([[canonical_features.get(f, 0) for f in ALL_FEATURES]])
print(f"   Base features array shape: {features_array.shape}")

# Check if CAMP features are being added
from models.unified_orchestrator_v3_integrated import UnifiedOrchestratorV3
import inspect

# Look at the predict method
print("\n4. Examining orchestrator predict method...")
source = inspect.getsource(orchestrator.predict)
if "calculate_camp_features" in source:
    print("   ⚠️  CAMP features are being calculated and added!")
    
    # Calculate CAMP features manually
    camp_features = orchestrator.calculate_camp_features(canonical_features)
    print(f"   CAMP features added: {len(camp_features)}")
    print(f"   Total features: {len(ALL_FEATURES) + len(camp_features)}")

# Check model expectations
print("\n5. Checking model expectations...")
if hasattr(orchestrator.models["dna_analyzer"], "n_features_in_"):
    print(f"   DNA model expects: {orchestrator.models['dna_analyzer'].n_features_in_} features")
if hasattr(orchestrator.scaler, "n_features_in_"):
    print(f"   Scaler expects: {orchestrator.scaler.n_features_in_} features")

# Try to see what features the scaler was trained with
if hasattr(orchestrator.scaler, "feature_names_in_"):
    scaler_features = list(orchestrator.scaler.feature_names_in_)
    print(f"\n6. Scaler feature names ({len(scaler_features)}):")
    
    # Compare with ALL_FEATURES
    extra_features = [f for f in scaler_features if f not in ALL_FEATURES]
    if extra_features:
        print(f"   ⚠️  Extra features in scaler: {extra_features}")
    
    missing_features = [f for f in ALL_FEATURES if f not in scaler_features]
    if missing_features:
        print(f"   ⚠️  Missing features in scaler: {missing_features}")