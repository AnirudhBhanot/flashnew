#!/usr/bin/env python3
"""
Enhanced Phase 3 Analyzer - McKinsey-grade implementation planning
"""

import logging
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import asyncio

from strategic_context_engine import CompanyContext, StrategicInflection
from mckinsey_grade_analyzer import McKinseyGradeAnalyzer

logger = logging.getLogger(__name__)


class EnhancedPhase3Analyzer:
    """Generate McKinsey-grade Phase 3 implementation analysis"""
    
    def __init__(self):
        self.mckinsey_analyzer = McKinseyGradeAnalyzer()
        
    async def analyze_phase3(
        self,
        company_data: Dict[str, Any],
        context: CompanyContext,
        phase1_insights: Dict[str, Any],
        phase2_strategy: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate comprehensive Phase 3 implementation plan"""
        
        # Build strategic context from previous phases
        strategic_context = self._build_strategic_context(
            phase1_insights, phase2_strategy
        )
        
        # Generate all Phase 3 components with proper context
        tasks = [
            self._create_implementation_roadmap(context, strategic_context),
            self._create_balanced_scorecard(context, strategic_context),
            self._create_okr_framework(context, strategic_context),
            self._create_resource_plan(context, strategic_context),
            self._create_risk_mitigation_plan(context, strategic_context),
            self._create_success_metrics(context, strategic_context)
        ]
        
        results = await asyncio.gather(*tasks)
        
        # Structure Phase 3 response
        phase3_data = {
            "implementation_roadmap": results[0],
            "balanced_scorecard": results[1],
            "okr_framework": results[2],
            "resource_requirements": results[3],
            "risk_mitigation_plan": results[4],
            "success_metrics": results[5]
        }
        
        # Add executive summary
        phase3_data["implementation_summary"] = await self._generate_implementation_summary(
            context, strategic_context, phase3_data
        )
        
        return phase3_data
        
    def _build_strategic_context(
        self,
        phase1: Dict[str, Any],
        phase2: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Build context from previous phases"""
        
        return {
            "current_position": phase1.get("bcg_matrix_analysis", {}).get("position", "Unknown"),
            "key_strengths": [s.get("point", "") for s in phase1.get("swot_analysis", {}).get("strengths", [])],
            "critical_weaknesses": [w.get("point", "") for w in phase1.get("swot_analysis", {}).get("weaknesses", [])],
            "strategic_priorities": phase1.get("swot_analysis", {}).get("strategic_priorities", []),
            "chosen_strategy": phase2.get("ansoff_matrix_analysis", {}).get("recommended_strategy", ""),
            "growth_scenario": phase2.get("growth_scenarios", [{}])[1] if len(phase2.get("growth_scenarios", [])) > 1 else {},  # Base case
            "blue_ocean_moves": phase2.get("blue_ocean_strategy", {}).get("four_actions", {}),
            "recommended_direction": phase2.get("recommended_direction", "")
        }
        
    async def _create_implementation_roadmap(
        self,
        context: CompanyContext,
        strategic_context: Dict[str, Any]
    ) -> str:
        """Create detailed implementation roadmap"""
        
        prompt = f"""
Create a McKinsey-quality 90-day implementation roadmap for {context.company_name}:

STRATEGIC CONTEXT:
- Current Position: {strategic_context['current_position']}
- Chosen Strategy: {strategic_context['chosen_strategy']}
- Key Priorities: {', '.join(strategic_context['strategic_priorities'][:3])}

COMPANY SPECIFICS:
- Stage: {context.stage}
- Industry: {context.industry}
- Team Size: {context.key_metrics.get('team_size', 10)}
- Runway: {context.key_metrics.get('runway', 12)} months
- Monthly Burn: ${context.key_metrics.get('burn_rate', 100000):,.0f}

Create a detailed roadmap with:
1. Week 1-2: Foundation (specific actions, owners, deliverables)
2. Week 3-4: Quick Wins (measurable improvements)
3. Month 2: Core Execution (major initiatives)
4. Month 3: Scale & Optimize (growth acceleration)

Include specific metrics, decision gates, and resource requirements for each phase.
Focus on {context.industry}-specific actions that address their primary challenge:
{context.primary_strategic_question}
"""
        
        roadmap = await self.mckinsey_analyzer._call_deepseek(prompt, max_tokens=800)
        
        # Ensure we have substantive content
        if len(roadmap) < 200:
            roadmap = self._generate_fallback_roadmap(context, strategic_context)
            
        return roadmap
        
    async def _create_balanced_scorecard(
        self,
        context: CompanyContext,
        strategic_context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Create context-aware balanced scorecard"""
        
        # Financial Perspective
        financial = await self._create_financial_perspective(context, strategic_context)
        
        # Customer Perspective
        customer = await self._create_customer_perspective(context, strategic_context)
        
        # Internal Process Perspective
        internal = await self._create_internal_perspective(context, strategic_context)
        
        # Learning & Growth Perspective
        learning = await self._create_learning_perspective(context, strategic_context)
        
        return {
            "financial_perspective": financial,
            "customer_perspective": customer,
            "internal_process_perspective": internal,
            "learning_growth_perspective": learning
        }
        
    async def _create_financial_perspective(
        self,
        context: CompanyContext,
        strategic_context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Create financial perspective with actual targets"""
        
        current_revenue = context.key_metrics.get('revenue', 0)
        burn_rate = context.key_metrics.get('burn_rate', 100000)
        growth_rate = context.key_metrics.get('growth_rate', 0)
        
        # Calculate realistic targets based on stage and industry
        if context.stage in ["pre_seed", "seed"]:
            revenue_target = "$1M ARR" if current_revenue < 1000000 else f"${current_revenue * 2.5 / 1e6:.1f}M ARR"
            burn_target = f"${burn_rate * 0.8:,.0f}" if current_revenue > 0 else f"${burn_rate:,.0f} (maintain)"
        else:
            revenue_target = f"${current_revenue * 2 / 1e6:.1f}M ARR"
            burn_target = f"${burn_rate * 0.7:,.0f}"
            
        return {
            "objectives": [
                f"Achieve {revenue_target} within 12 months",
                "Optimize burn rate for 18+ month runway",
                "Improve unit economics to top quartile"
            ],
            "measures": [
                f"Monthly Revenue (current: ${current_revenue/12:,.0f})",
                f"Burn Multiple (current: {burn_rate*12/max(current_revenue,1):.1f}x)",
                f"LTV/CAC Ratio (current: {context.key_metrics.get('ltv_cac', 2.0):.1f}x)",
                f"Gross Margin (current: {context.key_metrics.get('gross_margin', 70)}%)"
            ],
            "targets": [
                revenue_target,
                burn_target + " monthly burn",
                f"{context.industry_benchmarks.top_quartile_ltv_cac}x LTV/CAC",
                f"{context.industry_benchmarks.typical_gross_margin}% gross margin"
            ],
            "initiatives": [
                self._get_revenue_initiative(context, strategic_context),
                "Implement zero-based budgeting for non-critical spend",
                "Automate high-cost manual processes",
                "Negotiate volume discounts with key vendors"
            ]
        }
        
    def _get_revenue_initiative(
        self,
        context: CompanyContext,
        strategic_context: Dict[str, Any]
    ) -> str:
        """Get specific revenue initiative based on strategy"""
        
        strategy = strategic_context.get('chosen_strategy', 'Market Penetration')
        
        initiatives = {
            "Market Penetration": "Launch high-velocity inside sales team",
            "Market Development": "Enter 2 adjacent geographic markets",
            "Product Development": "Launch premium tier at 2.5x price point",
            "Diversification": "Acquire complementary product line"
        }
        
        return initiatives.get(strategy, "Optimize pricing and packaging")
        
    async def _create_customer_perspective(
        self,
        context: CompanyContext,
        strategic_context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Create customer perspective with specific targets"""
        
        current_users = context.key_metrics.get('users', 1000)
        market_share = context.key_metrics.get('market_share', 0.1)
        
        return {
            "objectives": [
                "Become category leader in target segment",
                "Achieve world-class customer satisfaction",
                "Build sustainable competitive moat"
            ],
            "measures": [
                f"Monthly Active Users (current: {current_users:,})",
                f"Market Share (current: {market_share:.1f}%)",
                "Net Promoter Score",
                "Customer Lifetime Value",
                "Monthly Churn Rate"
            ],
            "targets": [
                f"{current_users * 5:,} MAUs (5x growth)",
                f"{min(market_share * 3, 15):.1f}% market share",
                "NPS > 60 (world-class)",
                f"${context.industry_benchmarks.top_quartile_ltv_cac * 1000:.0f} LTV",
                "< 3% monthly churn"
            ],
            "initiatives": [
                "Launch customer success program for enterprise accounts",
                "Implement product-led growth with viral features",
                "Create customer advisory board",
                "Build community platform for users"
            ]
        }
        
    async def _create_internal_perspective(
        self,
        context: CompanyContext,
        strategic_context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Create internal process perspective"""
        
        return {
            "objectives": [
                "Build scalable operations for 10x growth",
                "Achieve product-market fit in core segment",
                "Create sustainable competitive advantages"
            ],
            "measures": [
                "Product Development Velocity",
                "Customer Onboarding Time",
                "System Uptime",
                "Employee Productivity",
                "Process Automation %"
            ],
            "targets": [
                "Ship weekly releases",
                "< 24 hour onboarding",
                "99.9% uptime SLA",
                f"${context.key_metrics.get('revenue', 0) / max(context.key_metrics.get('team_size', 10), 1) * 2:,.0f} revenue/employee",
                "70% processes automated"
            ],
            "initiatives": [
                "Implement CI/CD pipeline with automated testing",
                "Build self-serve onboarding flow",
                "Migrate to cloud-native architecture",
                "Create operational playbooks for all key processes"
            ]
        }
        
    async def _create_learning_perspective(
        self,
        context: CompanyContext,
        strategic_context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Create learning & growth perspective"""
        
        current_team = context.key_metrics.get('team_size', 10)
        
        return {
            "objectives": [
                "Build world-class team",
                "Foster innovation culture",
                "Develop core competencies for scale"
            ],
            "measures": [
                f"Team Size (current: {current_team})",
                "Employee Net Promoter Score",
                "Skills Coverage %",
                "Innovation Metrics",
                "Leadership Pipeline"
            ],
            "targets": [
                f"{current_team * 2} employees (selective hiring)",
                "eNPS > 50",
                "100% critical skills covered",
                "20% time for innovation",
                "2:1 internal promotion ratio"
            ],
            "initiatives": [
                "Launch employer branding campaign",
                "Implement learning & development program",
                "Create innovation time (Google's 20%)",
                "Build mentorship program"
            ]
        }
        
    async def _create_okr_framework(
        self,
        context: CompanyContext,
        strategic_context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Create OKR framework aligned with strategy"""
        
        prompt = f"""
Create Q1 OKRs for {context.company_name} that directly support their {strategic_context['chosen_strategy']} strategy:

CONTEXT:
- Industry: {context.industry}
- Current Revenue: ${context.key_metrics.get('revenue', 0):,.0f}
- Users: {context.key_metrics.get('users', 0):,}
- Primary Challenge: {context.primary_strategic_question}
- Strategic Priority: {strategic_context['strategic_priorities'][0] if strategic_context['strategic_priorities'] else 'Growth'}

Create 3 objectives with 3-4 measurable key results each.
Make KRs specific with numbers and deadlines.
Focus on {context.industry}-specific metrics.
"""
        
        okr_response = await self.mckinsey_analyzer._call_deepseek(prompt, max_tokens=600)
        
        # Parse response into structured format
        okrs = self._parse_okr_response(okr_response, context)
        
        return {
            "q1": okrs,
            "q2": self._project_q2_okrs(okrs, context),
            "q3": self._project_q3_okrs(okrs, context),
            "q4": self._project_q4_okrs(okrs, context)
        }
        
    def _parse_okr_response(
        self,
        response: str,
        context: CompanyContext
    ) -> Dict[str, Any]:
        """Parse OKR response into structured format"""
        
        # Default OKRs if parsing fails
        default_okrs = {
            "objectives": [
                {
                    "objective": f"Achieve product-market fit in {context.industry}",
                    "key_results": [
                        f"Reach {context.key_metrics.get('users', 1000) * 2:,} active users",
                        f"Achieve {context.industry_benchmarks.median_growth}% MoM growth",
                        "Maintain < 5% monthly churn",
                        "Generate 100+ user testimonials"
                    ]
                },
                {
                    "objective": "Build sustainable unit economics",
                    "key_results": [
                        f"Achieve LTV/CAC > {context.industry_benchmarks.top_quartile_ltv_cac}x",
                        f"Reduce CAC to ${context.key_metrics.get('cac', 1000) * 0.7:.0f}",
                        f"Increase ARPU by 30%",
                        "Achieve positive contribution margin"
                    ]
                },
                {
                    "objective": "Prepare for Series A fundraise",
                    "key_results": [
                        f"Reach ${max(1000000, context.key_metrics.get('revenue', 0) * 3):,.0f} ARR",
                        "Complete SOC2 Type 1 certification",
                        "Build relationships with 20+ A-tier VCs",
                        "Achieve 3 customer case studies"
                    ]
                }
            ]
        }
        
        # Try to parse actual response
        try:
            objectives = []
            current_obj = None
            
            lines = response.split('\n')
            for line in lines:
                if 'objective' in line.lower() and ':' in line:
                    if current_obj:
                        objectives.append(current_obj)
                    current_obj = {
                        "objective": line.split(':', 1)[1].strip(),
                        "key_results": []
                    }
                elif current_obj and any(marker in line for marker in ['KR', '-', '•', '1.', '2.', '3.']):
                    kr_text = line.strip().lstrip('KR123456789.-•* ')
                    if kr_text:
                        current_obj["key_results"].append(kr_text)
                        
            if current_obj:
                objectives.append(current_obj)
                
            return {"objectives": objectives[:3]} if objectives else default_okrs
            
        except:
            return default_okrs
            
    def _project_q2_okrs(self, q1_okrs: Dict, context: CompanyContext) -> Dict[str, Any]:
        """Project Q2 OKRs based on Q1"""
        
        return {
            "objectives": [
                {
                    "objective": "Scale proven playbooks",
                    "key_results": [
                        f"Scale to {context.key_metrics.get('users', 1000) * 5:,} users",
                        "Maintain CAC while doubling volume",
                        "Launch in 2 new segments/geos"
                    ]
                }
            ]
        }
        
    def _project_q3_okrs(self, q1_okrs: Dict, context: CompanyContext) -> Dict[str, Any]:
        """Project Q3 OKRs"""
        
        return {
            "objectives": [
                {
                    "objective": "Achieve market leadership position",
                    "key_results": [
                        "Reach top 3 in category",
                        "Launch platform strategy",
                        "Close Series A funding"
                    ]
                }
            ]
        }
        
    def _project_q4_okrs(self, q1_okrs: Dict, context: CompanyContext) -> Dict[str, Any]:
        """Project Q4 OKRs"""
        
        return {
            "objectives": [
                {
                    "objective": "Prepare for hypergrowth",
                    "key_results": [
                        "Build leadership team",
                        "Achieve operational excellence",
                        "Set foundation for international expansion"
                    ]
                }
            ]
        }
        
    async def _create_resource_plan(
        self,
        context: CompanyContext,
        strategic_context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Create detailed resource requirements"""
        
        current_team = context.key_metrics.get('team_size', 10)
        burn_rate = context.key_metrics.get('burn_rate', 100000)
        runway = context.key_metrics.get('runway', 12)
        
        # Human resources based on strategy
        if strategic_context['chosen_strategy'] == "Market Penetration":
            priority_hires = ["VP Sales", "Sales Engineers", "Customer Success Managers"]
            team_growth = 1.5
        elif strategic_context['chosen_strategy'] == "Product Development":
            priority_hires = ["VP Engineering", "Senior Engineers", "Product Managers"]
            team_growth = 1.8
        else:
            priority_hires = ["VP Marketing", "Growth Lead", "Partnerships Manager"]
            team_growth = 1.4
            
        return {
            "human_resources": {
                "current_team_size": current_team,
                "target_team_size": int(current_team * team_growth),
                "immediate_hires": priority_hires[:2],
                "q1_hires": priority_hires,
                "q2_hires": ["Data Scientist", "Finance Lead", "HR Manager"],
                "total_headcount_eoy": int(current_team * 2),
                "key_skill_gaps": self._identify_skill_gaps(context, strategic_context),
                "hiring_priorities": {
                    "immediate": priority_hires[0],
                    "30_days": priority_hires[1] if len(priority_hires) > 1 else "Sales Lead",
                    "60_days": priority_hires[2] if len(priority_hires) > 2 else "Operations Lead"
                }
            },
            "financial_resources": {
                "current_cash": burn_rate * runway,
                "current_burn": burn_rate,
                "runway_months": runway,
                "funding_required": burn_rate * 18,  # 18 month target
                "funding_timeline": "3-6 months",
                "use_of_funds": {
                    "Product Development": "40%",
                    "Sales & Marketing": "35%",
                    "Operations": "15%",
                    "G&A": "10%"
                },
                "fundraising_milestones": {
                    "30_days": "Complete pitch deck and financial model",
                    "60_days": "First partner meetings",
                    "90_days": "Term sheets",
                    "120_days": "Close funding"
                }
            },
            "technology_resources": {
                "current_infrastructure": self._assess_current_tech(context),
                "required_upgrades": [
                    "Migrate to cloud-native architecture",
                    "Implement CI/CD pipeline",
                    "Add monitoring and observability",
                    "Enhance security posture"
                ],
                "tool_requirements": self._get_tool_requirements(context),
                "estimated_cost": "$50-100k over 6 months",
                "critical_investments": [
                    "Scalable infrastructure",
                    "Data platform",
                    "Security compliance"
                ]
            },
            "operational_resources": {
                "key_processes": [
                    "Sales playbook",
                    "Customer onboarding",
                    "Product development",
                    "Financial planning"
                ],
                "required_systems": [
                    "CRM implementation",
                    "Analytics platform",
                    "HR system",
                    "Financial reporting"
                ],
                "external_support": [
                    "Legal counsel",
                    "Accounting firm",
                    "Recruiting agency",
                    "PR agency"
                ]
            }
        }
        
    def _identify_skill_gaps(
        self,
        context: CompanyContext,
        strategic_context: Dict[str, Any]
    ) -> List[str]:
        """Identify critical skill gaps"""
        
        gaps = []
        
        # Strategy-specific gaps
        if strategic_context['chosen_strategy'] == "Market Penetration":
            gaps.extend(["Enterprise sales", "Channel partnerships", "Sales operations"])
        elif strategic_context['chosen_strategy'] == "Product Development":
            gaps.extend(["AI/ML expertise", "Platform architecture", "DevOps"])
            
        # Stage-specific gaps
        if context.stage in ["seed", "series_a"]:
            gaps.extend(["Financial planning", "People operations", "Data analytics"])
            
        # Industry-specific gaps
        if context.industry == "fintech":
            gaps.append("Regulatory compliance")
        elif context.industry == "healthtech":
            gaps.append("Clinical expertise")
            
        return gaps[:5]
        
    def _assess_current_tech(self, context: CompanyContext) -> str:
        """Assess current technology state"""
        
        if context.stage == "pre_seed":
            return "MVP on basic infrastructure"
        elif context.stage == "seed":
            return "Early product with some technical debt"
        else:
            return "Scaling product with growth challenges"
            
    def _get_tool_requirements(self, context: CompanyContext) -> List[str]:
        """Get required tools based on stage"""
        
        base_tools = ["Monitoring (Datadog)", "Analytics (Amplitude)", "CRM (Salesforce)"]
        
        if context.stage in ["series_a", "series_b"]:
            base_tools.extend(["Data Platform (Snowflake)", "BI Tool (Looker)", "Security (SOC2)"])
            
        return base_tools
        
    async def _create_risk_mitigation_plan(
        self,
        context: CompanyContext,
        strategic_context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Create comprehensive risk mitigation plan"""
        
        risks = []
        
        # Financial risks
        if context.key_metrics.get('runway', 12) < 12:
            risks.append({
                "risk": "Cash runway depletion",
                "impact": "Critical",
                "probability": "High" if context.key_metrics.get('runway', 12) < 9 else "Medium",
                "mitigation": "Raise bridge round within 60 days or reduce burn by 30%",
                "owner": "CEO/CFO",
                "timeline": "Immediate",
                "success_metric": "Extend runway to 15+ months"
            })
            
        # Market risks
        if context.competitive_dynamics.our_relative_position > 3:
            risks.append({
                "risk": "Competitive displacement",
                "impact": "High",
                "probability": "Medium",
                "mitigation": "Accelerate product differentiation and lock in key accounts",
                "owner": "CPO/CTO",
                "timeline": "90 days",
                "success_metric": "Win 3 lighthouse customers from competitors"
            })
            
        # Operational risks
        if context.key_metrics.get('team_size', 10) < 20:
            risks.append({
                "risk": "Key person dependency",
                "impact": "High",
                "probability": "Medium",
                "mitigation": "Document critical processes and cross-train team",
                "owner": "COO",
                "timeline": "30 days",
                "success_metric": "All critical functions have backup coverage"
            })
            
        # Technical risks
        risks.append({
            "risk": "Technical scalability limits",
            "impact": "Medium",
            "probability": "Low" if context.stage == "seed" else "Medium",
            "mitigation": "Conduct architecture review and implement auto-scaling",
            "owner": "CTO",
            "timeline": "60 days",
            "success_metric": "System handles 10x current load"
        })
        
        # Strategic risks
        if strategic_context['chosen_strategy'] == "Diversification":
            risks.append({
                "risk": "Strategy execution failure",
                "impact": "High",
                "probability": "Medium",
                "mitigation": "Set clear stage gates and success metrics",
                "owner": "CEO",
                "timeline": "Ongoing",
                "success_metric": "Hit 80% of quarterly milestones"
            })
            
        return {
            "top_risks": risks,
            "risk_monitoring": {
                "frequency": "Weekly leadership review",
                "dashboard": "Real-time risk indicators",
                "escalation": "Board notification for critical risks"
            },
            "contingency_plans": {
                "financial": "Bridge round or aggressive cost cutting",
                "market": "Pivot to adjacent segment",
                "operational": "Advisor/consultant support",
                "technical": "Cloud migration or re-architecture"
            }
        }
        
    async def _create_success_metrics(
        self,
        context: CompanyContext,
        strategic_context: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Create specific success metrics with targets"""
        
        metrics = []
        
        # Growth metrics
        current_revenue = context.key_metrics.get('revenue', 0)
        metrics.append({
            "metric": "Monthly Recurring Revenue",
            "current": f"${current_revenue/12:,.0f}",
            "target": f"${current_revenue/12 * 1.3:,.0f}",
            "frequency": "Weekly",
            "owner": "VP Sales",
            "leading_indicators": ["Pipeline velocity", "Demo conversion rate"]
        })
        
        # Efficiency metrics
        metrics.append({
            "metric": "LTV/CAC Ratio",
            "current": f"{context.key_metrics.get('ltv_cac', 2.0):.1f}x",
            "target": f"{context.industry_benchmarks.top_quartile_ltv_cac}x",
            "frequency": "Monthly",
            "owner": "VP Marketing",
            "leading_indicators": ["CAC by channel", "Retention cohorts"]
        })
        
        # Product metrics
        metrics.append({
            "metric": "Product-Market Fit Score",
            "current": "TBD",
            "target": "> 40% would be very disappointed",
            "frequency": "Quarterly",
            "owner": "VP Product",
            "leading_indicators": ["NPS", "Feature adoption", "User engagement"]
        })
        
        # Operational metrics
        metrics.append({
            "metric": "Burn Multiple",
            "current": f"{context.key_metrics.get('burn_rate', 100000) * 12 / max(current_revenue + 1, 1):.1f}x",
            "target": f"< {context.industry_benchmarks.median_burn_multiple}x",
            "frequency": "Monthly",
            "owner": "CFO",
            "leading_indicators": ["Gross margin", "OpEx ratio"]
        })
        
        # Strategic metrics
        metrics.append({
            "metric": "Market Share",
            "current": f"{context.key_metrics.get('market_share', 0.1):.1f}%",
            "target": f"{min(context.key_metrics.get('market_share', 0.1) * 3, 10):.1f}%",
            "frequency": "Quarterly",
            "owner": "CEO",
            "leading_indicators": ["Win rate", "Customer acquisition"]
        })
        
        return metrics
        
    async def _generate_implementation_summary(
        self,
        context: CompanyContext,
        strategic_context: Dict[str, Any],
        phase3_data: Dict[str, Any]
    ) -> str:
        """Generate executive summary of implementation plan"""
        
        prompt = f"""
Write a 2-3 paragraph executive summary of the implementation plan for {context.company_name}:

STRATEGIC CONTEXT:
- Current Position: {strategic_context['current_position']} 
- Chosen Strategy: {strategic_context['chosen_strategy']}
- Primary Goal: Address "{context.primary_strategic_question}"

KEY IMPLEMENTATION ELEMENTS:
- Team Growth: {phase3_data['resource_requirements']['human_resources']['current_team_size']} → {phase3_data['resource_requirements']['human_resources']['target_team_size']}
- Funding Need: ${phase3_data['resource_requirements']['financial_resources']['funding_required']:,.0f}
- Top Risk: {phase3_data['risk_mitigation_plan']['top_risks'][0]['risk'] if phase3_data['risk_mitigation_plan']['top_risks'] else 'Execution risk'}
- Success Metric: {phase3_data['success_metrics'][0]['metric']} to {phase3_data['success_metrics'][0]['target']}

Make it specific, actionable, and focused on the next 90 days.
Reference {context.industry} best practices and benchmarks.
"""
        
        summary = await self.mckinsey_analyzer._call_deepseek(prompt, max_tokens=400)
        
        if len(summary) < 100:
            summary = self._generate_fallback_summary(context, strategic_context, phase3_data)
            
        return summary
        
    def _generate_fallback_roadmap(
        self,
        context: CompanyContext,
        strategic_context: Dict[str, Any]
    ) -> str:
        """Generate fallback roadmap if API fails"""
        
        return f"""
90-Day Implementation Roadmap for {context.company_name}

WEEK 1-2: FOUNDATION
• Day 1-3: Leadership alignment on {strategic_context['chosen_strategy']} strategy
  - Owner: CEO
  - Deliverable: Strategy one-pager and success metrics
  
• Day 4-7: Resource audit and gap analysis  
  - Owner: COO
  - Deliverable: Skills matrix and hiring priorities
  
• Day 8-14: Quick wins identification
  - Owner: Product/Sales leads
  - Deliverable: 5 improvements implementable in 30 days

WEEK 3-4: QUICK WINS
• Pricing optimization: Increase prices 15% on new customers
  - Expected impact: ${context.key_metrics.get('revenue', 1000000) * 0.15 / 12:,.0f}/month
  
• Sales process improvement: Implement qualification framework
  - Expected impact: 25% improvement in close rate
  
• Product enhancement: Ship top 3 customer requests
  - Expected impact: 10% reduction in churn

MONTH 2: CORE EXECUTION
• Hire {strategic_context.get('priority_hires', ['VP Sales'])[0]}
• Launch {strategic_context['chosen_strategy'].lower()} initiatives
• Implement weekly metrics review
• Begin Series A fundraising process

MONTH 3: SCALE & OPTIMIZE
• Double down on working initiatives
• Kill underperforming experiments
• Achieve rhythm of execution
• Close key hires and partnerships

Success Criteria:
- 30% improvement in primary growth metric
- 2 key hires closed
- Fundraising process launched
- Team aligned and executing
"""
        
    def _generate_fallback_summary(
        self,
        context: CompanyContext,
        strategic_context: Dict[str, Any],
        phase3_data: Dict[str, Any]
    ) -> str:
        """Generate fallback summary if API fails"""
        
        return f"""
{context.company_name} is at a critical inflection point as a {strategic_context['current_position']} in the {context.industry} market. The 90-day implementation plan focuses on executing the {strategic_context['chosen_strategy']} strategy to address the primary challenge of {context.primary_strategic_question.lower()}.

The plan requires growing the team from {phase3_data['resource_requirements']['human_resources']['current_team_size']} to {phase3_data['resource_requirements']['human_resources']['target_team_size']} people, with immediate hires in {', '.join(phase3_data['resource_requirements']['human_resources']['immediate_hires'][:2])}. Financial requirements include raising ${phase3_data['resource_requirements']['financial_resources']['funding_required']/1e6:.1f}M to extend runway to 18 months while executing the growth plan.

Success will be measured by achieving {phase3_data['success_metrics'][0]['target']} in {phase3_data['success_metrics'][0]['metric']}, while maintaining discipline on unit economics. The biggest risk is {phase3_data['risk_mitigation_plan']['top_risks'][0]['risk']}, which will be mitigated through {phase3_data['risk_mitigation_plan']['top_risks'][0]['mitigation'].lower()}. With focused execution, {context.company_name} can achieve market leadership in their segment within 12-18 months.
"""
        
    async def close(self):
        """Close resources"""
        await self.mckinsey_analyzer.close()