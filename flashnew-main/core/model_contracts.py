"""
Model Contract System - Define exact input/output specifications for each model
Ensures models can never receive wrong features or feature counts
"""

from typing import List, Dict, Callable, Optional, Any, Union
import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer
import json
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class FeatureSpecification:
    """Specification for a single input feature"""
    
    def __init__(self,
                 name: str,
                 source: str = 'raw',  # raw, derived, computed
                 computation: Optional[Callable] = None,
                 dependencies: Optional[List[str]] = None):
        self.name = name
        self.source = source
        self.computation = computation
        self.dependencies = dependencies or []
        
        # Validate
        if source == 'computed' and computation is None:
            raise ValueError(f"Computed feature {name} requires a computation function")
        if source == 'raw' and computation is not None:
            raise ValueError(f"Raw feature {name} should not have a computation function")
    
    def to_dict(self) -> Dict:
        """Serialize feature specification"""
        return {
            'name': self.name,
            'source': self.source,
            'dependencies': self.dependencies,
            'has_computation': self.computation is not None
        }


class ModelContract:
    """Define exact input/output contract for a model"""
    
    def __init__(self, 
                 model_name: str,
                 model_type: str,  # classifier, regressor, ensemble
                 version: str = "1.0.0"):
        self.model_name = model_name
        self.model_type = model_type
        self.version = version
        self.created_at = datetime.now()
        
        # Input specifications
        self.input_features: List[FeatureSpecification] = []
        self.feature_count: int = 0
        
        # Output specifications
        self.output_schema = {
            'primary': 'probability',  # Default for classifiers
            'type': 'float',
            'range': [0.0, 1.0]
        }
        
        # Preprocessing pipeline (built from contract)
        self.preprocessing_pipeline: Optional[Pipeline] = None
        
        # Validation rules
        self.validation_rules: List[Callable] = []
        
        # Model-specific metadata
        self.metadata: Dict[str, Any] = {}
    
    def add_raw_feature(self, feature_name: str) -> 'ModelContract':
        """Add a raw feature from the dataset"""
        spec = FeatureSpecification(
            name=feature_name,
            source='raw'
        )
        self.input_features.append(spec)
        self.feature_count += 1
        return self
    
    def add_raw_features(self, feature_names: List[str]) -> 'ModelContract':
        """Add multiple raw features"""
        for name in feature_names:
            self.add_raw_feature(name)
        return self
    
    def add_computed_feature(self, 
                           feature_name: str,
                           computation: Callable,
                           dependencies: List[str]) -> 'ModelContract':
        """Add a computed feature with its computation function"""
        spec = FeatureSpecification(
            name=feature_name,
            source='computed',
            computation=computation,
            dependencies=dependencies
        )
        self.input_features.append(spec)
        self.feature_count += 1
        return self
    
    def add_camp_scores(self) -> 'ModelContract':
        """Add standard CAMP score computations"""
        # Capital score
        self.add_computed_feature(
            'capital_score',
            computation=lambda df: df[[
                'funding_stage', 'total_capital_raised_usd', 
                'annual_recurring_revenue_millions', 'burn_multiple',
                'investor_tier_primary', 'active_investors', 'runway_months'
            ]].mean(axis=1),
            dependencies=['funding_stage', 'total_capital_raised_usd', 
                         'annual_recurring_revenue_millions', 'burn_multiple',
                         'investor_tier_primary', 'active_investors', 'runway_months']
        )
        
        # Advantage score
        self.add_computed_feature(
            'advantage_score',
            computation=lambda df: df[[
                'product_market_fit_score', 'technology_score', 'scalability_score',
                'has_patent', 'research_development_percent', 'uses_ai_ml',
                'cloud_native', 'mobile_first'
            ]].mean(axis=1),
            dependencies=['product_market_fit_score', 'technology_score', 'scalability_score',
                         'has_patent', 'research_development_percent', 'uses_ai_ml',
                         'cloud_native', 'mobile_first']
        )
        
        # Market score
        self.add_computed_feature(
            'market_score',
            computation=lambda df: df[[
                'market_tam_billions', 'market_growth_rate', 'customer_acquisition_cost',
                'customer_lifetime_value', 'net_revenue_retention', 'international_revenue_percent',
                'target_enterprise', 'media_coverage', 'regulatory_risk'
            ]].mean(axis=1),
            dependencies=['market_tam_billions', 'market_growth_rate', 'customer_acquisition_cost',
                         'customer_lifetime_value', 'net_revenue_retention', 'international_revenue_percent',
                         'target_enterprise', 'media_coverage', 'regulatory_risk']
        )
        
        # People score
        self.add_computed_feature(
            'people_score',
            computation=lambda df: df[[
                'team_size_full_time', 'founder_experience_years', 'repeat_founder',
                'technical_founder', 'employee_growth_rate', 'advisor_quality_score',
                'team_industry_experience', 'top_university_alumni', 'previous_exit'
            ]].mean(axis=1),
            dependencies=['team_size_full_time', 'founder_experience_years', 'repeat_founder',
                         'technical_founder', 'employee_growth_rate', 'advisor_quality_score',
                         'team_industry_experience', 'top_university_alumni', 'previous_exit']
        )
        
        return self
    
    def add_temporal_features(self) -> 'ModelContract':
        """Add temporal feature computations"""
        self.add_computed_feature(
            'time_momentum',
            computation=lambda df: df['revenue_growth_rate'] * df['customer_growth_rate'] / 100,
            dependencies=['revenue_growth_rate', 'customer_growth_rate']
        )
        
        self.add_computed_feature(
            'growth_efficiency',
            computation=lambda df: df['revenue_growth_rate'] / (df['burn_multiple'] + 1),
            dependencies=['revenue_growth_rate', 'burn_multiple']
        )
        
        self.add_computed_feature(
            'market_timing',
            computation=lambda df: df['market_growth_rate'] * (1 - df['market_competitiveness'] / 5),
            dependencies=['market_growth_rate', 'market_competitiveness']
        )
        
        return self
    
    def set_output_schema(self, 
                         primary_output: str,
                         output_type: str,
                         output_range: Optional[List[float]] = None) -> 'ModelContract':
        """Define the output schema"""
        self.output_schema = {
            'primary': primary_output,
            'type': output_type,
            'range': output_range
        }
        return self
    
    def add_validation_rule(self, rule: Callable) -> 'ModelContract':
        """Add a validation rule for inputs"""
        self.validation_rules.append(rule)
        return self
    
    def build_preprocessing_pipeline(self) -> Pipeline:
        """Build sklearn Pipeline from contract specifications"""
        steps = []
        
        # Group features by source
        computed_features = [f for f in self.input_features if f.source == 'computed']
        
        if computed_features:
            # Create a transformer that adds computed features
            def add_computed_features(X):
                """Add all computed features to the dataframe"""
                X_copy = X.copy()
                
                for feature in computed_features:
                    try:
                        X_copy[feature.name] = feature.computation(X_copy)
                    except Exception as e:
                        logger.error(f"Failed to compute {feature.name}: {e}")
                        # Use a default value or raise
                        X_copy[feature.name] = 0
                
                return X_copy
            
            steps.append(('add_computed', FunctionTransformer(add_computed_features)))
        
        # Select only the features specified in the contract
        feature_names = [f.name for f in self.input_features]
        
        def select_contract_features(X):
            """Select only features specified in contract"""
            return X[feature_names]
        
        steps.append(('select_features', FunctionTransformer(select_contract_features)))
        
        self.preprocessing_pipeline = Pipeline(steps)
        return self.preprocessing_pipeline
    
    def validate_input(self, data: Union[pd.DataFrame, Dict]) -> tuple[bool, List[str]]:
        """Validate input data against contract"""
        errors = []
        
        # Convert dict to dataframe if needed
        if isinstance(data, dict):
            data = pd.DataFrame([data])
        
        # Check required raw features exist
        raw_features = [f.name for f in self.input_features if f.source == 'raw']
        missing = set(raw_features) - set(data.columns)
        if missing:
            errors.append(f"Missing required features: {missing}")
        
        # Check dependencies for computed features
        computed_features = [f for f in self.input_features if f.source == 'computed']
        for feature in computed_features:
            missing_deps = set(feature.dependencies) - set(data.columns)
            if missing_deps:
                errors.append(f"Cannot compute {feature.name}, missing: {missing_deps}")
        
        # Run custom validation rules
        for rule in self.validation_rules:
            try:
                is_valid, error = rule(data)
                if not is_valid:
                    errors.append(error)
            except Exception as e:
                errors.append(f"Validation rule failed: {str(e)}")
        
        return len(errors) == 0, errors
    
    def prepare_features(self, data: Union[pd.DataFrame, Dict]) -> np.ndarray:
        """Prepare features according to contract"""
        # Validate first
        is_valid, errors = self.validate_input(data)
        if not is_valid:
            raise ValueError(f"Input validation failed: {errors}")
        
        # Convert dict to dataframe if needed
        if isinstance(data, dict):
            data = pd.DataFrame([data])
        
        # Build pipeline if not exists
        if self.preprocessing_pipeline is None:
            self.build_preprocessing_pipeline()
        
        # Transform data
        transformed = self.preprocessing_pipeline.transform(data)
        
        # Convert to numpy array
        if isinstance(transformed, pd.DataFrame):
            return transformed.values
        return transformed
    
    def get_feature_names(self) -> List[str]:
        """Get ordered list of all feature names"""
        return [f.name for f in self.input_features]
    
    def get_dependency_graph(self) -> Dict[str, List[str]]:
        """Get feature dependency graph"""
        graph = {}
        for feature in self.input_features:
            if feature.source == 'computed':
                graph[feature.name] = feature.dependencies
        return graph
    
    def to_dict(self) -> Dict:
        """Serialize contract to dictionary"""
        return {
            'model_name': self.model_name,
            'model_type': self.model_type,
            'version': self.version,
            'created_at': self.created_at.isoformat(),
            'feature_count': self.feature_count,
            'input_features': [f.to_dict() for f in self.input_features],
            'output_schema': self.output_schema,
            'metadata': self.metadata
        }
    
    def save(self, path: str):
        """Save contract to JSON file"""
        with open(path, 'w') as f:
            json.dump(self.to_dict(), f, indent=2)
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'ModelContract':
        """Load contract from dictionary"""
        contract = cls(
            model_name=data['model_name'],
            model_type=data['model_type'],
            version=data['version']
        )
        contract.created_at = datetime.fromisoformat(data['created_at'])
        contract.feature_count = data['feature_count']
        contract.output_schema = data['output_schema']
        contract.metadata = data.get('metadata', {})
        
        # Note: Cannot deserialize computation functions
        # They need to be re-added after loading
        logger.warning("Loaded contract without computation functions - these must be re-added")
        
        return contract
    
    @classmethod
    def load(cls, path: str) -> 'ModelContract':
        """Load contract from JSON file"""
        with open(path, 'r') as f:
            data = json.load(f)
        return cls.from_dict(data)


class ContractBuilder:
    """Helper class to build standard contracts"""
    
    @staticmethod
    def build_dna_analyzer_contract(feature_registry) -> ModelContract:
        """Build contract for DNA Analyzer model (45 base + 4 CAMP = 49 features)"""
        contract = ModelContract(
            model_name="dna_analyzer",
            model_type="classifier",
            version="2.0.0"
        )
        
        # Add all 45 base features
        feature_names = feature_registry.get_feature_names()
        contract.add_raw_features(feature_names)
        
        # Add CAMP scores
        contract.add_camp_scores()
        
        # Add validation rules
        contract.add_validation_rule(
            lambda df: (df.shape[1] >= 45, f"Expected at least 45 features, got {df.shape[1]}")
        )
        
        return contract
    
    @staticmethod
    def build_temporal_model_contract(feature_registry) -> ModelContract:
        """Build contract for Temporal model (45 base + 3 temporal = 48 features)"""
        contract = ModelContract(
            model_name="temporal_model",
            model_type="classifier",
            version="2.0.0"
        )
        
        # Add all 45 base features
        feature_names = feature_registry.get_feature_names()
        contract.add_raw_features(feature_names)
        
        # Add temporal features
        contract.add_temporal_features()
        
        return contract
    
    @staticmethod
    def build_industry_model_contract(feature_registry) -> ModelContract:
        """Build contract for Industry model (45 base features only)"""
        contract = ModelContract(
            model_name="industry_model",
            model_type="classifier",
            version="2.0.0"
        )
        
        # Add all 45 base features
        feature_names = feature_registry.get_feature_names()
        contract.add_raw_features(feature_names)
        
        return contract
    
    @staticmethod
    def build_ensemble_model_contract() -> ModelContract:
        """Build contract for Ensemble model (3 model predictions)"""
        contract = ModelContract(
            model_name="ensemble_model",
            model_type="ensemble",
            version="2.0.0"
        )
        
        # Ensemble takes predictions from other models
        contract.add_raw_feature("dna_prediction")
        contract.add_raw_feature("temporal_prediction")
        contract.add_raw_feature("industry_prediction")
        
        # Different output schema for ensemble
        contract.set_output_schema(
            primary_output="ensemble_probability",
            output_type="float",
            output_range=[0.0, 1.0]
        )
        
        return contract