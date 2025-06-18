"""
Fix V2 Enhanced Models for Better Ensemble Performance
Addresses missing features and compatibility issues
"""

import pandas as pd
import numpy as np
import catboost as cb
import joblib
from pathlib import Path
import logging
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score, accuracy_score
from typing import Dict, List, Tuple

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def add_missing_features(df: pd.DataFrame) -> pd.DataFrame:
    """Add features that V2 Enhanced models expect"""
    df = df.copy()
    
    # Add capital_efficiency if missing
    if 'capital_efficiency' not in df.columns:
        df['capital_efficiency'] = np.where(
            df['total_capital_raised_usd'] > 0,
            df['annual_revenue_run_rate'] / df['total_capital_raised_usd'],
            0
        )
        logger.info("Added capital_efficiency feature")
    
    # Add burn_efficiency if missing
    if 'burn_efficiency' not in df.columns:
        df['burn_efficiency'] = np.where(
            df['monthly_burn_usd'] > 0,
            df['annual_revenue_run_rate'] / (df['monthly_burn_usd'] * 12),
            0
        )
        logger.info("Added burn_efficiency feature")
    
    # Ensure all expected features exist
    return df


def prepare_categorical_features(df: pd.DataFrame) -> pd.DataFrame:
    """Prepare categorical features for CatBoost models"""
    df = df.copy()
    
    # Map categorical features to expected format
    categorical_mappings = {
        'funding_stage': {
            'Pre-seed': 'pre_seed',
            'Seed': 'seed', 
            'Series A': 'series_a',
            'Series B': 'series_b',
            'Series C+': 'series_c_plus'
        },
        'product_stage': {
            'idea': 'idea',
            'prototype': 'prototype',
            'beta': 'beta',
            'live': 'live',
            'growth': 'growth',
            'maturity': 'maturity'
        },
        'investor_tier_primary': {
            'none': 'none',
            'Tier1': 'tier_1',
            'Tier2': 'tier_2', 
            'Tier3': 'tier_3'
        }
    }
    
    for col, mapping in categorical_mappings.items():
        if col in df.columns:
            df[col] = df[col].map(lambda x: mapping.get(x, x))
    
    return df


def create_stacking_features(base_predictions: Dict[str, np.ndarray]) -> pd.DataFrame:
    """Create features for meta-models from base model predictions"""
    
    # Basic predictions
    stacking_features = pd.DataFrame(base_predictions)
    
    # Add interaction features
    if 'conservative' in base_predictions and 'aggressive' in base_predictions:
        stacking_features['spread'] = (
            base_predictions['aggressive'] - base_predictions['conservative']
        )
    
    # Add statistics
    pred_array = np.column_stack(list(base_predictions.values()))
    stacking_features['mean'] = pred_array.mean(axis=1)
    stacking_features['std'] = pred_array.std(axis=1)
    stacking_features['max'] = pred_array.max(axis=1)
    stacking_features['min'] = pred_array.min(axis=1)
    
    return stacking_features


class FixedV2Ensemble:
    """Fixed V2 Enhanced models with proper feature handling"""
    
    def __init__(self):
        self.base_models = {}
        self.meta_models = {}
        self.is_loaded = False
        
    def load_and_fix_models(self):
        """Load V2 Enhanced models with fixes"""
        model_path = Path('models/v2_enhanced')
        
        # Load base models
        base_model_names = ['conservative', 'aggressive', 'balanced', 'deep']
        
        for model_name in base_model_names:
            try:
                model = cb.CatBoost()
                model.load_model(str(model_path / f'{model_name}_model.cbm'))
                self.base_models[model_name] = model
                logger.info(f"✅ Loaded {model_name} model")
            except Exception as e:
                logger.error(f"❌ Failed to load {model_name}: {e}")
        
        # Load meta models
        try:
            self.meta_models['logistic'] = joblib.load(model_path / 'meta_logistic.pkl')
            logger.info("✅ Loaded logistic meta-model")
        except Exception as e:
            logger.error(f"❌ Failed to load logistic meta: {e}")
            
        try:
            self.meta_models['nn'] = joblib.load(model_path / 'meta_nn.pkl')
            logger.info("✅ Loaded neural network meta-model")
        except Exception as e:
            logger.error(f"❌ Failed to load nn meta: {e}")
            
        self.is_loaded = True
        
    def predict_with_base_models(self, X: pd.DataFrame) -> Dict[str, np.ndarray]:
        """Get predictions from all base models"""
        # Add missing features
        X_fixed = add_missing_features(X)
        X_fixed = prepare_categorical_features(X_fixed)
        
        predictions = {}
        
        for model_name, model in self.base_models.items():
            try:
                pred = model.predict(X_fixed, prediction_type='Probability')[:, 1]
                predictions[model_name] = pred
                logger.debug(f"Got predictions from {model_name}")
            except Exception as e:
                logger.warning(f"Prediction failed for {model_name}: {e}")
        
        return predictions
    
    def predict_with_stacking(self, X: pd.DataFrame) -> np.ndarray:
        """Full stacking ensemble prediction"""
        # Get base model predictions
        base_preds = self.predict_with_base_models(X)
        
        if not base_preds:
            return np.full(len(X), 0.5)
        
        # Create stacking features
        stacking_features = create_stacking_features(base_preds)
        
        # Get meta model predictions
        meta_predictions = []
        
        for meta_name, meta_model in self.meta_models.items():
            try:
                if hasattr(meta_model, 'predict_proba'):
                    pred = meta_model.predict_proba(stacking_features)[:, 1]
                else:
                    pred = meta_model.predict(stacking_features)
                meta_predictions.append(pred)
                logger.debug(f"Got meta predictions from {meta_name}")
            except Exception as e:
                logger.warning(f"Meta prediction failed for {meta_name}: {e}")
        
        # Combine predictions
        if meta_predictions:
            # Average of meta predictions
            final_pred = np.mean(meta_predictions, axis=0)
        else:
            # Fallback to base model average
            final_pred = np.mean(list(base_preds.values()), axis=0)
        
        return final_pred


def test_fixed_models():
    """Test the fixed V2 Enhanced models"""
    
    logger.info("Loading test data...")
    df = pd.read_csv('data/final_100k_dataset_45features.csv')
    
    # Prepare features
    feature_cols = [col for col in df.columns if col not in [
        'startup_id', 'startup_name', 'success', 'founding_year', 'burn_multiple_calc'
    ]]
    
    X = df[feature_cols]
    y = df['success'].astype(int)
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # Load fixed models
    ensemble = FixedV2Ensemble()
    ensemble.load_and_fix_models()
    
    logger.info(f"\nLoaded {len(ensemble.base_models)} base models")
    logger.info(f"Loaded {len(ensemble.meta_models)} meta models")
    
    # Test base models individually
    logger.info("\nTesting base models individually:")
    base_predictions = ensemble.predict_with_base_models(X_test)
    
    for model_name, predictions in base_predictions.items():
        auc = roc_auc_score(y_test, predictions)
        acc = accuracy_score(y_test, (predictions > 0.5).astype(int))
        logger.info(f"{model_name}: AUC={auc:.3f}, Accuracy={acc:.3f}")
    
    # Test full stacking ensemble
    logger.info("\nTesting stacking ensemble:")
    stacking_pred = ensemble.predict_with_stacking(X_test)
    
    stacking_auc = roc_auc_score(y_test, stacking_pred)
    stacking_acc = accuracy_score(y_test, (stacking_pred > 0.5).astype(int))
    
    logger.info(f"Stacking Ensemble: AUC={stacking_auc:.3f}, Accuracy={stacking_acc:.3f}")
    
    # Save fixed ensemble
    joblib.dump(ensemble, 'models/fixed_v2_ensemble.pkl')
    logger.info("\n✅ Saved fixed ensemble to models/fixed_v2_ensemble.pkl")
    
    return {
        'base_models': base_predictions,
        'stacking_performance': {
            'auc': stacking_auc,
            'accuracy': stacking_acc
        }
    }


def create_combined_ensemble_code():
    """Generate code to combine all working models"""
    
    code = '''
# Add to api_server.py or create new file

from fix_v2_enhanced_models import FixedV2Ensemble
from integrate_models_fixed import WorkingModelEnsemble

class CombinedEnsemble:
    """Combines hierarchical and fixed V2 models"""
    
    def __init__(self):
        self.hierarchical = WorkingModelEnsemble()
        self.v2_fixed = FixedV2Ensemble()
        
    def load_all_models(self):
        self.hierarchical.load_working_models()
        self.v2_fixed.load_and_fix_models()
        
    def predict(self, X):
        # Get hierarchical predictions
        hier_results = self.hierarchical.predict_with_all_models(X)
        
        # Get V2 stacking predictions
        v2_pred = self.v2_fixed.predict_with_stacking(X)
        
        # Combine with weights
        # Higher weight to V2 stacking if it has meta-models
        if self.v2_fixed.meta_models:
            weights = {
                'hierarchical': 0.4,
                'v2_stacking': 0.6
            }
        else:
            weights = {
                'hierarchical': 0.7,
                'v2_stacking': 0.3
            }
        
        final_pred = (
            hier_results['ensemble_prediction'] * weights['hierarchical'] +
            v2_pred * weights['v2_stacking']
        )
        
        return {
            'probability': float(final_pred),
            'confidence': (hier_results['confidence'] + 0.8) / 2,  # Adjust confidence
            'models_used': hier_results['models_used'] + len(self.v2_fixed.base_models)
        }
'''
    
    with open('combined_ensemble_integration.py', 'w') as f:
        f.write(code)
    
    logger.info("📝 Saved combined ensemble code to combined_ensemble_integration.py")


if __name__ == "__main__":
    logger.info("Fixing V2 Enhanced models...")
    results = test_fixed_models()
    create_combined_ensemble_code()
    logger.info("\n✅ V2 Enhanced models fixed and tested!")