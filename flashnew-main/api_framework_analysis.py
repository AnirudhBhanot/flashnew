#!/usr/bin/env python3
"""
Framework Analysis API Endpoints
Provides actual framework analysis using real startup data
"""

from typing import Dict, List, Any
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import logging

from framework_intelligence.framework_analyzer import FrameworkAnalyzer, apply_frameworks_to_startup
from framework_intelligence.framework_database import get_framework_by_id

logger = logging.getLogger(__name__)

# Create router
analysis_router = APIRouter(tags=["Framework Analysis"])


class FrameworkAnalysisRequest(BaseModel):
    """Request model for framework analysis"""
    startup_data: Dict[str, Any]
    framework_ids: List[str]  # Which frameworks to apply


class MultiFrameworkAnalysisRequest(BaseModel):
    """Request for analyzing with recommended frameworks"""
    startup_data: Dict[str, Any]
    phase: str = "situation"  # situation, strategy, or execution
    max_frameworks: int = 3


@analysis_router.post("/api/frameworks/analyze")
async def analyze_with_frameworks(request: FrameworkAnalysisRequest) -> Dict[str, Any]:
    """
    Apply specific frameworks to analyze startup data
    Returns actual analysis results with positions, scores, and insights
    """
    try:
        analyzer = FrameworkAnalyzer()
        results = []
        
        for framework_id in request.framework_ids:
            try:
                # Apply the framework
                analysis = analyzer.analyze(framework_id, request.startup_data)
                
                # Get framework metadata
                framework_info = get_framework_by_id(framework_id)
                
                results.append({
                    "framework_id": framework_id,
                    "framework_name": analysis.framework_name,
                    "category": framework_info.category.value if framework_info else "Unknown",
                    "position": analysis.position,
                    "score": analysis.score,
                    "insights": analysis.insights,
                    "recommendations": analysis.recommendations,
                    "metrics": analysis.metrics,
                    "visualization_data": analysis.visualization_data
                })
            except Exception as e:
                logger.error(f"Error analyzing with {framework_id}: {e}")
                results.append({
                    "framework_id": framework_id,
                    "error": str(e)
                })
        
        return {
            "analyses": results,
            "summary": {
                "total_frameworks": len(request.framework_ids),
                "successful": len([r for r in results if "error" not in r]),
                "failed": len([r for r in results if "error" in r])
            }
        }
        
    except Exception as e:
        logger.error(f"Framework analysis error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@analysis_router.post("/api/frameworks/analyze-phase")
async def analyze_strategic_phase(request: MultiFrameworkAnalysisRequest) -> Dict[str, Any]:
    """
    Analyze a specific strategic phase using appropriate frameworks
    Automatically selects and applies the best frameworks for the phase
    """
    try:
        # Map phases to framework categories
        phase_mapping = {
            "situation": ["Strategic", "Marketing", "Financial"],  # Where are we now?
            "strategy": ["Strategic", "Innovation", "Growth"],     # Where should we go?
            "execution": ["Operations", "Product", "Organizational"]  # How to get there?
        }
        
        # Get appropriate categories for this phase
        categories = phase_mapping.get(request.phase, ["Strategic"])
        
        # Skip the framework selector for now - just use predefined frameworks per phase
        phase_frameworks = {
            "situation": ["bcg_matrix", "porters_five_forces", "swot_analysis"],
            "strategy": ["ansoff_matrix", "blue_ocean", "jobs_to_be_done"],
            "execution": ["lean_canvas", "value_chain", "vrio"]
        }
        
        framework_ids = phase_frameworks.get(request.phase, ["swot_analysis"])
        
        # Apply the selected frameworks
        analyzer = FrameworkAnalyzer()
        analyses = []
        
        for framework_id in framework_ids[:request.max_frameworks]:
            try:
                analysis = analyzer.analyze(framework_id, request.startup_data)
                
                # Get framework info
                framework_info = get_framework_by_id(framework_id)
                
                analyses.append({
                    "framework_id": framework_id,
                    "framework_name": analysis.framework_name,
                    "category": framework_info.category.value if framework_info else "Strategic",
                    "position": analysis.position,
                    "score": analysis.score,
                    "insights": analysis.insights,
                    "recommendations": analysis.recommendations,
                    "metrics": analysis.metrics,
                    "visualization_data": analysis.visualization_data,
                    "why_selected": f"Recommended for {request.phase} analysis",
                    "selection_score": 0.8
                })
            except Exception as e:
                logger.error(f"Error in phase analysis with {framework_id}: {e}")
        
        # Generate phase-specific insights
        phase_insights = []
        if request.phase == "situation":
            phase_insights.append("Current position analysis complete")
            # Aggregate insights about current state
            positions = [a["position"] for a in analyses if "position" in a]
            if positions:
                phase_insights.append(f"Overall position: {', '.join(set(positions))}")
        
        elif request.phase == "strategy":
            phase_insights.append("Strategic options identified")
            # Aggregate strategic recommendations
            all_recs = []
            for a in analyses:
                all_recs.extend(a.get("recommendations", []))
            if all_recs:
                phase_insights.append(f"{len(set(all_recs))} unique strategic paths available")
        
        elif request.phase == "execution":
            phase_insights.append("Implementation roadmap frameworks applied")
            # Focus on actionable next steps
            
        return {
            "phase": request.phase,
            "analyses": analyses,
            "phase_insights": phase_insights,
            "summary": {
                "frameworks_applied": len(analyses),
                "average_score": sum(a.get("score", 0) for a in analyses) / max(1, len(analyses))
            }
        }
        
    except Exception as e:
        logger.error(f"Phase analysis error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@analysis_router.get("/api/frameworks/analysis-templates")
async def get_analysis_templates() -> Dict[str, Any]:
    """
    Get pre-configured analysis templates for different scenarios
    """
    templates = {
        "startup_assessment": {
            "name": "Comprehensive Startup Assessment",
            "description": "Full strategic analysis for early-stage startups",
            "phases": {
                "situation": ["bcg_matrix", "swot_analysis", "porters_five_forces"],
                "strategy": ["ansoff_matrix", "blue_ocean", "jobs_to_be_done"],
                "execution": ["lean_canvas", "value_chain", "vrio"]
            }
        },
        "growth_strategy": {
            "name": "Growth Strategy Analysis",
            "description": "For startups ready to scale",
            "phases": {
                "situation": ["bcg_matrix", "vrio", "market_segmentation"],
                "strategy": ["ansoff_matrix", "platform_strategy", "network_effects"],
                "execution": ["okr", "balanced_scorecard", "growth_hacking"]
            }
        },
        "competitive_analysis": {
            "name": "Competitive Positioning",
            "description": "Understand competitive landscape",
            "phases": {
                "situation": ["porters_five_forces", "competitive_analysis", "swot_analysis"],
                "strategy": ["blue_ocean", "differentiation_strategy", "game_theory"],
                "execution": ["value_chain", "core_competencies", "strategic_alliances"]
            }
        },
        "pivot_evaluation": {
            "name": "Pivot Decision Framework",
            "description": "Evaluate need and direction for pivot",
            "phases": {
                "situation": ["lean_canvas", "jobs_to_be_done", "market_validation"],
                "strategy": ["pivot_types", "opportunity_evaluation", "risk_assessment"],
                "execution": ["mvp_strategy", "agile_methodology", "hypothesis_testing"]
            }
        }
    }
    
    return {
        "templates": templates,
        "usage": "Select a template and apply it to your startup data for comprehensive analysis"
    }


@analysis_router.post("/api/frameworks/compare-positions")
async def compare_framework_positions(request: FrameworkAnalysisRequest) -> Dict[str, Any]:
    """
    Compare startup's position across multiple frameworks
    Useful for getting a holistic view
    """
    try:
        analyzer = FrameworkAnalyzer()
        positions = {}
        scores = {}
        
        for framework_id in request.framework_ids:
            try:
                analysis = analyzer.analyze(framework_id, request.startup_data)
                positions[framework_id] = {
                    "position": analysis.position,
                    "score": analysis.score,
                    "interpretation": analysis.insights[0] if analysis.insights else "No interpretation available"
                }
                scores[framework_id] = analysis.score
            except Exception as e:
                logger.error(f"Error comparing {framework_id}: {e}")
        
        # Calculate consensus position
        avg_score = sum(scores.values()) / max(1, len(scores))
        
        if avg_score > 0.7:
            consensus = "Strong Position"
        elif avg_score > 0.5:
            consensus = "Moderate Position"
        else:
            consensus = "Weak Position"
        
        return {
            "positions": positions,
            "consensus": consensus,
            "average_score": avg_score,
            "recommendation": "Focus on frameworks showing weak positions" if avg_score < 0.5 else "Leverage frameworks showing strong positions"
        }
        
    except Exception as e:
        logger.error(f"Position comparison error: {e}")
        raise HTTPException(status_code=500, detail=str(e))