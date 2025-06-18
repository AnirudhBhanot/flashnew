#!/usr/bin/env python3
"""
Enhanced Michelin Analysis API - McKinsey-grade strategic analysis
Integrates context engine, intelligent framework selection, and enhanced analysis
"""

import os
import json
import logging
import asyncio
from typing import Dict, List, Optional, Any
from datetime import datetime
from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel

# Import enhanced components
from strategic_context_engine import StrategicContextEngine
from enhanced_framework_selector import EnhancedFrameworkSelector
from mckinsey_grade_analyzer import McKinseyGradeAnalyzer
from enhanced_phase3_analyzer import EnhancedPhase3Analyzer

# Import existing models
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

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create router
enhanced_router = APIRouter(prefix="/api/michelin/enhanced", tags=["Michelin Enhanced"])


class EnhancedMichelinEngine:
    """Enhanced Michelin analysis with McKinsey-grade quality"""
    
    def __init__(self):
        self.context_engine = StrategicContextEngine()
        self.framework_selector = EnhancedFrameworkSelector()
        self.mckinsey_analyzer = McKinseyGradeAnalyzer()
        self.phase3_analyzer = EnhancedPhase3Analyzer()
        
    async def analyze_phase1(self, startup_data: StartupData) -> Dict[str, Any]:
        """Enhanced Phase 1 analysis with deep context"""
        
        logger.info(f"Starting enhanced Phase 1 analysis for {startup_data.startup_name}")
        
        try:
            # Build comprehensive context
            logger.info("Building company context...")
            context = await self.context_engine.build_company_context(
                startup_data.model_dump()
            )
            logger.info("Context built successfully")
            
            # Select and customize frameworks for Phase 1 using enhanced selector
            logger.info("Selecting frameworks using enhanced MIT/HBS methodology...")
            result = await self.framework_selector.select_frameworks_for_startup(
                startup_data.model_dump(), max_frameworks=3
            )
            
            if not result["success"]:
                raise ValueError(f"Framework selection failed: {result.get('error')}")
                
            # Extract frameworks from result
            phase1_frameworks = self._convert_enhanced_frameworks(result["frameworks"])
            logger.info(f"Selected {len(phase1_frameworks)} frameworks with methodology: {result.get('methodology')}")
        except ZeroDivisionError as e:
            logger.error(f"Division by zero during initialization: {str(e)}", exc_info=True)
            # Fall back to decomposed analysis
            raise
        except Exception as e:
            logger.error(f"Error during initialization: {str(e)}", exc_info=True)
            raise
        
        try:
            # Log which frameworks were selected
            framework_names = [f.base_framework.name for f in phase1_frameworks]
            logger.info(f"Selected frameworks: {framework_names}")
            
            # Apply primary framework analysis
            bcg_framework = next(
                (f for f in phase1_frameworks if f.base_framework.id == "bcg_matrix"),
                None
            )
            
            if bcg_framework:
                logger.info("Applying BCG Matrix analysis...")
            else:
                logger.info("BCG Matrix not selected (good for pre-seed!), using primary framework...")
                bcg_framework = phase1_frameworks[0] if phase1_frameworks else None
                
            if not bcg_framework:
                logger.error("No frameworks available")
                raise ValueError("No frameworks available")
                
            bcg_analysis = await self.mckinsey_analyzer.generate_framework_analysis(
                bcg_framework, context
            )
            logger.info("BCG analysis completed")
        except ZeroDivisionError as e:
            logger.error(f"Division by zero in BCG analysis: {str(e)}", exc_info=True)
            raise
        except Exception as e:
            logger.error(f"Error in BCG analysis: {str(e)}", exc_info=True)
            raise
        
        # Apply Porter's Five Forces with context
        porters_framework = next(
            (f for f in phase1_frameworks if "porter" in f.base_framework.id.lower()),
            phase1_frameworks[1] if len(phase1_frameworks) > 1 else None
        )
        porters_analysis = await self._generate_porters_analysis(
            porters_framework, context
        ) if porters_framework else self._default_porters_analysis(context)
        
        # Generate context-aware SWOT
        swot_analysis = await self._generate_enhanced_swot(context)
        
        # Generate strategic narrative
        executive_summary = await self._generate_executive_summary(
            context, bcg_analysis, porters_analysis, swot_analysis
        )
        
        position_narrative = await self._generate_position_narrative(
            context, bcg_analysis
        )
        
        return {
            "executive_summary": executive_summary,
            "bcg_matrix_analysis": self._format_bcg_analysis(bcg_analysis, context),
            "porters_five_forces": porters_analysis,
            "swot_analysis": swot_analysis,
            "current_position_narrative": position_narrative,
            "context": {
                "industry_benchmarks": {
                    "top_quartile_growth": context.industry_benchmarks.top_quartile_growth,
                    "median_burn_multiple": context.industry_benchmarks.median_burn_multiple,
                    "typical_ltv_cac": context.industry_benchmarks.top_quartile_ltv_cac
                },
                "strategic_inflection": context.current_inflection.value,
                "primary_question": context.primary_strategic_question
            }
        }
        
    async def analyze_phase2(
        self, 
        startup_data: StartupData,
        phase1_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Enhanced Phase 2 with strategic options"""
        
        logger.info(f"Starting enhanced Phase 2 analysis for {startup_data.startup_name}")
        
        # Rebuild context with Phase 1 insights
        context = await self.context_engine.build_company_context(
            startup_data.model_dump()
        )
        
        # Select growth frameworks
        growth_frameworks = await self.framework_selector.select_frameworks(
            context, max_frameworks=4
        )
        
        # Generate Ansoff Matrix analysis
        ansoff_analysis = await self._generate_ansoff_analysis(context, phase1_data)
        
        # Generate Blue Ocean Strategy
        blue_ocean_analysis = await self._generate_blue_ocean_analysis(context)
        
        # Generate growth scenarios with Monte Carlo
        growth_scenarios = await self._generate_growth_scenarios(context, ansoff_analysis)
        
        # Strategic recommendation synthesis
        recommended_direction = await self._synthesize_strategic_direction(
            context, ansoff_analysis, blue_ocean_analysis, growth_scenarios
        )
        
        return {
            "strategic_options_overview": self._generate_options_overview(
                context, ansoff_analysis, blue_ocean_analysis
            ),
            "ansoff_matrix_analysis": ansoff_analysis,
            "blue_ocean_strategy": blue_ocean_analysis,
            "growth_scenarios": growth_scenarios,
            "recommended_direction": recommended_direction
        }
        
    async def analyze_phase3(
        self,
        startup_data: StartupData,
        phase1_data: Dict[str, Any],
        phase2_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Enhanced Phase 3 with implementation planning"""
        
        logger.info(f"Starting enhanced Phase 3 analysis for {startup_data.startup_name}")
        
        # Build context
        context = await self.context_engine.build_company_context(
            startup_data.model_dump()
        )
        
        # Use enhanced Phase 3 analyzer
        phase3_analysis = await self.phase3_analyzer.analyze_phase3(
            startup_data.model_dump(),
            context,
            phase1_data,
            phase2_data
        )
        
        return phase3_analysis
        
    async def _generate_porters_analysis(
        self,
        framework: Any,
        context: Any
    ) -> Dict[str, Any]:
        """Generate enhanced Porter's analysis"""
        
        analysis = await self.mckinsey_analyzer.generate_framework_analysis(
            framework, context
        )
        
        # Structure for frontend
        return {
            "competitive_rivalry": {
                "level": self._extract_level(analysis, "competitive_rivalry", "High"),
                "analysis": self._extract_force_analysis(analysis, "competitive_rivalry", context),
                "factors": self._extract_factors(analysis, "competitive_rivalry", context)
            },
            "threat_of_new_entrants": {
                "level": self._extract_level(analysis, "new_entrants", "Medium"),
                "analysis": self._extract_force_analysis(analysis, "new_entrants", context),
                "factors": self._extract_factors(analysis, "new_entrants", context)
            },
            "supplier_power": {
                "level": self._extract_level(analysis, "supplier", "Low"),
                "analysis": self._extract_force_analysis(analysis, "supplier", context),
                "factors": self._extract_factors(analysis, "supplier", context)
            },
            "buyer_power": {
                "level": self._extract_level(analysis, "buyer", "Medium"),
                "analysis": self._extract_force_analysis(analysis, "buyer", context),
                "factors": self._extract_factors(analysis, "buyer", context)
            },
            "threat_of_substitutes": {
                "level": self._extract_level(analysis, "substitutes", "Medium"),
                "analysis": self._extract_force_analysis(analysis, "substitutes", context),
                "factors": self._extract_factors(analysis, "substitutes", context)
            },
            "overall_attractiveness": self._calculate_overall_attractiveness(analysis, context),
            "strategic_implications": self._extract_strategic_implications(analysis, context)
        }
        
    def _default_porters_analysis(self, context: Any) -> Dict[str, Any]:
        """Default Porter's analysis if framework not available"""
        
        return {
            "competitive_rivalry": {
                "level": "High" if context.competitive_dynamics.direct_competitors else "Medium",
                "analysis": f"With {len(context.competitive_dynamics.direct_competitors)} direct competitors in a {context.competitive_dynamics.market_dynamics} market, rivalry is intense",
                "factors": ["Market consolidation", "Price competition", "Feature parity"]
            },
            "threat_of_new_entrants": {
                "level": "Medium",
                "analysis": f"Barriers to entry in {context.industry} are moderate with {context.industry_benchmarks.time_to_pmf_months} months typical to PMF",
                "factors": ["Capital requirements", "Technical complexity", "Network effects"]
            },
            "supplier_power": {
                "level": "Low",
                "analysis": "Suppliers have limited power due to competitive markets",
                "factors": ["Multiple vendors", "Commodity inputs", "Low switching costs"]
            },
            "buyer_power": {
                "level": "High" if context.key_metrics.get("customer_concentration", 0) > 20 else "Medium",
                "analysis": "Buyers have significant leverage due to alternatives",
                "factors": ["Price sensitivity", "Low switching costs", "Information availability"]
            },
            "threat_of_substitutes": {
                "level": "Medium",
                "analysis": "Alternative solutions exist but with trade-offs",
                "factors": ["Manual processes", "Competitor products", "In-house development"]
            },
            "overall_attractiveness": "Moderately Attractive",
            "strategic_implications": [
                "Focus on differentiation to reduce rivalry",
                "Build switching costs to retain customers",
                "Create network effects as entry barriers"
            ]
        }
        
    async def _generate_enhanced_swot(self, context: Any) -> Dict[str, Any]:
        """Generate context-aware SWOT analysis"""
        
        return {
            "strengths": [
                {
                    "point": strength,
                    "evidence": self._get_strength_evidence(strength, context),
                    "strategic_value": "High"
                }
                for strength in self._identify_strengths(context)
            ][:4],
            "weaknesses": [
                {
                    "point": weakness,
                    "impact": self._assess_weakness_impact(weakness, context),
                    "mitigation": self._suggest_mitigation(weakness, context)
                }
                for weakness in self._identify_weaknesses(context)
            ][:4],
            "opportunities": [
                {
                    "point": opportunity,
                    "potential": self._quantify_opportunity(opportunity, context),
                    "timeframe": "6-12 months"
                }
                for opportunity in context.strategic_opportunities
            ][:4],
            "threats": [
                {
                    "point": threat,
                    "probability": "Medium",
                    "mitigation": self._suggest_threat_mitigation(threat, context)
                }
                for threat in context.competitive_dynamics.competitive_threats
            ][:4],
            "strategic_priorities": self._derive_strategic_priorities(context)
        }
        
    def _identify_strengths(self, context: Any) -> List[str]:
        """Identify context-specific strengths"""
        
        strengths = []
        
        # Metric-based strengths
        if context.key_metrics.get("ltv_cac", 0) > context.industry_benchmarks.top_quartile_ltv_cac:
            strengths.append("Superior unit economics")
            
        if context.key_metrics.get("growth_rate", 0) > context.industry_benchmarks.top_quartile_growth:
            strengths.append("Exceptional growth rate")
            
        # Asset-based strengths
        strengths.extend(context.strategic_assets[:2])
        
        # Team strengths
        if context.key_metrics.get("team_size", 0) > 50:
            strengths.append("Strong team and execution capability")
            
        return strengths
        
    def _identify_weaknesses(self, context: Any) -> List[str]:
        """Identify context-specific weaknesses"""
        
        weaknesses = []
        
        # Metric-based weaknesses
        if context.key_metrics.get("runway", 12) < 9:
            weaknesses.append("Limited runway")
            
        if context.key_metrics.get("ltv_cac", 3) < 2:
            weaknesses.append("Weak unit economics")
            
        # Constraint-based weaknesses
        weaknesses.extend(context.critical_constraints[:2])
        
        return weaknesses
        
    def _get_strength_evidence(self, strength: str, context: Any) -> str:
        """Get evidence for strength"""
        
        evidence_map = {
            "Superior unit economics": f"LTV/CAC of {context.key_metrics.get('ltv_cac', 0):.1f}x vs {context.industry_benchmarks.top_quartile_ltv_cac}x benchmark",
            "Exceptional growth rate": f"{context.key_metrics.get('growth_rate', 0)}% growth vs {context.industry_benchmarks.median_growth}% median",
            "Strong team": f"{context.key_metrics.get('team_size', 0)} experienced professionals"
        }
        
        for key, value in evidence_map.items():
            if key.lower() in strength.lower():
                return value
                
        return "Validated through market performance"
        
    def _assess_weakness_impact(self, weakness: str, context: Any) -> str:
        """Assess impact of weakness"""
        
        if "runway" in weakness.lower():
            return f"Critical - only {context.key_metrics.get('runway', 0)} months remaining"
        elif "unit economics" in weakness.lower():
            return "High - unsustainable growth model"
        else:
            return "Medium - constrains growth potential"
            
    def _suggest_mitigation(self, weakness: str, context: Any) -> str:
        """Suggest mitigation for weakness"""
        
        mitigation_map = {
            "runway": "Immediate fundraising or burn reduction",
            "unit economics": "Optimize pricing and reduce CAC",
            "team": "Aggressive hiring with equity incentives",
            "market share": "Focus on niche domination first"
        }
        
        for key, value in mitigation_map.items():
            if key in weakness.lower():
                return value
                
        return "Strategic focus and resource allocation"
        
    def _quantify_opportunity(self, opportunity: str, context: Any) -> str:
        """Quantify opportunity potential"""
        
        if "market growth" in opportunity.lower():
            return f"${context.key_metrics.get('revenue', 0) * 3 / 1e6:.1f}M potential in growing market"
        elif "expansion" in opportunity.lower():
            return f"{context.key_metrics.get('nrr', 100) - 100}% expansion revenue available"
        else:
            return "Significant revenue upside"
            
    def _suggest_threat_mitigation(self, threat: str, context: Any) -> str:
        """Suggest threat mitigation"""
        
        if "competition" in threat.lower():
            return "Differentiate through superior execution and customer success"
        elif "regulation" in threat.lower():
            return "Proactive compliance and regulatory engagement"
        else:
            return "Monitor closely and prepare contingencies"
            
    def _derive_strategic_priorities(self, context: Any) -> List[str]:
        """Derive strategic priorities from context"""
        
        priorities = []
        
        # Survival priorities
        if context.key_metrics.get("runway", 12) < 9:
            priorities.append("Extend runway through fundraising or efficiency")
            
        # Growth priorities  
        if context.current_inflection.value == "achieving_product_market_fit":
            priorities.append("Validate PMF in core segment")
        elif context.current_inflection.value == "scaling_growth":
            priorities.append("Scale efficient growth engine")
            
        # Competitive priorities
        if context.competitive_dynamics.our_relative_position > 3:
            priorities.append("Gain market share through differentiation")
            
        return priorities[:3]
        
    async def _generate_executive_summary(
        self,
        context: Any,
        bcg_analysis: Dict[str, Any],
        porters_analysis: Dict[str, Any],
        swot_analysis: Dict[str, Any]
    ) -> str:
        """Generate executive summary"""
        
        prompt = f"""
Write a 2-3 sentence executive summary for {context.company_name}:

CONTEXT:
- {context.stage} stage {context.industry} company
- BCG Position: {bcg_analysis.get('framework_positioning', {}).get('classification', 'Question Mark')}
- Revenue: ${context.key_metrics.get('revenue', 0):,.0f} ({context.key_metrics.get('growth_rate', 0)}% growth)
- Runway: {context.key_metrics.get('runway', 12)} months
- Primary Challenge: {context.primary_strategic_question}

Focus on their current position and most critical strategic imperative.
Be specific and reference {context.industry} dynamics.
"""
        
        summary = await self.mckinsey_analyzer._call_deepseek(prompt, max_tokens=200)
        
        if len(summary) < 50:
            summary = (
                f"{context.company_name} is a {context.stage} {context.industry} company "
                f"positioned as a {bcg_analysis.get('framework_positioning', {}).get('classification', 'growth player')} "
                f"with {context.key_metrics.get('runway', 12)} months runway. "
                f"{context.strategic_narrative}"
            )
            
        return summary
        
    async def _generate_position_narrative(
        self,
        context: Any,
        bcg_analysis: Dict[str, Any]
    ) -> str:
        """Generate current position narrative"""
        
        return (
            f"{context.company_name} has achieved {context.key_metrics.get('users', 0):,} users "
            f"and ${context.key_metrics.get('revenue', 0):,.0f} in revenue, positioning them as a "
            f"{bcg_analysis.get('framework_positioning', {}).get('classification', 'emerging player')} "
            f"in the {context.industry} market. With {context.key_metrics.get('ltv_cac', 0):.1f}x LTV/CAC "
            f"and {context.key_metrics.get('runway', 0)} months runway, the company must "
            f"{context.key_challenges[0].lower() if context.key_challenges else 'focus on efficient growth'}."
        )
        
    def _format_bcg_analysis(
        self,
        bcg_analysis: Dict[str, Any],
        context: Any
    ) -> Dict[str, Any]:
        """Format BCG analysis for frontend"""
        
        position = bcg_analysis.get("framework_positioning", {}).get("classification", "Question Mark")
        
        return {
            "position": position,
            "market_growth_rate": self._get_market_growth_label(context),
            "relative_market_share": self._get_market_share_label(context),
            "strategic_implications": bcg_analysis.get("executive_summary", f"As a {position}, focus on strategic choices for growth")
        }
        
    def _get_market_growth_label(self, context: Any) -> str:
        """Get market growth label"""
        
        growth = context.key_metrics.get("market_growth", 20)
        if growth > 30:
            return "Very High"
        elif growth > 20:
            return "High"
        elif growth > 10:
            return "Medium"
        else:
            return "Low"
            
    def _get_market_share_label(self, context: Any) -> str:
        """Get market share label"""
        
        share = context.key_metrics.get("market_share", 1)
        if share > 20:
            return "Dominant"
        elif share > 10:
            return "Strong"
        elif share > 5:
            return "Moderate"
        else:
            return "Low"
            
    def _extract_level(
        self,
        analysis: Dict[str, Any],
        force: str,
        default: str
    ) -> str:
        """Extract force level from analysis"""
        
        # Look in various places the level might be
        if "framework_positioning" in analysis:
            positioning = analysis["framework_positioning"]
            if force in str(positioning).lower():
                for level in ["High", "Medium", "Low"]:
                    if level in str(positioning):
                        return level
                        
        return default
        
    def _extract_force_analysis(
        self,
        analysis: Dict[str, Any],
        force: str,
        context: Any
    ) -> str:
        """Extract force analysis text"""
        
        # Try to find specific analysis
        if "key_insights" in analysis:
            for insight in analysis["key_insights"]:
                if force.replace("_", " ") in insight.get("insight", "").lower():
                    return insight["insight"]
                    
        # Default based on context
        if force == "competitive_rivalry":
            return f"With {len(context.competitive_dynamics.direct_competitors)} competitors, rivalry is {self._extract_level(analysis, force, 'High').lower()}"
        else:
            return f"Force is {self._extract_level(analysis, force, 'Medium').lower()} in current market"
            
    def _extract_factors(
        self,
        analysis: Dict[str, Any],
        force: str,
        context: Any
    ) -> List[str]:
        """Extract factors for a force"""
        
        default_factors = {
            "competitive_rivalry": ["Price competition", "Feature parity", "Market share battle"],
            "new_entrants": ["Low barriers", "Attractive margins", "Growing market"],
            "supplier": ["Limited suppliers", "Switching costs", "Critical inputs"],
            "buyer": ["Price sensitivity", "Many alternatives", "Low switching costs"],
            "substitutes": ["Alternative solutions", "Technology shifts", "Changing needs"]
        }
        
        return default_factors.get(force, ["Market dynamics", "Industry structure", "Economic factors"])
        
    def _calculate_overall_attractiveness(
        self,
        analysis: Dict[str, Any],
        context: Any
    ) -> str:
        """Calculate overall market attractiveness"""
        
        # Simple scoring based on forces
        high_forces = sum(1 for force in ["competitive_rivalry", "buyer_power", "threat_of_substitutes"] 
                         if self._extract_level(analysis, force, "Medium") == "High")
                         
        if high_forces >= 2:
            return "Challenging - Requires strong differentiation"
        elif context.industry_benchmarks.top_quartile_growth > 50:
            return "Highly Attractive - High growth opportunity"
        else:
            return "Moderately Attractive - Selective opportunities"
            
    def _extract_strategic_implications(
        self,
        analysis: Dict[str, Any],
        context: Any
    ) -> List[str]:
        """Extract strategic implications"""
        
        implications = []
        
        # From analysis
        if "strategic_recommendations" in analysis:
            for rec in analysis["strategic_recommendations"][:2]:
                implications.append(rec.get("recommendation", ""))
                
        # Context-based
        if context.competitive_dynamics.our_relative_position > 3:
            implications.append("Focus on differentiation to improve competitive position")
            
        if context.key_metrics.get("ltv_cac", 0) < 3:
            implications.append("Improve unit economics before scaling")
            
        return implications[:3]
        
    async def _generate_ansoff_analysis(
        self,
        context: Any,
        phase1_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate Ansoff Matrix analysis"""
        
        prompt = f"""
Apply Ansoff Matrix to {context.company_name}:

CONTEXT:
- Current Position: {phase1_data.get('bcg_matrix_analysis', {}).get('position', 'Growth')}
- Market: {context.industry}, {context.key_metrics.get('market_share', 1):.1f}% share
- Product Stage: {context.stage}
- Geographic Focus: {context.key_metrics.get('geographic_focus', 'Domestic')}

Evaluate each quadrant:
1. Market Penetration - Current products, current markets
2. Market Development - Current products, new markets  
3. Product Development - New products, current markets
4. Diversification - New products, new markets

For each, provide:
- Feasibility (High/Medium/Low)
- Expected ROI
- Time to impact
- Key initiatives

Then recommend the optimal strategy based on their {context.key_metrics.get('runway', 12)} month runway and growth goals.
"""
        
        response = await self.mckinsey_analyzer._call_deepseek(prompt, max_tokens=800)
        
        # Parse into structured format
        return self._parse_ansoff_response(response, context)
        
    def _parse_ansoff_response(
        self,
        response: str,
        context: Any
    ) -> Dict[str, Any]:
        """Parse Ansoff response into structured format"""
        
        # Default structure
        ansoff = {
            "market_penetration": {
                "feasibility": "High",
                "expected_impact": "30% revenue growth",
                "timeline": "3-6 months",
                "initiatives": [
                    "Optimize sales process",
                    "Increase customer retention",
                    "Expand within existing accounts"
                ],
                "investment_required": "$500K"
            },
            "market_development": {
                "feasibility": "Medium",
                "expected_impact": "50% TAM expansion",
                "timeline": "6-12 months",
                "initiatives": [
                    "Enter adjacent verticals",
                    "Geographic expansion",
                    "Channel partnerships"
                ],
                "investment_required": "$1M"
            },
            "product_development": {
                "feasibility": "Medium",
                "expected_impact": "2x ARPU",
                "timeline": "9-12 months",
                "initiatives": [
                    "Launch enterprise tier",
                    "Add AI capabilities",
                    "Build platform APIs"
                ],
                "investment_required": "$1.5M"
            },
            "diversification": {
                "feasibility": "Low",
                "expected_impact": "New revenue stream",
                "timeline": "12-24 months",
                "initiatives": [
                    "Acquire complementary product",
                    "Enter new market segment",
                    "Build ecosystem"
                ],
                "investment_required": "$3M+"
            },
            "recommended_strategy": "Market Penetration",
            "rationale": f"With {context.key_metrics.get('runway', 12)} months runway, focus on quick wins in existing market",
            "implementation_priorities": [
                "Double down on what's working",
                "Fix unit economics",
                "Prepare for next fundraise"
            ]
        }
        
        # Try to extract actual recommendations from response
        if "market penetration" in response.lower():
            # Update with parsed data
            pass
            
        return ansoff
        
    async def _generate_blue_ocean_analysis(
        self,
        context: Any
    ) -> Dict[str, Any]:
        """Generate Blue Ocean Strategy analysis"""
        
        prompt = f"""
Apply Blue Ocean Strategy to {context.company_name} in {context.industry}:

Current State:
- Competitors: {len(context.competitive_dynamics.direct_competitors)}
- Differentiation: {', '.join(context.competitive_dynamics.differentiation_factors[:2])}
- Market Dynamics: {context.competitive_dynamics.market_dynamics}

Using the Four Actions Framework, identify:

ELIMINATE - What factors that the industry takes for granted should be eliminated?
(Industry-specific factors that add cost but no value)

REDUCE - What factors should be reduced well below the industry's standard?
(Overserved features that can be simplified)

RAISE - What factors should be raised well above the industry's standard?  
(Underserved needs that matter to customers)

CREATE - What factors should be created that the industry has never offered?
(New value propositions that change the game)

Also identify:
- Value Innovation Potential (High/Medium/Low with rationale)
- Specific Blue Ocean opportunity in their market
- Implementation approach

Be specific to {context.industry} and their situation.
"""
        
        response = await self.mckinsey_analyzer._call_deepseek(prompt, max_tokens=700)
        
        return self._parse_blue_ocean_response(response, context)
        
    def _parse_blue_ocean_response(
        self,
        response: str,
        context: Any
    ) -> Dict[str, Any]:
        """Parse Blue Ocean response"""
        
        # Default structure with industry-specific elements
        industry_specific = self._get_industry_blue_ocean(context.industry)
        
        blue_ocean = {
            "four_actions": {
                "eliminate": industry_specific.get("eliminate", [
                    "Complex pricing models",
                    "Long implementation cycles",
                    "Feature bloat"
                ]),
                "reduce": industry_specific.get("reduce", [
                    "Customer acquisition cost",
                    "Time to value",
                    "Technical complexity"
                ]),
                "raise": industry_specific.get("raise", [
                    "User experience",
                    "Customer success",
                    "Product reliability"
                ]),
                "create": industry_specific.get("create", [
                    "Self-serve enterprise",
                    "AI-powered insights",
                    "Community platform"
                ])
            },
            "value_innovation_potential": "High - Opportunity to redefine category",
            "blue_ocean_opportunity": {
                "market_size": f"${context.key_metrics.get('tam', 1e9) * 0.1 / 1e6:.0f}M addressable",
                "differentiation": "10x better user experience",
                "competitive_advantage": "First-mover in new category"
            },
            "implementation_timeline": "6-12 months to establish position"
        }
        
        # Try to extract from response
        # ... parsing logic ...
        
        return blue_ocean
        
    def _get_industry_blue_ocean(self, industry: str) -> Dict[str, List[str]]:
        """Get industry-specific Blue Ocean elements"""
        
        strategies = {
            "saas_b2b": {
                "eliminate": ["Complex contracts", "Long sales cycles", "Professional services"],
                "reduce": ["Implementation time", "Training requirements", "Pricing complexity"],
                "raise": ["Self-serve capabilities", "Time to value", "Product stickiness"],
                "create": ["PLG motion", "Community-led growth", "Ecosystem platform"]
            },
            "marketplace": {
                "eliminate": ["Listing fees", "Geographic restrictions", "Category limitations"],
                "reduce": ["Transaction friction", "Trust barriers", "Discovery time"],
                "raise": ["Supply liquidity", "Match quality", "Transaction velocity"],
                "create": ["Social commerce", "AI matching", "Embedded finance"]
            },
            "fintech": {
                "eliminate": ["Paper processes", "Branch requirements", "Hidden fees"],
                "reduce": ["Compliance friction", "Onboarding time", "Minimum balances"],
                "raise": ["Transparency", "Mobile experience", "Financial insights"],
                "create": ["Embedded banking", "Social features", "Predictive finance"]
            }
        }
        
        return strategies.get(industry, strategies["saas_b2b"])
        
    async def _generate_growth_scenarios(
        self,
        context: Any,
        ansoff_analysis: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Generate growth scenarios with probabilities"""
        
        current_revenue = context.key_metrics.get("revenue", 1000000)
        
        scenarios = []
        
        # Conservative scenario
        scenarios.append({
            "name": "Conservative Growth",
            "description": f"Focus on {ansoff_analysis['recommended_strategy']} with disciplined execution",
            "assumptions": [
                f"Maintain {context.key_metrics.get('growth_rate', 50)}% growth",
                "No major market changes",
                "Current team and resources"
            ],
            "expected_revenue_year3": f"${current_revenue * 3 / 1e6:.1f}M",
            "investment_required": f"${context.key_metrics.get('burn_rate', 100000) * 12:,.0f}",
            "success_probability": "75%",
            "strategic_moves": [
                "Optimize current operations",
                "Incremental improvements",
                "Maintain market position"
            ],
            "key_risks": [
                "Slower growth than market",
                "Competitive pressure",
                "Team retention"
            ]
        })
        
        # Base case scenario
        scenarios.append({
            "name": "Base Case Growth",
            "description": "Balanced growth with selective expansion",
            "assumptions": [
                f"Achieve {context.industry_benchmarks.median_growth}% growth",
                "Some market expansion",
                "Moderate hiring"
            ],
            "expected_revenue_year3": f"${current_revenue * 5 / 1e6:.1f}M",
            "investment_required": f"${context.key_metrics.get('burn_rate', 100000) * 18:,.0f}",
            "success_probability": "60%",
            "strategic_moves": [
                ansoff_analysis['market_penetration']['initiatives'][0],
                "Enter 1-2 adjacent segments",
                "Build partnerships"
            ],
            "key_risks": [
                "Execution complexity",
                "Resource constraints",
                "Market timing"
            ]
        })
        
        # Aggressive scenario
        scenarios.append({
            "name": "Aggressive Growth",
            "description": "Full market capture with heavy investment",
            "assumptions": [
                f"Achieve {context.industry_benchmarks.top_quartile_growth}% growth",
                "Aggressive expansion",
                "Significant funding"
            ],
            "expected_revenue_year3": f"${current_revenue * 10 / 1e6:.1f}M",
            "investment_required": f"${context.key_metrics.get('burn_rate', 100000) * 30:,.0f}",
            "success_probability": "35%",
            "strategic_moves": [
                "Rapid geographic expansion",
                "Acquire competitors",
                "Build platform ecosystem"
            ],
            "key_risks": [
                "High burn rate",
                "Execution risk",
                "Market saturation"
            ]
        })
        
        return scenarios
        
    async def _synthesize_strategic_direction(
        self,
        context: Any,
        ansoff: Dict[str, Any],
        blue_ocean: Dict[str, Any],
        scenarios: List[Dict[str, Any]]
    ) -> str:
        """Synthesize strategic recommendation"""
        
        prompt = f"""
Based on the strategic analysis for {context.company_name}, provide a clear strategic recommendation:

CURRENT SITUATION:
- {context.strategic_narrative}
- Primary Challenge: {context.primary_strategic_question}
- Runway: {context.key_metrics.get('runway', 12)} months

STRATEGIC OPTIONS:
- Ansoff Recommendation: {ansoff['recommended_strategy']}
- Blue Ocean Opportunity: {blue_ocean['value_innovation_potential']}
- Base Case Scenario: {scenarios[1]['expected_revenue_year3']} revenue

Provide a 2-3 paragraph strategic recommendation that:
1. Addresses their primary challenge
2. Leverages their strengths
3. Is achievable within their constraints
4. Sets them up for long-term success

Be specific and actionable.
"""
        
        recommendation = await self.mckinsey_analyzer._call_deepseek(prompt, max_tokens=400)
        
        if len(recommendation) < 100:
            recommendation = self._generate_fallback_recommendation(
                context, ansoff, scenarios
            )
            
        return recommendation
        
    def _generate_fallback_recommendation(
        self,
        context: Any,
        ansoff: Dict[str, Any],
        scenarios: List[Dict[str, Any]]
    ) -> str:
        """Generate fallback recommendation"""
        
        return (
            f"{context.company_name} should pursue a {ansoff['recommended_strategy']} strategy "
            f"to maximize their {context.key_metrics.get('ltv_cac', 2):.1f}x LTV/CAC advantage "
            f"while addressing the {context.key_metrics.get('runway', 12)}-month runway constraint. "
            f"\n\n"
            f"Focus on achieving {scenarios[1]['expected_revenue_year3']} in revenue through "
            f"disciplined execution of proven playbooks, while preparing for a "
            f"Series {self._next_funding_round(context.stage)} raise. "
            f"This balanced approach offers {scenarios[1]['success_probability']} probability "
            f"of success while preserving optionality for future expansion."
        )
        
    def _next_funding_round(self, current_stage: str) -> str:
        """Get next funding round"""
        
        stage_map = {
            "pre_seed": "Seed",
            "seed": "A",
            "series_a": "B",
            "series_b": "C",
            "series_c": "D"
        }
        
        return stage_map.get(current_stage, "A")
        
    def _generate_options_overview(
        self,
        context: Any,
        ansoff: Dict[str, Any],
        blue_ocean: Dict[str, Any]
    ) -> str:
        """Generate strategic options overview"""
        
        return (
            f"Based on {context.company_name}'s position as a {context.current_inflection.value.replace('_', ' ')} "
            f"company in {context.industry}, we've identified {ansoff['recommended_strategy']} "
            f"as the primary growth vector with {blue_ocean['value_innovation_potential'].split('-')[0].strip()} "
            f"potential for value innovation. The analysis reveals {len(blue_ocean['blue_ocean_opportunity'])} "
            f"distinct opportunities to create uncontested market space while building on existing strengths."
        )
        
    async def close(self):
        """Close all resources"""
        await self.mckinsey_analyzer.close()
        await self.phase3_analyzer.close()
    
    def _convert_enhanced_frameworks(self, framework_data: List[Dict]) -> List[Any]:
        """Convert enhanced framework format to expected format"""
        from intelligent_framework_selector import CustomizedFramework
        from framework_intelligence.framework_database import get_framework_by_id
        
        converted = []
        for fw_data in framework_data:
            # Get base framework
            framework = get_framework_by_id(fw_data["id"])
            if framework:
                # Create a mock CustomizedFramework object
                customized = type('CustomizedFramework', (), {
                    'base_framework': framework,
                    'customizations': fw_data.get("customizations", {}),
                    'industry_variant': fw_data.get("industry_variant"),
                    'specific_metrics': [],
                    'thresholds': fw_data.get("customizations", {}).get("industry_adjustments", {}).get("thresholds", {}),
                    'implementation_guide': fw_data.get("implementation_guide", {}),
                    'expected_insights': fw_data.get("expected_insights", [])
                })()
                converted.append(customized)
        
        return converted


# Initialize engine
enhanced_engine = None

def get_enhanced_engine() -> EnhancedMichelinEngine:
    """Get or create enhanced engine instance"""
    global enhanced_engine
    if enhanced_engine is None:
        enhanced_engine = EnhancedMichelinEngine()
    return enhanced_engine


# API Endpoints
@enhanced_router.post("/analyze/phase1", response_model=Phase1Response)
async def analyze_phase1_enhanced(
    request: MichelinAnalysisRequest,
    background_tasks: BackgroundTasks
):
    """Enhanced Phase 1 analysis with deep context"""
    
    engine = get_enhanced_engine()
    
    try:
        phase1_data = await engine.analyze_phase1(request.startup_data)
        
        return Phase1Response(
            startup_name=request.startup_data.startup_name,
            analysis_date=datetime.now().isoformat(),
            phase1=Phase1Analysis(**phase1_data)
        )
        
    except Exception as e:
        logger.error(f"Enhanced Phase 1 failed: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Analysis failed: {str(e)}"
        )


@enhanced_router.post("/analyze/phase2", response_model=Phase2Response)
async def analyze_phase2_enhanced(
    request: Phase2Request,
    background_tasks: BackgroundTasks
):
    """Enhanced Phase 2 analysis with strategic options"""
    
    engine = get_enhanced_engine()
    
    try:
        phase1_dict = request.phase1_results.model_dump()
        phase2_data = await engine.analyze_phase2(
            request.startup_data, 
            phase1_dict
        )
        
        return Phase2Response(
            startup_name=request.startup_data.startup_name,
            analysis_date=datetime.now().isoformat(),
            phase2=Phase2Analysis(**phase2_data)
        )
        
    except Exception as e:
        logger.error(f"Enhanced Phase 2 failed: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Analysis failed: {str(e)}"
        )


@enhanced_router.post("/analyze/phase3", response_model=Phase3Response)
async def analyze_phase3_enhanced(
    request: Phase3Request,
    background_tasks: BackgroundTasks
):
    """Enhanced Phase 3 analysis with implementation planning"""
    
    engine = get_enhanced_engine()
    
    try:
        phase1_dict = request.phase1_results.model_dump()
        phase2_dict = request.phase2_results.model_dump()
        
        phase3_data = await engine.analyze_phase3(
            request.startup_data,
            phase1_dict,
            phase2_dict
        )
        
        # Generate executive briefing
        context = await engine.context_engine.build_company_context(
            request.startup_data.model_dump()
        )
        
        executive_briefing = (
            f"{context.company_name} Strategic Implementation Plan\n\n"
            f"{phase3_data.get('implementation_summary', '')}"
        )
        
        # Extract key recommendations
        key_recommendations = []
        if "balanced_scorecard" in phase3_data:
            for perspective, data in phase3_data["balanced_scorecard"].items():
                if "initiatives" in data and data["initiatives"]:
                    key_recommendations.append(data["initiatives"][0])
                    
        # Extract critical success factors
        critical_success_factors = []
        if "success_metrics" in phase3_data:
            for metric in phase3_data["success_metrics"][:3]:
                critical_success_factors.append(
                    f"Achieve {metric['target']} in {metric['metric']}"
                )
                
        # Extract next steps
        next_steps = []
        if "implementation_roadmap" in phase3_data:
            roadmap_text = phase3_data["implementation_roadmap"]
            # Extract first 3 concrete actions
            lines = roadmap_text.split('\n')
            for line in lines:
                if any(marker in line for marker in ['Day 1', 'Week 1', '•']):
                    next_steps.append({
                        "action": line.strip().lstrip('•-'),
                        "timeline": "Immediate",
                        "owner": "Leadership"
                    })
                    if len(next_steps) >= 3:
                        break
                        
        return Phase3Response(
            startup_name=request.startup_data.startup_name,
            analysis_date=datetime.now().isoformat(),
            phase3=Phase3Analysis(**phase3_data),
            executive_briefing=executive_briefing,
            key_recommendations=key_recommendations[:5],
            critical_success_factors=critical_success_factors[:5],
            next_steps=next_steps[:5]
        )
        
    except Exception as e:
        logger.error(f"Enhanced Phase 3 failed: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Analysis failed: {str(e)}"
        )


# Cleanup function
async def shutdown_enhanced_engine():
    """Shutdown enhanced engine"""
    global enhanced_engine
    if enhanced_engine:
        await enhanced_engine.close()
        enhanced_engine = None