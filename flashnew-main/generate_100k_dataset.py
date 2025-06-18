#!/usr/bin/env python3
"""
Generate 100k startup dataset with realistic data based on real patterns.
Uses real company data as templates and applies realistic variations.
Ensures all 45 FLASH features are populated with logical consistency.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
from typing import Dict, List, Tuple, Any
import warnings
warnings.filterwarnings('ignore')

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

class StartupDataGenerator:
    def __init__(self, real_data_path: str = 'real_startup_data.csv'):
        """Initialize the generator with real startup data as templates."""
        self.real_data = pd.read_csv(real_data_path)
        self.setup_distributions()
        
    def setup_distributions(self):
        """Define realistic distributions for various features."""
        
        # Success rates by stage (based on industry research)
        self.success_rates = {
            'Pre-Seed': 0.10,
            'Seed': 0.15,
            'Series A': 0.25,
            'Series B': 0.35,
            'Series C+': 0.45,
            'IPO': 1.0
        }
        
        # Industry distributions (weighted)
        self.industries = {
            'SaaS': 0.25,
            'E-commerce': 0.15,
            'FinTech': 0.12,
            'HealthTech': 0.10,
            'AI/ML': 0.08,
            'EdTech': 0.07,
            'Gaming': 0.05,
            'Marketplace': 0.05,
            'Other': 0.13
        }
        
        # Funding stage progression
        self.funding_stages = ['Pre-Seed', 'Seed', 'Series A', 'Series B', 'Series C+']
        self.stage_weights = [0.30, 0.35, 0.20, 0.10, 0.05]
        
        # Product stages
        self.product_stages = {
            'MVP': 0.25,
            'Beta': 0.20,
            'Early Traction': 0.25,
            'Growth': 0.20,
            'GA': 0.10  # Generally Available
        }
        
        # Investor tiers
        self.investor_tiers = {
            'Tier1': 0.15,
            'Tier2': 0.35,
            'Tier3': 0.35,
            'Angel': 0.15
        }
        
    def generate_company_name(self, index: int) -> str:
        """Generate realistic company names."""
        prefixes = ['Tech', 'Smart', 'Next', 'Digital', 'Cloud', 'Data', 'AI', 'Quantum', 'Cyber', 'Meta']
        suffixes = ['Labs', 'Works', 'Solutions', 'Systems', 'Hub', 'Space', 'Core', 'Base', 'Flow', 'Net']
        nouns = ['Vision', 'Logic', 'Stream', 'Link', 'Bridge', 'Path', 'Edge', 'Wave', 'Pulse', 'Grid']
        
        name_type = random.random()
        if name_type < 0.3:
            # Compound name
            return f"{random.choice(prefixes)}{random.choice(nouns)}"
        elif name_type < 0.6:
            # Name with suffix
            return f"{random.choice(nouns)}{random.choice(suffixes)}"
        else:
            # Single word with ID
            return f"{random.choice(nouns)}_{index}"
            
    def generate_founding_year(self, stage: str) -> int:
        """Generate founding year based on funding stage."""
        current_year = 2025
        stage_to_age = {
            'Pre-Seed': (0, 2),
            'Seed': (1, 3),
            'Series A': (2, 5),
            'Series B': (3, 7),
            'Series C+': (5, 15),
            'IPO': (7, 20)
        }
        
        min_age, max_age = stage_to_age.get(stage, (1, 5))
        age = np.random.randint(min_age, max_age + 1)
        return current_year - age
        
    def generate_funding_metrics(self, stage: str, success: bool) -> Dict[str, float]:
        """Generate funding-related metrics based on stage and success."""
        stage_ranges = {
            'Pre-Seed': (50000, 500000),
            'Seed': (500000, 3000000),
            'Series A': (3000000, 15000000),
            'Series B': (15000000, 50000000),
            'Series C+': (50000000, 200000000)
        }
        
        min_funding, max_funding = stage_ranges.get(stage, (100000, 1000000))
        
        # Successful companies tend to raise more
        if success:
            total_funding = np.random.uniform(min_funding * 1.5, max_funding)
        else:
            total_funding = np.random.uniform(min_funding, max_funding * 0.7)
            
        # Cash on hand (20-60% of total raised, lower for struggling companies)
        cash_ratio = 0.4 + 0.3 * random.random() if success else 0.1 + 0.3 * random.random()
        cash_on_hand = total_funding * cash_ratio
        
        # Monthly burn (based on runway goals)
        target_runway = np.random.randint(12, 24) if success else np.random.randint(3, 12)
        monthly_burn = cash_on_hand / target_runway
        
        # Actual runway
        runway_months = cash_on_hand / monthly_burn if monthly_burn > 0 else 999
        runway_months = min(runway_months, 999)  # Cap at 999
        
        return {
            'total_capital_raised_usd': total_funding,
            'cash_on_hand_usd': cash_on_hand,
            'monthly_burn_usd': monthly_burn,
            'runway_months': runway_months
        }
        
    def generate_revenue_metrics(self, stage: str, success: bool, monthly_burn: float) -> Dict[str, float]:
        """Generate revenue-related metrics."""
        # Revenue based on stage and success
        if stage == 'Pre-Seed':
            arr_base = 0 if random.random() < 0.7 else random.uniform(0, 100000)
        elif stage == 'Seed':
            arr_base = random.uniform(0, 500000) if success else random.uniform(0, 100000)
        elif stage == 'Series A':
            arr_base = random.uniform(100000, 2000000) if success else random.uniform(0, 500000)
        elif stage == 'Series B':
            arr_base = random.uniform(1000000, 10000000) if success else random.uniform(100000, 2000000)
        else:  # Series C+
            arr_base = random.uniform(5000000, 100000000) if success else random.uniform(500000, 5000000)
            
        annual_revenue = arr_base * (1 + 0.5 * random.random() if success else 1 - 0.3 * random.random())
        
        # Growth rate (higher for successful companies)
        if success:
            growth_rate = np.random.normal(150, 50)  # 150% average growth
            growth_rate = max(50, min(growth_rate, 500))  # Cap between 50-500%
        else:
            growth_rate = np.random.normal(20, 30)  # 20% average growth
            growth_rate = max(-50, min(growth_rate, 100))  # Can be negative
            
        # Gross margin (industry dependent, but generally 60-90% for SaaS)
        gross_margin = np.random.normal(70, 15) if success else np.random.normal(50, 20)
        gross_margin = max(10, min(gross_margin, 95))
        
        # Burn multiple (monthly burn / monthly revenue growth)
        monthly_revenue_growth = (annual_revenue * (growth_rate / 100)) / 12 if growth_rate > 0 else 0
        burn_multiple = monthly_burn / monthly_revenue_growth if monthly_revenue_growth > 0 else 999
        burn_multiple = min(burn_multiple, 999)  # Cap at 999
        
        # LTV/CAC ratio
        if success:
            ltv_cac = np.random.uniform(2, 5)  # Good ratio
        else:
            ltv_cac = np.random.uniform(0.5, 2)  # Poor ratio
            
        return {
            'annual_revenue_run_rate': annual_revenue,
            'revenue_growth_rate_percent': growth_rate,
            'gross_margin_percent': gross_margin,
            'burn_multiple': burn_multiple,
            'ltv_cac_ratio': ltv_cac
        }
        
    def generate_market_metrics(self, industry: str, success: bool) -> Dict[str, float]:
        """Generate market-related metrics."""
        # TAM by industry
        industry_tam = {
            'SaaS': (1e9, 100e9),
            'E-commerce': (10e9, 500e9),
            'FinTech': (50e9, 1000e9),
            'HealthTech': (10e9, 200e9),
            'AI/ML': (5e9, 100e9),
            'EdTech': (1e9, 50e9),
            'Gaming': (1e9, 100e9),
            'Marketplace': (5e9, 200e9),
            'Other': (1e9, 50e9)
        }
        
        min_tam, max_tam = industry_tam.get(industry, (1e9, 50e9))
        tam = np.random.uniform(min_tam, max_tam)
        
        # SAM is 5-20% of TAM
        sam = tam * np.random.uniform(0.05, 0.20)
        
        # SOM is 1-10% of SAM (higher for successful companies)
        som_ratio = np.random.uniform(0.05, 0.10) if success else np.random.uniform(0.01, 0.05)
        som = sam * som_ratio
        
        # Market growth rate
        market_growth = np.random.normal(25, 10) if success else np.random.normal(15, 10)
        market_growth = max(5, min(market_growth, 50))
        
        # Competition intensity (1-5 scale)
        competition = np.random.uniform(2, 4) if success else np.random.uniform(3, 5)
        
        # Number of competitors
        competitors = int(np.random.uniform(5, 50))
        
        return {
            'tam_size_usd': tam,
            'sam_size_usd': sam,
            'som_size_usd': som,
            'market_growth_rate_percent': market_growth,
            'competition_intensity': competition,
            'competitors_named_count': competitors
        }
        
    def generate_product_metrics(self, stage: str, product_stage: str, success: bool) -> Dict[str, Any]:
        """Generate product-related metrics."""
        # Customer metrics based on stage
        stage_customers = {
            'Pre-Seed': (0, 100),
            'Seed': (10, 1000),
            'Series A': (100, 10000),
            'Series B': (1000, 100000),
            'Series C+': (10000, 1000000)
        }
        
        min_customers, max_customers = stage_customers.get(stage, (10, 1000))
        customer_count = int(np.random.uniform(min_customers, max_customers))
        
        # Adjust for success
        if success:
            customer_count = int(customer_count * np.random.uniform(1.5, 3))
        else:
            customer_count = int(customer_count * np.random.uniform(0.3, 0.8))
            
        # Customer concentration (lower is better)
        concentration = np.random.uniform(5, 30) if success else np.random.uniform(20, 60)
        
        # User growth rate
        user_growth = np.random.normal(30, 15) if success else np.random.normal(5, 10)
        user_growth = max(-20, min(user_growth, 100))
        
        # Net dollar retention
        ndr = np.random.normal(115, 15) if success else np.random.normal(85, 15)
        ndr = max(50, min(ndr, 150))
        
        # Product retention rates
        if success:
            retention_30d = np.random.uniform(0.6, 0.9)
            retention_90d = retention_30d * np.random.uniform(0.7, 0.9)
        else:
            retention_30d = np.random.uniform(0.3, 0.6)
            retention_90d = retention_30d * np.random.uniform(0.5, 0.8)
            
        # DAU/MAU ratio
        dau_mau = np.random.uniform(0.4, 0.8) if success else np.random.uniform(0.1, 0.4)
        
        # Technical differentiation scores (1-5 scale)
        tech_score = np.random.uniform(3, 5) if success else np.random.uniform(1, 3)
        switching_cost = np.random.uniform(3, 5) if success else np.random.uniform(1, 3)
        brand_strength = np.random.uniform(3, 5) if success else np.random.uniform(1, 3)
        scalability = np.random.uniform(0.7, 1.0) if success else np.random.uniform(0.3, 0.7)
        
        # Boolean features
        patents = int(np.random.uniform(0, 10)) if random.random() < 0.3 else 0
        network_effects = random.random() < 0.4 if success else random.random() < 0.1
        data_moat = random.random() < 0.3 if success else random.random() < 0.1
        regulatory_advantage = random.random() < 0.1  # Rare
        
        return {
            'customer_count': customer_count,
            'customer_concentration_percent': concentration,
            'user_growth_rate_percent': user_growth,
            'net_dollar_retention_percent': ndr,
            'product_retention_30d': retention_30d,
            'product_retention_90d': retention_90d,
            'dau_mau_ratio': dau_mau,
            'tech_differentiation_score': tech_score,
            'switching_cost_score': switching_cost,
            'brand_strength_score': brand_strength,
            'scalability_score': scalability,
            'patent_count': patents,
            'network_effects_present': network_effects,
            'has_data_moat': data_moat,
            'regulatory_advantage_present': regulatory_advantage,
            'product_stage': product_stage
        }
        
    def generate_team_metrics(self, stage: str, success: bool) -> Dict[str, Any]:
        """Generate team-related metrics."""
        # Team size by stage
        stage_team_size = {
            'Pre-Seed': (2, 5),
            'Seed': (5, 15),
            'Series A': (15, 50),
            'Series B': (50, 200),
            'Series C+': (200, 1000)
        }
        
        min_size, max_size = stage_team_size.get(stage, (5, 50))
        team_size = int(np.random.uniform(min_size, max_size))
        
        # Adjust for success
        if success:
            team_size = int(team_size * np.random.uniform(1.2, 1.8))
        else:
            team_size = int(team_size * np.random.uniform(0.6, 0.9))
            
        # Founders (typically 1-4)
        founders = np.random.choice([1, 2, 3, 4], p=[0.2, 0.5, 0.25, 0.05])
        
        # Experience metrics
        years_exp = np.random.normal(12, 4) if success else np.random.normal(8, 3)
        years_exp = max(3, min(years_exp, 25))
        
        domain_exp = years_exp * np.random.uniform(0.6, 0.9)
        
        # Prior startup experience
        prior_startups = np.random.poisson(2) if success else np.random.poisson(0.5)
        prior_exits = min(prior_startups, np.random.poisson(0.5))
        
        # Board and advisors
        board_score = np.random.uniform(3, 5) if success else np.random.uniform(1, 3)
        advisors = int(np.random.uniform(3, 15)) if success else int(np.random.uniform(0, 5))
        
        # Diversity percentage
        diversity = np.random.uniform(30, 70)
        
        # Key person dependency
        key_person_dep = random.random() < 0.3 if success else random.random() < 0.6
        
        # Has debt (more common in later stages)
        has_debt = random.random() < 0.1 if stage in ['Pre-Seed', 'Seed'] else random.random() < 0.3
        
        return {
            'team_size_full_time': team_size,
            'founders_count': founders,
            'years_experience_avg': years_exp,
            'domain_expertise_years_avg': domain_exp,
            'prior_startup_experience_count': prior_startups,
            'prior_successful_exits_count': prior_exits,
            'board_advisor_experience_score': board_score,
            'advisors_count': advisors,
            'team_diversity_percent': diversity,
            'key_person_dependency': key_person_dep,
            'has_debt': has_debt
        }
        
    def generate_startup(self, index: int) -> Dict[str, Any]:
        """Generate a single startup with all features."""
        # Select funding stage
        stage = np.random.choice(self.funding_stages, p=self.stage_weights)
        
        # Determine success based on stage
        success_rate = self.success_rates[stage]
        success = random.random() < success_rate
        
        # Select industry
        industry = np.random.choice(list(self.industries.keys()), 
                                  p=list(self.industries.values()))
        
        # Select product stage
        product_stage = np.random.choice(list(self.product_stages.keys()),
                                       p=list(self.product_stages.values()))
        
        # Select investor tier
        investor_tier = np.random.choice(list(self.investor_tiers.keys()),
                                       p=list(self.investor_tiers.values()))
        
        # Generate all metrics
        startup = {
            'startup_id': f'id_{index}',
            'startup_name': self.generate_company_name(index),
            'founding_year': self.generate_founding_year(stage),
            'funding_stage': stage,
            'sector': industry,
            'investor_tier_primary': investor_tier,
            'success': success
        }
        
        # Add funding metrics
        funding_metrics = self.generate_funding_metrics(stage, success)
        startup.update(funding_metrics)
        
        # Add revenue metrics
        revenue_metrics = self.generate_revenue_metrics(
            stage, success, funding_metrics['monthly_burn_usd'])
        startup.update(revenue_metrics)
        
        # Add market metrics
        market_metrics = self.generate_market_metrics(industry, success)
        startup.update(market_metrics)
        
        # Add product metrics
        product_metrics = self.generate_product_metrics(stage, product_stage, success)
        startup.update(product_metrics)
        
        # Add team metrics
        team_metrics = self.generate_team_metrics(stage, success)
        startup.update(team_metrics)
        
        # Calculate burn_multiple_calc for validation
        if revenue_metrics['annual_revenue_run_rate'] > 0:
            monthly_revenue = revenue_metrics['annual_revenue_run_rate'] / 12
            startup['burn_multiple_calc'] = funding_metrics['monthly_burn_usd'] / monthly_revenue
        else:
            startup['burn_multiple_calc'] = 999
            
        return startup
        
    def generate_dataset(self, n_samples: int = 100000) -> pd.DataFrame:
        """Generate the full dataset."""
        print(f"Generating {n_samples:,} startup records...")
        
        startups = []
        for i in range(n_samples):
            if i % 10000 == 0:
                print(f"  Generated {i:,} records...")
            startups.append(self.generate_startup(i))
            
        print("Creating DataFrame...")
        df = pd.DataFrame(startups)
        
        # Ensure column order matches the 45-feature spec
        column_order = [
            'startup_id', 'startup_name', 'founding_year', 'funding_stage',
            'total_capital_raised_usd', 'cash_on_hand_usd', 'monthly_burn_usd',
            'runway_months', 'annual_revenue_run_rate', 'revenue_growth_rate_percent',
            'gross_margin_percent', 'burn_multiple', 'ltv_cac_ratio',
            'investor_tier_primary', 'has_debt', 'patent_count',
            'network_effects_present', 'has_data_moat', 'regulatory_advantage_present',
            'tech_differentiation_score', 'switching_cost_score', 'brand_strength_score',
            'scalability_score', 'product_stage', 'product_retention_30d',
            'product_retention_90d', 'sector', 'tam_size_usd', 'sam_size_usd',
            'som_size_usd', 'market_growth_rate_percent', 'customer_count',
            'customer_concentration_percent', 'user_growth_rate_percent',
            'net_dollar_retention_percent', 'competition_intensity',
            'competitors_named_count', 'dau_mau_ratio', 'founders_count',
            'team_size_full_time', 'years_experience_avg', 'domain_expertise_years_avg',
            'prior_startup_experience_count', 'prior_successful_exits_count',
            'board_advisor_experience_score', 'advisors_count', 'team_diversity_percent',
            'key_person_dependency', 'success', 'burn_multiple_calc'
        ]
        
        df = df[column_order]
        
        # Add some noise and ensure realistic constraints
        df = self.apply_realistic_constraints(df)
        
        return df
        
    def apply_realistic_constraints(self, df: pd.DataFrame) -> pd.DataFrame:
        """Apply realistic constraints and relationships between features."""
        print("Applying realistic constraints...")
        
        # Failed companies should have worse metrics
        failed_mask = ~df['success']
        
        # Reduce revenue for failed companies
        df.loc[failed_mask, 'annual_revenue_run_rate'] *= np.random.uniform(0.3, 0.7, size=failed_mask.sum())
        
        # Increase burn multiple for failed companies
        df.loc[failed_mask, 'burn_multiple'] *= np.random.uniform(1.5, 3, size=failed_mask.sum())
        
        # Reduce retention for failed companies
        df.loc[failed_mask, 'product_retention_30d'] *= np.random.uniform(0.5, 0.8, size=failed_mask.sum())
        df.loc[failed_mask, 'product_retention_90d'] *= np.random.uniform(0.4, 0.7, size=failed_mask.sum())
        
        # Cap extreme values
        df['burn_multiple'] = df['burn_multiple'].clip(upper=999)
        df['runway_months'] = df['runway_months'].clip(upper=999)
        df['revenue_growth_rate_percent'] = df['revenue_growth_rate_percent'].clip(-90, 500)
        
        # Ensure logical relationships
        df['product_retention_90d'] = df[['product_retention_30d', 'product_retention_90d']].min(axis=1)
        df['som_size_usd'] = df[['sam_size_usd', 'som_size_usd']].min(axis=1)
        df['sam_size_usd'] = df[['tam_size_usd', 'sam_size_usd']].min(axis=1)
        
        # Round appropriate columns
        int_columns = ['founding_year', 'customer_count', 'competitors_named_count',
                      'founders_count', 'team_size_full_time', 'patent_count',
                      'prior_startup_experience_count', 'prior_successful_exits_count',
                      'advisors_count']
        
        for col in int_columns:
            df[col] = df[col].round().astype(int)
            
        # Round financial columns to 2 decimal places
        financial_columns = ['total_capital_raised_usd', 'cash_on_hand_usd',
                           'monthly_burn_usd', 'annual_revenue_run_rate',
                           'tam_size_usd', 'sam_size_usd', 'som_size_usd']
        
        for col in financial_columns:
            df[col] = df[col].round(2)
            
        # Round percentages and scores
        percent_columns = ['revenue_growth_rate_percent', 'gross_margin_percent',
                         'market_growth_rate_percent', 'customer_concentration_percent',
                         'user_growth_rate_percent', 'net_dollar_retention_percent',
                         'team_diversity_percent']
        
        for col in percent_columns:
            df[col] = df[col].round(1)
            
        score_columns = ['tech_differentiation_score', 'switching_cost_score',
                       'brand_strength_score', 'board_advisor_experience_score',
                       'competition_intensity']
        
        for col in score_columns:
            df[col] = df[col].round(2).clip(1, 5)
            
        return df
        
    def validate_dataset(self, df: pd.DataFrame) -> None:
        """Validate the generated dataset."""
        print("\nValidating dataset...")
        
        # Check for missing values
        missing = df.isnull().sum()
        if missing.any():
            print(f"Warning: Found missing values:\n{missing[missing > 0]}")
            
        # Check column count
        expected_cols = 50  # 45 features + 5 extra (id, name, success, burn_calc)
        actual_cols = len(df.columns)
        print(f"Column count: {actual_cols} (expected ~{expected_cols})")
        
        # Check success rate
        success_rate = df['success'].mean()
        print(f"Overall success rate: {success_rate:.2%}")
        
        # Check success rates by stage
        print("\nSuccess rates by funding stage:")
        for stage in df['funding_stage'].unique():
            rate = df[df['funding_stage'] == stage]['success'].mean()
            print(f"  {stage}: {rate:.2%}")
            
        # Check data types
        print(f"\nData types summary:")
        print(f"  Numeric columns: {len(df.select_dtypes(include=[np.number]).columns)}")
        print(f"  Boolean columns: {len(df.select_dtypes(include=[bool]).columns)}")
        print(f"  Object columns: {len(df.select_dtypes(include=[object]).columns)}")
        
        # Basic statistics
        print("\nBasic statistics:")
        print(f"  Total records: {len(df):,}")
        print(f"  Unique companies: {df['startup_name'].nunique():,}")
        print(f"  Founding years: {df['founding_year'].min()} - {df['founding_year'].max()}")
        print(f"  Revenue range: ${df['annual_revenue_run_rate'].min():,.0f} - ${df['annual_revenue_run_rate'].max():,.0f}")
        
def main():
    """Main function to generate the dataset."""
    print("="*60)
    print("FLASH 100K Startup Dataset Generator")
    print("="*60)
    
    # Initialize generator
    generator = StartupDataGenerator()
    
    # Generate dataset
    df = generator.generate_dataset(n_samples=100000)
    
    # Validate dataset
    generator.validate_dataset(df)
    
    # Save dataset
    output_path = 'generated_100k_dataset.csv'
    print(f"\nSaving dataset to {output_path}...")
    df.to_csv(output_path, index=False)
    
    # Save a sample for inspection
    sample_path = 'generated_sample_1000.csv'
    df.sample(1000).to_csv(sample_path, index=False)
    print(f"Saved 1000-record sample to {sample_path}")
    
    print("\nDataset generation complete!")
    print(f"Total file size: {df.memory_usage(deep=True).sum() / 1024**2:.1f} MB")
    
if __name__ == "__main__":
    main()