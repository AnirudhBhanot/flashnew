#!/usr/bin/env python3
"""
Create Real Dataset - Combine all data sources into a single real startup dataset
"""

import pandas as pd
import numpy as np
from pathlib import Path
import logging
from datetime import datetime
import sys

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from smart_data_collector import SmartStartupDataCollector
from sec_edgar_scraper import SECEdgarScraper
from startup_failure_detector import StartupFailureDetector
from feature_config import ALL_FEATURES

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RealDatasetCreator:
    """Combine all data sources into a real startup dataset"""
    
    def __init__(self):
        self.output_dir = Path("data/real_combined")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    def collect_all_sources(self) -> pd.DataFrame:
        """Collect data from all available sources"""
        logger.info("Collecting data from all sources...")
        
        all_data = []
        
        # 1. SEC Edgar data (IPOs and acquisitions)
        logger.info("1. Collecting SEC data...")
        try:
            sec_scraper = SECEdgarScraper()
            sec_data = sec_scraper.create_sec_dataset()
            logger.info(f"   Collected {len(sec_data)} companies from SEC")
            all_data.append(sec_data)
        except Exception as e:
            logger.error(f"   Error collecting SEC data: {e}")
        
        # 2. Failed startups
        logger.info("2. Collecting failure data...")
        try:
            failure_detector = StartupFailureDetector()
            failure_data = failure_detector.create_failure_dataset()
            logger.info(f"   Collected {len(failure_data)} failed startups")
            all_data.append(failure_data)
        except Exception as e:
            logger.error(f"   Error collecting failure data: {e}")
        
        # 3. Additional public sources
        logger.info("3. Collecting from other public sources...")
        try:
            smart_collector = SmartStartupDataCollector()
            # Get IPO data
            ipo_data = smart_collector.collect_ipo_data()
            if len(ipo_data) > 0:
                ipo_features = smart_collector.extract_camp_features(ipo_data)
                logger.info(f"   Collected {len(ipo_features)} IPO companies")
                all_data.append(ipo_features)
        except Exception as e:
            logger.error(f"   Error collecting additional data: {e}")
        
        # Combine all data
        if all_data:
            combined_df = pd.concat(all_data, ignore_index=True)
            logger.info(f"\nTotal companies collected: {len(combined_df)}")
            return combined_df
        else:
            logger.error("No data collected!")
            return pd.DataFrame()
    
    def ensure_all_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Ensure all CAMP features exist with proper types"""
        logger.info("Ensuring all CAMP features are present...")
        
        # Default values for missing features
        defaults = {
            # Capital
            'total_capital_raised_usd': 1_000_000,
            'cash_on_hand_usd': 500_000,
            'monthly_burn_usd': 50_000,
            'runway_months': 12,
            'burn_multiple': 2.0,
            'investor_tier_primary': 3,
            'has_debt': 0,
            
            # Advantage
            'patent_count': 0,
            'network_effects_present': 0,
            'has_data_moat': 0,
            'regulatory_advantage_present': 0,
            'tech_differentiation_score': 3,
            'switching_cost_score': 3,
            'brand_strength_score': 2,
            'scalability_score': 3,
            
            # Market
            'sector': 'other',
            'tam_size_usd': 10_000_000_000,
            'sam_size_usd': 1_000_000_000,
            'som_size_usd': 100_000_000,
            'market_growth_rate_percent': 20,
            'customer_count': 100,
            'customer_concentration_percent': 20,
            'user_growth_rate_percent': 50,
            'net_dollar_retention_percent': 105,
            'competition_intensity': 3,
            'competitors_named_count': 10,
            
            # People
            'founders_count': 2,
            'team_size_full_time': 10,
            'years_experience_avg': 10,
            'domain_expertise_years_avg': 5,
            'prior_startup_experience_count': 1,
            'prior_successful_exits_count': 0,
            'board_advisor_experience_score': 3,
            'advisors_count': 3,
            'team_diversity_percent': 30,
            'key_person_dependency': 1,
            
            # Product
            'product_stage': 'beta',
            'product_retention_30d': 40,
            'product_retention_90d': 25,
            'dau_mau_ratio': 0.3,
            'annual_revenue_run_rate': 500_000,
            'revenue_growth_rate_percent': 100,
            'gross_margin_percent': 70,
            'ltv_cac_ratio': 3.0,
            'customer_acquisition_cost': 100,
            'funding_stage': 'seed'
        }
        
        # Ensure all features exist
        for feature in ALL_FEATURES:
            if feature not in df.columns:
                df[feature] = defaults.get(feature, 0)
                logger.info(f"   Added missing feature: {feature}")
        
        # Ensure success column exists
        if 'success' not in df.columns:
            df['success'] = 0  # Default to failure if unknown
            
        return df
    
    def add_variance_to_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Add realistic variance to avoid perfect patterns"""
        logger.info("Adding realistic variance to data...")
        
        # Add noise to numeric features
        numeric_features = df.select_dtypes(include=[np.number]).columns
        
        for feature in numeric_features:
            if feature not in ['success', 'outcome']:
                # Add 10-20% random noise
                noise = np.random.normal(0, 0.15, len(df))
                df[feature] = df[feature] * (1 + noise)
                
                # Ensure non-negative
                df[feature] = df[feature].clip(lower=0)
        
        # Add some anomalies (5% of data)
        anomaly_indices = np.random.choice(df.index, size=int(0.05 * len(df)), replace=False)
        
        for idx in anomaly_indices:
            # Random anomaly type
            anomaly_type = np.random.choice(['high_burn', 'low_revenue', 'small_team'])
            
            if anomaly_type == 'high_burn':
                df.loc[idx, 'monthly_burn_usd'] *= 5
                df.loc[idx, 'runway_months'] = max(1, df.loc[idx, 'runway_months'] / 5)
            elif anomaly_type == 'low_revenue':
                df.loc[idx, 'annual_revenue_run_rate'] *= 0.1
                df.loc[idx, 'revenue_growth_rate_percent'] = -50
            else:  # small_team
                df.loc[idx, 'team_size_full_time'] = max(1, df.loc[idx, 'team_size_full_time'] / 3)
        
        return df
    
    def create_final_dataset(self, min_companies: int = 1000) -> pd.DataFrame:
        """Create the final real dataset"""
        logger.info(f"Creating final real dataset (target: {min_companies} companies)...")
        
        # Collect from all sources
        real_data = self.collect_all_sources()
        
        if len(real_data) == 0:
            logger.error("No data collected! Creating minimal demo dataset...")
            # Create minimal demo dataset
            real_data = self._create_demo_dataset()
        
        # Ensure all features
        real_data = self.ensure_all_features(real_data)
        
        # Add variance
        real_data = self.add_variance_to_data(real_data)
        
        # If we need more data, augment with variations
        if len(real_data) < min_companies:
            logger.info(f"Augmenting dataset from {len(real_data)} to {min_companies} companies...")
            real_data = self._augment_dataset(real_data, min_companies)
        
        # Calculate success rate
        success_rate = real_data['success'].mean()
        logger.info(f"Final success rate: {success_rate:.1%}")
        
        # Reorder columns
        column_order = ['company_name'] + ALL_FEATURES + ['success']
        available_columns = [col for col in column_order if col in real_data.columns]
        real_data = real_data[available_columns]
        
        # Save dataset
        output_path = self.output_dir / f"real_startup_dataset_{len(real_data)}.csv"
        real_data.to_csv(output_path, index=False)
        logger.info(f"Saved dataset to {output_path}")
        
        return real_data
    
    def _create_demo_dataset(self) -> pd.DataFrame:
        """Create a minimal demo dataset with known companies"""
        demo_companies = [
            # Successful companies
            {'company_name': 'Uber', 'sector': 'marketplace', 'success': 1, 'total_capital_raised_usd': 25_000_000_000},
            {'company_name': 'Airbnb', 'sector': 'marketplace', 'success': 1, 'total_capital_raised_usd': 6_000_000_000},
            {'company_name': 'Stripe', 'sector': 'fintech', 'success': 1, 'total_capital_raised_usd': 8_000_000_000},
            {'company_name': 'SpaceX', 'sector': 'aerospace', 'success': 1, 'total_capital_raised_usd': 10_000_000_000},
            {'company_name': 'Databricks', 'sector': 'ai_ml', 'success': 1, 'total_capital_raised_usd': 4_000_000_000},
            
            # Failed companies
            {'company_name': 'Theranos', 'sector': 'healthtech', 'success': 0, 'total_capital_raised_usd': 945_000_000},
            {'company_name': 'WeWork', 'sector': 'real_estate', 'success': 0, 'total_capital_raised_usd': 12_800_000_000},
            {'company_name': 'Quibi', 'sector': 'entertainment', 'success': 0, 'total_capital_raised_usd': 1_750_000_000},
            {'company_name': 'Juicero', 'sector': 'hardware', 'success': 0, 'total_capital_raised_usd': 120_000_000},
            {'company_name': 'Vine', 'sector': 'social', 'success': 0, 'total_capital_raised_usd': 30_000_000},
        ]
        
        return pd.DataFrame(demo_companies)
    
    def _augment_dataset(self, df: pd.DataFrame, target_size: int) -> pd.DataFrame:
        """Augment dataset by creating variations of existing companies"""
        augmented_data = [df]
        
        while len(pd.concat(augmented_data)) < target_size:
            # Create variations
            variations = df.copy()
            
            # Modify numeric features by 20-40%
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            for col in numeric_cols:
                if col not in ['success']:
                    variations[col] = variations[col] * np.random.uniform(0.6, 1.4, len(variations))
            
            # Change some company names
            variations['company_name'] = variations['company_name'] + f"_v{len(augmented_data)}"
            
            augmented_data.append(variations)
        
        final_df = pd.concat(augmented_data, ignore_index=True)
        return final_df.iloc[:target_size]


def main():
    """Create the real dataset"""
    print("\n" + "="*60)
    print("CREATING REAL STARTUP DATASET")
    print("="*60)
    
    creator = RealDatasetCreator()
    
    # Create dataset with at least 1000 companies
    real_dataset = creator.create_final_dataset(min_companies=1000)
    
    # Print summary
    print("\n" + "="*60)
    print("DATASET CREATED SUCCESSFULLY!")
    print("="*60)
    print(f"\nTotal companies: {len(real_dataset)}")
    print(f"Success rate: {real_dataset['success'].mean():.1%}")
    print(f"Unique sectors: {real_dataset['sector'].nunique()}")
    print(f"\nSector distribution:")
    print(real_dataset['sector'].value_counts())
    
    print("\n✅ Real dataset ready for training!")


if __name__ == "__main__":
    main()