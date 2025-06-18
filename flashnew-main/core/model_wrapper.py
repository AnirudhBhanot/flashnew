"""
Contractual Model Wrapper
Wraps ML models with contracts, metadata, and self-validation
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Any, Union, Tuple
from sklearn.base import BaseEstimator
import joblib
import json
from datetime import datetime
import hashlib
import logging
from pathlib import Path

from .model_contracts import ModelContract
from .feature_pipeline import UnifiedFeaturePipeline
from .feature_registry import FeatureRegistry

logger = logging.getLogger(__name__)


class ModelMetadata:
    """Comprehensive metadata for a model"""
    
    def __init__(self,
                 model_name: str,
                 model_version: str,
                 training_date: datetime,
                 training_dataset: str,
                 performance_metrics: Dict[str, float]):
        self.model_name = model_name
        self.model_version = model_version
        self.training_date = training_date
        self.training_dataset = training_dataset
        self.performance_metrics = performance_metrics
        self.prediction_count = 0
        self.last_prediction_date = None
        self.error_count = 0
        self.validation_failures = 0
        
        # Generate unique model ID
        self.model_id = self._generate_model_id()
    
    def _generate_model_id(self) -> str:
        """Generate unique model ID from metadata"""
        id_string = f"{self.model_name}_{self.model_version}_{self.training_date.isoformat()}"
        return hashlib.sha256(id_string.encode()).hexdigest()[:16]
    
    def update_prediction_stats(self, success: bool = True):
        """Update prediction statistics"""
        self.prediction_count += 1
        self.last_prediction_date = datetime.now()
        if not success:
            self.error_count += 1
    
    def to_dict(self) -> Dict:
        """Serialize metadata"""
        return {
            'model_id': self.model_id,
            'model_name': self.model_name,
            'model_version': self.model_version,
            'training_date': self.training_date.isoformat(),
            'training_dataset': self.training_dataset,
            'performance_metrics': self.performance_metrics,
            'prediction_count': self.prediction_count,
            'last_prediction_date': self.last_prediction_date.isoformat() if self.last_prediction_date else None,
            'error_count': self.error_count,
            'validation_failures': self.validation_failures
        }


class ContractualModel:
    """Model wrapper that enforces contracts and tracks metadata"""
    
    def __init__(self,
                 model: BaseEstimator,
                 contract: ModelContract,
                 feature_pipeline: UnifiedFeaturePipeline,
                 metadata: ModelMetadata):
        self.model = model
        self.contract = contract
        self.feature_pipeline = feature_pipeline
        self.metadata = metadata
        
        # Validation cache to avoid repeated validation
        self._validation_cache = {}
        
        # Feature importance cache
        self._feature_importance = None
        
        logger.info(f"Created contractual model: {metadata.model_name} v{metadata.model_version}")
    
    def predict(self, 
                raw_data: Union[pd.DataFrame, Dict],
                return_diagnostics: bool = False) -> Union[np.ndarray, Tuple[np.ndarray, Dict]]:
        """Predict with automatic feature preparation and validation"""
        start_time = datetime.now()
        diagnostics = {
            'model_id': self.metadata.model_id,
            'model_name': self.metadata.model_name,
            'start_time': start_time.isoformat()
        }
        
        try:
            # Convert dict to dataframe if needed
            if isinstance(raw_data, dict):
                df = pd.DataFrame([raw_data])
            else:
                df = raw_data.copy()
            
            # Validate input against contract
            is_valid, errors = self.contract.validate_input(df)
            if not is_valid:
                self.metadata.validation_failures += 1
                raise ValueError(f"Input validation failed: {errors}")
            
            diagnostics['validation_passed'] = True
            
            # Transform according to contract
            X = self.feature_pipeline.transform(df, self.contract)
            diagnostics['features_prepared'] = X.shape[1]
            
            # Verify feature count matches contract
            if X.shape[1] != self.contract.feature_count:
                raise ValueError(f"Feature count mismatch: expected {self.contract.feature_count}, got {X.shape[1]}")
            
            # Make prediction
            if hasattr(self.model, 'predict_proba'):
                predictions = self.model.predict_proba(X)[:, 1]
            else:
                predictions = self.model.predict(X)
            
            # Validate output
            self._validate_output(predictions)
            
            # Update statistics
            self.metadata.update_prediction_stats(success=True)
            
            # Calculate diagnostics
            end_time = datetime.now()
            diagnostics['end_time'] = end_time.isoformat()
            diagnostics['duration_ms'] = (end_time - start_time).total_seconds() * 1000
            diagnostics['predictions_shape'] = predictions.shape
            diagnostics['success'] = True
            
            if return_diagnostics:
                return predictions, diagnostics
            return predictions
            
        except Exception as e:
            # Update error statistics
            self.metadata.update_prediction_stats(success=False)
            
            # Add error to diagnostics
            diagnostics['error'] = str(e)
            diagnostics['success'] = False
            
            logger.error(f"Prediction failed for {self.metadata.model_name}: {e}")
            
            if return_diagnostics:
                return np.array([]), diagnostics
            raise
    
    def predict_proba(self,
                      raw_data: Union[pd.DataFrame, Dict],
                      return_diagnostics: bool = False) -> Union[np.ndarray, Tuple[np.ndarray, Dict]]:
        """Get probability predictions"""
        if not hasattr(self.model, 'predict_proba'):
            raise AttributeError(f"Model {self.metadata.model_name} does not support probability predictions")
        
        # Use regular predict method since it handles predict_proba internally
        return self.predict(raw_data, return_diagnostics)
    
    def _validate_output(self, predictions: np.ndarray):
        """Validate model output against contract"""
        output_schema = self.contract.output_schema
        
        # Check type
        if output_schema['type'] == 'float':
            if predictions.dtype not in [np.float32, np.float64]:
                raise ValueError(f"Expected float output, got {predictions.dtype}")
        
        # Check range if specified
        if output_schema.get('range'):
            min_val, max_val = output_schema['range']
            if predictions.min() < min_val or predictions.max() > max_val:
                raise ValueError(f"Predictions outside valid range [{min_val}, {max_val}]")
        
        # Check for NaN/Inf
        if np.any(np.isnan(predictions)) or np.any(np.isinf(predictions)):
            raise ValueError("Predictions contain NaN or Inf values")
    
    def explain(self,
                raw_data: Union[pd.DataFrame, Dict],
                method: str = 'feature_importance') -> Dict[str, Any]:
        """Explain model predictions"""
        # Prepare features
        if isinstance(raw_data, dict):
            df = pd.DataFrame([raw_data])
        else:
            df = raw_data
        
        X = self.feature_pipeline.transform(df, self.contract)
        
        explanation = {
            'method': method,
            'model_name': self.metadata.model_name,
            'features_used': self.contract.get_feature_names()
        }
        
        if method == 'feature_importance':
            # Get feature importance if available
            if hasattr(self.model, 'feature_importances_'):
                importance = self.model.feature_importances_
                feature_names = self.contract.get_feature_names()
                
                # Create importance dict
                importance_dict = {name: float(imp) for name, imp in zip(feature_names, importance)}
                
                # Sort by importance
                sorted_importance = dict(sorted(importance_dict.items(), 
                                              key=lambda x: x[1], 
                                              reverse=True))
                
                explanation['feature_importance'] = sorted_importance
                explanation['top_features'] = list(sorted_importance.keys())[:10]
            else:
                explanation['error'] = "Model does not support feature importance"
        
        elif method == 'prediction_breakdown':
            # Show how each feature contributes
            prediction = self.predict(df)[0]
            explanation['prediction'] = float(prediction)
            
            # For tree-based models, we can get decision path
            if hasattr(self.model, 'decision_path'):
                path = self.model.decision_path(X)
                explanation['decision_path_density'] = path.mean()
        
        return explanation
    
    def get_feature_importance(self) -> Optional[pd.DataFrame]:
        """Get feature importance as a dataframe"""
        if hasattr(self.model, 'feature_importances_'):
            importance = self.model.feature_importances_
            feature_names = self.contract.get_feature_names()
            
            df = pd.DataFrame({
                'feature': feature_names,
                'importance': importance
            }).sort_values('importance', ascending=False)
            
            return df
        return None
    
    def validate_consistency(self, test_data: pd.DataFrame, tolerance: float = 0.01) -> Dict[str, Any]:
        """Validate model consistency on test data"""
        results = {
            'model_name': self.metadata.model_name,
            'test_size': len(test_data),
            'consistency_checks': []
        }
        
        # Check 1: Prediction stability (same input -> same output)
        sample = test_data.head(10)
        pred1 = self.predict(sample)
        pred2 = self.predict(sample)
        
        stability = np.allclose(pred1, pred2, rtol=tolerance)
        results['consistency_checks'].append({
            'check': 'prediction_stability',
            'passed': stability,
            'details': f"Max difference: {np.max(np.abs(pred1 - pred2))}"
        })
        
        # Check 2: Output distribution
        all_predictions = self.predict(test_data)
        results['output_stats'] = {
            'mean': float(np.mean(all_predictions)),
            'std': float(np.std(all_predictions)),
            'min': float(np.min(all_predictions)),
            'max': float(np.max(all_predictions)),
            'nan_count': int(np.sum(np.isnan(all_predictions)))
        }
        
        # Check 3: Feature importance stability
        if hasattr(self.model, 'feature_importances_'):
            imp1 = self.model.feature_importances_.copy()
            # Re-access to check caching
            imp2 = self.model.feature_importances_.copy()
            
            importance_stable = np.allclose(imp1, imp2)
            results['consistency_checks'].append({
                'check': 'feature_importance_stability',
                'passed': importance_stable
            })
        
        results['overall_consistency'] = all(check['passed'] for check in results['consistency_checks'])
        
        return results
    
    def save(self, path: str):
        """Save model with all components"""
        save_path = Path(path)
        save_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Create save dictionary
        save_dict = {
            'model': self.model,
            'contract': self.contract.to_dict(),
            'metadata': self.metadata.to_dict(),
            'feature_pipeline': self.feature_pipeline,
            'saved_at': datetime.now().isoformat(),
            'contractual_model_version': '1.0.0'
        }
        
        # Save with joblib
        joblib.dump(save_dict, path)
        
        # Also save contract separately for reference
        contract_path = save_path.with_suffix('.contract.json')
        self.contract.save(str(contract_path))
        
        # Save metadata separately
        metadata_path = save_path.with_suffix('.metadata.json')
        with open(metadata_path, 'w') as f:
            json.dump(self.metadata.to_dict(), f, indent=2)
        
        logger.info(f"Saved contractual model to {path}")
    
    @classmethod
    def load(cls, 
             path: str,
             feature_registry: Optional[FeatureRegistry] = None) -> 'ContractualModel':
        """Load model with contract validation"""
        # Load save dictionary
        save_dict = joblib.load(path)
        
        # Validate version
        saved_version = save_dict.get('contractual_model_version', '0.0.0')
        if saved_version != '1.0.0':
            logger.warning(f"Version mismatch: saved {saved_version}, current 1.0.0")
        
        # Reconstruct components
        model = save_dict['model']
        feature_pipeline = save_dict['feature_pipeline']
        
        # Reconstruct contract (without computation functions)
        contract_dict = save_dict['contract']
        
        # Use ContractBuilder to rebuild the contract properly
        from .model_contracts import ContractBuilder
        
        if contract_dict['model_name'] == 'dna_analyzer':
            contract = ContractBuilder.build_dna_analyzer_contract(feature_registry)
        elif contract_dict['model_name'] == 'temporal_model':
            contract = ContractBuilder.build_temporal_model_contract(feature_registry)
        elif contract_dict['model_name'] == 'industry_model':
            contract = ContractBuilder.build_industry_model_contract(feature_registry)
        elif contract_dict['model_name'] == 'ensemble_model':
            contract = ContractBuilder.build_ensemble_model_contract()
        else:
            # Fallback to basic reconstruction
            contract = ModelContract(
                model_name=contract_dict['model_name'],
                model_type=contract_dict['model_type'],
                version=contract_dict['version']
            )
            contract.feature_count = contract_dict['feature_count']
            contract.output_schema = contract_dict['output_schema']
        
        # Reconstruct metadata
        metadata_dict = save_dict['metadata']
        metadata = ModelMetadata(
            model_name=metadata_dict['model_name'],
            model_version=metadata_dict['model_version'],
            training_date=datetime.fromisoformat(metadata_dict['training_date']),
            training_dataset=metadata_dict['training_dataset'],
            performance_metrics=metadata_dict['performance_metrics']
        )
        
        # Restore statistics
        metadata.prediction_count = metadata_dict['prediction_count']
        metadata.error_count = metadata_dict['error_count']
        metadata.validation_failures = metadata_dict['validation_failures']
        
        if metadata_dict['last_prediction_date']:
            metadata.last_prediction_date = datetime.fromisoformat(metadata_dict['last_prediction_date'])
        
        # Create contractual model
        contractual_model = cls(model, contract, feature_pipeline, metadata)
        
        logger.info(f"Loaded contractual model: {metadata.model_name} v{metadata.model_version}")
        
        return contractual_model
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get comprehensive model information"""
        info = {
            'model_id': self.metadata.model_id,
            'model_name': self.metadata.model_name,
            'model_version': self.metadata.model_version,
            'model_type': self.contract.model_type,
            'training_date': self.metadata.training_date.isoformat(),
            'performance_metrics': self.metadata.performance_metrics,
            'feature_count': self.contract.feature_count,
            'feature_names': self.contract.get_feature_names(),
            'output_schema': self.contract.output_schema,
            'prediction_stats': {
                'total_predictions': self.metadata.prediction_count,
                'error_count': self.metadata.error_count,
                'validation_failures': self.metadata.validation_failures,
                'error_rate': self.metadata.error_count / max(1, self.metadata.prediction_count)
            }
        }
        
        # Add feature importance if available
        importance_df = self.get_feature_importance()
        if importance_df is not None:
            info['top_features'] = importance_df.head(10).to_dict('records')
        
        return info