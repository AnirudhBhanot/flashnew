#!/usr/bin/env python3
"""
Debug individual models to understand why they return 0%
"""

import joblib
import numpy as np
import pandas as pd
from feature_config import ALL_FEATURES

# Load models individually
print("Loading models...")
dna_model = joblib.load('models/production_v45_fixed/dna_analyzer.pkl')
temporal_model = joblib.load('models/production_v45_fixed/temporal_model.pkl')
industry_model = joblib.load('models/production_v45_fixed/industry_model.pkl')
ensemble_model = joblib.load('models/production_v45_fixed/ensemble_model.pkl')

# Create test data - strong startup profile
test_data = {f: 0 for f in ALL_FEATURES}
test_data.update({
    'funding_stage': 'series_a',
    'monthly_burn_usd': 200000,
    'runway_months': 24,
    'revenue_usd': 500000,
    'revenue_growth_rate_percent': 40,
    'gross_margin_percent': 80,
    'customer_acquisition_cost_usd': 200,
    'lifetime_value_usd': 5000,
    'arr_usd': 6000000,
    'market_size_usd': 10000000000,
    'market_growth_rate_percent': 50,
    'product_stage': 'growth',
    'team_size': 25,
    'founder_experience_years': 15,
    'technical_team_percent': 60,
    'sales_team_percent': 20,
    'customer_churn_rate_percent': 2,
    'nps_score': 80,
    'cash_balance_usd': 4800000,
})

# Convert categorical variables
categorical_mapping = {
    'funding_stage': {'pre_seed': 0, 'seed': 1, 'series_a': 2, 'series_b': 3, 'series_c': 4, 'growth': 5},
    'product_stage': {'idea': 0, 'mvp': 1, 'beta': 2, 'launched': 3, 'growth': 4},
}

# Apply mappings
for field, mapping in categorical_mapping.items():
    if field in test_data and test_data[field] in mapping:
        test_data[field] = mapping[test_data[field]]

# Create DataFrame
df = pd.DataFrame([test_data])

print(f"\nDataFrame shape: {df.shape}")
print(f"Data types:\n{df.dtypes.value_counts()}")

# Test each model
print("\n" + "="*60)
print("Testing Individual Models")
print("="*60)

# Test DNA model
try:
    print("\n1. DNA Analyzer:")
    print(f"   Expected features: {dna_model.n_features_in_}")
    if hasattr(dna_model, 'feature_names_in_'):
        print(f"   First 5 features: {list(dna_model.feature_names_in_[:5])}")
    pred = dna_model.predict_proba(df[ALL_FEATURES])
    print(f"   Prediction: {pred[0][1]:.1%}")
    print(f"   Classes: {dna_model.classes_}")
except Exception as e:
    print(f"   Error: {e}")

# Test Temporal model
try:
    print("\n2. Temporal Model:")
    print(f"   Expected features: {temporal_model.n_features_in_}")
    if hasattr(temporal_model, 'feature_names_in_'):
        print(f"   First 5 features: {list(temporal_model.feature_names_in_[:5])}")
    
    # Add burn efficiency for temporal model
    df_temporal = df.copy()
    df_temporal['burn_efficiency'] = df_temporal['revenue_usd'] / (df_temporal['monthly_burn_usd'] + 1)
    
    pred = temporal_model.predict_proba(df_temporal[ALL_FEATURES + ['burn_efficiency']])
    print(f"   Prediction: {pred[0][1]:.1%}")
    print(f"   Raw prediction values: {pred[0]}")
except Exception as e:
    print(f"   Error: {e}")

# Test Industry model  
try:
    print("\n3. Industry Model:")
    print(f"   Expected features: {industry_model.n_features_in_}")
    if hasattr(industry_model, 'feature_names_in_'):
        print(f"   First 5 features: {list(industry_model.feature_names_in_[:5])}")
    pred = industry_model.predict_proba(df[ALL_FEATURES])
    print(f"   Prediction: {pred[0][1]:.1%}")
    print(f"   Raw prediction values: {pred[0]}")
except Exception as e:
    print(f"   Error: {e}")

# Test Ensemble model
try:
    print("\n4. Ensemble Model:")
    print(f"   Expected features: {ensemble_model.n_features_in_}")
    if hasattr(ensemble_model, 'feature_names_in_'):
        print(f"   Feature names: {list(ensemble_model.feature_names_in_)}")
    
    # Ensemble expects 3 probability features
    probs = pd.DataFrame({
        'dna_prob': [0.2],
        'temporal_prob': [0.1], 
        'industry_prob': [0.1]
    })
    pred = ensemble_model.predict_proba(probs)
    print(f"   Prediction: {pred[0][1]:.1%}")
except Exception as e:
    print(f"   Error: {e}")

# Check for extreme values in predictions
print("\n" + "="*60)
print("Checking for Extreme Values")
print("="*60)

# Test with all 0s
zero_data = {f: 0 for f in ALL_FEATURES}
df_zero = pd.DataFrame([zero_data])

print("\nWith all zeros:")
for name, model in [('DNA', dna_model), ('Industry', industry_model)]:
    try:
        pred = model.predict_proba(df_zero)
        print(f"  {name}: {pred[0][1]:.1%}")
    except:
        print(f"  {name}: Error")

# Test with reasonable values
print("\nWith mid-range values:")
mid_data = {f: 0.5 if f not in categorical_mapping else 2 for f in ALL_FEATURES}
mid_data.update({
    'monthly_burn_usd': 100000,
    'revenue_usd': 100000,
    'cash_balance_usd': 1000000,
    'team_size': 10,
    'runway_months': 10,
})
df_mid = pd.DataFrame([mid_data])

for name, model in [('DNA', dna_model), ('Industry', industry_model)]:
    try:
        pred = model.predict_proba(df_mid)
        print(f"  {name}: {pred[0][1]:.1%}")
    except:
        print(f"  {name}: Error")