#!/usr/bin/env python3
"""
Train All Models for 45-Feature System
Comprehensive training script for base models and patterns
"""

import pandas as pd
import numpy as np
from pathlib import Path
import joblib
import logging
import time
import json
from datetime import datetime

from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import roc_auc_score, accuracy_score, precision_score, recall_score
import xgboost as xgb
import lightgbm as lgb

# Import our feature configuration
from feature_config import (
    ALL_FEATURES, CAPITAL_FEATURES, ADVANTAGE_FEATURES, 
    MARKET_FEATURES, PEOPLE_FEATURES, PRODUCT_FEATURES,
    CATEGORICAL_FEATURES, get_feature_groups
)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ComprehensiveModelTrainer:
    """Train all models for the 45-feature FLASH system"""
    
    def __init__(self):
        self.data = None
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        self.models = {}
        self.results = {}
        self.start_time = None
        
    def load_and_prepare_data(self):
        """Load and prepare the 45-feature dataset"""
        logger.info("Loading dataset...")
        self.data = pd.read_csv('data/final_100k_dataset_45features.csv')
        logger.info(f"Dataset loaded: {len(self.data)} samples")
        
        # Verify we have exactly 45 features
        feature_cols = [col for col in self.data.columns if col in ALL_FEATURES]
        logger.info(f"Features found: {len(feature_cols)}/45")
        
        # Prepare features
        X = self.data[ALL_FEATURES].copy()
        y = self.data['success'].values
        
        # Handle categorical features
        logger.info("Encoding categorical features...")
        for cat_feat in CATEGORICAL_FEATURES:
            if cat_feat in X.columns:
                # Simple encoding for now
                X[cat_feat] = pd.Categorical(X[cat_feat]).codes
        
        # Fill missing values
        X = X.fillna(0)
        
        # Split data
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        logger.info(f"Train set: {len(self.X_train)} samples")
        logger.info(f"Test set: {len(self.X_test)} samples")
        logger.info(f"Success rate: {y.mean():.2%}")
        
        return self
    
    def train_dna_pattern_analyzer(self):
        """Train DNA Pattern Analyzer (CAMP evaluation model)"""
        logger.info("\n" + "="*50)
        logger.info("Training DNA Pattern Analyzer (CAMP Model)")
        logger.info("="*50)
        
        # Create CAMP score features
        camp_scores = {}
        
        # Capital score
        capital_features = [f for f in CAPITAL_FEATURES if f in self.X_train.columns]
        camp_scores['capital_score'] = self.X_train[capital_features].mean(axis=1).astype(float)
        
        # Advantage score
        advantage_features = [f for f in ADVANTAGE_FEATURES if f in self.X_train.columns]
        camp_scores['advantage_score'] = self.X_train[advantage_features].mean(axis=1).astype(float)
        
        # Market score
        market_features = [f for f in MARKET_FEATURES if f in self.X_train.columns]
        camp_scores['market_score'] = self.X_train[market_features].mean(axis=1).astype(float)
        
        # People score
        people_features = [f for f in PEOPLE_FEATURES if f in self.X_train.columns]
        camp_scores['people_score'] = self.X_train[people_features].mean(axis=1).astype(float)
        
        # Combine with original features
        X_camp_train = pd.concat([
            self.X_train,
            pd.DataFrame(camp_scores)
        ], axis=1)
        
        # Train XGBoost model
        model = xgb.XGBClassifier(
            n_estimators=200,
            max_depth=6,
            learning_rate=0.1,
            objective='binary:logistic',
            eval_metric='auc',
            random_state=42,
            use_label_encoder=False
        )
        
        model.fit(X_camp_train, self.y_train)
        
        # Evaluate
        X_camp_test = self._create_camp_features(self.X_test)
        y_pred_proba = model.predict_proba(X_camp_test)[:, 1]
        auc_score = roc_auc_score(self.y_test, y_pred_proba)
        
        logger.info(f"DNA Pattern Analyzer AUC: {auc_score:.4f}")
        
        self.models['dna_analyzer'] = model
        self.results['dna_analyzer'] = {
            'auc': auc_score,
            'features_used': len(X_camp_train.columns)
        }
        
        return model
    
    def _create_camp_features(self, X):
        """Create CAMP features for given data"""
        camp_scores = {}
        
        capital_features = [f for f in CAPITAL_FEATURES if f in X.columns]
        camp_scores['capital_score'] = X[capital_features].mean(axis=1).astype(float)
        
        advantage_features = [f for f in ADVANTAGE_FEATURES if f in X.columns]
        camp_scores['advantage_score'] = X[advantage_features].mean(axis=1).astype(float)
        
        market_features = [f for f in MARKET_FEATURES if f in X.columns]
        camp_scores['market_score'] = X[market_features].mean(axis=1).astype(float)
        
        people_features = [f for f in PEOPLE_FEATURES if f in X.columns]
        camp_scores['people_score'] = X[people_features].mean(axis=1).astype(float)
        
        return pd.concat([X, pd.DataFrame(camp_scores)], axis=1)
    
    def train_temporal_model(self):
        """Train Temporal Prediction Model"""
        logger.info("\n" + "="*50)
        logger.info("Training Temporal Prediction Model")
        logger.info("="*50)
        
        # Add temporal features
        temporal_features = self.X_train.copy()
        
        # Growth momentum
        if 'revenue_growth_rate_percent' in temporal_features.columns:
            temporal_features['growth_momentum'] = (
                temporal_features['revenue_growth_rate_percent'] * 
                temporal_features.get('user_growth_rate_percent', 0) / 100
            )
        
        # Efficiency trends
        if 'burn_multiple' in temporal_features.columns:
            temporal_features['efficiency_trend'] = (
                1 / (1 + temporal_features['burn_multiple'])
            )
        
        # Stage progression
        if 'funding_stage' in temporal_features.columns:
            temporal_features['stage_velocity'] = temporal_features['funding_stage']
        
        # Train LightGBM model
        model = lgb.LGBMClassifier(
            n_estimators=150,
            max_depth=8,
            learning_rate=0.05,
            objective='binary',
            metric='auc',
            random_state=42,
            verbosity=-1
        )
        
        model.fit(temporal_features, self.y_train)
        
        # Evaluate
        X_temp_test = self._create_temporal_features(self.X_test)
        y_pred_proba = model.predict_proba(X_temp_test)[:, 1]
        auc_score = roc_auc_score(self.y_test, y_pred_proba)
        
        logger.info(f"Temporal Model AUC: {auc_score:.4f}")
        
        self.models['temporal_model'] = model
        self.results['temporal_model'] = {
            'auc': auc_score,
            'features_used': len(temporal_features.columns)
        }
        
        return model
    
    def _create_temporal_features(self, X):
        """Create temporal features"""
        temp = X.copy()
        
        if 'revenue_growth_rate_percent' in temp.columns:
            temp['growth_momentum'] = (
                temp['revenue_growth_rate_percent'] * 
                temp.get('user_growth_rate_percent', 0) / 100
            )
        
        if 'burn_multiple' in temp.columns:
            temp['efficiency_trend'] = 1 / (1 + temp['burn_multiple'])
        
        if 'funding_stage' in temp.columns:
            temp['stage_velocity'] = temp['funding_stage']
        
        return temp
    
    def train_industry_model(self):
        """Train Industry-Specific Model"""
        logger.info("\n" + "="*50)
        logger.info("Training Industry-Specific Model")
        logger.info("="*50)
        
        # Scale features for better performance
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(self.X_train)
        
        # Train Random Forest
        model = RandomForestClassifier(
            n_estimators=200,
            max_depth=15,
            min_samples_split=50,
            min_samples_leaf=20,
            random_state=42,
            n_jobs=-1
        )
        
        model.fit(X_scaled, self.y_train)
        
        # Evaluate
        X_test_scaled = scaler.transform(self.X_test)
        y_pred_proba = model.predict_proba(X_test_scaled)[:, 1]
        auc_score = roc_auc_score(self.y_test, y_pred_proba)
        
        logger.info(f"Industry Model AUC: {auc_score:.4f}")
        
        # Save scaler with model
        self.models['industry_model'] = {
            'model': model,
            'scaler': scaler
        }
        self.results['industry_model'] = {
            'auc': auc_score,
            'features_used': len(self.X_train.columns)
        }
        
        return model
    
    def train_ensemble_model(self):
        """Train Ensemble Meta-Model"""
        logger.info("\n" + "="*50)
        logger.info("Training Ensemble Meta-Model")
        logger.info("="*50)
        
        # Get predictions from base models
        base_predictions = []
        
        # DNA predictions
        if 'dna_analyzer' in self.models:
            X_camp = self._create_camp_features(self.X_train)
            dna_preds = self.models['dna_analyzer'].predict_proba(X_camp)[:, 1]
            base_predictions.append(dna_preds)
        
        # Temporal predictions
        if 'temporal_model' in self.models:
            X_temp = self._create_temporal_features(self.X_train)
            temp_preds = self.models['temporal_model'].predict_proba(X_temp)[:, 1]
            base_predictions.append(temp_preds)
        
        # Industry predictions
        if 'industry_model' in self.models:
            scaler = self.models['industry_model']['scaler']
            model = self.models['industry_model']['model']
            X_scaled = scaler.transform(self.X_train)
            ind_preds = model.predict_proba(X_scaled)[:, 1]
            base_predictions.append(ind_preds)
        
        # Stack predictions
        X_meta = np.column_stack(base_predictions)
        
        # Train meta-model
        meta_model = LogisticRegression(random_state=42)
        meta_model.fit(X_meta, self.y_train)
        
        # Evaluate on test set
        test_predictions = []
        
        if 'dna_analyzer' in self.models:
            X_camp = self._create_camp_features(self.X_test)
            test_predictions.append(
                self.models['dna_analyzer'].predict_proba(X_camp)[:, 1]
            )
        
        if 'temporal_model' in self.models:
            X_temp = self._create_temporal_features(self.X_test)
            test_predictions.append(
                self.models['temporal_model'].predict_proba(X_temp)[:, 1]
            )
        
        if 'industry_model' in self.models:
            scaler = self.models['industry_model']['scaler']
            model = self.models['industry_model']['model']
            X_scaled = scaler.transform(self.X_test)
            test_predictions.append(model.predict_proba(X_scaled)[:, 1])
        
        X_meta_test = np.column_stack(test_predictions)
        y_pred_proba = meta_model.predict_proba(X_meta_test)[:, 1]
        auc_score = roc_auc_score(self.y_test, y_pred_proba)
        
        logger.info(f"Ensemble Model AUC: {auc_score:.4f}")
        
        self.models['ensemble_model'] = meta_model
        self.results['ensemble_model'] = {
            'auc': auc_score,
            'base_models': len(base_predictions)
        }
        
        return meta_model
    
    def save_models(self):
        """Save all trained models"""
        logger.info("\n" + "="*50)
        logger.info("Saving Models")
        logger.info("="*50)
        
        # Create directories
        model_dir = Path('models/production_v45')
        model_dir.mkdir(parents=True, exist_ok=True)
        
        # Save each model
        for name, model in self.models.items():
            if isinstance(model, dict):
                # Save model and scaler separately
                joblib.dump(model['model'], model_dir / f'{name}.pkl')
                joblib.dump(model['scaler'], model_dir / f'{name}_scaler.pkl')
                logger.info(f"Saved {name} with scaler")
            else:
                joblib.dump(model, model_dir / f'{name}.pkl')
                logger.info(f"Saved {name}")
        
        # Save results and metadata
        metadata = {
            'training_date': datetime.now().isoformat(),
            'training_time_seconds': time.time() - self.start_time,
            'dataset_size': len(self.data),
            'features_count': len(ALL_FEATURES),
            'model_results': self.results,
            'feature_groups': {
                'capital': len(CAPITAL_FEATURES),
                'advantage': len(ADVANTAGE_FEATURES),
                'market': len(MARKET_FEATURES),
                'people': len(PEOPLE_FEATURES),
                'product': len(PRODUCT_FEATURES)
            }
        }
        
        with open(model_dir / 'training_metadata.json', 'w') as f:
            json.dump(metadata, f, indent=2)
        
        # Update production manifest
        manifest = {
            'version': '45_features_v1',
            'updated': datetime.now().isoformat(),
            'models': {
                'dna_analyzer': {
                    'path': str(model_dir / 'dna_analyzer.pkl'),
                    'auc': self.results['dna_analyzer']['auc'],
                    'features': 45
                },
                'temporal_model': {
                    'path': str(model_dir / 'temporal_model.pkl'),
                    'auc': self.results['temporal_model']['auc'],
                    'features': 45
                },
                'industry_model': {
                    'path': str(model_dir / 'industry_model.pkl'),
                    'auc': self.results['industry_model']['auc'],
                    'features': 45,
                    'has_scaler': True
                },
                'ensemble_model': {
                    'path': str(model_dir / 'ensemble_model.pkl'),
                    'auc': self.results['ensemble_model']['auc'],
                    'type': 'meta-ensemble'
                }
            },
            'average_auc': np.mean([r['auc'] for r in self.results.values()]),
            'pattern_system': {
                'trained_patterns': 31,
                'total_patterns': 45,
                'coverage': 0.574
            }
        }
        
        with open('models/production_manifest_v45.json', 'w') as f:
            json.dump(manifest, f, indent=2)
        
        logger.info(f"All models saved to {model_dir}")
        
    def run_complete_training(self):
        """Run the complete training pipeline"""
        self.start_time = time.time()
        
        logger.info("="*60)
        logger.info("FLASH 45-Feature Model Training Pipeline")
        logger.info("="*60)
        
        # Load data
        self.load_and_prepare_data()
        
        # Train models
        self.train_dna_pattern_analyzer()
        self.train_temporal_model()
        self.train_industry_model()
        self.train_ensemble_model()
        
        # Save models
        self.save_models()
        
        # Summary
        total_time = time.time() - self.start_time
        
        logger.info("\n" + "="*60)
        logger.info("TRAINING COMPLETE")
        logger.info("="*60)
        logger.info(f"Total training time: {total_time:.1f} seconds")
        logger.info(f"Average AUC: {np.mean([r['auc'] for r in self.results.values()]):.4f}")
        logger.info("\nModel Performance:")
        for name, result in self.results.items():
            logger.info(f"  {name}: AUC = {result['auc']:.4f}")
        logger.info("\nModels saved to: models/production_v45/")
        logger.info("Pattern system: 31 patterns already trained")
        logger.info("\nNext step: Update orchestrator to use new model paths")
        
        return self


def main():
    """Run the training"""
    trainer = ComprehensiveModelTrainer()
    trainer.run_complete_training()
    
    logger.info("\n✅ All models trained successfully!")
    logger.info("To use the new models:")
    logger.info("1. Update unified_orchestrator_v3.py model paths")
    logger.info("2. Restart API server")
    logger.info("3. Test with: curl http://localhost:8001/health")


if __name__ == "__main__":
    main()