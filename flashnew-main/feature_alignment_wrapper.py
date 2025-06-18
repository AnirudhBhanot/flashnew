
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
