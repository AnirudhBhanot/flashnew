# Feature Mapping Status Table

## Legend
- ✅ Correctly mapped
- ⚠️ Partially mapped or wrong type/calculation
- ❌ Not collected (hardcoded/missing)
- 🔄 Name mismatch between systems

| # | Backend Feature (Registry) | Frontend Field | Transform Mapping | Status | Issue |
|---|---------------------------|----------------|-------------------|---------|--------|
| 0 | funding_stage | companyInfo.stage | ✅ | ✅ | |
| 1 | revenue_growth_rate | - | revenue_growth_rate_percent: 100 | ❌ | Hardcoded |
| 2 | team_size_full_time | people.teamSize | ✅ | ✅ | |
| 3 | total_capital_raised_usd | capital.totalFundingRaised | ✅ | ✅ | |
| 4 | annual_recurring_revenue_millions | - | - | ❌ | Not in transform |
| 5 | annual_revenue_run_rate | capital.annualRevenueRunRate | ✅ | ✅ | |
| 6 | burn_multiple | capital.ltvCacRatio | ⚠️ | ⚠️ | Wrong metric used |
| 7 | market_tam_billions | market.marketSize | tam_size_usd | 🔄 | Name/unit mismatch |
| 8 | market_growth_rate | market.marketGrowthRate | market_growth_rate_percent | 🔄 | Name mismatch |
| 9 | market_competitiveness | market.competitionLevel | competition_intensity | 🔄 | Name mismatch |
| 10 | customer_acquisition_cost | market.customerAcquisitionCost | - | ❌ | Not in transform |
| 11 | customer_lifetime_value | - | - | ❌ | Not collected |
| 12 | customer_growth_rate | - | user_growth_rate_percent: 100 | ❌ | Hardcoded |
| 13 | net_revenue_retention | - | net_dollar_retention_percent: 110 | ❌ | Hardcoded |
| 14 | average_deal_size | - | - | ❌ | Not collected |
| 15 | sales_cycle_days | - | - | ❌ | Not collected |
| 16 | international_revenue_percent | - | - | ❌ | Not collected |
| 17 | target_enterprise | - | - | ❌ | Not collected |
| 18 | product_market_fit_score | - | - | ❌ | Not collected |
| 19 | technology_score | advantage.moatStrength | tech_differentiation_score | ⚠️ | Scale mismatch |
| 20 | scalability_score | - | scalability_score: 4 | ❌ | Hardcoded |
| 21 | has_patent | advantage.hasPatents | patent_count > 0 | ⚠️ | Type conversion |
| 22 | research_development_percent | - | - | ❌ | Not collected |
| 23 | uses_ai_ml | - | - | ❌ | Not collected |
| 24 | cloud_native | - | - | ❌ | Not collected |
| 25 | mobile_first | - | - | ❌ | Not collected |
| 26 | platform_business | - | - | ❌ | Not collected |
| 27 | founder_experience_years | people.industryExperience | years_experience_avg | ⚠️ | Scale vs years |
| 28 | repeat_founder | people.previousStartups | prior_startup_experience_count | ⚠️ | Bool vs count |
| 29 | technical_founder | people.technicalFounders | - | ❌ | Type mismatch |
| 30 | employee_growth_rate | - | - | ❌ | Not collected |
| 31 | advisor_quality_score | - | board_advisor_experience_score: 3 | ❌ | Hardcoded |
| 32 | board_diversity_score | - | - | ❌ | Not collected |
| 33 | team_industry_experience | people.industryExperience | domain_expertise_years_avg | ⚠️ | Scale vs years |
| 34 | key_person_dependency | - | key_person_dependency: false | ❌ | Hardcoded |
| 35 | top_university_alumni | - | - | ❌ | Not collected |
| 36 | investor_tier_primary | - | Calculated from funding | ⚠️ | Derived |
| 37 | active_investors | - | - | ❌ | Not collected |
| 38 | cash_on_hand_months | - | - | ❌ | Not collected |
| 39 | runway_months | capital.runwayMonths | ✅ | ✅ | |
| 40 | time_to_next_funding | - | - | ❌ | Not collected |
| 41 | previous_exit | people.previousExits | prior_successful_exits_count | ⚠️ | Bool vs count |
| 42 | industry_connections | - | - | ❌ | Not collected |
| 43 | media_coverage | - | - | ❌ | Not collected |
| 44 | regulatory_risk | - | - | ❌ | Not collected |

## Summary Statistics

- ✅ **Correctly Mapped**: 5/45 (11%)
- ⚠️ **Partially/Incorrectly Mapped**: 10/45 (22%)
- ❌ **Not Collected/Hardcoded**: 26/45 (58%)
- 🔄 **Name Mismatches**: 4/45 (9%)

## Most Critical Missing Features

1. **Financial Metrics**
   - annual_recurring_revenue_millions
   - revenue_growth_rate
   - customer_lifetime_value
   - average_deal_size

2. **Product Metrics**
   - product_market_fit_score
   - research_development_percent
   - All product feature flags (AI/ML, cloud, mobile, platform)

3. **Market Metrics**
   - sales_cycle_days
   - international_revenue_percent
   - target_enterprise
   - Proper CAC usage

4. **Team Metrics**
   - employee_growth_rate
   - board_diversity_score
   - active_investors
   - industry_connections

5. **Risk Metrics**
   - time_to_next_funding
   - media_coverage
   - regulatory_risk