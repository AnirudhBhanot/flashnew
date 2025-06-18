"""
Quality-based recalibration for FLASH models
"""

import numpy as np
import pandas as pd

def calculate_quality_score(features):
    """Calculate a quality score based on key startup indicators"""
    
    # Extract key metrics
    revenue = features.get('annual_revenue_run_rate', 0)
    growth_rate = features.get('revenue_growth_rate_percent', 0)
    burn_multiple = features.get('burn_multiple', 10)  # Lower is better
    ltv_cac = features.get('ltv_cac_ratio', 0)
    runway = features.get('runway_months', 0)
    team_size = features.get('team_size_full_time', 0)
    founder_exp = features.get('founders_previous_experience_score', 0)
    funding_stage = features.get('funding_stage', 'Pre_Seed')
    investor_tier = features.get('investor_tier_primary', 'Tier_3')
    retention = features.get('product_retention_90d', 0)
    nps = features.get('nps_score', 0)
    market_size = features.get('tam_size_usd', 0)
    
    # Score components (0-1 scale)
    scores = []
    
    # Revenue and growth
    revenue_score = min(1.0, np.log10(revenue + 1) / 8)  # Up to $100M
    growth_score = min(1.0, growth_rate / 100)
    scores.extend([revenue_score, growth_score])
    
    # Efficiency
    burn_score = max(0, 1.0 - (burn_multiple / 5))  # 5x burn is bad
    ltv_score = min(1.0, ltv_cac / 3)  # 3+ is good
    scores.extend([burn_score, ltv_score])
    
    # Runway and funding
    runway_score = min(1.0, runway / 24)  # 24 months is excellent
    stage_scores = {'Pre_Seed': 0.1, 'Seed': 0.3, 'Series_A': 0.5, 'Series_B': 0.7, 'Series_C': 0.9}
    stage_score = stage_scores.get(funding_stage, 0.1)
    tier_scores = {'Tier_3': 0.3, 'Tier_2': 0.6, 'Tier_1': 0.9}
    tier_score = tier_scores.get(investor_tier, 0.3)
    scores.extend([runway_score, stage_score, tier_score])
    
    # Team and execution
    team_score = min(1.0, np.log10(team_size + 1) / 2)  # Up to 100 people
    exp_score = founder_exp / 5.0  # Assuming 1-5 scale
    scores.extend([team_score, exp_score])
    
    # Product metrics
    retention_score = retention  # Already 0-1
    nps_normalized = (nps + 100) / 200  # -100 to 100 -> 0 to 1
    scores.extend([retention_score, nps_normalized])
    
    # Market
    market_score = min(1.0, np.log10(market_size + 1) / 11)  # Up to $100B
    scores.append(market_score)
    
    # Calculate weighted average
    quality_score = np.mean([s for s in scores if s > 0])
    
    return quality_score

def quality_adjusted_prediction(base_prob, features):
    """Adjust prediction based on startup quality"""
    
    quality_score = calculate_quality_score(features)
    
    # Blend base prediction with quality score
    # More weight on quality for very low base predictions
    if base_prob < 0.1:
        # 70% quality, 30% base
        adjusted = 0.7 * quality_score + 0.3 * base_prob
    elif base_prob < 0.3:
        # 50% quality, 50% base
        adjusted = 0.5 * quality_score + 0.5 * base_prob
    else:
        # 30% quality, 70% base
        adjusted = 0.3 * quality_score + 0.7 * base_prob
    
    # Apply bounds
    return np.clip(adjusted, 0.05, 0.95)

def differentiate_predictions(predictions, features_list):
    """Ensure predictions have meaningful differentiation"""
    
    # Calculate quality scores for all startups
    quality_scores = [calculate_quality_score(f) for f in features_list]
    
    # Rank startups by quality
    ranks = np.argsort(quality_scores)
    
    # Map to probability ranges based on rank
    n = len(predictions)
    adjusted_predictions = []
    
    for i, idx in enumerate(ranks):
        # Map rank to probability range
        percentile = i / n
        
        if percentile < 0.1:  # Bottom 10%
            target_range = (0.05, 0.15)
        elif percentile < 0.3:  # Bottom 30%
            target_range = (0.15, 0.30)
        elif percentile < 0.5:  # Middle
            target_range = (0.30, 0.50)
        elif percentile < 0.7:  # Top 50-70%
            target_range = (0.50, 0.70)
        elif percentile < 0.9:  # Top 30%
            target_range = (0.70, 0.85)
        else:  # Top 10%
            target_range = (0.85, 0.95)
        
        # Blend original prediction with target range
        original = predictions[idx]
        target = target_range[0] + (target_range[1] - target_range[0]) * 0.5
        adjusted = 0.3 * original + 0.7 * target
        
        adjusted_predictions.append(adjusted)
    
    return adjusted_predictions