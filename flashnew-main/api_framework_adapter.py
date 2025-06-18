#!/usr/bin/env python3
"""
Framework Intelligence Adapter for Startup Data
Converts startup assessment data to framework recommendation format
"""

from typing import Dict, List, Any
from fastapi import APIRouter, HTTPException, Body
from pydantic import BaseModel
import logging

logger = logging.getLogger(__name__)

# Create router
adapter_router = APIRouter(tags=["Framework Adapter"])

class StartupDataRequest(BaseModel):
    """Request model matching the frontend assessment data format"""
    # All the 45 fields from the assessment
    total_capital_raised_usd: float = 0
    cash_on_hand_usd: float = 0
    monthly_burn_usd: float = 0
    runway_months: float = 0
    funding_stage: str = "seed"
    investor_tier_primary: str = "none"
    
    product_stage: str = "mvp"
    proprietary_tech: bool = False
    patents_filed: int = 0
    monthly_active_users: int = 0
    
    market_size_usd: float = 0
    market_growth_rate_annual: float = 0
    competitor_count: int = 0
    market_share_percentage: float = 0
    
    team_size_full_time: int = 1
    founders_industry_experience_years: float = 0
    
    b2b_or_b2c: str = "b2b"
    sector: str = "saas"
    
    # Add any other fields as needed
    startup_name: str = "Startup"


def convert_to_framework_request(startup_data: Dict[str, Any]) -> Dict[str, Any]:
    """Convert startup data to framework recommendation request format"""
    
    # Determine company stage based on funding and product stage
    company_stage = "mvp"
    if startup_data.get("funding_stage") == "series_a":
        company_stage = "growth"
    elif startup_data.get("funding_stage") == "series_b":
        company_stage = "scale"
    elif startup_data.get("product_stage") == "launched":
        company_stage = "product_market_fit"
    
    # Determine primary challenge based on metrics
    primary_challenge = "finding_product_market_fit"
    if startup_data.get("monthly_active_users", 0) > 10000:
        primary_challenge = "scaling_operations"
    elif startup_data.get("runway_months", 0) < 6:
        primary_challenge = "raising_funding"
    elif startup_data.get("team_size_full_time", 0) < 5:
        primary_challenge = "team_building"
    
    # Determine resources based on funding
    resources = "limited"
    if startup_data.get("total_capital_raised_usd", 0) > 5000000:
        resources = "abundant"
    elif startup_data.get("total_capital_raised_usd", 0) > 1000000:
        resources = "moderate"
    
    # Set timeline based on runway
    timeline = "urgent"
    if startup_data.get("runway_months", 0) > 12:
        timeline = "flexible"
    elif startup_data.get("runway_months", 0) > 6:
        timeline = "moderate"
    
    # Generate goals based on current state
    goals = []
    if startup_data.get("product_stage") in ["mvp", "beta"]:
        goals.append("Achieve product-market fit")
    if startup_data.get("monthly_active_users", 0) < 1000:
        goals.append("Acquire first customers")
    if startup_data.get("runway_months", 0) < 12:
        goals.append("Extend runway")
    if startup_data.get("team_size_full_time", 0) < 10:
        goals.append("Build core team")
    
    return {
        "company_stage": company_stage,
        "industry": startup_data.get("sector", "saas"),
        "primary_challenge": primary_challenge,
        "team_size": max(1, startup_data.get("team_size_full_time", 1)),  # Ensure minimum of 1
        "resources": resources,
        "timeline": timeline,
        "goals": goals,
        "current_frameworks": []  # Could be populated from user input
    }


@adapter_router.post("/api/frameworks/recommend-for-startup")
async def get_framework_recommendations_for_startup(startup_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Get framework recommendations based on startup assessment data
    This endpoint adapts the startup data format to the framework request format
    """
    try:
        # Convert startup data to framework request format
        framework_request = convert_to_framework_request(startup_data)
        
        # Import framework router's handler directly to avoid circular dependencies
        from api_framework_endpoints import get_framework_recommendations, FrameworkRequest
        
        # Create a proper FrameworkRequest object
        request_obj = FrameworkRequest(
            company_stage=framework_request["company_stage"],
            industry=framework_request["industry"],
            primary_challenge=framework_request["primary_challenge"],
            team_size=framework_request["team_size"],
            resources=framework_request["resources"],
            timeline=framework_request["timeline"],
            goals=framework_request["goals"],
            current_frameworks=framework_request["current_frameworks"]
        )
        
        # Call the framework recommendation function directly
        data = await get_framework_recommendations(request_obj)
        
        # Add total frameworks available
        from framework_intelligence.framework_database import get_framework_statistics
        stats = get_framework_statistics()
        data["total_frameworks_available"] = stats["total_frameworks"]
        
        # Transform the response to match frontend expectations
        if "recommendations" in data:
            data["frameworks"] = [
                {
                    "framework_id": rec["framework_name"].lower().replace(" ", "_"),
                    "framework_name": rec["framework_name"],
                    "score": rec["score"],
                    "category": rec["category"],
                    "complexity": rec["complexity"],
                    "time_to_implement": rec["time_to_implement"],
                    "description": rec["description"],
                    "why_recommended": rec["why_recommended"],
                    "key_benefits": rec["key_benefits"]
                }
                for rec in data["recommendations"]
            ]
        
        return data
            
    except Exception as e:
        logger.error(f"Framework recommendation adapter error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


class RoadmapRequest(BaseModel):
    startup_data: Dict[str, Any]
    selected_option: str = "vertical-focus"


@adapter_router.post("/api/frameworks/roadmap-for-startup")
async def get_implementation_roadmap_for_startup(request: RoadmapRequest) -> Dict[str, Any]:
    """
    Generate implementation roadmap based on startup assessment data
    This endpoint adapts the startup data format to the framework request format
    """
    try:
        # Convert startup data to framework request format
        framework_request = convert_to_framework_request(request.startup_data)
        
        # Import framework router's handler directly
        from api_framework_endpoints import get_implementation_roadmap, FrameworkRequest
        
        # Create a proper FrameworkRequest object
        request_obj = FrameworkRequest(
            company_stage=framework_request["company_stage"],
            industry=framework_request["industry"],
            primary_challenge=framework_request["primary_challenge"],
            team_size=framework_request["team_size"],
            resources=framework_request["resources"],
            timeline=framework_request["timeline"],
            goals=framework_request["goals"],
            current_frameworks=framework_request["current_frameworks"]
        )
        
        # Call the roadmap function directly
        data = await get_implementation_roadmap(request_obj)
        
        # Transform the response to match frontend expectations
        if "roadmap" in data:
            # Enhance roadmap with startup-specific context
            for phase in data["roadmap"]:
                if phase["phase"] == 1:
                    phase["title"] = "Foundation & Quick Wins"
                    phase["actions"] = [
                        f"Validate {framework_request['primary_challenge'].replace('_', ' ')} assumptions",
                        "Set up measurement systems",
                        "Quick wins implementation",
                        "Team alignment workshops"
                    ]
                elif phase["phase"] == 2:
                    phase["title"] = "Market Validation & Scaling"
                    phase["actions"] = [
                        "Launch pilot programs",
                        f"Scale in {framework_request['industry']} market",
                        "Build customer success processes"
                    ]
                elif phase["phase"] == 3:
                    phase["title"] = "Full Implementation & Optimization"
                    phase["actions"] = [
                        "Optimize based on learnings",
                        "Scale successful initiatives",
                        "Build sustainable processes"
                    ]
                    
        return data
            
    except Exception as e:
        logger.error(f"Roadmap adapter error: {e}")
        raise HTTPException(status_code=500, detail=str(e))