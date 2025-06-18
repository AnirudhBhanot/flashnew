#!/usr/bin/env python3
"""Map dataset columns to FLASH features"""

import pandas as pd

# Load dataset
df = pd.read_csv('generated_100k_dataset.csv')

print("Dataset columns:")
print("="*60)
for i, col in enumerate(df.columns):
    print(f"{i+1:3d}. {col}")

print(f"\nTotal columns: {len(df.columns)}")
print(f"Total rows: {len(df)}")

# Check success distribution
if 'success' in df.columns:
    print(f"\nSuccess rate: {df['success'].mean():.1%}")
    print(f"Success count: {df['success'].sum()}")
    print(f"Failure count: {len(df) - df['success'].sum()}")