#!/usr/bin/env python3
"""
Retrain Production Models on 100K Dataset
Maintains exact same model architecture as existing production models
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score, accuracy_score
import xgboost as xgb
import joblib
from pathlib import Path
import json
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Import CAMP features
from feature_config import ALL_FEATURES, CATEGORICAL_FEATURES

class ProductionModelRetrainer:
    """Retrain production models with same architecture"""
    
    def __init__(self):
        self.model_dir = Path("models/production_v45_fixed")
        self.model_dir.mkdir(parents=True, exist_ok=True)
        self.label_encoders = {}
        
    def load_and_prepare_data(self):
        """Load 100K dataset and prepare for training"""
        print("Loading 100K dataset...")
        df = pd.read_csv('real_startup_data_100k.csv')
        print(f"Loaded {len(df):,} companies with {df['success'].mean():.1%} success rate")
        
        # Prepare features
        X = df[ALL_FEATURES].copy()
        y = df['success'].copy()
        
        # Encode categorical features
        print("Encoding categorical features...")
        for col in CATEGORICAL_FEATURES:
            if col in X.columns:
                le = LabelEncoder()
                X[col] = le.fit_transform(X[col].astype(str))
                self.label_encoders[col] = le
        
        # Fill any missing values
        X = X.fillna(X.median())
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        print(f"Train: {len(X_train):,} | Test: {len(X_test):,}")
        
        return X_train, X_test, y_train, y_test, X.columns.tolist()
    
    def train_dna_analyzer(self, X_train, y_train, X_test, y_test):
        """Train DNA Analyzer - Random Forest model"""
        print("\n1. Training DNA Analyzer (Random Forest)...")
        
        # DNA Analyzer uses all 45 features
        model = RandomForestClassifier(
            n_estimators=200,
            max_depth=15,
            min_samples_split=10,
            min_samples_leaf=5,
            class_weight='balanced',
            random_state=42,
            n_jobs=-1
        )
        
        model.fit(X_train, y_train)
        
        # Evaluate
        y_pred_proba = model.predict_proba(X_test)[:, 1]
        auc = roc_auc_score(y_test, y_pred_proba)
        acc = accuracy_score(y_test, (y_pred_proba >= 0.5).astype(int))
        
        print(f"   AUC: {auc:.4f}")
        print(f"   Accuracy: {acc:.3f}")
        
        # Save model
        joblib.dump(model, self.model_dir / 'dna_analyzer.pkl')
        
        # Save feature order (important for API compatibility)
        joblib.dump(X_train.columns.tolist(), self.model_dir / 'dna_feature_order.pkl')
        
        return auc
    
    def train_temporal_model(self, X_train, y_train, X_test, y_test):
        """Train Temporal Model - XGBoost with temporal features"""
        print("\n2. Training Temporal Model (XGBoost)...")
        
        # Add temporal features
        X_train_temp = X_train.copy()
        X_test_temp = X_test.copy()
        
        # Add momentum features
        X_train_temp['revenue_momentum'] = X_train_temp['revenue_growth_rate_percent'] * X_train_temp['net_dollar_retention_percent'] / 100
        X_test_temp['revenue_momentum'] = X_test_temp['revenue_growth_rate_percent'] * X_test_temp['net_dollar_retention_percent'] / 100
        
        X_train_temp['burn_momentum'] = X_train_temp['monthly_burn_usd'] / (X_train_temp['runway_months'] + 1)
        X_test_temp['burn_momentum'] = X_test_temp['monthly_burn_usd'] / (X_test_temp['runway_months'] + 1)
        
        X_train_temp['growth_efficiency'] = X_train_temp['user_growth_rate_percent'] / (X_train_temp['burn_multiple'] + 1)
        X_test_temp['growth_efficiency'] = X_test_temp['user_growth_rate_percent'] / (X_test_temp['burn_multiple'] + 1)
        
        # Train model
        model = xgb.XGBClassifier(
            n_estimators=200,
            max_depth=6,
            learning_rate=0.1,
            subsample=0.8,
            colsample_bytree=0.8,
            scale_pos_weight=(y_train == 0).sum() / (y_train == 1).sum(),
            random_state=42,
            n_jobs=-1
        )
        
        model.fit(X_train_temp, y_train)
        
        # Evaluate
        y_pred_proba = model.predict_proba(X_test_temp)[:, 1]
        auc = roc_auc_score(y_test, y_pred_proba)
        acc = accuracy_score(y_test, (y_pred_proba >= 0.5).astype(int))
        
        print(f"   AUC: {auc:.4f}")
        print(f"   Accuracy: {acc:.3f}")
        
        # Save model
        joblib.dump(model, self.model_dir / 'temporal_model.pkl')
        joblib.dump(X_train_temp.columns.tolist(), self.model_dir / 'temporal_feature_order.pkl')
        
        return auc
    
    def train_industry_model(self, X_train, y_train, X_test, y_test):
        """Train Industry-Specific Model - XGBoost with industry focus"""
        print("\n3. Training Industry Model (XGBoost)...")
        
        # Industry model uses standard features but with different weights
        model = xgb.XGBClassifier(
            n_estimators=200,
            max_depth=8,
            learning_rate=0.1,
            subsample=0.8,
            colsample_bytree=0.8,
            scale_pos_weight=(y_train == 0).sum() / (y_train == 1).sum(),
            random_state=42,
            n_jobs=-1
        )
        
        # Scale features for industry model
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        
        model.fit(X_train_scaled, y_train)
        
        # Evaluate
        y_pred_proba = model.predict_proba(X_test_scaled)[:, 1]
        auc = roc_auc_score(y_test, y_pred_proba)
        acc = accuracy_score(y_test, (y_pred_proba >= 0.5).astype(int))
        
        print(f"   AUC: {auc:.4f}")
        print(f"   Accuracy: {acc:.3f}")
        
        # Save model and scaler
        joblib.dump(model, self.model_dir / 'industry_model.pkl')
        joblib.dump(scaler, self.model_dir / 'industry_scaler.pkl')
        joblib.dump(X_train.columns.tolist(), self.model_dir / 'industry_feature_order.pkl')
        
        return auc
    
    def train_ensemble_model(self, X_train, y_train, X_test, y_test):
        """Train Ensemble Model - Combines predictions from all models"""
        print("\n4. Training Ensemble Model...")
        
        # Load the three models we just trained
        dna_model = joblib.load(self.model_dir / 'dna_analyzer.pkl')
        temporal_model = joblib.load(self.model_dir / 'temporal_model.pkl')
        industry_model = joblib.load(self.model_dir / 'industry_model.pkl')
        industry_scaler = joblib.load(self.model_dir / 'industry_scaler.pkl')
        
        # Get predictions from each model
        print("   Getting base model predictions...")
        
        # DNA predictions
        dna_train = dna_model.predict_proba(X_train)[:, 1]
        dna_test = dna_model.predict_proba(X_test)[:, 1]
        
        # Temporal predictions (need temporal features)
        X_train_temp = X_train.copy()
        X_test_temp = X_test.copy()
        X_train_temp['revenue_momentum'] = X_train_temp['revenue_growth_rate_percent'] * X_train_temp['net_dollar_retention_percent'] / 100
        X_test_temp['revenue_momentum'] = X_test_temp['revenue_growth_rate_percent'] * X_test_temp['net_dollar_retention_percent'] / 100
        X_train_temp['burn_momentum'] = X_train_temp['monthly_burn_usd'] / (X_train_temp['runway_months'] + 1)
        X_test_temp['burn_momentum'] = X_test_temp['monthly_burn_usd'] / (X_test_temp['runway_months'] + 1)
        X_train_temp['growth_efficiency'] = X_train_temp['user_growth_rate_percent'] / (X_train_temp['burn_multiple'] + 1)
        X_test_temp['growth_efficiency'] = X_test_temp['user_growth_rate_percent'] / (X_test_temp['burn_multiple'] + 1)
        
        temporal_train = temporal_model.predict_proba(X_train_temp)[:, 1]
        temporal_test = temporal_model.predict_proba(X_test_temp)[:, 1]
        
        # Industry predictions (scaled)
        X_train_scaled = industry_scaler.transform(X_train)
        X_test_scaled = industry_scaler.transform(X_test)
        industry_train = industry_model.predict_proba(X_train_scaled)[:, 1]
        industry_test = industry_model.predict_proba(X_test_scaled)[:, 1]
        
        # Create ensemble features
        X_ensemble_train = np.column_stack([dna_train, temporal_train, industry_train])
        X_ensemble_test = np.column_stack([dna_test, temporal_test, industry_test])
        
        # Train ensemble (Random Forest for robustness)
        ensemble = RandomForestClassifier(
            n_estimators=100,
            max_depth=5,
            random_state=42,
            n_jobs=-1
        )
        
        ensemble.fit(X_ensemble_train, y_train)
        
        # Evaluate
        y_pred_proba = ensemble.predict_proba(X_ensemble_test)[:, 1]
        auc = roc_auc_score(y_test, y_pred_proba)
        acc = accuracy_score(y_test, (y_pred_proba >= 0.5).astype(int))
        
        print(f"   AUC: {auc:.4f}")
        print(f"   Accuracy: {acc:.3f}")
        
        # Save ensemble
        joblib.dump(ensemble, self.model_dir / 'ensemble_model.pkl')
        
        return auc
    
    def save_metadata(self, results):
        """Save training metadata"""
        metadata = {
            'training_date': datetime.now().isoformat(),
            'dataset': 'real_startup_data_100k.csv',
            'dataset_size': 100000,
            'model_performance': results,
            'model_types': {
                'dna_analyzer': 'RandomForestClassifier',
                'temporal_model': 'XGBClassifier',
                'industry_model': 'XGBClassifier', 
                'ensemble_model': 'RandomForestClassifier'
            }
        }
        
        with open(self.model_dir / 'training_metadata.json', 'w') as f:
            json.dump(metadata, f, indent=2)
        
        # Save label encoders
        joblib.dump(self.label_encoders, self.model_dir / 'label_encoders.pkl')
        
        # Update production manifest
        manifest = {
            'version': '4.0-100k-real-data',
            'created_at': datetime.now().isoformat(),
            'models': {
                'dna_analyzer': {
                    'path': 'models/production_v45_fixed/dna_analyzer.pkl',
                    'type': 'RandomForestClassifier',
                    'features': 45,
                    'auc': results['dna_analyzer'],
                    'description': 'DNA Analyzer trained on 100k real startups'
                },
                'temporal_model': {
                    'path': 'models/production_v45_fixed/temporal_model.pkl',
                    'type': 'XGBClassifier',
                    'features': 48,  # 45 + 3 temporal
                    'auc': results['temporal_model'],
                    'description': 'Temporal model with momentum features'
                },
                'industry_model': {
                    'path': 'models/production_v45_fixed/industry_model.pkl',
                    'type': 'XGBClassifier',
                    'features': 45,
                    'auc': results['industry_model'],
                    'description': 'Industry-specific patterns model'
                },
                'ensemble_model': {
                    'path': 'models/production_v45_fixed/ensemble_model.pkl',
                    'type': 'RandomForestClassifier',
                    'features': 3,  # 3 model predictions
                    'auc': results['ensemble_model'],
                    'description': 'Ensemble combining all models'
                }
            },
            'training_data': {
                'size': 100000,
                'success_rate': 0.162,
                'source': '100k realistic dataset with YC, unicorns, failures',
                'features': 45
            }
        }
        
        with open('models/production_manifest.json', 'w') as f:
            json.dump(manifest, f, indent=2)


def main():
    """Main training pipeline"""
    print("\n" + "="*80)
    print("RETRAINING PRODUCTION MODELS ON 100K DATASET")
    print("="*80)
    
    trainer = ProductionModelRetrainer()
    
    # Load and prepare data
    X_train, X_test, y_train, y_test, feature_names = trainer.load_and_prepare_data()
    
    # Train all models
    results = {}
    
    # 1. DNA Analyzer
    results['dna_analyzer'] = trainer.train_dna_analyzer(X_train, y_train, X_test, y_test)
    
    # 2. Temporal Model
    results['temporal_model'] = trainer.train_temporal_model(X_train, y_train, X_test, y_test)
    
    # 3. Industry Model
    results['industry_model'] = trainer.train_industry_model(X_train, y_train, X_test, y_test)
    
    # 4. Ensemble Model
    results['ensemble_model'] = trainer.train_ensemble_model(X_train, y_train, X_test, y_test)
    
    # Save metadata
    trainer.save_metadata(results)
    
    # Summary
    print("\n" + "="*80)
    print("RETRAINING COMPLETE!")
    print("="*80)
    print("\nModel Performance Summary:")
    for model, auc in results.items():
        print(f"  {model}: {auc:.4f} AUC")
    print(f"\nAverage AUC: {np.mean(list(results.values())):.4f}")
    print(f"\nModels saved to: {trainer.model_dir}")
    print("\n✅ Production models successfully retrained on 100K dataset!")
    print("✅ API will automatically use the new models")
    print("="*80)


if __name__ == "__main__":
    main()