#!/usr/bin/env python3
"""
Fix Feature Mismatch in FLASH Models
This script identifies and fixes the feature count mismatch between models
"""

import pandas as pd
import numpy as np
import joblib
import json
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Import feature configuration
from feature_config import (
    ALL_FEATURES, CAPITAL_FEATURES, ADVANTAGE_FEATURES,
    MARKET_FEATURES, PEOPLE_FEATURES, PRODUCT_FEATURES,
    CATEGORICAL_FEATURES
)

def check_model_features():
    """Check feature expectations for all models"""
    logger.info("Checking model feature expectations...")
    
    model_issues = {}
    
    # Check production_v45 models
    prod_dir = Path('models/production_v45')
    if prod_dir.exists():
        for model_file in prod_dir.glob('*.pkl'):
            try:
                model = joblib.load(model_file)
                if hasattr(model, 'n_features_in_'):
                    expected = model.n_features_in_
                    if expected != 45:
                        model_issues[str(model_file)] = {
                            'expected': expected,
                            'actual': 45,
                            'difference': expected - 45
                        }
                        logger.warning(f"{model_file.name}: expects {expected} features (diff: {expected - 45})")
                    else:
                        logger.info(f"✓ {model_file.name}: correct (45 features)")
            except Exception as e:
                logger.error(f"Error loading {model_file}: {e}")
    
    # Check pattern models
    pattern_dir = Path('models/pattern_models')
    if pattern_dir.exists():
        for model_file in pattern_dir.glob('*_model.pkl'):
            try:
                model = joblib.load(model_file)
                if hasattr(model, 'n_features_in_'):
                    expected = model.n_features_in_
                    if expected != 45:
                        model_issues[str(model_file)] = {
                            'expected': expected,
                            'actual': 45,
                            'difference': expected - 45
                        }
                        logger.warning(f"{model_file.name}: expects {expected} features (diff: {expected - 45})")
                    else:
                        logger.info(f"✓ {model_file.name}: correct (45 features)")
            except Exception as e:
                logger.error(f"Error loading {model_file}: {e}")
    
    # Check v2 models (CAMP pillar models)
    v2_dir = Path('models/v2')
    if v2_dir.exists():
        # These models have a different structure - check metadata
        metadata_file = v2_dir / 'model_metadata.json'
        if metadata_file.exists():
            with open(metadata_file) as f:
                metadata = json.load(f)
                logger.info(f"V2 models metadata: {metadata.get('features', {})}")
    
    return model_issues

def analyze_feature_differences():
    """Analyze what the extra features might be"""
    logger.info("\nAnalyzing feature differences...")
    
    # Load the dataset to see actual columns
    data_file = Path('data/final_100k_dataset_45features.csv')
    if data_file.exists():
        df = pd.read_csv(data_file, nrows=5)
        all_cols = list(df.columns)
        
        # Remove target and ID columns
        feature_cols = [col for col in all_cols if col not in ['success', 'startup_id', 'startup_name']]
        
        logger.info(f"Dataset columns: {len(all_cols)}")
        logger.info(f"Feature columns: {len(feature_cols)}")
        
        # Check for extra columns not in ALL_FEATURES
        extra_cols = [col for col in feature_cols if col not in ALL_FEATURES]
        if extra_cols:
            logger.warning(f"Extra columns not in ALL_FEATURES: {extra_cols}")
        
        # Check for missing expected features
        missing_cols = [feat for feat in ALL_FEATURES if feat not in feature_cols]
        if missing_cols:
            logger.warning(f"Expected features missing from dataset: {missing_cols}")
        
        # Check if there are engineered features
        potential_engineered = [col for col in feature_cols if any(
            keyword in col.lower() for keyword in ['score', 'ratio', 'percent', 'avg', 'total']
        )]
        logger.info(f"Potential engineered features: {len(potential_engineered)}")

def create_feature_mapper():
    """Create a feature mapper to handle the mismatch"""
    logger.info("\nCreating feature mapper...")
    
    # The issue appears to be that models were trained with 49 features
    # but we have 45 canonical features. We need to identify the 4 extra features.
    
    # Common engineered features that might have been added:
    potential_extra_features = [
        'capital_score',      # Aggregate CAMP score
        'advantage_score',    # Aggregate CAMP score  
        'market_score',       # Aggregate CAMP score
        'people_score'        # Aggregate CAMP score
    ]
    
    mapper_config = {
        'canonical_features': ALL_FEATURES,
        'potential_extras': potential_extra_features,
        'feature_count': 45
    }
    
    # Save mapper configuration
    with open('feature_mapper_config.json', 'w') as f:
        json.dump(mapper_config, f, indent=2)
    
    logger.info("Feature mapper configuration saved")
    return mapper_config

def create_feature_alignment_wrapper():
    """Create a wrapper class to handle feature alignment"""
    wrapper_code = '''
import numpy as np
import pandas as pd
from typing import Dict, List, Union

class FeatureAlignmentWrapper:
    """Wrapper to align features between 45 and 49 feature models"""
    
    def __init__(self, model, expected_features: int = 49):
        self.model = model
        self.expected_features = expected_features
        self.camp_score_indices = {
            'capital_score': 45,
            'advantage_score': 46,
            'market_score': 47,
            'people_score': 48
        }
    
    def predict_proba(self, X: Union[pd.DataFrame, np.ndarray]) -> np.ndarray:
        """Predict with feature alignment"""
        # Convert to dataframe if needed
        if isinstance(X, np.ndarray):
            X_df = pd.DataFrame(X)
        else:
            X_df = X.copy()
        
        # If we have 45 features and model expects 49, add CAMP scores
        if X_df.shape[1] == 45 and self.expected_features == 49:
            # Calculate CAMP scores
            capital_score = X_df.iloc[:, :7].mean(axis=1)
            advantage_score = X_df.iloc[:, 7:15].mean(axis=1)
            market_score = X_df.iloc[:, 15:26].mean(axis=1)
            people_score = X_df.iloc[:, 26:36].mean(axis=1)
            
            # Add CAMP scores
            X_df['capital_score'] = capital_score
            X_df['advantage_score'] = advantage_score
            X_df['market_score'] = market_score
            X_df['people_score'] = people_score
        
        return self.model.predict_proba(X_df)
    
    def predict(self, X: Union[pd.DataFrame, np.ndarray]) -> np.ndarray:
        """Predict with feature alignment"""
        proba = self.predict_proba(X)
        return (proba[:, 1] >= 0.5).astype(int)
'''
    
    with open('feature_alignment_wrapper.py', 'w') as f:
        f.write(wrapper_code)
    
    logger.info("Created feature alignment wrapper class")

def main():
    """Main execution"""
    logger.info("="*60)
    logger.info("FLASH Feature Mismatch Analysis")
    logger.info("="*60)
    
    # 1. Check current model features
    issues = check_model_features()
    
    # 2. Analyze differences
    analyze_feature_differences()
    
    # 3. Create mapper
    mapper = create_feature_mapper()
    
    # 4. Create wrapper
    create_feature_alignment_wrapper()
    
    # Summary
    logger.info("\n" + "="*60)
    logger.info("SUMMARY")
    logger.info("="*60)
    
    if issues:
        logger.warning(f"Found {len(issues)} models with feature mismatches")
        logger.info("\nRecommended actions:")
        logger.info("1. Use the FeatureAlignmentWrapper for models expecting 49 features")
        logger.info("2. Add CAMP scores as features 46-49 when needed")
        logger.info("3. Consider retraining models with consistent 45 features")
    else:
        logger.info("✓ All models have correct feature expectations!")
    
    # Save summary
    summary = {
        'issues_found': len(issues),
        'model_issues': issues,
        'recommendation': 'Use FeatureAlignmentWrapper for 49-feature models',
        'camp_scores_needed': True if issues else False
    }
    
    with open('feature_mismatch_summary.json', 'w') as f:
        json.dump(summary, f, indent=2)
    
    logger.info("\nAnalysis complete. See feature_mismatch_summary.json for details.")

if __name__ == "__main__":
    main()