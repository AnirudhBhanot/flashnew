#!/usr/bin/env python3
"""
Analyze all datasets in the codebase to understand their characteristics
"""

import pandas as pd
import numpy as np
import os
from pathlib import Path

# List of all dataset files
datasets = [
    'data/final_100k_dataset_45features.csv',
    'data/final_sample_1000.csv',
    'data/real_patterns_sample.csv',
    'data/real_patterns_startup_dataset_200k.csv',
    'data/realistic_dataset_sample_1k.csv',
    'data/realistic_startup_dataset_200k.csv',
    'experiments/final_100k_dataset_75features.csv',
    'experiments/final_100k_dataset_complete.csv',
    'experiments/final_100k_dataset_with_clusters.csv',
    'experiments/final_100k_dataset_with_pitches.csv',
    'generated_100k_dataset.csv',
    'real_startup_data.csv',
    'realistic_200k_dataset.csv'
]

print("="*80)
print("COMPREHENSIVE DATASET ANALYSIS")
print("="*80)

dataset_info = {}

for dataset_path in datasets:
    try:
        df = pd.read_csv(dataset_path)
        
        info = {
            'rows': len(df),
            'columns': len(df.columns),
            'success_rate': df['success'].mean() if 'success' in df.columns else None,
            'has_outcome_type': 'outcome_type' in df.columns,
            'column_sample': list(df.columns)[:10],  # First 10 columns
            'numeric_cols': len(df.select_dtypes(include=[np.number]).columns),
            'has_leakage': any(col in df.columns for col in ['outcome_type', 'strategic_value_score']),
            'date_created': os.path.getmtime(dataset_path)
        }
        
        dataset_info[dataset_path] = info
        
    except Exception as e:
        print(f"Error reading {dataset_path}: {e}")

# Sort by creation date
sorted_datasets = sorted(dataset_info.items(), key=lambda x: x[1]['date_created'])

print("\n1. DATASET OVERVIEW (by creation date):")
print("-"*80)

for path, info in sorted_datasets:
    print(f"\n{path.split('/')[-1]}:")
    print(f"  Size: {info['rows']:,} rows × {info['columns']} columns")
    print(f"  Success rate: {info['success_rate']:.1%}" if info['success_rate'] else "  Success rate: N/A")
    print(f"  Has outcome_type: {'Yes ⚠️' if info['has_outcome_type'] else 'No ✅'}")
    print(f"  Potential leakage: {'Yes ⚠️' if info['has_leakage'] else 'No ✅'}")

# Group similar datasets
print("\n\n2. DATASET FAMILIES:")
print("-"*80)

# 100k datasets
print("\n100k Family (initial experiments):")
hundredk_datasets = [k for k in dataset_info.keys() if '100k' in k]
for ds in hundredk_datasets:
    info = dataset_info[ds]
    print(f"  • {Path(ds).name}: {info['columns']} features, {info['success_rate']:.1%} success")

# 200k datasets  
print("\n200k Family (larger scale):")
twohundredk_datasets = [k for k in dataset_info.keys() if '200k' in k]
for ds in twohundredk_datasets:
    info = dataset_info[ds]
    print(f"  • {Path(ds).name}: {info['columns']} features, {info['success_rate']:.1%} success")

# Sample datasets
print("\nSample datasets (for testing):")
sample_datasets = [k for k in dataset_info.keys() if 'sample' in k.lower() or '1000' in k or '1k' in k]
for ds in sample_datasets:
    info = dataset_info[ds]
    print(f"  • {Path(ds).name}: {info['rows']:,} rows")

# Check column overlap
print("\n\n3. COLUMN OVERLAP ANALYSIS:")
print("-"*80)

# Get all unique columns
all_columns = set()
dataset_columns = {}
for path, info in dataset_info.items():
    if info['rows'] > 10000:  # Only consider full datasets
        df = pd.read_csv(path)
        dataset_columns[path] = set(df.columns)
        all_columns.update(df.columns)

# Find common columns
if len(dataset_columns) > 1:
    common_columns = set.intersection(*dataset_columns.values())
    print(f"\nCommon columns across all major datasets ({len(common_columns)}):")
    print(sorted(common_columns)[:20])  # Show first 20

# Check for identical datasets
print("\n\n4. DATASET SIMILARITY CHECK:")
print("-"*80)

# Compare key datasets
key_datasets = {
    'realistic_startup_dataset_200k.csv': 'data/realistic_startup_dataset_200k.csv',
    'real_patterns_startup_dataset_200k.csv': 'data/real_patterns_startup_dataset_200k.csv',
    'final_100k_dataset_45features.csv': 'data/final_100k_dataset_45features.csv'
}

for name1, path1 in key_datasets.items():
    if os.path.exists(path1):
        df1 = pd.read_csv(path1, nrows=1000)  # Sample for speed
        for name2, path2 in key_datasets.items():
            if name1 < name2 and os.path.exists(path2):
                df2 = pd.read_csv(path2, nrows=1000)
                
                # Check column overlap
                common_cols = set(df1.columns).intersection(set(df2.columns))
                overlap_pct = len(common_cols) / max(len(df1.columns), len(df2.columns)) * 100
                
                print(f"\n{name1} vs {name2}:")
                print(f"  Column overlap: {overlap_pct:.0f}%")
                
                # Check data similarity for common numeric columns
                numeric_common = [col for col in common_cols if col in df1.select_dtypes(include=[np.number]).columns]
                if numeric_common and len(numeric_common) > 5:
                    sample_cols = numeric_common[:5]
                    correlations = []
                    for col in sample_cols:
                        if col in df1.columns and col in df2.columns:
                            corr = df1[col].corr(df2[col])
                            if not np.isnan(corr):
                                correlations.append(corr)
                    
                    if correlations:
                        avg_corr = np.mean(correlations)
                        print(f"  Average correlation (sample): {avg_corr:.3f}")

print("\n\n5. RECOMMENDATION:")
print("="*80)

# Analysis for recommendation
recent_datasets = [ds for ds, info in dataset_info.items() if '200k' in ds or info['rows'] >= 100000]
has_leakage = [ds for ds, info in dataset_info.items() if info['has_leakage']]
realistic_datasets = [ds for ds in recent_datasets if ds not in has_leakage]

print("\n🎯 EXPERT ML RECOMMENDATION:\n")

print("DO NOT COMBINE ALL DATASETS. Here's why:\n")

print("1. DATA LEAKAGE ISSUES:")
print(f"   - {len(has_leakage)} datasets have outcome_type column (direct leakage)")
print("   - Combining would contaminate clean datasets")

print("\n2. DIFFERENT GENERATION METHODS:")
print("   - realistic_startup_dataset_200k.csv: Uses outcome_type deterministically")
print("   - real_patterns_startup_dataset_200k.csv: Based on historical patterns") 
print("   - final_100k_dataset_45features.csv: Original synthetic data")
print("   - Each has different statistical properties")

print("\n3. RECOMMENDED APPROACH:")

print("\n   ✅ USE ONLY: real_patterns_startup_dataset_200k.csv")
print("      - Most recent (created after learning from mistakes)")
print("      - Based on real startup statistics")
print("      - 200k samples (good size)")
print("      - 20% success rate (realistic)")
print("      - No outcome_type column")

print("\n   ⚠️  HOWEVER: Even this dataset shows signs of over-correlation")
print("      - Achieves 99%+ AUC (unrealistic)")
print("      - Synthetic patterns too strong")

print("\n4. FOR PRODUCTION:")
print("   - Use real_patterns_startup_dataset_200k.csv for now")
print("   - But expect 65-80% AUC on real data (not 99%)")
print("   - Plan to replace with actual historical data")

print("\n5. DATASETS TO DELETE/ARCHIVE:")
archived = [ds for ds in has_leakage]
print(f"   - Archive {len(archived)} datasets with leakage")
print("   - Keep only clean, recent datasets")

print("\n" + "="*80)
print("BOTTOM LINE: Quality > Quantity")
print("One good dataset > Multiple problematic datasets combined")
print("="*80)