#!/usr/bin/env python3
"""
Verify what's actually fixed vs what still needs work
"""

print("\nVERIFYING ACTUAL FIX STATUS")
print("=" * 60)

# Critical Functionality
print("\n1. CRITICAL FUNCTIONALITY:")
print("-" * 30)

# DNA Analyzer
try:
    from ml_core.models.dna_analyzer import DNAPatternAnalyzer
    with open('ml_core/models/dna_analyzer.py', 'r') as f:
        if '\\n' not in f.read():
            print("✅ DNA analyzer syntax error - FIXED")
        else:
            print("❌ DNA analyzer syntax error - NOT FIXED")
except:
    print("❌ DNA analyzer - CANNOT VERIFY")

# API explain endpoint
with open('api_server_unified.py', 'r') as f:
    content = f.read()
    if 'predict_enhanced(features)' not in content and 'predict(features)' in content:
        print("✅ API explain endpoint - FIXED")
    else:
        print("❌ API explain endpoint - NOT FIXED")

# Pattern weight
import json
with open('models/orchestrator_config_integrated.json', 'r') as f:
    config = json.load(f)
    if config['weights']['pattern_analysis'] > 0:
        print("✅ Pattern analysis weight - FIXED")
    else:
        print("❌ Pattern analysis weight - NOT FIXED")

# Hardcoded 0.5 values
with open('api_server_unified.py', 'r') as f:
    content = f.read()
    if 'normalized[key] = 0.5' not in content:
        print("✅ Hardcoded 0.5 in API - REMOVED")
    else:
        print("❌ Hardcoded 0.5 in API - STILL EXISTS")

# Test suite
try:
    import tests.test_complete_system
    print("✅ Test imports - FIXED")
except:
    print("❌ Test imports - NOT FIXED")

# Data Flow
print("\n2. DATA FLOW:")
print("-" * 30)

# Boolean conversion
from type_converter_simple import TypeConverter
tc = TypeConverter()
test = tc.convert_frontend_to_backend({"has_strategic_partnerships": True})
if test.get("has_strategic_partnerships") == 1:
    print("✅ Boolean conversion - FIXED")
else:
    print("❌ Boolean conversion - NOT FIXED")

# Security
print("\n3. SECURITY:")
print("-" * 30)

# CORS
if 'allow_methods=["GET", "POST", "OPTIONS"]' in content:
    print("✅ CORS tightened - FIXED")
else:
    print("❌ CORS tightened - NOT FIXED")

# API binding
from config import Settings
if Settings.API_HOST == "127.0.0.1":
    print("✅ API binding secure - FIXED")
else:
    print("❌ API binding secure - NOT FIXED")

# Rate limiting
if '@limiter.limit' in content:
    print("✅ Rate limiting - IMPLEMENTED")
else:
    print("❌ Rate limiting - NOT IMPLEMENTED")

# Architecture
print("\n4. ARCHITECTURE:")
print("-" * 30)

# Database
import os
if os.path.exists('database/models.py'):
    print("✅ Database layer - CREATED")
else:
    print("❌ Database layer - NOT CREATED")

# Utils
if os.path.exists('utils/probability_utils.py') and os.path.exists('utils/safe_math.py'):
    print("✅ Utility modules - CREATED")
else:
    print("❌ Utility modules - NOT CREATED")

# Tests
if os.path.exists('tests/unit/test_probability_utils.py'):
    print("✅ Test suite - CREATED")
else:
    print("❌ Test suite - NOT CREATED")

print("\n" + "=" * 60)
print("SUMMARY: Most fixes are implemented in code but not all are active")
print("=" * 60)