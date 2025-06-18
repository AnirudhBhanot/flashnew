#!/usr/bin/env python3
"""
Validate the enhanced 75-feature dataset
"""
import pandas as pd
import numpy as np
import json

def validate_dataset():
    """Comprehensive validation of the enhanced dataset"""
    
    # Load datasets
    original_path = "/Users/sf/Desktop/FLASH/data/final_100k_dataset_45features.csv"
    enhanced_path = "/Users/sf/Desktop/FLASH/data/final_100k_dataset_75features.csv"
    
    df_original = pd.read_csv(original_path)
    df_enhanced = pd.read_csv(enhanced_path)
    
    print("Dataset Validation Report")
    print("=" * 60)
    
    # Basic stats
    print(f"\nOriginal dataset: {df_original.shape}")
    print(f"Enhanced dataset: {df_enhanced.shape}")
    print(f"New features added: {df_enhanced.shape[1] - df_original.shape[1]}")
    
    # Check data consistency
    print("\nData Consistency Checks:")
    print(f"Same number of rows: {len(df_original) == len(df_enhanced)}")
    print(f"Same startup IDs: {(df_original['startup_id'] == df_enhanced['startup_id']).all()}")
    print(f"Same success labels: {(df_original['success'] == df_enhanced['success']).all()}")
    
    # List new features
    new_features = set(df_enhanced.columns) - set(df_original.columns)
    print(f"\nNew features ({len(new_features)}):")
    
    # Categorize new features
    capital_features = [f for f in new_features if any(x in f for x in ['revenue', 'burn', 'funding', 'cash', 'payback', 'margin', 'efficiency'])]
    advantage_features = [f for f in new_features if any(x in f for x in ['customer_logo', 'competitive', 'organic', 'pilot', 'promoter', 'value'])]
    market_features = [f for f in new_features if any(x in f for x in ['market', 'category', 'competitor', 'sales_cycle', 'expansion'])]
    people_features = [f for f in new_features if any(x in f for x in ['founder', 'technical', 'team', 'employee', 'hire', 'commitment', 'exit'])]
    
    print(f"\nCAPITAL features ({len(capital_features)}):")
    for f in sorted(capital_features):
        print(f"  - {f}")
    
    print(f"\nADVANTAGE features ({len(advantage_features)}):")
    for f in sorted(advantage_features):
        print(f"  - {f}")
    
    print(f"\nMARKET features ({len(market_features)}):")
    for f in sorted(market_features):
        print(f"  - {f}")
        
    print(f"\nPEOPLE features ({len(people_features)}):")
    for f in sorted(people_features):
        print(f"  - {f}")
    
    # Data quality checks
    print("\nData Quality Checks:")
    
    # Check for nulls
    null_counts = df_enhanced[list(new_features)].isnull().sum()
    if null_counts.sum() > 0:
        print("WARNING: Null values found in new features:")
        print(null_counts[null_counts > 0])
    else:
        print("✓ No null values in new features")
    
    # Check ranges for key features
    print("\nFeature Range Validation:")
    
    # Percentage features (should be 0-100)
    pct_features = ['monthly_revenue_growth_rate', 'competitive_win_rate', 'organic_growth_percentage', 
                    'pilot_to_paid_conversion', 'founder_ownership_percentage', 'technical_founder_percentage',
                    'key_hire_retention', 'expansion_revenue_percentage']
    
    for feat in pct_features:
        if feat in df_enhanced.columns:
            min_val = df_enhanced[feat].min()
            max_val = df_enhanced[feat].max()
            print(f"  {feat}: [{min_val:.1f}, {max_val:.1f}]")
    
    # Score features (should be 1-10)
    score_features = ['customer_logo_quality', 'market_timing_score', 'team_completeness_score']
    
    print("\nScore Features (1-10):")
    for feat in score_features:
        if feat in df_enhanced.columns:
            min_val = df_enhanced[feat].min()
            max_val = df_enhanced[feat].max()
            mean_val = df_enhanced[feat].mean()
            print(f"  {feat}: [{min_val:.1f}, {max_val:.1f}], mean={mean_val:.1f}")
    
    # Distribution checks
    print("\nDistribution Analysis:")
    
    # Success rate by key features
    print("\nSuccess rate by customer_logo_quality:")
    logo_bins = pd.cut(df_enhanced['customer_logo_quality'], bins=[0, 3, 5, 7, 10])
    success_by_logo = df_enhanced.groupby(logo_bins)['success'].agg(['mean', 'count'])
    print(success_by_logo)
    
    print("\nSuccess rate by market_timing_score:")
    timing_bins = pd.cut(df_enhanced['market_timing_score'], bins=[0, 3, 5, 7, 10])
    success_by_timing = df_enhanced.groupby(timing_bins)['success'].agg(['mean', 'count'])
    print(success_by_timing)
    
    # Save validation report
    validation_report = {
        'original_shape': df_original.shape,
        'enhanced_shape': df_enhanced.shape,
        'new_features_count': len(new_features),
        'capital_features': len(capital_features),
        'advantage_features': len(advantage_features),
        'market_features': len(market_features),
        'people_features': len(people_features),
        'null_values': int(null_counts.sum()),
        'success_rate': float(df_enhanced['success'].mean())
    }
    
    with open('/Users/sf/Desktop/FLASH/data/validation_report.json', 'w') as f:
        json.dump(validation_report, f, indent=2)
    
    print("\n✓ Validation complete. Report saved to validation_report.json")
    
    return df_enhanced

if __name__ == "__main__":
    validate_dataset()