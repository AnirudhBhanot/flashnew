"""
Fixed Feature Configuration for FLASH
Defines the canonical 45 features in the EXACT order they appear in the dataset
"""

# All 45 features in the exact order from the dataset
ALL_FEATURES = [
    'funding_stage',
    'total_capital_raised_usd',
    'cash_on_hand_usd',
    'monthly_burn_usd',
    'runway_months',
    'annual_revenue_run_rate',
    'revenue_growth_rate_percent',
    'gross_margin_percent',
    'burn_multiple',
    'ltv_cac_ratio',
    'investor_tier_primary',
    'has_debt',
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
]

# CAMP Framework Feature Groups (reorganized to match dataset order)
CAPITAL_FEATURES = [
    'funding_stage',
    'total_capital_raised_usd',
    'cash_on_hand_usd', 
    'monthly_burn_usd',
    'runway_months',
    'annual_revenue_run_rate',
    'revenue_growth_rate_percent',
    'gross_margin_percent',
    'burn_multiple',
    'ltv_cac_ratio',
    'investor_tier_primary',
    'has_debt'
]

ADVANTAGE_FEATURES = [
    'patent_count',
    'network_effects_present',
    'has_data_moat',
    'regulatory_advantage_present',
    'tech_differentiation_score',
    'switching_cost_score',
    'brand_strength_score',
    'scalability_score'
]

PRODUCT_FEATURES = [
    'product_stage',
    'product_retention_30d',
    'product_retention_90d',
    'dau_mau_ratio'
]

MARKET_FEATURES = [
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
    'competitors_named_count'
]

PEOPLE_FEATURES = [
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
]

# Feature type mapping
CATEGORICAL_FEATURES = [
    'funding_stage',
    'investor_tier_primary',
    'product_stage',
    'sector'
]

BOOLEAN_FEATURES = [
    'has_debt',
    'network_effects_present',
    'has_data_moat',
    'regulatory_advantage_present',
    'key_person_dependency'
]

NUMERIC_FEATURES = [f for f in ALL_FEATURES if f not in CATEGORICAL_FEATURES + BOOLEAN_FEATURES]

# Feature ranges for validation
FEATURE_RANGES = {
    # Scores (1-5 scale)
    'tech_differentiation_score': (1, 5),
    'switching_cost_score': (1, 5),
    'brand_strength_score': (1, 5),
    'scalability_score': (1, 5),
    'board_advisor_experience_score': (1, 5),
    'competition_intensity': (1, 5),
    
    # Percentages (0-100)
    'gross_margin_percent': (0, 100),
    'market_growth_rate_percent': (-50, 500),
    'revenue_growth_rate_percent': (-100, 1000),
    'user_growth_rate_percent': (-100, 10000),
    'net_dollar_retention_percent': (0, 500),
    'customer_concentration_percent': (0, 100),
    'team_diversity_percent': (0, 100),
    
    # Ratios
    'burn_multiple': (0, 20),
    'ltv_cac_ratio': (0, 10),
    'product_retention_30d': (0, 1),
    'product_retention_90d': (0, 1),
    'dau_mau_ratio': (0, 1),
    
    # Counts
    'patent_count': (0, 1000),
    'customer_count': (0, 1000000000),
    'competitors_named_count': (0, 1000),
    'founders_count': (1, 10),
    'team_size_full_time': (0, 100000),
    'prior_startup_experience_count': (0, 100),
    'prior_successful_exits_count': (0, 50),
    'advisors_count': (0, 1000),
    
    # Years
    'years_experience_avg': (0, 50),
    'domain_expertise_years_avg': (0, 50),
    'runway_months': (0, 120),
    
    # USD amounts
    'total_capital_raised_usd': (0, 1e12),
    'cash_on_hand_usd': (0, 1e12),
    'monthly_burn_usd': (0, 1e9),
    'tam_size_usd': (0, 1e12),
    'sam_size_usd': (0, 1e12),
    'som_size_usd': (0, 1e12),
    'annual_revenue_run_rate': (0, 1e12)
}

# Feature descriptions for API documentation
FEATURE_DESCRIPTIONS = {
    # Capital Features
    'funding_stage': 'Current funding stage',
    'total_capital_raised_usd': 'Total capital raised to date in USD',
    'cash_on_hand_usd': 'Current cash reserves in USD',
    'monthly_burn_usd': 'Monthly cash burn rate in USD',
    'runway_months': 'Months of runway at current burn rate',
    'annual_revenue_run_rate': 'Annual revenue run rate in USD',
    'revenue_growth_rate_percent': 'Revenue growth rate percentage',
    'gross_margin_percent': 'Gross margin percentage',
    'burn_multiple': 'Net burn divided by net new ARR',
    'ltv_cac_ratio': 'Lifetime value to customer acquisition cost ratio',
    'investor_tier_primary': 'Quality tier of lead investor (Tier1, Tier2, etc.)',
    'has_debt': 'Whether company has debt financing',
    
    # Advantage Features
    'patent_count': 'Number of patents filed/granted',
    'network_effects_present': 'Whether product has network effects',
    'has_data_moat': 'Whether company has proprietary data advantage',
    'regulatory_advantage_present': 'Whether company has regulatory advantages',
    'tech_differentiation_score': 'Technology differentiation score (1-5)',
    'switching_cost_score': 'Customer switching cost score (1-5)',
    'brand_strength_score': 'Brand strength score (1-5)',
    'scalability_score': 'Business scalability score (1-5)',
    
    # Product Features
    'product_stage': 'Product development stage',
    'product_retention_30d': '30-day product retention rate',
    'product_retention_90d': '90-day product retention rate',
    'dau_mau_ratio': 'Daily to monthly active user ratio',
    
    # Market Features
    'sector': 'Industry sector',
    'tam_size_usd': 'Total addressable market in USD',
    'sam_size_usd': 'Serviceable addressable market in USD',
    'som_size_usd': 'Serviceable obtainable market in USD',
    'market_growth_rate_percent': 'Annual market growth rate percentage',
    'customer_count': 'Number of customers',
    'customer_concentration_percent': 'Revenue concentration in top customers',
    'user_growth_rate_percent': 'Monthly user growth rate percentage',
    'net_dollar_retention_percent': 'Net dollar retention rate',
    'competition_intensity': 'Competition intensity score (1-5)',
    'competitors_named_count': 'Number of direct competitors',
    
    # People Features
    'founders_count': 'Number of founders',
    'team_size_full_time': 'Full-time employee count',
    'years_experience_avg': 'Average years of professional experience',
    'domain_expertise_years_avg': 'Average years in the domain',
    'prior_startup_experience_count': 'Number of prior startups',
    'prior_successful_exits_count': 'Number of successful exits',
    'board_advisor_experience_score': 'Board/advisor quality score (1-5)',
    'advisors_count': 'Number of advisors',
    'team_diversity_percent': 'Team diversity percentage',
    'key_person_dependency': 'Whether company depends on key person'
}

# CAMP score calculation weights
CAMP_WEIGHTS = {
    'capital': 0.25,
    'advantage': 0.25,
    'market': 0.25,
    'people': 0.25
}

# Stage-specific weight adjustments
STAGE_WEIGHTS = {
    'pre_seed': {'people': 0.4, 'advantage': 0.3, 'market': 0.2, 'capital': 0.1},
    'seed': {'people': 0.3, 'advantage': 0.3, 'market': 0.25, 'capital': 0.15},
    'series_a': {'market': 0.3, 'advantage': 0.25, 'capital': 0.25, 'people': 0.2},
    'series_b': {'market': 0.35, 'capital': 0.3, 'advantage': 0.2, 'people': 0.15},
    'series_c': {'capital': 0.4, 'market': 0.3, 'advantage': 0.2, 'people': 0.1}
}

def validate_features(data: dict) -> list:
    """Validate feature values and return list of errors"""
    errors = []
    
    # Check required features
    missing = [f for f in ALL_FEATURES if f not in data]
    if missing:
        errors.append(f"Missing features: {', '.join(missing)}")
    
    # Check feature ranges
    for feature, (min_val, max_val) in FEATURE_RANGES.items():
        if feature in data:
            value = data[feature]
            if isinstance(value, (int, float)) and (value < min_val or value > max_val):
                errors.append(f"{feature} must be between {min_val} and {max_val}, got {value}")
    
    # Check boolean features
    for feature in BOOLEAN_FEATURES:
        if feature in data and data[feature] not in [0, 1, True, False]:
            errors.append(f"{feature} must be boolean (0/1 or True/False)")
    
    return errors

def get_feature_groups():
    """Return feature groups for easy access"""
    return {
        'capital': CAPITAL_FEATURES,
        'advantage': ADVANTAGE_FEATURES,
        'market': MARKET_FEATURES,
        'people': PEOPLE_FEATURES,
        'product': PRODUCT_FEATURES
    }

def get_feature_order_mapping():
    """Get mapping from feature name to dataset column index"""
    return {feature: idx for idx, feature in enumerate(ALL_FEATURES)}

# Export count verification
assert len(ALL_FEATURES) == 45, f"Expected 45 features, got {len(ALL_FEATURES)}"
assert len(set(ALL_FEATURES)) == 45, "Duplicate features detected"

# Verify grouping completeness
all_grouped = (
    set(CAPITAL_FEATURES) | 
    set(ADVANTAGE_FEATURES) | 
    set(MARKET_FEATURES) | 
    set(PEOPLE_FEATURES) | 
    set(PRODUCT_FEATURES)
)
assert all_grouped == set(ALL_FEATURES), "Feature groups don't cover all features"