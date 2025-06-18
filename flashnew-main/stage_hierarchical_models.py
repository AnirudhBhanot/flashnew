#!/usr/bin/env python3
"""
Stage-Based Hierarchical Models for FLASH Platform
Production-grade implementation with proper error handling and logging
"""
import numpy as np
import pandas as pd
import joblib
import logging
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union, Any
from dataclasses import dataclass
import json
from datetime import datetime

logger = logging.getLogger(__name__)


@dataclass
class StageConfig:
    """Configuration for stage-based models"""
    stages: List[str] = None
    thresholds: Dict[str, float] = None
    weights: Dict[str, Dict[str, float]] = None
    
    def __post_init__(self):
        if self.stages is None:
            self.stages = ['Pre-seed', 'Seed', 'Series A', 'Series B', 'Series C+']
        
        if self.thresholds is None:
            self.thresholds = {
                'Pre-seed': 0.35,
                'Seed': 0.45,
                'Series A': 0.50,
                'Series B': 0.55,
                'Series C+': 0.60
            }
        
        if self.weights is None:
            self.weights = {
                'Pre-seed': {'people': 0.4, 'advantage': 0.3, 'market': 0.2, 'capital': 0.1},
                'Seed': {'people': 0.3, 'advantage': 0.3, 'market': 0.25, 'capital': 0.15},
                'Series A': {'market': 0.3, 'advantage': 0.25, 'capital': 0.25, 'people': 0.2},
                'Series B': {'market': 0.35, 'capital': 0.3, 'advantage': 0.2, 'people': 0.15},
                'Series C+': {'capital': 0.4, 'market': 0.3, 'advantage': 0.2, 'people': 0.1}
            }


class StageHierarchicalModel:
    """
    Stage-specific hierarchical model for startup evaluation
    Provides different evaluation criteria based on funding stage
    """
    
    def __init__(self, config: Optional[StageConfig] = None):
        self.config = config or StageConfig()
        self.models = {}
        self.is_loaded = False
        self.model_path = None
        
    def load_models(self, model_path: Union[str, Path]) -> bool:
        """
        Load stage-specific models from disk
        
        Args:
            model_path: Path to model directory
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            self.model_path = Path(model_path)
            
            # Try to load the complete hierarchical model first
            hierarchical_path = self.model_path / 'stage_hierarchical_model.pkl'
            if hierarchical_path.exists():
                try:
                    logger.info(f"Loading hierarchical model from {hierarchical_path}")
                    loaded_model = joblib.load(hierarchical_path)
                    
                    # Extract stage models if they exist
                    if hasattr(loaded_model, 'stage_models'):
                        self.models = loaded_model.stage_models
                        logger.info(f"Loaded {len(self.models)} stage models from hierarchical model")
                    else:
                        # If it's the model itself, wrap it
                        self.models = {'unified': loaded_model}
                        logger.info("Loaded unified stage model")
                except Exception as e:
                    logger.warning(f"Could not load hierarchical model: {e}")
                    # Fall back to loading individual models
            
            # If no models loaded yet, try loading individual stage models
            if not self.models:
                # First check if we're in stage_hierarchical directory
                stage_dir = self.model_path / 'stage_hierarchical'
                if stage_dir.exists():
                    self.model_path = stage_dir
                    logger.info(f"Using stage_hierarchical subdirectory: {stage_dir}")
                
                loaded_count = 0
                for stage in self.config.stages:
                    stage_key = self._get_stage_key(stage)
                    model_file = self.model_path / f'{stage_key}_model.pkl'
                    
                    if model_file.exists():
                        self.models[stage_key] = joblib.load(model_file)
                        loaded_count += 1
                        logger.info(f"Loaded {stage} model")
                    else:
                        logger.warning(f"Model file not found: {model_file}")
                
                if loaded_count == 0:
                    logger.error("No stage models found")
                    return False
                    
                logger.info(f"Loaded {loaded_count} stage-specific models")
            
            self.is_loaded = True
            return True
            
        except Exception as e:
            logger.error(f"Error loading stage models: {str(e)}")
            return False
    
    def _get_stage_key(self, stage: str) -> str:
        """Convert stage name to key format"""
        return stage.lower().replace(' ', '_').replace('+', '_plus').replace('-', '_')
    
    def _normalize_stage(self, stage: str) -> str:
        """Normalize stage name to standard format"""
        stage_lower = stage.lower()
        
        if 'pre' in stage_lower or 'angel' in stage_lower:
            return 'Pre-seed'
        elif 'seed' in stage_lower and 'pre' not in stage_lower:
            return 'Seed'
        elif 'series a' in stage_lower or 'seriesa' in stage_lower:
            return 'Series A'
        elif 'series b' in stage_lower or 'seriesb' in stage_lower:
            return 'Series B'
        elif 'series c' in stage_lower or 'seriesc' in stage_lower:
            return 'Series C+'
        elif 'growth' in stage_lower or 'series d' in stage_lower:
            return 'Series C+'
        else:
            # Default mapping for frontend values
            stage_map = {
                'pre_seed': 'Pre-seed',
                'seed': 'Seed',
                'series_a': 'Series A',
                'series_b': 'Series B',
                'series_c': 'Series C+',
                'growth': 'Series C+'
            }
            return stage_map.get(stage_lower, 'Seed')
    
    def predict(self, features: pd.DataFrame) -> np.ndarray:
        """
        Make predictions using stage-specific models
        
        Args:
            features: DataFrame with startup features
            
        Returns:
            Array of binary predictions
        """
        probabilities = self.predict_proba(features)[:, 1]
        
        # Apply stage-specific thresholds
        predictions = []
        for idx, row in features.iterrows():
            stage = self._normalize_stage(row.get('funding_stage', 'Seed'))
            threshold = self.config.thresholds.get(stage, 0.5)
            predictions.append(int(probabilities[idx] >= threshold))
            
        return np.array(predictions)
    
    def predict_proba(self, features: pd.DataFrame) -> np.ndarray:
        """
        Get probability predictions using stage-specific models
        
        Args:
            features: DataFrame with startup features
            
        Returns:
            Array of probabilities (n_samples, 2)
        """
        if not self.is_loaded:
            raise RuntimeError("Models not loaded. Call load_models() first.")
        
        n_samples = len(features)
        probabilities = np.zeros((n_samples, 2))
        
        # If we have a unified model, use it
        if 'unified' in self.models:
            try:
                # Check if it has a predict_proba method
                if hasattr(self.models['unified'], 'predict_proba'):
                    return self.models['unified'].predict_proba(features)
                else:
                    # It might be the full hierarchical model
                    logger.warning("Unified model doesn't have predict_proba, using default")
                    probabilities[:, 1] = 0.5
                    probabilities[:, 0] = 0.5
                    return probabilities
            except Exception as e:
                logger.error(f"Error using unified model: {e}")
                probabilities[:, 1] = 0.5
                probabilities[:, 0] = 0.5
                return probabilities
        
        # Otherwise, use stage-specific models
        for idx, row in features.iterrows():
            stage = self._normalize_stage(row.get('funding_stage', 'Seed'))
            stage_key = self._get_stage_key(stage)
            
            if stage_key in self.models:
                try:
                    model = self.models[stage_key]
                    # Prepare features properly
                    prepared = self._prepare_features(row.to_frame().T)
                    # Get single prediction
                    prob = model.predict_proba(prepared)[0]
                    probabilities[idx] = prob
                except Exception as e:
                    logger.error(f"Error predicting for stage {stage}: {e}")
                    # Use average of other models as fallback
                    probabilities[idx] = self._get_fallback_prediction(row)
            else:
                # Use fallback if stage model not available
                probabilities[idx] = self._get_fallback_prediction(row)
                
        return probabilities
    
    def _prepare_features(self, features: pd.DataFrame) -> pd.DataFrame:
        """Prepare features for CatBoost models"""
        # Import stage model specific features
        try:
            from stage_model_features import (
                STAGE_MODEL_FEATURES, 
                STAGE_MODEL_CATEGORICAL, 
                STAGE_MODEL_BOOLEAN
            )
        except ImportError:
            # Fallback to using feature_config without funding_stage
            from feature_config import ALL_FEATURES, CATEGORICAL_FEATURES, BOOLEAN_FEATURES
            STAGE_MODEL_FEATURES = [f for f in ALL_FEATURES if f != 'funding_stage']
            STAGE_MODEL_CATEGORICAL = CATEGORICAL_FEATURES
            STAGE_MODEL_BOOLEAN = BOOLEAN_FEATURES
        
        df = features.copy()
        
        # Ensure all required features exist
        for feature in STAGE_MODEL_FEATURES:
            if feature not in df.columns:
                if feature in STAGE_MODEL_CATEGORICAL:
                    df[feature] = 'unknown'
                elif feature in STAGE_MODEL_BOOLEAN:
                    df[feature] = False
                else:
                    df[feature] = 0.0
        
        # Convert categorical features to strings
        for cat_feature in STAGE_MODEL_CATEGORICAL:
            if cat_feature in df.columns:
                df[cat_feature] = df[cat_feature].astype(str)
        
        # Convert boolean features to integers
        for bool_feature in STAGE_MODEL_BOOLEAN:
            if bool_feature in df.columns:
                df[bool_feature] = df[bool_feature].astype(int)
        
        # Select only the features the model expects (44 features, no funding_stage)
        return df[STAGE_MODEL_FEATURES]
    
    def _get_fallback_prediction(self, features: pd.Series) -> np.ndarray:
        """Get fallback prediction when stage-specific model unavailable"""
        if len(self.models) == 0:
            return np.array([0.5, 0.5])
            
        # Average predictions from available models
        predictions = []
        for model in self.models.values():
            if hasattr(model, 'predict_proba'):
                try:
                    # Prepare features properly
                    prepared = self._prepare_features(features.to_frame().T)
                    pred = model.predict_proba(prepared)[0]
                    predictions.append(pred)
                except:
                    pass
        
        if predictions:
            return np.mean(predictions, axis=0)
        else:
            return np.array([0.5, 0.5])
    
    def get_stage_insights(self, features: pd.DataFrame) -> Dict[str, Any]:
        """
        Get stage-specific insights and recommendations
        
        Args:
            features: DataFrame with startup features
            
        Returns:
            Dictionary with insights
        """
        insights = {}
        
        for idx, row in features.iterrows():
            stage = self._normalize_stage(row.get('funding_stage', 'Seed'))
            stage_weights = self.config.weights.get(stage, {})
            
            # Calculate weighted importance
            importance_scores = {}
            for pillar, weight in stage_weights.items():
                importance_scores[pillar] = weight
            
            # Get prediction for this startup
            prob = self.predict_proba(row.to_frame().T)[0, 1]
            threshold = self.config.thresholds.get(stage, 0.5)
            
            insights[idx] = {
                'stage': stage,
                'probability': float(prob),
                'threshold': threshold,
                'prediction': 'Pass' if prob >= threshold else 'Fail',
                'stage_focus': max(importance_scores, key=importance_scores.get),
                'importance_ranking': sorted(importance_scores.items(), 
                                           key=lambda x: x[1], reverse=True),
                'recommendations': self._generate_recommendations(stage, prob, threshold)
            }
            
        return insights
    
    def _generate_recommendations(self, stage: str, probability: float, 
                                  threshold: float) -> List[str]:
        """Generate stage-specific recommendations"""
        recommendations = []
        
        gap = threshold - probability
        if gap > 0:
            # Below threshold
            stage_focus = self.config.weights.get(stage, {})
            top_priority = max(stage_focus, key=stage_focus.get)
            
            if top_priority == 'people':
                recommendations.append("Strengthen founding team with domain experts")
                recommendations.append("Add experienced advisors or board members")
            elif top_priority == 'market':
                recommendations.append("Validate product-market fit with more customers")
                recommendations.append("Demonstrate clear market expansion strategy")
            elif top_priority == 'capital':
                recommendations.append("Improve unit economics and burn efficiency")
                recommendations.append("Extend runway to 18+ months")
            elif top_priority == 'advantage':
                recommendations.append("Build stronger competitive moats")
                recommendations.append("Develop proprietary technology or data assets")
                
            if gap > 0.2:
                recommendations.append(f"Consider staying at {stage} to strengthen fundamentals")
        else:
            # Above threshold
            recommendations.append(f"Strong position for {stage} funding")
            next_stage = self._get_next_stage(stage)
            if next_stage:
                recommendations.append(f"Begin preparing for {next_stage} requirements")
                
        return recommendations
    
    def _get_next_stage(self, current_stage: str) -> Optional[str]:
        """Get the next funding stage"""
        stage_progression = {
            'Pre-seed': 'Seed',
            'Seed': 'Series A',
            'Series A': 'Series B',
            'Series B': 'Series C+',
            'Series C+': 'Growth/IPO'
        }
        return stage_progression.get(current_stage)
    
    def get_stage_requirements(self, stage: str) -> Dict[str, Any]:
        """Get typical requirements for a funding stage"""
        stage = self._normalize_stage(stage)
        
        requirements = {
            'Pre-seed': {
                'typical_raise': '$100K - $500K',
                'team_size': '2-5',
                'product_stage': 'Concept/MVP',
                'key_metrics': ['Founder expertise', 'Market opportunity', 'Initial traction'],
                'investors': 'Angels, Pre-seed funds'
            },
            'Seed': {
                'typical_raise': '$500K - $2M',
                'team_size': '5-15',
                'product_stage': 'MVP/Early customers',
                'key_metrics': ['Product-market fit signals', 'Early revenue', 'User growth'],
                'investors': 'Seed funds, Angels'
            },
            'Series A': {
                'typical_raise': '$2M - $15M',
                'team_size': '15-50',
                'product_stage': 'Product-market fit',
                'key_metrics': ['$1M+ ARR', 'Unit economics', 'Growth rate'],
                'investors': 'Series A VCs'
            },
            'Series B': {
                'typical_raise': '$15M - $50M',
                'team_size': '50-150',
                'product_stage': 'Scaling',
                'key_metrics': ['$5M+ ARR', 'Market leadership', 'Expansion strategy'],
                'investors': 'Growth VCs'
            },
            'Series C+': {
                'typical_raise': '$50M+',
                'team_size': '150+',
                'product_stage': 'Market leader',
                'key_metrics': ['$20M+ ARR', 'Path to profitability', 'International expansion'],
                'investors': 'Late-stage funds, PE'
            }
        }
        
        return requirements.get(stage, requirements['Seed'])