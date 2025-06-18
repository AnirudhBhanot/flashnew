#!/usr/bin/env python3
"""Analyze the new features to understand why improvement is minimal"""
import pandas as pd
import numpy as np

# Load the enhanced dataset
df = pd.read_csv('data/final_100k_dataset_75features.csv')

# Get the new features (those not in the original 45)
original_features = [
    'funding_stage', 'total_capital_raised_usd', 'cash_on_hand_usd', 'monthly_burn_usd',
    'runway_months', 'annual_revenue_run_rate', 'revenue_growth_rate_percent',
    'gross_margin_percent', 'burn_multiple', 'ltv_cac_ratio', 'investor_tier_primary',
    'has_debt', 'patent_count', 'network_effects_present', 'has_data_moat',
    'regulatory_advantage_present', 'tech_differentiation_score', 'switching_cost_score',
    'brand_strength_score', 'scalability_score', 'product_stage', 'product_retention_30d',
    'product_retention_90d', 'sector', 'tam_size_usd', 'sam_size_usd', 'som_size_usd',
    'market_growth_rate_percent', 'customer_count', 'customer_concentration_percent',
    'user_growth_rate_percent', 'net_dollar_retention_percent', 'competition_intensity',
    'competitors_named_count', 'dau_mau_ratio', 'founders_count', 'team_size_full_time',
    'years_experience_avg', 'domain_expertise_years_avg', 'prior_startup_experience_count',
    'prior_successful_exits_count', 'board_advisor_experience_score', 'advisors_count',
    'team_diversity_percent', 'key_person_dependency'
]

new_features = [col for col in df.columns if col not in original_features and col != 'success']

print(f'Total new features: {len(new_features)}')
print('\nCorrelation with target for new features:')
print('Feature                                   Correlation  Variance')
print('-' * 65)

# Calculate correlations and variance for numeric features
correlations = []
for feat in sorted(new_features):
    if feat in df.columns and df[feat].dtype in ['float64', 'int64']:
        corr = df[feat].corr(df['success'])
        var = df[feat].var()
        correlations.append((feat, corr, var))

# Sort by absolute correlation
correlations.sort(key=lambda x: abs(x[1]), reverse=True)

for feat, corr, var in correlations:
    print(f'{feat:40s} {corr:7.4f}     {var:10.2f}')

print('\n\nChecking if new features are mostly derived from existing ones...')
# Sample some values to check
print('\nSample values for key new features:')
sample_cols = ['monthly_revenue_growth_rate', 'burn_months_remaining', 'revenue_per_employee']
print(df[sample_cols].describe())

# Check correlation between new and old features
print('\n\nChecking high correlations between new and existing features:')
for new_feat in ['monthly_revenue_growth_rate', 'burn_months_remaining', 'revenue_per_employee']:
    if new_feat in df.columns:
        print(f'\n{new_feat}:')
        for old_feat in ['revenue_growth_rate_percent', 'runway_months', 'annual_revenue_run_rate']:
            if old_feat in df.columns:
                corr = df[new_feat].corr(df[old_feat])
                print(f'  vs {old_feat}: {corr:.4f}')