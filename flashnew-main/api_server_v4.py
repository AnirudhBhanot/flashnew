#!/usr/bin/env python3
"""
FLASH API Server V4 - With Integrated CAMP Explainability
This version ensures CAMP scores explain rather than contradict ML predictions
"""

import os
import sys
import logging
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, List, Any

import numpy as np
import uvicorn
from fastapi import FastAPI, HTTPException, Request, Response, Depends, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, validator
from typing import Annotated

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

# Import the new orchestrator
from models.unified_orchestrator_v4 import create_orchestrator
from type_converter_simple import TypeConverter
from feature_config import ALL_FEATURES
from frontend_models import FrontendStartupData

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('api_server_v4.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="FLASH API V4",
    description="Fast Learning and Assessment of Startup Health with Integrated Explainability",
    version="4.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
type_converter = TypeConverter()
orchestrator = create_orchestrator()

# Request/Response Models
class StartupData(BaseModel):
    """Input model for startup data"""
    # Capital features
    total_capital_raised_usd: float = Field(..., ge=0)
    cash_on_hand_usd: float = Field(..., ge=0)
    monthly_burn_usd: float = Field(..., ge=0)
    runway_months: float = Field(..., ge=0)
    burn_multiple: float = Field(..., ge=0)
    
    # Advantage features
    investor_tier_primary: str
    has_debt: bool
    patent_count: int = Field(..., ge=0)
    network_effects_present: bool
    has_data_moat: bool
    regulatory_advantage_present: bool
    tech_differentiation_score: int = Field(..., ge=1, le=5)
    switching_cost_score: int = Field(..., ge=1, le=5)
    brand_strength_score: int = Field(..., ge=1, le=5)
    scalability_score: int = Field(..., ge=1, le=5)
    
    # Market features
    sector: str
    tam_size_usd: float = Field(..., ge=0)
    sam_size_usd: float = Field(..., ge=0)
    som_size_usd: float = Field(..., ge=0)
    market_growth_rate_percent: float
    customer_count: int = Field(..., ge=0)
    customer_concentration_percent: float = Field(..., ge=0, le=100)
    user_growth_rate_percent: float
    net_dollar_retention_percent: float = Field(..., ge=0)
    competition_intensity: int = Field(..., ge=1, le=5)
    competitors_named_count: int = Field(..., ge=0)
    
    # People features
    founders_count: int = Field(..., ge=1)
    team_size_full_time: int = Field(..., ge=1)
    years_experience_avg: float = Field(..., ge=0)
    domain_expertise_years_avg: float = Field(..., ge=0)
    prior_startup_experience_count: int = Field(..., ge=0)
    prior_successful_exits_count: int = Field(..., ge=0)
    board_advisor_experience_score: int = Field(..., ge=1, le=5)
    advisors_count: int = Field(..., ge=0)
    strategic_partners_count: int = Field(..., ge=0)
    has_repeat_founder: bool
    execution_risk_score: int = Field(..., ge=1, le=5)
    
    # Additional features
    vertical_integration_score: int = Field(..., ge=1, le=5)
    time_to_market_advantage_years: float
    partnership_leverage_score: int = Field(..., ge=1, le=5)
    company_age_months: float = Field(..., ge=0)
    cash_efficiency_score: float = Field(..., ge=0)
    operating_leverage_trend: float
    predictive_modeling_score: int = Field(..., ge=1, le=5)
    
    class Config:
        schema_extra = {
            "example": {
                "total_capital_raised_usd": 10000000,
                "cash_on_hand_usd": 6000000,
                "monthly_burn_usd": 400000,
                "runway_months": 15,
                "burn_multiple": 1.8,
                "investor_tier_primary": "Tier 1",
                "has_debt": False,
                "patent_count": 5,
                "network_effects_present": True,
                "has_data_moat": True,
                "regulatory_advantage_present": False,
                "tech_differentiation_score": 4,
                "switching_cost_score": 4,
                "brand_strength_score": 3,
                "scalability_score": 5,
                "sector": "SaaS",
                "tam_size_usd": 10000000000,
                "sam_size_usd": 1000000000,
                "som_size_usd": 100000000,
                "market_growth_rate_percent": 45,
                "customer_count": 500,
                "customer_concentration_percent": 15,
                "user_growth_rate_percent": 25,
                "net_dollar_retention_percent": 125,
                "competition_intensity": 3,
                "competitors_named_count": 15,
                "founders_count": 3,
                "team_size_full_time": 45,
                "years_experience_avg": 12,
                "domain_expertise_years_avg": 8,
                "prior_startup_experience_count": 4,
                "prior_successful_exits_count": 2,
                "board_advisor_experience_score": 4,
                "advisors_count": 6,
                "strategic_partners_count": 4,
                "has_repeat_founder": True,
                "execution_risk_score": 2,
                "vertical_integration_score": 3,
                "time_to_market_advantage_years": 1.5,
                "partnership_leverage_score": 4,
                "company_age_months": 24,
                "cash_efficiency_score": 1.2,
                "operating_leverage_trend": 1,
                "predictive_modeling_score": 3
            }
        }


class PredictionResponse(BaseModel):
    """Response model for predictions"""
    success_probability: float
    confidence_score: float
    verdict: str
    risk_level: str
    camp_analysis: Dict[str, float]
    critical_factors: List[Dict[str, Any]]
    alignment_explanation: str
    insights: List[str]
    model_predictions: Dict[str, float]
    model_agreement: float
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "FLASH API V4 - With Integrated CAMP Explainability",
        "version": "4.0.0",
        "endpoints": {
            "/predict": "Generate startup success prediction with aligned CAMP scores",
            "/health": "Check API health status",
            "/features": "Get list of required features"
        }
    }


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "models_loaded": list(orchestrator.models.keys()),
        "explainer_ready": orchestrator.camp_explainer is not None
    }


@app.get("/features")
async def get_features():
    """Get list of required features with descriptions"""
    return {
        "total_features": len(ALL_FEATURES),
        "features": ALL_FEATURES,
        "categories": {
            "capital": len([f for f in ALL_FEATURES if f in type_converter.feature_mappings and 
                           any(cat in f for cat in ['capital', 'cash', 'burn', 'runway'])]),
            "advantage": len([f for f in ALL_FEATURES if f in type_converter.feature_mappings and
                            any(cat in f for cat in ['patent', 'moat', 'differentiation'])]),
            "market": len([f for f in ALL_FEATURES if f in type_converter.feature_mappings and
                         any(cat in f for cat in ['market', 'customer', 'growth'])]),
            "people": len([f for f in ALL_FEATURES if f in type_converter.feature_mappings and
                         any(cat in f for cat in ['founder', 'team', 'experience'])])
        }
    }


@app.post("/predict", response_model=PredictionResponse)
async def predict(data: Annotated[StartupData, Body()]):
    """
    Generate prediction with integrated CAMP explainability
    CAMP scores now explain the ML prediction rather than contradicting it
    """
    try:
        # Convert input data
        startup_dict = data.dict()
        logger.info(f"Received prediction request for {data.sector} startup")
        
        # Convert to backend format
        features = type_converter.convert_frontend_to_backend(startup_dict)
        
        # Ensure all features present
        canonical_features = {k: features.get(k, 0) for k in ALL_FEATURES}
        
        # Get prediction with integrated explainability
        result = orchestrator.predict(canonical_features)
        
        # Log the alignment
        avg_camp = np.mean([
            result['camp_analysis']['capital'],
            result['camp_analysis']['advantage'],
            result['camp_analysis']['market'],
            result['camp_analysis']['people']
        ])
        
        logger.info(
            f"Prediction complete: {result['success_probability']:.1%} success, "
            f"CAMP avg: {avg_camp:.1%}, "
            f"Alignment: {abs(result['success_probability'] - avg_camp):.1%} difference"
        )
        
        # Create response
        response = PredictionResponse(
            success_probability=result['success_probability'],
            confidence_score=result['confidence_score'],
            verdict=result['verdict'],
            risk_level=result['risk_level'],
            camp_analysis=result['camp_analysis'],
            critical_factors=result['critical_factors'],
            alignment_explanation=result['alignment_explanation'],
            insights=result['insights'],
            model_predictions=result['model_predictions'],
            model_agreement=result['model_agreement']
        )
        
        return response
        
    except ValueError as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Prediction failed: {str(e)}"
        )


@app.post("/predict_batch")
async def predict_batch(data: List[StartupData]):
    """Batch prediction endpoint"""
    results = []
    for startup in data:
        try:
            prediction = await predict(startup)
            results.append(prediction)
        except Exception as e:
            results.append({
                "error": str(e),
                "startup": startup.dict()
            })
    return {"predictions": results}


if __name__ == "__main__":
    # Run the server
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8002,  # Different port to avoid conflicts
        log_level="info"
    )