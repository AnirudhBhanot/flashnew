#!/usr/bin/env python3
"""
Enhanced Framework API Endpoints
Uses advanced MIT/HBS framework selection methodology
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import logging
import asyncio

from enhanced_framework_selector import EnhancedFrameworkSelector

logger = logging.getLogger(__name__)
router = APIRouter()

# Initialize enhanced selector
enhanced_selector = EnhancedFrameworkSelector()


class FrameworkRequest(BaseModel):
    """Request model for framework selection"""
    startup_name: str
    sector: str
    stage: str
    revenue: float = 0
    growth_rate: float = 0
    burn_rate: float = 0
    ltv_cac_ratio: float = 0
    net_revenue_retention: float = 100
    team_size: int = 10
    runway_months: float = 12
    key_challenges: List[str] = []
    customer_count: Optional[int] = None
    market_share: Optional[float] = None
    include_journey: bool = False
    max_frameworks: int = 5


class FrameworkDetailRequest(BaseModel):
    """Request for specific framework details"""
    framework_id: str
    industry: Optional[str] = None


@router.post("/api/frameworks/enhanced/select")
async def select_frameworks_enhanced(request: FrameworkRequest):
    """
    Select frameworks using advanced academic methodology
    
    This endpoint uses the MIT/HBS framework selection system that includes:
    - Multi-dimensional taxonomy scoring
    - Anti-pattern detection
    - Industry-specific customization
    - Journey planning
    """
    try:
        logger.info(f"Enhanced framework selection for {request.startup_name}")
        
        # Convert request to startup data dict
        startup_data = request.dict()
        
        # Get enhanced recommendations
        result = await enhanced_selector.select_frameworks_for_startup(
            startup_data,
            max_frameworks=request.max_frameworks
        )
        
        if not result["success"]:
            logger.error(f"Framework selection failed: {result.get('error')}")
            # Return fallback frameworks
            return {
                "success": True,
                "frameworks": result.get("fallback", []),
                "methodology": "Fallback selection",
                "warning": "Using simplified selection due to error"
            }
            
        return result
        
    except Exception as e:
        logger.error(f"Enhanced framework selection error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/api/frameworks/enhanced/journey")
async def create_framework_journey(request: FrameworkRequest):
    """
    Create a comprehensive framework implementation journey
    
    Returns a phased approach with:
    - Immediate (0-30 days)
    - Short-term (30-90 days)  
    - Medium-term (3-6 months)
    - Long-term (6-12 months)
    """
    try:
        logger.info(f"Creating framework journey for {request.startup_name}")
        
        # Ensure journey is included
        startup_data = request.dict()
        startup_data["include_journey"] = True
        
        result = await enhanced_selector.select_frameworks_for_startup(
            startup_data,
            max_frameworks=10  # Get more for journey planning
        )
        
        if not result["success"] or not result.get("journey"):
            raise HTTPException(
                status_code=500, 
                detail="Failed to create framework journey"
            )
            
        return {
            "success": True,
            "journey": result["journey"],
            "company_context": result["company_context"],
            "methodology": result["methodology"]
        }
        
    except Exception as e:
        logger.error(f"Journey creation error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/api/frameworks/enhanced/details")
async def get_framework_details(request: FrameworkDetailRequest):
    """
    Get detailed information about a specific framework
    Including industry-specific variants
    """
    try:
        details = await enhanced_selector.get_framework_details(
            request.framework_id,
            request.industry
        )
        
        if "error" in details:
            raise HTTPException(status_code=404, detail=details["error"])
            
        return {
            "success": True,
            "framework": details["framework"],
            "industry_variant": details.get("industry_variant")
        }
        
    except Exception as e:
        logger.error(f"Framework details error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/api/frameworks/enhanced/test")
async def test_enhanced_system():
    """Test endpoint to verify the enhanced system is working"""
    
    test_data = {
        "startup_name": "API Test Company",
        "sector": "saas_b2b",
        "stage": "series_a",
        "revenue": 3000000,
        "growth_rate": 120,
        "burn_rate": 400000,
        "ltv_cac_ratio": 3.2,
        "net_revenue_retention": 112,
        "team_size": 45,
        "runway_months": 15,
        "key_challenges": [
            "Competitive pressure from Microsoft",
            "Need to improve unit economics",
            "Scaling engineering team"
        ],
        "max_frameworks": 3
    }
    
    try:
        result = await enhanced_selector.select_frameworks_for_startup(test_data)
        
        return {
            "success": True,
            "test_company": test_data["startup_name"],
            "frameworks_selected": len(result.get("frameworks", [])),
            "top_framework": result["frameworks"][0]["name"] if result.get("frameworks") else None,
            "methodology": result.get("methodology", "Unknown"),
            "system_status": "Enhanced framework system operational"
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "system_status": "Enhanced framework system error"
        }


# Include router in main app
def include_enhanced_framework_routes(app):
    """Include enhanced framework routes in FastAPI app"""
    app.include_router(router)
    logger.info("Enhanced Framework API endpoints loaded - MIT/HBS methodology active")