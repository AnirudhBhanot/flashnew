#!/usr/bin/env python3
"""
Minimal working training - focuses on getting models trained quickly
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score
import xgboost as xgb
import lightgbm as lgb
import joblib
from pathlib import Path
import json
from datetime import datetime

# Simple feature engineering
def prepare_data(df):
    """Minimal data preparation"""
    # Select key features
    feature_cols = [
        'total_capital_raised_usd', 'revenue_growth_rate_percent', 
        'burn_multiple', 'team_size_full_time', 'runway_months',
        'customer_count', 'net_dollar_retention_percent', 
        'annual_revenue_run_rate', 'burn_rate_monthly',
        'team_experience_score', 'product_completeness_score',
        'customer_acquisition_cost', 'customer_lifetime_value',
        'prior_successful_exits_count', 'years_experience_avg'
    ]
    
    # Use available features
    available_features = [col for col in feature_cols if col in df.columns]
    X = df[available_features].fillna(0)
    y = df['success']
    
    print(f"Using {len(available_features)} features")
    return X, y, available_features


def main():
    print("\nMINIMAL WORKING MODEL TRAINING")
    print("="*50)
    
    # Create output directory
    output_dir = Path("models/complete_v1")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Load data
    print("\n1. Loading data...")
    df = pd.read_csv('data/realistic_startup_dataset_200k.csv')
    print(f"   Loaded {len(df):,} samples")
    
    # Prepare data
    print("\n2. Preparing data...")
    X, y, feature_names = prepare_data(df)
    
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
    
    # XGBoost
    print("   Training XGBoost...")
    models['xgboost'] = xgb.XGBClassifier(
        n_estimators=50,
        max_depth=4,
        random_state=42,
        n_jobs=-1
    )
    models['xgboost'].fit(X_train, y_train)
    
    # LightGBM
    print("   Training LightGBM...")
    models['lightgbm'] = lgb.LGBMClassifier(
        n_estimators=50,
        num_leaves=15,
        random_state=42,
        n_jobs=-1,
        verbosity=-1
    )
    models['lightgbm'].fit(X_train, y_train)
    
    # Random Forest
    print("   Training Random Forest...")
    models['random_forest'] = RandomForestClassifier(
        n_estimators=50,
        max_depth=8,
        random_state=42,
        n_jobs=-1
    )
    models['random_forest'].fit(X_train, y_train)
    
    # Meta ensemble
    print("   Creating ensemble...")
    train_preds = []
    test_preds = []
    
    for name, model in models.items():
        train_pred = model.predict_proba(X_train)[:, 1]
        test_pred = model.predict_proba(X_test)[:, 1]
        train_preds.append(train_pred)
        test_preds.append(test_pred)
        
        # Individual AUC
        auc = roc_auc_score(y_test, test_pred)
        results[name] = auc
        print(f"     {name} AUC: {auc:.4f}")
    
    # Stack predictions
    X_train_meta = np.column_stack(train_preds)
    X_test_meta = np.column_stack(test_preds)
    
    # Meta learner
    models['meta_learner'] = xgb.XGBClassifier(
        n_estimators=20,
        max_depth=3,
        random_state=42
    )
    models['meta_learner'].fit(X_train_meta, y_train)
    
    # Final prediction
    y_pred_final = models['meta_learner'].predict_proba(X_test_meta)[:, 1]
    final_auc = roc_auc_score(y_test, y_pred_final)
    results['ensemble'] = final_auc
    
    print(f"\n   ENSEMBLE AUC: {final_auc:.4f}")
    print(f"   Prediction range: {y_pred_final.min():.3f} - {y_pred_final.max():.3f}")
    
    # Save models
    print("\n5. Saving models...")
    for name, model in models.items():
        joblib.dump(model, output_dir / f'{name}.pkl')
    
    # Save metadata
    metadata = {
        'training_date': datetime.now().isoformat(),
        'training_mode': 'MINIMAL_WORKING',
        'feature_count': len(feature_names),
        'feature_names': feature_names,
        'model_performance': results
    }
    
    with open(output_dir / 'metadata.json', 'w') as f:
        json.dump(metadata, f, indent=2)
    
    # Save simple feature engineer
    joblib.dump({}, output_dir / 'feature_engineer.pkl')
    joblib.dump({}, output_dir / 'label_encoders.pkl')
    
    print(f"\n   Models saved to {output_dir}/")
    
    print("\n" + "="*50)
    print("TRAINING COMPLETE!")
    print("="*50)
    print(f"Final accuracy: {final_auc:.1%}")
    print(f"Full probability range: {y_pred_final.min():.1%} - {y_pred_final.max():.1%}")
    print("="*50)


if __name__ == "__main__":
    main()