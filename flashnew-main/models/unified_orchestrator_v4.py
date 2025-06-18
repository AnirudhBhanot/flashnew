#!/usr/bin/env python3
"""
Unified Orchestrator V4 - With Integrated CAMP Explainability
This version ensures CAMP scores explain ML predictions rather than contradicting them
"""

import os
import sys
import json
import pickle
import logging
import numpy as np
import pandas as pd
from typing import Dict, List, Any, Union, Optional, Tuple
from datetime import datetime
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from feature_config import (
    ALL_FEATURES, CAPITAL_FEATURES, ADVANTAGE_FEATURES, 
    MARKET_FEATURES, PEOPLE_FEATURES
)
from models.camp_explainability import create_camp_explainer, CAMPExplanation

logger = logging.getLogger(__name__)

class UnifiedOrchestratorV4:
    """
    Enhanced orchestrator with integrated CAMP explainability
    Ensures CAMP scores align with and explain ML predictions
    """
    
    def __init__(self, model_dir: str = "models/production_v45"):
        self.model_dir = model_dir
        self.models = {}
        self.model_metadata = {}
        self.config = self._load_config()
        self.camp_explainer = create_camp_explainer(model_dir)
        self._load_models()
        
        # Categorical encodings
        self.categorical_mappings = {
            'investor_tier_primary': {
                'Tier 1': 1.0,
                'Tier 2': 0.75,
                'Tier 3': 0.5,
                'No Tier': 0.25,
                'Unknown': 0.25
            },
            'sector': {
                'AI': 0.9,
                'SaaS': 0.85,
                'Fintech': 0.8,
                'Healthcare': 0.75,
                'E-commerce': 0.7,
                'Marketplace': 0.65,
                'Hardware': 0.6,
                'Services': 0.5,
                'Other': 0.5
            },
            'funding_stage': {
                'series_c+': 1.0,
                'series_b': 0.8,
                'series_a': 0.6,
                'seed': 0.4,
                'pre_seed': 0.2,
                'unknown': 0.3
            }
        }
        
    def _load_config(self) -> Dict:
        """Load orchestrator configuration"""
        config_path = os.path.join(self.model_dir, "orchestrator_config.json")
        
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                return json.load(f)
        else:
            # Default config
            return {
                "weights": {
                    "dna_analyzer": 0.25,
                    "temporal_model": 0.25,
                    "industry_model": 0.25,
                    "ensemble_model": 0.25
                },
                "thresholds": {
                    "strong_pass": 0.75,
                    "pass": 0.60,
                    "conditional_pass": 0.40,
                    "fail": 0.20,
                    "strong_fail": 0.0
                }
            }
    
    def _load_models(self):
        """Load ML models"""
        model_files = {
            'dna_analyzer': 'dna_analyzer.pkl',
            'temporal_model': 'temporal_model.pkl',
            'industry_model': 'industry_model.pkl',
            'ensemble_model': 'ensemble_model.pkl'
        }
        
        for name, filename in model_files.items():
            model_path = os.path.join(self.model_dir, filename)
            if os.path.exists(model_path):
                try:
                    with open(model_path, 'rb') as f:
                        self.models[name] = pickle.load(f)
                    logger.info(f"Loaded {name} from {model_path}")
                except Exception as e:
                    logger.error(f"Error loading {name}: {e}")
            else:
                logger.warning(f"Model file not found: {model_path}")
    
    def normalize_features(self, features: pd.DataFrame) -> pd.DataFrame:
        """
        Enhanced normalization that properly handles categorical features
        """
        normalized = features.copy()
        
        # Define feature categories
        MONETARY_FEATURES = [
            'total_capital_raised_usd', 'cash_on_hand_usd', 'monthly_burn_usd',
            'revenue_mrr_usd', 'gross_burn_usd', 'marketing_spend_usd',
            'r_and_d_spend_usd', 'current_valuation_usd', 'last_round_size_usd',
            'total_addressable_market_usd', 'serviceable_addressable_market_usd',
            'ltv_value_usd', 'cac_value_usd', 'arpu_value_usd',
            'tam_size_usd', 'sam_size_usd', 'som_size_usd'
        ]
        
        PERCENTAGE_FEATURES = [
            'market_growth_rate_percent', 'user_growth_rate_percent', 
            'net_dollar_retention_percent', 'customer_concentration_percent',
            'gross_margin_percent', 'revenue_growth_rate_percent'
        ]
        
        SCORE_FEATURES = [
            'tech_differentiation_score', 'switching_cost_score', 'brand_strength_score',
            'scalability_score', 'board_advisor_experience_score', 'competition_intensity',
            'execution_risk_score', 'vertical_integration_score', 'partnership_leverage_score',
            'predictive_modeling_score', 'cash_efficiency_score'
        ]
        
        CATEGORICAL_FEATURES = ['investor_tier_primary', 'sector', 'funding_stage']
        
        # Apply normalization based on feature type
        for col in normalized.columns:
            if col in CATEGORICAL_FEATURES:
                # Handle categorical features
                normalized[col] = normalized[col].apply(
                    lambda x: self.categorical_mappings.get(col, {}).get(x, 0.5)
                )
            elif col in MONETARY_FEATURES:
                # Log scale for monetary values
                normalized[col] = normalized[col].apply(
                    lambda x: np.clip(np.log10(max(x, 1)) / 9, 0, 1) if pd.notna(x) else 0
                )
            elif col in PERCENTAGE_FEATURES:
                # Percentages: handle different ranges
                if col in ['net_dollar_retention_percent']:
                    # NDR typically 80-140%
                    normalized[col] = np.clip((normalized[col] - 80) / 60, 0, 1)
                elif col == 'customer_concentration_percent':
                    # Lower is better for concentration
                    normalized[col] = np.clip(1 - (normalized[col] / 100), 0, 1)
                else:
                    # Standard percentage 0-100%
                    normalized[col] = np.clip(normalized[col] / 100, 0, 1)
            elif col in SCORE_FEATURES:
                # Scores typically 1-5
                if col == 'execution_risk_score':
                    # Lower is better for risk
                    normalized[col] = 1 - (normalized[col] - 1) / 4
                else:
                    normalized[col] = (normalized[col] - 1) / 4
            elif col == 'runway_months':
                # Runway: 0-24 months optimal
                normalized[col] = np.clip(normalized[col] / 24, 0, 1)
            elif col == 'burn_multiple':
                # Burn multiple: lower is better, inverse scale
                normalized[col] = np.clip(1 / (1 + normalized[col] / 5), 0, 1)
            elif col in ['company_age_months']:
                # Age: 0-60 months
                normalized[col] = np.clip(normalized[col] / 60, 0, 1)
            elif 'count' in col:
                # Count features: 0-20 typical
                normalized[col] = np.clip(normalized[col] / 20, 0, 1)
            elif col in ['has_repeat_founder', 'has_debt', 'network_effects_present',
                         'has_data_moat', 'regulatory_advantage_present']:
                # Binary features - already 0 or 1
                normalized[col] = normalized[col].astype(float)
            else:
                # Default normalization for unknown features
                if normalized[col].dtype in ['int64', 'float64']:
                    # Normalize numeric features to 0-1
                    min_val = normalized[col].min()
                    max_val = normalized[col].max()
                    if max_val > min_val:
                        normalized[col] = (normalized[col] - min_val) / (max_val - min_val)
                    else:
                        normalized[col] = 0.5
        
        return normalized
    
    def prepare_features_for_model(self, features: pd.DataFrame, model_name: str) -> np.ndarray:
        """Prepare features for specific model requirements"""
        # Ensure all features are present
        for feat in ALL_FEATURES:
            if feat not in features.columns:
                features[feat] = 0
        
        # Get features in correct order
        base_features = features[ALL_FEATURES].values
        
        # Each model expects exactly 45 features now
        # No more adding CAMP scores or temporal features
        return base_features
    
    def predict(self, features: Union[pd.DataFrame, Dict]) -> Dict:
        """
        Generate prediction with integrated CAMP explainability
        """
        # Convert to DataFrame if needed
        if isinstance(features, dict):
            # Store original for explanation
            original_features = features.copy()
            features = pd.DataFrame([features])
        else:
            original_features = features.iloc[0].to_dict()
        
        # Ensure numeric types and handle missing values
        for col in features.columns:
            if col not in ['investor_tier_primary', 'sector', 'funding_stage']:
                features[col] = pd.to_numeric(features[col], errors='coerce').fillna(0)
        
        # Normalize features
        normalized = self.normalize_features(features)
        
        predictions = {}
        weights = self.config['weights']
        
        # Get predictions from each model
        for model_name, model in self.models.items():
            if model_name == 'ensemble_model':
                continue  # Handle ensemble separately
                
            try:
                # Prepare features - all models now expect 45 features
                model_features = self.prepare_features_for_model(normalized, model_name)
                
                # Get prediction
                if hasattr(model, 'predict_proba'):
                    pred_proba = model.predict_proba(model_features)[:, 1]
                else:
                    # Fallback for models without predict_proba
                    pred_proba = model.predict(model_features)
                    
                predictions[model_name] = float(pred_proba[0])
                logger.info(f"{model_name} prediction: {predictions[model_name]:.3f}")
                
            except Exception as e:
                logger.error(f"Error in {model_name}: {e}")
                predictions[model_name] = 0.5
        
        # Calculate weighted average
        weighted_sum = sum(
            pred * weights.get(name, 0.25) 
            for name, pred in predictions.items()
        )
        weight_sum = sum(weights.get(name, 0.25) for name in predictions.keys())
        
        if weight_sum > 0:
            success_probability = weighted_sum / weight_sum
        else:
            success_probability = 0.5
        
        # Handle ensemble if available
        if 'ensemble_model' in self.models and len(predictions) >= 3:
            try:
                ensemble_features = np.array([[
                    predictions.get('dna_analyzer', 0.5),
                    predictions.get('temporal_model', 0.5),
                    predictions.get('industry_model', 0.5)
                ]])
                
                ensemble_pred = self.models['ensemble_model'].predict_proba(ensemble_features)[:, 1]
                predictions['ensemble_model'] = float(ensemble_pred[0])
                
                # Blend with ensemble
                if weights.get('ensemble_model', 0) > 0:
                    success_probability = (
                        success_probability * 0.7 +
                        predictions['ensemble_model'] * 0.3
                    )
            except Exception as e:
                logger.error(f"Ensemble prediction error: {e}")
        
        # Ensure valid probability
        success_probability = max(0.01, min(0.99, success_probability))
        
        # Get CAMP explanation that aligns with ML prediction
        original_features['success_probability'] = success_probability
        camp_explanation = self.camp_explainer.explain_prediction(
            original_features, 
            success_probability
        )
        
        # Determine verdict
        verdict = self._determine_verdict(success_probability)
        
        # Calculate model agreement
        if len(predictions) > 1:
            model_values = list(predictions.values())
            model_agreement = 1 - np.std(model_values)
            confidence_score = min(0.95, model_agreement * 0.8 + 0.2)
        else:
            model_agreement = 0.8
            confidence_score = 0.7
        
        # Build response with integrated CAMP scores
        result = {
            "success_probability": success_probability,
            "confidence_score": confidence_score,
            "verdict": verdict,
            "model_predictions": predictions,
            "model_agreement": model_agreement,
            "camp_analysis": {
                "capital": camp_explanation.capital_score,
                "advantage": camp_explanation.advantage_score,
                "market": camp_explanation.market_score,
                "people": camp_explanation.people_score
            },
            "critical_factors": camp_explanation.critical_factors,
            "alignment_explanation": camp_explanation.alignment_explanation,
            "risk_level": self._calculate_risk_level(
                success_probability, 
                camp_explanation
            ),
            "insights": self._generate_insights(
                camp_explanation,
                success_probability
            )
        }
        
        return result
    
    def _determine_verdict(self, probability: float) -> str:
        """Determine investment verdict"""
        thresholds = self.config['thresholds']
        
        if probability >= thresholds['strong_pass']:
            return "STRONG PASS"
        elif probability >= thresholds['pass']:
            return "PASS"
        elif probability >= thresholds['conditional_pass']:
            return "CONDITIONAL PASS"
        elif probability >= thresholds['fail']:
            return "FAIL"
        else:
            return "STRONG FAIL"
    
    def _calculate_risk_level(self, probability: float, 
                            camp_explanation: CAMPExplanation) -> str:
        """Calculate risk level based on probability and CAMP scores"""
        camp_scores = [
            camp_explanation.capital_score,
            camp_explanation.advantage_score,
            camp_explanation.market_score,
            camp_explanation.people_score
        ]
        
        min_camp = min(camp_scores)
        avg_camp = np.mean(camp_scores)
        
        # Critical weakness in any pillar
        if min_camp < 0.2 or probability < 0.2:
            return "High Risk"
        elif min_camp < 0.3 or probability < 0.4:
            return "Medium-High Risk" 
        elif avg_camp < 0.5 or probability < 0.6:
            return "Medium Risk"
        elif probability < 0.75:
            return "Low-Medium Risk"
        else:
            return "Low Risk"
    
    def _generate_insights(self, camp_explanation: CAMPExplanation,
                         probability: float) -> List[str]:
        """Generate actionable insights"""
        insights = []
        
        # Overall assessment
        if probability >= 0.7:
            insights.append("Strong investment opportunity with high success probability")
        elif probability >= 0.5:
            insights.append("Promising opportunity with moderate risk")
        else:
            insights.append("High-risk investment requiring significant improvements")
        
        # Critical factors
        for factor in camp_explanation.critical_factors[:3]:
            insights.append(factor['explanation'])
        
        # CAMP-specific insights
        camp_scores = {
            'Capital': camp_explanation.capital_score,
            'Advantage': camp_explanation.advantage_score,
            'Market': camp_explanation.market_score,
            'People': camp_explanation.people_score
        }
        
        for pillar, score in camp_scores.items():
            if score < 0.3:
                insights.append(f"{pillar} pillar needs immediate attention (score: {score:.1%})")
            elif score > 0.7:
                insights.append(f"Strong {pillar} fundamentals (score: {score:.1%})")
        
        return insights[:5]  # Top 5 insights


def create_orchestrator(model_dir: str = "models/production_v45") -> UnifiedOrchestratorV4:
    """Factory function to create orchestrator V4"""
    return UnifiedOrchestratorV4(model_dir)