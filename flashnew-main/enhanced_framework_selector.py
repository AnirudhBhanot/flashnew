#!/usr/bin/env python3
"""
Enhanced Framework Selector - Production wrapper for advanced framework system
Replaces the basic scoring with MIT/HBS academic methodology
"""

import sys
import logging
from typing import List, Dict, Any, Optional
import asyncio

# Add framework_intelligence to path
sys.path.insert(0, '/Users/sf/Desktop/FLASH')

from strategic_context_engine import CompanyContext, StrategicContextEngine
from intelligent_framework_selector import CustomizedFramework
from framework_intelligence.integrated_framework_selector import IntegratedFrameworkSelector
from framework_intelligence.framework_selection_engine import generate_framework_report

logger = logging.getLogger(__name__)


class EnhancedFrameworkSelector:
    """
    Production-ready framework selector using advanced academic methodology
    """
    
    def __init__(self):
        """Initialize with advanced selector"""
        self.integrated_selector = IntegratedFrameworkSelector()
        self.context_engine = StrategicContextEngine()
        
    async def select_frameworks_for_startup(
        self,
        startup_data: Dict[str, Any],
        max_frameworks: int = 5
    ) -> Dict[str, Any]:
        """
        Main entry point for framework selection
        Returns frameworks with full analysis
        """
        
        try:
            # Build strategic context
            logger.info(f"Building context for {startup_data.get('startup_name', 'Unknown')}")
            context = await self.context_engine.build_company_context(startup_data)
            
            # Select frameworks using advanced logic
            logger.info("Selecting frameworks using advanced academic methodology")
            frameworks = await self.integrated_selector.select_frameworks(
                strategic_context=context,
                max_frameworks=max_frameworks,
                use_academic_logic=True
            )
            
            # Generate comprehensive report
            report = self.integrated_selector.generate_selection_report(
                context, frameworks
            )
            
            # Create journey if requested
            journey = None
            if startup_data.get("include_journey", False):
                journey = await self.integrated_selector.create_strategic_journey(
                    context, 
                    planning_horizon_months=12
                )
            
            return {
                "success": True,
                "company_context": {
                    "name": context.company_name,
                    "industry": context.industry,
                    "stage": context.stage,
                    "inflection": context.current_inflection.value if hasattr(context, 'current_inflection') else None,
                    "challenges": context.key_challenges[:3]
                },
                "frameworks": self._serialize_frameworks(frameworks),
                "report": report,
                "journey": self._serialize_journey(journey) if journey else None,
                "methodology": "MIT/HBS Advanced Framework Selection v2.0"
            }
            
        except Exception as e:
            logger.error(f"Framework selection error: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "frameworks": [],
                "fallback": self._get_fallback_frameworks(startup_data)
            }
    
    def _serialize_frameworks(self, frameworks: List[CustomizedFramework]) -> List[Dict]:
        """Convert framework objects to JSON-serializable format"""
        
        serialized = []
        for fw in frameworks:
            academic_insights = fw.customizations.get("academic_insights", {})
            
            serialized.append({
                "id": fw.base_framework.id,
                "name": fw.base_framework.name,
                "category": fw.base_framework.category.value,
                "description": fw.base_framework.description,
                "fit_score": academic_insights.get("fit_score", 75),
                "confidence": academic_insights.get("confidence", 70),
                "rationale": academic_insights.get("rationale", []),
                "risks": academic_insights.get("risks", []),
                "success_factors": academic_insights.get("success_factors", []),
                "industry_variant": fw.industry_variant,
                "customizations": fw.customizations,
                "implementation_guide": fw.implementation_guide,
                "expected_insights": fw.expected_insights,
                "time_to_implement": fw.base_framework.time_to_implement,
                "complexity": fw.base_framework.complexity.value
            })
            
        return serialized
    
    def _serialize_journey(self, journey: Dict[str, Any]) -> Dict[str, Any]:
        """Convert journey to JSON-serializable format"""
        
        serialized_journey = {
            "total_frameworks": journey["total_frameworks"],
            "estimated_days": journey["estimated_days"],
            "critical_path": journey["critical_path"],
            "phases": {}
        }
        
        for phase_name, phase_items in journey["phases"].items():
            serialized_journey["phases"][phase_name] = []
            
            for item in phase_items:
                framework = item["framework"]
                recommendation = item["academic_recommendation"]
                
                serialized_journey["phases"][phase_name].append({
                    "framework_id": framework.base_framework.id,
                    "framework_name": framework.base_framework.name,
                    "fit_score": recommendation.fit_score,
                    "estimated_days": recommendation.estimated_days,
                    "rationale": recommendation.rationale[:2]
                })
                
        return serialized_journey
    
    def _get_fallback_frameworks(self, startup_data: Dict[str, Any]) -> List[Dict]:
        """Get basic fallback frameworks if advanced selection fails"""
        
        stage = startup_data.get("stage", "seed")
        
        if stage in ["pre_seed", "seed"]:
            return [
                {"id": "lean_canvas", "name": "Lean Canvas"},
                {"id": "customer_development", "name": "Customer Development"},
                {"id": "jobs_to_be_done", "name": "Jobs to be Done"}
            ]
        elif stage in ["series_a", "series_b"]:
            return [
                {"id": "unit_economics", "name": "Unit Economics"},
                {"id": "aarrr_metrics", "name": "AARRR Metrics"},
                {"id": "ansoff_matrix", "name": "Ansoff Matrix"}
            ]
        else:
            return [
                {"id": "swot_analysis", "name": "SWOT Analysis"},
                {"id": "porters_five_forces", "name": "Porter's Five Forces"},
                {"id": "bcg_matrix", "name": "BCG Matrix"}
            ]
    
    async def get_framework_details(
        self,
        framework_id: str,
        industry: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get detailed information about a specific framework"""
        
        from framework_intelligence.framework_database import get_framework_by_id
        from framework_intelligence.industry_framework_variants import IndustryFrameworkEngine, IndustryContext
        
        framework = get_framework_by_id(framework_id)
        if not framework:
            return {"error": "Framework not found"}
            
        # Get industry variant if applicable
        variant = None
        if industry:
            industry_engine = IndustryFrameworkEngine()
            industry_map = {
                "saas_b2b": IndustryContext.B2B_SAAS,
                "marketplace": IndustryContext.MARKETPLACE,
                "fintech": IndustryContext.FINTECH,
                "healthtech": IndustryContext.HEALTHTECH
            }
            
            if industry in industry_map:
                variant = industry_engine.get_variant(framework_id, industry_map[industry])
                
        return {
            "framework": {
                "id": framework.id,
                "name": framework.name,
                "description": framework.description,
                "category": framework.category.value,
                "when_to_use": framework.when_to_use,
                "key_components": framework.key_components,
                "application_steps": framework.application_steps,
                "expected_outcomes": framework.expected_outcomes,
                "complexity": framework.complexity.value,
                "time_to_implement": framework.time_to_implement,
                "prerequisites": framework.prerequisites,
                "common_pitfalls": framework.common_pitfalls
            },
            "industry_variant": {
                "name": variant.variant_name if variant else None,
                "custom_metrics": {
                    k: {
                        "name": v.name,
                        "description": v.description,
                        "good_benchmark": v.good_benchmark,
                        "great_benchmark": v.great_benchmark
                    }
                    for k, v in variant.custom_metrics.items()
                } if variant else {},
                "key_considerations": variant.key_considerations if variant else []
            } if variant else None
        }


# Example usage
async def test_enhanced_selector():
    """Test the enhanced framework selector"""
    
    selector = EnhancedFrameworkSelector()
    
    # Test data
    startup_data = {
        "startup_name": "TestSaaS",
        "sector": "saas_b2b",
        "stage": "series_a",
        "revenue": 2000000,
        "growth_rate": 150,
        "burn_rate": 300000,
        "ltv_cac_ratio": 3.5,
        "net_revenue_retention": 115,
        "team_size": 50,
        "runway_months": 18,
        "key_challenges": [
            "Intense competition from incumbents",
            "Unit economics optimization needed",
            "Scaling sales team efficiently"
        ],
        "include_journey": True
    }
    
    result = await selector.select_frameworks_for_startup(startup_data)
    
    if result["success"]:
        print(f"\n✅ Selected {len(result['frameworks'])} frameworks")
        for fw in result["frameworks"]:
            print(f"\n📊 {fw['name']}")
            print(f"   Fit Score: {fw['fit_score']:.0f}/100")
            print(f"   Confidence: {fw['confidence']:.0f}%")
            print(f"   Industry Variant: {fw['industry_variant']}")
            if fw['rationale']:
                print(f"   Why: {fw['rationale'][0]}")
                
        if result.get("journey"):
            print(f"\n📈 12-Month Journey:")
            print(f"   Total Days: {result['journey']['estimated_days']}")
            print(f"   Critical Path: {' → '.join(result['journey']['critical_path'][:3])}")
    else:
        print(f"\n❌ Error: {result['error']}")


if __name__ == "__main__":
    asyncio.run(test_enhanced_selector())