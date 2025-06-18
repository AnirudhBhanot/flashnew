#!/usr/bin/env python3
"""
Strategy to scale to 100k real companies with verified outcomes
This outlines how to build a complete real startup database
"""

import json
from datetime import datetime

def get_data_collection_strategy():
    """Define strategy to reach 100k companies with real data"""
    
    strategy = {
        "target": 100000,
        "timeline": "2-3 months",
        "data_sources": [
            {
                "source": "SEC EDGAR Database",
                "type": "free",
                "companies": 15000,
                "description": "All US public companies (IPOs)",
                "data_quality": "excellent",
                "outcomes": ["ipo"],
                "api": "https://www.sec.gov/edgar/searchedgar/companysearch.html",
                "method": "automated_scraping"
            },
            {
                "source": "Crunchbase Basic (Free Tier)",
                "type": "free_limited",
                "companies": 5000,
                "description": "Basic company info, funding rounds",
                "data_quality": "good",
                "outcomes": ["active", "acquired", "ipo"],
                "method": "manual_export"
            },
            {
                "source": "AngelList Public Data",
                "type": "free",
                "companies": 10000,
                "description": "Startup profiles, funding info",
                "data_quality": "good",
                "outcomes": ["active", "acquired", "shutdown"],
                "api": "public_profiles",
                "method": "web_scraping"
            },
            {
                "source": "PitchBook (Paid)",
                "type": "paid",
                "companies": 30000,
                "description": "Comprehensive startup data",
                "data_quality": "excellent",
                "cost": "$2000/month",
                "outcomes": ["all"],
                "method": "api_access"
            },
            {
                "source": "CB Insights",
                "type": "paid",
                "companies": 20000,
                "description": "Unicorns, exits, failures",
                "data_quality": "excellent", 
                "cost": "$1500/month",
                "outcomes": ["all"],
                "method": "data_export"
            },
            {
                "source": "Dealroom.co",
                "type": "freemium",
                "companies": 10000,
                "description": "European startup ecosystem",
                "data_quality": "very_good",
                "outcomes": ["all"],
                "method": "api_limited"
            },
            {
                "source": "Government Databases",
                "type": "free",
                "companies": 5000,
                "description": "SBA, USPTO, state records",
                "data_quality": "good",
                "outcomes": ["active", "shutdown"],
                "method": "bulk_download"
            },
            {
                "source": "News & Press Releases",
                "type": "free",
                "companies": 5000,
                "description": "TechCrunch, Reuters, Bloomberg",
                "data_quality": "verified",
                "outcomes": ["acquired", "shutdown", "ipo"],
                "method": "news_api_parsing"
            }
        ],
        "outcome_distribution": {
            "ipo": 2000,          # ~2% (realistic)
            "acquired": 15000,    # ~15% (realistic)
            "active": 60000,      # ~60% (still operating)
            "shutdown": 20000,    # ~20% (failed)
            "pivoted": 3000       # ~3% (major pivot)
        },
        "collection_phases": [
            {
                "phase": 1,
                "name": "Public Companies",
                "duration": "1 week",
                "sources": ["SEC EDGAR"],
                "expected_companies": 15000,
                "automation": "high"
            },
            {
                "phase": 2,
                "name": "Known Exits",
                "duration": "2 weeks",
                "sources": ["News APIs", "M&A databases"],
                "expected_companies": 10000,
                "automation": "medium"
            },
            {
                "phase": 3,
                "name": "Funded Startups",
                "duration": "1 month",
                "sources": ["Crunchbase", "AngelList", "PitchBook"],
                "expected_companies": 50000,
                "automation": "high"
            },
            {
                "phase": 4,
                "name": "Failed Startups",
                "duration": "2 weeks",
                "sources": ["Shutdown databases", "News", "Forums"],
                "expected_companies": 20000,
                "automation": "low"
            },
            {
                "phase": 5,
                "name": "International",
                "duration": "2 weeks",
                "sources": ["Dealroom", "Regional databases"],
                "expected_companies": 5000,
                "automation": "medium"
            }
        ]
    }
    
    return strategy

def calculate_budget():
    """Calculate budget for data collection"""
    
    budget = {
        "one_time_costs": {
            "developer_time": {
                "hours": 200,
                "rate": 150,
                "total": 30000
            },
            "data_cleaning_tools": 500,
            "server_costs": 1000
        },
        "monthly_costs": {
            "pitchbook": 2000,
            "cb_insights": 1500,
            "news_apis": 200,
            "cloud_storage": 100,
            "total_monthly": 3800
        },
        "total_3_months": 11400 + 31500,  # monthly * 3 + one_time
        "cost_per_company": 42900 / 100000  # $0.43 per company
    }
    
    return budget

def get_data_schema():
    """Define the complete data schema for real companies"""
    
    schema = {
        "required_fields": [
            "company_name",
            "founded_year", 
            "industry",
            "outcome",  # ipo/acquired/active/failed
            "outcome_date",
            "success_label",  # 1/0/null
            "total_funding_amount",
            "last_funding_stage",
            "team_size",
            "headquarters_location"
        ],
        "financial_metrics": [
            "revenue_growth_rate",
            "gross_margin",
            "burn_multiple",
            "runway_months",
            "current_arr",
            "ltv_cac_ratio"
        ],
        "verification_fields": [
            "data_source",
            "verification_date",
            "confidence_score",
            "outcome_verified",
            "financial_data_available"
        ]
    }
    
    return schema

def create_collection_pipeline():
    """Create the actual data collection pipeline"""
    
    pipeline = """
# Real Startup Data Collection Pipeline

## Phase 1: SEC EDGAR (Week 1)
```python
# 1. Download all IPO S-1 filings
# 2. Parse financial data
# 3. Match with current stock data
# 4. Verify IPO success/failure
```

## Phase 2: M&A Databases (Week 2-3)
```python
# 1. Scrape Crunchbase acquisitions
# 2. Cross-reference with news
# 3. Get acquisition prices
# 4. Verify acquirer details
```

## Phase 3: Failed Startups (Week 4-5)
```python
# 1. Failory database
# 2. Startup post-mortems
# 3. Bankruptcy filings
# 4. News archives
```

## Phase 4: Active Unicorns (Week 6-7)
```python
# 1. CB Insights unicorn list
# 2. PitchBook private companies
# 3. Recent funding rounds
# 4. Valuation data
```

## Phase 5: Data Enrichment (Week 8)
```python
# 1. Add LinkedIn employee counts
# 2. Add patent data from USPTO
# 3. Add web traffic from SimilarWeb
# 4. Add app ratings where applicable
```
"""
    
    return pipeline

def save_strategy():
    """Save the complete strategy"""
    
    print("📊 100K Real Startup Database Strategy")
    print("=" * 60)
    
    strategy = get_data_collection_strategy()
    budget = calculate_budget()
    schema = get_data_schema()
    
    # Save strategy
    with open('100k_strategy.json', 'w') as f:
        json.dump({
            "strategy": strategy,
            "budget": budget,
            "schema": schema,
            "created_date": datetime.now().isoformat()
        }, f, indent=2)
    
    print(f"\n✅ Strategy saved to 100k_strategy.json")
    
    # Print summary
    print(f"\n🎯 Target: {strategy['target']:,} companies")
    print(f"⏱️  Timeline: {strategy['timeline']}")
    print(f"💰 Total Budget: ${budget['total_3_months']:,}")
    print(f"📊 Cost per company: ${budget['cost_per_company']:.2f}")
    
    print("\n📈 Outcome Distribution:")
    for outcome, count in strategy['outcome_distribution'].items():
        percentage = (count / strategy['target']) * 100
        print(f"  {outcome}: {count:,} ({percentage:.1f}%)")
    
    print("\n🔄 Collection Phases:")
    for phase in strategy['collection_phases']:
        print(f"  Phase {phase['phase']}: {phase['name']}")
        print(f"    Duration: {phase['duration']}")
        print(f"    Expected: {phase['expected_companies']:,} companies")
    
    print("\n📝 Next Steps:")
    print("1. Start with SEC EDGAR (free, high quality)")
    print("2. Build scraping infrastructure")
    print("3. Create data validation pipeline")
    print("4. Begin with 1,000 company pilot")
    print("5. Scale to 100k over 3 months")

if __name__ == "__main__":
    save_strategy()
    
    print("\n" + "="*60)
    print("🚀 We now have:")
    print("  1. Initial real data (11 companies) ✅")
    print("  2. Complete 100k collection strategy ✅")
    print("  3. Budget and timeline ✅")
    print("  4. Data sources identified ✅")
    print("\n🎯 Ready to build REAL predictive models!")