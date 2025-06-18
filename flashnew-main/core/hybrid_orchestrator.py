"""
Hybrid Orchestrator - Combines base models with pattern, stage, and industry models
Achieves the best of both worlds: safety + performance
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime
import logging
from dataclasses import dataclass

from .model_wrapper import ContractualModel
from .enhanced_contracts import PatternType, FundingStage, Industry, EnhancedContractBuilder
from .pattern_contracts import PatternContractFactory
from .feature_registry import feature_registry

logger = logging.getLogger(__name__)


@dataclass
class PredictionContext:
    """Context for making predictions"""
    funding_stage: FundingStage
    industry: Industry
    detected_patterns: List[PatternType]
    confidence_scores: Dict[str, float]
    

@dataclass
class HybridPrediction:
    """Result from hybrid prediction"""
    # Core predictions
    base_probability: float  # From base 4 models
    pattern_adjusted_probability: float  # After pattern adjustment
    final_probability: float  # Final hybrid result
    
    # Component scores
    base_predictions: Dict[str, float]
    pattern_scores: Dict[str, float]
    stage_score: float
    industry_score: float
    
    # Analysis
    dominant_pattern: Optional[PatternType]
    pattern_synergy: float
    confidence_score: float
    
    # Insights
    verdict: str
    risk_level: str
    key_strengths: List[str]
    improvement_areas: List[str]
    pattern_recommendations: List[str]


class HybridOrchestrator:
    """Orchestrates predictions across all model types for maximum accuracy"""
    
    def __init__(self, 
                 base_models: Dict[str, ContractualModel],
                 pattern_models: Optional[Dict[str, ContractualModel]] = None,
                 use_patterns: bool = True,
                 use_stage_specific: bool = True,
                 use_industry_specific: bool = True):
        """
        Initialize hybrid orchestrator
        
        Args:
            base_models: The 4 core contractual models (DNA, temporal, industry, ensemble)
            pattern_models: Optional pre-loaded pattern models
            use_patterns: Whether to use pattern analysis
            use_stage_specific: Whether to use stage-specific adjustments
            use_industry_specific: Whether to use industry-specific adjustments
        """
        self.base_models = base_models
        self.pattern_models = pattern_models or {}
        self.use_patterns = use_patterns
        self.use_stage_specific = use_stage_specific
        self.use_industry_specific = use_industry_specific
        
        # Initialize builders
        self.enhanced_builder = EnhancedContractBuilder(feature_registry)
        self.pattern_factory = PatternContractFactory()
        
        # Weights for combining predictions
        self.weights = {
            'base': 0.6,  # 60% weight to base models
            'patterns': 0.25,  # 25% to pattern analysis
            'stage': 0.075,  # 7.5% to stage-specific
            'industry': 0.075  # 7.5% to industry-specific
        }
        
        logger.info(f"Initialized hybrid orchestrator with {len(base_models)} base models")
    
    def predict(self, 
                startup_data: Dict[str, Any],
                detected_patterns: Optional[List[PatternType]] = None,
                return_diagnostics: bool = False) -> HybridPrediction:
        """
        Make a hybrid prediction using all available models
        
        Args:
            startup_data: Input features
            detected_patterns: Pre-detected patterns (optional)
            return_diagnostics: Whether to return detailed diagnostics
            
        Returns:
            HybridPrediction with comprehensive results
        """
        start_time = datetime.now()
        
        # Step 1: Get base predictions
        base_predictions = self._get_base_predictions(startup_data)
        base_probability = self._combine_base_predictions(base_predictions)
        
        # Step 2: Detect context
        context = self._detect_context(startup_data, detected_patterns)
        
        # Initialize results
        pattern_scores = {}
        pattern_adjusted_probability = base_probability
        stage_score = 0.5
        industry_score = 0.5
        
        # Step 3: Pattern analysis
        if self.use_patterns and context.detected_patterns:
            pattern_scores = self._analyze_patterns(startup_data, context.detected_patterns)
            pattern_modifier = self._compute_pattern_modifier(pattern_scores, context.detected_patterns)
            pattern_adjusted_probability = self._apply_modifier(base_probability, pattern_modifier)
        
        # Step 4: Stage-specific adjustment
        if self.use_stage_specific:
            stage_score = self._compute_stage_score(startup_data, context.funding_stage)
        
        # Step 5: Industry-specific adjustment
        if self.use_industry_specific:
            industry_score = self._compute_industry_score(startup_data, context.industry)
        
        # Step 6: Combine all components
        final_probability = self._combine_all_predictions(
            base_probability,
            pattern_adjusted_probability,
            stage_score,
            industry_score
        )
        
        # Step 7: Generate insights
        insights = self._generate_insights(
            startup_data,
            base_predictions,
            pattern_scores,
            context
        )
        
        # Calculate confidence
        confidence = self._calculate_confidence(
            base_predictions,
            pattern_scores,
            context
        )
        
        # Determine verdict and risk
        verdict = self._determine_verdict(final_probability, confidence)
        risk_level = self._assess_risk_level(final_probability, confidence, context)
        
        # Create result
        result = HybridPrediction(
            base_probability=base_probability,
            pattern_adjusted_probability=pattern_adjusted_probability,
            final_probability=final_probability,
            base_predictions=base_predictions,
            pattern_scores=pattern_scores,
            stage_score=stage_score,
            industry_score=industry_score,
            dominant_pattern=context.detected_patterns[0] if context.detected_patterns else None,
            pattern_synergy=self._calculate_pattern_synergy(pattern_scores),
            confidence_score=confidence,
            verdict=verdict,
            risk_level=risk_level,
            key_strengths=insights['strengths'],
            improvement_areas=insights['improvements'],
            pattern_recommendations=insights['pattern_recommendations']
        )
        
        if return_diagnostics:
            duration = (datetime.now() - start_time).total_seconds()
            logger.info(f"Hybrid prediction completed in {duration:.2f}s")
            logger.info(f"Base: {base_probability:.3f}, Pattern: {pattern_adjusted_probability:.3f}, Final: {final_probability:.3f}")
        
        return result
    
    def _get_base_predictions(self, startup_data: Dict[str, Any]) -> Dict[str, float]:
        """Get predictions from base models"""
        predictions = {}
        
        for name, model in self.base_models.items():
            if name != 'ensemble_model':
                try:
                    pred = model.predict(startup_data)
                    predictions[name] = float(pred[0])
                except Exception as e:
                    logger.error(f"Error in {name}: {e}")
                    predictions[name] = 0.5
        
        # Get ensemble prediction if we have base predictions
        if len(predictions) >= 3 and 'ensemble_model' in self.base_models:
            ensemble_input = {
                'dna_prediction': predictions.get('dna_analyzer', 0.5),
                'temporal_prediction': predictions.get('temporal_model', 0.5),
                'industry_prediction': predictions.get('industry_model', 0.5)
            }
            try:
                ensemble_pred = self.base_models['ensemble_model'].predict(ensemble_input)
                predictions['ensemble_model'] = float(ensemble_pred[0])
            except Exception as e:
                logger.error(f"Error in ensemble: {e}")
                predictions['ensemble_model'] = np.mean(list(predictions.values()))
        
        return predictions
    
    def _combine_base_predictions(self, predictions: Dict[str, float]) -> float:
        """Combine base model predictions"""
        if 'ensemble_model' in predictions:
            # Trust the ensemble more
            return predictions['ensemble_model']
        else:
            # Simple average
            return np.mean(list(predictions.values()))
    
    def _detect_context(self, 
                       startup_data: Dict[str, Any],
                       provided_patterns: Optional[List[PatternType]] = None) -> PredictionContext:
        """Detect the context for prediction"""
        # Detect funding stage
        funding_stage = self._detect_funding_stage(startup_data)
        
        # Detect industry
        industry = self._detect_industry(startup_data)
        
        # Detect patterns if not provided
        if provided_patterns:
            detected_patterns = provided_patterns
        else:
            detected_patterns = self._detect_patterns(startup_data)
        
        # Calculate confidence in detection
        confidence_scores = {
            'stage_detection': 0.9,  # High confidence if explicitly provided
            'industry_detection': 0.8,
            'pattern_detection': 0.7 if detected_patterns else 0.0
        }
        
        return PredictionContext(
            funding_stage=funding_stage,
            industry=industry,
            detected_patterns=detected_patterns,
            confidence_scores=confidence_scores
        )
    
    def _detect_funding_stage(self, startup_data: Dict[str, Any]) -> FundingStage:
        """Detect the funding stage from data"""
        stage_str = startup_data.get('funding_stage', 'seed')
        
        stage_map = {
            'pre_seed': FundingStage.PRE_SEED,
            'seed': FundingStage.SEED,
            'series_a': FundingStage.SERIES_A,
            'series_b': FundingStage.SERIES_B,
            'series_c': FundingStage.SERIES_C,
            'series_d_plus': FundingStage.SERIES_D_PLUS
        }
        
        return stage_map.get(stage_str, FundingStage.SEED)
    
    def _detect_industry(self, startup_data: Dict[str, Any]) -> Industry:
        """Detect the industry from data"""
        # Simple heuristics for now
        if startup_data.get('uses_ai_ml', False):
            return Industry.AI_ML
        elif startup_data.get('target_enterprise', False) and startup_data.get('cloud_native', False):
            return Industry.SAAS
        elif startup_data.get('platform_business', False):
            return Industry.MARKETPLACE
        else:
            return Industry.SAAS  # Default
    
    def _detect_patterns(self, startup_data: Dict[str, Any]) -> List[PatternType]:
        """Detect applicable patterns from startup data"""
        detected = []
        
        # Growth pattern detection
        revenue_growth = startup_data.get('revenue_growth_rate', 0)
        burn_multiple = startup_data.get('burn_multiple', 2)
        
        if revenue_growth > 200 and burn_multiple > 2.5:
            detected.append(PatternType.HIGH_BURN_GROWTH)
        elif revenue_growth > 100 and burn_multiple < 1.5:
            detected.append(PatternType.EFFICIENT_GROWTH)
        elif revenue_growth < 20:
            detected.append(PatternType.STALLED_GROWTH)
        
        # Business model detection
        if startup_data.get('net_revenue_retention', 0) > 110 and startup_data.get('target_enterprise', False):
            detected.append(PatternType.B2B_SAAS)
        elif startup_data.get('platform_business', False):
            detected.append(PatternType.PLATFORM_NETWORK)
        
        # Tech pattern detection
        if startup_data.get('uses_ai_ml', False):
            detected.append(PatternType.AI_ML_CORE)
        
        # Funding pattern detection
        if startup_data.get('total_capital_raised_usd', 0) < 500000 and burn_multiple < 1:
            detected.append(PatternType.BOOTSTRAP_PROFITABLE)
        elif startup_data.get('total_capital_raised_usd', 0) > 10000000:
            detected.append(PatternType.VC_HYPERGROWTH)
        
        return detected[:3]  # Return top 3 patterns
    
    def _analyze_patterns(self, 
                         startup_data: Dict[str, Any],
                         patterns: List[PatternType]) -> Dict[str, float]:
        """Analyze pattern fit scores"""
        pattern_scores = {}
        
        for pattern in patterns:
            # Check if we have a pre-loaded model
            if pattern.value in self.pattern_models:
                try:
                    model = self.pattern_models[pattern.value]
                    pred = model.predict(startup_data)
                    pattern_scores[pattern.value] = float(pred[0])
                except Exception as e:
                    logger.error(f"Error in pattern model {pattern.value}: {e}")
                    pattern_scores[pattern.value] = 0.5
            else:
                # Use pattern profile matching
                profile = self.pattern_factory.pattern_profiles.get(pattern)
                if profile:
                    df = pd.DataFrame([startup_data])
                    score = self.pattern_factory._compute_pattern_match_score(df, profile)
                    pattern_scores[pattern.value] = score
        
        return pattern_scores
    
    def _compute_pattern_modifier(self, 
                                pattern_scores: Dict[str, float],
                                patterns: List[PatternType]) -> float:
        """Compute success modifier based on pattern analysis"""
        if not pattern_scores:
            return 1.0
        
        # Get the best pattern match
        best_score = max(pattern_scores.values())
        
        # Strong pattern match increases success probability
        if best_score > 0.8:
            modifier = 1.2  # 20% boost
        elif best_score > 0.6:
            modifier = 1.1  # 10% boost
        elif best_score < 0.3:
            modifier = 0.9  # 10% penalty
        else:
            modifier = 1.0
        
        # Check for synergistic patterns
        if len(patterns) > 1:
            synergy = self._check_pattern_synergy(patterns)
            modifier *= (1 + synergy)
        
        return modifier
    
    def _apply_modifier(self, base_probability: float, modifier: float) -> float:
        """Apply modifier while keeping probability in valid range"""
        adjusted = base_probability * modifier
        
        # Use logit transformation to keep in bounds
        if adjusted <= 0:
            return 0.01
        elif adjusted >= 1:
            return 0.99
        else:
            # Apply smoothing near boundaries
            if adjusted < 0.1:
                adjusted = 0.1 * (adjusted / 0.1) ** 0.5
            elif adjusted > 0.9:
                adjusted = 1 - 0.1 * ((1 - adjusted) / 0.1) ** 0.5
            
            return adjusted
    
    def _compute_stage_score(self, 
                           startup_data: Dict[str, Any],
                           stage: FundingStage) -> float:
        """Compute stage-specific success score"""
        stage_requirements = self.enhanced_builder.stage_requirements.get(stage)
        if not stage_requirements:
            return 0.5
        
        scores = []
        for feature in stage_requirements['critical_features']:
            if feature in startup_data:
                value = startup_data[feature]
                # Normalize based on stage expectations
                if feature in stage_requirements.get('min_thresholds', {}):
                    threshold = stage_requirements['min_thresholds'][feature]
                    score = min(1.0, value / (threshold * 2))
                else:
                    score = min(1.0, value / 100)  # Simple normalization
                scores.append(score)
        
        return np.mean(scores) if scores else 0.5
    
    def _compute_industry_score(self, 
                              startup_data: Dict[str, Any],
                              industry: Industry) -> float:
        """Compute industry-specific success score"""
        industry_requirements = self.enhanced_builder.industry_requirements.get(industry)
        if not industry_requirements:
            return 0.5
        
        scores = []
        for feature in industry_requirements['critical_features']:
            if feature in startup_data:
                value = startup_data[feature]
                # Industry-specific scoring
                if industry == Industry.SAAS and feature == 'net_revenue_retention':
                    score = min(1.0, value / 120)  # 120% is excellent for SaaS
                elif industry == Industry.AI_ML and feature == 'research_development_percent':
                    score = min(1.0, value / 30)  # 30% R&D is high for AI
                else:
                    score = min(1.0, value / 100)
                scores.append(score)
        
        return np.mean(scores) if scores else 0.5
    
    def _combine_all_predictions(self,
                               base: float,
                               pattern_adjusted: float,
                               stage: float,
                               industry: float) -> float:
        """Combine all prediction components"""
        # If pattern adjustment is significant, weight it more
        if abs(pattern_adjusted - base) > 0.1:
            # Pattern signal is strong
            weights = {
                'base': 0.5,
                'pattern': 0.35,
                'stage': 0.075,
                'industry': 0.075
            }
        else:
            # Use default weights
            weights = self.weights
        
        final = (
            base * weights.get('base', 0.6) +
            pattern_adjusted * weights.get('pattern', 0.25) +
            stage * weights.get('stage', 0.075) +
            industry * weights.get('industry', 0.075)
        )
        
        # Ensure in valid range
        return max(0.01, min(0.99, final))
    
    def _generate_insights(self,
                         startup_data: Dict[str, Any],
                         base_predictions: Dict[str, float],
                         pattern_scores: Dict[str, float],
                         context: PredictionContext) -> Dict[str, List[str]]:
        """Generate actionable insights"""
        insights = {
            'strengths': [],
            'improvements': [],
            'pattern_recommendations': []
        }
        
        # Analyze strengths
        if startup_data.get('revenue_growth_rate', 0) > 150:
            insights['strengths'].append("Strong revenue growth momentum")
        if startup_data.get('net_revenue_retention', 0) > 120:
            insights['strengths'].append("Excellent customer retention and expansion")
        if startup_data.get('burn_multiple', 2) < 1.5:
            insights['strengths'].append("Efficient capital utilization")
        
        # Analyze weaknesses
        if startup_data.get('runway_months', 12) < 12:
            insights['improvements'].append("Extend runway to 18+ months")
        if startup_data.get('customer_acquisition_cost', 100) > startup_data.get('customer_lifetime_value', 0) * 0.33:
            insights['improvements'].append("Improve CAC/LTV ratio to 3:1 or better")
        
        # Pattern-based recommendations
        for pattern, score in pattern_scores.items():
            if score > 0.7:
                if pattern == PatternType.EFFICIENT_GROWTH.value:
                    insights['pattern_recommendations'].append(
                        "Continue efficient growth strategy - ideal for sustainable scaling"
                    )
                elif pattern == PatternType.VC_HYPERGROWTH.value:
                    insights['pattern_recommendations'].append(
                        "Hypergrowth trajectory detected - ensure unit economics remain healthy"
                    )
        
        return insights
    
    def _calculate_confidence(self,
                            base_predictions: Dict[str, float],
                            pattern_scores: Dict[str, float],
                            context: PredictionContext) -> float:
        """Calculate overall prediction confidence"""
        confidences = []
        
        # Model agreement confidence
        if base_predictions:
            std_dev = np.std(list(base_predictions.values()))
            model_confidence = 1 - (std_dev * 2)  # Lower std = higher confidence
            confidences.append(max(0.5, model_confidence))
        
        # Pattern detection confidence
        if pattern_scores:
            pattern_confidence = max(pattern_scores.values())
            confidences.append(pattern_confidence)
        
        # Context confidence
        context_confidence = np.mean(list(context.confidence_scores.values()))
        confidences.append(context_confidence)
        
        return np.mean(confidences) if confidences else 0.5
    
    def _determine_verdict(self, probability: float, confidence: float) -> str:
        """Determine investment verdict"""
        if probability >= 0.7 and confidence >= 0.7:
            return "STRONG PASS"
        elif probability >= 0.6:
            return "PASS"
        elif probability >= 0.5 and confidence >= 0.6:
            return "CONDITIONAL PASS"
        elif probability < 0.3:
            return "STRONG NO"
        else:
            return "NO"
    
    def _assess_risk_level(self,
                         probability: float,
                         confidence: float,
                         context: PredictionContext) -> str:
        """Assess investment risk level"""
        # Base risk on probability
        if probability >= 0.7:
            risk = "LOW"
        elif probability >= 0.5:
            risk = "MEDIUM"
        else:
            risk = "HIGH"
        
        # Adjust for confidence
        if confidence < 0.5 and risk != "HIGH":
            # Low confidence increases risk
            if risk == "LOW":
                risk = "MEDIUM"
            elif risk == "MEDIUM":
                risk = "HIGH"
        
        # Adjust for stage
        if context.funding_stage in [FundingStage.PRE_SEED, FundingStage.SEED]:
            # Early stage is inherently riskier
            if risk == "LOW":
                risk = "MEDIUM"
        
        return risk
    
    def _calculate_pattern_synergy(self, pattern_scores: Dict[str, float]) -> float:
        """Calculate synergy between detected patterns"""
        if len(pattern_scores) < 2:
            return 0.0
        
        # Check for known synergistic combinations
        synergistic_pairs = [
            ('ai_ml_core', 'b2b_saas'),
            ('efficient_growth', 'bootstrap_profitable'),
            ('platform_network', 'exponential_scale'),
            ('product_led', 'freemium_conversion')
        ]
        
        synergy = 0.0
        patterns = list(pattern_scores.keys())
        
        for p1, p2 in synergistic_pairs:
            if p1 in patterns and p2 in patterns:
                # Synergy based on how well both patterns match
                synergy += pattern_scores[p1] * pattern_scores[p2] * 0.2
        
        return min(0.3, synergy)  # Cap at 30% bonus
    
    def _check_pattern_synergy(self, patterns: List[PatternType]) -> float:
        """Check synergy between pattern types"""
        synergy = 0.0
        
        # Define synergistic combinations
        if PatternType.AI_ML_CORE in patterns and PatternType.B2B_SAAS in patterns:
            synergy += 0.1
        if PatternType.EFFICIENT_GROWTH in patterns and PatternType.BOOTSTRAP_PROFITABLE in patterns:
            synergy += 0.1
        if PatternType.PLATFORM_NETWORK in patterns and PatternType.EXPONENTIAL_SCALE in patterns:
            synergy += 0.15
        
        return synergy