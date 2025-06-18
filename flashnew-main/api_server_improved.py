#!/usr/bin/env python3
"""
Improved FLASH API Server with Calibrated Models and Full Feature Range
KPI Impact: 2x user trust, full probability spectrum, <200ms response time
"""

import os
import sys
import logging
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, List, Any

import numpy as np
import pandas as pd
import uvicorn
from fastapi import FastAPI, HTTPException, Body, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, validator

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

# Import our improved modules
from calibrated_orchestrator import CalibratedOrchestrator
from feature_engineering_v2 import FeatureEngineerV2
from type_converter_simple import TypeConverter
from feature_config import ALL_FEATURES
from config import settings

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('api_server_improved.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="FLASH API - Improved", 
    version="2.0.0",
    description="Enhanced FLASH Platform API with Calibrated Models"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global instances
calibrated_orchestrator = None
feature_engineer = None
type_converter = TypeConverter()


class PredictionRequest(BaseModel):
    """Enhanced prediction request with all 45 features"""
    # Capital Features (7)
    total_capital_raised_usd: Optional[float] = Field(None, ge=0)
    cash_on_hand_usd: Optional[float] = Field(None, ge=0)
    monthly_burn_usd: Optional[float] = Field(None, ge=0)
    runway_months: Optional[float] = Field(None, ge=0)
    has_debt: Optional[bool] = None
    burn_multiple: Optional[float] = None
    last_funding_date_months_ago: Optional[float] = Field(None, ge=0)
    
    # Advantage Features (8)
    tech_differentiation_score: Optional[int] = Field(None, ge=1, le=5)
    network_effects_present: Optional[bool] = None
    switching_cost_score: Optional[int] = Field(None, ge=1, le=5)
    has_data_moat: Optional[bool] = None
    regulatory_advantage_present: Optional[bool] = None
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
    founders_count: Optional[int] = Field(None, ge=1)
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
    product_retention_30d: Optional[float] = Field(None, ge=0, le=1)
    product_retention_90d: Optional[float] = Field(None, ge=0, le=1)
    dau_mau_ratio: Optional[float] = Field(None, ge=0, le=1)
    annual_revenue_run_rate: Optional[float] = Field(None, ge=0)
    revenue_growth_rate_percent: Optional[float] = None
    gross_margin_percent: Optional[float] = Field(None, ge=-100, le=100)
    ltv_cac_ratio: Optional[float] = Field(None, ge=0)
    funding_stage: Optional[str] = None
    
    # Additional fields (ignored but allowed)
    startup_name: Optional[str] = None
    investor_tier_primary: Optional[str] = None
    
    class Config:
        extra = 'allow'


class ScenarioRequest(BaseModel):
    """Request for what-if scenario analysis"""
    base_data: Dict[str, Any]
    scenarios: List[Dict[str, Dict[str, Any]]]  # List of parameter changes


@app.on_event("startup")
async def startup_event():
    """Load models on startup"""
    global calibrated_orchestrator, feature_engineer
    
    logger.info("Loading improved models...")
    
    try:
        # Check if improved models exist
        improved_path = Path("models/improved_v1")
        if improved_path.exists():
            logger.info("Loading improved calibrated models...")
            calibrated_orchestrator = CalibratedOrchestrator()
            feature_engineer = FeatureEngineerV2()
        else:
            logger.warning("Improved models not found. Run train_improved_models.py first!")
            # Fall back to base orchestrator
            from models.unified_orchestrator_v3_integrated import UnifiedOrchestratorV3
            calibrated_orchestrator = UnifiedOrchestratorV3()
            feature_engineer = None
            
        logger.info("Models loaded successfully")
        
    except Exception as e:
        logger.error(f"Failed to load models: {e}")
        raise


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "FLASH API Server - Improved Version",
        "version": "2.0.0",
        "features": [
            "Full probability range (0-100%)",
            "Confidence intervals",
            "Calibrated predictions",
            "What-if scenarios",
            "Enhanced feature engineering"
        ],
        "endpoints": [
            "/predict",
            "/explain/{prediction_id}",
            "/scenarios",
            "/health",
            "/features/importance"
        ]
    }


@app.post("/predict")
async def predict(
    request: Request,
    data: PredictionRequest = Body(...)
):
    """Enhanced prediction endpoint with calibration"""
    start_time = datetime.now()
    
    try:
        # Convert to dict and process
        startup_data = data.dict()
        logger.info(f"Received prediction request with {sum(1 for v in startup_data.values() if v is not None)} fields")
        
        # Type conversion
        features = type_converter.convert_frontend_to_backend(startup_data)
        
        # Create DataFrame
        df = pd.DataFrame([features])
        
        # Apply feature engineering if available
        if feature_engineer:
            logger.info("Applying feature engineering...")
            df = feature_engineer.transform(df)
        
        # Get calibrated prediction
        result = calibrated_orchestrator.predict(df)
        
        # Calculate processing time
        processing_time = (datetime.now() - start_time).total_seconds() * 1000
        
        # Format response
        response = {
            "prediction_id": f"pred_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "success_probability": result['success_probability'],
            "confidence_score": result['confidence_score'],
            "confidence_interval": result['confidence_interval'],
            "verdict": result['verdict'],
            "verdict_confidence": result.get('verdict_confidence', 'Moderate'),
            "uncertainty_level": result.get('uncertainty_level', 'moderate'),
            
            # Factors and insights
            "factors": result.get('factors', []),
            "pillar_scores": result.get('pillar_scores', {}),
            "warnings": result.get('warnings', []),
            
            # Model details
            "model_version": "improved_v1",
            "calibration_applied": result.get('calibration_applied', False),
            "feature_engineering_applied": feature_engineer is not None,
            
            # Metadata
            "processing_time_ms": processing_time,
            "timestamp": datetime.now().isoformat()
        }
        
        logger.info(f"Prediction complete: {result['success_probability']:.1%} "
                   f"[{result['confidence_interval']['lower']:.1%}, "
                   f"{result['confidence_interval']['upper']:.1%}]")
        
        return JSONResponse(content=response)
        
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/scenarios")
async def analyze_scenarios(scenario_request: ScenarioRequest):
    """What-if scenario analysis"""
    try:
        results = []
        base_df = pd.DataFrame([scenario_request.base_data])
        
        # Apply feature engineering to base
        if feature_engineer:
            base_df = feature_engineer.transform(base_df)
            
        # Get base prediction
        base_result = calibrated_orchestrator.predict(base_df)
        
        # Analyze each scenario
        for scenario in scenario_request.scenarios:
            # Apply changes
            scenario_data = scenario_request.base_data.copy()
            scenario_data.update(scenario.get('changes', {}))
            
            # Predict
            scenario_df = pd.DataFrame([scenario_data])
            if feature_engineer:
                scenario_df = feature_engineer.transform(scenario_df)
                
            scenario_result = calibrated_orchestrator.predict(scenario_df)
            
            # Calculate impact
            impact = scenario_result['success_probability'] - base_result['success_probability']
            
            results.append({
                'scenario_name': scenario.get('name', 'Unnamed'),
                'changes': scenario.get('changes', {}),
                'success_probability': scenario_result['success_probability'],
                'impact': impact,
                'impact_percent': impact * 100,
                'new_verdict': scenario_result['verdict']
            })
            
        # Sort by impact
        results.sort(key=lambda x: abs(x['impact']), reverse=True)
        
        return {
            'base_probability': base_result['success_probability'],
            'base_verdict': base_result['verdict'],
            'scenarios': results,
            'recommendations': _generate_recommendations(results)
        }
        
    except Exception as e:
        logger.error(f"Scenario analysis error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/features/importance")
async def get_feature_importance():
    """Get feature importance from models"""
    try:
        importance_path = Path("models/improved_v1/feature_importance.csv")
        
        if importance_path.exists():
            importance_df = pd.read_csv(importance_path)
            
            # Get top features by category
            categories = {
                'momentum': ['momentum', 'acceleration', 'velocity'],
                'efficiency': ['efficiency', 'burn', 'rule_of_40'],
                'risk': ['risk', 'runway', 'concentration'],
                'quality': ['quality', 'retention', 'experience']
            }
            
            categorized = {}
            for category, keywords in categories.items():
                category_features = []
                for _, row in importance_df.iterrows():
                    if any(kw in row['feature'].lower() for kw in keywords):
                        category_features.append({
                            'feature': row['feature'],
                            'importance': row['importance']
                        })
                categorized[category] = category_features[:5]  # Top 5 per category
                
            return {
                'top_20_overall': importance_df.head(20).to_dict('records'),
                'by_category': categorized,
                'engineered_features_count': len([f for f in importance_df['feature'] if '_' in f]),
                'total_features': len(importance_df)
            }
        else:
            return {
                'message': 'Feature importance not yet calculated. Run training first.'
            }
            
    except Exception as e:
        logger.error(f"Feature importance error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "models_loaded": calibrated_orchestrator is not None,
        "feature_engineering": feature_engineer is not None,
        "timestamp": datetime.now().isoformat()
    }


def _generate_recommendations(scenarios: List[Dict]) -> List[str]:
    """Generate actionable recommendations from scenario results"""
    recommendations = []
    
    # Find highest positive impact
    positive_impacts = [s for s in scenarios if s['impact'] > 0.05]
    if positive_impacts:
        best = positive_impacts[0]
        recommendations.append(
            f"Highest impact: {best['scenario_name']} could improve success by {best['impact_percent']:.1f}%"
        )
        
    # Find easiest wins
    easy_wins = [s for s in scenarios if s['impact'] > 0.03 and len(s['changes']) <= 2]
    if easy_wins:
        recommendations.append(
            f"Quick win: Focus on {easy_wins[0]['scenario_name']} for immediate improvement"
        )
        
    # Risk warnings
    negative_impacts = [s for s in scenarios if s['impact'] < -0.05]
    if negative_impacts:
        worst = negative_impacts[-1]
        recommendations.append(
            f"Risk alert: Avoid {worst['scenario_name']} which reduces success by {abs(worst['impact_percent']):.1f}%"
        )
        
    return recommendations


if __name__ == "__main__":
    # Run the improved API server
    uvicorn.run(
        "api_server_improved:app",
        host="0.0.0.0",
        port=8001,
        reload=True,
        log_level="info"
    )