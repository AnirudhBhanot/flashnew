#!/usr/bin/env python3
"""Generate realistic training data for FLASH models"""

import pandas as pd
import numpy as np
from feature_config import ALL_FEATURES as CANONICAL_FEATURES

def generate_training_data(n_samples=10000):
    """Generate realistic startup training data"""
    
    np.random.seed(42)
    data = []
    
    for i in range(n_samples):
        # Determine startup quality (0-1)
        quality = np.random.beta(2, 5)  # Skewed towards lower quality (realistic)
        
        # Funding stage distribution
        stage_probs = [0.3, 0.3, 0.2, 0.15, 0.05]  # pre_seed, seed, a, b, c
        funding_stage = np.random.choice(['pre_seed', 'seed', 'series_a', 'series_b', 'series_c'], p=stage_probs)
        
        # Generate correlated features based on quality
        startup = {}
        
        # Capital features
        if quality > 0.7:
            startup['total_capital_raised_usd'] = np.random.lognormal(15, 1.5)  # $1M - $100M
            startup['runway_months'] = np.random.uniform(18, 36)
            startup['burn_multiple'] = np.random.uniform(0.8, 2)
            startup['gross_margin_percent'] = np.random.uniform(60, 85)
        elif quality > 0.4:
            startup['total_capital_raised_usd'] = np.random.lognormal(13, 1.5)  # $100K - $10M
            startup['runway_months'] = np.random.uniform(12, 24)
            startup['burn_multiple'] = np.random.uniform(1.5, 3.5)
            startup['gross_margin_percent'] = np.random.uniform(40, 70)
        else:
            startup['total_capital_raised_usd'] = np.random.lognormal(11, 1.5)  # $10K - $1M
            startup['runway_months'] = np.random.uniform(3, 12)
            startup['burn_multiple'] = np.random.uniform(3, 10)
            startup['gross_margin_percent'] = np.random.uniform(-20, 50)
        
        startup['cash_on_hand_usd'] = startup['total_capital_raised_usd'] * np.random.uniform(0.3, 0.8)
        startup['monthly_burn_usd'] = startup['cash_on_hand_usd'] / max(startup['runway_months'], 1)
        startup['investor_tier_primary'] = 1 if quality > 0.6 else 0
        startup['has_debt'] = 1 if np.random.rand() < (1 - quality) * 0.3 else 0
        
        # Advantage features
        startup['patent_count'] = np.random.poisson(quality * 5)
        startup['network_effects_present'] = 1 if np.random.rand() < quality * 0.6 else 0
        startup['has_data_moat'] = 1 if np.random.rand() < quality * 0.4 else 0
        startup['regulatory_advantage_present'] = 1 if np.random.rand() < quality * 0.3 else 0
        startup['tech_differentiation_score'] = min(5, max(1, int(np.random.normal(1 + quality * 4, 0.5))))
        startup['switching_cost_score'] = min(5, max(1, int(np.random.normal(1 + quality * 4, 0.5))))
        startup['brand_strength_score'] = min(5, max(1, int(np.random.normal(1 + quality * 4, 0.5))))
        startup['scalability_score'] = min(5, max(1, int(np.random.normal(1 + quality * 4, 0.5))))
        
        # Market features
        if quality > 0.7:
            startup['tam_size_usd'] = np.random.lognormal(22, 1)  # $1B - $100B
            startup['market_growth_rate_percent'] = np.random.uniform(20, 50)
            startup['ltv_cac_ratio'] = np.random.uniform(3, 5)
        elif quality > 0.4:
            startup['tam_size_usd'] = np.random.lognormal(20, 1)  # $100M - $10B
            startup['market_growth_rate_percent'] = np.random.uniform(10, 30)
            startup['ltv_cac_ratio'] = np.random.uniform(1.5, 3)
        else:
            startup['tam_size_usd'] = np.random.lognormal(18, 1)  # $10M - $1B
            startup['market_growth_rate_percent'] = np.random.uniform(-10, 20)
            startup['ltv_cac_ratio'] = np.random.uniform(0.5, 2)
            
        startup['sam_size_usd'] = startup['tam_size_usd'] * np.random.uniform(0.05, 0.2)
        startup['som_size_usd'] = startup['sam_size_usd'] * np.random.uniform(0.05, 0.2)
        startup['sector'] = 0  # Simplified
        startup['customer_count'] = int(np.random.lognormal(2 + quality * 4, 1.5))
        startup['customer_concentration_percent'] = max(0, min(100, np.random.normal(50 - quality * 40, 10)))
        startup['user_growth_rate_percent'] = np.random.normal(quality * 100 - 20, 20)
        startup['net_dollar_retention_percent'] = np.random.normal(80 + quality * 40, 10)
        startup['competition_intensity'] = min(5, max(1, int(np.random.normal(4 - quality * 3, 0.5))))
        startup['competitors_named_count'] = np.random.poisson(10 - quality * 8)
        
        # People features
        startup['founders_count'] = np.random.randint(1, 4)
        startup['team_size_full_time'] = int(np.random.lognormal(1 + quality * 2, 0.5))
        startup['years_experience_avg'] = np.random.uniform(2, 15) * quality
        startup['domain_expertise_years_avg'] = startup['years_experience_avg'] * np.random.uniform(0.5, 1)
        startup['prior_startup_experience_count'] = np.random.poisson(quality * 2)
        startup['prior_successful_exits_count'] = np.random.poisson(quality * 0.5)
        startup['board_advisor_experience_score'] = min(5, max(1, int(np.random.normal(1 + quality * 4, 0.5))))
        startup['advisors_count'] = np.random.poisson(quality * 5)
        startup['team_diversity_percent'] = np.random.uniform(10, 60) * quality
        startup['key_person_dependency'] = 1 if np.random.rand() < (1 - quality) * 0.7 else 0
        
        # Product features
        startup['product_stage'] = 0  # Simplified
        startup['product_retention_30d'] = np.random.uniform(20, 90) * quality
        startup['product_retention_90d'] = startup['product_retention_30d'] * np.random.uniform(0.5, 0.9)
        startup['dau_mau_ratio'] = np.random.uniform(0.1, 0.6) * quality
        startup['annual_revenue_run_rate'] = np.random.lognormal(10 + quality * 5, 2) if quality > 0.3 else 0
        startup['revenue_growth_rate_percent'] = np.random.normal(quality * 200 - 50, 30)
        startup['ltv_cac_ratio'] = startup['ltv_cac_ratio']  # Already set
        startup['funding_stage'] = 0  # Simplified
        
        # Ensure all features are present
        for feature in CANONICAL_FEATURES:
            if feature not in startup:
                startup[feature] = 0
                
        data.append(startup)
    
    return pd.DataFrame(data)

if __name__ == "__main__":
    import os
    print("Generating training data...")
    df = generate_training_data(10000)
    
    # Save to file
    os.makedirs('data', exist_ok=True)
    df.to_csv('data/synthetic_training_data.csv', index=False)
    
    print(f"Generated {len(df)} samples")
    print(f"Columns: {len(df.columns)}")
    print(f"Sample data:\n{df.head()}")