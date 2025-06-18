#!/usr/bin/env python3
"""
Debug raw model predictions before recalibration
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
    'funding_stage': 'Series_A',
    'monthly_burn_usd': 200000,
    'runway_months': 24,
    'annual_revenue_run_rate': 6000000,
    'revenue_growth_rate_percent': 40,
    'gross_margin_percent': 80,
    'customer_acquisition_cost_usd': 200,
    'lifetime_value_usd': 5000,
    'ltv_cac_ratio': 25,
    'tam_size_usd': 10000000000,
    'market_growth_rate_percent': 50,
    'product_stage': 'Growth',
    'team_size_full_time': 25,
    'founders_previous_experience_score': 4,
    'technical_team_percent': 60,
    'customer_churn_rate_percent': 2,
    'nps_score': 80,
    'cash_on_hand_usd': 4800000,
    'total_capital_raised_usd': 10000000,
    'investor_tier_primary': 'Tier_1',
    'sector': 'SaaS',
    'network_effects_present': True,
    'has_data_moat': True,
    'patent_count': 5,
    'burn_multiple': 0.4,
})

# Create DataFrame
df = pd.DataFrame([test_data])

print(f"\nDataFrame shape: {df.shape}")

# Test each model
print("\n" + "="*60)
print("Testing Individual Models (Raw Predictions)")
print("="*60)

# Test DNA model
try:
    print("\n1. DNA Analyzer:")
    pred = dna_model.predict_proba(df)
    print(f"   Prediction: {pred[0][1]:.4%}")
    print(f"   Raw values: {pred[0]}")
except Exception as e:
    print(f"   Error: {e}")

# Test Temporal model with burn_efficiency
try:
    print("\n2. Temporal Model:")
    df_temporal = df.copy()
    df_temporal['burn_efficiency'] = df['annual_revenue_run_rate'] / (12 * (df['monthly_burn_usd'] + 1))
    
    # Try to match exact feature order
    if hasattr(temporal_model, 'feature_names_in_'):
        feature_names = list(temporal_model.feature_names_in_)
        print(f"   Expected features: {len(feature_names)}")
        print(f"   First 5: {feature_names[:5]}")
        print(f"   Last 5: {feature_names[-5:]}")
        
        # Create ordered features
        ordered_features = pd.DataFrame()
        for feat in feature_names:
            if feat in df_temporal.columns:
                ordered_features[feat] = df_temporal[feat]
            else:
                ordered_features[feat] = 0
        
        pred = temporal_model.predict_proba(ordered_features)
    else:
        pred = temporal_model.predict_proba(df_temporal)
        
    print(f"   Prediction: {pred[0][1]:.4%}")
    print(f"   Raw values: {pred[0]}")
except Exception as e:
    print(f"   Error: {e}")

# Test Industry model  
try:
    print("\n3. Industry Model:")
    pred = industry_model.predict_proba(df)
    print(f"   Prediction: {pred[0][1]:.4%}")
    print(f"   Raw values: {pred[0]}")
except Exception as e:
    print(f"   Error: {e}")

# Test models after loading base predictions
dna_pred = 0.209
temporal_pred = 0.00006
industry_pred = 0.00005

print("\n" + "="*60)
print("Testing Ensemble Model")
print("="*60)

# The ensemble model expects predictions from the 3 base models
ensemble_features = pd.DataFrame({
    'dna_probability': [dna_pred],
    'temporal_probability': [temporal_pred],
    'industry_probability': [industry_pred]
})

ensemble_pred = ensemble_model.predict_proba(ensemble_features)[:, 1][0]
print(f"\nEnsemble model prediction: {ensemble_pred:.4%}")

# Show what recalibration would do
print("\n" + "="*50)
print("Testing Recalibration")
print("="*50)

def recalibrate_aggressive(prob):
    """More aggressive recalibration for extremely conservative models"""
    if prob < 0.0001:  # Less than 0.01%
        # Map to 10-20% range
        return 0.10 + (prob / 0.0001) * 0.10
    elif prob < 0.001:  # Less than 0.1%
        # Map to 20-30% range
        return 0.20 + ((prob - 0.0001) / 0.0009) * 0.10
    elif prob < 0.01:  # Less than 1%
        # Map to 30-40% range
        return 0.30 + ((prob - 0.001) / 0.009) * 0.10
    elif prob < 0.1:  # Less than 10%
        # Map to 40-50% range
        return 0.40 + ((prob - 0.01) / 0.09) * 0.10
    elif prob < 0.2:  # Less than 20%
        # Map to 50-60% range
        return 0.50 + ((prob - 0.1) / 0.1) * 0.10
    else:
        # Keep as is (or slight boost)
        return min(0.95, prob * 1.2)

print(f"\nIndustry: {industry_pred:.6f} → {recalibrate_aggressive(industry_pred):.4f}")
print(f"Temporal: {temporal_pred:.6f} → {recalibrate_aggressive(temporal_pred):.4f}")
print(f"Ensemble: {ensemble_pred:.6f} → {recalibrate_aggressive(ensemble_pred):.4f}")

# Show the impact on final score
print("\n" + "="*50)
print("Impact on Final Score")
print("="*50)

weights = {
    'camp_evaluation': 0.50,
    'industry_specific': 0.20,
    'temporal_prediction': 0.20,
    'ensemble': 0.10
}

# Current (too conservative)
current_score = (
    dna_pred * weights['camp_evaluation'] +
    industry_pred * weights['industry_specific'] +
    temporal_pred * weights['temporal_prediction'] +
    ensemble_pred * weights['ensemble']
)

# Recalibrated
recal_score = (
    dna_pred * weights['camp_evaluation'] +
    recalibrate_aggressive(industry_pred) * weights['industry_specific'] +
    recalibrate_aggressive(temporal_pred) * weights['temporal_prediction'] +
    recalibrate_aggressive(ensemble_pred) * weights['ensemble']
)

print(f"\nCurrent final score: {current_score:.1%}")
print(f"Recalibrated score: {recal_score:.1%}")
print(f"\nThis would bring the strong startup from ~14% to ~{recal_score:.0%}%")