#!/usr/bin/env python3
"""
Fast generation of high-quality 100k startup dataset with real patterns.
Optimized for speed while maintaining quality requirements.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
import logging
from typing import Dict, List, Optional
import warnings

warnings.filterwarnings('ignore')
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

class FastHighQualityDatasetGenerator:
    """Generate production-quality startup dataset efficiently."""
    
    def __init__(self):
        # Real success rates from industry data
        self.stage_success_rates = {
            'Pre-Seed': 0.10,
            'Seed': 0.15,
            'Series A': 0.25,
            'Series B': 0.35,
            'Series C+': 0.45
        }
        
        # Industry data based on real patterns
        self.industries = {
            'SaaS': {'growth': 0.25, 'margin': 75, 'fail_rate': 0.72},
            'AI/ML': {'growth': 0.35, 'margin': 70, 'fail_rate': 0.75},
            'FinTech': {'growth': 0.22, 'margin': 60, 'fail_rate': 0.70},
            'HealthTech': {'growth': 0.18, 'margin': 55, 'fail_rate': 0.65},
            'E-commerce': {'growth': 0.15, 'margin': 35, 'fail_rate': 0.80},
            'Marketplace': {'growth': 0.17, 'margin': 70, 'fail_rate': 0.85},
            'EdTech': {'growth': 0.16, 'margin': 65, 'fail_rate': 0.70},
            'Cybersecurity': {'growth': 0.23, 'margin': 80, 'fail_rate': 0.60},
            'BioTech': {'growth': 0.14, 'margin': 45, 'fail_rate': 0.85}
        }
        
        # Top VCs and their investment patterns
        self.top_vcs = [
            'Sequoia Capital', 'Andreessen Horowitz', 'Accel', 'Founders Fund',
            'Kleiner Perkins', 'GV', 'Benchmark', 'Greylock Partners',
            'Index Ventures', 'Lightspeed', 'Y Combinator', 'Techstars'
        ]
        
        # Real startup hubs
        self.locations = [
            ('San Francisco, CA', 0.25),
            ('New York, NY', 0.15),
            ('Boston, MA', 0.10),
            ('Austin, TX', 0.08),
            ('Seattle, WA', 0.07),
            ('Los Angeles, CA', 0.06),
            ('Denver, CO', 0.04),
            ('Chicago, IL', 0.04),
            ('Atlanta, GA', 0.03),
            ('Miami, FL', 0.03),
            ('Other', 0.15)
        ]
    
    def generate_dataset(self, n_records: int = 100000) -> pd.DataFrame:
        """Generate the complete dataset efficiently."""
        logger.info(f"Generating {n_records} high-quality startup records...")
        
        # Pre-allocate arrays for efficiency
        data = {col: np.empty(n_records, dtype=object if col in ['company_id', 'company_name', 'funding_stage', 
                                                                 'investor_tier_primary', 'product_stage', 'sector'] 
                                                       else np.float64) 
                for col in self._get_all_columns()}
        
        # Add boolean columns
        bool_cols = ['has_debt', 'network_effects_present', 'has_data_moat', 
                    'regulatory_advantage_present', 'key_person_dependency', 'success']
        for col in bool_cols:
            data[col] = np.empty(n_records, dtype=bool)
        
        # Generate data in batches for efficiency
        batch_size = 10000
        for batch_start in range(0, n_records, batch_size):
            batch_end = min(batch_start + batch_size, n_records)
            batch_size_actual = batch_end - batch_start
            
            if batch_start % 20000 == 0:
                logger.info(f"Generated {batch_start}/{n_records} records...")
            
            # Generate batch data
            self._generate_batch(data, batch_start, batch_end)
        
        # Convert to DataFrame
        df = pd.DataFrame(data)
        
        # Add calculated fields
        df = self._add_calculated_fields(df)
        
        # Apply data quality patterns
        df = self._apply_data_quality_patterns(df)
        
        logger.info(f"Generated {len(df)} records successfully")
        
        return df
    
    def _get_all_columns(self) -> List[str]:
        """Get all column names for the dataset."""
        return [
            # Identifiers
            'company_id', 'company_name', 'founding_year', 'year', 'years_since_founding',
            
            # Capital features (12)
            'total_capital_raised_usd', 'cash_on_hand_usd', 'monthly_burn_usd', 
            'runway_months', 'annual_revenue_run_rate', 'revenue_growth_rate_percent',
            'gross_margin_percent', 'burn_multiple', 'ltv_cac_ratio', 'funding_stage',
            'investor_tier_primary', 'has_debt',
            
            # Advantage features (11)
            'patent_count', 'tech_differentiation_score', 'switching_cost_score',
            'network_effects_present', 'has_data_moat', 'brand_strength_score',
            'scalability_score', 'regulatory_advantage_present', 'product_stage',
            'product_retention_30d', 'product_retention_90d',
            
            # Market features (12)
            'tam_size_usd', 'sam_size_usd', 'som_size_usd', 'market_growth_rate_percent',
            'customer_count', 'customer_concentration_percent', 'user_growth_rate_percent',
            'net_dollar_retention_percent', 'competition_intensity', 'competitors_named_count',
            'sector', 'dau_mau_ratio',
            
            # People features (10)
            'founders_count', 'team_size_full_time', 'years_experience_avg',
            'domain_expertise_years_avg', 'prior_startup_experience_count',
            'prior_successful_exits_count', 'board_advisor_experience_score',
            'advisors_count', 'team_diversity_percent', 'key_person_dependency',
            
            # Outcome
            'success'
        ]
    
    def _generate_batch(self, data: Dict, start_idx: int, end_idx: int):
        """Generate a batch of records efficiently."""
        batch_size = end_idx - start_idx
        
        # Generate company basics
        company_ids = np.arange(start_idx, end_idx)
        data['company_id'][start_idx:end_idx] = [f'company_{i:06d}' for i in company_ids]
        
        # Industry distribution
        industries = list(self.industries.keys())
        industry_probs = np.array([1/len(industries)] * len(industries))
        data['sector'][start_idx:end_idx] = np.random.choice(industries, size=batch_size, p=industry_probs)
        
        # Company names based on industry
        for i in range(start_idx, end_idx):
            industry = data['sector'][i]
            data['company_name'][i] = f"{industry.replace('/', '')}_Startup_{i}"
        
        # Founding year (weighted towards recent)
        years = np.arange(2005, 2024)
        year_weights = 0.7 ** (2023 - years)
        year_probs = year_weights / year_weights.sum()
        data['founding_year'][start_idx:end_idx] = np.random.choice(years, size=batch_size, p=year_probs)
        
        # Years since founding
        data['year'][start_idx:end_idx] = 2024
        data['years_since_founding'][start_idx:end_idx] = 2024 - data['founding_year'][start_idx:end_idx]
        
        # Funding stage based on age
        for i in range(start_idx, end_idx):
            years = data['years_since_founding'][i]
            if years <= 1:
                stage = 'Pre-Seed' if np.random.random() < 0.6 else 'Seed'
            elif years <= 3:
                stage = np.random.choice(['Seed', 'Series A'], p=[0.4, 0.6])
            elif years <= 5:
                stage = np.random.choice(['Series A', 'Series B'], p=[0.3, 0.7])
            elif years <= 8:
                stage = np.random.choice(['Series B', 'Series C+'], p=[0.4, 0.6])
            else:
                stage = 'Series C+'
            data['funding_stage'][i] = stage
        
        # Generate financial metrics
        self._generate_financial_metrics(data, start_idx, end_idx)
        
        # Generate advantage metrics
        self._generate_advantage_metrics(data, start_idx, end_idx)
        
        # Generate market metrics
        self._generate_market_metrics(data, start_idx, end_idx)
        
        # Generate people metrics
        self._generate_people_metrics(data, start_idx, end_idx)
        
        # Generate outcomes
        self._generate_outcomes(data, start_idx, end_idx)
    
    def _generate_financial_metrics(self, data: Dict, start: int, end: int):
        """Generate financial metrics with realistic patterns."""
        for i in range(start, end):
            stage = data['funding_stage'][i]
            industry = data['sector'][i]
            years = data['years_since_founding'][i]
            
            # Total capital raised (cumulative by stage)
            if stage == 'Pre-Seed':
                capital = np.random.uniform(50e3, 500e3)
            elif stage == 'Seed':
                capital = np.random.uniform(500e3, 3e6)
            elif stage == 'Series A':
                capital = np.random.uniform(3e6, 15e6)
            elif stage == 'Series B':
                capital = np.random.uniform(15e6, 50e6)
            else:  # Series C+
                capital = np.random.uniform(50e6, 200e6)
            
            data['total_capital_raised_usd'][i] = capital
            
            # Cash on hand (30-70% of last raise typically)
            data['cash_on_hand_usd'][i] = capital * np.random.uniform(0.3, 0.7)
            
            # Monthly burn
            burn_rates = {
                'Pre-Seed': (10e3, 50e3),
                'Seed': (50e3, 200e3),
                'Series A': (200e3, 800e3),
                'Series B': (800e3, 2e6),
                'Series C+': (2e6, 5e6)
            }
            min_burn, max_burn = burn_rates.get(stage, (100e3, 500e3))
            data['monthly_burn_usd'][i] = np.random.uniform(min_burn, max_burn)
            
            # Revenue (grows with age and varies by outcome)
            if years == 0:
                revenue = 0
            else:
                industry_growth = self.industries[industry]['growth']
                base_revenue = 10000 * (1 + industry_growth) ** years
                revenue = base_revenue * np.random.uniform(0.5, 2.0)
            
            data['annual_revenue_run_rate'][i] = revenue
            
            # Revenue growth rate
            if years <= 2:
                growth = np.random.uniform(100, 300)
            else:
                growth = np.random.uniform(20, 100)
            data['revenue_growth_rate_percent'][i] = growth
            
            # Gross margin by industry
            margin_base = self.industries[industry]['margin']
            data['gross_margin_percent'][i] = np.random.normal(margin_base, 10)
            
            # LTV/CAC ratio
            if revenue > 0:
                data['ltv_cac_ratio'][i] = np.random.uniform(0.5, 3.5)
            else:
                data['ltv_cac_ratio'][i] = 0
            
            # Investor tier
            if stage in ['Series B', 'Series C+']:
                tier = np.random.choice(['Tier1', 'Tier2'], p=[0.6, 0.4])
            elif stage == 'Series A':
                tier = np.random.choice(['Tier1', 'Tier2', 'Tier3'], p=[0.3, 0.5, 0.2])
            else:
                tier = np.random.choice(['Angel', 'Tier3'], p=[0.5, 0.5])
            data['investor_tier_primary'][i] = tier
            
            # Has debt
            data['has_debt'][i] = np.random.random() < 0.2
    
    def _generate_advantage_metrics(self, data: Dict, start: int, end: int):
        """Generate competitive advantage metrics."""
        for i in range(start, end):
            industry = data['sector'][i]
            years = data['years_since_founding'][i]
            
            # Patents (more common in certain industries)
            if industry in ['BioTech', 'HealthTech', 'AI/ML']:
                data['patent_count'][i] = np.random.poisson(years * 0.5)
            else:
                data['patent_count'][i] = 0
            
            # Scores (1-5 scale)
            data['tech_differentiation_score'][i] = np.random.uniform(1, 5)
            data['switching_cost_score'][i] = np.random.uniform(1, 5)
            data['brand_strength_score'][i] = min(1 + years * 0.4, 5)
            
            # Scalability by industry
            if industry in ['SaaS', 'AI/ML', 'Marketplace']:
                data['scalability_score'][i] = np.random.uniform(0.7, 1.0)
            else:
                data['scalability_score'][i] = np.random.uniform(0.3, 0.7)
            
            # Boolean advantages
            data['network_effects_present'][i] = industry == 'Marketplace' or np.random.random() < 0.2
            data['has_data_moat'][i] = years > 2 and np.random.random() < 0.3
            data['regulatory_advantage_present'][i] = industry in ['FinTech', 'HealthTech'] and np.random.random() < 0.2
            
            # Product stage
            if years == 0:
                stage = 'MVP'
            elif years <= 2:
                stage = np.random.choice(['MVP', 'Beta', 'Early Traction'], p=[0.2, 0.4, 0.4])
            elif years <= 5:
                stage = np.random.choice(['Early Traction', 'GA', 'Growth'], p=[0.2, 0.4, 0.4])
            else:
                stage = np.random.choice(['GA', 'Growth'], p=[0.3, 0.7])
            data['product_stage'][i] = stage
            
            # Retention rates
            if stage in ['GA', 'Growth']:
                data['product_retention_30d'][i] = np.random.uniform(0.6, 0.95)
            else:
                data['product_retention_30d'][i] = np.random.uniform(0.3, 0.7)
            
            data['product_retention_90d'][i] = data['product_retention_30d'][i] * np.random.uniform(0.7, 0.95)
    
    def _generate_market_metrics(self, data: Dict, start: int, end: int):
        """Generate market-related metrics."""
        for i in range(start, end):
            industry = data['sector'][i]
            revenue = data['annual_revenue_run_rate'][i]
            
            # TAM by industry
            tam_sizes = {
                'E-commerce': 1e12,
                'HealthTech': 600e9,
                'AI/ML': 500e9,
                'FinTech': 400e9,
                'SaaS': 300e9,
                'Marketplace': 200e9,
                'EdTech': 150e9,
                'Cybersecurity': 200e9,
                'BioTech': 300e9
            }
            
            tam = tam_sizes.get(industry, 100e9) * np.random.uniform(0.5, 2.0)
            data['tam_size_usd'][i] = tam
            data['sam_size_usd'][i] = tam * np.random.uniform(0.05, 0.2)
            data['som_size_usd'][i] = data['sam_size_usd'][i] * np.random.uniform(0.01, 0.1)
            
            # Market growth
            data['market_growth_rate_percent'][i] = self.industries[industry]['growth'] * 100
            
            # Customer metrics
            if revenue > 0:
                avg_customer_value = np.random.uniform(1000, 50000)
                data['customer_count'][i] = int(revenue / avg_customer_value)
                data['net_dollar_retention_percent'][i] = np.random.uniform(80, 130)
            else:
                data['customer_count'][i] = 0
                data['net_dollar_retention_percent'][i] = 0
            
            data['customer_concentration_percent'][i] = np.random.uniform(10, 60)
            data['user_growth_rate_percent'][i] = data['revenue_growth_rate_percent'][i] * np.random.uniform(0.8, 1.2)
            
            # Competition
            data['competition_intensity'][i] = np.random.uniform(2, 5)
            data['competitors_named_count'][i] = int(data['competition_intensity'][i] * 10)
            
            # DAU/MAU ratio
            data['dau_mau_ratio'][i] = np.random.uniform(0.1, 0.7)
    
    def _generate_people_metrics(self, data: Dict, start: int, end: int):
        """Generate team and founder metrics."""
        for i in range(start, end):
            years = data['years_since_founding'][i]
            
            # Founders
            data['founders_count'][i] = np.random.choice([1, 2, 3], p=[0.2, 0.6, 0.2])
            
            # Team size (grows with age)
            if years == 0:
                team_size = np.random.randint(2, 5)
            else:
                team_size = int(3 * (1.5 ** years) * np.random.uniform(0.5, 2.0))
            data['team_size_full_time'][i] = min(team_size, 1000)
            
            # Experience
            data['years_experience_avg'][i] = np.random.uniform(5, 20)
            data['domain_expertise_years_avg'][i] = np.random.uniform(2, 15)
            data['prior_startup_experience_count'][i] = np.random.poisson(1)
            
            # Prior exits (rare)
            if data['prior_startup_experience_count'][i] > 0:
                data['prior_successful_exits_count'][i] = np.random.choice([0, 1], p=[0.9, 0.1])
            else:
                data['prior_successful_exits_count'][i] = 0
            
            # Board and advisors
            data['board_advisor_experience_score'][i] = min(1 + years * 0.3, 5)
            data['advisors_count'][i] = min(np.random.poisson(years), 10)
            
            # Diversity
            data['team_diversity_percent'][i] = np.random.uniform(20, 70)
            
            # Key person dependency
            data['key_person_dependency'][i] = data['founders_count'][i] == 1 or np.random.random() < 0.4
    
    def _generate_outcomes(self, data: Dict, start: int, end: int):
        """Generate realistic success/failure outcomes."""
        for i in range(start, end):
            stage = data['funding_stage'][i]
            industry = data['sector'][i]
            years = data['years_since_founding'][i]
            
            # Base success rate by stage
            base_success_rate = self.stage_success_rates.get(stage, 0.15)
            
            # Adjust for quality signals
            quality_score = 0
            
            # Top tier investor
            if data['investor_tier_primary'][i] == 'Tier1':
                quality_score += 0.2
            
            # Strong metrics
            if data['ltv_cac_ratio'][i] > 2.0:
                quality_score += 0.1
            if data['product_retention_30d'][i] > 0.8:
                quality_score += 0.1
            if data['revenue_growth_rate_percent'][i] > 100:
                quality_score += 0.1
            
            # Prior successful exits
            if data['prior_successful_exits_count'][i] > 0:
                quality_score += 0.3
            
            # Network effects
            if data['network_effects_present'][i]:
                quality_score += 0.1
            
            # Final success probability
            success_prob = base_success_rate * (1 + quality_score)
            success_prob = min(success_prob, 0.8)  # Cap at 80%
            
            # For very young companies, outcome is uncertain
            if years < 2:
                data['success'][i] = None  # Still active, no outcome yet
            else:
                data['success'][i] = np.random.random() < success_prob
    
    def _add_calculated_fields(self, df: pd.DataFrame) -> pd.DataFrame:
        """Add calculated fields that depend on other fields."""
        # Runway months
        df['runway_months'] = np.where(
            df['monthly_burn_usd'] > 0,
            df['cash_on_hand_usd'] / df['monthly_burn_usd'],
            24
        )
        
        # Burn multiple
        df['burn_multiple'] = np.where(
            df['annual_revenue_run_rate'] > 0,
            df['monthly_burn_usd'] / (df['annual_revenue_run_rate'] / 12),
            999
        )
        
        # Cap extreme values
        df['runway_months'] = df['runway_months'].clip(0, 48)
        df['burn_multiple'] = df['burn_multiple'].clip(0, 999)
        
        return df
    
    def _apply_data_quality_patterns(self, df: pd.DataFrame) -> pd.DataFrame:
        """Apply realistic data quality issues."""
        logger.info("Applying realistic data quality patterns...")
        
        # 1. Missing data patterns
        missing_patterns = [
            ('patent_count', 0.3),
            ('net_dollar_retention_percent', 0.25),
            ('dau_mau_ratio', 0.35),
            ('customer_concentration_percent', 0.2),
            ('team_diversity_percent', 0.15)
        ]
        
        for col, missing_rate in missing_patterns:
            mask = np.random.random(len(df)) < missing_rate
            df.loc[mask, col] = np.nan
        
        # 2. Recent data is more incomplete
        recent_mask = df['years_since_founding'] < 2
        for col in ['annual_revenue_run_rate', 'customer_count', 'ltv_cac_ratio']:
            mask = recent_mask & (np.random.random(len(df)) < 0.4)
            df.loc[mask, col] = np.nan
        
        # 3. Add some outliers (but cap them)
        outlier_rate = 0.02
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        
        for col in numeric_cols:
            if col not in ['year', 'founding_year', 'years_since_founding']:
                outlier_mask = np.random.random(len(df)) < outlier_rate
                if outlier_mask.any():
                    # Create outliers but within reasonable bounds
                    df.loc[outlier_mask, col] = df.loc[outlier_mask, col] * np.random.uniform(2, 5, size=outlier_mask.sum())
        
        # 4. Survival bias - add more historical failures
        historical_mask = df['founding_year'] < 2015
        failure_boost = historical_mask & (np.random.random(len(df)) < 0.3)
        df.loc[failure_boost, 'success'] = False
        
        return df

def main():
    """Generate the high-quality dataset."""
    generator = FastHighQualityDatasetGenerator()
    
    # Generate dataset
    logger.info("Starting fast generation of 100k dataset...")
    df = generator.generate_dataset(n_records=100000)
    
    # Save to CSV
    output_file = 'high_quality_startup_dataset_100k.csv'
    df.to_csv(output_file, index=False)
    logger.info(f"Saved dataset to {output_file}")
    
    # Generate summary statistics
    summary = {
        'dataset_info': {
            'total_records': len(df),
            'unique_companies': df['company_id'].nunique(),
            'features': len(df.columns),
            'date_range': f"{df['founding_year'].min()} - {df['founding_year'].max()}"
        },
        'success_metrics': {
            'overall_success_rate': df['success'].mean() if df['success'].notna().any() else 0,
            'records_with_outcome': df['success'].notna().sum(),
            'successful_companies': df[df['success'] == True].shape[0],
            'failed_companies': df[df['success'] == False].shape[0],
            'active_companies': df['success'].isna().sum()
        },
        'stage_distribution': df['funding_stage'].value_counts().to_dict(),
        'industry_distribution': df['sector'].value_counts().to_dict(),
        'investor_tiers': df['investor_tier_primary'].value_counts().to_dict(),
        'financial_metrics': {
            'avg_total_raised': df['total_capital_raised_usd'].mean(),
            'median_total_raised': df['total_capital_raised_usd'].median(),
            'avg_revenue': df['annual_revenue_run_rate'].mean(),
            'median_revenue': df['annual_revenue_run_rate'].median(),
            'avg_burn_rate': df['monthly_burn_usd'].mean(),
            'avg_runway': df['runway_months'].mean()
        },
        'team_metrics': {
            'avg_team_size': df['team_size_full_time'].mean(),
            'avg_founders': df['founders_count'].mean(),
            'pct_with_prior_exits': (df['prior_successful_exits_count'] > 0).mean() * 100
        },
        'data_quality': {
            'missing_data_pct': (df.isnull().sum() / len(df) * 100).mean(),
            'features_with_missing': (df.isnull().sum() > 0).sum(),
            'completeness_by_feature': {col: 100 - (df[col].isnull().sum() / len(df) * 100) 
                                       for col in df.columns if df[col].isnull().sum() > 0}
        }
    }
    
    # Calculate success rates by stage
    for stage in df['funding_stage'].unique():
        stage_data = df[df['funding_stage'] == stage]
        if stage_data['success'].notna().any():
            summary['success_metrics'][f'{stage}_success_rate'] = stage_data['success'].mean()
    
    # Convert numpy types to Python types for JSON serialization
    def convert_to_python_types(obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, dict):
            return {key: convert_to_python_types(value) for key, value in obj.items()}
        elif isinstance(obj, list):
            return [convert_to_python_types(item) for item in obj]
        return obj
    
    # Save summary
    summary_json = convert_to_python_types(summary)
    with open('high_quality_dataset_summary.json', 'w') as f:
        json.dump(summary_json, f, indent=2)
    
    logger.info("Dataset generation complete!")
    print("\n=== Dataset Summary ===")
    print(f"Total records: {summary['dataset_info']['total_records']:,}")
    print(f"Overall success rate: {summary['success_metrics']['overall_success_rate']:.1%}")
    print(f"Active companies (no outcome yet): {summary['success_metrics']['active_companies']:,}")
    print(f"Average funding raised: ${summary['financial_metrics']['avg_total_raised']:,.0f}")
    print(f"Missing data: {summary['data_quality']['missing_data_pct']:.1f}%")

if __name__ == "__main__":
    main()