#!/usr/bin/env python3
"""
Train models WITHOUT data leakage
Removes outcome_type and other leakage columns
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score, classification_report
import xgboost as xgb
import lightgbm as lgb
import joblib
from pathlib import Path
import json
from datetime import datetime

def prepare_data_no_leakage(df):
    """Prepare data WITHOUT leakage columns"""
    
    # CRITICAL: Remove columns that leak the target
    leakage_columns = [
        'outcome_type',  # This directly determines success!
        'outcome_date',  # Future information
        'success',       # Target variable
        'startup_id',    # ID column
        'data_collection_date'  # Not predictive
    ]
    
    # Get feature columns (exclude leakage)
    feature_cols = [col for col in df.columns if col not in leakage_columns]
    
    print(f"Using {len(feature_cols)} features (removed {len(leakage_columns)} leakage columns)")
    print(f"Removed columns: {leakage_columns}")
    
    # Prepare features and target
    X = df[feature_cols]
    y = df['success']
    
    # Handle categorical columns
    categorical_cols = ['funding_stage', 'sector', 'product_stage', 'investor_tier_primary']
    
    for col in categorical_cols:
        if col in X.columns:
            # Convert to category codes
            X[col] = pd.Categorical(X[col]).codes
    
    # Fill any NaN values
    X = X.fillna(0)
    
    return X, y, feature_cols


def main():
    print("\nTRAINING WITHOUT DATA LEAKAGE")
    print("="*60)
    
    # Create output directory
    output_dir = Path("models/no_leakage_v1")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Load data
    print("\n1. Loading data...")
    df = pd.read_csv('data/realistic_startup_dataset_200k.csv')
    print(f"   Loaded {len(df):,} samples")
    print(f"   Success rate: {df['success'].mean():.1%}")
    
    # Prepare data WITHOUT leakage
    print("\n2. Preparing data (removing leakage columns)...")
    X, y, feature_names = prepare_data_no_leakage(df)
    
    # Split data
    print("\n3. Splitting data...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    print(f"   Train: {len(X_train):,} samples")
    print(f"   Test: {len(X_test):,} samples")
    
    # Train models
    print("\n4. Training models...")
    models = {}
    results = {}
    
    # Calculate class weight
    n_pos = y_train.sum()
    n_neg = len(y_train) - n_pos
    scale_pos_weight = n_neg / n_pos
    
    # XGBoost
    print("   Training XGBoost...")
    models['xgboost'] = xgb.XGBClassifier(
        n_estimators=100,
        max_depth=5,
        learning_rate=0.1,
        scale_pos_weight=scale_pos_weight,
        random_state=42,
        n_jobs=-1
    )
    models['xgboost'].fit(X_train, y_train)
    
    # LightGBM
    print("   Training LightGBM...")
    models['lightgbm'] = lgb.LGBMClassifier(
        n_estimators=100,
        num_leaves=31,
        learning_rate=0.1,
        scale_pos_weight=scale_pos_weight,
        random_state=42,
        n_jobs=-1,
        verbosity=-1
    )
    models['lightgbm'].fit(X_train, y_train)
    
    # Random Forest
    print("   Training Random Forest...")
    models['random_forest'] = RandomForestClassifier(
        n_estimators=100,
        max_depth=10,
        class_weight='balanced',
        random_state=42,
        n_jobs=-1
    )
    models['random_forest'].fit(X_train, y_train)
    
    # Evaluate models
    print("\n5. Evaluating models...")
    for name, model in models.items():
        y_pred = model.predict_proba(X_test)[:, 1]
        auc = roc_auc_score(y_test, y_pred)
        results[name] = auc
        
        print(f"\n   {name}:")
        print(f"     AUC: {auc:.4f}")
        print(f"     Prediction range: {y_pred.min():.3f} - {y_pred.max():.3f}")
        print(f"     Prediction std: {y_pred.std():.3f}")
        
        # Show prediction distribution
        bins = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
        hist, _ = np.histogram(y_pred, bins=bins)
        print(f"     Distribution: {hist}")
    
    # Ensemble prediction
    print("\n   Ensemble:")
    ensemble_pred = np.mean([
        models[name].predict_proba(X_test)[:, 1] 
        for name in models.keys()
    ], axis=0)
    
    ensemble_auc = roc_auc_score(y_test, ensemble_pred)
    results['ensemble'] = ensemble_auc
    
    print(f"     AUC: {ensemble_auc:.4f}")
    print(f"     Prediction range: {ensemble_pred.min():.3f} - {ensemble_pred.max():.3f}")
    
    # Feature importance
    print("\n6. Top 10 important features (XGBoost):")
    importance = models['xgboost'].feature_importances_
    indices = np.argsort(importance)[::-1][:10]
    
    for i, idx in enumerate(indices):
        print(f"   {i+1}. {feature_names[idx]}: {importance[idx]:.4f}")
    
    # Save models
    print("\n7. Saving models...")
    for name, model in models.items():
        joblib.dump(model, output_dir / f'{name}.pkl')
    
    # Save metadata
    metadata = {
        'training_date': datetime.now().isoformat(),
        'training_mode': 'NO_LEAKAGE',
        'feature_count': len(feature_names),
        'feature_names': feature_names,
        'model_performance': results,
        'removed_columns': [
            'outcome_type (direct leakage!)',
            'outcome_date (future info)',
            'success (target)',
            'startup_id',
            'data_collection_date'
        ]
    }
    
    with open(output_dir / 'metadata.json', 'w') as f:
        json.dump(metadata, f, indent=2)
    
    print(f"\n   Models saved to {output_dir}/")
    
    # Show realistic expectations
    print("\n" + "="*60)
    print("REALISTIC RESULTS (No Data Leakage)")
    print("="*60)
    print(f"Average AUC: {np.mean(list(results.values())):.4f}")
    print(f"Expected range: 0.65-0.85 AUC for startup prediction")
    print(f"Prediction variance shows proper uncertainty")
    print("="*60)


if __name__ == "__main__":
    main()