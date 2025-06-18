#!/usr/bin/env python3
"""
Simple diverse ensemble to quickly test if model diversity improves AUC
"""
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
import catboost as cb
import xgboost as xgb
import lightgbm as lgb
import warnings
warnings.filterwarnings('ignore')

# Load data
print("Loading data...")
df = pd.read_csv('data/final_100k_dataset_75features.csv')

# Prepare data
exclude_cols = ['success', 'startup_id', 'startup_name']
feature_cols = [col for col in df.columns if col not in exclude_cols]
X = df[feature_cols]
y = df['success']

# Encode categoricals
categorical_cols = X.select_dtypes(include=['object']).columns.tolist()
X_encoded = X.copy()
encoders = {}
for col in categorical_cols:
    encoders[col] = LabelEncoder()
    X_encoded[col] = encoders[col].fit_transform(X[col].astype(str))

# Fill NaNs
numeric_cols = X_encoded.select_dtypes(include=['number']).columns
X_encoded[numeric_cols] = X_encoded[numeric_cols].fillna(X_encoded[numeric_cols].median())

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X_encoded, y, test_size=0.2, random_state=42, stratify=y
)

print(f"Train: {len(y_train)}, Test: {len(y_test)}")

# Create diverse models with different parameters
models = [
    ('catboost', cb.CatBoostClassifier(iterations=300, depth=6, learning_rate=0.05, verbose=False)),
    ('xgboost', xgb.XGBClassifier(n_estimators=300, max_depth=5, learning_rate=0.05)),
    ('lightgbm', lgb.LGBMClassifier(n_estimators=300, num_leaves=31, learning_rate=0.05, verbosity=-1)),
    ('rf', RandomForestClassifier(n_estimators=200, max_depth=10, random_state=42))
]

# Train and evaluate individual models
print("\nTraining individual models...")
individual_scores = {}
for name, model in models:
    print(f"Training {name}...")
    model.fit(X_train, y_train)
    pred = model.predict_proba(X_test)[:, 1]
    auc = roc_auc_score(y_test, pred)
    individual_scores[name] = auc
    print(f"  {name} AUC: {auc:.4f}")

# Create voting ensemble
print("\nTraining voting ensemble...")
ensemble = VotingClassifier(models, voting='soft')
ensemble.fit(X_train, y_train)
ensemble_pred = ensemble.predict_proba(X_test)[:, 1]
ensemble_auc = roc_auc_score(y_test, ensemble_pred)

print("\n" + "="*50)
print("RESULTS")
print("="*50)
print("Individual models:")
for name, score in individual_scores.items():
    print(f"  {name}: {score:.4f}")
print(f"\nVoting Ensemble: {ensemble_auc:.4f}")
print(f"\nBaseline (45 features): 0.7730")
print(f"Simple ensemble (75 features): 0.7750")
print(f"Diverse ensemble: {ensemble_auc:.4f}")
print(f"Improvement: +{(ensemble_auc - 0.773):.4f}")
print("="*50)