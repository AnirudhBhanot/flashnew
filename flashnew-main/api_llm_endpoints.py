#!/usr/bin/env python3
"""
LLM-Powered API Endpoints for Dynamic Analysis
"""

import os
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime
from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from pydantic import BaseModel, Field, field_validator, validator
import asyncio

from llm_analysis import LLMAnalysisEngine, get_fallback_recommendations

# Setup logging
logger = logging.getLogger(__name__)

# Create router
llm_router = APIRouter(prefix="/api/analysis", tags=["LLM Analysis"])

# Initialize LLM engine (singleton)
llm_engine = None

def get_llm_engine() -> LLMAnalysisEngine:
    """Get or create LLM engine instance"""
    global llm_engine
    if llm_engine is None:
        # Import and check for API key
        import os
        from dotenv import load_dotenv
        load_dotenv()  # Ensure environment variables are loaded
        
        api_key = os.getenv("DEEPSEEK_API_KEY")
        if api_key:
            logger.info(f"Initializing LLM engine with DeepSeek API key: {api_key[:10]}...")
        else:
            logger.warning("No DEEPSEEK_API_KEY found, using fallback mode")
            
        llm_engine = LLMAnalysisEngine(api_key=api_key)
    return llm_engine

# Request/Response Models
class RecommendationsRequest(BaseModel):
    startup_data: Dict[str, Any]
    scores: Dict[str, float]
    verdict: Optional[str] = None
    
    @field_validator('scores')
    def validate_scores(cls, v):
        required_keys = ['capital', 'advantage', 'market', 'people', 'success_probability']
        for key in required_keys:
            if key not in v:
                raise ValueError(f"Missing required score: {key}")
        return v

class WhatIfImprovement(BaseModel):
    id: str
    description: str
    camp_area: Optional[str] = None

class WhatIfRequest(BaseModel):
    startup_data: Dict[str, Any]
    current_scores: Dict[str, float]
    improvements: List[WhatIfImprovement]
    
    @field_validator('improvements')
    @classmethod
    def validate_improvements(cls, v):
        if len(v) == 0:
            raise ValueError("At least one improvement required")
        if len(v) > 10:
            raise ValueError("Maximum 10 improvements allowed")
        return v

class MarketInsightsRequest(BaseModel):
    startup_data: Dict[str, Any]

class CompetitorAnalysisRequest(BaseModel):
    startup_data: Dict[str, Any]
    top_n: int = Field(default=5, ge=1, le=10)

# Endpoints
@llm_router.post("/recommendations/dynamic")
async def get_dynamic_recommendations(
    request: RecommendationsRequest,
    background_tasks: BackgroundTasks = None,
    engine: LLMAnalysisEngine = Depends(get_llm_engine)
):
    """
    Generate AI-powered personalized recommendations
    
    Returns recommendations tailored to the startup's specific situation,
    industry, stage, and weaknesses.
    """
    try:
        logger.info(f"Generating dynamic recommendations for {request.startup_data.get('sector', 'startup')}")
        
        # Call LLM engine
        result = await engine.get_recommendations(
            request.startup_data,
            request.scores
        )
        
        # Log success for analytics if background_tasks available
        if background_tasks:
            background_tasks.add_task(
                log_llm_usage,
                "recommendations",
                request.startup_data.get("funding_stage"),
                request.startup_data.get("sector")
            )
        
        return result
        
    except Exception as e:
        logger.error(f"LLM recommendations failed: {e}")
        
        # Return fallback recommendations
        fallback = get_fallback_recommendations(
            request.startup_data,
            request.scores
        )
        fallback["error"] = "LLM unavailable, using fallback"
        return fallback

@llm_router.post("/whatif/dynamic")
async def analyze_whatif_scenario(
    request: WhatIfRequest,
    engine: LLMAnalysisEngine = Depends(get_llm_engine)
):
    """
    Analyze realistic impact of proposed improvements
    
    Uses AI to predict how specific changes would affect the startup's
    success probability and CAMP scores based on real market data.
    """
    try:
        logger.info(f"Analyzing what-if scenario with {len(request.improvements)} improvements")
        
        # Convert improvements to dict format
        improvements = [
            {"id": imp.id, "description": imp.description}
            for imp in request.improvements
        ]
        
        result = await engine.analyze_whatif(
            request.startup_data,
            request.current_scores,
            improvements
        )
        
        return result
        
    except Exception as e:
        logger.error(f"What-if analysis failed: {e}")
        raise HTTPException(
            status_code=503,
            detail="What-if analysis temporarily unavailable"
        )

@llm_router.post("/insights/market")
async def get_market_insights(
    request: MarketInsightsRequest,
    engine: LLMAnalysisEngine = Depends(get_llm_engine)
):
    """
    Get current market intelligence for the startup's industry
    
    Provides AI-generated insights on market trends, funding climate,
    recent exits, and emerging opportunities.
    """
    try:
        logger.info(f"Generating market insights for {request.startup_data.get('sector', 'startup')}")
        
        result = await engine.get_market_insights(request.startup_data)
        
        return result
        
    except Exception as e:
        logger.error(f"Market insights failed: {e}")
        raise HTTPException(
            status_code=503,
            detail="Market insights temporarily unavailable"
        )

@llm_router.post("/competitors/analyze")
async def analyze_competitors(
    request: CompetitorAnalysisRequest,
    engine: LLMAnalysisEngine = Depends(get_llm_engine)
):
    """
    Identify and analyze similar companies in the space
    
    Uses AI to find comparable companies and analyze their
    strengths, weaknesses, and positioning.
    """
    try:
        # Use the startup_data directly from the request
        startup_data = request.startup_data
        
        # Call the LLM engine for competitor analysis
        result = await engine.analyze_competitors(startup_data)
        
        return result
        
    except Exception as e:
        logger.error(f"Competitor analysis failed: {e}")
        raise HTTPException(
            status_code=503,
            detail="Competitor analysis temporarily unavailable"
        )

@llm_router.get("/status")
async def check_llm_status(engine: LLMAnalysisEngine = Depends(get_llm_engine)):
    """Check if LLM service is available"""
    try:
        # Simple health check
        test_data = {
            "funding_stage": "Seed",
            "sector": "SaaS",
            "annual_revenue_run_rate": 1000000
        }
        
        test_scores = {
            "capital": 0.6,
            "advantage": 0.7,
            "market": 0.8,
            "people": 0.65,
            "success_probability": 0.7
        }
        
        # Try a quick call with short cache
        await engine.get_recommendations(test_data, test_scores)
        
        return {
            "status": "operational",
            "model": engine.config.model,
            "cache_enabled": engine.redis_client is not None,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        return {
            "status": "degraded",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }

# Helper functions
async def log_llm_usage(
    analysis_type: str,
    funding_stage: Optional[str],
    sector: Optional[str]
):
    """Log LLM usage for analytics"""
    # TODO: Implement actual logging to analytics service
    logger.info(f"LLM usage: {analysis_type} for {funding_stage} {sector}")

# Cleanup on shutdown
async def shutdown_llm_engine():
    """Clean up LLM engine on shutdown"""
    global llm_engine
    if llm_engine:
        await llm_engine.close()
        llm_engine = None

# Progressive Deep Dive Request Models
class Phase1AnalysisRequest(BaseModel):
    porters_five_forces: Dict[str, Any] = Field(
        description="Porter's Five Forces analysis data"
    )
    internal_audit: Dict[str, Any] = Field(
        description="Internal audit data including strengths and weaknesses"
    )
    
    @field_validator('porters_five_forces')
    def validate_porters(cls, v):
        required_keys = [
            'supplier_power', 'buyer_power', 'competitive_rivalry',
            'threat_of_substitution', 'threat_of_new_entry'
        ]
        for key in required_keys:
            if key not in v:
                raise ValueError(f"Missing required Porter's force: {key}")
        return v

class Phase2VisionRealityRequest(BaseModel):
    vision_statement: str = Field(description="Company vision statement")
    current_reality: Dict[str, Any] = Field(
        description="Current state assessment"
    )
    ansoff_matrix_position: str = Field(
        description="Current position in Ansoff Matrix",
        pattern="^(market_penetration|market_development|product_development|diversification)$"
    )

class Phase3OrganizationalRequest(BaseModel):
    seven_s_framework: Dict[str, Any] = Field(
        description="7S framework assessment data"
    )
    
    @field_validator('seven_s_framework')
    def validate_seven_s(cls, v):
        required_keys = [
            'strategy', 'structure', 'systems', 'shared_values',
            'skills', 'style', 'staff'
        ]
        for key in required_keys:
            if key not in v:
                raise ValueError(f"Missing required 7S element: {key}")
        return v

class ScenarioDefinition(BaseModel):
    id: str
    name: str
    description: str
    assumptions: List[str]
    investment_required: float
    time_horizon_months: int

class Phase4ScenariosRequest(BaseModel):
    scenarios: List[ScenarioDefinition] = Field(
        min_items=2,
        max_items=5,
        description="Scenario definitions to analyze"
    )
    market_data: Dict[str, Any] = Field(
        description="Current market conditions and trends"
    )
    company_capabilities: Dict[str, Any] = Field(
        description="Company resources and capabilities"
    )

class DeepDiveSynthesisRequest(BaseModel):
    phase1_data: Dict[str, Any] = Field(description="Phase 1 analysis results")
    phase2_data: Dict[str, Any] = Field(description="Phase 2 vision-reality results")
    phase3_data: Dict[str, Any] = Field(description="Phase 3 organizational results")
    phase4_data: Dict[str, Any] = Field(description="Phase 4 scenario results")
    ml_predictions: Dict[str, Any] = Field(description="ML model predictions")

# Progressive Deep Dive Endpoints
@llm_router.post("/deepdive/phase1/analysis")
async def analyze_competitive_position(
    request: Phase1AnalysisRequest,
    background_tasks: BackgroundTasks = None,
    engine: LLMAnalysisEngine = Depends(get_llm_engine)
):
    """
    Phase 1: Analyze competitive position using Porter's Five Forces and internal audit
    
    Returns:
    - Competitive position assessment
    - Strategic gaps identification
    - Key opportunities and threats
    """
    try:
        logger.info("Starting Phase 1 Deep Dive Analysis")
        
        # Prepare context for LLM
        context = {
            "analysis_type": "competitive_position",
            "porters_five_forces": request.porters_five_forces,
            "internal_audit": request.internal_audit
        }
        
        # Call LLM engine for analysis
        result = await engine.analyze_competitive_position(context)
        
        # Log usage
        if background_tasks:
            background_tasks.add_task(
                log_llm_usage,
                "deepdive_phase1",
                None,
                None
            )
        
        return {
            "competitive_position": result.get("position_assessment"),
            "strategic_gaps": result.get("gaps"),
            "opportunities": result.get("opportunities"),
            "threats": result.get("threats"),
            "recommendations": result.get("recommendations"),
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Phase 1 analysis failed: {e}")
        raise HTTPException(
            status_code=503,
            detail="Competitive position analysis temporarily unavailable"
        )

@llm_router.post("/deepdive/phase2/vision-reality")
async def analyze_vision_reality_gap(
    request: Phase2VisionRealityRequest,
    engine: LLMAnalysisEngine = Depends(get_llm_engine)
):
    """
    Phase 2: Analyze vision-reality gaps and suggest growth strategies
    
    Returns:
    - Vision-reality gap analysis
    - Bridging strategies
    - Ansoff Matrix-based growth recommendations
    """
    try:
        logger.info("Starting Phase 2 Vision-Reality Analysis")
        
        context = {
            "vision": request.vision_statement,
            "reality": request.current_reality,
            "ansoff_position": request.ansoff_matrix_position
        }
        
        result = await engine.analyze_vision_reality_gap(context)
        
        return {
            "gap_analysis": result.get("gap_assessment"),
            "bridging_strategies": result.get("bridging_strategies"),
            "growth_recommendations": result.get("growth_recommendations"),
            "ansoff_progression": result.get("ansoff_next_steps"),
            "milestone_plan": result.get("milestones"),
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Phase 2 analysis failed: {e}")
        raise HTTPException(
            status_code=503,
            detail="Vision-reality analysis temporarily unavailable"
        )

@llm_router.post("/deepdive/phase3/organizational")
async def analyze_organizational_alignment(
    request: Phase3OrganizationalRequest,
    engine: LLMAnalysisEngine = Depends(get_llm_engine)
):
    """
    Phase 3: Analyze organizational alignment using 7S framework
    
    Returns:
    - Alignment assessment for each S
    - Misalignment identification
    - Intervention recommendations
    """
    try:
        logger.info("Starting Phase 3 Organizational Analysis")
        
        result = await engine.analyze_organizational_alignment(
            request.seven_s_framework
        )
        
        return {
            "alignment_scores": result.get("alignment_scores"),
            "misalignments": result.get("misalignments"),
            "critical_gaps": result.get("critical_gaps"),
            "interventions": result.get("interventions"),
            "implementation_roadmap": result.get("roadmap"),
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Phase 3 analysis failed: {e}")
        raise HTTPException(
            status_code=503,
            detail="Organizational analysis temporarily unavailable"
        )

@llm_router.post("/deepdive/phase4/scenarios")
async def analyze_strategic_scenarios(
    request: Phase4ScenariosRequest,
    engine: LLMAnalysisEngine = Depends(get_llm_engine)
):
    """
    Phase 4: Analyze strategic scenarios with ML-powered predictions
    
    Returns:
    - Probability of success for each scenario
    - Risk-weighted recommendations
    - Optimal scenario selection
    """
    try:
        logger.info(f"Starting Phase 4 Scenario Analysis with {len(request.scenarios)} scenarios")
        
        # Prepare scenarios for analysis
        scenarios_data = [
            {
                "id": s.id,
                "name": s.name,
                "description": s.description,
                "assumptions": s.assumptions,
                "investment": s.investment_required,
                "timeline": s.time_horizon_months
            }
            for s in request.scenarios
        ]
        
        context = {
            "scenarios": scenarios_data,
            "market_data": request.market_data,
            "capabilities": request.company_capabilities
        }
        
        # Get ML predictions and LLM analysis
        result = await engine.analyze_scenarios_with_ml(context)
        
        return {
            "scenario_assessments": result.get("assessments"),
            "success_probabilities": result.get("probabilities"),
            "risk_analysis": result.get("risks"),
            "recommended_scenario": result.get("recommended"),
            "alternative_paths": result.get("alternatives"),
            "decision_criteria": result.get("criteria"),
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Phase 4 analysis failed: {e}")
        raise HTTPException(
            status_code=503,
            detail="Scenario analysis temporarily unavailable"
        )

@llm_router.post("/deepdive/synthesis")
async def synthesize_deep_dive_analysis(
    request: DeepDiveSynthesisRequest,
    engine: LLMAnalysisEngine = Depends(get_llm_engine)
):
    """
    Synthesize all deep dive phases into executive summary and action plan
    
    Returns:
    - Executive summary
    - Prioritized action plan
    - Key decisions required
    - Success metrics
    """
    try:
        logger.info("Starting Deep Dive Synthesis")
        
        # Combine all phase data
        full_context = {
            "phase1": request.phase1_data,
            "phase2": request.phase2_data,
            "phase3": request.phase3_data,
            "phase4": request.phase4_data,
            "ml_predictions": request.ml_predictions
        }
        
        result = await engine.synthesize_deep_dive(full_context)
        
        return {
            "executive_summary": result.get("summary"),
            "critical_insights": result.get("insights"),
            "action_plan": result.get("action_plan"),
            "priority_matrix": result.get("priorities"),
            "key_decisions": result.get("decisions"),
            "success_metrics": result.get("metrics"),
            "risk_mitigation": result.get("risk_mitigation"),
            "timeline": result.get("timeline"),
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Deep dive synthesis failed: {e}")
        raise HTTPException(
            status_code=503,
            detail="Analysis synthesis temporarily unavailable"
        )

# Export router and shutdown function
__all__ = ['llm_router', 'shutdown_llm_engine']