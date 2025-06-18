def calculate_camp_scores(features: Dict[str, Any]) -> Dict[str, float]:
    """Calculate normalized CAMP scores from features (0-1 range)"""
    import numpy as np
    from feature_config import CAPITAL_FEATURES, ADVANTAGE_FEATURES, MARKET_FEATURES, PEOPLE_FEATURES
    
    # Define feature normalization rules
    MONETARY_FEATURES = [
        'total_capital_raised_usd', 'cash_on_hand_usd', 'monthly_burn_usd',
        'tam_size_usd', 'sam_size_usd', 'som_size_usd', 'annual_revenue_run_rate',
        'customer_count', 'team_size_full_time', 'founders_count', 'advisors_count',
        'competitors_named_count'
    ]
    
    PERCENTAGE_FEATURES = [
        'market_growth_rate_percent', 'user_growth_rate_percent', 
        'net_dollar_retention_percent', 'customer_concentration_percent',
        'team_diversity_percent', 'gross_margin_percent', 'revenue_growth_rate_percent'
    ]
    
    SCORE_FEATURES = [  # Already 1-5 scale
        'tech_differentiation_score', 'switching_cost_score', 'brand_strength_score',
        'scalability_score', 'board_advisor_experience_score', 'competition_intensity'
    ]
    
    # Normalize features first
    normalized = {}
    for key, value in features.items():
        if value is None:
            normalized[key] = 0.5  # Default for missing values
        elif key in MONETARY_FEATURES:
            # Log scale for monetary values
            if value > 0:
                # Map log scale to 0-1 (assumes $1K to $1B range)
                normalized[key] = np.clip(np.log10(value + 1) / 9, 0, 1)
            else:
                normalized[key] = 0
        elif key in PERCENTAGE_FEATURES:
            # Percentages: -100% to 200% mapped to 0-1
            normalized[key] = np.clip((value + 100) / 300, 0, 1)
        elif key in SCORE_FEATURES:
            # 1-5 scores mapped to 0-1
            normalized[key] = (value - 1) / 4 if value >= 1 else 0
        elif key == 'runway_months':
            # Runway: 0-24 months mapped to 0-1
            normalized[key] = np.clip(value / 24, 0, 1)
        elif key == 'burn_multiple':
            # Burn multiple: inverse (lower is better), 0-10 range
            normalized[key] = np.clip(1 - (value / 10), 0, 1)
        elif key == 'ltv_cac_ratio':
            # LTV/CAC: 0-5 mapped to 0-1
            normalized[key] = np.clip(value / 5, 0, 1)
        elif key in ['patent_count', 'prior_startup_experience_count', 'prior_successful_exits_count']:
            # Counts: 0-10 mapped to 0-1
            normalized[key] = np.clip(value / 10, 0, 1)
        elif key in ['years_experience_avg', 'domain_expertise_years_avg']:
            # Years: 0-20 mapped to 0-1
            normalized[key] = np.clip(value / 20, 0, 1)
        elif key in ['product_retention_30d', 'product_retention_90d']:
            # Retention percentages
            normalized[key] = np.clip(value / 100, 0, 1)
        elif key == 'dau_mau_ratio':
            # DAU/MAU already 0-1
            normalized[key] = np.clip(value, 0, 1)
        else:
            # Binary features or unknown - keep as is
            try:
                normalized[key] = np.clip(float(value), 0, 1)
            except:
                normalized[key] = 0.5
    
    # Calculate CAMP scores from normalized features
    scores = {}
    
    # Capital score
    capital_features = [f for f in CAPITAL_FEATURES if f in normalized]
    if capital_features:
        scores['capital'] = np.mean([normalized[f] for f in capital_features])
    else:
        scores['capital'] = 0.5
    
    # Advantage score
    advantage_features = [f for f in ADVANTAGE_FEATURES if f in normalized]
    if advantage_features:
        scores['advantage'] = np.mean([normalized[f] for f in advantage_features])
    else:
        scores['advantage'] = 0.5
    
    # Market score
    market_features = [f for f in MARKET_FEATURES if f in normalized]
    if market_features:
        scores['market'] = np.mean([normalized[f] for f in market_features])
    else:
        scores['market'] = 0.5
    
    # People score
    people_features = [f for f in PEOPLE_FEATURES if f in normalized]
    if people_features:
        scores['people'] = np.mean([normalized[f] for f in people_features])
    else:
        scores['people'] = 0.5
    
    # Ensure all scores are bounded between 0 and 1
    for key in scores:
        scores[key] = max(0.0, min(1.0, scores[key]))
    
    # Return scores in 0-1 scale
    return scores