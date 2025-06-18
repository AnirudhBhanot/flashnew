#!/usr/bin/env python3
"""
Analyze the quality of the generated high-quality startup dataset.
"""

import pandas as pd
import numpy as np
import json

def analyze_dataset():
    # Load the dataset
    df = pd.read_csv('high_quality_startup_dataset_100k.csv')
    
    print("=== HIGH-QUALITY STARTUP DATASET ANALYSIS ===\n")
    
    # Basic info
    print(f"Total records: {len(df):,}")
    print(f"Features: {len(df.columns)}")
    print(f"Memory usage: {df.memory_usage(deep=True).sum() / 1024**2:.1f} MB\n")
    
    # Success metrics
    if 'success' in df.columns:
        success_data = df['success'].dropna()
        print(f"Records with outcome: {len(success_data):,} ({len(success_data)/len(df)*100:.1f}%)")
        print(f"Success rate: {success_data.mean():.1%}")
        print(f"Successful companies: {success_data.sum():,.0f}")
        print(f"Failed companies: {(~success_data).sum():,.0f}")
        print(f"Active (no outcome): {df['success'].isna().sum():,}\n")
    
    # Industry distribution
    if 'sector' in df.columns:
        print("Industry Distribution:")
        for industry, count in df['sector'].value_counts().head(10).items():
            print(f"  {industry}: {count:,} ({count/len(df)*100:.1f}%)")
        print()
    
    # Funding stage distribution
    if 'funding_stage' in df.columns:
        print("Funding Stage Distribution:")
        for stage, count in df['funding_stage'].value_counts().items():
            print(f"  {stage}: {count:,} ({count/len(df)*100:.1f}%)")
        print()
    
    # Financial metrics
    print("Financial Metrics:")
    if 'total_capital_raised_usd' in df.columns:
        print(f"  Avg total raised: ${df['total_capital_raised_usd'].mean():,.0f}")
        print(f"  Median total raised: ${df['total_capital_raised_usd'].median():,.0f}")
    if 'annual_revenue_run_rate' in df.columns:
        revenue_data = df['annual_revenue_run_rate'].dropna()
        print(f"  Avg revenue (non-zero): ${revenue_data[revenue_data > 0].mean():,.0f}")
    if 'monthly_burn_usd' in df.columns:
        print(f"  Avg monthly burn: ${df['monthly_burn_usd'].mean():,.0f}")
    if 'runway_months' in df.columns:
        print(f"  Avg runway: {df['runway_months'].mean():.1f} months")
    print()
    
    # Team metrics
    print("Team Metrics:")
    if 'team_size_full_time' in df.columns:
        print(f"  Avg team size: {df['team_size_full_time'].mean():.1f}")
    if 'founders_count' in df.columns:
        print(f"  Avg founders: {df['founders_count'].mean():.1f}")
    if 'prior_successful_exits_count' in df.columns:
        print(f"  % with prior exits: {(df['prior_successful_exits_count'] > 0).mean()*100:.1f}%")
    print()
    
    # Data quality
    print("Data Quality Metrics:")
    missing_pct = (df.isnull().sum() / len(df) * 100)
    print(f"  Overall missing data: {missing_pct.mean():.1f}%")
    print(f"  Features with missing data: {(missing_pct > 0).sum()}")
    print("\n  Top 5 features with most missing data:")
    for col, pct in missing_pct.nlargest(5).items():
        print(f"    {col}: {pct:.1f}% missing")
    
    # Key validation checks
    print("\nData Validation Checks:")
    
    # Check if retention rates make sense
    if 'product_retention_30d' in df.columns and 'product_retention_90d' in df.columns:
        retention_valid = (df['product_retention_30d'] >= df['product_retention_90d']).mean()
        print(f"  Retention logic (30d >= 90d): {retention_valid*100:.1f}% valid")
    
    # Check market size relationships
    if all(col in df.columns for col in ['tam_size_usd', 'sam_size_usd', 'som_size_usd']):
        market_valid = ((df['tam_size_usd'] >= df['sam_size_usd']) & 
                       (df['sam_size_usd'] >= df['som_size_usd'])).mean()
        print(f"  Market size logic (TAM >= SAM >= SOM): {market_valid*100:.1f}% valid")
    
    # Check burn multiple calculation
    if all(col in df.columns for col in ['monthly_burn_usd', 'annual_revenue_run_rate', 'burn_multiple']):
        revenue_positive = df['annual_revenue_run_rate'] > 0
        calc_burn = df.loc[revenue_positive, 'monthly_burn_usd'] / (df.loc[revenue_positive, 'annual_revenue_run_rate'] / 12)
        actual_burn = df.loc[revenue_positive, 'burn_multiple']
        burn_accurate = (abs(calc_burn - actual_burn) < 0.1).mean()
        print(f"  Burn multiple calculation accuracy: {burn_accurate*100:.1f}%")
    
    # Success rate by stage
    if 'funding_stage' in df.columns and 'success' in df.columns:
        print("\nSuccess Rates by Funding Stage:")
        for stage in ['Pre-Seed', 'Seed', 'Series A', 'Series B', 'Series C+']:
            if stage in df['funding_stage'].values:
                stage_data = df[df['funding_stage'] == stage]['success'].dropna()
                if len(stage_data) > 0:
                    print(f"  {stage}: {stage_data.mean():.1%} (n={len(stage_data):,})")
    
    # Save detailed report
    report = {
        'dataset_overview': {
            'total_records': int(len(df)),
            'features': int(len(df.columns)),
            'memory_mb': float(df.memory_usage(deep=True).sum() / 1024**2)
        },
        'success_metrics': {
            'overall_rate': float(df['success'].mean()) if 'success' in df.columns else None,
            'records_with_outcome': int(df['success'].notna().sum()) if 'success' in df.columns else 0
        },
        'data_quality': {
            'missing_data_pct': float(missing_pct.mean()),
            'features_with_missing': int((missing_pct > 0).sum())
        },
        'financial_summary': {
            'avg_funding': float(df['total_capital_raised_usd'].mean()) if 'total_capital_raised_usd' in df.columns else 0,
            'median_funding': float(df['total_capital_raised_usd'].median()) if 'total_capital_raised_usd' in df.columns else 0
        }
    }
    
    with open('dataset_quality_report.json', 'w') as f:
        json.dump(report, f, indent=2)
    
    print("\nDetailed report saved to: dataset_quality_report.json")

if __name__ == "__main__":
    analyze_dataset()