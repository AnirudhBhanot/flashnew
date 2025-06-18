#!/usr/bin/env python3
"""
Fixed API Server - Complete rewrite without shortcuts
Uses the fixed orchestrator with proper model loading
"""

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, validator
from typing import Optional, Dict, Any, List
import logging
import numpy as np
from datetime import datetime

# Import fixed components
from models.unified_orchestrator_v3_fixed import create_orchestrator
from type_converter_fixed import TypeConverterFixed
from feature_config import ALL_FEATURES

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="FLASH API - Fixed Version",
    description="Fixed startup success prediction API without shortcuts",
    version="3.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components - NO GLOBAL CACHING
type_converter = TypeConverterFixed()


class StartupData(BaseModel):
    """Input model for startup data"""
    
    # Capital Features (7)
    total_capital_raised_usd: Optional[float] = Field(None, ge=0)
    cash_on_hand_usd: Optional[float] = Field(None, ge=0)
    monthly_burn_usd: Optional[float] = Field(None, ge=0)
    runway_months: Optional[float] = Field(None, ge=0)
    burn_multiple: Optional[float] = Field(None, ge=0)
    investor_tier_primary: Optional[str] = None
    has_debt: Optional[bool] = None
    
    # Advantage Features (8)
    patent_count: Optional[int] = Field(None, ge=0)
    network_effects_present: Optional[bool] = None
    has_data_moat: Optional[bool] = None
    regulatory_advantage_present: Optional[bool] = None
    tech_differentiation_score: Optional[int] = Field(None, ge=1, le=5)
    switching_cost_score: Optional[int] = Field(None, ge=1, le=5)
    brand_strength_score: Optional[int] = Field(None, ge=1, le=5)
    scalability_score: Optional[int] = Field(None, ge=1, le=5)
    
    # Market Features (11)
    sector: Optional[str] = None
    tam_size_usd: Optional[float] = Field(None, ge=0)
    sam_size_usd: Optional[float] = Field(None, ge=0)
    som_size_usd: Optional[float] = Field(None, ge=0)
    market_growth_rate_percent: Optional[float] = None
    customer_count: Optional[int] = Field(None, ge=0)
    customer_concentration_percent: Optional[float] = Field(None, ge=0, le=100)
    user_growth_rate_percent: Optional[float] = None
    net_dollar_retention_percent: Optional[float] = None
    competition_intensity: Optional[int] = Field(None, ge=1, le=5)
    competitors_named_count: Optional[int] = Field(None, ge=0)
    
    # People Features (10)
    founders_count: Optional[int] = Field(None, ge=0)
    team_size_full_time: Optional[int] = Field(None, ge=0)
    years_experience_avg: Optional[float] = Field(None, ge=0)
    domain_expertise_years_avg: Optional[float] = Field(None, ge=0)
    prior_startup_experience_count: Optional[int] = Field(None, ge=0)
    prior_successful_exits_count: Optional[int] = Field(None, ge=0)
    board_advisor_experience_score: Optional[int] = Field(None, ge=1, le=5)
    advisors_count: Optional[int] = Field(None, ge=0)
    team_diversity_percent: Optional[float] = Field(None, ge=0, le=100)
    key_person_dependency: Optional[bool] = None
    
    # Product Features (9)
    product_stage: Optional[str] = None
    product_retention_30d: Optional[float] = Field(None, ge=0, le=100)
    product_retention_90d: Optional[float] = Field(None, ge=0, le=100)
    dau_mau_ratio: Optional[float] = Field(None, ge=0, le=1)
    annual_revenue_run_rate: Optional[float] = Field(None, ge=0)
    revenue_growth_rate_percent: Optional[float] = None
    gross_margin_percent: Optional[float] = None
    ltv_cac_ratio: Optional[float] = Field(None, ge=0)
    funding_stage: Optional[str] = None
    
    # Additional fields frontend might send
    proprietary_tech: Optional[bool] = None
    switching_costs_high: Optional[bool] = None
    gross_margin_improvement_percent: Optional[float] = None
    technical_moat_score: Optional[int] = None
    time_to_revenue_months: Optional[float] = None
    market_maturity_score: Optional[int] = None
    customer_acquisition_cost_usd: Optional[float] = None
    average_contract_value_usd: Optional[float] = None
    payback_period_months: Optional[float] = None
    market_timing_score: Optional[int] = None
    regulatory_risk_score: Optional[int] = None
    technical_team_percent: Optional[float] = None
    founders_experience_score: Optional[int] = None
    advisors_score: Optional[int] = None
    board_strength_score: Optional[int] = None
    team_domain_expertise_score: Optional[int] = None
    previous_startup_experience: Optional[int] = None
    team_completeness_score: Optional[int] = None
    culture_fit_score: Optional[int] = None
    diversity_score: Optional[int] = None
    active_users: Optional[int] = None
    mrr_usd: Optional[float] = None
    feature_completeness_score: Optional[int] = None
    user_satisfaction_score: Optional[int] = None
    product_market_fit_score: Optional[int] = None
    innovation_score: Optional[int] = None
    time_to_market_score: Optional[int] = None
    iteration_speed_score: Optional[int] = None
    
    @validator('*', pre=True)
    def empty_str_to_none(cls, v):
        """Convert empty strings to None"""
        if v == '':
            return None
        return v
    
    class Config:
        # Use Pydantic v2 style
        validate_assignment = True
        use_enum_values = True


class PredictionResponse(BaseModel):
    """Response model for predictions"""
    success_probability: float
    confidence_score: float
    confidence_interval: Dict[str, float]
    verdict: str
    pillar_scores: Dict[str, float]
    risk_level: str
    risk_factors: List[str]
    key_insights: List[str]
    critical_failures: List[str]
    below_threshold: List[str]
    model_predictions: Optional[Dict[str, float]] = None
    model_agreement: Optional[float] = None
    funding_stage: Optional[str] = None


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "FLASH API Fixed Version",
        "version": "3.0.0",
        "status": "operational",
        "endpoints": [
            "/predict",
            "/predict_enhanced",
            "/health",
            "/config/stage-weights",
            "/config/company-examples"
        ]
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "3.0.0"
    }


@app.post("/predict", response_model=PredictionResponse)
@app.post("/predict_simple", response_model=PredictionResponse)
@app.post("/predict_enhanced", response_model=PredictionResponse)
async def predict(data: StartupData):
    """Main prediction endpoint - all variants use same logic"""
    try:
        # Create fresh orchestrator instance - NO CACHING
        orchestrator = create_orchestrator()
        logger.info("Created fresh orchestrator instance")
        
        # Convert to dict and process
        features = data.model_dump()
        
        # Use type converter to handle frontend format
        canonical_features = type_converter.convert_frontend_to_backend(features)
        logger.info(f"Converted {len(features)} fields to {len(canonical_features)} canonical features")
        
        # Get prediction from orchestrator
        result = orchestrator.predict(canonical_features)
        
        # Add additional fields for frontend
        result['funding_stage'] = canonical_features.get('funding_stage', 'seed')
        
        # Calculate confidence interval
        prob = result['success_probability']
        confidence = result.get('confidence_score', 0.7)
        interval_width = (1 - confidence) * 0.2
        
        result['confidence_interval'] = {
            'lower': max(0, prob - interval_width),
            'upper': min(1, prob + interval_width)
        }
        
        # Ensure risk_factors is a list
        if 'risk_factors' not in result:
            result['risk_factors'] = result.get('critical_failures', [])
        
        logger.info(f"Prediction complete: {result['verdict']} ({result['success_probability']:.1%})")
        
        return PredictionResponse(**result)
        
    except Exception as e:
        logger.error(f"Prediction error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/config/stage-weights")
async def get_stage_weights():
    """Get stage-specific weightings"""
    return {
        "pre_seed": {
            "capital": 0.10,
            "advantage": 0.30,
            "market": 0.20,
            "people": 0.40
        },
        "seed": {
            "capital": 0.15,
            "advantage": 0.30,
            "market": 0.25,
            "people": 0.30
        },
        "series_a": {
            "capital": 0.25,
            "advantage": 0.25,
            "market": 0.30,
            "people": 0.20
        },
        "series_b": {
            "capital": 0.30,
            "advantage": 0.20,
            "market": 0.35,
            "people": 0.15
        },
        "series_c": {
            "capital": 0.40,
            "advantage": 0.20,
            "market": 0.30,
            "people": 0.10
        },
        "growth": {
            "capital": 0.45,
            "advantage": 0.15,
            "market": 0.30,
            "people": 0.10
        }
    }


@app.get("/config/company-examples")
async def get_company_examples():
    """Get example companies for each stage"""
    return {
        "pre_seed": {
            "company": "Airbnb (2008)",
            "story": "Two founders renting air mattresses during a conference"
        },
        "seed": {
            "company": "Uber (2009)",
            "story": "Simple app connecting riders with drivers in San Francisco"
        },
        "series_a": {
            "company": "Slack (2014)",
            "story": "Workplace communication tool growing from internal tool to product"
        },
        "series_b": {
            "company": "Stripe (2012)",
            "story": "Payment infrastructure achieving product-market fit"
        },
        "series_c": {
            "company": "Canva (2017)",
            "story": "Design platform scaling globally with strong unit economics"
        },
        "growth": {
            "company": "SpaceX (2015)",
            "story": "Proven business model revolutionizing space industry"
        }
    }


@app.get("/validate")
async def validate_features():
    """Validate that all required features are present"""
    return {
        "required_features": ALL_FEATURES,
        "total_count": len(ALL_FEATURES),
        "categories": {
            "capital": 7,
            "advantage": 8,
            "market": 11,
            "people": 10,
            "product": 9
        }
    }


if __name__ == "__main__":
    logger.info("Starting FLASH Fixed API Server...")
    logger.info("This server creates fresh orchestrator instances for each request")
    logger.info("No caching or shortcuts - pure predictions")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8001,
        log_level="info",
        reload=False  # Disable reload to ensure clean state
    )