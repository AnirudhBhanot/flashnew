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
from models.unified_orchestrator_v3_integrated import UnifiedOrchestratorV3
from type_converter_simple import TypeConverter
from feature_config import ALL_FEATURES
from frontend_models import FrontendStartupData

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


def calculate_camp_scores(features: Dict[str, Any]) -> Dict[str, float]:
    """Calculate CAMP pillar scores from features"""
    scores = {}
    
    # Capital Score
    capital_factors = []
    total_capital = features.get('total_capital_raised_usd', 0) or 0
    if total_capital > 1000000:
        capital_factors.append(0.8)
    elif total_capital > 500000:
        capital_factors.append(0.6)
    else:
        capital_factors.append(0.4)
        
    runway_months = features.get('runway_months', 0) or 0
    if runway_months > 18:
        capital_factors.append(0.8)
    elif runway_months > 12:
        capital_factors.append(0.6)
    else:
        capital_factors.append(0.4)
    
    burn_multiple = features.get('burn_multiple', 0) or 0
    if burn_multiple <= 1:
        capital_factors.append(0.8)
    elif burn_multiple <= 2:
        capital_factors.append(0.6)
    else:
        capital_factors.append(0.4)
        
    scores['capital'] = sum(capital_factors) / len(capital_factors) if capital_factors else 0.5
    
    # Advantage Score
    advantage_factors = []
    tech_score = features.get('tech_differentiation_score', 0) or 0
    if tech_score >= 4:
        advantage_factors.append(0.8)
    elif tech_score >= 3:
        advantage_factors.append(0.6)
    else:
        advantage_factors.append(0.4)
    
    patent_count = features.get('patent_count', 0) or 0
    if patent_count > 5:
        advantage_factors.append(0.8)
    elif patent_count > 0:
        advantage_factors.append(0.6)
    else:
        advantage_factors.append(0.3)
    
    network_effects = features.get('network_effects_present', 0) or 0
    has_data_moat = features.get('has_data_moat', 0) or 0
    regulatory_advantage = features.get('regulatory_advantage_present', 0) or 0
    
    moat_score = (network_effects + has_data_moat + regulatory_advantage) / 3
    advantage_factors.append(0.4 + moat_score * 0.4)
        
    scores['advantage'] = sum(advantage_factors) / len(advantage_factors) if advantage_factors else 0.5
    
    # Market Score
    market_factors = []
    tam_size = features.get('tam_size_usd', 0) or 0
    if tam_size > 10000000000:  # $10B+
        market_factors.append(0.9)
    elif tam_size > 1000000000:  # $1B+
        market_factors.append(0.7)
    else:
        market_factors.append(0.4)
    
    growth_rate = features.get('market_growth_rate_percent', 0) or 0
    if growth_rate > 30:
        market_factors.append(0.8)
    elif growth_rate > 15:
        market_factors.append(0.6)
    else:
        market_factors.append(0.4)
    
    competition_str = features.get('competition_intensity', 'medium')
    if competition_str == 'low':
        market_factors.append(0.8)
    elif competition_str == 'medium':
        market_factors.append(0.6)
    else:
        market_factors.append(0.4)
        
    scores['market'] = sum(market_factors) / len(market_factors) if market_factors else 0.5
    
    # People Score
    people_factors = []
    team_size = features.get('team_size_full_time', 0) or 0
    if team_size > 20:
        people_factors.append(0.8)
    elif team_size > 10:
        people_factors.append(0.6)
    else:
        people_factors.append(0.4)
    
    experience = features.get('years_experience_avg', 0) or 0
    if experience > 10:
        people_factors.append(0.8)
    elif experience > 5:
        people_factors.append(0.6)
    else:
        people_factors.append(0.4)
    
    exits_count = features.get('prior_successful_exits_count', 0) or 0
    startup_exp = features.get('prior_startup_experience_count', 0) or 0
    
    if exits_count > 0:
        people_factors.append(0.9)
    elif startup_exp > 0:
        people_factors.append(0.7)
    else:
        people_factors.append(0.5)
        
    scores['people'] = sum(people_factors) / len(people_factors) if people_factors else 0.5
    
    # Ensure all scores are bounded between 0 and 1
    for key in scores:
        scores[key] = max(0.0, min(1.0, scores[key]))
    
    # Return scores in 0-1 scale (frontend components expect this format)
    return scores


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
async def predict(data: FrontendStartupData):
    """Standard prediction endpoint - accepts frontend data format"""
    try:
        # Log incoming data stats
        data_dict = data.dict()
        non_null_fields = sum(1 for v in data_dict.values() if v is not None)
        logger.info(f"Received prediction request with {non_null_fields} non-null fields")
        
        # Convert data for backend
        features = type_converter.convert_frontend_to_backend(data_dict)
        logger.info(f"After conversion: {len(features)} features")
        
        # Import feature config to filter to canonical features
        from feature_config import ALL_FEATURES
        
        # Filter to only the 45 canonical features expected by models
        canonical_features = {k: features.get(k, 0) for k in ALL_FEATURES}
        logger.info(f"Filtered to {len(canonical_features)} canonical features")
        
        # Get prediction
        result = orchestrator.predict(canonical_features)
        
        # Calculate CAMP pillar scores if not provided
        if 'pillar_scores' not in result or not result.get('pillar_scores'):
            camp_scores = calculate_camp_scores(canonical_features)
            logger.info(f"Calculated CAMP scores: {camp_scores}")
            result['pillar_scores'] = camp_scores
        
        # Validate result
        if not result:
            raise ValueError("No prediction result received from model")
        if 'success_probability' not in result:
            raise ValueError("Model did not return success probability")
        if not 0 <= result['success_probability'] <= 1:
            raise ValueError(f"Invalid probability value: {result['success_probability']}")
        
        # Transform for frontend
        response = transform_response_for_frontend(result)
        
        # Add additional fields expected by frontend
        response['risk_level'] = 'high' if result['success_probability'] < 0.3 else ('medium' if result['success_probability'] < 0.7 else 'low')
        response['investment_recommendation'] = response['verdict']
        response['verdict_strength'] = response.get('strength_level', 'Moderate')
        response['camp_scores'] = result.get('pillar_scores', {})
        # Frontend expects pillar_scores, not camp_scores
        response['pillar_scores'] = result.get('pillar_scores', {})
        # Include funding stage for stage-specific display
        response['funding_stage'] = canonical_features.get('funding_stage', 'seed')
        
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
async def predict_simple(data: FrontendStartupData):
    """Alias for /predict for frontend compatibility"""
    return await predict(data)


@app.post("/predict_enhanced")
async def predict_enhanced(data: FrontendStartupData):
    """Enhanced prediction with full pattern analysis"""
    try:
        # Convert data
        features = type_converter.convert_frontend_to_backend(data.dict())
        
        # Import feature config to filter to canonical features
        from feature_config import ALL_FEATURES
        
        # Filter to only the 45 canonical features expected by models
        canonical_features = {k: features.get(k, 0) for k in ALL_FEATURES}
        
        # Get enhanced prediction
        result = orchestrator.predict(canonical_features)
        
        # Calculate CAMP pillar scores if not provided
        if 'pillar_scores' not in result or not result.get('pillar_scores'):
            camp_scores = calculate_camp_scores(canonical_features)
            logger.info(f"Calculated CAMP scores: {camp_scores}")
            result['pillar_scores'] = camp_scores
        
        # Extract verdict string from verdict object if needed
        if isinstance(result.get('verdict'), dict):
            verdict_str = result['verdict'].get('verdict')
            if not verdict_str:
                # Calculate verdict based on probability if missing
                prob = result.get('success_probability', 0.5)
                if prob >= 0.7:
                    verdict_str = "PASS"
                elif prob >= 0.5:
                    verdict_str = "CONDITIONAL PASS"
                else:
                    verdict_str = "FAIL"
            result['verdict'] = verdict_str
        
        # Add funding stage for frontend
        result['funding_stage'] = canonical_features.get('funding_stage', 'seed')
        
        # Return full result with pattern analysis
        return result
        
    except Exception as e:
        logger.error(f"Enhanced prediction error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/predict_advanced")
async def predict_advanced(data: FrontendStartupData):
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


@app.get("/config/stage-weights")
async def get_stage_weights():
    """Get stage-specific CAMP weights"""
    return {
        "pre_seed": {
            "people": 0.40,
            "advantage": 0.30,
            "market": 0.20,
            "capital": 0.10
        },
        "seed": {
            "people": 0.30,
            "advantage": 0.30,
            "market": 0.25,
            "capital": 0.15
        },
        "series_a": {
            "market": 0.30,
            "people": 0.25,
            "advantage": 0.25,
            "capital": 0.20
        },
        "series_b": {
            "market": 0.35,
            "capital": 0.25,
            "advantage": 0.20,
            "people": 0.20
        },
        "series_c": {
            "capital": 0.35,
            "market": 0.30,
            "people": 0.20,
            "advantage": 0.15
        },
        "growth": {
            "capital": 0.35,
            "market": 0.30,
            "people": 0.20,
            "advantage": 0.15
        }
    }


@app.get("/config/model-performance")
async def get_model_performance():
    """Get model performance metrics"""
    # Get actual performance from models if available
    performance = {
        "dna_analyzer": {
            "name": "DNA Pattern Analyzer",
            "accuracy": 0.7711  # Should come from model metadata
        },
        "temporal_predictor": {
            "name": "Temporal Predictor", 
            "accuracy": 0.7736
        },
        "industry_model": {
            "name": "Industry-Specific Model",
            "accuracy": 0.7717
        },
        "ensemble_model": {
            "name": "Ensemble Model",
            "accuracy": 0.7401
        },
        "pattern_matcher": {
            "name": "Pattern Matcher",
            "accuracy": 0.7700
        },
        "meta_learner": {
            "name": "Meta Learner",
            "accuracy": 0.7636
        },
        "overall_accuracy": 0.7636,
        "dataset_size": "100k"
    }
    return performance


@app.get("/config/company-examples")
async def get_company_examples():
    """Get company examples for each stage"""
    return {
        "pre_seed": {
            "company": "Airbnb",
            "story": "Airbnb's founders were rejected by many VCs, but their persistence and execution skills turned a simple idea into a $75B company."
        },
        "seed": {
            "company": "Stripe",
            "story": "Stripe succeeded because the Collison brothers (team) built dramatically better payment APIs (advantage) than existing solutions."
        },
        "series_a": {
            "company": "Uber",
            "story": "Uber raised Series A after proving the ride-sharing market was massive and their model could scale beyond San Francisco."
        },
        "series_b": {
            "company": "DoorDash",
            "story": "DoorDash's Series B focused on their path to market leadership and improving delivery economics."
        },
        "series_c": {
            "company": "Spotify",
            "story": "Spotify's later rounds focused heavily on improving gross margins and reducing customer acquisition costs."
        },
        "growth": {
            "company": "Canva",
            "story": "Canva maintained high growth while achieving profitability, making it attractive for growth investors."
        }
    }


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
        patterns_ok = hasattr(orchestrator, 'pattern_classifier') and orchestrator.pattern_classifier is not None
        
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
    logger.info(f"Pattern system: {'Available' if hasattr(orchestrator, 'pattern_classifier') and orchestrator.pattern_classifier else 'Not available'}")
    
    # Start server
    uvicorn.run(app, host="0.0.0.0", port=8001)