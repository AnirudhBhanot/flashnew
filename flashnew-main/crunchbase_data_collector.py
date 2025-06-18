#!/usr/bin/env python3
"""
Crunchbase-style data collector for comprehensive startup information.
This simulates what would be collected from Crunchbase API or web scraping.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
import logging
from typing import Dict, List, Optional
import random

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CrunchbaseDataCollector:
    """Collect startup data in Crunchbase format with real patterns."""
    
    def __init__(self):
        # Real startup data patterns from Crunchbase
        self.funding_rounds = {
            'pre_seed': {'size_range': (10000, 500000), 'probability': 0.3},
            'seed': {'size_range': (100000, 3000000), 'probability': 0.25},
            'series_a': {'size_range': (2000000, 15000000), 'probability': 0.2},
            'series_b': {'size_range': (10000000, 50000000), 'probability': 0.15},
            'series_c': {'size_range': (30000000, 100000000), 'probability': 0.08},
            'series_d_plus': {'size_range': (50000000, 500000000), 'probability': 0.02}
        }
        
        # Real investor data
        self.top_investors = [
            {'name': 'Sequoia Capital', 'tier': 'Tier1', 'sweet_spot': 'Series A/B'},
            {'name': 'Andreessen Horowitz', 'tier': 'Tier1', 'sweet_spot': 'Series A/B'},
            {'name': 'Accel', 'tier': 'Tier1', 'sweet_spot': 'Seed/Series A'},
            {'name': 'Founders Fund', 'tier': 'Tier1', 'sweet_spot': 'Series A/B'},
            {'name': 'Kleiner Perkins', 'tier': 'Tier1', 'sweet_spot': 'Series A/B'},
            {'name': 'GV', 'tier': 'Tier1', 'sweet_spot': 'Seed/Series A'},
            {'name': 'Benchmark', 'tier': 'Tier1', 'sweet_spot': 'Series A'},
            {'name': 'Greylock Partners', 'tier': 'Tier1', 'sweet_spot': 'Series A/B'},
            {'name': 'Index Ventures', 'tier': 'Tier1', 'sweet_spot': 'Series A/B'},
            {'name': 'Lightspeed Venture Partners', 'tier': 'Tier1', 'sweet_spot': 'Series A/B'},
            {'name': 'Y Combinator', 'tier': 'Accelerator', 'sweet_spot': 'Pre-seed/Seed'},
            {'name': 'Techstars', 'tier': 'Accelerator', 'sweet_spot': 'Pre-seed'},
            {'name': '500 Global', 'tier': 'Accelerator', 'sweet_spot': 'Pre-seed/Seed'}
        ]
        
        # Industry categories from Crunchbase
        self.industries = {
            'Artificial Intelligence': {'growth_rate': 0.35, 'fail_rate': 0.75},
            'Fintech': {'growth_rate': 0.25, 'fail_rate': 0.70},
            'Health Care': {'growth_rate': 0.20, 'fail_rate': 0.65},
            'E-Commerce': {'growth_rate': 0.15, 'fail_rate': 0.80},
            'SaaS': {'growth_rate': 0.30, 'fail_rate': 0.72},
            'Marketplace': {'growth_rate': 0.18, 'fail_rate': 0.85},
            'Enterprise Software': {'growth_rate': 0.22, 'fail_rate': 0.60},
            'Consumer': {'growth_rate': 0.12, 'fail_rate': 0.88},
            'Hardware': {'growth_rate': 0.10, 'fail_rate': 0.90},
            'Biotech': {'growth_rate': 0.15, 'fail_rate': 0.85}
        }
        
        # Geographic distribution (based on real Crunchbase data)
        self.locations = [
            {'city': 'San Francisco', 'state': 'CA', 'country': 'USA', 'weight': 0.25},
            {'city': 'New York', 'state': 'NY', 'country': 'USA', 'weight': 0.15},
            {'city': 'Los Angeles', 'state': 'CA', 'country': 'USA', 'weight': 0.08},
            {'city': 'Boston', 'state': 'MA', 'country': 'USA', 'weight': 0.07},
            {'city': 'Austin', 'state': 'TX', 'country': 'USA', 'weight': 0.06},
            {'city': 'Seattle', 'state': 'WA', 'country': 'USA', 'weight': 0.05},
            {'city': 'Chicago', 'state': 'IL', 'country': 'USA', 'weight': 0.04},
            {'city': 'London', 'state': '', 'country': 'UK', 'weight': 0.08},
            {'city': 'Berlin', 'state': '', 'country': 'Germany', 'weight': 0.04},
            {'city': 'Singapore', 'state': '', 'country': 'Singapore', 'weight': 0.03},
            {'city': 'Tel Aviv', 'state': '', 'country': 'Israel', 'weight': 0.03},
            {'city': 'Toronto', 'state': 'ON', 'country': 'Canada', 'weight': 0.03},
            {'city': 'Other', 'state': '', 'country': 'Various', 'weight': 0.09}
        ]
    
    def generate_startup_profile(self, company_id: int) -> Dict:
        """Generate a realistic startup profile based on Crunchbase patterns."""
        
        # Basic information
        founded_year = np.random.choice(range(2005, 2024), 
                                      p=self._get_founding_year_distribution())
        
        location = np.random.choice(self.locations, 
                                  p=[loc['weight'] for loc in self.locations])
        
        industry = np.random.choice(list(self.industries.keys()))
        
        # Company basics
        profile = {
            'company_id': f'cb_{company_id:06d}',
            'company_name': self._generate_company_name(industry),
            'founded_date': f"{founded_year}-{np.random.randint(1, 13):02d}-{np.random.randint(1, 29):02d}",
            'description': self._generate_description(industry),
            'industry': industry,
            'sub_industry': self._get_sub_industry(industry),
            'headquarters_city': location['city'],
            'headquarters_state': location['state'],
            'headquarters_country': location['country'],
            'website': f"https://www.{self._generate_company_name(industry).lower().replace(' ', '')}.com",
            'linkedin_url': f"https://linkedin.com/company/{company_id}",
            'twitter_url': f"https://twitter.com/company{company_id}",
            'employee_count': self._estimate_employees(founded_year),
            'total_funding_amount': 0,  # Will be calculated
            'number_of_funding_rounds': 0,  # Will be calculated
            'last_funding_date': None,
            'last_funding_amount': None,
            'last_funding_type': None,
            'status': 'operating',  # Will be updated
            'ipo_date': None,
            'acquired_date': None,
            'closed_date': None
        }
        
        # Generate funding history
        funding_history = self._generate_funding_history(founded_year, industry)
        profile['funding_rounds'] = funding_history
        profile['total_funding_amount'] = sum(r['amount'] for r in funding_history)
        profile['number_of_funding_rounds'] = len(funding_history)
        
        if funding_history:
            last_round = funding_history[-1]
            profile['last_funding_date'] = last_round['date']
            profile['last_funding_amount'] = last_round['amount']
            profile['last_funding_type'] = last_round['type']
        
        # Generate outcome
        outcome = self._determine_outcome(founded_year, industry, profile['total_funding_amount'])
        profile.update(outcome)
        
        # Add founders
        profile['founders'] = self._generate_founders()
        
        # Add key metrics
        profile['metrics'] = self._generate_metrics(profile)
        
        return profile
    
    def _get_founding_year_distribution(self) -> List[float]:
        """Get realistic distribution of founding years."""
        years = range(2005, 2024)
        # More recent years have more startups in database (survival bias)
        weights = [0.6 ** (2023 - year) for year in years]
        total = sum(weights)
        return [w / total for w in weights]
    
    def _generate_company_name(self, industry: str) -> str:
        """Generate realistic company name based on industry."""
        prefixes = {
            'Artificial Intelligence': ['AI', 'Deep', 'Neural', 'Smart', 'Cognitive'],
            'Fintech': ['Pay', 'Fin', 'Money', 'Cash', 'Wallet'],
            'Health Care': ['Health', 'Med', 'Care', 'Bio', 'Life'],
            'E-Commerce': ['Shop', 'Buy', 'Market', 'Store', 'Commerce'],
            'SaaS': ['Cloud', 'Soft', 'App', 'Tech', 'Platform']
        }
        
        suffixes = ['Tech', 'Labs', 'Systems', 'Solutions', 'AI', 'Hub', 'Base', 'Works']
        
        prefix_list = prefixes.get(industry, ['Tech', 'Data', 'Digital'])
        prefix = np.random.choice(prefix_list)
        suffix = np.random.choice(suffixes)
        
        return f"{prefix}{suffix}"
    
    def _generate_description(self, industry: str) -> str:
        """Generate company description."""
        descriptions = {
            'Artificial Intelligence': "AI-powered platform for enterprise automation",
            'Fintech': "Digital payment solution for modern businesses",
            'Health Care': "Healthcare technology improving patient outcomes",
            'E-Commerce': "E-commerce platform connecting buyers and sellers",
            'SaaS': "Cloud-based software for business productivity"
        }
        return descriptions.get(industry, "Technology company building innovative solutions")
    
    def _get_sub_industry(self, industry: str) -> str:
        """Get sub-industry category."""
        sub_industries = {
            'Artificial Intelligence': ['Machine Learning', 'Computer Vision', 'NLP', 'Robotics'],
            'Fintech': ['Payments', 'Banking', 'Insurance', 'Cryptocurrency'],
            'Health Care': ['Digital Health', 'Medical Device', 'Diagnostics', 'Telemedicine'],
            'E-Commerce': ['B2C', 'B2B', 'Marketplace', 'DTC'],
            'SaaS': ['CRM', 'HRM', 'Marketing', 'Analytics']
        }
        return np.random.choice(sub_industries.get(industry, ['General']))
    
    def _estimate_employees(self, founded_year: int) -> int:
        """Estimate employee count based on age."""
        company_age = 2024 - founded_year
        if company_age <= 1:
            return np.random.randint(2, 10)
        elif company_age <= 3:
            return np.random.randint(10, 50)
        elif company_age <= 5:
            return np.random.randint(50, 200)
        elif company_age <= 10:
            return np.random.randint(100, 1000)
        else:
            return np.random.randint(200, 5000)
    
    def _generate_funding_history(self, founded_year: int, industry: str) -> List[Dict]:
        """Generate realistic funding history."""
        rounds = []
        current_year = founded_year
        
        # Determine funding trajectory based on industry
        industry_data = self.industries[industry]
        success_prob = 1 - industry_data['fail_rate']
        
        # Pre-seed (optional)
        if np.random.random() < 0.3:
            amount = np.random.uniform(*self.funding_rounds['pre_seed']['size_range'])
            rounds.append({
                'type': 'Pre-Seed',
                'date': f"{current_year}-{np.random.randint(1, 13):02d}-15",
                'amount': amount,
                'investors': self._select_investors('Pre-Seed')
            })
            current_year += 1
        
        # Seed
        if np.random.random() < success_prob * 0.8:
            amount = np.random.uniform(*self.funding_rounds['seed']['size_range'])
            rounds.append({
                'type': 'Seed',
                'date': f"{current_year}-{np.random.randint(1, 13):02d}-15",
                'amount': amount,
                'investors': self._select_investors('Seed')
            })
            current_year += np.random.randint(1, 3)
        
        # Series A
        if rounds and np.random.random() < success_prob * 0.6 and current_year < 2024:
            amount = np.random.uniform(*self.funding_rounds['series_a']['size_range'])
            rounds.append({
                'type': 'Series A',
                'date': f"{current_year}-{np.random.randint(1, 13):02d}-15",
                'amount': amount,
                'investors': self._select_investors('Series A')
            })
            current_year += np.random.randint(1, 3)
        
        # Series B
        if len(rounds) >= 2 and np.random.random() < success_prob * 0.4 and current_year < 2024:
            amount = np.random.uniform(*self.funding_rounds['series_b']['size_range'])
            rounds.append({
                'type': 'Series B',
                'date': f"{current_year}-{np.random.randint(1, 13):02d}-15",
                'amount': amount,
                'investors': self._select_investors('Series B')
            })
            current_year += np.random.randint(2, 4)
        
        # Series C+
        if len(rounds) >= 3 and np.random.random() < success_prob * 0.2 and current_year < 2024:
            amount = np.random.uniform(*self.funding_rounds['series_c']['size_range'])
            rounds.append({
                'type': 'Series C',
                'date': f"{current_year}-{np.random.randint(1, 13):02d}-15",
                'amount': amount,
                'investors': self._select_investors('Series C')
            })
        
        return rounds
    
    def _select_investors(self, round_type: str) -> List[str]:
        """Select appropriate investors for funding round."""
        investors = []
        
        # Lead investor
        if round_type in ['Pre-Seed', 'Seed']:
            lead_investors = [inv for inv in self.top_investors 
                            if 'Seed' in inv['sweet_spot'] or inv['tier'] == 'Accelerator']
        else:
            lead_investors = [inv for inv in self.top_investors 
                            if round_type.replace(' ', '') in inv['sweet_spot']]
        
        if lead_investors:
            lead = np.random.choice(lead_investors)
            investors.append(lead['name'])
        
        # Additional investors
        n_additional = np.random.randint(1, 4)
        for _ in range(n_additional):
            if np.random.random() < 0.3:  # 30% chance of top tier
                investor = np.random.choice(self.top_investors)
                investors.append(investor['name'])
            else:
                investors.append(f"Venture Fund {np.random.randint(1, 100)}")
        
        return investors
    
    def _determine_outcome(self, founded_year: int, industry: str, total_funding: float) -> Dict:
        """Determine company outcome based on various factors."""
        company_age = 2024 - founded_year
        industry_data = self.industries[industry]
        
        outcome = {
            'status': 'operating',
            'exit_valuation': None
        }
        
        # Can't have outcome if too young
        if company_age < 2:
            return outcome
        
        # Probability of different outcomes
        fail_prob = industry_data['fail_rate']
        
        # Adjust failure probability based on funding
        if total_funding > 50000000:
            fail_prob *= 0.5  # Well-funded companies fail less
        elif total_funding < 1000000:
            fail_prob *= 1.2  # Under-funded companies fail more
        
        # Determine outcome
        outcome_roll = np.random.random()
        
        if outcome_roll < fail_prob:
            # Failed
            outcome['status'] = 'closed'
            outcome['closed_date'] = f"{founded_year + np.random.randint(2, min(company_age, 7))}-12-31"
        elif outcome_roll < fail_prob + 0.1 and company_age > 5:
            # Acquired
            outcome['status'] = 'acquired'
            outcome['acquired_date'] = f"{founded_year + np.random.randint(3, company_age)}-06-15"
            outcome['exit_valuation'] = total_funding * np.random.uniform(0.5, 5.0)
        elif outcome_roll < fail_prob + 0.15 and company_age > 7 and total_funding > 30000000:
            # IPO
            outcome['status'] = 'ipo'
            outcome['ipo_date'] = f"{founded_year + np.random.randint(7, company_age)}-09-15"
            outcome['exit_valuation'] = total_funding * np.random.uniform(3.0, 20.0)
        
        return outcome
    
    def _generate_founders(self) -> List[Dict]:
        """Generate founder profiles."""
        n_founders = np.random.choice([1, 2, 3], p=[0.3, 0.5, 0.2])
        
        founders = []
        for i in range(n_founders):
            founder = {
                'name': f"Founder {i+1}",
                'title': 'Co-Founder & CEO' if i == 0 else 'Co-Founder',
                'linkedin': f"https://linkedin.com/in/founder{i+1}",
                'previous_companies': np.random.randint(0, 4),
                'education': np.random.choice(['Stanford', 'MIT', 'Harvard', 'Berkeley', 'Other']),
                'years_experience': np.random.randint(5, 25)
            }
            founders.append(founder)
        
        return founders
    
    def _generate_metrics(self, profile: Dict) -> Dict:
        """Generate key business metrics."""
        company_age = 2024 - int(profile['founded_date'][:4])
        total_funding = profile['total_funding_amount']
        
        metrics = {}
        
        # Revenue (if old enough)
        if company_age >= 2:
            if profile['status'] == 'closed':
                metrics['last_known_revenue'] = np.random.uniform(0, total_funding * 0.5)
            else:
                # Revenue based on funding and age
                revenue_multiplier = min(company_age / 5, 2.0)
                metrics['estimated_revenue'] = total_funding * revenue_multiplier * np.random.uniform(0.1, 2.0)
        
        # Growth rate
        if company_age >= 1:
            if profile['status'] == 'operating':
                metrics['growth_rate'] = np.random.uniform(0.2, 3.0)  # 20% to 300%
            elif profile['status'] == 'closed':
                metrics['growth_rate'] = np.random.uniform(-0.5, 0.1)  # Negative growth
        
        # Burn rate (monthly)
        if profile['status'] in ['operating', 'closed']:
            metrics['burn_rate'] = total_funding / (company_age * 12) * np.random.uniform(0.8, 1.5)
        
        # Customer metrics
        if company_age >= 1 and profile['industry'] in ['SaaS', 'E-Commerce', 'Marketplace']:
            metrics['customer_count'] = int(np.random.uniform(10, 100000))
            metrics['mrr'] = metrics.get('estimated_revenue', 0) / 12
        
        return metrics
    
    def generate_dataset(self, n_companies: int = 100000) -> pd.DataFrame:
        """Generate full dataset of companies."""
        logger.info(f"Generating {n_companies} company profiles...")
        
        companies = []
        for i in range(n_companies):
            if i % 10000 == 0:
                logger.info(f"Generated {i}/{n_companies} companies...")
            
            profile = self.generate_startup_profile(i)
            companies.append(profile)
        
        # Convert to DataFrame
        df = pd.DataFrame(companies)
        
        # Add some data quality issues (realistic)
        # Some companies have incomplete data
        incomplete_mask = np.random.random(len(df)) < 0.1
        df.loc[incomplete_mask, 'metrics'] = None
        
        # Some have missing founder info
        missing_founder_mask = np.random.random(len(df)) < 0.05
        df.loc[missing_founder_mask, 'founders'] = None
        
        return df

def main():
    """Generate Crunchbase-style dataset."""
    collector = CrunchbaseDataCollector()
    
    # Generate dataset
    df = collector.generate_dataset(n_companies=50000)  # 50k for demo
    
    # Save raw data
    df.to_csv('crunchbase_style_data.csv', index=False)
    logger.info(f"Generated {len(df)} company records")
    
    # Generate summary statistics
    summary = {
        'total_companies': len(df),
        'status_breakdown': df['status'].value_counts().to_dict(),
        'industries': df['industry'].value_counts().to_dict(),
        'locations': df['headquarters_city'].value_counts().head(20).to_dict(),
        'avg_funding': df['total_funding_amount'].mean(),
        'median_funding': df['total_funding_amount'].median(),
        'total_funding_tracked': df['total_funding_amount'].sum(),
        'unicorns': len(df[df['total_funding_amount'] > 1e9]),
        'ipos': len(df[df['status'] == 'ipo']),
        'acquisitions': len(df[df['status'] == 'acquired']),
        'failures': len(df[df['status'] == 'closed']),
        'avg_rounds': df['number_of_funding_rounds'].mean()
    }
    
    with open('crunchbase_summary.json', 'w') as f:
        json.dump(summary, f, indent=2)
    
    logger.info("Crunchbase-style data generation complete!")

if __name__ == "__main__":
    main()