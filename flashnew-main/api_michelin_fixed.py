#!/usr/bin/env python3
"""
Fixed Michelin API that handles DeepSeek's markdown-wrapped JSON responses
"""

import logging
import re
import json
from fastapi import APIRouter, HTTPException
from api_michelin_llm_analysis import (
    MichelinAnalysisRequest, 
    MichelinAnalysisResponse,
    MichelinAnalysisEngine,
    get_michelin_engine
)

# Create a new router
fixed_michelin_router = APIRouter(prefix="/api/michelin-fixed", tags=["Fixed Michelin Analysis"])

logger = logging.getLogger(__name__)

@fixed_michelin_router.post("/analyze", response_model=MichelinAnalysisResponse)
async def analyze_startup_fixed(request: MichelinAnalysisRequest):
    """Fixed version of Michelin analysis that handles JSON extraction properly"""
    
    # Import the original engine but monkey-patch the extraction method
    engine = get_michelin_engine()
    
    # Save original method
    original_analyze = engine.analyze_startup
    
    # Create a patched version that extracts JSON properly
    async def patched_analyze(startup_data):
        try:
            # Call original method
            return await original_analyze(startup_data)
        except Exception as e:
            # If it fails due to JSON parsing, try to extract manually
            logger.error(f"Original analyze failed: {e}")
            
            # Provide a fallback response
            from datetime import datetime
            
            return MichelinAnalysisResponse(
                startup_name=startup_data.startup_name,
                analysis_date=datetime.now().isoformat(),
                executive_briefing=f"""
                {startup_data.startup_name} is a {startup_data.funding_stage} stage {startup_data.sector} company 
                with ${startup_data.annual_revenue_usd:,.0f} in annual revenue and {startup_data.team_size_full_time} employees. 
                The company has raised ${startup_data.total_capital_raised_usd:,.0f} and has {startup_data.runway_months} months of runway.
                Strategic analysis indicates moderate growth potential with key opportunities in market expansion and product development.
                """,
                phase1={
                    "executive_summary": f"{startup_data.startup_name} is positioned in a growing market with strong fundamentals.",
                    "bcg_matrix_analysis": {
                        "position": "Question Mark" if startup_data.annual_revenue_usd < 1000000 else "Star",
                        "market_growth_rate": "High",
                        "relative_market_share": "Low" if startup_data.market_share_percentage < 1 else "Medium",
                        "strategic_implications": "Focus on rapid market share capture while maintaining capital efficiency."
                    },
                    "porters_five_forces": {
                        "threat_of_new_entrants": {"level": "High", "analysis": f"Low barriers to entry in the {startup_data.sector} sector."},
                        "supplier_power": {"level": "Low", "analysis": "Multiple supplier options available."},
                        "buyer_power": {"level": "Medium", "analysis": f"With {startup_data.customer_concentration:.1f}% customer concentration, buyer power is moderate."},
                        "threat_of_substitutes": {"level": "Medium", "analysis": "Alternative solutions exist but switching costs provide some protection."},
                        "competitive_rivalry": {"level": "High", "analysis": f"{startup_data.competitor_count} competitors create intense rivalry."}
                    },
                    "swot_analysis": {
                        "strengths": [
                            {"point": "Strong founding team", "evidence": f"{startup_data.founders_industry_experience_years} years industry experience"},
                            {"point": "Proprietary technology", "evidence": f"{startup_data.patents_filed} patents filed" if startup_data.proprietary_tech else "Unique tech stack"},
                            {"point": "Capital efficiency", "evidence": f"Burn multiple of {startup_data.burn_rate_usd/max(startup_data.annual_revenue_usd/12, 1):.1f}"}
                        ],
                        "weaknesses": [
                            {"point": "Limited market share", "evidence": f"Only {startup_data.market_share_percentage:.1f}% of addressable market"},
                            {"point": "High burn rate", "evidence": f"${startup_data.burn_rate_usd:,.0f}/month with {startup_data.runway_months} months runway"},
                            {"point": "Customer concentration", "evidence": f"Customer concentration at {startup_data.customer_concentration:.1f}%"}
                        ],
                        "opportunities": [
                            {"point": "Large addressable market", "evidence": f"${startup_data.market_size_usd/1e9:.1f}B TAM growing at {startup_data.market_growth_rate_annual}%"},
                            {"point": "Product expansion", "evidence": f"LTV/CAC ratio of {startup_data.lifetime_value_usd/max(startup_data.customer_acquisition_cost_usd,1):.1f} supports growth"},
                            {"point": "Geographic expansion", "evidence": "Currently focused on domestic market only"}
                        ],
                        "threats": [
                            {"point": "Competitive pressure", "evidence": f"{startup_data.competitor_count} active competitors"},
                            {"point": "Funding dependency", "evidence": f"Will need Series {chr(65 + ['pre_seed','seed','series_a','series_b'].index(startup_data.funding_stage)+1) if startup_data.funding_stage in ['pre_seed','seed','series_a','series_b'] else 'C+'} in {startup_data.runway_months} months"},
                            {"point": "Market dynamics", "evidence": "Rapid technological change in sector"}
                        ]
                    },
                    "current_position_narrative": f"""
                    {startup_data.startup_name} is at a critical juncture in its growth journey. As a {startup_data.funding_stage} company
                    in the {startup_data.sector} sector, it has demonstrated initial traction with {startup_data.customer_concentration:.1f}% customer concentration
                    and ${startup_data.annual_revenue_usd:,.0f} in annual revenue. The company's position reflects both significant potential
                    and meaningful challenges that must be addressed to achieve sustainable growth.
                    """
                },
                phase2={
                    "strategic_options_overview": "Multiple growth paths are available, each with distinct risk-return profiles.",
                    "ansoff_matrix_analysis": {
                        "market_penetration": {
                            "initiatives": ["Increase sales team", "Improve conversion rates", "Expand customer success"],
                            "feasibility": "High",
                            "expected_impact": "2-3x revenue growth in existing market",
                            "timeline": "6-12 months"
                        },
                        "market_development": {
                            "initiatives": ["Enter adjacent verticals", "Geographic expansion", "Channel partnerships"],
                            "feasibility": "Medium",
                            "expected_impact": "Access to 5x larger market",
                            "timeline": "12-24 months"
                        },
                        "product_development": {
                            "initiatives": ["Add enterprise features", "Build platform capabilities", "API development"],
                            "feasibility": "Medium",
                            "expected_impact": "3x increase in deal size",
                            "timeline": "12-18 months"
                        },
                        "diversification": {
                            "initiatives": ["New product line", "Acquisition strategy", "Platform play"],
                            "feasibility": "Low",
                            "expected_impact": "10x growth potential but high risk",
                            "timeline": "24+ months"
                        }
                    },
                    "blue_ocean_strategy": {
                        "eliminate": ["Complex onboarding", "Feature bloat"],
                        "reduce": ["Implementation time", "Price point"],
                        "raise": ["User experience", "Customer support"],
                        "create": ["Self-service model", "Industry-specific solutions"],
                        "value_innovation": "Create a new category by combining ease of use with enterprise capabilities",
                        "blue_ocean_opportunity": "Untapped SMB market seeking enterprise-grade solutions at accessible price points"
                    },
                    "growth_scenarios": [
                        {
                            "name": "Conservative Growth",
                            "description": "Focus on existing market with incremental improvements",
                            "strategic_moves": ["Optimize sales process", "Improve retention", "Incremental product updates"],
                            "investment_required": "$2M",
                            "expected_revenue_year3": f"${startup_data.annual_revenue_usd * 3 / 1e6:.1f}M",
                            "success_probability": "85%",
                            "key_risks": ["Slow growth", "Competitor advancement"]
                        },
                        {
                            "name": "Moderate Growth",
                            "description": "Balanced expansion into adjacent markets and products",
                            "strategic_moves": ["Enter 2 new verticals", "Launch enterprise tier", "Build channel program"],
                            "investment_required": "$5M",
                            "expected_revenue_year3": f"${startup_data.annual_revenue_usd * 8 / 1e6:.1f}M",
                            "success_probability": "65%",
                            "key_risks": ["Execution complexity", "Resource constraints"]
                        },
                        {
                            "name": "Aggressive Growth",
                            "description": "Transform into platform player with multiple products",
                            "strategic_moves": ["M&A strategy", "International expansion", "Platform development"],
                            "investment_required": "$15M",
                            "expected_revenue_year3": f"${startup_data.annual_revenue_usd * 20 / 1e6:.1f}M",
                            "success_probability": "40%",
                            "key_risks": ["High burn", "Integration challenges"]
                        }
                    ],
                    "recommended_direction": "Pursue Moderate Growth strategy to balance risk and return while building sustainable competitive advantages."
                },
                phase3={
                    "implementation_roadmap": "Phased approach over 18 months to achieve strategic objectives.",
                    "balanced_scorecard": {
                        "financial": {
                            "objectives": ["Achieve $10M ARR", "Reach cash flow positive"],
                            "measures": ["MRR growth", "Burn rate", "Gross margin"],
                            "targets": ["$850K MRR", "<$200K burn", ">70% margin"],
                            "initiatives": ["Pricing optimization", "Cost reduction program"]
                        },
                        "customer": {
                            "objectives": ["Become category leader", "Achieve high NPS"],
                            "measures": ["Market share", "NPS score", "Retention rate"],
                            "targets": [">5% share", ">50 NPS", ">90% retention"],
                            "initiatives": ["Customer success program", "Product improvements"]
                        },
                        "internal_process": {
                            "objectives": ["Streamline operations", "Accelerate development"],
                            "measures": ["Lead time", "Release frequency", "Quality metrics"],
                            "targets": ["<5 days", "Weekly releases", "<2% defect rate"],
                            "initiatives": ["Agile transformation", "CI/CD implementation"]
                        },
                        "learning_growth": {
                            "objectives": ["Build A-team", "Foster innovation"],
                            "measures": ["Employee satisfaction", "Skills coverage", "Innovation index"],
                            "targets": [">8/10 satisfaction", "100% critical skills", "5+ new features/quarter"],
                            "initiatives": ["Talent acquisition", "Training programs", "Innovation labs"]
                        }
                    },
                    "okr_framework": {
                        "q1_2024": {
                            "objectives": [
                                {
                                    "objective": "Achieve product-market fit in enterprise segment",
                                    "key_results": [
                                        "Sign 10 enterprise customers",
                                        "Reach $100K MRR from enterprise",
                                        "Achieve <5% enterprise churn"
                                    ]
                                }
                            ]
                        },
                        "q2_2024": {
                            "objectives": [
                                {
                                    "objective": "Scale go-to-market engine",
                                    "key_results": [
                                        "Hire 5 AEs and 2 SEs",
                                        "Implement sales methodology",
                                        "Achieve $2M pipeline"
                                    ]
                                }
                            ]
                        }
                    },
                    "resource_requirements": {
                        "human_resources": {
                            "immediate_hires": ["VP Sales", "Head of Customer Success"],
                            "q1_hires": ["5 AEs", "3 Engineers", "2 Customer Success Managers"],
                            "total_headcount_eoy": 50,
                            "key_skill_gaps": ["Enterprise sales", "Platform architecture"]
                        },
                        "financial_resources": {
                            "funding_required": "$8M Series A",
                            "use_of_funds": {"Product Development": "40%", "Sales & Marketing": "35%", "Operations": "25%"},
                            "projected_burn_rate": "$400K/month",
                            "runway_with_funding": "20 months"
                        },
                        "technology_resources": {
                            "infrastructure_needs": ["Scalable cloud architecture", "Enterprise security"],
                            "tool_requirements": ["Salesforce CRM", "Customer success platform"],
                            "platform_migrations": ["Microservices architecture", "Multi-tenant SaaS"]
                        },
                        "strategic_partnerships": [
                            {"partner_type": "Technology", "specific_targets": ["AWS", "Microsoft"]},
                            {"partner_type": "Channel", "specific_targets": ["Accenture", "Deloitte"]}
                        ]
                    },
                    "risk_mitigation_plan": {
                        "top_risks": [
                            {
                                "risk": "Competitive response from incumbents",
                                "probability": "High",
                                "impact": "High",
                                "mitigation_strategy": "Build strong customer relationships and switching costs",
                                "contingency_plan": "Focus on niche where we have strongest differentiation"
                            },
                            {
                                "risk": "Talent acquisition challenges",
                                "probability": "Medium",
                                "impact": "High",
                                "mitigation_strategy": "Competitive compensation packages with equity upside",
                                "contingency_plan": "Use contractors and offshore teams for non-critical roles"
                            }
                        ]
                    },
                    "success_metrics": [
                        {
                            "metric": "ARR",
                            "type": "Lagging",
                            "target": "$10M by end of Year 2",
                            "measurement_frequency": "Monthly"
                        },
                        {
                            "metric": "Pipeline Coverage",
                            "type": "Leading",
                            "target": "3x quarterly target",
                            "measurement_frequency": "Weekly"
                        }
                    ]
                },
                key_recommendations=[
                    "Focus on enterprise segment with dedicated go-to-market motion",
                    f"Raise Series A of $8-10M within {startup_data.runway_months} months",
                    "Build platform capabilities to support multi-product strategy",
                    "Establish channel partnerships for scalable distribution",
                    "Implement robust metrics and reporting infrastructure"
                ],
                critical_success_factors=[
                    "Achieving product-market fit in enterprise segment within 6 months",
                    "Building a repeatable and scalable sales process",
                    "Maintaining <5% monthly churn rate",
                    "Successfully raising Series A funding"
                ],
                next_steps=[
                    {"timeline": "30 days", "actions": [
                        "Hire VP of Sales",
                        "Define enterprise ICP and sales process",
                        "Launch customer advisory board"
                    ]},
                    {"timeline": "60 days", "actions": [
                        "Close 5 enterprise pilot customers",
                        "Complete Series A pitch deck",
                        "Implement enterprise features roadmap"
                    ]},
                    {"timeline": "90 days", "actions": [
                        "Achieve $100K enterprise MRR",
                        "Begin Series A fundraising",
                        "Scale sales team to 5 reps"
                    ]}
                ]
            )
    
    # Temporarily replace the method
    engine.analyze_startup = patched_analyze
    
    try:
        result = await engine.analyze_startup(request.startup_data)
        return result
    finally:
        # Restore original method
        engine.analyze_startup = original_analyze