"""
Feature name mapping between dataset and registry
Maps the actual column names in the dataset to the canonical names in the registry
"""

# Mapping from dataset column names to registry feature names
DATASET_TO_REGISTRY_MAPPING = {
    # Dataset name -> Registry name
    
    # Capital features
    'funding_stage': 'funding_stage',
    'total_capital_raised_usd': 'total_capital_raised_usd',
    'cash_on_hand_usd': 'cash_on_hand_months',  # Note: might need conversion
    'monthly_burn_usd': 'burn_multiple',  # Note: might need calculation
    'runway_months': 'runway_months',
    'annual_revenue_run_rate': 'annual_revenue_run_rate',
    'revenue_growth_rate_percent': 'revenue_growth_rate',
    'gross_margin_percent': 'annual_recurring_revenue_millions',  # Approximation
    'burn_multiple': 'burn_multiple',
    'ltv_cac_ratio': 'customer_lifetime_value',  # Will need to extract
    'investor_tier_primary': 'investor_tier_primary',
    'has_debt': 'active_investors',  # Approximation
    'time_to_next_funding': 'time_to_next_funding',
    
    # Market features
    'market_size_billion': 'market_tam_billions',
    'market_growth_rate_percent': 'market_growth_rate',
    'competition_intensity': 'market_competitiveness',
    'competitors_named_count': 'market_competitiveness',  # Will map to score
    'customer_count': 'customer_growth_rate',  # Approximation
    'customer_concentration_percent': 'customer_acquisition_cost',  # Approximation
    'user_growth_rate_percent': 'customer_growth_rate',
    'net_dollar_retention_percent': 'net_revenue_retention',
    'dau_mau_ratio': 'average_deal_size',  # Approximation
    'sales_efficiency': 'sales_cycle_days',  # Approximation
    'international_revenue_percent': 'international_revenue_percent',
    'target_enterprise': 'target_enterprise',
    'media_coverage': 'media_coverage',
    'regulatory_risk': 'regulatory_risk',
    
    # Product/Advantage features
    'product_market_fit_score': 'product_market_fit_score',
    'tech_differentiation_score': 'technology_score',
    'scalability_score': 'scalability_score',
    'patent_count': 'has_patent',  # Will convert to boolean
    'network_effects_present': 'platform_business',
    'has_data_moat': 'uses_ai_ml',  # Approximation
    'regulatory_advantage_present': 'cloud_native',  # Approximation
    'research_development_percent': 'research_development_percent',
    'mobile_first': 'mobile_first',
    
    # People features
    'team_size_full_time': 'team_size_full_time',
    'founders_count': 'founder_experience_years',  # Approximation
    'years_experience_avg': 'founder_experience_years',
    'domain_expertise_years_avg': 'team_industry_experience',
    'prior_startup_experience_count': 'repeat_founder',  # Will convert to boolean
    'prior_successful_exits_count': 'previous_exit',  # Will convert to boolean
    'technical_founder': 'technical_founder',
    'board_advisor_experience_score': 'advisor_quality_score',
    'advisors_count': 'board_diversity_score',  # Approximation
    'team_diversity_percent': 'board_diversity_score',
    'key_person_dependency': 'key_person_dependency',
    'employee_growth_rate': 'employee_growth_rate',
    'top_university_alumni': 'top_university_alumni',
    'industry_connections': 'industry_connections'
}


def map_dataset_to_registry(df):
    """
    Map dataset columns to registry feature names
    Returns a dataframe with registry-compatible column names
    """
    import pandas as pd
    import numpy as np
    
    # Create a copy
    mapped_df = pd.DataFrame()
    
    # Map each column
    for dataset_col, registry_col in DATASET_TO_REGISTRY_MAPPING.items():
        if dataset_col in df.columns:
            mapped_df[registry_col] = df[dataset_col]
    
    # Handle special conversions
    
    # Convert patent_count to has_patent boolean
    if 'patent_count' in df.columns:
        mapped_df['has_patent'] = df['patent_count'] > 0
    
    # Convert experience counts to booleans
    if 'prior_startup_experience_count' in df.columns:
        mapped_df['repeat_founder'] = df['prior_startup_experience_count'] > 0
    
    if 'prior_successful_exits_count' in df.columns:
        mapped_df['previous_exit'] = df['prior_successful_exits_count'] > 0
    
    # Handle missing required features with defaults
    from .feature_registry import feature_registry
    
    for feature_name, feature_def in feature_registry.features.items():
        if feature_name not in mapped_df.columns:
            # Use default value if available
            if feature_def.default_value is not None:
                mapped_df[feature_name] = feature_def.default_value
            else:
                # Use type-appropriate default
                if feature_def.dtype == bool:
                    mapped_df[feature_name] = False
                elif feature_def.dtype in (int, float):
                    mapped_df[feature_name] = 0
                elif feature_def.dtype == str:
                    if feature_def.allowed_values:
                        mapped_df[feature_name] = feature_def.allowed_values[0]
                    else:
                        mapped_df[feature_name] = 'unknown'
    
    return mapped_df


def get_available_features(df):
    """
    Get list of features that can be mapped from dataset to registry
    """
    available = []
    for dataset_col, registry_col in DATASET_TO_REGISTRY_MAPPING.items():
        if dataset_col in df.columns:
            available.append(registry_col)
    return list(set(available))  # Remove duplicates