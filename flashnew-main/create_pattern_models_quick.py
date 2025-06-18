#!/usr/bin/env python3
"""
Quick Pattern Model Creation
Creates placeholder pattern models for immediate testing
"""

import joblib
import numpy as np
from pathlib import Path
import json
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression

def create_quick_pattern_models():
    """Create quick pattern models for testing"""
    
    # Create directories
    Path('models/pattern_models').mkdir(parents=True, exist_ok=True)
    
    # Define main patterns that need models
    patterns = [
        'EFFICIENT_B2B_SAAS',
        'BLITZSCALE_MARKETPLACE', 
        'DEEP_TECH_R&D',
        'BOOTSTRAP_PROFITABLE',
        'STRUGGLING_SEEKING_PMF'
    ]
    
    # Create simple models for each pattern
    for pattern in patterns:
        # Create a simple logistic regression model
        # In production, these would be trained on actual data
        model = LogisticRegression(random_state=42)
        
        # Create dummy training data
        # Features: 45 dimensions matching our feature set
        X_dummy = np.random.randn(100, 45)
        
        # Labels based on pattern type (different success rates)
        if pattern == 'EFFICIENT_B2B_SAAS':
            y_dummy = np.random.binomial(1, 0.78, 100)  # 78% success rate
        elif pattern == 'BOOTSTRAP_PROFITABLE':
            y_dummy = np.random.binomial(1, 0.72, 100)  # 72% success rate
        elif pattern == 'DEEP_TECH_R&D':
            y_dummy = np.random.binomial(1, 0.65, 100)  # 65% success rate
        elif pattern == 'BLITZSCALE_MARKETPLACE':
            y_dummy = np.random.binomial(1, 0.52, 100)  # 52% success rate
        else:  # STRUGGLING_SEEKING_PMF
            y_dummy = np.random.binomial(1, 0.28, 100)  # 28% success rate
        
        # Train model
        model.fit(X_dummy, y_dummy)
        
        # Save model
        model_path = f'models/pattern_models/{pattern}_model.pkl'
        joblib.dump(model, model_path)
        print(f"Created model for {pattern}")
    
    # Create pattern model metadata
    metadata = {
        "created": "2025-05-29",
        "type": "quick_placeholder",
        "patterns": patterns,
        "note": "These are placeholder models for testing. Train with real data for production."
    }
    
    with open('models/pattern_models/metadata.json', 'w') as f:
        json.dump(metadata, f, indent=2)
    
    print(f"\nCreated {len(patterns)} pattern models for testing")
    print("Note: These are placeholder models. Run full training for production use.")

if __name__ == "__main__":
    create_quick_pattern_models()