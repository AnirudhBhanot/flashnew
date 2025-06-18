#!/usr/bin/env python3
"""
Hybrid Michelin Analysis - Uses DeepSeek when available, fallback when not
"""

import os
import json
import logging
import asyncio
from typing import Dict, List, Optional, Any
from datetime import datetime
from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel, Field

# Import the original components
from api_michelin_llm_analysis import (
    MichelinAnalysisEngine,
    StartupData,
    MichelinAnalysisRequest,
    MichelinAnalysisResponse
)

# Import the working/fallback version
from api_michelin_working import analyze_startup_working, SimpleStartupData, SimpleAnalysisRequest

logger = logging.getLogger(__name__)

# Create router
hybrid_router = APIRouter(prefix="/api/michelin", tags=["Michelin Hybrid"])

class HybridMichelinEngine:
    """Hybrid engine that uses DeepSeek with fallback"""
    
    def __init__(self):
        self.deepseek_engine = MichelinAnalysisEngine()
        self.use_deepseek = True  # Can be toggled
        self.deepseek_timeout = 30  # 30 second timeout for quick check
        
    async def analyze_with_fallback(self, request: MichelinAnalysisRequest) -> Dict:
        """Try DeepSeek first, fallback if it fails or times out"""
        
        if not self.use_deepseek:
            logger.info("DeepSeek disabled, using fallback")
            return await self._use_fallback(request)
        
        try:
            # First, try a quick test to see if DeepSeek is responsive
            logger.info(f"Testing DeepSeek availability for {request.startup_data.startup_name}")
            
            # Try to get just Phase 1 with a reasonable timeout
            test_response = await asyncio.wait_for(
                self._test_deepseek_availability(),
                timeout=10.0
            )
            
            if not test_response:
                logger.warning("DeepSeek test failed, using fallback")
                return await self._use_fallback(request)
            
            # If test passed, try full analysis with longer timeout
            logger.info("DeepSeek available, performing full analysis")
            result = await asyncio.wait_for(
                self.deepseek_engine.analyze_startup(request.startup_data),
                timeout=120.0  # 120 second timeout for full analysis
            )
            
            # Convert to dict if it's a Pydantic model
            if hasattr(result, 'model_dump'):
                return result.model_dump()
            return result
            
        except asyncio.TimeoutError:
            logger.warning(f"DeepSeek timed out, using fallback")
            return await self._use_fallback(request)
        except Exception as e:
            logger.error(f"DeepSeek failed: {str(e)}, using fallback")
            return await self._use_fallback(request)
    
    async def _test_deepseek_availability(self) -> bool:
        """Quick test to check if DeepSeek is responding"""
        try:
            response = await self.deepseek_engine._call_deepseek([
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Reply with 'OK' in JSON format: {\"status\": \"OK\"}"}
            ], max_tokens=20)
            
            return "OK" in response or "ok" in response.lower()
        except:
            return False
    
    async def _use_fallback(self, request: MichelinAnalysisRequest) -> Dict:
        """Use the working fallback implementation"""
        # Convert to simple format
        simple_data = SimpleStartupData(
            startup_name=request.startup_data.startup_name,
            sector=request.startup_data.sector,
            funding_stage=request.startup_data.funding_stage,
            total_capital_raised_usd=request.startup_data.total_capital_raised_usd,
            cash_on_hand_usd=request.startup_data.cash_on_hand_usd,
            monthly_burn_usd=request.startup_data.monthly_burn_usd,
            runway_months=request.startup_data.runway_months,
            team_size_full_time=request.startup_data.team_size_full_time,
            market_size_usd=request.startup_data.market_size_usd,
            market_growth_rate_annual=request.startup_data.market_growth_rate_annual,
            competitor_count=request.startup_data.competitor_count,
            market_share_percentage=request.startup_data.market_share_percentage,
            annual_revenue_usd=request.startup_data.annual_revenue_usd or 0,
            customer_count=request.startup_data.customer_acquisition_cost_usd or 0,
            gross_margin=request.startup_data.gross_margin or 0,
            ltv_cac_ratio=10.0  # Calculate from LTV/CAC if needed
        )
        
        simple_request = SimpleAnalysisRequest(startup_data=simple_data)
        
        # Call the working endpoint directly
        result = await analyze_startup_working(simple_request)
        
        # Add a note that this is fallback data
        result["data_source"] = "fallback"
        result["note"] = "Using pre-computed analysis due to DeepSeek unavailability"
        
        return result

# Initialize engine
hybrid_engine = HybridMichelinEngine()

@hybrid_router.post("/analyze")
async def analyze_with_hybrid_engine(
    request: MichelinAnalysisRequest,
    background_tasks: BackgroundTasks
):
    """
    Hybrid Michelin analysis - uses DeepSeek when available, fallback otherwise
    """
    try:
        logger.info(f"Starting hybrid Michelin analysis for {request.startup_data.startup_name}")
        
        # Perform analysis
        result = await hybrid_engine.analyze_with_fallback(request)
        
        logger.info(f"Hybrid analysis completed for {request.startup_data.startup_name}")
        
        return result
        
    except Exception as e:
        logger.error(f"Hybrid analysis failed: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Analysis failed: {str(e)}"
        )

@hybrid_router.get("/status")
async def get_hybrid_status():
    """Check hybrid engine status"""
    deepseek_available = False
    
    try:
        # Test DeepSeek availability
        deepseek_available = await hybrid_engine._test_deepseek_availability()
    except:
        pass
    
    return {
        "engine": "hybrid",
        "deepseek_enabled": hybrid_engine.use_deepseek,
        "deepseek_available": deepseek_available,
        "fallback_ready": True,
        "recommendation": "DeepSeek available" if deepseek_available else "Using fallback mode"
    }

@hybrid_router.post("/toggle-deepseek")
async def toggle_deepseek_usage(enable: bool = True):
    """Enable or disable DeepSeek usage"""
    hybrid_engine.use_deepseek = enable
    return {
        "deepseek_enabled": hybrid_engine.use_deepseek,
        "message": f"DeepSeek {'enabled' if enable else 'disabled'}"
    }

# Export router
__all__ = ['hybrid_router']