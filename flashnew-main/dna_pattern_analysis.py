#!/usr/bin/env python3
"""
DNA Pattern Analysis for Startup Success Prediction
Production-grade implementation with pattern recognition and clustering
"""
import numpy as np
import pandas as pd
import joblib
import logging
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union, Any
from dataclasses import dataclass
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
import json
from datetime import datetime

logger = logging.getLogger(__name__)


@dataclass
class DNAConfig:
    """Configuration for DNA pattern analysis"""
    n_patterns: int = 5
    n_components: int = 10
    pattern_names: List[str] = None
    dna_components: Dict[str, List[str]] = None
    
    def __post_init__(self):
        if self.pattern_names is None:
            self.pattern_names = [
                'Rocket Ship',      # High growth, high burn
                'Slow Burn',        # Steady growth, efficient
                'Blitzscale',       # Extreme growth focus
                'Sustainable',      # Balanced growth and efficiency
                'Technical Moat'    # Deep tech focus
            ]
            
        if self.dna_components is None:
            self.dna_components = {
                'growth_velocity': [
                    'revenue_growth_rate_percent',
                    'user_growth_rate_percent',
                    'customer_count'
                ],
                'efficiency_genes': [
                    'burn_multiple',
                    'ltv_cac_ratio',
                    'gross_margin_percent',
                    'runway_months'
                ],
                'market_dominance': [
                    'customer_concentration_percent',
                    'net_dollar_retention_percent',
                    'market_growth_rate_percent'
                ],
                'founder_dna': [
                    'years_experience_avg',
                    'prior_successful_exits_count',
                    'domain_expertise_years_avg',
                    'team_size_full_time'
                ],
                'product_evolution': [
                    'product_retention_30d',
                    'product_retention_90d',
                    'dau_mau_ratio',
                    'product_stage'
                ],
                'competitive_advantage': [
                    'patent_count',
                    'tech_differentiation_score',
                    'switching_cost_score',
                    'brand_strength_score'
                ]
            }


class StartupDNAAnalyzer:
    """
    Analyzes startup patterns and DNA for success prediction
    Uses clustering and pattern recognition techniques
    """
    
    def __init__(self, config: Optional[DNAConfig] = None):
        self.config = config or DNAConfig()
        self.scaler = StandardScaler()
        self.pca = PCA(n_components=self.config.n_components)
        self.success_patterns = []
        self.failure_patterns = []
        self.pattern_model = None
        self.is_fitted = False
        self.feature_importance = {}
        
    def load(self, model_path: Union[str, Path]) -> bool:
        """
        Load DNA analyzer from disk
        
        Args:
            model_path: Path to model directory
            
        Returns:
            bool: True if successful
        """
        try:
            model_path = Path(model_path)
            
            # Try to load the DNA analyzer model
            dna_model_file = model_path / 'startup_dna_analyzer.pkl'
            if not dna_model_file.exists():
                dna_model_file = model_path / 'dna_pattern_model.pkl'
                
            if dna_model_file.exists():
                loaded_model = joblib.load(dna_model_file)
                
                # Copy attributes from loaded model
                if hasattr(loaded_model, 'scaler'):
                    self.scaler = loaded_model.scaler
                if hasattr(loaded_model, 'pca'):
                    self.pca = loaded_model.pca
                if hasattr(loaded_model, 'success_patterns'):
                    self.success_patterns = loaded_model.success_patterns
                if hasattr(loaded_model, 'failure_patterns'):
                    self.failure_patterns = loaded_model.failure_patterns
                if hasattr(loaded_model, 'pattern_model'):
                    self.pattern_model = loaded_model.pattern_model
                    
                self.is_fitted = True
                logger.info(f"Loaded DNA analyzer from {dna_model_file}")
                return True
            else:
                logger.error(f"DNA model file not found: {dna_model_file}")
                return False
                
        except Exception as e:
            logger.error(f"Error loading DNA analyzer: {str(e)}")
            return False
    
    def analyze_dna(self, features: pd.DataFrame) -> Dict[str, Any]:
        """
        Analyze startup DNA and return patterns
        
        Args:
            features: DataFrame with startup features
            
        Returns:
            Dictionary with DNA analysis results
        """
        if not self.is_fitted:
            logger.warning("DNA analyzer not fitted, returning default analysis")
            return self._get_default_analysis(features)
        
        try:
            # Extract DNA features
            dna_features = self._extract_dna_features(features)
            
            # Transform to DNA space
            dna_scaled = self.scaler.transform(dna_features)
            dna_reduced = self.pca.transform(dna_scaled)
            
            # Find closest patterns
            pattern_analysis = self._analyze_patterns(dna_reduced)
            
            # Get predictions if model available
            if self.pattern_model is not None:
                pattern_features = self._extract_pattern_features(dna_reduced)
                probabilities = self.pattern_model.predict_proba(pattern_features)[:, 1]
            else:
                probabilities = np.array([0.5] * len(features))
            
            # Generate insights
            insights = self._generate_dna_insights(features, pattern_analysis)
            
            return {
                'overall_prediction': int(probabilities[0] >= 0.5),
                'success_probability': float(probabilities[0]),
                'dna_pattern': pattern_analysis['primary_pattern'],
                'pattern_confidence': pattern_analysis['confidence'],
                'success_similarity': pattern_analysis['success_similarity'],
                'failure_similarity': pattern_analysis['failure_similarity'],
                'dna_components': self._get_component_scores(features),
                'insights': insights,
                'recommendations': self._generate_recommendations(pattern_analysis, probabilities[0])
            }
            
        except Exception as e:
            logger.error(f"Error in DNA analysis: {str(e)}")
            return self._get_default_analysis(features)
    
    def _extract_dna_features(self, features: pd.DataFrame) -> pd.DataFrame:
        """Extract DNA-relevant features"""
        dna_features = []
        
        for component, feature_list in self.config.dna_components.items():
            available_features = [f for f in feature_list 
                                if f in features.columns and f != 'product_stage']
            if available_features:
                component_data = features[available_features].fillna(0)
                dna_features.append(component_data)
        
        if dna_features:
            return pd.concat(dna_features, axis=1)
        else:
            # Return numeric features if DNA features not available
            numeric_features = features.select_dtypes(include=[np.number])
            return numeric_features.fillna(0)
    
    def _analyze_patterns(self, dna_reduced: np.ndarray) -> Dict[str, Any]:
        """Analyze DNA patterns and find similarities"""
        analysis = {
            'primary_pattern': 'Unknown',
            'confidence': 0.0,
            'success_similarity': 0.0,
            'failure_similarity': 0.0,
            'pattern_scores': {}
        }
        
        if len(self.success_patterns) == 0:
            return analysis
        
        # Calculate distances to success patterns
        success_distances = []
        for pattern in self.success_patterns:
            dist = np.linalg.norm(dna_reduced[0] - pattern)
            success_distances.append(dist)
        
        # Calculate distances to failure patterns
        failure_distances = []
        if len(self.failure_patterns) > 0:
            for pattern in self.failure_patterns:
                dist = np.linalg.norm(dna_reduced[0] - pattern)
                failure_distances.append(dist)
        
        # Find closest success pattern
        min_success_dist = min(success_distances)
        closest_pattern_idx = success_distances.index(min_success_dist)
        
        # Calculate similarities (inverse of distance)
        max_dist = 10.0  # Normalize distances
        success_similarity = max(0, 1 - (min_success_dist / max_dist))
        failure_similarity = 0.0
        if failure_distances:
            min_failure_dist = min(failure_distances)
            failure_similarity = max(0, 1 - (min_failure_dist / max_dist))
        
        # Determine pattern name
        if closest_pattern_idx < len(self.config.pattern_names):
            pattern_name = self.config.pattern_names[closest_pattern_idx]
        else:
            pattern_name = f'Pattern {closest_pattern_idx + 1}'
        
        analysis.update({
            'primary_pattern': pattern_name,
            'confidence': success_similarity,
            'success_similarity': success_similarity,
            'failure_similarity': failure_similarity,
            'pattern_scores': {
                name: 1 - (dist / max_dist) 
                for name, dist in zip(self.config.pattern_names[:len(success_distances)], 
                                    success_distances)
            }
        })
        
        return analysis
    
    def _extract_pattern_features(self, dna_data: np.ndarray) -> np.ndarray:
        """Extract features based on pattern similarities"""
        features = []
        
        for dna in dna_data:
            feat = []
            
            # Distance to success patterns
            if len(self.success_patterns) > 0:
                success_distances = [np.linalg.norm(dna - pattern) 
                                   for pattern in self.success_patterns]
                feat.extend([
                    np.min(success_distances),
                    np.mean(success_distances),
                    np.std(success_distances),
                    np.argmin(success_distances)
                ])
            else:
                feat.extend([0, 0, 0, 0])
            
            # Distance to failure patterns
            if len(self.failure_patterns) > 0:
                failure_distances = [np.linalg.norm(dna - pattern) 
                                   for pattern in self.failure_patterns]
                feat.extend([
                    np.min(failure_distances),
                    np.mean(failure_distances),
                    np.std(failure_distances),
                    np.argmin(failure_distances)
                ])
            else:
                feat.extend([0, 0, 0, 0])
            
            features.append(feat)
        
        return np.array(features)
    
    def _get_component_scores(self, features: pd.DataFrame) -> Dict[str, float]:
        """Calculate scores for each DNA component"""
        scores = {}
        
        for component, feature_list in self.config.dna_components.items():
            available_features = [f for f in feature_list 
                                if f in features.columns and f != 'product_stage']
            if available_features:
                # Normalize and average component features
                component_values = features[available_features].fillna(0)
                
                # Custom scoring for each component
                if component == 'growth_velocity':
                    score = np.mean([
                        min(component_values.get('revenue_growth_rate_percent', 0) / 300, 1),
                        min(component_values.get('user_growth_rate_percent', 0) / 200, 1)
                    ])
                elif component == 'efficiency_genes':
                    score = np.mean([
                        max(0, 1 - component_values.get('burn_multiple', 5) / 10),
                        min(component_values.get('ltv_cac_ratio', 0) / 5, 1),
                        component_values.get('gross_margin_percent', 0) / 100
                    ])
                elif component == 'market_dominance':
                    score = np.mean([
                        max(0, 1 - component_values.get('customer_concentration_percent', 100) / 100),
                        min(component_values.get('net_dollar_retention_percent', 0) / 150, 1)
                    ])
                elif component == 'founder_dna':
                    score = np.mean([
                        min(component_values.get('years_experience_avg', 0) / 15, 1),
                        min(component_values.get('prior_successful_exits_count', 0) / 2, 1),
                        min(component_values.get('domain_expertise_years_avg', 0) / 10, 1)
                    ])
                else:
                    # Generic scoring for other components
                    score = np.mean(component_values.iloc[0]) / 5  # Assume 5-point scale
                
                scores[component] = float(np.clip(score, 0, 1))
            else:
                scores[component] = 0.5  # Default middle score
        
        return scores
    
    def _generate_dna_insights(self, features: pd.DataFrame, 
                              pattern_analysis: Dict[str, Any]) -> List[str]:
        """Generate insights based on DNA analysis"""
        insights = []
        
        # Pattern-based insights
        pattern = pattern_analysis['primary_pattern']
        confidence = pattern_analysis['confidence']
        
        if confidence > 0.7:
            insights.append(f"Strong {pattern} DNA pattern detected")
        elif confidence > 0.5:
            insights.append(f"Moderate {pattern} characteristics observed")
        
        # Component-based insights
        component_scores = self._get_component_scores(features)
        
        # Find strongest and weakest components
        sorted_components = sorted(component_scores.items(), key=lambda x: x[1], reverse=True)
        strongest = sorted_components[0]
        weakest = sorted_components[-1]
        
        if strongest[1] > 0.7:
            insights.append(f"Exceptional {strongest[0].replace('_', ' ')} (score: {strongest[1]:.2f})")
        
        if weakest[1] < 0.3:
            insights.append(f"Weak {weakest[0].replace('_', ' ')} needs improvement (score: {weakest[1]:.2f})")
        
        # Pattern-specific insights
        pattern_insights = {
            'Rocket Ship': "High-growth trajectory with aggressive scaling",
            'Slow Burn': "Efficient growth with strong fundamentals",
            'Blitzscale': "Extreme growth focus, monitor burn rate carefully",
            'Sustainable': "Balanced approach with long-term viability",
            'Technical Moat': "Strong technical differentiation advantage"
        }
        
        if pattern in pattern_insights:
            insights.append(pattern_insights[pattern])
        
        return insights
    
    def _generate_recommendations(self, pattern_analysis: Dict[str, Any], 
                                  probability: float) -> List[str]:
        """Generate recommendations based on DNA analysis"""
        recommendations = []
        pattern = pattern_analysis['primary_pattern']
        
        # Pattern-specific recommendations
        if pattern == 'Rocket Ship':
            recommendations.append("Maintain growth momentum while improving unit economics")
            recommendations.append("Consider raising larger rounds to fuel expansion")
        elif pattern == 'Slow Burn':
            recommendations.append("Focus on sustainable growth and profitability path")
            recommendations.append("Consider strategic partnerships to accelerate growth")
        elif pattern == 'Blitzscale':
            recommendations.append("Ensure sufficient runway for aggressive expansion")
            recommendations.append("Build operational excellence to handle rapid scaling")
        elif pattern == 'Sustainable':
            recommendations.append("Continue balanced approach to growth and efficiency")
            recommendations.append("Look for opportunities to accelerate without compromising fundamentals")
        elif pattern == 'Technical Moat':
            recommendations.append("Invest in R&D to maintain technical advantage")
            recommendations.append("Build go-to-market capabilities to commercialize innovation")
        
        # Success probability based recommendations
        if probability < 0.5:
            if pattern_analysis['failure_similarity'] > pattern_analysis['success_similarity']:
                recommendations.append("Current trajectory resembles unsuccessful patterns - consider pivot")
            else:
                recommendations.append("Strengthen weak DNA components to improve success likelihood")
        else:
            recommendations.append("Current DNA profile shows positive signals - maintain course")
            
        return recommendations
    
    def _get_default_analysis(self, features: pd.DataFrame) -> Dict[str, Any]:
        """Return default analysis when model not fitted"""
        return {
            'overall_prediction': 0,
            'success_probability': 0.5,
            'dna_pattern': 'Not Analyzed',
            'pattern_confidence': 0.0,
            'success_similarity': 0.5,
            'failure_similarity': 0.5,
            'dna_components': {
                component: 0.5 for component in self.config.dna_components.keys()
            },
            'insights': ["DNA analysis model not available"],
            'recommendations': ["Complete DNA pattern training for detailed analysis"]
        }
    
    def get_pattern_description(self, pattern_name: str) -> Dict[str, Any]:
        """Get detailed description of a DNA pattern"""
        patterns = {
            'Rocket Ship': {
                'description': 'High-growth startups with exponential trajectories',
                'characteristics': [
                    'Revenue growth >200% YoY',
                    'User growth >150% YoY',
                    'High burn rate but improving unit economics',
                    'Strong product-market fit signals'
                ],
                'typical_metrics': {
                    'growth_rate': '>200%',
                    'burn_multiple': '2-5x',
                    'runway': '12-18 months'
                },
                'examples': 'Uber, Airbnb in early stages'
            },
            'Slow Burn': {
                'description': 'Capital-efficient startups with steady growth',
                'characteristics': [
                    'Revenue growth 50-100% YoY',
                    'Positive unit economics',
                    'Extended runway (24+ months)',
                    'Focus on profitability'
                ],
                'typical_metrics': {
                    'growth_rate': '50-100%',
                    'burn_multiple': '<1x',
                    'runway': '24+ months'
                },
                'examples': 'Basecamp, Mailchimp'
            },
            'Blitzscale': {
                'description': 'Winner-take-all market approach with extreme growth',
                'characteristics': [
                    'Revenue growth >300% YoY',
                    'Very high burn rate',
                    'Land grab strategy',
                    'Network effects present'
                ],
                'typical_metrics': {
                    'growth_rate': '>300%',
                    'burn_multiple': '>5x',
                    'runway': '6-12 months'
                },
                'examples': 'Uber, DoorDash in expansion phase'
            },
            'Sustainable': {
                'description': 'Balanced growth with strong fundamentals',
                'characteristics': [
                    'Revenue growth 100-150% YoY',
                    'Improving margins',
                    'Reasonable burn rate',
                    'Clear path to profitability'
                ],
                'typical_metrics': {
                    'growth_rate': '100-150%',
                    'burn_multiple': '1-2x',
                    'runway': '18-24 months'
                },
                'examples': 'Zoom, Slack'
            },
            'Technical Moat': {
                'description': 'Deep tech startups with strong IP',
                'characteristics': [
                    'Multiple patents',
                    'High R&D investment',
                    'Longer development cycles',
                    'High barriers to entry'
                ],
                'typical_metrics': {
                    'patent_count': '>5',
                    'R&D_spend': '>50% of budget',
                    'time_to_market': '2-5 years'
                },
                'examples': 'SpaceX, DeepMind'
            }
        }
        
        return patterns.get(pattern_name, {
            'description': 'Unknown pattern',
            'characteristics': [],
            'typical_metrics': {},
            'examples': 'N/A'
        })