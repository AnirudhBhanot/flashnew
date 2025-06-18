#!/usr/bin/env python3
"""
Generate TRULY realistic startup dataset without deterministic patterns
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import random

def generate_realistic_startup_data(n_samples=200000, seed=42):
    """Generate startup data with realistic patterns but no deterministic rules"""
    
    np.random.seed(seed)
    random.seed(seed)
    
    data = []
    
    for i in range(n_samples):
        # Base characteristics (no direct correlation with success)
        funding_stage = np.random.choice(
            ['pre_seed', 'seed', 'series_a', 'series_b', 'series_c'],
            p=[0.3, 0.35, 0.2, 0.1, 0.05]
        )
        
        # Stage multiplier for realistic scale
        stage_mult = {
            'pre_seed': 0.1, 'seed': 0.5, 'series_a': 1.0, 
            'series_b': 3.0, 'series_c': 10.0
        }[funding_stage]
        
        # Generate features with realistic distributions
        startup = {
            'startup_id': f"startup_{i:06d}",
            'funding_stage': funding_stage,
            
            # Capital features
            'total_capital_raised_usd': np.random.lognormal(14 + np.log(stage_mult), 1.5),
            'cash_on_hand_usd': np.random.lognormal(13 + np.log(stage_mult), 1.2),
            'monthly_burn_usd': np.random.lognormal(11 + np.log(stage_mult), 0.8),
            'runway_months': np.random.uniform(6, 36),
            'burn_multiple': np.random.lognormal(1.0, 0.5),
            'valuation_usd': np.random.lognormal(15 + np.log(stage_mult), 1.5),
            'ownership_founder_percent': np.random.uniform(10, 60),
            'last_funding_date_months_ago': np.random.uniform(0, 24),
            
            # Advantage features
            'customer_acquisition_cost': np.random.lognormal(3, 1.5),
            'customer_lifetime_value': np.random.lognormal(4, 1.5),
            'product_completeness_score': np.random.uniform(0.3, 1.0),
            'years_to_profitability': np.random.uniform(1, 7),
            'switching_cost_score': np.random.uniform(1, 5),
            'has_data_moat': np.random.choice([0, 1], p=[0.8, 0.2]),
            'regulatory_advantage_present': np.random.choice([0, 1], p=[0.9, 0.1]),
            'brand_strength_score': np.random.uniform(1, 5),
            'scalability_score': np.random.uniform(1, 5),
            
            # Market features
            'tam_size_usd': np.random.lognormal(20, 2),
            'sam_size_usd': np.random.lognormal(18, 1.5),
            'som_size_usd': np.random.lognormal(16, 1.5),
            'market_growth_rate_percent': np.random.normal(20, 15),
            'customer_count': int(np.random.lognormal(3 + np.log(stage_mult), 1.5)),
            'customer_concentration_percent': np.random.uniform(5, 50),
            'user_growth_rate_percent': np.random.normal(50, 30),
            'net_dollar_retention_percent': np.random.normal(110, 20),
            'competition_intensity': np.random.uniform(1, 5),
            'competitors_named_count': np.random.randint(2, 20),
            
            # People features
            'founders_count': np.random.randint(1, 4),
            'team_size_full_time': int(np.random.lognormal(2 + np.log(stage_mult), 0.8)),
            'years_experience_avg': np.random.uniform(3, 20),
            'domain_expertise_years_avg': np.random.uniform(2, 15),
            'prior_startup_experience_count': np.random.poisson(1.5),
            'prior_successful_exits_count': np.random.poisson(0.3),
            'board_advisor_experience_score': np.random.uniform(1, 5),
            'advisors_count': np.random.randint(0, 10),
            'team_diversity_percent': np.random.uniform(0, 100),
            'key_person_dependency': np.random.uniform(0, 1),  # Continuous, not binary!
            
            # Product features
            'product_stage': np.random.choice(['idea', 'prototype', 'mvp', 'beta', 'growth']),
            'product_retention_30d': np.random.beta(2, 5),  # Realistic retention
            'product_retention_90d': np.random.beta(1.5, 6),
            'dau_mau_ratio': np.random.beta(2, 8),
            'annual_revenue_run_rate': np.random.lognormal(10 + np.log(stage_mult), 2),
            'revenue_growth_rate_percent': np.random.normal(100, 50),
            'gross_margin_percent': np.random.uniform(20, 80),
            'ltv_cac_ratio': np.random.lognormal(0.5, 0.8),
            
            # Additional
            'sector': np.random.choice(['saas', 'marketplace', 'hardware', 'consumer', 'enterprise']),
            'investor_tier_primary': np.random.choice(['tier_1', 'tier_2', 'tier_3', 'none']),
            'team_experience_score': np.random.uniform(1, 10),
            'product_experience_score': np.random.uniform(1, 10)
        }
        
        # Calculate success probability based on multiple factors (not deterministic!)
        success_factors = []
        
        # Capital health
        if startup['runway_months'] > 18:
            success_factors.append(np.random.uniform(0.5, 0.7))
        else:
            success_factors.append(np.random.uniform(0.2, 0.4))
            
        # Growth metrics
        if startup['revenue_growth_rate_percent'] > 100:
            success_factors.append(np.random.uniform(0.6, 0.8))
        else:
            success_factors.append(np.random.uniform(0.3, 0.5))
            
        # Team quality
        if startup['prior_successful_exits_count'] > 0:
            success_factors.append(np.random.uniform(0.7, 0.9))
        else:
            success_factors.append(np.random.uniform(0.3, 0.5))
            
        # Market opportunity
        if startup['tam_size_usd'] > 1e9:
            success_factors.append(np.random.uniform(0.4, 0.6))
        else:
            success_factors.append(np.random.uniform(0.2, 0.4))
            
        # Product metrics
        if startup['ltv_cac_ratio'] > 3:
            success_factors.append(np.random.uniform(0.6, 0.8))
        else:
            success_factors.append(np.random.uniform(0.2, 0.4))
            
        # Combine factors with noise
        base_success_prob = np.mean(success_factors)
        
        # Add significant noise to prevent perfect prediction
        noise = np.random.normal(0, 0.2)
        final_success_prob = np.clip(base_success_prob + noise, 0.05, 0.95)
        
        # Determine success (target ~25% success rate)
        threshold = np.percentile([base_success_prob + np.random.normal(0, 0.2) for _ in range(1000)], 75)
        startup['success'] = 1 if final_success_prob > threshold else 0
        
        # Clip extreme values
        for key in startup:
            if isinstance(startup[key], (int, float)) and key not in ['success', 'has_data_moat', 'regulatory_advantage_present']:
                if startup[key] < 0:
                    startup[key] = 0
                    
        data.append(startup)
    
    # Create DataFrame
    df = pd.DataFrame(data)
    
    # Ensure ~25% success rate
    actual_success_rate = df['success'].mean()
    print(f"Actual success rate: {actual_success_rate:.1%}")
    
    # Save dataset
    df.to_csv('data/truly_realistic_startup_dataset.csv', index=False)
    print(f"Saved {len(df):,} samples to data/truly_realistic_startup_dataset.csv")
    
    # Verify no perfect correlations
    print("\nChecking for data leakage...")
    for col in df.columns:
        if col != 'success' and col != 'startup_id':
            if df[col].dtype in ['int64', 'float64']:
                corr = df[col].corr(df['success'])
                if abs(corr) > 0.8:
                    print(f"WARNING: High correlation found! {col}: {corr:.3f}")
    
    print("\nDataset statistics:")
    print(f"  Total samples: {len(df):,}")
    print(f"  Success rate: {df['success'].mean():.1%}")
    print(f"  Features: {len(df.columns) - 2}")  # Exclude startup_id and success
    
    return df


if __name__ == "__main__":
    print("Generating TRULY realistic startup dataset...")
    print("="*60)
    df = generate_realistic_startup_data(n_samples=50000)  # Smaller for faster testing
    
    print("\nSample correlations with success:")
    correlations = df.corr()['success'].sort_values(ascending=False)
    print(correlations.head(10))
    
    print("\nExpected: No single feature should have >0.5 correlation")
    print("This ensures models must combine multiple signals")