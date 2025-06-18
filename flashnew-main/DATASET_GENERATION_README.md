# FLASH 100K Startup Dataset Generation System

## Overview

This system generates a comprehensive 100,000 startup dataset with realistic data patterns based on real company templates. The dataset includes all 45 FLASH features with logical consistency and realistic success/failure patterns.

## Key Components

### 1. `generate_100k_dataset.py`
The main dataset generator that creates realistic startup data with:
- **Realistic distributions** based on industry research
- **Stage-based success rates** (Pre-Seed: 10%, Seed: 15%, Series A: 25%, etc.)
- **Logical consistency** between related features
- **Industry-specific patterns** for 9 different sectors
- **Comprehensive feature coverage** for all 45 FLASH attributes

### 2. Generated Features (45 total)

#### Financial Metrics (9 features)
- `total_capital_raised_usd`: Total funding raised
- `cash_on_hand_usd`: Current cash reserves
- `monthly_burn_usd`: Monthly cash burn rate
- `runway_months`: Months of runway remaining
- `annual_revenue_run_rate`: Annualized revenue
- `revenue_growth_rate_percent`: Year-over-year growth
- `gross_margin_percent`: Gross profit margin
- `burn_multiple`: Burn rate vs revenue growth efficiency
- `ltv_cac_ratio`: Customer lifetime value to acquisition cost

#### Market Metrics (6 features)
- `tam_size_usd`: Total addressable market
- `sam_size_usd`: Serviceable addressable market
- `som_size_usd`: Serviceable obtainable market
- `market_growth_rate_percent`: Market growth rate
- `competition_intensity`: Competition level (1-5 scale)
- `competitors_named_count`: Number of direct competitors

#### Product Metrics (16 features)
- `customer_count`: Total customers
- `customer_concentration_percent`: Revenue concentration
- `user_growth_rate_percent`: User growth rate
- `net_dollar_retention_percent`: NDR metric
- `product_retention_30d`: 30-day retention
- `product_retention_90d`: 90-day retention
- `dau_mau_ratio`: Daily to monthly active users
- `tech_differentiation_score`: Technical moat (1-5)
- `switching_cost_score`: Customer lock-in (1-5)
- `brand_strength_score`: Brand value (1-5)
- `scalability_score`: Growth potential (0-1)
- `patent_count`: Number of patents
- `network_effects_present`: Boolean network effects
- `has_data_moat`: Boolean data advantage
- `regulatory_advantage_present`: Boolean regulatory moat
- `product_stage`: MVP/Beta/Early Traction/Growth/GA

#### Team Metrics (11 features)
- `founders_count`: Number of founders
- `team_size_full_time`: Full-time employees
- `years_experience_avg`: Average years of experience
- `domain_expertise_years_avg`: Domain-specific experience
- `prior_startup_experience_count`: Previous startups
- `prior_successful_exits_count`: Successful exits
- `board_advisor_experience_score`: Advisor quality (1-5)
- `advisors_count`: Number of advisors
- `team_diversity_percent`: Team diversity percentage
- `key_person_dependency`: Boolean key person risk
- `has_debt`: Boolean debt financing

#### Other Features (3 features)
- `funding_stage`: Pre-Seed/Seed/Series A/B/C+
- `sector`: Industry category
- `investor_tier_primary`: Tier1/Tier2/Tier3/Angel

## Dataset Characteristics

### Success Rate Distribution
- **Overall**: 19.11% success rate
- **By Stage**:
  - Pre-Seed: 10.2%
  - Seed: 15.1%
  - Series A: 25.1%
  - Series B: 35.2%
  - Series C+: 44.6%

### Industry Distribution
- SaaS: 25%
- E-commerce: 15%
- FinTech: 12%
- HealthTech: 10%
- AI/ML: 8%
- EdTech: 7%
- Gaming: 5%
- Marketplace: 5%
- Other: 13%

### Key Differentiators (Success vs Failure)
- **Revenue**: Successful companies have ~84x higher revenue
- **Growth Rate**: 151% vs 20% average growth
- **Burn Multiple**: 4.1 vs 173 (lower is better)
- **LTV/CAC**: 3.5 vs 1.25
- **Retention**: 75% vs 29% (30-day)
- **Team Size**: 144 vs 27 employees

## Usage

### Generate the Dataset
```bash
python generate_100k_dataset.py
```

This creates:
- `generated_100k_dataset.csv`: Full 100k dataset (70MB)
- `generated_sample_1000.csv`: 1000-record sample for inspection

### Analyze the Dataset
```bash
python analyze_generated_dataset.py
```

This produces:
- `dataset_analysis.png`: Visual analysis of distributions
- `dataset_statistics.txt`: Detailed statistical report

### Train Models
```bash
python example_training_usage.py
```

Demonstrates:
- Data preprocessing
- Feature encoding
- Model training (XGBoost example)
- Performance evaluation
- Feature importance analysis

## Logical Constraints

The generator ensures realistic relationships:
1. **Financial Logic**: Failed companies have lower revenue, higher burn
2. **Market Logic**: TAM ≥ SAM ≥ SOM
3. **Retention Logic**: 30-day retention ≥ 90-day retention
4. **Stage Logic**: Later stages have larger teams, more revenue
5. **Success Logic**: Successful companies have better metrics across the board

## Customization

Modify distributions in `StartupDataGenerator.setup_distributions()`:
- Adjust success rates by stage
- Change industry weights
- Modify metric ranges
- Add new correlations

## Output Format

The dataset matches the 45-feature FLASH specification with:
- 50 total columns (45 features + metadata)
- Consistent data types
- No missing values
- Realistic value ranges
- Logical relationships preserved

## Performance

- Generation time: ~30 seconds for 100k records
- Memory usage: ~71MB in memory, ~61MB on disk
- Scalable to millions of records