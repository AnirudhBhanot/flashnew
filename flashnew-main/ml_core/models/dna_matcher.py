"""
DNA Pattern Matching System
Matches startups to DNA patterns using multi-factor analysis
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass
import logging
from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import cosine_similarity
import xgboost as xgb

from .startup_dna_library import StartupDNALibrary, DNAPattern

logger = logging.getLogger(__name__)

@dataclass
class DNAMatch:
    """Represents a match to a DNA pattern"""
    pattern_name: str
    overall_score: float
    indicator_score: float
    statistical_score: float
    ml_score: float
    confidence: float
    match_details: Dict[str, Any]
    evolution_stage: str
    recommendations: List[str]

class DNAMatcher:
    """Advanced DNA pattern matching system"""
    
    def __init__(self, dna_library: Optional[StartupDNALibrary] = None):
        self.dna_library = dna_library or StartupDNALibrary()
        self.scaler = StandardScaler()
        self.pattern_models = {}  # ML models for each pattern
        self.pattern_profiles = {}  # Statistical profiles
        self.is_trained = False
        
    def train(self, X: pd.DataFrame, y: np.ndarray, 
              pattern_assignments: Optional[Dict[int, str]] = None):
        """Train the DNA matcher on historical data"""
        logger.info(f"Training DNA matcher on {len(X)} samples")
        
        # Fit scaler
        self.scaler.fit(X)
        X_scaled = self.scaler.transform(X)
        
        if pattern_assignments is None:
            # Auto-assign patterns based on characteristics
            pattern_assignments = self._auto_assign_patterns(X, y)
        
        # Build statistical profiles for each pattern
        self._build_pattern_profiles(X, y, pattern_assignments)
        
        # Train ML models for each pattern
        self._train_pattern_models(X, y, pattern_assignments)
        
        self.is_trained = True
        logger.info("DNA matcher training complete")
        
    def match_dna(self, startup_data: pd.DataFrame, 
                  top_k: int = 3) -> List[DNAMatch]:
        """Match a startup to DNA patterns"""
        
        # Ensure single row
        if len(startup_data) > 1:
            startup_data = startup_data.iloc[:1]
        
        # Calculate scores for each pattern
        matches = []
        
        for pattern in self.dna_library.patterns:
            # 1. Indicator-based matching (rule-based)
            indicator_score = self._calculate_indicator_score(
                startup_data, pattern
            )
            
            # 2. Statistical similarity (if trained)
            statistical_score = 0.5  # Default
            if self.is_trained and pattern.name in self.pattern_profiles:
                statistical_score = self._calculate_statistical_score(
                    startup_data, pattern.name
                )
            
            # 3. ML-based score (if trained)
            ml_score = 0.5  # Default
            if self.is_trained and pattern.name in self.pattern_models:
                ml_score = self._calculate_ml_score(
                    startup_data, pattern.name
                )
            
            # Weighted combination
            weights = {
                'indicator': 0.4,
                'statistical': 0.3,
                'ml': 0.3
            }
            
            if not self.is_trained:
                # Use only indicators if not trained
                weights = {'indicator': 1.0, 'statistical': 0, 'ml': 0}
            
            overall_score = (
                weights['indicator'] * indicator_score +
                weights['statistical'] * statistical_score +
                weights['ml'] * ml_score
            )
            
            # Calculate confidence based on score components
            confidence = self._calculate_confidence(
                indicator_score, statistical_score, ml_score
            )
            
            # Get match details
            match_details = self._get_match_details(
                startup_data, pattern, indicator_score
            )
            
            # Determine evolution stage
            evolution_stage = self._determine_evolution_stage(
                startup_data, pattern
            )
            
            # Generate recommendations
            recommendations = self._generate_recommendations(
                startup_data, pattern, overall_score
            )
            
            matches.append(DNAMatch(
                pattern_name=pattern.name,
                overall_score=overall_score,
                indicator_score=indicator_score,
                statistical_score=statistical_score,
                ml_score=ml_score,
                confidence=confidence,
                match_details=match_details,
                evolution_stage=evolution_stage,
                recommendations=recommendations
            ))
        
        # Sort by overall score
        matches.sort(key=lambda x: x.overall_score, reverse=True)
        
        return matches[:top_k]
    
    def _calculate_indicator_score(self, data: pd.DataFrame, 
                                  pattern: DNAPattern) -> float:
        """Calculate rule-based indicator matching score"""
        scores = []
        details = {}
        
        for indicator_name, indicator_func in pattern.indicators.items():
            if callable(indicator_func):
                # It's a lambda function
                try:
                    # Map indicator names to dataframe columns
                    col_name = self._map_indicator_to_column(indicator_name)
                    if col_name in data.columns:
                        value = data[col_name].iloc[0]
                        matches = indicator_func(value)
                        scores.append(1.0 if matches else 0.0)
                        details[indicator_name] = {
                            'value': value,
                            'matches': matches
                        }
                except Exception as e:
                    logger.debug(f"Error evaluating {indicator_name}: {e}")
                    scores.append(0.5)  # Neutral score for errors
            else:
                # It's a string condition like 'high' or 'aggressive'
                # These need domain-specific evaluation
                scores.append(0.7)  # Default positive score
        
        return np.mean(scores) if scores else 0.5
    
    def _map_indicator_to_column(self, indicator_name: str) -> str:
        """Map indicator names to dataframe column names"""
        # Handle common mappings
        mappings = {
            'revenue_growth_rate': 'revenue_growth_rate_percent',
            'burn_multiple': 'burn_multiple',
            'user_growth_rate': 'user_growth_rate_percent',
            'net_retention': 'net_dollar_retention_percent',
            'viral_coefficient': 'k_factor',
            'r_and_d_intensity': 'r_and_d_spend_percent',
            'gross_margin': 'gross_margin_percent',
            'ltv_cac': 'ltv_cac_ratio',
            'dau_mau_ratio': 'dau_mau_ratio',
            'viral_coefficient': 'viral_coefficient',
            'organic_acquisition': 'organic_acquisition_percent',
            'time_to_value': 'time_to_value_minutes'
        }
        
        return mappings.get(indicator_name, indicator_name)
    
    def _calculate_statistical_score(self, data: pd.DataFrame, 
                                    pattern_name: str) -> float:
        """Calculate statistical similarity to pattern profile"""
        if pattern_name not in self.pattern_profiles:
            return 0.5
        
        profile = self.pattern_profiles[pattern_name]
        
        # Scale the data
        data_scaled = self.scaler.transform(data)
        
        # Calculate cosine similarity
        similarity = cosine_similarity(
            data_scaled.reshape(1, -1),
            profile['mean_features'].reshape(1, -1)
        )[0, 0]
        
        # Convert to 0-1 range
        return (similarity + 1) / 2
    
    def _calculate_ml_score(self, data: pd.DataFrame, 
                           pattern_name: str) -> float:
        """Calculate ML model probability for pattern"""
        if pattern_name not in self.pattern_models:
            return 0.5
        
        model = self.pattern_models[pattern_name]
        
        try:
            # Get probability of matching this pattern
            prob = model.predict_proba(data)[0, 1]
            return float(prob)
        except Exception as e:
            logger.debug(f"ML prediction error for {pattern_name}: {e}")
            return 0.5
    
    def _calculate_confidence(self, indicator: float, 
                             statistical: float, ml: float) -> float:
        """Calculate confidence based on agreement between methods"""
        scores = [indicator, statistical, ml]
        
        # Remove default values (0.5) if not trained
        if not self.is_trained:
            scores = [indicator]
        
        # Calculate standard deviation as measure of disagreement
        if len(scores) > 1:
            std = np.std(scores)
            # Convert to confidence (low std = high confidence)
            confidence = 1 - (std * 2)  # Scale std to confidence
            return max(0.1, min(0.95, confidence))
        else:
            # Single score - moderate confidence
            return 0.7
    
    def _get_match_details(self, data: pd.DataFrame, pattern: DNAPattern,
                          indicator_score: float) -> Dict[str, Any]:
        """Get detailed matching information"""
        details = {
            'pattern_description': pattern.description,
            'typical_examples': pattern.examples[:3],
            'pattern_success_rate': pattern.success_rate,
            'indicator_matches': {},
            'strengths': [],
            'gaps': []
        }
        
        # Analyze each indicator
        for indicator_name, indicator_func in pattern.indicators.items():
            if callable(indicator_func):
                try:
                    col_name = self._map_indicator_to_column(indicator_name)
                    if col_name in data.columns:
                        value = data[col_name].iloc[0]
                        matches = indicator_func(value)
                        
                        details['indicator_matches'][indicator_name] = {
                            'current_value': value,
                            'matches_pattern': matches
                        }
                        
                        if matches:
                            details['strengths'].append(indicator_name)
                        else:
                            details['gaps'].append(indicator_name)
                except:
                    pass
        
        return details
    
    def _determine_evolution_stage(self, data: pd.DataFrame, 
                                  pattern: DNAPattern) -> str:
        """Determine where in the pattern evolution the startup is"""
        # Simple stage determination based on funding stage
        funding_stage = data.get('funding_stage', pd.Series(['unknown'])).iloc[0]
        
        stage_mapping = {
            'pre_seed': 'early',
            'seed': 'emerging',
            'series_a': 'growing',
            'series_b': 'scaling',
            'series_c': 'maturing',
            'growth': 'mature'
        }
        
        base_stage = stage_mapping.get(funding_stage, 'unknown')
        
        # Adjust based on metrics
        if 'revenue_growth_rate_percent' in data.columns:
            growth = data['revenue_growth_rate_percent'].iloc[0]
            if growth > 200 and base_stage in ['emerging', 'growing']:
                return 'hypergrowth'
            elif growth < 50 and base_stage in ['scaling', 'maturing']:
                return 'optimizing'
        
        return base_stage
    
    def _generate_recommendations(self, data: pd.DataFrame, 
                                 pattern: DNAPattern, score: float) -> List[str]:
        """Generate pattern-specific recommendations"""
        recommendations = []
        
        if score > 0.8:
            # Strong match - focus on optimization
            recommendations.append(
                f"Strong {pattern.name} DNA match. Focus on perfecting the model:"
            )
            recommendations.extend([
                f"- Benchmark against: {', '.join(pattern.examples[:2])}",
                f"- Key success factors: {', '.join(pattern.success_factors[:3])}",
                f"- Evolution path: {' → '.join(pattern.evolution_paths[:2])}"
            ])
        elif score > 0.6:
            # Moderate match - address gaps
            recommendations.append(
                f"Moderate {pattern.name} DNA match. Address key gaps:"
            )
            
            # Find specific gaps
            gaps = []
            for risk in pattern.key_risks[:3]:
                recommendations.append(f"- Monitor: {risk}")
        else:
            # Weak match - consider if this is the right pattern
            recommendations.append(
                f"Weak {pattern.name} match. Consider pivoting strategy or strengthening fundamentals."
            )
        
        return recommendations
    
    def _auto_assign_patterns(self, X: pd.DataFrame, y: np.ndarray) -> Dict[int, str]:
        """Automatically assign patterns to training data"""
        assignments = {}
        
        for i in range(len(X)):
            # Get top match for this startup
            startup_data = X.iloc[i:i+1]
            matches = self.match_dna(startup_data, top_k=1)
            
            if matches:
                assignments[i] = matches[0].pattern_name
            else:
                assignments[i] = 'UNKNOWN'
        
        return assignments
    
    def _build_pattern_profiles(self, X: pd.DataFrame, y: np.ndarray,
                               assignments: Dict[int, str]):
        """Build statistical profiles for each pattern"""
        X_scaled = self.scaler.transform(X)
        
        for pattern_name in set(assignments.values()):
            if pattern_name == 'UNKNOWN':
                continue
                
            # Get indices for this pattern
            indices = [i for i, p in assignments.items() if p == pattern_name]
            
            if len(indices) < 10:  # Need minimum samples
                continue
            
            # Calculate profile
            pattern_data = X_scaled[indices]
            pattern_success = y[indices]
            
            self.pattern_profiles[pattern_name] = {
                'mean_features': pattern_data.mean(axis=0),
                'std_features': pattern_data.std(axis=0),
                'success_rate': pattern_success.mean(),
                'sample_count': len(indices),
                'success_percentiles': {
                    'p25': np.percentile(pattern_data[pattern_success == 1], 25, axis=0),
                    'p50': np.percentile(pattern_data[pattern_success == 1], 50, axis=0),
                    'p75': np.percentile(pattern_data[pattern_success == 1], 75, axis=0)
                }
            }
    
    def _train_pattern_models(self, X: pd.DataFrame, y: np.ndarray,
                             assignments: Dict[int, str]):
        """Train ML models for each pattern"""
        for pattern_name in set(assignments.values()):
            if pattern_name == 'UNKNOWN':
                continue
            
            # Get indices for this pattern
            indices = [i for i, p in assignments.items() if p == pattern_name]
            
            if len(indices) < 50:  # Need minimum samples for ML
                continue
            
            # Train a model to predict if a startup matches this pattern
            # Create binary labels: 1 if matches this pattern, 0 otherwise
            pattern_labels = np.zeros(len(X))
            pattern_labels[indices] = 1
            
            # Train XGBoost model
            model = xgb.XGBClassifier(
                n_estimators=100,
                max_depth=4,
                learning_rate=0.1,
                random_state=42,
                use_label_encoder=False,
                eval_metric='logloss'
            )
            
            model.fit(X, pattern_labels)
            self.pattern_models[pattern_name] = model
            
            logger.info(f"Trained model for {pattern_name} pattern ({len(indices)} samples)")
    
    def get_pattern_distribution(self, X: pd.DataFrame) -> Dict[str, int]:
        """Get distribution of patterns in a dataset"""
        distribution = {}
        
        for i in range(len(X)):
            matches = self.match_dna(X.iloc[i:i+1], top_k=1)
            if matches:
                pattern = matches[0].pattern_name
                distribution[pattern] = distribution.get(pattern, 0) + 1
        
        return distribution
    
    def explain_dna_match(self, match: DNAMatch) -> str:
        """Generate human-readable explanation of DNA match"""
        pattern = self.dna_library.get_pattern(match.pattern_name)
        
        explanation = f"""
DNA Pattern: {match.pattern_name}
Match Confidence: {match.confidence:.1%}
Overall Score: {match.overall_score:.1%}

Description: {pattern.description}

Similar Companies: {', '.join(pattern.examples[:3])}

Pattern Success Rate: {pattern.success_rate:.1%}

Your Strengths:
{chr(10).join(f"• {s}" for s in match.match_details.get('strengths', [])[:3])}

Areas to Improve:
{chr(10).join(f"• {g}" for g in match.match_details.get('gaps', [])[:3])}

Evolution Stage: {match.evolution_stage}

Recommendations:
{chr(10).join(match.recommendations[:3])}

Potential Evolution Paths:
{' → '.join(pattern.evolution_paths[:2])}
"""
        return explanation.strip()