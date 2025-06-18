"""
DNA Pattern Analyzer - Production Implementation
Combines pre-defined patterns with data-driven discovery
"""

import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
import xgboost as xgb
from catboost import CatBoostClassifier
from typing import Dict, Any, Optional, List, Tuple
import logging
import joblib
from pathlib import Path

from ..interfaces.base_models import BaseMLModel
from .startup_dna_library import StartupDNALibrary, DNAPattern
from .dna_matcher import DNAMatcher, DNAMatch

logger = logging.getLogger(__name__)

class DNAPatternAnalyzer(BaseMLModel):
    """
    Advanced DNA Pattern Analysis for Startups
    Combines domain knowledge with unsupervised pattern discovery
    """

    def _encode_features(self, X: pd.DataFrame) -> pd.DataFrame:
        """Encode categorical features to match training data"""
        X_encoded = X.copy()
        
        # Encoding mappings from training
        funding_stage_map = {
            'Pre-seed': 0, 'Seed': 1, 'Series A': 2, 
            'Series B': 3, 'Series C+': 4, 'Unknown': 5
        }
        sector_map = {
            'Technology': 0, 'Healthcare': 1, 'Financial Services': 2,
            'Consumer': 3, 'Enterprise Software': 4, 'Unknown': 5
        }
        product_stage_map = {
            'MVP': 0, 'Beta': 1, 'Live': 2, 'Growth': 3, 'Unknown': 4
        }
        investor_tier_map = {1: 0, 2: 1, 3: 2, 'Unknown': 3}
        
        # Apply encodings
        if 'funding_stage' in X_encoded.columns:
            X_encoded['funding_stage'] = X_encoded['funding_stage'].map(funding_stage_map).fillna(5)
        if 'sector' in X_encoded.columns:
            X_encoded['sector'] = X_encoded['sector'].map(sector_map).fillna(5)
        if 'product_stage' in X_encoded.columns:
            X_encoded['product_stage'] = X_encoded['product_stage'].map(product_stage_map).fillna(4)
        if 'investor_tier_primary' in X_encoded.columns:
            X_encoded['investor_tier_primary'] = X_encoded['investor_tier_primary'].map(investor_tier_map).fillna(3)
            
        return X_encoded
    
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__(config)
        
        # Configuration
        self.config.update({
            'n_discovered_patterns': self.config.get('n_discovered_patterns', 10),
            'n_components': self.config.get('n_components', 20),
            'use_library': self.config.get('use_library', True),
            'min_pattern_size': self.config.get('min_pattern_size', 100),
            'enable_evolution': self.config.get('enable_evolution', True)
        })
        
        # Core components
        self.dna_library = StartupDNALibrary()
        self.dna_matcher = DNAMatcher(self.dna_library)
        
        # Pattern discovery components
        self.scaler = StandardScaler()
        self.pca = PCA(n_components=self.config['n_components'], random_state=42)
        self.pattern_discoverer = KMeans(
            n_clusters=self.config['n_discovered_patterns'],
            random_state=42,
            n_init=10
        )
        
        # Success prediction models
        self.pattern_predictors = {}
        self.meta_predictor = None
        
        # Discovered patterns
        self.discovered_patterns = {}
        self.pattern_assignments = {}
        self.pattern_evolution_map = {}
        
    def fit(self, X: pd.DataFrame, y: np.ndarray) -> 'DNAPatternAnalyzer':
        """Train the DNA Pattern Analyzer"""
        logger.info(f"Training DNA Pattern Analyzer on {len(X)} samples")
        
        # Store metadata
        self.metadata['feature_names'] = X.columns.tolist()
        self.metadata['trained_on_samples'] = len(X)
        
        # Step 1: Match to library patterns
        logger.info("Step 1: Matching to DNA library patterns...")
        library_assignments = self._match_to_library(X, y)
        
        # Step 2: Discover new patterns in unmatched data
        logger.info("Step 2: Discovering new patterns...")
        discovered_assignments = self._discover_new_patterns(X, y, library_assignments)
        
        # Step 3: Combine assignments
        self.pattern_assignments = self._combine_assignments(
            library_assignments, discovered_assignments
        )
        
        # Step 4: Train pattern-specific predictors
        logger.info("Step 3: Training pattern-specific models...")
        self._train_pattern_predictors(X, y)
        
        # Step 5: Train meta predictor
        logger.info("Step 4: Training meta ensemble...")
        self._train_meta_predictor(X, y)
        
        # Step 6: Learn evolution paths
        if self.config['enable_evolution']:
            logger.info("Step 5: Learning evolution paths...")
            self._learn_evolution_paths(X, y)
        
        # Calculate performance
        self._calculate_performance_metrics(X, y)
        
        logger.info("DNA Pattern Analyzer training complete")
        return self
    
    def _match_to_library(self, X: pd.DataFrame, y: np.ndarray) -> Dict[int, str]:
        """Match each startup to library patterns"""
        # First train the matcher
        self.dna_matcher.train(X, y)
        
        assignments = {}
        unmatched_indices = []
        
        for i in range(len(X)):
            startup_data = X.iloc[i:i+1]
            matches = self.dna_matcher.match_dna(startup_data, top_k=1)
            
            if matches and matches[0].overall_score > 0.6:
                # Good match to library pattern
                assignments[i] = matches[0].pattern_name
            else:
                # Poor match - candidate for new pattern discovery
                unmatched_indices.append(i)
                assignments[i] = None
        
        matched_count = sum(1 for v in assignments.values() if v is not None)
        logger.info(f"Matched {matched_count}/{len(X)} to library patterns")
        
        return assignments
    
    def _discover_new_patterns(self, X: pd.DataFrame, y: np.ndarray,
                              library_assignments: Dict[int, str]) -> Dict[int, str]:
        """Discover new patterns in unmatched data"""
        # Get unmatched indices
        unmatched_indices = [i for i, v in library_assignments.items() if v is None]
        
        if len(unmatched_indices) < self.config['min_pattern_size']:
            logger.info("Not enough unmatched samples for pattern discovery")
            return {}
        
        # Extract unmatched data
        X_unmatched = X.iloc[unmatched_indices]
        y_unmatched = y[unmatched_indices]
        
        # Scale and reduce dimensions
        X_scaled = self.scaler.fit_transform(X_unmatched)
        X_pca = self.pca.fit_transform(X_scaled)
        
        # Discover clusters
        clusters = self.pattern_discoverer.fit_predict(X_pca)
        
        # Analyze discovered patterns
        discovered_assignments = {}
        
        for cluster_id in range(self.config['n_discovered_patterns']):
            cluster_mask = clusters == cluster_id
            if cluster_mask.sum() < 10:
                continue
            
            # Analyze cluster characteristics
            cluster_success_rate = y_unmatched[cluster_mask].mean()
            cluster_size = cluster_mask.sum()
            
            # Create pattern name based on characteristics
            pattern_name = self._name_discovered_pattern(
                X_unmatched[cluster_mask], 
                cluster_success_rate,
                cluster_id
            )
            
            # Store pattern information
            self.discovered_patterns[pattern_name] = {
                'success_rate': cluster_success_rate,
                'size': cluster_size,
                'centroid': X_scaled[cluster_mask].mean(axis=0),
                'key_features': self._extract_key_features(
                    X_unmatched[cluster_mask], 
                    X_unmatched
                )
            }
            
            # Assign pattern to indices
            for idx, is_in_cluster in zip(unmatched_indices, cluster_mask):
                if is_in_cluster:
                    discovered_assignments[idx] = pattern_name
        
        logger.info(f"Discovered {len(self.discovered_patterns)} new patterns")
        return discovered_assignments
    
    def _name_discovered_pattern(self, cluster_data: pd.DataFrame, 
                                success_rate: float, cluster_id: int) -> str:
        """Generate meaningful name for discovered pattern"""
        # Analyze cluster characteristics
        avg_growth = cluster_data.get('revenue_growth_rate_percent', pd.Series([0])).mean()
        avg_burn = cluster_data.get('burn_multiple', pd.Series([0])).mean()
        avg_efficiency = cluster_data.get('ltv_cac_ratio', pd.Series([0])).mean()
        
        # Generate name based on characteristics
        if success_rate > 0.7:
            prefix = "HIGH_PERFORMANCE"
        elif success_rate < 0.3:
            prefix = "STRUGGLING"
        else:
            prefix = "MODERATE"
        
        if avg_growth > 150:
            growth_tag = "HYPERGROWTH"
        elif avg_growth > 50:
            growth_tag = "GROWTH"
        else:
            growth_tag = "SLOW"
        
        if avg_burn > 3:
            efficiency_tag = "BURN"
        elif avg_efficiency > 3:
            efficiency_tag = "EFFICIENT"
        else:
            efficiency_tag = "BALANCED"
        
        return f"DISCOVERED_{prefix}_{growth_tag}_{efficiency_tag}_{cluster_id}"
    
    def _extract_key_features(self, cluster_data: pd.DataFrame, 
                             all_data: pd.DataFrame) -> List[str]:
        """Extract most distinguishing features for a cluster"""
        # Calculate feature importance using statistical tests
        key_features = []
        
        for column in cluster_data.columns:
            try:
                cluster_mean = cluster_data[column].mean()
                overall_mean = all_data[column].mean()
                
                # Simple effect size calculation
                if overall_mean != 0:
                    effect_size = abs(cluster_mean - overall_mean) / overall_mean
                    if effect_size > 0.5:  # 50% difference
                        key_features.append((column, effect_size))
            except:
                continue
        
        # Sort by effect size and return top features
        key_features.sort(key=lambda x: x[1], reverse=True)
        return [f[0] for f in key_features[:5]]
    
    def _combine_assignments(self, library: Dict[int, str], 
                           discovered: Dict[int, str]) -> Dict[int, str]:
        """Combine library and discovered pattern assignments"""
        combined = library.copy()
        
        for idx, pattern in discovered.items():
            if combined.get(idx) is None:
                combined[idx] = pattern
        
        # Handle any remaining unassigned
        for idx in combined:
            if combined[idx] is None:
                combined[idx] = 'UNCLASSIFIED'
        
        return combined
    
    def _train_pattern_predictors(self, X: pd.DataFrame, y: np.ndarray):
        """Train a predictor for each pattern"""
        pattern_counts = {}
        
        for pattern in set(self.pattern_assignments.values()):
            if pattern == 'UNCLASSIFIED':
                continue
            
            # Get indices for this pattern
            indices = [i for i, p in self.pattern_assignments.items() if p == pattern]
            pattern_counts[pattern] = len(indices)
            
            if len(indices) < 20:  # Skip patterns with too few samples
                continue
            
            # Extract pattern data
            X_pattern = X.iloc[indices]
            y_pattern = y[indices]
            
            # Choose model based on sample size
            if len(indices) < 100:
                # Simple model for small samples
                model = RandomForestClassifier(
                    n_estimators=50,
                    max_depth=4,
                    random_state=42
                )
            elif len(indices) < 500:
                # XGBoost for medium samples
                model = xgb.XGBClassifier(
                    n_estimators=100,
                    max_depth=4,
                    learning_rate=0.1,
                    random_state=42,
                    use_label_encoder=False,
                    eval_metric='logloss'
                )
            else:
                # CatBoost for large samples
                model = CatBoostClassifier(
                    iterations=200,
                    depth=6,
                    learning_rate=0.1,
                    random_seed=42,
                    verbose=False
                )
            
            # Train model
            model.fit(X_pattern, y_pattern)
            self.pattern_predictors[pattern] = model
            
            logger.info(f"Trained predictor for {pattern} ({len(indices)} samples)")
        
        # Log pattern distribution
        logger.info(f"Pattern distribution: {pattern_counts}")
    
    def _train_meta_predictor(self, X: pd.DataFrame, y: np.ndarray):
        """Train meta model that combines pattern predictions"""
        # Get predictions from each pattern predictor
        meta_features = []
        
        for i in range(len(X)):
            pattern = self.pattern_assignments[i]
            features = []
            
            # Add pattern predictions
            for p_name, p_model in self.pattern_predictors.items():
                if p_name == pattern and i in [idx for idx, p in self.pattern_assignments.items() if p == p_name]:
                    # In-pattern prediction
                    pred = p_model.predict_proba(X.iloc[i:i+1])[0, 1]
                else:
                    # Out-of-pattern prediction (useful signal)
                    pred = 0.5  # Neutral
                features.append(pred)
            
            # Add pattern match scores
            matches = self.dna_matcher.match_dna(X.iloc[i:i+1], top_k=3)
            for match in matches:
                features.append(match.overall_score)
            
            meta_features.append(features)
        
        meta_features = np.array(meta_features)
        
        # Train gradient boosting as meta model
        self.meta_predictor = GradientBoostingClassifier(
            n_estimators=100,
            max_depth=3,
            learning_rate=0.1,
            random_state=42
        )
        self.meta_predictor.fit(meta_features, y)
        
        logger.info("Trained meta predictor")
    
    def _learn_evolution_paths(self, X: pd.DataFrame, y: np.ndarray):
        """Learn how startups evolve between patterns over time"""
        # This would require temporal data - simplified version
        # Maps current pattern to likely next patterns
        
        evolution_map = {}
        
        # Use funding stage as proxy for evolution
        if 'funding_stage' in X.columns:
            stages = ['pre_seed', 'seed', 'series_a', 'series_b', 'series_c']
            
            for i, current_stage in enumerate(stages[:-1]):
                next_stage = stages[i + 1]
                
                # Find patterns common at each stage
                current_patterns = [
                    self.pattern_assignments[idx] 
                    for idx in range(len(X))
                    if X.iloc[idx].get('funding_stage') == current_stage
                ]
                
                next_patterns = [
                    self.pattern_assignments[idx]
                    for idx in range(len(X))
                    if X.iloc[idx].get('funding_stage') == next_stage
                ]
                
                # Simple transition counting
                for pattern in set(current_patterns):
                    if pattern not in evolution_map:
                        evolution_map[pattern] = {}
                    
                    for next_pattern in set(next_patterns):
                        evolution_map[pattern][next_pattern] = \
                            evolution_map[pattern].get(next_pattern, 0) + 1
        
        self.pattern_evolution_map = evolution_map
    
    def predict_proba(self, X: pd.DataFrame) -> np.ndarray:
        """Predict success probability with DNA analysis"""
        # Encode categorical features
        X = self._encode_features(X)
        
        n_samples = len(X)
        probabilities = np.zeros((n_samples, 2))
        
        for i in range(n_samples):
            startup_data = X.iloc[i:i+1]
            
            # Get DNA matches
            matches = self.dna_matcher.match_dna(startup_data, top_k=3)
            
            if matches:
                primary_pattern = matches[0].pattern_name
                
                # Use pattern-specific predictor if available
                if primary_pattern in self.pattern_predictors:
                    # Get pattern prediction
                    pattern_prob = self.pattern_predictors[primary_pattern].predict_proba(startup_data)[0]
                    
                    # Adjust based on match confidence
                    confidence_weight = matches[0].confidence
                    
                    # Blend with pattern success rate
                    pattern_obj = self.dna_library.get_pattern(primary_pattern)
                    if pattern_obj:
                        base_rate = pattern_obj.success_rate
                    else:
                        base_rate = self.discovered_patterns.get(primary_pattern, {}).get('success_rate', 0.5)
                    
                    # Weighted combination
                    final_prob = (
                        confidence_weight * pattern_prob[1] + 
                        (1 - confidence_weight) * base_rate
                    )
                    
                    probabilities[i] = [1 - final_prob, final_prob]
                else:
                    # Use base model prediction when no pattern match
                    if hasattr(self, 'base_model') and self.base_model is not None:
                        base_pred = self.base_model.predict_proba(startup_data)
                        probabilities[i] = base_pred[0]
                    else:
                        # Conservative estimate when no info available
                        probabilities[i] = [0.7, 0.3]  # 30% success rate baseline
            else:
                # No pattern match - use base model if available
                if hasattr(self, 'base_model') and self.base_model is not None:
                    base_pred = self.base_model.predict_proba(startup_data)
                    probabilities[i] = base_pred[0]
                else:
                    # Conservative estimate when no info available
                    probabilities[i] = [0.7, 0.3]  # 30% success rate baseline
        
        return probabilities
    
    def get_dna_analysis(self, X: pd.DataFrame) -> Dict[str, Any]:
        """Get comprehensive DNA analysis for a startup"""
        # Encode categorical features
        X = self._encode_features(X)
        
        if len(X) > 1:
            X = X.iloc[:1]
        
        # Get DNA matches
        matches = self.dna_matcher.match_dna(X, top_k=3)
        
        if not matches:
            return {
                'status': 'no_match',
                'message': 'Unable to match to any DNA pattern'
            }
        
        primary_match = matches[0]
        pattern = self.dna_library.get_pattern(primary_match.pattern_name)
        
        # Get prediction
        prob = self.predict_proba(X)[0, 1]
        
        # Build comprehensive analysis
        analysis = {
            'primary_dna': {
                'pattern': primary_match.pattern_name,
                'confidence': primary_match.confidence,
                'description': pattern.description if pattern else 'Discovered pattern',
                'match_score': primary_match.overall_score
            },
            'success_probability': float(prob),
            'similar_companies': pattern.examples[:3] if pattern else [],
            'pattern_success_rate': pattern.success_rate if pattern else 0.5,
            'match_details': primary_match.match_details,
            'evolution_stage': primary_match.evolution_stage,
            'recommendations': primary_match.recommendations,
            'secondary_patterns': [
                {
                    'pattern': m.pattern_name,
                    'score': m.overall_score,
                    'confidence': m.confidence
                }
                for m in matches[1:3]
            ],
            'evolution_paths': pattern.evolution_paths if pattern else [],
            'key_risks': pattern.key_risks[:3] if pattern else [],
            'success_factors': pattern.success_factors[:3] if pattern else [],
            'dna_explanation': self.dna_matcher.explain_dna_match(primary_match)
        }
        
        return analysis
    
    def _calculate_performance_metrics(self, X: pd.DataFrame, y: np.ndarray):
        """Calculate and store performance metrics"""
        from sklearn.metrics import roc_auc_score, accuracy_score
        
        # Get predictions
        y_pred_proba = self.predict_proba(X)[:, 1]
        y_pred = (y_pred_proba >= 0.5).astype(int)
        
        # Calculate metrics
        self.metadata['performance_metrics'] = {
            'auc': float(roc_auc_score(y, y_pred_proba)),
            'accuracy': float(accuracy_score(y, y_pred)),
            'pattern_count': len(self.pattern_predictors),
            'library_patterns_used': sum(1 for p in self.pattern_predictors.keys() 
                                       if p in [pattern.name for pattern in self.dna_library.patterns]),
            'discovered_patterns': len(self.discovered_patterns)
        }
        
        logger.info(f"Model AUC: {self.metadata['performance_metrics']['auc']:.4f}")
    
    def _get_serializable_components(self) -> Dict[str, Any]:
        """Get components for serialization"""
        return {
            'dna_library': self.dna_library,
            'dna_matcher': self.dna_matcher,
            'scaler': self.scaler,
            'pca': self.pca,
            'pattern_discoverer': self.pattern_discoverer,
            'pattern_predictors': self.pattern_predictors,
            'meta_predictor': self.meta_predictor,
            'discovered_patterns': self.discovered_patterns,
            'pattern_assignments': self.pattern_assignments,
            'pattern_evolution_map': self.pattern_evolution_map
        }
    
    def _load_components(self, components: Dict[str, Any]) -> None:
        """Load components from serialized data"""
        self.dna_library = components['dna_library']
        self.dna_matcher = components['dna_matcher']
        self.scaler = components['scaler']
        self.pca = components['pca']
        self.pattern_discoverer = components['pattern_discoverer']
        self.pattern_predictors = components['pattern_predictors']
        self.meta_predictor = components['meta_predictor']
        self.discovered_patterns = components['discovered_patterns']
        self.pattern_assignments = components['pattern_assignments']
        self.pattern_evolution_map = components['pattern_evolution_map']