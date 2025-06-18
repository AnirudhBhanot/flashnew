"""
Hierarchical Pattern Classifier for FLASH V2
Handles 45 patterns organized into 8 master categories
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional, Set
from dataclasses import dataclass
import joblib
import logging
from pathlib import Path

from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import roc_auc_score, precision_recall_curve
from sklearn.multioutput import MultiOutputClassifier
import xgboost as xgb
import lightgbm as lgb

from .pattern_definitions_v2 import (
    ALL_PATTERNS, PATTERN_LOOKUP, MasterCategory,
    PatternDefinition, PATTERN_COMPATIBILITY_MATRIX
)

logger = logging.getLogger(__name__)


@dataclass
class PatternPrediction:
    """Single pattern prediction with confidence"""
    pattern_name: str
    confidence: float
    master_category: MasterCategory
    compatible_patterns: List[str]
    incompatible_patterns: List[str]
    
    def to_dict(self):
        return {
            'pattern': self.pattern_name,
            'confidence': round(self.confidence, 3),
            'category': self.master_category.value,
            'compatible_with': self.compatible_patterns,
            'incompatible_with': self.incompatible_patterns
        }


@dataclass
class StartupPatternProfile:
    """Complete pattern profile for a startup"""
    primary_patterns: List[PatternPrediction]  # Top patterns by confidence
    secondary_patterns: List[PatternPrediction]  # Additional relevant patterns
    master_categories: Dict[str, float]  # Category-level scores
    warnings: List[str]  # Pattern conflicts or issues
    recommendations: List[str]  # Strategic recommendations
    
    def to_dict(self):
        return {
            'primary_patterns': [p.to_dict() for p in self.primary_patterns],
            'secondary_patterns': [p.to_dict() for p in self.secondary_patterns],
            'master_categories': self.master_categories,
            'warnings': self.warnings,
            'recommendations': self.recommendations
        }


class HierarchicalPatternClassifier:
    """
    Two-tier hierarchical classifier for startup patterns
    Tier 1: Master categories (8)
    Tier 2: Specific patterns (45)
    """
    
    def __init__(self, model_dir: str = 'models/pattern_v2'):
        self.model_dir = Path(model_dir)
        self.model_dir.mkdir(parents=True, exist_ok=True)
        
        # Feature configuration
        self.feature_groups = {
            'growth': [
                'revenue_growth_rate_percent',
                'user_growth_rate_percent',
                'customer_count',
                'net_dollar_retention_percent',
                'burn_multiple',
                'dau_mau_ratio'
            ],
            'economics': [
                'gross_margin_percent',
                'ltv_cac_ratio',
                'annual_revenue_run_rate',
                'customer_concentration_percent',
                'product_retention_30d'
            ],
            'technology': [
                'tech_differentiation_score',
                'patent_count',
                'has_data_moat',
                'network_effects_present',
                'regulatory_advantage_present',
                'scalability_score'
            ],
            'team': [
                'team_size_full_time',
                'prior_successful_exits_count',
                'years_experience_avg',
                'domain_expertise_years_avg',
                'board_advisor_experience_score'
            ],
            'funding': [
                'total_capital_raised_usd',
                'runway_months',
                'has_debt',
                'investor_tier_primary'
            ]
        }
        
        # All features for training
        self.all_features = []
        for features in self.feature_groups.values():
            self.all_features.extend(features)
        
        # Models
        self.scalers = {}
        self.master_category_models = {}
        self.pattern_models = {}
        self.is_trained = False
        
        # Pattern metadata
        self.pattern_groups = self._organize_patterns_by_category()
        
    def _organize_patterns_by_category(self) -> Dict[MasterCategory, List[str]]:
        """Organize patterns by their master category"""
        groups = {}
        for pattern in ALL_PATTERNS:
            if pattern.master_category not in groups:
                groups[pattern.master_category] = []
            groups[pattern.master_category].append(pattern.name)
        return groups
    
    def train(self, df: pd.DataFrame, save_models: bool = True):
        """Train the hierarchical classifier"""
        logger.info(f"Training hierarchical classifier on {len(df)} samples")
        
        # Prepare features
        X = df[self.all_features].fillna(0)
        
        # Train master category classifiers
        self._train_master_category_models(X, df)
        
        # Train individual pattern models
        self._train_pattern_models(X, df)
        
        self.is_trained = True
        
        if save_models:
            self.save_models()
            
        logger.info("Training complete")
    
    def _train_master_category_models(self, X: pd.DataFrame, df: pd.DataFrame):
        """Train models for each master category"""
        logger.info("Training master category models...")
        
        # Create category labels
        category_labels = {}
        for category in MasterCategory:
            # A startup belongs to a category if it matches any pattern in that category
            category_mask = pd.Series(False, index=df.index)
            
            for pattern_name in self.pattern_groups.get(category, []):
                if f'pattern_{pattern_name}' in df.columns:
                    category_mask |= (df[f'pattern_{pattern_name}'] == 1)
            
            category_labels[category.value] = category_mask.astype(int)
        
        # Train a model for each category
        for category_name, labels in category_labels.items():
            logger.info(f"Training {category_name} model (positive examples: {labels.sum()})")
            
            if labels.sum() < 100:
                logger.warning(f"Insufficient positive examples for {category_name}")
                continue
            
            # Scale features
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X)
            self.scalers[category_name] = scaler
            
            # Train ensemble model
            model = self._create_ensemble_model()
            
            # Handle class imbalance
            pos_weight = len(labels) / labels.sum()
            model.set_params(scale_pos_weight=pos_weight)
            
            # Train with cross-validation
            scores = cross_val_score(model, X_scaled, labels, cv=5, scoring='roc_auc')
            logger.info(f"{category_name} CV AUC: {scores.mean():.3f} (+/- {scores.std():.3f})")
            
            # Final training
            model.fit(X_scaled, labels)
            self.master_category_models[category_name] = model
    
    def _train_pattern_models(self, X: pd.DataFrame, df: pd.DataFrame):
        """Train models for individual patterns"""
        logger.info("Training individual pattern models...")
        
        for pattern in ALL_PATTERNS:
            pattern_col = f'pattern_{pattern.name}'
            
            if pattern_col not in df.columns:
                # Create synthetic labels based on pattern definition
                labels = self._create_pattern_labels(df, pattern)
            else:
                labels = df[pattern_col]
            
            if labels.sum() < 50:
                logger.warning(f"Insufficient examples for {pattern.name}")
                continue
            
            logger.info(f"Training {pattern.name} model (positive examples: {labels.sum()})")
            
            # Feature selection based on pattern requirements
            selected_features = self._select_pattern_features(pattern)
            X_pattern = X[selected_features]
            
            # Scale features
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X_pattern)
            self.scalers[pattern.name] = scaler
            
            # Create and train model
            model = self._create_pattern_model(pattern)
            
            # Handle class imbalance
            pos_weight = len(labels) / labels.sum() if labels.sum() > 0 else 1
            if hasattr(model, 'set_params'):
                model.set_params(scale_pos_weight=pos_weight)
            
            # Train
            model.fit(X_scaled, labels)
            self.pattern_models[pattern.name] = {
                'model': model,
                'features': selected_features,
                'threshold': self._find_optimal_threshold(model, X_scaled, labels)
            }
    
    def _create_pattern_labels(self, df: pd.DataFrame, pattern: PatternDefinition) -> pd.Series:
        """Create labels based on pattern definition criteria"""
        labels = pd.Series(True, index=df.index)
        
        # Apply required conditions
        for feature, condition in pattern.required_conditions.items():
            if feature in df.columns:
                labels &= df[feature].apply(condition)
        
        # Apply optional conditions (at least one must be met)
        if pattern.optional_conditions:
            optional_mask = pd.Series(False, index=df.index)
            for feature, condition in pattern.optional_conditions.items():
                if feature in df.columns:
                    optional_mask |= df[feature].apply(condition)
            labels &= optional_mask
        
        # Apply exclusion conditions
        for feature, condition in pattern.exclusion_conditions.items():
            if feature in df.columns:
                labels &= ~df[feature].apply(condition)
        
        return labels.astype(int)
    
    def _select_pattern_features(self, pattern: PatternDefinition) -> List[str]:
        """Select relevant features for a pattern"""
        # Start with features mentioned in pattern conditions
        relevant_features = set()
        
        for conditions in [pattern.required_conditions, 
                          pattern.optional_conditions, 
                          pattern.exclusion_conditions]:
            relevant_features.update(conditions.keys())
        
        # Add category-specific features
        if pattern.master_category == MasterCategory.GROWTH_DYNAMICS:
            relevant_features.update(self.feature_groups['growth'])
        elif pattern.master_category == MasterCategory.BUSINESS_MODEL:
            relevant_features.update(self.feature_groups['economics'])
        elif pattern.master_category == MasterCategory.TECHNOLOGY_DEPTH:
            relevant_features.update(self.feature_groups['technology'])
        elif pattern.master_category == MasterCategory.FUNDING_PROFILE:
            relevant_features.update(self.feature_groups['funding'])
        
        # Ensure all features exist
        available_features = [f for f in relevant_features if f in self.all_features]
        
        # Add some general features if too few
        if len(available_features) < 10:
            available_features.extend([
                'team_size_full_time',
                'total_capital_raised_usd', 
                'annual_revenue_run_rate',
                'tech_differentiation_score'
            ])
        
        return list(set(available_features))
    
    def _create_ensemble_model(self):
        """Create ensemble model for master categories"""
        return xgb.XGBClassifier(
            n_estimators=100,
            max_depth=6,
            learning_rate=0.1,
            objective='binary:logistic',
            eval_metric='auc',
            random_state=42,
            use_label_encoder=False
        )
    
    def _create_pattern_model(self, pattern: PatternDefinition):
        """Create model for specific pattern"""
        # Use different models based on pattern characteristics
        if pattern.master_category in [MasterCategory.TECHNOLOGY_DEPTH, 
                                      MasterCategory.INDUSTRY_VERTICAL]:
            # Complex patterns need gradient boosting
            return lgb.LGBMClassifier(
                n_estimators=150,
                max_depth=8,
                learning_rate=0.05,
                objective='binary',
                metric='auc',
                random_state=42,
                verbosity=-1
            )
        else:
            # Simpler patterns can use RandomForest
            return RandomForestClassifier(
                n_estimators=100,
                max_depth=10,
                min_samples_split=50,
                random_state=42,
                n_jobs=-1
            )
    
    def _find_optimal_threshold(self, model, X, y, target_precision=0.7):
        """Find optimal prediction threshold"""
        y_scores = model.predict_proba(X)[:, 1]
        precisions, recalls, thresholds = precision_recall_curve(y, y_scores)
        
        # Find threshold for target precision
        valid_idx = np.where(precisions >= target_precision)[0]
        if len(valid_idx) > 0:
            optimal_idx = valid_idx[np.argmax(recalls[valid_idx])]
            return float(thresholds[optimal_idx])
        else:
            return 0.5
    
    def predict(self, features: Dict[str, float]) -> StartupPatternProfile:
        """Predict patterns for a startup"""
        if not self.is_trained:
            raise ValueError("Classifier not trained yet")
        
        # Convert to DataFrame for consistency
        df = pd.DataFrame([features])
        df = df.reindex(columns=self.all_features, fill_value=0)
        
        # Step 1: Predict master categories
        category_scores = self._predict_master_categories(df)
        
        # Step 2: Predict individual patterns
        pattern_predictions = self._predict_patterns(df, category_scores)
        
        # Step 3: Check compatibility and conflicts
        warnings = self._check_pattern_conflicts(pattern_predictions)
        
        # Step 4: Generate recommendations
        recommendations = self._generate_recommendations(pattern_predictions)
        
        # Step 5: Create profile
        primary_patterns = [p for p in pattern_predictions if p.confidence >= 0.7]
        secondary_patterns = [p for p in pattern_predictions 
                            if 0.4 <= p.confidence < 0.7]
        
        # Sort by confidence
        primary_patterns.sort(key=lambda x: x.confidence, reverse=True)
        secondary_patterns.sort(key=lambda x: x.confidence, reverse=True)
        
        return StartupPatternProfile(
            primary_patterns=primary_patterns[:5],  # Top 5
            secondary_patterns=secondary_patterns[:5],  # Next 5
            master_categories=category_scores,
            warnings=warnings,
            recommendations=recommendations
        )
    
    def _predict_master_categories(self, df: pd.DataFrame) -> Dict[str, float]:
        """Predict master category scores"""
        scores = {}
        
        for category_name, model in self.master_category_models.items():
            if category_name in self.scalers:
                X_scaled = self.scalers[category_name].transform(df[self.all_features])
                score = float(model.predict_proba(X_scaled)[0, 1])
                scores[category_name] = round(score, 3)
        
        return scores
    
    def _predict_patterns(self, df: pd.DataFrame, 
                         category_scores: Dict[str, float]) -> List[PatternPrediction]:
        """Predict individual patterns"""
        predictions = []
        
        for pattern_name, pattern_info in self.pattern_models.items():
            pattern = PATTERN_LOOKUP[pattern_name]
            
            # Check if category score is high enough
            category_score = category_scores.get(pattern.master_category.value, 0)
            if category_score < 0.3:
                continue
            
            # Get features and scale
            features = pattern_info['features']
            X_pattern = df[features]
            
            if pattern_name in self.scalers:
                X_scaled = self.scalers[pattern_name].transform(X_pattern)
                
                # Predict
                model = pattern_info['model']
                confidence = float(model.predict_proba(X_scaled)[0, 1])
                
                # Apply threshold
                if confidence >= pattern_info['threshold'] * 0.8:  # 80% of optimal threshold
                    predictions.append(PatternPrediction(
                        pattern_name=pattern_name,
                        confidence=confidence,
                        master_category=pattern.master_category,
                        compatible_patterns=pattern.compatible_patterns,
                        incompatible_patterns=pattern.incompatible_patterns
                    ))
        
        return predictions
    
    def _check_pattern_conflicts(self, predictions: List[PatternPrediction]) -> List[str]:
        """Check for incompatible pattern combinations"""
        warnings = []
        pattern_names = [p.pattern_name for p in predictions if p.confidence >= 0.5]
        
        for i, pattern1 in enumerate(pattern_names):
            for pattern2 in pattern_names[i+1:]:
                # Check incompatibility
                pattern1_def = PATTERN_LOOKUP.get(pattern1)
                if pattern1_def and pattern2 in pattern1_def.incompatible_patterns:
                    warnings.append(
                        f"Pattern conflict: {pattern1} is incompatible with {pattern2}"
                    )
        
        # Check for missing complementary patterns
        for prediction in predictions:
            if prediction.confidence >= 0.7:
                pattern_def = PATTERN_LOOKUP.get(prediction.pattern_name)
                if pattern_def:
                    for compatible in pattern_def.compatible_patterns:
                        if compatible not in pattern_names:
                            # Check if we should have detected it
                            if compatible in self.pattern_models:
                                warnings.append(
                                    f"Expected pattern {compatible} not detected "
                                    f"(usually appears with {prediction.pattern_name})"
                                )
        
        return warnings
    
    def _generate_recommendations(self, 
                                predictions: List[PatternPrediction]) -> List[str]:
        """Generate strategic recommendations based on patterns"""
        recommendations = []
        
        # Get primary patterns
        primary_patterns = [p for p in predictions if p.confidence >= 0.7]
        
        if not primary_patterns:
            recommendations.append(
                "No clear pattern detected - consider focusing on establishing "
                "a clearer strategic direction"
            )
            return recommendations
        
        # Pattern-specific recommendations
        for prediction in primary_patterns[:3]:  # Top 3 patterns
            pattern = PATTERN_LOOKUP.get(prediction.pattern_name)
            if pattern and pattern.strategic_recommendations:
                for rec in pattern.strategic_recommendations[:2]:  # Top 2 recommendations
                    recommendations.append(f"[{pattern.name}] {rec}")
        
        # Evolution recommendations
        for prediction in primary_patterns[:2]:
            pattern = PATTERN_LOOKUP.get(prediction.pattern_name)
            if pattern and pattern.evolution_paths:
                evolution = pattern.evolution_paths[0]
                recommendations.append(
                    f"Consider evolving from {pattern.name} → {evolution}"
                )
        
        # Conflict resolutions
        conflicts = self._check_pattern_conflicts(predictions)
        if conflicts:
            recommendations.append(
                "Resolve pattern conflicts to improve focus and execution"
            )
        
        return recommendations[:5]  # Limit to 5 recommendations
    
    def save_models(self):
        """Save all trained models"""
        logger.info(f"Saving models to {self.model_dir}")
        
        # Save scalers
        joblib.dump(self.scalers, self.model_dir / 'scalers.pkl')
        
        # Save master category models
        joblib.dump(self.master_category_models, 
                   self.model_dir / 'master_category_models.pkl')
        
        # Save pattern models
        joblib.dump(self.pattern_models, self.model_dir / 'pattern_models.pkl')
        
        # Save configuration
        config = {
            'all_features': self.all_features,
            'feature_groups': self.feature_groups,
            'pattern_groups': {k.value: v for k, v in self.pattern_groups.items()}
        }
        joblib.dump(config, self.model_dir / 'config.pkl')
        
        logger.info("Models saved successfully")
    
    def load_models(self):
        """Load pre-trained models"""
        logger.info(f"Loading models from {self.model_dir}")
        
        try:
            # Load configuration
            config = joblib.load(self.model_dir / 'config.pkl')
            self.all_features = config['all_features']
            self.feature_groups = config['feature_groups']
            
            # Load models
            self.scalers = joblib.load(self.model_dir / 'scalers.pkl')
            self.master_category_models = joblib.load(
                self.model_dir / 'master_category_models.pkl'
            )
            self.pattern_models = joblib.load(self.model_dir / 'pattern_models.pkl')
            
            self.is_trained = True
            logger.info("Models loaded successfully")
            
        except Exception as e:
            logger.error(f"Error loading models: {e}")
            raise
    
    def evaluate(self, df: pd.DataFrame) -> Dict[str, float]:
        """Evaluate classifier performance"""
        results = {}
        
        # Master category performance
        for category_name, model in self.master_category_models.items():
            if f'category_{category_name}' in df.columns:
                X_scaled = self.scalers[category_name].transform(df[self.all_features])
                y_true = df[f'category_{category_name}']
                y_scores = model.predict_proba(X_scaled)[:, 1]
                
                auc = roc_auc_score(y_true, y_scores)
                results[f'category_{category_name}_auc'] = auc
        
        # Pattern performance
        for pattern_name, pattern_info in self.pattern_models.items():
            if f'pattern_{pattern_name}' in df.columns:
                features = pattern_info['features']
                X_scaled = self.scalers[pattern_name].transform(df[features])
                y_true = df[f'pattern_{pattern_name}']
                y_scores = pattern_info['model'].predict_proba(X_scaled)[:, 1]
                
                if y_true.sum() > 0:  # Need positive examples
                    auc = roc_auc_score(y_true, y_scores)
                    results[f'pattern_{pattern_name}_auc'] = auc
        
        # Overall metrics
        results['num_patterns_trained'] = len(self.pattern_models)
        results['num_categories_trained'] = len(self.master_category_models)
        results['avg_pattern_auc'] = np.mean([
            v for k, v in results.items() if k.startswith('pattern_') and k.endswith('_auc')
        ])
        
        return results


def train_hierarchical_classifier(data_path: str = 'data/final_100k_dataset_45features.csv'):
    """Train the hierarchical pattern classifier"""
    logger.info("Starting hierarchical classifier training")
    
    # Load data
    df = pd.read_csv(data_path)
    
    # Create pattern labels based on definitions
    logger.info("Creating pattern labels from definitions...")
    for pattern in ALL_PATTERNS:
        df[f'pattern_{pattern.name}'] = 0  # Initialize
        
        # Apply pattern conditions
        mask = pd.Series(True, index=df.index)
        
        # Required conditions
        for feature, condition in pattern.required_conditions.items():
            if feature in df.columns:
                mask &= df[feature].apply(condition)
        
        # Optional conditions (at least one)
        if pattern.optional_conditions:
            optional_mask = pd.Series(False, index=df.index)
            for feature, condition in pattern.optional_conditions.items():
                if feature in df.columns:
                    optional_mask |= df[feature].apply(condition)
            mask &= optional_mask
        
        # Exclusion conditions
        for feature, condition in pattern.exclusion_conditions.items():
            if feature in df.columns:
                mask &= ~df[feature].apply(condition)
        
        df[f'pattern_{pattern.name}'] = mask.astype(int)
        
        if mask.sum() > 0:
            logger.info(f"Pattern {pattern.name}: {mask.sum()} examples ({mask.mean():.1%})")
    
    # Create category labels
    for category in MasterCategory:
        category_mask = pd.Series(False, index=df.index)
        for pattern in ALL_PATTERNS:
            if pattern.master_category == category:
                category_mask |= (df[f'pattern_{pattern.name}'] == 1)
        df[f'category_{category.value}'] = category_mask.astype(int)
    
    # Initialize and train classifier
    classifier = HierarchicalPatternClassifier()
    
    # Split data
    train_df, test_df = train_test_split(df, test_size=0.2, random_state=42)
    
    # Train
    classifier.train(train_df, save_models=True)
    
    # Evaluate
    logger.info("Evaluating classifier performance...")
    results = classifier.evaluate(test_df)
    
    logger.info("Evaluation Results:")
    for metric, value in sorted(results.items()):
        logger.info(f"  {metric}: {value:.3f}")
    
    return classifier


if __name__ == "__main__":
    # Train the classifier
    classifier = train_hierarchical_classifier()
    
    # Test prediction
    test_startup = {
        'revenue_growth_rate_percent': 250,
        'user_growth_rate_percent': 300,
        'gross_margin_percent': 85,
        'ltv_cac_ratio': 4.5,
        'tech_differentiation_score': 4,
        'has_data_moat': 1,
        'network_effects_present': 0,
        'team_size_full_time': 45,
        'total_capital_raised_usd': 15000000,
        'burn_multiple': 3.5,
        'customer_count': 150,
        'net_dollar_retention_percent': 125,
        'annual_revenue_run_rate': 5000000,
        'product_retention_30d': 0.75,
        'dau_mau_ratio': 0.6,
        'patent_count': 2,
        'scalability_score': 4,
        'customer_concentration_percent': 15,
        'runway_months': 18,
        'has_debt': 0,
        'regulatory_advantage_present': 0,
        'investor_tier_primary': 2,
        'prior_successful_exits_count': 1,
        'years_experience_avg': 12,
        'domain_expertise_years_avg': 8,
        'board_advisor_experience_score': 4
    }
    
    profile = classifier.predict(test_startup)
    
    print("\nTest Startup Pattern Profile:")
    print(f"Primary Patterns: {[p.pattern_name for p in profile.primary_patterns]}")
    print(f"Master Categories: {profile.master_categories}")
    print(f"Warnings: {profile.warnings}")
    print(f"Recommendations: {profile.recommendations}")