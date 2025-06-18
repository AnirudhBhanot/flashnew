#!/usr/bin/env python3
"""
FLASH API Server - Consolidated Final Version
Integrates all fixes and improvements
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, validator
from typing import Optional, Dict, List, Any
import uvicorn
import logging
from datetime import datetime
import numpy as np
from pathlib import Path
import sys

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

# Import models and utilities
from models.unified_orchestrator_v3 import UnifiedOrchestratorV3
from type_converter_simple import TypeConverter
from feature_config import ALL_FEATURES

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('api_server.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(title="FLASH API", version="1.0.0")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
orchestrator = UnifiedOrchestratorV3()
type_converter = TypeConverter()


class StartupData(BaseModel):
    """Input model for startup data - matches 45 feature configuration"""
    
    # Capital Features (7)
    total_capital_raised_usd: Optional[float] = None
    cash_on_hand_usd: Optional[float] = None
    monthly_burn_usd: Optional[float] = None
    runway_months: Optional[float] = None
    burn_multiple: Optional[float] = None
    investor_tier_primary: Optional[str] = None
    has_debt: Optional[bool] = None
    
    # Advantage Features (8)
    patent_count: Optional[int] = None
    network_effects_present: Optional[bool] = None
    has_data_moat: Optional[bool] = None
    regulatory_advantage_present: Optional[bool] = None
    tech_differentiation_score: Optional[int] = Field(None, ge=1, le=5)
    switching_cost_score: Optional[int] = Field(None, ge=1, le=5)
    brand_strength_score: Optional[int] = Field(None, ge=1, le=5)
    scalability_score: Optional[int] = Field(None, ge=1, le=5)
    
    # Market Features (11)
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
    
    # People Features (10)
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
    
    # Product Features (9)
    product_stage: Optional[str] = None
    product_retention_30d: Optional[float] = Field(None, ge=0, le=1)
    product_retention_90d: Optional[float] = Field(None, ge=0, le=1)
    dau_mau_ratio: Optional[float] = Field(None, ge=0, le=1)
    annual_revenue_run_rate: Optional[float] = None
    revenue_growth_rate_percent: Optional[float] = None
    gross_margin_percent: Optional[float] = Field(None, ge=-100, le=100)
    ltv_cac_ratio: Optional[float] = None
    funding_stage: Optional[str] = None
    
    # Additional fields for calculations
    monthly_revenue: Optional[float] = None
    monthly_cogs: Optional[float] = None
    arpu: Optional[float] = None
    monthly_churn_rate: Optional[float] = None
    customer_acquisition_cost: Optional[float] = None
    
    # Frontend-specific fields (ignored)
    startup_name: Optional[str] = None
    hq_location: Optional[str] = None
    vertical: Optional[str] = None
    
    @validator('funding_stage', 'product_stage', 'sector', 'investor_tier_primary')
    def lowercase_string_fields(cls, v):
        """Ensure string fields are lowercase"""
        if v and isinstance(v, str):
            return v.lower().replace(' ', '_').replace('-', '_')
        return v
    
    @validator('*', pre=True)
    def empty_strings_to_none(cls, v):
        """Convert empty strings to None"""
        if v == '':
            return None
        return v
    
    class Config:
        """Pydantic config"""
        # Allow extra fields that aren't in the model
        extra = 'allow'
        # Validate on assignment
        validate_assignment = True


def transform_response_for_frontend(response: Dict) -> Dict:
    """Transform backend response to match frontend expectations"""
    
    # Calculate verdict
    prob = response['success_probability']
    confidence = response.get('confidence_score', 0.7)
    
    if prob >= 0.7:
        verdict = "PASS"
        strength_level = "Strong" if prob >= 0.8 else "Moderate"
    elif prob >= 0.5:
        verdict = "CONDITIONAL PASS"
        strength_level = "Moderate" if prob >= 0.6 else "Weak"
    else:
        verdict = "FAIL"
        strength_level = "Weak"
    
    # Transform the response
    transformed = {
        'success_probability': response['success_probability'],
        'confidence_interval': {
            'lower': max(0, response['success_probability'] - (1 - confidence) * 0.2),
            'upper': min(1, response['success_probability'] + (1 - confidence) * 0.2)
        },
        'verdict': verdict,
        'strength_level': strength_level,
        'pillar_scores': response.get('pillar_scores', {}),
        'risk_factors': response.get('interpretation', {}).get('risks', []),
        'success_factors': response.get('interpretation', {}).get('strengths', []),
        'processing_time_ms': response.get('processing_time_ms', 0),
        'timestamp': response.get('timestamp', datetime.now().isoformat()),
        'model_version': response.get('model_version', 'orchestrator_v3')
    }
    
    # Add pattern insights if available
    if 'pattern_analysis' in response and response['pattern_analysis']:
        transformed['pattern_insights'] = response['pattern_analysis'].get('pattern_insights', [])
        transformed['primary_patterns'] = response['pattern_analysis'].get('primary_patterns', [])
    
    return transformed


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "FLASH API Server",
        "version": "1.0.0",
        "endpoints": [
            "/predict",
            "/predict_enhanced",
            "/features",
            "/patterns",
            "/system_info",
            "/health"
        ]
    }


@app.post("/predict")
async def predict(data: StartupData):
    """Standard prediction endpoint"""
    try:
        # Log incoming data stats
        data_dict = data.dict()
        non_null_fields = sum(1 for v in data_dict.values() if v is not None)
        logger.info(f"Received prediction request with {non_null_fields} non-null fields")
        
        # Convert data for backend
        features = type_converter.convert_frontend_to_backend(data_dict)
        logger.info(f"After conversion: {len(features)} features")
        
        # Get prediction
        result = orchestrator.predict_enhanced(features)
        
        # Validate result
        if not result:
            raise ValueError("No prediction result received from model")
        if 'success_probability' not in result:
            raise ValueError("Model did not return success probability")
        if not 0 <= result['success_probability'] <= 1:
            raise ValueError(f"Invalid probability value: {result['success_probability']}")
        
        # Transform for frontend
        response = transform_response_for_frontend(result)
        
        # Log prediction summary
        logger.info(f"Prediction complete: {result['success_probability']:.1%} probability, "
                   f"verdict: {response['verdict']}")
        
        return response
        
    except ValueError as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(
            status_code=400, 
            detail={
                "error": "Validation Error",
                "message": str(e),
                "fields_received": non_null_fields
            }
        )
    except KeyError as e:
        logger.error(f"Missing required field: {str(e)}")
        raise HTTPException(
            status_code=400,
            detail={
                "error": "Missing Required Field", 
                "message": f"Required field not found: {str(e)}",
                "hint": "Ensure all 45 features are provided"
            }
        )
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail={
                "error": "Prediction Failed",
                "message": str(e),
                "type": type(e).__name__
            }
        )


@app.post("/predict_simple")
async def predict_simple(data: StartupData):
    """Alias for /predict for frontend compatibility"""
    return await predict(data)


@app.post("/predict_enhanced")
async def predict_enhanced(data: StartupData):
    """Enhanced prediction with full pattern analysis"""
    try:
        # Convert data
        features = type_converter.convert_frontend_to_backend(data.dict())
        
        # Get enhanced prediction
        result = orchestrator.predict_enhanced(features)
        
        # Return full result with pattern analysis
        return result
        
    except Exception as e:
        logger.error(f"Enhanced prediction error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/predict_advanced")
async def predict_advanced(data: StartupData):
    """Alias for /predict_enhanced"""
    return await predict_enhanced(data)


@app.post("/validate")
async def validate_data(data: StartupData):
    """Validate startup data without making prediction"""
    try:
        data_dict = data.dict()
        
        # Count fields
        total_expected = len(ALL_FEATURES)
        non_null_fields = sum(1 for k, v in data_dict.items() if v is not None and k in ALL_FEATURES)
        missing_fields = [f for f in ALL_FEATURES if f not in data_dict or data_dict.get(f) is None]
        
        # Check field types
        type_errors = []
        for field in ALL_FEATURES:
            if field in data_dict and data_dict[field] is not None:
                value = data_dict[field]
                if field in ['funding_stage', 'investor_tier_primary', 'product_stage', 'sector']:
                    if not isinstance(value, str):
                        type_errors.append(f"{field} should be string, got {type(value).__name__}")
                elif field in TypeConverter.BOOLEAN_FIELDS:
                    if not isinstance(value, (bool, int)):
                        type_errors.append(f"{field} should be boolean, got {type(value).__name__}")
                else:
                    try:
                        float(value)
                    except:
                        type_errors.append(f"{field} should be numeric, got {type(value).__name__}")
        
        is_valid = len(missing_fields) == 0 and len(type_errors) == 0
        
        return {
            "valid": is_valid,
            "fields_received": non_null_fields,
            "fields_expected": total_expected,
            "missing_fields": missing_fields,
            "type_errors": type_errors,
            "completeness": f"{non_null_fields}/{total_expected}",
            "message": "Data is valid and ready for prediction" if is_valid else "Data validation failed"
        }
        
    except Exception as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/features")
async def get_features():
    """Get feature documentation"""
    return {
        "total_features": len(ALL_FEATURES),
        "features": ALL_FEATURES,
        "categories": {
            "capital": 7,
            "advantage": 8,
            "market": 11,
            "people": 10,
            "product": 9
        }
    }


@app.get("/patterns")
async def get_patterns():
    """Get available patterns"""
    if orchestrator.pattern_classifier:
        patterns = orchestrator.pattern_classifier.get_all_patterns()
        return {
            "total_patterns": len(patterns),
            "patterns": patterns
        }
    else:
        return {"total_patterns": 0, "patterns": []}


@app.get("/patterns/{pattern_name}")
async def get_pattern_details(pattern_name: str):
    """Get details for a specific pattern"""
    if orchestrator.pattern_classifier:
        pattern = orchestrator.pattern_classifier.get_pattern(pattern_name)
        if pattern:
            return pattern
        else:
            raise HTTPException(status_code=404, detail=f"Pattern '{pattern_name}' not found")
    else:
        raise HTTPException(status_code=503, detail="Pattern system not available")


@app.post("/analyze_pattern")
async def analyze_pattern(data: StartupData):
    """Analyze patterns for a startup"""
    try:
        features = type_converter.convert_frontend_to_backend(data.dict())
        
        if orchestrator.pattern_classifier:
            result = orchestrator.pattern_classifier.predict(features)
            return result
        else:
            raise HTTPException(status_code=503, detail="Pattern system not available")
            
    except Exception as e:
        logger.error(f"Pattern analysis error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/investor_profiles")
async def get_investor_profiles():
    """Get sample investor profiles"""
    return [
        {
            "id": 1,
            "name": "TechVentures Capital",
            "type": "VC",
            "focus": ["B2B SaaS", "AI/ML", "Enterprise"],
            "stage": ["Series A", "Series B"],
            "typical_investment": "$5M - $20M",
            "portfolio_size": 45,
            "notable_investments": ["DataCo", "AIStartup", "CloudTech"]
        },
        {
            "id": 2,
            "name": "Innovation Partners",
            "type": "VC",
            "focus": ["Consumer Tech", "Marketplace", "FinTech"],
            "stage": ["Seed", "Series A"],
            "typical_investment": "$1M - $10M",
            "portfolio_size": 72,
            "notable_investments": ["PayApp", "MarketPlace", "FinanceAI"]
        },
        {
            "id": 3,
            "name": "Growth Equity Fund",
            "type": "PE",
            "focus": ["Late Stage", "Growth", "Scale-ups"],
            "stage": ["Series C+"],
            "typical_investment": "$20M+",
            "portfolio_size": 28,
            "notable_investments": ["ScaleUp", "GrowthCo", "MarketLeader"]
        }
    ]


@app.get("/system_info")
async def get_system_info():
    """Get system information"""
    return {
        "api_version": "1.0.0",
        "model_version": "orchestrator_v3_with_patterns",
        "feature_count": len(ALL_FEATURES),
        "pattern_count": 31 if orchestrator.pattern_classifier else 0,
        "models_loaded": list(orchestrator.models.keys()),
        "weights": orchestrator.weights,
        "status": "operational"
    }


@app.post("/explain")
async def explain_prediction(data: StartupData):
    """Generate explanations for a prediction"""
    try:
        # Get prediction first
        features = type_converter.convert_frontend_to_backend(data.dict())
        result = orchestrator.predict_enhanced(features)
        
        # Generate explanations
        explanations = {
            'feature_importance': {},
            'decision_factors': [],
            'improvement_suggestions': [],
            'confidence_breakdown': {}
        }
        
        # Feature importance based on CAMP scores
        if 'pillar_scores' in result:
            explanations['feature_importance'] = {
                'Capital': result['pillar_scores'].get('capital', 0.5),
                'Advantage': result['pillar_scores'].get('advantage', 0.5),
                'Market': result['pillar_scores'].get('market', 0.5),
                'People': result['pillar_scores'].get('people', 0.5)
            }
        
        # Decision factors
        if result['success_probability'] > 0.7:
            explanations['decision_factors'].append("Strong overall fundamentals across CAMP dimensions")
        if result.get('pillar_scores', {}).get('market', 0) > 0.7:
            explanations['decision_factors'].append("Excellent market opportunity and growth potential")
        if result.get('pillar_scores', {}).get('people', 0) > 0.7:
            explanations['decision_factors'].append("Experienced team with proven track record")
        
        # Risk factors
        if result.get('risk_factors'):
            explanations['decision_factors'].extend([f"Risk: {risk}" for risk in result['risk_factors']])
        
        # Success factors
        if result.get('success_factors'):
            explanations['decision_factors'].extend([f"Strength: {factor}" for factor in result['success_factors']])
        
        # Improvement suggestions
        if result.get('pillar_scores', {}).get('capital', 0) < 0.5:
            explanations['improvement_suggestions'].append("Improve capital efficiency and extend runway")
        if result.get('pillar_scores', {}).get('market', 0) < 0.5:
            explanations['improvement_suggestions'].append("Strengthen market positioning and growth metrics")
        if result.get('pillar_scores', {}).get('people', 0) < 0.5:
            explanations['improvement_suggestions'].append("Build stronger team with domain expertise")
        if result.get('pillar_scores', {}).get('advantage', 0) < 0.5:
            explanations['improvement_suggestions'].append("Develop stronger competitive moats and differentiation")
        
        # Confidence breakdown
        explanations['confidence_breakdown'] = {
            'model_agreement': result.get('model_agreement', 0),
            'pattern_confidence': result.get('pattern_analysis', {}).get('pattern_score', 0.5),
            'overall_confidence': result.get('confidence_score', 0.7)
        }
        
        return {
            'prediction': result,
            'explanations': explanations,
            'methodology': "CAMP framework analysis with pattern recognition",
            'timestamp': datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Explanation error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        # Check if models are loaded
        models_ok = len(orchestrator.models) > 0
        patterns_ok = orchestrator.pattern_classifier is not None
        
        if models_ok:
            return {
                "status": "healthy",
                "models_loaded": len(orchestrator.models),
                "patterns_available": patterns_ok,
                "timestamp": datetime.now().isoformat()
            }
        else:
            raise HTTPException(status_code=503, detail="Models not loaded")
            
    except Exception as e:
        raise HTTPException(status_code=503, detail=str(e))


if __name__ == "__main__":
    logger.info("Starting FLASH API Server...")
    logger.info(f"Loaded {len(orchestrator.models)} models")
    logger.info(f"Pattern system: {'Available' if orchestrator.pattern_classifier else 'Not available'}")
    
    # Start server
    uvicorn.run(app, host="0.0.0.0", port=8001)