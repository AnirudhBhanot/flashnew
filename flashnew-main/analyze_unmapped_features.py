#!/usr/bin/env python3
"""Analyze which frontend features are not mapped to backend features"""

# Frontend features collected (43 total from DataCollectionCAMP.tsx)
frontend_features = {
    # Capital features (10)
    'funding_stage',
    'total_capital_raised_usd',
    'cash_on_hand_usd',
    'monthly_burn_usd',
    'annual_revenue_run_rate',
    'revenue_growth_rate_percent',
    'gross_margin_percent',
    'ltv_cac_ratio',
    'investor_tier_primary',
    'has_debt',
    
    # Advantage features (11)
    'patent_count',
    'network_effects_present',
    'has_data_moat',
    'regulatory_advantage_present',
    'tech_differentiation_score',
    'switching_cost_score',
    'brand_strength_score',
    'scalability_score',
    'product_stage',
    'product_retention_30d',
    'product_retention_90d',
    
    # Market features (12)
    'sector',
    'tam_size_usd',
    'sam_size_usd',
    'som_size_usd',
    'market_growth_rate_percent',
    'customer_count',
    'customer_concentration_percent',
    'user_growth_rate_percent',
    'net_dollar_retention_percent',
    'competition_intensity',
    'competitors_named_count',
    'dau_mau_ratio',
    
    # People features (10)
    'founders_count',
    'team_size_full_time',
    'years_experience_avg',
    'domain_expertise_years_avg',
    'prior_startup_experience_count',
    'prior_successful_exits_count',
    'board_advisor_experience_score',
    'advisors_count',
    'team_diversity_percent',
    'key_person_dependency'
}

# Backend features (45 total from feature_registry.py)
backend_features = {
    'funding_stage',
    'total_capital_raised_usd',
    'annual_recurring_revenue_millions',
    'annual_revenue_run_rate',
    'burn_multiple',
    'revenue_growth_rate',
    'team_size_full_time',
    'market_tam_billions',
    'market_growth_rate',
    'market_competitiveness',
    'customer_acquisition_cost',
    'customer_lifetime_value',
    'customer_growth_rate',
    'net_revenue_retention',
    'average_deal_size',
    'sales_cycle_days',
    'international_revenue_percent',
    'target_enterprise',
    'product_market_fit_score',
    'technology_score',
    'scalability_score',
    'has_patent',
    'research_development_percent',
    'uses_ai_ml',
    'cloud_native',
    'mobile_first',
    'platform_business',
    'founder_experience_years',
    'repeat_founder',
    'technical_founder',
    'employee_growth_rate',
    'advisor_quality_score',
    'board_diversity_score',
    'team_industry_experience',
    'key_person_dependency',
    'top_university_alumni',
    'investor_tier_primary',
    'active_investors',
    'cash_on_hand_months',
    'runway_months',
    'time_to_next_funding',
    'previous_exit',
    'industry_connections',
    'media_coverage',
    'regulatory_risk'
}

# Find unmapped frontend features
unmapped_features = frontend_features - backend_features

# Create mapping for similar features with different names
feature_mapping = {
    # Frontend -> Backend mapping
    'revenue_growth_rate_percent': 'revenue_growth_rate',
    'market_growth_rate_percent': 'market_growth_rate',
    'net_dollar_retention_percent': 'net_revenue_retention',
    'user_growth_rate_percent': 'customer_growth_rate',
    'board_advisor_experience_score': 'advisor_quality_score',
    'patent_count': 'has_patent',  # Different representation (count vs boolean)
    'competition_intensity': 'market_competitiveness',
}

# Apply mapping to find truly unmapped features
truly_unmapped = []
for feature in unmapped_features:
    if feature not in feature_mapping:
        truly_unmapped.append(feature)
    else:
        print(f"Frontend '{feature}' maps to backend '{feature_mapping[feature]}'")

print("\n=== FRONTEND FEATURES NOT MAPPED TO BACKEND ===")
print(f"\nTotal frontend features: {len(frontend_features)}")
print(f"Total backend features: {len(backend_features)}")
print(f"Unmapped features: {len(truly_unmapped)}")

print("\n--- Unmapped Frontend Features ---")
for i, feature in enumerate(sorted(truly_unmapped), 1):
    print(f"{i}. {feature}")

# Analyze what each unmapped feature captures
feature_descriptions = {
    'cash_on_hand_usd': "Current bank balance and liquid assets in USD - captures absolute cash position",
    'monthly_burn_usd': "Average monthly cash expenditure in USD - captures burn rate",
    'gross_margin_percent': "(Revenue - COGS) / Revenue × 100 - captures unit economics",
    'ltv_cac_ratio': "Customer lifetime value ÷ Customer acquisition cost - key SaaS metric",
    'has_debt': "Whether company has venture debt or loans - captures financing structure",
    'network_effects_present': "Whether value increases with more users - captures growth dynamics",
    'has_data_moat': "Whether company has proprietary data advantage - competitive advantage",
    'regulatory_advantage_present': "Licenses or regulatory barriers - competitive moat",
    'tech_differentiation_score': "1-5 score for technology uniqueness - innovation level",
    'switching_cost_score': "1-5 score for customer stickiness - retention indicator",
    'brand_strength_score': "1-5 score for brand recognition - market position",
    'product_stage': "MVP/Beta/GA/Mature - product maturity level",
    'product_retention_30d': "% of users active after 30 days - engagement metric",
    'product_retention_90d': "% of users active after 90 days - long-term engagement",
    'sector': "Industry vertical (SaaS, Fintech, etc.) - market segment",
    'tam_size_usd': "Total addressable market in USD - market opportunity",
    'sam_size_usd': "Serviceable addressable market in USD - realistic market",
    'som_size_usd': "Serviceable obtainable market in USD - achievable market",
    'customer_count': "Total number of paying customers - traction metric",
    'customer_concentration_percent': "% revenue from top customer - risk metric",
    'competitors_named_count': "Number of direct competitors - competitive landscape",
    'dau_mau_ratio': "Daily active users ÷ Monthly active users - engagement depth",
    'founders_count': "Number of founding team members - team structure",
    'years_experience_avg': "Average professional experience of team - team quality",
    'domain_expertise_years_avg': "Years in specific industry - domain knowledge",
    'prior_startup_experience_count': "Number of previous startups founded - entrepreneurial experience",
    'prior_successful_exits_count': "Previous successful acquisitions or IPOs - track record",
    'advisors_count': "Total advisors and mentors - support network",
    'team_diversity_percent': "% of team from underrepresented groups - diversity metric"
}

print("\n--- Detailed Analysis of Unmapped Features ---")
for feature in sorted(truly_unmapped):
    desc = feature_descriptions.get(feature, "No description available")
    print(f"\n{feature}:")
    print(f"  Purpose: {desc}")

# Find backend features not collected by frontend
backend_only = backend_features - frontend_features
print("\n\n=== BACKEND FEATURES NOT COLLECTED BY FRONTEND ===")
print(f"Count: {len(backend_only)}")
for i, feature in enumerate(sorted(backend_only), 1):
    print(f"{i}. {feature}")