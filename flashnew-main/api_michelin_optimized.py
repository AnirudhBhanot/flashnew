#!/usr/bin/env python3
"""
Optimized Michelin Analysis with DeepSeek
- Breaks analysis into smaller chunks
- Implements caching
- Provides fallback for timeouts
"""

import os
import json
import logging
import asyncio
from typing import Dict, List, Optional, Any
from datetime import datetime
from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel, Field
import hashlib

# Import the original components
from api_michelin_llm_analysis import (
    MichelinAnalysisEngine,
    StartupData,
    MichelinAnalysisRequest
)

# Import components for fallback generation
from api_michelin_working import working_engine

# Simple in-memory cache
from simple_cache import SimpleCache

logger = logging.getLogger(__name__)

# Create router
optimized_router = APIRouter(prefix="/api/michelin", tags=["Michelin Optimized"])

# Initialize cache with 1 hour TTL
analysis_cache = SimpleCache(ttl=3600)

class OptimizedMichelinEngine:
    """Optimized engine that handles timeouts and caching"""
    
    def __init__(self):
        self.engine = MichelinAnalysisEngine()
        self.timeout_seconds = 30  # Shorter timeout per phase
        
    def _get_cache_key(self, startup_data: Dict, phase: str) -> str:
        """Generate cache key for a specific phase"""
        # Create a deterministic key from startup data
        data_str = json.dumps(startup_data, sort_keys=True)
        data_hash = hashlib.md5(data_str.encode()).hexdigest()
        return f"michelin:{phase}:{data_hash}"
    
    async def analyze_phase_with_timeout(self, phase: str, prompt: str) -> Optional[Dict]:
        """Analyze a single phase with timeout protection"""
        try:
            # Call DeepSeek with timeout
            result = await asyncio.wait_for(
                self.engine._call_deepseek([
                    {"role": "system", "content": "You are a senior McKinsey consultant. Provide a concise analysis."},
                    {"role": "user", "content": prompt}
                ], max_tokens=2000),  # Reduced tokens per phase
                timeout=self.timeout_seconds
            )
            
            # Extract JSON from response
            return self.engine._extract_json_from_response(result)
            
        except asyncio.TimeoutError:
            logger.warning(f"Phase {phase} timed out after {self.timeout_seconds}s")
            return None
        except Exception as e:
            logger.error(f"Phase {phase} failed: {str(e)}")
            return None
    
    async def analyze_startup_optimized(self, startup_data: StartupData) -> Dict:
        """Perform optimized analysis with caching and fallback"""
        startup_dict = startup_data.model_dump()
        
        # Check if we have a complete cached analysis
        complete_cache_key = self._get_cache_key(startup_dict, "complete")
        cached_complete = analysis_cache.get(complete_cache_key)
        if cached_complete:
            logger.info("Returning complete cached analysis")
            return cached_complete
        
        # Initialize result structure
        result = {
            "startup_name": startup_data.startup_name,
            "analysis_date": datetime.now().isoformat(),
            "executive_briefing": f"Strategic analysis for {startup_data.startup_name}",
            "phase1": {},
            "phase2": {},
            "phase3": {},
            "key_recommendations": [],
            "critical_success_factors": [],
            "next_steps": []
        }
        
        # Try to get each phase with caching
        phases_completed = 0
        
        # Phase 1: Current State (BCG, Porter's, SWOT)
        phase1_cache_key = self._get_cache_key(startup_dict, "phase1")
        phase1_data = analysis_cache.get(phase1_cache_key)
        
        if not phase1_data:
            logger.info("Analyzing Phase 1...")
            phase1_prompt = self._create_simplified_phase1_prompt(startup_data)
            phase1_data = await self.analyze_phase_with_timeout("phase1", phase1_prompt)
            
            if phase1_data:
                analysis_cache.set(phase1_cache_key, phase1_data)
                phases_completed += 1
        else:
            logger.info("Using cached Phase 1")
            phases_completed += 1
        
        if phase1_data:
            result["phase1"] = self._transform_phase1_data(phase1_data, startup_data)
        
        # Phase 2: Strategic Options (Ansoff, Blue Ocean)
        phase2_cache_key = self._get_cache_key(startup_dict, "phase2")
        phase2_data = analysis_cache.get(phase2_cache_key)
        
        if not phase2_data:
            logger.info("Analyzing Phase 2...")
            phase2_prompt = self._create_simplified_phase2_prompt(startup_data)
            phase2_data = await self.analyze_phase_with_timeout("phase2", phase2_prompt)
            
            if phase2_data:
                analysis_cache.set(phase2_cache_key, phase2_data)
                phases_completed += 1
        else:
            logger.info("Using cached Phase 2")
            phases_completed += 1
        
        if phase2_data:
            result["phase2"] = self._transform_phase2_data(phase2_data, startup_data)
        
        # Phase 3: Implementation (Balanced Scorecard, OKRs)
        phase3_cache_key = self._get_cache_key(startup_dict, "phase3")
        phase3_data = analysis_cache.get(phase3_cache_key)
        
        if not phase3_data:
            logger.info("Analyzing Phase 3...")
            phase3_prompt = self._create_simplified_phase3_prompt(startup_data)
            phase3_data = await self.analyze_phase_with_timeout("phase3", phase3_prompt)
            
            if phase3_data:
                analysis_cache.set(phase3_cache_key, phase3_data)
                phases_completed += 1
        else:
            logger.info("Using cached Phase 3")
            phases_completed += 1
        
        if phase3_data:
            result["phase3"] = self._transform_phase3_data(phase3_data, startup_data)
        
        # If we got at least 2 phases, generate synthesis
        if phases_completed >= 2:
            # Generate executive briefing and recommendations
            result["executive_briefing"] = self._generate_executive_briefing(
                startup_data, result["phase1"], result["phase2"], result["phase3"]
            )
            result["key_recommendations"] = self._generate_recommendations(
                startup_data, result["phase1"], result["phase2"], result["phase3"]
            )
            result["critical_success_factors"] = self._generate_success_factors(startup_data)
            result["next_steps"] = self._generate_next_steps()
            
            # Cache the complete result
            analysis_cache.set(complete_cache_key, result)
            
            return result
        else:
            # If DeepSeek failed, use fallback
            logger.warning("Insufficient DeepSeek responses, using fallback")
            return working_engine.generate_michelin_analysis(startup_data)
    
    def _create_simplified_phase1_prompt(self, startup_data: StartupData) -> str:
        """Create a simplified Phase 1 prompt that's faster to process"""
        return f"""Analyze {startup_data.startup_name} (a {startup_data.funding_stage} {startup_data.sector} startup) current position.

Key metrics:
- Capital: ${startup_data.total_capital_raised_usd:,.0f} raised, ${startup_data.cash_on_hand_usd:,.0f} cash
- Market: ${startup_data.market_size_usd:,.0f} TAM, {startup_data.market_growth_rate_annual}% growth
- Team: {startup_data.team_size_full_time} people

Provide a CONCISE analysis in JSON format:
{{
  "bcg_position": "Star/Cash Cow/Question Mark/Dog",
  "key_strengths": ["strength1", "strength2", "strength3"],
  "key_weaknesses": ["weakness1", "weakness2", "weakness3"],
  "market_position": "Brief market position analysis",
  "competitive_threats": ["threat1", "threat2"]
}}"""

    def _create_simplified_phase2_prompt(self, startup_data: StartupData) -> str:
        """Create a simplified Phase 2 prompt"""
        return f"""Recommend growth strategies for {startup_data.startup_name}.

Provide 3 strategic options in JSON format:
{{
  "primary_strategy": {{
    "name": "Strategy name",
    "description": "Brief description",
    "investment": 1000000,
    "timeline": "6-12 months",
    "success_probability": 70
  }},
  "alternative_strategies": [
    {{"name": "Alt 1", "description": "Brief", "investment": 500000}},
    {{"name": "Alt 2", "description": "Brief", "investment": 2000000}}
  ],
  "recommended_focus": "Market penetration/Product development/Market development/Diversification"
}}"""

    def _create_simplified_phase3_prompt(self, startup_data: StartupData) -> str:
        """Create a simplified Phase 3 prompt"""
        return f"""Create an implementation plan for {startup_data.startup_name}.

Provide a CONCISE plan in JSON format:
{{
  "q1_objectives": [
    {{"objective": "Objective 1", "key_result": "Measurable outcome"}},
    {{"objective": "Objective 2", "key_result": "Measurable outcome"}}
  ],
  "resource_needs": {{
    "headcount": 10,
    "funding": 2000000,
    "key_hires": ["VP Sales", "Senior Engineers"]
  }},
  "success_metrics": [
    {{"metric": "ARR", "target": "$1M", "timeline": "12 months"}},
    {{"metric": "Customer Count", "target": "100", "timeline": "6 months"}}
  ],
  "top_risks": ["Risk 1", "Risk 2", "Risk 3"]
}}"""

    def _transform_phase1_data(self, data: Dict, startup_data: StartupData) -> Dict:
        """Transform Phase 1 data to frontend format"""
        return {
            "executive_summary": f"{startup_data.startup_name} is positioned as a {data.get('bcg_position', 'Question Mark')} in the market",
            "bcg_matrix": {
                "position": data.get("bcg_position", "Question Mark"),
                "market_growth": startup_data.market_growth_rate_annual,
                "relative_market_share": startup_data.market_share_percentage,
                "strategic_implications": [
                    data.get("market_position", "Growing market presence"),
                    "Focus on customer acquisition",
                    "Build competitive advantages"
                ],
                "action_items": ["Accelerate growth", "Optimize burn rate", "Strengthen team"]
            },
            "porters_five_forces": {
                "threat_of_new_entrants": {
                    "intensity": "Medium",
                    "score": 3,
                    "factors": ["Low barriers", "VC funding available", "Growing market"]
                },
                "supplier_power": {
                    "intensity": "Low",
                    "score": 2,
                    "factors": ["Multiple options", "Cloud infrastructure", "Commoditized"]
                },
                "buyer_power": {
                    "intensity": "Medium",
                    "score": 3,
                    "factors": ["Price sensitivity", "Switching costs", "Alternatives"]
                },
                "threat_of_substitutes": {
                    "intensity": "Medium",
                    "score": 3,
                    "factors": data.get("competitive_threats", ["DIY solutions", "Incumbents"])
                },
                "competitive_rivalry": {
                    "intensity": "High",
                    "score": 4,
                    "factors": [f"{startup_data.competitor_count} competitors", "Feature parity", "Price competition"]
                },
                "overall_industry_attractiveness": "Medium",
                "key_strategic_imperatives": ["Build moats", "Scale quickly", "Differentiate"]
            },
            "swot_analysis": {
                "strengths": [
                    {"item": s, "evidence": "Strong capability"} 
                    for s in data.get("key_strengths", ["Team", "Technology", "Traction"])
                ],
                "weaknesses": [
                    {"item": w, "impact": "Needs improvement"} 
                    for w in data.get("key_weaknesses", ["Limited resources", "Market share", "Brand"])
                ],
                "opportunities": [
                    {"item": "Market growth", "potential": f"{startup_data.market_growth_rate_annual}% annual growth"},
                    {"item": "Expansion", "potential": "Adjacent markets"},
                    {"item": "Partnerships", "potential": "Strategic alliances"}
                ],
                "threats": [
                    {"item": t, "mitigation": "Strategic response needed"} 
                    for t in data.get("competitive_threats", ["Competition", "Market dynamics"])
                ],
                "strategic_priorities": [
                    "Achieve product-market fit",
                    "Extend runway",
                    "Build competitive advantages",
                    "Scale customer acquisition",
                    "Strengthen team"
                ]
            },
            "current_position_narrative": data.get("market_position", f"{startup_data.startup_name} is well-positioned in a growing market")
        }

    def _transform_phase2_data(self, data: Dict, startup_data: StartupData) -> Dict:
        """Transform Phase 2 data to frontend format"""
        primary = data.get("primary_strategy", {})
        alts = data.get("alternative_strategies", [])
        
        return {
            "strategic_options_overview": f"Three strategic paths for {startup_data.startup_name}",
            "ansoff_matrix": {
                "market_penetration": {
                    "strategy": "Deepen current market presence",
                    "initiatives": ["Increase sales", "Improve retention", "Optimize pricing"],
                    "investment": primary.get("investment", 1000000) if data.get("recommended_focus") == "Market penetration" else 500000,
                    "timeline": "6-12 months"
                },
                "market_development": {
                    "strategy": "Expand to new markets",
                    "initiatives": ["Geographic expansion", "New segments", "Partnerships"],
                    "investment": primary.get("investment", 2000000) if data.get("recommended_focus") == "Market development" else 1000000,
                    "timeline": "12-18 months"
                },
                "product_development": {
                    "strategy": "Build new products",
                    "initiatives": ["Feature expansion", "Platform capabilities", "APIs"],
                    "investment": primary.get("investment", 1500000) if data.get("recommended_focus") == "Product development" else 750000,
                    "timeline": "9-15 months"
                },
                "diversification": {
                    "strategy": "New products for new markets",
                    "initiatives": ["Adjacent products", "M&A", "New models"],
                    "investment": 5000000,
                    "timeline": "18-24 months"
                },
                "recommended_strategy": data.get("recommended_focus", "Market Penetration"),
                "implementation_priorities": ["Focus on core", "Validate assumptions", "Measure progress", "Stay lean"]
            },
            "blue_ocean_strategy": {
                "eliminate_factors": ["Complexity", "Long cycles", "High costs"],
                "reduce_factors": ["Implementation time", "Training needs", "Support burden"],
                "raise_factors": ["User experience", "Value delivery", "Automation"],
                "create_factors": ["New category", "Unique value", "Network effects"],
                "value_innovation_opportunities": [
                    {"opportunity": "Self-service model", "impact": "Lower CAC"},
                    {"opportunity": "Platform play", "impact": "Network effects"},
                    {"opportunity": "AI automation", "impact": "Higher margins"}
                ],
                "new_market_spaces": ["Underserved SMBs", "International markets", "Adjacent verticals"]
            },
            "growth_scenarios": [
                {
                    "name": primary.get("name", "Primary Strategy"),
                    "description": primary.get("description", "Recommended path forward"),
                    "investment_required": primary.get("investment", 2000000),
                    "revenue_projection_3yr": primary.get("investment", 2000000) * 10,
                    "team_size_projection": 50,
                    "probability_of_success": primary.get("success_probability", 65),
                    "key_milestones": ["Q1: Foundation", "Q2: Launch", "Q3: Scale"],
                    "risks": ["Execution risk", "Market timing", "Competition"]
                },
                {
                    "name": alts[0].get("name", "Conservative") if alts else "Conservative Growth",
                    "description": alts[0].get("description", "Lower risk approach") if alts else "Steady growth",
                    "investment_required": alts[0].get("investment", 1000000) if alts else 1000000,
                    "revenue_projection_3yr": 5000000,
                    "team_size_projection": 30,
                    "probability_of_success": 80,
                    "key_milestones": ["Gradual expansion", "Profitability focus", "Sustainable growth"],
                    "risks": ["Slow growth", "Market share loss"]
                },
                {
                    "name": alts[1].get("name", "Aggressive") if len(alts) > 1 else "Aggressive Growth",
                    "description": alts[1].get("description", "High growth strategy") if len(alts) > 1 else "Rapid expansion",
                    "investment_required": alts[1].get("investment", 5000000) if len(alts) > 1 else 5000000,
                    "revenue_projection_3yr": 50000000,
                    "team_size_projection": 150,
                    "probability_of_success": 45,
                    "key_milestones": ["Rapid scaling", "Market leadership", "IPO preparation"],
                    "risks": ["High burn", "Integration complexity", "Market risk"]
                }
            ],
            "recommended_direction": primary.get("description", f"Focus on {data.get('recommended_focus', 'market penetration')} to maximize growth potential")
        }

    def _transform_phase3_data(self, data: Dict, startup_data: StartupData) -> Dict:
        """Transform Phase 3 data to frontend format"""
        resources = data.get("resource_needs", {})
        objectives = data.get("q1_objectives", [])
        
        return {
            "implementation_roadmap_summary": "18-month strategic implementation plan",
            "balanced_scorecard": [
                {
                    "perspective": "Financial",
                    "objectives": ["Revenue growth", "Capital efficiency"],
                    "measures": ["ARR", "Burn multiple"],
                    "targets": ["$5M ARR", "<1.5x burn"],
                    "initiatives": ["Sales acceleration", "Cost optimization"]
                },
                {
                    "perspective": "Customer",
                    "objectives": ["Customer satisfaction", "Market share"],
                    "measures": ["NPS", "Market share %"],
                    "targets": [">50 NPS", "5% share"],
                    "initiatives": ["Success program", "Product improvements"]
                },
                {
                    "perspective": "Internal Process",
                    "objectives": ["Operational efficiency", "Product velocity"],
                    "measures": ["Cycle time", "Deploy frequency"],
                    "targets": ["2-week cycles", "Daily deploys"],
                    "initiatives": ["Agile transformation", "CI/CD pipeline"]
                },
                {
                    "perspective": "Learning & Growth",
                    "objectives": ["Team capability", "Innovation"],
                    "measures": ["Skill coverage", "New features"],
                    "targets": ["100% coverage", "10 features/quarter"],
                    "initiatives": ["Training program", "Innovation time"]
                }
            ],
            "okr_framework": [
                {
                    "quarter": "Q1 2024",
                    "objectives": [
                        {
                            "objective": obj.get("objective", "Achieve product-market fit") if len(objectives) > 0 else "Achieve product-market fit",
                            "key_results": [
                                {"kr": obj.get("key_result", "50 customer interviews"), "current": "10", "target": "50"},
                                {"kr": "NPS > 50", "current": "30", "target": "50"},
                                {"kr": "$100K MRR", "current": "$25K", "target": "$100K"}
                            ]
                        }
                    ]
                },
                {
                    "quarter": "Q2 2024",
                    "objectives": [
                        {
                            "objective": "Scale go-to-market",
                            "key_results": [
                                {"kr": "Hire 5 sales reps", "current": "0", "target": "5"},
                                {"kr": "Launch in 3 new markets", "current": "1", "target": "4"},
                                {"kr": "$250K MRR", "current": "$100K", "target": "$250K"}
                            ]
                        }
                    ]
                }
            ],
            "execution_plan": {
                "phase1_foundation": {
                    "timeline": "Months 1-6",
                    "focus": "Product-market fit and team building",
                    "key_activities": ["Customer development", "Product iteration", "Core hires"],
                    "success_criteria": ["PMF validated", f"Team of {resources.get('headcount', 20)}", "$50K MRR"]
                },
                "phase2_growth": {
                    "timeline": "Months 7-12",
                    "focus": "Scaling go-to-market",
                    "key_activities": ["Sales team", "Marketing launch", "Partnerships"],
                    "success_criteria": ["$250K MRR", "100 customers", "Series A ready"]
                },
                "phase3_expansion": {
                    "timeline": "Months 13-18",
                    "focus": "Market expansion",
                    "key_activities": ["New products", "New markets", "Strategic initiatives"],
                    "success_criteria": ["$1M MRR", "Market leader", "Sustainable growth"]
                }
            },
            "resource_requirements": {
                "human_resources": [
                    {"role": hire, "level": "Senior", "timeline": "Q1 2024", "cost": 200000}
                    for hire in resources.get("key_hires", ["VP Sales", "Senior Engineers"])
                ],
                "financial_resources": {
                    "total_capital_needed": resources.get("funding", 5000000),
                    "runway_extension": 18,
                    "monthly_burn_target": resources.get("funding", 5000000) / 18
                },
                "technology_resources": [
                    "Cloud infrastructure scaling",
                    "Security compliance",
                    "Data analytics platform",
                    "DevOps automation"
                ],
                "partnership_resources": [
                    "Channel partners",
                    "Technology integrations",
                    "Strategic alliances",
                    "Advisory board"
                ]
            },
            "risk_mitigation_plan": [
                {
                    "risk": risk,
                    "impact": "High",
                    "likelihood": "Medium",
                    "mitigation_strategy": "Proactive monitoring and response",
                    "contingency_plan": "Pivot strategy if needed"
                }
                for risk in data.get("top_risks", ["Talent acquisition", "Competition", "Market timing"])
            ],
            "success_metrics": [
                {
                    "metric": m.get("metric", "Revenue"),
                    "type": "Lagging",
                    "target": m.get("target", "$1M"),
                    "frequency": "Monthly"
                }
                for m in data.get("success_metrics", [])
            ]
        }
    
    def _generate_executive_briefing(self, startup_data: StartupData, phase1: Dict, phase2: Dict, phase3: Dict) -> str:
        """Generate executive briefing"""
        return f"""{startup_data.startup_name} is a {startup_data.funding_stage} {startup_data.sector} startup positioned as a {phase1.get('bcg_matrix', {}).get('position', 'Question Mark')} with significant growth potential in a ${startup_data.market_size_usd/1e9:.1f}B market growing at {startup_data.market_growth_rate_annual}% annually.

With ${startup_data.cash_on_hand_usd:,.0f} in cash providing {startup_data.runway_months} months of runway, the company must execute efficiently to capture market share and achieve sustainable growth. The recommended strategy focuses on {phase2.get('ansoff_matrix', {}).get('recommended_strategy', 'market penetration')} to maximize capital efficiency while building competitive advantages.

Success will require disciplined execution across product development, go-to-market, and team building, with clear milestones and metrics to track progress."""
    
    def _generate_recommendations(self, startup_data: StartupData, phase1: Dict, phase2: Dict, phase3: Dict) -> List[str]:
        """Generate key recommendations"""
        return [
            f"Focus on {phase2.get('ansoff_matrix', {}).get('recommended_strategy', 'market penetration')} as primary growth strategy",
            f"Extend runway to 18+ months through efficient burn management",
            f"Build competitive moats in {startup_data.sector} through technology and customer success",
            f"Scale team to {phase3.get('resource_requirements', {}).get('human_resources', [{}])[0].get('headcount', 50)} with focus on sales and engineering",
            "Establish clear OKRs and track progress weekly"
        ]
    
    def _generate_success_factors(self, startup_data: StartupData) -> List[str]:
        """Generate critical success factors"""
        return [
            "Achieving product-market fit within 6 months",
            "Maintaining burn multiple below 1.5x",
            "Building a world-class team with domain expertise",
            f"Capturing meaningful market share in {startup_data.sector}",
            "Creating sustainable competitive advantages"
        ]
    
    def _generate_next_steps(self) -> List[Dict[str, Any]]:
        """Generate next steps"""
        return [
            {
                "timeline": "30 days",
                "actions": [
                    "Complete customer discovery interviews",
                    "Refine product roadmap based on feedback",
                    "Initiate key hiring processes"
                ]
            },
            {
                "timeline": "60 days",
                "actions": [
                    "Launch MVP improvements",
                    "Close first enterprise customers",
                    "Establish key partnerships"
                ]
            },
            {
                "timeline": "90 days",
                "actions": [
                    "Scale go-to-market operations",
                    "Achieve target metrics",
                    "Prepare for next funding round"
                ]
            }
        ]

# Initialize engine
optimized_engine = OptimizedMichelinEngine()

@optimized_router.post("/analyze")
async def analyze_with_optimized_engine(
    request: MichelinAnalysisRequest,
    background_tasks: BackgroundTasks
):
    """
    Optimized Michelin analysis with caching and timeout protection
    """
    try:
        logger.info(f"Starting optimized Michelin analysis for {request.startup_data.startup_name}")
        
        # Perform analysis
        result = await optimized_engine.analyze_startup_optimized(request.startup_data)
        
        logger.info(f"Optimized analysis completed for {request.startup_data.startup_name}")
        
        return result
        
    except Exception as e:
        logger.error(f"Optimized analysis failed: {str(e)}")
        # Return fallback on any error
        return working_engine.generate_michelin_analysis(request.startup_data)

@optimized_router.get("/cache/status")
async def get_cache_status():
    """Get cache statistics"""
    stats = analysis_cache.get_stats()
    return {
        "cache_enabled": True,
        "ttl_seconds": analysis_cache.ttl,
        "stats": stats,
        "message": "In-memory cache is active"
    }

@optimized_router.post("/cache/clear")
async def clear_analysis_cache():
    """Clear the analysis cache"""
    cleared = analysis_cache.clear()
    return {
        "status": "success",
        "cleared": cleared,
        "message": f"Cleared {cleared} cached analyses"
    }

# Export router
__all__ = ['optimized_router']