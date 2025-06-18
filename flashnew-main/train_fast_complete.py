#!/usr/bin/env python3
"""
FAST Complete Model Training - Adjusted for time constraints
Trains full ensemble but with reduced iterations
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import roc_auc_score
import xgboost as xgb
import lightgbm as lgb
from catboost import CatBoostClassifier
import joblib
from pathlib import Path
import logging
import json
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Import our modules
from feature_engineering_v2_fixed import FeatureEngineerV2
from calibrated_orchestrator import CalibratedOrchestrator

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class FastCompleteTrainer:
    """Fast complete training - balanced for time"""
    
    def __init__(self, output_dir: str = "models/complete_v1"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.models = {}
        self.results = {}
        self.feature_engineer = FeatureEngineerV2()
        
    def prepare_data(self, df: pd.DataFrame):
        """Complete data preparation"""
        logger.info("Preparing data with feature engineering...")
        
        # Apply feature engineering
        df_engineered = self.feature_engineer.transform(df)
        
        # Separate features and target
        feature_cols = [col for col in df_engineered.columns if col not in [
            'startup_id', 'success', 'outcome_type', 'data_collection_date', 'outcome_date'
        ]]
        
        X = df_engineered[feature_cols]
        y = df_engineered['success']
        
        # Handle categorical features
        categorical_features = ['funding_stage', 'sector', 'product_stage', 'investor_tier_primary', 'risk_level']
        
        self.label_encoders = {}
        
        for col in categorical_features:
            if col in X.columns:
                from sklearn.preprocessing import LabelEncoder
                le = LabelEncoder()
                X[col] = X[col].astype(str).replace('nan', 'unknown')
                X[col] = le.fit_transform(X[col])
                self.label_encoders[col] = le
                
        # Fill NaN values
        numeric_columns = X.select_dtypes(include=[np.number]).columns
        X[numeric_columns] = X[numeric_columns].fillna(X[numeric_columns].median())
        
        logger.info(f"Prepared {len(X)} samples with {len(X.columns)} features")
        
        return X, y, feature_cols
    
    def train_fast_ensemble(self, X_train, y_train, X_val, y_val):
        """Train ensemble with reduced iterations"""
        logger.info("Training ensemble models (fast mode)...")
        
        # Calculate class weights
        n_pos = y_train.sum()
        n_neg = len(y_train) - n_pos
        scale_pos_weight = n_neg / n_pos
        
        # 1. XGBoost
        logger.info("Training XGBoost...")
        self.models['xgboost'] = xgb.XGBClassifier(
            n_estimators=100,
            max_depth=6,
            learning_rate=0.1,
            scale_pos_weight=scale_pos_weight,
            random_state=42,
            n_jobs=-1,
            eval_metric='auc'
        )
        
        self.models['xgboost'].fit(
            X_train, y_train,
            eval_set=[(X_val, y_val)],
            early_stopping_rounds=20,
            verbose=False
        )
        
        # 2. LightGBM
        logger.info("Training LightGBM...")
        self.models['lightgbm'] = lgb.LGBMClassifier(
            n_estimators=100,
            num_leaves=31,
            learning_rate=0.1,
            scale_pos_weight=scale_pos_weight,
            random_state=42,
            n_jobs=-1,
            verbosity=-1
        )
        
        self.models['lightgbm'].fit(
            X_train, y_train,
            eval_set=[(X_val, y_val)],
            callbacks=[lgb.early_stopping(20), lgb.log_evaluation(0)]
        )
        
        # 3. CatBoost
        logger.info("Training CatBoost...")
        self.models['catboost'] = CatBoostClassifier(
            iterations=100,
            depth=6,
            learning_rate=0.1,
            scale_pos_weight=scale_pos_weight,
            random_seed=42,
            verbose=False,
            early_stopping_rounds=20
        )
        
        self.models['catboost'].fit(
            X_train, y_train,
            eval_set=(X_val, y_val),
            use_best_model=True
        )
        
        # 4. Random Forest
        logger.info("Training Random Forest...")
        self.models['random_forest'] = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            class_weight='balanced',
            random_state=42,
            n_jobs=-1
        )
        self.models['random_forest'].fit(X_train, y_train)
        
        # 5. Gradient Boosting
        logger.info("Training Gradient Boosting...")
        self.models['gradient_boosting'] = GradientBoostingClassifier(
            n_estimators=100,
            max_depth=4,
            learning_rate=0.1,
            random_state=42,
            validation_fraction=0.2,
            n_iter_no_change=10
        )
        self.models['gradient_boosting'].fit(X_train, y_train)
        
        # Evaluate all models
        for name, model in self.models.items():
            y_pred_proba = model.predict_proba(X_val)[:, 1]
            auc = roc_auc_score(y_val, y_pred_proba)
            self.results[name] = {
                'auc': auc,
                'predictions': y_pred_proba
            }
            logger.info(f"{name} AUC: {auc:.4f}")
            
    def create_meta_learner(self, X_train, y_train, X_val, y_val):
        """Create meta-learner"""
        logger.info("Creating meta-learner...")
        
        # Get predictions from base models
        train_meta_features = []
        val_meta_features = []
        
        for name, model in self.models.items():
            train_pred = model.predict_proba(X_train)[:, 1]
            val_pred = model.predict_proba(X_val)[:, 1]
            
            train_meta_features.append(train_pred)
            val_meta_features.append(val_pred)
            
        # Stack predictions
        X_train_meta = np.column_stack(train_meta_features)
        X_val_meta = np.column_stack(val_meta_features)
        
        # Train meta-learner
        self.models['meta_learner'] = xgb.XGBClassifier(
            n_estimators=50,
            max_depth=3,
            learning_rate=0.1,
            random_state=42,
            n_jobs=-1
        )
        self.models['meta_learner'].fit(X_train_meta, y_train)
        
        # Evaluate
        y_pred_meta = self.models['meta_learner'].predict_proba(X_val_meta)[:, 1]
        meta_auc = roc_auc_score(y_val, y_pred_meta)
        
        self.results['meta_ensemble'] = {
            'auc': meta_auc,
            'predictions': y_pred_meta
        }
        
        logger.info(f"Meta-ensemble AUC: {meta_auc:.4f}")
        logger.info(f"Prediction range: {y_pred_meta.min():.3f} - {y_pred_meta.max():.3f}")
        
    def save_models(self, feature_names):
        """Save all models and metadata"""
        logger.info("Saving models...")
        
        # Save models
        for name, model in self.models.items():
            joblib.dump(model, self.output_dir / f'{name}.pkl')
            
        # Save feature engineer
        joblib.dump(self.feature_engineer, self.output_dir / 'feature_engineer.pkl')
        
        # Save label encoders
        joblib.dump(self.label_encoders, self.output_dir / 'label_encoders.pkl')
        
        # Save metadata
        metadata = {
            'training_date': datetime.now().isoformat(),
            'training_mode': 'FAST_COMPLETE',
            'feature_count': len(feature_names),
            'model_performance': {k: v['auc'] for k, v in self.results.items()},
            'feature_names': feature_names
        }
        
        with open(self.output_dir / 'metadata.json', 'w') as f:
            json.dump(metadata, f, indent=2)
            
        logger.info(f"Models saved to {self.output_dir}")


def main():
    """Main training pipeline"""
    print("\n" + "="*80)
    print("FAST COMPLETE MODEL TRAINING")
    print("="*80)
    
    # Load dataset
    print("\n1. Loading dataset...")
    df = pd.read_csv('data/realistic_startup_dataset_200k.csv')
    print(f"   Loaded {len(df):,} samples")
    
    # Initialize trainer
    trainer = FastCompleteTrainer()
    
    # Prepare data
    print("\n2. Preparing data...")
    X, y, feature_names = trainer.prepare_data(df)
    
    # Split data
    print("\n3. Splitting data...")
    X_temp, X_test, y_temp, y_test = train_test_split(
        X, y, test_size=0.15, random_state=42, stratify=y
    )
    
    X_train, X_val, y_train, y_val = train_test_split(
        X_temp, y_temp, test_size=0.176, random_state=42, stratify=y_temp
    )
    
    print(f"   Train: {len(X_train):,} samples")
    print(f"   Val: {len(X_val):,} samples")
    print(f"   Test: {len(X_test):,} samples")
    
    # Train ensemble
    print("\n4. Training ensemble...")
    trainer.train_fast_ensemble(X_train, y_train, X_val, y_val)
    
    # Create meta-learner
    print("\n5. Creating meta-learner...")
    trainer.create_meta_learner(X_train, y_train, X_val, y_val)
    
    # Test evaluation
    print("\n6. Final test evaluation...")
    test_meta_features = []
    for name, model in trainer.models.items():
        if name != 'meta_learner':
            test_pred = model.predict_proba(X_test)[:, 1]
            test_meta_features.append(test_pred)
            
    X_test_meta = np.column_stack(test_meta_features)
    y_test_pred = trainer.models['meta_learner'].predict_proba(X_test_meta)[:, 1]
    
    test_auc = roc_auc_score(y_test, y_test_pred)
    print(f"\n   FINAL TEST AUC: {test_auc:.4f}")
    print(f"   Prediction range: {y_test_pred.min():.3f} - {y_test_pred.max():.3f}")
    
    # Save models
    print("\n7. Saving models...")
    trainer.save_models(feature_names)
    
    print("\n" + "="*80)
    print("TRAINING COMPLETE!")
    print("="*80)
    print(f"Final accuracy: {test_auc:.1%}")
    print(f"Models saved to: {trainer.output_dir}/")
    print("="*80)


if __name__ == "__main__":
    main()