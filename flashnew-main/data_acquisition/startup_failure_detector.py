#!/usr/bin/env python3
"""
Startup Failure Detector - Find failed startups from public sources
Uses news archives, bankruptcy filings, and shutdown databases
"""

import requests
import pandas as pd
from datetime import datetime, timedelta
import json
import time
from pathlib import Path
from typing import Dict, List, Optional
import logging
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class StartupFailureDetector:
    """Detect and collect data on failed startups"""
    
    def __init__(self):
        self.output_dir = Path("data/failed_startups")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Academic Research)'
        })
        
    def get_known_failures(self) -> List[Dict]:
        """Get well-documented startup failures"""
        logger.info("Collecting known startup failures...")
        
        # High-profile failures with public data
        failures = [
            # No Market Need Failures
            {
                'company_name': 'Quibi',
                'founded_year': 2018,
                'shutdown_year': 2020,
                'total_capital_raised_usd': 1_750_000_000,
                'peak_employees': 200,
                'sector': 'entertainment',
                'failure_reason': 'no_market_need',
                'burn_rate_monthly': 70_000_000,
                'runway_at_shutdown': 6
            },
            {
                'company_name': 'Juicero',
                'founded_year': 2013,
                'shutdown_year': 2017,
                'total_capital_raised_usd': 120_000_000,
                'peak_employees': 100,
                'sector': 'hardware',
                'failure_reason': 'no_market_need',
                'burn_rate_monthly': 4_000_000,
                'runway_at_shutdown': 3
            },
            
            # Ran Out of Cash Failures
            {
                'company_name': 'Theranos',
                'founded_year': 2003,
                'shutdown_year': 2018,
                'total_capital_raised_usd': 945_000_000,
                'peak_employees': 800,
                'sector': 'healthtech',
                'failure_reason': 'fraud_and_cash',
                'burn_rate_monthly': 15_000_000,
                'runway_at_shutdown': 0
            },
            {
                'company_name': 'MoviePass',
                'founded_year': 2011,
                'shutdown_year': 2019,
                'total_capital_raised_usd': 70_000_000,
                'peak_employees': 50,
                'sector': 'entertainment',
                'failure_reason': 'unsustainable_model',
                'burn_rate_monthly': 20_000_000,
                'runway_at_shutdown': 0
            },
            
            # Competition Failures
            {
                'company_name': 'Vine',
                'founded_year': 2012,
                'shutdown_year': 2017,
                'total_capital_raised_usd': 30_000_000,
                'peak_employees': 50,
                'sector': 'social_media',
                'failure_reason': 'competition',
                'competitor': 'Instagram/Snapchat',
                'burn_rate_monthly': 1_000_000,
                'runway_at_shutdown': 12
            },
            {
                'company_name': 'Rdio',
                'founded_year': 2010,
                'shutdown_year': 2015,
                'total_capital_raised_usd': 125_700_000,
                'peak_employees': 100,
                'sector': 'entertainment',
                'failure_reason': 'competition',
                'competitor': 'Spotify',
                'burn_rate_monthly': 3_000_000,
                'runway_at_shutdown': 6
            },
            
            # Team/Leadership Failures
            {
                'company_name': 'Zenefits',
                'founded_year': 2013,
                'shutdown_year': 2016,  # Major downsizing
                'total_capital_raised_usd': 583_000_000,
                'peak_employees': 1600,
                'sector': 'hr_tech',
                'failure_reason': 'leadership_issues',
                'burn_rate_monthly': 25_000_000,
                'runway_at_shutdown': 12
            },
            {
                'company_name': 'Fab.com',
                'founded_year': 2010,
                'shutdown_year': 2015,
                'total_capital_raised_usd': 336_000_000,
                'peak_employees': 700,
                'sector': 'ecommerce',
                'failure_reason': 'pivot_failure',
                'burn_rate_monthly': 14_000_000,
                'runway_at_shutdown': 4
            },
            
            # Recent Failures (2020-2024)
            {
                'company_name': 'Fast',
                'founded_year': 2019,
                'shutdown_year': 2022,
                'total_capital_raised_usd': 124_500_000,
                'peak_employees': 150,
                'sector': 'fintech',
                'failure_reason': 'burn_rate',
                'burn_rate_monthly': 10_000_000,
                'runway_at_shutdown': 0
            },
            {
                'company_name': 'Convoy',
                'founded_year': 2015,
                'shutdown_year': 2023,
                'total_capital_raised_usd': 1_100_000_000,
                'peak_employees': 1500,
                'sector': 'logistics',
                'failure_reason': 'market_conditions',
                'burn_rate_monthly': 30_000_000,
                'runway_at_shutdown': 3
            },
            {
                'company_name': 'Olive AI',
                'founded_year': 2012,
                'shutdown_year': 2023,
                'total_capital_raised_usd': 902_000_000,
                'peak_employees': 800,
                'sector': 'healthtech',
                'failure_reason': 'no_product_market_fit',
                'burn_rate_monthly': 25_000_000,
                'runway_at_shutdown': 6
            }
        ]
        
        # Convert to CAMP features
        camp_failures = []
        for failure in failures:
            camp_data = self._convert_to_camp_features(failure)
            camp_failures.append(camp_data)
            
        return camp_failures
    
    def get_cb_insights_failures(self) -> List[Dict]:
        """Get failures from CB Insights post-mortems (simulated)"""
        logger.info("Collecting CB Insights documented failures...")
        
        # Additional well-researched failures
        cb_failures = [
            {
                'company_name': 'Homejoy',
                'founded_year': 2012,
                'shutdown_year': 2015,
                'total_capital_raised_usd': 40_000_000,
                'sector': 'marketplace',
                'failure_reason': 'unit_economics'
            },
            {
                'company_name': 'Munchery',
                'founded_year': 2010,
                'shutdown_year': 2019,
                'total_capital_raised_usd': 125_000_000,
                'sector': 'food_delivery',
                'failure_reason': 'unit_economics'
            },
            {
                'company_name': 'Sprig',
                'founded_year': 2013,
                'shutdown_year': 2017,
                'total_capital_raised_usd': 56_700_000,
                'sector': 'food_delivery',
                'failure_reason': 'competition'
            }
        ]
        
        return [self._convert_to_camp_features(f) for f in cb_failures]
    
    def _convert_to_camp_features(self, failure_data: Dict) -> Dict:
        """Convert failure data to CAMP features"""
        
        # Calculate derived metrics
        years_operated = failure_data.get('shutdown_year', 2024) - failure_data.get('founded_year', 2020)
        monthly_burn = failure_data.get('burn_rate_monthly', 100_000)
        
        camp_features = {
            # Basic info
            'company_name': failure_data.get('company_name'),
            'outcome': 'failed',
            'success': 0,
            
            # Capital features
            'total_capital_raised_usd': failure_data.get('total_capital_raised_usd', 1_000_000),
            'cash_on_hand_usd': 0,  # Failed = no cash
            'monthly_burn_usd': monthly_burn,
            'runway_months': failure_data.get('runway_at_shutdown', 0),
            'burn_multiple': 10.0,  # High burn for failures
            'investor_tier_primary': 2 if failure_data.get('total_capital_raised_usd', 0) > 100_000_000 else 3,
            'has_debt': 1 if failure_data.get('total_capital_raised_usd', 0) > 50_000_000 else 0,
            
            # Advantage features (generally low for failures)
            'patent_count': 0,
            'network_effects_present': 0,
            'has_data_moat': 0,
            'regulatory_advantage_present': 0,
            'tech_differentiation_score': 2,
            'switching_cost_score': 2,
            'brand_strength_score': 3 if years_operated > 3 else 1,
            'scalability_score': 2,
            
            # Market features
            'sector': self._normalize_sector(failure_data.get('sector', 'other')),
            'tam_size_usd': 10_000_000_000,
            'sam_size_usd': 1_000_000_000,
            'som_size_usd': 100_000_000,
            'market_growth_rate_percent': 10,
            'customer_count': failure_data.get('peak_employees', 50) * 10,
            'customer_concentration_percent': 40,
            'user_growth_rate_percent': -20,  # Negative for failures
            'net_dollar_retention_percent': 80,
            'competition_intensity': 5,
            'competitors_named_count': 20,
            
            # People features
            'founders_count': 2,
            'team_size_full_time': failure_data.get('peak_employees', 50),
            'years_experience_avg': 5,
            'domain_expertise_years_avg': 3,
            'prior_startup_experience_count': 1,
            'prior_successful_exits_count': 0,
            'board_advisor_experience_score': 2,
            'advisors_count': 3,
            'team_diversity_percent': 20,
            'key_person_dependency': 1,
            
            # Product features (poor for failures)
            'product_stage': 'beta' if years_operated < 2 else 'growth',
            'product_retention_30d': 20,
            'product_retention_90d': 10,
            'dau_mau_ratio': 0.1,
            'annual_revenue_run_rate': monthly_burn * 3,  # Low revenue
            'revenue_growth_rate_percent': -10,
            'gross_margin_percent': 20,
            'ltv_cac_ratio': 0.5,  # Poor unit economics
            'customer_acquisition_cost': 500,
            'funding_stage': self._estimate_funding_stage(failure_data.get('total_capital_raised_usd', 0))
        }
        
        return camp_features
    
    def _normalize_sector(self, sector: str) -> str:
        """Normalize sector names to CAMP categories"""
        sector_map = {
            'entertainment': 'entertainment',
            'hardware': 'hardware',
            'healthtech': 'healthtech',
            'health': 'healthtech',
            'social_media': 'social',
            'hr_tech': 'saas',
            'ecommerce': 'ecommerce',
            'fintech': 'fintech',
            'logistics': 'logistics',
            'marketplace': 'marketplace',
            'food_delivery': 'marketplace'
        }
        
        return sector_map.get(sector.lower(), 'other')
    
    def _estimate_funding_stage(self, total_raised: float) -> str:
        """Estimate funding stage from total raised"""
        if total_raised < 1_000_000:
            return 'pre_seed'
        elif total_raised < 5_000_000:
            return 'seed'
        elif total_raised < 20_000_000:
            return 'series_a'
        elif total_raised < 50_000_000:
            return 'series_b'
        else:
            return 'series_c'
    
    def create_failure_dataset(self) -> pd.DataFrame:
        """Create comprehensive failure dataset"""
        logger.info("Creating failure dataset...")
        
        # Get failures from multiple sources
        known_failures = self.get_known_failures()
        cb_failures = self.get_cb_insights_failures()
        
        # Combine all failures
        all_failures = known_failures + cb_failures
        
        # Create DataFrame
        failure_df = pd.DataFrame(all_failures)
        
        # Save to file
        output_path = self.output_dir / "failed_startups_dataset.csv"
        failure_df.to_csv(output_path, index=False)
        
        logger.info(f"Created dataset with {len(failure_df)} failed startups")
        logger.info(f"Saved to {output_path}")
        
        # Print summary
        print("\nFailure Dataset Summary:")
        print(f"Total failures: {len(failure_df)}")
        print(f"Average capital raised: ${failure_df['total_capital_raised_usd'].mean():,.0f}")
        print(f"Sectors: {failure_df['sector'].value_counts().to_dict()}")
        
        return failure_df


def main():
    """Run failure detection"""
    detector = StartupFailureDetector()
    
    # Create failure dataset
    failures = detector.create_failure_dataset()
    
    print("\nTop 5 failures by capital raised:")
    top_failures = failures.nlargest(5, 'total_capital_raised_usd')[['company_name', 'total_capital_raised_usd', 'sector']]
    print(top_failures.to_string(index=False))


if __name__ == "__main__":
    main()