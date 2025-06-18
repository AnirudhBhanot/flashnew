#!/usr/bin/env python3
"""
Adapter to connect the frontend to the DeepSeek-powered Michelin analysis
Maps the LLM response to the frontend's expected structure
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from datetime import datetime
from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional
import logging
import asyncio

# Import the original DeepSeek engine
from api_michelin_llm_analysis import (
    MichelinAnalysisRequest as OriginalRequest,
    get_michelin_engine,
    StartupData as OriginalStartupData
)

logger = logging.getLogger(__name__)

# Create router that will replace the frontend fix
deepseek_adapter_router = APIRouter(prefix="/api/michelin", tags=["Michelin DeepSeek Adapter"])

# Frontend-compatible models
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
    
    # Optional fields
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

def transform_deepseek_response(llm_response: Dict[str, Any], startup_data: StartupData) -> Dict[str, Any]:
    """Transform DeepSeek response to match frontend expectations"""
    
    # Extract phase data with safe defaults
    phase1 = llm_response.get("phase1", {})
    phase2 = llm_response.get("phase2", {})
    phase3 = llm_response.get("phase3", {})
    
    # Transform Phase 1
    transformed_phase1 = {
        "executive_summary": phase1.get("executive_summary", f"Strategic analysis for {startup_data.startup_name}"),
        "bcg_matrix": {
            "position": phase1.get("bcg_matrix", {}).get("position", "Question Mark"),
            "market_growth": startup_data.market_growth_rate_annual,
            "relative_market_share": startup_data.market_share_percentage,
            "strategic_implications": phase1.get("bcg_matrix", {}).get("strategic_implications", [
                "Focus on market share capture",
                "Optimize resource allocation",
                "Build competitive advantages"
            ]) if isinstance(phase1.get("bcg_matrix", {}).get("strategic_implications"), list) else [
                phase1.get("bcg_matrix", {}).get("strategic_implications", "Focus on growth")
            ],
            "action_items": phase1.get("bcg_matrix", {}).get("action_items", [
                "Accelerate customer acquisition",
                "Strengthen product differentiation",
                "Optimize unit economics"
            ])
        },
        "porters_five_forces": transform_porters_forces(phase1.get("porters_five_forces", {})),
        "swot_analysis": transform_swot(phase1.get("swot_analysis", {}), startup_data),
        "current_position_narrative": phase1.get("current_position_narrative", 
            f"{startup_data.startup_name} is positioned in a growing market with opportunities for expansion.")
    }
    
    # Transform Phase 2
    transformed_phase2 = {
        "strategic_options_overview": phase2.get("strategic_options_overview", "Multiple growth paths available"),
        "ansoff_matrix": transform_ansoff_matrix(phase2.get("ansoff_matrix", {})),
        "blue_ocean_strategy": transform_blue_ocean(phase2.get("blue_ocean_strategy", {})),
        "growth_scenarios": transform_growth_scenarios(phase2.get("growth_scenarios", []), startup_data),
        "recommended_direction": phase2.get("recommended_direction", "Pursue balanced growth strategy")
    }
    
    # Transform Phase 3
    transformed_phase3 = {
        "implementation_roadmap_summary": phase3.get("implementation_roadmap", "18-month strategic implementation plan"),
        "balanced_scorecard": transform_balanced_scorecard(phase3.get("balanced_scorecard", {})),
        "okr_framework": transform_okr_framework(phase3.get("okr_framework", {})),
        "execution_plan": phase3.get("execution_plan", create_default_execution_plan()),
        "resource_requirements": transform_resource_requirements(phase3.get("resource_requirements", {})),
        "risk_mitigation_plan": transform_risk_mitigation(phase3.get("risk_mitigation_plan", {})),
        "success_metrics": transform_success_metrics(phase3.get("success_metrics", []))
    }
    
    return {
        "startup_name": llm_response.get("startup_name", startup_data.startup_name),
        "analysis_date": llm_response.get("analysis_date", datetime.now().isoformat()),
        "executive_briefing": llm_response.get("executive_briefing", 
            f"Strategic analysis for {startup_data.startup_name} in the {startup_data.sector} sector."),
        "phase1": transformed_phase1,
        "phase2": transformed_phase2,
        "phase3": transformed_phase3,
        "key_recommendations": llm_response.get("key_recommendations", [
            f"Focus on product-market fit in {startup_data.sector}",
            "Optimize burn rate and extend runway",
            "Build strategic partnerships",
            "Scale customer acquisition",
            "Strengthen competitive positioning"
        ]),
        "critical_success_factors": llm_response.get("critical_success_factors", [
            "Achieving product-market fit",
            "Efficient capital allocation",
            "Strong team execution",
            "Market timing",
            "Competitive differentiation"
        ]),
        "next_steps": llm_response.get("next_steps", [
            {"timeline": "30 days", "actions": ["Complete market analysis", "Refine product roadmap", "Initiate fundraising"]},
            {"timeline": "60 days", "actions": ["Launch pilot program", "Hire key positions", "Establish partnerships"]},
            {"timeline": "90 days", "actions": ["Scale operations", "Measure KPIs", "Iterate based on feedback"]}
        ])
    }

def transform_porters_forces(forces_data: Dict) -> Dict:
    """Transform Porter's Five Forces to frontend format"""
    default_forces = {
        "threat_of_new_entrants": {"intensity": "High", "score": 4, "factors": ["Low barriers", "Growing market", "VC funding available"]},
        "supplier_power": {"intensity": "Low", "score": 2, "factors": ["Multiple options", "Commoditized inputs", "Low switching costs"]},
        "buyer_power": {"intensity": "Medium", "score": 3, "factors": ["Price sensitivity", "Alternative options", "Information availability"]},
        "threat_of_substitutes": {"intensity": "Medium", "score": 3, "factors": ["Alternative solutions", "DIY options", "Status quo"]},
        "competitive_rivalry": {"intensity": "High", "score": 4, "factors": ["Many competitors", "Low differentiation", "Growth stage market"]},
        "overall_industry_attractiveness": "Medium",
        "key_strategic_imperatives": ["Build moats", "Focus on differentiation", "Scale quickly", "Lock in customers"]
    }
    
    # Merge with actual data
    result = default_forces.copy()
    for force, data in forces_data.items():
        if force in result and isinstance(data, dict):
            result[force].update(data)
    
    return result

def transform_swot(swot_data: Dict, startup_data: StartupData) -> Dict:
    """Transform SWOT analysis to frontend format"""
    return {
        "strengths": swot_data.get("strengths", [
            {"item": "Strong team", "evidence": f"{startup_data.team_size_full_time} experienced professionals"},
            {"item": "Capital position", "evidence": f"${startup_data.cash_on_hand_usd:,.0f} runway"},
            {"item": "Market opportunity", "evidence": f"${startup_data.market_size_usd/1e9:.1f}B TAM"}
        ]),
        "weaknesses": swot_data.get("weaknesses", [
            {"item": "Limited market share", "impact": f"Only {startup_data.market_share_percentage}% captured"},
            {"item": "Burn rate", "impact": f"${startup_data.monthly_burn_usd:,.0f}/month"},
            {"item": "Early stage", "impact": f"{startup_data.funding_stage} funding"}
        ]),
        "opportunities": swot_data.get("opportunities", [
            {"item": "Market growth", "potential": f"{startup_data.market_growth_rate_annual}% annual growth"},
            {"item": "Product expansion", "potential": "Adjacent markets available"},
            {"item": "Strategic partnerships", "potential": "Channel opportunities"}
        ]),
        "threats": swot_data.get("threats", [
            {"item": "Competition", "mitigation": "Build differentiation and moats"},
            {"item": "Market dynamics", "mitigation": "Stay agile and responsive"},
            {"item": "Funding risk", "mitigation": "Optimize burn and metrics"}
        ]),
        "strategic_priorities": swot_data.get("strategic_priorities", [
            "Achieve product-market fit",
            "Extend runway through efficiency",
            "Build competitive advantages",
            "Scale customer acquisition",
            "Develop strategic partnerships"
        ])
    }

def transform_ansoff_matrix(ansoff_data: Dict) -> Dict:
    """Transform Ansoff Matrix to frontend format"""
    default_strategies = {
        "market_penetration": {
            "strategy": "Deepen presence in current markets",
            "initiatives": ["Increase sales velocity", "Improve retention", "Optimize pricing"],
            "investment": 2000000,
            "timeline": "6-12 months"
        },
        "market_development": {
            "strategy": "Expand to new markets and segments",
            "initiatives": ["Geographic expansion", "New verticals", "Channel partnerships"],
            "investment": 5000000,
            "timeline": "12-18 months"
        },
        "product_development": {
            "strategy": "Build new products for existing customers",
            "initiatives": ["Feature expansion", "Platform capabilities", "API ecosystem"],
            "investment": 4000000,
            "timeline": "9-15 months"
        },
        "diversification": {
            "strategy": "New products for new markets",
            "initiatives": ["Adjacent products", "M&A opportunities", "New business models"],
            "investment": 10000000,
            "timeline": "18-24 months"
        },
        "recommended_strategy": "Market Penetration + Product Development",
        "implementation_priorities": [
            "Focus on core market first",
            "Build incrementally",
            "Validate before scaling",
            "Maintain capital efficiency"
        ]
    }
    
    # Merge with actual data
    result = default_strategies.copy()
    for strategy, data in ansoff_data.items():
        if strategy in result and isinstance(data, dict):
            result[strategy].update(data)
    
    return result

def transform_blue_ocean(blue_ocean_data: Dict) -> Dict:
    """Transform Blue Ocean Strategy to frontend format"""
    return {
        "eliminate_factors": blue_ocean_data.get("eliminate", ["Complexity", "Long cycles", "High costs"]),
        "reduce_factors": blue_ocean_data.get("reduce", ["Implementation time", "Training needs", "Friction"]),
        "raise_factors": blue_ocean_data.get("raise", ["User experience", "Value delivery", "Support"]),
        "create_factors": blue_ocean_data.get("create", ["New category", "Unique value", "Network effects"]),
        "value_innovation_opportunities": blue_ocean_data.get("value_innovation_opportunities", [
            {"opportunity": "Productized services", "impact": "Higher margins"},
            {"opportunity": "Platform play", "impact": "Network effects"},
            {"opportunity": "Ecosystem approach", "impact": "Lock-in effects"}
        ]),
        "new_market_spaces": blue_ocean_data.get("new_market_spaces", ["Underserved segments", "Adjacent verticals", "New geographies"])
    }

def transform_growth_scenarios(scenarios_data: List, startup_data: StartupData) -> List:
    """Transform growth scenarios to frontend format"""
    if scenarios_data and isinstance(scenarios_data, list):
        return [transform_single_scenario(s) for s in scenarios_data]
    
    # Default scenarios
    return [
        {
            "name": "Conservative Growth",
            "description": "Focus on core market with steady expansion",
            "investment_required": 3000000,
            "revenue_projection_3yr": max(startup_data.annual_revenue_usd * 5, 10000000) if startup_data.annual_revenue_usd else 10000000,
            "team_size_projection": 30,
            "probability_of_success": 80,
            "key_milestones": ["PMF validation", "Sales playbook", "100 customers"],
            "risks": ["Slow growth", "Competition", "Market changes"]
        },
        {
            "name": "Balanced Growth",
            "description": "Core market plus selective expansion",
            "investment_required": 8000000,
            "revenue_projection_3yr": max(startup_data.annual_revenue_usd * 10, 25000000) if startup_data.annual_revenue_usd else 25000000,
            "team_size_projection": 75,
            "probability_of_success": 60,
            "key_milestones": ["Multi-product", "Channel partners", "Market leader"],
            "risks": ["Execution complexity", "Resource constraints", "Timing"]
        },
        {
            "name": "Aggressive Growth",
            "description": "Multi-market, multi-product expansion",
            "investment_required": 20000000,
            "revenue_projection_3yr": max(startup_data.annual_revenue_usd * 20, 50000000) if startup_data.annual_revenue_usd else 50000000,
            "team_size_projection": 150,
            "probability_of_success": 40,
            "key_milestones": ["Platform play", "M&A", "IPO ready"],
            "risks": ["High burn", "Integration", "Market risk"]
        }
    ]

def transform_single_scenario(scenario: Dict) -> Dict:
    """Transform a single growth scenario"""
    return {
        "name": scenario.get("name", "Growth Scenario"),
        "description": scenario.get("description", "Strategic growth path"),
        "investment_required": scenario.get("investment_required", 5000000) if isinstance(scenario.get("investment_required"), (int, float)) else 5000000,
        "revenue_projection_3yr": scenario.get("expected_revenue_year3", 10000000) if isinstance(scenario.get("expected_revenue_year3"), (int, float)) else 10000000,
        "team_size_projection": scenario.get("team_size_projection", 50),
        "probability_of_success": int(scenario.get("success_probability", "60%").replace("%", "")) if isinstance(scenario.get("success_probability"), str) else scenario.get("success_probability", 60),
        "key_milestones": scenario.get("key_milestones", ["Milestone 1", "Milestone 2", "Milestone 3"]),
        "risks": scenario.get("key_risks", ["Risk 1", "Risk 2", "Risk 3"])
    }

def transform_balanced_scorecard(scorecard_data: Dict) -> List:
    """Transform Balanced Scorecard to frontend format"""
    if isinstance(scorecard_data, list):
        return scorecard_data
    
    # Transform dict to list format
    perspectives = ["Financial", "Customer", "Internal Process", "Learning & Growth"]
    result = []
    
    for perspective in perspectives:
        perspective_data = scorecard_data.get(perspective.lower().replace(" ", "_"), {})
        result.append({
            "perspective": perspective,
            "objectives": perspective_data.get("objectives", ["Objective 1", "Objective 2"]),
            "measures": perspective_data.get("measures", ["Measure 1", "Measure 2"]),
            "targets": perspective_data.get("targets", ["Target 1", "Target 2"]),
            "initiatives": perspective_data.get("initiatives", ["Initiative 1", "Initiative 2"])
        })
    
    return result

def transform_okr_framework(okr_data: Dict) -> List:
    """Transform OKR Framework to frontend format"""
    if isinstance(okr_data, list):
        return okr_data
    
    # Transform dict to list format
    result = []
    for quarter, data in okr_data.items():
        if isinstance(data, dict) and "objectives" in data:
            result.append({
                "quarter": quarter.replace("_", " ").upper(),
                "objectives": transform_okr_objectives(data["objectives"])
            })
    
    return result if result else [
        {
            "quarter": "Q1 2024",
            "objectives": [
                {
                    "objective": "Achieve product-market fit",
                    "key_results": [
                        {"kr": "Complete 50 customer interviews", "current": "10", "target": "50"},
                        {"kr": "Achieve NPS > 50", "current": "30", "target": "50"},
                        {"kr": "Reach $100K MRR", "current": "$25K", "target": "$100K"}
                    ]
                }
            ]
        }
    ]

def transform_okr_objectives(objectives: List) -> List:
    """Transform OKR objectives to frontend format"""
    result = []
    for obj in objectives:
        if isinstance(obj, dict):
            key_results = []
            for kr in obj.get("key_results", []):
                if isinstance(kr, str):
                    key_results.append({"kr": kr, "current": "0%", "target": "100%"})
                elif isinstance(kr, dict):
                    key_results.append(kr)
            
            result.append({
                "objective": obj.get("objective", "Objective"),
                "key_results": key_results
            })
    
    return result

def create_default_execution_plan() -> Dict:
    """Create default execution plan"""
    return {
        "phase1_foundation": {
            "timeline": "Months 1-6",
            "focus": "Product-market fit and team building",
            "key_activities": ["Customer development", "Product iteration", "Hiring"],
            "success_criteria": ["PMF validated", "Team of 20", "$50K MRR"]
        },
        "phase2_growth": {
            "timeline": "Months 7-12",
            "focus": "Scaling go-to-market",
            "key_activities": ["Sales team", "Marketing", "Partnerships"],
            "success_criteria": ["$250K MRR", "100 customers", "Series A"]
        },
        "phase3_expansion": {
            "timeline": "Months 13-18",
            "focus": "Market expansion",
            "key_activities": ["New products", "New markets", "M&A"],
            "success_criteria": ["$1M MRR", "Market leader", "Series B ready"]
        }
    }

def transform_resource_requirements(resources_data: Dict) -> Dict:
    """Transform resource requirements to frontend format"""
    return {
        "human_resources": resources_data.get("human_resources", [
            {"role": "VP Sales", "level": "Senior", "timeline": "Q1 2024", "cost": 250000},
            {"role": "Engineers", "count": 5, "timeline": "Q1-Q2 2024", "cost": 800000},
            {"role": "Customer Success", "count": 3, "timeline": "Q2 2024", "cost": 300000}
        ]) if isinstance(resources_data.get("human_resources"), list) else [
            {"role": "VP Sales", "level": "Senior", "timeline": "Q1 2024", "cost": 250000}
        ],
        "financial_resources": resources_data.get("financial_resources", {
            "total_capital_needed": 8000000,
            "runway_extension": 18,
            "monthly_burn_target": 400000
        }),
        "technology_resources": resources_data.get("technology_resources", [
            "Scalable cloud infrastructure",
            "Enterprise security compliance",
            "Modern data stack",
            "DevOps tooling"
        ]) if isinstance(resources_data.get("technology_resources"), list) else [
            "Cloud infrastructure"
        ],
        "partnership_resources": resources_data.get("partnership_resources", [
            "Strategic technology partners",
            "Channel partners",
            "Industry associations",
            "Advisory board"
        ]) if isinstance(resources_data.get("partnership_resources"), list) else [
            "Strategic partners"
        ]
    }

def transform_risk_mitigation(risk_data: Any) -> List:
    """Transform risk mitigation plan to frontend format"""
    if isinstance(risk_data, list):
        return [transform_single_risk(r) for r in risk_data]
    
    # Default risks
    return [
        {
            "risk": "Talent acquisition",
            "impact": "High",
            "likelihood": "Medium",
            "mitigation_strategy": "Competitive compensation and strong culture",
            "contingency_plan": "Use contractors and remote talent"
        },
        {
            "risk": "Market competition",
            "impact": "High",
            "likelihood": "High",
            "mitigation_strategy": "Build moats and differentiation",
            "contingency_plan": "Focus on niche segments"
        },
        {
            "risk": "Product-market fit",
            "impact": "Medium",
            "likelihood": "Medium",
            "mitigation_strategy": "Continuous customer feedback",
            "contingency_plan": "Pivot to adjacent use case"
        }
    ]

def transform_single_risk(risk: Dict) -> Dict:
    """Transform a single risk"""
    return {
        "risk": risk.get("risk", "Risk"),
        "impact": risk.get("impact", "Medium"),
        "likelihood": risk.get("likelihood", risk.get("probability", "Medium")),
        "mitigation_strategy": risk.get("mitigation_strategy", risk.get("mitigation", "Mitigation strategy")),
        "contingency_plan": risk.get("contingency_plan", "Contingency plan")
    }

def transform_success_metrics(metrics_data: List) -> List:
    """Transform success metrics to frontend format"""
    if metrics_data and isinstance(metrics_data, list):
        return [transform_single_metric(m) for m in metrics_data]
    
    # Default metrics
    return [
        {"metric": "ARR", "type": "Lagging", "target": "$5M by Year 2", "frequency": "Monthly"},
        {"metric": "Customer Count", "type": "Lagging", "target": "200 customers", "frequency": "Weekly"},
        {"metric": "NPS", "type": "Leading", "target": ">60", "frequency": "Quarterly"},
        {"metric": "Burn Rate", "type": "Leading", "target": "<$400K/month", "frequency": "Monthly"},
        {"metric": "Pipeline Coverage", "type": "Leading", "target": "3x quota", "frequency": "Weekly"}
    ]

def transform_single_metric(metric: Dict) -> Dict:
    """Transform a single success metric"""
    return {
        "metric": metric.get("metric", "Metric"),
        "type": metric.get("type", "Leading"),
        "target": metric.get("target", "Target"),
        "frequency": metric.get("measurement_frequency", metric.get("frequency", "Monthly"))
    }

@deepseek_adapter_router.post("/analyze")
async def analyze_with_deepseek(
    request: MichelinAnalysisRequest,
    background_tasks: BackgroundTasks
):
    """
    Perform DeepSeek-powered Michelin analysis with frontend-compatible response format
    """
    try:
        logger.info(f"Starting DeepSeek Michelin analysis for {request.startup_data.startup_name}")
        
        # Convert to original format
        original_startup_data = OriginalStartupData(
            startup_name=request.startup_data.startup_name,
            sector=request.startup_data.sector,
            funding_stage=request.startup_data.funding_stage,
            total_capital_raised_usd=request.startup_data.total_capital_raised_usd,
            cash_on_hand_usd=request.startup_data.cash_on_hand_usd,
            monthly_burn_usd=request.startup_data.monthly_burn_usd or 50000,
            runway_months=request.startup_data.runway_months or 12,
            team_size_full_time=request.startup_data.team_size_full_time,
            market_size_usd=request.startup_data.market_size_usd,
            market_growth_rate_annual=request.startup_data.market_growth_rate_annual,
            competitor_count=request.startup_data.competitor_count,
            market_share_percentage=request.startup_data.market_share_percentage,
            customer_acquisition_cost_usd=request.startup_data.customer_acquisition_cost_usd or 1000,
            lifetime_value_usd=request.startup_data.lifetime_value_usd or 10000,
            monthly_active_users=request.startup_data.monthly_active_users or 1000,
            product_stage=request.startup_data.product_stage or "beta",
            proprietary_tech=request.startup_data.proprietary_tech or False,
            patents_filed=request.startup_data.patents_filed or 0,
            founders_industry_experience_years=request.startup_data.founders_industry_experience_years or 5,
            b2b_or_b2c=request.startup_data.b2b_or_b2c or "b2b",
            burn_rate_usd=request.startup_data.burn_rate_usd or request.startup_data.monthly_burn_usd or 50000,
            investor_tier_primary=request.startup_data.investor_tier_primary or "tier_2",
            revenue_growth_rate=request.startup_data.revenue_growth_rate or 0,
            gross_margin=request.startup_data.gross_margin or 70,
            annual_revenue_usd=request.startup_data.annual_revenue_usd or 0
        )
        
        original_request = OriginalRequest(
            startup_data=original_startup_data,
            analysis_depth=request.analysis_depth
        )
        
        # Get DeepSeek engine and perform analysis
        engine = get_michelin_engine()
        
        # Set a timeout for the DeepSeek call
        try:
            llm_response = await asyncio.wait_for(
                engine.analyze_startup(original_request.startup_data),
                timeout=120.0  # 2 minute timeout
            )
            
            # Convert the response to a dict
            llm_response_dict = llm_response.model_dump()
            
            # Transform to frontend format
            frontend_response = transform_deepseek_response(llm_response_dict, request.startup_data)
            
            logger.info(f"DeepSeek analysis completed for {request.startup_data.startup_name}")
            
            return frontend_response
            
        except asyncio.TimeoutError:
            logger.error("DeepSeek analysis timed out after 120 seconds")
            raise HTTPException(
                status_code=504,
                detail="Analysis timed out. Please try again or use a smaller analysis depth."
            )
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"DeepSeek analysis failed: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Analysis failed: {str(e)}"
        )