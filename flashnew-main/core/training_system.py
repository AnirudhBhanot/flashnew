"""
Unified Training System with Contracts
Single system for training all models with proper contracts and validation
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple, Any
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import roc_auc_score, accuracy_score, precision_score, recall_score, f1_score
import xgboost as xgb
from catboost import CatBoostClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
import logging
from datetime import datetime
from pathlib import Path
import json

from .feature_registry import FeatureRegistry, feature_registry
from .model_contracts import ModelContract, ContractBuilder
from .feature_pipeline import UnifiedFeaturePipeline
from .model_wrapper import ContractualModel, ModelMetadata
from .feature_mapping import map_dataset_to_registry

logger = logging.getLogger(__name__)


class ModelTrainingConfig:
    """Configuration for training a specific model"""
    
    def __init__(self,
                 model_name: str,
                 model_class: type,
                 model_params: Dict[str, Any],
                 contract_builder: callable,
                 description: str = ""):
        self.model_name = model_name
        self.model_class = model_class
        self.model_params = model_params
        self.contract_builder = contract_builder
        self.description = description


class UnifiedTrainingSystem:
    """Single training system for all models with contracts"""
    
    def __init__(self, 
                 feature_registry: FeatureRegistry,
                 output_dir: str = "models/contractual"):
        self.registry = feature_registry
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Single unified pipeline for all models
        self.pipeline = UnifiedFeaturePipeline(feature_registry)
        
        # Model configurations
        self.model_configs = self._setup_model_configs()
        
        # Training results
        self.training_results = {}
        
    def _setup_model_configs(self) -> Dict[str, ModelTrainingConfig]:
        """Setup configurations for all models"""
        configs = {}
        
        # DNA Analyzer - XGBoost with CAMP scores
        configs['dna_analyzer'] = ModelTrainingConfig(
            model_name='dna_analyzer',
            model_class=xgb.XGBClassifier,
            model_params={
                'n_estimators': 100,
                'max_depth': 6,
                'learning_rate': 0.1,
                'objective': 'binary:logistic',
                'use_label_encoder': False,
                'eval_metric': 'auc',
                'random_state': 42
            },
            contract_builder=lambda reg: ContractBuilder.build_dna_analyzer_contract(reg),
            description="DNA Pattern Analyzer with CAMP scores (49 features)"
        )
        
        # Temporal Model - CatBoost with temporal features
        configs['temporal_model'] = ModelTrainingConfig(
            model_name='temporal_model',
            model_class=CatBoostClassifier,
            model_params={
                'iterations': 100,
                'depth': 6,
                'learning_rate': 0.1,
                'loss_function': 'Logloss',
                'eval_metric': 'AUC',
                'random_state': 42,
                'verbose': False
            },
            contract_builder=lambda reg: ContractBuilder.build_temporal_model_contract(reg),
            description="Temporal Prediction Model (48 features)"
        )
        
        # Industry Model - Random Forest with base features
        configs['industry_model'] = ModelTrainingConfig(
            model_name='industry_model',
            model_class=RandomForestClassifier,
            model_params={
                'n_estimators': 100,
                'max_depth': 10,
                'min_samples_split': 5,
                'min_samples_leaf': 2,
                'random_state': 42,
                'n_jobs': -1
            },
            contract_builder=lambda reg: ContractBuilder.build_industry_model_contract(reg),
            description="Industry-Specific Model (45 features)"
        )
        
        # Ensemble Model - Gradient Boosting on predictions
        configs['ensemble_model'] = ModelTrainingConfig(
            model_name='ensemble_model',
            model_class=GradientBoostingClassifier,
            model_params={
                'n_estimators': 50,
                'max_depth': 3,
                'learning_rate': 0.1,
                'random_state': 42
            },
            contract_builder=lambda reg: ContractBuilder.build_ensemble_model_contract(),
            description="Ensemble Meta-Model (3 features)"
        )
        
        return configs
    
    def load_and_prepare_data(self, 
                             data_path: str,
                             target_column: str = None,
                             test_size: float = 0.2) -> Tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
        """Load data and split into train/test"""
        logger.info(f"Loading data from {data_path}")
        
        # Load data
        df = pd.read_csv(data_path)
        logger.info(f"Loaded {len(df)} samples with {len(df.columns)} columns")
        
        # Determine target column
        if target_column is None:
            if 'success_label' in df.columns:
                target_column = 'success_label'
            elif 'success' in df.columns:
                target_column = 'success'
            else:
                raise ValueError("No target column found (looked for 'success_label' and 'success')")
        
        logger.info(f"Using target column: {target_column}")
        
        # Store target before mapping
        y = df[target_column]
        
        # Map dataset columns to registry features
        logger.info("Mapping dataset columns to registry features...")
        X = map_dataset_to_registry(df)
        
        logger.info(f"Mapped to {len(X.columns)} registry features")
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=42, stratify=y
        )
        
        logger.info(f"Train set: {len(X_train)} samples")
        logger.info(f"Test set: {len(X_test)} samples")
        logger.info(f"Class distribution - Train: {y_train.value_counts().to_dict()}")
        logger.info(f"Class distribution - Test: {y_test.value_counts().to_dict()}")
        
        return X_train, X_test, y_train, y_test
    
    def train_model(self,
                   model_name: str,
                   X_train: pd.DataFrame,
                   y_train: pd.Series,
                   X_test: pd.DataFrame,
                   y_test: pd.Series) -> ContractualModel:
        """Train a single model with its contract"""
        if model_name not in self.model_configs:
            raise ValueError(f"Unknown model: {model_name}")
        
        config = self.model_configs[model_name]
        logger.info(f"\nTraining {model_name}: {config.description}")
        
        # Build contract
        contract = config.contract_builder(self.registry)
        logger.info(f"Contract expects {contract.feature_count} features")
        
        # Prepare features according to contract
        X_train_prepared = self.pipeline.transform(X_train, contract)
        X_test_prepared = self.pipeline.transform(X_test, contract)
        
        logger.info(f"Prepared training features: {X_train_prepared.shape}")
        
        # Train model
        start_time = datetime.now()
        model = config.model_class(**config.model_params)
        model.fit(X_train_prepared, y_train)
        training_time = (datetime.now() - start_time).total_seconds()
        
        # Evaluate model
        train_pred_proba = model.predict_proba(X_train_prepared)[:, 1]
        test_pred_proba = model.predict_proba(X_test_prepared)[:, 1]
        
        train_pred = (train_pred_proba >= 0.5).astype(int)
        test_pred = (test_pred_proba >= 0.5).astype(int)
        
        # Calculate metrics
        metrics = {
            'train_auc': roc_auc_score(y_train, train_pred_proba),
            'test_auc': roc_auc_score(y_test, test_pred_proba),
            'train_accuracy': accuracy_score(y_train, train_pred),
            'test_accuracy': accuracy_score(y_test, test_pred),
            'test_precision': precision_score(y_test, test_pred),
            'test_recall': recall_score(y_test, test_pred),
            'test_f1': f1_score(y_test, test_pred),
            'training_time_seconds': training_time
        }
        
        logger.info(f"Performance - Train AUC: {metrics['train_auc']:.4f}, Test AUC: {metrics['test_auc']:.4f}")
        
        # Create metadata
        metadata = ModelMetadata(
            model_name=model_name,
            model_version="2.0.0",
            training_date=datetime.now(),
            training_dataset="unified_training_data",
            performance_metrics=metrics
        )
        
        # Create contractual model
        contractual_model = ContractualModel(
            model=model,
            contract=contract,
            feature_pipeline=self.pipeline,
            metadata=metadata
        )
        
        # Store results
        self.training_results[model_name] = {
            'model': contractual_model,
            'metrics': metrics,
            'contract': contract
        }
        
        return contractual_model
    
    def train_ensemble(self,
                      base_models: Dict[str, ContractualModel],
                      X_train: pd.DataFrame,
                      y_train: pd.Series,
                      X_test: pd.DataFrame,
                      y_test: pd.Series) -> ContractualModel:
        """Train ensemble model using base model predictions"""
        logger.info("\nTraining ensemble model")
        
        # Get predictions from base models
        train_predictions = {}
        test_predictions = {}
        
        for name, model in base_models.items():
            if name != 'ensemble_model':  # Skip ensemble itself
                logger.info(f"Getting predictions from {name}")
                train_predictions[f'{name}_prediction'] = model.predict(X_train)
                test_predictions[f'{name}_prediction'] = model.predict(X_test)
        
        # Create dataframes for ensemble
        X_train_ensemble = pd.DataFrame(train_predictions)
        X_test_ensemble = pd.DataFrame(test_predictions)
        
        # Rename columns to match ensemble contract
        X_train_ensemble.columns = ['dna_prediction', 'temporal_prediction', 'industry_prediction']
        X_test_ensemble.columns = ['dna_prediction', 'temporal_prediction', 'industry_prediction']
        
        # Train ensemble with its own contract
        config = self.model_configs['ensemble_model']
        contract = config.contract_builder(self.registry)
        
        # For ensemble, we don't need the full pipeline transformation
        model = config.model_class(**config.model_params)
        model.fit(X_train_ensemble.values, y_train)
        
        # Evaluate
        train_pred_proba = model.predict_proba(X_train_ensemble.values)[:, 1]
        test_pred_proba = model.predict_proba(X_test_ensemble.values)[:, 1]
        
        metrics = {
            'train_auc': roc_auc_score(y_train, train_pred_proba),
            'test_auc': roc_auc_score(y_test, test_pred_proba),
            'train_accuracy': accuracy_score(y_train, (train_pred_proba >= 0.5).astype(int)),
            'test_accuracy': accuracy_score(y_test, (test_pred_proba >= 0.5).astype(int))
        }
        
        logger.info(f"Ensemble Performance - Test AUC: {metrics['test_auc']:.4f}")
        
        # Create metadata
        metadata = ModelMetadata(
            model_name='ensemble_model',
            model_version="2.0.0",
            training_date=datetime.now(),
            training_dataset="base_model_predictions",
            performance_metrics=metrics
        )
        
        # Create contractual model
        # Note: Ensemble needs a special pipeline that just passes through
        ensemble_pipeline = UnifiedFeaturePipeline(self.registry)
        ensemble_pipeline.is_fitted = True  # Mark as fitted since ensemble doesn't need transformation
        
        contractual_model = ContractualModel(
            model=model,
            contract=contract,
            feature_pipeline=ensemble_pipeline,
            metadata=metadata
        )
        
        return contractual_model
    
    def train_all_models(self,
                        data_path: str,
                        save_models: bool = True) -> Dict[str, ContractualModel]:
        """Train all models in the system"""
        logger.info("=== Starting Unified Model Training ===")
        
        # Load and prepare data
        X_train, X_test, y_train, y_test = self.load_and_prepare_data(data_path)
        
        # Fit the unified pipeline once on training data
        logger.info("\nFitting unified feature pipeline...")
        self.pipeline.fit(X_train)
        
        # Save fitted pipeline
        if save_models:
            pipeline_path = self.output_dir / "unified_pipeline.pkl"
            self.pipeline.save(str(pipeline_path))
            logger.info(f"Saved pipeline to {pipeline_path}")
        
        # Train base models
        trained_models = {}
        base_model_names = ['dna_analyzer', 'temporal_model', 'industry_model']
        
        for model_name in base_model_names:
            model = self.train_model(model_name, X_train, y_train, X_test, y_test)
            trained_models[model_name] = model
            
            if save_models:
                model_path = self.output_dir / f"{model_name}.pkl"
                model.save(str(model_path))
                logger.info(f"Saved {model_name} to {model_path}")
        
        # Train ensemble using base model predictions
        ensemble = self.train_ensemble(trained_models, X_train, y_train, X_test, y_test)
        trained_models['ensemble_model'] = ensemble
        
        if save_models:
            ensemble_path = self.output_dir / "ensemble_model.pkl"
            ensemble.save(str(ensemble_path))
            logger.info(f"Saved ensemble to {ensemble_path}")
        
        # Generate training report
        self._generate_training_report(trained_models)
        
        logger.info("\n=== Training Complete ===")
        return trained_models
    
    def _generate_training_report(self, models: Dict[str, ContractualModel]):
        """Generate comprehensive training report"""
        report = {
            'training_date': datetime.now().isoformat(),
            'feature_registry_version': self.registry.version,
            'models': {}
        }
        
        for name, model in models.items():
            report['models'][name] = {
                'model_id': model.metadata.model_id,
                'version': model.metadata.model_version,
                'feature_count': model.contract.feature_count,
                'performance': model.metadata.performance_metrics,
                'contract_features': model.contract.get_feature_names()[:10]  # First 10
            }
        
        # Calculate average performance
        all_aucs = [m.metadata.performance_metrics.get('test_auc', 0) for m in models.values()]
        report['summary'] = {
            'total_models': len(models),
            'average_test_auc': np.mean(all_aucs),
            'best_model': max(models.items(), key=lambda x: x[1].metadata.performance_metrics.get('test_auc', 0))[0]
        }
        
        # Save report
        report_path = self.output_dir / "training_report.json"
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        logger.info(f"\nTraining Report saved to {report_path}")
        logger.info(f"Average Test AUC across all models: {report['summary']['average_test_auc']:.4f}")
        logger.info(f"Best performing model: {report['summary']['best_model']}")
    
    def cross_validate_model(self,
                           model_name: str,
                           X: pd.DataFrame,
                           y: pd.Series,
                           cv_folds: int = 5) -> Dict[str, float]:
        """Perform cross-validation for a model"""
        if model_name not in self.model_configs:
            raise ValueError(f"Unknown model: {model_name}")
        
        config = self.model_configs[model_name]
        contract = config.contract_builder(self.registry)
        
        # Prepare features
        X_prepared = self.pipeline.transform(X, contract)
        
        # Create model
        model = config.model_class(**config.model_params)
        
        # Perform cross-validation
        scores = cross_val_score(model, X_prepared, y, cv=cv_folds, scoring='roc_auc')
        
        results = {
            'mean_auc': scores.mean(),
            'std_auc': scores.std(),
            'min_auc': scores.min(),
            'max_auc': scores.max(),
            'all_scores': scores.tolist()
        }
        
        logger.info(f"{model_name} CV Results: {results['mean_auc']:.4f} (+/- {results['std_auc']:.4f})")
        
        return results