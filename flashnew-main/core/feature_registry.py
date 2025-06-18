"""
Feature Registry - Single Source of Truth for All Features
This replaces all scattered feature configurations with a central registry
"""

from collections import OrderedDict
from typing import Callable, Dict, List, Optional, Any, Union
import pandas as pd
import numpy as np
from datetime import datetime
import json
import logging

logger = logging.getLogger(__name__)


class FeatureDefinition:
    """Complete definition of a single feature"""
    
    def __init__(self, 
                 name: str,
                 position: int,
                 dtype: type,
                 category: str,
                 description: str = "",
                 min_value: Optional[float] = None,
                 max_value: Optional[float] = None,
                 allowed_values: Optional[List[Any]] = None,
                 default_value: Optional[Any] = None,
                 validator: Optional[Callable] = None,
                 transformer: Optional[Callable] = None,
                 is_required: bool = True):
        self.name = name
        self.position = position
        self.dtype = dtype
        self.category = category  # CAMP category: capital, advantage, market, people, product
        self.description = description
        self.min_value = min_value
        self.max_value = max_value
        self.allowed_values = allowed_values
        self.default_value = default_value
        self.validator = validator
        self.transformer = transformer
        self.is_required = is_required
    
    def validate(self, value: Any) -> tuple[bool, Optional[str]]:
        """Validate a single value against this feature's constraints"""
        # Check if None and required
        if value is None:
            if self.is_required:
                return False, f"{self.name} is required but got None"
            else:
                return True, None
        
        # Type check
        try:
            if self.dtype in (int, float):
                value = self.dtype(value)
            elif self.dtype == bool:
                if isinstance(value, str):
                    value = value.lower() in ('true', '1', 'yes')
        except (ValueError, TypeError):
            return False, f"{self.name} should be {self.dtype.__name__} but got {type(value).__name__}"
        
        # Range check
        if self.min_value is not None and value < self.min_value:
            return False, f"{self.name} = {value} is below minimum {self.min_value}"
        if self.max_value is not None and value > self.max_value:
            return False, f"{self.name} = {value} is above maximum {self.max_value}"
        
        # Allowed values check
        if self.allowed_values is not None and value not in self.allowed_values:
            return False, f"{self.name} = {value} not in allowed values: {self.allowed_values}"
        
        # Custom validator
        if self.validator:
            try:
                if not self.validator(value):
                    return False, f"{self.name} failed custom validation"
            except Exception as e:
                return False, f"{self.name} validator error: {str(e)}"
        
        return True, None
    
    def transform(self, value: Any) -> Any:
        """Transform value if transformer is defined"""
        if self.transformer:
            return self.transformer(value)
        return value
    
    def to_dict(self) -> Dict:
        """Serialize feature definition"""
        return {
            'name': self.name,
            'position': self.position,
            'dtype': self.dtype.__name__,
            'category': self.category,
            'description': self.description,
            'min_value': self.min_value,
            'max_value': self.max_value,
            'allowed_values': self.allowed_values,
            'default_value': self.default_value,
            'is_required': self.is_required
        }


class FeatureRegistry:
    """Central registry for all features in the system"""
    
    def __init__(self):
        self.features: OrderedDict[str, FeatureDefinition] = OrderedDict()
        self.version = "1.0.0"
        self.created_at = datetime.now()
        self._initialize_core_features()
    
    def _initialize_core_features(self):
        """Initialize the 45 core features in exact dataset order"""
        # Based on the actual dataset: data/final_100k_dataset_45features.csv
        
        # Capital features (positions 0-6)
        self.register_feature(
            name="funding_stage",
            position=0,
            dtype=str,
            category="capital",
            description="Current funding stage of the startup",
            allowed_values=["pre_seed", "seed", "series_a", "series_b", "series_c", "series_d_plus"],
            default_value="seed"
        )
        
        self.register_feature(
            name="revenue_growth_rate",
            position=1,
            dtype=float,
            category="capital",
            description="Revenue growth rate as a percentage",
            min_value=-100,
            max_value=1000,
            default_value=0
        )
        
        self.register_feature(
            name="team_size_full_time",
            position=2,
            dtype=int,
            category="people",
            description="Number of full-time employees",
            min_value=0,
            max_value=10000,
            default_value=1
        )
        
        self.register_feature(
            name="total_capital_raised_usd",
            position=3,
            dtype=float,
            category="capital",
            description="Total capital raised in USD",
            min_value=0,
            max_value=10_000_000_000,
            default_value=0
        )
        
        self.register_feature(
            name="annual_recurring_revenue_millions",
            position=4,
            dtype=float,
            category="capital",
            description="Annual recurring revenue in millions USD",
            min_value=0,
            max_value=10000,
            default_value=0
        )
        
        self.register_feature(
            name="annual_revenue_run_rate",
            position=5,
            dtype=float,
            category="capital",
            description="Annual revenue run rate",
            min_value=0,
            max_value=10_000_000_000,
            default_value=0
        )
        
        self.register_feature(
            name="burn_multiple",
            position=6,
            dtype=float,
            category="capital",
            description="Burn multiple (burn rate / growth rate)",
            min_value=0,
            max_value=100,
            default_value=2.0
        )
        
        # Market features (positions 7-17)
        self.register_feature(
            name="market_tam_billions",
            position=7,
            dtype=float,
            category="market",
            description="Total addressable market in billions USD",
            min_value=0,
            max_value=10000,
            default_value=1
        )
        
        self.register_feature(
            name="market_growth_rate",
            position=8,
            dtype=float,
            category="market",
            description="Market growth rate percentage",
            min_value=-50,
            max_value=500,
            default_value=10
        )
        
        self.register_feature(
            name="market_competitiveness",
            position=9,
            dtype=int,
            category="market",
            description="Market competitiveness score (1-5)",
            min_value=1,
            max_value=5,
            default_value=3
        )
        
        self.register_feature(
            name="customer_acquisition_cost",
            position=10,
            dtype=float,
            category="market",
            description="Customer acquisition cost in USD",
            min_value=0,
            max_value=100000,
            default_value=100
        )
        
        self.register_feature(
            name="customer_lifetime_value",
            position=11,
            dtype=float,
            category="market",
            description="Customer lifetime value in USD",
            min_value=0,
            max_value=1000000,
            default_value=1000
        )
        
        self.register_feature(
            name="customer_growth_rate",
            position=12,
            dtype=float,
            category="market",
            description="Customer growth rate percentage",
            min_value=-100,
            max_value=1000,
            default_value=0
        )
        
        self.register_feature(
            name="net_revenue_retention",
            position=13,
            dtype=float,
            category="market",
            description="Net revenue retention percentage",
            min_value=0,
            max_value=300,
            default_value=100
        )
        
        self.register_feature(
            name="average_deal_size",
            position=14,
            dtype=float,
            category="market",
            description="Average deal size in USD",
            min_value=0,
            max_value=10000000,
            default_value=1000
        )
        
        self.register_feature(
            name="sales_cycle_days",
            position=15,
            dtype=int,
            category="market",
            description="Average sales cycle in days",
            min_value=0,
            max_value=1000,
            default_value=30
        )
        
        self.register_feature(
            name="international_revenue_percent",
            position=16,
            dtype=float,
            category="market",
            description="Percentage of revenue from international markets",
            min_value=0,
            max_value=100,
            default_value=0
        )
        
        self.register_feature(
            name="target_enterprise",
            position=17,
            dtype=bool,
            category="market",
            description="Whether targeting enterprise customers",
            default_value=False
        )
        
        # Product/Advantage features (positions 18-26)
        self.register_feature(
            name="product_market_fit_score",
            position=18,
            dtype=int,
            category="advantage",
            description="Product-market fit score (1-5)",
            min_value=1,
            max_value=5,
            default_value=3
        )
        
        self.register_feature(
            name="technology_score",
            position=19,
            dtype=int,
            category="advantage",
            description="Technology innovation score (1-5)",
            min_value=1,
            max_value=5,
            default_value=3
        )
        
        self.register_feature(
            name="scalability_score",
            position=20,
            dtype=int,
            category="advantage",
            description="Scalability score (1-5)",
            min_value=1,
            max_value=5,
            default_value=3
        )
        
        self.register_feature(
            name="has_patent",
            position=21,
            dtype=bool,
            category="advantage",
            description="Whether company has patents",
            default_value=False
        )
        
        self.register_feature(
            name="research_development_percent",
            position=22,
            dtype=float,
            category="advantage",
            description="R&D spending as percentage of revenue",
            min_value=0,
            max_value=100,
            default_value=10
        )
        
        self.register_feature(
            name="uses_ai_ml",
            position=23,
            dtype=bool,
            category="advantage",
            description="Whether product uses AI/ML",
            default_value=False
        )
        
        self.register_feature(
            name="cloud_native",
            position=24,
            dtype=bool,
            category="advantage",
            description="Whether product is cloud-native",
            default_value=True
        )
        
        self.register_feature(
            name="mobile_first",
            position=25,
            dtype=bool,
            category="advantage",
            description="Whether product is mobile-first",
            default_value=False
        )
        
        self.register_feature(
            name="platform_business",
            position=26,
            dtype=bool,
            category="product",
            description="Whether it's a platform business model",
            default_value=False
        )
        
        # People features (positions 27-35)
        self.register_feature(
            name="founder_experience_years",
            position=27,
            dtype=int,
            category="people",
            description="Founder's years of relevant experience",
            min_value=0,
            max_value=50,
            default_value=5
        )
        
        self.register_feature(
            name="repeat_founder",
            position=28,
            dtype=bool,
            category="people",
            description="Whether founder has started companies before",
            default_value=False
        )
        
        self.register_feature(
            name="technical_founder",
            position=29,
            dtype=bool,
            category="people",
            description="Whether there's a technical co-founder",
            default_value=True
        )
        
        self.register_feature(
            name="employee_growth_rate",
            position=30,
            dtype=float,
            category="people",
            description="Employee growth rate percentage",
            min_value=-100,
            max_value=1000,
            default_value=0
        )
        
        self.register_feature(
            name="advisor_quality_score",
            position=31,
            dtype=int,
            category="people",
            description="Quality of advisors score (1-5)",
            min_value=1,
            max_value=5,
            default_value=3
        )
        
        self.register_feature(
            name="board_diversity_score",
            position=32,
            dtype=int,
            category="people",
            description="Board diversity score (1-5)",
            min_value=1,
            max_value=5,
            default_value=3
        )
        
        self.register_feature(
            name="team_industry_experience",
            position=33,
            dtype=int,
            category="people",
            description="Average team industry experience in years",
            min_value=0,
            max_value=50,
            default_value=5
        )
        
        self.register_feature(
            name="key_person_dependency",
            position=34,
            dtype=int,
            category="people",
            description="Key person dependency risk (1-5, lower is better)",
            min_value=1,
            max_value=5,
            default_value=3
        )
        
        self.register_feature(
            name="top_university_alumni",
            position=35,
            dtype=bool,
            category="people",
            description="Whether founders are from top universities",
            default_value=False
        )
        
        # Additional features (positions 36-44)
        self.register_feature(
            name="investor_tier_primary",
            position=36,
            dtype=str,
            category="capital",
            description="Primary investor tier",
            allowed_values=["tier_1", "tier_2", "tier_3"],
            default_value="tier_2"
        )
        
        self.register_feature(
            name="active_investors",
            position=37,
            dtype=int,
            category="capital",
            description="Number of active investors",
            min_value=0,
            max_value=100,
            default_value=1
        )
        
        self.register_feature(
            name="cash_on_hand_months",
            position=38,
            dtype=float,
            category="capital",
            description="Runway in months",
            min_value=0,
            max_value=120,
            default_value=12
        )
        
        self.register_feature(
            name="runway_months",
            position=39,
            dtype=float,
            category="capital",
            description="Calculated runway in months",
            min_value=0,
            max_value=120,
            default_value=12
        )
        
        self.register_feature(
            name="time_to_next_funding",
            position=40,
            dtype=int,
            category="capital",
            description="Expected months to next funding",
            min_value=0,
            max_value=60,
            default_value=12
        )
        
        self.register_feature(
            name="previous_exit",
            position=41,
            dtype=bool,
            category="people",
            description="Whether founders have previous exits",
            default_value=False
        )
        
        self.register_feature(
            name="industry_connections",
            position=42,
            dtype=int,
            category="people",
            description="Industry connections score (1-5)",
            min_value=1,
            max_value=5,
            default_value=3
        )
        
        self.register_feature(
            name="media_coverage",
            position=43,
            dtype=int,
            category="market",
            description="Media coverage score (1-5)",
            min_value=1,
            max_value=5,
            default_value=3
        )
        
        self.register_feature(
            name="regulatory_risk",
            position=44,
            dtype=int,
            category="market",
            description="Regulatory risk score (1-5, lower is better)",
            min_value=1,
            max_value=5,
            default_value=3
        )
    
    def register_feature(self, 
                        name: str,
                        position: int,
                        dtype: type,
                        category: str,
                        description: str = "",
                        min_value: Optional[float] = None,
                        max_value: Optional[float] = None,
                        allowed_values: Optional[List[Any]] = None,
                        default_value: Optional[Any] = None,
                        validator: Optional[Callable] = None,
                        transformer: Optional[Callable] = None,
                        is_required: bool = True):
        """Register a feature with all its metadata"""
        if name in self.features:
            raise ValueError(f"Feature {name} already registered")
        
        feature = FeatureDefinition(
            name=name,
            position=position,
            dtype=dtype,
            category=category,
            description=description,
            min_value=min_value,
            max_value=max_value,
            allowed_values=allowed_values,
            default_value=default_value,
            validator=validator,
            transformer=transformer,
            is_required=is_required
        )
        
        self.features[name] = feature
        logger.info(f"Registered feature: {name} at position {position}")
    
    def get_feature(self, name: str) -> FeatureDefinition:
        """Get a feature definition by name"""
        if name not in self.features:
            raise KeyError(f"Feature {name} not found in registry")
        return self.features[name]
    
    def get_features_by_category(self, category: str) -> List[FeatureDefinition]:
        """Get all features in a category"""
        return [f for f in self.features.values() if f.category == category]
    
    def get_feature_names(self) -> List[str]:
        """Get ordered list of feature names"""
        return list(self.features.keys())
    
    def get_feature_positions(self) -> Dict[str, int]:
        """Get feature name to position mapping"""
        return {name: feat.position for name, feat in self.features.items()}
    
    def get_schema(self) -> pd.DataFrame:
        """Return feature schema as DataFrame"""
        data = []
        for name, feature in self.features.items():
            data.append({
                'name': name,
                'position': feature.position,
                'dtype': feature.dtype.__name__,
                'category': feature.category,
                'description': feature.description,
                'min_value': feature.min_value,
                'max_value': feature.max_value,
                'default_value': feature.default_value,
                'is_required': feature.is_required
            })
        return pd.DataFrame(data)
    
    def validate_dataframe(self, df: pd.DataFrame) -> tuple[bool, List[str]]:
        """Validate a dataframe against registry"""
        errors = []
        
        # Check all required features are present
        required_features = [name for name, feat in self.features.items() if feat.is_required]
        missing = set(required_features) - set(df.columns)
        if missing:
            errors.append(f"Missing required features: {missing}")
        
        # Check column order matches position
        if len(df.columns) == len(self.features):
            for i, col in enumerate(df.columns):
                if col in self.features:
                    expected_pos = self.features[col].position
                    if i != expected_pos:
                        errors.append(f"Feature {col} at position {i}, expected {expected_pos}")
        
        # Validate each row
        for idx, row in df.iterrows():
            for col in df.columns:
                if col in self.features:
                    is_valid, error = self.features[col].validate(row[col])
                    if not is_valid:
                        errors.append(f"Row {idx}: {error}")
                        if len(errors) > 100:  # Limit error messages
                            errors.append("... (truncated)")
                            return False, errors
        
        return len(errors) == 0, errors
    
    def validate_dict(self, data: Dict[str, Any]) -> tuple[bool, List[str]]:
        """Validate a dictionary of features"""
        errors = []
        
        # Check required features
        for name, feature in self.features.items():
            if feature.is_required and name not in data:
                errors.append(f"Missing required feature: {name}")
            elif name in data:
                is_valid, error = feature.validate(data[name])
                if not is_valid:
                    errors.append(error)
        
        # Check for unknown features
        unknown = set(data.keys()) - set(self.features.keys())
        if unknown:
            errors.append(f"Unknown features: {unknown}")
        
        return len(errors) == 0, errors
    
    def transform_dict(self, data: Dict[str, Any], fill_defaults: bool = True) -> Dict[str, Any]:
        """Transform and validate input dictionary"""
        result = {}
        
        for name, feature in self.features.items():
            if name in data:
                # Transform if transformer exists
                value = feature.transform(data[name])
                result[name] = value
            elif fill_defaults and feature.default_value is not None:
                result[name] = feature.default_value
            elif feature.is_required:
                raise ValueError(f"Required feature {name} not provided and has no default")
        
        return result
    
    def to_array(self, data: Dict[str, Any]) -> np.ndarray:
        """Convert dictionary to ordered array based on positions"""
        # First transform and fill defaults
        data = self.transform_dict(data, fill_defaults=True)
        
        # Create array in position order
        array = np.zeros(len(self.features))
        for name, feature in self.features.items():
            if name in data:
                value = data[name]
                # Handle categorical to numeric conversion
                if feature.dtype == str:
                    # This should be handled by model-specific encoders
                    # For now, we'll leave as-is
                    if feature.allowed_values:
                        value = feature.allowed_values.index(value) if value in feature.allowed_values else 0
                    else:
                        value = 0  # Placeholder
                elif feature.dtype == bool:
                    value = float(value)
                
                array[feature.position] = value
        
        return array
    
    def save(self, path: str):
        """Save registry to file"""
        data = {
            'version': self.version,
            'created_at': self.created_at.isoformat(),
            'features': [feat.to_dict() for feat in self.features.values()]
        }
        with open(path, 'w') as f:
            json.dump(data, f, indent=2)
    
    @classmethod
    def load(cls, path: str) -> 'FeatureRegistry':
        """Load registry from file"""
        with open(path, 'r') as f:
            data = json.load(f)
        
        registry = cls()
        registry.version = data['version']
        registry.created_at = datetime.fromisoformat(data['created_at'])
        
        # Clear and reload features
        registry.features.clear()
        for feat_data in data['features']:
            # Convert dtype string back to type
            dtype_map = {
                'int': int,
                'float': float,
                'str': str,
                'bool': bool
            }
            feat_data['dtype'] = dtype_map[feat_data['dtype']]
            
            registry.register_feature(**feat_data)
        
        return registry


# Create singleton instance
feature_registry = FeatureRegistry()