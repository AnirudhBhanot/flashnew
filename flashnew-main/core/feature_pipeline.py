"""
Unified Feature Engineering Pipeline
Single pipeline that handles all feature transformations for all models
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Any, Union, Tuple
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder, LabelEncoder
from sklearn.impute import SimpleImputer
import logging
from datetime import datetime

from .feature_registry import FeatureRegistry, feature_registry
from .model_contracts import ModelContract

logger = logging.getLogger(__name__)


class CAMPScoreCalculator(BaseEstimator, TransformerMixin):
    """Calculate CAMP scores from raw features"""
    
    def __init__(self, feature_registry: FeatureRegistry):
        self.feature_registry = feature_registry
        self.camp_mappings = self._build_camp_mappings()
    
    def _build_camp_mappings(self) -> Dict[str, List[str]]:
        """Build mapping of CAMP categories to features"""
        mappings = {}
        for category in ['capital', 'advantage', 'market', 'people']:
            features = self.feature_registry.get_features_by_category(category)
            mappings[category] = [f.name for f in features]
        return mappings
    
    def fit(self, X, y=None):
        """Fit method (no-op for this transformer)"""
        return self
    
    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        """Add CAMP scores to dataframe"""
        X_copy = X.copy()
        
        # Normalize features for scoring (0-1 scale)
        for category, feature_names in self.camp_mappings.items():
            # Get numeric features only
            numeric_features = []
            for fname in feature_names:
                if fname in X_copy.columns:
                    feature_def = self.feature_registry.get_feature(fname)
                    if feature_def.dtype in (int, float):
                        numeric_features.append(fname)
            
            if numeric_features:
                # Calculate normalized score
                scores = []
                for fname in numeric_features:
                    feature_def = self.feature_registry.get_feature(fname)
                    values = X_copy[fname].fillna(feature_def.default_value)
                    
                    # Normalize based on min/max if available
                    if feature_def.min_value is not None and feature_def.max_value is not None:
                        normalized = (values - feature_def.min_value) / (feature_def.max_value - feature_def.min_value)
                        normalized = normalized.clip(0, 1)
                    else:
                        # Use percentile normalization
                        p5 = values.quantile(0.05)
                        p95 = values.quantile(0.95)
                        if p95 > p5:
                            normalized = (values - p5) / (p95 - p5)
                            normalized = normalized.clip(0, 1)
                        else:
                            normalized = pd.Series(0.5, index=values.index)
                    
                    scores.append(normalized)
                
                # Average the scores
                X_copy[f'{category}_score'] = pd.concat(scores, axis=1).mean(axis=1)
            else:
                X_copy[f'{category}_score'] = 0.5  # Default if no features
        
        logger.info(f"Added CAMP scores: {X_copy[['capital_score', 'advantage_score', 'market_score', 'people_score']].mean()}")
        return X_copy


class TemporalFeatureExtractor(BaseEstimator, TransformerMixin):
    """Extract temporal features from raw data"""
    
    def fit(self, X, y=None):
        """Fit method (no-op for this transformer)"""
        return self
    
    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        """Add temporal features to dataframe"""
        X_copy = X.copy()
        
        # Time momentum: combination of growth rates
        revenue_growth = X_copy.get('revenue_growth_rate', 0).fillna(0)
        customer_growth = X_copy.get('customer_growth_rate', 0).fillna(0)
        X_copy['time_momentum'] = (revenue_growth * customer_growth) / 100
        
        # Growth efficiency: growth per burn
        burn_multiple = X_copy.get('burn_multiple', 2).fillna(2)
        X_copy['growth_efficiency'] = revenue_growth / (burn_multiple + 1)
        
        # Market timing: market growth adjusted by competition
        market_growth = X_copy.get('market_growth_rate', 10).fillna(10)
        market_competition = X_copy.get('market_competitiveness', 3).fillna(3)
        X_copy['market_timing'] = market_growth * (1 - market_competition / 5)
        
        logger.info("Added temporal features: time_momentum, growth_efficiency, market_timing")
        return X_copy


class CategoricalEncoder(BaseEstimator, TransformerMixin):
    """Handle categorical encoding with proper fit/transform"""
    
    def __init__(self, feature_registry: FeatureRegistry):
        self.feature_registry = feature_registry
        self.encoders = {}
        self.categorical_features = []
    
    def fit(self, X, y=None):
        """Fit encoders for categorical features"""
        self.categorical_features = []
        
        for feature_name in X.columns:
            if feature_name in self.feature_registry.features:
                feature_def = self.feature_registry.get_feature(feature_name)
                if feature_def.dtype == str:
                    self.categorical_features.append(feature_name)
                    
                    # Use LabelEncoder for features with known categories
                    if feature_def.allowed_values:
                        encoder = LabelEncoder()
                        # Fit on allowed values to ensure consistent encoding
                        encoder.fit(feature_def.allowed_values)
                        self.encoders[feature_name] = encoder
                    else:
                        # For open-ended categories, fit on data
                        encoder = LabelEncoder()
                        unique_values = X[feature_name].fillna('unknown').unique()
                        encoder.fit(unique_values)
                        self.encoders[feature_name] = encoder
        
        return self
    
    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        """Transform categorical features to numeric"""
        X_copy = X.copy()
        
        for feature_name in self.categorical_features:
            if feature_name in X_copy.columns and feature_name in self.encoders:
                # Handle missing values
                feature_def = self.feature_registry.get_feature(feature_name)
                default = feature_def.default_value or 'unknown'
                values = X_copy[feature_name].fillna(default)
                
                # Transform with error handling for unseen categories
                encoder = self.encoders[feature_name]
                transformed = []
                for val in values:
                    try:
                        transformed.append(encoder.transform([val])[0])
                    except ValueError:
                        # Unseen category - use default encoding
                        if default in encoder.classes_:
                            transformed.append(encoder.transform([default])[0])
                        else:
                            transformed.append(0)  # Fallback
                
                X_copy[feature_name] = transformed
        
        return X_copy


class UnifiedFeaturePipeline:
    """Single pipeline for all feature engineering"""
    
    def __init__(self, feature_registry: FeatureRegistry):
        self.registry = feature_registry
        self.camp_calculator = CAMPScoreCalculator(feature_registry)
        self.temporal_extractor = TemporalFeatureExtractor()
        self.categorical_encoder = CategoricalEncoder(feature_registry)
        self.numeric_scaler = StandardScaler()
        self.is_fitted = False
        
        # Track which features are numeric vs categorical
        self.numeric_features = []
        self.categorical_features = []
        
    def fit(self, df: pd.DataFrame, y=None):
        """Fit all transformers on training data"""
        # Validate against registry
        is_valid, errors = self.registry.validate_dataframe(df)
        if not is_valid:
            logger.warning(f"Dataframe validation errors: {errors[:5]}")  # Show first 5
        
        # Identify numeric and categorical features
        self.numeric_features = []
        self.categorical_features = []
        
        for col in df.columns:
            if col in self.registry.features:
                feature_def = self.registry.get_feature(col)
                if feature_def.dtype in (int, float):
                    self.numeric_features.append(col)
                elif feature_def.dtype == str:
                    self.categorical_features.append(col)
        
        # Fit categorical encoder
        self.categorical_encoder.fit(df)
        
        # Transform to get numeric data for scaler
        df_encoded = self.categorical_encoder.transform(df)
        
        # Fit numeric scaler on numeric features only
        if self.numeric_features:
            self.numeric_scaler.fit(df_encoded[self.numeric_features])
        
        # Fit other components (they don't need fitting but we call for consistency)
        self.camp_calculator.fit(df_encoded)
        self.temporal_extractor.fit(df_encoded)
        
        self.is_fitted = True
        logger.info(f"Fitted pipeline with {len(self.numeric_features)} numeric and {len(self.categorical_features)} categorical features")
        
        return self
    
    def transform(self, df: pd.DataFrame, contract: Optional[ModelContract] = None) -> np.ndarray:
        """Transform data according to contract or return all features"""
        if not self.is_fitted:
            raise ValueError("Pipeline must be fitted before transform")
        
        # Start with copy
        X = df.copy()
        
        # Fill missing values with defaults from registry
        for col in X.columns:
            if col in self.registry.features:
                feature_def = self.registry.get_feature(col)
                if feature_def.default_value is not None:
                    X[col] = X[col].fillna(feature_def.default_value)
        
        # Apply categorical encoding
        X = self.categorical_encoder.transform(X)
        
        # Scale numeric features
        if self.numeric_features:
            X[self.numeric_features] = self.numeric_scaler.transform(X[self.numeric_features])
        
        # If contract specifies computed features, add them
        if contract:
            # Check which computed features are needed
            computed_features = [f for f in contract.input_features if f.source == 'computed']
            
            # Add CAMP scores if needed
            camp_features = ['capital_score', 'advantage_score', 'market_score', 'people_score']
            if any(f.name in camp_features for f in computed_features):
                X = self.camp_calculator.transform(X)
            
            # Add temporal features if needed
            temporal_features = ['time_momentum', 'growth_efficiency', 'market_timing']
            if any(f.name in temporal_features for f in computed_features):
                X = self.temporal_extractor.transform(X)
            
            # Select only contract features in order
            feature_names = contract.get_feature_names()
            X = X[feature_names]
        
        # Convert to numpy array
        return X.values
    
    def fit_transform(self, df: pd.DataFrame, contract: Optional[ModelContract] = None) -> np.ndarray:
        """Fit and transform in one step"""
        self.fit(df)
        return self.transform(df, contract)
    
    def inverse_transform_predictions(self, predictions: np.ndarray) -> pd.DataFrame:
        """Convert model predictions back to interpretable format"""
        # For binary classification
        if predictions.ndim == 1:
            df = pd.DataFrame({
                'prediction': predictions,
                'probability': predictions,
                'class': (predictions >= 0.5).astype(int)
            })
        else:
            # Multi-class or probability output
            df = pd.DataFrame(predictions)
            df['predicted_class'] = predictions.argmax(axis=1)
        
        return df
    
    def get_feature_importance_names(self, contract: ModelContract) -> List[str]:
        """Get feature names in order for feature importance interpretation"""
        if contract:
            return contract.get_feature_names()
        else:
            # Return all features in registry order
            return self.registry.get_feature_names()
    
    def save(self, path: str):
        """Save fitted pipeline"""
        import joblib
        
        if not self.is_fitted:
            raise ValueError("Cannot save unfitted pipeline")
        
        save_dict = {
            'camp_calculator': self.camp_calculator,
            'temporal_extractor': self.temporal_extractor,
            'categorical_encoder': self.categorical_encoder,
            'numeric_scaler': self.numeric_scaler,
            'numeric_features': self.numeric_features,
            'categorical_features': self.categorical_features,
            'is_fitted': self.is_fitted,
            'registry_version': self.registry.version
        }
        
        joblib.dump(save_dict, path)
        logger.info(f"Saved pipeline to {path}")
    
    @classmethod
    def load(cls, path: str, feature_registry: FeatureRegistry) -> 'UnifiedFeaturePipeline':
        """Load fitted pipeline"""
        import joblib
        
        save_dict = joblib.load(path)
        
        # Create new instance
        pipeline = cls(feature_registry)
        
        # Restore fitted components
        pipeline.camp_calculator = save_dict['camp_calculator']
        pipeline.temporal_extractor = save_dict['temporal_extractor']
        pipeline.categorical_encoder = save_dict['categorical_encoder']
        pipeline.numeric_scaler = save_dict['numeric_scaler']
        pipeline.numeric_features = save_dict['numeric_features']
        pipeline.categorical_features = save_dict['categorical_features']
        pipeline.is_fitted = save_dict['is_fitted']
        
        # Verify registry version matches
        if feature_registry.version != save_dict.get('registry_version'):
            logger.warning(f"Registry version mismatch: {feature_registry.version} vs {save_dict.get('registry_version')}")
        
        logger.info(f"Loaded pipeline from {path}")
        return pipeline


# Helper functions for common feature engineering tasks

def create_interaction_features(df: pd.DataFrame, feature_pairs: List[Tuple[str, str]]) -> pd.DataFrame:
    """Create interaction features between specified pairs"""
    df_copy = df.copy()
    
    for feat1, feat2 in feature_pairs:
        if feat1 in df.columns and feat2 in df.columns:
            df_copy[f'{feat1}_x_{feat2}'] = df[feat1] * df[feat2]
    
    return df_copy


def create_ratio_features(df: pd.DataFrame, ratios: List[Tuple[str, str, str]]) -> pd.DataFrame:
    """Create ratio features (numerator, denominator, name)"""
    df_copy = df.copy()
    
    for numerator, denominator, name in ratios:
        if numerator in df.columns and denominator in df.columns:
            # Avoid division by zero
            denom = df[denominator].replace(0, 1)
            df_copy[name] = df[numerator] / denom
    
    return df_copy


def create_polynomial_features(df: pd.DataFrame, features: List[str], degree: int = 2) -> pd.DataFrame:
    """Create polynomial features for specified columns"""
    from sklearn.preprocessing import PolynomialFeatures
    
    df_copy = df.copy()
    
    if features:
        poly = PolynomialFeatures(degree=degree, include_bias=False)
        poly_features = poly.fit_transform(df[features])
        
        # Get feature names
        feature_names = poly.get_feature_names_out(features)
        
        # Add to dataframe
        for i, name in enumerate(feature_names):
            if name not in df.columns:  # Don't overwrite originals
                df_copy[name] = poly_features[:, i]
    
    return df_copy