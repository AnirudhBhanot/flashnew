#!/usr/bin/env python3
"""
FLASH API Server - Final Fixed Version
Fixes the validation issue with predict endpoint
"""

import os
import sys
import logging
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, List, Any

import numpy as np
import uvicorn
from fastapi import FastAPI, HTTPException, Security, status, Request, Response, Depends, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import APIKeyHeader
from pydantic import BaseModel, Field, validator, ValidationError

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

# Import models and utilities
from models.unified_orchestrator_v3_integrated import UnifiedOrchestratorV3
from type_converter_simple import TypeConverter
from feature_config import ALL_FEATURES
from config import settings

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI
app = FastAPI(
    title="FLASH 2.0 API",
    description="AI-powered startup evaluation platform",
    version="2.0.0"
)

# Initialize components
orchestrator = UnifiedOrchestratorV3()
type_converter = TypeConverter()

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001", "*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type", "X-API-Key", "Authorization"],
    expose_headers=["X-Request-ID"],
    max_age=3600,
)

class StartupData(BaseModel):
    """Input model for startup data"""
    # Capital Features
    total_capital_raised_usd: Optional[float] = None
    cash_on_hand_usd: Optional[float] = None
    monthly_burn_usd: Optional[float] = None
    runway_months: Optional[float] = None
    burn_multiple: Optional[float] = None
    investor_tier_primary: Optional[str] = None
    has_debt: Optional[bool] = None
    
    # Advantage Features
    patent_count: Optional[int] = None
    network_effects_present: Optional[bool] = None
    has_data_moat: Optional[bool] = None
    regulatory_advantage_present: Optional[bool] = None
    tech_differentiation_score: Optional[int] = Field(None, ge=1, le=5)
    switching_cost_score: Optional[int] = Field(None, ge=1, le=5)
    brand_strength_score: Optional[int] = Field(None, ge=1, le=5)
    scalability_score: Optional[int] = Field(None, ge=1, le=5)
    
    # Market Features
    sector: Optional[str] = None
    tam_size_usd: Optional[float] = None
    sam_size_usd: Optional[float] = None
    som_size_usd: Optional[float] = None
    market_growth_rate_percent: Optional[float] = None
    customer_count: Optional[int] = None
    customer_concentration_percent: Optional[float] = Field(None, ge=0, le=100)
    user_growth_rate_percent: Optional[float] = None
    net_dollar_retention_percent: Optional[float] = None
    competition_intensity: Optional[int] = Field(None, ge=1, le=5)
    competitors_named_count: Optional[int] = None
    
    # People Features
    founders_count: Optional[int] = None
    team_size_full_time: Optional[int] = None
    years_experience_avg: Optional[float] = None
    domain_expertise_years_avg: Optional[float] = None
    prior_startup_experience_count: Optional[int] = None
    prior_successful_exits_count: Optional[int] = None
    board_advisor_experience_score: Optional[int] = Field(None, ge=1, le=5)
    advisors_count: Optional[int] = None
    team_diversity_percent: Optional[float] = Field(None, ge=0, le=100)
    key_person_dependency: Optional[bool] = None
    
    # Product Features
    product_stage: Optional[str] = None
    product_retention_30d: Optional[float] = Field(None, ge=0, le=1)
    product_retention_90d: Optional[float] = Field(None, ge=0, le=1)
    dau_mau_ratio: Optional[float] = Field(None, ge=0, le=1)
    annual_revenue_run_rate: Optional[float] = None
    revenue_growth_rate_percent: Optional[float] = None
    gross_margin_percent: Optional[float] = Field(None, ge=-100, le=100)
    ltv_cac_ratio: Optional[float] = None
    funding_stage: Optional[str] = None
    
    class Config:
        extra = "allow"  # Allow extra fields from frontend
    
    @validator('funding_stage', 'product_stage', 'sector', 'investor_tier_primary')
    def lowercase_string_fields(cls, v):
        """Ensure string fields are lowercase"""
        if v and isinstance(v, str):
            return v.lower().replace(' ', '_').replace('-', '_')
        return v


# Simple auth check for development
def check_auth():
    """Simple auth check - returns True in development mode"""
    if os.getenv("DISABLE_AUTH", "false").lower() == "true":
        return True
    return False


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "FLASH API Server",
        "version": "2.0.0",
        "endpoints": [
            "/predict",
            "/predict_simple",
            "/predict_enhanced",
            "/validate",
            "/health",
            "/investor_profiles"
        ]
    }


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "models_loaded": len(orchestrator.models),
        "patterns_available": hasattr(orchestrator, 'pattern_system') and orchestrator.pattern_system is not None,
        "timestamp": datetime.now().isoformat()
    }


@app.post("/predict")
async def predict(data: StartupData = Body(...)):
    """Standard prediction endpoint"""
    try:
        # Convert to dict
        data_dict = data.model_dump() if hasattr(data, 'model_dump') else data.dict()
        
        # Log request
        non_null_fields = sum(1 for v in data_dict.values() if v is not None)
        logger.info(f"Received prediction request with {non_null_fields} non-null fields")
        
        # Convert frontend format to backend
        features = type_converter.convert_frontend_to_backend(data_dict)
        
        # Get only canonical features
        canonical_features = {k: features.get(k, 0) for k in ALL_FEATURES}
        
        # Get prediction
        result = orchestrator.predict(canonical_features)
        
        # Format response
        verdict = result.get("verdict", "UNKNOWN")
        if isinstance(verdict, dict):
            verdict = verdict.get("verdict", "UNKNOWN")
        
        # Calculate CAMP scores if not provided
        camp_scores = result.get("pillar_scores", {})
        if not camp_scores:
            # Simple CAMP score calculation
            from feature_config import CAPITAL_FEATURES, ADVANTAGE_FEATURES, MARKET_FEATURES, PEOPLE_FEATURES
            
            def calc_score(feature_list):
                values = []
                for f in feature_list:
                    val = canonical_features.get(f, 0)
                    if val is not None and not isinstance(val, str):
                        # Normalize numeric values to 0-1 range
                        try:
                            if f in ['total_capital_raised_usd', 'cash_on_hand_usd']:
                                # Log scale for large monetary values
                                val = min(1.0, np.log10(float(val) + 1) / 8)  # Up to $100M
                            elif f == 'monthly_burn_usd':
                                # Inverse - lower burn is better
                                val = max(0, 1.0 - (float(val) / 1000000))  # $1M/month = 0
                            elif f == 'runway_months':
                                val = min(1.0, float(val) / 24)  # 24 months = perfect
                            elif f == 'burn_multiple':
                                # Inverse - lower is better
                                val = max(0, 1.0 - (float(val) / 10))
                            elif f in ['tam_size_usd', 'sam_size_usd', 'som_size_usd']:
                                # Log scale for market sizes
                                val = min(1.0, np.log10(float(val) + 1) / 10)  # Up to $10B
                            elif f.endswith('_percent'):
                                val = min(1.0, max(0, float(val) / 100.0))
                            elif f.endswith('_score'):
                                val = min(1.0, max(0, float(val) / 5.0))
                            elif f in ['customer_count', 'team_size_full_time', 'founders_count', 'advisors_count']:
                                # Log scale for counts
                                val = min(1.0, np.log10(float(val) + 1) / 4)  # Up to 10,000
                            elif f in ['patent_count', 'competitors_named_count']:
                                val = min(1.0, float(val) / 20)  # 20+ = max
                            elif isinstance(val, bool):
                                val = 1.0 if val else 0.0
                            elif f == 'key_person_dependency':
                                # Inverse - lower is better
                                val = 0.0 if val else 1.0
                            else:
                                # Default normalization
                                val = min(1.0, max(0, float(val)))
                            
                            values.append(val)
                        except (ValueError, TypeError):
                            pass
                return sum(values) / len(values) if values else 0.5
            
            camp_scores = {
                "capital": calc_score(CAPITAL_FEATURES),
                "advantage": calc_score(ADVANTAGE_FEATURES),
                "market": calc_score(MARKET_FEATURES),
                "people": calc_score(PEOPLE_FEATURES)
            }
        
        success_prob = result.get("success_probability", 0.5)
        
        return {
            "success": True,
            "success_probability": success_prob,
            "verdict": verdict,
            "confidence_interval": {
                "lower": max(0, success_prob - 0.1),
                "upper": min(1, success_prob + 0.1)
            },
            "camp_scores": camp_scores,
            "model_consensus": result.get("model_consensus", 0.8),
            "risk_level": "high" if success_prob < 0.3 else "medium" if success_prob < 0.7 else "low"
        }
        
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        return {
            "success": False,
            "error": "Prediction Failed",
            "message": str(e)
        }


@app.post("/predict_simple")
async def predict_simple(data: StartupData = Body(...)):
    """Alias for /predict for frontend compatibility"""
    return await predict(data)


@app.post("/predict_enhanced")
async def predict_enhanced(data: StartupData = Body(...)):
    """Enhanced prediction with pattern analysis"""
    # For now, just call standard predict
    return await predict(data)


@app.post("/predict_advanced")
async def predict_advanced(data: StartupData = Body(...)):
    """Alias for predict_enhanced"""
    return await predict_enhanced(data)


@app.post("/validate")
async def validate(data: StartupData = Body(...)):
    """Validate input data"""
    data_dict = data.model_dump() if hasattr(data, 'model_dump') else data.dict()
    
    # Count non-null fields
    non_null = sum(1 for k, v in data_dict.items() if v is not None and k in ALL_FEATURES)
    missing = [f for f in ALL_FEATURES if f not in data_dict or data_dict.get(f) is None]
    
    return {
        "valid": non_null >= len(ALL_FEATURES) * 0.8,  # 80% of fields required
        "fields_received": non_null,
        "fields_expected": len(ALL_FEATURES),
        "missing_fields": missing[:10] if len(missing) > 10 else missing  # Limit to 10
    }


@app.get("/investor_profiles")
async def get_investor_profiles():
    """Get investor profile templates"""
    return [
        {
            "id": "techventures",
            "name": "TechVentures Capital",
            "focus": ["B2B SaaS", "AI/ML", "Enterprise"],
            "stage_preference": ["Series A", "Series B"],
            "check_size": "$5M - $25M",
            "priorities": {
                "market": 0.35,
                "advantage": 0.30,
                "people": 0.20,
                "capital": 0.15
            }
        },
        {
            "id": "innovation",
            "name": "Innovation Partners",
            "focus": ["Consumer Tech", "Marketplace", "FinTech"],
            "stage_preference": ["Seed", "Series A"],
            "check_size": "$1M - $10M",
            "priorities": {
                "people": 0.35,
                "market": 0.30,
                "advantage": 0.20,
                "capital": 0.15
            }
        },
        {
            "id": "growth",
            "name": "Growth Equity Fund",
            "focus": ["SaaS", "E-commerce", "HealthTech"],
            "stage_preference": ["Series B", "Series C"],
            "check_size": "$20M - $100M",
            "priorities": {
                "capital": 0.35,
                "market": 0.30,
                "advantage": 0.20,
                "people": 0.15
            }
        }
    ]


@app.post("/explain")
async def explain(data: StartupData = Body(...)):
    """Get explanation for prediction"""
    # Get prediction first
    prediction_result = await predict(data)
    
    # Generate explanation
    explanation = {
        "success_probability": prediction_result.get("success_probability", 0.5),
        "key_factors": [],
        "recommendations": []
    }
    
    # Add key factors based on CAMP scores
    camp_scores = prediction_result.get("camp_scores", {})
    for pillar, score in camp_scores.items():
        if score < 0.3:
            explanation["key_factors"].append(f"Weak {pillar} metrics")
            explanation["recommendations"].append(f"Strengthen {pillar} foundation")
        elif score > 0.7:
            explanation["key_factors"].append(f"Strong {pillar} position")
    
    return {"explanation": explanation}


if __name__ == "__main__":
    port = int(os.getenv("API_PORT", "8001"))
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=port,
        log_level="info"
    )