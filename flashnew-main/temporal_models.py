#!/usr/bin/env python3
"""
Temporal Prediction Models for FLASH Platform
Time-horizon based predictions with trajectory analysis
"""
import numpy as np
import pandas as pd
import joblib
import logging
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union, Any
from dataclasses import dataclass
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

logger = logging.getLogger(__name__)


@dataclass
class TemporalConfig:
    """Configuration for temporal models"""
    horizons: List[str] = None
    horizon_months: Dict[str, int] = None
    feature_importance: Dict[str, List[str]] = None
    
    def __post_init__(self):
        if self.horizons is None:
            self.horizons = ['6_months', '1_year', '2_years']
            
        if self.horizon_months is None:
            self.horizon_months = {
                '6_months': 6,
                '1_year': 12,
                '2_years': 24
            }
            
        if self.feature_importance is None:
            self.feature_importance = {
                '6_months': [  # Short-term survival
                    'runway_months',
                    'monthly_burn_usd',
                    'cash_on_hand_usd',
                    'revenue_growth_rate_percent',
                    'burn_multiple'
                ],
                '1_year': [  # Product-market fit
                    'annual_revenue_run_rate',
                    'customer_count',
                    'product_retention_30d',
                    'net_dollar_retention_percent',
                    'user_growth_rate_percent'
                ],
                '2_years': [  # Long-term success
                    'market_growth_rate_percent',
                    'tam_size_usd',
                    'tech_differentiation_score',
                    'team_size_full_time',
                    'prior_successful_exits_count'
                ]
            }


class TemporalPredictionModel:
    """
    Time-based prediction model for startup success at different horizons
    Provides trajectory analysis and time-specific insights
    """
    
    def __init__(self, config: Optional[TemporalConfig] = None):
        self.config = config or TemporalConfig()
        self.models = {}
        self.is_loaded = False
        self.trajectory_analyzer = TrajectoryAnalyzer()
        
    def load(self, model_path: Union[str, Path]) -> bool:
        """
        Load temporal models from disk
        
        Args:
            model_path: Path to model directory
            
        Returns:
            bool: True if successful
        """
        try:
            model_path = Path(model_path)
            
            # Try to load the complete temporal model first
            temporal_file = model_path / 'temporal_prediction_model.pkl'
            if not temporal_file.exists():
                temporal_file = model_path / 'temporal_hierarchical_model.pkl'
                
            if temporal_file.exists():
                logger.info(f"Loading temporal model from {temporal_file}")
                loaded_model = joblib.load(temporal_file)
                
                # Extract temporal models if they exist
                if hasattr(loaded_model, 'temporal_models'):
                    self.models = loaded_model.temporal_models
                    logger.info(f"Loaded {len(self.models)} temporal models")
                else:
                    # Wrap single model for all horizons
                    for horizon in self.config.horizons:
                        self.models[horizon] = loaded_model
                    logger.info("Using single model for all time horizons")
            else:
                # Try to load individual horizon models
                loaded_count = 0
                for horizon in self.config.horizons:
                    horizon_file = model_path / f'{horizon}_model.pkl'
                    if horizon_file.exists():
                        self.models[horizon] = joblib.load(horizon_file)
                        loaded_count += 1
                        logger.info(f"Loaded {horizon} model")
                        
                if loaded_count == 0:
                    logger.error("No temporal models found")
                    return False
                    
            self.is_loaded = True
            return True
            
        except Exception as e:
            logger.error(f"Error loading temporal models: {str(e)}")
            return False
    
    def predict(self, features: pd.DataFrame, 
                horizon: Optional[str] = None) -> Dict[str, Any]:
        """
        Make temporal predictions
        
        Args:
            features: DataFrame with startup features
            horizon: Specific time horizon (optional)
            
        Returns:
            Dictionary with predictions and analysis
        """
        if not self.is_loaded:
            logger.warning("Temporal models not loaded, returning default predictions")
            return self._get_default_predictions(features)
        
        try:
            if horizon:
                # Single horizon prediction
                predictions = self._predict_horizon(features, horizon)
                trajectory = self.trajectory_analyzer.analyze_single(
                    features, predictions['probability']
                )
            else:
                # All horizons prediction
                predictions = self._predict_all_horizons(features)
                trajectory = self.trajectory_analyzer.analyze_trajectory(
                    features, predictions['probabilities']
                )
            
            # Generate temporal insights
            insights = self._generate_temporal_insights(features, predictions, trajectory)
            
            # Risk assessment
            risk_factors = self._assess_temporal_risks(features, predictions)
            
            return {
                'predictions': predictions.get('predictions', {}),
                'probabilities': predictions.get('probabilities', {}),
                'trajectory': trajectory,
                'insights': insights,
                'risk_factors': risk_factors,
                'recommendations': self._generate_recommendations(trajectory, risk_factors)
            }
            
        except Exception as e:
            logger.error(f"Error in temporal prediction: {str(e)}")
            return self._get_default_predictions(features)
    
    def _predict_horizon(self, features: pd.DataFrame, 
                        horizon: str) -> Dict[str, Any]:
        """Predict for a specific time horizon"""
        if horizon not in self.models:
            logger.warning(f"Model for horizon {horizon} not available")
            return {'prediction': 0, 'probability': 0.5}
        
        model = self.models[horizon]
        
        # Get important features for this horizon
        important_features = self.config.feature_importance.get(horizon, [])
        available_features = [f for f in important_features if f in features.columns]
        
        if available_features:
            # Use horizon-specific features if available
            horizon_features = features[available_features]
        else:
            # Use all features
            horizon_features = features
        
        try:
            probabilities = model.predict_proba(horizon_features)[:, 1]
            predictions = (probabilities >= 0.5).astype(int)
            
            return {
                'prediction': int(predictions[0]),
                'probability': float(probabilities[0]),
                'horizon': horizon,
                'months': self.config.horizon_months[horizon]
            }
        except Exception as e:
            logger.error(f"Error predicting for horizon {horizon}: {e}")
            return {'prediction': 0, 'probability': 0.5}
    
    def _predict_all_horizons(self, features: pd.DataFrame) -> Dict[str, Any]:
        """Predict for all time horizons"""
        predictions = {}
        probabilities = {}
        
        for horizon in self.config.horizons:
            result = self._predict_horizon(features, horizon)
            predictions[horizon] = result['prediction']
            probabilities[horizon] = result['probability']
        
        # Add current state (time 0)
        probabilities['current'] = self._assess_current_state(features)
        predictions['current'] = int(probabilities['current'] >= 0.5)
        
        return {
            'predictions': predictions,
            'probabilities': probabilities
        }
    
    def _assess_current_state(self, features: pd.DataFrame) -> float:
        """Assess current startup health"""
        score = 0.5  # Base score
        
        # Runway assessment
        if 'runway_months' in features.columns:
            runway = features['runway_months'].iloc[0]
            if runway > 18:
                score += 0.1
            elif runway < 6:
                score -= 0.2
        
        # Revenue assessment
        if 'annual_revenue_run_rate' in features.columns:
            arr = features['annual_revenue_run_rate'].iloc[0]
            if arr > 1000000:  # $1M ARR
                score += 0.15
            elif arr > 100000:  # $100K ARR
                score += 0.05
        
        # Growth assessment
        if 'revenue_growth_rate_percent' in features.columns:
            growth = features['revenue_growth_rate_percent'].iloc[0]
            if growth > 200:
                score += 0.1
            elif growth < 0:
                score -= 0.1
        
        # Team assessment
        if 'team_size_full_time' in features.columns:
            team = features['team_size_full_time'].iloc[0]
            if team > 10:
                score += 0.05
        
        return np.clip(score, 0, 1)
    
    def _generate_temporal_insights(self, features: pd.DataFrame,
                                   predictions: Dict[str, Any],
                                   trajectory: Dict[str, Any]) -> List[str]:
        """Generate time-based insights"""
        insights = []
        
        # Trajectory insights
        trend = trajectory.get('trend', 'stable')
        if trend == 'improving':
            insights.append("Success probability improves over time - positive momentum")
        elif trend == 'declining':
            insights.append("Success probability declines over time - intervention needed")
        elif trend == 'volatile':
            insights.append("Uncertain trajectory - high variability in outcomes")
        
        # Horizon-specific insights
        probs = predictions.get('probabilities', {})
        
        # Short-term insights
        if '6_months' in probs:
            if probs['6_months'] < 0.4:
                insights.append("High short-term risk - immediate action required")
            elif probs['6_months'] > 0.7:
                insights.append("Strong short-term position")
        
        # Medium-term insights
        if '1_year' in probs:
            if probs['1_year'] > probs.get('6_months', 0.5):
                insights.append("Product-market fit improving over next year")
            elif probs['1_year'] < 0.5:
                insights.append("PMF challenges expected within 12 months")
        
        # Long-term insights
        if '2_years' in probs:
            if probs['2_years'] > 0.7:
                insights.append("Strong long-term success indicators")
            elif probs['2_years'] < probs.get('1_year', 0.5):
                insights.append("Long-term sustainability concerns")
        
        # Critical points
        critical = trajectory.get('critical_points', [])
        if critical:
            insights.append(f"Critical decision points at: {', '.join(critical)}")
        
        return insights
    
    def _assess_temporal_risks(self, features: pd.DataFrame,
                              predictions: Dict[str, Any]) -> Dict[str, List[str]]:
        """Assess risks at different time horizons"""
        risks = {
            'immediate': [],
            'short_term': [],
            'medium_term': [],
            'long_term': []
        }
        
        # Immediate risks (0-3 months)
        if 'runway_months' in features.columns:
            if features['runway_months'].iloc[0] < 3:
                risks['immediate'].append("Critical: Less than 3 months runway")
        
        if 'monthly_burn_usd' in features.columns and 'cash_on_hand_usd' in features.columns:
            burn = features['monthly_burn_usd'].iloc[0]
            cash = features['cash_on_hand_usd'].iloc[0]
            if burn > cash * 0.5:
                risks['immediate'].append("Unsustainable burn rate")
        
        # Short-term risks (3-6 months)
        probs = predictions.get('probabilities', {})
        if probs.get('6_months', 1) < 0.5:
            if 'customer_count' in features.columns:
                if features['customer_count'].iloc[0] < 10:
                    risks['short_term'].append("Insufficient customer validation")
            
            if 'product_retention_30d' in features.columns:
                if features['product_retention_30d'].iloc[0] < 0.5:
                    risks['short_term'].append("Poor product retention")
        
        # Medium-term risks (6-12 months)
        if probs.get('1_year', 1) < 0.5:
            if 'revenue_growth_rate_percent' in features.columns:
                if features['revenue_growth_rate_percent'].iloc[0] < 50:
                    risks['medium_term'].append("Below-target growth rate")
            
            if 'ltv_cac_ratio' in features.columns:
                if features['ltv_cac_ratio'].iloc[0] < 1:
                    risks['medium_term'].append("Negative unit economics")
        
        # Long-term risks (12-24 months)
        if probs.get('2_years', 1) < 0.5:
            if 'market_growth_rate_percent' in features.columns:
                if features['market_growth_rate_percent'].iloc[0] < 10:
                    risks['long_term'].append("Slow market growth")
            
            if 'competition_intensity' in features.columns:
                if features['competition_intensity'].iloc[0] > 4:
                    risks['long_term'].append("Intense competition threat")
        
        return risks
    
    def _generate_recommendations(self, trajectory: Dict[str, Any],
                                 risk_factors: Dict[str, List[str]]) -> List[str]:
        """Generate time-based recommendations"""
        recommendations = []
        
        # Immediate action items
        if risk_factors['immediate']:
            recommendations.append("URGENT: Address immediate risks within 30 days")
            if any('runway' in risk for risk in risk_factors['immediate']):
                recommendations.append("Extend runway through fundraising or cost reduction")
        
        # Trajectory-based recommendations
        trend = trajectory.get('trend', 'stable')
        if trend == 'declining':
            recommendations.append("Pivot strategy to reverse negative trajectory")
            recommendations.append("Focus on quick wins to build momentum")
        elif trend == 'improving':
            recommendations.append("Maintain current strategy and accelerate growth")
            recommendations.append("Consider raising growth capital")
        
        # Milestone recommendations
        inflection = trajectory.get('inflection_point')
        if inflection:
            recommendations.append(f"Key inflection point at {inflection} - prepare strategic initiatives")
        
        # Risk mitigation
        if risk_factors['short_term']:
            recommendations.append("Build 6-month risk mitigation plan")
        
        if risk_factors['medium_term']:
            recommendations.append("Develop product-market fit acceleration program")
        
        return recommendations
    
    def _get_default_predictions(self, features: pd.DataFrame) -> Dict[str, Any]:
        """Return default predictions when models not loaded"""
        default_prob = 0.5
        
        return {
            'predictions': {
                'current': 0,
                '6_months': 0,
                '1_year': 0,
                '2_years': 0
            },
            'probabilities': {
                'current': default_prob,
                '6_months': default_prob,
                '1_year': default_prob,
                '2_years': default_prob
            },
            'trajectory': {
                'trend': 'unknown',
                'confidence': 0
            },
            'insights': ["Temporal models not available"],
            'risk_factors': {
                'immediate': [],
                'short_term': [],
                'medium_term': [],
                'long_term': []
            },
            'recommendations': ["Load temporal models for trajectory analysis"]
        }
    
    def get_survival_curve(self, features: pd.DataFrame) -> Dict[str, Any]:
        """
        Generate survival probability curve over time
        
        Args:
            features: Startup features
            
        Returns:
            Survival curve data
        """
        if not self.is_loaded:
            return {
                'months': list(range(0, 25)),
                'probabilities': [0.5] * 25,
                'confidence_lower': [0.4] * 25,
                'confidence_upper': [0.6] * 25
            }
        
        # Get predictions at key points
        predictions = self._predict_all_horizons(features)
        probs = predictions['probabilities']
        
        # Interpolate between points
        key_months = [0, 6, 12, 24]
        key_probs = [
            probs.get('current', 0.5),
            probs.get('6_months', 0.5),
            probs.get('1_year', 0.5),
            probs.get('2_years', 0.5)
        ]
        
        # Generate smooth curve
        months = list(range(0, 25))
        probabilities = np.interp(months, key_months, key_probs)
        
        # Add confidence intervals
        confidence_width = 0.1
        confidence_lower = np.maximum(0, probabilities - confidence_width)
        confidence_upper = np.minimum(1, probabilities + confidence_width)
        
        return {
            'months': months,
            'probabilities': probabilities.tolist(),
            'confidence_lower': confidence_lower.tolist(),
            'confidence_upper': confidence_upper.tolist(),
            'key_points': {
                'current': probs.get('current', 0.5),
                '6_months': probs.get('6_months', 0.5),
                '1_year': probs.get('1_year', 0.5),
                '2_years': probs.get('2_years', 0.5)
            }
        }


class TrajectoryAnalyzer:
    """Analyzes startup trajectory over time"""
    
    def analyze_trajectory(self, features: pd.DataFrame,
                          probabilities: Dict[str, float]) -> Dict[str, Any]:
        """Analyze the trajectory based on temporal probabilities"""
        
        # Extract time series
        time_points = ['current', '6_months', '1_year', '2_years']
        time_values = [0, 6, 12, 24]
        probs = [probabilities.get(tp, 0.5) for tp in time_points]
        
        # Calculate trend
        if len(probs) < 2:
            trend = 'unknown'
        else:
            # Simple linear regression
            slope = np.polyfit(time_values, probs, 1)[0]
            
            if slope > 0.01:
                trend = 'improving'
            elif slope < -0.01:
                trend = 'declining'
            else:
                trend = 'stable'
            
            # Check for volatility
            prob_std = np.std(probs)
            if prob_std > 0.2:
                trend = 'volatile'
        
        # Find inflection points
        inflection_point = None
        critical_points = []
        
        for i in range(1, len(probs) - 1):
            # Check for direction change
            if (probs[i] - probs[i-1]) * (probs[i+1] - probs[i]) < 0:
                inflection_point = time_points[i]
            
            # Check for critical thresholds
            if probs[i] < 0.4 and probs[i-1] >= 0.4:
                critical_points.append(f"{time_points[i]} (drops below 40%)")
            elif probs[i] > 0.6 and probs[i-1] <= 0.6:
                critical_points.append(f"{time_points[i]} (exceeds 60%)")
        
        # Calculate confidence
        confidence = 1 - prob_std if prob_std < 0.3 else 0.7
        
        return {
            'trend': trend,
            'slope': float(slope) if 'slope' in locals() else 0,
            'volatility': float(prob_std) if 'prob_std' in locals() else 0,
            'inflection_point': inflection_point,
            'critical_points': critical_points,
            'confidence': confidence,
            'trajectory_score': np.mean(probs)
        }
    
    def analyze_single(self, features: pd.DataFrame,
                      probability: float) -> Dict[str, Any]:
        """Analyze trajectory for a single time point"""
        return {
            'trend': 'stable',
            'slope': 0,
            'volatility': 0,
            'inflection_point': None,
            'critical_points': [],
            'confidence': 0.8,
            'trajectory_score': probability
        }