#!/usr/bin/env python3
"""
Fast version of advanced ensemble - fewer models for quicker results
"""
import numpy as np
import pandas as pd
import json
import joblib
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

from sklearn.model_selection import StratifiedKFold, train_test_split
from sklearn.metrics import roc_auc_score, accuracy_score, f1_score
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.neural_network import MLPClassifier

import catboost as cb
from catboost import CatBoostClassifier
import xgboost as xgb
from xgboost import XGBClassifier
import lightgbm as lgb
from lightgbm import LGBMClassifier

import os
os.makedirs('models/advanced_ensemble_fast', exist_ok=True)

class FastAdvancedEnsemble:
    def __init__(self):
        self.models = {}
        self.scalers = {}
        self.encoders = {}
        self.meta_model = None
        
    def create_base_models(self):
        """Create core diverse models"""
        
        # 1. CatBoost - handles categoricals well
        self.models['catboost'] = CatBoostClassifier(
            iterations=500,
            learning_rate=0.05,
            depth=6,
            random_state=42,
            verbose=False
        )
        
        # 2. XGBoost - different algorithm
        self.models['xgboost'] = XGBClassifier(
            n_estimators=300,
            max_depth=6,
            learning_rate=0.05,
            random_state=42
        )
        
        # 3. LightGBM - fast and effective
        self.models['lightgbm'] = LGBMClassifier(
            n_estimators=300,
            num_leaves=31,
            learning_rate=0.05,
            random_state=42,
            verbosity=-1
        )
        
        # 4. Random Forest - bagging approach
        self.models['random_forest'] = RandomForestClassifier(
            n_estimators=200,
            max_depth=10,
            random_state=42,
            n_jobs=-1
        )
        
        # 5. Neural Network - captures non-linear patterns
        self.models['neural_net'] = MLPClassifier(
            hidden_layer_sizes=(100, 50),
            max_iter=200,
            early_stopping=True,
            random_state=42
        )
        
        # 6. Gradient Boosting - different boosting approach
        self.models['gradient_boost'] = GradientBoostingClassifier(
            n_estimators=200,
            max_depth=5,
            learning_rate=0.05,
            random_state=42
        )
    
    def prepare_data(self, df):
        """Prepare data with proper encoding"""
        
        # Exclude non-feature columns
        exclude_cols = ['success', 'raise_successful', 'startup_id', 'startup_name']
        feature_cols = [col for col in df.columns if col not in exclude_cols]
        X = df[feature_cols]
        y = df['success'] if 'success' in df.columns else df['raise_successful']
        
        # Identify categorical columns
        categorical_cols = X.select_dtypes(include=['object']).columns.tolist()
        numeric_cols = X.select_dtypes(include=['number']).columns.tolist()
        
        # Encode categoricals
        X_encoded = X.copy()
        for col in categorical_cols:
            self.encoders[col] = LabelEncoder()
            X_encoded[col] = self.encoders[col].fit_transform(X[col].astype(str))
        
        # Fill NaN values before scaling
        X_encoded[numeric_cols] = X_encoded[numeric_cols].fillna(X_encoded[numeric_cols].median())
        
        # Scale for neural network
        self.scalers['standard'] = StandardScaler()
        X_scaled = X_encoded.copy()
        X_scaled[numeric_cols] = self.scalers['standard'].fit_transform(X_encoded[numeric_cols])
        
        return X, X_encoded, X_scaled, y, feature_cols, categorical_cols
    
    def train_models(self, X_train, X_train_enc, X_train_scaled, y_train, 
                    X_val, X_val_enc, X_val_scaled, y_val, categorical_cols):
        """Train all models and return predictions"""
        
        predictions = {}
        
        for name, model in self.models.items():
            print(f"Training {name}...")
            
            if name == 'catboost':
                # CatBoost with categorical features
                cat_indices = [i for i, col in enumerate(X_train.columns) if col in categorical_cols]
                model.fit(
                    X_train, y_train,
                    cat_features=cat_indices,
                    eval_set=(X_val, y_val),
                    early_stopping_rounds=50,
                    verbose=False
                )
                predictions[name] = model.predict_proba(X_val)[:, 1]
                
            elif name == 'neural_net':
                # Neural network with scaled data
                model.fit(X_train_scaled, y_train)
                predictions[name] = model.predict_proba(X_val_scaled)[:, 1]
                
            elif name in ['xgboost', 'lightgbm']:
                # Tree models with early stopping
                if name == 'xgboost':
                    model.fit(
                        X_train_enc, y_train,
                        eval_set=[(X_val_enc, y_val)],
                        early_stopping_rounds=50,
                        verbose=False
                    )
                else:  # lightgbm
                    model.fit(
                        X_train_enc, y_train,
                        eval_set=[(X_val_enc, y_val)],
                        callbacks=[lgb.early_stopping(50), lgb.log_evaluation(0)]
                    )
                predictions[name] = model.predict_proba(X_val_enc)[:, 1]
                
            else:
                # Other models
                model.fit(X_train_enc, y_train)
                predictions[name] = model.predict_proba(X_val_enc)[:, 1]
            
            # Print individual model performance
            auc = roc_auc_score(y_val, predictions[name])
            print(f"  {name} AUC: {auc:.4f}")
        
        return predictions
    
    def train_stacking(self, predictions, y_train):
        """Train meta-learner"""
        
        # Stack predictions
        X_meta = np.column_stack([predictions[name] for name in sorted(predictions.keys())])
        
        # Train multiple meta-learners and pick best
        meta_models = {
            'logistic': LogisticRegression(random_state=42),
            'gradient_boost': GradientBoostingClassifier(n_estimators=100, random_state=42),
            'neural_net': MLPClassifier(hidden_layer_sizes=(20, 10), random_state=42)
        }
        
        best_score = 0
        best_model = None
        
        print("\nTraining meta-learners...")
        for name, model in meta_models.items():
            # Use internal CV to evaluate
            cv_scores = []
            kf = StratifiedKFold(n_splits=3, shuffle=True, random_state=42)
            
            for train_idx, val_idx in kf.split(X_meta, y_train):
                model_clone = model.__class__(**model.get_params())
                model_clone.fit(X_meta[train_idx], y_train.iloc[train_idx])
                pred = model_clone.predict_proba(X_meta[val_idx])[:, 1]
                score = roc_auc_score(y_train.iloc[val_idx], pred)
                cv_scores.append(score)
            
            mean_score = np.mean(cv_scores)
            print(f"  {name} CV AUC: {mean_score:.4f}")
            
            if mean_score > best_score:
                best_score = mean_score
                best_model = model
        
        # Train best model on full data
        print(f"\nUsing {best_model.__class__.__name__} as meta-learner")
        self.meta_model = best_model
        self.meta_model.fit(X_meta, y_train)
        
        return X_meta
    
    def predict_ensemble(self, X, X_enc, X_scaled, categorical_cols):
        """Make ensemble predictions"""
        
        predictions = {}
        
        for name, model in self.models.items():
            if name == 'catboost':
                predictions[name] = model.predict_proba(X)[:, 1]
            elif name == 'neural_net':
                predictions[name] = model.predict_proba(X_scaled)[:, 1]
            else:
                predictions[name] = model.predict_proba(X_enc)[:, 1]
        
        # Stack and predict
        X_meta = np.column_stack([predictions[name] for name in sorted(predictions.keys())])
        ensemble_pred = self.meta_model.predict_proba(X_meta)[:, 1]
        
        return ensemble_pred, predictions

from sklearn.linear_model import LogisticRegression

def main():
    print("="*60)
    print("FLASH Fast Advanced Ensemble Training")
    print("="*60)
    
    # Load data
    print("\nLoading data...")
    df = pd.read_csv('data/final_100k_dataset_75features.csv')
    print(f"Loaded {len(df)} records")
    
    # Initialize ensemble
    ensemble = FastAdvancedEnsemble()
    ensemble.create_base_models()
    
    # Prepare data
    X, X_encoded, X_scaled, y, feature_cols, categorical_cols = ensemble.prepare_data(df)
    
    # Split data
    X_train, X_test, X_enc_train, X_enc_test, X_scaled_train, X_scaled_test, y_train, y_test = train_test_split(
        X, X_encoded, X_scaled, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # Further split train into train/val for stacking
    X_t, X_v, X_enc_t, X_enc_v, X_scaled_t, X_scaled_v, y_t, y_v = train_test_split(
        X_train, X_enc_train, X_scaled_train, y_train, test_size=0.2, random_state=42, stratify=y_train
    )
    
    print(f"\nDataset sizes:")
    print(f"  Train: {len(y_t)}")
    print(f"  Val: {len(y_v)}")
    print(f"  Test: {len(y_test)}")
    
    # Train base models
    print("\nTraining base models...")
    val_predictions = ensemble.train_models(
        X_t, X_enc_t, X_scaled_t, y_t,
        X_v, X_enc_v, X_scaled_v, y_v,
        categorical_cols
    )
    
    # Train stacking
    ensemble.train_stacking(val_predictions, y_v)
    
    # Evaluate on test set
    print("\n" + "="*60)
    print("TEST SET EVALUATION")
    print("="*60)
    
    test_pred, test_predictions = ensemble.predict_ensemble(
        X_test, X_enc_test, X_scaled_test, categorical_cols
    )
    
    # Calculate metrics
    test_auc = roc_auc_score(y_test, test_pred)
    test_acc = accuracy_score(y_test, (test_pred > 0.5).astype(int))
    test_f1 = f1_score(y_test, (test_pred > 0.5).astype(int))
    
    print(f"\nEnsemble Performance:")
    print(f"  AUC: {test_auc:.4f}")
    print(f"  Accuracy: {test_acc:.4f}")
    print(f"  F1: {test_f1:.4f}")
    
    print(f"\nIndividual Model Test Performance:")
    for name in sorted(test_predictions.keys()):
        auc = roc_auc_score(y_test, test_predictions[name])
        print(f"  {name}: {auc:.4f}")
    
    # Save results
    print("\nSaving models...")
    for name, model in ensemble.models.items():
        joblib.dump(model, f'models/advanced_ensemble_fast/{name}.pkl')
    
    joblib.dump(ensemble.meta_model, 'models/advanced_ensemble_fast/meta_model.pkl')
    joblib.dump(ensemble.encoders, 'models/advanced_ensemble_fast/encoders.pkl')
    joblib.dump(ensemble.scalers, 'models/advanced_ensemble_fast/scalers.pkl')
    
    # Save metadata
    metadata = {
        'test_auc': float(test_auc),
        'test_accuracy': float(test_acc),
        'test_f1': float(test_f1),
        'comparison': {
            'baseline_45_features': 0.773,
            'simple_75_features': 0.775,
            'advanced_ensemble': float(test_auc),
            'improvement_percentage': (test_auc - 0.773) * 100
        }
    }
    
    with open('models/advanced_ensemble_fast/results.json', 'w') as f:
        json.dump(metadata, f, indent=2)
    
    print("\n" + "="*60)
    print("FINAL RESULTS")
    print("="*60)
    print(f"Baseline (45 features): 77.3% AUC")
    print(f"Advanced Ensemble: {test_auc*100:.1f}% AUC")
    print(f"Improvement: +{(test_auc - 0.773)*100:.1f} percentage points")
    print("="*60)

if __name__ == "__main__":
    main()