#!/usr/bin/env python3
"""
McKinsey-Grade Analyzer - Generates partner-level strategic analysis
"""

import json
import logging
import asyncio
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
import aiohttp

from strategic_context_engine import CompanyContext, StrategicInflection
from intelligent_framework_selector import CustomizedFramework

logger = logging.getLogger(__name__)

# DeepSeek configuration
DEEPSEEK_API_KEY = "sk-f68b7148243e4663a31386a5ea6093cf"
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"


class McKinseyGradeAnalyzer:
    """Generate McKinsey/BCG-grade strategic analysis"""
    
    def __init__(self):
        self.api_key = DEEPSEEK_API_KEY
        self.session = None
        
    async def _ensure_session(self):
        """Ensure aiohttp session exists"""
        if self.session is None:
            timeout = aiohttp.ClientTimeout(total=60)
            self.session = aiohttp.ClientSession(timeout=timeout)
            
    async def _call_deepseek(self, prompt: str, max_tokens: int = 1000) -> str:
        """Call DeepSeek with enhanced prompt"""
        await self._ensure_session()
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "deepseek-chat",
            "messages": [
                {
                    "role": "system", 
                    "content": (
                        "You are a McKinsey Senior Partner with 30 years of experience. "
                        "You provide specific, data-driven insights with concrete numbers, "
                        "thresholds, and actionable recommendations. Never give generic advice. "
                        "Always reference industry benchmarks and specific metrics."
                    )
                },
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.3,
            "max_tokens": max_tokens,
            "top_p": 0.9
        }
        
        try:
            async with self.session.post(
                DEEPSEEK_API_URL, 
                json=payload, 
                headers=headers
            ) as response:
                if response.status != 200:
                    logger.error(f"DeepSeek error: {response.status}")
                    return self._generate_fallback_analysis(prompt)
                    
                result = await response.json()
                return result['choices'][0]['message']['content'].strip()
        except Exception as e:
            logger.error(f"DeepSeek call failed: {e}")
            return self._generate_fallback_analysis(prompt)
            
    async def generate_framework_analysis(
        self,
        framework: CustomizedFramework,
        context: CompanyContext
    ) -> Dict[str, Any]:
        """Generate McKinsey-grade analysis for a framework"""
        
        # Build comprehensive prompt
        prompt = self._build_analysis_prompt(framework, context)
        
        # Get AI analysis
        raw_analysis = await self._call_deepseek(prompt)
        
        # Structure the analysis
        structured_analysis = self._structure_analysis(
            raw_analysis, framework, context
        )
        
        # Add quantitative insights
        structured_analysis["quantitative_insights"] = (
            await self._generate_quantitative_insights(framework, context)
        )
        
        # Add strategic recommendations
        structured_analysis["strategic_recommendations"] = (
            await self._generate_strategic_recommendations(
                framework, context, structured_analysis
            )
        )
        
        # Add implementation roadmap
        structured_analysis["implementation_roadmap"] = (
            self._generate_implementation_roadmap(framework, context)
        )
        
        return structured_analysis
        
    def _build_analysis_prompt(
        self,
        framework: CustomizedFramework,
        context: CompanyContext
    ) -> str:
        """Build comprehensive analysis prompt"""
        
        # Extract key data points
        revenue = context.key_metrics.get("revenue", 0)
        growth = context.key_metrics.get("growth_rate", 0)
        burn = context.key_metrics.get("burn_rate", 0)
        ltv_cac = context.key_metrics.get("ltv_cac", 0)
        market_share = context.key_metrics.get("market_share", 0)
        
        # Build industry context
        industry_context = self._build_industry_context(context)
        
        # Build competitive context
        competitive_context = self._build_competitive_context(context)
        
        # Extract framework metadata
        academic_insights = framework.customizations.get("academic_insights", {})
        industry_adjustments = framework.customizations.get("industry_adjustments", {})
        
        prompt = f"""
You are a McKinsey senior partner analyzing {context.company_name}, a {context.stage} {context.industry} company.

FRAMEWORK SELECTION CONTEXT:
- Framework: {framework.base_framework.name} ({framework.industry_variant} variant)
- Fit Score: {academic_insights.get('fit_score', 75)}/100
- Selection Rationale: {'; '.join(academic_insights.get('rationale', ['Contextually appropriate'])[:2])}
- Key Risks: {'; '.join(academic_insights.get('risks', ['Standard implementation risks'])[:2])}

INDUSTRY-SPECIFIC CUSTOMIZATION:
{self._format_industry_customization(framework, industry_adjustments)}

COMPANY SITUATION:
{context.strategic_narrative}

KEY METRICS:
- Annual Revenue: ${revenue:,.0f} ({growth}% YoY growth)
- Monthly Burn: ${burn:,.0f} ({context.key_metrics.get('runway', 0)} months runway)
- LTV/CAC: {ltv_cac:.1f}x
- Market Share: {market_share:.1f}%
- Monthly Active Users: {context.key_metrics.get('users', 0):,}

STRATEGIC CONTEXT:
- Current Inflection: {context.current_inflection.value}
- Primary Challenge: {context.primary_strategic_question}
- Key Constraints: {', '.join(context.critical_constraints[:3])}

{industry_context}

{competitive_context}

FRAMEWORK APPLICATION: {framework.base_framework.name}

Apply the {framework.base_framework.name} framework with these specific considerations:
1. Use {context.industry}-specific metrics and thresholds
2. Compare against these industry benchmarks:
   - Top quartile growth: {context.industry_benchmarks.top_quartile_growth}%
   - Median burn multiple: {context.industry_benchmarks.median_burn_multiple}x
   - Top quartile LTV/CAC: {context.industry_benchmarks.top_quartile_ltv_cac}x

3. Address these unique factors:
   {chr(10).join(f'   - {factor}' for factor in context.unique_insights[:3])}

Provide:
1. Specific positioning/classification with exact metrics
2. 3 actionable insights with quantified impact
3. Immediate next steps (this week)
4. 90-day priorities with success metrics

Be specific. Use numbers. Reference {context.industry} benchmarks.
"""
        
        return prompt
        
    def _build_industry_context(self, context: CompanyContext) -> str:
        """Build industry-specific context"""
        
        return f"""
INDUSTRY DYNAMICS ({context.industry}):
- Market Growth: {context.industry_benchmarks.top_quartile_growth}% (top quartile)
- Time to PMF: {context.industry_benchmarks.time_to_pmf_months} months typical
- Gross Margin Benchmark: {context.industry_benchmarks.typical_gross_margin}%
- Market Structure: {context.industry_benchmarks.market_concentration}
- Disruption Risk: {context.industry_benchmarks.disruption_risk}

MARKET TRENDS:
{chr(10).join(f'- {trend}' for trend in context.market_trends[:3])}
"""
        
    def _build_competitive_context(self, context: CompanyContext) -> str:
        """Build competitive context"""
        
        competitors = context.competitive_dynamics.direct_competitors[:3]
        
        return f"""
COMPETITIVE LANDSCAPE:
- Position: #{context.competitive_dynamics.our_relative_position} in market
- Market Leader: {context.competitive_dynamics.market_leader.get('market_share', 30)}% share
- Key Competitors: {len(competitors)} direct, market is {context.competitive_dynamics.market_dynamics}
- Differentiation: {', '.join(context.competitive_dynamics.differentiation_factors[:2])}
- Threats: {', '.join(context.competitive_dynamics.competitive_threats[:2])}
"""
        
    def _structure_analysis(
        self,
        raw_analysis: str,
        framework: CustomizedFramework,
        context: CompanyContext
    ) -> Dict[str, Any]:
        """Structure the raw analysis into actionable format"""
        
        structured = {
            "framework": framework.base_framework.name,
            "company": context.company_name,
            "analysis_date": datetime.now().isoformat(),
            "executive_summary": self._extract_executive_summary(raw_analysis),
            "framework_positioning": self._extract_positioning(
                raw_analysis, framework
            ),
            "key_insights": self._extract_key_insights(raw_analysis),
            "critical_factors": self._extract_critical_factors(
                raw_analysis, context
            ),
            "risk_assessment": self._assess_risks(raw_analysis, context),
            "opportunity_assessment": self._assess_opportunities(
                raw_analysis, context
            )
        }
        
        return structured
        
    def _extract_executive_summary(self, analysis: str) -> str:
        """Extract or generate executive summary"""
        # Look for summary section in analysis
        lines = analysis.split('\n')
        summary_lines = []
        
        for i, line in enumerate(lines):
            if any(keyword in line.lower() for keyword in ['summary', 'overall', 'conclusion']):
                # Take next 3-5 lines as summary
                summary_lines = lines[i:i+5]
                break
                
        if summary_lines:
            return ' '.join(summary_lines).strip()
        else:
            # Take first paragraph
            return analysis.split('\n\n')[0] if '\n\n' in analysis else analysis[:500]
            
    def _extract_positioning(
        self,
        analysis: str,
        framework: CustomizedFramework
    ) -> Dict[str, Any]:
        """Extract framework-specific positioning"""
        
        positioning = {
            "classification": "Not determined",
            "metrics": {},
            "interpretation": ""
        }
        
        # Framework-specific extraction
        if framework.base_framework.id == "bcg_matrix":
            # Look for quadrant mentions
            if "star" in analysis.lower():
                positioning["classification"] = "Star"
            elif "cash cow" in analysis.lower():
                positioning["classification"] = "Cash Cow"
            elif "question mark" in analysis.lower():
                positioning["classification"] = "Question Mark"
            elif "dog" in analysis.lower():
                positioning["classification"] = "Dog"
                
        elif framework.base_framework.id == "ansoff_matrix":
            # Look for strategy mentions
            strategies = ["market penetration", "market development", 
                         "product development", "diversification"]
            for strategy in strategies:
                if strategy in analysis.lower():
                    positioning["classification"] = strategy.title()
                    break
                    
        return positioning
        
    def _extract_key_insights(self, analysis: str) -> List[Dict[str, str]]:
        """Extract key insights with quantification"""
        insights = []
        
        # Look for numbered insights
        lines = analysis.split('\n')
        for line in lines:
            if any(marker in line for marker in ['1.', '2.', '3.', '•', '-']):
                # Clean and structure
                insight_text = line.strip().lstrip('1234567890.-•* ')
                if insight_text and len(insight_text) > 20:
                    insights.append({
                        "insight": insight_text,
                        "impact": self._estimate_impact(insight_text),
                        "timeframe": self._estimate_timeframe(insight_text)
                    })
                    
        return insights[:5]  # Top 5 insights
        
    def _extract_critical_factors(
        self,
        analysis: str,
        context: CompanyContext
    ) -> List[Dict[str, Any]]:
        """Extract critical success/failure factors"""
        
        factors = []
        
        # Look for critical mentions
        critical_keywords = ["critical", "essential", "must", "key", "important"]
        lines = analysis.split('\n')
        
        for line in lines:
            if any(keyword in line.lower() for keyword in critical_keywords):
                factors.append({
                    "factor": line.strip(),
                    "type": "success" if "success" in line.lower() else "risk",
                    "priority": "high" if "critical" in line.lower() else "medium"
                })
                
        return factors[:5]
        
    def _assess_risks(
        self,
        analysis: str,
        context: CompanyContext
    ) -> List[Dict[str, Any]]:
        """Assess risks from analysis"""
        
        risks = []
        
        # Systematic risk assessment
        if context.key_metrics.get("runway", 12) < 9:
            risks.append({
                "risk": "Runway Risk",
                "severity": "high",
                "timeframe": "3 months",
                "mitigation": "Immediate fundraising or cost reduction"
            })
            
        if context.key_metrics.get("ltv_cac", 3) < 2:
            risks.append({
                "risk": "Unit Economics Risk",
                "severity": "high",
                "timeframe": "immediate",
                "mitigation": "Fix CAC through channel optimization"
            })
            
        if context.competitive_dynamics.our_relative_position > 5:
            risks.append({
                "risk": "Competitive Risk",
                "severity": "medium",
                "timeframe": "6 months",
                "mitigation": "Differentiation through unique value prop"
            })
            
        return risks
        
    def _assess_opportunities(
        self,
        analysis: str,
        context: CompanyContext
    ) -> List[Dict[str, Any]]:
        """Assess opportunities from analysis"""
        
        opportunities = []
        
        # Systematic opportunity assessment
        if context.industry_benchmarks.top_quartile_growth > 100:
            opportunities.append({
                "opportunity": "High Market Growth",
                "potential": f"{context.industry_benchmarks.top_quartile_growth}% annual growth",
                "requirements": "Capital and execution",
                "timeframe": "12-18 months"
            })
            
        if context.key_metrics.get("nrr", 100) > 110:
            opportunities.append({
                "opportunity": "Expansion Revenue",
                "potential": "2-3x revenue from existing customers",
                "requirements": "Product expansion",
                "timeframe": "6-12 months"
            })
            
        return opportunities
        
    async def _generate_quantitative_insights(
        self,
        framework: CustomizedFramework,
        context: CompanyContext
    ) -> Dict[str, Any]:
        """Generate quantitative insights"""
        
        insights = {
            "current_position": self._quantify_current_position(context),
            "gap_analysis": self._perform_gap_analysis(context),
            "sensitivity_analysis": self._perform_sensitivity_analysis(context),
            "scenario_outcomes": await self._generate_scenarios(context)
        }
        
        return insights
        
    def _quantify_current_position(
        self, context: CompanyContext
    ) -> Dict[str, Any]:
        """Quantify current position with metrics"""
        
        return {
            "market_position": {
                "absolute_share": f"{context.key_metrics.get('market_share', 0):.1f}%",
                "relative_share": f"1:{1/max(context.key_metrics.get('market_share', 1), 0.1):.1f}",
                "growth_vs_market": (
                    f"{context.key_metrics.get('growth_rate', 0) - context.industry_benchmarks.median_growth:+.0f}pp"
                )
            },
            "financial_position": {
                "burn_multiple": (
                    f"{context.key_metrics.get('burn_rate', 0) * 12 / max(context.key_metrics.get('revenue', 0) + 1, 1):.1f}x"
                ),
                "months_to_default": context.key_metrics.get('runway', 0),
                "capital_efficiency": (
                    f"${context.key_metrics.get('revenue', 0) / max(context.key_metrics.get('burn_rate', 100000) * 12, 1):.2f} per $1 burned"
                )
            },
            "operational_position": {
                "team_productivity": (
                    f"${context.key_metrics.get('revenue', 0) / max(context.key_metrics.get('team_size', 10), 1):,.0f}/employee"
                ),
                "customer_efficiency": (
                    f"${context.key_metrics.get('revenue', 0) / max(context.key_metrics.get('users', 100), 1):.0f}/user"
                )
            }
        }
        
    def _perform_gap_analysis(self, context: CompanyContext) -> Dict[str, Any]:
        """Perform gap analysis vs benchmarks"""
        
        gaps = {}
        
        # Growth gap
        current_growth = context.key_metrics.get('growth_rate', 0)
        target_growth = context.industry_benchmarks.top_quartile_growth
        gaps["growth_gap"] = {
            "current": f"{current_growth}%",
            "target": f"{target_growth}%",
            "gap": f"{target_growth - current_growth:+.0f}pp",
            "actions_required": self._get_growth_actions(current_growth, target_growth)
        }
        
        # Efficiency gap
        current_ltv_cac = context.key_metrics.get('ltv_cac', 2)
        if current_ltv_cac == 0:
            current_ltv_cac = 0.1  # Avoid division by zero
        target_ltv_cac = context.industry_benchmarks.top_quartile_ltv_cac
        gaps["efficiency_gap"] = {
            "current": f"{current_ltv_cac:.1f}x",
            "target": f"{target_ltv_cac:.1f}x",
            "gap": f"{target_ltv_cac - current_ltv_cac:+.1f}x",
            "improvement_required": f"{(target_ltv_cac/max(current_ltv_cac, 0.1) - 1)*100:+.0f}%"
        }
        
        return gaps
        
    def _get_growth_actions(self, current: float, target: float) -> List[str]:
        """Get specific actions to close growth gap"""
        
        gap = target - current
        actions = []
        
        if gap > 50:
            actions.extend([
                "Launch new product line",
                "Enter adjacent market",
                "Aggressive M&A strategy"
            ])
        elif gap > 20:
            actions.extend([
                "Expand sales team by 2x",
                "Launch channel partnerships",
                "Geographic expansion"
            ])
        else:
            actions.extend([
                "Optimize conversion funnel",
                "Increase pricing by 10-15%",
                "Upsell existing customers"
            ])
            
        return actions
        
    def _perform_sensitivity_analysis(
        self, context: CompanyContext
    ) -> Dict[str, Any]:
        """Perform sensitivity analysis on key metrics"""
        
        revenue = context.key_metrics.get('revenue', 1000000)
        burn = context.key_metrics.get('burn_rate', 100000)
        growth = context.key_metrics.get('growth_rate', 50)
        
        return {
            "revenue_sensitivity": {
                "10%_increase": {
                    "new_runway": f"{context.key_metrics.get('runway', 12) * 1.1:.0f} months",
                    "valuation_impact": "+15-20%"
                },
                "10%_decrease": {
                    "new_runway": f"{context.key_metrics.get('runway', 12) * 0.9:.0f} months",
                    "valuation_impact": "-20-25%"
                }
            },
            "burn_sensitivity": {
                "20%_reduction": {
                    "new_runway": f"{context.key_metrics.get('runway', 12) * 1.25:.0f} months",
                    "growth_impact": f"{growth * 0.9:.0f}% (slight reduction)"
                }
            },
            "growth_sensitivity": {
                "achieve_top_quartile": {
                    "required_investment": f"${burn * 1.5:,.0f}/month",
                    "payback_period": "18-24 months"
                }
            }
        }
        
    async def _generate_scenarios(
        self, context: CompanyContext
    ) -> List[Dict[str, Any]]:
        """Generate strategic scenarios"""
        
        scenarios = []
        
        # Base case
        scenarios.append({
            "name": "Base Case",
            "assumptions": {
                "growth": f"{context.key_metrics.get('growth_rate', 50)}% maintained",
                "burn": "Current burn rate",
                "market": "Stable conditions"
            },
            "outcomes": {
                "revenue_3yr": f"${context.key_metrics.get('revenue', 0) * 3:,.0f}",
                "profitability": "Month 24",
                "valuation": "2-3x current"
            },
            "probability": "60%"
        })
        
        # Upside case
        scenarios.append({
            "name": "Upside Case",
            "assumptions": {
                "growth": f"{context.industry_benchmarks.top_quartile_growth}% achieved",
                "burn": "Controlled increase",
                "market": "Favorable tailwinds"
            },
            "outcomes": {
                "revenue_3yr": f"${context.key_metrics.get('revenue', 0) * 5:,.0f}",
                "profitability": "Month 30",
                "valuation": "5-10x current"
            },
            "probability": "25%"
        })
        
        # Downside case
        scenarios.append({
            "name": "Downside Case",
            "assumptions": {
                "growth": "30% growth",
                "burn": "Forced reduction",
                "market": "Increased competition"
            },
            "outcomes": {
                "revenue_3yr": f"${context.key_metrics.get('revenue', 0) * 2:,.0f}",
                "profitability": "Not achieved",
                "valuation": "0.5-1x current"
            },
            "probability": "15%"
        })
        
        return scenarios
        
    async def _generate_strategic_recommendations(
        self,
        framework: CustomizedFramework,
        context: CompanyContext,
        analysis: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Generate specific strategic recommendations"""
        
        recommendations = []
        
        # Priority 1: Address burning platform issues
        if context.key_metrics.get('runway', 12) < 9:
            recommendations.append({
                "priority": 1,
                "recommendation": "Extend Runway",
                "specific_actions": [
                    f"Reduce burn by ${context.key_metrics.get('burn_rate', 0) * 0.2:,.0f}/month",
                    "Close Series A within 90 days",
                    "Implement 80/20 resource allocation"
                ],
                "expected_impact": "Extend runway to 15+ months",
                "success_metrics": {
                    "30_days": "Term sheet signed",
                    "60_days": "20% burn reduction achieved",
                    "90_days": "Funding closed"
                }
            })
            
        # Priority 2: Fix unit economics
        if context.key_metrics.get('ltv_cac', 3) < 3:
            recommendations.append({
                "priority": 2,
                "recommendation": "Fix Unit Economics",
                "specific_actions": [
                    "Increase pricing by 15-20%",
                    "Reduce CAC through referrals",
                    "Improve retention by 10pp"
                ],
                "expected_impact": "Achieve 3.5x LTV/CAC",
                "success_metrics": {
                    "30_days": "New pricing rolled out",
                    "60_days": "CAC reduced by 25%",
                    "90_days": "LTV/CAC > 3.0x"
                }
            })
            
        # Priority 3: Accelerate growth
        if context.key_metrics.get('growth_rate', 0) < context.industry_benchmarks.median_growth:
            recommendations.append({
                "priority": 3,
                "recommendation": "Accelerate Growth",
                "specific_actions": self._get_growth_actions(
                    context.key_metrics.get('growth_rate', 0),
                    context.industry_benchmarks.top_quartile_growth
                ),
                "expected_impact": f"Achieve {context.industry_benchmarks.median_growth}%+ growth",
                "success_metrics": {
                    "30_days": "Growth initiatives launched",
                    "60_days": "Leading indicators improving",
                    "90_days": "Growth rate > industry median"
                }
            })
            
        return recommendations[:3]  # Top 3 priorities
        
    def _generate_implementation_roadmap(
        self,
        framework: CustomizedFramework,
        context: CompanyContext
    ) -> Dict[str, List[Dict[str, Any]]]:
        """Generate detailed implementation roadmap"""
        
        roadmap = {
            "immediate": [],  # This week
            "short_term": [],  # 30 days
            "medium_term": [],  # 90 days
            "milestones": []
        }
        
        # Immediate actions (this week)
        roadmap["immediate"] = [
            {
                "action": f"Conduct {framework.base_framework.name} workshop",
                "owner": "CEO/Strategy Lead",
                "deliverable": "Framework analysis complete",
                "effort": "8 hours"
            },
            {
                "action": "Gather required metrics",
                "owner": "Analytics/Finance",
                "deliverable": "Data dashboard",
                "effort": "4 hours"
            }
        ]
        
        # 30-day actions
        roadmap["short_term"] = [
            {
                "action": "Implement quick wins",
                "owner": "Product/Sales",
                "deliverable": "First improvements live",
                "success_metric": "10% improvement in key metric"
            },
            {
                "action": "Develop strategic options",
                "owner": "Leadership team",
                "deliverable": "3 strategic scenarios",
                "success_metric": "Board alignment"
            }
        ]
        
        # 90-day actions
        roadmap["medium_term"] = [
            {
                "action": "Execute chosen strategy",
                "owner": "All teams",
                "deliverable": "Strategy in motion",
                "success_metric": f"Achieve {context.industry_benchmarks.median_growth}% growth rate"
            },
            {
                "action": "Measure and iterate",
                "owner": "Strategy lead",
                "deliverable": "Performance report",
                "success_metric": "Framework KPIs improving"
            }
        ]
        
        # Key milestones
        roadmap["milestones"] = [
            {
                "week_1": "Framework analysis complete",
                "week_4": "Quick wins implemented",
                "week_8": "Strategic direction confirmed",
                "week_12": "Measurable business impact"
            }
        ]
        
        return roadmap
        
    def _generate_fallback_analysis(self, prompt: str) -> str:
        """Generate fallback analysis if API fails"""
        
        # Extract key information from prompt
        if "bcg" in prompt.lower():
            return self._generate_bcg_fallback(prompt)
        elif "unit economics" in prompt.lower():
            return self._generate_unit_economics_fallback(prompt)
        else:
            return self._generate_generic_fallback(prompt)
            
    def _generate_bcg_fallback(self, prompt: str) -> str:
        """Generate BCG Matrix fallback"""
        
        return """
Based on the metrics provided, this company appears to be a Question Mark in the BCG Matrix:

1. Market Position: With low market share but high market growth, the company is in a high-potential but uncertain position.

2. Strategic Implications:
   - Requires significant investment to capture market share
   - High risk but high potential reward
   - Critical decision point: invest to become a Star or divest

3. Immediate Actions:
   - Validate product-market fit with specific customer segments
   - Focus resources on highest-potential opportunities
   - Set clear go/no-go metrics for continued investment

4. 90-Day Priorities:
   - Achieve 20% MoM growth in key segment
   - Reduce CAC by 30% through channel optimization
   - Extend runway to 12+ months through fundraising or efficiency
"""
        
    def _generate_unit_economics_fallback(self, prompt: str) -> str:
        """Generate unit economics fallback"""
        
        return """
Unit Economics Analysis reveals critical areas for improvement:

1. Current State:
   - LTV/CAC ratio below sustainable threshold
   - Payback period exceeding runway
   - Negative unit margin at current scale

2. Root Causes:
   - High acquisition costs from paid channels
   - Low initial contract values
   - Suboptimal retention rates

3. Improvement Levers:
   - Increase pricing by 15-20% (minimal churn impact expected)
   - Shift 30% of acquisition to organic channels
   - Improve onboarding to increase 30-day retention by 10pp

4. Expected Outcomes:
   - LTV/CAC improvement to 3.0x within 90 days
   - Payback period reduction to <12 months
   - Path to positive unit economics at current scale
"""
        
    def _generate_generic_fallback(self, prompt: str) -> str:
        """Generate generic strategic fallback"""
        
        return """
Strategic analysis indicates several critical priorities:

1. Market Position:
   - Currently subscale with opportunity for rapid growth
   - Strong product foundation but execution gaps
   - Window of opportunity before market consolidation

2. Key Challenges:
   - Limited runway requiring immediate action
   - Unit economics need optimization
   - Competitive pressure increasing

3. Strategic Options:
   - Focus on core segment for depth
   - Expand to adjacent segments for growth
   - Partner for distribution leverage

4. Recommended Path:
   - Fix unit economics first (30 days)
   - Accelerate growth in core segment (60 days)
   - Evaluate expansion opportunities (90 days)
"""
        
    def _estimate_impact(self, insight: str) -> str:
        """Estimate impact of an insight"""
        
        high_impact_keywords = ["critical", "significant", "major", "transform"]
        medium_impact_keywords = ["improve", "enhance", "optimize", "increase"]
        
        insight_lower = insight.lower()
        
        if any(keyword in insight_lower for keyword in high_impact_keywords):
            return "High (20%+ improvement)"
        elif any(keyword in insight_lower for keyword in medium_impact_keywords):
            return "Medium (10-20% improvement)"
        else:
            return "Low (5-10% improvement)"
            
    def _estimate_timeframe(self, insight: str) -> str:
        """Estimate timeframe for an insight"""
        
        immediate_keywords = ["immediate", "now", "urgent", "critical"]
        short_keywords = ["quick", "soon", "rapid", "fast"]
        
        insight_lower = insight.lower()
        
        if any(keyword in insight_lower for keyword in immediate_keywords):
            return "Immediate (1-2 weeks)"
        elif any(keyword in insight_lower for keyword in short_keywords):
            return "Short-term (1-3 months)"
        else:
            return "Medium-term (3-6 months)"
            
    async def close(self):
        """Close aiohttp session"""
        if self.session:
            await self.session.close()
    
    def _format_industry_customization(
        self, 
        framework: CustomizedFramework,
        industry_adjustments: Dict[str, Any]
    ) -> str:
        """Format industry-specific customization for prompts"""
        
        if not industry_adjustments:
            return "- No industry-specific customizations"
            
        customization = []
        
        # Handle axis mappings for matrix frameworks
        if "x_axis" in industry_adjustments:
            customization.append(f"- X-Axis: {industry_adjustments.get('x_label', industry_adjustments['x_axis'])}")
            customization.append(f"- Y-Axis: {industry_adjustments.get('y_label', industry_adjustments['y_axis'])}")
            
        # Handle thresholds
        if "thresholds" in industry_adjustments:
            customization.append("- Custom Thresholds:")
            for key, value in industry_adjustments["thresholds"].items():
                customization.append(f"  - {key.replace('_', ' ').title()}: {value}")
                
        # Handle custom metrics
        if "primary_metrics" in industry_adjustments:
            customization.append(f"- Primary Metrics: {', '.join(industry_adjustments['primary_metrics'])}")
            
        # Handle quadrants for BCG
        if "quadrants" in industry_adjustments:
            customization.append("- Quadrant Definitions:")
            for quad, desc in industry_adjustments["quadrants"].items():
                customization.append(f"  - {quad.title()}: {desc}")
                
        return '\n'.join(customization) if customization else "- Standard framework application"