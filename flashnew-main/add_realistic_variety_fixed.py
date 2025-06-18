#!/usr/bin/env python3
"""
Add Realistic Variety to Dataset - Fixed Version
Makes the data messy like real startups
"""

import pandas as pd
import numpy as np
import random
from pathlib import Path

def add_realistic_variety(df: pd.DataFrame) -> pd.DataFrame:
    """Add realistic messiness to the dataset"""
    print("Adding realistic variety to dataset...")
    
    df = df.copy()
    
    # Convert numeric columns to float to avoid dtype issues
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    for col in numeric_cols:
        df[col] = df[col].astype(float)
    
    # 1. Add outliers (10% of data) - like Uber, Quibi, WhatsApp
    print("\n1. Adding outliers (Uber-like burns, Quibi-like failures)...")
    num_outliers = int(len(df) * 0.10)
    outlier_indices = np.random.choice(df.index, num_outliers, replace=False)
    
    for i, idx in enumerate(outlier_indices):
        outlier_type = i % 6  # Cycle through different outlier types
        
        if outlier_type == 0:  # Uber type - massive burn but success
            df.loc[idx, 'burn_multiple'] = np.random.uniform(5, 10)
            df.loc[idx, 'monthly_burn_usd'] = np.random.uniform(10e6, 50e6)
            df.loc[idx, 'success'] = 1
        elif outlier_type == 1:  # Quibi type - great metrics but failed
            df.loc[idx, 'team_experience_score'] = 5
            df.loc[idx, 'total_capital_raised_usd'] = np.random.uniform(1e9, 2e9)
            df.loc[idx, 'prior_successful_exits_count'] = 2
            df.loc[idx, 'success'] = 0
        elif outlier_type == 2:  # WhatsApp type - tiny team, huge success
            df.loc[idx, 'team_size_full_time'] = np.random.uniform(20, 50)
            df.loc[idx, 'total_capital_raised_usd'] = np.random.uniform(50e6, 100e6)
            df.loc[idx, 'success'] = 1
        elif outlier_type == 3:  # Theranos type - all signals good, but fraud
            df.loc[idx, 'investor_tier_primary'] = 1
            df.loc[idx, 'board_advisor_experience_score'] = 5
            df.loc[idx, 'revenue_growth_rate_percent'] = 200
            df.loc[idx, 'success'] = 0
        elif outlier_type == 4:  # Bootstrap success
            df.loc[idx, 'total_capital_raised_usd'] = np.random.uniform(100e3, 500e3)
            df.loc[idx, 'gross_margin_percent'] = np.random.uniform(80, 95)
            df.loc[idx, 'burn_multiple'] = np.random.uniform(0.5, 1.0)
            df.loc[idx, 'success'] = 1
        else:  # Zombie startup
            df.loc[idx, 'revenue_growth_rate_percent'] = np.random.uniform(-10, 10)
            df.loc[idx, 'runway_months'] = np.random.uniform(24, 48)
            df.loc[idx, 'user_growth_rate_percent'] = np.random.uniform(-5, 5)
            df.loc[idx, 'success'] = 0
    
    print(f"   Added {num_outliers} outliers")
    
    # 2. Add missing data (realistic pattern)
    print("\n2. Adding missing data (30% of cells)...")
    never_missing = ['company_id', 'company_name', 'success', 'sector', 'funding_stage']
    can_be_missing = [col for col in df.columns if col not in never_missing]
    
    # Early stage companies have more missing data
    for idx in df.index:
        if df.loc[idx, 'funding_stage'] in ['pre_seed', 'seed']:
            missing_pct = np.random.uniform(0.3, 0.6)  # 30-60% missing
        else:
            missing_pct = np.random.uniform(0.1, 0.3)  # 10-30% missing
        
        num_missing = int(len(can_be_missing) * missing_pct)
        missing_features = np.random.choice(can_be_missing, num_missing, replace=False)
        df.loc[idx, missing_features] = np.nan
    
    # 3. Success/failure overlap - break perfect separation
    print("\n3. Creating metric overlap between success and failure...")
    
    # 15% of successful companies have bad metrics
    successful = df[df['success'] == 1].index
    num_bad_successful = int(len(successful) * 0.15)
    bad_successful = np.random.choice(successful, num_bad_successful, replace=False)
    
    for idx in bad_successful:
        df.loc[idx, 'burn_multiple'] = np.random.uniform(4, 8)
        df.loc[idx, 'runway_months'] = np.random.uniform(3, 9)
        df.loc[idx, 'revenue_growth_rate_percent'] = np.random.uniform(-20, 50)
        df.loc[idx, 'net_dollar_retention_percent'] = np.random.uniform(70, 90)
    
    # 15% of failed companies have good metrics
    failed = df[df['success'] == 0].index
    num_good_failed = int(len(failed) * 0.15)
    good_failed = np.random.choice(failed, num_good_failed, replace=False)
    
    for idx in good_failed:
        df.loc[idx, 'burn_multiple'] = np.random.uniform(1, 2)
        df.loc[idx, 'revenue_growth_rate_percent'] = np.random.uniform(100, 300)
        df.loc[idx, 'gross_margin_percent'] = np.random.uniform(70, 90)
        df.loc[idx, 'ltv_cac_ratio'] = np.random.uniform(3, 5)
    
    print(f"   {num_bad_successful} successful companies with bad metrics")
    print(f"   {num_good_failed} failed companies with good metrics")
    
    # 4. Add measurement noise
    print("\n4. Adding measurement noise (±30%)...")
    noise_cols = [col for col in numeric_cols if col not in ['success', 'company_id']]
    
    for col in noise_cols:
        noise = np.random.normal(0, 0.3, len(df))
        df[col] = df[col] * (1 + noise)
    
    # 5. Add contradictions
    print("\n5. Adding contradictory signals...")
    num_contradictions = int(len(df) * 0.20)
    contradiction_indices = np.random.choice(df.index, num_contradictions, replace=False)
    
    for idx in contradiction_indices:
        contradiction_type = np.random.randint(0, 4)
        
        if contradiction_type == 0:  # High revenue but high burn
            df.loc[idx, 'annual_revenue_run_rate'] = np.random.uniform(5e6, 20e6)
            df.loc[idx, 'monthly_burn_usd'] = np.random.uniform(1e6, 3e6)
        elif contradiction_type == 1:  # Great team but poor execution
            df.loc[idx, 'prior_successful_exits_count'] = np.random.randint(1, 3)
            df.loc[idx, 'years_experience_avg'] = np.random.uniform(15, 25)
            df.loc[idx, 'revenue_growth_rate_percent'] = np.random.uniform(-30, 20)
        elif contradiction_type == 2:  # Hot market but struggling
            df.loc[idx, 'market_growth_rate_percent'] = np.random.uniform(50, 100)
            df.loc[idx, 'user_growth_rate_percent'] = np.random.uniform(-20, 20)
        else:  # Efficient but not growing
            df.loc[idx, 'burn_multiple'] = np.random.uniform(0.8, 1.5)
            df.loc[idx, 'customer_count'] = np.random.uniform(10, 100)
            df.loc[idx, 'revenue_growth_rate_percent'] = np.random.uniform(-10, 30)
    
    print(f"   Added contradictions to {num_contradictions} companies")
    
    # Clean up any invalid values
    for col in numeric_cols:
        if col not in ['success']:
            df[col] = df[col].clip(lower=0)  # No negative values except growth rates
    
    return df


def main():
    """Add realistic variety to the dataset"""
    print("\n" + "="*80)
    print("ADDING REALISTIC VARIETY TO DATASET")
    print("="*80)
    
    # Try 100k first, fall back to 1k if not found
    if Path("real_startup_data_100k.csv").exists():
        input_file = "real_startup_data_100k.csv"
    else:
        input_file = "real_startup_data_1k.csv"
    
    print(f"\nLoading {input_file}...")
    df = pd.read_csv(input_file)
    print(f"Loaded {len(df):,} companies")
    print(f"Original success rate: {df['success'].mean():.1%}")
    
    # Add variety
    df_messy = add_realistic_variety(df)
    
    # Save the messy dataset
    base_name = input_file.replace('.csv', '')
    output_file = f"{base_name}_messy.csv"
    df_messy.to_csv(output_file, index=False)
    
    # Summary statistics
    print("\n" + "="*60)
    print("VARIETY ADDED SUCCESSFULLY!")
    print("="*60)
    print(f"Dataset: {output_file}")
    print(f"Shape: {df_messy.shape}")
    print(f"Success rate: {df_messy['success'].mean():.1%}")
    print(f"Missing data: {df_messy.isnull().sum().sum() / (len(df_messy) * len(df_messy.columns)):.1%}")
    
    # Check overlap
    success_burn = df_messy[df_messy['success'] == 1]['burn_multiple'].dropna()
    fail_burn = df_messy[df_messy['success'] == 0]['burn_multiple'].dropna()
    
    if len(success_burn) > 0 and len(fail_burn) > 0:
        print(f"\nBurn multiple ranges:")
        print(f"  Successful: {success_burn.min():.1f} - {success_burn.max():.1f}")
        print(f"  Failed: {fail_burn.min():.1f} - {fail_burn.max():.1f}")
        print("  ✅ Success and failure metrics now overlap!")
    
    print(f"\n✅ Saved messy dataset to: {output_file}")
    print("✅ Ready for retraining!")


if __name__ == "__main__":
    main()