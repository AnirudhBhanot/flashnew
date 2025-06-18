#!/usr/bin/env python3
"""Fix CAMP score calculation by normalizing features"""

def calculate_camp_scores_normalized(features):
    """Calculate normalized CAMP scores (0-1 range)"""
    from feature_config import CAPITAL_FEATURES, ADVANTAGE_FEATURES, MARKET_FEATURES, PEOPLE_FEATURES
    
    # Define which features need special normalization
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
    
    # Normalize features
    normalized = {}
    for key, value in features.items():
        if key in MONETARY_FEATURES:
            # Log scale for monetary values
            import numpy as np
            if value > 0:
                # Map log scale to 0-1 (assumes $1K to $1B range)
                normalized[key] = np.clip(np.log10(value + 1) / 9, 0, 1)  # log10(1B) ≈ 9
            else:
                normalized[key] = 0
        elif key in PERCENTAGE_FEATURES:
            # Percentages: -100% to 200% mapped to 0-1
            normalized[key] = np.clip((value + 100) / 300, 0, 1)
        elif key in SCORE_FEATURES:
            # 1-5 scores mapped to 0-1
            normalized[key] = (value - 1) / 4
        elif key in ['runway_months']:
            # Runway: 0-24 months mapped to 0-1
            normalized[key] = np.clip(value / 24, 0, 1)
        elif key in ['burn_multiple']:
            # Burn multiple: inverse (lower is better), 0-10 range
            normalized[key] = np.clip(1 - (value / 10), 0, 1)
        elif key in ['ltv_cac_ratio']:
            # LTV/CAC: 0-5 mapped to 0-1
            normalized[key] = np.clip(value / 5, 0, 1)
        elif key in ['patent_count', 'prior_startup_experience_count', 'prior_successful_exits_count']:
            # Counts: 0-10 mapped to 0-1
            normalized[key] = np.clip(value / 10, 0, 1)
        elif key in ['years_experience_avg', 'domain_expertise_years_avg']:
            # Years: 0-20 mapped to 0-1
            normalized[key] = np.clip(value / 20, 0, 1)
        elif key in ['product_retention_30d', 'product_retention_90d', 'dau_mau_ratio']:
            # Already 0-100 or 0-1
            normalized[key] = np.clip(value / 100 if value > 1 else value, 0, 1)
        else:
            # Binary features or unknown - keep as is
            normalized[key] = np.clip(value, 0, 1)
    
    # Calculate CAMP scores from normalized features
    scores = {}
    
    # Capital
    capital_features = [f for f in CAPITAL_FEATURES if f in normalized]
    scores['capital'] = np.mean([normalized[f] for f in capital_features]) if capital_features else 0.5
    
    # Advantage
    advantage_features = [f for f in ADVANTAGE_FEATURES if f in normalized]
    scores['advantage'] = np.mean([normalized[f] for f in advantage_features]) if advantage_features else 0.5
    
    # Market
    market_features = [f for f in MARKET_FEATURES if f in normalized]
    scores['market'] = np.mean([normalized[f] for f in market_features]) if market_features else 0.5
    
    # People
    people_features = [f for f in PEOPLE_FEATURES if f in normalized]
    scores['people'] = np.mean([normalized[f] for f in people_features]) if people_features else 0.5
    
    return scores

# Test with the terrible data
test_data = {
    'total_capital_raised_usd': 10000,
    'cash_on_hand_usd': 5000,
    'monthly_burn_usd': 20000,
    'runway_months': 0.25,
    'burn_multiple': 10,
    'investor_tier_primary': 0,
    'has_debt': 1,
    'patent_count': 0,
    'network_effects_present': 0,
    'has_data_moat': 0,
    'regulatory_advantage_present': 0,
    'tech_differentiation_score': 1,
    'switching_cost_score': 1,
    'brand_strength_score': 1,
    'scalability_score': 1,
    'sector': 0,
    'tam_size_usd': 1000000,
    'sam_size_usd': 100000,
    'som_size_usd': 10000,
    'market_growth_rate_percent': 0,
    'customer_count': 1,
    'customer_concentration_percent': 100,
    'user_growth_rate_percent': -10,
    'net_dollar_retention_percent': 50,
    'competition_intensity': 5,
    'competitors_named_count': 20,
    'founders_count': 1,
    'team_size_full_time': 1,
    'years_experience_avg': 0,
    'domain_expertise_years_avg': 0,
    'prior_startup_experience_count': 0,
    'prior_successful_exits_count': 0,
    'board_advisor_experience_score': 1,
    'advisors_count': 0,
    'team_diversity_percent': 0,
    'key_person_dependency': 1,
    'product_stage': 0,
    'product_retention_30d': 10,
    'product_retention_90d': 5,
    'dau_mau_ratio': 0.05,
    'annual_revenue_run_rate': 0,
    'revenue_growth_rate_percent': -50,
    'gross_margin_percent': -20,
    'ltv_cac_ratio': 0.1,
    'funding_stage': 0
}

import numpy as np
scores = calculate_camp_scores_normalized(test_data)
print("Normalized CAMP Scores for terrible startup:")
for pillar, score in scores.items():
    print(f"  {pillar.capitalize()}: {score:.1%}")
    
print(f"\nAverage CAMP Score: {np.mean(list(scores.values())):.1%}")
print("(This should be low for a terrible startup!)")