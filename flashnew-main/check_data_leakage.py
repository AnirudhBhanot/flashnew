#!/usr/bin/env python3
"""
Check for data leakage in real patterns dataset
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import train_test_split

# Load data
print("Loading dataset...")
df = pd.read_csv('data/real_patterns_startup_dataset_200k.csv')

print(f"\nDataset shape: {df.shape}")
print(f"Success rate: {df['success'].mean():.1%}")

# Check for perfect correlations
print("\n1. Checking for perfect correlations with success:")
numeric_cols = df.select_dtypes(include=[np.number]).columns
correlations = df[numeric_cols].corr()['success'].sort_values(ascending=False)

print("\nTop 10 correlations:")
print(correlations.head(10))

print("\nBottom 10 correlations:")
print(correlations.tail(10))

# Check for features that perfectly predict success
print("\n2. Checking for features that perfectly separate success/failure:")

for col in numeric_cols:
    if col != 'success':
        # Check if any value perfectly predicts success
        success_vals = df[df['success'] == 1][col].unique()
        failure_vals = df[df['success'] == 0][col].unique()
        
        # Find values that only appear in success or failure
        success_only = set(success_vals) - set(failure_vals)
        failure_only = set(failure_vals) - set(success_vals)
        
        if len(success_only) > 0 or len(failure_only) > 0:
            print(f"\nWARNING: {col} has deterministic values!")
            if len(success_only) > 0:
                print(f"  Values that ALWAYS mean success: {list(success_only)[:5]}")
            if len(failure_only) > 0:
                print(f"  Values that ALWAYS mean failure: {list(failure_only)[:5]}")

# Check categorical features
print("\n3. Checking categorical features:")
categorical_cols = ['funding_stage', 'sector', 'product_stage', 'investor_tier']

for col in categorical_cols:
    if col in df.columns:
        print(f"\n{col}:")
        success_by_cat = df.groupby(col)['success'].agg(['mean', 'count'])
        print(success_by_cat)
        
        # Check for perfect prediction
        if (success_by_cat['mean'] == 0).any() or (success_by_cat['mean'] == 1).any():
            print(f"  WARNING: Some categories perfectly predict outcome!")

# Quick model test
print("\n4. Testing simple model with different feature sets:")

# Prepare features
exclude_cols = ['startup_id', 'success', 'outcome_type']
feature_cols = [col for col in df.columns if col not in exclude_cols]
X = df[feature_cols]
y = df['success']

# Handle categorical
for col in categorical_cols:
    if col in X.columns:
        X[col] = pd.Categorical(X[col]).codes

X = X.fillna(0)

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Test 1: All features
rf = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
rf.fit(X_train, y_train)
y_pred = rf.predict_proba(X_test)[:, 1]
auc_all = roc_auc_score(y_test, y_pred)
print(f"\nWith ALL features: {auc_all:.4f} AUC")

# Get feature importance
importances = pd.DataFrame({
    'feature': X.columns,
    'importance': rf.feature_importances_
}).sort_values('importance', ascending=False)

print("\nTop 10 most important features:")
print(importances.head(10))

# Test 2: Remove top features
suspicious_features = importances.head(5)['feature'].tolist()
X_clean = X.drop(columns=suspicious_features)

rf_clean = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
rf_clean.fit(X_clean.iloc[X_train.index], y_train)
y_pred_clean = rf_clean.predict_proba(X_clean.iloc[X_test.index])[:, 1]
auc_clean = roc_auc_score(y_test, y_pred_clean)
print(f"\nWithout top 5 features: {auc_clean:.4f} AUC")

print("\n5. Recommendation:")
if auc_all > 0.95:
    print("⚠️  Model performance is suspiciously high! There's likely data leakage.")
    print("    The most suspicious features are:")
    for feat in suspicious_features:
        print(f"    - {feat}")
else:
    print("✅ Model performance seems realistic.")