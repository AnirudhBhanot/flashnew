#!/usr/bin/env python3
"""
Test if the fixes actually work
"""

import sys
import pandas as pd

print("Testing Flash System Fixes...")
print("=" * 50)

# Test 1: Import critical components
try:
    from ml_core.models.dna_analyzer import DNAPatternAnalyzer
    print("✅ DNA Analyzer imports successfully")
except Exception as e:
    print(f"❌ DNA Analyzer import failed: {e}")

# Test 2: Type converter
try:
    from type_converter_simple import TypeConverter
    converter = TypeConverter()
    
    # Test boolean conversion
    test_data = {
        "has_strategic_partnerships": True,
        "key_person_dependency": "false",
        "funding_stage": "Series A"
    }
    
    converted = converter.convert_frontend_to_backend(test_data)
    
    if converted["has_strategic_partnerships"] == 1:
        print("✅ Boolean True → 1 conversion works")
    else:
        print("❌ Boolean conversion failed")
        
    if converted["funding_stage"] == "series_a":
        print("✅ String normalization works")
    else:
        print("❌ String normalization failed")
        
except Exception as e:
    print(f"❌ Type converter test failed: {e}")

# Test 3: Probability utilities
try:
    from utils.probability_utils import normalize_probabilities, ensure_probability_bounds
    
    # Test normalization
    probs = [0.3, 0.5, 0.7]
    normalized = normalize_probabilities(probs)
    
    if abs(sum(normalized) - 1.0) < 0.0001:
        print("✅ Probability normalization works")
    else:
        print("❌ Probability normalization failed")
        
    # Test bounds
    bounded = ensure_probability_bounds(1.5)
    if 0 < bounded < 1:
        print("✅ Probability bounds work")
    else:
        print("❌ Probability bounds failed")
        
except Exception as e:
    print(f"❌ Probability utils test failed: {e}")

# Test 4: Safe math
try:
    from utils.safe_math import safe_divide, safe_log
    
    # Test division by zero
    result = safe_divide(10, 0)
    if result == 0:
        print("✅ Division by zero protection works")
    else:
        print("❌ Division by zero protection failed")
        
    # Test log of negative
    result = safe_log(-5)
    if result > -30:  # Should use epsilon
        print("✅ Safe log works")
    else:
        print("❌ Safe log failed")
        
except Exception as e:
    print(f"❌ Safe math test failed: {e}")

# Test 5: Orchestrator
try:
    from models.unified_orchestrator_v3_integrated import UnifiedOrchestratorV3
    
    # Check if pattern weight is fixed
    orchestrator = UnifiedOrchestratorV3()
    pattern_weight = orchestrator.config["weights"]["pattern_analysis"]
    
    if pattern_weight > 0:
        print(f"✅ Pattern analysis weight is {pattern_weight} (not 0)")
    else:
        print("❌ Pattern analysis weight is still 0")
        
except Exception as e:
    print(f"❌ Orchestrator test failed: {e}")

print("\n" + "=" * 50)
print("Fix verification complete!")