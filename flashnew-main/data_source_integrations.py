#!/usr/bin/env python3
"""
Data Source Integration Guide for Real Startup Data
Shows how to connect to legitimate startup data sources
"""

import os
import json
import requests
import pandas as pd
from typing import Dict, List, Optional
from datetime import datetime
import yfinance as yf
from bs4 import BeautifulSoup
import feedparser
import logging

logger = logging.getLogger(__name__)

class DataSourceIntegrations:
    """Integration methods for various startup data sources"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Research Bot) Startup Data Collection'
        })
    
    # ===== LEGITIMATE FREE DATA SOURCES =====
    
    def get_sec_edgar_data(self, cik_or_ticker: str) -> Dict:
        """
        Get public company data from SEC EDGAR (completely free and legal)
        Perfect for IPO outcomes and public company financials
        """
        base_url = "https://data.sec.gov/submissions/CIK{}.json"
        
        # Convert ticker to CIK if needed
        if not cik_or_ticker.isdigit():
            cik = self._ticker_to_cik(cik_or_ticker)
        else:
            cik = cik_or_ticker.zfill(10)
        
        try:
            response = self.session.get(
                base_url.format(cik),
                headers={'User-Agent': 'Research Bot (research@example.com)'}
            )
            
            if response.status_code == 200:
                data = response.json()
                return {
                    'company_name': data.get('name'),
                    'cik': data.get('cik'),
                    'sic': data.get('sic'),
                    'sic_description': data.get('sicDescription'),
                    'ticker': data.get('tickers', [None])[0],
                    'exchange': data.get('exchanges', [None])[0],
                    'ipo_date': self._extract_ipo_date(data),
                    'filings': data.get('filings', {}).get('recent', {})
                }
        except Exception as e:
            logger.error(f"Error fetching SEC data: {e}")
            return {}
    
    def get_yahoo_finance_data(self, ticker: str) -> Dict:
        """
        Get public company data from Yahoo Finance
        Provides IPO info, market cap, financials
        """
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            
            return {
                'company_name': info.get('longName'),
                'ticker': ticker,
                'market_cap': info.get('marketCap'),
                'ipo_date': info.get('ipoDate'),
                'sector': info.get('sector'),
                'industry': info.get('industry'),
                'website': info.get('website'),
                'headquarters': f"{info.get('city', '')}, {info.get('state', '')} {info.get('country', '')}",
                'employees': info.get('fullTimeEmployees'),
                'revenue': info.get('totalRevenue'),
                'founded': info.get('founded'),
                'outcome': 'ipo',
                'stock_price': info.get('currentPrice'),
                'pe_ratio': info.get('trailingPE')
            }
        except Exception as e:
            logger.error(f"Error fetching Yahoo Finance data: {e}")
            return {}
    
    def scrape_techcrunch_exits(self, days_back: int = 30) -> List[Dict]:
        """
        Scrape recent exit announcements from TechCrunch
        Provides acquisition and shutdown data
        """
        exits = []
        
        # TechCrunch RSS feeds
        feeds = [
            'https://techcrunch.com/category/mergers-and-acquisitions/feed/',
            'https://techcrunch.com/category/startups/feed/'
        ]
        
        for feed_url in feeds:
            try:
                feed = feedparser.parse(feed_url)
                
                for entry in feed.entries:
                    # Parse for acquisition/exit keywords
                    if any(keyword in entry.title.lower() 
                          for keyword in ['acquires', 'acquired', 'buys', 'merger', 'ipo', 'shuts down']):
                        
                        exits.append({
                            'title': entry.title,
                            'link': entry.link,
                            'published': entry.published,
                            'summary': entry.summary,
                            'source': 'techcrunch'
                        })
                        
            except Exception as e:
                logger.error(f"Error scraping TechCrunch: {e}")
                
        return exits
    
    def get_github_startup_data(self, org_name: str) -> Dict:
        """
        Get startup technology data from GitHub
        Useful for tech stack, team size, activity metrics
        """
        api_url = f"https://api.github.com/orgs/{org_name}"
        
        try:
            response = self.session.get(api_url)
            if response.status_code == 200:
                data = response.json()
                
                # Get repository data
                repos_response = self.session.get(data['repos_url'])
                repos = repos_response.json() if repos_response.status_code == 200 else []
                
                return {
                    'company_name': data.get('name') or org_name,
                    'website': data.get('blog'),
                    'location': data.get('location'),
                    'public_repos': data.get('public_repos'),
                    'created_at': data.get('created_at'),
                    'tech_stack': self._analyze_tech_stack(repos),
                    'team_activity': len(set(r.get('owner', {}).get('login') for r in repos)),
                    'github_url': data.get('html_url')
                }
        except Exception as e:
            logger.error(f"Error fetching GitHub data: {e}")
            return {}
    
    def get_producthunt_data(self, product_slug: str) -> Dict:
        """
        Get product launch and traction data from Product Hunt
        Useful for early validation metrics
        """
        # Note: This would require Product Hunt API access
        # Shows product launches, upvotes, reviews
        pass
    
    def get_linkedin_company_data(self, company_url: str) -> Dict:
        """
        Template for LinkedIn company data extraction
        Note: Requires LinkedIn API access or careful web scraping
        """
        # LinkedIn provides:
        # - Employee count and growth
        # - Founder profiles
        # - Company updates
        # - Industry and location
        
        # This would require LinkedIn API credentials
        # or careful rate-limited scraping
        pass
    
    # ===== PAID/RESTRICTED DATA SOURCES =====
    
    def get_crunchbase_data(self, api_key: str, company_name: str) -> Dict:
        """
        Get comprehensive startup data from Crunchbase API
        Note: Requires paid API access (~$500-5000/month)
        """
        headers = {'X-API-KEY': api_key}
        
        # Search for company
        search_url = "https://api.crunchbase.com/v4/data/entities/organizations"
        params = {
            'field_ids': 'identifier,name,website,categories,founded_on,funding_total',
            'query': company_name,
            'limit': 1
        }
        
        try:
            response = self.session.get(search_url, headers=headers, params=params)
            if response.status_code == 200:
                data = response.json()
                # Process and return company data
                return data
        except Exception as e:
            logger.error(f"Error fetching Crunchbase data: {e}")
            return {}
    
    def get_pitchbook_data(self, company_id: str) -> Dict:
        """
        Template for PitchBook data access
        Note: Requires institutional subscription (~$15k-40k/year)
        """
        # PitchBook provides:
        # - Detailed funding history
        # - Valuations
        # - Exit details
        # - Investor information
        # - Financial metrics
        
        # Most universities and investment firms have access
        # Data can be exported to CSV for processing
        pass
    
    def get_cbinsights_data(self, company_name: str) -> Dict:
        """
        Template for CB Insights data access
        Note: Requires subscription (~$5k-50k/year)
        """
        # CB Insights provides:
        # - Market intelligence
        # - Company metrics
        # - Industry analysis
        # - Competitive landscape
        pass
    
    # ===== DATA ENRICHMENT METHODS =====
    
    def enrich_with_news_data(self, company_name: str) -> List[Dict]:
        """
        Search news sources for company mentions and events
        """
        news_sources = []
        
        # Google News RSS
        google_news_url = f"https://news.google.com/rss/search?q={company_name}+startup+funding"
        
        try:
            feed = feedparser.parse(google_news_url)
            for entry in feed.entries[:10]:
                news_sources.append({
                    'title': entry.title,
                    'link': entry.link,
                    'published': entry.published,
                    'source': 'google_news'
                })
        except Exception as e:
            logger.error(f"Error fetching news: {e}")
            
        return news_sources
    
    def enrich_with_patent_data(self, company_name: str) -> Dict:
        """
        Search USPTO for company patents (indicator of innovation)
        """
        # USPTO provides free patent search API
        # Patents indicate technical innovation and IP strength
        pass
    
    def enrich_with_trademark_data(self, company_name: str) -> Dict:
        """
        Search USPTO for company trademarks
        """
        # Trademarks indicate brand building and market presence
        pass
    
    # ===== HELPER METHODS =====
    
    def _ticker_to_cik(self, ticker: str) -> str:
        """Convert stock ticker to SEC CIK number"""
        # SEC provides a mapping file
        mapping_url = "https://www.sec.gov/include/ticker.txt"
        
        try:
            response = self.session.get(mapping_url)
            for line in response.text.split('\n'):
                if line.strip():
                    t, c = line.split('\t')
                    if t.upper() == ticker.upper():
                        return c.zfill(10)
        except:
            pass
            
        return ""
    
    def _extract_ipo_date(self, sec_data: Dict) -> Optional[str]:
        """Extract IPO date from SEC filings"""
        filings = sec_data.get('filings', {}).get('recent', {})
        
        # Look for S-1 filings (IPO registration)
        for i, form in enumerate(filings.get('form', [])):
            if form in ['S-1', 'S-1/A', '424B4']:
                return filings.get('filingDate', [])[i]
                
        return None
    
    def _analyze_tech_stack(self, repos: List[Dict]) -> List[str]:
        """Analyze repositories to determine tech stack"""
        languages = {}
        
        for repo in repos:
            lang = repo.get('language')
            if lang:
                languages[lang] = languages.get(lang, 0) + 1
                
        # Sort by usage
        sorted_langs = sorted(languages.items(), key=lambda x: x[1], reverse=True)
        return [lang for lang, _ in sorted_langs[:5]]

class DataCollectionStrategy:
    """Strategic approach to collecting 100k+ real startup records"""
    
    def __init__(self):
        self.integrations = DataSourceIntegrations()
    
    def get_collection_plan(self) -> Dict:
        """
        Realistic plan to collect 100k startup records
        """
        return {
            "phase_1_public_companies": {
                "source": "SEC EDGAR + Yahoo Finance",
                "estimated_records": 10000,
                "data_quality": "Very High",
                "cost": "Free",
                "includes": [
                    "All US IPOs from 2000-2024",
                    "Complete financials",
                    "Verified outcomes",
                    "Market performance"
                ]
            },
            "phase_2_unicorns": {
                "source": "Public lists + News scraping",
                "estimated_records": 2000,
                "data_quality": "High",
                "cost": "Free",
                "includes": [
                    "CB Insights Unicorn List",
                    "Forbes Next Billion-Dollar Startups",
                    "TechCrunch coverage"
                ]
            },
            "phase_3_acquisitions": {
                "source": "M&A databases + News",
                "estimated_records": 20000,
                "data_quality": "High",
                "cost": "Free-Low",
                "includes": [
                    "Crunchbase acquisitions (public data)",
                    "TechCrunch exit coverage",
                    "SEC M&A filings"
                ]
            },
            "phase_4_funded_startups": {
                "source": "Multiple sources",
                "estimated_records": 50000,
                "data_quality": "Medium-High",
                "cost": "Varies",
                "includes": [
                    "AngelList public profiles",
                    "ProductHunt launches",
                    "GitHub organizations",
                    "Startup competition winners"
                ]
            },
            "phase_5_shutdowns": {
                "source": "Failure tracking",
                "estimated_records": 20000,
                "data_quality": "Medium",
                "cost": "Free",
                "includes": [
                    "CB Insights failure reports",
                    "Shutdown announcement tracking",
                    "Domain expiration monitoring"
                ]
            }
        }
    
    def estimate_data_collection_time(self) -> Dict:
        """
        Realistic timeline for data collection
        """
        return {
            "automated_collection": {
                "sec_data": "1-2 days for 10k companies",
                "news_scraping": "3-5 days for 20k articles",
                "api_calls": "Depends on rate limits"
            },
            "manual_enrichment": {
                "data_validation": "1-2 weeks",
                "missing_data_research": "2-4 weeks",
                "outcome_verification": "Ongoing"
            },
            "total_estimate": "4-8 weeks for 100k records with 70%+ completeness"
        }

def demonstrate_data_collection():
    """Demonstrate collecting real startup data"""
    integrations = DataSourceIntegrations()
    
    print("=== Startup Data Collection Demo ===\n")
    
    # Example 1: Get IPO data
    print("1. Fetching IPO data from SEC/Yahoo Finance:")
    ipo_examples = ['ABNB', 'UBER', 'LYFT', 'SNAP', 'PINS']
    
    for ticker in ipo_examples[:2]:  # Demo with 2 companies
        yf_data = integrations.get_yahoo_finance_data(ticker)
        if yf_data:
            print(f"\n{ticker}:")
            print(f"  Company: {yf_data.get('company_name')}")
            print(f"  IPO Date: {yf_data.get('ipo_date')}")
            print(f"  Market Cap: ${yf_data.get('market_cap', 0):,.0f}")
            print(f"  Employees: {yf_data.get('employees', 'N/A')}")
    
    # Example 2: Get recent exits
    print("\n\n2. Recent Exit Announcements:")
    exits = integrations.scrape_techcrunch_exits(days_back=7)
    for exit in exits[:3]:
        print(f"\n- {exit['title']}")
        print(f"  Date: {exit['published']}")
        print(f"  Link: {exit['link']}")
    
    # Example 3: Show collection strategy
    print("\n\n3. Data Collection Strategy:")
    strategy = DataCollectionStrategy()
    plan = strategy.get_collection_plan()
    
    total_records = sum(phase['estimated_records'] for phase in plan.values())
    print(f"\nTotal estimated records: {total_records:,}")
    
    for phase_name, phase_data in plan.items():
        print(f"\n{phase_name}:")
        print(f"  Records: {phase_data['estimated_records']:,}")
        print(f"  Quality: {phase_data['data_quality']}")
        print(f"  Cost: {phase_data['cost']}")

if __name__ == "__main__":
    demonstrate_data_collection()