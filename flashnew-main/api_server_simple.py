#!/usr/bin/env python3
"""
Simplified API server for testing - no auth
"""

import os
import sys
import logging
from pathlib import Path
from typing import Dict, Optional

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

sys.path.insert(0, str(Path(__file__).parent))

from models.unified_orchestrator_v3_integrated import UnifiedOrchestratorV3
from type_converter_simple import TypeConverter
from feature_config import ALL_FEATURES

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize
app = FastAPI(title="FLASH API (Simple)", version="1.0.0")
orchestrator = UnifiedOrchestratorV3()
type_converter = TypeConverter()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class StartupData(BaseModel):
    """Simplified startup data model"""
    # Just include a few key fields, rest are optional
    total_capital_raised_usd: Optional[float] = None
    cash_on_hand_usd: Optional[float] = None
    monthly_burn_usd: Optional[float] = None
    sector: Optional[str] = None
    team_size_full_time: Optional[int] = None
    product_stage: Optional[str] = None
    funding_stage: Optional[str] = None
    
    class Config:
        extra = "allow"  # Allow any extra fields

@app.get("/health")
async def health():
    return {"status": "healthy", "models_loaded": len(orchestrator.models)}

@app.post("/predict")
async def predict(data: StartupData):
    """Simple prediction endpoint"""
    try:
        # Convert to dict and process
        data_dict = data.dict()
        
        # Convert frontend format to backend
        features = type_converter.convert_frontend_to_backend(data_dict)
        
        # Get only canonical features
        canonical_features = {k: features.get(k, 0) for k in ALL_FEATURES}
        
        # Get prediction
        result = orchestrator.predict(canonical_features)
        
        # Format response
        # Handle verdict - it might be a string or dict
        verdict = result.get("verdict", "UNKNOWN")
        if isinstance(verdict, dict):
            verdict = verdict.get("verdict", "UNKNOWN")
        
        return {
            "success": True,
            "success_probability": result.get("success_probability", 0.5),
            "verdict": verdict,
            "confidence_interval": {
                "lower": max(0, result.get("success_probability", 0.5) - 0.1),
                "upper": min(1, result.get("success_probability", 0.5) + 0.1)
            },
            "camp_scores": result.get("pillar_scores", {})
        }
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/validate")
async def validate(data: StartupData):
    """Validate input data"""
    data_dict = data.dict()
    non_null = sum(1 for v in data_dict.values() if v is not None)
    return {
        "valid": non_null >= 5,  # At least 5 fields
        "fields_received": non_null,
        "fields_expected": 45
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8002)
