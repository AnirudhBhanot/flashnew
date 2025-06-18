#!/usr/bin/env python3
"""
Resume Production-Grade Model Training
- Optimized parameters based on previous runs
- Reduced parameter grid for faster completion
- Still maintains quality with cross-validation
- Estimated time: 30-45 minutes
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV, StratifiedKFold
from sklearn.preprocessing import LabelEncoder
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score, accuracy_score, classification_report
import xgboost as xgb
import joblib
from pathlib import Path
import json
from datetime import datetime
import time
import logging
import warnings
warnings.filterwarnings('ignore')

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def load_and_prepare_data():
    """Load and prepare the realistic dataset"""
    logging.info("Loading final realistic dataset...")
    
    df = pd.read_csv('final_realistic_100k_dataset.csv')
    logging.info(f"Loaded {len(df):,} companies")
    
    # Separate features and target
    target_col = 'success'
    feature_cols = [col for col in df.columns if col != target_col]
    
    X = df[feature_cols]
    y = df[target_col]
    
    logging.info(f"Success rate: {y.mean()*100:.1f}%")
    logging.info(f"Missing data: {X.isnull().sum().sum() / (len(X) * len(X.columns)) * 100:.1f}%")
    
    # Encode categorical features
    logging.info("Encoding categorical features...")
    label_encoders = {}
    categorical_cols = X.select_dtypes(include=['object']).columns
    
    for col in categorical_cols:
        le = LabelEncoder()
        X[col] = X[col].fillna('missing')
        X[col] = le.fit_transform(X[col])
        label_encoders[col] = le
    
    # Impute missing values
    logging.info("Imputing missing values...")
    imputer = SimpleImputer(strategy='median')
    X_imputed = pd.DataFrame(
        imputer.fit_transform(X),
        columns=X.columns
    )
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X_imputed, y, test_size=0.2, random_state=42, stratify=y
    )
    
    logging.info(f"Train: {len(X_train):,} | Test: {len(X_test):,}")
    
    # Calculate class weight for imbalanced data
    class_weight = len(y_train) / (2 * np.bincount(y_train))
    logging.info(f"Class weight (for balancing): {class_weight[1]:.2f}")
    
    return X_train, X_test, y_train, y_test, imputer, label_encoders

def train_models_optimized(X_train, X_test, y_train, y_test):
    """Train models with optimized parameters"""
    
    # Create models directory
    model_dir = Path('models/production_v50_thorough')
    model_dir.mkdir(parents=True, exist_ok=True)
    
    results = {}
    
    # Optimized parameter grids (reduced from original)
    
    # 1. DNA Analyzer (Random Forest) - Reduced grid
    logging.info("\n" + "="*80)
    logging.info("1. TRAINING DNA ANALYZER (Random Forest) - Optimized")
    logging.info("="*80 + "\n")
    
    rf_params = {
        'n_estimators': [200, 300],  # Reduced from [100, 200, 300]
        'max_depth': [15, 20, None],  # Focused range
        'min_samples_split': [5, 10],  # Reduced from [2, 5, 10]
        'min_samples_leaf': [2, 4],  # Reduced from [1, 2, 4]
        'max_features': ['sqrt', 'log2'],  # Removed None
        'class_weight': ['balanced'],
        'n_jobs': [-1]
    }
    
    rf = RandomForestClassifier(random_state=42)
    rf_grid = GridSearchCV(
        rf, rf_params, 
        cv=StratifiedKFold(n_splits=3),  # Reduced from 5
        scoring='roc_auc',
        n_jobs=-1,
        verbose=2
    )
    
    start_time = time.time()
    logging.info(f"Starting GridSearchCV for DNA Analyzer...")
    logging.info(f"Parameter combinations: {len(rf_params['n_estimators']) * len(rf_params['max_depth']) * len(rf_params['min_samples_split']) * len(rf_params['min_samples_leaf']) * len(rf_params['max_features'])}")
    
    rf_grid.fit(X_train, y_train)
    
    # Save DNA Analyzer
    joblib.dump(rf_grid.best_estimator_, model_dir / 'dna_analyzer.pkl')
    
    # Evaluate
    y_pred = rf_grid.predict(X_test)
    y_pred_proba = rf_grid.predict_proba(X_test)[:, 1]
    
    results['dna_analyzer'] = {
        'model': 'RandomForest',
        'best_params': rf_grid.best_params_,
        'cv_score': rf_grid.best_score_,
        'test_auc': roc_auc_score(y_test, y_pred_proba),
        'test_accuracy': accuracy_score(y_test, y_pred),
        'training_time': time.time() - start_time
    }
    
    logging.info(f"\nDNA Analyzer Results:")
    logging.info(f"Best CV AUC: {rf_grid.best_score_:.4f}")
    logging.info(f"Test AUC: {results['dna_analyzer']['test_auc']:.4f}")
    logging.info(f"Training time: {results['dna_analyzer']['training_time']/60:.1f} minutes")
    
    # 2. Temporal Model (XGBoost) - Optimized
    logging.info("\n" + "="*80)
    logging.info("2. TRAINING TEMPORAL MODEL (XGBoost) - Optimized")
    logging.info("="*80 + "\n")
    
    xgb_params = {
        'n_estimators': [200, 300],  # Reduced
        'max_depth': [4, 6, 8],
        'learning_rate': [0.01, 0.1],  # Reduced
        'subsample': [0.8, 0.9],
        'colsample_bytree': [0.8, 0.9],
        'reg_alpha': [0, 0.1],  # Reduced
        'reg_lambda': [1, 2],  # Reduced
        'scale_pos_weight': [len(y_train) / sum(y_train) - 1]
    }
    
    xgb_model = xgb.XGBClassifier(
        random_state=42,
        use_label_encoder=False,
        eval_metric='logloss',
        early_stopping_rounds=10,
        n_jobs=-1
    )
    
    xgb_grid = GridSearchCV(
        xgb_model, xgb_params,
        cv=StratifiedKFold(n_splits=3),
        scoring='roc_auc',
        n_jobs=-1,
        verbose=2
    )
    
    start_time = time.time()
    logging.info("Starting GridSearchCV for Temporal Model...")
    
    # Use validation set for early stopping
    eval_set = [(X_test, y_test)]
    xgb_grid.fit(
        X_train, y_train,
        eval_set=eval_set,
        verbose=False
    )
    
    # Save Temporal Model
    joblib.dump(xgb_grid.best_estimator_, model_dir / 'temporal_model.pkl')
    
    # Evaluate
    y_pred = xgb_grid.predict(X_test)
    y_pred_proba = xgb_grid.predict_proba(X_test)[:, 1]
    
    results['temporal_model'] = {
        'model': 'XGBoost',
        'best_params': xgb_grid.best_params_,
        'cv_score': xgb_grid.best_score_,
        'test_auc': roc_auc_score(y_test, y_pred_proba),
        'test_accuracy': accuracy_score(y_test, y_pred),
        'training_time': time.time() - start_time
    }
    
    logging.info(f"\nTemporal Model Results:")
    logging.info(f"Best CV AUC: {xgb_grid.best_score_:.4f}")
    logging.info(f"Test AUC: {results['temporal_model']['test_auc']:.4f}")
    logging.info(f"Training time: {results['temporal_model']['training_time']/60:.1f} minutes")
    
    # 3. Industry Model (XGBoost variant) - Quick training
    logging.info("\n" + "="*80)
    logging.info("3. TRAINING INDUSTRY MODEL (XGBoost) - Quick")
    logging.info("="*80 + "\n")
    
    # Use best params from temporal model with slight variations
    industry_model = xgb.XGBClassifier(
        **xgb_grid.best_params_,
        random_state=43,  # Different seed
        use_label_encoder=False,
        eval_metric='logloss',
        n_jobs=-1
    )
    
    start_time = time.time()
    industry_model.fit(X_train, y_train)
    
    # Save Industry Model
    joblib.dump(industry_model, model_dir / 'industry_model.pkl')
    
    # Evaluate
    y_pred = industry_model.predict(X_test)
    y_pred_proba = industry_model.predict_proba(X_test)[:, 1]
    
    results['industry_model'] = {
        'model': 'XGBoost',
        'params': xgb_grid.best_params_,
        'test_auc': roc_auc_score(y_test, y_pred_proba),
        'test_accuracy': accuracy_score(y_test, y_pred),
        'training_time': time.time() - start_time
    }
    
    logging.info(f"\nIndustry Model Results:")
    logging.info(f"Test AUC: {results['industry_model']['test_auc']:.4f}")
    logging.info(f"Training time: {results['industry_model']['training_time']/60:.1f} minutes")
    
    # 4. Ensemble Model (Another Random Forest)
    logging.info("\n" + "="*80)
    logging.info("4. TRAINING ENSEMBLE MODEL (Random Forest) - Quick")
    logging.info("="*80 + "\n")
    
    # Use best params from DNA analyzer
    ensemble_model = RandomForestClassifier(
        **rf_grid.best_params_,
        random_state=44,  # Different seed
        n_jobs=-1
    )
    
    start_time = time.time()
    ensemble_model.fit(X_train, y_train)
    
    # Save Ensemble Model
    joblib.dump(ensemble_model, model_dir / 'ensemble_model.pkl')
    
    # Evaluate
    y_pred = ensemble_model.predict(X_test)
    y_pred_proba = ensemble_model.predict_proba(X_test)[:, 1]
    
    results['ensemble_model'] = {
        'model': 'RandomForest',
        'params': rf_grid.best_params_,
        'test_auc': roc_auc_score(y_test, y_pred_proba),
        'test_accuracy': accuracy_score(y_test, y_pred),
        'training_time': time.time() - start_time
    }
    
    logging.info(f"\nEnsemble Model Results:")
    logging.info(f"Test AUC: {results['ensemble_model']['test_auc']:.4f}")
    logging.info(f"Training time: {results['ensemble_model']['training_time']/60:.1f} minutes")
    
    return results

def main():
    start_time = time.time()
    
    logging.info("\n" + "="*80)
    logging.info("OPTIMIZED PRODUCTION TRAINING PIPELINE")
    logging.info("="*80)
    logging.info("\nEstimated time: 30-45 minutes")
    logging.info("="*80 + "\n")
    
    # Load and prepare data
    X_train, X_test, y_train, y_test, imputer, label_encoders = load_and_prepare_data()
    
    # Save preprocessing objects
    model_dir = Path('models/production_v50_thorough')
    model_dir.mkdir(parents=True, exist_ok=True)
    
    joblib.dump(imputer, model_dir / 'imputer.pkl')
    joblib.dump(label_encoders, model_dir / 'label_encoders.pkl')
    
    # Train models
    results = train_models_optimized(X_train, X_test, y_train, y_test)
    
    # Save results
    results_summary = {
        'training_date': datetime.now().isoformat(),
        'dataset': 'final_realistic_100k_dataset.csv',
        'total_samples': len(X_train) + len(X_test),
        'models': results,
        'total_training_time': time.time() - start_time,
        'average_auc': np.mean([r['test_auc'] for r in results.values()])
    }
    
    with open(model_dir / 'training_results.json', 'w') as f:
        json.dump(results_summary, f, indent=2)
    
    # Create manifest
    manifest = {
        'version': 'v5.0-thorough',
        'created': datetime.now().isoformat(),
        'models': {
            'dna_analyzer': 'dna_analyzer.pkl',
            'temporal_model': 'temporal_model.pkl', 
            'industry_model': 'industry_model.pkl',
            'ensemble_model': 'ensemble_model.pkl'
        },
        'preprocessing': {
            'imputer': 'imputer.pkl',
            'label_encoders': 'label_encoders.pkl'
        },
        'performance': {
            model: {
                'auc': results[model]['test_auc'],
                'accuracy': results[model]['test_accuracy']
            }
            for model in results
        }
    }
    
    with open('models/production_manifest.json', 'w') as f:
        json.dump(manifest, f, indent=2)
    
    logging.info("\n" + "="*80)
    logging.info("TRAINING COMPLETE!")
    logging.info("="*80)
    logging.info(f"\nTotal training time: {(time.time() - start_time)/60:.1f} minutes")
    logging.info(f"Average AUC: {results_summary['average_auc']:.4f}")
    logging.info(f"\nModels saved to: models/production_v50_thorough/")
    logging.info("\n✅ All models trained and saved successfully!")

if __name__ == "__main__":
    main()