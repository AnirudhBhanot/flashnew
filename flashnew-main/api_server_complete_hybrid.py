#!/usr/bin/env python3
"""
Complete Hybrid API Server
Integrates Base + Pattern + Stage + Industry + CAMP models
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
import uvicorn
from datetime import datetime
import logging

# Import the complete orchestrator
from complete_hybrid_orchestrator import CompleteHybridOrchestrator, CompleteHybridPrediction

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="FLASH Complete Hybrid API",
    description="Comprehensive startup evaluation with all model types",
    version="4.0.0"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request model (same as before)
class StartupData(BaseModel):
    """Input data for startup evaluation"""
    funding_stage: str
    total_capital_raised_usd: float
    cash_on_hand_usd: float
    monthly_burn_usd: float
    runway_months: float
    annual_revenue_run_rate: float
    revenue_growth_rate_percent: float
    gross_margin_percent: float
    burn_multiple: float
    ltv_cac_ratio: float
    investor_tier_primary: str
    has_debt: bool
    patent_count: int
    network_effects_present: bool
    has_data_moat: bool
    regulatory_advantage_present: bool
    tech_differentiation_score: float
    switching_cost_score: float
    brand_strength_score: float
    scalability_score: float
    product_stage: str
    product_retention_30d: float
    product_retention_90d: float
    sector: str
    tam_size_usd: float
    sam_size_usd: float
    som_size_usd: float
    market_growth_rate_percent: float
    customer_count: int
    customer_concentration_percent: float
    user_growth_rate_percent: float
    net_dollar_retention_percent: float
    competition_intensity: int
    competitors_named_count: int
    dau_mau_ratio: float
    founders_count: int
    team_size_full_time: int
    years_experience_avg: float
    domain_expertise_years_avg: float
    prior_startup_experience_count: int
    prior_successful_exits_count: int
    board_advisor_experience_score: float
    advisors_count: int
    team_diversity_percent: float
    key_person_dependency: int

# Initialize orchestrator
orchestrator = CompleteHybridOrchestrator()

@app.on_event("startup")
async def startup_event():
    """Load models on startup"""
    orchestrator.load_models()
    logger.info("Complete Hybrid API server started successfully")

@app.get("/")
async def root():
    """Root endpoint"""
    model_counts = {
        'base': len(orchestrator.models['base']),
        'patterns': len(orchestrator.models['patterns']),
        'stages': len(orchestrator.models['stages']),
        'industries': len(orchestrator.models['industries']),
        'camp': len(orchestrator.models['camp'])
    }
    
    return {
        "name": "FLASH Complete Hybrid API",
        "version": "4.0.0",
        "description": "Comprehensive evaluation with 5 model types",
        "model_counts": model_counts,
        "total_models": sum(model_counts.values()),
        "endpoints": [
            "/predict",
            "/predict_detailed",
            "/model_info",
            "/system_performance",
            "/health"
        ]
    }

@app.post("/predict")
async def predict(data: StartupData):
    """Make comprehensive prediction"""
    try:
        # Convert to dict
        startup_data = data.model_dump()
        
        # Get complete prediction
        result = orchestrator.predict(startup_data)
        
        # Return simplified response for frontend compatibility
        return {
            'success_probability': result.final_probability,
            'confidence_score': result.confidence_score,
            'verdict': result.verdict,
            'risk_level': result.risk_level,
            'key_insights': [
                f"Stage fit: {result.stage_fit}",
                f"Industry fit: {result.industry_fit}",
                f"Dominant pattern: {result.dominant_patterns[0] if result.dominant_patterns else 'None'}"
            ],
            'recommendations': result.recommendations,
            'camp_scores': result.camp_scores,
            'model_components': {
                'base': result.base_probability,
                'patterns': result.pattern_probability,
                'stage': result.stage_probability,
                'industry': result.industry_probability,
                'camp_avg': sum(result.camp_scores.values()) / 4
            }
        }
        
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/predict_detailed")
async def predict_detailed(data: StartupData):
    """Make prediction with full details"""
    try:
        startup_data = data.model_dump()
        result = orchestrator.predict(startup_data)
        
        # Return complete result
        return {
            'final_probability': result.final_probability,
            'confidence_score': result.confidence_score,
            'verdict': result.verdict,
            'risk_level': result.risk_level,
            'base_probability': result.base_probability,
            'pattern_probability': result.pattern_probability,
            'stage_probability': result.stage_probability,
            'industry_probability': result.industry_probability,
            'camp_scores': result.camp_scores,
            'base_predictions': result.base_predictions,
            'pattern_predictions': result.pattern_predictions,
            'stage_prediction': result.stage_prediction,
            'industry_prediction': result.industry_prediction,
            'camp_predictions': result.camp_predictions,
            'dominant_patterns': result.dominant_patterns,
            'stage_fit': result.stage_fit,
            'industry_fit': result.industry_fit,
            'camp_strengths': result.camp_strengths,
            'camp_weaknesses': result.camp_weaknesses,
            'recommendations': result.recommendations,
            'model_weights': result.model_weights,
            'models_used': result.models_used,
            'prediction_variance': result.prediction_variance
        }
        
    except Exception as e:
        logger.error(f"Detailed prediction error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/model_info")
async def model_info():
    """Get information about loaded models"""
    model_info = {}
    
    for category, models in orchestrator.models.items():
        model_info[category] = {
            'count': len(models),
            'models': list(models.keys())
        }
    
    return {
        'model_categories': model_info,
        'weights': orchestrator.weights,
        'total_models': sum(len(m) for m in orchestrator.models.values())
    }

@app.get("/system_performance")
async def system_performance():
    """Get expected performance metrics"""
    return {
        'base_models': {
            'expected_auc': 0.77,
            'description': 'Contractual architecture foundation'
        },
        'pattern_models': {
            'expected_auc': 0.81,
            'description': 'Pattern-specific predictions'
        },
        'stage_models': {
            'expected_auc': 0.79,
            'description': 'Funding stage optimization'
        },
        'industry_models': {
            'expected_auc': 0.77,
            'description': 'Industry-specific insights'
        },
        'camp_models': {
            'expected_auc': 0.77,
            'description': 'CAMP framework refinement'
        },
        'complete_hybrid': {
            'expected_auc': 0.82,
            'description': 'All models combined',
            'improvement': '+5% over base models'
        }
    }

@app.get("/health")
async def health():
    """Health check endpoint"""
    model_status = {}
    for category, models in orchestrator.models.items():
        model_status[category] = len(models) > 0
    
    return {
        'status': 'healthy' if all(model_status.values()) else 'degraded',
        'timestamp': datetime.now().isoformat(),
        'models_loaded': orchestrator.loaded,
        'model_status': model_status
    }

if __name__ == "__main__":
    logger.info("Starting Complete Hybrid API Server on port 8001...")
    uvicorn.run(app, host="0.0.0.0", port=8001)