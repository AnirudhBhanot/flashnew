#!/usr/bin/env python3
"""
Debug version of decomposed Michelin Analysis with enhanced logging
"""

import os
import json
import logging
import asyncio
import re
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
import aiohttp
from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel, Field
from tenacity import retry, stop_after_attempt, wait_exponential
import traceback

# Import models from the original file
from api_michelin_llm_analysis import (
    StartupData,
    MichelinAnalysisRequest,
    Phase1Analysis,
    Phase2Analysis,
    Phase3Analysis,
    MichelinAnalysisResponse,
    Phase1Response,
    Phase2Response,
    Phase3Response,
    Phase2Request,
    Phase3Request
)

# Setup enhanced logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configuration
DEEPSEEK_API_KEY = "sk-f68b7148243e4663a31386a5ea6093cf"
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"

# Create router
decomposed_debug_router = APIRouter(prefix="/api/michelin/decomposed-debug", tags=["Michelin Decomposed Debug"])

class DecomposedMichelinEngineDebug:
    """Debug version of decomposed Michelin engine with enhanced logging"""
    
    def __init__(self):
        self.api_key = DEEPSEEK_API_KEY
        self.session = None
        logger.info("Initialized DecomposedMichelinEngineDebug")
        
    async def _ensure_session(self):
        """Ensure aiohttp session exists"""
        if self.session is None:
            self.session = aiohttp.ClientSession()
            logger.debug("Created new aiohttp session")
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    async def _call_deepseek(self, prompt: str, max_tokens: int = 500) -> str:
        """Call DeepSeek API with simple prompt"""
        logger.debug(f"Calling DeepSeek with prompt length: {len(prompt)} chars")
        await self._ensure_session()
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "deepseek-chat",
            "messages": [
                {"role": "system", "content": "You are a McKinsey senior consultant. Answer concisely and specifically."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.3,
            "max_tokens": max_tokens,
            "top_p": 0.9
        }
        
        try:
            logger.debug("Sending request to DeepSeek API...")
            start_time = datetime.now()
            
            async with self.session.post(
                DEEPSEEK_API_URL, 
                json=payload, 
                headers=headers,
                timeout=aiohttp.ClientTimeout(total=60)  # 60 second timeout
            ) as response:
                elapsed = (datetime.now() - start_time).total_seconds()
                logger.debug(f"DeepSeek response received in {elapsed:.2f}s - Status: {response.status}")
                
                if response.status != 200:
                    error_text = await response.text()
                    logger.error(f"DeepSeek API error: {response.status} - {error_text}")
                    raise Exception(f"DeepSeek API error: {response.status}")
                
                result = await response.json()
                content = result['choices'][0]['message']['content']
                logger.debug(f"DeepSeek response: {content[:200]}...")
                return content.strip()
                
        except asyncio.TimeoutError:
            logger.error("DeepSeek API request timed out after 60 seconds")
            raise
        except Exception as e:
            logger.error(f"DeepSeek API call failed: {type(e).__name__}: {e}")
            raise
    
    # Simplified Phase 2 methods for debugging
    async def get_ansoff_position_simple(self, data: StartupData) -> Dict[str, Any]:
        """Simplified Ansoff Matrix recommendation"""
        logger.debug("Getting Ansoff position (simplified)")
        
        # Simple logic without API call
        if data.market_share_percentage < 1:
            strategy = "Market Penetration"
            rationale = "Low market share requires focus on existing market first"
        else:
            strategy = "Product Development"
            rationale = "Strong position allows for product expansion"
        
        return {
            "recommended_strategy": strategy,
            "rationale": rationale,
            "implementation_approach": f"Focus on {strategy.lower()} to maximize growth"
        }
    
    async def analyze_blue_ocean_simple(self, data: StartupData) -> Dict[str, Any]:
        """Simplified Blue Ocean analysis"""
        logger.debug("Analyzing Blue Ocean opportunities (simplified)")
        
        return {
            "opportunities": [
                {
                    "opportunity": "Target underserved SMB segment",
                    "approach": f"Focus on businesses with 10-50 employees in {data.sector}"
                },
                {
                    "opportunity": "Create integrated solution",
                    "approach": "Combine fragmented tools into single platform"
                }
            ],
            "value_innovation_potential": "High" if data.proprietary_tech else "Medium"
        }
    
    async def create_growth_scenarios_simple(self, data: StartupData) -> List[Dict[str, Any]]:
        """Simplified growth scenarios"""
        logger.debug("Creating growth scenarios (simplified)")
        
        base_revenue = data.annual_revenue_usd or 100000
        
        return [
            {
                "scenario_name": "Conservative",
                "12_month_revenue_projection": int(base_revenue * 1.5),
                "key_assumptions": ["15% MoM growth", "Current burn rate maintained"],
                "required_resources": f"${data.monthly_burn_usd * 12:,.0f}"
            },
            {
                "scenario_name": "Base",
                "12_month_revenue_projection": int(base_revenue * 2),
                "key_assumptions": ["25% MoM growth", "Moderate hiring"],
                "required_resources": f"${data.monthly_burn_usd * 15:,.0f}"
            },
            {
                "scenario_name": "Aggressive",
                "12_month_revenue_projection": int(base_revenue * 3),
                "key_assumptions": ["40% MoM growth", "Significant expansion"],
                "required_resources": f"${data.monthly_burn_usd * 24:,.0f}"
            }
        ]
    
    async def analyze_phase2_debug(self, startup_data: StartupData, phase1_data: Dict[str, Any]) -> Dict[str, Any]:
        """Debug version of Phase 2 analysis"""
        try:
            logger.info(f"Starting DEBUG Phase 2 analysis for {startup_data.startup_name}")
            
            # Extract BCG position from phase1
            bcg_position = phase1_data.get("bcg_matrix_analysis", {}).get("position", "Question Mark")
            logger.debug(f"BCG Position: {bcg_position}")
            
            # Use simplified methods to avoid API timeouts
            logger.debug("Step 1: Ansoff Matrix Analysis")
            ansoff_analysis = await self.get_ansoff_position_simple(startup_data)
            
            logger.debug("Step 2: Blue Ocean Strategy")
            blue_ocean = await self.analyze_blue_ocean_simple(startup_data)
            
            logger.debug("Step 3: Growth Scenarios")
            growth_scenarios = await self.create_growth_scenarios_simple(startup_data)
            
            logger.debug("Step 4: Creating strategic recommendation")
            recommended_direction = (
                f"{startup_data.startup_name} should pursue {ansoff_analysis['recommended_strategy']} "
                f"to maximize growth potential. With {len(blue_ocean['opportunities'])} Blue Ocean "
                f"opportunities identified, focus on execution excellence while maintaining capital efficiency."
            )
            
            # Build Phase 2 response
            phase2_data = {
                "strategic_options_overview": (
                    f"Based on {startup_data.startup_name}'s position as a {bcg_position}, "
                    f"we recommend {ansoff_analysis['recommended_strategy']} as the primary growth strategy."
                ),
                "ansoff_matrix_analysis": ansoff_analysis,
                "blue_ocean_strategy": blue_ocean,
                "growth_scenarios": growth_scenarios,
                "recommended_direction": recommended_direction
            }
            
            logger.info("DEBUG Phase 2 analysis completed successfully")
            return phase2_data
            
        except Exception as e:
            logger.error(f"DEBUG Phase 2 analysis failed: {e}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            raise
    
    async def close(self):
        """Close the aiohttp session"""
        if self.session:
            await self.session.close()
            logger.debug("Closed aiohttp session")

# Initialize debug engine
debug_engine = None

def get_debug_engine() -> DecomposedMichelinEngineDebug:
    """Get or create debug engine instance"""
    global debug_engine
    if debug_engine is None:
        debug_engine = DecomposedMichelinEngineDebug()
    return debug_engine

# Debug endpoint
@decomposed_debug_router.post("/analyze/phase2", response_model=Phase2Response)
async def analyze_phase2_debug(
    request: Phase2Request,
    background_tasks: BackgroundTasks
):
    """
    Debug endpoint for Phase 2 analysis
    Uses simplified logic to avoid timeouts
    """
    engine = get_debug_engine()
    
    try:
        logger.info(f"DEBUG endpoint: Starting Phase 2 for {request.startup_data.startup_name}")
        
        # Convert Phase1Analysis to dict
        phase1_dict = request.phase1_results.model_dump()
        
        # Perform debug Phase 2 analysis
        phase2_data = await engine.analyze_phase2_debug(request.startup_data, phase1_dict)
        
        # Construct response
        response = Phase2Response(
            startup_name=request.startup_data.startup_name,
            analysis_date=datetime.now().isoformat(),
            phase2=Phase2Analysis(
                strategic_options_overview=phase2_data["strategic_options_overview"],
                ansoff_matrix_analysis=phase2_data["ansoff_matrix_analysis"],
                blue_ocean_strategy=phase2_data["blue_ocean_strategy"],
                growth_scenarios=phase2_data["growth_scenarios"],
                recommended_direction=phase2_data["recommended_direction"]
            )
        )
        
        logger.info("DEBUG endpoint: Phase 2 response created successfully")
        return response
        
    except Exception as e:
        logger.error(f"DEBUG endpoint failed: {e}")
        logger.error(f"Full traceback: {traceback.format_exc()}")
        raise HTTPException(
            status_code=500,
            detail=f"Phase 2 debug analysis failed: {str(e)}"
        )

# Cleanup function
async def shutdown_debug_engine():
    """Shutdown the debug engine"""
    global debug_engine
    if debug_engine:
        await debug_engine.close()
        debug_engine = None

if __name__ == "__main__":
    # Test the debug engine directly
    import uvicorn
    from fastapi import FastAPI
    
    app = FastAPI()
    app.include_router(decomposed_debug_router)
    
    @app.on_event("shutdown")
    async def shutdown_event():
        await shutdown_debug_engine()
    
    uvicorn.run(app, host="0.0.0.0", port=8002)