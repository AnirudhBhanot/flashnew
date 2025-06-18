#!/usr/bin/env python3
"""
Unified Model Training Script - Elite Engineering Standards
Trains all models on canonical 45 features for consistency
"""

import numpy as np
import pandas as pd
from pathlib import Path
import joblib
import json
import time
from datetime import datetime
from typing import Dict, Tuple, List
import logging
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import roc_auc_score, precision_recall_curve, auc
from catboost import CatBoostClassifier
from lightgbm import LGBMClassifier
import xgboost as xgb
from sklearn.ensemble import VotingClassifier
import warnings
warnings.filterwarnings('ignore')

# Configure elite logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('unified_training.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Import canonical features
from feature_config import ALL_FEATURES, CATEGORICAL_FEATURES

class UnifiedDataPipeline:
    """Single source of truth for data preprocessing"""
    
    def __init__(self):
        self.features = ALL_FEATURES
        self.categorical_features = CATEGORICAL_FEATURES
        self.scaler = StandardScaler()
        self.categorical_encoders = {}
        
    def fit_transform(self, df: pd.DataFrame) -> Tuple[np.ndarray, np.ndarray]:
        """Fit and transform data with canonical features"""
        # Ensure all features exist
        for feature in self.features:
            if feature not in df.columns:
                logger.warning(f"Missing feature {feature}, using default")
                if feature in self.categorical_features:
                    df[feature] = 'unknown'
                else:
                    df[feature] = 0.0
        
        # Select only canonical features
        X = df[self.features].copy()
        
        # Encode categorical features
        for cat_feature in self.categorical_features:
            if cat_feature in X.columns:
                # Create consistent encoding
                unique_vals = X[cat_feature].unique()
                encoding_map = {val: i for i, val in enumerate(unique_vals)}
                self.categorical_encoders[cat_feature] = encoding_map
                X[cat_feature] = X[cat_feature].map(encoding_map).fillna(0)
        
        # Scale numerical features
        numerical_features = [f for f in self.features if f not in self.categorical_features]
        X[numerical_features] = self.scaler.fit_transform(X[numerical_features])
        
        return X.values, df['success'].values
    
    def transform(self, df: pd.DataFrame) -> np.ndarray:
        """Transform data using fitted pipeline"""
        X = df[self.features].copy()
        
        # Apply categorical encoding
        for cat_feature, encoding_map in self.categorical_encoders.items():
            if cat_feature in X.columns:
                X[cat_feature] = X[cat_feature].map(encoding_map).fillna(0)
        
        # Scale numerical features
        numerical_features = [f for f in self.features if f not in self.categorical_features]
        X[numerical_features] = self.scaler.transform(X[numerical_features])
        
        return X.values


class UnifiedModelTrainer:
    """Trains all models with consistent 45-feature input"""
    
    def __init__(self):
        self.pipeline = UnifiedDataPipeline()
        self.models = {}
        self.results = {}
        
    def load_data(self) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """Load training data"""
        logger.info("Loading training data...")
        
        # Check for existing dataset
        data_path = Path("data/final_100k_dataset_45features.csv")
        if not data_path.exists():
            raise FileNotFoundError(f"Dataset not found at {data_path}")
        
        df = pd.read_csv(data_path)
        logger.info(f"Loaded {len(df)} samples")
        
        # Split data
        train_df, test_df = train_test_split(df, test_size=0.2, random_state=42, stratify=df['success'])
        logger.info(f"Train: {len(train_df)}, Test: {len(test_df)}")
        
        return train_df, test_df
    
    def train_dna_analyzer(self, X_train: np.ndarray, y_train: np.ndarray, 
                          X_test: np.ndarray, y_test: np.ndarray) -> Dict:
        """Train DNA Analyzer with CatBoost"""
        logger.info("Training DNA Analyzer (CAMP evaluation model)...")
        
        model = CatBoostClassifier(
            iterations=1000,
            learning_rate=0.05,
            depth=6,
            l2_leaf_reg=3,
            loss_function='Logloss',
            eval_metric='AUC',
            random_seed=42,
            verbose=False,
            early_stopping_rounds=50
        )
        
        model.fit(
            X_train, y_train,
            eval_set=(X_test, y_test),
            use_best_model=True
        )
        
        # Evaluate
        y_pred = model.predict_proba(X_test)[:, 1]
        auc_score = roc_auc_score(y_test, y_pred)
        
        self.models['dna_analyzer'] = model
        result = {
            'name': 'DNA Analyzer',
            'auc': auc_score,
            'n_features': len(self.pipeline.features),
            'feature_importance': dict(zip(self.pipeline.features, model.feature_importances_))
        }
        
        logger.info(f"DNA Analyzer AUC: {auc_score:.4f}")
        return result
    
    def train_temporal_model(self, X_train: np.ndarray, y_train: np.ndarray,
                           X_test: np.ndarray, y_test: np.ndarray) -> Dict:
        """Train Temporal Model with LightGBM"""
        logger.info("Training Temporal Model...")
        
        model = LGBMClassifier(
            n_estimators=500,
            learning_rate=0.05,
            num_leaves=31,
            max_depth=6,
            min_child_samples=20,
            subsample=0.8,
            colsample_bytree=0.8,
            reg_alpha=0.1,
            reg_lambda=0.1,
            random_state=42,
            n_jobs=-1,
            verbose=-1
        )
        
        model.fit(
            X_train, y_train,
            eval_set=[(X_test, y_test)],
            eval_metric='auc',
            callbacks=None
        )
        
        # Evaluate
        y_pred = model.predict_proba(X_test)[:, 1]
        auc_score = roc_auc_score(y_test, y_pred)
        
        self.models['temporal_model'] = model
        result = {
            'name': 'Temporal Model',
            'auc': auc_score,
            'n_features': len(self.pipeline.features),
            'feature_importance': dict(zip(self.pipeline.features, model.feature_importances_))
        }
        
        logger.info(f"Temporal Model AUC: {auc_score:.4f}")
        return result
    
    def train_industry_model(self, X_train: np.ndarray, y_train: np.ndarray,
                           X_test: np.ndarray, y_test: np.ndarray) -> Dict:
        """Train Industry Model with XGBoost"""
        logger.info("Training Industry Model...")
        
        model = xgb.XGBClassifier(
            n_estimators=500,
            learning_rate=0.05,
            max_depth=6,
            min_child_weight=1,
            subsample=0.8,
            colsample_bytree=0.8,
            reg_alpha=0.1,
            reg_lambda=1,
            random_state=42,
            use_label_encoder=False,
            eval_metric='auc'
        )
        
        model.fit(
            X_train, y_train,
            eval_set=[(X_test, y_test)],
            early_stopping_rounds=50,
            verbose=False
        )
        
        # Evaluate
        y_pred = model.predict_proba(X_test)[:, 1]
        auc_score = roc_auc_score(y_test, y_pred)
        
        self.models['industry_model'] = model
        result = {
            'name': 'Industry Model',
            'auc': auc_score,
            'n_features': len(self.pipeline.features),
            'feature_importance': dict(zip(self.pipeline.features, model.feature_importances_))
        }
        
        logger.info(f"Industry Model AUC: {auc_score:.4f}")
        return result
    
    def train_ensemble_model(self, X_train: np.ndarray, y_train: np.ndarray,
                           X_test: np.ndarray, y_test: np.ndarray) -> Dict:
        """Train Ensemble Meta-Model"""
        logger.info("Training Ensemble Model...")
        
        # Create base predictions for ensemble
        base_predictions_train = np.column_stack([
            self.models['dna_analyzer'].predict_proba(X_train)[:, 1],
            self.models['temporal_model'].predict_proba(X_train)[:, 1],
            self.models['industry_model'].predict_proba(X_train)[:, 1]
        ])
        
        base_predictions_test = np.column_stack([
            self.models['dna_analyzer'].predict_proba(X_test)[:, 1],
            self.models['temporal_model'].predict_proba(X_test)[:, 1],
            self.models['industry_model'].predict_proba(X_test)[:, 1]
        ])
        
        # Train meta-model on base predictions
        meta_model = xgb.XGBClassifier(
            n_estimators=100,
            learning_rate=0.1,
            max_depth=3,
            random_state=42,
            use_label_encoder=False
        )
        
        meta_model.fit(base_predictions_train, y_train)
        
        # Create ensemble wrapper
        class EnsembleModel:
            def __init__(self, base_models, meta_model):
                self.base_models = base_models
                self.meta_model = meta_model
                self.n_features_in_ = 45  # Canonical features
            
            def predict_proba(self, X):
                base_preds = np.column_stack([
                    model.predict_proba(X)[:, 1] 
                    for model in self.base_models.values()
                ])
                return self.meta_model.predict_proba(base_preds)
        
        ensemble = EnsembleModel(
            {'dna': self.models['dna_analyzer'],
             'temporal': self.models['temporal_model'],
             'industry': self.models['industry_model']},
            meta_model
        )
        
        # Evaluate
        y_pred = meta_model.predict_proba(base_predictions_test)[:, 1]
        auc_score = roc_auc_score(y_test, y_pred)
        
        self.models['ensemble_model'] = ensemble
        result = {
            'name': 'Ensemble Model',
            'auc': auc_score,
            'n_features': len(self.pipeline.features),
            'uses_models': ['dna_analyzer', 'temporal_model', 'industry_model']
        }
        
        logger.info(f"Ensemble Model AUC: {auc_score:.4f}")
        return result
    
    def train_all_models(self):
        """Train all models with unified pipeline"""
        start_time = time.time()
        
        # Load and prepare data
        train_df, test_df = self.load_data()
        
        # Transform with unified pipeline
        X_train, y_train = self.pipeline.fit_transform(train_df)
        X_test, y_test = self.pipeline.transform(test_df), test_df['success'].values
        
        # Train models in sequence
        self.results['dna_analyzer'] = self.train_dna_analyzer(X_train, y_train, X_test, y_test)
        self.results['temporal_model'] = self.train_temporal_model(X_train, y_train, X_test, y_test)
        self.results['industry_model'] = self.train_industry_model(X_train, y_train, X_test, y_test)
        self.results['ensemble_model'] = self.train_ensemble_model(X_train, y_train, X_test, y_test)
        
        # Calculate average performance
        avg_auc = np.mean([r['auc'] for r in self.results.values() if 'auc' in r])
        
        training_time = time.time() - start_time
        logger.info(f"\nTraining completed in {training_time:.1f} seconds")
        logger.info(f"Average AUC: {avg_auc:.4f}")
        
        return self.results
    
    def save_models(self, output_dir: str = "models/unified_v45"):
        """Save all trained models and metadata"""
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Save models
        for name, model in self.models.items():
            model_path = output_path / f"{name}.pkl"
            joblib.dump(model, model_path)
            logger.info(f"Saved {name} to {model_path}")
        
        # Save pipeline
        pipeline_path = output_path / "data_pipeline.pkl"
        joblib.dump(self.pipeline, pipeline_path)
        logger.info(f"Saved data pipeline to {pipeline_path}")
        
        # Save metadata
        metadata = {
            'training_date': datetime.now().isoformat(),
            'n_features': len(self.pipeline.features),
            'features': self.pipeline.features,
            'categorical_features': list(self.pipeline.categorical_features),
            'results': self.results,
            'models': list(self.models.keys())
        }
        
        metadata_path = output_path / "training_metadata.json"
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        logger.info(f"Saved metadata to {metadata_path}")
        
        # Create model manifest
        manifest = {
            'version': 'unified_v45',
            'created_at': datetime.now().isoformat(),
            'models': {
                name: {
                    'path': f"{output_dir}/{name}.pkl",
                    'auc': self.results[name]['auc'] if 'auc' in self.results[name] else None,
                    'n_features': 45
                }
                for name in self.models.keys()
            },
            'pipeline_path': f"{output_dir}/data_pipeline.pkl",
            'average_auc': np.mean([r['auc'] for r in self.results.values() if 'auc' in r])
        }
        
        manifest_path = Path("models/unified_manifest.json")
        with open(manifest_path, 'w') as f:
            json.dump(manifest, f, indent=2)
        logger.info(f"Created model manifest at {manifest_path}")


def main():
    """Execute unified training"""
    logger.info("=" * 60)
    logger.info("FLASH Unified Model Training - Elite Standards")
    logger.info("=" * 60)
    
    trainer = UnifiedModelTrainer()
    
    # Train all models
    results = trainer.train_all_models()
    
    # Save everything
    trainer.save_models()
    
    # Print summary
    logger.info("\n" + "=" * 60)
    logger.info("Training Summary:")
    logger.info("=" * 60)
    for name, result in results.items():
        if 'auc' in result:
            logger.info(f"{result['name']}: {result['auc']:.4f} AUC")
    
    avg_auc = np.mean([r['auc'] for r in results.values() if 'auc' in r])
    logger.info(f"\nAverage AUC: {avg_auc:.4f}")
    logger.info("All models now use canonical 45 features!")
    logger.info("=" * 60)


if __name__ == "__main__":
    main()