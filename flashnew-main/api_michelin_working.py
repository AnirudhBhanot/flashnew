#!/usr/bin/env python3
"""
Working Michelin API that provides immediate fallback responses
"""

import logging
from fastapi import APIRouter, HTTPException
from datetime import datetime
from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional

# Create a new router
working_michelin_router = APIRouter(prefix="/api/michelin-working", tags=["Working Michelin Analysis"])

logger = logging.getLogger(__name__)

# Simplified models to avoid field issues
class SimpleStartupData(BaseModel):
    """Simplified startup data for analysis"""
    startup_name: str
    sector: str
    funding_stage: str
    annual_revenue_usd: float = 0
    runway_months: int = 12
    team_size_full_time: int = 1
    market_size_usd: float = 1000000000
    competitor_count: int = 5
    
class SimpleAnalysisRequest(BaseModel):
    """Request for Michelin-style analysis"""
    startup_data: SimpleStartupData
    
@working_michelin_router.post("/analyze")
async def analyze_startup_working(request: SimpleAnalysisRequest):
    """Working version of Michelin analysis with immediate response"""
    
    # Extract basic data safely
    startup = request.startup_data
    name = startup.startup_name
    sector = startup.sector
    stage = startup.funding_stage
    revenue = startup.annual_revenue_usd
    runway = startup.runway_months
    team_size = startup.team_size_full_time
    market_size = startup.market_size_usd
    competitors = startup.competitor_count
    
    # Generate response immediately without DeepSeek
    return {
        "startup_name": name,
        "analysis_date": datetime.now().isoformat(),
        "executive_briefing": f"""
        {name} is a {stage} stage {sector} company with significant growth potential in a ${market_size/1e9:.1f}B market.
        With {team_size} team members and {runway} months of runway, the company is positioned to capture market share
        through strategic initiatives. The competitive landscape includes {competitors} players, creating both challenges
        and opportunities for differentiation. Key focus areas include product-market fit, scalable go-to-market strategy,
        and sustainable unit economics.
        """,
        "phase1": {
            "executive_summary": f"{name} operates in the {sector} sector with clear opportunities for growth.",
            "bcg_matrix_analysis": {
                "position": "Question Mark" if revenue < 1000000 else "Star",
                "market_growth_rate": "High",
                "relative_market_share": "Low" if revenue < 1000000 else "Medium",
                "strategic_implications": "Focus on market share capture while maintaining capital efficiency."
            },
            "porters_five_forces": {
                "threat_of_new_entrants": {"level": "High", "analysis": f"Low barriers in {sector} sector"},
                "supplier_power": {"level": "Low", "analysis": "Multiple supplier options available"},
                "buyer_power": {"level": "Medium", "analysis": "Buyers have moderate negotiating power"},
                "threat_of_substitutes": {"level": "Medium", "analysis": "Alternative solutions exist"},
                "competitive_rivalry": {"level": "High", "analysis": f"{competitors} active competitors"}
            },
            "swot_analysis": {
                "strengths": [
                    {"point": "Agile team", "evidence": f"{team_size} focused team members"},
                    {"point": "Market timing", "evidence": f"Early in ${market_size/1e9:.1f}B market"},
                    {"point": "Capital efficiency", "evidence": f"{runway} months runway"}
                ],
                "weaknesses": [
                    {"point": "Limited resources", "evidence": f"Small team of {team_size}"},
                    {"point": "Market position", "evidence": "Early stage presence"},
                    {"point": "Brand recognition", "evidence": "Building market awareness"}
                ],
                "opportunities": [
                    {"point": "Market growth", "evidence": f"${market_size/1e9:.1f}B TAM"},
                    {"point": "Product expansion", "evidence": "Adjacent market opportunities"},
                    {"point": "Strategic partnerships", "evidence": "Channel development potential"}
                ],
                "threats": [
                    {"point": "Competition", "evidence": f"{competitors} competitors"},
                    {"point": "Market dynamics", "evidence": "Rapid technology changes"},
                    {"point": "Funding needs", "evidence": f"Runway of {runway} months"}
                ]
            },
            "current_position_narrative": f"""
            {name} stands at a pivotal moment in its journey. As a {stage} company in the {sector} space,
            it has the opportunity to establish itself as a key player in a growing market. The company's
            position reflects both the challenges of early-stage growth and the significant potential ahead.
            """
        },
        "phase2": {
            "strategic_options_overview": "Multiple growth paths available with distinct risk-return profiles.",
            "ansoff_matrix_analysis": {
                "market_penetration": {
                    "initiatives": ["Increase sales velocity", "Improve conversion rates", "Expand customer success"],
                    "feasibility": "High",
                    "expected_impact": "2-3x growth in current segment",
                    "timeline": "6-12 months"
                },
                "market_development": {
                    "initiatives": ["Geographic expansion", "New customer segments", "Channel partnerships"],
                    "feasibility": "Medium",
                    "expected_impact": "Access to 5x larger market",
                    "timeline": "12-18 months"
                },
                "product_development": {
                    "initiatives": ["New features", "Platform capabilities", "API ecosystem"],
                    "feasibility": "Medium",
                    "expected_impact": "3x increase in deal size",
                    "timeline": "9-15 months"
                },
                "diversification": {
                    "initiatives": ["Adjacent products", "New business models", "Strategic acquisitions"],
                    "feasibility": "Low",
                    "expected_impact": "10x potential but higher risk",
                    "timeline": "18-24 months"
                }
            },
            "blue_ocean_strategy": {
                "eliminate": ["Complexity", "Long sales cycles"],
                "reduce": ["Implementation time", "Total cost of ownership"],
                "raise": ["User experience", "Customer value"],
                "create": ["New category", "Unique positioning"],
                "value_innovation": "Create differentiated offering that redefines market expectations",
                "blue_ocean_opportunity": "Untapped segment seeking innovative solutions"
            },
            "growth_scenarios": [
                {
                    "name": "Conservative Growth",
                    "description": "Focus on core market with steady expansion",
                    "investment_required": "$2M",
                    "expected_revenue_year3": f"${max(revenue * 5, 5000000)/1e6:.1f}M",
                    "success_probability": "80%"
                },
                {
                    "name": "Accelerated Growth",
                    "description": "Aggressive expansion across markets and products",
                    "investment_required": "$10M",
                    "expected_revenue_year3": f"${max(revenue * 20, 20000000)/1e6:.1f}M",
                    "success_probability": "50%"
                }
            ],
            "recommended_direction": "Pursue balanced growth strategy optimizing for sustainable expansion"
        },
        "phase3": {
            "implementation_roadmap": "Structured 18-month plan to achieve strategic objectives",
            "balanced_scorecard": {
                "financial": {
                    "objectives": ["Achieve profitability", "Secure funding"],
                    "measures": ["Monthly burn", "Revenue growth", "Gross margin"],
                    "targets": ["<$100K burn", ">20% MoM growth", ">70% margin"],
                    "initiatives": ["Cost optimization", "Pricing strategy"]
                },
                "customer": {
                    "objectives": ["Market leadership", "Customer delight"],
                    "measures": ["Market share", "NPS", "Retention"],
                    "targets": [">5% share", ">50 NPS", ">90% retention"],
                    "initiatives": ["Customer success program", "Product improvements"]
                },
                "internal_process": {
                    "objectives": ["Operational excellence", "Scalability"],
                    "measures": ["Cycle time", "Quality", "Automation"],
                    "targets": ["<2 week cycles", ">99% uptime", "80% automated"],
                    "initiatives": ["Process optimization", "Technology upgrades"]
                },
                "learning_growth": {
                    "objectives": ["Build A-team", "Innovation culture"],
                    "measures": ["Team satisfaction", "Skills", "Innovation"],
                    "targets": [">8/10 satisfaction", "Full coverage", "Quarterly launches"],
                    "initiatives": ["Hiring program", "Training", "R&D investment"]
                }
            },
            "okr_framework": {
                "q1_2024": {
                    "objectives": [
                        {
                            "objective": "Achieve product-market fit",
                            "key_results": [
                                "10 customer testimonials",
                                "$100K MRR",
                                "<5% monthly churn"
                            ]
                        }
                    ]
                },
                "q2_2024": {
                    "objectives": [
                        {
                            "objective": "Scale go-to-market",
                            "key_results": [
                                "Hire 5 sales reps",
                                "$1M pipeline",
                                "3 channel partners"
                            ]
                        }
                    ]
                }
            },
            "resource_requirements": {
                "human_resources": {
                    "immediate_hires": ["Head of Sales", "Senior Engineers"],
                    "q1_hires": ["5 sales reps", "3 engineers", "2 customer success"],
                    "total_headcount_eoy": 25,
                    "key_skill_gaps": ["Enterprise sales", "Data science"]
                },
                "financial_resources": {
                    "funding_required": "$5M Series A",
                    "use_of_funds": {"Product": "40%", "Sales": "35%", "Operations": "25%"},
                    "runway_extension": "18 months"
                },
                "technology_resources": {
                    "infrastructure_needs": ["Scalable architecture", "Security compliance"],
                    "tool_requirements": ["CRM", "Analytics", "Communication"],
                    "platform_migrations": ["Cloud-native", "Microservices"]
                }
            },
            "risk_mitigation_plan": {
                "top_risks": [
                    {
                        "risk": "Market competition",
                        "probability": "High",
                        "impact": "High",
                        "mitigation": "Build moats through customer relationships and product differentiation"
                    },
                    {
                        "risk": "Talent acquisition",
                        "probability": "Medium",
                        "impact": "High",
                        "mitigation": "Competitive compensation and strong culture"
                    }
                ]
            },
            "success_metrics": [
                {"metric": "ARR", "target": "$5M", "frequency": "Monthly"},
                {"metric": "Customer count", "target": "100", "frequency": "Weekly"},
                {"metric": "Team size", "target": "25", "frequency": "Quarterly"}
            ]
        },
        "key_recommendations": [
            f"Focus on achieving product-market fit in the {sector} vertical",
            f"Raise Series A funding within {runway} months to accelerate growth",
            "Build repeatable and scalable sales process",
            "Establish strategic partnerships for distribution",
            "Invest in product differentiation and customer success"
        ],
        "critical_success_factors": [
            "Achieving product-market fit within 6 months",
            "Building world-class team across all functions",
            "Maintaining capital efficiency while scaling",
            "Creating sustainable competitive advantages"
        ],
        "next_steps": [
            {
                "timeline": "30 days",
                "actions": [
                    "Complete customer discovery interviews",
                    "Finalize product roadmap",
                    "Begin fundraising preparation"
                ]
            },
            {
                "timeline": "60 days",
                "actions": [
                    "Launch MVP to beta customers",
                    "Hire key leadership positions",
                    "Establish sales process"
                ]
            },
            {
                "timeline": "90 days",
                "actions": [
                    "Close first paying customers",
                    "Complete Series A deck",
                    "Scale team to 15 people"
                ]
            }
        ]
    }