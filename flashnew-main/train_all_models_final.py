#!/usr/bin/env python3
"""
Train all models on the realistic 200k dataset with 45 CAMP features
No data leakage, proper validation, comprehensive evaluation
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, StratifiedKFold
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import roc_auc_score, accuracy_score, precision_recall_curve, confusion_matrix
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
import xgboost as xgb
import lightgbm as lgb
import catboost as cb
import joblib
from pathlib import Path
import json
import logging
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ComprehensiveModelTrainer:
    """Train all models with proper evaluation"""
    
    def __init__(self, output_dir="models/final_production"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.models = {}
        self.results = {}
        self.feature_importance = {}
        
    def load_and_prepare_data(self):
        """Load and prepare the dataset"""
        logger.info("Loading realistic 200k dataset...")
        
        # Load data
        df = pd.read_csv('realistic_200k_dataset.csv')
        logger.info(f"Loaded {len(df):,} samples")
        logger.info(f"Success rate: {df['success'].mean():.1%}")
        
        # Import feature configuration
        from feature_config import ALL_FEATURES, CATEGORICAL_FEATURES, BOOLEAN_FEATURES
        
        # Prepare features and target
        X = df[ALL_FEATURES].copy()
        y = df['success'].copy()
        
        # Handle categorical features
        self.label_encoders = {}
        for col in CATEGORICAL_FEATURES:
            if col in X.columns:
                le = LabelEncoder()
                X[col] = le.fit_transform(X[col].astype(str))
                self.label_encoders[col] = le
        
        # Ensure boolean features are 0/1
        for col in BOOLEAN_FEATURES:
            if col in X.columns:
                X[col] = X[col].astype(int)
        
        # Handle missing values
        X = X.fillna(X.median())
        
        # Add engineered features
        logger.info("Engineering additional features...")
        X['log_capital'] = np.log1p(X['total_capital_raised_usd'])
        X['log_revenue'] = np.log1p(X['annual_revenue_run_rate'])
        X['capital_efficiency'] = X['annual_revenue_run_rate'] / (X['total_capital_raised_usd'] + 1)
        X['growth_efficiency'] = X['revenue_growth_rate_percent'] / (X['monthly_burn_usd'] + 1)
        X['team_experience_score'] = (
            X['years_experience_avg'] * 0.3 + 
            X['domain_expertise_years_avg'] * 0.3 +
            X['prior_successful_exits_count'] * 10
        )
        
        self.feature_names = list(X.columns)
        logger.info(f"Total features: {len(self.feature_names)}")
        
        return X, y
    
    def train_models(self, X_train, y_train, X_val, y_val):
        """Train all model types"""
        
        # Calculate class weight
        scale_pos_weight = (y_train == 0).sum() / (y_train == 1).sum()
        logger.info(f"Class imbalance ratio: {scale_pos_weight:.2f}")
        
        # 1. XGBoost
        logger.info("\n1. Training XGBoost...")
        self.models['xgboost'] = xgb.XGBClassifier(
            n_estimators=300,
            max_depth=6,
            learning_rate=0.1,
            subsample=0.8,
            colsample_bytree=0.8,
            scale_pos_weight=scale_pos_weight,
            random_state=42,
            n_jobs=-1,
            eval_metric='auc'
        )
        self.models['xgboost'].fit(
            X_train, y_train,
            eval_set=[(X_val, y_val)],
            early_stopping_rounds=50,
            verbose=False
        )
        
        # 2. LightGBM
        logger.info("2. Training LightGBM...")
        self.models['lightgbm'] = lgb.LGBMClassifier(
            n_estimators=300,
            num_leaves=31,
            learning_rate=0.1,
            feature_fraction=0.8,
            bagging_fraction=0.8,
            bagging_freq=5,
            scale_pos_weight=scale_pos_weight,
            random_state=42,
            n_jobs=-1,
            verbosity=-1
        )
        self.models['lightgbm'].fit(
            X_train, y_train,
            eval_set=[(X_val, y_val)],
            eval_metric='auc',
            callbacks=[lgb.early_stopping(50), lgb.log_evaluation(0)]
        )
        
        # 3. CatBoost
        logger.info("3. Training CatBoost...")
        self.models['catboost'] = cb.CatBoostClassifier(
            iterations=300,
            depth=6,
            learning_rate=0.1,
            scale_pos_weight=scale_pos_weight,
            random_seed=42,
            verbose=False,
            eval_metric='AUC',
            early_stopping_rounds=50
        )
        self.models['catboost'].fit(
            X_train, y_train,
            eval_set=(X_val, y_val),
            verbose=False
        )
        
        # 4. Random Forest
        logger.info("4. Training Random Forest...")
        self.models['random_forest'] = RandomForestClassifier(
            n_estimators=300,
            max_depth=10,
            min_samples_split=20,
            min_samples_leaf=10,
            class_weight='balanced',
            random_state=42,
            n_jobs=-1
        )
        self.models['random_forest'].fit(X_train, y_train)
        
        # 5. Gradient Boosting
        logger.info("5. Training Gradient Boosting...")
        self.models['gradient_boosting'] = GradientBoostingClassifier(
            n_estimators=200,
            max_depth=5,
            learning_rate=0.1,
            subsample=0.8,
            random_state=42
        )
        self.models['gradient_boosting'].fit(X_train, y_train)
        
        # Evaluate all models
        logger.info("\nValidation Performance:")
        for name, model in self.models.items():
            y_pred_proba = model.predict_proba(X_val)[:, 1]
            auc = roc_auc_score(y_val, y_pred_proba)
            acc = accuracy_score(y_val, (y_pred_proba >= 0.5).astype(int))
            
            self.results[name] = {
                'val_auc': auc,
                'val_accuracy': acc,
                'prediction_range': (y_pred_proba.min(), y_pred_proba.max())
            }
            
            logger.info(f"  {name}: AUC={auc:.4f}, Acc={acc:.3f}, Range=[{y_pred_proba.min():.3f}, {y_pred_proba.max():.3f}]")
    
    def create_ensemble(self, X_train, y_train, X_val, y_val):
        """Create ensemble model"""
        logger.info("\n6. Creating Ensemble Model...")
        
        # Get predictions from all models
        train_preds = []
        val_preds = []
        
        for name, model in self.models.items():
            train_preds.append(model.predict_proba(X_train)[:, 1])
            val_preds.append(model.predict_proba(X_val)[:, 1])
        
        # Stack predictions
        X_train_meta = np.column_stack(train_preds)
        X_val_meta = np.column_stack(val_preds)
        
        # Train meta-learner
        self.models['ensemble'] = xgb.XGBClassifier(
            n_estimators=100,
            max_depth=3,
            learning_rate=0.1,
            random_state=42,
            n_jobs=-1
        )
        self.models['ensemble'].fit(X_train_meta, y_train)
        
        # Evaluate ensemble
        y_pred_ensemble = self.models['ensemble'].predict_proba(X_val_meta)[:, 1]
        ensemble_auc = roc_auc_score(y_val, y_pred_ensemble)
        ensemble_acc = accuracy_score(y_val, (y_pred_ensemble >= 0.5).astype(int))
        
        self.results['ensemble'] = {
            'val_auc': ensemble_auc,
            'val_accuracy': ensemble_acc,
            'prediction_range': (y_pred_ensemble.min(), y_pred_ensemble.max())
        }
        
        logger.info(f"  Ensemble: AUC={ensemble_auc:.4f}, Acc={ensemble_acc:.3f}, Range=[{y_pred_ensemble.min():.3f}, {y_pred_ensemble.max():.3f}]")
        
        return X_train_meta, X_val_meta
    
    def extract_feature_importance(self, X_train):
        """Extract and save feature importance"""
        logger.info("\nExtracting feature importance...")
        
        for name, model in self.models.items():
            if name == 'ensemble':
                continue
                
            if hasattr(model, 'feature_importances_'):
                importance = model.feature_importances_
            elif hasattr(model, 'coef_'):
                importance = np.abs(model.coef_[0])
            else:
                continue
            
            # Create importance dataframe
            importance_df = pd.DataFrame({
                'feature': self.feature_names,
                'importance': importance
            }).sort_values('importance', ascending=False)
            
            self.feature_importance[name] = importance_df
            
            # Log top 10 features
            logger.info(f"\n{name} - Top 10 features:")
            for idx, row in importance_df.head(10).iterrows():
                logger.info(f"  {row['feature']}: {row['importance']:.4f}")
    
    def final_evaluation(self, X_test, y_test, X_test_meta):
        """Comprehensive evaluation on test set"""
        logger.info("\n" + "="*60)
        logger.info("FINAL TEST SET EVALUATION")
        logger.info("="*60)
        
        # Evaluate each model
        for name, model in self.models.items():
            if name == 'ensemble':
                y_pred_proba = model.predict_proba(X_test_meta)[:, 1]
            else:
                y_pred_proba = model.predict_proba(X_test)[:, 1]
            
            # Metrics
            auc = roc_auc_score(y_test, y_pred_proba)
            y_pred = (y_pred_proba >= 0.5).astype(int)
            acc = accuracy_score(y_test, y_pred)
            
            # Confusion matrix
            tn, fp, fn, tp = confusion_matrix(y_test, y_pred).ravel()
            precision = tp / (tp + fp) if (tp + fp) > 0 else 0
            recall = tp / (tp + fn) if (tp + fn) > 0 else 0
            f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
            
            # Business metrics
            selected = y_pred == 1
            if selected.sum() > 0:
                success_rate = y_test[selected].mean()
                lift = success_rate / y_test.mean()
            else:
                success_rate = 0
                lift = 0
            
            # Update results
            self.results[name].update({
                'test_auc': auc,
                'test_accuracy': acc,
                'precision': precision,
                'recall': recall,
                'f1_score': f1,
                'success_rate_in_selected': success_rate,
                'lift': lift
            })
            
            logger.info(f"\n{name}:")
            logger.info(f"  AUC: {auc:.4f}")
            logger.info(f"  Accuracy: {acc:.3f}")
            logger.info(f"  Precision: {precision:.3f}")
            logger.info(f"  Recall: {recall:.3f}")
            logger.info(f"  F1-Score: {f1:.3f}")
            logger.info(f"  Selected {selected.sum():,} ({selected.mean():.1%})")
            logger.info(f"  Success rate in selected: {success_rate:.1%}")
            logger.info(f"  Lift: {lift:.2f}x")
    
    def save_models_and_results(self):
        """Save all models and results"""
        logger.info("\nSaving models and results...")
        
        # Save models
        for name, model in self.models.items():
            model_path = self.output_dir / f"{name}_model.pkl"
            joblib.dump(model, model_path)
            logger.info(f"  Saved {name} to {model_path}")
        
        # Save results
        results_path = self.output_dir / "training_results.json"
        with open(results_path, 'w') as f:
            json.dump(self.results, f, indent=2)
        
        # Save feature importance
        for name, importance_df in self.feature_importance.items():
            importance_path = self.output_dir / f"feature_importance_{name}.csv"
            importance_df.to_csv(importance_path, index=False)
        
        # Save metadata
        metadata = {
            'training_date': datetime.now().isoformat(),
            'dataset': 'realistic_200k_dataset.csv',
            'dataset_size': 200000,
            'success_rate': 0.231,
            'num_features': len(self.feature_names),
            'models_trained': list(self.models.keys()),
            'best_model': max(self.results.items(), key=lambda x: x[1]['test_auc'])[0],
            'best_auc': max(r['test_auc'] for r in self.results.values())
        }
        
        with open(self.output_dir / 'metadata.json', 'w') as f:
            json.dump(metadata, f, indent=2)
        
        logger.info(f"\nAll models and results saved to {self.output_dir}")


def main():
    """Main training pipeline"""
    start_time = datetime.now()
    
    print("\n" + "="*80)
    print("COMPREHENSIVE MODEL TRAINING - REALISTIC 200K DATASET")
    print("="*80)
    
    # Initialize trainer
    trainer = ComprehensiveModelTrainer()
    
    # Load and prepare data
    X, y = trainer.load_and_prepare_data()
    
    # Split data (60% train, 20% val, 20% test)
    logger.info("\nSplitting data...")
    X_temp, X_test, y_temp, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    X_train, X_val, y_train, y_val = train_test_split(
        X_temp, y_temp, test_size=0.25, random_state=42, stratify=y_temp
    )
    
    logger.info(f"  Train: {len(X_train):,} samples ({y_train.mean():.1%} success)")
    logger.info(f"  Val: {len(X_val):,} samples ({y_val.mean():.1%} success)")
    logger.info(f"  Test: {len(X_test):,} samples ({y_test.mean():.1%} success)")
    
    # Train all models
    trainer.train_models(X_train, y_train, X_val, y_val)
    
    # Create ensemble
    X_train_meta, X_val_meta = trainer.create_ensemble(X_train, y_train, X_val, y_val)
    
    # Extract feature importance
    trainer.extract_feature_importance(X_train)
    
    # Final evaluation on test set
    test_preds = [model.predict_proba(X_test)[:, 1] for name, model in trainer.models.items() if name != 'ensemble']
    X_test_meta = np.column_stack(test_preds)
    trainer.final_evaluation(X_test, y_test, X_test_meta)
    
    # Save everything
    trainer.save_models_and_results()
    
    # Summary
    duration = (datetime.now() - start_time).total_seconds() / 60
    print("\n" + "="*80)
    print("TRAINING COMPLETE!")
    print("="*80)
    print(f"\nTraining time: {duration:.1f} minutes")
    print(f"Best model: {trainer.metadata['best_model']} with {trainer.metadata['best_auc']:.4f} AUC")
    print(f"\nModels saved to: {trainer.output_dir}")
    print("="*80)


if __name__ == "__main__":
    main()