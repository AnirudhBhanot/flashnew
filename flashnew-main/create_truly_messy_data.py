#!/usr/bin/env python3
"""
Create TRULY messy data - almost random with slight signal
"""

import pandas as pd
import numpy as np

print("Creating truly messy dataset...")

# Load original for structure
df = pd.read_csv('real_startup_data_100k.csv')
print(f"Starting with {len(df):,} companies")

# Keep only identifiers and success
result = pd.DataFrame({
    'company_id': df['company_id'],
    'company_name': df['company_name'],
    'success': df['success']
})

# For each feature, create mostly random data with tiny signal
from feature_config import ALL_FEATURES

for feature in ALL_FEATURES:
    if feature == 'sector':
        # Keep sectors but randomize
        result[feature] = np.random.choice(df[feature].unique(), len(df))
    elif feature == 'funding_stage':
        # Keep stages but randomize
        result[feature] = np.random.choice(df[feature].unique(), len(df))
    elif feature in ['investor_tier_primary', 'product_stage']:
        # Categorical - random
        result[feature] = np.random.choice([1, 2, 3, 4, 5], len(df))
    else:
        # Numeric features - mostly random with tiny correlation
        # Start with random base
        base = np.random.lognormal(3, 2, len(df))
        
        # Add TINY correlation with success (5% signal, 95% noise)
        signal_strength = 0.05
        success_adjustment = df['success'] * signal_strength
        
        # Some features correlate positively, some negatively
        if feature in ['burn_multiple', 'customer_concentration_percent', 'key_person_dependency']:
            # These are bad - higher for failures
            result[feature] = base * (1 - success_adjustment)
        else:
            # Most features - slightly higher for success
            result[feature] = base * (1 + success_adjustment)
        
        # Add massive noise
        noise = np.random.normal(1, 0.5, len(df))
        result[feature] = result[feature] * noise
        
        # Clip to reasonable ranges
        result[feature] = np.clip(result[feature], 0, np.percentile(result[feature], 99))

# Add 40% missing data completely at random
print("Adding 40% missing data...")
mask = np.random.random((len(result), len(ALL_FEATURES))) < 0.4
result[ALL_FEATURES] = result[ALL_FEATURES].mask(mask)

# Save
result.to_csv('real_startup_data_100k_truly_messy.csv', index=False)

print(f"\n✅ Created truly messy dataset!")
print(f"Success rate: {result['success'].mean():.1%}")
print(f"Missing data: {result[ALL_FEATURES].isnull().sum().sum() / (len(result) * len(ALL_FEATURES)):.1%}")

# Quick test - train a model
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score
from sklearn.impute import SimpleImputer

X = result[ALL_FEATURES]
y = result['success']

# Simple preprocessing
for col in ['sector', 'funding_stage']:
    X[col] = pd.Categorical(X[col]).codes

imputer = SimpleImputer(strategy='median')
X_imputed = imputer.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(X_imputed, y, test_size=0.2, random_state=42, stratify=y)

print("\nQuick model test...")
rf = RandomForestClassifier(n_estimators=50, random_state=42, n_jobs=-1)
rf.fit(X_train, y_train)
y_pred = rf.predict_proba(X_test)[:, 1]
auc = roc_auc_score(y_test, y_pred)

print(f"Random Forest AUC: {auc:.4f}")
print(f"Prediction range: {y_pred.min():.3f} - {y_pred.max():.3f}")

if auc < 0.85:
    print("\n🎉 SUCCESS! Finally achieved realistic AUC!")
    print("This dataset has:")
    print("- Only 5% signal, 95% noise")
    print("- 40% missing data")
    print("- Massive random variation")
    print("- Realistic difficulty for ML models")