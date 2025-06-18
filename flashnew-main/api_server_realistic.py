#!/usr/bin/env python3
"""
API Server using realistic models - honest predictions for startup success
"""

from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Any
from datetime import datetime
import os
import json
import logging
import time

# Import the unified orchestrator
from models.unified_orchestrator_v3_integrated import UnifiedOrchestratorV3

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create custom orchestrator config for realistic models
REALISTIC_CONFIG = {
    "models": {
        "paths": {
            "dna_analyzer": "models/production_v46_realistic/dna_analyzer.pkl",
            "temporal_model": "models/production_v46_realistic/temporal_model.pkl", 
            "industry_model": "models/production_v46_realistic/industry_model.pkl",
            "ensemble_model": "models/production_v46_realistic/ensemble_model.pkl"
        },
        "weights": {
            "camp_evaluation": 0.40,
            "pattern_analysis": 0.00,  # Pattern system disabled
            "industry_specific": 0.30,
            "temporal_prediction": 0.20,
            "ensemble": 0.10
        }
    },
    "realistic_mode": True,
    "calibration": {
        "enabled": False,  # Don't artificially boost predictions
        "disclaimer": "These predictions are based on realistic data. Early-stage success is inherently uncertain."
    }
}

# Save config file for orchestrator
with open('orchestrator_config_realistic.json', 'w') as f:
    json.dump(REALISTIC_CONFIG, f, indent=2)

# Initialize FastAPI app
app = FastAPI(
    title="FLASH API - Realistic Models",
    description="Honest startup success predictions based on realistic data",
    version="1.0.0"
)

# CORS configuration
origins = [
    "http://localhost:3000",
    "http://localhost:3001", 
    "http://127.0.0.1:3000",
    "http://127.0.0.1:3001",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=3600,
)

# Initialize orchestrator with realistic config
try:
    orchestrator = UnifiedOrchestratorV3(config_file='orchestrator_config_realistic.json')
    logger.info("Orchestrator loaded with realistic models")
except Exception as e:
    logger.error(f"Failed to initialize orchestrator: {e}")
    orchestrator = None

# Import type converter
try:
    from type_converter_simple import TypeConverter
    type_converter = TypeConverter()
except ImportError:
    logger.warning("TypeConverter not found, using direct conversion")
    type_converter = None

# Pydantic models
class StartupData(BaseModel):
    # Capital metrics
    total_capital_raised_usd: float = Field(..., ge=0)
    cash_on_hand_usd: float = Field(..., ge=0)
    monthly_burn_usd: float = Field(..., ge=0)
    runway_months: float = Field(..., ge=0)
    burn_multiple: float = Field(..., ge=0)
    
    # Market metrics
    tam_size_usd: float = Field(..., ge=0)
    sam_size_usd: float = Field(..., ge=0)
    som_size_usd: float = Field(..., ge=0)
    market_growth_rate_percent: float = Field(..., ge=0)
    
    # Team metrics
    founders_count: int = Field(..., ge=1)
    team_size_full_time: int = Field(..., ge=0)
    years_experience_avg: float = Field(..., ge=0)
    
    # Product metrics
    customer_count: int = Field(..., ge=0)
    annual_revenue_run_rate: float = Field(..., ge=0)
    gross_margin_percent: float = Field(..., ge=0, le=100)
    
    # Additional fields...
    funding_stage: str
    sector: str
    product_stage: str
    
    # All other fields as optional
    class Config:
        extra = "allow"

class PredictionResponse(BaseModel):
    success_probability: float
    confidence_score: float
    confidence_interval: Dict[str, float]
    verdict: str
    verdict_strength: str
    risk_level: str
    camp_analysis: Dict[str, float]
    risk_factors: List[str]
    success_factors: List[str]
    processing_time_ms: float
    timestamp: str
    model_version: str = "realistic-v1"
    disclaimer: str = "Based on realistic data. Early-stage predictions are inherently uncertain."
    
    # Frontend compatibility
    pillar_scores: Dict[str, float]
    investment_recommendation: str
    camp_scores: Dict[str, float]

# Authentication
API_KEYS = {
    "test-api-key-123": "Development",
    "demo-api-key-456": "Demo"
}

def verify_api_key(x_api_key: Optional[str] = Header(None)):
    """Verify API key from header"""
    if not x_api_key or x_api_key not in API_KEYS:
        raise HTTPException(status_code=401, detail="Invalid or missing API key")
    return API_KEYS[x_api_key]

# Helper Functions
def get_realistic_verdict(prob: float) -> tuple[str, str]:
    """Get verdict based on realistic probability thresholds"""
    if prob < 0.10:
        return "STRONG FAIL", "high"
    elif prob < 0.16:  # Below average (16% is dataset average)
        return "FAIL", "medium"
    elif prob < 0.20:
        return "CONDITIONAL FAIL", "low"
    elif prob < 0.25:
        return "CONDITIONAL PASS", "low"
    elif prob < 0.35:
        return "PASS", "medium"
    else:
        return "STRONG PASS", "high"

def transform_response_realistic(result: Dict) -> PredictionResponse:
    """Transform orchestrator response with realistic interpretation"""
    success_prob = result.get('success_probability', 0.16)  # Default to dataset average
    
    # Get realistic verdict
    verdict, strength = get_realistic_verdict(success_prob)
    
    # Risk level based on realistic thresholds
    if success_prob < 0.10:
        risk_level = "Very High Risk"
    elif success_prob < 0.16:
        risk_level = "High Risk"
    elif success_prob < 0.25:
        risk_level = "Medium-High Risk"
    elif success_prob < 0.35:
        risk_level = "Medium Risk"
    else:
        risk_level = "Lower Risk"
    
    # CAMP scores (likely all around 0.5 due to low model discrimination)
    camp_scores = result.get('pillar_scores', {
        'capital': 0.5,
        'advantage': 0.5,
        'market': 0.5,
        'people': 0.5
    })
    
    # Realistic confidence interval (wider due to uncertainty)
    confidence_interval = {
        'lower': max(0, success_prob - 0.15),
        'upper': min(1, success_prob + 0.15)
    }
    
    # Risk and success factors based on realistic insights
    risk_factors = []
    success_factors = []
    
    if success_prob < 0.16:
        risk_factors.append("Below average success probability for stage")
        risk_factors.append("Limited differentiation in quantitative metrics")
    
    if result.get('funding_stage') == 'pre_seed':
        risk_factors.append("Pre-seed stage has ~90% failure rate historically")
        if result.get('annual_revenue_run_rate', 0) == 0:
            risk_factors.append("No revenue traction yet")
    
    if success_prob > 0.20:
        success_factors.append("Above average indicators for stage")
    
    response = PredictionResponse(
        success_probability=success_prob,
        confidence_score=0.5,  # Low confidence due to model uncertainty
        confidence_interval=confidence_interval,
        verdict=verdict,
        verdict_strength=strength,
        risk_level=risk_level,
        camp_analysis=camp_scores,
        risk_factors=risk_factors,
        success_factors=success_factors,
        processing_time_ms=result.get('processing_time_ms', 100),
        timestamp=datetime.now().isoformat(),
        disclaimer="Predictions based on realistic data show early-stage success is highly uncertain (50% AUC).",
        # Compatibility
        pillar_scores=camp_scores,
        investment_recommendation=verdict,
        camp_scores=camp_scores
    )
    
    return response

# API Endpoints
@app.get("/")
def root():
    return {
        "message": "FLASH API - Realistic Models",
        "version": "1.0.0",
        "models": "production_v46_realistic",
        "disclaimer": "Using honest models trained on realistic data",
        "expected_auc": "~0.50 (realistic for early-stage prediction)"
    }

@app.get("/health")
def health():
    return {
        "status": "healthy",
        "models_loaded": orchestrator is not None,
        "model_version": "realistic-v46",
        "timestamp": datetime.now().isoformat()
    }

@app.post("/predict", response_model=PredictionResponse)
def predict(data: StartupData, api_key: str = Depends(verify_api_key)):
    """Make prediction using realistic models"""
    if not orchestrator:
        raise HTTPException(status_code=503, detail="Models not loaded")
    
    try:
        logger.info(f"Prediction request from {api_key}")
        
        # Convert to dict
        startup_dict = data.model_dump()
        
        # Use type converter if available
        if type_converter:
            startup_dict = type_converter.frontend_to_backend(startup_dict)
            logger.info(f"Converted {len(startup_dict)} fields to backend format")
        
        # Get prediction
        start_time = time.time()
        result = orchestrator.predict(startup_dict)
        processing_time = (time.time() - start_time) * 1000
        
        result['processing_time_ms'] = processing_time
        result['funding_stage'] = startup_dict.get('funding_stage')
        result['annual_revenue_run_rate'] = startup_dict.get('annual_revenue_run_rate', 0)
        
        # Log realistic prediction
        logger.info(f"Realistic prediction: {result.get('success_probability', 0):.1%}")
        
        # Transform response
        response = transform_response_realistic(result)
        return response
        
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/features")
def get_features(api_key: str = Depends(verify_api_key)):
    """Get list of features used by models"""
    try:
        with open('models/production_v46_realistic/model_metadata.json', 'r') as f:
            metadata = json.load(f)
        
        return {
            "total_features": metadata.get('n_features', 85),
            "key_features": [
                "market_growth_rate_percent",
                "team_diversity_percent", 
                "growth_potential",
                "experience_score",
                "years_experience_avg"
            ],
            "note": "Features have low predictive power due to realistic data",
            "model_auc": metadata.get('average_auc', 0.499)
        }
    except:
        return {"error": "Could not load feature information"}

# Config endpoints (for frontend compatibility)
@app.get("/config/{config_type}")
def get_config(config_type: str, api_key: str = Depends(verify_api_key)):
    """Get configuration with realistic thresholds"""
    
    configs = {
        "success-thresholds": {
            "pre_seed": 0.10,      # 10% reach Series A
            "seed": 0.22,          # 22% reach Series A  
            "series_a": 0.38,      # 38% reach Series B
            "series_b": 0.52,      # 52% reach Series C
            "note": "Based on realistic success rates"
        },
        "model-performance": {
            "average_auc": 0.499,
            "dna_analyzer": {"auc": 0.489, "tpr": 0.032},
            "temporal_model": {"auc": 0.504, "tpr": 0.339},
            "industry_model": {"auc": 0.504, "tpr": 0.339},
            "ensemble_model": {"auc": 0.499, "tpr": 0.032},
            "disclaimer": "Low AUC reflects true difficulty of early-stage prediction"
        },
        "stage-weights": {
            "pre_seed": {
                "capital": 0.20,
                "advantage": 0.15, 
                "market": 0.25,
                "people": 0.40
            },
            "seed": {
                "capital": 0.25,
                "advantage": 0.25,
                "market": 0.25, 
                "people": 0.25
            }
        }
    }
    
    if config_type == "all":
        return configs
    
    return configs.get(config_type, {})

if __name__ == "__main__":
    import uvicorn
    
    print("="*60)
    print("Starting FLASH API with REALISTIC MODELS")
    print("="*60)
    print("Models: production_v46_realistic")
    print("Expected AUC: ~0.50 (honest performance)")
    print("Success rate: 16% average")
    print("="*60)
    
    uvicorn.run(app, host="0.0.0.0", port=8001)