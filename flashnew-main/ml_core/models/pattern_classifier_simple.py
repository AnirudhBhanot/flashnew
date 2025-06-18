"""
Simple Pattern Classifier Wrapper
Uses the trained simplified pattern models
"""

import pandas as pd
import numpy as np
import joblib
import json
from pathlib import Path
from typing import Dict, List, Tuple
import logging

from .pattern_definitions_v2 import PATTERN_LOOKUP, MasterCategory

logger = logging.getLogger(__name__)


class SimplePatternClassifier:
    """Simplified pattern classifier using pre-trained models"""
    
    def __init__(self, model_dir: str = 'models/pattern_v2_simple'):
        self.model_dir = Path(model_dir)
        self.pattern_models = {}
        self.metadata = {}
        self.is_loaded = False
        
    def load_models(self):
        """Load all trained pattern models"""
        if self.is_loaded:
            return
            
        # Load metadata
        metadata_path = self.model_dir / 'metadata.json'
        if not metadata_path.exists():
            logger.warning(f"No metadata found at {metadata_path}")
            return
            
        with open(metadata_path, 'r') as f:
            self.metadata = json.load(f)
        
        # Load each pattern model
        pattern_stats = self.metadata.get('pattern_stats', {})
        loaded_count = 0
        
        for pattern_name in pattern_stats.keys():
            pattern_dir = self.model_dir / pattern_name
            
            try:
                model = joblib.load(pattern_dir / 'model.pkl')
                scaler = joblib.load(pattern_dir / 'scaler.pkl')
                features = joblib.load(pattern_dir / 'features.pkl')
                
                self.pattern_models[pattern_name] = {
                    'model': model,
                    'scaler': scaler,
                    'features': features,
                    'stats': pattern_stats[pattern_name]
                }
                loaded_count += 1
                
            except Exception as e:
                logger.warning(f"Could not load model for {pattern_name}: {e}")
        
        logger.info(f"Loaded {loaded_count} pattern models")
        self.is_loaded = True
    
    def prepare_features(self, startup_data: Dict) -> Tuple[pd.DataFrame, List[str]]:
        """Prepare features for prediction"""
        # Create DataFrame
        df = pd.DataFrame([startup_data])
        
        # Numeric features
        numeric_features = [
            'revenue_growth_rate_percent',
            'user_growth_rate_percent',
            'customer_count',
            'net_dollar_retention_percent',
            'burn_multiple',
            'dau_mau_ratio',
            'gross_margin_percent',
            'ltv_cac_ratio',
            'annual_revenue_run_rate',
            'customer_concentration_percent',
            'product_retention_30d',
            'tech_differentiation_score',
            'patent_count',
            'scalability_score',
            'team_size_full_time',
            'prior_successful_exits_count',
            'years_experience_avg',
            'domain_expertise_years_avg',
            'board_advisor_experience_score',
            'total_capital_raised_usd',
            'runway_months',
            'has_debt',
            'network_effects_present',
            'has_data_moat',
            'regulatory_advantage_present',
            'key_person_dependency'
        ]
        
        # Ensure all numeric features exist
        for col in numeric_features:
            if col not in df.columns:
                df[col] = 0
            else:
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
        
        # Handle categorical features
        feature_list = numeric_features.copy()
        
        if 'funding_stage' in df.columns:
            funding_dummies = pd.get_dummies(df['funding_stage'], prefix='funding')
            for col in funding_dummies.columns:
                df[col] = funding_dummies[col]
                feature_list.append(col)
        
        if 'product_stage' in df.columns:
            product_dummies = pd.get_dummies(df['product_stage'], prefix='product')
            for col in product_dummies.columns:
                df[col] = product_dummies[col]
                feature_list.append(col)
        
        return df, feature_list
    
    def predict(self, startup_data: Dict) -> Dict:
        """Predict patterns for a startup"""
        if not self.is_loaded:
            self.load_models()
        
        # Prepare features
        df, _ = self.prepare_features(startup_data)
        
        # Get predictions from each model
        predictions = []
        category_scores = {}
        
        for pattern_name, model_info in self.pattern_models.items():
            model = model_info['model']
            scaler = model_info['scaler']
            features = model_info['features']
            
            # Ensure all required features exist
            missing_features = [f for f in features if f not in df.columns]
            for f in missing_features:
                df[f] = 0
            
            # Get features and scale
            X = df[features].values
            X_scaled = scaler.transform(X)
            
            # Get prediction probability
            prob = model.predict_proba(X_scaled)[0, 1]
            
            # Get pattern info
            pattern = PATTERN_LOOKUP.get(pattern_name)
            if pattern:
                # Track category scores
                category = pattern.master_category.value
                if category not in category_scores:
                    category_scores[category] = []
                category_scores[category].append(prob)
                
                # Add to predictions if confident enough
                if prob > 0.3:  # Lower threshold to catch more patterns
                    predictions.append({
                        'pattern': pattern_name,
                        'confidence': float(prob),
                        'category': category,
                        'description': pattern.description,
                        'success_rate_range': pattern.typical_success_rate,
                        'key_factors': pattern.key_success_factors[:3]
                    })
        
        # Sort by confidence
        predictions.sort(key=lambda x: x['confidence'], reverse=True)
        
        # Calculate category scores (average of pattern scores in category)
        for cat, scores in category_scores.items():
            category_scores[cat] = float(np.mean(scores))
        
        # Identify primary patterns (confidence > 0.5)
        primary_patterns = [p for p in predictions if p['confidence'] > 0.5]
        secondary_patterns = [p for p in predictions if 0.3 <= p['confidence'] <= 0.5]
        
        # Generate insights
        insights = self._generate_insights(primary_patterns, secondary_patterns)
        
        return {
            'primary_patterns': primary_patterns[:5],  # Top 5
            'secondary_patterns': secondary_patterns[:5],  # Next 5
            'category_scores': category_scores,
            'total_patterns_detected': len(predictions),
            'insights': insights,
            'coverage_info': {
                'patterns_available': len(self.pattern_models),
                'total_patterns': 45,
                'coverage_percentage': self.metadata.get('pattern_stats', {}).get('coverage', 0.574)
            }
        }
    
    def _generate_insights(self, primary_patterns, secondary_patterns):
        """Generate insights based on detected patterns"""
        insights = []
        
        if not primary_patterns:
            insights.append({
                'type': 'warning',
                'message': 'No strong pattern match detected. Consider clarifying strategic focus.'
            })
        else:
            # Dominant pattern insight
            top_pattern = primary_patterns[0]
            pattern_def = PATTERN_LOOKUP.get(top_pattern['pattern'])
            if pattern_def:
                insights.append({
                    'type': 'primary',
                    'message': f"Strong {top_pattern['pattern']} pattern detected ({top_pattern['confidence']:.0%} confidence). Focus on: {', '.join(pattern_def.key_success_factors[:2])}"
                })
            
            # Category dominance
            categories = {}
            for p in primary_patterns:
                cat = p['category']
                categories[cat] = categories.get(cat, 0) + 1
            
            if len(categories) > 1:
                dominant_cat = max(categories.items(), key=lambda x: x[1])[0]
                insights.append({
                    'type': 'category',
                    'message': f"Primary focus area: {dominant_cat.replace('_', ' ').title()}"
                })
        
        # Evolution opportunities
        if primary_patterns:
            for p in primary_patterns[:2]:
                pattern_def = PATTERN_LOOKUP.get(p['pattern'])
                if pattern_def and pattern_def.evolution_paths:
                    insights.append({
                        'type': 'evolution',
                        'message': f"Potential evolution path: {p['pattern']} → {pattern_def.evolution_paths[0]}"
                    })
        
        return insights
    
    def get_pattern_info(self, pattern_name: str) -> Dict:
        """Get detailed information about a specific pattern"""
        pattern = PATTERN_LOOKUP.get(pattern_name)
        if not pattern:
            return None
            
        stats = self.metadata.get('pattern_stats', {}).get(pattern_name, {})
        
        return {
            'name': pattern.name,
            'category': pattern.master_category.value,
            'description': pattern.description,
            'success_rate_range': pattern.typical_success_rate,
            'typical_characteristics': {
                'team_size': pattern.typical_team_size,
                'burn_multiple': pattern.typical_burn_multiple,
                'growth_rate': pattern.typical_growth_rate,
                'gross_margin': pattern.typical_gross_margin
            },
            'key_success_factors': pattern.key_success_factors,
            'common_failure_modes': pattern.common_failure_modes,
            'strategic_recommendations': pattern.strategic_recommendations,
            'example_companies': pattern.example_companies,
            'evolution_paths': pattern.evolution_paths,
            'compatible_patterns': pattern.compatible_patterns,
            'incompatible_patterns': pattern.incompatible_patterns,
            'training_stats': {
                'examples_in_dataset': stats.get('positive_examples', 0),
                'dataset_percentage': stats.get('percentage', 0),
                'model_accuracy': stats.get('test_accuracy', 0)
            }
        }
    
    def list_available_patterns(self) -> List[Dict]:
        """List all available patterns"""
        if not self.is_loaded:
            self.load_models()
            
        patterns = []
        for pattern_name in self.pattern_models.keys():
            pattern = PATTERN_LOOKUP.get(pattern_name)
            if pattern:
                stats = self.metadata.get('pattern_stats', {}).get(pattern_name, {})
                patterns.append({
                    'name': pattern_name,
                    'category': pattern.master_category.value,
                    'description': pattern.description,
                    'examples_in_dataset': stats.get('positive_examples', 0),
                    'success_rate_range': pattern.typical_success_rate
                })
        
        return sorted(patterns, key=lambda x: x['category'])


# Singleton instance
_pattern_classifier = None

def get_pattern_classifier():
    """Get or create the singleton pattern classifier"""
    global _pattern_classifier
    if _pattern_classifier is None:
        _pattern_classifier = SimplePatternClassifier()
        _pattern_classifier.load_models()
    return _pattern_classifier