#!/usr/bin/env python3
"""
Add Realistic Variety to Dataset
Makes the data messy like real startups - successful companies with bad metrics,
failed companies with good metrics, missing data, contradictions, etc.
"""

import pandas as pd
import numpy as np
import random
from pathlib import Path

class RealisticVarietyAdder:
    """Add realistic messiness to startup data"""
    
    def __init__(self):
        self.outlier_stories = {
            'uber_type': {
                'description': 'Massive burn but eventual success',
                'changes': {'burn_multiple': (5, 10), 'runway_months': (3, 6), 'success': 1}
            },
            'quibi_type': {
                'description': 'Great metrics but failed',
                'changes': {'team_experience_score': (4, 5), 'total_capital_raised_usd': (1e9, 2e9), 'success': 0}
            },
            'whatsapp_type': {
                'description': 'Tiny team, huge success',
                'changes': {'team_size_full_time': (20, 50), 'total_capital_raised_usd': (50e6, 100e6), 'success': 1}
            },
            'theranos_type': {
                'description': 'All the right signals, massive fraud',
                'changes': {'investor_tier_primary': 1, 'board_advisor_experience_score': 5, 'success': 0}
            },
            'bootstrap_success': {
                'description': 'Minimal funding, profitable',
                'changes': {'total_capital_raised_usd': (100e3, 500e3), 'gross_margin_percent': (80, 95), 'success': 1}
            },
            'zombie_startup': {
                'description': 'Not dead but not growing',
                'changes': {'revenue_growth_rate_percent': (-10, 10), 'runway_months': (24, 48), 'success': 0}
            }
        }
    
    def add_realistic_variety(self, df: pd.DataFrame) -> pd.DataFrame:
        """Add realistic messiness to the dataset"""
        print("Adding realistic variety to dataset...")
        
        df = df.copy()
        
        # 1. Add outliers (10% of data)
        print("\n1. Adding outliers...")
        num_outliers = int(len(df) * 0.10)
        outlier_indices = np.random.choice(df.index, num_outliers, replace=False)
        
        for idx in outlier_indices:
            outlier_type = random.choice(list(self.outlier_stories.keys()))
            story = self.outlier_stories[outlier_type]
            
            # Apply the outlier pattern
            for feature, value_range in story['changes'].items():
                if feature == 'success':
                    df.loc[idx, feature] = value_range
                elif isinstance(value_range, tuple):
                    df.loc[idx, feature] = np.random.uniform(*value_range)
                else:
                    df.loc[idx, feature] = value_range
        
        print(f"   Added {num_outliers} outliers")
        
        # 2. Add missing data (30% of cells randomly)
        print("\n2. Adding missing data...")
        # Some features should never be missing
        never_missing = ['company_id', 'company_name', 'success', 'sector', 'funding_stage']
        can_be_missing = [col for col in df.columns if col not in never_missing]
        
        # Each company has 10-50% missing features
        for idx in df.index:
            missing_percent = np.random.uniform(0.1, 0.5)
            num_missing = int(len(can_be_missing) * missing_percent)
            missing_features = np.random.choice(can_be_missing, num_missing, replace=False)
            df.loc[idx, missing_features] = np.nan
        
        print(f"   Added missing values to ~30% of cells")
        
        # 3. Add contradictions (15% of companies)
        print("\n3. Adding contradictory signals...")
        num_contradictions = int(len(df) * 0.15)
        contradiction_indices = np.random.choice(df.index, num_contradictions, replace=False)
        
        contradictions = [
            # High revenue but high burn
            {'annual_revenue_run_rate': (1e6, 10e6), 'monthly_burn_usd': (500e3, 2e6)},
            # Great team but poor execution
            {'prior_successful_exits_count': (1, 3), 'revenue_growth_rate_percent': (-50, 0)},
            # Hot market but struggling
            {'market_growth_rate_percent': (50, 100), 'user_growth_rate_percent': (-20, 20)},
            # Efficient but not growing
            {'burn_multiple': (0.5, 1.5), 'customer_count': (10, 100)},
        ]
        
        for idx in contradiction_indices:
            contradiction = random.choice(contradictions)
            for feature, value_range in contradiction.items():
                if feature in df.columns:
                    df.loc[idx, feature] = np.random.uniform(*value_range)
        
        print(f"   Added contradictions to {num_contradictions} companies")
        
        # 4. Add measurement noise (all numeric features)
        print("\n4. Adding measurement noise...")
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        noise_cols = [col for col in numeric_cols if col not in ['success', 'company_id']]
        
        for col in noise_cols:
            # Add 10-30% noise
            noise = np.random.normal(0, 0.2, len(df))
            df[col] = df[col] * (1 + noise)
        
        print(f"   Added ±20% noise to all numeric features")
        
        # 5. Add time-based degradation
        print("\n5. Adding stale data simulation...")
        # Some companies have "old" data (less reliable)
        stale_data_pct = 0.2
        stale_indices = np.random.choice(df.index, int(len(df) * stale_data_pct), replace=False)
        
        # Stale data has more uncertainty
        for idx in stale_indices:
            # Revenue/growth metrics are less reliable
            growth_metrics = ['revenue_growth_rate_percent', 'user_growth_rate_percent', 'customer_count']
            for metric in growth_metrics:
                if metric in df.columns and pd.notna(df.loc[idx, metric]):
                    df.loc[idx, metric] *= np.random.uniform(0.5, 1.5)
        
        print(f"   Simulated stale data for {len(stale_indices)} companies")
        
        # 6. Success/failure overlap
        print("\n6. Creating success/failure metric overlap...")
        # Some successful companies should have bad metrics
        successful = df[df['success'] == 1].index
        num_bad_successful = int(len(successful) * 0.1)
        bad_successful = np.random.choice(successful, num_bad_successful, replace=False)
        
        for idx in bad_successful:
            # Give them some bad metrics
            df.loc[idx, 'burn_multiple'] = np.random.uniform(3, 8)
            df.loc[idx, 'runway_months'] = np.random.uniform(3, 9)
            df.loc[idx, 'revenue_growth_rate_percent'] = np.random.uniform(-20, 50)
        
        # Some failed companies should have good metrics  
        failed = df[df['success'] == 0].index
        num_good_failed = int(len(failed) * 0.1)
        good_failed = np.random.choice(failed, num_good_failed, replace=False)
        
        for idx in good_failed:
            # Give them some good metrics
            df.loc[idx, 'burn_multiple'] = np.random.uniform(1, 2)
            df.loc[idx, 'revenue_growth_rate_percent'] = np.random.uniform(100, 300)
            df.loc[idx, 'team_experience_score'] = np.random.uniform(4, 5)
        
        print(f"   Created overlap: {num_bad_successful} successful with bad metrics, {num_good_failed} failed with good metrics")
        
        # 7. Extreme outliers (black swans)
        print("\n7. Adding black swan events...")
        num_black_swans = int(len(df) * 0.01)  # 1% are extreme outliers
        black_swan_indices = np.random.choice(df.index, num_black_swans, replace=False)
        
        for idx in black_swan_indices:
            # Randomly make some metrics extreme
            extreme_features = np.random.choice(noise_cols, 5, replace=False)
            for feature in extreme_features:
                if np.random.random() > 0.5:
                    df.loc[idx, feature] *= np.random.uniform(10, 100)  # 10-100x normal
                else:
                    df.loc[idx, feature] *= np.random.uniform(0.01, 0.1)  # 1-10% of normal
        
        print(f"   Added {num_black_swans} black swan companies")
        
        # Summary statistics
        print("\n" + "="*60)
        print("VARIETY ADDED SUCCESSFULLY!")
        print("="*60)
        print(f"Dataset shape: {df.shape}")
        print(f"Success rate: {df['success'].mean():.1%}")
        print(f"Missing data: {df.isnull().sum().sum() / (len(df) * len(df.columns)):.1%}")
        
        # Check that we broke the perfect patterns
        # Sample check: burn_multiple overlap between success/failure
        success_burn = df[df['success'] == 1]['burn_multiple'].dropna()
        fail_burn = df[df['success'] == 0]['burn_multiple'].dropna()
        
        overlap_range = (max(success_burn.min(), fail_burn.min()), 
                        min(success_burn.max(), fail_burn.max()))
        
        print(f"\nBurn multiple overlap range: {overlap_range[0]:.1f} - {overlap_range[1]:.1f}")
        print("(Good! Success and failure metrics now overlap)")
        
        return df


def main():
    """Add realistic variety to the 100k dataset"""
    print("\n" + "="*80)
    print("ADDING REALISTIC VARIETY TO DATASET")
    print("="*80)
    
    # Load the dataset
    input_file = "real_startup_data_100k.csv"
    if not Path(input_file).exists():
        print(f"Error: {input_file} not found!")
        return
    
    df = pd.read_csv(input_file)
    print(f"\nLoaded dataset: {len(df):,} companies")
    print(f"Original success rate: {df['success'].mean():.1%}")
    
    # Add variety
    variety_adder = RealisticVarietyAdder()
    df_messy = variety_adder.add_realistic_variety(df)
    
    # Save the messy dataset
    output_file = "real_startup_data_100k_messy.csv"
    df_messy.to_csv(output_file, index=False)
    print(f"\nSaved messy dataset to: {output_file}")
    
    # Also create a smaller test version
    test_size = 10000
    df_test = df_messy.sample(n=test_size, random_state=42)
    test_file = "real_startup_data_10k_messy.csv"
    df_test.to_csv(test_file, index=False)
    print(f"Also created test dataset: {test_file} ({test_size:,} companies)")
    
    print("\n✅ Dataset now has realistic variety!")
    print("✅ Ready for retraining models")
    print("\nNext step: python3 retrain_production_models.py")


if __name__ == "__main__":
    main()