#!/usr/bin/env python3
"""
Framework Intelligence Engine API Endpoints
"""

import os
import sys
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field

# Setup logging
logger = logging.getLogger(__name__)

# Add framework_intelligence to path
current_dir = os.path.dirname(os.path.abspath(__file__))

try:
    from framework_intelligence.framework_selector import FrameworkSelector, StartupContext, BusinessStage, IndustryType, ChallengeType
    from framework_intelligence.framework_database import FRAMEWORKS as FRAMEWORK_DATABASE, ComplexityLevel
except ImportError as e:
    logger.error(f"Failed to import framework modules: {e}")
    raise

# Create router
framework_router = APIRouter(prefix="/api/frameworks", tags=["Framework Intelligence"])

# Initialize framework selector
framework_selector = FrameworkSelector()

# Request/Response Models
class FrameworkRequest(BaseModel):
    company_stage: str = Field(..., description="Current stage of the company")
    industry: str = Field(..., description="Industry or sector")
    primary_challenge: str = Field(..., description="Main challenge or focus area")
    team_size: int = Field(..., ge=1, description="Size of the team")
    resources: str = Field(..., description="Available resources (limited/moderate/abundant)")
    timeline: str = Field(..., description="Implementation timeline")
    goals: List[str] = Field(default_factory=list, description="Business goals")
    current_frameworks: List[str] = Field(default_factory=list, description="Frameworks already in use")

# Helper function to create StartupContext from request
def create_startup_context(request: FrameworkRequest) -> StartupContext:
    """Convert request data to StartupContext object"""
    # Map string values to enums
    stage_map = {
        # Frontend values
        "pre_seed": BusinessStage.IDEA,
        "pre-seed": BusinessStage.IDEA,
        "seed": BusinessStage.MVP,
        "series_a": BusinessStage.GROWTH,
        "series-a": BusinessStage.GROWTH,
        "series_b": BusinessStage.GROWTH,
        "series-b": BusinessStage.GROWTH,
        "series_c": BusinessStage.SCALE,
        "series-c": BusinessStage.SCALE,
        # Original values
        "idea": BusinessStage.IDEA,
        "mvp": BusinessStage.MVP,
        "product_market_fit": BusinessStage.PRODUCT_MARKET_FIT,
        "growth": BusinessStage.GROWTH,
        "scale": BusinessStage.SCALE,
        "mature": BusinessStage.MATURE,
        # Additional values
        "startup": BusinessStage.MVP,
        "expansion": BusinessStage.SCALE
    }
    
    industry_map = {
        # Frontend values
        "tech": IndustryType.TECHNOLOGY,
        "technology": IndustryType.TECHNOLOGY,
        "artificial_intelligence": IndustryType.DEEPTECH,
        "ai": IndustryType.DEEPTECH,
        "ai-ml": IndustryType.DEEPTECH,
        "machine-learning": IndustryType.DEEPTECH,
        # Original values
        "b2b_saas": IndustryType.B2B_SAAS,
        "b2c_saas": IndustryType.B2C_SAAS,
        "saas": IndustryType.B2B_SAAS,
        "ecommerce": IndustryType.ECOMMERCE,
        "marketplace": IndustryType.MARKETPLACE,
        "fintech": IndustryType.FINTECH,
        "healthtech": IndustryType.HEALTHTECH,
        "healthcare": IndustryType.HEALTHTECH,
        "edtech": IndustryType.EDTECH,
        "enterprise": IndustryType.ENTERPRISE,
        "consumer": IndustryType.CONSUMER,
        "hardware": IndustryType.HARDWARE,
        "deeptech": IndustryType.DEEPTECH,
        "services": IndustryType.SERVICES,
        "retail": IndustryType.RETAIL,
        "manufacturing": IndustryType.MANUFACTURING,
        # Additional values
        "blockchain": IndustryType.FINTECH,
        "crypto": IndustryType.FINTECH,
        "real-estate": IndustryType.REAL_ESTATE,
        "transportation": IndustryType.LOGISTICS,
        "clean-tech": IndustryType.CLEANTECH,
        "deep-tech": IndustryType.DEEPTECH
    }
    
    challenge_map = {
        # Frontend values
        "finding_product_market_fit": ChallengeType.PRODUCT_DEVELOPMENT,
        "fundraising": ChallengeType.FUNDING,
        "accelerating_growth": ChallengeType.SCALING,
        "scaling_operations": ChallengeType.SCALING,
        # Original values
        "raising_funding": ChallengeType.FUNDING,
        "customer_acquisition": ChallengeType.CUSTOMER_ACQUISITION,
        "team_building": ChallengeType.TEAM_BUILDING,
        "revenue_growth": ChallengeType.SCALING,
        "operational_efficiency": ChallengeType.OPERATIONAL_EFFICIENCY,
        # Additional common values
        "product_development": ChallengeType.PRODUCT_DEVELOPMENT,
        "market_expansion": ChallengeType.MARKET_PENETRATION,
        "competition": ChallengeType.COMPETITION,
        "talent_acquisition": ChallengeType.TALENT_ACQUISITION,
        "regulatory": ChallengeType.REGULATORY_COMPLIANCE
    }
    
    # Create context object
    return StartupContext(
        stage=stage_map.get(request.company_stage.lower(), BusinessStage.MVP),
        industry=industry_map.get(request.industry.lower(), IndustryType.OTHER),
        team_size=request.team_size,
        funding_stage=request.resources,
        primary_challenges=[challenge_map.get(request.primary_challenge.lower(), ChallengeType.PRODUCT_DEVELOPMENT)],
        goals=request.goals,
        constraints=[request.timeline],
        existing_frameworks=request.current_frameworks,
        complexity_preference=ComplexityLevel.BASIC if request.resources == "limited" else ComplexityLevel.INTERMEDIATE
    )

class FrameworkRecommendation(BaseModel):
    framework_name: str
    score: float
    category: str
    complexity: str
    time_to_implement: str
    description: str
    why_recommended: str
    key_benefits: List[str]
    implementation_tips: List[str]

class ImplementationRoadmap(BaseModel):
    phase: int
    duration: str
    frameworks: List[str]
    objectives: List[str]
    success_metrics: List[str]
    dependencies: List[str]

class FrameworkCombination(BaseModel):
    frameworks: List[str]
    synergy_score: float
    combined_benefit: str
    implementation_order: List[str]
    estimated_impact: str

# Endpoints
@framework_router.post("/recommend")
async def get_framework_recommendations(request: FrameworkRequest) -> Dict[str, Any]:
    """
    Get AI-powered framework recommendations based on company context
    """
    try:
        # Create context object
        context = create_startup_context(request)
        
        # Get recommendations
        recommendations = framework_selector.recommend_frameworks(
            context=context,
            max_recommendations=10
        )
        
        # Format recommendations
        formatted_recommendations = []
        for rec in recommendations:
            framework = rec.framework
            # Ensure framework is properly loaded
            if isinstance(framework, str):
                logger.warning(f"Framework {framework} is string, not object")
                continue
            formatted_recommendations.append({
                "framework_name": framework.name,
                "score": round(rec.relevance_score, 2),
                "category": getattr(framework.category, "value", str(framework.category)) if hasattr(framework, "category") else "Unknown",
                "complexity": framework.complexity.value,
                "time_to_implement": framework.time_to_implement,
                "description": framework.description,
                "why_recommended": rec.rationale[0] if rec.rationale else "Strong match for your context",
                "key_benefits": framework.expected_outcomes[:3],
                "implementation_tips": framework.application_steps[:3]
            })
        
        return {
            "recommendations": formatted_recommendations,
            "total_frameworks_analyzed": len(FRAMEWORK_DATABASE),
            "context_summary": f"{request.company_stage} {request.industry} company focusing on {request.primary_challenge}",
            "generated_at": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Framework recommendation error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@framework_router.post("/roadmap")
async def get_implementation_roadmap(request: FrameworkRequest) -> Dict[str, Any]:
    """
    Generate a phased implementation roadmap for recommended frameworks
    """
    try:
        # Create context object
        context = create_startup_context(request)
        
        # First get recommendations
        recommendations = framework_selector.recommend_frameworks(
            context=context,
            max_recommendations=8
        )
        
        # Then create roadmap from recommendations
        roadmap = framework_selector.create_implementation_roadmap(
            recommendations=recommendations
        )
        
        # Format roadmap
        formatted_phases = []
        phase_number = 1
        for phase_name, phase_recommendations in roadmap.items():
            if phase_recommendations:  # Only include phases with frameworks
                frameworks = []
                for rec in phase_recommendations:
                    frameworks.append({
                        "name": rec.framework.name,
                        "category": getattr(rec.framework.category, "value", str(rec.framework.category)) if hasattr(rec.framework, "category") else "Unknown",
                        "complexity": getattr(rec.framework.complexity, "value", str(rec.framework.complexity)) if hasattr(rec.framework, "complexity") else "Unknown"
                    })
                
                # Extract duration from phase name
                duration = phase_name.split("(")[1].split(")")[0] if "(" in phase_name else "3 months"
                
                formatted_phases.append({
                    "phase": phase_number,
                    "duration": duration,
                    "frameworks": [f["name"] for f in frameworks],
                    "objectives": [
                        f"Implement {len(frameworks)} framework{'s' if len(frameworks) > 1 else ''}",
                        "Establish measurement systems",
                        "Build team capabilities"
                    ],
                    "success_metrics": [
                        "Framework adoption rate > 80%",
                        "Team competency assessments",
                        "Business metric improvements"
                    ],
                    "dependencies": [frameworks[0]["name"]] if phase_number > 1 and formatted_phases else []
                })
                phase_number += 1
        
        return {
            "roadmap": formatted_phases,
            "total_duration": "12-18 months",
            "complexity_level": "Progressive",
            "success_factors": [
                "Executive commitment and sponsorship",
                "Dedicated implementation team",
                "Regular progress monitoring",
                "Flexibility to adapt as needed"
            ],
            "generated_at": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Roadmap generation error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@framework_router.post("/combinations")
async def find_framework_combinations(request: FrameworkRequest) -> Dict[str, Any]:
    """
    Find synergistic framework combinations
    """
    try:
        # Create context object
        context = create_startup_context(request)
        
        # Find combinations
        combinations = framework_selector.find_framework_combinations(
            context=context,
            max_combinations=5
        )
        
        # Format combinations
        formatted_combinations = []
        for i, combo in enumerate(combinations[:5]):  # Limit to 5 combinations
            framework_names = [f.name for f in combo]
            framework_categories = [getattr(f.category, "value", str(f.category)) if hasattr(f, "category") else "Unknown" for f in combo]
            
            # Calculate a synergy score based on complementary frameworks
            synergy_score = 0.8 + (0.1 * len(combo))  # Base score + bonus for more frameworks
            
            formatted_combinations.append({
                "frameworks": framework_names,
                "synergy_score": round(synergy_score, 2),
                "combined_benefit": f"Integrated {' + '.join(set(framework_categories))} approach",
                "implementation_order": framework_names,  # Order matters
                "estimated_impact": "High" if synergy_score > 0.85 else "Medium"
            })
        
        return {
            "combinations": formatted_combinations,
            "recommendation": "Start with the highest synergy score combination for maximum impact",
            "generated_at": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Combination finding error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@framework_router.get("/categories")
async def get_framework_categories() -> Dict[str, Any]:
    """
    Get all available framework categories and counts
    """
    categories = {}
    for framework_id, framework in FRAMEWORK_DATABASE.items():
        # Get category name from enum
        category = framework.category.value if hasattr(framework, 'category') else "Unknown"
        
        if category not in categories:
            categories[category] = {
                "count": 0,
                "subcategories": set(),
                "complexity_distribution": {"Basic": 0, "Intermediate": 0, "Advanced": 0, "Expert": 0}
            }
        
        categories[category]["count"] += 1
        if hasattr(framework, "subcategory") and framework.subcategory:
            categories[category]["subcategories"].add(framework.subcategory)
        
        # Get complexity name
        if hasattr(framework, 'complexity'):
            complexity_name = framework.complexity.name.capitalize()
            if complexity_name in categories[category]["complexity_distribution"]:
                categories[category]["complexity_distribution"][complexity_name] += 1
    
    # Convert sets to lists for JSON serialization
    for cat in categories:
        categories[cat]["subcategories"] = list(categories[cat]["subcategories"])
    
    return {
        "categories": categories,
        "total_frameworks": len(FRAMEWORK_DATABASE),
        "last_updated": datetime.now().isoformat()
    }

@framework_router.get("/framework/{framework_name}")
async def get_framework_details(framework_name: str) -> Dict[str, Any]:
    """
    Get detailed information about a specific framework
    """
    # Find framework
    framework = None
    for fid, f in FRAMEWORK_DATABASE.items():
        if f.name.lower() == framework_name.lower():
            framework = f
            break
    
    if not framework:
        raise HTTPException(status_code=404, detail=f"Framework '{framework_name}' not found")
    
    return {
        "name": framework.name,
        "category": getattr(framework.category, "value", str(framework.category)) if hasattr(framework, "category") else "Unknown",
        "subcategory": framework.subcategory,
        "description": framework.description,
        "when_to_use": framework.when_to_use,
        "key_components": framework.key_components,
        "steps": getattr(framework, "application_steps", getattr(framework, "steps", [])),
        "expected_outcomes": framework.expected_outcomes,
        "complexity": getattr(framework.complexity, "value", str(framework.complexity)) if hasattr(framework, "complexity") else "Unknown",
        "time_to_implement": framework.time_to_implement,
        "industries": getattr(framework, "industry_relevance", getattr(framework, "industries", [])),
        "business_stages": getattr(framework, "business_stages", []),
        "prerequisites": framework.prerequisites,
        "resources_required": framework.resources_required,
        "common_pitfalls": framework.common_pitfalls,
        "success_metrics": framework.success_metrics,
        "complementary_frameworks": framework.complementary_frameworks,
        "references": getattr(framework, "references", [])
    }

@framework_router.post("/implementation-guide")
async def get_implementation_guide(
    framework_name: str,
    context: FrameworkRequest
) -> Dict[str, Any]:
    """
    Get customized implementation guide for a specific framework
    """
    try:
        guide_context = {
            "business_stage": context.company_stage,
            "industry": context.industry,
            "team_size": context.team_size,
            "resources": context.resources,
            "timeline": context.timeline
        }
        
        guide = framework_selector.generate_implementation_guide(
            framework_name=framework_name,
            context=guide_context
        )
        
        return {
            "framework": framework_name,
            "customized_steps": guide["customized_steps"],
            "timeline": guide["timeline"],
            "resource_allocation": guide["resource_allocation"],
            "quick_wins": guide["quick_wins"],
            "risk_mitigation": guide["risk_mitigation"],
            "success_indicators": guide["success_indicators"],
            "generated_at": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Implementation guide error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@framework_router.get("/search")
async def search_frameworks(
    query: str,
    category: Optional[str] = None,
    complexity: Optional[str] = None,
    industry: Optional[str] = None
) -> Dict[str, Any]:
    """
    Search frameworks by name, description, or filters
    """
    results = []
    query_lower = query.lower()
    
    for fid, framework in FRAMEWORK_DATABASE.items():
        # Apply filters
        framework_category = framework.category.value if hasattr(framework, 'category') else "Unknown"
        framework_complexity = framework.complexity.name.capitalize() if hasattr(framework, 'complexity') else "Unknown"
        
        if category and framework_category != category:
            continue
        if complexity and framework_complexity != complexity:
            continue
        if industry and hasattr(framework, "industry_relevance") and industry not in framework.industry_relevance:
            continue
        
        # Search in name and description
        if (query_lower in framework.name.lower() or 
            query_lower in framework.description.lower() or
            any(query_lower in component.lower() for component in framework.key_components)):
            
            results.append({
                "name": framework.name,
                "category": framework_category,
                "complexity": framework_complexity,
                "description": framework.description[:200] + "...",
                "match_relevance": 1.0 if query_lower in framework.name.lower() else 0.7
            })
    
    # Sort by relevance
    results.sort(key=lambda x: x["match_relevance"], reverse=True)
    
    return {
        "results": results[:20],  # Limit to top 20
        "total_matches": len(results),
        "query": query,
        "filters_applied": {
            "category": category,
            "complexity": complexity,
            "industry": industry
        }
    }

# Export router
__all__ = ['framework_router']