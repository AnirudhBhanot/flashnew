#!/usr/bin/env python3
"""
Advanced Ensemble Architecture for FLASH V2
Implements diverse models with stacking to achieve 82-83% AUC
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
from sklearn.calibration import CalibratedClassifierCV
from sklearn.neural_network import MLPClassifier
from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier

import catboost as cb
from catboost import CatBoostClassifier
import xgboost as xgb
from xgboost import XGBClassifier
import lightgbm as lgb
from lightgbm import LGBMClassifier

from sklearn.neural_network import MLPRegressor
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import GradientBoostingClassifier

import os
os.makedirs('models/advanced_ensemble', exist_ok=True)

class AdvancedEnsemble:
    def __init__(self):
        self.models = {}
        self.feature_subsets = {}
        self.scalers = {}
        self.encoders = {}
        self.meta_model = None
        self.calibrators = {}
        self.feature_importance = {}
        
    def create_feature_subsets(self, feature_cols):
        """Define feature subsets for specialized models"""
        
        # Financial features
        self.feature_subsets['financial'] = [
            col for col in feature_cols if any(keyword in col.lower() for keyword in [
                'revenue', 'burn', 'cash', 'capital', 'margin', 'ltv', 'cac', 
                'cost', 'dollar', 'usd', 'efficiency', 'runway'
            ])
        ]
        
        # Team/People features
        self.feature_subsets['team'] = [
            col for col in feature_cols if any(keyword in col.lower() for keyword in [
                'founder', 'team', 'experience', 'advisor', 'person', 'employee',
                'diversity', 'expertise', 'exit'
            ])
        ]
        
        # Market/Competition features
        self.feature_subsets['market'] = [
            col for col in feature_cols if any(keyword in col.lower() for keyword in [
                'market', 'tam', 'sam', 'som', 'competition', 'competitor',
                'growth_rate', 'share', 'sector'
            ])
        ]
        
        # Product/Tech features
        self.feature_subsets['product'] = [
            col for col in feature_cols if any(keyword in col.lower() for keyword in [
                'product', 'retention', 'tech', 'patent', 'network', 'moat',
                'switch', 'brand', 'stage', 'dau', 'mau', 'user'
            ])
        ]
        
        # All features
        self.feature_subsets['all'] = feature_cols
        
        print("Feature subsets created:")
        for name, features in self.feature_subsets.items():
            print(f"  {name}: {len(features)} features")
    
    def create_base_models(self):
        """Create diverse base models"""
        
        # 1. CatBoost - Best performer from previous runs
        self.models['catboost_main'] = CatBoostClassifier(
            iterations=1500,
            learning_rate=0.03,
            depth=6,
            l2_leaf_reg=3,
            bagging_temperature=0.8,
            random_strength=0.8,
            border_count=128,
            grow_policy='Lossguide',
            max_leaves=64,
            random_state=42,
            verbose=False
        )
        
        # 2. XGBoost with different parameters
        self.models['xgboost_deep'] = XGBClassifier(
            n_estimators=1000,
            max_depth=8,
            learning_rate=0.02,
            subsample=0.7,
            colsample_bytree=0.7,
            gamma=0.1,
            reg_alpha=0.1,
            reg_lambda=1,
            random_state=42,
            eval_metric='auc',
            early_stopping_rounds=50
        )
        
        # 3. LightGBM with dart
        self.models['lightgbm_dart'] = LGBMClassifier(
            n_estimators=1000,
            learning_rate=0.03,
            num_leaves=64,
            max_depth=7,
            min_child_samples=20,
            subsample=0.8,
            colsample_bytree=0.8,
            reg_alpha=0.1,
            reg_lambda=0.1,
            boosting_type='dart',
            drop_rate=0.1,
            random_state=42,
            verbosity=-1
        )
        
        # 4. Random Forest for diversity
        self.models['random_forest'] = RandomForestClassifier(
            n_estimators=500,
            max_depth=12,
            min_samples_split=10,
            min_samples_leaf=5,
            max_features='sqrt',
            bootstrap=True,
            oob_score=True,
            random_state=42,
            n_jobs=-1
        )
        
        # 5. ExtraTrees for more randomness
        self.models['extra_trees'] = ExtraTreesClassifier(
            n_estimators=500,
            max_depth=12,
            min_samples_split=10,
            min_samples_leaf=5,
            max_features='sqrt',
            bootstrap=True,
            oob_score=True,
            random_state=42,
            n_jobs=-1
        )
        
        # 6. Neural Network
        self.models['neural_net'] = MLPClassifier(
            hidden_layer_sizes=(128, 64, 32),
            activation='relu',
            solver='adam',
            alpha=0.001,
            batch_size=256,
            learning_rate='adaptive',
            learning_rate_init=0.001,
            max_iter=300,
            early_stopping=True,
            validation_fraction=0.1,
            n_iter_no_change=20,
            random_state=42
        )
        
        # Feature subset models
        self.models['catboost_financial'] = CatBoostClassifier(
            iterations=800, learning_rate=0.05, depth=5, random_state=43, verbose=False
        )
        
        self.models['xgboost_team'] = XGBClassifier(
            n_estimators=600, max_depth=6, learning_rate=0.05, random_state=44
        )
        
        self.models['lightgbm_market'] = LGBMClassifier(
            n_estimators=600, num_leaves=32, learning_rate=0.05, random_state=45, verbosity=-1
        )
        
        self.models['catboost_product'] = CatBoostClassifier(
            iterations=800, learning_rate=0.05, depth=5, random_state=46, verbose=False
        )
    
    def create_neural_meta_learner(self, n_models):
        """Create a neural network for stacking using sklearn"""
        
        # Use MLPClassifier as meta-learner
        model = MLPClassifier(
            hidden_layer_sizes=(64, 32, 16),
            activation='relu',
            solver='adam',
            alpha=0.01,
            batch_size=256,
            learning_rate='adaptive',
            learning_rate_init=0.001,
            max_iter=500,
            early_stopping=True,
            validation_fraction=0.2,
            n_iter_no_change=20,
            random_state=42
        )
        
        return model
    
    def prepare_data(self, df):
        """Prepare data with proper encoding and scaling"""
        
        # Separate features and target
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
        
        # Scale numeric features for neural network
        self.scalers['standard'] = StandardScaler()
        X_scaled = X_encoded.copy()
        X_scaled[numeric_cols] = self.scalers['standard'].fit_transform(X_encoded[numeric_cols])
        
        return X, X_encoded, X_scaled, y, feature_cols, categorical_cols, numeric_cols
    
    def train_with_cross_validation(self, X, X_encoded, X_scaled, y, feature_cols, categorical_cols):
        """Train models using 5-fold CV for stacking"""
        
        n_folds = 5
        kf = StratifiedKFold(n_splits=n_folds, shuffle=True, random_state=42)
        
        # Store out-of-fold predictions
        oof_predictions = {}
        test_predictions = {}
        
        # Initialize
        for model_name in self.models.keys():
            oof_predictions[model_name] = np.zeros(len(y))
            test_predictions[model_name] = []
        
        # Train each model
        for model_name, model in self.models.items():
            print(f"\nTraining {model_name} with cross-validation...")
            
            # Determine which features to use
            if 'financial' in model_name:
                use_features = [f for f in self.feature_subsets['financial'] if f in feature_cols]
            elif 'team' in model_name:
                use_features = [f for f in self.feature_subsets['team'] if f in feature_cols]
            elif 'market' in model_name:
                use_features = [f for f in self.feature_subsets['market'] if f in feature_cols]
            elif 'product' in model_name:
                use_features = [f for f in self.feature_subsets['product'] if f in feature_cols]
            else:
                use_features = feature_cols
            
            # Cross-validation
            fold_aucs = []
            for fold, (train_idx, val_idx) in enumerate(kf.split(X, y)):
                X_train_fold = X.iloc[train_idx]
                X_val_fold = X.iloc[val_idx]
                y_train_fold = y.iloc[train_idx]
                y_val_fold = y.iloc[val_idx]
                
                # Use appropriate data format
                if 'catboost' in model_name:
                    # CatBoost handles categoricals directly
                    model_clone = model.__class__(**model.get_params())
                    # Identify categorical features in use_features
                    cat_features_indices = [i for i, f in enumerate(use_features) if f in categorical_cols]
                    model_clone.fit(
                        X_train_fold[use_features], y_train_fold,
                        cat_features=cat_features_indices,
                        eval_set=(X_val_fold[use_features], y_val_fold),
                        early_stopping_rounds=50,
                        verbose=False
                    )
                    val_pred = model_clone.predict_proba(X_val_fold[use_features])[:, 1]
                    
                elif 'neural' in model_name:
                    # Neural network needs scaled data
                    X_train_scaled = X_scaled.iloc[train_idx][use_features]
                    X_val_scaled = X_scaled.iloc[val_idx][use_features]
                    
                    model_clone = model.__class__(**model.get_params())
                    model_clone.fit(X_train_scaled, y_train_fold)
                    val_pred = model_clone.predict_proba(X_val_scaled)[:, 1]
                    
                else:
                    # Other models use encoded data
                    X_train_enc = X_encoded.iloc[train_idx][use_features]
                    X_val_enc = X_encoded.iloc[val_idx][use_features]
                    
                    model_clone = model.__class__(**model.get_params())
                    
                    if hasattr(model_clone, 'fit') and 'eval_set' in model_clone.fit.__code__.co_varnames:
                        # XGBoost/LightGBM with early stopping
                        if isinstance(model_clone, XGBClassifier):
                            model_clone.fit(
                                X_train_enc, y_train_fold,
                                eval_set=[(X_val_enc, y_val_fold)],
                                verbose=False
                            )
                        else:  # LightGBM
                            model_clone.fit(
                                X_train_enc, y_train_fold,
                                eval_set=[(X_val_enc, y_val_fold)],
                                callbacks=[lgb.early_stopping(50), lgb.log_evaluation(0)]
                            )
                    else:
                        model_clone.fit(X_train_enc, y_train_fold)
                    
                    val_pred = model_clone.predict_proba(X_val_enc)[:, 1]
                
                # Store out-of-fold predictions
                oof_predictions[model_name][val_idx] = val_pred
                
                # Calculate fold AUC
                fold_auc = roc_auc_score(y_val_fold, val_pred)
                fold_aucs.append(fold_auc)
            
            # Print model performance
            mean_auc = np.mean(fold_aucs)
            print(f"  {model_name} CV AUC: {mean_auc:.4f} (+/- {np.std(fold_aucs):.4f})")
            
            # Train final model on full data for test predictions
            if 'catboost' in model_name:
                cat_features_indices = [i for i, f in enumerate(use_features) if f in categorical_cols]
                model.fit(X[use_features], y, cat_features=cat_features_indices, verbose=False)
            elif 'neural' in model_name:
                model.fit(X_scaled[use_features], y)
            else:
                if hasattr(model, 'fit') and 'eval_set' in model.fit.__code__.co_varnames:
                    # For models that support eval_set but we're training on full data
                    if isinstance(model, XGBClassifier):
                        model.set_params(early_stopping_rounds=None)
                    model.fit(X_encoded[use_features], y)
                else:
                    model.fit(X_encoded[use_features], y)
        
        return oof_predictions
    
    def train_meta_learner(self, oof_predictions, y):
        """Train the neural network meta-learner"""
        
        print("\nTraining neural network meta-learner...")
        
        # Convert OOF predictions to array
        X_meta = np.column_stack([oof_predictions[model] for model in sorted(oof_predictions.keys())])
        
        # Create and train meta-learner
        self.meta_model = self.create_neural_meta_learner(X_meta.shape[1])
        
        # Train meta-learner
        self.meta_model.fit(X_meta, y)
        
        # Evaluate meta-model
        meta_pred = self.meta_model.predict_proba(X_meta)[:, 1]
        meta_auc = roc_auc_score(y, meta_pred)
        print(f"  Meta-learner training AUC: {meta_auc:.4f}")
        
        return X_meta
    
    def calibrate_probabilities(self, X_meta, y):
        """Apply probability calibration"""
        
        print("\nCalibrating probabilities...")
        
        # Get base predictions
        base_pred = self.meta_model.predict_proba(X_meta)[:, 1]
        
        # Calibrate using Platt scaling
        calibrator = CalibratedClassifierCV(
            estimator=None,
            method='sigmoid',
            cv=3
        )
        
        # Reshape for sklearn
        base_pred_2d = base_pred.reshape(-1, 1)
        
        # Create a dummy classifier that just returns the predictions
        from sklearn.base import BaseEstimator, ClassifierMixin
        
        class PreTrainedClassifier(BaseEstimator, ClassifierMixin):
            def __init__(self, predictions):
                self.predictions = predictions
                
            def fit(self, X, y):
                return self
                
            def predict_proba(self, X):
                # X contains indices
                probs = self.predictions[X.flatten()]
                return np.column_stack([1 - probs, probs])
        
        # Calibrate
        dummy_clf = PreTrainedClassifier(base_pred)
        indices = np.arange(len(base_pred)).reshape(-1, 1)
        
        self.calibrators['platt'] = CalibratedClassifierCV(
            base_estimator=dummy_clf,
            method='sigmoid',
            cv='prefit'
        )
        self.calibrators['platt'].fit(indices, y)
        
        # Evaluate calibration
        calibrated_pred = self.calibrators['platt'].predict_proba(indices)[:, 1]
        calibrated_auc = roc_auc_score(y, calibrated_pred)
        print(f"  Calibrated AUC: {calibrated_auc:.4f}")
    
    def predict(self, X, X_encoded, X_scaled, feature_cols):
        """Make predictions using the full ensemble"""
        
        predictions = {}
        
        # Get predictions from each base model
        for model_name, model in self.models.items():
            # Determine features
            if 'financial' in model_name:
                use_features = [f for f in self.feature_subsets['financial'] if f in feature_cols]
            elif 'team' in model_name:
                use_features = [f for f in self.feature_subsets['team'] if f in feature_cols]
            elif 'market' in model_name:
                use_features = [f for f in self.feature_subsets['market'] if f in feature_cols]
            elif 'product' in model_name:
                use_features = [f for f in self.feature_subsets['product'] if f in feature_cols]
            else:
                use_features = feature_cols
            
            # Predict
            if 'catboost' in model_name:
                predictions[model_name] = model.predict_proba(X[use_features])[:, 1]
            elif 'neural' in model_name:
                predictions[model_name] = model.predict_proba(X_scaled[use_features])[:, 1]
            else:
                predictions[model_name] = model.predict_proba(X_encoded[use_features])[:, 1]
        
        # Stack predictions
        X_meta = np.column_stack([predictions[model] for model in sorted(predictions.keys())])
        
        # Get meta predictions
        meta_pred = self.meta_model.predict_proba(X_meta)[:, 1]
        
        # Calibrate if available
        if 'platt' in self.calibrators:
            # We need to apply calibration differently for new data
            # For now, return uncalibrated predictions
            # In production, you'd save the calibration mapping
            final_pred = meta_pred
        else:
            final_pred = meta_pred
        
        return final_pred, predictions

def main():
    print("="*60)
    print("FLASH Advanced Ensemble Training")
    print("="*60)
    
    # Load data
    print("\nLoading data...")
    df = pd.read_csv('data/final_100k_dataset_75features.csv')
    print(f"Loaded {len(df)} records with {df.shape[1]} columns")
    
    # Initialize ensemble
    ensemble = AdvancedEnsemble()
    
    # Prepare data
    X, X_encoded, X_scaled, y, feature_cols, categorical_cols, numeric_cols = ensemble.prepare_data(df)
    
    # Create feature subsets
    ensemble.create_feature_subsets(feature_cols)
    
    # Create models
    ensemble.create_base_models()
    
    # Split data
    X_temp, X_test, X_temp_enc, X_test_enc, X_temp_scaled, X_test_scaled, y_temp, y_test = train_test_split(
        X, X_encoded, X_scaled, y, test_size=0.2, random_state=42, stratify=y
    )
    
    print(f"\nTraining set: {len(y_temp)} samples")
    print(f"Test set: {len(y_test)} samples")
    
    # Train with cross-validation
    oof_predictions = ensemble.train_with_cross_validation(
        X_temp, X_temp_enc, X_temp_scaled, y_temp, feature_cols, categorical_cols
    )
    
    # Train meta-learner
    X_meta_train = ensemble.train_meta_learner(oof_predictions, y_temp)
    
    # Calibrate
    ensemble.calibrate_probabilities(X_meta_train, y_temp)
    
    # Evaluate on test set
    print("\n" + "="*60)
    print("FINAL EVALUATION ON TEST SET")
    print("="*60)
    
    test_pred, test_predictions_dict = ensemble.predict(
        X_test, X_test_enc, X_test_scaled, feature_cols
    )
    
    # Calculate metrics
    test_auc = roc_auc_score(y_test, test_pred)
    test_acc = accuracy_score(y_test, (test_pred > 0.5).astype(int))
    test_f1 = f1_score(y_test, (test_pred > 0.5).astype(int))
    
    print(f"\nTest AUC: {test_auc:.4f}")
    print(f"Test Accuracy: {test_acc:.4f}")
    print(f"Test F1: {test_f1:.4f}")
    
    # Individual model performance
    print("\nIndividual Model Test Performance:")
    for model_name in sorted(test_predictions_dict.keys()):
        model_auc = roc_auc_score(y_test, test_predictions_dict[model_name])
        print(f"  {model_name}: {model_auc:.4f}")
    
    # Save models and metadata
    print("\nSaving models...")
    
    # Save base models
    for name, model in ensemble.models.items():
        joblib.dump(model, f'models/advanced_ensemble/{name}.pkl')
    
    # Save meta-model
    joblib.dump(ensemble.meta_model, 'models/advanced_ensemble/meta_model.pkl')
    
    # Save encoders and scalers
    joblib.dump(ensemble.encoders, 'models/advanced_ensemble/encoders.pkl')
    joblib.dump(ensemble.scalers, 'models/advanced_ensemble/scalers.pkl')
    joblib.dump(ensemble.feature_subsets, 'models/advanced_ensemble/feature_subsets.pkl')
    
    # Save metadata
    metadata = {
        'version': 'advanced_ensemble_v1',
        'training_date': datetime.now().isoformat(),
        'test_performance': {
            'auc': float(test_auc),
            'accuracy': float(test_acc),
            'f1': float(test_f1)
        },
        'model_count': len(ensemble.models),
        'feature_count': len(feature_cols),
        'comparison': {
            '45_features_baseline': 0.773,
            '75_features_simple': 0.775,
            'advanced_ensemble': float(test_auc),
            'improvement': float(test_auc) - 0.773
        }
    }
    
    with open('models/advanced_ensemble/metadata.json', 'w') as f:
        json.dump(metadata, f, indent=2)
    
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    print(f"Baseline (45 features): 77.3% AUC")
    print(f"Simple ensemble (75 features): 77.5% AUC")
    print(f"Advanced ensemble: {test_auc*100:.1f}% AUC")
    print(f"Total improvement: +{(test_auc - 0.773)*100:.1f}%")
    print("="*60)

if __name__ == "__main__":
    main()