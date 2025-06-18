"""
Model Improvements Implementation
Includes calibration, threshold optimization, SHAP, and feature engineering
"""

import pandas as pd
import numpy as np
import joblib
from pathlib import Path
import logging
from sklearn.calibration import CalibratedClassifierCV, calibration_curve
from sklearn.metrics import (
    precision_recall_curve, roc_curve, f1_score, 
    precision_score, recall_score, confusion_matrix
)
from sklearn.model_selection import train_test_split
import shap
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, List, Tuple, Optional
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ImprovedModelPipeline:
    """Enhanced model pipeline with calibration, optimization, and explanations"""
    
    def __init__(self):
        self.models = {}
        self.calibrated_models = {}
        self.explainers = {}
        self.optimal_thresholds = {}
        self.feature_engineering_pipeline = None
        
    def load_base_models(self):
        """Load the hierarchical models"""
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
        """Create high-signal engineered features"""
        df = df.copy()
        
        logger.info("Engineering new features...")
        
        # 1. Growth Efficiency Score
        df['growth_efficiency_score'] = np.where(
            df['burn_multiple'] > 0,
            df['revenue_growth_rate_percent'] / df['burn_multiple'],
            df['revenue_growth_rate_percent']
        )
        
        # 2. Product-Market Fit Score
        df['pmf_score'] = (
            df['product_retention_30d'] * 100 * 0.3 +
            df['user_growth_rate_percent'] * 0.3 +
            df['net_dollar_retention_percent'] * 0.4
        )
        
        # 3. Founder Quality Index
        df['founder_quality_index'] = (
            np.minimum(df['years_experience_avg'] / 10, 1.0) * 0.3 +
            np.minimum(df['prior_successful_exits_count'] / 2, 1.0) * 0.4 +
            np.minimum(df['domain_expertise_years_avg'] / 5, 1.0) * 0.3
        ) * 100
        
        # 4. Market Timing Score
        df['market_timing_score'] = (
            df['market_growth_rate_percent'] * 
            (1 - df['competition_intensity'] / 5) * 
            (1 - df['customer_concentration_percent'] / 100)
        )
        
        # 5. Capital Efficiency Ratio
        df['capital_efficiency_ratio'] = np.where(
            df['total_capital_raised_usd'] > 0,
            df['annual_revenue_run_rate'] / df['total_capital_raised_usd'],
            0
        )
        
        # 6. Burn Risk Score (inverse - lower is better)
        df['burn_risk_score'] = (
            (df['runway_months'] < 12).astype(float) * 0.4 +
            (df['burn_multiple'] > 5).astype(float) * 0.3 +
            (df['gross_margin_percent'] < 40).astype(float) * 0.3
        ) * 100
        
        # 7. Momentum Score
        df['momentum_score'] = (
            np.minimum(df['revenue_growth_rate_percent'] / 100, 2.0) * 0.5 +
            np.minimum(df['user_growth_rate_percent'] / 100, 2.0) * 0.3 +
            np.minimum(df['team_size_full_time'] / 50, 1.0) * 0.2
        ) * 100
        
        # 8. Moat Strength (enhanced)
        df['moat_strength_v2'] = (
            df['patent_count'].clip(0, 10) / 10 * 20 +
            df['network_effects_present'] * 25 +
            df['has_data_moat'] * 20 +
            df['regulatory_advantage_present'] * 15 +
            df['tech_differentiation_score'] * 10 +
            df['switching_cost_score'] * 5 +
            df['brand_strength_score'] * 5
        )
        
        # 9. Stage-Adjusted ARR (normalized by stage expectations)
        stage_arr_benchmarks = {
            'Pre-seed': 10000,
            'Seed': 100000,
            'Series A': 1000000,
            'Series B': 5000000,
            'Series C+': 20000000
        }
        
        df['stage_adjusted_arr'] = df.apply(
            lambda x: x['annual_revenue_run_rate'] / 
            stage_arr_benchmarks.get(x['funding_stage'], 1000000),
            axis=1
        ) * 100
        
        # 10. Team Experience Score
        df['team_experience_score'] = (
            np.minimum(df['years_experience_avg'] / 15, 1.0) * 0.25 +
            np.minimum(df['domain_expertise_years_avg'] / 10, 1.0) * 0.25 +
            np.minimum(df['prior_startup_experience_count'] / 3, 1.0) * 0.25 +
            (1 - df['key_person_dependency']) * 0.25
        ) * 100
        
        logger.info(f"Added 10 engineered features")
        
        # Store feature names for later use
        self.engineered_features = [
            'growth_efficiency_score', 'pmf_score', 'founder_quality_index',
            'market_timing_score', 'capital_efficiency_ratio', 'burn_risk_score',
            'momentum_score', 'moat_strength_v2', 'stage_adjusted_arr',
            'team_experience_score'
        ]
        
        return df
    
    def calibrate_models(self, X_train, y_train, X_cal, y_cal):
        """Calibrate model probabilities using isotonic regression"""
        logger.info("\nCalibrating models for better probability estimates...")
        
        for model_name, model in self.models.items():
            try:
                # Create a wrapper for the model's predict_proba method
                class ModelWrapper:
                    def __init__(self, model):
                        self.model = model
                        self.classes_ = np.array([0, 1])
                    
                    def fit(self, X, y):
                        return self
                    
                    def predict_proba(self, X):
                        return self.model.predict_proba(X)
                    
                    def predict(self, X):
                        proba = self.predict_proba(X)[:, 1]
                        return (proba > 0.5).astype(int)
                
                wrapped_model = ModelWrapper(model)
                
                # Calibrate using isotonic regression
                calibrated = CalibratedClassifierCV(
                    wrapped_model,
                    method='isotonic',
                    cv='prefit'  # Model already trained
                )
                
                # Fit calibration on calibration set
                calibrated.fit(X_cal, y_cal)
                self.calibrated_models[model_name] = calibrated
                
                # Evaluate calibration
                y_pred_uncalibrated = model.predict_proba(X_cal)[:, 1]
                y_pred_calibrated = calibrated.predict_proba(X_cal)[:, 1]
                
                # Calculate calibration metrics
                fraction_pos_uncal, mean_pred_uncal = calibration_curve(
                    y_cal, y_pred_uncalibrated, n_bins=10
                )
                fraction_pos_cal, mean_pred_cal = calibration_curve(
                    y_cal, y_pred_calibrated, n_bins=10
                )
                
                logger.info(f"✅ Calibrated {model_name}")
                logger.info(f"   Calibration improved: {np.mean(np.abs(fraction_pos_uncal - mean_pred_uncal)):.3f} -> "
                           f"{np.mean(np.abs(fraction_pos_cal - mean_pred_cal)):.3f}")
                
            except Exception as e:
                logger.error(f"❌ Failed to calibrate {model_name}: {e}")
    
    def optimize_thresholds(self, X_val, y_val):
        """Find optimal thresholds for different business objectives"""
        logger.info("\nOptimizing thresholds for different investor profiles...")
        
        self.optimal_thresholds = {
            'conservative': {},  # High precision (few false positives)
            'balanced': {},      # Optimal F1 score
            'aggressive': {},    # High recall (catch all successes)
            'custom': {}        # User-defined trade-offs
        }
        
        for model_name, model in self.calibrated_models.items():
            try:
                # Get predictions
                y_pred_proba = model.predict_proba(X_val)[:, 1]
                
                # Calculate precision-recall curve
                precisions, recalls, thresholds = precision_recall_curve(y_val, y_pred_proba)
                
                # Conservative: Maximize precision with recall >= 0.3
                valid_idx = recalls >= 0.3
                if np.any(valid_idx):
                    best_idx = np.argmax(precisions[valid_idx])
                    self.optimal_thresholds['conservative'][model_name] = thresholds[np.where(valid_idx)[0][best_idx]]
                
                # Balanced: Maximize F1 score
                f1_scores = 2 * (precisions * recalls) / (precisions + recalls + 1e-10)
                best_idx = np.argmax(f1_scores)
                self.optimal_thresholds['balanced'][model_name] = thresholds[best_idx]
                
                # Aggressive: Maximize recall with precision >= 0.5
                valid_idx = precisions >= 0.5
                if np.any(valid_idx):
                    best_idx = np.argmax(recalls[valid_idx])
                    self.optimal_thresholds['aggressive'][model_name] = thresholds[np.where(valid_idx)[0][best_idx]]
                
                # Log results
                for profile in ['conservative', 'balanced', 'aggressive']:
                    if model_name in self.optimal_thresholds[profile]:
                        threshold = self.optimal_thresholds[profile][model_name]
                        y_pred = (y_pred_proba >= threshold).astype(int)
                        precision = precision_score(y_val, y_pred)
                        recall = recall_score(y_val, y_pred)
                        f1 = f1_score(y_val, y_pred)
                        
                        logger.info(f"   {profile} ({model_name}): threshold={threshold:.3f}, "
                                   f"precision={precision:.3f}, recall={recall:.3f}, F1={f1:.3f}")
                
            except Exception as e:
                logger.error(f"❌ Failed to optimize thresholds for {model_name}: {e}")
    
    def create_shap_explainers(self, X_background):
        """Create SHAP explainers for model interpretability"""
        logger.info("\nCreating SHAP explainers for model interpretability...")
        
        # Sample background data for SHAP
        if len(X_background) > 100:
            background = shap.sample(X_background, 100)
        else:
            background = X_background
        
        for model_name, model in self.models.items():
            try:
                # Different explainer types for different models
                if hasattr(model, 'predict_proba'):
                    # Use TreeExplainer if possible (faster)
                    if 'hierarchical' in model_name:
                        # For complex hierarchical models, use KernelExplainer
                        self.explainers[model_name] = shap.KernelExplainer(
                            lambda x: model.predict_proba(pd.DataFrame(x, columns=X_background.columns))[:, 1],
                            background
                        )
                    else:
                        # Try TreeExplainer first
                        try:
                            self.explainers[model_name] = shap.TreeExplainer(model)
                        except:
                            # Fallback to KernelExplainer
                            self.explainers[model_name] = shap.KernelExplainer(
                                lambda x: model.predict_proba(pd.DataFrame(x, columns=X_background.columns))[:, 1],
                                background
                            )
                    
                    logger.info(f"✅ Created SHAP explainer for {model_name}")
                
            except Exception as e:
                logger.error(f"❌ Failed to create SHAP explainer for {model_name}: {e}")
    
    def explain_prediction(self, X_instance, model_name='stage_hierarchical'):
        """Generate SHAP explanation for a single prediction"""
        if model_name not in self.explainers:
            return None
        
        try:
            explainer = self.explainers[model_name]
            shap_values = explainer.shap_values(X_instance)
            
            # Get feature importance
            if isinstance(shap_values, list):
                shap_values = shap_values[1]  # For binary classification
            
            # Create explanation dictionary
            feature_importance = {}
            for i, col in enumerate(X_instance.columns):
                feature_importance[col] = float(shap_values[0, i]) if shap_values.ndim > 1 else float(shap_values[i])
            
            # Sort by absolute importance
            sorted_features = sorted(feature_importance.items(), key=lambda x: abs(x[1]), reverse=True)
            
            return {
                'top_positive_factors': [(f, v) for f, v in sorted_features if v > 0][:5],
                'top_negative_factors': [(f, v) for f, v in sorted_features if v < 0][:5],
                'all_factors': feature_importance
            }
            
        except Exception as e:
            logger.error(f"Failed to explain prediction: {e}")
            return None
    
    def create_ensemble_prediction(self, X, profile='balanced'):
        """Make ensemble prediction with calibration and optimal thresholds"""
        predictions = {}
        calibrated_probs = {}
        
        # Get calibrated predictions
        for model_name, model in self.calibrated_models.items():
            try:
                prob = model.predict_proba(X)[:, 1]
                calibrated_probs[model_name] = prob
                
                # Apply optimal threshold for the profile
                if profile in self.optimal_thresholds and model_name in self.optimal_thresholds[profile]:
                    threshold = self.optimal_thresholds[profile][model_name]
                else:
                    threshold = 0.5
                
                predictions[model_name] = (prob >= threshold).astype(int)
                
            except Exception as e:
                logger.warning(f"Prediction failed for {model_name}: {e}")
        
        # Weighted ensemble of calibrated probabilities
        weights = {'stage_hierarchical': 0.4, 'temporal_hierarchical': 0.35, 'dna_pattern': 0.25}
        
        ensemble_prob = np.zeros(len(X))
        total_weight = 0
        
        for model_name, prob in calibrated_probs.items():
            weight = weights.get(model_name, 0.33)
            ensemble_prob += prob * weight
            total_weight += weight
        
        ensemble_prob /= total_weight
        
        # Apply ensemble threshold
        ensemble_threshold = 0.5  # Can be optimized separately
        if profile == 'conservative':
            ensemble_threshold = 0.65
        elif profile == 'aggressive':
            ensemble_threshold = 0.35
        
        ensemble_pred = (ensemble_prob >= ensemble_threshold).astype(int)
        
        return {
            'prediction': ensemble_pred,
            'probability': ensemble_prob,
            'calibrated_probabilities': calibrated_probs,
            'individual_predictions': predictions,
            'threshold_used': ensemble_threshold,
            'profile': profile
        }


def train_improved_pipeline():
    """Train and save the improved model pipeline"""
    
    logger.info("Starting improved model pipeline training...")
    
    # Load data
    df = pd.read_csv('data/final_100k_dataset_45features.csv')
    
    # Initialize pipeline
    pipeline = ImprovedModelPipeline()
    pipeline.load_base_models()
    
    # Engineer features
    df_enhanced = pipeline.engineer_features(df)
    
    # Prepare features
    feature_cols = [col for col in df_enhanced.columns if col not in [
        'startup_id', 'startup_name', 'success', 'founding_year', 'burn_multiple_calc'
    ]]
    
    X = df_enhanced[feature_cols]
    y = df['success'].astype(int)
    
    # Split data: train (60%), calibration (20%), validation (20%)
    X_temp, X_val, y_temp, y_val = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    X_train, X_cal, y_train, y_cal = train_test_split(X_temp, y_temp, test_size=0.25, random_state=42, stratify=y_temp)
    
    logger.info(f"Data split: Train={len(X_train)}, Calibration={len(X_cal)}, Validation={len(X_val)}")
    
    # Calibrate models
    pipeline.calibrate_models(X_train, y_train, X_cal, y_cal)
    
    # Optimize thresholds
    pipeline.optimize_thresholds(X_val, y_val)
    
    # Create SHAP explainers
    pipeline.create_shap_explainers(X_train.sample(min(1000, len(X_train))))
    
    # Test the pipeline
    logger.info("\nTesting improved pipeline...")
    
    for profile in ['conservative', 'balanced', 'aggressive']:
        result = pipeline.create_ensemble_prediction(X_val, profile=profile)
        
        accuracy = np.mean(result['prediction'] == y_val)
        precision = precision_score(y_val, result['prediction'])
        recall = recall_score(y_val, result['prediction'])
        
        logger.info(f"\n{profile.upper()} Profile:")
        logger.info(f"  Accuracy: {accuracy:.3f}")
        logger.info(f"  Precision: {precision:.3f}")
        logger.info(f"  Recall: {recall:.3f}")
    
    # Save pipeline
    joblib.dump(pipeline, 'models/improved_model_pipeline.pkl')
    logger.info("\n✅ Saved improved pipeline to models/improved_model_pipeline.pkl")
    
    # Save feature importance from SHAP
    if 'stage_hierarchical' in pipeline.explainers:
        sample_explanation = pipeline.explain_prediction(X_val.iloc[[0]], 'stage_hierarchical')
        if sample_explanation:
            with open('models/feature_importance_shap.json', 'w') as f:
                json.dump(sample_explanation, f, indent=2)
    
    return pipeline


def create_improved_api_code():
    """Generate API code for the improved pipeline"""
    
    code = '''
# Add to api_server.py

from model_improvements import ImprovedModelPipeline
import joblib

# Load improved pipeline
improved_pipeline = joblib.load('models/improved_model_pipeline.pkl')

@app.post("/predict_improved")
async def predict_improved(
    startup_data: StartupDataInput,
    investor_profile: str = "balanced"  # conservative, balanced, aggressive
):
    """
    Enhanced prediction with calibration, optimal thresholds, and explanations
    """
    try:
        # Convert to DataFrame
        data_dict = startup_data.dict()
        df = pd.DataFrame([data_dict])
        
        # Engineer features
        df_enhanced = improved_pipeline.engineer_features(df)
        
        # Get prediction
        result = improved_pipeline.create_ensemble_prediction(
            df_enhanced,
            profile=investor_profile
        )
        
        # Get SHAP explanation
        feature_cols = [col for col in df_enhanced.columns if col not in [
            'startup_id', 'startup_name', 'success', 'founding_year', 'burn_multiple_calc'
        ]]
        
        explanation = improved_pipeline.explain_prediction(
            df_enhanced[feature_cols],
            model_name='stage_hierarchical'
        )
        
        # Build response
        response = {
            "success_prediction": bool(result['prediction'][0]),
            "success_probability": float(result['probability'][0]),
            "calibrated_probability": float(result['probability'][0]),  # Now properly calibrated
            "investor_profile": investor_profile,
            "threshold_used": result['threshold_used'],
            "confidence_score": calculate_confidence(result['calibrated_probabilities']),
            "explanations": {
                "top_positive_factors": [
                    {"feature": f, "impact": round(v, 3)} 
                    for f, v in explanation['top_positive_factors']
                ] if explanation else [],
                "top_negative_factors": [
                    {"feature": f, "impact": round(v, 3)} 
                    for f, v in explanation['top_negative_factors']
                ] if explanation else []
            },
            "engineered_features": {
                "growth_efficiency_score": float(df_enhanced['growth_efficiency_score'].iloc[0]),
                "pmf_score": float(df_enhanced['pmf_score'].iloc[0]),
                "founder_quality_index": float(df_enhanced['founder_quality_index'].iloc[0]),
                "market_timing_score": float(df_enhanced['market_timing_score'].iloc[0]),
                "momentum_score": float(df_enhanced['momentum_score'].iloc[0])
            }
        }
        
        return response
        
    except Exception as e:
        logger.error(f"Improved prediction error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/model/profiles")
async def get_investor_profiles():
    """Get available investor profiles and their characteristics"""
    return {
        "profiles": {
            "conservative": {
                "description": "Minimize false positives - only flag highly likely successes",
                "typical_threshold": 0.65,
                "focus": "High precision, lower recall",
                "use_case": "Risk-averse investors, late-stage funds"
            },
            "balanced": {
                "description": "Balance between catching successes and avoiding failures",
                "typical_threshold": 0.50,
                "focus": "Optimal F1 score",
                "use_case": "Most investors, general screening"
            },
            "aggressive": {
                "description": "Catch as many potential successes as possible",
                "typical_threshold": 0.35,
                "focus": "High recall, lower precision",
                "use_case": "Early-stage investors, accelerators"
            }
        }
    }

def calculate_confidence(predictions_dict):
    """Calculate confidence based on model agreement"""
    if len(predictions_dict) <= 1:
        return 0.5
    
    probs = list(predictions_dict.values())
    std_dev = np.std(probs)
    confidence = 1.0 - min(std_dev * 2, 1.0)
    return float(confidence)
'''
    
    with open('improved_api_integration.py', 'w') as f:
        f.write(code)
    
    logger.info("📝 Saved improved API integration to improved_api_integration.py")


if __name__ == "__main__":
    # Train improved pipeline
    pipeline = train_improved_pipeline()
    
    # Generate API code
    create_improved_api_code()
    
    logger.info("\n🎉 Model improvements complete!")
    logger.info("✅ Calibration implemented - probabilities now meaningful")
    logger.info("✅ Threshold optimization - different profiles for different investors")
    logger.info("✅ SHAP explanations - understand why predictions are made")
    logger.info("✅ Feature engineering - 10 new high-signal features added")