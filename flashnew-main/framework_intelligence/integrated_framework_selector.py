#!/usr/bin/env python3
"""
Integrated Framework Selector
Combines the original intelligent selector with the advanced academic system
"""

from typing import List, Dict, Optional, Any
import logging
from datetime import datetime

from strategic_context_engine import CompanyContext as StrategicContext
from intelligent_framework_selector import IntelligentFrameworkSelector, CustomizedFramework
from framework_intelligence.framework_selection_engine import (
    AdvancedFrameworkSelector, 
    CompanyContext as AcademicContext,
    FrameworkRecommendation,
    FrameworkJourney
)
from framework_intelligence.framework_taxonomy import *
from framework_intelligence.industry_framework_variants import IndustryFrameworkEngine

logger = logging.getLogger(__name__)


class IntegratedFrameworkSelector:
    """
    Unified framework selector combining:
    1. Original intelligent selector (context-aware, industry variants)
    2. Advanced academic selector (MIT/HBS methodology)
    """
    
    def __init__(self):
        self.intelligent_selector = IntelligentFrameworkSelector()
        self.academic_selector = AdvancedFrameworkSelector()
        self.industry_engine = IndustryFrameworkEngine()
        
    async def select_frameworks(
        self,
        strategic_context: StrategicContext,
        max_frameworks: int = 5,
        use_academic_logic: bool = True
    ) -> List[CustomizedFramework]:
        """
        Select frameworks using hybrid approach
        """
        
        if use_academic_logic:
            # Convert strategic context to academic context
            academic_context = self._convert_to_academic_context(strategic_context)
            
            # Get academic recommendations
            academic_recs = self.academic_selector.select_frameworks(
                academic_context, 
                max_recommendations=max_frameworks * 2  # Get more for filtering
            )
            
            # Filter and customize using original system
            customized_frameworks = []
            for rec in academic_recs[:max_frameworks]:
                framework = self._get_framework_by_id(rec.framework_id)
                if framework:
                    customized = await self.intelligent_selector._customize_framework(
                        framework, strategic_context
                    )
                    # Add academic insights
                    customized.customizations["academic_insights"] = {
                        "fit_score": rec.fit_score,
                        "rationale": rec.rationale,
                        "risks": rec.risks,
                        "success_factors": rec.success_factors,
                        "prerequisites": rec.prerequisites
                    }
                    customized_frameworks.append(customized)
                    
            return customized_frameworks
        else:
            # Use original intelligent selector
            return self.intelligent_selector.select_frameworks(
                strategic_context, max_frameworks
            )
    
    async def create_strategic_journey(
        self,
        strategic_context: StrategicContext,
        planning_horizon_months: int = 12
    ) -> Dict[str, Any]:
        """
        Create comprehensive framework journey with phases
        """
        
        # Convert context
        academic_context = self._convert_to_academic_context(strategic_context)
        
        # Get academic journey
        journey = self.academic_selector.create_framework_journey(
            academic_context, planning_horizon_months
        )
        
        # Enhance with customizations
        enhanced_journey = {
            "company": strategic_context.company_name,
            "horizon_months": planning_horizon_months,
            "total_frameworks": journey.total_frameworks,
            "estimated_days": journey.estimated_total_days,
            "phases": {}
        }
        
        # Process each phase
        for phase_name, phase_recs in [
            ("immediate", journey.immediate),
            ("short_term", journey.short_term),
            ("medium_term", journey.medium_term),
            ("long_term", journey.long_term)
        ]:
            enhanced_journey["phases"][phase_name] = []
            
            for rec in phase_recs:
                framework = self._get_framework_by_id(rec.framework_id)
                if framework:
                    customized = await self.intelligent_selector._customize_framework(
                        framework, strategic_context
                    )
                    
                    phase_item = {
                        "framework": customized,
                        "academic_recommendation": rec,
                        "industry_variant": self._get_industry_variant(
                            rec.framework_id, strategic_context.industry
                        )
                    }
                    enhanced_journey["phases"][phase_name].append(phase_item)
                    
        # Add critical path
        enhanced_journey["critical_path"] = journey.critical_path
        
        return enhanced_journey
    
    def _convert_to_academic_context(
        self, 
        strategic_context: StrategicContext
    ) -> AcademicContext:
        """Convert strategic context to academic context format"""
        
        # Map stage
        stage_map = {
            "pre_seed": TemporalStage.PRE_FORMATION,
            "seed": TemporalStage.VALIDATION,
            "series_a": TemporalStage.GROWTH,  # Series A is typically growth stage
            "series_b": TemporalStage.GROWTH,
            "series_c": TemporalStage.SCALE,
            "growth": TemporalStage.SCALE,
            "mature": TemporalStage.MATURITY
        }
        
        # Map industry
        industry_map = {
            "saas_b2b": IndustryContext.B2B_SAAS,
            "marketplace": IndustryContext.MARKETPLACE,
            "fintech": IndustryContext.FINTECH,
            "healthtech": IndustryContext.HEALTHTECH,
            "edtech": IndustryContext.EDTECH,
            "ecommerce": IndustryContext.ECOMMERCE
        }
        
        # Map problems
        problem_map = {
            "customer_acquisition": ProblemArchetype.CUSTOMER_DISCOVERY,
            "retention": ProblemArchetype.UNIT_ECONOMICS_OPTIMIZATION,
            "unit_economics": ProblemArchetype.UNIT_ECONOMICS_OPTIMIZATION,
            "competition": ProblemArchetype.COMPETITIVE_STRATEGY,
            "scaling": ProblemArchetype.GROWTH_MECHANICS,
            "pmf": ProblemArchetype.PRODUCT_MARKET_FIT
        }
        
        # Determine available data
        available_data = [DataRequirement.QUALITATIVE_ONLY]
        if strategic_context.key_metrics.get("revenue", 0) > 0:
            available_data.append(DataRequirement.BASIC_QUANTITATIVE)
        if strategic_context.key_metrics.get("ltv_cac", 0) > 0:
            available_data.append(DataRequirement.ADVANCED_METRICS)
            
        # Convert challenges to problem archetypes
        primary_problems = []
        for challenge in strategic_context.key_challenges[:3]:
            challenge_lower = challenge.lower()
            for key, archetype in problem_map.items():
                if key in challenge_lower:
                    primary_problems.append(archetype)
                    break
                    
        # Ensure we have at least one problem
        if not primary_problems:
            primary_problems = [ProblemArchetype.BUSINESS_MODEL_DESIGN]
            
        return AcademicContext(
            company_name=strategic_context.company_name,
            industry=industry_map.get(strategic_context.industry, IndustryContext.UNIVERSAL),
            stage=stage_map.get(strategic_context.stage, TemporalStage.VALIDATION),
            team_size=strategic_context.key_metrics.get("team_size", 10),
            primary_problems=primary_problems,
            available_data=available_data,
            revenue_usd=strategic_context.key_metrics.get("revenue", 0),
            growth_rate_percent=strategic_context.key_metrics.get("growth_rate", 0),
            burn_rate_usd=strategic_context.key_metrics.get("burn_rate", 0),
            runway_months=strategic_context.key_metrics.get("runway_months", 12),
            is_crisis_mode=strategic_context.key_metrics.get("runway_months", 12) < 6,
            is_fundraising="fundraising" in str(strategic_context.key_challenges).lower()
        )
    
    def _get_framework_by_id(self, framework_id: str):
        """Get framework from database"""
        from framework_intelligence.framework_database import get_framework_by_id
        return get_framework_by_id(framework_id)
    
    def _get_industry_variant(self, framework_id: str, industry: str):
        """Get industry-specific variant if available"""
        industry_enum = {
            "saas_b2b": IndustryContext.B2B_SAAS,
            "marketplace": IndustryContext.MARKETPLACE,
            "fintech": IndustryContext.FINTECH,
            "healthtech": IndustryContext.HEALTHTECH
        }.get(industry)
        
        if industry_enum:
            return self.industry_engine.get_variant(framework_id, industry_enum)
        return None
    
    def generate_selection_report(
        self,
        strategic_context: StrategicContext,
        frameworks: List[CustomizedFramework]
    ) -> str:
        """Generate comprehensive selection report"""
        
        report = f"""
# Framework Selection Report - {strategic_context.company_name}
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}

## Company Profile
- **Industry**: {strategic_context.industry}
- **Stage**: {strategic_context.stage}
- **Key Metrics**:
  - Revenue: ${strategic_context.key_metrics.get('revenue', 0):,.0f}
  - Growth Rate: {strategic_context.key_metrics.get('growth_rate', 0):.0f}%
  - Runway: {strategic_context.key_metrics.get('runway_months', 0):.0f} months

## Strategic Context
- **Current Inflection**: {strategic_context.current_inflection.value if hasattr(strategic_context, 'current_inflection') else 'Unknown'}
- **Key Challenges**: {', '.join(strategic_context.key_challenges[:3])}

## Recommended Frameworks

"""
        
        for i, framework in enumerate(frameworks, 1):
            academic_insights = framework.customizations.get("academic_insights", {})
            
            report += f"""
### {i}. {framework.base_framework.name}

**Fit Score**: {academic_insights.get('fit_score', 'N/A'):.0f}/100

**Why This Framework**:
{chr(10).join(f"- {r}" for r in academic_insights.get('rationale', ['Good general fit'])[:3])}

**Industry Customization**: {framework.industry_variant}
{self._format_industry_customizations(framework)}

**Implementation**:
- **Time Required**: {framework.implementation_guide.get('timeline', '2-4 weeks')}
- **Key Steps**:
{chr(10).join(f"  {j}. {step}" for j, step in enumerate(framework.base_framework.application_steps[:5], 1))}

**Success Factors**:
{chr(10).join(f"- {factor}" for factor in academic_insights.get('success_factors', framework.base_framework.success_metrics or [])[:3])}

**Risks to Consider**:
{chr(10).join(f"- {risk}" for risk in academic_insights.get('risks', ['Standard implementation risks'])[:3])}

---
"""
        
        return report
    
    def _format_industry_customizations(self, framework: CustomizedFramework) -> str:
        """Format industry-specific customizations"""
        
        if not framework.customizations.get("industry_adjustments"):
            return ""
            
        adjustments = framework.customizations["industry_adjustments"]
        
        result = "\n**Industry-Specific Adjustments**:\n"
        
        if "x_axis" in adjustments:
            result += f"- X-Axis: {adjustments.get('x_label', adjustments['x_axis'])}\n"
        if "y_axis" in adjustments:
            result += f"- Y-Axis: {adjustments.get('y_label', adjustments['y_axis'])}\n"
            
        if "thresholds" in adjustments:
            result += "- Custom Thresholds:\n"
            for key, value in adjustments["thresholds"].items():
                result += f"  - {key.replace('_', ' ').title()}: {value}\n"
                
        return result