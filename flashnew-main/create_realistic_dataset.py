#!/usr/bin/env python3
"""
Create a truly realistic startup dataset based on real-world patterns
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
from typing import Dict, List, Tuple, Optional
import json

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

class RealisticStartupGenerator:
    def __init__(self):
        self.current_date = datetime.now()
        
        # Stage distributions (based on real data)
        self.stage_weights = {
            'pre_seed': 0.35,
            'seed': 0.25, 
            'series_a': 0.20,
            'series_b': 0.12,
            'series_c': 0.05,
            'series_d': 0.02,
            'series_e_plus': 0.01
        }
        
        # Sector distributions
        self.sectors = {
            'SaaS': 0.30,
            'Fintech': 0.15,
            'Healthcare': 0.12,
            'E-commerce': 0.10,
            'AI/ML': 0.08,
            'Marketplace': 0.07,
            'Consumer': 0.07,
            'Deep Tech': 0.06,
            'Other': 0.05
        }
        
        # Geographic distribution
        self.locations = {
            'SF Bay Area': 0.25,
            'New York': 0.15,
            'Boston': 0.08,
            'Los Angeles': 0.07,
            'Austin': 0.05,
            'Seattle': 0.05,
            'International': 0.20,
            'Other US': 0.15
        }
        
        # Success rates by stage (reach next stage)
        self.success_rates = {
            'pre_seed': 0.10,      # 10% reach Series A
            'seed': 0.22,          # 22% reach Series A
            'series_a': 0.38,      # 38% reach Series B
            'series_b': 0.52,      # 52% reach Series C
            'series_c': 0.65,      # 65% reach exit
            'series_d': 0.70,      # 70% reach exit
            'series_e_plus': 0.75  # 75% reach exit
        }
        
    def weighted_choice(self, choices: Dict[str, float]) -> str:
        """Make a weighted random choice"""
        items = list(choices.keys())
        weights = list(choices.values())
        return np.random.choice(items, p=weights)
    
    def generate_company_age(self, stage: str) -> int:
        """Generate realistic company age in months based on stage"""
        age_ranges = {
            'pre_seed': (3, 12),
            'seed': (6, 24),
            'series_a': (18, 48),
            'series_b': (36, 72),
            'series_c': (48, 96),
            'series_d': (60, 120),
            'series_e_plus': (72, 144)
        }
        min_age, max_age = age_ranges[stage]
        return np.random.randint(min_age, max_age + 1)
    
    def generate_funding(self, stage: str) -> Tuple[float, float]:
        """Generate realistic funding amounts (raised and on hand)"""
        if stage == 'pre_seed':
            # Log-normal distribution centered around $150K
            raised = np.random.lognormal(np.log(150000), 0.8)
            raised = np.clip(raised, 10000, 500000)
            on_hand = raised * np.random.uniform(0.5, 0.9)
            
        elif stage == 'seed':
            # Log-normal centered around $1.5M
            raised = np.random.lognormal(np.log(1500000), 0.6)
            raised = np.clip(raised, 250000, 3000000)
            on_hand = raised * np.random.uniform(0.4, 0.8)
            
        elif stage == 'series_a':
            # Log-normal centered around $10M
            raised = np.random.lognormal(np.log(10000000), 0.5)
            raised = np.clip(raised, 2000000, 25000000)
            on_hand = raised * np.random.uniform(0.3, 0.7)
            
        elif stage == 'series_b':
            # Log-normal centered around $30M
            raised = np.random.lognormal(np.log(30000000), 0.5)
            raised = np.clip(raised, 15000000, 60000000)
            on_hand = raised * np.random.uniform(0.3, 0.6)
            
        else:  # C+
            # Larger rounds
            raised = np.random.lognormal(np.log(50000000), 0.6)
            raised = np.clip(raised, 30000000, 200000000)
            on_hand = raised * np.random.uniform(0.2, 0.5)
            
        return round(raised), round(on_hand)
    
    def generate_revenue(self, stage: str, sector: str) -> float:
        """Generate realistic revenue based on stage"""
        if stage == 'pre_seed':
            # 85% have no revenue
            if np.random.random() < 0.85:
                return 0
            # 10% have $1-50K
            elif np.random.random() < 0.95:
                return np.random.uniform(1000, 50000)
            # 5% have $50-100K (exceptional)
            else:
                return np.random.uniform(50000, 100000)
                
        elif stage == 'seed':
            # 40% have no revenue
            if np.random.random() < 0.40:
                return 0
            # 30% have $1-100K
            elif np.random.random() < 0.70:
                return np.random.uniform(1000, 100000)
            # 20% have $100-500K
            elif np.random.random() < 0.90:
                return np.random.uniform(100000, 500000)
            # 10% have $500K-1M
            else:
                return np.random.uniform(500000, 1000000)
                
        elif stage == 'series_a':
            # Series A should have meaningful revenue
            if np.random.random() < 0.05:
                return np.random.uniform(100000, 500000)
            elif np.random.random() < 0.30:
                return np.random.uniform(500000, 1000000)
            elif np.random.random() < 0.70:
                return np.random.uniform(1000000, 3000000)
            elif np.random.random() < 0.95:
                return np.random.uniform(3000000, 10000000)
            else:
                return np.random.uniform(10000000, 20000000)
                
        elif stage == 'series_b':
            # Series B companies at scale
            return np.random.lognormal(np.log(15000000), 0.8)
            
        else:  # C+
            # Late stage companies
            return np.random.lognormal(np.log(50000000), 0.9)
    
    def generate_team_size(self, stage: str) -> int:
        """Generate realistic team size"""
        if stage == 'pre_seed':
            # 70% have 1-2 people
            if np.random.random() < 0.70:
                return np.random.randint(1, 3)
            # 25% have 3-4
            elif np.random.random() < 0.95:
                return np.random.randint(3, 5)
            # 5% have 5-6
            else:
                return np.random.randint(5, 7)
                
        elif stage == 'seed':
            # More distributed
            if np.random.random() < 0.30:
                return np.random.randint(3, 6)
            elif np.random.random() < 0.70:
                return np.random.randint(6, 11)
            elif np.random.random() < 0.95:
                return np.random.randint(11, 21)
            else:
                return np.random.randint(21, 31)
                
        elif stage == 'series_a':
            return int(np.random.lognormal(np.log(35), 0.5))
            
        elif stage == 'series_b':
            return int(np.random.lognormal(np.log(100), 0.5))
            
        else:  # C+
            return int(np.random.lognormal(np.log(250), 0.6))
    
    def generate_customers(self, stage: str, revenue: float, sector: str) -> int:
        """Generate realistic customer count"""
        if stage == 'pre_seed':
            if revenue == 0:
                # 60% have no customers
                if np.random.random() < 0.60:
                    return 0
                # 40% have some beta users
                else:
                    return np.random.randint(1, 20)
            else:
                # If they have revenue, they have some customers
                return np.random.randint(5, 50)
                
        elif stage == 'seed':
            if revenue == 0:
                return np.random.randint(0, 10)
            elif revenue < 100000:
                return np.random.randint(10, 100)
            elif revenue < 500000:
                return np.random.randint(50, 500)
            else:
                return np.random.randint(100, 1000)
                
        else:  # Later stages
            # Rough estimate based on revenue and sector
            if sector == 'E-commerce':
                # B2C typically has more customers
                return int(revenue / np.random.uniform(50, 200))
            elif sector == 'SaaS':
                # B2B SaaS has fewer, higher-value customers
                return int(revenue / np.random.uniform(5000, 50000))
            else:
                return int(revenue / np.random.uniform(1000, 10000))
    
    def generate_product_stage(self, funding_stage: str) -> str:
        """Generate realistic product stage"""
        product_stages = {
            'pre_seed': {
                'idea': 0.40,
                'prototype': 0.35,
                'mvp': 0.20,
                'beta': 0.05
            },
            'seed': {
                'prototype': 0.05,
                'mvp': 0.15,
                'beta': 0.50,
                'live': 0.25,
                'growth': 0.05
            },
            'series_a': {
                'beta': 0.05,
                'live': 0.35,
                'growth': 0.50,
                'scale': 0.10
            },
            'series_b': {
                'live': 0.10,
                'growth': 0.40,
                'scale': 0.40,
                'mature': 0.10
            }
        }
        
        # Later stages default to scale/mature
        if funding_stage not in product_stages:
            return np.random.choice(['scale', 'mature'], p=[0.6, 0.4])
            
        return self.weighted_choice(product_stages[funding_stage])
    
    def generate_metrics(self, stage: str, revenue: float, customers: int) -> Dict:
        """Generate stage-appropriate metrics"""
        metrics = {}
        
        # Burn rate (monthly)
        if stage == 'pre_seed':
            metrics['monthly_burn_usd'] = np.random.uniform(5000, 30000)
        elif stage == 'seed':
            metrics['monthly_burn_usd'] = np.random.uniform(30000, 150000)
        elif stage == 'series_a':
            metrics['monthly_burn_usd'] = np.random.uniform(150000, 500000)
        else:
            metrics['monthly_burn_usd'] = np.random.uniform(500000, 2000000)
            
        # Growth metrics (only if there's revenue)
        if revenue > 0:
            if stage in ['pre_seed', 'seed']:
                # High variance in early stage
                metrics['revenue_growth_rate_percent'] = np.random.uniform(-50, 300)
                metrics['user_growth_rate_percent'] = np.random.uniform(-20, 200)
            else:
                # More stable growth in later stages
                if stage == 'series_a':
                    metrics['revenue_growth_rate_percent'] = np.random.uniform(50, 300)
                elif stage == 'series_b':
                    metrics['revenue_growth_rate_percent'] = np.random.uniform(40, 200)
                else:
                    metrics['revenue_growth_rate_percent'] = np.random.uniform(20, 150)
                    
                metrics['user_growth_rate_percent'] = metrics['revenue_growth_rate_percent'] * np.random.uniform(0.7, 1.3)
        else:
            metrics['revenue_growth_rate_percent'] = 0
            metrics['user_growth_rate_percent'] = 0
            
        # Retention metrics (only if product is live)
        if customers > 10:
            if stage == 'pre_seed':
                metrics['product_retention_30d'] = np.random.uniform(0.2, 0.6)
            elif stage == 'seed':
                metrics['product_retention_30d'] = np.random.uniform(0.3, 0.7)
            else:
                metrics['product_retention_30d'] = np.random.uniform(0.5, 0.9)
                
            metrics['product_retention_90d'] = metrics['product_retention_30d'] * np.random.uniform(0.5, 0.8)
            metrics['net_dollar_retention_percent'] = 100 * np.random.uniform(0.8, 1.3) if revenue > 0 else 0
        else:
            metrics['product_retention_30d'] = 0
            metrics['product_retention_90d'] = 0
            metrics['net_dollar_retention_percent'] = 0
            
        # LTV/CAC (only meaningful with revenue)
        if revenue > 100000 and customers > 50:
            metrics['ltv_cac_ratio'] = np.random.uniform(0.5, 5.0)
        else:
            metrics['ltv_cac_ratio'] = 0
            
        # Gross margin (if revenue)
        if revenue > 0:
            if stage in ['pre_seed', 'seed']:
                metrics['gross_margin_percent'] = np.random.uniform(20, 80)
            else:
                metrics['gross_margin_percent'] = np.random.uniform(40, 90)
        else:
            metrics['gross_margin_percent'] = 0
            
        return metrics
    
    def generate_team_metrics(self, stage: str, team_size: int) -> Dict:
        """Generate team-related metrics"""
        metrics = {}
        
        # Founders count
        if stage == 'pre_seed':
            metrics['founders_count'] = np.random.choice([1, 2, 3], p=[0.2, 0.7, 0.1])
        else:
            metrics['founders_count'] = np.random.choice([1, 2, 3, 4], p=[0.1, 0.6, 0.25, 0.05])
            
        # Experience metrics
        if stage == 'pre_seed':
            metrics['years_experience_avg'] = np.random.uniform(3, 15)
            metrics['domain_expertise_years_avg'] = np.random.uniform(1, 10)
        else:
            metrics['years_experience_avg'] = np.random.uniform(5, 20)
            metrics['domain_expertise_years_avg'] = np.random.uniform(3, 15)
            
        # Prior startup experience
        metrics['prior_startup_experience_count'] = np.random.poisson(0.8)
        metrics['prior_successful_exits_count'] = 0 if np.random.random() < 0.85 else np.random.randint(1, 3)
        
        # Team composition
        metrics['team_diversity_percent'] = np.random.uniform(10, 60)
        metrics['key_person_dependency'] = team_size < 5 or np.random.random() < 0.3
        
        # Advisors
        if stage == 'pre_seed':
            metrics['advisors_count'] = np.random.poisson(1)
            metrics['board_advisor_experience_score'] = np.random.randint(1, 4)
        else:
            metrics['advisors_count'] = np.random.poisson(3)
            metrics['board_advisor_experience_score'] = np.random.randint(2, 5)
            
        return metrics
    
    def generate_competitive_metrics(self, sector: str, stage: str) -> Dict:
        """Generate competitive landscape metrics"""
        metrics = {}
        
        # Hot sectors have more competition
        if sector in ['AI/ML', 'Fintech', 'SaaS']:
            metrics['competitors_named_count'] = np.random.poisson(20)
            metrics['competition_intensity'] = np.random.randint(3, 6)
        else:
            metrics['competitors_named_count'] = np.random.poisson(10)
            metrics['competition_intensity'] = np.random.randint(1, 5)
            
        # Differentiation scores
        if stage == 'pre_seed':
            metrics['tech_differentiation_score'] = np.random.randint(1, 4)
            metrics['brand_strength_score'] = 1
        elif stage == 'seed':
            metrics['tech_differentiation_score'] = np.random.randint(2, 5)
            metrics['brand_strength_score'] = np.random.randint(1, 3)
        else:
            metrics['tech_differentiation_score'] = np.random.randint(2, 6)
            metrics['brand_strength_score'] = np.random.randint(2, 5)
            
        # Moat characteristics
        metrics['patent_count'] = 0 if np.random.random() < 0.7 else np.random.poisson(2)
        metrics['network_effects_present'] = np.random.random() < 0.3
        metrics['has_data_moat'] = np.random.random() < 0.2 and stage != 'pre_seed'
        metrics['regulatory_advantage_present'] = np.random.random() < 0.1
        
        # Switching costs
        if stage == 'pre_seed':
            metrics['switching_cost_score'] = np.random.randint(1, 3)
        else:
            metrics['switching_cost_score'] = np.random.randint(1, 6)
            
        metrics['scalability_score'] = np.random.randint(2, 6)
        
        return metrics
    
    def add_missing_data(self, company: Dict, stage: str) -> Dict:
        """Realistically add missing data based on stage"""
        missing_rates = {
            'pre_seed': 0.4,
            'seed': 0.25,
            'series_a': 0.15,
            'series_b': 0.10,
            'series_c': 0.08,
            'series_d': 0.05,
            'series_e_plus': 0.05
        }
        
        missing_rate = missing_rates.get(stage, 0.05)
        
        # Some fields are more likely to be missing
        optional_fields = [
            'product_retention_30d', 'product_retention_90d',
            'ltv_cac_ratio', 'net_dollar_retention_percent',
            'user_growth_rate_percent', 'customer_concentration_percent',
            'dau_mau_ratio', 'vertical_integration_score',
            'time_to_market_advantage_years', 'partnership_leverage_score',
            'cash_efficiency_score', 'operating_leverage_trend'
        ]
        
        for field in optional_fields:
            if field in company and np.random.random() < missing_rate:
                company[field] = None
                
        return company
    
    def generate_company(self, force_success: Optional[bool] = None) -> Dict:
        """Generate a single realistic company"""
        # Basic attributes
        stage = self.weighted_choice(self.stage_weights)
        sector = self.weighted_choice(self.sectors)
        location = self.weighted_choice(self.locations)
        
        # Age and funding
        company_age_months = self.generate_company_age(stage)
        total_raised, cash_on_hand = self.generate_funding(stage)
        
        # Revenue and customers
        revenue = self.generate_revenue(stage, sector)
        team_size = self.generate_team_size(stage)
        customers = self.generate_customers(stage, revenue, sector)
        
        # Product stage
        product_stage = self.generate_product_stage(stage)
        
        # Build company dict
        company = {
            'funding_stage': stage,
            'sector': sector,
            'company_age_months': company_age_months,
            'total_capital_raised_usd': total_raised,
            'cash_on_hand_usd': cash_on_hand,
            'annual_revenue_run_rate': revenue,
            'team_size_full_time': team_size,
            'customer_count': customers,
            'product_stage': product_stage
        }
        
        # Add various metrics
        metrics = self.generate_metrics(stage, revenue, customers)
        company.update(metrics)
        
        team_metrics = self.generate_team_metrics(stage, team_size)
        company.update(team_metrics)
        
        competitive_metrics = self.generate_competitive_metrics(sector, stage)
        company.update(competitive_metrics)
        
        # Market metrics
        if sector in ['AI/ML', 'Fintech', 'Healthcare']:
            tam_base = 10000000000  # $10B
        else:
            tam_base = 5000000000   # $5B
            
        company['tam_size_usd'] = tam_base * np.random.uniform(0.5, 10)
        company['sam_size_usd'] = company['tam_size_usd'] * np.random.uniform(0.05, 0.2)
        company['som_size_usd'] = company['sam_size_usd'] * np.random.uniform(0.01, 0.1)
        company['market_growth_rate_percent'] = np.random.uniform(10, 100)
        
        # Additional metrics
        company['runway_months'] = company['cash_on_hand_usd'] / company['monthly_burn_usd'] if company['monthly_burn_usd'] > 0 else 0
        company['burn_multiple'] = company['annual_revenue_run_rate'] / (company['monthly_burn_usd'] * 12) if company['monthly_burn_usd'] > 0 and revenue > 0 else 0
        
        # Investor tier
        if stage == 'pre_seed':
            company['investor_tier_primary'] = np.random.choice(['none', 'Angel'], p=[0.6, 0.4])
        elif stage == 'seed':
            company['investor_tier_primary'] = np.random.choice(['Angel', 'Tier 3', 'Tier 2'], p=[0.3, 0.5, 0.2])
        elif stage == 'series_a':
            company['investor_tier_primary'] = np.random.choice(['Tier 3', 'Tier 2', 'Tier 1'], p=[0.3, 0.5, 0.2])
        else:
            company['investor_tier_primary'] = np.random.choice(['Tier 2', 'Tier 1'], p=[0.4, 0.6])
            
        # Other boolean/categorical fields
        company['has_debt'] = np.random.random() < 0.15
        company['has_repeat_founder'] = company['prior_successful_exits_count'] > 0
        company['strategic_partners_count'] = np.random.poisson(1 if stage in ['pre_seed', 'seed'] else 3)
        
        # Risk and efficiency scores
        company['execution_risk_score'] = np.random.randint(1, 6)
        company['vertical_integration_score'] = np.random.randint(1, 5)
        company['time_to_market_advantage_years'] = np.random.uniform(0, 2)
        company['partnership_leverage_score'] = np.random.randint(1, 5)
        company['cash_efficiency_score'] = np.random.uniform(0.3, 2.0)
        company['operating_leverage_trend'] = np.random.uniform(-1, 1)
        company['predictive_modeling_score'] = np.random.randint(1, 5)
        
        # DAU/MAU ratio
        if customers > 0 and product_stage in ['live', 'growth', 'scale', 'mature']:
            company['dau_mau_ratio'] = np.random.uniform(0.1, 0.6)
        else:
            company['dau_mau_ratio'] = 0
            
        # Customer concentration
        if customers > 0:
            company['customer_concentration_percent'] = np.random.uniform(5, 60)
        else:
            company['customer_concentration_percent'] = 0
            
        # Determine success
        if force_success is not None:
            company['success'] = force_success
        else:
            # Success probability based on stage and quality signals
            base_success_rate = self.success_rates[stage]
            
            # Adjust based on quality signals
            if company['prior_successful_exits_count'] > 0:
                base_success_rate *= 1.5
            if company['investor_tier_primary'] == 'Tier 1':
                base_success_rate *= 1.3
            if revenue > 0 and stage == 'pre_seed':
                base_success_rate *= 2.0  # Revenue at pre-seed is strong signal
            if company['runway_months'] < 6:
                base_success_rate *= 0.5
            if team_size == 1 and stage != 'pre_seed':
                base_success_rate *= 0.3  # Solo founder past pre-seed is risky
                
            # Cap at reasonable bounds
            base_success_rate = min(base_success_rate, 0.9)
            
            company['success'] = 1 if np.random.random() < base_success_rate else 0
            
        # Add missing data realistically
        company = self.add_missing_data(company, stage)
        
        return company
    
    def generate_dataset(self, n_companies: int = 100000) -> pd.DataFrame:
        """Generate full dataset"""
        companies = []
        
        # Calculate how many successful companies we need
        target_success_rate = 0.16  # 16% overall success rate
        n_successful = int(n_companies * target_success_rate)
        n_failed = n_companies - n_successful
        
        print(f"Generating {n_companies} companies...")
        print(f"Target: {n_successful} successful ({target_success_rate*100:.1f}%), {n_failed} failed")
        
        # Generate successful companies
        for i in range(n_successful):
            if i % 1000 == 0:
                print(f"Generated {i}/{n_companies} companies...")
            companies.append(self.generate_company(force_success=True))
            
        # Generate failed companies
        for i in range(n_failed):
            if (i + n_successful) % 1000 == 0:
                print(f"Generated {i + n_successful}/{n_companies} companies...")
            companies.append(self.generate_company(force_success=False))
            
        # Shuffle to mix successful and failed companies
        random.shuffle(companies)
        
        # Convert to DataFrame
        df = pd.DataFrame(companies)
        
        # Add company names
        df['company_name'] = [f"Company_{i:06d}" for i in range(len(df))]
        
        # Reorder columns
        column_order = [
            'company_name', 'funding_stage', 'sector', 'product_stage',
            'company_age_months', 'total_capital_raised_usd', 'cash_on_hand_usd',
            'monthly_burn_usd', 'runway_months', 'burn_multiple',
            'annual_revenue_run_rate', 'revenue_growth_rate_percent',
            'customer_count', 'user_growth_rate_percent', 'customer_concentration_percent',
            'team_size_full_time', 'founders_count', 'years_experience_avg',
            'success'
        ]
        
        # Get remaining columns
        remaining_cols = [col for col in df.columns if col not in column_order]
        column_order.extend(remaining_cols)
        
        # Reorder DataFrame
        df = df[column_order]
        
        return df


def validate_dataset(df: pd.DataFrame) -> None:
    """Validate the dataset meets realistic criteria"""
    print("\n" + "="*60)
    print("DATASET VALIDATION REPORT")
    print("="*60)
    
    # Overall statistics
    print(f"\nTotal companies: {len(df):,}")
    print(f"Success rate: {df['success'].mean()*100:.1f}%")
    
    # Stage distribution
    print("\nStage Distribution:")
    stage_dist = df['funding_stage'].value_counts()
    for stage, count in stage_dist.items():
        print(f"  {stage}: {count:,} ({count/len(df)*100:.1f}%)")
    
    # Pre-seed validation
    print("\nPre-Seed Validation:")
    pre_seed = df[df['funding_stage'] == 'pre_seed']
    print(f"  Total pre-seed companies: {len(pre_seed):,}")
    print(f"  With $0 revenue: {(pre_seed['annual_revenue_run_rate'] == 0).sum()/len(pre_seed)*100:.1f}%")
    print(f"  With >$100k revenue: {(pre_seed['annual_revenue_run_rate'] > 100000).sum()/len(pre_seed)*100:.1f}%")
    print(f"  Average team size: {pre_seed['team_size_full_time'].mean():.1f}")
    print(f"  With >10 employees: {(pre_seed['team_size_full_time'] > 10).sum()/len(pre_seed)*100:.1f}%")
    print(f"  Average funding: ${pre_seed['total_capital_raised_usd'].mean():,.0f}")
    print(f"  Success rate: {pre_seed['success'].mean()*100:.1f}%")
    
    # Seed validation
    print("\nSeed Stage Validation:")
    seed = df[df['funding_stage'] == 'seed']
    print(f"  Total seed companies: {len(seed):,}")
    print(f"  With $0 revenue: {(seed['annual_revenue_run_rate'] == 0).sum()/len(seed)*100:.1f}%")
    print(f"  With >$100k revenue: {(seed['annual_revenue_run_rate'] > 100000).sum()/len(seed)*100:.1f}%")
    print(f"  Average team size: {seed['team_size_full_time'].mean():.1f}")
    print(f"  Average funding: ${seed['total_capital_raised_usd'].mean():,.0f}")
    print(f"  Success rate: {seed['success'].mean()*100:.1f}%")
    
    # Revenue distribution by stage
    print("\nRevenue Distribution by Stage:")
    for stage in ['pre_seed', 'seed', 'series_a', 'series_b']:
        stage_data = df[df['funding_stage'] == stage]
        if len(stage_data) > 0:
            print(f"\n  {stage}:")
            print(f"    Median revenue: ${stage_data['annual_revenue_run_rate'].median():,.0f}")
            print(f"    % with $0: {(stage_data['annual_revenue_run_rate'] == 0).sum()/len(stage_data)*100:.1f}%")
            print(f"    % with >$1M: {(stage_data['annual_revenue_run_rate'] > 1000000).sum()/len(stage_data)*100:.1f}%")
    
    # Product stage distribution
    print("\nProduct Stage Distribution (Pre-seed):")
    if 'product_stage' in pre_seed.columns:
        ps_dist = pre_seed['product_stage'].value_counts()
        for ps, count in ps_dist.items():
            print(f"  {ps}: {count/len(pre_seed)*100:.1f}%")
    
    # Missing data statistics
    print("\nMissing Data Statistics:")
    missing_pct = df.isnull().sum() / len(df) * 100
    high_missing = missing_pct[missing_pct > 10].sort_values(ascending=False)
    if len(high_missing) > 0:
        print("  Fields with >10% missing:")
        for field, pct in high_missing.items():
            print(f"    {field}: {pct:.1f}%")
    else:
        print("  No fields with >10% missing data")
    
    print("\n" + "="*60)


def main():
    """Main function to generate the dataset"""
    print("Starting realistic dataset generation...")
    print(f"Timestamp: {datetime.now()}")
    
    # Create generator
    generator = RealisticStartupGenerator()
    
    # Generate dataset
    df = generator.generate_dataset(n_companies=100000)
    
    # Save to CSV
    output_file = "realistic_startup_dataset_100k.csv"
    df.to_csv(output_file, index=False)
    print(f"\nDataset saved to: {output_file}")
    
    # Validate dataset
    validate_dataset(df)
    
    # Save summary statistics
    summary = {
        'generation_date': datetime.now().isoformat(),
        'total_companies': len(df),
        'success_rate': float(df['success'].mean()),
        'stage_distribution': df['funding_stage'].value_counts().to_dict(),
        'sector_distribution': df['sector'].value_counts().to_dict(),
        'pre_seed_stats': {
            'count': len(df[df['funding_stage'] == 'pre_seed']),
            'zero_revenue_pct': float((df[df['funding_stage'] == 'pre_seed']['annual_revenue_run_rate'] == 0).mean()),
            'avg_team_size': float(df[df['funding_stage'] == 'pre_seed']['team_size_full_time'].mean()),
            'avg_funding': float(df[df['funding_stage'] == 'pre_seed']['total_capital_raised_usd'].mean())
        }
    }
    
    with open('dataset_generation_summary.json', 'w') as f:
        json.dump(summary, f, indent=2)
    
    print("\nDataset generation complete!")
    print(f"Files created:")
    print(f"  - {output_file}")
    print(f"  - dataset_generation_summary.json")


if __name__ == "__main__":
    main()