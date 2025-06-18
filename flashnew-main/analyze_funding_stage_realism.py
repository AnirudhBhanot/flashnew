import pandas as pd
import numpy as np

# Load the dataset
df = pd.read_csv('real_startup_data_100k.csv')

# Create a detailed analysis by funding stage
stages = ['pre_seed', 'seed', 'series_a', 'series_b', 'series_c', 'series_d']

print("=" * 80)
print("FUNDING STAGE REALISM ANALYSIS")
print("=" * 80)

for stage in stages:
    stage_df = df[df['funding_stage'] == stage]
    print(f"\n{stage.upper()} STAGE ({len(stage_df)} companies)")
    print("-" * 60)
    
    # Key metrics to analyze
    metrics = {
        'total_capital_raised_usd': 'Total Capital Raised (USD)',
        'team_size_full_time': 'Team Size',
        'customer_count': 'Customer Count',
        'annual_revenue_run_rate': 'Annual Revenue (USD)',
        'revenue_growth_rate_percent': 'Revenue Growth Rate (%)',
        'monthly_burn_usd': 'Monthly Burn (USD)',
        'runway_months': 'Runway (months)',
        'product_stage': 'Product Stage'
    }
    
    for col, name in metrics.items():
        if col == 'product_stage':
            # For product stage, show distribution
            print(f"\n{name} Distribution:")
            stage_counts = stage_df[col].value_counts()
            for ps, count in stage_counts.items():
                print(f"  {ps}: {count} ({count/len(stage_df)*100:.1f}%)")
        else:
            # For numeric metrics, show statistics
            data = stage_df[col]
            print(f"\n{name}:")
            print(f"  Mean: ${data.mean():,.0f}" if 'usd' in col or col == 'annual_revenue_run_rate' else f"  Mean: {data.mean():.1f}")
            print(f"  Median: ${data.median():,.0f}" if 'usd' in col or col == 'annual_revenue_run_rate' else f"  Median: {data.median():.1f}")
            print(f"  Min: ${data.min():,.0f}" if 'usd' in col or col == 'annual_revenue_run_rate' else f"  Min: {data.min():.1f}")
            print(f"  Max: ${data.max():,.0f}" if 'usd' in col or col == 'annual_revenue_run_rate' else f"  Max: {data.max():.1f}")
            
            # For pre-seed and seed, check percentage with significant revenue/customers
            if stage in ['pre_seed', 'seed'] and col in ['annual_revenue_run_rate', 'customer_count']:
                if col == 'annual_revenue_run_rate':
                    high_revenue = (data > 100000).sum()
                    print(f"  Companies with >$100k revenue: {high_revenue} ({high_revenue/len(stage_df)*100:.1f}%)")
                elif col == 'customer_count':
                    high_customers = (data > 100).sum()
                    print(f"  Companies with >100 customers: {high_customers} ({high_customers/len(stage_df)*100:.1f}%)")

print("\n" + "=" * 80)
print("UNREALISTIC PATTERNS IDENTIFIED:")
print("=" * 80)

# Check for unrealistic patterns
issues = []

# Pre-seed companies with high metrics
preseed_df = df[df['funding_stage'] == 'pre_seed']
preseed_high_revenue = preseed_df[preseed_df['annual_revenue_run_rate'] > 100000]
issues.append(f"1. {len(preseed_high_revenue)} pre-seed companies ({len(preseed_high_revenue)/len(preseed_df)*100:.1f}%) have >$100k ARR")
issues.append(f"   - Average ARR for these companies: ${preseed_high_revenue['annual_revenue_run_rate'].mean():,.0f}")

preseed_large_teams = preseed_df[preseed_df['team_size_full_time'] > 10]
issues.append(f"\n2. {len(preseed_large_teams)} pre-seed companies ({len(preseed_large_teams)/len(preseed_df)*100:.1f}%) have >10 employees")
issues.append(f"   - Average team size for these companies: {preseed_large_teams['team_size_full_time'].mean():.0f}")

# Seed companies with unrealistic metrics
seed_df = df[df['funding_stage'] == 'seed']
seed_high_revenue = seed_df[seed_df['annual_revenue_run_rate'] > 1000000]
issues.append(f"\n3. {len(seed_high_revenue)} seed companies ({len(seed_high_revenue)/len(seed_df)*100:.1f}%) have >$1M ARR")

# Check funding progression
avg_funding_by_stage = df.groupby('funding_stage')['total_capital_raised_usd'].mean()
issues.append("\n4. Average funding by stage shows unrealistic progression:")
for stage in stages:
    if stage in avg_funding_by_stage.index:
        issues.append(f"   - {stage}: ${avg_funding_by_stage[stage]:,.0f}")

# Product stage misalignment
preseed_growth = preseed_df[preseed_df['product_stage'] == 'growth']
issues.append(f"\n5. {len(preseed_growth)} pre-seed companies are already at 'growth' stage")

for issue in issues:
    print(issue)

print("\n" + "=" * 80)
print("SPECIFIC EXAMPLES OF UNREALISTIC PRE-SEED COMPANIES:")
print("=" * 80)

# Show specific examples
unrealistic_preseed = preseed_df[
    (preseed_df['annual_revenue_run_rate'] > 200000) | 
    (preseed_df['customer_count'] > 1000) |
    (preseed_df['team_size_full_time'] > 20)
].head(10)

for idx, row in unrealistic_preseed.iterrows():
    print(f"\nCompany {row['company_id']}:")
    print(f"  - Annual Revenue: ${row['annual_revenue_run_rate']:,.0f}")
    print(f"  - Customers: {row['customer_count']:,}")
    print(f"  - Team Size: {row['team_size_full_time']}")
    print(f"  - Product Stage: {row['product_stage']}")
    print(f"  - Total Raised: ${row['total_capital_raised_usd']:,.0f}")