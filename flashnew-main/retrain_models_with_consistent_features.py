#!/usr/bin/env python3
"""
Retrain all models with consistent feature ordering and naming
This ensures all models work together properly
"""

import pandas as pd
import numpy as np
import joblib
import logging
import json
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import roc_auc_score, accuracy_score
import xgboost as xgb
import lightgbm as lgb

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Import consistent feature configuration
from feature_config_fixed import (
    ALL_FEATURES, CAPITAL_FEATURES, ADVANTAGE_FEATURES, 
    MARKET_FEATURES, PEOPLE_FEATURES, CATEGORICAL_FEATURES
)


class ConsistentModelTrainer:
    """Train all models with consistent feature handling"""
    
    def __init__(self):
        self.data = None
        self.encoders = {}
        self.scalers = {}
        self.feature_order = ALL_FEATURES  # Use canonical feature order
        
    def load_and_prepare_data(self):
        """Load and prepare data with consistent encoding"""
        logger.info("Loading dataset...")
        self.data = pd.read_csv('data/final_100k_dataset_45features.csv')
        logger.info(f"Loaded {len(self.data)} samples")
        
        # Ensure we have all features in correct order
        X = self.data[self.feature_order].copy()
        y = self.data['success'].values
        
        # Encode categorical features
        for col in CATEGORICAL_FEATURES:
            if col in X.columns:
                le = LabelEncoder()
                X[col] = le.fit_transform(X[col].fillna('missing').astype(str))
                self.encoders[col] = le
                logger.info(f"Encoded {col}: {len(le.classes_)} classes")
        
        # Fill missing values
        X = X.fillna(0)
        
        return X, y
    
    def train_dna_analyzer(self, X, y):
        """Train DNA analyzer with CAMP scores"""
        logger.info("\nTraining DNA Analyzer...")
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        # Calculate CAMP scores
        def calculate_camp_scores(df):
            scores = pd.DataFrame()
            
            # Capital score
            capital_cols = [c for c in CAPITAL_FEATURES if c in df.columns]
            scores['capital_score'] = df[capital_cols].mean(axis=1).astype(float)
            
            # Advantage score
            advantage_cols = [c for c in ADVANTAGE_FEATURES if c in df.columns]
            scores['advantage_score'] = df[advantage_cols].mean(axis=1).astype(float)
            
            # Market score
            market_cols = [c for c in MARKET_FEATURES if c in df.columns]
            scores['market_score'] = df[market_cols].mean(axis=1).astype(float)
            
            # People score
            people_cols = [c for c in PEOPLE_FEATURES if c in df.columns]
            scores['people_score'] = df[people_cols].mean(axis=1).astype(float)
            
            return scores
        
        # Add CAMP scores to features
        camp_train = calculate_camp_scores(X_train)
        camp_test = calculate_camp_scores(X_test)
        
        X_train_dna = pd.concat([X_train, camp_train], axis=1)
        X_test_dna = pd.concat([X_test, camp_test], axis=1)
        
        # Store feature order for DNA model
        dna_feature_order = list(X_train_dna.columns)
        
        # Train model
        model = xgb.XGBClassifier(
            n_estimators=200,
            max_depth=6,
            learning_rate=0.1,
            random_state=42,
            eval_metric='auc',
            use_label_encoder=False
        )
        
        model.fit(X_train_dna, y_train)
        
        # Evaluate
        y_pred = model.predict_proba(X_test_dna)[:, 1]
        auc = roc_auc_score(y_test, y_pred)
        logger.info(f"DNA Analyzer AUC: {auc:.4f}")
        
        # Save model and metadata
        output_dir = Path('models/production_v45_fixed')
        output_dir.mkdir(parents=True, exist_ok=True)
        
        joblib.dump(model, output_dir / 'dna_analyzer.pkl')
        joblib.dump(dna_feature_order, output_dir / 'dna_feature_order.pkl')
        
        return model, auc
    
    def train_temporal_model(self, X, y):
        """Train temporal model with temporal features"""
        logger.info("\nTraining Temporal Model...")
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        # Add temporal features
        def add_temporal_features(df):
            temp_df = df.copy()
            
            # Growth momentum
            if 'revenue_growth_rate_percent' in df.columns:
                temp_df['growth_momentum'] = (
                    df['revenue_growth_rate_percent'] * 
                    df.get('user_growth_rate_percent', 0) / 100
                ).fillna(0)
            else:
                temp_df['growth_momentum'] = 0
                
            # Efficiency trend
            if 'burn_multiple' in df.columns:
                temp_df['efficiency_trend'] = (1 / (1 + df['burn_multiple'])).fillna(0.5)
            else:
                temp_df['efficiency_trend'] = 0.5
                
            # Stage velocity
            if 'funding_stage' in df.columns:
                temp_df['stage_velocity'] = df['funding_stage']
            else:
                temp_df['stage_velocity'] = 1
                
            return temp_df
        
        X_train_temp = add_temporal_features(X_train)
        X_test_temp = add_temporal_features(X_test)
        
        # Store feature order
        temporal_feature_order = list(X_train_temp.columns)
        
        # Train model
        model = lgb.LGBMClassifier(
            n_estimators=150,
            max_depth=8,
            learning_rate=0.05,
            random_state=42,
            verbosity=-1
        )
        
        model.fit(X_train_temp, y_train)
        
        # Evaluate
        y_pred = model.predict_proba(X_test_temp)[:, 1]
        auc = roc_auc_score(y_test, y_pred)
        logger.info(f"Temporal Model AUC: {auc:.4f}")
        
        # Save
        output_dir = Path('models/production_v45_fixed')
        joblib.dump(model, output_dir / 'temporal_model.pkl')
        joblib.dump(temporal_feature_order, output_dir / 'temporal_feature_order.pkl')
        
        return model, auc
    
    def train_industry_model(self, X, y):
        """Train industry model with scaling"""
        logger.info("\nTraining Industry Model...")
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        # Scale features
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        
        # Train model
        model = RandomForestClassifier(
            n_estimators=200,
            max_depth=15,
            min_samples_split=20,
            random_state=42,
            n_jobs=-1
        )
        
        model.fit(X_train_scaled, y_train)
        
        # Evaluate
        y_pred = model.predict_proba(X_test_scaled)[:, 1]
        auc = roc_auc_score(y_test, y_pred)
        logger.info(f"Industry Model AUC: {auc:.4f}")
        
        # Save
        output_dir = Path('models/production_v45_fixed')
        joblib.dump(model, output_dir / 'industry_model.pkl')
        joblib.dump(scaler, output_dir / 'industry_scaler.pkl')
        joblib.dump(self.feature_order, output_dir / 'industry_feature_order.pkl')
        
        return model, auc
    
    def train_ensemble_model(self, X, y):
        """Train ensemble model using other model predictions"""
        logger.info("\nTraining Ensemble Model...")
        
        # This is a meta-model that uses predictions from other models
        # For now, we'll train a simple model on base features
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        model = GradientBoostingClassifier(
            n_estimators=100,
            max_depth=5,
            learning_rate=0.1,
            random_state=42
        )
        
        model.fit(X_train, y_train)
        
        # Evaluate
        y_pred = model.predict_proba(X_test)[:, 1]
        auc = roc_auc_score(y_test, y_pred)
        logger.info(f"Ensemble Model AUC: {auc:.4f}")
        
        # Save
        output_dir = Path('models/production_v45_fixed')
        joblib.dump(model, output_dir / 'ensemble_model.pkl')
        
        return model, auc
    
    def save_metadata(self, results):
        """Save training metadata"""
        metadata = {
            'feature_order': self.feature_order,
            'encoders': list(self.encoders.keys()),
            'categorical_features': CATEGORICAL_FEATURES,
            'model_performance': results,
            'total_features': len(self.feature_order)
        }
        
        output_dir = Path('models/production_v45_fixed')
        with open(output_dir / 'training_metadata.json', 'w') as f:
            json.dump(metadata, f, indent=2)
            
        # Save encoders
        joblib.dump(self.encoders, output_dir / 'label_encoders.pkl')
        
        logger.info("\nMetadata saved successfully")
    
    def run_training(self):
        """Run complete training pipeline"""
        logger.info("="*80)
        logger.info("CONSISTENT MODEL TRAINING PIPELINE")
        logger.info("="*80)
        
        # Load data
        X, y = self.load_and_prepare_data()
        
        results = {}
        
        # Train all models
        model, auc = self.train_dna_analyzer(X, y)
        results['dna_analyzer'] = auc
        
        model, auc = self.train_temporal_model(X, y)
        results['temporal_model'] = auc
        
        model, auc = self.train_industry_model(X, y)
        results['industry_model'] = auc
        
        model, auc = self.train_ensemble_model(X, y)
        results['ensemble_model'] = auc
        
        # Save metadata
        self.save_metadata(results)
        
        # Summary
        logger.info("\n" + "="*80)
        logger.info("TRAINING COMPLETE")
        logger.info("="*80)
        logger.info("\nModel Performance:")
        for model_name, auc in results.items():
            logger.info(f"  {model_name}: {auc:.4f}")
        logger.info(f"\nAverage AUC: {np.mean(list(results.values())):.4f}")
        logger.info("\nModels saved to: models/production_v45_fixed/")
        
        # Copy to production
        logger.info("\nCopying to production...")
        import shutil
        prod_dir = Path('models/production_v45')
        fixed_dir = Path('models/production_v45_fixed')
        
        for file in fixed_dir.glob('*.pkl'):
            shutil.copy(file, prod_dir / file.name)
        
        shutil.copy(fixed_dir / 'training_metadata.json', prod_dir / 'training_metadata.json')
        
        logger.info("✅ All models updated in production!")


if __name__ == "__main__":
    trainer = ConsistentModelTrainer()
    trainer.run_training()