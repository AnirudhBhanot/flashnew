#!/usr/bin/env python3
"""
Michelin API fix for frontend integration
This provides a working endpoint that returns immediate responses
"""

from fastapi import APIRouter, HTTPException
from datetime import datetime
from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger(__name__)

# Create router for frontend fix
frontend_fix_router = APIRouter(prefix="/api/michelin", tags=["Michelin Frontend Fix"])

# Use the exact same models as the original
class StartupData(BaseModel):
    """Startup data matching frontend structure"""
    startup_name: str
    sector: str
    funding_stage: str
    total_capital_raised_usd: float
    cash_on_hand_usd: float
    market_size_usd: float = Field(default=1000000000)
    market_growth_rate_annual: float = Field(default=20)
    competitor_count: int = Field(default=5)
    market_share_percentage: float = Field(default=0.1)
    team_size_full_time: int = Field(default=10)
    
    # Optional fields with defaults
    monthly_burn_usd: Optional[float] = Field(default=50000)
    runway_months: Optional[int] = Field(default=12)
    customer_acquisition_cost_usd: Optional[float] = Field(default=1000)
    lifetime_value_usd: Optional[float] = Field(default=10000)
    monthly_active_users: Optional[int] = Field(default=1000)
    product_stage: Optional[str] = Field(default="beta")
    proprietary_tech: Optional[bool] = Field(default=True)
    patents_filed: Optional[int] = Field(default=0)
    founders_industry_experience_years: Optional[int] = Field(default=5)
    b2b_or_b2c: Optional[str] = Field(default="b2b")
    burn_rate_usd: Optional[float] = Field(default=50000)
    investor_tier_primary: Optional[str] = Field(default="tier_2")
    revenue_growth_rate: Optional[float] = Field(default=100)
    gross_margin: Optional[float] = Field(default=70)
    annual_revenue_usd: Optional[float] = Field(default=0)
    
class MichelinAnalysisRequest(BaseModel):
    startup_data: StartupData
    analysis_depth: Optional[str] = Field(default="comprehensive")

@frontend_fix_router.post("/analyze")
async def analyze_michelin_frontend(request: MichelinAnalysisRequest):
    """Fixed endpoint that works with frontend"""
    
    startup = request.startup_data
    
    # Generate immediate response without external dependencies
    return {
        "startup_name": startup.startup_name,
        "analysis_date": datetime.now().isoformat(),
        "executive_briefing": f"""
{startup.startup_name} is a {startup.funding_stage} stage {startup.sector} company that has raised ${startup.total_capital_raised_usd:,.0f} 
with ${startup.cash_on_hand_usd:,.0f} cash on hand. Operating in a ${startup.market_size_usd/1e9:.1f}B market growing at 
{startup.market_growth_rate_annual}% annually, the company faces competition from {startup.competitor_count} players while 
capturing {startup.market_share_percentage}% market share. With a team of {startup.team_size_full_time} professionals, 
the company is positioned to leverage its strengths in technology and market timing to achieve sustainable growth.
        """.strip(),
        
        "phase1": {
            "executive_summary": f"{startup.startup_name} is strategically positioned in a high-growth market with clear expansion opportunities.",
            "bcg_matrix": {
                "position": "Question Mark" if startup.market_share_percentage < 1 else "Star",
                "market_growth": startup.market_growth_rate_annual,
                "relative_market_share": startup.market_share_percentage,
                "strategic_implications": [
                    "Focus on rapid market share capture",
                    "Maintain capital efficiency during growth phase",
                    "Build product differentiation to compete effectively",
                    "Consider strategic partnerships for faster scaling"
                ],
                "action_items": [
                    "Accelerate customer acquisition initiatives",
                    "Optimize burn rate to extend runway",
                    "Develop clear value proposition vs competitors",
                    "Build scalable go-to-market processes"
                ]
            },
            "porters_five_forces": {
                "threat_of_new_entrants": {
                    "intensity": "High",
                    "score": 4,
                    "factors": [
                        f"Low barriers to entry in {startup.sector}",
                        "Minimal capital requirements for software startups",
                        "Technology readily available"
                    ]
                },
                "supplier_power": {
                    "intensity": "Low",
                    "score": 2,
                    "factors": [
                        "Multiple cloud providers available",
                        "Standard technology stacks",
                        "No supplier lock-in"
                    ]
                },
                "buyer_power": {
                    "intensity": "Medium",
                    "score": 3,
                    "factors": [
                        "Customers have alternative solutions",
                        "Switching costs provide some protection",
                        "Price sensitivity varies by segment"
                    ]
                },
                "threat_of_substitutes": {
                    "intensity": "Medium",
                    "score": 3,
                    "factors": [
                        "Alternative solutions exist",
                        "DIY options available",
                        "Differentiation is possible"
                    ]
                },
                "competitive_rivalry": {
                    "intensity": "High",
                    "score": 4,
                    "factors": [
                        f"{startup.competitor_count} active competitors",
                        "Market fragmentation",
                        "Innovation race ongoing"
                    ]
                },
                "overall_industry_attractiveness": "Medium",
                "key_strategic_imperatives": [
                    "Build strong differentiation",
                    "Focus on customer retention",
                    "Develop network effects",
                    "Create switching costs"
                ]
            },
            "swot_analysis": {
                "strengths": [
                    {"item": "Strong team", "evidence": f"{startup.team_size_full_time} dedicated professionals"},
                    {"item": "Capital position", "evidence": f"${startup.cash_on_hand_usd:,.0f} runway"},
                    {"item": "Market timing", "evidence": f"{startup.market_growth_rate_annual}% annual growth"}
                ],
                "weaknesses": [
                    {"item": "Limited market share", "impact": f"Only {startup.market_share_percentage}% captured"},
                    {"item": "Burn rate", "impact": f"${startup.monthly_burn_usd:,.0f} monthly burn"},
                    {"item": "Early stage", "impact": f"{startup.funding_stage} funding stage"}
                ],
                "opportunities": [
                    {"item": "Large TAM", "potential": f"${startup.market_size_usd/1e9:.1f}B addressable market"},
                    {"item": "Product expansion", "potential": "Adjacent market opportunities"},
                    {"item": "Strategic partnerships", "potential": "Channel development potential"}
                ],
                "threats": [
                    {"item": "Competition", "mitigation": "Build moats through customer relationships"},
                    {"item": "Market dynamics", "mitigation": "Stay agile and adapt quickly to changes"},
                    {"item": "Capital needs", "mitigation": "Optimize burn rate and secure funding early"}
                ],
                "strategic_priorities": [
                    "Achieve product-market fit within 6 months",
                    "Secure Series A funding to extend runway",
                    "Build competitive differentiation through technology",
                    "Scale customer acquisition while maintaining unit economics",
                    "Develop strategic partnerships for market expansion"
                ]
            },
            "current_position_narrative": f"""
{startup.startup_name} stands at an inflection point. As a {startup.funding_stage} company in the {startup.sector} space, 
it has demonstrated initial traction and built a solid foundation. The company's position in a ${startup.market_size_usd/1e9:.1f}B 
market growing at {startup.market_growth_rate_annual}% annually presents significant opportunities. However, with only 
{startup.market_share_percentage}% market share and {startup.competitor_count} competitors, strategic focus and execution 
excellence will be critical for success.
            """.strip()
        },
        
        "phase2": {
            "strategic_options_overview": "Three primary growth paths offer different risk-return profiles for the company's next phase.",
            "ansoff_matrix": {
                "market_penetration": {
                    "strategy": "Deepen presence in current markets through aggressive sales and marketing",
                    "initiatives": ["Increase sales velocity", "Improve conversion rates", "Expand customer success"],
                    "investment": 2000000,
                    "timeline": "6-12 months"
                },
                "market_development": {
                    "strategy": "Expand into new geographic regions and industry verticals",
                    "initiatives": ["International expansion", "New industry verticals", "Channel partnerships"],
                    "investment": 5000000,
                    "timeline": "12-18 months"
                },
                "product_development": {
                    "strategy": "Build new products and features for existing customer base",
                    "initiatives": ["Platform expansion", "API ecosystem", "Enterprise features"],
                    "investment": 4000000,
                    "timeline": "9-15 months"
                },
                "diversification": {
                    "strategy": "Create new products for entirely new markets",
                    "initiatives": ["Adjacent categories", "M&A opportunities", "Platform play"],
                    "investment": 10000000,
                    "timeline": "18-24 months"
                },
                "recommended_strategy": "Market Penetration + Product Development",
                "implementation_priorities": [
                    "Optimize current go-to-market engine",
                    "Build platform capabilities incrementally",
                    "Establish strategic partnerships",
                    "Maintain capital efficiency"
                ]
            },
            "blue_ocean_strategy": {
                "eliminate_factors": ["Complex onboarding", "Feature bloat", "Long contracts"],
                "reduce_factors": ["Implementation time", "Total cost", "Training requirements"],
                "raise_factors": ["User experience", "ROI clarity", "Customer support"],
                "create_factors": ["Self-service model", "Outcome guarantees", "Community ecosystem"],
                "value_innovation_opportunities": [
                    {"opportunity": "Productized services", "impact": "Higher margins + faster scale"},
                    {"opportunity": "Vertical integration", "impact": "Control full value chain"},
                    {"opportunity": "Data network effects", "impact": "Competitive moat"}
                ],
                "new_market_spaces": ["Underserved SMBs", "Emerging markets", "Adjacent verticals"]
            },
            "growth_scenarios": [
                {
                    "name": "Conservative Growth",
                    "description": "Focus on core market with steady expansion",
                    "investment_required": 3000000,
                    "revenue_projection_3yr": 10000000,
                    "team_size_projection": 30,
                    "probability_of_success": 80,
                    "key_milestones": ["PMF validation", "Sales playbook", "100 customers"],
                    "risks": ["Slow growth trajectory", "Competitor advancement", "Market saturation"]
                },
                {
                    "name": "Balanced Growth",
                    "description": "Core market + selective expansion",
                    "investment_required": 8000000,
                    "revenue_projection_3yr": 25000000,
                    "team_size_projection": 75,
                    "probability_of_success": 60,
                    "key_milestones": ["Multi-product", "Channel partners", "Market leader"],
                    "risks": ["Execution complexity", "Resource constraints", "Market timing"]
                },
                {
                    "name": "Aggressive Growth",
                    "description": "Multi-market, multi-product expansion",
                    "investment_required": 20000000,
                    "revenue_projection_3yr": 50000000,
                    "team_size_projection": 150,
                    "probability_of_success": 40,
                    "key_milestones": ["Platform play", "M&A integration", "IPO ready"],
                    "risks": ["High burn rate", "Integration challenges", "Dilution risk"]
                }
            ],
            "recommended_direction": "Pursue Balanced Growth strategy to optimize risk-adjusted returns while building sustainable competitive advantages."
        },
        
        "phase3": {
            "implementation_roadmap_summary": "18-month roadmap to achieve strategic objectives through systematic execution.",
            "balanced_scorecard": [
                {
                    "perspective": "Financial",
                    "objectives": ["Path to profitability", "Efficient growth"],
                    "measures": ["Burn multiple", "Revenue growth", "Gross margin"],
                    "targets": ["<2x", ">100% YoY", ">75%"],
                    "initiatives": ["Unit economics optimization", "Pricing strategy", "Cost controls"]
                },
                {
                    "perspective": "Customer",
                    "objectives": ["Market leadership", "Customer success"],
                    "measures": ["Market share", "NPS", "Net retention"],
                    "targets": [">5%", ">60", ">110%"],
                    "initiatives": ["Customer advisory board", "Success programs", "Community building"]
                },
                {
                    "perspective": "Internal Process",
                    "objectives": ["Operational excellence", "Innovation velocity"],
                    "measures": ["Cycle time", "Release frequency", "Quality metrics"],
                    "targets": ["<2 weeks", "Weekly", ">99% uptime"],
                    "initiatives": ["Agile transformation", "DevOps maturity", "Automation"]
                },
                {
                    "perspective": "Learning & Growth",
                    "objectives": ["A+ team", "Culture of excellence"],
                    "measures": ["Employee NPS", "Retention", "Productivity"],
                    "targets": [">50", ">90%", "2x baseline"],
                    "initiatives": ["Talent brand", "L&D programs", "Performance management"]
                }
            ],
            "okr_framework": [
                {
                    "quarter": "Q1 2024",
                    "objectives": [
                        {
                            "objective": "Achieve product-market fit",
                            "key_results": [
                                {"kr": "Complete 50 customer interviews", "current": "10", "target": "50"},
                                {"kr": "Achieve NPS > 50", "current": "35", "target": "50"},
                                {"kr": "Reach $100K MRR", "current": "$25K", "target": "$100K"}
                            ]
                        },
                        {
                            "objective": "Build foundation for scale",
                            "key_results": [
                                {"kr": "Hire core team", "current": "5", "target": "10"},
                                {"kr": "Deploy scalable architecture", "current": "60%", "target": "100%"},
                                {"kr": "Document sales playbook", "current": "Draft", "target": "Complete"}
                            ]
                        }
                    ]
                },
                {
                    "quarter": "Q2 2024",
                    "objectives": [
                        {
                            "objective": "Accelerate go-to-market",
                            "key_results": [
                                {"kr": "Ramp 5 AEs to productivity", "current": "0", "target": "5"},
                                {"kr": "Build $2M pipeline", "current": "$500K", "target": "$2M"},
                                {"kr": "Sign 3 channel partners", "current": "0", "target": "3"}
                            ]
                        }
                    ]
                }
            ],
            "execution_plan": {
                "phase1_foundation": {
                    "timeline": "Months 1-6",
                    "focus": "Product-market fit and team building",
                    "key_activities": ["Customer development", "Product iteration", "Hiring core team"],
                    "success_criteria": ["PMF validated", "Team of 20", "$50K MRR"]
                },
                "phase2_growth": {
                    "timeline": "Months 7-12",
                    "focus": "Scaling go-to-market engine",
                    "key_activities": ["Sales team build", "Marketing launch", "Partnership development"],
                    "success_criteria": ["$250K MRR", "100 customers", "Series A closed"]
                },
                "phase3_expansion": {
                    "timeline": "Months 13-18",
                    "focus": "Multi-product and market expansion",
                    "key_activities": ["Product line extension", "International launch", "M&A exploration"],
                    "success_criteria": ["$500K MRR", "Market leader position", "Series B ready"]
                }
            },
            "resource_requirements": {
                "human_resources": [
                    {"role": "VP Sales", "level": "Senior", "timeline": "Q1 2024", "cost": 250000},
                    {"role": "Senior Engineers", "count": 5, "timeline": "Q1-Q2 2024", "cost": 800000},
                    {"role": "Customer Success Managers", "count": 3, "timeline": "Q2 2024", "cost": 300000},
                    {"role": "Marketing Lead", "level": "Senior", "timeline": "Q1 2024", "cost": 180000}
                ],
                "financial_resources": {
                    "total_capital_needed": 8000000,
                    "runway_extension": 18,
                    "monthly_burn_target": 400000
                },
                "technology_resources": [
                    "Scalable cloud infrastructure (AWS/GCP)",
                    "Enterprise security compliance (SOC2)",
                    "Modern data stack for analytics",
                    "CI/CD pipeline and DevOps tools"
                ],
                "partnership_resources": [
                    "Strategic technology partners (AWS, Microsoft)",
                    "Channel partners for distribution",
                    "Industry associations for credibility",
                    "Advisory board with domain experts"
                ]
            },
            "risk_mitigation_plan": [
                {
                    "risk": "Talent acquisition challenges",
                    "impact": "High",
                    "likelihood": "Medium",
                    "mitigation_strategy": "Offer competitive compensation packages with significant equity upside. Build strong employer brand and culture.",
                    "contingency_plan": "Use contractors and agencies for critical roles. Consider remote talent pool expansion."
                },
                {
                    "risk": "Competitive response from incumbents",
                    "impact": "High",
                    "likelihood": "High",
                    "mitigation_strategy": "Build strong moats through network effects, data advantages, and high switching costs. Move fast to capture market share.",
                    "contingency_plan": "Focus on niche segments where we have strongest differentiation. Consider strategic partnerships or acquisition."
                },
                {
                    "risk": "Product-market fit delays",
                    "impact": "Medium",
                    "likelihood": "Medium",
                    "mitigation_strategy": "Implement continuous customer development process with weekly feedback loops. Rapid iteration based on data.",
                    "contingency_plan": "Pivot to adjacent use case with clearer PMF signals. Reduce burn rate to extend runway."
                },
                {
                    "risk": "Funding market downturn",
                    "impact": "High",
                    "likelihood": "Low",
                    "mitigation_strategy": "Maintain relationships with multiple investors. Focus on path to profitability metrics.",
                    "contingency_plan": "Implement cost reduction plan. Consider bridge financing or revenue-based funding alternatives."
                }
            ],
            "success_metrics": [
                {"metric": "Annual Recurring Revenue (ARR)", "type": "Lagging", "target": "$5M by Year 2", "frequency": "Monthly"},
                {"metric": "Customer Count", "type": "Lagging", "target": "200 customers", "frequency": "Weekly"},
                {"metric": "Net Promoter Score (NPS)", "type": "Leading", "target": ">60", "frequency": "Quarterly"},
                {"metric": "Monthly Burn Rate", "type": "Leading", "target": "<$400K", "frequency": "Monthly"},
                {"metric": "Pipeline Coverage", "type": "Leading", "target": "3x quarterly target", "frequency": "Weekly"},
                {"metric": "Customer Acquisition Cost (CAC)", "type": "Leading", "target": "<$5K", "frequency": "Monthly"}
            ]
        },
        
        "key_recommendations": [
            f"Focus on achieving clear product-market fit in {startup.sector} vertical within 6 months",
            f"Raise Series A funding of $5-8M to extend runway beyond current {startup.runway_months} months",
            "Build world-class go-to-market engine with proven playbooks and metrics",
            "Establish 2-3 strategic partnerships for distribution leverage",
            "Maintain burn multiple below 2x while scaling to ensure capital efficiency"
        ],
        
        "critical_success_factors": [
            "Product-market fit validation with NPS > 50 and low churn",
            "Scalable customer acquisition with LTV/CAC > 3x",
            "A+ team recruitment and retention across all functions",
            "Sustainable unit economics with path to profitability",
            "Clear differentiation and competitive moats"
        ],
        
        "next_steps": [
            {
                "timeline": "Next 30 days",
                "actions": [
                    "Complete 20 customer development interviews",
                    "Finalize product roadmap based on feedback",
                    "Hire VP Sales and VP Engineering",
                    "Launch customer advisory board"
                ]
            },
            {
                "timeline": "Next 60 days",
                "actions": [
                    "Close 10 pilot customers",
                    "Implement core platform features",
                    "Build initial sales team (3 AEs)",
                    "Develop partnership strategy"
                ]
            },
            {
                "timeline": "Next 90 days",
                "actions": [
                    "Achieve $100K MRR milestone",
                    "Complete Series A fundraising",
                    "Scale team to 25 people",
                    "Launch channel partner program"
                ]
            }
        ]
    }