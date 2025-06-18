"""
Consolidated API Integration Module
Provides functions to integrate advanced models into the main API server
"""

from pathlib import Path
import logging
import catboost as cb
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)


def load_advanced_models(models_dir: Path = Path("models")) -> Dict[str, Any]:
    """
    Load all advanced ML models from the models directory
    
    Returns:
        Dictionary containing loaded models
    """
    loaded_models = {}
    
    # Load Stage-Based Models
    try:
        stage_path = models_dir / "stage_hierarchical"
        if stage_path.exists():
            from stage_hierarchical_models import StageHierarchicalModel
            stage_model = StageHierarchicalModel()
            stage_model.load_models(stage_path)
            loaded_models['stage_model'] = stage_model
            logger.info("Stage-based hierarchical models loaded")
    except Exception as e:
        logger.error(f"Failed to load stage models: {e}")
    
    # Load DNA Pattern Analyzer
    try:
        dna_path = models_dir / "dna_analyzer"
        if dna_path.exists():
            from dna_pattern_analysis import StartupDNAAnalyzer
            dna_analyzer = StartupDNAAnalyzer()
            dna_analyzer.load(dna_path)
            loaded_models['dna_analyzer'] = dna_analyzer
            logger.info("DNA pattern analyzer loaded")
    except Exception as e:
        logger.error(f"Failed to load DNA analyzer: {e}")
    
    # Load Temporal Models
    try:
        temporal_path = models_dir / "temporal"
        if temporal_path.exists():
            from temporal_models import TemporalPredictionModel
            temporal_model = TemporalPredictionModel()
            temporal_model.load(temporal_path)
            loaded_models['temporal_model'] = temporal_model
            logger.info("Temporal models loaded")
    except Exception as e:
        logger.error(f"Failed to load temporal models: {e}")
    
    # Load Industry-Specific Models
    try:
        industry_path = models_dir / "industry_specific"
        if industry_path.exists():
            from industry_specific_models import IndustrySpecificModel
            industry_model = IndustrySpecificModel()
            industry_model.load(industry_path)
            loaded_models['industry_model'] = industry_model
            logger.info("Industry-specific models loaded")
    except Exception as e:
        logger.error(f"Failed to load industry models: {e}")
    
    return loaded_models


def get_comprehensive_prediction(df, models: Dict[str, Any]) -> Dict[str, Any]:
    """
    Get predictions from all available models
    
    Args:
        df: Input DataFrame
        models: Dictionary of loaded models
        
    Returns:
        Comprehensive prediction results
    """
    results = {
        'predictions': {},
        'insights': {},
        'confidence_scores': {}
    }
    
    # Stage-based prediction
    if 'stage_model' in models:
        try:
            stage_pred = models['stage_model'].predict_proba(df)[:, 1]
            results['predictions']['stage'] = float(stage_pred[0])
            results['insights']['stage'] = models['stage_model'].get_stage_insights(df)
        except Exception as e:
            logger.error(f"Stage prediction error: {e}")
    
    # DNA pattern prediction
    if 'dna_analyzer' in models:
        try:
            dna_pattern = models['dna_analyzer'].predict_growth_trajectory(df)
            results['predictions']['dna'] = dna_pattern.get('success_probability', 0.5)
            results['insights']['dna'] = dna_pattern
        except Exception as e:
            logger.error(f"DNA prediction error: {e}")
    
    # Temporal prediction
    if 'temporal_model' in models:
        try:
            temporal_preds = models['temporal_model'].predict_temporal(df)
            results['predictions']['temporal'] = temporal_preds
            results['insights']['temporal'] = models['temporal_model'].get_temporal_insights(temporal_preds)
        except Exception as e:
            logger.error(f"Temporal prediction error: {e}")
    
    # Industry-specific prediction
    if 'industry_model' in models and 'sector' in df.columns:
        try:
            industry_pred = models['industry_model'].predict_proba(df)[:, 1]
            results['predictions']['industry'] = float(industry_pred[0])
            results['insights']['industry'] = models['industry_model'].get_industry_insights(df['sector'].iloc[0])
        except Exception as e:
            logger.error(f"Industry prediction error: {e}")
    
    # Calculate ensemble prediction
    if results['predictions']:
        predictions = list(results['predictions'].values())
        # Handle temporal predictions which might be a dict
        flat_predictions = []
        for pred in predictions:
            if isinstance(pred, dict):
                flat_predictions.extend(pred.values())
            else:
                flat_predictions.append(pred)
        
        results['ensemble_probability'] = sum(flat_predictions) / len(flat_predictions)
        results['confidence_score'] = 1.0 - (max(flat_predictions) - min(flat_predictions))
    else:
        results['ensemble_probability'] = 0.5
        results['confidence_score'] = 0.0
    
    return results


def integrate_with_api_server():
    """
    Code snippet to integrate advanced models with the main API server
    Copy this into api_server.py
    """
    integration_code = '''
# Add to imports section
from api_integration import load_advanced_models, get_comprehensive_prediction

# Add to global variables section
ADVANCED_MODELS = {}

# Add to startup_event function
@app.on_event("startup")
async def startup_event():
    global ADVANCED_MODELS
    # ... existing code ...
    
    # Load advanced models
    ADVANCED_MODELS = load_advanced_models()
    logger.info(f"Loaded {len(ADVANCED_MODELS)} advanced models")

# Add new endpoint
@app.post("/predict_comprehensive")
async def predict_comprehensive(
    request: Request,
    metrics: StartupMetrics,
    include_all_models: bool = True
):
    """Comprehensive prediction using all available models"""
    try:
        # Get standard prediction first
        standard_result = await predict(request, metrics)
        
        # Get advanced predictions if models available
        if ADVANCED_MODELS and include_all_models:
            df = pd.DataFrame([metrics.dict()])
            advanced_results = get_comprehensive_prediction(df, ADVANCED_MODELS)
            
            # Combine results
            return {
                "success_probability": standard_result.success_probability,
                "ensemble_probability": advanced_results.get('ensemble_probability', standard_result.success_probability),
                "confidence_score": advanced_results.get('confidence_score', 0.5),
                "pillar_scores": standard_result.pillar_scores,
                "predictions": {
                    "standard": standard_result.success_probability,
                    **advanced_results.get('predictions', {})
                },
                "insights": {
                    "standard": {
                        "verdict": standard_result.verdict,
                        "key_insights": standard_result.key_insights
                    },
                    **advanced_results.get('insights', {})
                },
                "risk_factors": standard_result.risk_factors,
                "recommendation": standard_result.recommendation
            }
        else:
            return standard_result.dict()
            
    except Exception as e:
        logger.error(f"Comprehensive prediction error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
'''
    
    return integration_code


if __name__ == "__main__":
    # Test loading models
    models = load_advanced_models()
    print(f"Successfully loaded {len(models)} models: {list(models.keys())}")
    
    # Show integration code
    print("\nIntegration code for api_server.py:")
    print(integrate_with_api_server())