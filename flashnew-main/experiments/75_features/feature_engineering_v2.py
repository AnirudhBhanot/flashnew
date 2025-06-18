#!/usr/bin/env python3
"""
Feature Engineering for FLASH V2: Adding 30 new features to create 75-feature dataset
"""
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

class FeatureEngineerV2:
    """Engineer 30 new features based on VC priorities"""
    
    def __init__(self):
        self.original_features = 45
        self.new_features = 30
        self.total_features = 75
        
    def engineer_all_features(self, df):
        """Add all 30 new features to the dataset"""
        print("Starting feature engineering for 30 new features...")
        
        # Create a copy to avoid modifying original
        df_enhanced = df.copy()
        
        # CAPITAL features (10 new)
        df_enhanced = self._add_capital_features(df_enhanced)
        
        # ADVANTAGE features (6 new)
        df_enhanced = self._add_advantage_features(df_enhanced)
        
        # MARKET features (6 new)
        df_enhanced = self._add_market_features(df_enhanced)
        
        # PEOPLE features (8 new)
        df_enhanced = self._add_people_features(df_enhanced)
        
        print(f"Feature engineering complete. Total features: {len(df_enhanced.columns) - 3}")  # -3 for id, name, success
        
        return df_enhanced
    
    def _add_capital_features(self, df):
        """Add 10 new CAPITAL features"""
        print("Adding CAPITAL features...")
        
        # 1. monthly_revenue_growth_rate
        # Estimate from annual growth rate (divide by 12 and add noise)
        df['monthly_revenue_growth_rate'] = np.where(
            df['revenue_growth_rate_percent'] > 0,
            df['revenue_growth_rate_percent'] / 12 * np.random.uniform(0.8, 1.2, len(df)),
            0
        )
        
        # 2. burn_months_remaining
        # More precise calculation including revenue
        df['burn_months_remaining'] = np.where(
            df['monthly_burn_usd'] > df['annual_revenue_run_rate'] / 12,
            df['cash_on_hand_usd'] / (df['monthly_burn_usd'] - df['annual_revenue_run_rate'] / 12),
            999  # If revenue > burn, runway is infinite
        ).clip(0, 999)
        
        # 3. months_since_last_funding
        # Estimate based on funding stage and typical timelines
        stage_to_months = {
            'Pre-seed': np.random.randint(3, 12),
            'Seed': np.random.randint(6, 18),
            'Series A': np.random.randint(12, 24),
            'Series B': np.random.randint(18, 30),
            'Series C+': np.random.randint(24, 36)
        }
        df['months_since_last_funding'] = df['funding_stage'].map(
            lambda x: stage_to_months.get(x, 12) + np.random.randint(-3, 3)
        )
        
        # 4. customer_payback_period
        # Calculate from LTV/CAC ratio
        df['customer_payback_period'] = np.where(
            df['ltv_cac_ratio'] > 0,
            12 / df['ltv_cac_ratio'],  # Months to recover CAC
            24  # Default if no LTV/CAC
        ).clip(1, 60)
        
        # 5. gross_margin_trend
        # Simulate based on stage and current margin
        df['gross_margin_trend'] = df.apply(
            lambda x: 'improving' if x['gross_margin_percent'] < 70 and np.random.random() > 0.3
            else 'declining' if x['gross_margin_percent'] > 80 and np.random.random() > 0.7
            else 'stable', axis=1
        )
        
        # 6. burn_multiple_trend
        # Based on stage and efficiency
        df['burn_multiple_trend'] = df.apply(
            lambda x: 'improving' if x['burn_multiple'] > 1.5 and np.random.random() > 0.4
            else 'worsening' if x['burn_multiple'] < 1 and np.random.random() > 0.6
            else 'stable', axis=1
        )
        
        # 7. revenue_per_employee_trend
        # Calculate current and simulate trend
        df['revenue_per_employee'] = df['annual_revenue_run_rate'] / df['team_size_full_time'].clip(lower=1)
        df['revenue_per_employee_trend'] = df.apply(
            lambda x: 'increasing' if x['revenue_per_employee'] < 200000 and np.random.random() > 0.3
            else 'decreasing' if x['revenue_per_employee'] > 500000 and np.random.random() > 0.7
            else 'stable', axis=1
        )
        
        # 8. cash_zero_date
        # Days until cash runs out
        df['cash_zero_date'] = (df['burn_months_remaining'] * 30).clip(0, 9999)
        
        # 9. revenue_quality_score
        # Based on sector and business model (B2B SaaS = high quality)
        sector_quality = {
            'SaaS': 0.9,
            'FinTech': 0.85,
            'HealthTech': 0.8,
            'BioTech': 0.7,
            'E-commerce': 0.6,
            'Other': 0.5
        }
        df['revenue_quality_score'] = df['sector'].map(sector_quality) * (1 + np.random.uniform(-0.1, 0.1, len(df)))
        df['revenue_quality_score'] = df['revenue_quality_score'].clip(0, 1)
        
        # 10. funding_efficiency_ratio
        # Revenue generated per dollar raised
        df['funding_efficiency_ratio'] = (
            df['annual_revenue_run_rate'] / df['total_capital_raised_usd'].clip(lower=1)
        ).clip(0, 10)
        
        return df
    
    def _add_advantage_features(self, df):
        """Add 6 new ADVANTAGE features"""
        print("Adding ADVANTAGE features...")
        
        # 1. customer_logo_quality (1-10 score)
        # Based on revenue per customer and sector
        df['avg_revenue_per_customer'] = df['annual_revenue_run_rate'] / df['customer_count'].clip(lower=1)
        df['customer_logo_quality'] = df.apply(
            lambda x: min(10, (
                5 +  # Base score
                (2 if x['avg_revenue_per_customer'] > 100000 else 0) +
                (2 if x['avg_revenue_per_customer'] > 1000000 else 0) +
                (1 if x['sector'] in ['FinTech', 'HealthTech'] else 0) +
                np.random.uniform(-1, 1)
            )), axis=1
        ).clip(1, 10)
        
        # 2. competitive_win_rate
        # Based on market share and growth
        df['competitive_win_rate'] = (
            50 +  # Base win rate
            (df['user_growth_rate_percent'] - df['market_growth_rate_percent']) * 0.5 +
            np.where(df['net_dollar_retention_percent'] > 120, 10, 0) +
            np.random.uniform(-10, 10, len(df))
        ).clip(10, 90)
        
        # 3. organic_growth_percentage
        # Based on NPS proxy and retention
        df['organic_growth_percentage'] = (
            df['product_retention_30d'] * 100 * 0.3 +  # Retention drives organic
            df['dau_mau_ratio'] * 100 * 0.3 +  # Engagement drives sharing
            np.where(df['network_effects_present'], 20, 0) +
            np.random.uniform(0, 20, len(df))
        ).clip(0, 80)
        
        # 4. pilot_to_paid_conversion
        # Based on product stage and retention
        stage_conversion = {'MVP': 30, 'Beta': 50, 'GA': 70, 'Mature': 80}
        df['pilot_to_paid_conversion'] = df.apply(
            lambda x: (
                stage_conversion.get(x['product_stage'], 50) +
                x['product_retention_30d'] * 20 +
                np.random.uniform(-10, 10)
            ), axis=1
        ).clip(10, 95)
        
        # 5. net_promoter_score
        # Estimate from retention and engagement
        df['net_promoter_score'] = (
            -50 +  # Base
            df['product_retention_90d'] * 100 +
            df['net_dollar_retention_percent'] * 0.5 +
            np.random.uniform(-10, 10, len(df))
        ).clip(-100, 100)
        
        # 6. time_to_value_days
        # Based on product complexity and sector
        sector_ttv = {
            'SaaS': 7, 'E-commerce': 1, 'FinTech': 14,
            'HealthTech': 30, 'BioTech': 90, 'Other': 14
        }
        df['time_to_value_days'] = df['sector'].map(sector_ttv) * np.random.uniform(0.5, 1.5, len(df))
        
        return df
    
    def _add_market_features(self, df):
        """Add 6 new MARKET features"""
        print("Adding MARKET features...")
        
        # 1. market_timing_score (1-10)
        # Based on market growth and competition
        df['market_timing_score'] = (
            5 +  # Base
            np.where(df['market_growth_rate_percent'] > 20, 2, -1) +
            np.where(df['competition_intensity'] < 5, 1, -1) +
            np.where(df['tam_size_usd'] > 10e9, 2, 0) +
            np.random.uniform(-1, 1, len(df))
        ).clip(1, 10)
        
        # 2. category_leader_distance
        # Estimate based on market share
        df['market_share_estimate'] = (df['som_size_usd'] / df['sam_size_usd']).clip(0, 1)
        df['category_leader_distance'] = (
            (0.3 - df['market_share_estimate']) * 100  # Assume leader has 30% share
        ).clip(0, 100)
        
        # 3. competitor_funding_last_12mo
        # Based on competition intensity and market size
        df['competitor_funding_last_12mo'] = (
            df['competition_intensity'] * df['tam_size_usd'] / 1000 * 
            np.random.uniform(0.5, 1.5, len(df))
        ).clip(0, 1e10)
        
        # 4. sales_cycle_trend
        # Based on product maturity and market
        df['sales_cycle_trend'] = df.apply(
            lambda x: 'shortening' if x['product_stage'] in ['GA', 'Mature'] and np.random.random() > 0.4
            else 'lengthening' if x['product_stage'] == 'MVP' and np.random.random() > 0.6
            else 'stable', axis=1
        )
        
        # 5. top_customer_concentration
        # Enhance existing metric
        df['top_customer_concentration'] = df['customer_concentration_percent'] * np.random.uniform(1.5, 2.5, len(df))
        df['top_customer_concentration'] = df['top_customer_concentration'].clip(0, 80)
        
        # 6. expansion_revenue_percentage
        # Based on NDR and sector
        df['expansion_revenue_percentage'] = np.where(
            df['net_dollar_retention_percent'] > 100,
            (df['net_dollar_retention_percent'] - 100) * 0.7,
            0
        ).clip(0, 50)
        
        return df
    
    def _add_people_features(self, df):
        """Add 8 new PEOPLE features"""
        print("Adding PEOPLE features...")
        
        # 1. founder_ownership_percentage
        # Estimate based on funding stage
        stage_dilution = {
            'Pre-seed': 0.85, 'Seed': 0.70, 'Series A': 0.50,
            'Series B': 0.35, 'Series C+': 0.25
        }
        df['founder_ownership_percentage'] = (
            df['funding_stage'].map(stage_dilution) * 
            (1 / df['founders_count']) * 100 *
            np.random.uniform(0.8, 1.2, len(df))
        ).clip(5, 80)
        
        # 2. technical_founder_percentage
        # Based on sector and team
        tech_sector_prob = {
            'AI/ML': 0.9, 'SaaS': 0.8, 'FinTech': 0.7,
            'E-commerce': 0.5, 'Other': 0.6
        }
        df['technical_founder_percentage'] = df.apply(
            lambda x: (
                tech_sector_prob.get(x['sector'], 0.6) * 
                x['founder_ownership_percentage'] *
                np.random.uniform(0.5, 1.0)
            ), axis=1
        ).clip(0, 100)
        
        # 3. founder_domain_years
        # Similar to domain expertise but for founders specifically
        df['founder_domain_years'] = (
            df['domain_expertise_years_avg'] * 1.2 +  # Founders usually more experienced
            np.random.uniform(-2, 2, len(df))
        ).clip(0, 30)
        
        # 4. team_completeness_score (1-10)
        # Based on team size and stage
        df['team_completeness_score'] = df.apply(
            lambda x: min(10, (
                2 +  # Base
                min(3, x['team_size_full_time'] / 10) +  # Size component
                (2 if x['funding_stage'] in ['Series A', 'Series B', 'Series C+'] else 0) +
                (1 if x['advisors_count'] > 3 else 0) +
                (2 if x['board_advisor_experience_score'] > 3 else 0) +
                np.random.uniform(-1, 1)
            )), axis=1
        ).clip(1, 10)
        
        # 5. previous_exit_multiple
        # Based on prior exits
        df['previous_exit_multiple'] = df.apply(
            lambda x: (
                0 if x['prior_successful_exits_count'] == 0 else
                np.random.choice([3, 5, 10, 20, 50]) if x['prior_successful_exits_count'] == 1 else
                np.random.choice([10, 20, 50, 100])
            ), axis=1
        )
        
        # 6. full_time_commitment
        # Binary - estimate based on burn and team size
        df['full_time_commitment'] = (
            (df['monthly_burn_usd'] / df['team_size_full_time'].clip(lower=1) > 5000) |
            (df['funding_stage'].isin(['Series A', 'Series B', 'Series C+']))
        ).astype(int)
        
        # 7. employee_growth_rate
        # Estimate based on funding and stage
        df['employee_growth_rate'] = df.apply(
            lambda x: (
                100 if x['funding_stage'] == 'Seed' and x['team_size_full_time'] < 10 else
                50 if x['funding_stage'] == 'Series A' else
                30 if x['funding_stage'] == 'Series B' else
                20
            ) + np.random.uniform(-10, 10), axis=1
        ).clip(0, 200)
        
        # 8. key_hire_retention
        # Based on culture and growth
        df['key_hire_retention'] = (
            50 +  # Base retention
            df['team_diversity_percent'] * 0.3 +  # Diversity helps retention
            np.where(df['employee_growth_rate'] > 50, -10, 10) +  # Fast growth hurts retention
            df['board_advisor_experience_score'] * 3 +  # Good board helps
            np.random.uniform(-10, 10, len(df))
        ).clip(20, 95)
        
        return df
    
    def validate_features(self, df_original, df_enhanced):
        """Validate that all features were added correctly"""
        original_cols = set(df_original.columns)
        enhanced_cols = set(df_enhanced.columns)
        new_cols = enhanced_cols - original_cols
        
        print(f"\nValidation Report:")
        print(f"Original features: {len(original_cols) - 3}")  # Exclude id, name, success
        print(f"New features added: {len(new_cols)}")
        print(f"Total features: {len(enhanced_cols) - 3}")
        
        # List new features by category
        capital_features = [
            'monthly_revenue_growth_rate', 'burn_months_remaining', 'months_since_last_funding',
            'customer_payback_period', 'gross_margin_trend', 'burn_multiple_trend',
            'revenue_per_employee_trend', 'cash_zero_date', 'revenue_quality_score',
            'funding_efficiency_ratio', 'revenue_per_employee'
        ]
        
        advantage_features = [
            'customer_logo_quality', 'competitive_win_rate', 'organic_growth_percentage',
            'pilot_to_paid_conversion', 'net_promoter_score', 'time_to_value_days',
            'avg_revenue_per_customer'
        ]
        
        market_features = [
            'market_timing_score', 'category_leader_distance', 'competitor_funding_last_12mo',
            'sales_cycle_trend', 'top_customer_concentration', 'expansion_revenue_percentage',
            'market_share_estimate'
        ]
        
        people_features = [
            'founder_ownership_percentage', 'technical_founder_percentage', 'founder_domain_years',
            'team_completeness_score', 'previous_exit_multiple', 'full_time_commitment',
            'employee_growth_rate', 'key_hire_retention'
        ]
        
        print("\nNew features by category:")
        print(f"CAPITAL: {len([f for f in capital_features if f in new_cols])}")
        print(f"ADVANTAGE: {len([f for f in advantage_features if f in new_cols])}")
        print(f"MARKET: {len([f for f in market_features if f in new_cols])}")
        print(f"PEOPLE: {len([f for f in people_features if f in new_cols])}")
        
        # Check for any missing expected features
        all_expected = set(capital_features + advantage_features + market_features + people_features)
        missing = all_expected - new_cols
        if missing:
            print(f"\nWarning: Missing expected features: {missing}")
        
        return True

def main():
    """Main function to create enhanced dataset"""
    print("FLASH V2 Feature Engineering")
    print("=" * 50)
    
    # Load original dataset
    input_path = "/Users/sf/Desktop/FLASH/data/final_100k_dataset_45features.csv"
    output_path = "/Users/sf/Desktop/FLASH/data/final_100k_dataset_75features.csv"
    
    print(f"Loading original dataset from: {input_path}")
    df_original = pd.read_csv(input_path)
    print(f"Loaded {len(df_original)} records with {len(df_original.columns)} columns")
    
    # Initialize feature engineer
    engineer = FeatureEngineerV2()
    
    # Engineer all new features
    df_enhanced = engineer.engineer_all_features(df_original)
    
    # Validate
    engineer.validate_features(df_original, df_enhanced)
    
    # Save enhanced dataset
    print(f"\nSaving enhanced dataset to: {output_path}")
    df_enhanced.to_csv(output_path, index=False)
    print("Done!")
    
    # Create summary statistics
    print("\nCreating summary statistics...")
    summary = {
        'original_features': len(df_original.columns) - 3,
        'new_features': len(df_enhanced.columns) - len(df_original.columns),
        'total_features': len(df_enhanced.columns) - 3,
        'records': len(df_enhanced),
        'file_size_mb': df_enhanced.memory_usage(deep=True).sum() / 1024**2
    }
    
    # Save summary
    import json
    with open('/Users/sf/Desktop/FLASH/data/dataset_v2_summary.json', 'w') as f:
        json.dump(summary, f, indent=2)
    
    print("\nSummary:")
    for key, value in summary.items():
        print(f"  {key}: {value}")

if __name__ == "__main__":
    main()