"""
Pattern-Specific Contracts for all 31 patterns
Each pattern has its own contract with specific requirements and computations
"""

from typing import Dict, List, Any
import pandas as pd
import numpy as np

from .model_contracts import ModelContract
from .enhanced_contracts import PatternType, PatternProfile
from .feature_registry import feature_registry


class PatternContractFactory:
    """Factory for creating contracts for all 31 startup patterns"""
    
    def __init__(self):
        self.registry = feature_registry
        self._init_all_patterns()
    
    def _init_all_patterns(self):
        """Initialize detailed profiles for all 31 patterns"""
        self.pattern_profiles = {
            # Growth Patterns
            PatternType.EFFICIENT_GROWTH: PatternProfile(
                pattern_type=PatternType.EFFICIENT_GROWTH,
                key_features=['burn_multiple', 'revenue_growth_rate', 'runway_months', 
                             'customer_acquisition_cost', 'customer_lifetime_value'],
                success_threshold=0.7,
                typical_metrics={
                    'burn_multiple': 1.2,
                    'revenue_growth_rate': 150,
                    'runway_months': 24,
                    'ltv_cac_ratio': 4
                },
                camp_weights={'capital': 0.35, 'advantage': 0.2, 'market': 0.3, 'people': 0.15}
            ),
            
            PatternType.HIGH_BURN_GROWTH: PatternProfile(
                pattern_type=PatternType.HIGH_BURN_GROWTH,
                key_features=['burn_multiple', 'revenue_growth_rate', 'total_capital_raised_usd',
                             'team_size_full_time', 'market_growth_rate'],
                success_threshold=0.65,
                typical_metrics={
                    'burn_multiple': 3.5,
                    'revenue_growth_rate': 400,
                    'team_size_full_time': 100,
                    'total_capital_raised_usd': 50000000
                },
                camp_weights={'capital': 0.4, 'advantage': 0.15, 'market': 0.35, 'people': 0.1}
            ),
            
            PatternType.EXPONENTIAL_SCALE: PatternProfile(
                pattern_type=PatternType.EXPONENTIAL_SCALE,
                key_features=['revenue_growth_rate', 'customer_growth_rate', 'net_revenue_retention',
                             'platform_business', 'network_effects'],
                success_threshold=0.75,
                typical_metrics={
                    'revenue_growth_rate': 500,
                    'customer_growth_rate': 300,
                    'net_revenue_retention': 140,
                    'platform_business': True
                },
                camp_weights={'capital': 0.25, 'advantage': 0.3, 'market': 0.35, 'people': 0.1}
            ),
            
            PatternType.STEADY_LINEAR: PatternProfile(
                pattern_type=PatternType.STEADY_LINEAR,
                key_features=['revenue_growth_rate', 'burn_multiple', 'employee_growth_rate'],
                success_threshold=0.6,
                typical_metrics={
                    'revenue_growth_rate': 50,
                    'burn_multiple': 1.0,
                    'employee_growth_rate': 30
                },
                camp_weights={'capital': 0.25, 'advantage': 0.25, 'market': 0.25, 'people': 0.25}
            ),
            
            PatternType.STALLED_GROWTH: PatternProfile(
                pattern_type=PatternType.STALLED_GROWTH,
                key_features=['revenue_growth_rate', 'customer_growth_rate', 'runway_months'],
                success_threshold=0.4,
                typical_metrics={
                    'revenue_growth_rate': 10,
                    'customer_growth_rate': 5,
                    'runway_months': 6
                },
                camp_weights={'capital': 0.3, 'advantage': 0.2, 'market': 0.2, 'people': 0.3}
            ),
            
            # Business Model Patterns
            PatternType.B2B_SAAS: PatternProfile(
                pattern_type=PatternType.B2B_SAAS,
                key_features=['net_revenue_retention', 'annual_recurring_revenue_millions',
                             'customer_acquisition_cost', 'sales_cycle_days', 'target_enterprise'],
                success_threshold=0.75,
                typical_metrics={
                    'net_revenue_retention': 120,
                    'annual_recurring_revenue_millions': 5,
                    'sales_cycle_days': 60,
                    'target_enterprise': True
                },
                camp_weights={'capital': 0.25, 'advantage': 0.25, 'market': 0.35, 'people': 0.15}
            ),
            
            PatternType.B2C_MARKETPLACE: PatternProfile(
                pattern_type=PatternType.B2C_MARKETPLACE,
                key_features=['platform_business', 'customer_growth_rate', 'market_competitiveness',
                             'international_revenue_percent', 'mobile_first'],
                success_threshold=0.7,
                typical_metrics={
                    'platform_business': True,
                    'customer_growth_rate': 200,
                    'mobile_first': True,
                    'international_revenue_percent': 30
                },
                camp_weights={'capital': 0.3, 'advantage': 0.2, 'market': 0.4, 'people': 0.1}
            ),
            
            PatternType.D2C_ECOMMERCE: PatternProfile(
                pattern_type=PatternType.D2C_ECOMMERCE,
                key_features=['customer_acquisition_cost', 'customer_lifetime_value',
                             'average_deal_size', 'mobile_first', 'international_revenue_percent'],
                success_threshold=0.65,
                typical_metrics={
                    'customer_acquisition_cost': 50,
                    'customer_lifetime_value': 200,
                    'mobile_first': True,
                    'average_deal_size': 75
                },
                camp_weights={'capital': 0.3, 'advantage': 0.15, 'market': 0.45, 'people': 0.1}
            ),
            
            PatternType.PLATFORM_NETWORK: PatternProfile(
                pattern_type=PatternType.PLATFORM_NETWORK,
                key_features=['platform_business', 'network_effects', 'customer_growth_rate',
                             'market_tam_billions', 'viral_coefficient'],
                success_threshold=0.75,
                typical_metrics={
                    'platform_business': True,
                    'customer_growth_rate': 250,
                    'market_tam_billions': 10
                },
                camp_weights={'capital': 0.25, 'advantage': 0.35, 'market': 0.3, 'people': 0.1}
            ),
            
            PatternType.FREEMIUM_CONVERSION: PatternProfile(
                pattern_type=PatternType.FREEMIUM_CONVERSION,
                key_features=['customer_acquisition_cost', 'conversion_rate', 'net_revenue_retention',
                             'product_market_fit_score', 'uses_ai_ml'],
                success_threshold=0.7,
                typical_metrics={
                    'customer_acquisition_cost': 10,
                    'net_revenue_retention': 115,
                    'product_market_fit_score': 4
                },
                camp_weights={'capital': 0.2, 'advantage': 0.3, 'market': 0.35, 'people': 0.15}
            ),
            
            PatternType.ENTERPRISE_SALES: PatternProfile(
                pattern_type=PatternType.ENTERPRISE_SALES,
                key_features=['target_enterprise', 'average_deal_size', 'sales_cycle_days',
                             'annual_recurring_revenue_millions', 'customer_concentration'],
                success_threshold=0.7,
                typical_metrics={
                    'target_enterprise': True,
                    'average_deal_size': 100000,
                    'sales_cycle_days': 180,
                    'annual_recurring_revenue_millions': 10
                },
                camp_weights={'capital': 0.25, 'advantage': 0.2, 'market': 0.35, 'people': 0.2}
            ),
            
            PatternType.API_FIRST: PatternProfile(
                pattern_type=PatternType.API_FIRST,
                key_features=['technology_score', 'developer_adoption', 'platform_business',
                             'cloud_native', 'scalability_score'],
                success_threshold=0.7,
                typical_metrics={
                    'technology_score': 5,
                    'cloud_native': True,
                    'scalability_score': 5,
                    'platform_business': True
                },
                camp_weights={'capital': 0.2, 'advantage': 0.4, 'market': 0.25, 'people': 0.15}
            ),
            
            # Funding Patterns
            PatternType.BOOTSTRAP_PROFITABLE: PatternProfile(
                pattern_type=PatternType.BOOTSTRAP_PROFITABLE,
                key_features=['burn_multiple', 'total_capital_raised_usd', 'runway_months',
                             'revenue_growth_rate', 'profit_margin'],
                success_threshold=0.65,
                typical_metrics={
                    'burn_multiple': 0.8,
                    'total_capital_raised_usd': 100000,
                    'runway_months': 36
                },
                camp_weights={'capital': 0.4, 'advantage': 0.15, 'market': 0.3, 'people': 0.15}
            ),
            
            PatternType.VC_HYPERGROWTH: PatternProfile(
                pattern_type=PatternType.VC_HYPERGROWTH,
                key_features=['total_capital_raised_usd', 'investor_tier_primary', 'revenue_growth_rate',
                             'team_size_full_time', 'burn_multiple'],
                success_threshold=0.7,
                typical_metrics={
                    'total_capital_raised_usd': 20000000,
                    'investor_tier_primary': 'tier_1',
                    'revenue_growth_rate': 300,
                    'team_size_full_time': 50
                },
                camp_weights={'capital': 0.35, 'advantage': 0.15, 'market': 0.35, 'people': 0.15}
            ),
            
            PatternType.STRATEGIC_FUNDED: PatternProfile(
                pattern_type=PatternType.STRATEGIC_FUNDED,
                key_features=['strategic_investors', 'industry_connections', 'partnership_revenue',
                             'market_share', 'competitive_advantage'],
                success_threshold=0.7,
                typical_metrics={
                    'industry_connections': 5,
                    'strategic_investors': True
                },
                camp_weights={'capital': 0.25, 'advantage': 0.25, 'market': 0.35, 'people': 0.15}
            ),
            
            PatternType.GRANT_SUPPORTED: PatternProfile(
                pattern_type=PatternType.GRANT_SUPPORTED,
                key_features=['grant_funding', 'research_development_percent', 'has_patent',
                             'academic_partnerships', 'social_impact_score'],
                success_threshold=0.6,
                typical_metrics={
                    'research_development_percent': 40,
                    'has_patent': True
                },
                camp_weights={'capital': 0.2, 'advantage': 0.35, 'market': 0.2, 'people': 0.25}
            ),
            
            PatternType.REVENUE_BASED: PatternProfile(
                pattern_type=PatternType.REVENUE_BASED,
                key_features=['revenue_predictability', 'gross_margin', 'customer_retention',
                             'cash_flow_positive', 'debt_to_equity'],
                success_threshold=0.65,
                typical_metrics={
                    'gross_margin': 70,
                    'customer_retention': 90
                },
                camp_weights={'capital': 0.35, 'advantage': 0.15, 'market': 0.35, 'people': 0.15}
            ),
            
            # Tech Patterns
            PatternType.AI_ML_CORE: PatternProfile(
                pattern_type=PatternType.AI_ML_CORE,
                key_features=['uses_ai_ml', 'research_development_percent', 'technical_founder',
                             'has_patent', 'data_advantage'],
                success_threshold=0.7,
                typical_metrics={
                    'uses_ai_ml': True,
                    'research_development_percent': 30,
                    'technical_founder': True
                },
                camp_weights={'capital': 0.2, 'advantage': 0.4, 'market': 0.25, 'people': 0.15}
            ),
            
            PatternType.BLOCKCHAIN_WEB3: PatternProfile(
                pattern_type=PatternType.BLOCKCHAIN_WEB3,
                key_features=['blockchain_tech', 'token_economy', 'decentralized',
                             'crypto_integration', 'community_size'],
                success_threshold=0.65,
                typical_metrics={
                    'blockchain_tech': True,
                    'community_size': 10000
                },
                camp_weights={'capital': 0.25, 'advantage': 0.35, 'market': 0.25, 'people': 0.15}
            ),
            
            PatternType.DEEP_TECH_RD: PatternProfile(
                pattern_type=PatternType.DEEP_TECH_RD,
                key_features=['research_development_percent', 'has_patent', 'phd_team_percent',
                             'time_to_market', 'technical_risk'],
                success_threshold=0.65,
                typical_metrics={
                    'research_development_percent': 50,
                    'has_patent': True,
                    'phd_team_percent': 40
                },
                camp_weights={'capital': 0.25, 'advantage': 0.4, 'market': 0.15, 'people': 0.2}
            ),
            
            PatternType.NO_CODE_LOW_CODE: PatternProfile(
                pattern_type=PatternType.NO_CODE_LOW_CODE,
                key_features=['ease_of_use_score', 'time_to_value', 'customer_acquisition_cost',
                             'viral_coefficient', 'product_market_fit_score'],
                success_threshold=0.7,
                typical_metrics={
                    'ease_of_use_score': 5,
                    'customer_acquisition_cost': 50,
                    'product_market_fit_score': 4
                },
                camp_weights={'capital': 0.2, 'advantage': 0.3, 'market': 0.35, 'people': 0.15}
            ),
            
            PatternType.MOBILE_FIRST: PatternProfile(
                pattern_type=PatternType.MOBILE_FIRST,
                key_features=['mobile_first', 'app_store_rating', 'daily_active_users',
                             'retention_day_30', 'viral_coefficient'],
                success_threshold=0.7,
                typical_metrics={
                    'mobile_first': True,
                    'app_store_rating': 4.5,
                    'retention_day_30': 40
                },
                camp_weights={'capital': 0.25, 'advantage': 0.25, 'market': 0.4, 'people': 0.1}
            ),
            
            # Market Patterns
            PatternType.MARKET_CREATOR: PatternProfile(
                pattern_type=PatternType.MARKET_CREATOR,
                key_features=['first_mover', 'market_education_cost', 'brand_recognition',
                             'patent_moat', 'market_tam_billions'],
                success_threshold=0.7,
                typical_metrics={
                    'first_mover': True,
                    'market_tam_billions': 5,
                    'brand_recognition': 4
                },
                camp_weights={'capital': 0.3, 'advantage': 0.3, 'market': 0.3, 'people': 0.1}
            ),
            
            PatternType.FAST_FOLLOWER: PatternProfile(
                pattern_type=PatternType.FAST_FOLLOWER,
                key_features=['execution_speed', 'feature_velocity', 'customer_feedback_score',
                             'competitive_differentiation', 'market_share_growth'],
                success_threshold=0.65,
                typical_metrics={
                    'execution_speed': 4,
                    'feature_velocity': 5,
                    'customer_feedback_score': 4
                },
                camp_weights={'capital': 0.25, 'advantage': 0.2, 'market': 0.35, 'people': 0.2}
            ),
            
            PatternType.NICHE_DOMINATOR: PatternProfile(
                pattern_type=PatternType.NICHE_DOMINATOR,
                key_features=['market_share', 'customer_concentration', 'specialization_score',
                             'customer_satisfaction', 'competitive_moat'],
                success_threshold=0.7,
                typical_metrics={
                    'market_share': 30,
                    'customer_satisfaction': 90,
                    'specialization_score': 5
                },
                camp_weights={'capital': 0.2, 'advantage': 0.3, 'market': 0.35, 'people': 0.15}
            ),
            
            PatternType.GEOGRAPHIC_EXPANSION: PatternProfile(
                pattern_type=PatternType.GEOGRAPHIC_EXPANSION,
                key_features=['international_revenue_percent', 'localization_score', 'market_count',
                             'cultural_adaptation', 'regulatory_compliance'],
                success_threshold=0.7,
                typical_metrics={
                    'international_revenue_percent': 40,
                    'market_count': 5,
                    'localization_score': 4
                },
                camp_weights={'capital': 0.3, 'advantage': 0.15, 'market': 0.4, 'people': 0.15}
            ),
            
            # Operational Patterns
            PatternType.LEAN_EFFICIENT: PatternProfile(
                pattern_type=PatternType.LEAN_EFFICIENT,
                key_features=['burn_multiple', 'revenue_per_employee', 'automation_score',
                             'operational_efficiency', 'gross_margin'],
                success_threshold=0.7,
                typical_metrics={
                    'burn_multiple': 0.9,
                    'revenue_per_employee': 200000,
                    'automation_score': 4,
                    'gross_margin': 80
                },
                camp_weights={'capital': 0.35, 'advantage': 0.25, 'market': 0.25, 'people': 0.15}
            ),
            
            PatternType.HEAVY_RD: PatternProfile(
                pattern_type=PatternType.HEAVY_RD,
                key_features=['research_development_percent', 'innovation_score', 'patent_pipeline',
                             'technical_debt_ratio', 'rd_roi'],
                success_threshold=0.65,
                typical_metrics={
                    'research_development_percent': 35,
                    'innovation_score': 5,
                    'patent_pipeline': 10
                },
                camp_weights={'capital': 0.25, 'advantage': 0.4, 'market': 0.2, 'people': 0.15}
            ),
            
            PatternType.SALES_DRIVEN: PatternProfile(
                pattern_type=PatternType.SALES_DRIVEN,
                key_features=['sales_efficiency', 'sales_team_size', 'average_deal_size',
                             'sales_cycle_days', 'quota_attainment'],
                success_threshold=0.7,
                typical_metrics={
                    'sales_efficiency': 1.2,
                    'quota_attainment': 80,
                    'average_deal_size': 50000
                },
                camp_weights={'capital': 0.25, 'advantage': 0.15, 'market': 0.35, 'people': 0.25}
            ),
            
            PatternType.PRODUCT_LED: PatternProfile(
                pattern_type=PatternType.PRODUCT_LED,
                key_features=['product_market_fit_score', 'user_onboarding_score', 'viral_coefficient',
                             'self_serve_revenue_percent', 'nps_score'],
                success_threshold=0.75,
                typical_metrics={
                    'product_market_fit_score': 5,
                    'viral_coefficient': 1.2,
                    'self_serve_revenue_percent': 70,
                    'nps_score': 50
                },
                camp_weights={'capital': 0.2, 'advantage': 0.35, 'market': 0.35, 'people': 0.1}
            )
        }
    
    def create_pattern_contract(self, pattern_type: PatternType) -> ModelContract:
        """Create a contract for a specific pattern"""
        profile = self.pattern_profiles.get(pattern_type)
        if not profile:
            raise ValueError(f"Unknown pattern: {pattern_type}")
        
        contract = ModelContract(
            model_name=f"pattern_{pattern_type.value}",
            model_type="pattern_classifier",
            version="2.0.0"
        )
        
        # Add all base features
        feature_names = self.registry.get_feature_names()
        contract.add_raw_features(feature_names)
        
        # Add pattern-specific score
        contract.add_computed_feature(
            f'{pattern_type.value}_match_score',
            computation=lambda df: self._compute_pattern_match_score(df, profile),
            dependencies=profile.key_features
        )
        
        # Add weighted CAMP scores based on pattern
        self._add_pattern_camp_scores(contract, profile)
        
        # Add pattern evolution features
        contract.add_computed_feature(
            'pattern_evolution_potential',
            computation=lambda df: self._compute_evolution_potential(df, profile),
            dependencies=['revenue_growth_rate', 'customer_growth_rate', 'runway_months']
        )
        
        # Add success probability modifier
        contract.add_computed_feature(
            'pattern_success_modifier',
            computation=lambda df: self._compute_success_modifier(df, profile),
            dependencies=profile.key_features
        )
        
        return contract
    
    def create_multi_pattern_contract(self, pattern_types: List[PatternType]) -> ModelContract:
        """Create a contract that handles multiple patterns"""
        contract = ModelContract(
            model_name="multi_pattern_classifier",
            model_type="multi_pattern",
            version="2.0.0"
        )
        
        # Add all base features
        feature_names = self.registry.get_feature_names()
        contract.add_raw_features(feature_names)
        
        # Add match scores for each pattern
        for pattern_type in pattern_types:
            profile = self.pattern_profiles.get(pattern_type)
            if profile:
                contract.add_computed_feature(
                    f'{pattern_type.value}_match',
                    computation=lambda df, p=profile: self._compute_pattern_match_score(df, p),
                    dependencies=profile.key_features
                )
        
        # Add dominant pattern detection
        contract.add_computed_feature(
            'dominant_pattern',
            computation=lambda df: self._detect_dominant_pattern(df, pattern_types),
            dependencies=[f for p in pattern_types for f in self.pattern_profiles[p].key_features]
        )
        
        # Add pattern combination score
        contract.add_computed_feature(
            'pattern_synergy_score',
            computation=lambda df: self._compute_pattern_synergy(df, pattern_types),
            dependencies=['dominant_pattern']
        )
        
        return contract
    
    def _compute_pattern_match_score(self, df: pd.DataFrame, profile: PatternProfile) -> float:
        """Compute how well the startup matches a pattern"""
        if len(df) == 0:
            return 0.0
        
        scores = []
        weights = []
        
        for feature in profile.key_features:
            if feature in df.columns:
                actual = df[feature].iloc[0]
                expected = profile.typical_metrics.get(feature)
                
                if expected is not None:
                    if isinstance(expected, bool):
                        score = 1.0 if actual == expected else 0.0
                    elif isinstance(expected, (int, float)):
                        # Gaussian-like scoring
                        diff_ratio = abs(actual - expected) / (expected + 1)
                        score = np.exp(-diff_ratio * diff_ratio)
                    else:
                        score = 0.5  # Default for unknown types
                    
                    scores.append(score)
                    # Weight more important features higher
                    weight = 2.0 if profile.key_features.index(feature) < 3 else 1.0
                    weights.append(weight)
        
        if not scores:
            return 0.5
        
        # Weighted average
        return np.average(scores, weights=weights)
    
    def _add_pattern_camp_scores(self, contract: ModelContract, profile: PatternProfile):
        """Add CAMP scores weighted for the specific pattern"""
        for camp_type, weight in profile.camp_weights.items():
            contract.add_computed_feature(
                f'{camp_type}_weighted_score',
                computation=lambda df, c=camp_type, w=weight: self._compute_weighted_camp(df, c, w),
                dependencies=self.registry.get_features_by_category(camp_type)[:5]  # Top 5 features
            )
    
    def _compute_weighted_camp(self, df: pd.DataFrame, camp_type: str, weight: float) -> float:
        """Compute weighted CAMP score for a category"""
        features = [f.name for f in self.registry.get_features_by_category(camp_type)]
        if not features or len(df) == 0:
            return 0.5 * weight
        
        scores = []
        for feature in features[:5]:  # Use top 5 features
            if feature in df.columns:
                value = df[feature].iloc[0]
                # Normalize based on feature type
                feature_def = self.registry.get_feature(feature)
                if feature_def.dtype == bool:
                    score = float(value)
                elif feature_def.min_value is not None and feature_def.max_value is not None:
                    score = (value - feature_def.min_value) / (feature_def.max_value - feature_def.min_value)
                    score = max(0, min(1, score))
                else:
                    score = min(1.0, value / 100)  # Simple normalization
                scores.append(score)
        
        return np.mean(scores) * weight if scores else 0.5 * weight
    
    def _compute_evolution_potential(self, df: pd.DataFrame, profile: PatternProfile) -> float:
        """Compute potential for pattern evolution"""
        if len(df) == 0:
            return 0.5
        
        # Check growth indicators
        growth_features = ['revenue_growth_rate', 'customer_growth_rate', 'employee_growth_rate']
        growth_scores = []
        
        for feature in growth_features:
            if feature in df.columns:
                value = df[feature].iloc[0]
                # Higher growth = higher evolution potential
                score = min(1.0, value / 200)  # Cap at 200% growth
                growth_scores.append(score)
        
        # Check stability indicators
        stability_features = ['runway_months', 'burn_multiple']
        stability_scores = []
        
        if 'runway_months' in df.columns:
            runway = df['runway_months'].iloc[0]
            stability_scores.append(min(1.0, runway / 24))  # 24 months is ideal
        
        if 'burn_multiple' in df.columns:
            burn = df['burn_multiple'].iloc[0]
            # Lower burn is better for evolution
            stability_scores.append(max(0, 1 - burn / 5))
        
        # Combine growth and stability
        growth_avg = np.mean(growth_scores) if growth_scores else 0.5
        stability_avg = np.mean(stability_scores) if stability_scores else 0.5
        
        return 0.6 * growth_avg + 0.4 * stability_avg
    
    def _compute_success_modifier(self, df: pd.DataFrame, profile: PatternProfile) -> float:
        """Compute success probability modifier based on pattern fit"""
        match_score = self._compute_pattern_match_score(df, profile)
        
        # Strong match increases success probability
        if match_score > 0.8:
            return 1.2  # 20% boost
        elif match_score > 0.6:
            return 1.1  # 10% boost
        elif match_score < 0.3:
            return 0.9  # 10% penalty
        else:
            return 1.0  # No modification
    
    def _detect_dominant_pattern(self, df: pd.DataFrame, pattern_types: List[PatternType]) -> str:
        """Detect which pattern is dominant"""
        if len(df) == 0:
            return "unknown"
        
        best_score = 0
        best_pattern = None
        
        for pattern_type in pattern_types:
            profile = self.pattern_profiles.get(pattern_type)
            if profile:
                score = self._compute_pattern_match_score(df, profile)
                if score > best_score:
                    best_score = score
                    best_pattern = pattern_type
        
        return best_pattern.value if best_pattern else "unknown"
    
    def _compute_pattern_synergy(self, df: pd.DataFrame, pattern_types: List[PatternType]) -> float:
        """Compute synergy between multiple patterns"""
        if len(df) == 0 or len(pattern_types) < 2:
            return 0.0
        
        # Some patterns work well together
        synergistic_pairs = [
            (PatternType.AI_ML_CORE, PatternType.B2B_SAAS),
            (PatternType.PLATFORM_NETWORK, PatternType.FREEMIUM_CONVERSION),
            (PatternType.EFFICIENT_GROWTH, PatternType.BOOTSTRAP_PROFITABLE),
            (PatternType.PRODUCT_LED, PatternType.VIRAL_GROWTH),
        ]
        
        synergy_score = 0
        for p1, p2 in synergistic_pairs:
            if p1 in pattern_types and p2 in pattern_types:
                synergy_score += 0.1
        
        return min(0.3, synergy_score)  # Cap at 30% bonus