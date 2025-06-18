#!/usr/bin/env python3
"""
Analyze the generated 100k startup dataset to verify quality and patterns.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

def analyze_dataset(df_path: str = 'generated_100k_dataset.csv'):
    """Comprehensive analysis of the generated dataset."""
    print("Loading dataset...")
    df = pd.read_csv(df_path)
    
    print("\n" + "="*60)
    print("DATASET OVERVIEW")
    print("="*60)
    
    # Basic info
    print(f"\nDataset shape: {df.shape}")
    print(f"Memory usage: {df.memory_usage(deep=True).sum() / 1024**2:.1f} MB")
    
    # Feature completeness
    missing = df.isnull().sum()
    print(f"\nMissing values: {missing.sum()} total")
    if missing.sum() > 0:
        print("Columns with missing values:")
        print(missing[missing > 0])
    
    # Success distribution
    print(f"\nOverall success rate: {df['success'].mean():.2%}")
    print("\nSuccess by funding stage:")
    success_by_stage = df.groupby('funding_stage')['success'].agg(['mean', 'count'])
    success_by_stage.columns = ['Success Rate', 'Count']
    success_by_stage['Success Rate'] = success_by_stage['Success Rate'].map(lambda x: f"{x:.1%}")
    print(success_by_stage)
    
    # Industry distribution
    print("\nIndustry distribution:")
    industry_dist = df['sector'].value_counts()
    for industry, count in industry_dist.items():
        print(f"  {industry}: {count:,} ({count/len(df)*100:.1f}%)")
    
    # Key metrics by success
    print("\n" + "="*60)
    print("KEY METRICS BY SUCCESS")
    print("="*60)
    
    metrics = ['annual_revenue_run_rate', 'revenue_growth_rate_percent', 
               'burn_multiple', 'ltv_cac_ratio', 'product_retention_30d',
               'net_dollar_retention_percent', 'team_size_full_time']
    
    for metric in metrics:
        successful = df[df['success']][metric]
        failed = df[~df['success']][metric]
        
        # Remove extreme values for cleaner comparison
        successful_clean = successful[(successful > successful.quantile(0.01)) & 
                                    (successful < successful.quantile(0.99))]
        failed_clean = failed[(failed > failed.quantile(0.01)) & 
                            (failed < failed.quantile(0.99))]
        
        print(f"\n{metric}:")
        print(f"  Successful: mean={successful_clean.mean():.2f}, median={successful_clean.median():.2f}")
        print(f"  Failed: mean={failed_clean.mean():.2f}, median={failed_clean.median():.2f}")
        
        # Statistical test
        if len(successful_clean) > 30 and len(failed_clean) > 30:
            t_stat, p_value = stats.ttest_ind(successful_clean, failed_clean)
            print(f"  T-test p-value: {p_value:.2e} ({'Significant' if p_value < 0.05 else 'Not significant'})")
    
    # Correlations with success
    print("\n" + "="*60)
    print("TOP FEATURE CORRELATIONS WITH SUCCESS")
    print("="*60)
    
    # Convert success to numeric if it's boolean
    df['success_numeric'] = df['success'].astype(int)
    
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    correlations = df[numeric_cols].corr()['success_numeric'].sort_values(ascending=False)
    
    print("\nTop positive correlations:")
    for col, corr in correlations[1:11].items():
        print(f"  {col}: {corr:.3f}")
    
    print("\nTop negative correlations:")
    for col, corr in correlations[-10:].items():
        print(f"  {col}: {corr:.3f}")
    
    # Logical consistency checks
    print("\n" + "="*60)
    print("LOGICAL CONSISTENCY CHECKS")
    print("="*60)
    
    # Check burn multiple calculation
    df['burn_multiple_check'] = np.where(
        df['annual_revenue_run_rate'] > 0,
        df['monthly_burn_usd'] / (df['annual_revenue_run_rate'] / 12),
        999
    )
    burn_diff = abs(df['burn_multiple'] - df['burn_multiple_check'])
    print(f"\nBurn multiple calculation accuracy: {(burn_diff < 0.1).mean():.1%}")
    
    # Check runway calculation
    df['runway_check'] = np.where(
        df['monthly_burn_usd'] > 0,
        df['cash_on_hand_usd'] / df['monthly_burn_usd'],
        999
    )
    runway_diff = abs(df['runway_months'] - df['runway_check'])
    print(f"Runway calculation accuracy: {(runway_diff < 1).mean():.1%}")
    
    # Check retention relationship (30d should be >= 90d)
    retention_logical = df['product_retention_30d'] >= df['product_retention_90d']
    print(f"Retention logic (30d >= 90d): {retention_logical.mean():.1%}")
    
    # Check market size relationship (TAM >= SAM >= SOM)
    market_logical = (df['tam_size_usd'] >= df['sam_size_usd']) & \
                    (df['sam_size_usd'] >= df['som_size_usd'])
    print(f"Market size logic (TAM >= SAM >= SOM): {market_logical.mean():.1%}")
    
    # Feature distributions
    print("\n" + "="*60)
    print("FEATURE DISTRIBUTIONS")
    print("="*60)
    
    # Create visualizations
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    axes = axes.flatten()
    
    # Revenue distribution
    revenue_log = np.log1p(df['annual_revenue_run_rate'])
    axes[0].hist(revenue_log[revenue_log > 0], bins=50, alpha=0.7)
    axes[0].set_title('Log(Annual Revenue)')
    axes[0].set_xlabel('Log(Revenue)')
    
    # Growth rate distribution
    growth = df['revenue_growth_rate_percent']
    axes[1].hist(growth[(growth > -50) & (growth < 300)], bins=50, alpha=0.7)
    axes[1].set_title('Revenue Growth Rate %')
    axes[1].set_xlabel('Growth Rate %')
    
    # Team size distribution
    team_log = np.log1p(df['team_size_full_time'])
    axes[2].hist(team_log, bins=50, alpha=0.7)
    axes[2].set_title('Log(Team Size)')
    axes[2].set_xlabel('Log(Team Size)')
    
    # LTV/CAC distribution
    ltv_cac = df['ltv_cac_ratio']
    axes[3].hist(ltv_cac[(ltv_cac > 0) & (ltv_cac < 10)], bins=50, alpha=0.7)
    axes[3].set_title('LTV/CAC Ratio')
    axes[3].set_xlabel('LTV/CAC')
    
    # Burn multiple distribution
    burn = df['burn_multiple']
    axes[4].hist(burn[(burn > 0) & (burn < 50)], bins=50, alpha=0.7)
    axes[4].set_title('Burn Multiple')
    axes[4].set_xlabel('Burn Multiple')
    
    # Success by stage
    stage_success = df.groupby('funding_stage')['success'].mean().sort_values()
    axes[5].bar(range(len(stage_success)), stage_success.values)
    axes[5].set_xticks(range(len(stage_success)))
    axes[5].set_xticklabels(stage_success.index, rotation=45)
    axes[5].set_title('Success Rate by Stage')
    axes[5].set_ylabel('Success Rate')
    
    plt.tight_layout()
    plt.savefig('dataset_analysis.png', dpi=300, bbox_inches='tight')
    print("\nSaved visualization to dataset_analysis.png")
    
    # Save detailed statistics
    print("\nGenerating detailed statistics report...")
    with open('dataset_statistics.txt', 'w') as f:
        f.write("="*60 + "\n")
        f.write("GENERATED DATASET STATISTICS\n")
        f.write("="*60 + "\n\n")
        
        f.write(f"Total records: {len(df):,}\n")
        f.write(f"Success rate: {df['success'].mean():.2%}\n\n")
        
        f.write("Numeric features summary:\n")
        f.write(df.describe().to_string())
        
        f.write("\n\nCategorical features:\n")
        for col in df.select_dtypes(include=['object', 'bool']).columns:
            f.write(f"\n{col}:\n")
            f.write(df[col].value_counts().head(10).to_string())
            f.write("\n")
    
    print("Saved detailed statistics to dataset_statistics.txt")
    
    return df

if __name__ == "__main__":
    analyze_dataset()