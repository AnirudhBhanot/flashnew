"""
Helper functions for LLM endpoints that can be called directly
"""
import logging
from typing import Dict, List, Any
from llm_analysis import LLMAnalysisEngine

logger = logging.getLogger(__name__)

# Global engine instance
_engine = None

def get_engine() -> LLMAnalysisEngine:
    """Get or create LLM engine instance"""
    global _engine
    if _engine is None:
        _engine = LLMAnalysisEngine()
    return _engine

async def get_dynamic_recommendations(data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Get dynamic recommendations - can be called directly
    
    Args:
        data: Dictionary with scores, startup_data, etc.
    """
    engine = get_engine()
    
    startup_data = data.get("userInput") or data.get("startup_data", {})
    scores = data.get("scores", {})
    
    logger.info(f"Generating recommendations for {startup_data.get('sector', 'unknown')} startup")
    
    try:
        result = await engine.get_recommendations(startup_data, scores)
        return result.get("recommendations", [])
    except Exception as e:
        logger.error(f"Failed to get recommendations: {e}")
        # Return fallback
        from llm_analysis import get_fallback_recommendations
        fallback = get_fallback_recommendations(startup_data, scores)
        return fallback.get("recommendations", [])

async def analyze_whatif_scenario(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Analyze what-if scenario - can be called directly
    
    Args:
        data: Dictionary with startup_data, current_scores, improvements
    """
    engine = get_engine()
    
    startup_data = data.get("startup_data", {})
    current_scores = data.get("current_scores", {})
    improvements = data.get("improvements", [])
    
    logger.info(f"Analyzing what-if with {len(improvements)} improvements")
    
    try:
        result = await engine.analyze_whatif(
            startup_data,
            current_scores,
            improvements
        )
        return result
    except Exception as e:
        logger.error(f"What-if analysis failed: {e}")
        raise ValueError(f"What-if analysis failed: {str(e)}")