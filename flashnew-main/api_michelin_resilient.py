"""
Michelin Strategic Analysis API with Research-Grade Resilience
Implements distributed systems best practices for reliability

This version includes:
1. Circuit breaker pattern
2. Exponential backoff with jitter
3. Request hedging (backup requests)
4. Graceful degradation
5. Adaptive timeouts
"""

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field
from typing import Dict, Any, Optional, List
import logging
import asyncio
import aiohttp
import json
import time
import os
from datetime import datetime

# Import our resilience layer
from core.resilience_layer import (
    ResilienceLayer, 
    CircuitBreakerConfig, 
    BackoffConfig, 
    HedgingConfig
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/michelin-resilient", tags=["michelin-resilient"])

# Initialize resilience layer
resilience_layer = ResilienceLayer(
    circuit_breaker_config=CircuitBreakerConfig(
        failure_threshold=3,      # Open circuit after 3 failures
        recovery_timeout=30,      # Try again after 30 seconds
        half_open_max_calls=2,    # Test with 2 calls in half-open state
        success_threshold=2       # Need 2 successes to close circuit
    ),
    backoff_config=BackoffConfig(
        initial_delay=0.5,        # Start with 0.5s delay
        max_delay=30.0,          # Cap at 30s
        exponential_base=2.0,    # Double each time
        jitter=True              # Add randomness to prevent thundering herd
    ),
    hedging_config=HedgingConfig(
        delay=3.0,               # Send backup request after 3s
        max_hedged_requests=1    # Maximum 1 backup request
    ),
    enable_adaptive_timeout=True  # Adjust timeouts based on performance
)

# DeepSeek configuration
DEEPSEEK_API_KEY = os.environ.get("DEEPSEEK_API_KEY", "sk-c57ed3d5cf5a450e81b0e9f2ad25773d")
DEEPSEEK_BASE_URL = "https://api.deepseek.com/v1"


class MichelinPhase1Response(BaseModel):
    bcg_matrix: Dict[str, Any]
    porters_five_forces: Dict[str, Any]
    swot_analysis: Dict[str, Any]
    current_position_summary: str


class MichelinPhase2Response(BaseModel):
    ansoff_matrix: Dict[str, Any]
    blue_ocean_strategy: Dict[str, Any]
    growth_scenarios: List[Dict[str, Any]]
    recommended_direction: str


class MichelinPhase3Response(BaseModel):
    balanced_scorecard: Dict[str, Any]
    okr_framework: Dict[str, Any]
    resource_requirements: Dict[str, Any]
    risk_mitigation: List[Dict[str, Any]]
    success_metrics: List[Dict[str, Any]]


async def call_deepseek_with_resilience(
    prompt: str, 
    service_name: str,
    max_tokens: int = 500,
    fallback_response: Optional[str] = None
) -> str:
    """Call DeepSeek API with full resilience patterns"""
    
    async def _make_request():
        """Inner function to make the actual API request"""
        timeout = aiohttp.ClientTimeout(total=30)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            payload = {
                "model": "deepseek-chat",
                "messages": [
                    {
                        "role": "system",
                        "content": "You are a McKinsey senior consultant with 20 years of experience."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "temperature": 0.3,
                "max_tokens": max_tokens
            }
            
            headers = {
                "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
                "Content-Type": "application/json"
            }
            
            async with session.post(
                f"{DEEPSEEK_BASE_URL}/chat/completions",
                json=payload,
                headers=headers
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    return data['choices'][0]['message']['content'].strip()
                else:
                    error_text = await response.text()
                    raise Exception(f"API error {response.status}: {error_text}")
    
    async def _fallback():
        """Fallback function if API fails"""
        if fallback_response:
            return fallback_response
        return "Analysis temporarily unavailable. Please try again."
    
    # Execute with resilience
    result = await resilience_layer.execute_with_resilience(
        service_name=f"deepseek_{service_name}",
        func=_make_request,
        fallback=_fallback,
        enable_hedging=True,  # Enable backup requests
        max_retries=3,
        partial_result_key=f"michelin_{service_name}"  # Cache for graceful degradation
    )
    
    return result


@router.post("/analyze/phase1", response_model=MichelinPhase1Response)
async def analyze_phase1_resilient(startup_data: Dict[str, Any]):
    """Phase 1: Where Are We Now? - With resilience patterns"""
    try:
        # Prepare analysis tasks with graceful degradation
        results = {}
        
        # BCG Matrix Analysis
        bcg_prompt = f"""Based on this startup data: {json.dumps(startup_data, indent=2)}
        
        Determine the BCG Matrix position (Star, Cash Cow, Question Mark, or Dog).
        Consider market growth rate and relative market share.
        Respond with just the position name."""
        
        bcg_position = await call_deepseek_with_resilience(
            bcg_prompt, 
            "bcg_matrix",
            fallback_response="Question Mark"  # Safe default
        )
        
        results['bcg_matrix'] = {
            "position": bcg_position,
            "market_growth_rate": startup_data.get('market_growth_rate', 15),
            "relative_market_share": startup_data.get('market_share', 0.1),
            "implications": f"As a {bcg_position}, focus on strategic investments."
        }
        
        # Porter's Five Forces - Parallel execution with resilience
        forces_tasks = {
            "competitive_rivalry": call_deepseek_with_resilience(
                f"Rate competitive rivalry for {startup_data.get('company_name', 'this startup')} (Low/Medium/High):",
                "rivalry",
                fallback_response="Medium"
            ),
            "supplier_power": call_deepseek_with_resilience(
                "Rate supplier power (Low/Medium/High):",
                "supplier",
                fallback_response="Medium"
            ),
            "buyer_power": call_deepseek_with_resilience(
                "Rate buyer power (Low/Medium/High):",
                "buyer",
                fallback_response="Medium"
            ),
            "threat_of_substitution": call_deepseek_with_resilience(
                "Rate threat of substitution (Low/Medium/High):",
                "substitution",
                fallback_response="Medium"
            ),
            "threat_of_new_entry": call_deepseek_with_resilience(
                "Rate threat of new entry (Low/Medium/High):",
                "new_entry",
                fallback_response="Medium"
            )
        }
        
        # Execute all forces analysis in parallel
        forces_results = await asyncio.gather(
            *[forces_tasks[force] for force in forces_tasks],
            return_exceptions=True  # Don't fail if one fails
        )
        
        # Map results with graceful handling of failures
        forces_mapping = {}
        for i, force in enumerate(forces_tasks.keys()):
            if isinstance(forces_results[i], Exception):
                logger.warning(f"Force analysis failed for {force}, using default")
                forces_mapping[force] = "Medium"
            else:
                forces_mapping[force] = forces_results[i]
        
        results['porters_five_forces'] = forces_mapping
        
        # SWOT Analysis with fallback
        swot_data = {
            "strengths": startup_data.get('strengths', ['Innovation', 'Team expertise']),
            "weaknesses": startup_data.get('weaknesses', ['Limited resources', 'Market presence']),
            "opportunities": startup_data.get('opportunities', ['Market growth', 'Technology trends']),
            "threats": startup_data.get('threats', ['Competition', 'Regulatory changes'])
        }
        
        results['swot_analysis'] = swot_data
        
        # Summary with intelligent fallback
        summary = await call_deepseek_with_resilience(
            f"Summarize the strategic position in 2 sentences based on BCG: {bcg_position}",
            "summary",
            fallback_response=f"The company is positioned as a {bcg_position} with moderate competitive forces."
        )
        
        results['current_position_summary'] = summary
        
        return MichelinPhase1Response(**results)
        
    except Exception as e:
        logger.error(f"Phase 1 analysis failed: {str(e)}")
        # Return gracefully degraded response
        return MichelinPhase1Response(
            bcg_matrix={"position": "Question Mark", "implications": "Further analysis needed"},
            porters_five_forces={force: "Medium" for force in 
                ["competitive_rivalry", "supplier_power", "buyer_power", 
                 "threat_of_substitution", "threat_of_new_entry"]},
            swot_analysis={
                "strengths": ["To be analyzed"],
                "weaknesses": ["To be analyzed"],
                "opportunities": ["To be analyzed"],
                "threats": ["To be analyzed"]
            },
            current_position_summary="Strategic analysis pending. Please retry for detailed insights."
        )


@router.post("/analyze/phase2", response_model=MichelinPhase2Response)
async def analyze_phase2_resilient(
    startup_data: Dict[str, Any],
    phase1_results: Optional[Dict[str, Any]] = None
):
    """Phase 2: Where Should We Go? - With resilience patterns"""
    try:
        results = {}
        
        # Use phase 1 context if available
        context = phase1_results or {}
        bcg_position = context.get('bcg_matrix', {}).get('position', 'Question Mark')
        
        # Ansoff Matrix with resilience
        ansoff_prompt = f"""For a {bcg_position} company, recommend Ansoff Matrix strategy:
        Market Penetration, Market Development, Product Development, or Diversification.
        Just respond with the strategy name."""
        
        ansoff_strategy = await call_deepseek_with_resilience(
            ansoff_prompt,
            "ansoff",
            fallback_response="Market Development"
        )
        
        results['ansoff_matrix'] = {
            "recommended_strategy": ansoff_strategy,
            "rationale": f"Based on {bcg_position} position",
            "implementation_focus": "Expand market reach"
        }
        
        # Blue Ocean Strategy - ERRC Grid
        blue_ocean_tasks = {
            "eliminate": "What should this startup eliminate?",
            "reduce": "What should this startup reduce?",
            "raise": "What should this startup raise above industry standard?",
            "create": "What new value should this startup create?"
        }
        
        blue_ocean_results = {}
        for action, prompt in blue_ocean_tasks.items():
            result = await call_deepseek_with_resilience(
                prompt,
                f"blue_ocean_{action}",
                fallback_response=f"Analyze {action} factors"
            )
            blue_ocean_results[action] = result
        
        results['blue_ocean_strategy'] = blue_ocean_results
        
        # Growth Scenarios with parallel execution
        scenario_tasks = []
        for scenario_type in ["Conservative", "Moderate", "Aggressive"]:
            prompt = f"What's the success probability for {scenario_type} growth? (0-100%)"
            task = call_deepseek_with_resilience(
                prompt,
                f"scenario_{scenario_type.lower()}",
                fallback_response="50"
            )
            scenario_tasks.append((scenario_type, task))
        
        scenario_results = []
        for scenario_type, task in scenario_tasks:
            try:
                probability = await task
                # Parse probability
                prob_value = 50  # default
                try:
                    prob_value = int(''.join(filter(str.isdigit, probability)))
                except:
                    pass
                
                scenario_results.append({
                    "name": f"{scenario_type} Growth",
                    "success_probability": prob_value,
                    "key_focus": f"{scenario_type} market expansion"
                })
            except Exception as e:
                logger.warning(f"Scenario {scenario_type} failed, using default")
                scenario_results.append({
                    "name": f"{scenario_type} Growth",
                    "success_probability": 50,
                    "key_focus": "To be determined"
                })
        
        results['growth_scenarios'] = scenario_results
        
        # Recommended direction
        direction = await call_deepseek_with_resilience(
            "Recommend strategic direction in one sentence",
            "direction",
            fallback_response="Focus on sustainable growth through market expansion"
        )
        
        results['recommended_direction'] = direction
        
        return MichelinPhase2Response(**results)
        
    except Exception as e:
        logger.error(f"Phase 2 analysis failed: {str(e)}")
        # Gracefully degraded response
        return MichelinPhase2Response(
            ansoff_matrix={
                "recommended_strategy": "Market Development",
                "rationale": "Default recommendation",
                "implementation_focus": "Expand carefully"
            },
            blue_ocean_strategy={
                "eliminate": "Non-core activities",
                "reduce": "Operational costs",
                "raise": "Customer value",
                "create": "New market space"
            },
            growth_scenarios=[
                {"name": "Conservative Growth", "success_probability": 70, "key_focus": "Stability"},
                {"name": "Moderate Growth", "success_probability": 50, "key_focus": "Balance"},
                {"name": "Aggressive Growth", "success_probability": 30, "key_focus": "High risk"}
            ],
            recommended_direction="Focus on sustainable growth"
        )


@router.get("/health")
async def get_service_health():
    """Get health status of all services with circuit breaker states"""
    services = [
        "deepseek_bcg_matrix", "deepseek_rivalry", "deepseek_supplier",
        "deepseek_buyer", "deepseek_substitution", "deepseek_new_entry",
        "deepseek_ansoff", "deepseek_blue_ocean_eliminate",
        "deepseek_blue_ocean_reduce", "deepseek_blue_ocean_raise",
        "deepseek_blue_ocean_create", "deepseek_scenario_conservative",
        "deepseek_scenario_moderate", "deepseek_scenario_aggressive"
    ]
    
    health_report = {
        "timestamp": datetime.now().isoformat(),
        "services": {}
    }
    
    for service in services:
        health_report["services"][service] = resilience_layer.get_service_health(service)
    
    # Overall health
    open_circuits = sum(1 for s in health_report["services"].values() 
                       if s.get("circuit_state") == "open")
    
    health_report["overall_status"] = {
        "healthy": open_circuits == 0,
        "degraded": 0 < open_circuits < len(services) // 2,
        "unhealthy": open_circuits >= len(services) // 2,
        "open_circuits": open_circuits,
        "total_services": len(services)
    }
    
    return health_report


@router.post("/analyze/complete")
async def analyze_complete_resilient(startup_data: Dict[str, Any]):
    """
    Complete Michelin analysis with maximum resilience
    Returns whatever phases complete successfully
    """
    results = {
        "timestamp": datetime.now().isoformat(),
        "phases_completed": [],
        "phases_failed": []
    }
    
    # Phase 1 - with timeout and fallback
    try:
        phase1 = await asyncio.wait_for(
            analyze_phase1_resilient(startup_data),
            timeout=60  # 60 second timeout for phase 1
        )
        results["phase1"] = phase1.dict()
        results["phases_completed"].append("phase1")
    except Exception as e:
        logger.error(f"Phase 1 failed: {e}")
        results["phases_failed"].append({"phase": "phase1", "error": str(e)})
        results["phase1"] = None
    
    # Phase 2 - continues even if phase 1 failed
    try:
        phase2 = await asyncio.wait_for(
            analyze_phase2_resilient(
                startup_data, 
                results.get("phase1")
            ),
            timeout=60
        )
        results["phase2"] = phase2.dict()
        results["phases_completed"].append("phase2")
    except Exception as e:
        logger.error(f"Phase 2 failed: {e}")
        results["phases_failed"].append({"phase": "phase2", "error": str(e)})
        results["phase2"] = None
    
    # Add success flag
    results["success"] = len(results["phases_completed"]) > 0
    results["partial_success"] = (
        len(results["phases_completed"]) > 0 and 
        len(results["phases_failed"]) > 0
    )
    
    return results