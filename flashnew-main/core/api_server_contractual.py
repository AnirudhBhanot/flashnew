"""
Contract-Based API Server
Clean prediction service that uses contractual models with guaranteed feature alignment
"""

import logging
from typing import Dict, List, Optional, Any
from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, validator
import numpy as np
from datetime import datetime
import asyncio
from pathlib import Path

from .feature_registry import feature_registry
from .model_wrapper import ContractualModel

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="FLASH Contractual API",
    description="Startup evaluation API with contract-based models",
    version="2.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request/Response models
class StartupData(BaseModel):
    """Input data for startup evaluation"""
    # Capital features
    funding_stage: str = Field(..., description="Current funding stage")
    revenue_growth_rate: float = Field(0.0, description="Revenue growth rate %")
    total_capital_raised_usd: float = Field(0.0, description="Total capital raised")
    annual_recurring_revenue_millions: float = Field(0.0, description="ARR in millions")
    annual_revenue_run_rate: float = Field(0.0, description="Annual revenue run rate")
    burn_multiple: float = Field(2.0, description="Burn multiple")
    investor_tier_primary: str = Field("tier_2", description="Primary investor tier")
    active_investors: int = Field(1, description="Number of active investors")
    cash_on_hand_months: float = Field(12.0, description="Runway in months")
    runway_months: float = Field(12.0, description="Calculated runway")
    time_to_next_funding: int = Field(12, description="Months to next funding")
    
    # Market features
    market_tam_billions: float = Field(1.0, description="TAM in billions")
    market_growth_rate: float = Field(10.0, description="Market growth rate %")
    market_competitiveness: int = Field(3, ge=1, le=5, description="Competition level 1-5")
    customer_acquisition_cost: float = Field(100.0, description="CAC")
    customer_lifetime_value: float = Field(1000.0, description="CLV")
    customer_growth_rate: float = Field(0.0, description="Customer growth rate %")
    net_revenue_retention: float = Field(100.0, description="NRR %")
    average_deal_size: float = Field(1000.0, description="Average deal size")
    sales_cycle_days: int = Field(30, description="Sales cycle in days")
    international_revenue_percent: float = Field(0.0, description="International revenue %")
    target_enterprise: bool = Field(False, description="Targets enterprise")
    media_coverage: int = Field(3, ge=1, le=5, description="Media coverage 1-5")
    regulatory_risk: int = Field(3, ge=1, le=5, description="Regulatory risk 1-5")
    
    # Product/Advantage features
    product_market_fit_score: int = Field(3, ge=1, le=5, description="PMF score 1-5")
    technology_score: int = Field(3, ge=1, le=5, description="Tech score 1-5")
    scalability_score: int = Field(3, ge=1, le=5, description="Scalability 1-5")
    has_patent: bool = Field(False, description="Has patents")
    research_development_percent: float = Field(10.0, description="R&D % of revenue")
    uses_ai_ml: bool = Field(False, description="Uses AI/ML")
    cloud_native: bool = Field(True, description="Cloud native")
    mobile_first: bool = Field(False, description="Mobile first")
    platform_business: bool = Field(False, description="Platform business model")
    
    # People features
    team_size_full_time: int = Field(1, description="Full-time team size")
    founder_experience_years: int = Field(5, description="Founder experience years")
    repeat_founder: bool = Field(False, description="Repeat founder")
    technical_founder: bool = Field(True, description="Technical co-founder")
    employee_growth_rate: float = Field(0.0, description="Employee growth rate %")
    advisor_quality_score: int = Field(3, ge=1, le=5, description="Advisor quality 1-5")
    board_diversity_score: int = Field(3, ge=1, le=5, description="Board diversity 1-5")
    team_industry_experience: int = Field(5, description="Team industry experience years")
    key_person_dependency: int = Field(3, ge=1, le=5, description="Key person risk 1-5")
    top_university_alumni: bool = Field(False, description="Top university alumni")
    previous_exit: bool = Field(False, description="Previous exits")
    industry_connections: int = Field(3, ge=1, le=5, description="Industry connections 1-5")
    
    class Config:
        schema_extra = {
            "example": {
                "funding_stage": "seed",
                "revenue_growth_rate": 150.0,
                "team_size_full_time": 10,
                "market_tam_billions": 5.0,
                "product_market_fit_score": 4
            }
        }


class PredictionResponse(BaseModel):
    """Response from prediction endpoint"""
    success_probability: float = Field(..., ge=0, le=1)
    verdict: str = Field(..., description="PASS/FAIL/CONDITIONAL PASS")
    confidence_score: float = Field(..., ge=0, le=1)
    
    # Model predictions
    model_predictions: Dict[str, float] = Field(..., description="Individual model predictions")
    
    # CAMP scores
    pillar_scores: Dict[str, float] = Field(..., description="CAMP pillar scores")
    
    # Risk assessment
    risk_level: str = Field(..., description="HIGH/MEDIUM/LOW")
    risk_factors: List[str] = Field(default_factory=list)
    
    # Recommendations
    key_strengths: List[str] = Field(default_factory=list)
    improvement_areas: List[str] = Field(default_factory=list)
    
    # Metadata
    model_version: str = Field(..., description="Model version used")
    prediction_id: str = Field(..., description="Unique prediction ID")
    timestamp: str = Field(..., description="Prediction timestamp")


class ModelInfo(BaseModel):
    """Information about a loaded model"""
    model_name: str
    model_id: str
    version: str
    feature_count: int
    performance_metrics: Dict[str, float]
    last_prediction: Optional[str]
    prediction_count: int
    error_rate: float


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    models_loaded: int
    feature_registry_version: str
    api_version: str
    timestamp: str


# Global model registry
class ModelRegistry:
    """Registry for loaded contractual models"""
    
    def __init__(self):
        self.models: Dict[str, ContractualModel] = {}
        self.load_order = ['dna_analyzer', 'temporal_model', 'industry_model', 'ensemble_model']
        self.is_loaded = False
    
    async def load_models(self, model_dir: str = "models/contractual"):
        """Load all contractual models"""
        model_path = Path(model_dir)
        
        if not model_path.exists():
            logger.error(f"Model directory not found: {model_dir}")
            return
        
        for model_name in self.load_order[:3]:  # Load base models first
            try:
                model_file = model_path / f"{model_name}.pkl"
                if model_file.exists():
                    model = ContractualModel.load(str(model_file), feature_registry)
                    self.models[model_name] = model
                    logger.info(f"Loaded {model_name} (contract: {model.contract.feature_count} features)")
                else:
                    logger.warning(f"Model file not found: {model_file}")
            except Exception as e:
                logger.error(f"Failed to load {model_name}: {e}")
        
        # Load ensemble last (depends on base models)
        try:
            ensemble_file = model_path / "ensemble_model.pkl"
            if ensemble_file.exists():
                self.models['ensemble_model'] = ContractualModel.load(str(ensemble_file), feature_registry)
                logger.info("Loaded ensemble model")
        except Exception as e:
            logger.error(f"Failed to load ensemble: {e}")
        
        self.is_loaded = True
        logger.info(f"Model registry initialized with {len(self.models)} models")
    
    def get_model(self, name: str) -> Optional[ContractualModel]:
        """Get a specific model"""
        return self.models.get(name)
    
    def get_all_models(self) -> Dict[str, ContractualModel]:
        """Get all loaded models"""
        return self.models


# Initialize model registry
model_registry = ModelRegistry()


# Dependency for model access
async def get_models() -> ModelRegistry:
    """Dependency to ensure models are loaded"""
    if not model_registry.is_loaded:
        await model_registry.load_models()
    return model_registry


# API Endpoints
@app.on_event("startup")
async def startup_event():
    """Load models on startup"""
    logger.info("Starting FLASH Contractual API Server...")
    await model_registry.load_models()
    logger.info(f"Loaded {len(model_registry.models)} models")


@app.get("/", response_model=HealthResponse)
async def root():
    """Root endpoint with health check"""
    return HealthResponse(
        status="healthy",
        models_loaded=len(model_registry.models),
        feature_registry_version=feature_registry.version,
        api_version="2.0.0",
        timestamp=datetime.now().isoformat()
    )


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return await root()


@app.post("/predict", response_model=PredictionResponse)
async def predict(
    data: StartupData,
    models: ModelRegistry = Depends(get_models)
):
    """Main prediction endpoint with contract-based models"""
    try:
        # Convert input to dict
        input_data = data.dict()
        
        # Get predictions from each model
        model_predictions = {}
        diagnostics = {}
        
        # Base models
        for model_name in ['dna_analyzer', 'temporal_model', 'industry_model']:
            model = models.get_model(model_name)
            if model:
                try:
                    pred, diag = model.predict(input_data, return_diagnostics=True)
                    model_predictions[model_name] = float(pred[0])
                    diagnostics[model_name] = diag
                except Exception as e:
                    logger.error(f"Error in {model_name}: {e}")
                    model_predictions[model_name] = 0.5  # Default
        
        # Ensemble prediction (if base models succeeded)
        if len(model_predictions) == 3:
            ensemble_model = models.get_model('ensemble_model')
            if ensemble_model:
                # Prepare ensemble input
                ensemble_input = {
                    'dna_prediction': model_predictions['dna_analyzer'],
                    'temporal_prediction': model_predictions['temporal_model'],
                    'industry_prediction': model_predictions['industry_model']
                }
                try:
                    ensemble_pred = ensemble_model.predict(ensemble_input)
                    final_probability = float(ensemble_pred[0])
                    model_predictions['ensemble_model'] = final_probability
                except Exception as e:
                    logger.error(f"Ensemble error: {e}")
                    # Fallback to average
                    final_probability = np.mean(list(model_predictions.values()))
            else:
                # No ensemble, use average
                final_probability = np.mean(list(model_predictions.values()))
        else:
            # Not enough models, use what we have
            final_probability = np.mean(list(model_predictions.values())) if model_predictions else 0.5
        
        # Calculate CAMP scores from input data
        pillar_scores = {
            'capital': np.mean([
                data.revenue_growth_rate / 100,
                min(data.total_capital_raised_usd / 10_000_000, 1),
                data.annual_recurring_revenue_millions / 10,
                1 / (data.burn_multiple + 1),
                data.runway_months / 24
            ]),
            'advantage': np.mean([
                data.product_market_fit_score / 5,
                data.technology_score / 5,
                data.scalability_score / 5,
                float(data.has_patent),
                float(data.uses_ai_ml)
            ]),
            'market': np.mean([
                min(data.market_tam_billions / 10, 1),
                data.market_growth_rate / 100,
                min(data.customer_lifetime_value / data.customer_acquisition_cost / 3, 1),
                data.net_revenue_retention / 120
            ]),
            'people': np.mean([
                min(data.team_size_full_time / 50, 1),
                data.founder_experience_years / 20,
                float(data.repeat_founder),
                float(data.technical_founder),
                data.advisor_quality_score / 5
            ])
        }
        
        # Determine verdict and risk
        if final_probability >= 0.7:
            verdict = "PASS"
            risk_level = "LOW"
        elif final_probability >= 0.5:
            verdict = "CONDITIONAL PASS"
            risk_level = "MEDIUM"
        else:
            verdict = "FAIL"
            risk_level = "HIGH"
        
        # Generate insights
        risk_factors = []
        if data.burn_multiple > 3:
            risk_factors.append("High burn multiple indicates inefficient growth")
        if data.runway_months < 12:
            risk_factors.append("Limited runway poses immediate funding risk")
        if data.customer_acquisition_cost > data.customer_lifetime_value * 0.3:
            risk_factors.append("High CAC relative to LTV threatens unit economics")
        
        key_strengths = []
        if data.revenue_growth_rate > 100:
            key_strengths.append("Strong revenue growth momentum")
        if data.repeat_founder:
            key_strengths.append("Experienced founding team")
        if data.net_revenue_retention > 110:
            key_strengths.append("Excellent customer retention and expansion")
        
        improvement_areas = []
        if data.product_market_fit_score < 3:
            improvement_areas.append("Focus on achieving stronger product-market fit")
        if not data.technical_founder:
            improvement_areas.append("Consider adding technical leadership")
        if data.international_revenue_percent < 10:
            improvement_areas.append("Explore international expansion opportunities")
        
        # Calculate confidence (based on model agreement)
        if model_predictions:
            predictions = list(model_predictions.values())
            confidence = 1 - np.std(predictions)
        else:
            confidence = 0.5
        
        # Create response
        response = PredictionResponse(
            success_probability=final_probability,
            verdict=verdict,
            confidence_score=confidence,
            model_predictions=model_predictions,
            pillar_scores=pillar_scores,
            risk_level=risk_level,
            risk_factors=risk_factors,
            key_strengths=key_strengths,
            improvement_areas=improvement_areas,
            model_version="2.0.0",
            prediction_id=datetime.now().strftime("%Y%m%d%H%M%S"),
            timestamp=datetime.now().isoformat()
        )
        
        return response
        
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/models", response_model=List[ModelInfo])
async def get_model_info(models: ModelRegistry = Depends(get_models)):
    """Get information about loaded models"""
    model_info = []
    
    for name, model in models.get_all_models().items():
        info = model.get_model_info()
        model_info.append(ModelInfo(
            model_name=name,
            model_id=info['model_id'],
            version=info['model_version'],
            feature_count=info['feature_count'],
            performance_metrics=info['performance_metrics'],
            last_prediction=info['prediction_stats'].get('last_prediction'),
            prediction_count=info['prediction_stats']['total_predictions'],
            error_rate=info['prediction_stats']['error_rate']
        ))
    
    return model_info


@app.post("/explain/{model_name}")
async def explain_prediction(
    model_name: str,
    data: StartupData,
    models: ModelRegistry = Depends(get_models)
):
    """Get explanation for a specific model's prediction"""
    model = models.get_model(model_name)
    if not model:
        raise HTTPException(status_code=404, detail=f"Model {model_name} not found")
    
    try:
        explanation = model.explain(data.dict())
        return explanation
    except Exception as e:
        logger.error(f"Explanation error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/features")
async def get_feature_info():
    """Get information about the feature registry"""
    schema = feature_registry.get_schema()
    
    return {
        "version": feature_registry.version,
        "total_features": len(feature_registry.features),
        "categories": {
            "capital": len(feature_registry.get_features_by_category("capital")),
            "advantage": len(feature_registry.get_features_by_category("advantage")),
            "market": len(feature_registry.get_features_by_category("market")),
            "people": len(feature_registry.get_features_by_category("people"))
        },
        "schema": schema.to_dict('records')
    }


@app.post("/validate")
async def validate_input(data: StartupData):
    """Validate input data against feature registry"""
    is_valid, errors = feature_registry.validate_dict(data.dict())
    
    return {
        "valid": is_valid,
        "errors": errors,
        "feature_count": len(data.dict()),
        "missing_features": list(set(feature_registry.get_feature_names()) - set(data.dict().keys()))
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)