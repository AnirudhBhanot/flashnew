#!/usr/bin/env python3
"""
Train FLASH V2 models with 75 features
Implements ensemble of CatBoost, XGBoost, LightGBM with proper validation
"""
import numpy as np
import pandas as pd
import json
import joblib
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

from sklearn.model_selection import StratifiedKFold, train_test_split
from sklearn.metrics import roc_auc_score, accuracy_score, f1_score, precision_recall_curve
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import VotingClassifier, StackingClassifier
from sklearn.linear_model import LogisticRegression

import catboost as cb
from catboost import CatBoostClassifier
import xgboost as xgb
from xgboost import XGBClassifier
import lightgbm as lgb
from lightgbm import LGBMClassifier

import matplotlib.pyplot as plt
import seaborn as sns

class FlashV2Trainer:
    """Train ensemble models on 75-feature dataset"""
    
    def __init__(self):
        self.models = {}
        self.label_encoders = {}
        self.feature_importance = {}
        self.performance_metrics = {}
        
        # Define feature groups
        self.categorical_features = [
            'funding_stage', 'investor_tier_primary', 'product_stage', 'sector',
            'gross_margin_trend', 'burn_multiple_trend', 'revenue_per_employee_trend',
            'sales_cycle_trend'
        ]
        
        # Features to exclude from training
        self.exclude_features = [
            'startup_id', 'startup_name', 'founding_year', 'success',
            'burn_multiple_calc'  # This seems to be a duplicate
        ]
        
    def prepare_data(self, df):
        """Prepare data for training"""
        print("Preparing data...")
        
        # Get feature columns
        feature_cols = [col for col in df.columns if col not in self.exclude_features]
        
        # Handle missing values
        # For numeric features, fill with median
        numeric_features = [f for f in feature_cols if f not in self.categorical_features]
        for feat in numeric_features:
            if df[feat].isnull().any():
                median_val = df[feat].median()
                df[feat] = df[feat].fillna(median_val)
                print(f"  Filled {feat} nulls with median: {median_val:.2f}")
        
        # For categorical features, fill with mode or 'unknown'
        for feat in self.categorical_features:
            if feat in df.columns and df[feat].isnull().any():
                mode_val = df[feat].mode()[0] if len(df[feat].mode()) > 0 else 'unknown'
                df[feat] = df[feat].fillna(mode_val)
                print(f"  Filled {feat} nulls with mode: {mode_val}")
        
        # Encode categorical features for non-CatBoost models
        df_encoded = df.copy()
        for feat in self.categorical_features:
            if feat in df_encoded.columns:
                le = LabelEncoder()
                # Handle unknown categories
                df_encoded[feat] = df_encoded[feat].astype(str)
                df_encoded[feat + '_encoded'] = le.fit_transform(df_encoded[feat])
                self.label_encoders[feat] = le
        
        return df, df_encoded, feature_cols
    
    def create_models(self):
        """Create diverse ensemble of models"""
        
        # Get categorical indices for CatBoost
        cat_indices = [i for i, f in enumerate(self.feature_cols) 
                      if f in self.categorical_features]
        
        models = {
            # CatBoost - handles categoricals natively
            'catboost_1': CatBoostClassifier(
                iterations=1500,
                learning_rate=0.02,
                depth=8,
                l2_leaf_reg=3,
                subsample=0.8,
                random_strength=0.5,
                cat_features=cat_indices,
                loss_function='Logloss',
                eval_metric='AUC',
                random_seed=42,
                verbose=False
            ),
            
            'catboost_2': CatBoostClassifier(
                iterations=1000,
                learning_rate=0.05,
                depth=6,
                l2_leaf_reg=5,
                subsample=0.85,
                grow_policy='Lossguide',
                cat_features=cat_indices,
                random_seed=43,
                verbose=False
            ),
            
            # XGBoost - different objective
            'xgboost': XGBClassifier(
                n_estimators=1000,
                learning_rate=0.02,
                max_depth=8,
                subsample=0.8,
                colsample_bytree=0.8,
                objective='binary:logistic',
                eval_metric='auc',
                random_state=42,
                use_label_encoder=False
            ),
            
            # LightGBM - different architecture
            'lightgbm': LGBMClassifier(
                n_estimators=1000,
                learning_rate=0.02,
                num_leaves=64,
                subsample=0.8,
                colsample_bytree=0.8,
                objective='binary',
                metric='auc',
                random_state=42,
                verbose=-1
            )
        }
        
        return models
    
    def train_with_validation(self, X_train, X_train_encoded, y_train, X_val, X_val_encoded, y_val):
        """Train models with validation set"""
        
        results = {}
        
        for name, model in self.models.items():
            print(f"\nTraining {name}...")
            
            if 'catboost' in name:
                # CatBoost uses original features with categoricals
                model.fit(
                    X_train[self.feature_cols], y_train,
                    eval_set=(X_val[self.feature_cols], y_val),
                    early_stopping_rounds=50,
                    verbose=100
                )
                val_pred = model.predict_proba(X_val[self.feature_cols])[:, 1]
                
                # Get feature importance
                self.feature_importance[name] = pd.DataFrame({
                    'feature': self.feature_cols,
                    'importance': model.feature_importances_
                }).sort_values('importance', ascending=False)
                
            else:
                # XGBoost and LightGBM use encoded features
                # Get encoded feature columns
                encoded_cols = []
                for col in self.feature_cols:
                    if col in self.categorical_features:
                        encoded_cols.append(col + '_encoded')
                    else:
                        encoded_cols.append(col)
                
                if 'lightgbm' in name:
                    # LightGBM requires callbacks for early stopping
                    model.fit(
                        X_train_encoded[encoded_cols], y_train,
                        eval_set=[(X_val_encoded[encoded_cols], y_val)],
                        callbacks=[lgb.early_stopping(50), lgb.log_evaluation(0)]
                    )
                else:
                    # XGBoost uses early_stopping_rounds parameter
                    model.fit(
                        X_train_encoded[encoded_cols], y_train,
                        eval_set=[(X_val_encoded[encoded_cols], y_val)],
                        early_stopping_rounds=50,
                        verbose=False
                    )
                val_pred = model.predict_proba(X_val_encoded[encoded_cols])[:, 1]
                
                # Get feature importance
                self.feature_importance[name] = pd.DataFrame({
                    'feature': encoded_cols,
                    'importance': model.feature_importances_
                }).sort_values('importance', ascending=False)
            
            # Calculate metrics
            val_auc = roc_auc_score(y_val, val_pred)
            results[name] = {
                'val_auc': val_auc,
                'val_predictions': val_pred
            }
            
            print(f"  Validation AUC: {val_auc:.4f}")
        
        return results
    
    def create_ensemble(self, X_train, X_train_encoded, y_train, val_predictions):
        """Create stacking ensemble"""
        print("\nCreating stacking ensemble...")
        
        # Create blend features from validation predictions
        blend_features = pd.DataFrame(val_predictions)
        
        # Add statistical features
        blend_features['mean'] = blend_features.mean(axis=1)
        blend_features['std'] = blend_features.std(axis=1)
        blend_features['max'] = blend_features.max(axis=1)
        blend_features['min'] = blend_features.min(axis=1)
        
        # Train meta-learner
        meta_model = LogisticRegression(C=0.1, random_state=42)
        meta_model.fit(blend_features, y_train)
        
        self.models['meta_learner'] = meta_model
        
        return meta_model
    
    def evaluate_on_test(self, X_test, X_test_encoded, y_test):
        """Evaluate ensemble on test set"""
        print("\nEvaluating on test set...")
        
        # Get predictions from each model
        test_predictions = {}
        
        for name, model in self.models.items():
            if name == 'meta_learner':
                continue
                
            if 'catboost' in name:
                test_predictions[name] = model.predict_proba(X_test[self.feature_cols])[:, 1]
            else:
                # Get encoded columns
                encoded_cols = []
                for col in self.feature_cols:
                    if col in self.categorical_features:
                        encoded_cols.append(col + '_encoded')
                    else:
                        encoded_cols.append(col)
                
                test_predictions[name] = model.predict_proba(X_test_encoded[encoded_cols])[:, 1]
        
        # Create blend features
        blend_features = pd.DataFrame(test_predictions)
        blend_features['mean'] = blend_features.mean(axis=1)
        blend_features['std'] = blend_features.std(axis=1)
        blend_features['max'] = blend_features.max(axis=1)
        blend_features['min'] = blend_features.min(axis=1)
        
        # Get ensemble prediction
        ensemble_pred = self.models['meta_learner'].predict_proba(blend_features)[:, 1]
        
        # Calculate metrics
        test_auc = roc_auc_score(y_test, ensemble_pred)
        test_pred_binary = (ensemble_pred > 0.5).astype(int)
        test_accuracy = accuracy_score(y_test, test_pred_binary)
        test_f1 = f1_score(y_test, test_pred_binary)
        
        print("\n" + "="*50)
        print("TEST SET PERFORMANCE (75 Features)")
        print("="*50)
        print(f"AUC: {test_auc:.4f}")
        print(f"Accuracy: {test_accuracy:.4f}")
        print(f"F1 Score: {test_f1:.4f}")
        
        # Individual model performance
        print("\nIndividual Model Performance:")
        for name, pred in test_predictions.items():
            auc = roc_auc_score(y_test, pred)
            print(f"  {name}: {auc:.4f}")
        
        # Store metrics
        self.performance_metrics = {
            'test_auc': test_auc,
            'test_accuracy': test_accuracy,
            'test_f1': test_f1,
            'individual_aucs': {name: roc_auc_score(y_test, pred) 
                               for name, pred in test_predictions.items()}
        }
        
        return ensemble_pred
    
    def plot_feature_importance(self, top_n=30):
        """Plot top feature importances"""
        # Average importance across models
        all_features = set()
        for fi in self.feature_importance.values():
            all_features.update(fi['feature'].values)
        
        avg_importance = {}
        for feat in all_features:
            importances = []
            for model_fi in self.feature_importance.values():
                if feat in model_fi['feature'].values:
                    imp = model_fi[model_fi['feature'] == feat]['importance'].values[0]
                    importances.append(imp)
            if importances:
                avg_importance[feat] = np.mean(importances)
        
        # Sort and get top features
        top_features = sorted(avg_importance.items(), key=lambda x: x[1], reverse=True)[:top_n]
        
        # Plot
        plt.figure(figsize=(10, 8))
        features, importances = zip(*top_features)
        
        # Color by feature category
        colors = []
        for feat in features:
            if any(x in feat for x in ['revenue', 'burn', 'funding', 'cash', 'margin']):
                colors.append('blue')  # Capital
            elif any(x in feat for x in ['customer', 'competitive', 'organic', 'pilot']):
                colors.append('green')  # Advantage
            elif any(x in feat for x in ['market', 'category', 'competitor', 'expansion']):
                colors.append('orange')  # Market
            elif any(x in feat for x in ['founder', 'team', 'employee', 'technical']):
                colors.append('red')  # People
            else:
                colors.append('gray')
        
        plt.barh(range(len(features)), importances, color=colors)
        plt.yticks(range(len(features)), features)
        plt.xlabel('Average Feature Importance')
        plt.title(f'Top {top_n} Feature Importances (75-Feature Model)')
        plt.tight_layout()
        plt.savefig('/Users/sf/Desktop/FLASH/feature_importance_v2.png')
        plt.close()
        
        print(f"\nFeature importance plot saved to feature_importance_v2.png")
    
    def save_models(self, output_dir="/Users/sf/Desktop/FLASH/models/v2_75features"):
        """Save all models and metadata"""
        import os
        os.makedirs(output_dir, exist_ok=True)
        
        print(f"\nSaving models to {output_dir}")
        
        # Save individual models
        for name, model in self.models.items():
            if 'catboost' in name:
                model.save_model(f"{output_dir}/{name}.cbm")
            else:
                joblib.dump(model, f"{output_dir}/{name}.pkl")
        
        # Save label encoders
        joblib.dump(self.label_encoders, f"{output_dir}/label_encoders.pkl")
        
        # Save metadata
        metadata = {
            'version': '2.0-75features',
            'training_date': datetime.now().isoformat(),
            'features_count': len(self.feature_cols),
            'categorical_features': self.categorical_features,
            'performance_metrics': self.performance_metrics,
            'feature_columns': self.feature_cols
        }
        
        with open(f"{output_dir}/metadata.json", 'w') as f:
            json.dump(metadata, f, indent=2)
        
        # Save feature importance
        for name, fi in self.feature_importance.items():
            fi.to_csv(f"{output_dir}/feature_importance_{name}.csv", index=False)
        
        print("✓ All models and metadata saved successfully!")
    
    def train_full_pipeline(self, data_path):
        """Run complete training pipeline"""
        print("="*60)
        print("FLASH V2 Training Pipeline (75 Features)")
        print("="*60)
        
        # Load data
        print(f"\nLoading data from {data_path}")
        df = pd.read_csv(data_path)
        print(f"Loaded {len(df)} records with {len(df.columns)} columns")
        
        # Prepare data
        df, df_encoded, feature_cols = self.prepare_data(df)
        self.feature_cols = feature_cols
        print(f"\nUsing {len(feature_cols)} features for training")
        
        # Split data
        X = df[feature_cols]
        y = df['success'].astype(int)
        
        # First split: train+val vs test
        X_trainval, X_test, y_trainval, y_test = train_test_split(
            df, y, test_size=0.2, random_state=42, stratify=y
        )
        
        # Second split: train vs val
        X_train, X_val, y_train, y_val = train_test_split(
            X_trainval, y_trainval, test_size=0.2, random_state=42, stratify=y_trainval
        )
        
        # Also split encoded versions
        X_trainval_enc, X_test_enc = train_test_split(
            df_encoded, test_size=0.2, random_state=42, stratify=y
        )[0:2]
        
        X_train_enc, X_val_enc = train_test_split(
            X_trainval_enc, test_size=0.2, random_state=42, stratify=y_trainval
        )[0:2]
        
        print(f"\nDataset splits:")
        print(f"  Train: {len(X_train)} ({y_train.mean():.1%} positive)")
        print(f"  Val: {len(X_val)} ({y_val.mean():.1%} positive)")
        print(f"  Test: {len(X_test)} ({y_test.mean():.1%} positive)")
        
        # Create models
        self.models = self.create_models()
        
        # Train models
        val_results = self.train_with_validation(
            X_train, X_train_enc, y_train,
            X_val, X_val_enc, y_val
        )
        
        # Create ensemble
        val_predictions = {name: res['val_predictions'] 
                          for name, res in val_results.items()}
        self.create_ensemble(X_val, X_val_enc, y_val, val_predictions)
        
        # Evaluate on test set
        test_predictions = self.evaluate_on_test(X_test, X_test_enc, y_test)
        
        # Plot feature importance
        self.plot_feature_importance()
        
        # Save everything
        self.save_models()
        
        print("\n" + "="*60)
        print("Training Complete!")
        print("="*60)
        
        return self


def main():
    """Main training function"""
    data_path = "/Users/sf/Desktop/FLASH/data/final_100k_dataset_75features.csv"
    
    trainer = FlashV2Trainer()
    trainer.train_full_pipeline(data_path)
    
    # Compare with 45-feature baseline
    print("\nComparison with 45-feature baseline:")
    print("45 features: 77.3% AUC")
    print(f"75 features: {trainer.performance_metrics['test_auc']:.1%} AUC")
    print(f"Improvement: +{(trainer.performance_metrics['test_auc'] - 0.773)*100:.1f}%")


if __name__ == "__main__":
    main()