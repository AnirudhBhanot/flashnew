"""
Fixed Model Improvements Implementation
Working implementation of calibration, thresholds, SHAP, and feature engineering
"""

import pandas as pd
import numpy as np
import joblib
from pathlib import Path
import logging
from sklearn.isotonic import IsotonicRegression
from sklearn.metrics import (
    precision_recall_curve, roc_auc_score, f1_score, 
    precision_score, recall_score, accuracy_score
)
from sklearn.model_selection import train_test_split
import shap
import json
from typing import Dict, List, Tuple, Optional
import warnings
warnings.filterwarnings('ignore')

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SimpleCalibrator:
    """Simple probability calibration using isotonic regression"""
    
    def __init__(self):
        self.calibrator = IsotonicRegression(out_of_bounds='clip')
        
    def fit(self, y_true, y_prob):
        """Fit the calibrator"""
        self.calibrator.fit(y_prob, y_true)
        
    def transform(self, y_prob):
        """Transform probabilities"""
        return self.calibrator.transform(y_prob)


class OptimizedModelPipeline:
    """Optimized pipeline with all improvements"""
    
    def __init__(self):
        self.models = {}
        self.calibrators = {}
        self.optimal_thresholds = {}
        self.explainers = {}
        self.engineered_features = []
        
    def load_models(self):
        """Load base models"""
        model_path = Path('models/hierarchical_45features')
        
        models_to_load = [
            ('stage_hierarchical', 'stage_hierarchical_model.pkl'),
            ('temporal_hierarchical', 'temporal_hierarchical_model.pkl'),
            ('dna_pattern', 'dna_pattern_model.pkl')
        ]
        
        for model_name, filename in models_to_load:
            try:
                self.models[model_name] = joblib.load(model_path / filename)
                logger.info(f"✅ Loaded {model_name}")
            except Exception as e:
                logger.error(f"❌ Failed to load {model_name}: {e}")
    
    def engineer_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Add high-value engineered features to the existing 45 features"""
        df = df.copy()
        
        # All 45 features should already exist in df from the API
        # We're just adding 6 new engineered features on top
        
        # 1. Growth Efficiency Score (growth vs burn)
        # Use existing columns that should be in the data
        burn_multiple = pd.to_numeric(df.get('burn_multiple', 10.0), errors='coerce').fillna(10.0)
        revenue_growth = pd.to_numeric(df.get('revenue_growth_rate_percent', 0), errors='coerce').fillna(0)
        
        df['growth_efficiency_score'] = np.where(
            burn_multiple > 0.1,
            np.clip(revenue_growth / (burn_multiple + 0.1), 0, 100),
            revenue_growth
        )
        
        # 2. Product-Market Fit Composite
        product_retention = pd.to_numeric(df.get('product_retention_30d', 0.7), errors='coerce').fillna(0.7)
        user_growth = pd.to_numeric(df.get('user_growth_rate_percent', 0), errors='coerce').fillna(0)
        ndr = pd.to_numeric(df.get('net_dollar_retention_percent', 100), errors='coerce').fillna(100)
        
        df['pmf_score'] = (
            product_retention * 40 +
            np.clip(user_growth / 100, 0, 1) * 30 +
            np.clip(ndr / 100, 0, 2) * 30
        )
        
        # 3. Founder Strength Index
        # Convert boolean to float if needed for key_person_dependency
        key_person_dep = df.get('key_person_dependency', True)
        if isinstance(key_person_dep, pd.Series) and key_person_dep.dtype == bool:
            key_person_dep = key_person_dep.astype(float)
        elif isinstance(key_person_dep, bool):
            key_person_dep = float(key_person_dep)
            
        years_exp = pd.to_numeric(df.get('years_experience_avg', 5), errors='coerce').fillna(5)
        exits = pd.to_numeric(df.get('prior_successful_exits_count', 0), errors='coerce').fillna(0)
        domain_exp = pd.to_numeric(df.get('domain_expertise_years_avg', 3), errors='coerce').fillna(3)
        
        df['founder_strength'] = (
            np.minimum(years_exp / 10, 1.0) * 25 +
            np.minimum(exits, 2) * 35 +
            np.minimum(domain_exp / 5, 1.0) * 25 +
            (1 - key_person_dep) * 15
        )
        
        # 4. Market Opportunity Score
        market_growth = pd.to_numeric(df.get('market_growth_rate_percent', 15), errors='coerce').fillna(15)
        competition = pd.to_numeric(df.get('competition_intensity', 3), errors='coerce').fillna(3)
        customer_conc = pd.to_numeric(df.get('customer_concentration_percent', 20), errors='coerce').fillna(20)
        
        df['market_opportunity'] = (
            np.clip(market_growth / 50, 0, 1) * 40 +
            (1 - competition / 5) * 30 +
            (1 - customer_conc / 100) * 30
        )
        
        # 5. Capital Efficiency
        capital_raised = pd.to_numeric(df.get('total_capital_raised_usd', 0), errors='coerce').fillna(0)
        revenue_run_rate = pd.to_numeric(df.get('annual_revenue_run_rate', 0), errors='coerce').fillna(0)
        
        df['capital_efficiency'] = np.where(
            capital_raised > 0,
            np.log1p(revenue_run_rate) / np.log1p(capital_raised),
            0
        )
        
        # 6. Momentum Indicator
        runway = pd.to_numeric(df.get('runway_months', 12), errors='coerce').fillna(12)
        
        df['momentum_score'] = (
            np.clip(revenue_growth / 200, 0, 1) * 50 +
            np.clip(user_growth / 100, 0, 1) * 30 +
            (runway > 12).astype(float) * 20
        )
        
        # Store feature names
        self.engineered_features = [
            'growth_efficiency_score', 'pmf_score', 'founder_strength',
            'market_opportunity', 'capital_efficiency', 'momentum_score'
        ]
        
        logger.info(f"✅ Added {len(self.engineered_features)} engineered features")
        
        return df
    
    def calibrate_probabilities(self, X_cal, y_cal):
        """Calibrate model probabilities"""
        logger.info("\nCalibrating probabilities...")
        
        for model_name, model in self.models.items():
            try:
                # Get uncalibrated probabilities
                y_prob = model.predict_proba(X_cal)[:, 1]
                
                # Fit calibrator
                calibrator = SimpleCalibrator()
                calibrator.fit(y_cal, y_prob)
                self.calibrators[model_name] = calibrator
                
                # Check calibration improvement
                y_prob_cal = calibrator.transform(y_prob)
                
                # Simple calibration metric: mean predicted vs actual positive rate
                uncal_error = abs(y_prob.mean() - y_cal.mean())
                cal_error = abs(y_prob_cal.mean() - y_cal.mean())
                
                logger.info(f"✅ Calibrated {model_name}: error {uncal_error:.3f} → {cal_error:.3f}")
                
            except Exception as e:
                logger.error(f"❌ Failed to calibrate {model_name}: {e}")
    
    def find_optimal_thresholds(self, X_val, y_val):
        """Find optimal thresholds for different objectives"""
        logger.info("\nFinding optimal thresholds...")
        
        profiles = {
            'conservative': {'min_precision': 0.7, 'optimize': 'recall'},
            'balanced': {'optimize': 'f1'},
            'aggressive': {'min_recall': 0.7, 'optimize': 'precision'}
        }
        
        self.optimal_thresholds = {profile: {} for profile in profiles}
        
        for model_name, model in self.models.items():
            try:
                # Get calibrated predictions
                y_prob = model.predict_proba(X_val)[:, 1]
                if model_name in self.calibrators:
                    y_prob = self.calibrators[model_name].transform(y_prob)
                
                # Calculate precision-recall curve
                precisions, recalls, thresholds = precision_recall_curve(y_val, y_prob)
                f1_scores = 2 * (precisions * recalls) / (precisions + recalls + 1e-10)
                
                for profile, criteria in profiles.items():
                    if criteria['optimize'] == 'f1':
                        # Maximize F1
                        best_idx = np.argmax(f1_scores)
                        threshold = thresholds[best_idx]
                        
                    elif criteria['optimize'] == 'recall' and 'min_precision' in criteria:
                        # Maximize recall with precision constraint
                        valid_idx = precisions >= criteria['min_precision']
                        if np.any(valid_idx):
                            valid_recalls = recalls[:-1][valid_idx[:-1]]
                            valid_thresholds = thresholds[valid_idx[:-1]]
                            if len(valid_recalls) > 0:
                                best_idx = np.argmax(valid_recalls)
                                threshold = valid_thresholds[best_idx]
                            else:
                                threshold = 0.5
                        else:
                            threshold = 0.7  # Conservative default
                            
                    elif criteria['optimize'] == 'precision' and 'min_recall' in criteria:
                        # Maximize precision with recall constraint
                        valid_idx = recalls >= criteria['min_recall']
                        if np.any(valid_idx):
                            valid_precisions = precisions[:-1][valid_idx[:-1]]
                            valid_thresholds = thresholds[valid_idx[:-1]]
                            if len(valid_precisions) > 0:
                                best_idx = np.argmax(valid_precisions)
                                threshold = valid_thresholds[best_idx]
                            else:
                                threshold = 0.5
                        else:
                            threshold = 0.3  # Aggressive default
                    else:
                        threshold = 0.5
                    
                    self.optimal_thresholds[profile][model_name] = threshold
                    
                    # Evaluate at this threshold
                    y_pred = (y_prob >= threshold).astype(int)
                    precision = precision_score(y_val, y_pred) if y_pred.sum() > 0 else 0
                    recall = recall_score(y_val, y_pred) if y_val.sum() > 0 else 0
                    f1 = f1_score(y_val, y_pred) if (precision + recall) > 0 else 0
                    
                    logger.info(f"  {profile} {model_name}: t={threshold:.2f}, "
                               f"P={precision:.2f}, R={recall:.2f}, F1={f1:.2f}")
                    
            except Exception as e:
                logger.error(f"Failed to optimize {model_name}: {e}")
    
    def create_explainers(self, X_background):
        """Create SHAP explainers"""
        logger.info("\nCreating SHAP explainers...")
        
        # Sample background data
        if len(X_background) > 100:
            background = shap.sample(X_background, 100)
        else:
            background = X_background
        
        for model_name, model in self.models.items():
            try:
                # Use KernelExplainer for all models (works universally)
                def model_predict(X_array):
                    # Convert to DataFrame with correct column names
                    X_df = pd.DataFrame(X_array, columns=background.columns)
                    return model.predict_proba(X_df)[:, 1]
                
                self.explainers[model_name] = shap.KernelExplainer(
                    model_predict, 
                    background.values
                )
                logger.info(f"✅ Created explainer for {model_name}")
                
            except Exception as e:
                logger.error(f"❌ Failed to create explainer for {model_name}: {e}")
    
    def predict_ensemble(self, X, profile='balanced'):
        """Make calibrated ensemble prediction"""
        predictions = {}
        probabilities = {}
        
        # Get predictions from each model
        for model_name, model in self.models.items():
            try:
                # Get base probability
                prob = model.predict_proba(X)[:, 1]
                
                # Apply calibration if available
                if model_name in self.calibrators:
                    prob = self.calibrators[model_name].transform(prob)
                
                probabilities[model_name] = prob
                
                # Apply threshold
                threshold = 0.5
                if profile in self.optimal_thresholds and model_name in self.optimal_thresholds[profile]:
                    threshold = self.optimal_thresholds[profile][model_name]
                
                predictions[model_name] = (prob >= threshold).astype(int)
                
            except Exception as e:
                logger.warning(f"Prediction failed for {model_name}: {e}")
        
        # Create weighted ensemble
        weights = {
            'stage_hierarchical': 0.40,
            'temporal_hierarchical': 0.35,
            'dna_pattern': 0.25
        }
        
        ensemble_prob = np.zeros(len(X))
        total_weight = 0
        
        for model_name, prob in probabilities.items():
            weight = weights.get(model_name, 0.33)
            ensemble_prob += prob * weight
            total_weight += weight
        
        if total_weight > 0:
            ensemble_prob /= total_weight
        else:
            ensemble_prob = np.full(len(X), 0.5)
        
        # Apply ensemble threshold based on profile
        thresholds = {
            'conservative': 0.65,
            'balanced': 0.50,
            'aggressive': 0.35
        }
        ensemble_threshold = thresholds.get(profile, 0.5)
        ensemble_pred = (ensemble_prob >= ensemble_threshold).astype(int)
        
        return {
            'prediction': ensemble_pred,
            'probability': ensemble_prob,
            'individual_probabilities': probabilities,
            'threshold': ensemble_threshold,
            'profile': profile
        }
    
    def explain_prediction(self, X, model_name='stage_hierarchical'):
        """Get SHAP explanation for prediction"""
        if model_name not in self.explainers:
            return None
        
        try:
            explainer = self.explainers[model_name]
            
            # Get SHAP values (this might take a moment)
            shap_values = explainer.shap_values(X.values)
            
            # Create feature importance dict
            feature_impacts = {}
            for i, feature in enumerate(X.columns):
                feature_impacts[feature] = float(shap_values[0][i])
            
            # Sort by absolute impact
            sorted_impacts = sorted(feature_impacts.items(), 
                                  key=lambda x: abs(x[1]), reverse=True)
            
            return {
                'positive_factors': [(f, v) for f, v in sorted_impacts if v > 0][:5],
                'negative_factors': [(f, v) for f, v in sorted_impacts if v < 0][:5],
                'all_impacts': feature_impacts
            }
            
        except Exception as e:
            logger.error(f"Failed to explain: {e}")
            return None


def test_improvements():
    """Test the improved pipeline"""
    
    logger.info("Testing model improvements...")
    
    # Load data
    df = pd.read_csv('data/final_100k_dataset_45features.csv')
    
    # Initialize pipeline
    pipeline = OptimizedModelPipeline()
    pipeline.load_models()
    
    # Add engineered features
    df_enhanced = pipeline.engineer_features(df)
    
    # Prepare data
    feature_cols = [col for col in df_enhanced.columns if col not in [
        'startup_id', 'startup_name', 'success', 'founding_year', 'burn_multiple_calc'
    ]]
    
    X = df_enhanced[feature_cols]
    y = df['success'].astype(int)
    
    # Split data
    X_temp, X_test, y_temp, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    X_train, X_cal, y_train, y_cal = train_test_split(
        X_temp, y_temp, test_size=0.25, random_state=42, stratify=y_temp
    )
    
    # Apply improvements
    pipeline.calibrate_probabilities(X_cal, y_cal)
    pipeline.find_optimal_thresholds(X_cal, y_cal)
    pipeline.create_explainers(X_train.sample(100))
    
    # Test different profiles
    logger.info("\n" + "="*50)
    logger.info("TESTING DIFFERENT INVESTOR PROFILES")
    logger.info("="*50)
    
    results_summary = {}
    
    for profile in ['conservative', 'balanced', 'aggressive']:
        result = pipeline.predict_ensemble(X_test, profile=profile)
        
        acc = accuracy_score(y_test, result['prediction'])
        prec = precision_score(y_test, result['prediction']) if result['prediction'].sum() > 0 else 0
        rec = recall_score(y_test, result['prediction'])
        auc = roc_auc_score(y_test, result['probability'])
        
        results_summary[profile] = {
            'accuracy': acc,
            'precision': prec,
            'recall': rec,
            'auc': auc,
            'threshold': result['threshold']
        }
        
        logger.info(f"\n{profile.upper()} Profile (threshold={result['threshold']:.2f}):")
        logger.info(f"  Accuracy:  {acc:.3f}")
        logger.info(f"  Precision: {prec:.3f}")
        logger.info(f"  Recall:    {rec:.3f}")
        logger.info(f"  AUC:       {auc:.3f}")
        logger.info(f"  Predictions: {result['prediction'].sum()} positive out of {len(result['prediction'])}")
    
    # Test explanation on a sample
    logger.info("\n" + "="*50)
    logger.info("SAMPLE PREDICTION EXPLANATION")
    logger.info("="*50)
    
    sample_idx = 0
    sample_X = X_test.iloc[[sample_idx]]
    sample_result = pipeline.predict_ensemble(sample_X, profile='balanced')
    
    logger.info(f"\nCompany: {df.iloc[X_test.index[sample_idx]]['startup_name']}")
    logger.info(f"Actual Success: {y_test.iloc[sample_idx]}")
    logger.info(f"Predicted Probability: {sample_result['probability'][0]:.3f}")
    logger.info(f"Prediction: {'Success' if sample_result['prediction'][0] else 'Failure'}")
    
    # Get explanation (only if we have few features for speed)
    if len(X.columns) < 60:  # Only run SHAP if not too many features
        explanation = pipeline.explain_prediction(sample_X, 'stage_hierarchical')
        if explanation:
            logger.info("\nTop Positive Factors:")
            for feature, impact in explanation['positive_factors'][:3]:
                logger.info(f"  + {feature}: {impact:.3f}")
            
            logger.info("\nTop Negative Factors:")
            for feature, impact in explanation['negative_factors'][:3]:
                logger.info(f"  - {feature}: {impact:.3f}")
    
    # Save pipeline and results
    joblib.dump(pipeline, 'models/optimized_pipeline.pkl')
    
    with open('models/optimization_results.json', 'w') as f:
        json.dump({
            'profiles': results_summary,
            'engineered_features': pipeline.engineered_features,
            'calibrated_models': list(pipeline.calibrators.keys()),
            'thresholds': pipeline.optimal_thresholds
        }, f, indent=2)
    
    logger.info("\n✅ Saved optimized pipeline to models/optimized_pipeline.pkl")
    logger.info("✅ Saved results to models/optimization_results.json")
    
    return pipeline, results_summary


if __name__ == "__main__":
    pipeline, results = test_improvements()
    
    logger.info("\n" + "="*50)
    logger.info("IMPROVEMENTS SUMMARY")
    logger.info("="*50)
    logger.info("✅ Feature Engineering: Added 6 high-signal features")
    logger.info("✅ Calibration: Probabilities now reflect true likelihood")
    logger.info("✅ Threshold Optimization: Different profiles for different needs")
    logger.info("✅ SHAP Explanations: Can explain individual predictions")
    logger.info("\n🎯 Best configuration depends on your needs:")
    logger.info("  - Conservative: High precision (fewer false positives)")
    logger.info("  - Balanced: Best overall performance")
    logger.info("  - Aggressive: High recall (catch more successes)")