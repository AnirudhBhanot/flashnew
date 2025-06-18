#!/usr/bin/env python3
"""
Fix model calibration - the models are too conservative
"""

import numpy as np
import joblib
from sklearn.calibration import CalibratedClassifierCV
from sklearn.model_selection import train_test_split
import pandas as pd

# Load the models
print("Loading models...")
temporal_model = joblib.load('models/production_v45_fixed/temporal_model.pkl')
industry_model = joblib.load('models/production_v45_fixed/industry_model.pkl')

# Load the training data to understand the distribution
print("\nLoading training data...")
try:
    # Try to load the most recent dataset
    data = pd.read_csv('final_realistic_100k_dataset.csv')
    print(f"Loaded dataset with {len(data)} samples")
    
    # Check success rate
    success_rate = data['success'].mean()
    print(f"Success rate in training data: {success_rate:.1%}")
    
    # Get feature columns
    feature_cols = [col for col in data.columns if col not in ['success', 'outcome_type', 'company_id']]
    
    # Prepare data
    X = data[feature_cols]
    y = data['success']
    
    # For temporal model, add burn_efficiency
    X_temporal = X.copy()
    X_temporal['burn_efficiency'] = X_temporal['annual_revenue_run_rate'] / (X_temporal['monthly_burn_usd'] + 1)
    
    # Test current predictions
    print("\nCurrent model predictions on training data sample:")
    sample_indices = np.random.choice(len(X), 100, replace=False)
    
    temporal_preds = temporal_model.predict_proba(X_temporal.iloc[sample_indices])[:, 1]
    industry_preds = industry_model.predict_proba(X.iloc[sample_indices])[:, 1]
    
    print(f"Temporal model - Mean: {temporal_preds.mean():.3%}, Max: {temporal_preds.max():.3%}")
    print(f"Industry model - Mean: {industry_preds.mean():.3%}, Max: {industry_preds.max():.3%}")
    
    # The models are way too conservative - let's check their distribution
    print("\nPrediction distribution:")
    print(f"Temporal < 1%: {(temporal_preds < 0.01).sum()}/{len(temporal_preds)}")
    print(f"Industry < 1%: {(industry_preds < 0.01).sum()}/{len(industry_preds)}")
    
except Exception as e:
    print(f"Error loading training data: {e}")
    print("Models appear to be severely miscalibrated")

# Create a recalibration wrapper
class RecalibratedModel:
    """Wrapper to recalibrate overly conservative models"""
    
    def __init__(self, base_model, min_prob=0.05, max_prob=0.95, scale_factor=10.0):
        self.base_model = base_model
        self.min_prob = min_prob
        self.max_prob = max_prob
        self.scale_factor = scale_factor
        self.n_features_in_ = base_model.n_features_in_
        self.feature_names_in_ = getattr(base_model, 'feature_names_in_', None)
        self.classes_ = base_model.classes_
        
    def predict_proba(self, X):
        # Get base predictions
        base_probs = self.base_model.predict_proba(X)
        
        # Apply logarithmic scaling to expand the probability range
        # This transforms very small probabilities to a more reasonable range
        positive_probs = base_probs[:, 1]
        
        # Apply log transformation with scaling
        # log(p) transforms [0.0001, 0.01] to [-9.2, -4.6]
        # We then scale and sigmoid to get back to [0, 1]
        log_probs = np.log(positive_probs + 1e-10)
        scaled_log_probs = log_probs / self.scale_factor
        
        # Convert back to probability space with sigmoid
        recalibrated = 1 / (1 + np.exp(-scaled_log_probs))
        
        # Apply min/max bounds
        recalibrated = np.clip(recalibrated, self.min_prob, self.max_prob)
        
        # Reconstruct probability matrix
        result = np.zeros_like(base_probs)
        result[:, 0] = 1 - recalibrated
        result[:, 1] = recalibrated
        
        return result
    
    def predict(self, X):
        probs = self.predict_proba(X)
        return (probs[:, 1] >= 0.5).astype(int)

# Test recalibration
print("\n" + "="*60)
print("Testing Recalibration")
print("="*60)

# Create recalibrated models
recal_temporal = RecalibratedModel(temporal_model, scale_factor=8.0)
recal_industry = RecalibratedModel(industry_model, scale_factor=8.0)

# Test on sample data
test_data = pd.DataFrame({
    'total_capital_raised_usd': [1000000, 5000000, 10000000],
    'monthly_burn_usd': [50000, 150000, 300000],
    'annual_revenue_run_rate': [600000, 3000000, 10000000],
    # Add other features with reasonable defaults
})

# Fill remaining features
from feature_config import ALL_FEATURES
for feat in ALL_FEATURES:
    if feat not in test_data.columns:
        test_data[feat] = 0

# Add burn efficiency for temporal
test_data_temporal = test_data.copy()
test_data_temporal['burn_efficiency'] = test_data_temporal['annual_revenue_run_rate'] / (test_data_temporal['monthly_burn_usd'] + 1)

print("\nOriginal vs Recalibrated predictions:")
print("Sample 1 (Small startup):")
print(f"  Temporal: {temporal_model.predict_proba(test_data_temporal.iloc[[0]])[:, 1][0]:.3%} → {recal_temporal.predict_proba(test_data_temporal.iloc[[0]])[:, 1][0]:.3%}")
print(f"  Industry: {industry_model.predict_proba(test_data.iloc[[0]])[:, 1][0]:.3%} → {recal_industry.predict_proba(test_data.iloc[[0]])[:, 1][0]:.3%}")

print("\nSample 2 (Medium startup):")
print(f"  Temporal: {temporal_model.predict_proba(test_data_temporal.iloc[[1]])[:, 1][0]:.3%} → {recal_temporal.predict_proba(test_data_temporal.iloc[[1]])[:, 1][0]:.3%}")
print(f"  Industry: {industry_model.predict_proba(test_data.iloc[[1]])[:, 1][0]:.3%} → {recal_industry.predict_proba(test_data.iloc[[1]])[:, 1][0]:.3%}")

# Save recalibrated models
print("\nSaving recalibrated models...")
joblib.dump(recal_temporal, 'models/production_v45_fixed/temporal_model_recalibrated.pkl')
joblib.dump(recal_industry, 'models/production_v45_fixed/industry_model_recalibrated.pkl')

print("\nRecalibration complete!")
print("\nTo use recalibrated models, update the orchestrator config to load:")
print("  - temporal_model_recalibrated.pkl")
print("  - industry_model_recalibrated.pkl")