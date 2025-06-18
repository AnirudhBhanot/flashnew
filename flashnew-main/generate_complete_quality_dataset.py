#!/usr/bin/env python3
"""
Complete high-quality 100k startup dataset with all features.
Optimized for efficiency while maintaining full quality.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
import logging
import warnings
from typing import Dict, List, Optional, Tuple
import multiprocessing as mp
from functools import partial
import yfinance as yf

warnings.filterwarnings('ignore')
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

class CompleteDatasetGenerator:
    """Generate complete high-quality startup dataset with all features."""
    
    def __init__(self):
        self.market_data = self._load_market_data_efficient()
        
        # Real patterns from industry research
        self.stage_progression = {
            'Pre-Seed': {'next': 'Seed', 'years': 1, 'success_rate': 0.10},
            'Seed': {'next': 'Series A', 'years': 2, 'success_rate': 0.15},
            'Series A': {'next': 'Series B', 'years': 2, 'success_rate': 0.25},
            'Series B': {'next': 'Series C+', 'years': 3, 'success_rate': 0.35},
            'Series C+': {'next': None, 'years': None, 'success_rate': 0.45}
        }
        
        self.industries = {
            'SaaS': {'growth': 0.25, 'margin': 75, 'fail_rate': 0.72, 'tam': 300e9},
            'AI/ML': {'growth': 0.35, 'margin': 70, 'fail_rate': 0.75, 'tam': 500e9},
            'FinTech': {'growth': 0.22, 'margin': 60, 'fail_rate': 0.70, 'tam': 400e9},
            'HealthTech': {'growth': 0.18, 'margin': 55, 'fail_rate': 0.65, 'tam': 600e9},
            'E-commerce': {'growth': 0.15, 'margin': 35, 'fail_rate': 0.80, 'tam': 1000e9},
            'Marketplace': {'growth': 0.17, 'margin': 70, 'fail_rate': 0.85, 'tam': 200e9},
            'EdTech': {'growth': 0.16, 'margin': 65, 'fail_rate': 0.70, 'tam': 150e9},
            'Cybersecurity': {'growth': 0.23, 'margin': 80, 'fail_rate': 0.60, 'tam': 200e9},
            'BioTech': {'growth': 0.14, 'margin': 45, 'fail_rate': 0.85, 'tam': 300e9}
        }
        
        # Real startup ecosystems
        self.ecosystems = {
            'Silicon Valley': {'weight': 0.25, 'quality_boost': 1.2},
            'New York': {'weight': 0.15, 'quality_boost': 1.1},
            'Boston': {'weight': 0.10, 'quality_boost': 1.1},
            'Austin': {'weight': 0.08, 'quality_boost': 1.0},
            'Seattle': {'weight': 0.07, 'quality_boost': 1.1},
            'Los Angeles': {'weight': 0.06, 'quality_boost': 0.9},
            'Denver': {'weight': 0.04, 'quality_boost': 0.9},
            'Chicago': {'weight': 0.04, 'quality_boost': 0.9},
            'Atlanta': {'weight': 0.03, 'quality_boost': 0.8},
            'Miami': {'weight': 0.03, 'quality_boost': 0.8},
            'Other': {'weight': 0.15, 'quality_boost': 0.7}
        }
        
        # Top VCs and their success multipliers
        self.top_vcs = {
            'Sequoia Capital': 2.5,
            'Andreessen Horowitz': 2.3,
            'Accel': 2.2,
            'Founders Fund': 2.4,
            'Kleiner Perkins': 2.1,
            'GV': 2.0,
            'Benchmark': 2.3,
            'Greylock Partners': 2.1,
            'Index Ventures': 2.0,
            'Lightspeed': 1.9,
            'Y Combinator': 2.2,
            'Techstars': 1.8
        }
    
    def _load_market_data_efficient(self) -> Dict:
        """Load market data efficiently."""
        try:
            # Download once and cache
            logger.info("Loading market indicators...")
            sp500 = yf.download('^GSPC', start='2004-01-01', end='2024-12-31', progress=False)
            nasdaq = yf.download('^IXIC', start='2004-01-01', end='2024-12-31', progress=False)
            vix = yf.download('^VIX', start='2004-01-01', end='2024-12-31', progress=False)
            
            # Pre-calculate yearly metrics for efficiency
            market_data = {}
            for year in range(2004, 2025):
                year_str = str(year)
                try:
                    sp500_year = sp500[sp500.index.year == year]
                    nasdaq_year = nasdaq[nasdaq.index.year == year]
                    vix_year = vix[vix.index.year == year]
                    
                    if len(sp500_year) > 0:
                        market_data[year] = {
                            'sp500_return': (sp500_year['Close'].iloc[-1] - sp500_year['Close'].iloc[0]) / sp500_year['Close'].iloc[0],
                            'nasdaq_return': (nasdaq_year['Close'].iloc[-1] - nasdaq_year['Close'].iloc[0]) / nasdaq_year['Close'].iloc[0] if len(nasdaq_year) > 0 else 0,
                            'avg_vix': vix_year['Close'].mean() if len(vix_year) > 0 else 20,
                            'market_sentiment': 0  # Will calculate
                        }
                        
                        # Market sentiment score
                        sentiment = 0.5 + market_data[year]['sp500_return']
                        market_data[year]['market_sentiment'] = max(0, min(1, sentiment))
                except:
                    market_data[year] = {
                        'sp500_return': 0,
                        'nasdaq_return': 0,
                        'avg_vix': 20,
                        'market_sentiment': 0.5
                    }
            
            logger.info("Market data loaded successfully")
            return market_data
        except Exception as e:
            logger.warning(f"Could not load market data: {e}. Using defaults.")
            return {year: {'sp500_return': 0, 'nasdaq_return': 0, 'avg_vix': 20, 'market_sentiment': 0.5} 
                   for year in range(2004, 2025)}
    
    def generate_company_batch(self, company_ids: List[int]) -> List[Dict]:
        """Generate a batch of companies with longitudinal data."""
        all_records = []
        
        for company_id in company_ids:
            # Generate base company
            company = self._generate_base_company(company_id)
            
            # Generate longitudinal records
            records = self._generate_longitudinal_records(company)
            all_records.extend(records)
        
        return all_records
    
    def _generate_base_company(self, company_id: int) -> Dict:
        """Generate base company profile."""
        # Founding year (weighted toward recent)
        years = np.arange(2005, 2024)
        weights = 0.7 ** (2023 - years)
        probs = weights / weights.sum()
        founded_year = np.random.choice(years, p=probs)
        
        # Industry
        industry = np.random.choice(list(self.industries.keys()))
        
        # Location
        locations = list(self.ecosystems.keys())
        location_weights = [self.ecosystems[loc]['weight'] for loc in locations]
        location = np.random.choice(locations, p=location_weights)
        
        # Founder quality (determines trajectory)
        founder_quality = np.random.choice(['low', 'medium', 'high'], p=[0.5, 0.35, 0.15])
        
        # Determine outcome based on multiple factors
        base_fail_rate = self.industries[industry]['fail_rate']
        location_boost = self.ecosystems[location]['quality_boost']
        
        # Adjust fail rate based on quality
        if founder_quality == 'high':
            fail_rate = base_fail_rate * 0.5
        elif founder_quality == 'medium':
            fail_rate = base_fail_rate * 0.8
        else:
            fail_rate = base_fail_rate * 1.2
        
        fail_rate = fail_rate / location_boost
        
        # Determine outcome
        outcome_roll = np.random.random()
        if outcome_roll < fail_rate:
            outcome = 'shutdown'
            outcome_year = founded_year + np.random.randint(2, 6)
        elif outcome_roll < fail_rate + 0.1:
            outcome = 'acquisition'
            outcome_year = founded_year + np.random.randint(3, 8)
        elif outcome_roll < fail_rate + 0.12:
            outcome = 'ipo'
            outcome_year = founded_year + np.random.randint(7, 12)
        else:
            outcome = 'active'
            outcome_year = 2024
        
        return {
            'company_id': f'company_{company_id:06d}',
            'company_name': f'{industry.replace("/", "")}_Co_{company_id}',
            'founded_year': founded_year,
            'industry': industry,
            'location': location,
            'founder_quality': founder_quality,
            'outcome': outcome,
            'outcome_year': min(outcome_year, 2024),
            'founders_count': np.random.choice([1, 2, 3, 4], p=[0.15, 0.55, 0.25, 0.05]),
            'founder_experience': np.random.uniform(5, 25) if founder_quality == 'high' else np.random.uniform(2, 15),
            'prior_exits': np.random.poisson(0.5) if founder_quality == 'high' else 0
        }
    
    def _generate_longitudinal_records(self, company: Dict) -> List[Dict]:
        """Generate yearly records for a company."""
        records = []
        
        founded_year = company['founded_year']
        outcome_year = company['outcome_year']
        
        # Track progression through stages
        current_stage = 'Pre-Seed'
        total_raised = 0
        last_revenue = 0
        
        for year in range(founded_year, min(outcome_year + 1, 2025)):
            years_active = year - founded_year
            
            # Progress through funding stages
            if years_active > 0 and current_stage in self.stage_progression:
                stage_info = self.stage_progression[current_stage]
                if stage_info['years'] is not None and years_active >= stage_info['years'] and stage_info['next']:
                    # Progress to next stage with some probability
                    if np.random.random() < 0.7:  # 70% chance to progress
                        current_stage = stage_info['next']
            
            # Generate record for this year
            record = self._generate_yearly_snapshot(
                company, year, current_stage, years_active, 
                total_raised, last_revenue
            )
            
            # Update cumulative metrics
            total_raised = record['total_capital_raised_usd']
            last_revenue = record['annual_revenue_run_rate']
            
            records.append(record)
        
        return records
    
    def _generate_yearly_snapshot(self, company: Dict, year: int, stage: str, 
                                 years_active: int, prior_raised: float, 
                                 prior_revenue: float) -> Dict:
        """Generate a single yearly snapshot."""
        industry_data = self.industries[company['industry']]
        market_data = self.market_data.get(year, self.market_data[2020])
        
        # Calculate stage-specific funding
        new_funding = self._calculate_funding(stage, company['founder_quality'])
        total_raised = prior_raised + new_funding
        
        # Calculate revenue based on trajectory
        if years_active == 0:
            revenue = 0
        else:
            if company['outcome'] == 'ipo':
                # Exponential growth for IPO companies
                revenue = 10000 * (1 + industry_data['growth'] * 2) ** years_active
            elif company['outcome'] == 'acquisition':
                # Good growth for acquired companies
                revenue = 10000 * (1 + industry_data['growth'] * 1.5) ** years_active
            elif company['outcome'] == 'shutdown':
                # Growth then decline
                if years_active < 3:
                    revenue = prior_revenue * (1 + industry_data['growth'])
                else:
                    revenue = prior_revenue * 0.8  # Declining
            else:  # active/zombie
                revenue = 10000 * (1 + industry_data['growth'] * 0.8) ** years_active
        
        # Add realistic variance
        revenue = revenue * np.random.uniform(0.8, 1.2)
        
        # Calculate other metrics
        burn_rate = self._calculate_burn_rate(stage, revenue)
        team_size = self._calculate_team_size(years_active, company['outcome'], stage)
        
        # Determine success at outcome year
        if year >= company['outcome_year']:
            if company['outcome'] in ['ipo', 'acquisition']:
                success = True
            elif company['outcome'] == 'shutdown':
                success = False
            else:
                success = None  # Still active
        else:
            success = None  # No outcome yet
        
        # Create full record
        record = {
            # Identifiers
            'company_id': company['company_id'],
            'company_name': company['company_name'],
            'year': year,
            'founding_year': company['founded_year'],
            'years_since_founding': years_active,
            
            # Company basics
            'industry': company['industry'],
            'sector': company['industry'],
            'location': company['location'],
            'funding_stage': stage,
            
            # Financial metrics
            'total_capital_raised_usd': total_raised,
            'cash_on_hand_usd': total_raised * np.random.uniform(0.2, 0.6),
            'monthly_burn_usd': burn_rate,
            'annual_revenue_run_rate': revenue,
            'revenue_growth_rate_percent': ((revenue - prior_revenue) / prior_revenue * 100) if prior_revenue > 0 else 0,
            'gross_margin_percent': np.random.normal(industry_data['margin'], 10),
            
            # Calculate later
            'runway_months': 0,
            'burn_multiple': 0,
            'ltv_cac_ratio': np.random.uniform(0.5, 3.5) if revenue > 0 else 0,
            
            # Investor info
            'investor_tier_primary': self._get_investor_tier(stage, company['founder_quality']),
            'has_debt': np.random.random() < 0.2,
            
            # Product/advantage metrics
            'patent_count': np.random.poisson(years_active * 0.3) if company['industry'] in ['BioTech', 'HealthTech'] else 0,
            'tech_differentiation_score': np.random.uniform(1, 5),
            'switching_cost_score': np.random.uniform(1, 5),
            'network_effects_present': company['industry'] == 'Marketplace' or np.random.random() < 0.2,
            'has_data_moat': years_active > 2 and np.random.random() < 0.3,
            'brand_strength_score': min(1 + years_active * 0.5, 5),
            'scalability_score': np.random.uniform(0.7, 1.0) if company['industry'] in ['SaaS', 'AI/ML'] else np.random.uniform(0.3, 0.7),
            'regulatory_advantage_present': company['industry'] in ['FinTech', 'HealthTech'] and np.random.random() < 0.2,
            'product_stage': self._get_product_stage(years_active),
            'product_retention_30d': self._get_retention(company['outcome'], years_active),
            'product_retention_90d': 0,  # Calculate later
            
            # Market metrics
            'tam_size_usd': industry_data['tam'] * (1.1 ** (year - 2020)),
            'sam_size_usd': 0,  # Calculate later
            'som_size_usd': 0,  # Calculate later
            'market_growth_rate_percent': industry_data['growth'] * 100,
            'customer_count': int(revenue / np.random.uniform(1000, 50000)) if revenue > 0 else 0,
            'customer_concentration_percent': np.random.uniform(10, 60),
            'user_growth_rate_percent': ((revenue - prior_revenue) / prior_revenue * 100 * np.random.uniform(0.8, 1.2)) if prior_revenue > 0 else 0,
            'net_dollar_retention_percent': np.random.uniform(80, 130) if revenue > 0 else 0,
            'competition_intensity': np.random.uniform(2, 5),
            'competitors_named_count': int(np.random.uniform(5, 50)),
            'dau_mau_ratio': np.random.uniform(0.1, 0.7),
            
            # Team metrics
            'founders_count': company['founders_count'],
            'team_size_full_time': team_size,
            'years_experience_avg': company['founder_experience'],
            'domain_expertise_years_avg': company['founder_experience'] * 0.7,
            'prior_startup_experience_count': np.random.poisson(1) if company['founder_quality'] == 'high' else 0,
            'prior_successful_exits_count': company['prior_exits'],
            'board_advisor_experience_score': min(1 + years_active * 0.3, 5),
            'advisors_count': min(np.random.poisson(years_active), 10),
            'team_diversity_percent': np.random.uniform(20, 70),
            'key_person_dependency': company['founders_count'] == 1 or np.random.random() < 0.4,
            
            # Outcome
            'outcome': company['outcome'] if year >= company['outcome_year'] else 'active',
            'success': success,
            
            # Market context
            'market_sentiment': market_data['market_sentiment'],
            'sp500_return': market_data['sp500_return'],
            'tech_index_return': market_data['nasdaq_return'],
            'market_volatility_vix': market_data['avg_vix']
        }
        
        # Calculate derived fields
        record['runway_months'] = record['cash_on_hand_usd'] / record['monthly_burn_usd'] if record['monthly_burn_usd'] > 0 else 24
        record['burn_multiple'] = record['monthly_burn_usd'] / (record['annual_revenue_run_rate'] / 12) if record['annual_revenue_run_rate'] > 0 else 999
        record['sam_size_usd'] = record['tam_size_usd'] * np.random.uniform(0.05, 0.2)
        record['som_size_usd'] = record['sam_size_usd'] * np.random.uniform(0.01, 0.1)
        record['product_retention_90d'] = record['product_retention_30d'] * np.random.uniform(0.7, 0.95)
        
        # Cap extreme values
        record['runway_months'] = min(record['runway_months'], 48)
        record['burn_multiple'] = min(record['burn_multiple'], 999)
        
        return record
    
    def _calculate_funding(self, stage: str, founder_quality: str) -> float:
        """Calculate funding amount for a round."""
        base_amounts = {
            'Pre-Seed': (50e3, 500e3),
            'Seed': (500e3, 3e6),
            'Series A': (3e6, 15e6),
            'Series B': (15e6, 50e6),
            'Series C+': (50e6, 200e6)
        }
        
        min_amt, max_amt = base_amounts.get(stage, (1e6, 10e6))
        
        # High quality founders raise more
        if founder_quality == 'high':
            min_amt *= 1.5
            max_amt *= 2.0
        elif founder_quality == 'low':
            max_amt *= 0.7
        
        return np.random.uniform(min_amt, max_amt)
    
    def _calculate_burn_rate(self, stage: str, revenue: float) -> float:
        """Calculate monthly burn rate."""
        base_burns = {
            'Pre-Seed': 20e3,
            'Seed': 100e3,
            'Series A': 500e3,
            'Series B': 1.5e6,
            'Series C+': 3e6
        }
        
        burn = base_burns.get(stage, 200e3)
        
        # Profitable companies burn less
        if revenue > burn * 12:
            burn *= 0.5
        
        return burn * np.random.uniform(0.8, 1.2)
    
    def _calculate_team_size(self, years: int, outcome: str, stage: str) -> int:
        """Calculate team size based on age and trajectory."""
        if outcome == 'ipo':
            base = 3 * (2.0 ** years)
        elif outcome == 'acquisition':
            base = 2 * (1.8 ** years)
        elif outcome == 'shutdown':
            base = 2 * (1.3 ** years)
        else:
            base = 2 * (1.5 ** years)
        
        # Cap by stage
        stage_caps = {
            'Pre-Seed': 10,
            'Seed': 25,
            'Series A': 100,
            'Series B': 500,
            'Series C+': 2000
        }
        
        cap = stage_caps.get(stage, 1000)
        return int(min(base * np.random.uniform(0.8, 1.2), cap))
    
    def _get_investor_tier(self, stage: str, founder_quality: str) -> str:
        """Determine investor tier."""
        if founder_quality == 'high':
            # High quality founders attract top VCs
            if stage in ['Series A', 'Series B', 'Series C+']:
                return np.random.choice(['Tier1', 'Tier2'], p=[0.7, 0.3])
            else:
                return np.random.choice(['Tier2', 'Tier3'], p=[0.6, 0.4])
        
        # Standard distribution
        if stage == 'Pre-Seed':
            return np.random.choice(['Angel', 'Tier3'], p=[0.7, 0.3])
        elif stage == 'Seed':
            return np.random.choice(['Angel', 'Tier3', 'Tier2'], p=[0.3, 0.5, 0.2])
        elif stage == 'Series A':
            return np.random.choice(['Tier3', 'Tier2', 'Tier1'], p=[0.3, 0.5, 0.2])
        else:
            return np.random.choice(['Tier2', 'Tier1'], p=[0.4, 0.6])
    
    def _get_product_stage(self, years: int) -> str:
        """Determine product stage based on company age."""
        if years == 0:
            return 'MVP'
        elif years == 1:
            return np.random.choice(['MVP', 'Beta'], p=[0.3, 0.7])
        elif years == 2:
            return np.random.choice(['Beta', 'Early Traction'], p=[0.3, 0.7])
        elif years <= 4:
            return np.random.choice(['Early Traction', 'GA', 'Growth'], p=[0.2, 0.4, 0.4])
        else:
            return np.random.choice(['GA', 'Growth'], p=[0.3, 0.7])
    
    def _get_retention(self, outcome: str, years: int) -> float:
        """Get retention rate based on outcome and maturity."""
        if years == 0:
            return np.random.uniform(0.2, 0.5)
        
        if outcome == 'ipo':
            return np.random.uniform(0.7, 0.95)
        elif outcome == 'acquisition':
            return np.random.uniform(0.6, 0.85)
        elif outcome == 'shutdown':
            return np.random.uniform(0.2, 0.6)
        else:
            return np.random.uniform(0.4, 0.75)
    
    def generate_dataset(self, target_records: int = 100000) -> pd.DataFrame:
        """Generate the complete dataset efficiently."""
        logger.info(f"Generating {target_records} records with longitudinal tracking...")
        
        # Estimate companies needed (avg ~5 records per company)
        n_companies = target_records // 5
        
        # Process companies
        logger.info(f"Creating {n_companies} companies with longitudinal data...")
        
        results = []
        for i in range(0, n_companies, 1000):
            batch_end = min(i + 1000, n_companies)
            batch_ids = list(range(i, batch_end))
            
            batch_results = self.generate_company_batch(batch_ids)
            results.extend(batch_results)
            
            logger.info(f"Processed {batch_end}/{n_companies} companies...")
        
        # Convert to DataFrame
        df = pd.DataFrame(results)
        
        # Trim to exact size if needed
        if len(df) > target_records:
            df = df.sample(n=target_records, random_state=42)
        
        # Apply data quality patterns
        df = self._apply_realistic_data_quality(df)
        
        # Sort by company and year
        df = df.sort_values(['company_id', 'year'])
        
        # Add record IDs
        df['record_id'] = [f'rec_{i:08d}' for i in range(len(df))]
        
        logger.info(f"Generated {len(df)} records for {df['company_id'].nunique()} companies")
        
        return df
    
    def _apply_realistic_data_quality(self, df: pd.DataFrame) -> pd.DataFrame:
        """Apply realistic missing data patterns."""
        # Features that are commonly missing
        missing_patterns = [
            ('patent_count', 0.30),
            ('dau_mau_ratio', 0.35),
            ('net_dollar_retention_percent', 0.25),
            ('customer_concentration_percent', 0.20),
            ('team_diversity_percent', 0.15),
            ('prior_successful_exits_count', 0.10)
        ]
        
        for col, missing_rate in missing_patterns:
            if col in df.columns:
                mask = np.random.random(len(df)) < missing_rate
                df.loc[mask, col] = np.nan
        
        # Recent data is less complete
        recent_mask = df['year'] >= 2023
        for col in ['annual_revenue_run_rate', 'customer_count']:
            if col in df.columns:
                mask = recent_mask & (np.random.random(len(df)) < 0.3)
                df.loc[mask, col] = np.nan
        
        return df

def main():
    """Generate the complete high-quality dataset."""
    generator = CompleteDatasetGenerator()
    
    # Generate dataset
    df = generator.generate_dataset(target_records=100000)
    
    # Save to CSV
    output_file = 'complete_high_quality_startup_dataset_100k.csv'
    df.to_csv(output_file, index=False)
    logger.info(f"Saved dataset to {output_file}")
    
    # Generate comprehensive summary
    summary = {
        'dataset_info': {
            'total_records': len(df),
            'unique_companies': df['company_id'].nunique(),
            'features': len(df.columns),
            'date_range': f"{df['founding_year'].min()} - {df['year'].max()}",
            'years_tracked': f"{df['years_since_founding'].min()} - {df['years_since_founding'].max()}"
        },
        'longitudinal_tracking': {
            'avg_years_per_company': df.groupby('company_id')['year'].count().mean(),
            'max_years_tracked': df.groupby('company_id')['year'].count().max(),
            'companies_with_full_history': (df.groupby('company_id')['year'].count() > 3).sum()
        },
        'outcome_distribution': {
            'ipo': df[df['outcome'] == 'ipo']['company_id'].nunique(),
            'acquisition': df[df['outcome'] == 'acquisition']['company_id'].nunique(),
            'shutdown': df[df['outcome'] == 'shutdown']['company_id'].nunique(),
            'active': df[df['outcome'] == 'active']['company_id'].nunique()
        },
        'success_rates': {
            'overall': df[df['success'].notna()]['success'].mean(),
            'by_stage': {},
            'by_location': {},
            'by_industry': {}
        },
        'market_context': {
            'years_with_data': df['year'].nunique(),
            'market_sentiment_range': f"{df['market_sentiment'].min():.2f} - {df['market_sentiment'].max():.2f}",
            'includes_2008_crisis': (df['year'] == 2008).any(),
            'includes_covid': (df['year'] == 2020).any()
        },
        'data_quality': {
            'missing_data_pct': (df.isnull().sum() / len(df) * 100).mean(),
            'features_with_missing': (df.isnull().sum() > 0).sum()
        }
    }
    
    # Calculate success rates by various dimensions
    for stage in ['Pre-Seed', 'Seed', 'Series A', 'Series B', 'Series C+']:
        stage_data = df[df['funding_stage'] == stage]
        if len(stage_data) > 0 and stage_data['success'].notna().any():
            summary['success_rates']['by_stage'][stage] = float(stage_data['success'].mean())
    
    # By location
    for location in df['location'].unique()[:5]:  # Top 5
        loc_data = df[df['location'] == location]
        if len(loc_data) > 0 and loc_data['success'].notna().any():
            summary['success_rates']['by_location'][location] = float(loc_data['success'].mean())
    
    # By industry
    for industry in df['industry'].unique():
        ind_data = df[df['industry'] == industry]
        if len(ind_data) > 0 and ind_data['success'].notna().any():
            summary['success_rates']['by_industry'][industry] = float(ind_data['success'].mean())
    
    # Save summary
    with open('complete_dataset_summary.json', 'w') as f:
        json.dump(summary, f, indent=2, default=str)
    
    logger.info("Complete dataset generation finished!")
    print(f"\nDataset Overview:")
    print(f"- Total records: {summary['dataset_info']['total_records']:,}")
    print(f"- Unique companies: {summary['dataset_info']['unique_companies']:,}")
    print(f"- Average years tracked: {summary['longitudinal_tracking']['avg_years_per_company']:.1f}")
    print(f"- Overall success rate: {summary['success_rates']['overall']:.1%}")
    print(f"- Missing data: {summary['data_quality']['missing_data_pct']:.1f}%")

if __name__ == "__main__":
    main()