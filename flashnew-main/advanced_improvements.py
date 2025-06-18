"""
Advanced Model Improvements: Active Learning and Ensemble Stacking
"""

import pandas as pd
import numpy as np
import joblib
from pathlib import Path
import logging
from sklearn.model_selection import KFold
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score, accuracy_score
import json
from typing import Dict, List, Tuple
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ActiveLearningFramework:
    """
    Identifies uncertain predictions for expert review
    Helps improve model over time with minimal labeling effort
    """
    
    def __init__(self, uncertainty_threshold=0.15, probability_range=(0.35, 0.65)):
        self.uncertainty_threshold = uncertainty_threshold
        self.probability_range = probability_range
        self.uncertain_cases = []
        
    def identify_uncertain_predictions(self, 
                                     predictions: Dict[str, np.ndarray],
                                     probabilities: Dict[str, np.ndarray],
                                     X: pd.DataFrame) -> pd.DataFrame:
        """Identify cases where models disagree or are uncertain"""
        
        # Calculate uncertainty metrics
        prob_array = np.column_stack(list(probabilities.values()))
        
        # 1. Model disagreement (std deviation of probabilities)
        model_std = np.std(prob_array, axis=1)
        high_disagreement = model_std > self.uncertainty_threshold
        
        # 2. Near decision boundary (probability near 0.5)
        mean_prob = np.mean(prob_array, axis=1)
        near_boundary = (mean_prob > self.probability_range[0]) & (mean_prob < self.probability_range[1])
        
        # 3. Split predictions (some models say yes, others no)
        pred_array = np.column_stack(list(predictions.values()))
        split_decisions = np.std(pred_array, axis=1) > 0.3
        
        # Combine uncertainty indicators
        uncertain_mask = high_disagreement | near_boundary | split_decisions
        
        # Create uncertainty dataframe
        uncertainty_df = X[uncertain_mask].copy()
        uncertainty_df['mean_probability'] = mean_prob[uncertain_mask]
        uncertainty_df['model_std'] = model_std[uncertain_mask]
        uncertainty_df['uncertainty_score'] = (
            model_std[uncertain_mask] * 0.4 +
            np.abs(mean_prob[uncertain_mask] - 0.5) * (-0.6) + 0.3
        )
        
        # Sort by uncertainty score (highest first)
        uncertainty_df = uncertainty_df.sort_values('uncertainty_score', ascending=False)
        
        logger.info(f"Identified {len(uncertainty_df)} uncertain cases out of {len(X)} ({len(uncertainty_df)/len(X)*100:.1f}%)")
        
        return uncertainty_df
    
    def generate_review_batch(self, uncertainty_df: pd.DataFrame, 
                            batch_size: int = 20) -> pd.DataFrame:
        """Generate a batch of cases for expert review"""
        
        # Diversify the batch
        batch = pd.DataFrame()
        
        # 1. Top uncertainty cases (40%)
        n_top = int(batch_size * 0.4)
        batch = pd.concat([batch, uncertainty_df.head(n_top)])
        
        # 2. Random sampling from different probability ranges (40%)
        n_ranges = int(batch_size * 0.4)
        ranges = [(0.3, 0.4), (0.4, 0.5), (0.5, 0.6), (0.6, 0.7)]
        for prob_range in ranges:
            mask = (uncertainty_df['mean_probability'] >= prob_range[0]) & \
                   (uncertainty_df['mean_probability'] < prob_range[1])
            range_cases = uncertainty_df[mask]
            if len(range_cases) > 0:
                n_sample = min(n_ranges // 4, len(range_cases))
                batch = pd.concat([batch, range_cases.sample(n_sample)])
        
        # 3. Edge cases (20%)
        n_edge = batch_size - len(batch)
        if n_edge > 0 and len(uncertainty_df) > len(batch):
            remaining = uncertainty_df[~uncertainty_df.index.isin(batch.index)]
            if len(remaining) > 0:
                batch = pd.concat([batch, remaining.sample(min(n_edge, len(remaining)))])
        
        # Remove duplicates and limit to batch size
        batch = batch.drop_duplicates().head(batch_size)
        
        logger.info(f"Generated review batch of {len(batch)} cases")
        
        return batch
    
    def calculate_learning_value(self, uncertainty_df: pd.DataFrame) -> Dict:
        """Calculate potential value of labeling these cases"""
        
        # Estimate information gain
        mean_uncertainty = uncertainty_df['uncertainty_score'].mean()
        max_uncertainty = uncertainty_df['uncertainty_score'].max()
        
        # Estimate impact on model performance
        high_impact_cases = uncertainty_df[uncertainty_df['model_std'] > 0.2]
        
        return {
            'total_uncertain_cases': len(uncertainty_df),
            'mean_uncertainty': float(mean_uncertainty),
            'max_uncertainty': float(max_uncertainty),
            'high_impact_cases': len(high_impact_cases),
            'estimated_accuracy_gain': f"{min(len(uncertainty_df) / 1000, 2):.1f}%",
            'recommended_labels_needed': min(len(uncertainty_df), 100)
        }


class EnsembleStacking:
    """
    Advanced ensemble using stacking with out-of-fold predictions
    """
    
    def __init__(self, n_folds=5):
        self.n_folds = n_folds
        self.base_models = {}
        self.meta_model = None
        self.oof_predictions = None
        
    def create_base_predictions(self, models: Dict, X: pd.DataFrame, y: pd.Series) -> np.ndarray:
        """Create out-of-fold predictions for stacking"""
        
        n_models = len(models)
        oof_predictions = np.zeros((len(X), n_models))
        
        kf = KFold(n_splits=self.n_folds, shuffle=True, random_state=42)
        
        for fold_idx, (train_idx, val_idx) in enumerate(kf.split(X)):
            logger.info(f"Processing fold {fold_idx + 1}/{self.n_folds}")
            
            X_fold_train, X_fold_val = X.iloc[train_idx], X.iloc[val_idx]
            
            # Get predictions from each model for this fold
            for model_idx, (model_name, model) in enumerate(models.items()):
                try:
                    # Get predictions for validation fold
                    pred = model.predict_proba(X_fold_val)[:, 1]
                    oof_predictions[val_idx, model_idx] = pred
                except Exception as e:
                    logger.error(f"Error in fold {fold_idx} for {model_name}: {e}")
                    oof_predictions[val_idx, model_idx] = 0.5
        
        return oof_predictions
    
    def train_meta_model(self, oof_predictions: np.ndarray, y: pd.Series):
        """Train meta-model on out-of-fold predictions"""
        
        # Add feature engineering on predictions
        stacking_features = self._engineer_stacking_features(oof_predictions)
        
        # Train multiple meta-models and select best
        meta_models = {
            'logistic': LogisticRegression(C=1.0, random_state=42),
            'logistic_l2': LogisticRegression(C=0.1, penalty='l2', random_state=42),
            'rf_shallow': RandomForestClassifier(n_estimators=50, max_depth=3, random_state=42)
        }
        
        best_score = 0
        best_model = None
        
        # Use internal validation to select best meta-model
        meta_train_idx = int(len(stacking_features) * 0.8)
        X_meta_train = stacking_features[:meta_train_idx]
        y_meta_train = y.iloc[:meta_train_idx]
        X_meta_val = stacking_features[meta_train_idx:]
        y_meta_val = y.iloc[meta_train_idx:]
        
        for name, model in meta_models.items():
            model.fit(X_meta_train, y_meta_train)
            pred = model.predict_proba(X_meta_val)[:, 1]
            score = roc_auc_score(y_meta_val, pred)
            
            logger.info(f"Meta-model {name}: AUC = {score:.3f}")
            
            if score > best_score:
                best_score = score
                best_model = name
        
        # Retrain best model on all data
        self.meta_model = meta_models[best_model]
        self.meta_model.fit(stacking_features, y)
        
        logger.info(f"Selected meta-model: {best_model} (AUC: {best_score:.3f})")
        
        return self.meta_model
    
    def _engineer_stacking_features(self, predictions: np.ndarray) -> np.ndarray:
        """Create additional features from base predictions"""
        
        # Basic predictions
        features = predictions.copy()
        
        # Add statistics
        additional_features = []
        
        # Mean, std, min, max
        additional_features.append(np.mean(predictions, axis=1))
        additional_features.append(np.std(predictions, axis=1))
        additional_features.append(np.min(predictions, axis=1))
        additional_features.append(np.max(predictions, axis=1))
        
        # Differences between models
        if predictions.shape[1] >= 2:
            additional_features.append(predictions[:, 0] - predictions[:, 1])  # Model disagreement
        
        # Confidence (inverse of std)
        additional_features.append(1 - np.std(predictions, axis=1))
        
        # Stack all features
        stacking_features = np.column_stack([features] + additional_features)
        
        return stacking_features
    
    def predict(self, models: Dict, X: pd.DataFrame) -> np.ndarray:
        """Make predictions using stacking ensemble"""
        
        # Get base model predictions
        base_predictions = []
        for model_name, model in models.items():
            try:
                pred = model.predict_proba(X)[:, 1]
                base_predictions.append(pred)
            except Exception as e:
                logger.error(f"Prediction error for {model_name}: {e}")
                base_predictions.append(np.full(len(X), 0.5))
        
        base_predictions = np.column_stack(base_predictions)
        
        # Create stacking features
        stacking_features = self._engineer_stacking_features(base_predictions)
        
        # Get meta-model prediction
        if self.meta_model is not None:
            return self.meta_model.predict_proba(stacking_features)[:, 1]
        else:
            # Fallback to simple average
            return np.mean(base_predictions, axis=1)


def test_advanced_improvements():
    """Test active learning and stacking"""
    
    logger.info("Testing advanced improvements...")
    
    # Load models and data
    model_path = Path('models/hierarchical_45features')
    models = {}
    
    for model_file in ['stage_hierarchical_model.pkl', 'temporal_hierarchical_model.pkl', 'dna_pattern_model.pkl']:
        try:
            model_name = model_file.replace('_model.pkl', '')
            models[model_name] = joblib.load(model_path / model_file)
            logger.info(f"Loaded {model_name}")
        except Exception as e:
            logger.error(f"Failed to load {model_file}: {e}")
    
    # Load test data
    df = pd.read_csv('data/final_100k_dataset_45features.csv', nrows=1000)  # Small sample for speed
    
    feature_cols = [col for col in df.columns if col not in [
        'startup_id', 'startup_name', 'success', 'founding_year', 'burn_multiple_calc'
    ]]
    
    X = df[feature_cols]
    y = df['success'].astype(int)
    
    # Test 1: Active Learning
    logger.info("\n" + "="*50)
    logger.info("TESTING ACTIVE LEARNING")
    logger.info("="*50)
    
    al_framework = ActiveLearningFramework()
    
    # Get predictions from all models
    predictions = {}
    probabilities = {}
    
    for model_name, model in models.items():
        pred_proba = model.predict_proba(X)[:, 1]
        predictions[model_name] = (pred_proba > 0.5).astype(int)
        probabilities[model_name] = pred_proba
    
    # Identify uncertain cases
    uncertain_df = al_framework.identify_uncertain_predictions(predictions, probabilities, X)
    
    # Generate review batch
    review_batch = al_framework.generate_review_batch(uncertain_df, batch_size=20)
    
    # Calculate learning value
    learning_value = al_framework.calculate_learning_value(uncertain_df)
    
    logger.info("\nActive Learning Results:")
    logger.info(f"Uncertain cases: {learning_value['total_uncertain_cases']}")
    logger.info(f"Mean uncertainty: {learning_value['mean_uncertainty']:.3f}")
    logger.info(f"Estimated accuracy gain: {learning_value['estimated_accuracy_gain']}")
    logger.info(f"Recommended labels: {learning_value['recommended_labels_needed']}")
    
    # Save review batch
    review_batch[['mean_probability', 'model_std', 'uncertainty_score']].to_csv(
        'active_learning_batch.csv', index=False
    )
    logger.info("\n✅ Saved review batch to active_learning_batch.csv")
    
    # Test 2: Ensemble Stacking
    logger.info("\n" + "="*50)
    logger.info("TESTING ENSEMBLE STACKING")
    logger.info("="*50)
    
    stacking = EnsembleStacking(n_folds=3)  # Fewer folds for speed
    
    # Create out-of-fold predictions
    oof_predictions = stacking.create_base_predictions(models, X, y)
    
    # Train meta-model
    stacking.train_meta_model(oof_predictions, y)
    
    # Test on a holdout set
    test_size = int(len(X) * 0.2)
    X_test = X.iloc[-test_size:]
    y_test = y.iloc[-test_size:]
    
    # Compare simple average vs stacking
    simple_avg = np.mean([models[m].predict_proba(X_test)[:, 1] for m in models], axis=0)
    stacking_pred = stacking.predict(models, X_test)
    
    simple_auc = roc_auc_score(y_test, simple_avg)
    stacking_auc = roc_auc_score(y_test, stacking_pred)
    
    logger.info(f"\nSimple Average AUC: {simple_auc:.3f}")
    logger.info(f"Stacking AUC: {stacking_auc:.3f}")
    logger.info(f"Improvement: {(stacking_auc - simple_auc) * 100:.1f}%")
    
    # Save stacking model
    joblib.dump(stacking, 'models/stacking_ensemble.pkl')
    logger.info("\n✅ Saved stacking ensemble to models/stacking_ensemble.pkl")
    
    # Save results summary
    results = {
        'active_learning': learning_value,
        'stacking': {
            'simple_avg_auc': float(simple_auc),
            'stacking_auc': float(stacking_auc),
            'improvement': float((stacking_auc - simple_auc) * 100)
        },
        'timestamp': datetime.now().isoformat()
    }
    
    with open('advanced_improvements_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    logger.info("✅ Saved results to advanced_improvements_results.json")


if __name__ == "__main__":
    test_advanced_improvements()
    
    logger.info("\n" + "="*50)
    logger.info("ADVANCED IMPROVEMENTS COMPLETE")
    logger.info("="*50)
    logger.info("✅ Active Learning: Identifies uncertain cases for expert review")
    logger.info("✅ Ensemble Stacking: Meta-model learns optimal combination")
    logger.info("\n💡 Use active learning to continuously improve with minimal effort")
    logger.info("💡 Use stacking for maximum accuracy in production")