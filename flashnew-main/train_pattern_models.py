#!/usr/bin/env python3
"""
Week 3: Train Pattern-Specific Models
Complete training pipeline for pattern-based prediction system
"""

import pandas as pd
import numpy as np
from pathlib import Path
import logging
import time
import json
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import roc_auc_score, precision_recall_fscore_support
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
import xgboost as xgb
from catboost import CatBoostClassifier
import joblib
import warnings
warnings.filterwarnings('ignore')

# Import pattern system
from ml_core.models.pattern_matcher_v2 import PatternMatcherV2
from ml_core.models.pattern_definitions import STARTUP_PATTERN_LIBRARY
from models.unified_orchestrator_v2 import UnifiedModelOrchestratorV2, EnhancedOrchestratorConfig

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class PatternModelTrainer:
    """Trains models for each discovered pattern"""
    
    def __init__(self, min_samples_per_pattern: int = 500):
        self.min_samples = min_samples_per_pattern
        self.pattern_matcher = PatternMatcherV2()
        self.pattern_models = {}
        self.pattern_stats = {}
        self.training_results = {}
        
    def load_data(self, data_path: str = "data/final_100k_dataset_45features.csv"):
        """Load training data"""
        logger.info(f"Loading data from {data_path}")
        self.df = pd.read_csv(data_path)
        
        # Separate features and target
        self.target_col = 'success'
        self.feature_cols = [col for col in self.df.columns if col not in [self.target_col, 'startup_id', 'startup_name']]
        
        self.X = self.df[self.feature_cols]
        self.y = self.df[self.target_col].values
        
        logger.info(f"Loaded {len(self.df)} samples with {len(self.feature_cols)} features")
        
        # Calculate CAMP scores
        self._calculate_camp_scores()
        
    def _calculate_camp_scores(self):
        """Calculate CAMP scores for all data"""
        logger.info("Calculating CAMP scores...")
        
        # Import the actual CAMP calculation logic
        from analyze_pattern_distribution import PatternDistributionAnalyzer
        
        analyzer = PatternDistributionAnalyzer()
        analyzer.df = self.df
        analyzer.calculate_camp_scores()
        
        self.camp_scores = analyzer.camp_scores
        logger.info("CAMP scores calculated")
        
    def assign_patterns(self):
        """Assign patterns to all training samples"""
        logger.info("Assigning patterns to training data...")
        
        # First train the pattern matcher
        self.pattern_matcher.train(self.X, self.y, self.camp_scores)
        
        # Assign patterns
        self.pattern_assignments = []
        self.pattern_details = []
        
        for i in range(len(self.X)):
            if i % 1000 == 0:
                logger.info(f"Processing sample {i}/{len(self.X)}")
            
            # Get CAMP scores for this sample
            camp_dict = {
                'capital_score': self.camp_scores.iloc[i]['capital_score'],
                'advantage_score': self.camp_scores.iloc[i]['advantage_score'],
                'market_score': self.camp_scores.iloc[i]['market_score'],
                'people_score': self.camp_scores.iloc[i]['people_score']
            }
            
            # Match pattern
            analysis = self.pattern_matcher.match_patterns(
                self.X.iloc[i:i+1],
                camp_dict,
                top_k=3
            )
            
            self.pattern_assignments.append(analysis.primary_pattern.pattern_name)
            self.pattern_details.append({
                'primary': analysis.primary_pattern.pattern_name,
                'confidence': analysis.primary_pattern.confidence,
                'secondary': [p.pattern_name for p in analysis.secondary_patterns],
                'tags': list(analysis.tags)
            })
        
        # Calculate pattern distribution
        from collections import Counter
        pattern_counts = Counter(self.pattern_assignments)
        
        logger.info("\nPattern Distribution:")
        for pattern, count in pattern_counts.most_common():
            pct = count / len(self.X) * 100
            logger.info(f"  {pattern}: {count} ({pct:.1f}%)")
        
        self.pattern_distribution = dict(pattern_counts)
        
    def train_pattern_models(self):
        """Train a model for each pattern with sufficient data"""
        logger.info("\nTraining pattern-specific models...")
        
        # Create output directory
        model_dir = Path('models/pattern_models')
        model_dir.mkdir(parents=True, exist_ok=True)
        
        # Group indices by pattern
        pattern_indices = {}
        for i, pattern in enumerate(self.pattern_assignments):
            if pattern not in pattern_indices:
                pattern_indices[pattern] = []
            pattern_indices[pattern].append(i)
        
        # Train model for each pattern
        for pattern_name, indices in pattern_indices.items():
            if len(indices) < self.min_samples:
                logger.warning(f"Skipping {pattern_name}: only {len(indices)} samples")
                continue
            
            logger.info(f"\nTraining model for {pattern_name} ({len(indices)} samples)...")
            
            # Extract pattern data
            X_pattern = self.X.iloc[indices]
            y_pattern = self.y[indices]
            
            # Split for validation
            X_train, X_val, y_train, y_val = train_test_split(
                X_pattern, y_pattern, test_size=0.2, random_state=42, stratify=y_pattern
            )
            
            # Choose model based on sample size
            model = self._select_model(len(indices))
            
            # Train model
            start_time = time.time()
            model.fit(X_train, y_train)
            train_time = time.time() - start_time
            
            # Evaluate
            y_pred_proba = model.predict_proba(X_val)[:, 1]
            auc = roc_auc_score(y_val, y_pred_proba)
            
            y_pred = (y_pred_proba >= 0.5).astype(int)
            precision, recall, f1, _ = precision_recall_fscore_support(
                y_val, y_pred, average='binary'
            )
            
            # Cross-validation score
            cv_scores = cross_val_score(model, X_pattern, y_pattern, cv=5, scoring='roc_auc')
            cv_mean = cv_scores.mean()
            cv_std = cv_scores.std()
            
            # Store results
            self.pattern_models[pattern_name] = model
            self.pattern_stats[pattern_name] = {
                'sample_count': len(indices),
                'success_rate': float(y_pattern.mean()),
                'train_samples': len(X_train),
                'val_samples': len(X_val),
                'auc': float(auc),
                'precision': float(precision),
                'recall': float(recall),
                'f1': float(f1),
                'cv_auc_mean': float(cv_mean),
                'cv_auc_std': float(cv_std),
                'training_time': train_time,
                'model_type': type(model).__name__
            }
            
            # Save model
            model_path = model_dir / f"{pattern_name}_model.pkl"
            joblib.dump(model, model_path)
            
            logger.info(f"  AUC: {auc:.3f}, F1: {f1:.3f}, CV AUC: {cv_mean:.3f}±{cv_std:.3f}")
        
        logger.info(f"\nTrained models for {len(self.pattern_models)} patterns")
        
    def _select_model(self, n_samples: int):
        """Select appropriate model based on sample size"""
        if n_samples < 1000:
            # Random Forest for small samples
            return RandomForestClassifier(
                n_estimators=100,
                max_depth=6,
                min_samples_split=20,
                random_state=42,
                n_jobs=-1
            )
        elif n_samples < 5000:
            # XGBoost for medium samples
            return xgb.XGBClassifier(
                n_estimators=200,
                max_depth=6,
                learning_rate=0.1,
                subsample=0.8,
                colsample_bytree=0.8,
                random_state=42,
                use_label_encoder=False,
                eval_metric='logloss'
            )
        else:
            # CatBoost for large samples
            return CatBoostClassifier(
                iterations=300,
                depth=8,
                learning_rate=0.05,
                random_seed=42,
                verbose=False
            )
    
    def analyze_pattern_features(self):
        """Analyze which features are important for each pattern"""
        logger.info("\nAnalyzing feature importance by pattern...")
        
        feature_importance_dir = Path('models/pattern_features')
        feature_importance_dir.mkdir(parents=True, exist_ok=True)
        
        self.pattern_features = {}
        
        for pattern_name, model in self.pattern_models.items():
            # Get feature importance
            if hasattr(model, 'feature_importances_'):
                importances = model.feature_importances_
            elif hasattr(model, 'feature_importance'):
                importances = model.feature_importance()
            else:
                continue
            
            # Get top features
            feature_importance = pd.DataFrame({
                'feature': self.feature_cols,
                'importance': importances
            }).sort_values('importance', ascending=False)
            
            # Save top 20 features
            top_features = feature_importance.head(20)
            self.pattern_features[pattern_name] = top_features.to_dict('records')
            
            # Save to file
            feature_path = feature_importance_dir / f"{pattern_name}_features.csv"
            top_features.to_csv(feature_path, index=False)
            
            logger.info(f"\n{pattern_name} top features:")
            for _, row in top_features.head(5).iterrows():
                logger.info(f"  {row['feature']}: {row['importance']:.3f}")
    
    def create_pattern_profiles(self):
        """Create detailed profiles for each pattern"""
        logger.info("\nCreating pattern profiles...")
        
        profiles = {}
        
        for pattern_name in self.pattern_models.keys():
            indices = [i for i, p in enumerate(self.pattern_assignments) 
                      if p == pattern_name]
            
            # Get pattern data
            X_pattern = self.X.iloc[indices]
            y_pattern = self.y[indices]
            camp_pattern = self.camp_scores.iloc[indices]
            
            # Calculate profile
            profile = {
                'pattern_name': pattern_name,
                'sample_count': len(indices),
                'success_rate': float(y_pattern.mean()),
                
                # CAMP profile
                'camp_means': {
                    'capital': float(camp_pattern['capital_score'].mean()),
                    'advantage': float(camp_pattern['advantage_score'].mean()),
                    'market': float(camp_pattern['market_score'].mean()),
                    'people': float(camp_pattern['people_score'].mean())
                },
                'camp_stds': {
                    'capital': float(camp_pattern['capital_score'].std()),
                    'advantage': float(camp_pattern['advantage_score'].std()),
                    'market': float(camp_pattern['market_score'].std()),
                    'people': float(camp_pattern['people_score'].std())
                },
                
                # Key metrics
                'key_metrics': {}
            }
            
            # Add key metric statistics
            key_metrics = [
                'revenue_growth_rate_percent',
                'burn_multiple',
                'net_dollar_retention_percent',
                'product_retention_30d',
                'ltv_cac_ratio'
            ]
            
            for metric in key_metrics:
                if metric in X_pattern.columns:
                    profile['key_metrics'][metric] = {
                        'mean': float(X_pattern[metric].mean()),
                        'median': float(X_pattern[metric].median()),
                        'p25': float(X_pattern[metric].quantile(0.25)),
                        'p75': float(X_pattern[metric].quantile(0.75))
                    }
            
            # Add model performance
            if pattern_name in self.pattern_stats:
                profile['model_performance'] = self.pattern_stats[pattern_name]
            
            # Add top features
            if pattern_name in self.pattern_features:
                profile['top_features'] = self.pattern_features[pattern_name][:10]
            
            profiles[pattern_name] = profile
        
        # Save profiles
        profiles_path = Path('models/pattern_profiles_detailed.json')
        with open(profiles_path, 'w') as f:
            json.dump(profiles, f, indent=2)
        
        logger.info(f"Created profiles for {len(profiles)} patterns")
        
        return profiles
    
    def train_enhanced_orchestrator(self):
        """Train the enhanced orchestrator with pattern support"""
        logger.info("\nTraining enhanced orchestrator...")
        
        # Create enhanced config
        config = EnhancedOrchestratorConfig(
            enable_patterns=True,
            pattern_weight=0.3,
            use_pattern_insights=True,
            pattern_success_modifier=True
        )
        
        # Initialize orchestrator
        orchestrator = UnifiedModelOrchestratorV2(config=config)
        
        # Load base models
        orchestrator.load_models()
        
        # Train pattern models
        orchestrator.train_pattern_models(self.X, self.y)
        
        # Save orchestrator config
        config_path = Path('models/orchestrator_config.json')
        with open(config_path, 'w') as f:
            json.dump({
                'enable_patterns': config.enable_patterns,
                'pattern_weight': config.pattern_weight,
                'model_weights': config.model_weights
            }, f, indent=2)
        
        logger.info("Enhanced orchestrator training complete")
        
        return orchestrator
    
    def evaluate_pattern_system(self):
        """Evaluate the complete pattern-based system"""
        logger.info("\nEvaluating pattern system performance...")
        
        # Split data for final evaluation
        X_train, X_test, y_train, y_test = train_test_split(
            self.X, self.y, test_size=0.2, random_state=42, stratify=self.y
        )
        
        # Get pattern assignments for test set
        test_patterns = []
        test_confidences = []
        
        for i in range(len(X_test)):
            idx = X_test.index[i]
            camp_dict = {
                'capital_score': self.camp_scores.loc[idx, 'capital_score'],
                'advantage_score': self.camp_scores.loc[idx, 'advantage_score'],
                'market_score': self.camp_scores.loc[idx, 'market_score'],
                'people_score': self.camp_scores.loc[idx, 'people_score']
            }
            
            analysis = self.pattern_matcher.match_patterns(
                X_test.iloc[i:i+1],
                camp_dict
            )
            
            test_patterns.append(analysis.primary_pattern.pattern_name)
            test_confidences.append(analysis.primary_pattern.confidence)
        
        # Evaluate pattern-specific predictions
        y_pred_proba = np.zeros(len(X_test))
        
        for i, (pattern, confidence) in enumerate(zip(test_patterns, test_confidences)):
            if pattern in self.pattern_models:
                # Use pattern-specific model
                model = self.pattern_models[pattern]
                prob = model.predict_proba(X_test.iloc[i:i+1])[0, 1]
            else:
                # Use pattern base rate
                if pattern in self.pattern_stats:
                    prob = self.pattern_stats[pattern]['success_rate']
                else:
                    prob = 0.5
            
            # Adjust by confidence
            y_pred_proba[i] = prob * confidence + 0.5 * (1 - confidence)
        
        # Calculate metrics
        auc = roc_auc_score(y_test, y_pred_proba)
        
        # Compare with baseline (no patterns)
        baseline_model = GradientBoostingClassifier(n_estimators=100, random_state=42)
        baseline_model.fit(X_train, y_train)
        baseline_proba = baseline_model.predict_proba(X_test)[:, 1]
        baseline_auc = roc_auc_score(y_test, baseline_proba)
        
        improvement = (auc - baseline_auc) / baseline_auc * 100
        
        logger.info(f"\nSystem Performance:")
        logger.info(f"  Pattern-based AUC: {auc:.4f}")
        logger.info(f"  Baseline AUC: {baseline_auc:.4f}")
        logger.info(f"  Improvement: {improvement:.1f}%")
        
        # Save evaluation results
        evaluation = {
            'test_samples': len(X_test),
            'pattern_auc': float(auc),
            'baseline_auc': float(baseline_auc),
            'improvement_percent': float(improvement),
            'pattern_distribution_test': dict(Counter(test_patterns)),
            'average_confidence': float(np.mean(test_confidences))
        }
        
        eval_path = Path('models/pattern_evaluation.json')
        with open(eval_path, 'w') as f:
            json.dump(evaluation, f, indent=2)
        
        return evaluation
    
    def save_training_summary(self):
        """Save comprehensive training summary"""
        summary = {
            'training_date': time.strftime('%Y-%m-%d %H:%M:%S'),
            'total_samples': len(self.X),
            'feature_count': len(self.feature_cols),
            'patterns_discovered': len(self.pattern_distribution),
            'patterns_with_models': len(self.pattern_models),
            'pattern_distribution': self.pattern_distribution,
            'model_performance': self.pattern_stats,
            'overall_metrics': {
                'average_pattern_auc': np.mean([
                    stats['auc'] for stats in self.pattern_stats.values()
                ]),
                'average_pattern_f1': np.mean([
                    stats['f1'] for stats in self.pattern_stats.values()
                ])
            }
        }
        
        summary_path = Path('models/pattern_training_summary.json')
        with open(summary_path, 'w') as f:
            json.dump(summary, f, indent=2)
        
        logger.info(f"\nTraining summary saved to {summary_path}")

def main():
    """Run complete pattern model training"""
    logger.info("="*80)
    logger.info("Starting Pattern Model Training Pipeline")
    logger.info("="*80)
    
    # Initialize trainer
    trainer = PatternModelTrainer(min_samples_per_pattern=500)
    
    # Step 1: Load data
    trainer.load_data()
    
    # Step 2: Assign patterns
    trainer.assign_patterns()
    
    # Step 3: Train pattern models
    trainer.train_pattern_models()
    
    # Step 4: Analyze features
    trainer.analyze_pattern_features()
    
    # Step 5: Create profiles
    trainer.create_pattern_profiles()
    
    # Step 6: Train enhanced orchestrator
    trainer.train_enhanced_orchestrator()
    
    # Step 7: Evaluate system
    evaluation = trainer.evaluate_pattern_system()
    
    # Step 8: Save summary
    trainer.save_training_summary()
    
    logger.info("\n" + "="*80)
    logger.info("Pattern Model Training Complete!")
    logger.info(f"Trained models for {len(trainer.pattern_models)} patterns")
    logger.info(f"System AUC: {evaluation['pattern_auc']:.4f}")
    logger.info(f"Improvement over baseline: {evaluation['improvement_percent']:.1f}%")
    logger.info("="*80)

if __name__ == "__main__":
    main()