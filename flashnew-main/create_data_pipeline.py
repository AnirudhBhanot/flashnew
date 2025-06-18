#!/usr/bin/env python3
"""
Create and save the data pipeline for unified models
This is CRITICAL for proper feature transformation
"""

import numpy as np
import pandas as pd
from pathlib import Path
import joblib
import json
from sklearn.preprocessing import StandardScaler
from typing import Dict, Tuple
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import canonical features
from feature_config import ALL_FEATURES, CATEGORICAL_FEATURES


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
                logger.info(f"Encoded {cat_feature}: {len(encoding_map)} unique values")
        
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
        
    def transform(self, df: pd.DataFrame) -> np.ndarray:
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


def create_and_save_pipeline():
    """Create pipeline using the training data"""
    logger.info("Creating unified data pipeline...")
    
    # Load training data
    data_path = Path("data/final_100k_dataset_45features.csv")
    if not data_path.exists():
        raise FileNotFoundError(f"Dataset not found at {data_path}")
    
    df = pd.read_csv(data_path)
    logger.info(f"Loaded {len(df)} samples")
    
    # Create and fit pipeline
    pipeline = UnifiedDataPipeline()
    pipeline.fit(df)
    
    # Save pipeline
    output_path = Path("models/unified_v45/data_pipeline.pkl")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    joblib.dump(pipeline, output_path)
    logger.info(f"Saved pipeline to {output_path}")
    
    # Save pipeline metadata
    metadata = {
        'n_features': len(pipeline.features),
        'features': pipeline.features,
        'categorical_features': list(pipeline.categorical_features),
        'categorical_encodings': {
            feature: {str(k): v for k, v in encoding.items()}
            for feature, encoding in pipeline.categorical_encoders.items()
        },
        'scaler_mean': pipeline.scaler.mean_.tolist(),
        'scaler_scale': pipeline.scaler.scale_.tolist()
    }
    
    metadata_path = output_path.parent / "pipeline_metadata.json"
    with open(metadata_path, 'w') as f:
        json.dump(metadata, f, indent=2)
    logger.info(f"Saved pipeline metadata to {metadata_path}")
    
    # Test pipeline
    test_sample = df.iloc[0:1].to_dict('records')[0]
    logger.info("\nTesting pipeline with sample:")
    
    try:
        X_test = pipeline.transform(test_sample)
        logger.info(f"✓ Transform successful: shape {X_test.shape}")
        logger.info(f"✓ Sample values: {X_test[0][:5]}...")
    except Exception as e:
        logger.error(f"✗ Transform failed: {e}")
        
    return pipeline


def verify_pipeline_with_models():
    """Verify pipeline works with trained models"""
    logger.info("\nVerifying pipeline with models...")
    
    # Load pipeline
    pipeline_path = Path("models/unified_v45/data_pipeline.pkl")
    pipeline = joblib.load(pipeline_path)
    
    # Load a model
    model_path = Path("models/unified_v45/dna_analyzer.pkl")
    if model_path.exists():
        model = joblib.load(model_path)
        
        # Create test data
        test_features = {
            'founding_year': 2021,
            'total_funding': 5000000,
            'num_funding_rounds': 2,
            'investor_tier_primary': 'tier_2',
            'burn_rate': 200000,
            'runway_months': 15,
            'funding_stage': 'series_a',
            'technology_score': 4,
            'has_patents': True,
            'patent_count': 3,
            'regulatory_advantage_present': True,
            'network_effects_present': True,
            'has_data_moat': True,
            'scalability_score': 4,
            'r_and_d_intensity': 0.25,
            'tam_size': 50000000000,
            'sam_percentage': 15,
            'market_share': 0.5,
            'market_growth_rate': 25,
            'competition_score': 3,
            'market_readiness_score': 4,
            'time_to_market': 6,
            'customer_acquisition_cost': 500,
            'ltv_cac_ratio': 3.5,
            'viral_coefficient': 1.2,
            'revenue_growth_rate': 2.5,
            'founder_experience_years': 10,
            'team_size': 15,
            'technical_team_percentage': 0.6,
            'founder_education_tier': 3,
            'employees_from_top_companies': 0.4,
            'advisory_board_score': 4,
            'key_person_dependency': False,
            'location_quality': 3,
            'has_lead_investor': True,
            'has_notable_investors': True,
            'product_launch_months': 8,
            'product_market_fit_score': 4,
            'revenue_model_score': 4,
            'unit_economics_score': 3,
            'customer_retention_rate': 0.85,
            'burn_multiple': 2.0,
            'investor_concentration': 0.3,
            'has_debt': False,
            'debt_to_equity': 0.0
        }
        
        # Transform and predict
        X = pipeline.transform(test_features)
        pred = model.predict_proba(X)[0, 1]
        
        logger.info(f"✓ Model prediction successful: {pred:.4f}")
        logger.info("✓ Pipeline is compatible with models!")
    else:
        logger.warning("Model not found for verification")


if __name__ == "__main__":
    logger.info("="*60)
    logger.info("Creating Unified Data Pipeline")
    logger.info("="*60)
    
    # Create and save pipeline
    pipeline = create_and_save_pipeline()
    
    # Verify it works
    verify_pipeline_with_models()
    
    logger.info("\n✅ Data pipeline created successfully!")
    logger.info("Models can now properly transform features!")
    logger.info("="*60)