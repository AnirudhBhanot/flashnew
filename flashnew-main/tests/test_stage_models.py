#!/usr/bin/env python3
"""
Test script to verify stage models are working properly
"""
import sys
import numpy as np
import pandas as pd
from pathlib import Path
import logging

# Add parent directory to path
sys.path.append(str(Path(__file__).parent))

from stage_hierarchical_models import StageHierarchicalModel, StageConfig

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_stage_models():
    """Test loading and using stage models"""
    
    # Initialize the model
    stage_model = StageHierarchicalModel()
    
    # Load models - try stage_hierarchical directory first, then models directory
    model_path = Path('models/stage_hierarchical')
    if not model_path.exists():
        model_path = Path('models')
    
    logger.info(f"Loading models from: {model_path}")
    success = stage_model.load_models(model_path)
    
    if not success:
        logger.error("Failed to load stage models")
        return False
    
    # Create test data for different stages
    test_cases = [
        {
            'funding_stage': 'pre_seed',
            'team_score': 0.6,
            'market_score': 0.5,
            'product_score': 0.4,
            'traction_score': 0.3,
            'burn_efficiency': 0.7
        },
        {
            'funding_stage': 'seed',
            'team_score': 0.7,
            'market_score': 0.6,
            'product_score': 0.6,
            'traction_score': 0.5,
            'burn_efficiency': 0.8
        },
        {
            'funding_stage': 'series_a',
            'team_score': 0.8,
            'market_score': 0.7,
            'product_score': 0.8,
            'traction_score': 0.7,
            'burn_efficiency': 0.85
        }
    ]
    
    # Test predictions
    for i, test_case in enumerate(test_cases):
        logger.info(f"\n--- Test Case {i+1}: {test_case['funding_stage']} ---")
        
        # Create DataFrame with all required features (45 features)
        # Start with zeros and fill in known values
        features = pd.DataFrame([{f'feature_{j}': 0.0 for j in range(45)}])
        
        # Add our test values
        for key, value in test_case.items():
            features[key] = value
        
        try:
            # Get predictions
            proba = stage_model.predict_proba(features)
            prediction = stage_model.predict(features)
            
            logger.info(f"Success probability: {proba[0, 1]:.3f}")
            logger.info(f"Prediction: {'Pass' if prediction[0] else 'Fail'}")
            
            # Get insights
            insights = stage_model.get_stage_insights(features)
            if insights and 0 in insights:
                insight = insights[0]
                logger.info(f"Stage focus: {insight['stage_focus']}")
                logger.info(f"Threshold: {insight['threshold']}")
                logger.info(f"Recommendations: {insight['recommendations'][:2]}")
            
        except Exception as e:
            logger.error(f"Error making predictions: {e}")
            return False
    
    logger.info("\nAll tests completed successfully!")
    return True

def test_individual_stage_models():
    """Test loading individual stage models directly"""
    logger.info("\n=== Testing Individual Stage Models ===")
    
    stage_models_path = Path('models/stage_hierarchical')
    if not stage_models_path.exists():
        logger.error(f"Stage models directory not found: {stage_models_path}")
        return False
    
    # List all model files
    model_files = list(stage_models_path.glob('*_model.pkl'))
    logger.info(f"Found {len(model_files)} stage model files")
    
    for model_file in model_files:
        logger.info(f"  - {model_file.name}")
    
    # Try loading the unified stage model if it exists
    stage_model = StageHierarchicalModel()
    success = stage_model.load_models('models/stage_hierarchical')
    
    if success:
        logger.info("Successfully loaded stage models")
        logger.info(f"Loaded models: {list(stage_model.models.keys())}")
    else:
        logger.warning("Could not load stage models through StageHierarchicalModel")
    
    return True

if __name__ == "__main__":
    logger.info("Testing stage hierarchical models...")
    
    # Test loading individual models
    test_individual_stage_models()
    
    # Test full functionality
    test_stage_models()