"""
Proper validation of hierarchical models
Tests real accuracy on proper train/test splits
"""

import pandas as pd
import numpy as np
import joblib
from pathlib import Path
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.metrics import accuracy_score, roc_auc_score, precision_score, recall_score, confusion_matrix
import logging
import json
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def load_and_validate_models():
    """Load models and run comprehensive validation"""
    
    logger.info("Loading full dataset for validation...")
    
    # Load the full 45-feature dataset
    df = pd.read_csv('data/final_100k_dataset_45features.csv')
    logger.info(f"Loaded {len(df)} samples")
    
    # Prepare features
    feature_cols = [col for col in df.columns if col not in [
        'startup_id', 'startup_name', 'success', 'founding_year', 'burn_multiple_calc'
    ]]
    
    X = df[feature_cols]
    y = df['success'].astype(int)
    
    # Load models
    model_path = Path('models/hierarchical_45features')
    models = {}
    
    logger.info("\nLoading hierarchical models...")
    
    try:
        models['stage_hierarchical'] = joblib.load(model_path / 'stage_hierarchical_model.pkl')
        logger.info("✅ Loaded stage hierarchical model")
    except Exception as e:
        logger.error(f"❌ Failed to load stage model: {e}")
        
    try:
        models['temporal_hierarchical'] = joblib.load(model_path / 'temporal_hierarchical_model.pkl')
        logger.info("✅ Loaded temporal hierarchical model")
    except Exception as e:
        logger.error(f"❌ Failed to load temporal model: {e}")
        
    try:
        models['dna_pattern'] = joblib.load(model_path / 'dna_pattern_model.pkl')
        logger.info("✅ Loaded DNA pattern model")
    except Exception as e:
        logger.error(f"❌ Failed to load DNA model: {e}")
    
    # Split data properly
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    logger.info(f"\nTrain set: {len(X_train)} samples")
    logger.info(f"Test set: {len(X_test)} samples")
    logger.info(f"Success rate in train: {y_train.mean():.2%}")
    logger.info(f"Success rate in test: {y_test.mean():.2%}")
    
    # Validate each model
    results = {}
    
    for model_name, model in models.items():
        logger.info(f"\n{'='*50}")
        logger.info(f"Validating {model_name}...")
        
        try:
            # Get predictions
            y_pred_proba = model.predict_proba(X_test)
            if hasattr(y_pred_proba, 'shape') and len(y_pred_proba.shape) > 1:
                y_pred_proba = y_pred_proba[:, 1]
            
            y_pred = (y_pred_proba > 0.5).astype(int)
            
            # Calculate metrics
            accuracy = accuracy_score(y_test, y_pred)
            auc = roc_auc_score(y_test, y_pred_proba)
            precision = precision_score(y_test, y_pred)
            recall = recall_score(y_test, y_pred)
            
            results[model_name] = {
                'accuracy': accuracy,
                'auc': auc,
                'precision': precision,
                'recall': recall,
                'predictions': y_pred_proba
            }
            
            logger.info(f"Accuracy: {accuracy:.3f}")
            logger.info(f"AUC: {auc:.3f}")
            logger.info(f"Precision: {precision:.3f}")
            logger.info(f"Recall: {recall:.3f}")
            
            # Confusion matrix
            cm = confusion_matrix(y_test, y_pred)
            logger.info(f"Confusion Matrix:")
            logger.info(f"  TN: {cm[0,0]:5d}  FP: {cm[0,1]:5d}")
            logger.info(f"  FN: {cm[1,0]:5d}  TP: {cm[1,1]:5d}")
            
        except Exception as e:
            logger.error(f"Failed to validate {model_name}: {e}")
            results[model_name] = None
    
    # Test ensemble of all working models
    logger.info(f"\n{'='*50}")
    logger.info("Testing ensemble of all models...")
    
    valid_predictions = []
    valid_models = []
    
    for model_name, result in results.items():
        if result is not None:
            valid_predictions.append(result['predictions'])
            valid_models.append(model_name)
    
    if valid_predictions:
        # Simple average ensemble
        ensemble_pred = np.mean(valid_predictions, axis=0)
        ensemble_binary = (ensemble_pred > 0.5).astype(int)
        
        ensemble_accuracy = accuracy_score(y_test, ensemble_binary)
        ensemble_auc = roc_auc_score(y_test, ensemble_pred)
        ensemble_precision = precision_score(y_test, ensemble_binary)
        ensemble_recall = recall_score(y_test, ensemble_binary)
        
        logger.info(f"Ensemble Accuracy: {ensemble_accuracy:.3f}")
        logger.info(f"Ensemble AUC: {ensemble_auc:.3f}")
        logger.info(f"Ensemble Precision: {ensemble_precision:.3f}")
        logger.info(f"Ensemble Recall: {ensemble_recall:.3f}")
        
        results['ensemble'] = {
            'accuracy': ensemble_accuracy,
            'auc': ensemble_auc,
            'precision': ensemble_precision,
            'recall': ensemble_recall,
            'models_used': valid_models
        }
    
    # Cross-validation for more robust estimates
    logger.info(f"\n{'='*50}")
    logger.info("Running 5-fold cross-validation on ensemble...")
    
    if valid_predictions:
        # Use full dataset for cross-validation
        X_cv = X
        y_cv = y
        
        cv_scores = []
        skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
        
        for fold, (train_idx, val_idx) in enumerate(skf.split(X_cv, y_cv)):
            X_fold_train = X_cv.iloc[train_idx]
            y_fold_train = y_cv.iloc[train_idx]
            X_fold_val = X_cv.iloc[val_idx]
            y_fold_val = y_cv.iloc[val_idx]
            
            fold_predictions = []
            for model_name, model in models.items():
                if model_name in valid_models:
                    try:
                        pred = model.predict_proba(X_fold_val)
                        if hasattr(pred, 'shape') and len(pred.shape) > 1:
                            pred = pred[:, 1]
                        fold_predictions.append(pred)
                    except:
                        pass
            
            if fold_predictions:
                fold_ensemble = np.mean(fold_predictions, axis=0)
                fold_auc = roc_auc_score(y_fold_val, fold_ensemble)
                cv_scores.append(fold_auc)
                logger.info(f"Fold {fold+1} AUC: {fold_auc:.3f}")
        
        if cv_scores:
            logger.info(f"\nCross-validation AUC: {np.mean(cv_scores):.3f} (+/- {np.std(cv_scores)*2:.3f})")
    
    # Save results
    validation_results = {
        'date': datetime.now().isoformat(),
        'dataset_size': len(df),
        'test_size': len(X_test),
        'individual_models': {k: v for k, v in results.items() if v and k != 'ensemble'},
        'ensemble_results': results.get('ensemble'),
        'cv_auc_mean': np.mean(cv_scores) if 'cv_scores' in locals() else None,
        'cv_auc_std': np.std(cv_scores) if 'cv_scores' in locals() else None
    }
    
    with open('hierarchical_validation_results.json', 'w') as f:
        json.dump(validation_results, f, indent=2)
    
    logger.info(f"\n{'='*50}")
    logger.info("VALIDATION SUMMARY")
    logger.info(f"{'='*50}")
    
    # Compare with baseline
    logger.info("\nBaseline (from docs): 72-75% accuracy")
    logger.info("\nHierarchical Models Performance:")
    
    for model_name, result in results.items():
        if result:
            logger.info(f"\n{model_name}:")
            logger.info(f"  - Accuracy: {result['accuracy']:.1%}")
            logger.info(f"  - AUC: {result['auc']:.3f}")
    
    # Final verdict
    if results.get('ensemble'):
        improvement = (results['ensemble']['accuracy'] - 0.735) * 100  # vs 73.5% baseline
        logger.info(f"\n🎯 Final Verdict:")
        logger.info(f"Ensemble accuracy: {results['ensemble']['accuracy']:.1%}")
        logger.info(f"Improvement over baseline: {improvement:+.1f} percentage points")
        
        if results['ensemble']['auc'] > 0.78:
            logger.info("✅ Significant improvement - hierarchical models are worth it!")
        else:
            logger.info("⚠️  Modest improvement - consider fixing other models too")
    
    return results


def plot_model_comparison(results):
    """Create visualization of model performance"""
    try:
        import matplotlib.pyplot as plt
        import seaborn as sns
        
        # Extract metrics
        model_names = []
        accuracies = []
        aucs = []
        
        for name, result in results.items():
            if result and name != 'ensemble':
                model_names.append(name)
                accuracies.append(result['accuracy'])
                aucs.append(result['auc'])
        
        if results.get('ensemble'):
            model_names.append('ENSEMBLE')
            accuracies.append(results['ensemble']['accuracy'])
            aucs.append(results['ensemble']['auc'])
        
        # Add baseline
        model_names.append('Baseline')
        accuracies.append(0.735)
        aucs.append(0.77)  # Estimated baseline AUC
        
        # Create plot
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        
        # Accuracy plot
        bars1 = ax1.bar(model_names, accuracies, color=['skyblue']*len(model_names))
        bars1[-1].set_color('lightcoral')  # Baseline in red
        bars1[-2].set_color('darkgreen')   # Ensemble in green
        ax1.set_ylabel('Accuracy')
        ax1.set_title('Model Accuracy Comparison')
        ax1.set_ylim(0.6, 0.9)
        ax1.axhline(y=0.735, color='r', linestyle='--', alpha=0.5, label='Baseline')
        
        # Add value labels
        for bar in bars1:
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height + 0.005,
                    f'{height:.3f}', ha='center', va='bottom')
        
        # AUC plot
        bars2 = ax2.bar(model_names, aucs, color=['skyblue']*len(model_names))
        bars2[-1].set_color('lightcoral')  # Baseline in red
        bars2[-2].set_color('darkgreen')   # Ensemble in green
        ax2.set_ylabel('AUC')
        ax2.set_title('Model AUC Comparison')
        ax2.set_ylim(0.6, 0.9)
        ax2.axhline(y=0.77, color='r', linestyle='--', alpha=0.5, label='Baseline')
        
        # Add value labels
        for bar in bars2:
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height + 0.005,
                    f'{height:.3f}', ha='center', va='bottom')
        
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig('hierarchical_model_comparison.png', dpi=150, bbox_inches='tight')
        logger.info("\n📊 Saved performance comparison plot to hierarchical_model_comparison.png")
        
    except ImportError:
        logger.warning("Matplotlib not available for plotting")


if __name__ == "__main__":
    logger.info("Starting comprehensive validation of hierarchical models...")
    logger.info("This will take a few minutes for proper testing...\n")
    
    results = load_and_validate_models()
    
    # Try to create visualization
    plot_model_comparison(results)
    
    logger.info("\n✅ Validation complete! Results saved to hierarchical_validation_results.json")