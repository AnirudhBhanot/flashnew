#!/usr/bin/env python3
"""
Generate 200k realistic startup dataset with real-world messiness
Includes successful companies with bad metrics and failed companies with good metrics
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import json

class RealisticStartupGenerator:
    def __init__(self):
        # Real startup data references (based on public information)
        self.real_examples = {
            'successful_with_issues': [
                {
                    'name': 'Uber',
                    'burn_multiple': 15.0,  # Burned cash heavily
                    'runway_months': 3,  # Often near death
                    'gross_margin_percent': -50,  # Negative for years
                    'success': True
                },
                {
                    'name': 'Twitter',
                    'revenue_growth_rate_percent': -5,  # Revenue declined some years
                    'product_retention_30d': 40,  # Low retention
                    'burn_multiple': 8.0,
                    'success': True
                },
                {
                    'name': 'Snapchat',
                    'ltv_cac_ratio': 0.8,  # Spent more to acquire than earn
                    'gross_margin_percent': -20,
                    'burn_multiple': 12.0,
                    'success': True
                }
            ],
            'failed_with_good_metrics': [
                {
                    'name': 'Quibi',
                    'total_capital_raised_usd': 1750000000,
                    'team_quality': 'exceptional',  # Hollywood veterans
                    'product_retention_30d': 60,  # Decent initial retention
                    'success': False
                },
                {
                    'name': 'Theranos',
                    'total_capital_raised_usd': 945000000,
                    'investor_tier': 'tier_1',  # Top investors
                    'board_advisor_experience_score': 5,  # Henry Kissinger, etc.
                    'success': False
                },
                {
                    'name': 'Pets.com',
                    'revenue_growth_rate_percent': 300,  # Growing fast
                    'brand_strength_score': 5,  # Famous sock puppet
                    'market_growth_rate_percent': 50,
                    'success': False
                }
            ]
        }
        
        # Industry distributions (based on CB Insights data)
        self.industries = {
            'SaaS': 0.22,
            'FinTech': 0.15,
            'HealthTech': 0.12,
            'E-commerce': 0.10,
            'AI/ML': 0.08,
            'Marketplace': 0.07,
            'EdTech': 0.06,
            'Gaming': 0.05,
            'Blockchain': 0.04,
            'CleanTech': 0.03,
            'FoodTech': 0.03,
            'Other': 0.05
        }
        
        # Stage distributions (from PitchBook data)
        self.stage_distribution = {
            'pre_seed': 0.35,
            'seed': 0.30,
            'series_a': 0.20,
            'series_b': 0.10,
            'series_c': 0.05
        }
        
        # Realistic success rates by stage (from multiple studies)
        self.success_rates = {
            'pre_seed': 0.10,  # 10% make it
            'seed': 0.15,      # 15% succeed
            'series_a': 0.25,  # 25% succeed
            'series_b': 0.35,  # 35% succeed
            'series_c': 0.45   # 45% succeed
        }
        
        # Add noise factors
        self.noise_factors = {
            'timing_luck': 0.15,  # 15% random factor
            'execution_variance': 0.20,  # 20% execution difference
            'market_shock': 0.10,  # 10% external factors
            'competition_surprise': 0.10  # 10% competitive dynamics
        }

    def generate_company(self, index, force_outcome=None):
        """Generate a single company with realistic attributes"""
        
        # Basic attributes
        stage = np.random.choice(list(self.stage_distribution.keys()), 
                               p=list(self.stage_distribution.values()))
        industry = np.random.choice(list(self.industries.keys()), 
                                  p=list(self.industries.values()))
        
        # Determine base success probability
        base_success_prob = self.success_rates[stage]
        
        # Add realistic variance
        luck_factor = np.random.normal(0, self.noise_factors['timing_luck'])
        execution_factor = np.random.normal(0, self.noise_factors['execution_variance'])
        market_factor = np.random.normal(0, self.noise_factors['market_shock'])
        
        # Calculate actual success with noise
        success_prob = base_success_prob + luck_factor + execution_factor + market_factor
        success_prob = np.clip(success_prob, 0, 1)
        
        # Determine outcome
        if force_outcome is not None:
            success = force_outcome
        else:
            success = np.random.random() < success_prob
        
        # Generate metrics based on success BUT with realistic variance
        company = self._generate_metrics(stage, industry, success, success_prob)
        company['company_id'] = f"company_{index:06d}"
        company['success'] = int(success)
        company['funding_stage'] = stage
        company['sector'] = industry
        
        # Add random anomalies (successful companies with bad metrics)
        if success and np.random.random() < 0.15:  # 15% of successful companies
            company = self._add_negative_anomalies(company)
        
        # Add random anomalies (failed companies with good metrics)  
        if not success and np.random.random() < 0.20:  # 20% of failed companies
            company = self._add_positive_anomalies(company)
        
        return company
    
    def _generate_metrics(self, stage, industry, success, success_prob):
        """Generate realistic metrics with variance"""
        
        metrics = {}
        
        # Stage multipliers
        stage_mult = {
            'pre_seed': 0.1,
            'seed': 0.3,
            'series_a': 1.0,
            'series_b': 3.0,
            'series_c': 10.0
        }[stage]
        
        # Financial metrics with realistic distributions
        if stage == 'pre_seed':
            metrics['total_capital_raised_usd'] = np.random.lognormal(12, 1.5)  # ~100k-2M
            metrics['annual_revenue_run_rate'] = np.random.lognormal(10, 2) if success else np.random.lognormal(8, 2)
        elif stage == 'seed':
            metrics['total_capital_raised_usd'] = np.random.lognormal(14, 1.2)  # ~1M-5M
            metrics['annual_revenue_run_rate'] = np.random.lognormal(12, 1.8) if success else np.random.lognormal(10, 2)
        elif stage == 'series_a':
            metrics['total_capital_raised_usd'] = np.random.lognormal(16, 1)  # ~5M-20M
            metrics['annual_revenue_run_rate'] = np.random.lognormal(14, 1.5) if success else np.random.lognormal(12, 2)
        elif stage == 'series_b':
            metrics['total_capital_raised_usd'] = np.random.lognormal(17.5, 0.8)  # ~20M-100M
            metrics['annual_revenue_run_rate'] = np.random.lognormal(15.5, 1.2) if success else np.random.lognormal(13.5, 1.8)
        else:  # series_c
            metrics['total_capital_raised_usd'] = np.random.lognormal(18.5, 0.7)  # ~50M-500M
            metrics['annual_revenue_run_rate'] = np.random.lognormal(16.5, 1) if success else np.random.lognormal(14.5, 1.5)
        
        # Cash and burn
        metrics['cash_on_hand_usd'] = metrics['total_capital_raised_usd'] * np.random.uniform(0.3, 0.8)
        metrics['monthly_burn_usd'] = metrics['cash_on_hand_usd'] / np.random.uniform(6, 24)
        metrics['runway_months'] = metrics['cash_on_hand_usd'] / metrics['monthly_burn_usd']
        
        # Growth metrics with high variance
        base_growth = 100 if success else 20
        growth_variance = 100  # High variance!
        metrics['revenue_growth_rate_percent'] = np.random.normal(base_growth, growth_variance)
        metrics['user_growth_rate_percent'] = np.random.normal(base_growth * 0.8, growth_variance * 0.8)
        
        # Burn multiple (lower is better, but high variance)
        if success:
            metrics['burn_multiple'] = abs(np.random.normal(2, 3))  # Can be high even for successful
        else:
            metrics['burn_multiple'] = abs(np.random.normal(5, 5))  # Very high variance
        
        # Unit economics
        if success:
            metrics['ltv_cac_ratio'] = np.random.lognormal(1.2, 0.5)  # Usually > 1
            metrics['gross_margin_percent'] = np.random.normal(70, 30)  # Can be negative!
        else:
            metrics['ltv_cac_ratio'] = np.random.lognormal(0.5, 0.5)  # Usually < 1
            metrics['gross_margin_percent'] = np.random.normal(40, 40)  # High variance
        
        # Market metrics
        tam_base = 16 + np.random.normal(0, 2)  # log scale
        metrics['tam_size_usd'] = np.exp(tam_base)
        metrics['sam_size_usd'] = metrics['tam_size_usd'] * np.random.uniform(0.05, 0.3)
        metrics['som_size_usd'] = metrics['sam_size_usd'] * np.random.uniform(0.01, 0.1)
        metrics['market_growth_rate_percent'] = np.random.normal(30, 20)
        
        # Team metrics (can be good even for failures)
        metrics['founders_count'] = np.random.choice([1, 2, 3, 4], p=[0.3, 0.5, 0.15, 0.05])
        metrics['team_size_full_time'] = int(np.random.lognormal(2 + stage_mult, 1))
        metrics['years_experience_avg'] = np.random.uniform(3, 20)
        metrics['domain_expertise_years_avg'] = np.random.uniform(1, 15)
        metrics['prior_startup_experience_count'] = np.random.poisson(1.5)
        metrics['prior_successful_exits_count'] = np.random.poisson(0.3)
        
        # Product metrics with realistic variance
        if success:
            metrics['product_retention_30d'] = np.random.beta(7, 3) * 100  # Skewed high but not always
            metrics['product_retention_90d'] = metrics['product_retention_30d'] * np.random.uniform(0.5, 0.9)
        else:
            metrics['product_retention_30d'] = np.random.beta(3, 7) * 100  # Skewed low but not always
            metrics['product_retention_90d'] = metrics['product_retention_30d'] * np.random.uniform(0.3, 0.8)
        
        # Some successful companies have terrible retention (e.g., dating apps)
        if success and industry in ['Dating', 'Gaming', 'E-commerce'] and np.random.random() < 0.3:
            metrics['product_retention_30d'] = np.random.uniform(10, 30)
            metrics['product_retention_90d'] = metrics['product_retention_30d'] * 0.5
        
        # Other metrics
        metrics['customer_count'] = int(np.random.lognormal(3 + stage_mult * 2, 2))
        metrics['customer_concentration_percent'] = np.random.beta(2, 5) * 100
        metrics['net_dollar_retention_percent'] = np.random.normal(110 if success else 90, 30)
        metrics['dau_mau_ratio'] = np.random.beta(3, 7)
        
        # Scores (1-5)
        for score in ['tech_differentiation_score', 'switching_cost_score', 'brand_strength_score',
                     'competition_intensity', 'board_advisor_experience_score']:
            # Even failed companies can have high scores
            metrics[score] = np.random.choice([1, 2, 3, 4, 5], 
                                            p=[0.1, 0.2, 0.3, 0.3, 0.1] if success else [0.2, 0.3, 0.3, 0.15, 0.05])
        
        # Scalability score (0-1)
        metrics['scalability_score'] = np.random.beta(5 if success else 3, 3)
        
        # Boolean features
        metrics['network_effects_present'] = int(np.random.random() < (0.4 if success else 0.2))
        metrics['has_data_moat'] = int(np.random.random() < (0.3 if success else 0.1))
        metrics['regulatory_advantage_present'] = int(np.random.random() < 0.1)
        metrics['has_debt'] = int(np.random.random() < 0.3)
        metrics['key_person_dependency'] = int(np.random.random() < 0.7)
        
        # Additional counts
        metrics['patent_count'] = np.random.poisson(2 if success else 0.5)
        metrics['competitors_named_count'] = np.random.poisson(10)
        metrics['advisors_count'] = np.random.poisson(3)
        metrics['team_diversity_percent'] = np.random.uniform(10, 60)
        
        # Stage
        stage_map = {'pre_seed': 0, 'seed': 1, 'series_a': 2, 'series_b': 3, 'series_c': 4}
        metrics['funding_stage'] = stage_map[stage]
        
        # Product stage
        if stage == 'pre_seed':
            metrics['product_stage'] = np.random.choice([0, 1], p=[0.7, 0.3])  # MVP, Beta
        elif stage == 'seed':
            metrics['product_stage'] = np.random.choice([1, 2], p=[0.6, 0.4])  # Beta, Early
        else:
            metrics['product_stage'] = np.random.choice([2, 3, 4], p=[0.3, 0.5, 0.2])  # Early, Growth, GA
        
        # Investor tier
        if stage in ['series_b', 'series_c']:
            metrics['investor_tier_primary'] = np.random.choice([0, 1, 2, 3], p=[0.5, 0.3, 0.15, 0.05])
        elif stage == 'series_a':
            metrics['investor_tier_primary'] = np.random.choice([0, 1, 2, 3], p=[0.3, 0.4, 0.2, 0.1])
        else:
            metrics['investor_tier_primary'] = np.random.choice([0, 1, 2, 3], p=[0.1, 0.3, 0.4, 0.2])
        
        return metrics
    
    def _add_negative_anomalies(self, company):
        """Add realistic negative anomalies to successful companies"""
        anomaly_type = np.random.choice(['burn', 'growth', 'retention', 'economics'])
        
        if anomaly_type == 'burn':
            # Uber-like: massive burn
            company['burn_multiple'] = np.random.uniform(10, 20)
            company['runway_months'] = np.random.uniform(3, 9)
            company['monthly_burn_usd'] *= 3
        elif anomaly_type == 'growth':
            # Twitter-like: stagnant growth
            company['revenue_growth_rate_percent'] = np.random.uniform(-20, 20)
            company['user_growth_rate_percent'] = np.random.uniform(-10, 10)
        elif anomaly_type == 'retention':
            # Dating app-like: low retention but still successful
            company['product_retention_30d'] = np.random.uniform(15, 35)
            company['product_retention_90d'] = company['product_retention_30d'] * 0.5
        elif anomaly_type == 'economics':
            # MoviePass-like: negative unit economics
            company['ltv_cac_ratio'] = np.random.uniform(0.3, 0.8)
            company['gross_margin_percent'] = np.random.uniform(-50, 10)
        
        return company
    
    def _add_positive_anomalies(self, company):
        """Add realistic positive anomalies to failed companies"""
        anomaly_type = np.random.choice(['funding', 'team', 'growth', 'product'])
        
        if anomaly_type == 'funding':
            # Quibi-like: massive funding
            company['total_capital_raised_usd'] *= 10
            company['investor_tier_primary'] = 0  # Tier 1
        elif anomaly_type == 'team':
            # Theranos-like: stellar team on paper
            company['board_advisor_experience_score'] = 5
            company['years_experience_avg'] = 20
            company['prior_successful_exits_count'] = 3
        elif anomaly_type == 'growth':
            # Pets.com-like: fast growth but unsustainable
            company['revenue_growth_rate_percent'] = np.random.uniform(200, 400)
            company['user_growth_rate_percent'] = np.random.uniform(150, 300)
        elif anomaly_type == 'product':
            # Good product metrics but other issues
            company['product_retention_30d'] = np.random.uniform(70, 85)
            company['net_dollar_retention_percent'] = np.random.uniform(120, 150)
        
        return company
    
    def generate_dataset(self, n_companies=200000, include_real_examples=True):
        """Generate full dataset with realistic distributions"""
        
        companies = []
        
        # Add some forced edge cases based on real examples
        if include_real_examples:
            print("Adding real-world inspired edge cases...")
            
            # Successful companies with bad metrics (10 examples)
            for i in range(10):
                company = self.generate_company(i, force_outcome=True)
                company = self._add_negative_anomalies(company)
                companies.append(company)
            
            # Failed companies with good metrics (10 examples)
            for i in range(10, 20):
                company = self.generate_company(i, force_outcome=False)
                company = self._add_positive_anomalies(company)
                companies.append(company)
        
        # Generate the rest
        print(f"Generating {n_companies - len(companies)} companies with realistic variance...")
        for i in range(len(companies), n_companies):
            if i % 10000 == 0:
                print(f"  Generated {i:,} companies...")
            company = self.generate_company(i)
            companies.append(company)
        
        # Convert to DataFrame
        df = pd.DataFrame(companies)
        
        # Add some missing values randomly (real data has gaps)
        optional_fields = ['advisors_count', 'patent_count', 'team_diversity_percent']
        for field in optional_fields:
            mask = np.random.random(len(df)) < 0.05  # 5% missing
            df.loc[mask, field] = np.nan
        
        # Final cleanup
        df = df.fillna(0)
        
        # Ensure we have the exact 45 features expected
        expected_features = [
            'total_capital_raised_usd', 'cash_on_hand_usd', 'monthly_burn_usd',
            'runway_months', 'burn_multiple', 'investor_tier_primary', 'has_debt',
            'patent_count', 'network_effects_present', 'has_data_moat',
            'regulatory_advantage_present', 'tech_differentiation_score',
            'switching_cost_score', 'brand_strength_score', 'scalability_score',
            'sector', 'tam_size_usd', 'sam_size_usd', 'som_size_usd',
            'market_growth_rate_percent', 'customer_count', 'customer_concentration_percent',
            'user_growth_rate_percent', 'net_dollar_retention_percent',
            'competition_intensity', 'competitors_named_count', 'founders_count',
            'team_size_full_time', 'years_experience_avg', 'domain_expertise_years_avg',
            'prior_startup_experience_count', 'prior_successful_exits_count',
            'board_advisor_experience_score', 'advisors_count', 'team_diversity_percent',
            'key_person_dependency', 'product_stage', 'product_retention_30d',
            'product_retention_90d', 'dau_mau_ratio', 'annual_revenue_run_rate',
            'revenue_growth_rate_percent', 'gross_margin_percent', 'ltv_cac_ratio',
            'funding_stage'
        ]
        
        # Add company_id and success
        all_columns = ['company_id'] + expected_features + ['success']
        df = df[all_columns]
        
        return df
    
    def analyze_dataset(self, df):
        """Analyze the generated dataset"""
        print("\n📊 Dataset Analysis")
        print("=" * 60)
        
        print(f"\nTotal companies: {len(df):,}")
        print(f"Success rate: {df['success'].mean():.1%}")
        
        print("\nSuccess rate by stage:")
        stage_map = {0: 'Pre-seed', 1: 'Seed', 2: 'Series A', 3: 'Series B', 4: 'Series C'}
        for stage, name in stage_map.items():
            mask = df['funding_stage'] == stage
            if mask.any():
                print(f"  {name}: {df[mask]['success'].mean():.1%} ({mask.sum():,} companies)")
        
        print("\nKey metrics comparison (Success vs Failure):")
        metrics_to_compare = [
            'annual_revenue_run_rate', 'revenue_growth_rate_percent', 
            'burn_multiple', 'product_retention_30d', 'ltv_cac_ratio'
        ]
        
        for metric in metrics_to_compare:
            success_mean = df[df['success'] == 1][metric].mean()
            failure_mean = df[df['success'] == 0][metric].mean()
            print(f"  {metric}:")
            print(f"    Success: {success_mean:,.1f}")
            print(f"    Failure: {failure_mean:,.1f}")
        
        # Check for anomalies
        print("\n🎲 Realistic anomalies:")
        
        # Successful companies with high burn
        high_burn_success = df[(df['success'] == 1) & (df['burn_multiple'] > 10)]
        print(f"  Successful companies with burn_multiple > 10: {len(high_burn_success):,} ({len(high_burn_success)/df['success'].sum():.1%})")
        
        # Failed companies with great metrics
        good_failed = df[(df['success'] == 0) & 
                        (df['revenue_growth_rate_percent'] > 200) & 
                        (df['product_retention_30d'] > 70)]
        print(f"  Failed companies with growth > 200% and retention > 70%: {len(good_failed):,}")
        
        # Successful companies with negative margins
        neg_margin_success = df[(df['success'] == 1) & (df['gross_margin_percent'] < 0)]
        print(f"  Successful companies with negative gross margins: {len(neg_margin_success):,}")

def main():
    """Generate the enhanced 200k dataset"""
    
    print("🚀 Generating Enhanced 200k Startup Dataset")
    print("=" * 60)
    print("Features: Realistic variance, edge cases, and anomalies")
    print("Based on: Real startup patterns and public data")
    print("=" * 60)
    
    # Initialize generator
    generator = RealisticStartupGenerator()
    
    # Generate dataset
    df = generator.generate_dataset(n_companies=200000, include_real_examples=True)
    
    # Analyze
    generator.analyze_dataset(df)
    
    # Save
    print("\n💾 Saving dataset...")
    df.to_csv('realistic_200k_dataset.csv', index=False)
    print(f"✅ Saved to realistic_200k_dataset.csv ({df.memory_usage().sum() / 1024**2:.1f} MB)")
    
    # Save a sample for inspection
    sample = df.sample(1000, random_state=42)
    sample.to_csv('realistic_200k_sample.csv', index=False)
    print(f"✅ Saved 1000-row sample to realistic_200k_sample.csv")
    
    # Save metadata
    metadata = {
        'generation_date': datetime.now().isoformat(),
        'total_companies': len(df),
        'success_rate': float(df['success'].mean()),
        'features': list(df.columns),
        'realistic_factors': {
            'timing_luck': 0.15,
            'execution_variance': 0.20,
            'market_shock': 0.10,
            'anomaly_rate': 0.15
        }
    }
    
    with open('realistic_200k_metadata.json', 'w') as f:
        json.dump(metadata, f, indent=2)
    
    print("\n✅ Dataset generation complete!")
    print("📊 This dataset includes:")
    print("  - Successful companies with terrible metrics (like Uber)")
    print("  - Failed companies with great metrics (like Quibi)")
    print("  - Realistic variance and noise")
    print("  - Stage-appropriate distributions")
    print("  - Industry-specific patterns")

if __name__ == "__main__":
    main()