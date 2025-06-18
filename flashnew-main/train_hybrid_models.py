#!/usr/bin/env python3
"""
Train Pattern Models with Contracts for the Hybrid System
This script trains pattern-specific models to complement the base contractual models
"""

import os
import sys
import logging
import pandas as pd
import numpy as np
from datetime import datetime
import json
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score
import xgboost as xgb
from catboost import CatBoostClassifier
import lightgbm as lgb
from sklearn.ensemble import RandomForestClassifier

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.feature_registry import feature_registry
from core.pattern_contracts import PatternContractFactory
from core.enhanced_contracts import PatternType
from core.feature_pipeline import UnifiedFeaturePipeline
from core.model_wrapper import ContractualModel, ModelMetadata
from core.feature_mapping import map_dataset_to_registry

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class PatternModelTrainer:
    """Train pattern-specific models with contracts"""
    
    def __init__(self, 
                 data_path: str = "data/final_100k_dataset_45features.csv",
                 output_dir: str = "models/hybrid_patterns"):
        self.data_path = data_path
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize components
        self.registry = feature_registry
        self.pattern_factory = PatternContractFactory()
        self.pipeline = None
        
        # Training results
        self.results = {
            'timestamp': datetime.now().isoformat(),
            'patterns_trained': [],
            'performance': {},
            'errors': []
        }
    
    def load_and_prepare_data(self):
        """Load and prepare training data"""
        logger.info("Loading training data...")
        
        # Load data
        df = pd.read_csv(self.data_path)
        logger.info(f"Loaded {len(df)} samples")
        
        # Map to registry features
        X = map_dataset_to_registry(df)
        
        # Get target
        if 'success' in df.columns:
            y = df['success']
        elif 'success_label' in df.columns:
            y = df['success_label']
        else:
            raise ValueError("No target column found")
        
        # Create and fit pipeline
        self.pipeline = UnifiedFeaturePipeline(self.registry)
        self.pipeline.fit(X)
        
        # Save pipeline
        pipeline_path = self.output_dir / "pattern_pipeline.pkl"
        self.pipeline.save(str(pipeline_path))
        logger.info(f"Saved pipeline to {pipeline_path}")
        
        return X, y
    
    def detect_pattern_labels(self, X: pd.DataFrame) -> pd.DataFrame:
        """Detect which patterns each startup belongs to"""
        logger.info("Detecting pattern labels for training data...")
        
        pattern_labels = pd.DataFrame(index=X.index)
        
        # Growth patterns
        pattern_labels['efficient_growth'] = (
            (X['revenue_growth_rate'] > 100) & 
            (X['burn_multiple'] < 1.5) &
            (X['runway_months'] > 18)
        ).astype(int)
        
        pattern_labels['high_burn_growth'] = (
            (X['revenue_growth_rate'] > 200) & 
            (X['burn_multiple'] > 2.5) &
            (X['total_capital_raised_usd'] > 5000000)
        ).astype(int)
        
        pattern_labels['bootstrap_profitable'] = (
            (X['burn_multiple'] < 1.0) & 
            (X['total_capital_raised_usd'] < 1000000) &
            (X['runway_months'] > 24)
        ).astype(int)
        
        # Business model patterns
        pattern_labels['b2b_saas'] = (
            (X['net_revenue_retention'] > 110) & 
            (X['target_enterprise'] == True) &
            (X['annual_recurring_revenue_millions'] > 1)
        ).astype(int)
        
        pattern_labels['ai_ml_core'] = (
            (X['uses_ai_ml'] == True) & 
            (X['research_development_percent'] > 20) &
            (X['technical_founder'] == True)
        ).astype(int)
        
        pattern_labels['platform_network'] = (
            (X['platform_business'] == True) & 
            (X['customer_growth_rate'] > 100)
        ).astype(int)
        
        # More patterns...
        pattern_labels['vc_hypergrowth'] = (
            (X['total_capital_raised_usd'] > 10000000) & 
            (X['revenue_growth_rate'] > 200) &
            (X['team_size_full_time'] > 30)
        ).astype(int)
        
        # Log pattern distribution
        pattern_counts = pattern_labels.sum()
        logger.info("Pattern distribution:")
        for pattern, count in pattern_counts.items():
            logger.info(f"  {pattern}: {count} ({count/len(X)*100:.1f}%)")
        
        return pattern_labels
    
    def train_pattern_model(self,
                          X: pd.DataFrame,
                          y: pd.Series,
                          pattern_name: str,
                          pattern_labels: pd.Series) -> ContractualModel:
        """Train a model for a specific pattern"""
        logger.info(f"\nTraining model for pattern: {pattern_name}")
        
        # Get pattern type
        pattern_type = PatternType(pattern_name)
        
        # Create contract
        contract = self.pattern_factory.create_pattern_contract(pattern_type)
        
        # Filter to samples that match this pattern
        pattern_mask = pattern_labels > 0
        if pattern_mask.sum() < 100:
            logger.warning(f"Only {pattern_mask.sum()} samples for {pattern_name}, skipping")
            return None
        
        # Use stratified sampling to include both pattern and non-pattern samples
        # This helps the model learn what distinguishes this pattern
        n_pattern = pattern_mask.sum()
        n_non_pattern = min(n_pattern * 2, (~pattern_mask).sum())  # 2:1 ratio
        
        pattern_indices = pattern_mask[pattern_mask].index
        non_pattern_indices = pattern_mask[~pattern_mask].sample(n_non_pattern).index
        
        train_indices = pattern_indices.union(non_pattern_indices)
        X_train = X.loc[train_indices]
        y_train = y.loc[train_indices]
        
        logger.info(f"Training set: {len(X_train)} samples ({n_pattern} pattern, {n_non_pattern} non-pattern)")
        
        # Split for validation
        X_tr, X_val, y_tr, y_val = train_test_split(
            X_train, y_train, test_size=0.2, random_state=42, stratify=y_train
        )
        
        # Transform features according to contract
        X_tr_transformed = self.pipeline.transform(X_tr, contract)
        X_val_transformed = self.pipeline.transform(X_val, contract)
        
        # Choose model based on pattern characteristics
        if pattern_name in ['efficient_growth', 'bootstrap_profitable']:
            # These patterns benefit from tree-based models
            model = xgb.XGBClassifier(
                n_estimators=100,
                max_depth=6,
                learning_rate=0.1,
                objective='binary:logistic',
                use_label_encoder=False,
                eval_metric='auc',
                random_state=42
            )
        elif pattern_name in ['ai_ml_core', 'deep_tech_rd']:
            # Technical patterns might benefit from CatBoost
            model = CatBoostClassifier(
                iterations=100,
                depth=6,
                learning_rate=0.1,
                loss_function='Logloss',
                eval_metric='AUC',
                random_state=42,
                verbose=False
            )
        else:
            # Default to LightGBM for efficiency
            model = lgb.LGBMClassifier(
                n_estimators=100,
                max_depth=6,
                learning_rate=0.1,
                objective='binary',
                metric='auc',
                random_state=42,
                verbosity=-1
            )
        
        # Train model
        model.fit(X_tr_transformed, y_tr)
        
        # Evaluate
        train_pred = model.predict_proba(X_tr_transformed)[:, 1]
        val_pred = model.predict_proba(X_val_transformed)[:, 1]
        
        train_auc = roc_auc_score(y_tr, train_pred)
        val_auc = roc_auc_score(y_val, val_pred)
        
        logger.info(f"Performance - Train AUC: {train_auc:.4f}, Val AUC: {val_auc:.4f}")
        
        # Create metadata
        metadata = ModelMetadata(
            model_name=f"pattern_{pattern_name}",
            model_version="1.0.0",
            training_date=datetime.now(),
            training_dataset=self.data_path,
            performance_metrics={
                'train_auc': train_auc,
                'val_auc': val_auc,
                'pattern_samples': int(n_pattern),
                'total_samples': len(X_train)
            }
        )
        
        # Wrap in contractual model
        contractual_model = ContractualModel(
            model=model,
            contract=contract,
            feature_pipeline=self.pipeline,
            metadata=metadata
        )
        
        # Store results
        self.results['patterns_trained'].append(pattern_name)
        self.results['performance'][pattern_name] = {
            'train_auc': train_auc,
            'val_auc': val_auc,
            'samples': int(n_pattern)
        }
        
        return contractual_model
    
    def train_top_patterns(self, n_patterns: int = 10):
        """Train models for the top N patterns"""
        logger.info("="*60)
        logger.info("Training Pattern Models for Hybrid System")
        logger.info("="*60)
        
        # Load data
        X, y = self.load_and_prepare_data()
        
        # Detect pattern labels
        pattern_labels = self.detect_pattern_labels(X)
        
        # Sort patterns by frequency
        pattern_counts = pattern_labels.sum().sort_values(ascending=False)
        top_patterns = pattern_counts.head(n_patterns).index.tolist()
        
        logger.info(f"\nTraining top {n_patterns} patterns:")
        for i, pattern in enumerate(top_patterns):
            logger.info(f"{i+1}. {pattern}: {pattern_counts[pattern]} samples")
        
        # Train models for each pattern
        trained_models = {}
        
        for pattern_name in top_patterns:
            try:
                model = self.train_pattern_model(
                    X, y, 
                    pattern_name, 
                    pattern_labels[pattern_name]
                )
                
                if model:
                    # Save model
                    model_path = self.output_dir / f"pattern_{pattern_name}.pkl"
                    model.save(str(model_path))
                    logger.info(f"Saved {pattern_name} model to {model_path}")
                    
                    trained_models[pattern_name] = model
                    
            except Exception as e:
                logger.error(f"Failed to train {pattern_name}: {e}")
                self.results['errors'].append({
                    'pattern': pattern_name,
                    'error': str(e)
                })
        
        # Save results
        results_path = self.output_dir / "pattern_training_results.json"
        with open(results_path, 'w') as f:
            json.dump(self.results, f, indent=2)
        
        logger.info(f"\nTraining complete!")
        logger.info(f"Trained {len(trained_models)} pattern models")
        logger.info(f"Results saved to {results_path}")
        
        # Display performance summary
        self._display_performance_summary()
        
        return trained_models
    
    def _display_performance_summary(self):
        """Display performance summary"""
        logger.info("\nPerformance Summary:")
        logger.info("-" * 50)
        
        if self.results['performance']:
            # Calculate average performance
            val_aucs = [p['val_auc'] for p in self.results['performance'].values()]
            avg_auc = np.mean(val_aucs)
            
            logger.info(f"Average Validation AUC: {avg_auc:.4f}")
            logger.info("\nPattern Performance:")
            
            # Sort by validation AUC
            sorted_patterns = sorted(
                self.results['performance'].items(),
                key=lambda x: x[1]['val_auc'],
                reverse=True
            )
            
            for pattern, metrics in sorted_patterns:
                logger.info(f"  {pattern:25s}: {metrics['val_auc']:.4f} AUC ({metrics['samples']:,} samples)")


def test_hybrid_prediction():
    """Test the hybrid system with pattern models"""
    logger.info("\n" + "="*60)
    logger.info("Testing Hybrid Prediction System")
    logger.info("="*60)
    
    from core.model_wrapper import ContractualModel
    from core.hybrid_orchestrator import HybridOrchestrator
    
    # Load base models
    base_models = {}
    base_model_dir = Path("models/contractual")
    
    for model_name in ['dna_analyzer', 'temporal_model', 'industry_model', 'ensemble_model']:
        model_path = base_model_dir / f"{model_name}.pkl"
        if model_path.exists():
            model = ContractualModel.load(str(model_path), feature_registry)
            base_models[model_name] = model
            logger.info(f"Loaded base model: {model_name}")
    
    # Load pattern models
    pattern_models = {}
    pattern_model_dir = Path("models/hybrid_patterns")
    
    if pattern_model_dir.exists():
        for model_file in pattern_model_dir.glob("pattern_*.pkl"):
            pattern_name = model_file.stem.replace("pattern_", "")
            model = ContractualModel.load(str(model_file), feature_registry)
            pattern_models[pattern_name] = model
            logger.info(f"Loaded pattern model: {pattern_name}")
    
    # Create hybrid orchestrator
    orchestrator = HybridOrchestrator(
        base_models=base_models,
        pattern_models=pattern_models,
        use_patterns=True,
        use_stage_specific=True,
        use_industry_specific=True
    )
    
    # Test with sample data
    test_startup = {
        'funding_stage': 'series_a',
        'revenue_growth_rate': 200.0,
        'team_size_full_time': 25,
        'total_capital_raised_usd': 5000000.0,
        'annual_recurring_revenue_millions': 2.0,
        'annual_revenue_run_rate': 2000000.0,
        'burn_multiple': 1.8,
        'market_tam_billions': 15.0,
        'market_growth_rate': 30.0,
        'market_competitiveness': 3,
        'customer_acquisition_cost': 500.0,
        'customer_lifetime_value': 5000.0,
        'customer_growth_rate': 150.0,
        'net_revenue_retention': 125.0,
        'average_deal_size': 10000.0,
        'sales_cycle_days': 45,
        'international_revenue_percent': 15.0,
        'target_enterprise': True,
        'product_market_fit_score': 4,
        'technology_score': 4,
        'scalability_score': 5,
        'has_patent': True,
        'research_development_percent': 25.0,
        'uses_ai_ml': True,
        'cloud_native': True,
        'mobile_first': False,
        'platform_business': True,
        'founder_experience_years': 15,
        'repeat_founder': True,
        'technical_founder': True,
        'employee_growth_rate': 100.0,
        'advisor_quality_score': 4,
        'board_diversity_score': 4,
        'team_industry_experience': 12,
        'key_person_dependency': 2,
        'top_university_alumni': True,
        'investor_tier_primary': 'tier_1',
        'active_investors': 5,
        'cash_on_hand_months': 20.0,
        'runway_months': 20.0,
        'time_to_next_funding': 12,
        'previous_exit': True,
        'industry_connections': 4,
        'media_coverage': 3,
        'regulatory_risk': 2
    }
    
    # Make prediction
    logger.info("\nMaking hybrid prediction...")
    result = orchestrator.predict(test_startup, return_diagnostics=True)
    
    # Display results
    logger.info("\nHybrid Prediction Results:")
    logger.info(f"Base Probability: {result.base_probability:.3f}")
    logger.info(f"Pattern-Adjusted: {result.pattern_adjusted_probability:.3f}")
    logger.info(f"Final Probability: {result.final_probability:.3f}")
    logger.info(f"Confidence: {result.confidence_score:.3f}")
    logger.info(f"Verdict: {result.verdict}")
    logger.info(f"Risk Level: {result.risk_level}")
    
    if result.dominant_pattern:
        logger.info(f"\nDominant Pattern: {result.dominant_pattern.value}")
        logger.info("Pattern Scores:")
        for pattern, score in result.pattern_scores.items():
            logger.info(f"  {pattern}: {score:.3f}")
    
    logger.info("\nKey Strengths:")
    for strength in result.key_strengths:
        logger.info(f"  - {strength}")
    
    logger.info("\nImprovement Areas:")
    for improvement in result.improvement_areas:
        logger.info(f"  - {improvement}")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Train pattern models for hybrid system")
    parser.add_argument('--data-path', default='data/final_100k_dataset_45features.csv',
                       help='Path to training data')
    parser.add_argument('--output-dir', default='models/hybrid_patterns',
                       help='Output directory for pattern models')
    parser.add_argument('--n-patterns', type=int, default=10,
                       help='Number of top patterns to train')
    parser.add_argument('--test', action='store_true',
                       help='Test the hybrid system after training')
    
    args = parser.parse_args()
    
    # Train pattern models
    trainer = PatternModelTrainer(
        data_path=args.data_path,
        output_dir=args.output_dir
    )
    
    trained_models = trainer.train_top_patterns(n_patterns=args.n_patterns)
    
    # Test if requested
    if args.test:
        test_hybrid_prediction()