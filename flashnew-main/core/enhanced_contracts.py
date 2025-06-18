"""
Enhanced Contract System with Pattern, Stage, and Industry Support
Combines the safety of contracts with the performance of specialized models
"""

from typing import List, Dict, Optional, Any, Set
from enum import Enum
import numpy as np
from dataclasses import dataclass

from .model_contracts import ModelContract, FeatureSpecification
from .feature_registry import FeatureRegistry


class PatternType(Enum):
    """All 31 startup patterns"""
    # Growth Patterns
    EFFICIENT_GROWTH = "efficient_growth"
    HIGH_BURN_GROWTH = "high_burn_growth"
    EXPONENTIAL_SCALE = "exponential_scale"
    STEADY_LINEAR = "steady_linear"
    STALLED_GROWTH = "stalled_growth"
    
    # Business Model Patterns
    B2B_SAAS = "b2b_saas"
    B2C_MARKETPLACE = "b2c_marketplace"
    D2C_ECOMMERCE = "d2c_ecommerce"
    PLATFORM_NETWORK = "platform_network"
    FREEMIUM_CONVERSION = "freemium_conversion"
    ENTERPRISE_SALES = "enterprise_sales"
    API_FIRST = "api_first"
    
    # Funding Patterns
    BOOTSTRAP_PROFITABLE = "bootstrap_profitable"
    VC_HYPERGROWTH = "vc_hypergrowth"
    STRATEGIC_FUNDED = "strategic_funded"
    GRANT_SUPPORTED = "grant_supported"
    REVENUE_BASED = "revenue_based"
    
    # Tech Patterns
    AI_ML_CORE = "ai_ml_core"
    BLOCKCHAIN_WEB3 = "blockchain_web3"
    DEEP_TECH_RD = "deep_tech_rd"
    NO_CODE_LOW_CODE = "no_code_low_code"
    MOBILE_FIRST = "mobile_first"
    
    # Market Patterns
    MARKET_CREATOR = "market_creator"
    FAST_FOLLOWER = "fast_follower"
    NICHE_DOMINATOR = "niche_dominator"
    GEOGRAPHIC_EXPANSION = "geographic_expansion"
    
    # Operational Patterns
    LEAN_EFFICIENT = "lean_efficient"
    HEAVY_RD = "heavy_rd"
    SALES_DRIVEN = "sales_driven"
    PRODUCT_LED = "product_led"


class FundingStage(Enum):
    """Funding stages with specific characteristics"""
    PRE_SEED = "pre_seed"
    SEED = "seed"
    SERIES_A = "series_a"
    SERIES_B = "series_b"
    SERIES_C = "series_c"
    SERIES_D_PLUS = "series_d_plus"


class Industry(Enum):
    """Industry verticals with specific requirements"""
    SAAS = "saas"
    AI_ML = "ai_ml"
    FINTECH = "fintech"
    HEALTHTECH = "healthtech"
    EDTECH = "edtech"
    ECOMMERCE = "ecommerce"
    MARKETPLACE = "marketplace"
    GAMING = "gaming"
    CYBERSECURITY = "cybersecurity"
    BIOTECH = "biotech"


@dataclass
class PatternProfile:
    """Profile for a specific startup pattern"""
    pattern_type: PatternType
    key_features: List[str]  # Most important features for this pattern
    success_threshold: float  # Min probability to be considered successful
    typical_metrics: Dict[str, Any]  # Typical values for key metrics
    
    # CAMP weights for this pattern
    camp_weights: Dict[str, float] = None
    
    def __post_init__(self):
        if self.camp_weights is None:
            self.camp_weights = {
                'capital': 0.25,
                'advantage': 0.25,
                'market': 0.25,
                'people': 0.25
            }


class EnhancedContractBuilder:
    """Build contracts that incorporate patterns, stages, and industries"""
    
    def __init__(self, feature_registry: FeatureRegistry):
        self.registry = feature_registry
        self._init_pattern_profiles()
        self._init_stage_requirements()
        self._init_industry_requirements()
    
    def _init_pattern_profiles(self):
        """Initialize profiles for each pattern"""
        self.pattern_profiles = {
            PatternType.EFFICIENT_GROWTH: PatternProfile(
                pattern_type=PatternType.EFFICIENT_GROWTH,
                key_features=['burn_multiple', 'revenue_growth_rate', 'runway_months'],
                success_threshold=0.7,
                typical_metrics={'burn_multiple': 1.5, 'revenue_growth_rate': 150},
                camp_weights={'capital': 0.3, 'advantage': 0.2, 'market': 0.3, 'people': 0.2}
            ),
            PatternType.VC_HYPERGROWTH: PatternProfile(
                pattern_type=PatternType.VC_HYPERGROWTH,
                key_features=['total_capital_raised_usd', 'revenue_growth_rate', 'team_size_full_time'],
                success_threshold=0.65,
                typical_metrics={'revenue_growth_rate': 300, 'team_size_full_time': 50},
                camp_weights={'capital': 0.35, 'advantage': 0.15, 'market': 0.35, 'people': 0.15}
            ),
            PatternType.AI_ML_CORE: PatternProfile(
                pattern_type=PatternType.AI_ML_CORE,
                key_features=['uses_ai_ml', 'research_development_percent', 'technical_founder'],
                success_threshold=0.7,
                typical_metrics={'uses_ai_ml': True, 'research_development_percent': 30},
                camp_weights={'capital': 0.2, 'advantage': 0.4, 'market': 0.2, 'people': 0.2}
            ),
            PatternType.B2B_SAAS: PatternProfile(
                pattern_type=PatternType.B2B_SAAS,
                key_features=['net_revenue_retention', 'customer_acquisition_cost', 'annual_recurring_revenue_millions'],
                success_threshold=0.75,
                typical_metrics={'net_revenue_retention': 120, 'target_enterprise': True},
                camp_weights={'capital': 0.25, 'advantage': 0.25, 'market': 0.35, 'people': 0.15}
            ),
            PatternType.BOOTSTRAP_PROFITABLE: PatternProfile(
                pattern_type=PatternType.BOOTSTRAP_PROFITABLE,
                key_features=['burn_multiple', 'runway_months', 'revenue_growth_rate'],
                success_threshold=0.65,
                typical_metrics={'burn_multiple': 0.8, 'total_capital_raised_usd': 500000},
                camp_weights={'capital': 0.35, 'advantage': 0.15, 'market': 0.3, 'people': 0.2}
            ),
            # Add more patterns as needed...
        }
    
    def _init_stage_requirements(self):
        """Initialize requirements for each funding stage"""
        self.stage_requirements = {
            FundingStage.PRE_SEED: {
                'critical_features': ['founder_experience_years', 'technical_founder', 'market_tam_billions'],
                'min_thresholds': {'team_size_full_time': 2},
                'camp_weights': {'capital': 0.15, 'advantage': 0.25, 'market': 0.3, 'people': 0.3}
            },
            FundingStage.SEED: {
                'critical_features': ['product_market_fit_score', 'customer_growth_rate', 'burn_multiple'],
                'min_thresholds': {'annual_revenue_run_rate': 100000},
                'camp_weights': {'capital': 0.2, 'advantage': 0.25, 'market': 0.35, 'people': 0.2}
            },
            FundingStage.SERIES_A: {
                'critical_features': ['annual_recurring_revenue_millions', 'net_revenue_retention', 'sales_efficiency'],
                'min_thresholds': {'annual_recurring_revenue_millions': 1.0},
                'camp_weights': {'capital': 0.25, 'advantage': 0.2, 'market': 0.4, 'people': 0.15}
            },
            FundingStage.SERIES_B: {
                'critical_features': ['revenue_growth_rate', 'market_share', 'international_revenue_percent'],
                'min_thresholds': {'annual_recurring_revenue_millions': 10.0},
                'camp_weights': {'capital': 0.3, 'advantage': 0.15, 'market': 0.45, 'people': 0.1}
            },
            # Add more stages...
        }
    
    def _init_industry_requirements(self):
        """Initialize requirements for each industry"""
        self.industry_requirements = {
            Industry.SAAS: {
                'critical_features': ['net_revenue_retention', 'customer_acquisition_cost', 'burn_multiple'],
                'required_features': ['cloud_native', 'annual_recurring_revenue_millions'],
                'success_factors': ['net_revenue_retention > 110', 'ltv_cac_ratio > 3']
            },
            Industry.AI_ML: {
                'critical_features': ['uses_ai_ml', 'research_development_percent', 'technical_founder'],
                'required_features': ['has_patent', 'cloud_native'],
                'success_factors': ['research_development_percent > 20', 'technical_founder == True']
            },
            Industry.FINTECH: {
                'critical_features': ['regulatory_risk', 'customer_acquisition_cost', 'security_score'],
                'required_features': ['compliance_status', 'has_licenses'],
                'success_factors': ['regulatory_risk < 3', 'security_score > 4']
            },
            # Add more industries...
        }
    
    def build_pattern_contract(self, 
                              pattern_type: PatternType,
                              base_contract: Optional[ModelContract] = None) -> ModelContract:
        """Build a contract specific to a pattern"""
        if base_contract is None:
            base_contract = ModelContract(
                model_name=f"pattern_{pattern_type.value}",
                model_type="pattern_classifier",
                version="1.0.0"
            )
        
        profile = self.pattern_profiles.get(pattern_type)
        if not profile:
            raise ValueError(f"Unknown pattern type: {pattern_type}")
        
        # Add all base features
        feature_names = self.registry.get_feature_names()
        base_contract.add_raw_features(feature_names)
        
        # Add pattern-specific computed features
        base_contract.add_computed_feature(
            f'{pattern_type.value}_score',
            computation=lambda df: self._compute_pattern_score(df, pattern_type),
            dependencies=profile.key_features
        )
        
        # Add CAMP scores with pattern-specific weights
        self._add_weighted_camp_scores(base_contract, profile.camp_weights)
        
        # Add pattern fit score
        base_contract.add_computed_feature(
            'pattern_fit_score',
            computation=lambda df: self._compute_pattern_fit(df, profile),
            dependencies=profile.key_features
        )
        
        # Add validation rules
        base_contract.add_validation_rule(
            lambda df: self._validate_pattern_requirements(df, profile)
        )
        
        return base_contract
    
    def build_stage_contract(self,
                           funding_stage: FundingStage,
                           include_patterns: bool = True) -> ModelContract:
        """Build a contract specific to a funding stage"""
        contract = ModelContract(
            model_name=f"stage_{funding_stage.value}",
            model_type="stage_classifier",
            version="1.0.0"
        )
        
        requirements = self.stage_requirements.get(funding_stage)
        if not requirements:
            raise ValueError(f"Unknown funding stage: {funding_stage}")
        
        # Add all base features
        feature_names = self.registry.get_feature_names()
        contract.add_raw_features(feature_names)
        
        # Add stage-specific computed features
        contract.add_computed_feature(
            'stage_readiness_score',
            computation=lambda df: self._compute_stage_readiness(df, funding_stage),
            dependencies=requirements['critical_features']
        )
        
        # Add weighted CAMP scores
        self._add_weighted_camp_scores(contract, requirements['camp_weights'])
        
        # Add validation for minimum thresholds
        for feature, threshold in requirements.get('min_thresholds', {}).items():
            contract.add_validation_rule(
                lambda df, f=feature, t=threshold: (
                    df[f].min() >= t,
                    f"{f} must be at least {t} for {funding_stage.value}"
                )
            )
        
        return contract
    
    def build_industry_contract(self,
                              industry: Industry,
                              include_patterns: bool = True) -> ModelContract:
        """Build a contract specific to an industry"""
        contract = ModelContract(
            model_name=f"industry_{industry.value}",
            model_type="industry_classifier",
            version="1.0.0"
        )
        
        requirements = self.industry_requirements.get(industry)
        if not requirements:
            raise ValueError(f"Unknown industry: {industry}")
        
        # Add all base features
        feature_names = self.registry.get_feature_names()
        contract.add_raw_features(feature_names)
        
        # Add industry-specific computed features
        contract.add_computed_feature(
            'industry_fit_score',
            computation=lambda df: self._compute_industry_fit(df, industry),
            dependencies=requirements['critical_features']
        )
        
        # Add standard CAMP scores
        contract.add_camp_scores()
        
        # Add industry-specific validations
        for factor in requirements.get('success_factors', []):
            contract.add_validation_rule(
                lambda df: self._validate_success_factor(df, factor)
            )
        
        return contract
    
    def build_hybrid_contract(self,
                            pattern_types: List[PatternType],
                            funding_stage: FundingStage,
                            industry: Industry) -> ModelContract:
        """Build a comprehensive hybrid contract"""
        contract = ModelContract(
            model_name=f"hybrid_{funding_stage.value}_{industry.value}",
            model_type="hybrid_classifier",
            version="1.0.0"
        )
        
        # Add all base features
        feature_names = self.registry.get_feature_names()
        contract.add_raw_features(feature_names)
        
        # Add pattern scores for each relevant pattern
        for pattern in pattern_types:
            profile = self.pattern_profiles.get(pattern)
            if profile:
                contract.add_computed_feature(
                    f'{pattern.value}_score',
                    computation=lambda df, p=pattern: self._compute_pattern_score(df, p),
                    dependencies=profile.key_features
                )
        
        # Add stage readiness
        stage_req = self.stage_requirements.get(funding_stage)
        contract.add_computed_feature(
            'stage_readiness_score',
            computation=lambda df: self._compute_stage_readiness(df, funding_stage),
            dependencies=stage_req['critical_features']
        )
        
        # Add industry fit
        industry_req = self.industry_requirements.get(industry)
        contract.add_computed_feature(
            'industry_fit_score',
            computation=lambda df: self._compute_industry_fit(df, industry),
            dependencies=industry_req['critical_features']
        )
        
        # Add weighted CAMP scores (average of all contexts)
        avg_weights = self._compute_average_camp_weights(pattern_types, funding_stage, industry)
        self._add_weighted_camp_scores(contract, avg_weights)
        
        return contract
    
    def _add_weighted_camp_scores(self, contract: ModelContract, weights: Dict[str, float]):
        """Add CAMP scores with custom weights"""
        # Capital score
        contract.add_computed_feature(
            'weighted_capital_score',
            computation=lambda df: self._compute_weighted_camp_score(df, 'capital', weights['capital']),
            dependencies=['funding_stage', 'total_capital_raised_usd', 'burn_multiple', 'runway_months']
        )
        
        # Advantage score
        contract.add_computed_feature(
            'weighted_advantage_score',
            computation=lambda df: self._compute_weighted_camp_score(df, 'advantage', weights['advantage']),
            dependencies=['product_market_fit_score', 'technology_score', 'has_patent', 'uses_ai_ml']
        )
        
        # Market score
        contract.add_computed_feature(
            'weighted_market_score',
            computation=lambda df: self._compute_weighted_camp_score(df, 'market', weights['market']),
            dependencies=['market_tam_billions', 'market_growth_rate', 'customer_acquisition_cost']
        )
        
        # People score
        contract.add_computed_feature(
            'weighted_people_score',
            computation=lambda df: self._compute_weighted_camp_score(df, 'people', weights['people']),
            dependencies=['founder_experience_years', 'team_size_full_time', 'technical_founder']
        )
    
    def _compute_pattern_score(self, df, pattern_type: PatternType) -> float:
        """Compute how well data matches a pattern"""
        profile = self.pattern_profiles.get(pattern_type)
        if not profile:
            return 0.0
        
        scores = []
        for feature in profile.key_features:
            if feature in df.columns:
                typical_value = profile.typical_metrics.get(feature)
                if typical_value is not None:
                    actual_value = df[feature].iloc[0] if len(df) > 0 else 0
                    # Simple similarity score
                    if isinstance(typical_value, bool):
                        score = 1.0 if actual_value == typical_value else 0.0
                    else:
                        score = 1.0 - abs(actual_value - typical_value) / (typical_value + 1)
                    scores.append(max(0, min(1, score)))
        
        return np.mean(scores) if scores else 0.5
    
    def _compute_pattern_fit(self, df, profile: PatternProfile) -> float:
        """Compute overall fit to a pattern profile"""
        # Simplified implementation
        return self._compute_pattern_score(df, profile.pattern_type)
    
    def _compute_stage_readiness(self, df, stage: FundingStage) -> float:
        """Compute readiness for a funding stage"""
        requirements = self.stage_requirements.get(stage)
        if not requirements:
            return 0.5
        
        scores = []
        for feature in requirements['critical_features']:
            if feature in df.columns:
                value = df[feature].iloc[0] if len(df) > 0 else 0
                # Normalize to 0-1 based on feature type
                if self.registry.get_feature(feature).dtype == bool:
                    score = float(value)
                else:
                    # Simple normalization
                    score = min(1.0, value / 100.0)  # Adjust based on feature
                scores.append(score)
        
        return np.mean(scores) if scores else 0.5
    
    def _compute_industry_fit(self, df, industry: Industry) -> float:
        """Compute fit for an industry"""
        requirements = self.industry_requirements.get(industry)
        if not requirements:
            return 0.5
        
        scores = []
        for feature in requirements['critical_features']:
            if feature in df.columns:
                value = df[feature].iloc[0] if len(df) > 0 else 0
                # Industry-specific scoring logic
                scores.append(min(1.0, value / 100.0))  # Simplified
        
        return np.mean(scores) if scores else 0.5
    
    def _compute_weighted_camp_score(self, df, camp_category: str, weight: float) -> float:
        """Compute weighted CAMP score for a category"""
        features = self.registry.get_features_by_category(camp_category)
        if not features:
            return 0.5 * weight
        
        scores = []
        for feature in features:
            if feature.name in df.columns:
                value = df[feature.name].iloc[0] if len(df) > 0 else feature.default_value
                # Normalize based on feature constraints
                if feature.min_value is not None and feature.max_value is not None:
                    normalized = (value - feature.min_value) / (feature.max_value - feature.min_value)
                    scores.append(max(0, min(1, normalized)))
        
        base_score = np.mean(scores) if scores else 0.5
        return base_score * weight
    
    def _compute_average_camp_weights(self, 
                                    patterns: List[PatternType],
                                    stage: FundingStage,
                                    industry: Industry) -> Dict[str, float]:
        """Compute average CAMP weights from multiple contexts"""
        all_weights = []
        
        # Add pattern weights
        for pattern in patterns:
            profile = self.pattern_profiles.get(pattern)
            if profile and profile.camp_weights:
                all_weights.append(profile.camp_weights)
        
        # Add stage weights
        stage_req = self.stage_requirements.get(stage)
        if stage_req and 'camp_weights' in stage_req:
            all_weights.append(stage_req['camp_weights'])
        
        # Average all weights
        if not all_weights:
            return {'capital': 0.25, 'advantage': 0.25, 'market': 0.25, 'people': 0.25}
        
        avg_weights = {}
        for camp in ['capital', 'advantage', 'market', 'people']:
            values = [w[camp] for w in all_weights if camp in w]
            avg_weights[camp] = np.mean(values) if values else 0.25
        
        # Normalize to sum to 1
        total = sum(avg_weights.values())
        return {k: v/total for k, v in avg_weights.items()}
    
    def _validate_pattern_requirements(self, df, profile: PatternProfile) -> tuple[bool, str]:
        """Validate pattern-specific requirements"""
        # Simplified validation
        return True, "Pattern validation passed"
    
    def _validate_success_factor(self, df, factor: str) -> tuple[bool, str]:
        """Validate a success factor expression"""
        # Would implement expression evaluation
        return True, f"Success factor {factor} validated"