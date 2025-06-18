#!/usr/bin/env python3
"""
Complete Pattern Model Training with Exact Dataset Feature Alignment
This script trains pattern models using the exact same features as in the dataset
"""

import pandas as pd
import numpy as np
from pathlib import Path
import joblib
import logging
import json
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score, roc_auc_score, classification_report
from sklearn.preprocessing import StandardScaler, LabelEncoder
import warnings
warnings.filterwarnings('ignore')

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Import the fixed feature configuration
from feature_config_fixed import (
    ALL_FEATURES, CAPITAL_FEATURES, ADVANTAGE_FEATURES, 
    MARKET_FEATURES, PEOPLE_FEATURES, CATEGORICAL_FEATURES
)

class PatternModelTrainer:
    """Trains models for pattern classification with proper feature alignment"""
    
    def __init__(self, data_path="data/final_100k_dataset_45features.csv"):
        self.data_path = data_path
        self.models = {}
        self.scalers = {}
        self.encoders = {}
        self.feature_orders = {}
        
    def load_and_prepare_data(self):
        """Load the dataset and prepare features"""
        logger.info(f"Loading dataset from {self.data_path}")
        df = pd.read_csv(self.data_path)
        logger.info(f"Dataset shape: {df.shape}")
        
        # Get the exact column order from the dataset
        dataset_columns = list(df.columns)
        logger.info(f"Dataset has {len(dataset_columns)} columns")
        
        # Extract only the 45 features we need (excluding metadata columns)
        feature_columns = []
        for col in dataset_columns:
            if col in ALL_FEATURES:
                feature_columns.append(col)
        
        logger.info(f"Found {len(feature_columns)} feature columns matching ALL_FEATURES")
        
        # Verify we have all 45 features
        missing_features = set(ALL_FEATURES) - set(feature_columns)
        if missing_features:
            logger.error(f"Missing features in dataset: {missing_features}")
            raise ValueError(f"Dataset missing required features: {missing_features}")
        
        # Store the exact feature order from the dataset
        self.feature_order = feature_columns
        
        # Extract features and target
        X = df[feature_columns].copy()
        y = df['success'].copy()
        
        logger.info(f"Features shape: {X.shape}, Target shape: {y.shape}")
        logger.info(f"Success rate: {y.mean():.2%}")
        
        # Handle missing values
        X = self._handle_missing_values(X)
        
        # Encode categorical features
        X_encoded = self._encode_features(X)
        
        return X_encoded, y, X
    
    def _handle_missing_values(self, X):
        """Handle missing values in the dataset"""
        # Check for missing values
        missing_counts = X.isnull().sum()
        if missing_counts.any():
            logger.warning(f"Found missing values:\n{missing_counts[missing_counts > 0]}")
            
            # Fill numeric features with median
            numeric_features = X.select_dtypes(include=[np.number]).columns
            for col in numeric_features:
                if X[col].isnull().any():
                    X[col].fillna(X[col].median(), inplace=True)
            
            # Fill categorical features with mode
            categorical_features = X.select_dtypes(include=['object']).columns
            for col in categorical_features:
                if X[col].isnull().any():
                    X[col].fillna(X[col].mode()[0] if not X[col].mode().empty else 'unknown', inplace=True)
        
        return X
    
    def _encode_features(self, X):
        """Encode categorical features"""
        X_encoded = X.copy()
        
        # Identify categorical columns in the dataset
        categorical_cols = []
        for col in X.columns:
            if col in CATEGORICAL_FEATURES or X[col].dtype == 'object':
                categorical_cols.append(col)
        
        logger.info(f"Encoding {len(categorical_cols)} categorical features: {categorical_cols}")
        
        # Encode each categorical feature
        for col in categorical_cols:
            le = LabelEncoder()
            X_encoded[col] = le.fit_transform(X[col].astype(str))
            self.encoders[col] = le
            logger.info(f"  {col}: {len(le.classes_)} unique values")
        
        return X_encoded
    
    def train_pillar_models(self, X, y):
        """Train models for each CAMP pillar"""
        logger.info("\nTraining pillar models...")
        
        # Define pillars with their features
        pillars = {
            'capital': CAPITAL_FEATURES,
            'advantage': ADVANTAGE_FEATURES,
            'market': MARKET_FEATURES,
            'people': PEOPLE_FEATURES
        }
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        results = {}
        
        for pillar_name, pillar_features in pillars.items():
            logger.info(f"\nTraining {pillar_name} model with {len(pillar_features)} features...")
            
            # Get the features for this pillar in the correct order
            pillar_feature_indices = [i for i, col in enumerate(self.feature_order) if col in pillar_features]
            pillar_feature_names = [self.feature_order[i] for i in pillar_feature_indices]
            
            # Extract pillar features
            X_pillar_train = X_train.iloc[:, pillar_feature_indices]
            X_pillar_test = X_test.iloc[:, pillar_feature_indices]
            
            # Scale features
            scaler = StandardScaler()
            X_pillar_train_scaled = scaler.fit_transform(X_pillar_train)
            X_pillar_test_scaled = scaler.transform(X_pillar_test)
            self.scalers[pillar_name] = scaler
            
            # Train model with optimized hyperparameters
            model = GradientBoostingClassifier(
                n_estimators=100,
                learning_rate=0.1,
                max_depth=5,
                min_samples_split=20,
                min_samples_leaf=10,
                subsample=0.8,
                random_state=42
            )
            
            model.fit(X_pillar_train_scaled, y_train)
            
            # Evaluate
            train_pred = model.predict(X_pillar_train_scaled)
            test_pred = model.predict(X_pillar_test_scaled)
            train_pred_proba = model.predict_proba(X_pillar_train_scaled)[:, 1]
            test_pred_proba = model.predict_proba(X_pillar_test_scaled)[:, 1]
            
            train_acc = accuracy_score(y_train, train_pred)
            test_acc = accuracy_score(y_test, test_pred)
            train_auc = roc_auc_score(y_train, train_pred_proba)
            test_auc = roc_auc_score(y_test, test_pred_proba)
            
            logger.info(f"  Train - Accuracy: {train_acc:.3f}, AUC: {train_auc:.3f}")
            logger.info(f"  Test  - Accuracy: {test_acc:.3f}, AUC: {test_auc:.3f}")
            
            # Cross-validation
            cv_scores = cross_val_score(model, X_pillar_train_scaled, y_train, cv=5, scoring='roc_auc')
            logger.info(f"  CV AUC: {cv_scores.mean():.3f} (+/- {cv_scores.std() * 2:.3f})")
            
            # Store results
            self.models[pillar_name] = model
            self.feature_orders[pillar_name] = pillar_feature_names
            
            results[pillar_name] = {
                'n_features': len(pillar_features),
                'features': pillar_feature_names,
                'feature_indices': pillar_feature_indices,
                'train_accuracy': train_acc,
                'test_accuracy': test_acc,
                'train_auc': train_auc,
                'test_auc': test_auc,
                'cv_auc_mean': cv_scores.mean(),
                'cv_auc_std': cv_scores.std()
            }
        
        return results
    
    def train_ensemble_model(self, X, y):
        """Train an ensemble model using all features"""
        logger.info("\nTraining ensemble pattern model...")
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        # Scale features
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        self.scalers['ensemble'] = scaler
        
        # Train ensemble model
        model = RandomForestClassifier(
            n_estimators=200,
            max_depth=15,
            min_samples_split=20,
            min_samples_leaf=10,
            max_features='sqrt',
            random_state=42,
            n_jobs=-1
        )
        
        model.fit(X_train_scaled, y_train)
        
        # Evaluate
        test_pred_proba = model.predict_proba(X_test_scaled)[:, 1]
        test_auc = roc_auc_score(y_test, test_pred_proba)
        
        logger.info(f"Ensemble model AUC: {test_auc:.3f}")
        
        # Feature importance
        feature_importance = pd.DataFrame({
            'feature': self.feature_order,
            'importance': model.feature_importances_
        }).sort_values('importance', ascending=False)
        
        logger.info("\nTop 10 most important features:")
        for idx, row in feature_importance.head(10).iterrows():
            logger.info(f"  {row['feature']}: {row['importance']:.4f}")
        
        self.models['ensemble'] = model
        self.feature_orders['ensemble'] = self.feature_order
        
        return test_auc, feature_importance
    
    def save_models(self, output_dir="models/pattern_models"):
        """Save all trained models and metadata"""
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"\nSaving models to {output_path}")
        
        # Save each model
        for name, model in self.models.items():
            model_path = output_path / f"{name}_model.pkl"
            joblib.dump(model, model_path)
            logger.info(f"  Saved {name} model")
            
            # Save scaler if exists
            if name in self.scalers:
                scaler_path = output_path / f"{name}_scaler.pkl"
                joblib.dump(self.scalers[name], scaler_path)
        
        # Save encoders
        if self.encoders:
            encoders_path = output_path / "label_encoders.pkl"
            joblib.dump(self.encoders, encoders_path)
            logger.info(f"  Saved {len(self.encoders)} label encoders")
        
        # Save feature orders
        feature_order_path = output_path / "feature_orders.json"
        with open(feature_order_path, 'w') as f:
            json.dump(self.feature_orders, f, indent=2)
        logger.info("  Saved feature orders")
        
        # Save complete metadata
        metadata = {
            'dataset_path': self.data_path,
            'total_features': len(self.feature_order),
            'feature_order': self.feature_order,
            'categorical_features': list(self.encoders.keys()),
            'models': {
                name: {
                    'type': type(model).__name__,
                    'n_features': len(self.feature_orders[name]),
                    'features': self.feature_orders[name]
                }
                for name, model in self.models.items()
            }
        }
        
        metadata_path = output_path / "training_metadata.json"
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        logger.info("  Saved training metadata")
        
        logger.info(f"\n✅ All models saved successfully to {output_path}")
    
    def verify_feature_alignment(self, X_original):
        """Verify that features are properly aligned"""
        logger.info("\nVerifying feature alignment...")
        
        # Check a few sample predictions
        sample_indices = [0, 100, 1000]
        
        for idx in sample_indices:
            sample = X_original.iloc[idx]
            logger.info(f"\nSample {idx}:")
            logger.info(f"  funding_stage: {sample.get('funding_stage', 'N/A')}")
            logger.info(f"  team_size: {sample.get('team_size', 'N/A')}")
            logger.info(f"  revenue_growth_rate_percent: {sample.get('revenue_growth_rate_percent', 'N/A')}")
            
            # Verify the features are in the expected positions
            for pillar, features in [('capital', CAPITAL_FEATURES[:3]), 
                                    ('market', MARKET_FEATURES[:3]),
                                    ('people', PEOPLE_FEATURES[:3])]:
                logger.info(f"  {pillar} features: {[sample.get(f, 'N/A') for f in features]}")
    
    def run_complete_training(self):
        """Run the complete training pipeline"""
        logger.info("Starting complete pattern model training...")
        logger.info("=" * 60)
        
        # Load and prepare data
        X_encoded, y, X_original = self.load_and_prepare_data()
        
        # Verify feature alignment
        self.verify_feature_alignment(X_original)
        
        # Train pillar models
        pillar_results = self.train_pillar_models(X_encoded, y)
        
        # Train ensemble model
        ensemble_auc, feature_importance = self.train_ensemble_model(X_encoded, y)
        
        # Save all models
        self.save_models()
        
        # Print summary
        logger.info("\n" + "=" * 60)
        logger.info("TRAINING COMPLETE - SUMMARY")
        logger.info("=" * 60)
        
        for pillar, results in pillar_results.items():
            logger.info(f"\n{pillar.upper()} Model:")
            logger.info(f"  Features: {results['n_features']}")
            logger.info(f"  Test AUC: {results['test_auc']:.3f}")
            logger.info(f"  CV AUC: {results['cv_auc_mean']:.3f} ± {results['cv_auc_std']*2:.3f}")
        
        logger.info(f"\nENSEMBLE Model:")
        logger.info(f"  Features: {len(self.feature_order)}")
        logger.info(f"  Test AUC: {ensemble_auc:.3f}")
        
        logger.info("\n✅ Pattern models trained successfully with proper feature alignment!")
        logger.info("✅ Models are ready to use with the current API feature set!")
        
        return pillar_results, ensemble_auc


if __name__ == "__main__":
    trainer = PatternModelTrainer()
    trainer.run_complete_training()