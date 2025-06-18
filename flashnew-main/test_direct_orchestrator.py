#!/usr/bin/env python3
"""
Test orchestrator directly to find the error
"""
import pandas as pd
import traceback
from models.unified_orchestrator_v3_integrated import UnifiedOrchestratorV3

# Initialize
orchestrator = UnifiedOrchestratorV3()

# Test data
test_data = {
    "funding_stage": "seed",
    "sector": "saas", 
    "product_stage": "mvp",
    "investor_tier_primary": "tier_2",
    "tech_differentiation_score": 3,
    "competition_intensity": 3,
    "scalability_score": 3,
    "total_capital_raised_usd": 1000000,
    "product_retention_30d": 0.6
}

print("Testing direct orchestrator prediction...")
print(f"Input data: {test_data}")

# Create DataFrame
df = pd.DataFrame([test_data])
print(f"\nDataFrame dtypes:")
for col in df.columns:
    print(f"  {col}: {df[col].dtype}")

try:
    result = orchestrator.predict(df)
    print("\n✅ Prediction successful!")
    print(f"Result: {result}")
except Exception as e:
    print(f"\n❌ Prediction failed: {e}")
    print("\nFull traceback:")
    traceback.print_exc()
    
    # Try to identify the problematic comparison
    print("\nChecking data types in features:")
    for col in df.columns:
        val = df[col].iloc[0]
        print(f"  {col}: {val} (type: {type(val).__name__})")