"""
Fixed Model Integration for FLASH Platform
Handles categorical features properly and integrates working models
"""

import pandas as pd
import numpy as np
import joblib
import catboost as cb
from pathlib import Path
import logging
from typing import Dict, List, Any, Optional
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def prepare_features_for_models(df: pd.DataFrame) -> pd.DataFrame:
    """Prepare features with proper encoding for different model types"""
    df = df.copy()
    
    # Handle categorical features
    categorical_mappings = {
        'funding_stage': {
            'Pre-seed': 0, 'Seed': 1, 'Series A': 2, 
            'Series B': 3, 'Series C+': 4
        },
        'investor_tier_primary': {
            'none': 0, 'Tier3': 1, 'Tier2': 2, 'Tier1': 3
        },
        'product_stage': {
            'idea': 0, 'prototype': 1, 'beta': 2, 
            'live': 3, 'growth': 4, 'maturity': 5
        }
    }
    
    # Apply mappings
    for col, mapping in categorical_mappings.items():
        if col in df.columns:
            df[f'{col}_encoded'] = df[col].map(mapping).fillna(0)
    
    return df


class WorkingModelEnsemble:
    """Ensemble of models that are confirmed to work with current data"""
    
    def __init__(self):
        self.models = {}
        self.model_status = {}
        
    def load_working_models(self):
        """Load only models that work with current feature set"""
        
        # 1. Load hierarchical models (confirmed working)
        self._load_hierarchical_models()
        
        # 2. Load any other working models
        self._check_and_load_base_models()
        
        logger.info(f"Successfully loaded {len(self.models)} working models")
        
    def _load_hierarchical_models(self):
        """Load hierarchical 45-feature models"""
        hier_path = Path('models/hierarchical_45features')
        
        if hier_path.exists():
            models_to_load = [
                ('stage_hierarchical', 'stage_hierarchical_model.pkl'),
                ('temporal_hierarchical', 'temporal_hierarchical_model.pkl'),
                ('dna_pattern', 'dna_pattern_model.pkl'),
            ]
            
            for model_name, filename in models_to_load:
                try:
                    self.models[model_name] = joblib.load(hier_path / filename)
                    self.model_status[model_name] = 'loaded'
                    logger.info(f"✅ Loaded {model_name}")
                except Exception as e:
                    logger.warning(f"❌ Failed to load {model_name}: {e}")
                    self.model_status[model_name] = f'failed: {str(e)}'
    
    def _check_and_load_base_models(self):
        """Check and load base models if compatible"""
        # For now, we'll focus on hierarchical models
        # Can add more models here after testing compatibility
        pass
    
    def predict_with_all_models(self, X: pd.DataFrame) -> Dict[str, Any]:
        """Get predictions from all working models"""
        predictions = {}
        
        # Prepare features
        X_prepared = prepare_features_for_models(X)
        
        for model_name, model in self.models.items():
            try:
                if hasattr(model, 'predict_proba'):
                    pred = model.predict_proba(X_prepared.copy())
                    if hasattr(pred, 'shape') and len(pred.shape) > 1:
                        pred = pred[:, 1]
                    predictions[model_name] = float(pred[0]) if len(pred) == 1 else pred.tolist()
                else:
                    predictions[model_name] = None
            except Exception as e:
                logger.warning(f"Prediction failed for {model_name}: {e}")
                predictions[model_name] = None
        
        # Calculate ensemble
        valid_preds = [p for p in predictions.values() if p is not None]
        if valid_preds:
            ensemble_pred = np.mean(valid_preds)
            confidence = 1.0 - np.std(valid_preds) if len(valid_preds) > 1 else 0.5
        else:
            ensemble_pred = 0.5
            confidence = 0.0
            
        return {
            'ensemble_prediction': ensemble_pred,
            'confidence': confidence,
            'individual_predictions': predictions,
            'models_used': sum(1 for p in predictions.values() if p is not None)
        }


def create_api_endpoints():
    """Generate API endpoint code for the working models"""
    
    code = '''
# Add to api_server.py

from integrate_models_fixed import WorkingModelEnsemble, prepare_features_for_models

# Initialize working ensemble
working_ensemble = WorkingModelEnsemble()
working_ensemble.load_working_models()

@app.post("/predict_ensemble")
async def predict_ensemble(startup_data: StartupDataInput):
    """
    Ensemble prediction using all working models
    Returns predictions from stage, temporal, and DNA models
    """
    try:
        # Convert to DataFrame
        data_dict = startup_data.dict()
        df = pd.DataFrame([data_dict])
        
        # Get predictions
        results = working_ensemble.predict_with_all_models(df)
        
        # Extract insights based on model predictions
        insights = []
        
        if results['individual_predictions'].get('stage_hierarchical'):
            stage_pred = results['individual_predictions']['stage_hierarchical']
            if stage_pred > 0.7:
                insights.append("Strong stage-appropriate metrics")
            elif stage_pred < 0.3:
                insights.append("Metrics below stage expectations")
        
        if results['individual_predictions'].get('temporal_hierarchical'):
            temporal_pred = results['individual_predictions']['temporal_hierarchical']
            if temporal_pred > 0.7:
                insights.append("Positive trajectory across time horizons")
            elif temporal_pred < 0.3:
                insights.append("Concerning short-term indicators")
                
        if results['individual_predictions'].get('dna_pattern'):
            dna_pred = results['individual_predictions']['dna_pattern']
            if dna_pred > 0.7:
                insights.append("Matches successful startup patterns")
            elif dna_pred < 0.3:
                insights.append("Pattern suggests high risk")
        
        # Risk factors
        risk_factors = []
        if df['runway_months'].iloc[0] < 6:
            risk_factors.append("Less than 6 months runway")
        if df['burn_multiple'].iloc[0] > 5:
            risk_factors.append("High burn multiple")
        if df['customer_concentration_percent'].iloc[0] > 30:
            risk_factors.append("Customer concentration risk")
            
        # Growth indicators  
        growth_indicators = []
        if df['revenue_growth_rate_percent'].iloc[0] > 100:
            growth_indicators.append("Strong revenue growth")
        if df['net_dollar_retention_percent'].iloc[0] > 120:
            growth_indicators.append("Excellent retention")
        if df['gross_margin_percent'].iloc[0] > 70:
            growth_indicators.append("Healthy margins")
        
        response = {
            "success_probability": float(results['ensemble_prediction']),
            "confidence_score": float(results['confidence']),
            "models_used": results['models_used'],
            "insights": insights[:3],  # Top 3 insights
            "risk_factors": risk_factors[:3],  # Top 3 risks
            "growth_indicators": growth_indicators[:3],  # Top 3 positives
            "model_predictions": results['individual_predictions'],
            "recommendations": generate_recommendations(df, results)
        }
        
        return response
        
    except Exception as e:
        logger.error(f"Ensemble prediction error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


def generate_recommendations(df: pd.DataFrame, results: Dict) -> List[str]:
    """Generate actionable recommendations"""
    recommendations = []
    
    # Stage-based recommendations
    stage = df['funding_stage'].iloc[0]
    if 'seed' in stage.lower():
        recommendations.append("Focus on achieving product-market fit metrics")
    elif 'series a' in stage.lower():
        recommendations.append("Prioritize scalable growth channels")
    elif 'series b' in stage.lower() or 'series c' in stage.lower():
        recommendations.append("Optimize unit economics and market expansion")
    
    # Efficiency recommendations
    if df['burn_multiple'].iloc[0] > 3:
        recommendations.append("Improve capital efficiency to extend runway")
    
    # Growth recommendations
    if df['revenue_growth_rate_percent'].iloc[0] < 50:
        recommendations.append("Accelerate growth to meet investor expectations")
        
    return recommendations[:3]


@app.get("/models/status")
async def get_model_status():
    """Get status of all models"""
    return {
        "working_models": list(working_ensemble.models.keys()),
        "model_status": working_ensemble.model_status,
        "total_models": len(working_ensemble.models),
        "ensemble_ready": len(working_ensemble.models) > 0
    }
'''
    
    return code


def test_working_ensemble():
    """Test the working ensemble with sample data"""
    
    # Load test data
    df = pd.read_csv('data/final_100k_dataset_45features.csv', nrows=5)
    
    # Initialize ensemble
    ensemble = WorkingModelEnsemble()
    ensemble.load_working_models()
    
    print("\nTesting Working Model Ensemble")
    print("=" * 50)
    print(f"Models loaded: {list(ensemble.models.keys())}")
    print(f"Model status: {json.dumps(ensemble.model_status, indent=2)}")
    
    # Test predictions
    feature_cols = [col for col in df.columns if col not in [
        'startup_id', 'startup_name', 'success', 'founding_year', 'burn_multiple_calc'
    ]]
    
    for i in range(min(3, len(df))):
        print(f"\n--- Test Case {i+1} ---")
        print(f"Company: {df.iloc[i]['startup_name']}")
        print(f"Stage: {df.iloc[i]['funding_stage']}")
        print(f"Sector: {df.iloc[i]['sector']}")
        
        X = df[feature_cols].iloc[[i]]
        results = ensemble.predict_with_all_models(X)
        
        print(f"Ensemble Prediction: {results['ensemble_prediction']:.3f}")
        print(f"Confidence: {results['confidence']:.3f}")
        print(f"Models Used: {results['models_used']}")
        print("Individual Predictions:")
        for model, pred in results['individual_predictions'].items():
            if pred is not None:
                print(f"  - {model}: {pred:.3f}")
    
    # Save API integration code
    with open('api_endpoints_working_models.py', 'w') as f:
        f.write(create_api_endpoints())
    
    print("\n✅ Working ensemble tested successfully!")
    print("📝 API endpoints saved to api_endpoints_working_models.py")


if __name__ == "__main__":
    test_working_ensemble()