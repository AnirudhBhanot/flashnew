#!/usr/bin/env python3
"""
Analyze the generated real patterns dataset
"""

import pandas as pd
import numpy as np

# Load the dataset
df = pd.read_csv('data/real_patterns_startup_dataset_200k.csv')

print('='*80)
print('REAL PATTERNS STARTUP DATASET SUMMARY')
print('='*80)

print(f'\nDataset shape: {df.shape[0]:,} rows, {df.shape[1]} columns')
print(f'Success rate: {df["success"].mean():.1%}')

print('\n1. SUCCESS DISTRIBUTION BY OUTCOME TYPE:')
print(df.groupby('outcome_type')['success'].agg(['sum', 'count', 'mean']).round(3))

print('\n2. KEY METRICS BY SUCCESS/FAILURE:')
metrics = ['annual_revenue_run_rate', 'burn_multiple', 'runway_months', 
           'revenue_growth_rate_percent', 'net_dollar_retention_percent']
for metric in metrics:
    failed_mean = df[df['success']==0][metric].mean()
    success_mean = df[df['success']==1][metric].mean()
    print(f'\n{metric}:')
    print(f'  Failed:  {failed_mean:,.0f}')
    print(f'  Success: {success_mean:,.0f}')
    print(f'  Ratio:   {success_mean/failed_mean:.1f}x')

print('\n3. REALISTIC PATTERNS IN THE DATA:')
print('\n- Team Experience:')
print(f'  Failed startups:  {df[df["success"]==0]["prior_successful_exits_count"].mean():.2f} prior exits')
print(f'  Success startups: {df[df["success"]==1]["prior_successful_exits_count"].mean():.2f} prior exits')

print('\n- Capital Efficiency:')
failed_eff = df[df['success']==0]['annual_revenue_run_rate'] / df[df['success']==0]['total_capital_raised_usd']
success_eff = df[df['success']==1]['annual_revenue_run_rate'] / df[df['success']==1]['total_capital_raised_usd']
print(f'  Failed:  ${failed_eff.mean():.2f} revenue per $1 raised')
print(f'  Success: ${success_eff.mean():.2f} revenue per $1 raised')

print('\n- Product Retention:')
print(f'  Failed:  {df[df["success"]==0]["product_retention_30d"].mean():.1%} 30-day retention')
print(f'  Success: {df[df["success"]==1]["product_retention_30d"].mean():.1%} 30-day retention')

print('\n4. MOST PREDICTIVE FEATURES (Correlation with Success):')
numeric_cols = df.select_dtypes(include=[np.number]).columns
correlations = df[numeric_cols].corr()['success'].sort_values(ascending=False)
print(correlations.head(15))

print('\n5. SAMPLE DATA POINTS:')
print('\nSuccessful IPO example:')
ipo_example = df[df['outcome_type'] == 'successful_ipo'].iloc[0]
print(f"  Revenue: ${ipo_example['annual_revenue_run_rate']:,.0f}")
print(f"  Growth: {ipo_example['revenue_growth_rate_percent']:.0f}%")
print(f"  Team size: {ipo_example['team_size_full_time']}")
print(f"  Burn multiple: {ipo_example['burn_multiple']:.1f}")

print('\nFailed (no market) example:')
failed_example = df[df['outcome_type'] == 'failed_no_market'].iloc[0]
print(f"  Revenue: ${failed_example['annual_revenue_run_rate']:,.0f}")
print(f"  Growth: {failed_example['revenue_growth_rate_percent']:.0f}%")  
print(f"  Customer count: {failed_example['customer_count']}")
print(f"  CAC/LTV ratio: {failed_example['ltv_cac_ratio']:.1f}")

print('\n' + '='*80)
print('DATASET READY FOR TRAINING WITH REAL PATTERNS!')
print('='*80)