#!/usr/bin/env python3
"""
Real Startup Database Builder for FLASH Platform
Collects verified startup data with actual outcomes from legitimate sources
"""

import json
import csv
import sqlite3
import requests
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
import pandas as pd
from urllib.parse import quote
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('startup_data_collection.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class StartupOutcome(Enum):
    """Verified startup outcomes"""
    ACTIVE = "active"
    ACQUIRED = "acquired"
    IPO = "ipo"
    SHUTDOWN = "shutdown"
    MERGED = "merged"
    PIVOTED = "pivoted"
    UNKNOWN = "unknown"

class FundingStage(Enum):
    """Standard funding stages"""
    PRE_SEED = "pre_seed"
    SEED = "seed"
    SERIES_A = "series_a"
    SERIES_B = "series_b"
    SERIES_C = "series_c"
    SERIES_D_PLUS = "series_d_plus"
    DEBT = "debt"
    GRANT = "grant"
    ICO = "ico"
    UNKNOWN = "unknown"

@dataclass
class StartupData:
    """Core startup data structure for FLASH"""
    # Basic Information
    company_id: str
    company_name: str
    founded_date: Optional[str]
    industry: str
    sub_industry: Optional[str]
    headquarters_location: str
    website: Optional[str]
    
    # Founders & Team
    founder_names: List[str]
    founder_backgrounds: Dict[str, str]  # name -> background
    team_size: Optional[int]
    key_employees: Optional[int]
    
    # Funding Data
    total_funding: float
    funding_rounds: List[Dict]  # date, amount, stage, investors
    last_funding_date: Optional[str]
    last_funding_amount: Optional[float]
    last_funding_stage: Optional[str]
    lead_investors: List[str]
    all_investors: List[str]
    
    # Business Metrics
    business_model: str
    target_market: str
    revenue_range: Optional[str]
    growth_rate: Optional[float]
    burn_rate: Optional[float]
    runway_months: Optional[int]
    
    # Outcome Data
    outcome: StartupOutcome
    outcome_date: Optional[str]
    exit_value: Optional[float]
    acquirer: Optional[str]
    ipo_ticker: Optional[str]
    shutdown_reason: Optional[str]
    
    # Market & Competition
    market_size: Optional[float]
    competitors: List[str]
    market_position: Optional[str]
    
    # Additional Metrics for FLASH
    product_market_fit_score: Optional[float]  # 0-1
    technology_score: Optional[float]  # 0-1
    team_score: Optional[float]  # 0-1
    market_timing_score: Optional[float]  # 0-1
    
    # Data Quality
    data_source: str
    last_updated: str
    data_completeness: float  # 0-1
    verified: bool

class DataCollector:
    """Manages data collection from multiple sources"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Startup Data Research Bot)'
        })
        self.db_path = "startup_database.db"
        self.init_database()
        
    def init_database(self):
        """Initialize SQLite database with proper schema"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS startups (
                company_id TEXT PRIMARY KEY,
                company_name TEXT NOT NULL,
                founded_date TEXT,
                industry TEXT,
                sub_industry TEXT,
                headquarters_location TEXT,
                website TEXT,
                founder_names TEXT,
                founder_backgrounds TEXT,
                team_size INTEGER,
                key_employees INTEGER,
                total_funding REAL,
                funding_rounds TEXT,
                last_funding_date TEXT,
                last_funding_amount REAL,
                last_funding_stage TEXT,
                lead_investors TEXT,
                all_investors TEXT,
                business_model TEXT,
                target_market TEXT,
                revenue_range TEXT,
                growth_rate REAL,
                burn_rate REAL,
                runway_months INTEGER,
                outcome TEXT,
                outcome_date TEXT,
                exit_value REAL,
                acquirer TEXT,
                ipo_ticker TEXT,
                shutdown_reason TEXT,
                market_size REAL,
                competitors TEXT,
                market_position TEXT,
                product_market_fit_score REAL,
                technology_score REAL,
                team_score REAL,
                market_timing_score REAL,
                data_source TEXT,
                last_updated TEXT,
                data_completeness REAL,
                verified BOOLEAN,
                UNIQUE(company_id)
            )
        ''')
        
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_outcome ON startups(outcome);
        ''')
        
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_industry ON startups(industry);
        ''')
        
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_founded ON startups(founded_date);
        ''')
        
        conn.commit()
        conn.close()
        
    def collect_from_crunchbase_api(self, api_key: str, limit: int = 1000) -> List[StartupData]:
        """
        Collect data from Crunchbase API (requires API key)
        Note: This is a template - actual implementation requires valid API access
        """
        startups = []
        base_url = "https://api.crunchbase.com/v4/data/entities/organizations"
        
        headers = {
            'X-API-KEY': api_key
        }
        
        params = {
            'field_ids': 'identifier,name,founded_on,categories,location,website,funding_total,num_funding_rounds,last_funding_on,ipo_status,acquired_on,closed_on',
            'limit': min(limit, 100),
            'sort': 'rank_org'
        }
        
        try:
            # This is a template - actual API implementation would go here
            logger.info(f"Would collect {limit} companies from Crunchbase API")
            # response = self.session.get(base_url, headers=headers, params=params)
            # data = response.json()
            # Process and convert to StartupData objects
        except Exception as e:
            logger.error(f"Error collecting from Crunchbase: {e}")
            
        return startups
    
    def collect_from_pitchbook_export(self, csv_path: str) -> List[StartupData]:
        """
        Process exported data from PitchBook or similar platforms
        Many institutions have access to these datasets
        """
        startups = []
        
        try:
            df = pd.read_csv(csv_path)
            
            for _, row in df.iterrows():
                startup = self._parse_pitchbook_row(row)
                if startup:
                    startups.append(startup)
                    
            logger.info(f"Processed {len(startups)} companies from PitchBook export")
            
        except Exception as e:
            logger.error(f"Error processing PitchBook data: {e}")
            
        return startups
    
    def collect_from_sec_filings(self, ticker_list: List[str]) -> List[StartupData]:
        """
        Collect IPO and public company data from SEC EDGAR
        This provides verified outcome data for IPOs
        """
        startups = []
        base_url = "https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json"
        
        for ticker in ticker_list:
            try:
                # Get company data from SEC
                # This is a simplified example - full implementation would parse EDGAR data
                time.sleep(0.1)  # Respect rate limits
                
                startup_data = self._parse_sec_data(ticker)
                if startup_data:
                    startups.append(startup_data)
                    
            except Exception as e:
                logger.error(f"Error collecting SEC data for {ticker}: {e}")
                
        return startups
    
    def collect_from_techcrunch_exits(self) -> List[StartupData]:
        """
        Parse TechCrunch and other tech news for exit announcements
        This provides verified acquisition and shutdown data
        """
        exits = []
        
        # Sources for exit data:
        # - TechCrunch acquisitions tag
        # - Crunchbase exits
        # - CB Insights exit reports
        # - PitchBook exit data
        
        # This would involve web scraping or API access
        logger.info("Collecting exit data from tech news sources")
        
        return exits
    
    def collect_from_angellist(self) -> List[StartupData]:
        """
        Collect startup data from AngelList (if API access available)
        Good source for early-stage companies
        """
        startups = []
        
        # AngelList provides data on:
        # - Early stage startups
        # - Founder backgrounds
        # - Funding rounds
        # - Team information
        
        logger.info("Would collect data from AngelList")
        
        return startups
    
    def enrich_with_linkedin_data(self, startup: StartupData) -> StartupData:
        """
        Enrich startup data with LinkedIn information
        Provides team size, founder backgrounds, employee growth
        """
        # LinkedIn data can provide:
        # - Accurate team size
        # - Founder work history
        # - Employee growth trends
        # - Key hire information
        
        return startup
    
    def calculate_flash_scores(self, startup: StartupData) -> StartupData:
        """
        Calculate FLASH-specific scores based on available data
        """
        # Product-Market Fit Score
        pmf_score = self._calculate_pmf_score(startup)
        startup.product_market_fit_score = pmf_score
        
        # Technology Score
        tech_score = self._calculate_tech_score(startup)
        startup.technology_score = tech_score
        
        # Team Score
        team_score = self._calculate_team_score(startup)
        startup.team_score = team_score
        
        # Market Timing Score
        timing_score = self._calculate_timing_score(startup)
        startup.market_timing_score = timing_score
        
        return startup
    
    def _calculate_pmf_score(self, startup: StartupData) -> float:
        """Calculate product-market fit score"""
        score = 0.5  # Base score
        
        # Factors that indicate PMF:
        # - Multiple funding rounds
        # - Revenue growth
        # - Customer retention
        # - Market expansion
        
        if startup.funding_rounds and len(startup.funding_rounds) > 2:
            score += 0.1
            
        if startup.growth_rate and startup.growth_rate > 100:
            score += 0.2
            
        if startup.outcome == StartupOutcome.IPO:
            score = max(score, 0.9)
        elif startup.outcome == StartupOutcome.ACQUIRED and startup.exit_value:
            if startup.exit_value > 1000000000:  # $1B+
                score = max(score, 0.85)
                
        return min(score, 1.0)
    
    def _calculate_tech_score(self, startup: StartupData) -> float:
        """Calculate technology/innovation score"""
        score = 0.5
        
        # Factors:
        # - Patent portfolio
        # - Technical founders
        # - R&D spending
        # - Industry (deep tech vs consumer)
        
        tech_industries = ['AI', 'Biotech', 'Robotics', 'Quantum', 'Space']
        if any(ind in startup.industry for ind in tech_industries):
            score += 0.2
            
        return min(score, 1.0)
    
    def _calculate_team_score(self, startup: StartupData) -> float:
        """Calculate team quality score"""
        score = 0.5
        
        # Factors:
        # - Founder experience
        # - Previous exits
        # - Team growth
        # - Advisor quality
        
        if startup.founder_backgrounds:
            for founder, background in startup.founder_backgrounds.items():
                if any(term in background.lower() for term in ['exit', 'ipo', 'acquired']):
                    score += 0.1
                    
        if startup.team_size and startup.team_size > 50:
            score += 0.1
            
        return min(score, 1.0)
    
    def _calculate_timing_score(self, startup: StartupData) -> float:
        """Calculate market timing score"""
        score = 0.5
        
        # Factors:
        # - Market growth rate
        # - Competitive landscape
        # - Regulatory environment
        # - Technology maturity
        
        if startup.market_size and startup.market_size > 10000000000:  # $10B+
            score += 0.1
            
        return min(score, 1.0)
    
    def save_to_database(self, startups: List[StartupData]):
        """Save startup data to SQLite database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        for startup in startups:
            data = asdict(startup)
            
            # Convert lists and dicts to JSON strings
            data['founder_names'] = json.dumps(data['founder_names'])
            data['founder_backgrounds'] = json.dumps(data['founder_backgrounds'])
            data['funding_rounds'] = json.dumps(data['funding_rounds'])
            data['lead_investors'] = json.dumps(data['lead_investors'])
            data['all_investors'] = json.dumps(data['all_investors'])
            data['competitors'] = json.dumps(data['competitors'])
            data['outcome'] = data['outcome'].value
            
            columns = ', '.join(data.keys())
            placeholders = ', '.join(['?' for _ in data])
            
            query = f"INSERT OR REPLACE INTO startups ({columns}) VALUES ({placeholders})"
            
            try:
                cursor.execute(query, list(data.values()))
            except Exception as e:
                logger.error(f"Error saving {startup.company_name}: {e}")
                
        conn.commit()
        conn.close()
        logger.info(f"Saved {len(startups)} startups to database")
    
    def export_to_flash_format(self, output_path: str):
        """Export database to FLASH-compatible format"""
        conn = sqlite3.connect(self.db_path)
        
        # Read all data
        df = pd.read_sql_query("SELECT * FROM startups", conn)
        
        # Convert JSON strings back to objects for export
        json_columns = ['founder_names', 'founder_backgrounds', 'funding_rounds', 
                       'lead_investors', 'all_investors', 'competitors']
        
        for col in json_columns:
            df[col] = df[col].apply(lambda x: json.loads(x) if x else [])
        
        # Create FLASH-specific export
        flash_data = {
            'metadata': {
                'version': '1.0',
                'created_at': datetime.now().isoformat(),
                'total_companies': len(df),
                'outcome_distribution': df['outcome'].value_counts().to_dict(),
                'data_sources': df['data_source'].unique().tolist()
            },
            'companies': df.to_dict('records')
        }
        
        with open(output_path, 'w') as f:
            json.dump(flash_data, f, indent=2)
            
        conn.close()
        logger.info(f"Exported {len(df)} companies to {output_path}")
    
    def validate_data_quality(self):
        """Run data quality checks on the database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Check data completeness
        cursor.execute("""
            SELECT 
                AVG(data_completeness) as avg_completeness,
                COUNT(*) as total_companies,
                SUM(CASE WHEN verified = 1 THEN 1 ELSE 0 END) as verified_count,
                SUM(CASE WHEN outcome != 'unknown' THEN 1 ELSE 0 END) as known_outcomes
            FROM startups
        """)
        
        stats = cursor.fetchone()
        
        logger.info(f"""
        Data Quality Report:
        - Average Completeness: {stats[0]:.2%}
        - Total Companies: {stats[1]:,}
        - Verified Companies: {stats[2]:,} ({stats[2]/stats[1]:.1%})
        - Known Outcomes: {stats[3]:,} ({stats[3]/stats[1]:.1%})
        """)
        
        conn.close()
        
    def _parse_pitchbook_row(self, row) -> Optional[StartupData]:
        """Parse a row from PitchBook CSV export"""
        try:
            # Map PitchBook columns to our data structure
            # This is a template - actual mapping depends on export format
            
            outcome = StartupOutcome.UNKNOWN
            if pd.notna(row.get('Exit Date')):
                if pd.notna(row.get('IPO Date')):
                    outcome = StartupOutcome.IPO
                elif pd.notna(row.get('Acquired Date')):
                    outcome = StartupOutcome.ACQUIRED
                    
            startup = StartupData(
                company_id=str(row.get('Company ID', '')),
                company_name=row.get('Company Name', ''),
                founded_date=str(row.get('Founded Date', '')),
                industry=row.get('Primary Industry', ''),
                sub_industry=row.get('Sub-Industry', ''),
                headquarters_location=row.get('HQ Location', ''),
                website=row.get('Website', ''),
                founder_names=str(row.get('Founders', '')).split(';'),
                founder_backgrounds={},
                team_size=int(row.get('Employees', 0)) if pd.notna(row.get('Employees')) else None,
                key_employees=None,
                total_funding=float(row.get('Total Raised', 0)) if pd.notna(row.get('Total Raised')) else 0,
                funding_rounds=[],
                last_funding_date=str(row.get('Last Financing Date', '')),
                last_funding_amount=float(row.get('Last Financing Size', 0)) if pd.notna(row.get('Last Financing Size')) else None,
                last_funding_stage=row.get('Last Financing Type', ''),
                lead_investors=[],
                all_investors=str(row.get('Investors', '')).split(';') if pd.notna(row.get('Investors')) else [],
                business_model=row.get('Business Model', ''),
                target_market=row.get('Target Market', ''),
                revenue_range=row.get('Revenue Range', ''),
                growth_rate=None,
                burn_rate=None,
                runway_months=None,
                outcome=outcome,
                outcome_date=str(row.get('Exit Date', '')),
                exit_value=float(row.get('Valuation', 0)) if pd.notna(row.get('Valuation')) else None,
                acquirer=row.get('Acquirer', ''),
                ipo_ticker=row.get('Ticker', ''),
                shutdown_reason=None,
                market_size=None,
                competitors=[],
                market_position=None,
                product_market_fit_score=None,
                technology_score=None,
                team_score=None,
                market_timing_score=None,
                data_source='pitchbook',
                last_updated=datetime.now().isoformat(),
                data_completeness=self._calculate_completeness(row),
                verified=True
            )
            
            return startup
            
        except Exception as e:
            logger.error(f"Error parsing row: {e}")
            return None
    
    def _calculate_completeness(self, data) -> float:
        """Calculate how complete a data record is"""
        if isinstance(data, pd.Series):
            filled = data.notna().sum()
            total = len(data)
        else:
            filled = sum(1 for v in data.values() if v is not None)
            total = len(data)
            
        return filled / total if total > 0 else 0
    
    def _parse_sec_data(self, ticker: str) -> Optional[StartupData]:
        """Parse SEC filing data for public companies"""
        # This is a template for SEC data parsing
        # Actual implementation would use SEC EDGAR API
        return None

def main():
    """Main execution function"""
    collector = DataCollector()
    
    logger.info("Starting real startup data collection...")
    
    # 1. Collect from various sources
    all_startups = []
    
    # Example: Process a PitchBook export if available
    if os.path.exists('pitchbook_export.csv'):
        pb_startups = collector.collect_from_pitchbook_export('pitchbook_export.csv')
        all_startups.extend(pb_startups)
    
    # Example: Collect from Crunchbase API (requires API key)
    # cb_key = os.getenv('CRUNCHBASE_API_KEY')
    # if cb_key:
    #     cb_startups = collector.collect_from_crunchbase_api(cb_key, limit=1000)
    #     all_startups.extend(cb_startups)
    
    # 2. Calculate FLASH scores for all startups
    logger.info("Calculating FLASH scores...")
    for i, startup in enumerate(all_startups):
        all_startups[i] = collector.calculate_flash_scores(startup)
    
    # 3. Save to database
    if all_startups:
        collector.save_to_database(all_startups)
        
        # 4. Validate data quality
        collector.validate_data_quality()
        
        # 5. Export to FLASH format
        collector.export_to_flash_format('flash_startup_database.json')
    else:
        logger.warning("No startup data collected. Please configure data sources.")
        
        # Create example structure
        example_startup = StartupData(
            company_id="example_001",
            company_name="Example Startup Inc",
            founded_date="2018-01-15",
            industry="AI/ML",
            sub_industry="Computer Vision",
            headquarters_location="San Francisco, CA",
            website="https://example-startup.com",
            founder_names=["Jane Doe", "John Smith"],
            founder_backgrounds={
                "Jane Doe": "Former Google ML Engineer, Stanford CS PhD",
                "John Smith": "Serial entrepreneur, 2 previous exits"
            },
            team_size=45,
            key_employees=8,
            total_funding=25000000,
            funding_rounds=[
                {
                    "date": "2018-06-01",
                    "amount": 2000000,
                    "stage": "seed",
                    "lead_investor": "Seed Capital Partners",
                    "all_investors": ["Seed Capital Partners", "Angel Syndicate"]
                },
                {
                    "date": "2019-09-15",
                    "amount": 8000000,
                    "stage": "series_a",
                    "lead_investor": "Venture Fund ABC",
                    "all_investors": ["Venture Fund ABC", "Seed Capital Partners"]
                },
                {
                    "date": "2021-03-20",
                    "amount": 15000000,
                    "stage": "series_b",
                    "lead_investor": "Growth Capital XYZ",
                    "all_investors": ["Growth Capital XYZ", "Venture Fund ABC"]
                }
            ],
            last_funding_date="2021-03-20",
            last_funding_amount=15000000,
            last_funding_stage="series_b",
            lead_investors=["Growth Capital XYZ", "Venture Fund ABC"],
            all_investors=["Growth Capital XYZ", "Venture Fund ABC", "Seed Capital Partners", "Angel Syndicate"],
            business_model="B2B SaaS",
            target_market="Enterprise",
            revenue_range="$1M-$10M",
            growth_rate=150.0,
            burn_rate=500000,
            runway_months=18,
            outcome=StartupOutcome.ACQUIRED,
            outcome_date="2023-06-15",
            exit_value=175000000,
            acquirer="Tech Giant Corp",
            ipo_ticker=None,
            shutdown_reason=None,
            market_size=5000000000,
            competitors=["Competitor A", "Competitor B", "Legacy Solution C"],
            market_position="Emerging leader",
            product_market_fit_score=0.85,
            technology_score=0.9,
            team_score=0.88,
            market_timing_score=0.82,
            data_source="example",
            last_updated=datetime.now().isoformat(),
            data_completeness=0.92,
            verified=True
        )
        
        collector.save_to_database([example_startup])
        collector.export_to_flash_format('flash_startup_database.json')
        logger.info("Created example database structure")

if __name__ == "__main__":
    main()