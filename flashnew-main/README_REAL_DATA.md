# Real Startup Database Builder for FLASH

This system provides a comprehensive framework for building a real startup database with verified outcomes for the FLASH prediction platform.

## Overview

The system consists of four main components:

1. **build_real_startup_database.py** - Core database builder with data structures and collection framework
2. **data_source_integrations.py** - Integration methods for various legitimate data sources
3. **data_validation_pipeline.py** - Data quality validation and verification system
4. **collect_real_data_example.py** - Practical example that collects real startup data

## Data Structure

The system captures comprehensive startup data including:

- Basic information (name, founding date, location, industry)
- Founder and team data
- Complete funding history
- Business metrics (revenue, growth, burn rate)
- Verified outcomes (IPO, acquisition, shutdown, active)
- FLASH-specific scores (PMF, technology, team, timing)

## Legitimate Data Sources

### Free Sources
1. **SEC EDGAR** - IPO data, public company filings
2. **Yahoo Finance** - Public company metrics, IPO performance
3. **GitHub API** - Tech stack, team activity
4. **News RSS Feeds** - Exit announcements, funding news
5. **USPTO** - Patent and trademark data

### Institutional Sources (Paid)
1. **Crunchbase API** ($500-5000/month) - Comprehensive startup data
2. **PitchBook** ($15k-40k/year) - Detailed VC and exit data
3. **CB Insights** ($5k-50k/year) - Market intelligence
4. **AngelList** - Early-stage startup data

## Getting Started

### 1. Install Dependencies
```bash
pip install pandas sqlite3 requests yfinance beautifulsoup4 feedparser fuzzywuzzy
```

### 2. Run Example Data Collection
```bash
python collect_real_data_example.py
```

This will collect real data on:
- Recent IPOs (Airbnb, DoorDash, Coinbase, etc.)
- Major acquisitions (Slack, GitHub, LinkedIn, etc.)
- Unicorn companies (SpaceX, Stripe, Canva, etc.)
- Failed startups (FTX, Theranos, WeWork, etc.)

### 3. Build Full Database
```bash
python build_real_startup_database.py
```

### 4. Validate Data Quality
```bash
python data_validation_pipeline.py
```

## Scaling to 100k Companies

To build a 100k company database:

### Phase 1: Public Companies (10k records)
- Scrape all US IPOs from SEC EDGAR (2000-2024)
- Collect international IPOs from major exchanges
- Complete financial and outcome data

### Phase 2: Unicorns & Late Stage (2k records)
- CB Insights Unicorn List
- PitchBook late-stage companies
- Forbes Next Billion-Dollar Startups

### Phase 3: Acquisitions (20k records)
- M&A databases
- Tech news archives
- Company press releases

### Phase 4: Funded Startups (50k records)
- Crunchbase/PitchBook exports
- AngelList profiles
- Accelerator portfolios (YC, Techstars, etc.)
- Government startup databases

### Phase 5: Failed Startups (20k records)
- Failure post-mortems
- Bankruptcy filings
- Domain expiration tracking

## Data Quality Metrics

The system tracks:
- **Completeness**: Percentage of fields filled
- **Verification**: Cross-referenced with multiple sources
- **Freshness**: Last update timestamp
- **Accuracy**: Validation against known patterns

## Output Formats

1. **SQLite Database** - Structured storage with indexes
2. **JSON Export** - FLASH-compatible format
3. **CSV Export** - For analysis and manual review

## Best Practices

1. **Respect Rate Limits** - Add delays between API calls
2. **Verify Outcomes** - Cross-reference exits with multiple sources
3. **Update Regularly** - Set up scheduled updates for active companies
4. **Document Sources** - Track where each data point came from
5. **Handle Duplicates** - Use fuzzy matching to detect duplicates

## Example Output

```json
{
  "company_name": "Airbnb",
  "ticker": "ABNB",
  "founded_date": "2008-08-01",
  "outcome": "ipo",
  "outcome_date": "2020-12-10",
  "ipo_price": 68.0,
  "current_price": 145.32,
  "market_cap": 91283746816,
  "total_funding": 6400000000,
  "industry": "Travel Technology",
  "headquarters_location": "San Francisco, CA",
  "verified": true
}
```

## Legal and Ethical Considerations

- Only use publicly available data
- Respect robots.txt and terms of service
- Don't scrape personal information
- Attribute data sources appropriately
- Consider GDPR and privacy regulations

## Next Steps

1. Set up automated collection pipelines
2. Implement continuous verification
3. Add more data sources
4. Build prediction model training pipeline
5. Create data quality dashboards

## Support

For questions about data sources or collection methods, consult:
- SEC EDGAR documentation
- Yahoo Finance API guides
- Crunchbase API documentation
- PitchBook data dictionary