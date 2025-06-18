#!/usr/bin/env python3
"""
Test script to verify feature alignment between dataset and API
"""

import pandas as pd
import numpy as np
from feature_config import ALL_FEATURES as CONFIG_FEATURES
from feature_config_fixed import ALL_FEATURES as FIXED_FEATURES

# Load dataset
df = pd.read_csv('data/final_100k_dataset_45features.csv')

# Get dataset columns (excluding metadata)
metadata_cols = ['startup_id', 'startup_name', 'founding_year', 'success', 'burn_multiple_calc']
dataset_features = [col for col in df.columns if col not in metadata_cols]

print("="*60)
print("FEATURE ALIGNMENT ANALYSIS")
print("="*60)

print(f"\nDataset has {len(dataset_features)} features")
print(f"Original feature_config.py has {len(CONFIG_FEATURES)} features")
print(f"Fixed feature_config.py has {len(FIXED_FEATURES)} features")

# Check if fixed config matches dataset
print("\n" + "="*60)
print("COMPARING FIXED CONFIG WITH DATASET")
print("="*60)

matches = 0
mismatches = []

for i, (dataset_feat, fixed_feat) in enumerate(zip(dataset_features, FIXED_FEATURES)):
    if dataset_feat == fixed_feat:
        matches += 1
    else:
        mismatches.append((i, dataset_feat, fixed_feat))
        print(f"Position {i}: Dataset has '{dataset_feat}', Fixed config has '{fixed_feat}'")

print(f"\nMatches: {matches}/{len(dataset_features)}")

if matches == len(dataset_features):
    print("✅ PERFECT ALIGNMENT! Fixed config matches dataset exactly.")
else:
    print("❌ Misalignment detected!")

# Show original config mismatches
print("\n" + "="*60)
print("ORIGINAL CONFIG MISMATCHES")
print("="*60)

original_mismatches = []
for i in range(min(len(dataset_features), len(CONFIG_FEATURES))):
    if i < len(dataset_features) and i < len(CONFIG_FEATURES):
        if dataset_features[i] != CONFIG_FEATURES[i]:
            original_mismatches.append((i, dataset_features[i], CONFIG_FEATURES[i]))

print(f"Found {len(original_mismatches)} position mismatches in original config:")
for i, dataset_feat, config_feat in original_mismatches[:10]:  # Show first 10
    print(f"  Position {i}: Dataset='{dataset_feat}', Config='{config_feat}'")

# Check for missing features
print("\n" + "="*60)
print("FEATURE PRESENCE CHECK")
print("="*60)

dataset_set = set(dataset_features)
config_set = set(CONFIG_FEATURES)
fixed_set = set(FIXED_FEATURES)

print("\nFeatures in dataset but not in original config:")
missing_in_config = dataset_set - config_set
if missing_in_config:
    print(f"  {missing_in_config}")
else:
    print("  None")

print("\nFeatures in original config but not in dataset:")
extra_in_config = config_set - dataset_set
if extra_in_config:
    print(f"  {extra_in_config}")
else:
    print("  None")

# Sample data test
print("\n" + "="*60)
print("SAMPLE DATA TEST")
print("="*60)

# Get first row of data
sample_row = df.iloc[0]
print("\nFirst row sample values:")
for feat in dataset_features[:5]:
    print(f"  {feat}: {sample_row[feat]}")

print("\n✅ Analysis complete!")
print("\nRECOMMENDATION:")
print("1. Use feature_config_fixed.py instead of feature_config.py")
print("2. Run train_pattern_models_fixed.py to train models with correct features")
print("3. Use pattern_classifier_fixed.py for predictions")