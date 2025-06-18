"""
Smart Feature Defaults for FLASH
Provides intelligent defaults based on startup stage and sector
"""

from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)


class FeatureDefaults:
    """Provides smart defaults for missing features based on context"""
    
    # Stage-based defaults
    STAGE_DEFAULTS = {
        'pre_seed': {
            'total_capital_raised_usd': 250000,
            'cash_on_hand_usd': 200000,
            'monthly_burn_usd': 25000,
            'runway_months': 8,
            'annual_revenue_run_rate': 0,
            'revenue_growth_rate_percent': 0,
            'gross_margin_percent': 0,
            'burn_multiple': 999,  # No revenue yet
            'ltv_cac_ratio': 0,
            'customer_count': 0,
            'team_size_full_time': 3,
            'product_stage': 'pre_launch',
            'product_retention_30d': 0,
            'product_retention_90d': 0,
            'user_growth_rate_percent': 0,
            'net_dollar_retention_percent': 0,
            'customer_concentration_percent': 100,  # If any customers, highly concentrated
            'dau_mau_ratio': 0,
            'founders_count': 2,
            'years_experience_avg': 5,
            'domain_expertise_years_avg': 3,
            'prior_startup_experience_count': 0,
            'prior_successful_exits_count': 0,
            'advisors_count': 2,
            'team_diversity_percent': 30
        },
        'seed': {
            'total_capital_raised_usd': 2000000,
            'cash_on_hand_usd': 1500000,
            'monthly_burn_usd': 100000,
            'runway_months': 15,
            'annual_revenue_run_rate': 500000,
            'revenue_growth_rate_percent': 200,
            'gross_margin_percent': 60,
            'burn_multiple': 2.4,
            'ltv_cac_ratio': 1.5,
            'customer_count': 20,
            'team_size_full_time': 10,
            'product_stage': 'beta',
            'product_retention_30d': 0.6,
            'product_retention_90d': 0.4,
            'user_growth_rate_percent': 50,
            'net_dollar_retention_percent': 95,
            'customer_concentration_percent': 40,
            'dau_mau_ratio': 0.3,
            'founders_count': 2,
            'years_experience_avg': 8,
            'domain_expertise_years_avg': 5,
            'prior_startup_experience_count': 1,
            'prior_successful_exits_count': 0,
            'advisors_count': 4,
            'team_diversity_percent': 35
        },
        'series_a': {
            'total_capital_raised_usd': 10000000,
            'cash_on_hand_usd': 8000000,
            'monthly_burn_usd': 400000,
            'runway_months': 20,
            'annual_revenue_run_rate': 3000000,
            'revenue_growth_rate_percent': 150,
            'gross_margin_percent': 70,
            'burn_multiple': 1.6,
            'ltv_cac_ratio': 3.0,
            'customer_count': 100,
            'team_size_full_time': 30,
            'product_stage': 'growth',
            'product_retention_30d': 0.75,
            'product_retention_90d': 0.60,
            'user_growth_rate_percent': 100,
            'net_dollar_retention_percent': 110,
            'customer_concentration_percent': 25,
            'dau_mau_ratio': 0.4,
            'founders_count': 2,
            'years_experience_avg': 10,
            'domain_expertise_years_avg': 7,
            'prior_startup_experience_count': 2,
            'prior_successful_exits_count': 0,
            'advisors_count': 6,
            'team_diversity_percent': 40
        },
        'series_b': {
            'total_capital_raised_usd': 35000000,
            'cash_on_hand_usd': 25000000,
            'monthly_burn_usd': 1000000,
            'runway_months': 25,
            'annual_revenue_run_rate': 15000000,
            'revenue_growth_rate_percent': 100,
            'gross_margin_percent': 75,
            'burn_multiple': 0.8,
            'ltv_cac_ratio': 4.0,
            'customer_count': 500,
            'team_size_full_time': 100,
            'product_stage': 'growth',
            'product_retention_30d': 0.85,
            'product_retention_90d': 0.75,
            'user_growth_rate_percent': 80,
            'net_dollar_retention_percent': 125,
            'customer_concentration_percent': 15,
            'dau_mau_ratio': 0.5,
            'founders_count': 2,
            'years_experience_avg': 12,
            'domain_expertise_years_avg': 8,
            'prior_startup_experience_count': 2,
            'prior_successful_exits_count': 1,
            'advisors_count': 8,
            'team_diversity_percent': 40
        }
    }
    
    # Sector-specific adjustments
    SECTOR_ADJUSTMENTS = {
        'saas': {
            'gross_margin_percent': 80,
            'ltv_cac_ratio': 3.5,
            'net_dollar_retention_percent': 115,
            'scalability_score': 4.5,
            'product_retention_30d': 0.8
        },
        'marketplace': {
            'gross_margin_percent': 25,
            'network_effects_present': 1,
            'scalability_score': 4,
            'user_growth_rate_percent': 150
        },
        'fintech': {
            'regulatory_advantage_present': 1,
            'switching_cost_score': 4,
            'has_data_moat': 1,
            'brand_strength_score': 4
        },
        'healthtech': {
            'regulatory_advantage_present': 1,
            'patent_count': 3,
            'switching_cost_score': 4.5,
            'market_growth_rate_percent': 35
        },
        'ai_ml': {
            'tech_differentiation_score': 4.5,
            'has_data_moat': 1,
            'patent_count': 2,
            'scalability_score': 4.5
        },
        'enterprise': {
            'ltv_cac_ratio': 4,
            'customer_concentration_percent': 20,
            'switching_cost_score': 4,
            'net_dollar_retention_percent': 120
        }
    }
    
    # Universal defaults for features not covered by stage/sector
    UNIVERSAL_DEFAULTS = {
        'investor_tier_primary': 'tier_2',
        'has_debt': 0,
        'patent_count': 0,
        'network_effects_present': 0,
        'has_data_moat': 0,
        'regulatory_advantage_present': 0,
        'tech_differentiation_score': 3,
        'switching_cost_score': 3,
        'brand_strength_score': 3,
        'scalability_score': 3.5,
        'tam_size_usd': 5000000000,
        'sam_size_usd': 1000000000,
        'som_size_usd': 100000000,
        'market_growth_rate_percent': 25,
        'competition_intensity': 3,
        'competitors_named_count': 10,
        'board_advisor_experience_score': 3,
        'key_person_dependency': 1  # Usually true for startups
    }
    
    @staticmethod
    def get_defaults(data: Dict[str, Any]) -> Dict[str, Any]:
        """Get smart defaults based on startup stage and sector"""
        # Start with universal defaults
        defaults = FeatureDefaults.UNIVERSAL_DEFAULTS.copy()
        
        # Get stage and sector from data
        stage = data.get('funding_stage', 'seed')
        if isinstance(stage, str):
            stage = stage.lower().replace(' ', '_').replace('-', '_')
        
        # Map variations to standard stages
        stage_mapping = {
            'pre_seed': 'pre_seed',
            'preseed': 'pre_seed',
            'seed': 'seed',
            'series_a': 'series_a',
            'a': 'series_a',
            'series_b': 'series_b',
            'b': 'series_b',
            'series_c': 'series_b',  # Use Series B defaults for C+
            'growth': 'series_b'
        }
        stage = stage_mapping.get(stage, 'seed')
        
        # Apply stage-based defaults
        if stage in FeatureDefaults.STAGE_DEFAULTS:
            defaults.update(FeatureDefaults.STAGE_DEFAULTS[stage])
            logger.info(f"Applied {stage} stage defaults")
        
        # Get sector and apply adjustments
        sector = data.get('sector', '').lower()
        
        # Check for sector keywords
        for sector_key, adjustments in FeatureDefaults.SECTOR_ADJUSTMENTS.items():
            if sector_key in sector or sector in sector_key:
                for key, value in adjustments.items():
                    if key.endswith('_percent') or key.endswith('_score'):
                        # For percentages and scores, take the better of default or sector-specific
                        defaults[key] = max(defaults.get(key, 0), value)
                    else:
                        defaults[key] = value
                logger.info(f"Applied {sector_key} sector adjustments")
                break
        
        return defaults
    
    @staticmethod
    def apply_defaults(data: Dict[str, Any]) -> Dict[str, Any]:
        """Apply smart defaults to missing features"""
        # Get appropriate defaults
        defaults = FeatureDefaults.get_defaults(data)
        
        # Create a copy of the data
        enhanced_data = data.copy()
        
        # Track what we're adding
        added_features = []
        
        # Apply defaults for missing features
        from feature_config import ALL_FEATURES
        
        for feature in ALL_FEATURES:
            if feature not in enhanced_data or enhanced_data[feature] is None:
                if feature in defaults:
                    enhanced_data[feature] = defaults[feature]
                    added_features.append(feature)
                else:
                    # Last resort defaults based on feature type
                    if feature.endswith('_count'):
                        enhanced_data[feature] = 0
                    elif feature.endswith('_percent'):
                        enhanced_data[feature] = 0
                    elif feature.endswith('_score'):
                        enhanced_data[feature] = 3  # Neutral score
                    elif feature.endswith('_usd'):
                        enhanced_data[feature] = 0
                    elif feature in ['has_debt', 'network_effects_present', 'has_data_moat', 
                                     'regulatory_advantage_present', 'key_person_dependency']:
                        enhanced_data[feature] = 0
                    else:
                        enhanced_data[feature] = 0
                    added_features.append(feature)
        
        if added_features:
            logger.info(f"Added {len(added_features)} default features: {', '.join(added_features[:5])}...")
        
        return enhanced_data