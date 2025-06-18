"""
Fixed Pattern Classifier Wrapper
Uses the correct feature order matching the dataset
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

# EXACT feature order from the dataset
DATASET_FEATURES = [
    'funding_stage',
    'total_capital_raised_usd',
    'cash_on_hand_usd',
    'monthly_burn_usd',
    'runway_months',
    'annual_revenue_run_rate',
    'revenue_growth_rate_percent',
    'gross_margin_percent',
    'burn_multiple',
    'ltv_cac_ratio',
    'investor_tier_primary',
    'has_debt',
    'patent_count',
    'network_effects_present',
    'has_data_moat',
    'regulatory_advantage_present',
    'tech_differentiation_score',
    'switching_cost_score',
    'brand_strength_score',
    'scalability_score',
    'product_stage',
    'product_retention_30d',
    'product_retention_90d',
    'sector',
    'tam_size_usd',
    'sam_size_usd',
    'som_size_usd',
    'market_growth_rate_percent',
    'customer_count',
    'customer_concentration_percent',
    'user_growth_rate_percent',
    'net_dollar_retention_percent',
    'competition_intensity',
    'competitors_named_count',
    'dau_mau_ratio',
    'founders_count',
    'team_size_full_time',
    'years_experience_avg',
    'domain_expertise_years_avg',
    'prior_startup_experience_count',
    'prior_successful_exits_count',
    'board_advisor_experience_score',
    'advisors_count',
    'team_diversity_percent',
    'key_person_dependency'
]

CATEGORICAL_FEATURES = ['funding_stage', 'investor_tier_primary', 'product_stage', 'sector']
BOOLEAN_FEATURES = ['has_debt', 'network_effects_present', 'has_data_moat', 
                    'regulatory_advantage_present', 'key_person_dependency']


class FixedPatternClassifier:
    """Pattern classifier with correct feature ordering"""
    
    def __init__(self, model_dir: str = 'models/pattern_v3_fixed'):
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
    
    def prepare_features(self, startup_data: Dict) -> pd.DataFrame:
        """Prepare features in the exact order expected by models"""
        # Create DataFrame with one row
        df = pd.DataFrame([startup_data])
        
        # Process features in exact dataset order
        processed_features = []
        feature_columns = []
        
        for feature in DATASET_FEATURES:
            if feature in CATEGORICAL_FEATURES:
                # One-hot encode categorical features
                if feature in df.columns:
                    value = df[feature].iloc[0]
                    # Get unique values from training (simplified for now)
                    if feature == 'funding_stage':
                        categories = ['Pre-seed', 'Seed', 'Series A', 'Series B', 'Series C', 'Series C+']
                    elif feature == 'investor_tier_primary':
                        categories = ['None', 'Tier3', 'Tier2', 'Tier1']
                    elif feature == 'product_stage':
                        categories = ['Concept', 'MVP', 'Beta', 'Launch', 'GA', 'Growth', 'Mature']
                    elif feature == 'sector':
                        categories = ['SaaS', 'E-commerce', 'Marketplace', 'AI/ML', 'FinTech', 
                                    'HealthTech', 'EdTech', 'Gaming', 'Hardware', 'Other']
                    
                    for cat in categories:
                        col_name = f"{feature}_{cat}"
                        processed_features.append(1 if str(value) == cat else 0)
                        feature_columns.append(col_name)
                else:
                    # If feature is missing, add zeros for all categories
                    if feature == 'funding_stage':
                        num_cats = 6
                    elif feature == 'investor_tier_primary':
                        num_cats = 4
                    elif feature == 'product_stage':
                        num_cats = 7
                    elif feature == 'sector':
                        num_cats = 10
                    
                    for i in range(num_cats):
                        processed_features.append(0)
                        feature_columns.append(f"{feature}_unknown_{i}")
            
            elif feature in BOOLEAN_FEATURES:
                # Boolean features
                if feature in df.columns:
                    value = df[feature].iloc[0]
                    processed_features.append(int(value) if pd.notna(value) else 0)
                else:
                    processed_features.append(0)
                feature_columns.append(feature)
            
            else:
                # Numeric features
                if feature in df.columns:
                    value = df[feature].iloc[0]
                    processed_features.append(float(value) if pd.notna(value) else 0.0)
                else:
                    processed_features.append(0.0)
                feature_columns.append(feature)
        
        # Create final DataFrame
        result_df = pd.DataFrame([processed_features], columns=feature_columns)
        
        return result_df
    
    def predict(self, startup_data: Dict) -> Dict:
        """Predict patterns for a startup"""
        if not self.is_loaded:
            self.load_models()
        
        # Prepare features
        df = self.prepare_features(startup_data)
        
        # Get predictions from each model
        predictions = []
        category_scores = {}
        
        for pattern_name, model_info in self.pattern_models.items():
            model = model_info['model']
            scaler = model_info['scaler']
            features = model_info['features']
            
            # Select features in the order the model expects
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
        
        # Calculate overall pattern score for orchestrator
        if predictions:
            # Weighted average of top patterns
            top_scores = [p['confidence'] for p in predictions[:5]]
            pattern_score = np.average(top_scores, weights=range(len(top_scores), 0, -1))
        else:
            pattern_score = 0.5
        
        # Identify primary patterns (confidence > 0.5)
        primary_patterns = [p for p in predictions if p['confidence'] > 0.5]
        secondary_patterns = [p for p in predictions if 0.3 <= p['confidence'] <= 0.5]
        
        # Generate insights
        insights = self._generate_insights(primary_patterns, secondary_patterns)
        
        return {
            'pattern_score': float(pattern_score),  # For orchestrator
            'primary_patterns': primary_patterns[:5],  # Top 5
            'secondary_patterns': secondary_patterns[:5],  # Next 5
            'category_scores': category_scores,
            'total_patterns_detected': len(predictions),
            'insights': insights,
            'coverage_info': {
                'patterns_available': len(self.pattern_models),
                'total_patterns': 45,
                'coverage_percentage': len(self.pattern_models) / 45
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
        _pattern_classifier = FixedPatternClassifier()
        _pattern_classifier.load_models()
    return _pattern_classifier