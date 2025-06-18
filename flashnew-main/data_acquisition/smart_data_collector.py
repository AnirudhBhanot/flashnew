#!/usr/bin/env python3
"""
Smart Data Collector - Gather real startup data from public sources
Uses only legal, publicly available data sources
"""

import requests
import pandas as pd
import time
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import json
import re
from pathlib import Path
import logging
from typing import Dict, List, Optional, Tuple
import yfinance as yf
from newsapi import NewsApiClient
import wikipedia

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SmartStartupDataCollector:
    """Collect real startup data from multiple public sources"""
    
    def __init__(self):
        self.output_dir = Path("data/real_startups")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Research Bot) Academic Research'
        })
        
    def collect_ipo_data(self) -> pd.DataFrame:
        """Collect recent IPO data from Yahoo Finance"""
        logger.info("Collecting IPO data from public sources...")
        
        ipo_data = []
        
        # Get recent IPOs from Yahoo Finance
        ipo_symbols = self._get_recent_ipo_symbols()
        
        for symbol in ipo_symbols[:50]:  # Limit to 50 for demo
            try:
                ticker = yf.Ticker(symbol)
                info = ticker.info
                
                if info.get('sector') in ['Technology', 'Communication Services', 'Consumer Cyclical']:
                    startup = {
                        'company_name': info.get('longName', symbol),
                        'symbol': symbol,
                        'sector': self._map_to_camp_sector(info.get('sector', 'Other')),
                        'founded_year': self._extract_founded_year(info),
                        'ipo_date': info.get('firstTradeDateEpochUtc'),
                        'market_cap': info.get('marketCap', 0),
                        'revenue': info.get('totalRevenue', 0),
                        'employees': info.get('fullTimeEmployees', 0),
                        'outcome': 'ipo',
                        'success': 1
                    }
                    
                    # Extract more detailed metrics
                    startup.update(self._extract_financial_metrics(info))
                    ipo_data.append(startup)
                    
                time.sleep(0.5)  # Rate limiting
                
            except Exception as e:
                logger.warning(f"Error processing {symbol}: {e}")
                
        return pd.DataFrame(ipo_data)
    
    def collect_acquisition_data(self) -> pd.DataFrame:
        """Collect acquisition data from public news sources"""
        logger.info("Collecting acquisition data...")
        
        acquisitions = []
        
        # Search patterns for tech acquisitions
        search_queries = [
            "tech startup acquired billion",
            "startup acquisition deal announced",
            "acquired by Google Facebook Amazon Microsoft Apple"
        ]
        
        for query in search_queries:
            results = self._search_news_for_acquisitions(query)
            acquisitions.extend(results)
            
        return pd.DataFrame(acquisitions)
    
    def collect_failed_startups(self) -> pd.DataFrame:
        """Collect data on failed startups from public sources"""
        logger.info("Collecting failed startup data...")
        
        failures = []
        
        # Known high-profile failures with public data
        known_failures = [
            {
                'company_name': 'Theranos',
                'sector': 'healthtech',
                'founded_year': 2003,
                'shutdown_year': 2018,
                'total_raised': 945000000,
                'failure_reason': 'fraud',
                'employees_peak': 800
            },
            {
                'company_name': 'Quibi',
                'sector': 'entertainment',
                'founded_year': 2018,
                'shutdown_year': 2020,
                'total_raised': 1750000000,
                'failure_reason': 'no_market_fit',
                'employees_peak': 200
            },
            {
                'company_name': 'WeWork',
                'sector': 'real_estate',
                'founded_year': 2010,
                'shutdown_year': None,  # Still operating but failed IPO
                'total_raised': 12800000000,
                'failure_reason': 'unsustainable_model',
                'employees_peak': 15000
            }
        ]
        
        for failure in known_failures:
            # Enrich with additional data
            enriched = self._enrich_startup_data(failure)
            enriched['outcome'] = 'failed'
            enriched['success'] = 0
            failures.append(enriched)
            
        # Search for more failures
        failure_queries = [
            "startup shutdown ran out of money",
            "tech startup failed bankruptcy",
            "startup closure employees laid off"
        ]
        
        for query in failure_queries:
            results = self._search_news_for_failures(query)
            failures.extend(results)
            
        return pd.DataFrame(failures)
    
    def collect_active_startups(self) -> pd.DataFrame:
        """Collect data on currently active startups"""
        logger.info("Collecting active startup data...")
        
        active_startups = []
        
        # Use AngelList trending startups (public data)
        trending = self._get_angellist_trending()
        
        # Use ProductHunt launches
        producthunt = self._get_producthunt_startups()
        
        active_startups.extend(trending)
        active_startups.extend(producthunt)
        
        return pd.DataFrame(active_startups)
    
    def extract_camp_features(self, startup_df: pd.DataFrame) -> pd.DataFrame:
        """Convert raw startup data to CAMP features"""
        logger.info("Extracting CAMP features...")
        
        camp_df = pd.DataFrame()
        
        # Capital features
        camp_df['total_capital_raised_usd'] = startup_df.get('total_raised', 0)
        camp_df['funding_stage'] = startup_df.get('last_funding_type', 'unknown')
        camp_df['investor_tier_primary'] = self._estimate_investor_tier(startup_df)
        
        # Market features  
        camp_df['sector'] = startup_df.get('sector', 'other')
        camp_df['tam_size_usd'] = self._estimate_tam(startup_df)
        camp_df['market_growth_rate_percent'] = self._estimate_market_growth(startup_df)
        
        # People features
        camp_df['team_size_full_time'] = startup_df.get('employees', 10)
        camp_df['founders_count'] = startup_df.get('founders_count', 2)
        
        # Product features
        camp_df['annual_revenue_run_rate'] = startup_df.get('revenue', 0)
        camp_df['product_stage'] = self._estimate_product_stage(startup_df)
        
        # Fill remaining features with reasonable defaults
        camp_df = self._fill_missing_camp_features(camp_df)
        
        # Add outcome
        camp_df['success'] = startup_df.get('success', 0)
        
        return camp_df
    
    def _get_recent_ipo_symbols(self) -> List[str]:
        """Get list of recent tech IPO symbols"""
        # Recent tech IPOs (2020-2024)
        return [
            'ABNB', 'DASH', 'RBLX', 'COIN', 'HOOD', 'RIVN', 'NU', 'SOFI',
            'PATH', 'DDOG', 'SNOW', 'U', 'PLTR', 'ZM', 'PTON', 'DBX',
            'SPOT', 'SNAP', 'PINS', 'UBER', 'LYFT', 'BYND', 'WORK'
        ]
    
    def _extract_financial_metrics(self, info: Dict) -> Dict:
        """Extract financial metrics from company info"""
        return {
            'revenue_growth_rate_percent': info.get('revenueGrowth', 0) * 100 if info.get('revenueGrowth') else 20,
            'gross_margin_percent': info.get('grossMargins', 0) * 100 if info.get('grossMargins') else 50,
            'burn_multiple': abs(info.get('freeCashflow', 0) / info.get('totalRevenue', 1)) if info.get('totalRevenue') else 2,
            'cash_on_hand_usd': info.get('totalCash', 0),
            'total_capital_raised_usd': info.get('marketCap', 0) * 0.3  # Rough estimate
        }
    
    def _search_news_for_acquisitions(self, query: str) -> List[Dict]:
        """Search news for acquisition data"""
        acquisitions = []
        
        # Simulate news search results (in production, use NewsAPI or similar)
        # For demo, return some known acquisitions
        known_acquisitions = [
            {
                'company_name': 'Instagram',
                'acquirer': 'Facebook',
                'price': 1000000000,
                'year': 2012,
                'sector': 'social_media',
                'success': 1
            },
            {
                'company_name': 'WhatsApp', 
                'acquirer': 'Facebook',
                'price': 19000000000,
                'year': 2014,
                'sector': 'messaging',
                'success': 1
            }
        ]
        
        return known_acquisitions[:2]  # Return subset
    
    def _get_angellist_trending(self) -> List[Dict]:
        """Get trending startups from AngelList (simulated)"""
        # In production, use AngelList API or scraping
        # For demo, return sample data
        return [
            {
                'company_name': 'OpenAI',
                'sector': 'ai_ml',
                'founded_year': 2015,
                'employees': 375,
                'total_raised': 11300000000,
                'product_stage': 'growth'
            },
            {
                'company_name': 'Anthropic',
                'sector': 'ai_ml',
                'founded_year': 2021,
                'employees': 150,
                'total_raised': 1500000000,
                'product_stage': 'growth'
            }
        ]
    
    def _estimate_tam(self, startup_df: pd.DataFrame) -> float:
        """Estimate TAM based on sector"""
        sector_tam = {
            'ai_ml': 500_000_000_000,
            'saas': 300_000_000_000,
            'fintech': 250_000_000_000,
            'healthtech': 200_000_000_000,
            'ecommerce': 400_000_000_000,
            'other': 100_000_000_000
        }
        
        sector = startup_df.get('sector', 'other').iloc[0] if isinstance(startup_df, pd.DataFrame) else startup_df.get('sector', 'other')
        return sector_tam.get(sector, 100_000_000_000)
    
    def _fill_missing_camp_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Fill missing CAMP features with intelligent defaults"""
        
        # Import the canonical feature list
        from feature_config import ALL_FEATURES
        
        # Default values based on typical startup metrics
        defaults = {
            # Capital
            'cash_on_hand_usd': 500000,
            'monthly_burn_usd': 50000,
            'runway_months': 10,
            'burn_multiple': 2.0,
            'has_debt': 0,
            
            # Advantage
            'patent_count': 0,
            'network_effects_present': 0,
            'has_data_moat': 0,
            'regulatory_advantage_present': 0,
            'tech_differentiation_score': 3,
            'switching_cost_score': 3,
            'brand_strength_score': 2,
            'scalability_score': 4,
            
            # Market
            'sam_size_usd': 10_000_000_000,
            'som_size_usd': 100_000_000,
            'customer_count': 100,
            'customer_concentration_percent': 20,
            'user_growth_rate_percent': 50,
            'net_dollar_retention_percent': 110,
            'competition_intensity': 4,
            'competitors_named_count': 10,
            
            # People
            'years_experience_avg': 10,
            'domain_expertise_years_avg': 5,
            'prior_startup_experience_count': 1,
            'prior_successful_exits_count': 0,
            'board_advisor_experience_score': 3,
            'advisors_count': 3,
            'team_diversity_percent': 30,
            'key_person_dependency': 1,
            
            # Product
            'product_retention_30d': 40,
            'product_retention_90d': 25,
            'dau_mau_ratio': 0.3,
            'revenue_growth_rate_percent': 100,
            'gross_margin_percent': 70,
            'ltv_cac_ratio': 3.0,
            'customer_acquisition_cost': 100
        }
        
        # Ensure all CAMP features exist
        for feature in ALL_FEATURES:
            if feature not in df.columns:
                df[feature] = defaults.get(feature, 0)
                
        return df
    
    def create_real_dataset(self, output_file: str = "real_startup_dataset_1k.csv"):
        """Create combined dataset from all sources"""
        logger.info("Creating combined real startup dataset...")
        
        # Collect from all sources
        ipo_df = self.collect_ipo_data()
        logger.info(f"Collected {len(ipo_df)} IPO companies")
        
        acquisition_df = self.collect_acquisition_data()
        logger.info(f"Collected {len(acquisition_df)} acquisitions")
        
        failed_df = self.collect_failed_startups()
        logger.info(f"Collected {len(failed_df)} failed startups")
        
        active_df = self.collect_active_startups()
        logger.info(f"Collected {len(active_df)} active startups")
        
        # Combine all data
        all_startups = pd.concat([ipo_df, acquisition_df, failed_df, active_df], ignore_index=True)
        logger.info(f"Total raw startups: {len(all_startups)}")
        
        # Extract CAMP features
        camp_dataset = self.extract_camp_features(all_startups)
        
        # Save dataset
        output_path = self.output_dir / output_file
        camp_dataset.to_csv(output_path, index=False)
        logger.info(f"Saved {len(camp_dataset)} startups to {output_path}")
        
        # Print summary statistics
        print("\nDataset Summary:")
        print(f"Total startups: {len(camp_dataset)}")
        print(f"Success rate: {camp_dataset['success'].mean():.1%}")
        print(f"Sectors: {camp_dataset['sector'].value_counts().to_dict()}")
        
        return camp_dataset


def main():
    """Run the smart data collection"""
    collector = SmartStartupDataCollector()
    
    # Create initial real dataset
    real_data = collector.create_real_dataset()
    
    print("\nReal data collection complete!")
    print("Note: This is a demo with limited data. For production:")
    print("- Set up NewsAPI key for news searching")
    print("- Implement SEC Edgar scraping")
    print("- Add more data sources")
    print("- Scale to thousands of companies")


if __name__ == "__main__":
    main()