#!/usr/bin/env python3
"""
Complete Hybrid Orchestrator
Combines Base, Pattern, Stage, Industry, and CAMP models for maximum performance
"""

import numpy as np
import pandas as pd
import joblib
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)

@dataclass
class CompleteHybridPrediction:
    """Comprehensive prediction result"""
    # Core predictions
    final_probability: float
    confidence_score: float
    verdict: str
    risk_level: str
    
    # Component predictions
    base_probability: float
    pattern_probability: float
    stage_probability: float
    industry_probability: float
    camp_scores: Dict[str, float]
    
    # Detailed breakdowns
    base_predictions: Dict[str, float]
    pattern_predictions: Dict[str, float]
    stage_prediction: float
    industry_prediction: float
    camp_predictions: Dict[str, float]
    
    # Insights
    dominant_patterns: List[str]
    stage_fit: str
    industry_fit: str
    camp_strengths: List[str]
    camp_weaknesses: List[str]
    recommendations: List[str]
    
    # Metadata
    model_weights: Dict[str, float]
    models_used: int
    prediction_variance: float

class CompleteHybridOrchestrator:
    """Orchestrates predictions across all model types"""
    
    def __init__(self):
        self.models = {
            'base': {},
            'patterns': {},
            'stages': {},
            'industries': {},
            'camp': {}
        }
        
        # Sophisticated weighting system
        self.weights = {
            'base': 0.35,      # 35% - Foundation models
            'patterns': 0.25,  # 25% - Pattern recognition
            'stage': 0.15,     # 15% - Stage-specific insights
            'industry': 0.15,  # 15% - Industry expertise
            'camp': 0.10       # 10% - CAMP refinement
        }
        
        self.loaded = False
        self.encoders = None
        
    def load_models(self):
        """Load all model types"""
        if self.loaded:
            return
            
        logger.info("Loading complete hybrid system...")
        
        # Load base contractual models
        self._load_base_models()
        
        # Load pattern models
        self._load_pattern_models()
        
        # Load stage models
        self._load_stage_models()
        
        # Load industry models
        self._load_industry_models()
        
        # Load CAMP models
        self._load_camp_models()
        
        # Load encoders
        encoder_path = Path("models/complete_hybrid/label_encoders.pkl")
        if encoder_path.exists():
            self.encoders = joblib.load(encoder_path)
        
        self.loaded = True
        total_models = sum(len(models) for models in self.models.values())
        logger.info(f"Loaded {total_models} models across 5 categories")
        
    def _load_base_models(self):
        """Load base contractual models"""
        base_dir = Path("models/contractual")
        if not base_dir.exists():
            base_dir = Path("models/production_v45_fixed")
        
        for model_name in ['dna_analyzer', 'temporal_model', 'industry_model', 'ensemble_model']:
            model_path = base_dir / f"{model_name}.pkl"
            if model_path.exists():
                try:
                    data = joblib.load(model_path)
                    if isinstance(data, dict) and 'sklearn_model' in data:
                        self.models['base'][model_name] = data['sklearn_model']
                    else:
                        self.models['base'][model_name] = data
                    logger.info(f"Loaded base model: {model_name}")
                except Exception as e:
                    logger.warning(f"Could not load {model_name}: {e}")
                    
    def _load_pattern_models(self):
        """Load pattern models"""
        pattern_dir = Path("models/hybrid_patterns")
        if pattern_dir.exists():
            for model_file in pattern_dir.glob("*_model.pkl"):
                pattern_name = model_file.stem.replace("_model", "")
                self.models['patterns'][pattern_name] = joblib.load(model_file)
                
    def _load_stage_models(self):
        """Load stage models"""
        stage_dir = Path("models/complete_hybrid")
        if stage_dir.exists():
            for model_file in stage_dir.glob("stage_*_model.pkl"):
                stage_name = model_file.stem.replace("stage_", "").replace("_model", "")
                self.models['stages'][stage_name] = joblib.load(model_file)
                
    def _load_industry_models(self):
        """Load industry models"""
        industry_dir = Path("models/complete_hybrid")
        if industry_dir.exists():
            for model_file in industry_dir.glob("industry_*_model.pkl"):
                industry_name = model_file.stem.replace("industry_", "").replace("_model", "")
                self.models['industries'][industry_name] = joblib.load(model_file)
                
    def _load_camp_models(self):
        """Load CAMP models"""
        camp_dir = Path("models/complete_hybrid")
        if camp_dir.exists():
            for camp_type in ['capital', 'advantage', 'market', 'people']:
                model_path = camp_dir / f"camp_{camp_type}_model.pkl"
                if model_path.exists():
                    self.models['camp'][camp_type] = joblib.load(model_path)
    
    def prepare_features(self, data: Dict[str, Any]) -> pd.DataFrame:
        """Prepare features for all models"""
        df = pd.DataFrame([data])
        
        # Handle categorical encoding
        categorical_cols = ['funding_stage', 'investor_tier_primary', 'product_stage', 'sector']
        
        for col in categorical_cols:
            if col in df.columns:
                # Create encoded version
                if self.encoders and col in self.encoders:
                    # Use saved encoders
                    categories = self.encoders[col]
                    df[f'{col}_encoded'] = pd.Categorical(df[col], categories=categories).codes
                else:
                    # Simple encoding
                    df[f'{col}_encoded'] = pd.Categorical(df[col]).codes
        
        # Convert booleans
        bool_cols = ['has_debt', 'network_effects_present', 'has_data_moat', 'regulatory_advantage_present']
        for col in bool_cols:
            if col in df.columns:
                df[col] = df[col].astype(int)
        
        return df
    
    def predict(self, data: Dict[str, Any]) -> CompleteHybridPrediction:
        """Make comprehensive prediction using all models"""
        if not self.loaded:
            self.load_models()
        
        # Prepare features
        features = self.prepare_features(data)
        
        # Get predictions from each model type
        base_prob, base_preds = self._predict_base(features)
        pattern_prob, pattern_preds = self._predict_patterns(features)
        stage_prob, stage_pred = self._predict_stage(features, data.get('funding_stage'))
        industry_prob, industry_pred = self._predict_industry(features, data.get('sector'))
        camp_scores, camp_preds = self._predict_camp(features)
        
        # Calculate weighted final probability
        final_prob = (
            base_prob * self.weights['base'] +
            pattern_prob * self.weights['patterns'] +
            stage_prob * self.weights['stage'] +
            industry_prob * self.weights['industry'] +
            np.mean(list(camp_scores.values())) * self.weights['camp']
        )
        
        # Calculate confidence based on model agreement
        all_probs = [base_prob, pattern_prob, stage_prob, industry_prob] + list(camp_scores.values())
        all_probs = [p for p in all_probs if p != 0.5]  # Exclude defaults
        
        if len(all_probs) > 1:
            pred_variance = np.var(all_probs)
            confidence = 0.9 - (pred_variance * 2)  # Lower variance = higher confidence
            confidence = max(0.5, min(0.95, confidence))
        else:
            confidence = 0.6
        
        # Determine verdict and risk
        verdict, risk_level = self._determine_verdict(final_prob, confidence)
        
        # Get insights
        dominant_patterns = self._get_dominant_patterns(pattern_preds)
        camp_strengths, camp_weaknesses = self._analyze_camp_scores(camp_scores)
        recommendations = self._generate_recommendations(
            pattern_preds, stage_pred, industry_pred, camp_scores
        )
        
        # Count models used
        models_used = (
            len(base_preds) + len(pattern_preds) + 
            (1 if stage_pred > 0 else 0) + 
            (1 if industry_pred > 0 else 0) + 
            len(camp_preds)
        )
        
        return CompleteHybridPrediction(
            final_probability=final_prob,
            confidence_score=confidence,
            verdict=verdict,
            risk_level=risk_level,
            base_probability=base_prob,
            pattern_probability=pattern_prob,
            stage_probability=stage_prob,
            industry_probability=industry_prob,
            camp_scores=camp_scores,
            base_predictions=base_preds,
            pattern_predictions=pattern_preds,
            stage_prediction=stage_pred,
            industry_prediction=industry_pred,
            camp_predictions=camp_preds,
            dominant_patterns=dominant_patterns,
            stage_fit=f"{data.get('funding_stage', 'Unknown')} - {'Strong' if stage_prob > 0.7 else 'Moderate' if stage_prob > 0.5 else 'Weak'}",
            industry_fit=f"{data.get('sector', 'Unknown')} - {'Strong' if industry_prob > 0.7 else 'Moderate' if industry_prob > 0.5 else 'Weak'}",
            camp_strengths=camp_strengths,
            camp_weaknesses=camp_weaknesses,
            recommendations=recommendations,
            model_weights=self.weights,
            models_used=models_used,
            prediction_variance=pred_variance if len(all_probs) > 1 else 0.0
        )
    
    def _predict_base(self, features: pd.DataFrame) -> Tuple[float, Dict[str, float]]:
        """Get base model predictions"""
        predictions = {}
        
        # Try unified orchestrator first
        try:
            from models.unified_orchestrator_v3 import get_orchestrator
            orch = get_orchestrator()
            result = orch.predict(features)
            return result.get('success_probability', 0.5), result.get('model_predictions', {})
        except:
            pass
        
        # Fall back to individual models
        if not self.models['base']:
            return 0.5, {}
        
        # DNA Analyzer
        if 'dna_analyzer' in self.models['base']:
            try:
                # Add CAMP scores
                features_camp = features.copy()
                features_camp['capital_score'] = 0.5
                features_camp['advantage_score'] = 0.5
                features_camp['market_score'] = 0.5
                features_camp['people_score'] = 0.5
                pred = self.models['base']['dna_analyzer'].predict_proba(features_camp)[:, 1]
                predictions['dna_analyzer'] = float(pred[0])
            except:
                predictions['dna_analyzer'] = 0.5
        
        # Other base models...
        
        return np.mean(list(predictions.values())) if predictions else 0.5, predictions
    
    def _predict_patterns(self, features: pd.DataFrame) -> Tuple[float, Dict[str, float]]:
        """Get pattern predictions"""
        if not self.models['patterns']:
            return 0.5, {}
        
        predictions = {}
        feature_cols = self._get_numeric_features(features)
        
        for pattern_name, model in self.models['patterns'].items():
            try:
                pred = model.predict_proba(features[feature_cols])[:, 1]
                predictions[pattern_name] = float(pred[0])
            except:
                predictions[pattern_name] = 0.5
        
        return np.mean(list(predictions.values())) if predictions else 0.5, predictions
    
    def _predict_stage(self, features: pd.DataFrame, stage: str) -> Tuple[float, float]:
        """Get stage-specific prediction"""
        if not self.models['stages'] or not stage:
            return 0.5, 0.0
        
        # Normalize stage name
        stage_key = stage.lower().replace(' ', '_').replace('+', '_plus')
        
        if stage_key in self.models['stages']:
            try:
                feature_cols = self._get_numeric_features(features)
                pred = self.models['stages'][stage_key].predict_proba(features[feature_cols])[:, 1]
                return float(pred[0]), float(pred[0])
            except:
                return 0.5, 0.0
        
        return 0.5, 0.0
    
    def _predict_industry(self, features: pd.DataFrame, industry: str) -> Tuple[float, float]:
        """Get industry-specific prediction"""
        if not self.models['industries'] or not industry:
            return 0.5, 0.0
        
        # Normalize industry name
        industry_key = industry.lower().replace(' ', '_').replace('/', '_')
        
        if industry_key in self.models['industries']:
            try:
                feature_cols = self._get_numeric_features(features)
                pred = self.models['industries'][industry_key].predict_proba(features[feature_cols])[:, 1]
                return float(pred[0]), float(pred[0])
            except:
                return 0.5, 0.0
        
        return 0.5, 0.0
    
    def _predict_camp(self, features: pd.DataFrame) -> Tuple[Dict[str, float], Dict[str, float]]:
        """Get CAMP predictions"""
        if not self.models['camp']:
            default_scores = {'capital': 0.5, 'advantage': 0.5, 'market': 0.5, 'people': 0.5}
            return default_scores, {}
        
        scores = {}
        predictions = {}
        
        # Define CAMP features
        camp_features = {
            'capital': ['total_capital_raised_usd', 'cash_on_hand_usd', 'monthly_burn_usd', 
                       'runway_months', 'burn_multiple', 'investor_tier_primary_encoded'],
            'advantage': ['patent_count', 'network_effects_present', 'has_data_moat', 
                         'regulatory_advantage_present', 'tech_differentiation_score', 
                         'switching_cost_score', 'brand_strength_score', 'scalability_score'],
            'market': ['tam_size_usd', 'sam_size_usd', 'som_size_usd', 'market_growth_rate_percent',
                      'customer_count', 'customer_concentration_percent', 'user_growth_rate_percent',
                      'net_dollar_retention_percent', 'competition_intensity', 'competitors_named_count',
                      'sector_encoded'],
            'people': ['founders_count', 'team_size_full_time', 'years_experience_avg',
                      'domain_expertise_years_avg', 'prior_startup_experience_count',
                      'prior_successful_exits_count', 'board_advisor_experience_score',
                      'advisors_count', 'team_diversity_percent', 'key_person_dependency']
        }
        
        for camp_type, model in self.models['camp'].items():
            try:
                # Get features for this CAMP type
                camp_feats = camp_features.get(camp_type, [])
                available_feats = [f for f in camp_feats if f in features.columns]
                
                # Add general features
                general_feats = ['funding_stage_encoded', 'product_stage_encoded', 
                               'annual_revenue_run_rate', 'revenue_growth_rate_percent']
                all_feats = available_feats + [f for f in general_feats if f in features.columns]
                
                pred = model.predict_proba(features[all_feats])[:, 1]
                scores[camp_type] = float(pred[0])
                predictions[f'camp_{camp_type}'] = float(pred[0])
            except:
                scores[camp_type] = 0.5
        
        # Ensure all CAMP scores exist
        for camp in ['capital', 'advantage', 'market', 'people']:
            if camp not in scores:
                scores[camp] = 0.5
        
        return scores, predictions
    
    def _get_numeric_features(self, features: pd.DataFrame) -> List[str]:
        """Get numeric feature columns"""
        # Exclude original categorical columns
        exclude = ['funding_stage', 'investor_tier_primary', 'product_stage', 'sector']
        numeric_cols = [col for col in features.columns if col not in exclude]
        return numeric_cols
    
    def _determine_verdict(self, probability: float, confidence: float) -> Tuple[str, str]:
        """Determine verdict and risk level"""
        if probability >= 0.75 and confidence >= 0.8:
            return "STRONG PASS", "LOW"
        elif probability >= 0.65:
            return "PASS", "LOW"
        elif probability >= 0.55:
            return "CONDITIONAL PASS", "MEDIUM"
        elif probability >= 0.45:
            return "CONDITIONAL FAIL", "MEDIUM"
        elif probability >= 0.35:
            return "FAIL", "HIGH"
        else:
            return "STRONG FAIL", "HIGH"
    
    def _get_dominant_patterns(self, pattern_preds: Dict[str, float]) -> List[str]:
        """Get top patterns"""
        if not pattern_preds:
            return []
        
        sorted_patterns = sorted(pattern_preds.items(), key=lambda x: x[1], reverse=True)
        return [p[0] for p in sorted_patterns[:3] if p[1] > 0.6]
    
    def _analyze_camp_scores(self, camp_scores: Dict[str, float]) -> Tuple[List[str], List[str]]:
        """Analyze CAMP scores for strengths and weaknesses"""
        strengths = []
        weaknesses = []
        
        camp_names = {
            'capital': 'Capital efficiency',
            'advantage': 'Competitive advantage',
            'market': 'Market opportunity',
            'people': 'Team strength'
        }
        
        for camp, score in camp_scores.items():
            if score > 0.7:
                strengths.append(camp_names.get(camp, camp))
            elif score < 0.4:
                weaknesses.append(camp_names.get(camp, camp))
        
        return strengths, weaknesses
    
    def _generate_recommendations(self, patterns: Dict, stage_pred: float, 
                                 industry_pred: float, camp_scores: Dict) -> List[str]:
        """Generate actionable recommendations"""
        recommendations = []
        
        # Pattern-based recommendations
        if patterns:
            weak_patterns = [p for p, score in patterns.items() if score < 0.4]
            if weak_patterns:
                recommendations.append(f"Consider {weak_patterns[0].replace('_', ' ')} strategies")
        
        # Stage recommendations
        if stage_pred < 0.5:
            recommendations.append("Strengthen stage-specific metrics")
        
        # CAMP recommendations
        if camp_scores.get('capital', 0.5) < 0.4:
            recommendations.append("Improve capital efficiency and runway")
        if camp_scores.get('market', 0.5) < 0.4:
            recommendations.append("Validate market size and growth potential")
        
        return recommendations[:3]  # Top 3 recommendations