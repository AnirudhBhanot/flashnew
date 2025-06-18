#!/usr/bin/env python3
"""
Analyze the complete dataset to identify areas for improvement.
"""

import pandas as pd
import numpy as np
import json

def analyze_dataset():
    # Load the complete dataset
    df = pd.read_csv('complete_high_quality_startup_dataset_100k.csv')
    
    print('=== COMPLETE DATASET ANALYSIS ===')
    print(f'Total records: {len(df):,}')
    print(f'Unique companies: {df["company_id"].nunique():,}')
    print(f'Years covered: {df["year"].min()} - {df["year"].max()}')
    print(f'Features: {len(df.columns)}')
    
    print('\n=== LONGITUDINAL TRACKING ===')
    years_per_company = df.groupby('company_id')['year'].count()
    print(f'Average years tracked: {years_per_company.mean():.1f}')
    print(f'Max years tracked: {years_per_company.max()}')
    print(f'Companies with 5+ years: {(years_per_company >= 5).sum():,}')
    
    print('\n=== OUTCOMES ===')
    # Get final outcome for each company
    final_outcomes = df.groupby('company_id').last()
    outcomes = final_outcomes['outcome'].value_counts()
    for outcome, count in outcomes.items():
        print(f'{outcome}: {count:,} ({count/df["company_id"].nunique()*100:.1f}%)')
    
    print('\n=== SUCCESS RATES BY STAGE ===')
    for stage in ['Pre-Seed', 'Seed', 'Series A', 'Series B', 'Series C+']:
        stage_data = df[df['funding_stage'] == stage]
        if len(stage_data) > 0:
            success_rate = stage_data['success'].mean()
            print(f'{stage}: {success_rate:.1%} (n={len(stage_data):,})')
    
    print('\n=== REVENUE ANALYSIS ===')
    revenue_data = df[df['annual_revenue_run_rate'] > 0]
    print(f'Companies with revenue: {revenue_data["company_id"].nunique():,}')
    if len(revenue_data) > 0:
        print(f'Avg revenue (when > 0): ${revenue_data["annual_revenue_run_rate"].mean():,.0f}')
        print(f'Median revenue (when > 0): ${revenue_data["annual_revenue_run_rate"].median():,.0f}')
    
    print('\n=== CRITICAL ISSUES FOUND ===')
    
    # 1. Revenue issue
    zero_revenue_pct = (df['annual_revenue_run_rate'] == 0).mean()
    print(f'1. Records with $0 revenue: {zero_revenue_pct:.1%} ❌')
    print('   - This is unrealistic - most companies have some revenue after year 1')
    
    # 2. Market sentiment issue
    print(f'\n2. Market sentiment range: {df["market_sentiment"].min():.2f} - {df["market_sentiment"].max():.2f} ❌')
    print('   - All values are 0.50 (no variation)')
    
    # 3. Geographic distribution
    print(f'\n3. Location distribution:')
    location_dist = df.groupby('company_id')['location'].first().value_counts()
    for loc, count in location_dist.head().items():
        print(f'   - {loc}: {count:,} ({count/df["company_id"].nunique()*100:.1f}%)')
    
    # 4. Funding progression
    print(f'\n4. Funding progression issues:')
    # Check if companies progress through stages
    company_stages = df.groupby('company_id')['funding_stage'].apply(list)
    stuck_in_stage = (company_stages.apply(lambda x: len(set(x)) == 1)).mean()
    print(f'   - Companies stuck in one stage: {stuck_in_stage:.1%}')
    
    # 5. Outcome timing
    print(f'\n5. Outcome timing:')
    ipo_companies = df[df['outcome'] == 'ipo'].groupby('company_id')['years_since_founding'].max()
    if len(ipo_companies) > 0:
        print(f'   - Avg years to IPO: {ipo_companies.mean():.1f}')
        print(f'   - Min years to IPO: {ipo_companies.min()}')
    
    # 6. Missing pivots
    print(f'\n6. Business model changes:')
    print('   - No pivot tracking implemented ❌')
    print('   - No industry changes tracked ❌')
    
    # 7. Customer metrics
    customer_data = df[df['customer_count'] > 0]
    print(f'\n7. Customer metrics:')
    print(f'   - Records with customers: {len(customer_data):,} ({len(customer_data)/len(df)*100:.1f}%)')
    
    print('\n=== RECOMMENDATIONS FOR IMPROVEMENT ===')
    print('1. Fix revenue generation - companies should have revenue after seed stage')
    print('2. Fix market sentiment - should vary with real market events')
    print('3. Add realistic pivots - 30-50% of startups pivot')
    print('4. Add burn rate variations based on market conditions')
    print('5. Add competitive dynamics - more competitors = harder to succeed')
    print('6. Add founder learning - serial entrepreneurs should do better')
    print('7. Add industry-specific failure patterns')
    print('8. Add COVID/crisis impacts on specific industries')
    print('9. Add realistic customer acquisition costs by channel')
    print('10. Add technical debt and scaling challenges')

if __name__ == "__main__":
    analyze_dataset()