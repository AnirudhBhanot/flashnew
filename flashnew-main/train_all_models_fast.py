#!/usr/bin/env python3
"""
Fast training of all models on the realistic 200k dataset
Optimized for speed while maintaining quality
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import roc_auc_score, accuracy_score
from sklearn.ensemble import RandomForestClassifier
import xgboost as xgb
import lightgbm as lgb
import joblib
from pathlib import Path
import json
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

print("\n" + "="*80)
print("FAST MODEL TRAINING - REALISTIC 200K DATASET")
print("="*80)

start_time = datetime.now()

# Load data
print("\nLoading data...")
df = pd.read_csv('realistic_200k_dataset.csv')
print(f"Loaded {len(df):,} samples with {df['success'].mean():.1%} success rate")

# Import features
from feature_config import ALL_FEATURES, CATEGORICAL_FEATURES

# Prepare data
X = df[ALL_FEATURES].copy()
y = df['success'].copy()

# Encode categorical features
print("\nEncoding categorical features...")
label_encoders = {}
for col in CATEGORICAL_FEATURES:
    if col in X.columns:
        le = LabelEncoder()
        X[col] = le.fit_transform(X[col].astype(str))
        label_encoders[col] = le

# Fill missing values
X = X.fillna(X.median())

# Add key engineered features
print("Adding engineered features...")
X['log_capital'] = np.log1p(X['total_capital_raised_usd'])
X['log_revenue'] = np.log1p(X['annual_revenue_run_rate'])
X['capital_efficiency'] = X['annual_revenue_run_rate'] / (X['total_capital_raised_usd'] + 1)

# Split data
print("\nSplitting data...")
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
print(f"Train: {len(X_train):,} | Test: {len(X_test):,}")

# Calculate class weight
scale_pos_weight = (y_train == 0).sum() / (y_train == 1).sum()
print(f"Class weight: {scale_pos_weight:.2f}")

# Create output directory
output_dir = Path("models/production_final")
output_dir.mkdir(parents=True, exist_ok=True)

models = {}
results = {}

# 1. XGBoost (fast)
print("\n1. Training XGBoost...")
models['xgboost'] = xgb.XGBClassifier(
    n_estimators=100,
    max_depth=6,
    learning_rate=0.3,
    scale_pos_weight=scale_pos_weight,
    random_state=42,
    n_jobs=-1
)
models['xgboost'].fit(X_train, y_train)

# 2. LightGBM (fast)
print("2. Training LightGBM...")
models['lightgbm'] = lgb.LGBMClassifier(
    n_estimators=100,
    num_leaves=31,
    learning_rate=0.3,
    scale_pos_weight=scale_pos_weight,
    random_state=42,
    n_jobs=-1,
    verbosity=-1
)
models['lightgbm'].fit(X_train, y_train)

# 3. Random Forest (fast)
print("3. Training Random Forest...")
models['random_forest'] = RandomForestClassifier(
    n_estimators=100,
    max_depth=10,
    class_weight='balanced',
    random_state=42,
    n_jobs=-1
)
models['random_forest'].fit(X_train, y_train)

# 4. Simple ensemble (average)
print("4. Creating Ensemble...")
ensemble_preds = []
for name, model in models.items():
    preds = model.predict_proba(X_test)[:, 1]
    ensemble_preds.append(preds)

ensemble_pred = np.mean(ensemble_preds, axis=0)

# Evaluate all models
print("\n" + "="*60)
print("EVALUATION RESULTS")
print("="*60)

for name, model in models.items():
    y_pred_proba = model.predict_proba(X_test)[:, 1]
    auc = roc_auc_score(y_test, y_pred_proba)
    acc = accuracy_score(y_test, (y_pred_proba >= 0.5).astype(int))
    
    results[name] = {
        'auc': auc,
        'accuracy': acc,
        'min_prob': float(y_pred_proba.min()),
        'max_prob': float(y_pred_proba.max())
    }
    
    print(f"\n{name}:")
    print(f"  AUC: {auc:.4f}")
    print(f"  Accuracy: {acc:.3f}")
    print(f"  Probability range: {y_pred_proba.min():.3f} - {y_pred_proba.max():.3f}")

# Ensemble results
ensemble_auc = roc_auc_score(y_test, ensemble_pred)
ensemble_acc = accuracy_score(y_test, (ensemble_pred >= 0.5).astype(int))

results['ensemble'] = {
    'auc': ensemble_auc,
    'accuracy': ensemble_acc,
    'min_prob': float(ensemble_pred.min()),
    'max_prob': float(ensemble_pred.max())
}

print(f"\nEnsemble:")
print(f"  AUC: {ensemble_auc:.4f}")
print(f"  Accuracy: {ensemble_acc:.3f}")
print(f"  Probability range: {ensemble_pred.min():.3f} - {ensemble_pred.max():.3f}")

# Business impact
print("\n" + "-"*60)
print("BUSINESS IMPACT")
print("-"*60)

threshold = 0.5
selected = ensemble_pred >= threshold
if selected.sum() > 0:
    success_rate = y_test[selected].mean()
    baseline = y_test.mean()
    lift = success_rate / baseline
    
    print(f"Baseline success rate: {baseline:.1%}")
    print(f"Model-selected success rate: {success_rate:.1%}")
    print(f"Lift: {lift:.2f}x")
    print(f"Startups selected: {selected.sum():,} ({selected.mean():.1%})")

# Save models
print("\nSaving models...")
for name, model in models.items():
    joblib.dump(model, output_dir / f"{name}.pkl")

# Save ensemble logic
ensemble_info = {
    'type': 'simple_average',
    'models': list(models.keys()),
    'weights': [1/len(models)] * len(models)
}
joblib.dump(ensemble_info, output_dir / "ensemble.pkl")

# Save results and metadata
metadata = {
    'training_date': datetime.now().isoformat(),
    'dataset': 'realistic_200k_dataset.csv',
    'dataset_size': len(df),
    'success_rate': float(df['success'].mean()),
    'features_used': len(X.columns),
    'results': results,
    'best_model': max(results.items(), key=lambda x: x[1]['auc'])[0],
    'training_time_minutes': (datetime.now() - start_time).total_seconds() / 60
}

with open(output_dir / 'metadata.json', 'w') as f:
    json.dump(metadata, f, indent=2)

# Save label encoders
joblib.dump(label_encoders, output_dir / 'label_encoders.pkl')

# Final summary
duration = (datetime.now() - start_time).total_seconds() / 60
print("\n" + "="*80)
print("TRAINING COMPLETE!")
print("="*80)
print(f"\nTotal time: {duration:.1f} minutes")
print(f"Best model: {metadata['best_model']} ({results[metadata['best_model']]['auc']:.4f} AUC)")
print(f"Models saved to: {output_dir}")
print("="*80)