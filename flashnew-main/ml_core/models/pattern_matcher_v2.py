"""
Week 2: Pattern Matcher V2 - Complete Implementation
Matches startups to patterns using CAMP scores and multi-label classification
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional, Any, Set
from dataclasses import dataclass
import logging
from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import cosine_similarity
import json
from pathlib import Path

from .pattern_definitions import (
    StartupPatternLibrary, 
    PatternDefinition, 
    PATTERN_TAGS,
    PatternCategory
)

logger = logging.getLogger(__name__)

@dataclass
class PatternMatch:
    """Represents a match to a startup pattern"""
    pattern_name: str
    confidence: float
    match_type: str  # 'primary', 'secondary', 'potential'
    
    # Detailed scoring breakdown
    camp_match_score: float
    feature_match_score: float
    statistical_match_score: float
    
    # Match details
    matching_features: List[str]
    missing_features: List[str]
    camp_distances: Dict[str, float]
    
    # Pattern info
    pattern_category: str
    expected_success_rate: float
    similar_companies: List[str]
    
    # Recommendations
    gap_analysis: List[str]
    improvement_suggestions: List[str]

@dataclass 
class PatternAnalysis:
    """Complete pattern analysis for a startup"""
    # Primary pattern (best match)
    primary_pattern: PatternMatch
    
    # Secondary patterns (other good matches)
    secondary_patterns: List[PatternMatch]
    
    # Pattern mixture (probability distribution)
    pattern_mixture: Dict[str, float]
    
    # Multi-label tags
    tags: Set[str]
    tag_confidence: Dict[str, float]
    
    # Evolution analysis
    current_stage: str
    next_likely_patterns: List[Tuple[str, float]]  # (pattern, probability)
    
    # Insights
    pattern_stability: float  # How clearly it matches primary pattern
    pattern_uniqueness: float  # How different from other patterns
    
    # Success prediction adjustment
    pattern_success_modifier: float  # Multiply base success probability

class PatternMatcherV2:
    """Advanced pattern matching system integrated with CAMP framework"""
    
    def __init__(self, pattern_library: Optional[StartupPatternLibrary] = None):
        self.pattern_library = pattern_library or StartupPatternLibrary()
        self.pattern_profiles = {}  # Statistical profiles from training data
        self.tag_models = {}  # Models for multi-label tag prediction
        self.evolution_matrix = {}  # Pattern transition probabilities
        self.is_trained = False
        
        # Load discovered patterns if available
        self.discovered_patterns = self._load_discovered_patterns()
        
    def _load_discovered_patterns(self) -> Dict[str, Any]:
        """Load patterns discovered from data analysis"""
        patterns_path = Path('ml_core/discovered_patterns.json')
        if patterns_path.exists():
            with open(patterns_path, 'r') as f:
                data = json.load(f)
                return data.get('patterns', {})
        return {}
    
    def train(self, X: pd.DataFrame, y: np.ndarray, camp_scores: pd.DataFrame):
        """Train pattern matcher on historical data"""
        logger.info(f"Training pattern matcher on {len(X)} samples")
        
        # Build statistical profiles for each pattern
        self._build_pattern_profiles(X, y, camp_scores)
        
        # Train tag prediction models
        self._train_tag_models(X, y, camp_scores)
        
        # Learn pattern evolution from data
        self._learn_pattern_evolution(X, camp_scores)
        
        self.is_trained = True
        logger.info("Pattern matcher training complete")
    
    def match_patterns(self, startup_data: pd.DataFrame, 
                      camp_scores: Dict[str, float],
                      top_k: int = 5) -> PatternAnalysis:
        """Match a startup to patterns"""
        
        # Calculate match scores for all patterns
        all_matches = []
        
        for pattern in self.pattern_library.patterns:
            match = self._evaluate_pattern_match(
                startup_data, camp_scores, pattern
            )
            if match.confidence > 0.3:  # Minimum threshold
                all_matches.append(match)
        
        # Sort by confidence
        all_matches.sort(key=lambda x: x.confidence, reverse=True)
        
        # Identify primary pattern
        primary_pattern = all_matches[0] if all_matches else self._get_default_match()
        
        # Get secondary patterns
        secondary_patterns = all_matches[1:top_k]
        
        # Calculate pattern mixture (probability distribution)
        pattern_mixture = self._calculate_pattern_mixture(all_matches)
        
        # Predict multi-label tags
        tags, tag_confidence = self._predict_tags(startup_data, camp_scores)
        
        # Analyze evolution possibilities
        current_stage = self._determine_current_stage(startup_data)
        next_patterns = self._predict_next_patterns(
            primary_pattern.pattern_name, 
            current_stage
        )
        
        # Calculate pattern stability and uniqueness
        pattern_stability = self._calculate_stability(all_matches)
        pattern_uniqueness = self._calculate_uniqueness(
            primary_pattern, all_matches
        )
        
        # Success modifier based on pattern fit
        success_modifier = self._calculate_success_modifier(
            primary_pattern, pattern_stability
        )
        
        return PatternAnalysis(
            primary_pattern=primary_pattern,
            secondary_patterns=secondary_patterns,
            pattern_mixture=pattern_mixture,
            tags=tags,
            tag_confidence=tag_confidence,
            current_stage=current_stage,
            next_likely_patterns=next_patterns,
            pattern_stability=pattern_stability,
            pattern_uniqueness=pattern_uniqueness,
            pattern_success_modifier=success_modifier
        )
    
    def _evaluate_pattern_match(self, startup_data: pd.DataFrame,
                               camp_scores: Dict[str, float],
                               pattern: PatternDefinition) -> PatternMatch:
        """Evaluate how well a startup matches a specific pattern"""
        
        # 1. CAMP-based matching (40% weight)
        camp_match_score, camp_distances = self._calculate_camp_match(
            camp_scores, pattern.camp_thresholds
        )
        
        # 2. Feature-based matching (40% weight)
        feature_match_score, matching_features, missing_features = \
            self._calculate_feature_match(startup_data, pattern.feature_rules)
        
        # 3. Statistical matching if trained (20% weight)
        statistical_match_score = 0.5  # Default
        if self.is_trained and pattern.name in self.pattern_profiles:
            statistical_match_score = self._calculate_statistical_match(
                startup_data, camp_scores, pattern.name
            )
        
        # Weighted combination
        weights = [0.4, 0.4, 0.2] if self.is_trained else [0.5, 0.5, 0.0]
        confidence = (
            weights[0] * camp_match_score +
            weights[1] * feature_match_score +
            weights[2] * statistical_match_score
        )
        
        # Determine match type
        if confidence > 0.75:
            match_type = 'primary'
        elif confidence > 0.5:
            match_type = 'secondary'
        else:
            match_type = 'potential'
        
        # Gap analysis
        gap_analysis = self._analyze_gaps(
            camp_scores, pattern.camp_thresholds,
            missing_features, pattern.key_metrics
        )
        
        # Improvement suggestions
        improvement_suggestions = self._generate_improvements(
            gap_analysis, pattern.success_factors
        )
        
        return PatternMatch(
            pattern_name=pattern.name,
            confidence=confidence,
            match_type=match_type,
            camp_match_score=camp_match_score,
            feature_match_score=feature_match_score,
            statistical_match_score=statistical_match_score,
            matching_features=matching_features,
            missing_features=missing_features,
            camp_distances=camp_distances,
            pattern_category=pattern.category.value,
            expected_success_rate=np.mean(pattern.success_rate_range),
            similar_companies=pattern.example_companies[:3],
            gap_analysis=gap_analysis,
            improvement_suggestions=improvement_suggestions
        )
    
    def _calculate_camp_match(self, camp_scores: Dict[str, float],
                             thresholds: Dict[str, tuple]) -> Tuple[float, Dict[str, float]]:
        """Calculate CAMP-based pattern match score"""
        match_scores = []
        distances = {}
        
        for dimension in ['capital', 'advantage', 'market', 'people']:
            score = camp_scores.get(f'{dimension}_score', 50)
            min_val, max_val = thresholds.get(dimension, (0, 100))
            
            # Calculate match score for this dimension
            if min_val <= score <= max_val:
                # Perfect match within range
                dim_score = 1.0
                distance = 0
            else:
                # Calculate distance from range
                if score < min_val:
                    distance = min_val - score
                else:
                    distance = score - max_val
                
                # Convert distance to score (exponential decay)
                dim_score = np.exp(-distance / 20)  # 20 point scale
            
            match_scores.append(dim_score)
            distances[dimension] = distance
        
        # Overall match is average of dimensions
        overall_match = np.mean(match_scores)
        
        return overall_match, distances
    
    def _calculate_feature_match(self, startup_data: pd.DataFrame,
                                feature_rules: Dict[str, callable]) -> Tuple[float, List[str], List[str]]:
        """Calculate feature-based pattern match score"""
        matching_features = []
        missing_features = []
        
        for feature_name, rule_func in feature_rules.items():
            if feature_name in startup_data.columns:
                value = startup_data[feature_name].iloc[0]
                try:
                    if rule_func(value):
                        matching_features.append(feature_name)
                    else:
                        missing_features.append(feature_name)
                except:
                    missing_features.append(feature_name)
            else:
                # Feature not available in data
                missing_features.append(feature_name)
        
        # Calculate match score
        total_rules = len(feature_rules)
        if total_rules > 0:
            match_score = len(matching_features) / total_rules
        else:
            match_score = 0.5  # No rules defined
        
        return match_score, matching_features, missing_features
    
    def _calculate_statistical_match(self, startup_data: pd.DataFrame,
                                   camp_scores: Dict[str, float],
                                   pattern_name: str) -> float:
        """Calculate statistical similarity to pattern profile"""
        if pattern_name not in self.pattern_profiles:
            return 0.5
        
        profile = self.pattern_profiles[pattern_name]
        
        # Create feature vector combining CAMP scores and key features
        feature_vector = []
        
        # Add CAMP scores
        for dim in ['capital', 'advantage', 'market', 'people']:
            feature_vector.append(camp_scores.get(f'{dim}_score', 50))
        
        # Add key numerical features
        key_features = [
            'revenue_growth_rate_percent',
            'burn_multiple',
            'net_dollar_retention_percent',
            'product_retention_30d',
            'team_size_full_time'
        ]
        
        for feature in key_features:
            if feature in startup_data.columns:
                feature_vector.append(startup_data[feature].iloc[0])
            else:
                feature_vector.append(profile.get(f'{feature}_mean', 0))
        
        # Convert to numpy array
        feature_vector = np.array(feature_vector).reshape(1, -1)
        profile_vector = profile['mean_vector'].reshape(1, -1)
        
        # Calculate cosine similarity
        similarity = cosine_similarity(feature_vector, profile_vector)[0, 0]
        
        # Convert to 0-1 range
        return (similarity + 1) / 2
    
    def _calculate_pattern_mixture(self, matches: List[PatternMatch]) -> Dict[str, float]:
        """Calculate probability distribution over patterns"""
        if not matches:
            return {}
        
        # Get all confidence scores
        confidences = [m.confidence for m in matches]
        
        # Convert to probabilities using softmax
        exp_scores = np.exp(confidences)
        probabilities = exp_scores / exp_scores.sum()
        
        # Create mixture dictionary
        mixture = {}
        for match, prob in zip(matches, probabilities):
            if prob > 0.01:  # Only include significant probabilities
                mixture[match.pattern_name] = float(prob)
        
        return mixture
    
    def _predict_tags(self, startup_data: pd.DataFrame,
                     camp_scores: Dict[str, float]) -> Tuple[Set[str], Dict[str, float]]:
        """Predict multi-label tags for startup"""
        tags = set()
        tag_confidence = {}
        
        # Rule-based tag assignment
        # Growth tags
        if 'revenue_growth_rate_percent' in startup_data.columns:
            growth = startup_data['revenue_growth_rate_percent'].iloc[0]
            if growth > 200:
                tags.add('hypergrowth')
                tag_confidence['hypergrowth'] = 0.9
            elif growth > 100:
                tags.add('steady_growth')
                tag_confidence['steady_growth'] = 0.8
            elif growth < 20:
                tags.add('stagnant')
                tag_confidence['stagnant'] = 0.7
        
        # Capital efficiency tags
        if 'burn_multiple' in startup_data.columns:
            burn = startup_data['burn_multiple'].iloc[0]
            if burn < 1:
                tags.add('profitable')
                tag_confidence['profitable'] = 0.9
            elif burn < 2:
                tags.add('capital_efficient')
                tag_confidence['capital_efficient'] = 0.8
            elif burn > 5:
                tags.add('high_burn')
                tag_confidence['high_burn'] = 0.8
        
        # Technology tags
        if 'ai_team_percent' in startup_data.columns:
            if startup_data['ai_team_percent'].iloc[0] > 20:
                tags.add('ai_enabled')
                tag_confidence['ai_enabled'] = 0.9
        
        # Business model tags
        if 'business_model' in startup_data.columns:
            model = startup_data['business_model'].iloc[0]
            if model in ['subscription', 'saas']:
                tags.add('subscription')
                tag_confidence['subscription'] = 0.95
            elif model == 'marketplace':
                tags.add('marketplace')
                tag_confidence['marketplace'] = 0.95
        
        # Risk tags based on CAMP scores
        avg_camp = np.mean(list(camp_scores.values()))
        if avg_camp < 40:
            tags.add('high_risk')
            tag_confidence['high_risk'] = 0.8
        elif avg_camp > 70:
            tags.add('low_risk')
            tag_confidence['low_risk'] = 0.8
        else:
            tags.add('moderate_risk')
            tag_confidence['moderate_risk'] = 0.7
        
        return tags, tag_confidence
    
    def _determine_current_stage(self, startup_data: pd.DataFrame) -> str:
        """Determine current evolution stage"""
        # Use funding stage as primary indicator
        if 'funding_stage' in startup_data.columns:
            funding_stage = startup_data['funding_stage'].iloc[0]
            
            stage_mapping = {
                'pre_seed': 'early',
                'seed': 'emerging', 
                'series_a': 'growing',
                'series_b': 'scaling',
                'series_c': 'maturing',
                'growth': 'mature'
            }
            
            return stage_mapping.get(funding_stage, 'unknown')
        
        # Fallback to revenue-based staging
        if 'annual_revenue_run_rate' in startup_data.columns:
            arr = startup_data['annual_revenue_run_rate'].iloc[0]
            if arr < 1000000:
                return 'early'
            elif arr < 10000000:
                return 'emerging'
            elif arr < 50000000:
                return 'growing'
            else:
                return 'scaling'
        
        return 'unknown'
    
    def _predict_next_patterns(self, current_pattern: str,
                              current_stage: str) -> List[Tuple[str, float]]:
        """Predict likely next patterns based on evolution matrix"""
        next_patterns = []
        
        # Get evolution paths from pattern definition
        pattern_def = self.pattern_library.get_pattern(current_pattern)
        if pattern_def:
            for next_pattern in pattern_def.evolution_paths:
                # Simple probability based on stage progression
                if current_stage in ['early', 'emerging']:
                    probability = 0.7
                elif current_stage in ['growing', 'scaling']:
                    probability = 0.5
                else:
                    probability = 0.3
                
                next_patterns.append((next_pattern, probability))
        
        # Add stage-based transitions
        if current_stage == 'early' and 'STRUGGLING' not in current_pattern:
            next_patterns.append(('EFFICIENT_B2B_SAAS', 0.3))
            next_patterns.append(('STRUGGLING_SEEKING_PMF', 0.2))
        
        # Sort by probability
        next_patterns.sort(key=lambda x: x[1], reverse=True)
        
        return next_patterns[:3]
    
    def _calculate_stability(self, matches: List[PatternMatch]) -> float:
        """Calculate how clearly the startup matches its primary pattern"""
        if len(matches) < 2:
            return 1.0
        
        # Stability is high when primary pattern has much higher confidence
        primary_conf = matches[0].confidence
        secondary_conf = matches[1].confidence if len(matches) > 1 else 0
        
        # Calculate relative difference
        if secondary_conf > 0:
            stability = (primary_conf - secondary_conf) / primary_conf
        else:
            stability = 1.0
        
        return max(0, min(1, stability))
    
    def _calculate_uniqueness(self, primary: PatternMatch,
                            all_matches: List[PatternMatch]) -> float:
        """Calculate how unique this pattern assignment is"""
        # High uniqueness when few other patterns match well
        matching_patterns = sum(1 for m in all_matches if m.confidence > 0.5)
        
        if matching_patterns <= 1:
            uniqueness = 1.0
        elif matching_patterns <= 3:
            uniqueness = 0.7
        else:
            uniqueness = 0.4
        
        return uniqueness
    
    def _calculate_success_modifier(self, primary: PatternMatch,
                                   stability: float) -> float:
        """Calculate modifier for success probability based on pattern fit"""
        # Base modifier from pattern success rate
        base_modifier = primary.expected_success_rate / 0.5  # Relative to 50% baseline
        
        # Adjust based on match quality
        quality_adjustment = primary.confidence * stability
        
        # Final modifier (bounded between 0.5 and 2.0)
        modifier = base_modifier * (0.5 + quality_adjustment)
        
        return max(0.5, min(2.0, modifier))
    
    def _analyze_gaps(self, camp_scores: Dict[str, float],
                     camp_thresholds: Dict[str, tuple],
                     missing_features: List[str],
                     key_metrics: Dict[str, str]) -> List[str]:
        """Analyze gaps between startup and pattern ideal"""
        gaps = []
        
        # CAMP gaps
        for dimension, (min_val, max_val) in camp_thresholds.items():
            score = camp_scores.get(f'{dimension}_score', 50)
            if score < min_val:
                gaps.append(f"{dimension.capitalize()} score {score:.0f} below pattern minimum {min_val}")
            elif score > max_val:
                gaps.append(f"{dimension.capitalize()} score {score:.0f} above pattern maximum {max_val}")
        
        # Feature gaps
        for feature in missing_features[:3]:  # Top 3 missing features
            feature_readable = feature.replace('_', ' ').title()
            gaps.append(f"{feature_readable} not meeting pattern criteria")
        
        return gaps
    
    def _generate_improvements(self, gaps: List[str],
                             success_factors: List[str]) -> List[str]:
        """Generate specific improvement suggestions"""
        improvements = []
        
        # Address gaps
        for gap in gaps[:3]:
            if 'Capital score' in gap and 'below' in gap:
                improvements.append("Improve capital efficiency: reduce burn or increase revenue")
            elif 'Market score' in gap and 'below' in gap:
                improvements.append("Strengthen market position: increase market share or improve retention")
            elif 'People score' in gap and 'below' in gap:
                improvements.append("Strengthen team: hire senior talent or add advisors")
            elif 'burn' in gap.lower():
                improvements.append("Optimize burn rate to extend runway")
        
        # Add pattern-specific success factors
        for factor in success_factors[:2]:
            improvements.append(f"Focus on: {factor}")
        
        return improvements
    
    def _build_pattern_profiles(self, X: pd.DataFrame, y: np.ndarray,
                               camp_scores: pd.DataFrame):
        """Build statistical profiles for each pattern from training data"""
        # This would be called during training to learn pattern characteristics
        logger.info("Building pattern profiles from training data...")
        
        # Assignment logic would go here
        # For now, using simplified version
        self.pattern_profiles = {}
    
    def _train_tag_models(self, X: pd.DataFrame, y: np.ndarray,
                         camp_scores: pd.DataFrame):
        """Train models for multi-label tag prediction"""
        # Simplified version - in production would train actual ML models
        logger.info("Training tag prediction models...")
        self.tag_models = {}
    
    def _learn_pattern_evolution(self, X: pd.DataFrame,
                                camp_scores: pd.DataFrame):
        """Learn pattern evolution from historical data"""
        # Simplified version - would track actual transitions
        logger.info("Learning pattern evolution...")
        self.evolution_matrix = {}
    
    def _get_default_match(self) -> PatternMatch:
        """Return default match when no patterns match well"""
        return PatternMatch(
            pattern_name="UNKNOWN",
            confidence=0.0,
            match_type='potential',
            camp_match_score=0.0,
            feature_match_score=0.0,
            statistical_match_score=0.0,
            matching_features=[],
            missing_features=[],
            camp_distances={},
            pattern_category="unknown",
            expected_success_rate=0.5,
            similar_companies=[],
            gap_analysis=["Unable to match to any defined pattern"],
            improvement_suggestions=["Focus on improving core metrics"]
        )

# Convenience function for pattern analysis
def analyze_startup_patterns(startup_data: pd.DataFrame,
                           camp_scores: Dict[str, float]) -> Dict[str, Any]:
    """Convenience function to analyze startup patterns"""
    matcher = PatternMatcherV2()
    analysis = matcher.match_patterns(startup_data, camp_scores)
    
    return {
        'primary_pattern': {
            'name': analysis.primary_pattern.pattern_name,
            'confidence': analysis.primary_pattern.confidence,
            'category': analysis.primary_pattern.pattern_category,
            'expected_success': analysis.primary_pattern.expected_success_rate,
            'similar_companies': analysis.primary_pattern.similar_companies
        },
        'secondary_patterns': [
            {
                'name': p.pattern_name,
                'confidence': p.confidence
            }
            for p in analysis.secondary_patterns[:3]
        ],
        'tags': list(analysis.tags),
        'evolution': {
            'current_stage': analysis.current_stage,
            'next_patterns': analysis.next_likely_patterns
        },
        'pattern_quality': {
            'stability': analysis.pattern_stability,
            'uniqueness': analysis.pattern_uniqueness
        },
        'success_modifier': analysis.pattern_success_modifier
    }