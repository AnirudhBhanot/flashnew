#!/usr/bin/env python3
"""
Add Realistic Variety - Simple and Fast Version
"""

import pandas as pd
import numpy as np

# Load dataset
print("Loading dataset...")
df = pd.read_csv('real_startup_data_100k.csv')
print(f"Loaded {len(df):,} companies")

# Convert to float to avoid dtype issues
numeric_cols = df.select_dtypes(include=[np.number]).columns
for col in numeric_cols:
    if col != 'success':
        df[col] = df[col].astype(float)

# 1. Break perfect separation - 20% overlap
print("\nBreaking perfect patterns...")
success_idx = df[df['success'] == 1].index
fail_idx = df[df['success'] == 0].index

# Give 20% of successful companies some bad metrics
bad_success = np.random.choice(success_idx, int(len(success_idx) * 0.2), replace=False)
df.loc[bad_success, 'burn_multiple'] = np.random.uniform(4, 8, len(bad_success))
df.loc[bad_success, 'runway_months'] = np.random.uniform(3, 9, len(bad_success))

# Give 20% of failed companies some good metrics  
good_fail = np.random.choice(fail_idx, int(len(fail_idx) * 0.2), replace=False)
df.loc[good_fail, 'burn_multiple'] = np.random.uniform(1, 2, len(good_fail))
df.loc[good_fail, 'revenue_growth_rate_percent'] = np.random.uniform(100, 300, len(good_fail))

# 2. Add 30% missing data
print("Adding missing data...")
can_be_missing = [col for col in df.columns if col not in ['company_id', 'company_name', 'success', 'sector']]
missing_mask = np.random.random((len(df), len(can_be_missing))) < 0.3
df[can_be_missing] = df[can_be_missing].mask(missing_mask)

# 3. Add noise to all numeric features
print("Adding measurement noise...")
for col in numeric_cols:
    if col not in ['success', 'company_id']:
        noise = np.random.normal(1, 0.3, len(df))  # 30% standard deviation
        df[col] = df[col] * noise

# 4. Add outliers (5% extreme cases)
print("Adding outliers...")
outlier_idx = np.random.choice(df.index, int(len(df) * 0.05), replace=False)
for idx in outlier_idx:
    # Randomly make 3-5 features extreme
    features = np.random.choice([col for col in numeric_cols if col != 'success'], 5, replace=False)
    for feat in features:
        if np.random.random() > 0.5:
            df.loc[idx, feat] *= np.random.uniform(5, 20)  # 5-20x
        else:
            df.loc[idx, feat] *= np.random.uniform(0.05, 0.2)  # 5-20%

# Save
output = 'real_startup_data_100k_messy.csv'
df.to_csv(output, index=False)

print(f"\n✅ Created messy dataset: {output}")
print(f"Success rate: {df['success'].mean():.1%}")
print(f"Missing data: {df.isnull().sum().sum() / (len(df) * len(df.columns)):.1%}")

# Check overlap worked
s_burn = df[df['success'] == 1]['burn_multiple'].dropna()
f_burn = df[df['success'] == 0]['burn_multiple'].dropna()
print(f"\nBurn multiple overlap: {max(s_burn.min(), f_burn.min()):.1f} - {min(s_burn.max(), f_burn.max()):.1f}")
print("Success/failure patterns now overlap! ✅")