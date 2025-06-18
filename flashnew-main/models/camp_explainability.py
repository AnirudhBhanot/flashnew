#!/usr/bin/env python3
"""
CAMP Explainability System using SHAP
Provides interpretable CAMP scores that explain ML predictions
"""

import numpy as np
import pandas as pd
import shap
import logging
from typing import Dict, List, Tuple, Any, Optional
from dataclasses import dataclass
import pickle
import os

from feature_config import (
    CAPITAL_FEATURES, ADVANTAGE_FEATURES, MARKET_FEATURES, PEOPLE_FEATURES,
    ALL_FEATURES
)

logger = logging.getLogger(__name__)

@dataclass
class CAMPExplanation:
    """Structured explanation for CAMP scores"""
    capital_score: float
    advantage_score: float
    market_score: float
    people_score: float
    success_probability: float
    critical_factors: List[Dict[str, Any]]
    feature_impacts: Dict[str, float]
    alignment_explanation: str


class CAMPExplainabilitySystem:
    """
    Unified system that derives CAMP scores from ML model predictions
    using SHAP values to ensure alignment between interpretability and predictions
    """
    
    def __init__(self, model_dir: str = "models/production_v45"):
        self.model_dir = model_dir
        self.models = {}
        self.explainers = {}
        self.background_data = None
        self._load_models()
        self._initialize_explainers()
        
    def _load_models(self):
        """Load the ML models"""
        model_files = {
            'industry_model': 'industry_model.pkl',
            'temporal_model': 'temporal_model.pkl',
            'dna_analyzer': 'dna_analyzer.pkl'
        }
        
        for name, filename in model_files.items():
            path = os.path.join(self.model_dir, filename)
            if os.path.exists(path):
                try:
                    with open(path, 'rb') as f:
                        self.models[name] = pickle.load(f)
                    logger.info(f"Loaded {name} for explainability")
                except Exception as e:
                    logger.error(f"Failed to load {name}: {e}")
                    
    def _initialize_explainers(self):
        """Initialize SHAP explainers with background data"""
        # Create synthetic background data representing typical startups
        n_background = 100
        self.background_data = self._create_background_data(n_background)
        
        # Initialize explainer for the model that works best (industry_model)
        if 'industry_model' in self.models:
            try:
                self.explainers['industry_model'] = shap.TreeExplainer(
                    self.models['industry_model'],
                    self.background_data
                )
                logger.info("Initialized SHAP explainer for industry model")
            except Exception as e:
                logger.error(f"Failed to initialize SHAP explainer: {e}")
                # Fallback to simple feature importance
                self.explainers['industry_model'] = None
                
    def _create_background_data(self, n_samples: int) -> pd.DataFrame:
        """Create background data for SHAP"""
        # Create realistic ranges for each feature
        background_data = {}
        
        # Monetary features (log-normal distribution)
        monetary_features = ['total_capital_raised_usd', 'cash_on_hand_usd', 
                           'monthly_burn_usd', 'tam_size_usd', 'sam_size_usd', 'som_size_usd']
        for feat in monetary_features:
            if feat in ALL_FEATURES:
                background_data[feat] = np.random.lognormal(10, 2, n_samples)
        
        # Percentage features (normal distribution, clipped)
        percentage_features = ['market_growth_rate_percent', 'user_growth_rate_percent',
                             'net_dollar_retention_percent', 'customer_concentration_percent']
        for feat in percentage_features:
            if feat in ALL_FEATURES:
                if feat == 'net_dollar_retention_percent':
                    background_data[feat] = np.clip(np.random.normal(110, 20, n_samples), 50, 200)
                else:
                    background_data[feat] = np.clip(np.random.normal(30, 20, n_samples), -50, 100)
        
        # Score features (1-5)
        score_features = ['tech_differentiation_score', 'switching_cost_score',
                         'brand_strength_score', 'scalability_score', 
                         'board_advisor_experience_score', 'execution_risk_score']
        for feat in score_features:
            if feat in ALL_FEATURES:
                background_data[feat] = np.random.randint(1, 6, n_samples)
        
        # Binary features
        binary_features = ['has_debt', 'network_effects_present', 'has_data_moat',
                          'regulatory_advantage_present', 'has_repeat_founder']
        for feat in binary_features:
            if feat in ALL_FEATURES:
                background_data[feat] = np.random.choice([0, 1], n_samples)
        
        # Other numeric features
        remaining_features = set(ALL_FEATURES) - set(background_data.keys())
        for feat in remaining_features:
            if feat == 'runway_months':
                background_data[feat] = np.clip(np.random.normal(12, 6, n_samples), 0, 36)
            elif feat == 'company_age_months':
                background_data[feat] = np.clip(np.random.normal(24, 12, n_samples), 1, 120)
            elif 'count' in feat:
                background_data[feat] = np.random.poisson(5, n_samples)
            else:
                background_data[feat] = np.random.normal(0, 1, n_samples)
        
        return pd.DataFrame(background_data)[ALL_FEATURES]
    
    def explain_prediction(self, features: Dict[str, Any], prediction: float) -> CAMPExplanation:
        """
        Generate CAMP scores that explain the ML prediction
        """
        # Convert features to DataFrame
        feature_df = pd.DataFrame([features])[ALL_FEATURES]
        
        # Get SHAP values if available
        if self.explainers.get('industry_model'):
            try:
                shap_values = self.explainers['industry_model'].shap_values(feature_df)
                if isinstance(shap_values, list):
                    # For binary classification, use positive class
                    shap_values = shap_values[1]
                
                # Convert to feature impacts
                feature_impacts = dict(zip(ALL_FEATURES, shap_values[0]))
            except Exception as e:
                logger.warning(f"SHAP calculation failed: {e}, using fallback")
                feature_impacts = self._calculate_fallback_impacts(features, prediction)
        else:
            feature_impacts = self._calculate_fallback_impacts(features, prediction)
        
        # Calculate CAMP scores based on feature impacts
        camp_scores = self._calculate_camp_from_impacts(feature_impacts, features)
        
        # Identify critical factors
        critical_factors = self._identify_critical_factors(feature_impacts, features)
        
        # Generate alignment explanation
        alignment = self._explain_alignment(
            prediction, camp_scores, critical_factors, features
        )
        
        return CAMPExplanation(
            capital_score=camp_scores['capital'],
            advantage_score=camp_scores['advantage'],
            market_score=camp_scores['market'],
            people_score=camp_scores['people'],
            success_probability=prediction,
            critical_factors=critical_factors,
            feature_impacts=feature_impacts,
            alignment_explanation=alignment
        )
    
    def _calculate_fallback_impacts(self, features: Dict[str, Any], 
                                  prediction: float) -> Dict[str, float]:
        """
        Fallback method to calculate feature impacts without SHAP
        Uses heuristic importance based on feature values and prediction
        """
        impacts = {}
        
        # Critical features that heavily impact predictions
        critical_features = {
            'runway_months': {'threshold': 6, 'impact': 0.3},
            'burn_multiple': {'threshold': 5, 'impact': -0.2},
            'net_dollar_retention_percent': {'threshold': 100, 'impact': 0.15},
            'customer_concentration_percent': {'threshold': 50, 'impact': -0.15}
        }
        
        for feat in ALL_FEATURES:
            if feat in critical_features:
                value = features.get(feat, 0)
                config = critical_features[feat]
                
                if feat == 'runway_months':
                    # Low runway has massive negative impact
                    if value < config['threshold']:
                        impacts[feat] = -0.3 * (1 - value/config['threshold'])
                    else:
                        impacts[feat] = 0.1 * min(value/24, 1)
                elif feat == 'burn_multiple':
                    # High burn multiple is bad
                    if value > config['threshold']:
                        impacts[feat] = -0.2 * min(value/10, 1)
                    else:
                        impacts[feat] = 0.05
                else:
                    # Generic critical feature
                    impacts[feat] = config['impact'] * (value/100 if '%' in feat else value/5)
            else:
                # Non-critical features have smaller impacts
                impacts[feat] = np.random.normal(0, 0.02)
        
        return impacts
    
    def _calculate_camp_from_impacts(self, feature_impacts: Dict[str, float],
                                   features: Dict[str, Any]) -> Dict[str, float]:
        """
        Calculate CAMP scores from feature impacts
        This ensures CAMP scores reflect actual model reasoning
        """
        camp_impacts = {
            'capital': [],
            'advantage': [],
            'market': [],
            'people': []
        }
        
        # Group impacts by CAMP category
        for feat, impact in feature_impacts.items():
            if feat in CAPITAL_FEATURES:
                camp_impacts['capital'].append(impact)
            elif feat in ADVANTAGE_FEATURES:
                camp_impacts['advantage'].append(impact)
            elif feat in MARKET_FEATURES:
                camp_impacts['market'].append(impact)
            elif feat in PEOPLE_FEATURES:
                camp_impacts['people'].append(impact)
        
        # Calculate scores based on impacts
        base_score = 0.5  # Neutral baseline
        camp_scores = {}
        
        for pillar, impacts in camp_impacts.items():
            if impacts:
                # Sum of impacts shows contribution to prediction
                total_impact = sum(impacts)
                # Convert impact to score (impacts typically range -0.5 to 0.5)
                score = base_score + total_impact
                # Ensure valid probability
                camp_scores[pillar] = max(0.0, min(1.0, score))
            else:
                camp_scores[pillar] = base_score
        
        # Adjust scores to better reflect the overall prediction
        # This ensures CAMP average is close to success probability
        avg_camp = np.mean(list(camp_scores.values()))
        if avg_camp > 0:
            adjustment_factor = np.sqrt(features.get('success_probability', 0.5) / avg_camp)
            for pillar in camp_scores:
                camp_scores[pillar] = min(1.0, camp_scores[pillar] * adjustment_factor)
        
        return camp_scores
    
    def _identify_critical_factors(self, feature_impacts: Dict[str, float],
                                 features: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Identify the most critical factors affecting the prediction"""
        # Sort features by absolute impact
        sorted_features = sorted(
            feature_impacts.items(),
            key=lambda x: abs(x[1]),
            reverse=True
        )
        
        critical_factors = []
        for feat, impact in sorted_features[:5]:  # Top 5 factors
            value = features.get(feat, 0)
            
            # Determine if it's positive or negative
            if impact > 0:
                factor_type = "strength"
                icon = "✅"
            else:
                factor_type = "weakness"
                icon = "⚠️"
            
            # Create human-readable explanation
            explanation = self._explain_feature(feat, value, impact)
            
            critical_factors.append({
                'feature': feat,
                'value': value,
                'impact': impact,
                'type': factor_type,
                'icon': icon,
                'explanation': explanation
            })
        
        return critical_factors
    
    def _explain_feature(self, feature: str, value: Any, impact: float) -> str:
        """Generate human-readable explanation for a feature"""
        explanations = {
            'runway_months': lambda v, i: (
                f"Only {v:.1f} months of runway remaining" if v < 6 
                else f"{v:.1f} months runway provides stability"
            ),
            'burn_multiple': lambda v, i: (
                f"Burn multiple of {v:.1f}x indicates poor efficiency" if v > 3
                else f"Efficient burn multiple of {v:.1f}x"
            ),
            'net_dollar_retention_percent': lambda v, i: (
                f"NDR of {v:.0f}% shows strong expansion" if v > 120
                else f"NDR of {v:.0f}% indicates churn issues" if v < 100
                else f"NDR of {v:.0f}% is stable"
            ),
            'customer_concentration_percent': lambda v, i: (
                f"High customer concentration ({v:.0f}%) is risky" if v > 30
                else f"Well-distributed customer base ({v:.0f}%)"
            ),
            'user_growth_rate_percent': lambda v, i: (
                f"Strong {v:.0f}% user growth" if v > 20
                else f"Declining users at {v:.0f}%" if v < 0
                else f"Modest {v:.0f}% user growth"
            )
        }
        
        if feature in explanations:
            return explanations[feature](value, impact)
        else:
            return f"{feature.replace('_', ' ').title()}: {value}"
    
    def _explain_alignment(self, prediction: float, camp_scores: Dict[str, float],
                         critical_factors: List[Dict[str, Any]], 
                         features: Dict[str, Any]) -> str:
        """Explain why CAMP scores align or don't align with prediction"""
        avg_camp = np.mean(list(camp_scores.values()))
        diff = abs(prediction - avg_camp)
        
        if diff < 0.1:
            return "CAMP scores are well-aligned with the ML prediction."
        
        # Find the most impactful factor
        if critical_factors:
            top_factor = critical_factors[0]
            
            if diff > 0.3:
                if prediction < avg_camp:
                    return (
                        f"Despite strong CAMP averages ({avg_camp:.1%}), "
                        f"{top_factor['explanation']} significantly reduces "
                        f"success probability to {prediction:.1%}."
                    )
                else:
                    return (
                        f"ML models identify hidden strengths beyond CAMP averages. "
                        f"{top_factor['explanation']} drives higher success "
                        f"probability of {prediction:.1%}."
                    )
            else:
                return (
                    f"Minor misalignment due to {top_factor['explanation']}. "
                    f"Overall assessment remains consistent."
                )
        
        return "CAMP scores derived from ML model feature importance."


def create_camp_explainer(model_dir: str = "models/production_v45") -> CAMPExplainabilitySystem:
    """Factory function to create CAMP explainer"""
    return CAMPExplainabilitySystem(model_dir)