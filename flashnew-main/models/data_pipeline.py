"""
Unified Data Pipeline for FLASH models
Handles all feature transformations consistently
"""

import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from typing import Dict, Union, Tuple
import logging

# Import canonical features
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from feature_config import ALL_FEATURES, CATEGORICAL_FEATURES

logger = logging.getLogger(__name__)


class UnifiedDataPipeline:
    """Data pipeline that matches the training process exactly"""
    
    def __init__(self):
        self.features = ALL_FEATURES
        self.categorical_features = CATEGORICAL_FEATURES
        self.scaler = StandardScaler()
        self.categorical_encoders = {}
        self.feature_names = []
        self.is_fitted = False
        
    def fit(self, df: pd.DataFrame):
        """Fit the pipeline on training data"""
        logger.info("Fitting data pipeline...")
        
        # Ensure all features exist
        for feature in self.features:
            if feature not in df.columns:
                if feature in self.categorical_features:
                    df[feature] = 'unknown'
                else:
                    df[feature] = 0.0
        
        # Select only canonical features
        X = df[self.features].copy()
        
        # Fit categorical encoders
        for cat_feature in self.categorical_features:
            if cat_feature in X.columns:
                # Create consistent encoding
                unique_vals = sorted(X[cat_feature].unique())
                encoding_map = {val: i for i, val in enumerate(unique_vals)}
                self.categorical_encoders[cat_feature] = encoding_map
                logger.debug(f"Encoded {cat_feature}: {len(encoding_map)} unique values")
        
        # Prepare data for scaler
        X_encoded = X.copy()
        for cat_feature, encoding_map in self.categorical_encoders.items():
            X_encoded[cat_feature] = X_encoded[cat_feature].map(encoding_map).fillna(0)
        
        # Fit scaler on numerical features
        numerical_features = [f for f in self.features if f not in self.categorical_features]
        self.scaler.fit(X_encoded[numerical_features])
        
        # Store feature names in order
        self.feature_names = list(self.features)
        self.is_fitted = True
        
        logger.info(f"Pipeline fitted with {len(self.features)} features")
        
    def transform(self, df: Union[pd.DataFrame, Dict]) -> np.ndarray:
        """Transform data using fitted pipeline"""
        if not self.is_fitted:
            raise ValueError("Pipeline must be fitted before transform")
            
        # Ensure DataFrame if dict passed
        if isinstance(df, dict):
            df = pd.DataFrame([df])
            
        # Ensure all features exist
        for feature in self.features:
            if feature not in df.columns:
                if feature in self.categorical_features:
                    df[feature] = 'unknown'
                else:
                    df[feature] = 0.0
        
        X = df[self.features].copy()
        
        # Apply categorical encoding
        for cat_feature, encoding_map in self.categorical_encoders.items():
            if cat_feature in X.columns:
                # Use 0 for unknown categories
                X[cat_feature] = X[cat_feature].map(encoding_map).fillna(0)
        
        # Scale numerical features
        numerical_features = [f for f in self.features if f not in self.categorical_features]
        X[numerical_features] = self.scaler.transform(X[numerical_features])
        
        return X.values
    
    def fit_transform(self, df: pd.DataFrame) -> Tuple[np.ndarray, np.ndarray]:
        """Fit and transform in one step"""
        self.fit(df)
        X = self.transform(df)
        y = df['success'].values if 'success' in df.columns else None
        return X, y