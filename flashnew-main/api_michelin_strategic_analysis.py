#!/usr/bin/env python3
"""
Michelin 3-Phase Strategic Analysis API
Implements the Michelin case study framework with DeepSeek integration
"""

import os
import sys
import logging
import json
import asyncio
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
import aiohttp
import re

# Add framework intelligence to path
current_dir = os.path.dirname(os.path.abspath(__file__))
framework_dir = os.path.join(current_dir, 'framework_intelligence')
sys.path.insert(0, framework_dir)

# Setup logging
logger = logging.getLogger(__name__)

# Import framework components
try:
    from framework_database import FRAMEWORKS
    FRAMEWORK_ANALYSIS_AVAILABLE = True
except ImportError as e:
    logger.warning(f"Framework analysis not available: {e}")
    FRAMEWORK_ANALYSIS_AVAILABLE = False

# Create router
michelin_router = APIRouter(prefix="/api/michelin", tags=["Michelin Strategic Analysis"])

# DeepSeek API configuration
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "sk-f68b7148243e4663a31386a5ea6093cf")
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"

# Pydantic models for request/response
class MichelinAnalysisRequest(BaseModel):
    """Request for Michelin 3-phase analysis"""
    startup_data: Dict[str, Any]
    analysis_depth: str = Field(default="comprehensive", description="comprehensive, standard, or quick")

class BCGMatrixAnalysis(BaseModel):
    position: str  # Star, Cash Cow, Question Mark, or Dog
    market_growth: float
    relative_market_share: float
    strategic_implications: List[str]
    action_items: List[str]

class PortersFiveForces(BaseModel):
    competitive_rivalry: Dict[str, Any]
    threat_of_new_entrants: Dict[str, Any]
    bargaining_power_of_suppliers: Dict[str, Any]
    bargaining_power_of_buyers: Dict[str, Any]
    threat_of_substitutes: Dict[str, Any]
    overall_industry_attractiveness: str
    key_strategic_imperatives: List[str]

class SWOTAnalysis(BaseModel):
    strengths: List[Dict[str, str]]
    weaknesses: List[Dict[str, str]]
    opportunities: List[Dict[str, str]]
    threats: List[Dict[str, str]]
    strategic_priorities: List[str]

class Phase1Analysis(BaseModel):
    executive_summary: str
    bcg_matrix: BCGMatrixAnalysis
    porters_five_forces: PortersFiveForces
    swot_analysis: SWOTAnalysis
    current_position_narrative: str

class AnsoffMatrixAnalysis(BaseModel):
    market_penetration: Dict[str, Any]
    market_development: Dict[str, Any]
    product_development: Dict[str, Any]
    diversification: Dict[str, Any]
    recommended_strategy: str
    implementation_priorities: List[str]

class BlueOceanAnalysis(BaseModel):
    eliminate_factors: List[str]
    reduce_factors: List[str]
    raise_factors: List[str]
    create_factors: List[str]
    value_innovation_opportunities: List[Dict[str, Any]]
    new_market_spaces: List[str]

class GrowthScenario(BaseModel):
    name: str
    description: str
    revenue_projection_3yr: float
    investment_required: float
    key_milestones: List[str]
    risks: List[str]
    probability_of_success: float

class Phase2Analysis(BaseModel):
    strategic_options_overview: str
    ansoff_matrix: AnsoffMatrixAnalysis
    blue_ocean_strategy: BlueOceanAnalysis
    growth_scenarios: List[GrowthScenario]
    recommended_direction: str

class BalancedScorecardPerspective(BaseModel):
    perspective: str
    objectives: List[str]
    measures: List[str]
    targets: List[str]
    initiatives: List[str]

class OKRSet(BaseModel):
    quarter: str
    objectives: List[Dict[str, Any]]

class ResourceRequirements(BaseModel):
    human_resources: List[Dict[str, Any]]
    financial_resources: Dict[str, float]
    technology_resources: List[str]
    partnership_resources: List[str]

class RiskMitigationItem(BaseModel):
    risk: str
    impact: str
    likelihood: str
    mitigation_strategy: str
    contingency_plan: str

class Phase3Analysis(BaseModel):
    implementation_roadmap_summary: str
    balanced_scorecard: List[BalancedScorecardPerspective]
    okr_framework: List[OKRSet]
    resource_requirements: ResourceRequirements
    risk_mitigation_plan: List[RiskMitigationItem]
    success_metrics: List[Dict[str, Any]]

class MichelinAnalysisResponse(BaseModel):
    """Complete Michelin 3-phase strategic analysis"""
    company_name: str
    analysis_date: str
    executive_briefing: str
    phase1: Phase1Analysis
    phase2: Phase2Analysis
    phase3: Phase3Analysis
    key_recommendations: List[str]
    critical_success_factors: List[str]
    next_steps: List[Dict[str, Any]]

async def call_deepseek_api(prompt: str, system_prompt: str = None) -> str:
    """Call DeepSeek API with McKinsey consultant persona"""
    
    if not system_prompt:
        system_prompt = """You are a senior McKinsey partner specializing in strategic transformation.
        You have 30+ years of experience advising Fortune 500 companies and high-growth startups.
        Your analysis should be:
        1. Data-driven and specific with numbers
        2. Framework-based but practical
        3. Action-oriented with clear next steps
        4. Confident without hedging
        5. Written in professional consulting language
        
        Always provide specific metrics, timelines, and financial projections where relevant.
        Format your response as valid JSON matching the expected structure."""
    
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": prompt}
    ]
    
    async with aiohttp.ClientSession() as session:
        headers = {
            "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "deepseek-chat",
            "messages": messages,
            "temperature": 0.7,
            "max_tokens": 4000
        }
        
        try:
            async with session.post(DEEPSEEK_API_URL, headers=headers, json=data) as response:
                if response.status == 200:
                    result = await response.json()
                    return result['choices'][0]['message']['content']
                else:
                    logger.error(f"DeepSeek API error: {response.status}")
                    return None
        except Exception as e:
            logger.error(f"DeepSeek API call failed: {e}")
            return None

def _extract_json_from_response(response_text: str) -> Dict[str, Any]:
    """Extract and parse JSON from LLM response"""
    if not response_text:
        return {}
    
    # Try to find JSON in markdown code blocks
    json_match = re.search(r'```json\s*(.*?)\s*```', response_text, re.DOTALL)
    if json_match:
        json_str = json_match.group(1)
    else:
        # Try to find raw JSON
        json_str = response_text.strip()
    
    try:
        return json.loads(json_str)
    except json.JSONDecodeError as e:
        logger.error(f"JSON decode error: {e}")
        # Try to fix common issues
        json_str = _fix_malformed_json(json_str)
        try:
            return json.loads(json_str)
        except:
            logger.error("Failed to parse JSON after fixing attempt")
            return {}

def _fix_malformed_json(json_str: str) -> str:
    """Fix common JSON formatting issues"""
    # Fix unquoted property names
    json_str = re.sub(r'(\w+):', r'"\1":', json_str)
    # Fix single quotes
    json_str = json_str.replace("'", '"')
    # Fix trailing commas
    json_str = re.sub(r',\s*}', '}', json_str)
    json_str = re.sub(r',\s*]', ']', json_str)
    return json_str

async def analyze_phase1_current_state(startup_data: Dict[str, Any]) -> Phase1Analysis:
    """Phase 1: Where Are We Now? - Current state analysis"""
    
    # Extract key metrics
    revenue = startup_data.get('annual_revenue_run_rate', 0)
    growth_rate = startup_data.get('revenue_growth_rate_percent', 0)
    market_size = startup_data.get('tam_size_usd', 10000000000)
    burn_rate = startup_data.get('monthly_burn_usd', 50000)
    customers = startup_data.get('customer_count', 0)
    stage = startup_data.get('funding_stage', 'seed')
    sector = startup_data.get('sector', 'technology')
    
    prompt = f"""
    Analyze this {sector} {stage} startup for Phase 1 (Where Are We Now?):
    - Revenue: ${revenue:,.0f}
    - Growth Rate: {growth_rate}%
    - Market Size: ${market_size:,.0f}
    - Monthly Burn: ${burn_rate:,.0f}
    - Customers: {customers}
    - Full data: {json.dumps(startup_data)}
    
    Provide a comprehensive analysis using:
    1. BCG Matrix positioning (with specific market share and growth calculations)
    2. Porter's Five Forces (rate each force as Low/Medium/High with justification)
    3. SWOT Analysis (3-4 items per quadrant with specific evidence)
    
    Return valid JSON matching this structure:
    {{
        "executive_summary": "2-3 paragraph summary of current position",
        "bcg_matrix": {{
            "position": "Star|Cash Cow|Question Mark|Dog",
            "market_growth": <number>,
            "relative_market_share": <number>,
            "strategic_implications": ["implication1", "implication2"],
            "action_items": ["action1", "action2"]
        }},
        "porters_five_forces": {{
            "competitive_rivalry": {{"intensity": "Low|Medium|High", "factors": ["factor1", "factor2"], "score": <1-5>}},
            "threat_of_new_entrants": {{"intensity": "Low|Medium|High", "factors": ["factor1", "factor2"], "score": <1-5>}},
            "bargaining_power_of_suppliers": {{"intensity": "Low|Medium|High", "factors": ["factor1", "factor2"], "score": <1-5>}},
            "bargaining_power_of_buyers": {{"intensity": "Low|Medium|High", "factors": ["factor1", "factor2"], "score": <1-5>}},
            "threat_of_substitutes": {{"intensity": "Low|Medium|High", "factors": ["factor1", "factor2"], "score": <1-5>}},
            "overall_industry_attractiveness": "Low|Medium|High",
            "key_strategic_imperatives": ["imperative1", "imperative2"]
        }},
        "swot_analysis": {{
            "strengths": [{{"item": "strength1", "evidence": "specific data"}}, {{"item": "strength2", "evidence": "specific data"}}],
            "weaknesses": [{{"item": "weakness1", "impact": "specific impact"}}, {{"item": "weakness2", "impact": "specific impact"}}],
            "opportunities": [{{"item": "opportunity1", "potential": "specific value"}}, {{"item": "opportunity2", "potential": "specific value"}}],
            "threats": [{{"item": "threat1", "mitigation": "specific action"}}, {{"item": "threat2", "mitigation": "specific action"}}],
            "strategic_priorities": ["priority1", "priority2", "priority3"]
        }},
        "current_position_narrative": "3-4 paragraph narrative synthesizing all analyses"
    }}
    """
    
    response = await call_deepseek_api(prompt)
    if not response:
        return generate_fallback_phase1_analysis(startup_data)
    
    try:
        data = _extract_json_from_response(response)
        return Phase1Analysis(**data)
    except Exception as e:
        logger.error(f"Failed to parse Phase 1 analysis: {e}")
        return generate_fallback_phase1_analysis(startup_data)

def generate_fallback_phase1_analysis(startup_data: Dict[str, Any]) -> Phase1Analysis:
    """Generate fallback Phase 1 analysis if API fails"""
    
    revenue = startup_data.get('annual_revenue_run_rate', 0)
    growth_rate = startup_data.get('revenue_growth_rate_percent', 30)
    market_size = startup_data.get('tam_size_usd', 10000000000)
    market_share = (revenue / market_size * 100) if market_size > 0 else 0
    
    # Determine BCG position
    if growth_rate > 20 and market_share > 1:
        position = "Star"
    elif growth_rate <= 20 and market_share > 1:
        position = "Cash Cow"
    elif growth_rate > 20 and market_share <= 1:
        position = "Question Mark"
    else:
        position = "Dog"
    
    return Phase1Analysis(
        executive_summary=f"The company is positioned as a {position} in the BCG matrix with {market_share:.2f}% market share and {growth_rate}% growth rate. The startup shows promising indicators but faces typical early-stage challenges.",
        bcg_matrix=BCGMatrixAnalysis(
            position=position,
            market_growth=growth_rate,
            relative_market_share=market_share,
            strategic_implications=[
                f"Current {position} position requires {'aggressive growth investment' if position == 'Question Mark' else 'maintaining market position'}",
                f"Market share of {market_share:.2f}% indicates {'early stage with growth potential' if market_share < 1 else 'established presence'}"
            ],
            action_items=[
                "Focus on customer acquisition to increase market share",
                "Optimize burn rate to extend runway",
                "Build competitive moats through product differentiation"
            ]
        ),
        porters_five_forces=PortersFiveForces(
            competitive_rivalry={"intensity": "Medium", "factors": ["Growing market attracts competitors", "Product differentiation emerging"], "score": 3},
            threat_of_new_entrants={"intensity": "High", "factors": ["Low barriers to entry", "VC funding available"], "score": 4},
            bargaining_power_of_suppliers={"intensity": "Low", "factors": ["Multiple supplier options", "Standard technologies"], "score": 2},
            bargaining_power_of_buyers={"intensity": "Medium", "factors": ["Increasing options", "Price sensitivity"], "score": 3},
            threat_of_substitutes={"intensity": "Medium", "factors": ["Alternative solutions exist", "Switching costs moderate"], "score": 3},
            overall_industry_attractiveness="Medium",
            key_strategic_imperatives=[
                "Build defensible competitive advantages",
                "Increase switching costs for customers",
                "Develop unique value propositions"
            ]
        ),
        swot_analysis=SWOTAnalysis(
            strengths=[
                {"item": "Early market entry", "evidence": f"{startup_data.get('customer_count', 0)} customers acquired"},
                {"item": "Strong team", "evidence": f"{startup_data.get('team_size_full_time', 5)} full-time employees"}
            ],
            weaknesses=[
                {"item": "Limited runway", "impact": f"Only {startup_data.get('runway_months', 12)} months of runway"},
                {"item": "High burn rate", "impact": f"${startup_data.get('monthly_burn_usd', 50000):,}/month burn"}
            ],
            opportunities=[
                {"item": "Large market", "potential": f"${market_size/1e9:.1f}B TAM"},
                {"item": "High growth rate", "potential": f"{growth_rate}% annual growth"}
            ],
            threats=[
                {"item": "Competition", "mitigation": "Build unique differentiators"},
                {"item": "Funding risk", "mitigation": "Improve unit economics"}
            ],
            strategic_priorities=[
                "Achieve product-market fit",
                "Extend runway through efficiency",
                "Build competitive advantages"
            ]
        ),
        current_position_narrative="The startup is in a critical growth phase with promising early traction but faces typical challenges of resource constraints and market competition. The key to success lies in rapidly achieving product-market fit while maintaining capital efficiency."
    )

async def analyze_phase2_strategic_direction(startup_data: Dict[str, Any], phase1_results: Phase1Analysis) -> Phase2Analysis:
    """Phase 2: Where Should We Go? - Strategic direction"""
    
    revenue = startup_data.get('annual_revenue_run_rate', 0)
    sector = startup_data.get('sector', 'technology')
    stage = startup_data.get('funding_stage', 'seed')
    
    prompt = f"""
    Based on the Phase 1 analysis showing the company as a {phase1_results.bcg_matrix.position} with these strategic priorities:
    {json.dumps(phase1_results.swot_analysis.strategic_priorities)}
    
    Analyze Phase 2 (Where Should We Go?) for this {sector} {stage} startup:
    - Current Revenue: ${revenue:,.0f}
    - Market Position: {phase1_results.bcg_matrix.position}
    - Key Strengths: {[s['item'] for s in phase1_results.swot_analysis.strengths[:2]]}
    - Key Opportunities: {[o['item'] for o in phase1_results.swot_analysis.opportunities[:2]]}
    
    Provide strategic direction using:
    1. Ansoff Matrix (evaluate all 4 quadrants with specific initiatives)
    2. Blue Ocean Strategy (specific factors to eliminate/reduce/raise/create)
    3. Three growth scenarios (Conservative, Moderate, Aggressive)
    
    Return valid JSON matching this structure:
    {{
        "strategic_options_overview": "2-3 paragraph overview of strategic choices",
        "ansoff_matrix": {{
            "market_penetration": {{"strategy": "description", "initiatives": ["init1", "init2"], "investment": <number>, "timeline": "X months"}},
            "market_development": {{"strategy": "description", "initiatives": ["init1", "init2"], "investment": <number>, "timeline": "X months"}},
            "product_development": {{"strategy": "description", "initiatives": ["init1", "init2"], "investment": <number>, "timeline": "X months"}},
            "diversification": {{"strategy": "description", "initiatives": ["init1", "init2"], "investment": <number>, "timeline": "X months"}},
            "recommended_strategy": "Which quadrant to focus on and why",
            "implementation_priorities": ["priority1", "priority2", "priority3"]
        }},
        "blue_ocean_strategy": {{
            "eliminate_factors": ["factor1", "factor2"],
            "reduce_factors": ["factor1", "factor2"],
            "raise_factors": ["factor1", "factor2"],
            "create_factors": ["factor1", "factor2"],
            "value_innovation_opportunities": [{{"opportunity": "description", "impact": "high|medium|low", "feasibility": "high|medium|low"}}],
            "new_market_spaces": ["space1", "space2"]
        }},
        "growth_scenarios": [
            {{
                "name": "Conservative",
                "description": "Low risk approach",
                "revenue_projection_3yr": <number>,
                "investment_required": <number>,
                "key_milestones": ["milestone1", "milestone2"],
                "risks": ["risk1", "risk2"],
                "probability_of_success": <0-100>
            }},
            {{
                "name": "Moderate",
                "description": "Balanced approach",
                "revenue_projection_3yr": <number>,
                "investment_required": <number>,
                "key_milestones": ["milestone1", "milestone2"],
                "risks": ["risk1", "risk2"],
                "probability_of_success": <0-100>
            }},
            {{
                "name": "Aggressive",
                "description": "High growth approach",
                "revenue_projection_3yr": <number>,
                "investment_required": <number>,
                "key_milestones": ["milestone1", "milestone2"],
                "risks": ["risk1", "risk2"],
                "probability_of_success": <0-100>
            }}
        ],
        "recommended_direction": "Clear recommendation with rationale"
    }}
    """
    
    response = await call_deepseek_api(prompt)
    if not response:
        return generate_fallback_phase2_analysis(startup_data)
    
    try:
        data = _extract_json_from_response(response)
        return Phase2Analysis(**data)
    except Exception as e:
        logger.error(f"Failed to parse Phase 2 analysis: {e}")
        return generate_fallback_phase2_analysis(startup_data)

def generate_fallback_phase2_analysis(startup_data: Dict[str, Any]) -> Phase2Analysis:
    """Generate fallback Phase 2 analysis if API fails"""
    
    revenue = startup_data.get('annual_revenue_run_rate', 1000000)
    
    return Phase2Analysis(
        strategic_options_overview="The company has multiple growth paths available. Market penetration offers the lowest risk approach while product development could unlock new revenue streams.",
        ansoff_matrix=AnsoffMatrixAnalysis(
            market_penetration={
                "strategy": "Deepen presence in current market",
                "initiatives": ["Increase sales force", "Customer success program"],
                "investment": revenue * 0.5,
                "timeline": "12 months"
            },
            market_development={
                "strategy": "Expand to adjacent markets",
                "initiatives": ["Geographic expansion", "New customer segments"],
                "investment": revenue * 0.8,
                "timeline": "18 months"
            },
            product_development={
                "strategy": "Enhance product offerings",
                "initiatives": ["New features", "Platform capabilities"],
                "investment": revenue * 0.6,
                "timeline": "12 months"
            },
            diversification={
                "strategy": "New products for new markets",
                "initiatives": ["Strategic acquisition", "New product line"],
                "investment": revenue * 1.5,
                "timeline": "24 months"
            },
            recommended_strategy="Market Penetration",
            implementation_priorities=[
                "Optimize current market position",
                "Build sales infrastructure",
                "Enhance customer retention"
            ]
        ),
        blue_ocean_strategy=BlueOceanAnalysis(
            eliminate_factors=["Complex pricing models", "Long implementation times"],
            reduce_factors=["Customer acquisition cost", "Feature complexity"],
            raise_factors=["User experience quality", "Customer support"],
            create_factors=["Self-service capabilities", "Industry-specific solutions"],
            value_innovation_opportunities=[
                {"opportunity": "Vertical-specific solution", "impact": "high", "feasibility": "medium"},
                {"opportunity": "Freemium model", "impact": "medium", "feasibility": "high"}
            ],
            new_market_spaces=["Underserved SMB segment", "Industry-specific verticals"]
        ),
        growth_scenarios=[
            GrowthScenario(
                name="Conservative",
                description="Focus on existing market with incremental improvements",
                revenue_projection_3yr=revenue * 3,
                investment_required=revenue * 0.5,
                key_milestones=["10% market share", "EBITDA positive"],
                risks=["Slow growth", "Competitor advances"],
                probability_of_success=80
            ),
            GrowthScenario(
                name="Moderate",
                description="Balanced growth through market and product expansion",
                revenue_projection_3yr=revenue * 5,
                investment_required=revenue * 1,
                key_milestones=["New market entry", "Product suite launch"],
                risks=["Execution complexity", "Resource constraints"],
                probability_of_success=60
            ),
            GrowthScenario(
                name="Aggressive",
                description="Rapid expansion through multiple initiatives",
                revenue_projection_3yr=revenue * 10,
                investment_required=revenue * 2,
                key_milestones=["Market leadership", "International expansion"],
                risks=["High burn rate", "Quality issues"],
                probability_of_success=40
            )
        ],
        recommended_direction="Pursue moderate growth strategy balancing market penetration with selective product enhancements. This optimizes risk-return profile while building sustainable competitive advantages."
    )

async def analyze_phase3_implementation(startup_data: Dict[str, Any], phase2_results: Phase2Analysis) -> Phase3Analysis:
    """Phase 3: How to Get There? - Implementation roadmap"""
    
    revenue = startup_data.get('annual_revenue_run_rate', 0)
    team_size = startup_data.get('team_size_full_time', 5)
    burn_rate = startup_data.get('monthly_burn_usd', 50000)
    
    prompt = f"""
    Based on Phase 2 recommendation of {phase2_results.recommended_direction}, create Phase 3 implementation plan:
    - Current Revenue: ${revenue:,.0f}
    - Team Size: {team_size}
    - Burn Rate: ${burn_rate:,.0f}/month
    - Chosen Strategy: {phase2_results.ansoff_matrix.recommended_strategy}
    
    Provide detailed implementation plan using:
    1. Balanced Scorecard (4 perspectives with specific KPIs)
    2. OKR Framework (quarterly objectives and key results)
    3. Resource Requirements (people, money, technology, partnerships)
    4. Risk Mitigation Plan (top 5 risks with mitigation strategies)
    5. Success Metrics (leading and lagging indicators)
    
    Return valid JSON matching this structure:
    {{
        "implementation_roadmap_summary": "2-3 paragraph executive summary of implementation plan",
        "balanced_scorecard": [
            {{
                "perspective": "Financial",
                "objectives": ["objective1", "objective2"],
                "measures": ["measure1", "measure2"],
                "targets": ["target1", "target2"],
                "initiatives": ["initiative1", "initiative2"]
            }},
            {{
                "perspective": "Customer",
                "objectives": ["objective1", "objective2"],
                "measures": ["measure1", "measure2"],
                "targets": ["target1", "target2"],
                "initiatives": ["initiative1", "initiative2"]
            }},
            {{
                "perspective": "Internal Process",
                "objectives": ["objective1", "objective2"],
                "measures": ["measure1", "measure2"],
                "targets": ["target1", "target2"],
                "initiatives": ["initiative1", "initiative2"]
            }},
            {{
                "perspective": "Learning & Growth",
                "objectives": ["objective1", "objective2"],
                "measures": ["measure1", "measure2"],
                "targets": ["target1", "target2"],
                "initiatives": ["initiative1", "initiative2"]
            }}
        ],
        "okr_framework": [
            {{
                "quarter": "Q1 2025",
                "objectives": [
                    {{
                        "objective": "Achieve product-market fit",
                        "key_results": [
                            {{"kr": "Reach 100 paying customers", "current": 50, "target": 100}},
                            {{"kr": "Achieve 90% retention rate", "current": 75, "target": 90}},
                            {{"kr": "Generate $500K ARR", "current": 250000, "target": 500000}}
                        ]
                    }}
                ]
            }},
            {{
                "quarter": "Q2 2025",
                "objectives": [
                    {{
                        "objective": "Scale go-to-market",
                        "key_results": [
                            {{"kr": "Hire 5 sales reps", "current": 2, "target": 7}},
                            {{"kr": "Launch partner program", "current": 0, "target": 10}},
                            {{"kr": "Reach $1M ARR", "current": 500000, "target": 1000000}}
                        ]
                    }}
                ]
            }}
        ],
        "resource_requirements": {{
            "human_resources": [
                {{"role": "VP Sales", "level": "Senior", "timeline": "Q1", "cost": 250000}},
                {{"role": "Engineers", "count": 5, "timeline": "Q1-Q2", "cost": 750000}}
            ],
            "financial_resources": {{
                "total_capital_needed": 5000000,
                "runway_extension": 18,
                "monthly_burn_target": 150000,
                "revenue_targets": {{"Q1": 125000, "Q2": 250000, "Q3": 400000, "Q4": 600000}}
            }},
            "technology_resources": ["CRM system", "Analytics platform", "CI/CD infrastructure"],
            "partnership_resources": ["Channel partners", "Technology integrators", "Industry associations"]
        }},
        "risk_mitigation_plan": [
            {{
                "risk": "Customer acquisition costs exceed projections",
                "impact": "High",
                "likelihood": "Medium",
                "mitigation_strategy": "Implement product-led growth features",
                "contingency_plan": "Reduce paid marketing, focus on organic channels"
            }},
            {{
                "risk": "Key talent retention",
                "impact": "High",
                "likelihood": "Low",
                "mitigation_strategy": "Competitive compensation packages with equity",
                "contingency_plan": "Executive search firm on retainer"
            }}
        ],
        "success_metrics": [
            {{"metric": "Monthly Recurring Revenue", "type": "lagging", "target": "$100K by Q2", "frequency": "monthly"}},
            {{"metric": "Customer Acquisition Cost", "type": "leading", "target": "<$1000", "frequency": "weekly"}},
            {{"metric": "Net Promoter Score", "type": "leading", "target": ">50", "frequency": "quarterly"}},
            {{"metric": "Runway Months", "type": "lagging", "target": ">18", "frequency": "monthly"}}
        ]
    }}
    """
    
    response = await call_deepseek_api(prompt)
    if not response:
        return generate_fallback_phase3_analysis(startup_data)
    
    try:
        data = _extract_json_from_response(response)
        return Phase3Analysis(**data)
    except Exception as e:
        logger.error(f"Failed to parse Phase 3 analysis: {e}")
        return generate_fallback_phase3_analysis(startup_data)

def generate_fallback_phase3_analysis(startup_data: Dict[str, Any]) -> Phase3Analysis:
    """Generate fallback Phase 3 analysis if API fails"""
    
    return Phase3Analysis(
        implementation_roadmap_summary="The implementation focuses on achieving product-market fit in Q1, scaling go-to-market in Q2-Q3, and preparing for Series A in Q4. Key success factors include maintaining capital efficiency while accelerating growth.",
        balanced_scorecard=[
            BalancedScorecardPerspective(
                perspective="Financial",
                objectives=["Achieve profitability", "Optimize burn rate"],
                measures=["Monthly burn", "Revenue growth"],
                targets=["<$100K/month", ">30% MoM"],
                initiatives=["Cost optimization", "Pricing strategy"]
            ),
            BalancedScorecardPerspective(
                perspective="Customer",
                objectives=["Improve satisfaction", "Increase retention"],
                measures=["NPS score", "Churn rate"],
                targets=[">50", "<5%"],
                initiatives=["Customer success program", "Product improvements"]
            ),
            BalancedScorecardPerspective(
                perspective="Internal Process",
                objectives=["Streamline operations", "Improve efficiency"],
                measures=["Cycle time", "Automation rate"],
                targets=["<2 days", ">80%"],
                initiatives=["Process automation", "Tool implementation"]
            ),
            BalancedScorecardPerspective(
                perspective="Learning & Growth",
                objectives=["Build team capabilities", "Foster innovation"],
                measures=["Training hours", "Innovation index"],
                targets=[">40 hrs/year", ">8/10"],
                initiatives=["Training program", "Innovation labs"]
            )
        ],
        okr_framework=[
            OKRSet(
                quarter="Q1 2025",
                objectives=[
                    {
                        "objective": "Achieve product-market fit",
                        "key_results": [
                            {"kr": "100 paying customers", "current": 50, "target": 100},
                            {"kr": "90% retention rate", "current": 75, "target": 90}
                        ]
                    }
                ]
            ),
            OKRSet(
                quarter="Q2 2025",
                objectives=[
                    {
                        "objective": "Scale revenue",
                        "key_results": [
                            {"kr": "$1M ARR", "current": 500000, "target": 1000000},
                            {"kr": "5 enterprise deals", "current": 1, "target": 5}
                        ]
                    }
                ]
            )
        ],
        resource_requirements=ResourceRequirements(
            human_resources=[
                {"role": "VP Sales", "level": "Senior", "timeline": "Q1", "cost": 250000},
                {"role": "Engineers", "count": 5, "timeline": "Q1-Q2", "cost": 750000}
            ],
            financial_resources={
                "total_capital_needed": 5000000,
                "runway_extension": 18,
                "monthly_burn_target": 150000
            },
            technology_resources=["Salesforce CRM", "Mixpanel Analytics", "AWS Infrastructure"],
            partnership_resources=["Channel partners", "System integrators"]
        ),
        risk_mitigation_plan=[
            RiskMitigationItem(
                risk="Market competition intensifies",
                impact="High",
                likelihood="Medium",
                mitigation_strategy="Accelerate product differentiation",
                contingency_plan="Focus on niche market segment"
            ),
            RiskMitigationItem(
                risk="Funding environment deteriorates",
                impact="High",
                likelihood="Low",
                mitigation_strategy="Extend runway, improve unit economics",
                contingency_plan="Bridge financing from existing investors"
            )
        ],
        success_metrics=[
            {"metric": "ARR", "type": "lagging", "target": "$2M by year-end", "frequency": "monthly"},
            {"metric": "CAC Payback", "type": "leading", "target": "<12 months", "frequency": "monthly"},
            {"metric": "Employee NPS", "type": "leading", "target": ">70", "frequency": "quarterly"}
        ]
    )

@michelin_router.post("/strategic-analysis", response_model=MichelinAnalysisResponse)
async def perform_michelin_analysis(request: MichelinAnalysisRequest):
    """Perform complete Michelin 3-phase strategic analysis"""
    
    try:
        startup_data = request.startup_data
        company_name = startup_data.get('company_name', 'Startup')
        
        # Execute all three phases
        logger.info("Starting Phase 1 analysis...")
        phase1 = await analyze_phase1_current_state(startup_data)
        
        logger.info("Starting Phase 2 analysis...")
        phase2 = await analyze_phase2_strategic_direction(startup_data, phase1)
        
        logger.info("Starting Phase 3 analysis...")
        phase3 = await analyze_phase3_implementation(startup_data, phase2)
        
        # Generate executive briefing
        executive_briefing = f"""
        {company_name} is positioned as a {phase1.bcg_matrix.position} in its market with significant growth potential. 
        The recommended strategic direction is {phase2.recommended_direction}. 
        Implementation will require ${phase3.resource_requirements.financial_resources.get('total_capital_needed', 5000000):,.0f} 
        in capital and focus on {phase3.okr_framework[0].objectives[0]['objective']} as the immediate priority.
        
        The company faces {phase1.porters_five_forces.overall_industry_attractiveness} industry attractiveness 
        but can leverage its {phase1.swot_analysis.strengths[0]['item']} to capture market opportunity.
        Success hinges on executing the {phase2.ansoff_matrix.recommended_strategy} strategy while 
        maintaining capital efficiency and achieving key milestones.
        """
        
        # Extract key recommendations
        key_recommendations = [
            f"Focus on {phase2.ansoff_matrix.recommended_strategy} as primary growth strategy",
            f"Target {phase3.okr_framework[0].objectives[0]['key_results'][0]['kr']}",
            f"Implement {phase3.balanced_scorecard[0].initiatives[0]} to improve financial performance",
            f"Mitigate '{phase3.risk_mitigation_plan[0].risk}' through {phase3.risk_mitigation_plan[0].mitigation_strategy}"
        ]
        
        # Define critical success factors
        critical_success_factors = [
            "Achieve product-market fit within 6 months",
            "Maintain burn rate below target while scaling",
            "Build competitive moats through differentiation",
            "Secure Series A funding within 12 months"
        ]
        
        # Create next steps
        next_steps = [
            {
                "timeline": "30 days",
                "actions": [
                    "Finalize strategic plan with board approval",
                    "Begin recruitment for key positions",
                    "Launch first strategic initiative"
                ]
            },
            {
                "timeline": "60 days",
                "actions": [
                    "Complete team scaling for Q1",
                    "Implement new processes and systems",
                    "Achieve first OKR milestone"
                ]
            },
            {
                "timeline": "90 days",
                "actions": [
                    "Review Q1 performance against targets",
                    "Adjust strategy based on learnings",
                    "Prepare for next funding round"
                ]
            }
        ]
        
        return MichelinAnalysisResponse(
            company_name=company_name,
            analysis_date=datetime.now().isoformat(),
            executive_briefing=executive_briefing.strip(),
            phase1=phase1,
            phase2=phase2,
            phase3=phase3,
            key_recommendations=key_recommendations,
            critical_success_factors=critical_success_factors,
            next_steps=next_steps
        )
        
    except Exception as e:
        logger.error(f"Michelin analysis failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@michelin_router.get("/status")
async def check_michelin_status():
    """Check if Michelin analysis service is available"""
    return {
        "status": "operational",
        "framework_analysis_available": FRAMEWORK_ANALYSIS_AVAILABLE,
        "deepseek_configured": bool(DEEPSEEK_API_KEY),
        "version": "1.0.0"
    }

# Shutdown handler for cleanup
async def shutdown_michelin_engine():
    """Cleanup resources on shutdown"""
    logger.info("Shutting down Michelin analysis engine")
    # Add any cleanup code here if needed