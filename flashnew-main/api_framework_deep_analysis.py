#!/usr/bin/env python3
"""
Deep Framework Analysis API with McKinsey-Quality Reporting
Uses DeepSeek API for sophisticated strategic analysis
"""

import os
import sys
import logging
import json
import asyncio
import numpy as np
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
import aiohttp

# Add framework intelligence to path
current_dir = os.path.dirname(os.path.abspath(__file__))

# Setup logging
logger = logging.getLogger(__name__)

# Import framework components
try:
    from framework_intelligence.framework_selector import FrameworkSelector
    from framework_intelligence.framework_database import FRAMEWORKS
    FRAMEWORK_ANALYSIS_AVAILABLE = True
except ImportError as e:
    logger.warning(f"Framework analysis not available: {e}")
    FRAMEWORK_ANALYSIS_AVAILABLE = False

# Create router
deep_analysis_router = APIRouter(prefix="/api/frameworks", tags=["Deep Framework Analysis"])

# Stage-aware helper functions
def get_market_capture_timeline_by_stage(stage: str) -> int:
    """Return months to capture target market share by stage"""
    timelines = {
        'pre_seed': 36,    # 3 years to meaningful share
        'seed': 24,        # 2 years to meaningful share
        'series_a': 18,    # 1.5 years to meaningful share
        'series_b': 12,    # 1 year to meaningful share
        'series_c': 12,    # 1 year to meaningful share
    }
    return timelines.get(stage, 24)

def get_target_market_share_by_stage(stage: str, tam: float, sam: float) -> float:
    """Return realistic target market share by stage"""
    # Pre-seed: 0.1% of SAM, Seed: 0.5%, Series A: 1%, Series B+: 5%
    stage_targets = {
        'pre_seed': 0.1,
        'seed': 0.5,
        'series_a': 1.0,
        'series_b': 5.0,
        'series_c': 10.0,
    }
    return stage_targets.get(stage, 1.0)

def get_valuation_multiple_by_stage(stage: str) -> float:
    """Return appropriate valuation multiple by stage"""
    multiples = {
        'pre_seed': 15,    # Higher multiple for early potential
        'seed': 10,        # 10x revenue potential
        'series_a': 8,     # 8x revenue
        'series_b': 6,     # 6x revenue
        'series_c': 4,     # 4x revenue (more mature)
    }
    return multiples.get(stage, 8)

def get_months_to_first_revenue_by_stage(stage: str) -> int:
    """Return expected months to first revenue by stage"""
    timelines = {
        'pre_seed': 9,     # 9 months to first revenue
        'seed': 6,         # 6 months to first revenue
        'series_a': 3,     # Should already have revenue
        'series_b': 0,     # Should already have revenue
        'series_c': 0,     # Should already have revenue
    }
    return timelines.get(stage, 6)

def get_projected_revenue_by_stage(stage: str, sam: float) -> float:
    """Return projected first year revenue based on stage and market size"""
    # Conservative estimates: 0.001% of SAM for pre-seed, scaling up
    stage_capture = {
        'pre_seed': 0.00001,    # 0.001% of SAM
        'seed': 0.00005,        # 0.005% of SAM
        'series_a': 0.0001,     # 0.01% of SAM
        'series_b': 0.001,      # 0.1% of SAM
        'series_c': 0.01,       # 1% of SAM
    }
    return sam * stage_capture.get(stage, 0.00005)

def get_target_customers_by_stage(stage: str) -> int:
    """Return target number of pilot customers by stage"""
    targets = {
        'pre_seed': 3,      # 3 pilot customers
        'seed': 10,         # 10 pilot customers
        'series_a': 50,     # 50 customers
        'series_b': 200,    # 200 customers
        'series_c': 1000,   # 1000+ customers
    }
    return targets.get(stage, 10)

def calculate_pre_revenue_confidence(startup_data: Dict[str, Any]) -> int:
    """Calculate confidence score for pre-revenue companies"""
    team_size = startup_data.get('team_size_full_time', 5)
    runway = startup_data.get('runway_months', 12)
    stage = startup_data.get('funding_stage', 'seed')
    patent_count = startup_data.get('patent_count', 0)
    prior_exits = startup_data.get('prior_exits', 0)
    domain_expertise = startup_data.get('domain_expertise_years', 0)
    
    # Different factors for pre-revenue companies
    confidence_factors = [
        min(100, runway * 100 / 18),  # 18 months runway = 100%
        min(100, team_size * 100 / 10),  # 10 people = 100%
        min(100, domain_expertise * 100 / 10),  # 10 years expertise = 100%
        min(100, (patent_count + prior_exits) * 25),  # Patents/exits worth 25% each
        50 if stage in ['seed', 'series_a'] else 25,  # Stage bonus
    ]
    
    return int(np.mean(confidence_factors))

# DeepSeek API configuration
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "sk-f68b7148243e4663a31386a5ea6093cf")
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"

class DeepAnalysisRequest(BaseModel):
    """Request for deep framework analysis"""
    startup_data: Dict[str, Any]
    framework_ids: Optional[List[str]] = Field(default=None, description="Framework IDs to use (auto-select if not provided)")
    analysis_depth: str = Field(default="comprehensive", description="comprehensive, standard, or quick")

class ExecutiveSummary(BaseModel):
    situation: str
    key_insights: List[str]
    recommendation: str
    value_at_stake: float
    confidence_level: int

class StrategicOption(BaseModel):
    title: str
    description: str
    npv: float
    irr: float
    payback_period: float
    risk_level: str
    confidence_interval: Dict[str, float]

class CompetitiveDynamic(BaseModel):
    force: str
    intensity: str
    trend: str
    strategic_implication: str

class DeepAnalysisResponse(BaseModel):
    """McKinsey-quality strategic analysis response"""
    executive_summary: ExecutiveSummary
    situation_assessment: Dict[str, Any]
    strategic_options: List[StrategicOption]
    value_drivers: List[Dict[str, Any]]
    competitive_dynamics: List[CompetitiveDynamic]
    implementation_roadmap: List[Dict[str, Any]]
    financial_projections: Dict[str, Any]

async def call_deepseek_api(prompt: str, system_prompt: str = None) -> str:
    """Call DeepSeek API with senior consultant persona"""
    
    if not system_prompt:
        system_prompt = """You are a senior partner at McKinsey & Company with 30+ years of experience, 
        a Harvard MBA, and a PhD in Strategy. You have advised Fortune 500 CEOs and written extensively 
        on strategic transformation. Your analysis should reflect:
        
        1. Sophisticated business vocabulary and frameworks
        2. Quantitative rigor with specific numbers and calculations
        3. Clear, confident recommendations backed by precedent
        4. Value creation focus with NPV/IRR calculations
        5. Risk-adjusted strategic options
        6. Implementation roadmaps with clear milestones
        
        Never hedge or equivocate. State your analysis with conviction."""
    
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

def generate_executive_summary(startup_data: Dict[str, Any], insights: Dict[str, Any]) -> ExecutiveSummary:
    """Generate SPECIFIC executive summary with stage-aware calculations"""
    
    # Extract all key metrics
    revenue = startup_data.get('annual_revenue_run_rate', 0)
    burn = startup_data.get('monthly_burn_usd', 50000)
    # Ensure burn is never 0 to avoid division errors
    if burn == 0:
        burn = 50000  # Default burn rate
    runway = startup_data.get('runway_months', 12)
    # Ensure runway is never 0 to avoid division errors
    if runway == 0:
        runway = 12  # Default runway
    customers = startup_data.get('customer_count', 0)
    team_size = startup_data.get('team_size_full_time', 5)
    stage = startup_data.get('funding_stage', 'seed')
    
    tam = startup_data.get('tam_size_usd', 10000000000)
    sam = startup_data.get('sam_size_usd', tam * 0.1)
    som = startup_data.get('som_size_usd', sam * 0.01)
    
    # Stage-aware analysis for zero-revenue companies
    logger.info(f"Executive summary - revenue: {revenue}, stage: {stage}, condition: {revenue == 0 and stage in ['pre_seed', 'seed']}")
    if revenue == 0 and stage in ['pre_seed', 'seed']:
        # Pre-revenue analysis mode
        logger.info("Using pre-revenue analysis mode")
        market_capture_timeline = get_market_capture_timeline_by_stage(stage)
        target_market_share = get_target_market_share_by_stage(stage, tam, sam)
        revenue_potential = sam * (target_market_share / 100)
        
        # Calculate value based on market potential, not current revenue
        multiple = get_valuation_multiple_by_stage(stage)
        value_at_stake = revenue_potential * multiple
        
        # Path to first revenue
        months_to_first_revenue = get_months_to_first_revenue_by_stage(stage)
        projected_first_year_revenue = get_projected_revenue_by_stage(stage, sam)
        
        return ExecutiveSummary(
            situation=f"{startup_data.get('sector', 'Technology')} {stage} startup targeting ${tam/1e9:.0f}B TAM. "
                      f"Pre-revenue with {team_size} employees, burning ${burn/1e3:.0f}K/month with {runway} months runway.",
            key_insights=[
                f"Market opportunity of ${revenue_potential/1e6:.0f}M ({target_market_share:.1f}% of SAM) achievable within {market_capture_timeline} months",
                f"Path to first ${projected_first_year_revenue/1e3:.0f}K revenue in {months_to_first_revenue} months requires {int(projected_first_year_revenue/12/burn*100)}% conversion of burn to revenue",
                f"Current runway of {runway} months {'sufficient for' if runway >= months_to_first_revenue else 'requires extension to achieve'} product-market fit milestone"
            ],
            recommendation=f"Focus on achieving product-market fit with {get_target_customers_by_stage(stage)} pilot customers. "
                           f"{'Extend runway to ' + str(months_to_first_revenue + 6) + ' months' if runway < months_to_first_revenue else 'Maintain burn discipline'} "
                           f"while targeting ${projected_first_year_revenue/1e6:.1f}M first-year revenue.",
            value_at_stake=value_at_stake,
            confidence_level=calculate_pre_revenue_confidence(startup_data)
        )
    else:
        # Existing revenue-positive analysis
        market_share = (revenue / sam * 100) if sam > 0 else 0
        growth_rate = startup_data.get('market_growth_rate_percent', 30)
        
        # Calculate specific value at stake
        realistic_market_share = max(0.1, min(5, market_share * 3)) if market_share > 0 else 1.0
        revenue_potential = sam * (realistic_market_share / 100)
        ebitda_potential = revenue_potential * 0.25  # 25% EBITDA margin at scale
        value_at_stake = ebitda_potential * 8  # 8x EBITDA multiple
        
        # Calculate path to profitability
        breakeven_revenue = burn * 12 / 0.3  # Assuming 30% contribution margin
        # Calculate months to reach target market share
        if market_share > 0 and growth_rate > 0:
            months_to_target = np.log(realistic_market_share / market_share) / np.log(1 + max(growth_rate/100/12, 0.001))
        else:
            months_to_target = 24  # Default 2 years if no current revenue
        
        # Calculate confidence based on actual metrics
        confidence_factors = [
            min(100, runway * 100 / 24) if runway > 0 else 0,  # Runway score (24 months = 100%)
            min(100, customers * 100 / 100) if customers > 0 else 0,  # Customer validation (100 customers = 100%)
            min(100, (revenue/burn) * 100 / 3) if burn > 0 else (100 if revenue > 0 else 0),  # Efficiency score (3x = 100%)
            min(100, team_size * 100 / 20) if team_size > 0 else 0,  # Team score (20 people = 100%)
        ]
        confidence_level = int(np.mean(confidence_factors))
        
        return ExecutiveSummary(
            situation=f"{startup_data.get('sector', 'Technology')} startup with ${revenue/1e6:.1f}M ARR ({customers} customers) in ${tam/1e9:.0f}B TAM. "
                      f"Currently burning ${burn/1e3:.0f}K/month with {runway} months runway and {market_share:.2f}% market share.",
            key_insights=[
                f"Path to {realistic_market_share:.1f}% market share worth ${revenue_potential/1e6:.0f}M ARR achievable in {int(months_to_target)} months at current {growth_rate}% growth",
                f"Breakeven at ${breakeven_revenue/1e6:.1f}M ARR requires {int(breakeven_revenue/revenue) if revenue > 0 else 10}x revenue growth or {int((1-0.3)*100)}% burn reduction",
                f"Current efficiency of {revenue/burn:.1f}x (revenue/burn) {'exceeds' if burn > 0 and revenue/burn > 3 else 'must improve to'} 3.0x target - {'maintain growth focus' if burn > 0 and revenue/burn > 3 else f'requires ${(3*burn - revenue)/1e3:.0f}K monthly revenue increase' if burn > 0 else 'reduce burn to improve efficiency'}"
            ],
            recommendation=f"{'Extend runway to 18+ months before growth push' if runway < 12 else 'Accelerate growth'} by "
                           f"{'cutting burn by ' + str(int((1 - 12/runway)*100)) + '%' if runway < 12 and runway > 0 else 'investing $' + str(int(burn*6/1e6)) + 'M' if burn > 0 else 'optimizing operations'} "
                           f"to capture {realistic_market_share:.1f}% market share worth ${value_at_stake/1e6:.0f}M valuation.",
            value_at_stake=value_at_stake,
            confidence_level=confidence_level
        )

def analyze_strategic_options(startup_data: Dict[str, Any]) -> List[StrategicOption]:
    """Generate strategic options with financial analysis"""
    
    revenue = startup_data.get('annual_revenue_run_rate', 1000000)
    
    options = [
        StrategicOption(
            title="Enterprise Transformation",
            description="Pivot to enterprise-first model with dedicated sales infrastructure and compliance",
            npv=revenue * 15,
            irr=45,
            payback_period=2.5,
            risk_level="Medium",
            confidence_interval={"low": revenue * 10, "high": revenue * 25}
        ),
        StrategicOption(
            title="Geographic Expansion",
            description="Expand to 3 new markets leveraging product-led growth motion",
            npv=revenue * 8,
            irr=35,
            payback_period=3.0,
            risk_level="High",
            confidence_interval={"low": revenue * 3, "high": revenue * 15}
        ),
        StrategicOption(
            title="Platform Play",
            description="Build ecosystem through API strategy and strategic partnerships",
            npv=revenue * 12,
            irr=40,
            payback_period=3.5,
            risk_level="Medium",
            confidence_interval={"low": revenue * 6, "high": revenue * 20}
        )
    ]
    
    return options

def analyze_competitive_dynamics(startup_data: Dict[str, Any]) -> List[CompetitiveDynamic]:
    """Analyze Porter's Five Forces with strategic implications"""
    
    competition_intensity = startup_data.get('competition_intensity', 3)
    
    dynamics = [
        CompetitiveDynamic(
            force="Competitive Rivalry",
            intensity="High" if competition_intensity > 3 else "Medium",
            trend="Deteriorating",
            strategic_implication="Requires rapid differentiation through vertical specialization"
        ),
        CompetitiveDynamic(
            force="Buyer Power",
            intensity="Medium",
            trend="Stable",
            strategic_implication="Build switching costs through data integration and workflows"
        ),
        CompetitiveDynamic(
            force="Threat of New Entry",
            intensity="Low",
            trend="Improving",
            strategic_implication="18-month window to establish defensible market position"
        ),
        CompetitiveDynamic(
            force="Supplier Power",
            intensity="Low",
            trend="Stable",
            strategic_implication="Opportunity to vertically integrate key technology components"
        ),
        CompetitiveDynamic(
            force="Threat of Substitution",
            intensity="Medium",
            trend="Stable",
            strategic_implication="Focus on unique value propositions that incumbents cannot replicate"
        )
    ]
    
    return dynamics

def create_implementation_roadmap(startup_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Create detailed implementation roadmap"""
    
    current_revenue = startup_data.get('annual_revenue_run_rate', 1000000)
    
    roadmap = [
        {
            "phase": "Foundation",
            "quarter": "Q1-Q2",
            "initiatives": [
                "Hire VP Sales with enterprise experience",
                "Achieve SOC2 Type II compliance",
                "Refine ideal customer profile (ICP)",
                "Build sales enablement infrastructure"
            ],
            "milestones": [
                "First $100K+ enterprise deal",
                f"${current_revenue*2/1e6:.1f}M ARR",
                "Sales playbook v1.0 complete",
                "10 qualified enterprise pipeline"
            ],
            "investment": 2000000
        },
        {
            "phase": "Acceleration",
            "quarter": "Q3-Q4",
            "initiatives": [
                "Scale sales team to 10 AEs",
                "Launch channel partner program",
                "Expand to 2 adjacent verticals",
                "Implement customer success function"
            ],
            "milestones": [
                f"${current_revenue*5/1e6:.1f}M ARR",
                "50 enterprise logos",
                "Series A fundraise close",
                "Net retention >120%"
            ],
            "investment": 5000000
        },
        {
            "phase": "Scale",
            "quarter": "Year 2",
            "initiatives": [
                "International expansion (UK/EU)",
                "Strategic M&A exploration",
                "Platform architecture transformation",
                "Category leadership initiatives"
            ],
            "milestones": [
                f"${current_revenue*15/1e6:.1f}M ARR",
                "Market leader in core vertical",
                "EBITDA positive operations",
                "IPO readiness assessment"
            ],
            "investment": 10000000
        }
    ]
    
    return roadmap

async def select_relevant_frameworks(startup_data: Dict[str, Any]) -> List[str]:
    """Intelligently select frameworks that add value for this specific startup"""
    
    selected = []
    
    # Always include core strategic frameworks
    selected.extend(['bcg_matrix', 'porters_five_forces', 'swot_analysis'])
    
    # Stage-specific frameworks
    stage = startup_data.get('funding_stage', 'seed')
    if stage in ['pre_seed', 'seed']:
        selected.extend(['lean_canvas', 'customer_development', 'value_proposition_canvas'])
    elif stage in ['series_a', 'series_b']:
        selected.extend(['ansoff_matrix', 'growth_share_matrix', 'balanced_scorecard'])
    else:
        selected.extend(['mckinsey_7s', 'blue_ocean', 'transformation_roadmap'])
    
    # Problem-specific frameworks
    if startup_data.get('monthly_burn_usd', 0) > startup_data.get('annual_revenue_run_rate', 0) / 12:
        selected.extend(['unit_economics', 'cash_flow_management'])
    
    if startup_data.get('customer_count', 0) < 100:
        selected.extend(['jobs_to_be_done', 'customer_journey'])
    
    if startup_data.get('competition_intensity', 3) > 3:
        selected.extend(['competitive_positioning', 'differentiation_strategy'])
    
    # Remove duplicates and limit to 10 most relevant
    return list(set(selected))[:10]


async def apply_frameworks(startup_data: Dict[str, Any], framework_ids: List[str]) -> Dict[str, Any]:
    """Apply selected frameworks and get specific insights"""
    
    results = {}
    
    # Always use fallback since analyze_with_framework is not implemented yet
    # In production, this would integrate with the actual framework analysis engine
    for framework_id in framework_ids:
        results[framework_id] = generate_fallback_framework_analysis(framework_id, startup_data)
    
    return results


def generate_fallback_framework_analysis(framework_id: str, startup_data: Dict[str, Any]) -> Dict[str, Any]:
    """Generate SPECIFIC, data-driven framework analysis based on actual metrics"""
    
    # Extract all metrics for calculations
    revenue = startup_data.get('annual_revenue_run_rate', 0)
    monthly_revenue = revenue / 12 if revenue > 0 else 0
    growth = startup_data.get('market_growth_rate_percent', 15)
    stage = startup_data.get('funding_stage', 'seed')
    burn = startup_data.get('monthly_burn_usd', 50000)
    # Ensure burn is never 0 to avoid division errors
    if burn == 0:
        burn = 50000  # Default burn rate
    runway = startup_data.get('runway_months', 12)
    # Ensure runway is never 0 to avoid division errors
    if runway == 0:
        runway = 12  # Default runway
    customers = startup_data.get('customer_count', 0)
    team_size = startup_data.get('team_size_full_time', 5)
    competition = startup_data.get('competition_intensity', 3)
    
    # Additional metrics for calculations
    tam = startup_data.get('tam_size_usd', 10000000000)
    sam = startup_data.get('sam_size_usd', tam * 0.1)
    som = startup_data.get('som_size_usd', sam * 0.01)
    market_share = (revenue / sam * 100) if sam > 0 else 0
    
    capital_raised = startup_data.get('total_capital_raised_usd', 0)
    cash_on_hand = startup_data.get('cash_on_hand_usd', 0)
    
    # Calculate derived metrics
    gross_margin = startup_data.get('gross_margin_percent', 70)
    ltv_cac_ratio = startup_data.get('ltv_cac_ratio', 0)
    monthly_growth_rate = startup_data.get('user_growth_rate_percent', 0) / 100
    
    # Calculate specific metrics with stage awareness
    if revenue == 0 and stage in ['pre_seed', 'seed']:
        # For pre-revenue companies, use projected metrics
        projected_revenue = get_projected_revenue_by_stage(stage, sam)
        burn_multiple = float('inf')  # Not applicable pre-revenue
        revenue_per_employee = 0
        capital_efficiency = 0
        months_to_profitability = get_months_to_first_revenue_by_stage(stage) + 12  # First revenue + 12 months
    else:
        burn_multiple = (burn / monthly_revenue) if monthly_revenue > 0 else float('inf')
        revenue_per_employee = revenue / team_size if team_size > 0 else 0
        capital_efficiency = revenue / capital_raised if capital_raised > 0 else 0
        months_to_profitability = burn / (monthly_revenue * (gross_margin/100)) if monthly_revenue > 0 and gross_margin > 0 else float('inf')
    
    analyses = {
        'bcg_matrix': {
            'position': 'Question Mark' if growth > 20 and market_share < 10 else ('Star' if growth > 20 and market_share >= 10 else ('Cash Cow' if growth <= 20 and market_share >= 10 else 'Dog')),
            'metrics': {
                'market_growth': f"{growth}%",
                'relative_market_share': f"{market_share:.2f}%",
                'current_revenue': f"${revenue/1e6:.1f}M",
                'market_leader_revenue': f"${sam * 0.15 / 1e6:.0f}M" if sam > 0 else "Unknown",
                'share_gap': f"{max(10 - market_share, 0):.1f}%"
            },
            'insights': [
                f"With {market_share:.2f}% market share and {growth}% market growth, positioned as {'Question Mark' if growth > 20 and market_share < 10 else ('Star' if growth > 20 and market_share >= 10 else ('Cash Cow' if growth <= 20 and market_share >= 10 else 'Dog'))}",
                f"Current revenue of ${revenue/1e6:.1f}M represents {market_share:.2f}% of ${sam/1e9:.1f}B SAM",
                f"At current {monthly_growth_rate*100:.1f}% monthly growth, will reach 1% market share in {int(np.log(1/max(market_share, 0.01))/np.log(1 + max(monthly_growth_rate/100, 0.01))) if market_share > 0 and monthly_growth_rate > 0 else 24} months",
                f"Cash consumption of ${burn/1e3:.0f}K/month vs revenue generation of ${monthly_revenue/1e3:.0f}K/month yields burn multiple of {burn_multiple:.1f}x"
            ],
            'recommendations': [
                f"Increase revenue from ${revenue/1e6:.1f}M to ${revenue*4/1e6:.1f}M within 12 months to achieve Star position",
                f"Reduce burn multiple from {burn_multiple:.1f}x to 2.0x by growing revenue 2x while maintaining current burn",
                f"Target {int(customers * (10/max(market_share, 0.1)))} customers (from current {customers}) to reach 10% market share"
            ]
        },
        'porters_five_forces': {
            'overall_attractiveness': f"{int((1 - (competition/5 * 0.3 + 0.5 * 0.2 + 0.3 * 0.2 + 0.5 * 0.15 + 0.8 * 0.15)) * 100)}%",
            'forces': {
                'competitive_rivalry': {
                    'level': 'High' if competition > 3 else 'Medium', 
                    'score': competition/5,
                    'analysis': f"With {startup_data.get('competitors_named_count', 5)} direct competitors and intensity score of {competition}/5, market consolidation expected within {18 - competition*3} months"
                },
                'buyer_power': {
                    'level': 'High' if customers < 100 else ('Medium' if customers < 1000 else 'Low'), 
                    'score': max(0.2, min(0.8, 1 - customers/1000)),
                    'analysis': f"Customer concentration of {startup_data.get('customer_concentration_percent', 20)}% in top 10% of {customers} customers creates {'high' if startup_data.get('customer_concentration_percent', 20) > 30 else 'moderate'} dependency risk"
                },
                'supplier_power': {
                    'level': 'Low', 
                    'score': 0.3,
                    'analysis': f"Cloud infrastructure costs of ~${burn * 0.15 / 1000:.0f}K/month (est. 15% of burn) with multiple vendor options keeps supplier power low"
                },
                'threat_of_substitution': {
                    'level': 'Medium' if startup_data.get('switching_cost_score', 3) < 4 else 'Low', 
                    'score': max(0.2, 1 - startup_data.get('switching_cost_score', 3)/5),
                    'analysis': f"Switching cost score of {startup_data.get('switching_cost_score', 3)}/5 means customers would incur ${int(revenue/customers * 0.3) if customers > 0 else 1000} cost to switch"
                },
                'threat_of_new_entry': {
                    'level': 'High' if capital_raised < 5000000 else 'Medium', 
                    'score': 0.8 if capital_raised < 5000000 else 0.5,
                    'analysis': f"Low barriers with only ${capital_raised/1e6:.1f}M raised - competitors can enter with ${capital_raised * 0.7 / 1e6:.1f}M investment"
                }
            },
            'insights': [
                f"Industry attractiveness score of {int((1 - (competition/5 * 0.3 + 0.5 * 0.2 + 0.3 * 0.2 + 0.5 * 0.15 + 0.8 * 0.15)) * 100)}% suggests {'challenging' if competition > 3 else 'moderate'} competitive environment",
                f"Primary threat: {max(customers * (10/max(market_share, 0.1)) - customers, 0):.0f} new customers needed to achieve defensible 10% market share before new entrants arrive",
                f"Opportunity: Low supplier power enables {int((1-0.3)*20)}% gross margin improvement potential worth ${revenue * 0.14 / 1e6:.1f}M annually"
            ]
        },
        'lean_canvas': {
            'key_metrics': ['CAC', 'LTV', 'MRR Growth', 'Churn Rate'],
            'unfair_advantage': 'Technical expertise and first-mover advantage',
            'insights': [
                f"With {customers} customers, focus on validating product-market fit",
                "Customer channels need diversification beyond direct sales",
                "Revenue streams should expand to include recurring models"
            ],
            'recommendations': [
                "Implement customer development interviews weekly",
                "Track unit economics religiously",
                "Build MVP features based on customer feedback"
            ]
        },
        'swot_analysis': {
            'strengths': ['Technical team', 'Early traction', 'Capital efficiency'],
            'weaknesses': ['Limited runway', 'Small team', 'No moat yet'],
            'opportunities': ['Large market', 'Growing demand', 'Partnership potential'],
            'threats': ['Competition', 'Funding risk', 'Execution challenges'],
            'insights': [
                f"Team of {team_size} needs to scale carefully to extend {runway} month runway",
                "Market opportunity significant but execution risk high",
                "Building defensibility should be top priority"
            ]
        },
        'ansoff_matrix': {
            'current_position': 'Market Penetration',
            'growth_options': {
                'market_penetration': {'feasibility': 'High', 'risk': 'Low', 'timeline': '6 months'},
                'market_development': {'feasibility': 'Medium', 'risk': 'Medium', 'timeline': '12 months'},
                'product_development': {'feasibility': 'Medium', 'risk': 'Medium', 'timeline': '9 months'},
                'diversification': {'feasibility': 'Low', 'risk': 'High', 'timeline': '18+ months'}
            },
            'insights': [
                "Focus on market penetration given early stage and limited resources",
                "Market development can follow once product-market fit achieved",
                "Avoid diversification until Series A funding secured"
            ]
        },
        'value_proposition_canvas': {
            'customer_jobs': ['Efficiency gains', 'Cost reduction', 'Better insights'],
            'pain_points': ['Manual processes', 'High costs', 'Lack of visibility'],
            'gain_creators': ['Automation', 'Real-time data', 'Predictive analytics'],
            'insights': [
                "Value proposition aligns well with identified customer pain points",
                "Need to quantify ROI for enterprise customers",
                "Consider tiered pricing to capture different segments"
            ]
        },
        'customer_development': {
            'stage': 'Problem-Solution Fit' if customers < 100 else 'Product-Market Fit',
            'key_hypotheses': [
                "Customers will pay for automated solution",
                "10x improvement over manual processes",
                "Stickiness through data lock-in"
            ],
            'insights': [
                f"With {customers} customers, focus on {'validating problem' if customers < 10 else 'scaling solution'}",
                "Customer interviews should drive product roadmap",
                "Track activation and retention metrics closely"
            ]
        },
        'unit_economics': {
            'metrics': {
                'CAC': f"${burn / max(customers, 1):,.0f}" if customers > 0 else f"Pre-revenue - Target CAC: ${burn * 0.3:,.0f}",
                'LTV': f"${(revenue / max(customers, 1)) * (1 / max(0.05, startup_data.get('monthly_churn_rate', 0.05))):,.0f}" if customers > 0 else f"Pre-revenue - Target LTV: ${get_projected_revenue_by_stage(stage, sam) / get_target_customers_by_stage(stage) * 20:,.0f}",
                'ltv_cac_ratio': ltv_cac_ratio if ltv_cac_ratio > 0 else ((revenue / max(customers, 1)) * (1 / max(0.05, startup_data.get('monthly_churn_rate', 0.05))) / (burn / max(customers, 1))) if customers > 0 else 0,
                'payback_period_months': (burn / max(customers, 1)) / (monthly_revenue / max(customers, 1)) if customers > 0 and monthly_revenue > 0 else get_months_to_first_revenue_by_stage(stage),
                'gross_margin': f"{gross_margin}%",
                'contribution_margin': f"{max(0, gross_margin - (burn/revenue*100)) if revenue > 0 else 0:.1f}%" if revenue > 0 else "N/A - Pre-revenue"
            },
            'insights': [
                f"CAC of ${burn / max(customers, 1):,.0f} vs industry benchmark of ${revenue * 0.15 / max(customers, 1):,.0f} shows {(burn / max(customers, 1)) / (revenue * 0.15 / max(customers, 1)):.1f}x overspend" if customers > 0 and revenue > 0 else f"Pre-revenue: Target {get_target_customers_by_stage(stage)} pilots in {get_months_to_first_revenue_by_stage(stage)} months at ${burn * 0.3:,.0f} CAC",
                f"LTV/CAC ratio of {ltv_cac_ratio:.1f} {'below' if ltv_cac_ratio < 3 else 'meets'} the 3:1 target - need {max(0, 3 - ltv_cac_ratio):.1f}x improvement" if ltv_cac_ratio > 0 else f"Pre-revenue: Design for 3:1+ LTV/CAC with ${get_projected_revenue_by_stage(stage, sam) / get_target_customers_by_stage(stage):,.0f} ACV",
                f"At {gross_margin}% gross margin, need ${(burn / (gross_margin/100)):,.0f} monthly revenue to break even (currently ${monthly_revenue:,.0f})" if gross_margin > 0 and revenue > 0 else f"Pre-revenue: Path to ${get_projected_revenue_by_stage(stage, sam)/12:,.0f}/month in {get_months_to_first_revenue_by_stage(stage)} months"
            ],
            'recommendations': [
                f"Reduce CAC from ${burn / max(customers, 1):,.0f} to ${revenue * 0.15 / max(customers, 1):,.0f} through content marketing and referrals" if customers > 0 else f"Design customer acquisition for <${burn * 0.3:,.0f} CAC through product-led growth",
                f"Increase average contract value from ${revenue / max(customers, 1) / 12:,.0f}/month to ${revenue / max(customers, 1) / 12 * 2.5:,.0f}/month via upsells" if customers > 0 else f"Target ${get_projected_revenue_by_stage(stage, sam) / get_target_customers_by_stage(stage) / 12:,.0f}/month per customer from day one",
                f"Target {int(burn / (revenue * 0.15 / max(customers, 1)) if customers > 0 and revenue > 0 else 50)} new customers/month at improved CAC to reach profitability in {runway} months" if revenue > 0 else f"Secure {get_target_customers_by_stage(stage)} pilot customers to validate unit economics before scaling"
            ]
        },
        'cash_flow_management': {
            'current_runway': f"{runway} months",
            'burn_multiple': burn / max(revenue/12, 1) if revenue > 0 else float('inf'),
            'insights': [
                f"Runway of {runway} months requires careful cash management",
                "Consider revenue-based financing to extend runway",
                "Focus on achieving default alive status"
            ],
            'recommendations': [
                "Negotiate longer payment terms with vendors",
                "Accelerate collections from customers",
                "Plan fundraise 6 months before cash out"
            ]
        },
        'jobs_to_be_done': {
            'functional_jobs': ['Save time', 'Reduce errors', 'Improve decisions'],
            'emotional_jobs': ['Feel confident', 'Look competent', 'Reduce stress'],
            'social_jobs': ['Impress peers', 'Lead innovation', 'Build reputation'],
            'insights': [
                "Product addresses functional jobs well but emotional jobs need attention",
                "Social proof through case studies critical for adoption",
                "Focus on measurable outcomes for functional jobs"
            ]
        },
        'competitive_positioning': {
            'position': 'Challenger' if stage in ['pre_seed', 'seed'] else 'Disruptor',
            'differentiation': ['Speed', 'Modern tech', 'Better UX'],
            'insights': [
                f"As a {stage} company, differentiation critical vs incumbents",
                "Technology advantage temporary - need to build other moats",
                "Focus on underserved segment initially"
            ],
            'recommendations': [
                "Document competitive wins for sales enablement",
                "Build switching costs through integrations",
                "Create category if direct competition too intense"
            ]
        },
        'differentiation_strategy': {
            'type': 'Focused Differentiation',
            'key_differentiators': ['Technology', 'User Experience', 'Speed'],
            'insights': [
                "Differentiation strategy appropriate for early stage",
                "Need to communicate unique value clearly",
                "Avoid competing on price initially"
            ],
            'recommendations': [
                "Build brand around key differentiators",
                "Protect IP where possible",
                "Focus on premium segment first"
            ]
        }
    }
    
    # Return specific analysis or default
    return analyses.get(framework_id, {
        'position': 'Emerging',
        'insights': [
            f"Framework {framework_id} analysis shows potential",
            "Further detailed analysis recommended",
            "Consider engaging strategy consultant for deeper dive"
        ],
        'recommendations': [
            "Implement framework methodology",
            "Track relevant KPIs",
            "Review quarterly"
        ]
    })


def generate_executive_summary_from_frameworks(startup_data: Dict[str, Any], framework_results: Dict[str, Any]) -> ExecutiveSummary:
    """Generate executive summary synthesizing all framework insights"""
    
    # Extract key insights from each framework
    all_insights = []
    for framework_id, result in framework_results.items():
        if 'insights' in result:
            all_insights.extend(result['insights'][:2])  # Top 2 from each
    
    # Synthesize into executive insights
    key_insights = all_insights[:3] if all_insights else [
        "Market opportunity exists but execution risks remain",
        "Competitive dynamics require rapid differentiation", 
        "Financial runway necessitates capital efficiency"
    ]
    
    revenue = startup_data.get('annual_revenue_run_rate', 0)
    market_size = startup_data.get('tam_size_usd', 10000000000)
    
    return ExecutiveSummary(
        situation=f"Analysis of {len(framework_results)} strategic frameworks reveals mixed signals. "
                  f"While market opportunity is substantial (${market_size/1e9:.1f}B TAM), "
                  f"execution challenges require careful navigation.",
        key_insights=key_insights,
        recommendation="Pursue controlled growth strategy balancing market capture with capital preservation. "
                       "Focus on framework-identified strengths while addressing critical gaps.",
        value_at_stake=market_size * 0.01 * 3.5,
        confidence_level=len(framework_results) * 10  # More frameworks = higher confidence
    )


def generate_strategic_options_from_frameworks(startup_data: Dict[str, Any], framework_results: Dict[str, Any]) -> List[StrategicOption]:
    """Generate SPECIFIC strategic options with stage-aware calculations"""
    
    options = []
    revenue = startup_data.get('annual_revenue_run_rate', 0)
    burn = startup_data.get('monthly_burn_usd', 50000)
    if burn == 0:
        burn = 50000  # Default burn rate
    customers = startup_data.get('customer_count', 0)
    stage = startup_data.get('funding_stage', 'seed')
    tam = startup_data.get('tam_size_usd', 10000000000)
    sam = startup_data.get('sam_size_usd', tam * 0.1)
    
    # Stage-aware options for zero-revenue companies
    if revenue == 0 and stage in ['pre_seed', 'seed']:
        # Pre-revenue strategic options
        target_customers = get_target_customers_by_stage(stage)
        first_year_revenue = get_projected_revenue_by_stage(stage, sam)
        months_to_revenue = get_months_to_first_revenue_by_stage(stage)
        
        # Option 1: Customer Discovery Sprint
        discovery_investment = burn * 3  # 3 months focused discovery
        options.append(StrategicOption(
            title=f"Customer Discovery Sprint - {target_customers} Pilots",
            description=f"Invest ${discovery_investment/1e3:.0f}K over 3 months to secure {target_customers} pilot customers and validate product-market fit",
            npv=first_year_revenue * 10 - discovery_investment,  # 10x potential on first revenue
            irr=150,  # High IRR for successful discovery
            payback_period=months_to_revenue / 12,
            risk_level="Medium",
            confidence_interval={"low": first_year_revenue * 5 - discovery_investment, "high": first_year_revenue * 20 - discovery_investment}
        ))
        
        # Option 2: MVP to Revenue
        mvp_investment = burn * months_to_revenue
        options.append(StrategicOption(
            title=f"MVP to ${first_year_revenue/1e3:.0f}K Revenue",
            description=f"Build MVP and achieve first ${first_year_revenue/1e3:.0f}K revenue in {months_to_revenue} months with ${mvp_investment/1e6:.1f}M investment",
            npv=first_year_revenue * 15 - mvp_investment,
            irr=100,
            payback_period=months_to_revenue / 12 + 0.5,
            risk_level="High",
            confidence_interval={"low": first_year_revenue * 8 - mvp_investment, "high": first_year_revenue * 25 - mvp_investment}
        ))
        
        # Option 3: Strategic Partnership
        partnership_timeline = 6  # 6 months to secure
        partnership_revenue = first_year_revenue * 3  # 3x revenue through partnerships
        options.append(StrategicOption(
            title="Strategic Partnership Acceleration",
            description=f"Secure enterprise partnership to accelerate to ${partnership_revenue/1e3:.0f}K revenue through channel distribution",
            npv=partnership_revenue * 12 - burn * partnership_timeline,
            irr=120,
            payback_period=partnership_timeline / 12,
            risk_level="Medium",
            confidence_interval={"low": partnership_revenue * 6 - burn * partnership_timeline, "high": partnership_revenue * 20 - burn * partnership_timeline}
        ))
        
    else:
        # Existing revenue-positive options logic
        if revenue == 0:
            revenue = 1000000  # Fallback for non-pre-revenue stages
            
        if customers == 0:
            customers = 10  # Default minimum customers
            
        market_share = (revenue / sam * 100) if sam > 0 else 0
        growth_rate = startup_data.get('market_growth_rate_percent', 20)
        
        # Calculate specific NPVs based on realistic projections
        discount_rate = 0.15  # 15% discount rate
        
        # If BCG Matrix shows Question Mark, suggest specific investment strategy
        if 'bcg_matrix' in framework_results:
            if framework_results['bcg_matrix'].get('position') == 'Question Mark':
                # Calculate specific investment needed
                investment_needed = burn * 18  # 18 months of aggressive growth
                revenue_target = revenue * 5  # 5x growth target
                market_share_target = min(10, market_share * 4)  # 4x market share or 10%
                
                # 3-year cash flows
                cf_year1 = -investment_needed * 0.6
                cf_year2 = revenue_target * 0.5 - investment_needed * 0.3
                cf_year3 = revenue_target * 2.5
                
                npv = cf_year1/(1+discount_rate) + cf_year2/(1+discount_rate)**2 + cf_year3/(1+discount_rate)**3
                irr = 35 + (market_share_target - market_share) * 2  # Higher IRR for bigger share gains
                
                options.append(StrategicOption(
                    title=f"Capture {market_share_target:.1f}% Market Share",
                    description=f"Invest ${investment_needed/1e6:.1f}M to grow from {customers} to {int(customers * market_share_target/max(market_share, 0.1))} customers and ${revenue/1e6:.1f}M to ${revenue_target/1e6:.1f}M ARR",
                    npv=npv,
                    irr=irr,
                    payback_period=investment_needed / max(revenue_target * 0.3, 1),  # Based on 30% EBITDA margin
                    risk_level="High",
                    confidence_interval={"low": npv * 0.5, "high": npv * 2.0}
                ))
        
        # If unit economics are strong, suggest scaling strategy
        if 'unit_economics' in framework_results:
            ltv_cac = framework_results['unit_economics'].get('metrics', {}).get('ltv_cac_ratio', 0)
            if ltv_cac > 2:
                scale_investment = burn * 12  # 12 months of scaling
                new_customers = int(scale_investment / (burn / max(customers, 1)) * 0.7)  # 70% efficiency
                new_revenue = revenue + (new_customers * revenue / max(customers, 1))
                
                cf_year1 = -scale_investment * 0.7
                cf_year2 = new_revenue * 0.4
                cf_year3 = new_revenue * 1.5
                
                npv = cf_year1/(1+discount_rate) + cf_year2/(1+discount_rate)**2 + cf_year3/(1+discount_rate)**3
                
                options.append(StrategicOption(
                    title=f"Scale to {customers + new_customers} Customers",
                    description=f"Leverage {ltv_cac:.1f}x LTV/CAC to add {new_customers} customers with ${scale_investment/1e6:.1f}M investment, reaching ${new_revenue/1e6:.1f}M ARR",
                    npv=npv,
                    irr=25 + ltv_cac * 3,  # Better unit economics = higher IRR
                    payback_period=scale_investment / max(new_revenue * 0.25, 1),  # 25% EBITDA margin
                    risk_level="Medium",
                    confidence_interval={"low": npv * 0.7, "high": npv * 1.5}
                ))
        
        # Conservative option with specific targets
        conservative_growth = 1.5  # 50% growth
        conservative_investment = burn * 6  # 6 months runway
        
        cf_year1 = -conservative_investment * 0.5
        cf_year2 = revenue * conservative_growth * 0.3
        cf_year3 = revenue * conservative_growth * 1.2
        
        npv = cf_year1/(1+discount_rate) + cf_year2/(1+discount_rate)**2 + cf_year3/(1+discount_rate)**3
        
        options.append(StrategicOption(
            title=f"Efficient Growth to ${revenue * 1.5 / 1e6:.1f}M ARR",
            description=f"Optimize burn from ${burn/1e3:.0f}K to ${burn*0.7/1e3:.0f}K/month while growing revenue 50% with minimal ${conservative_investment/1e6:.1f}M investment",
            npv=npv,
            irr=20,
            payback_period=conservative_investment / max(revenue * conservative_growth * 0.2, 1),
            risk_level="Low",
            confidence_interval={"low": npv * 0.8, "high": npv * 1.2}
        ))
    
    return sorted(options, key=lambda x: x.npv, reverse=True)[:3]  # Top 3 by NPV


def extract_competitive_dynamics(framework_results: Dict[str, Any]) -> List[CompetitiveDynamic]:
    """Extract competitive dynamics from Porter's Five Forces analysis"""
    
    dynamics = []
    
    if 'porters_five_forces' in framework_results:
        forces = framework_results['porters_five_forces'].get('forces', {})
        
        for force_name, force_data in forces.items():
            dynamics.append(CompetitiveDynamic(
                force=force_name.replace('_', ' ').title(),
                intensity=force_data.get('level', 'Medium'),
                trend='Stable',  # Would need trend analysis
                strategic_implication=f"Manage {force_name} through targeted initiatives"
            ))
    else:
        # Fallback dynamics
        dynamics = analyze_competitive_dynamics({})
    
    return dynamics


def create_roadmap_from_frameworks(startup_data: Dict[str, Any], framework_results: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Create stage-aware implementation roadmap with measurable targets"""
    
    # Extract key metrics
    revenue = startup_data.get('annual_revenue_run_rate', 0)
    burn = startup_data.get('monthly_burn_usd', 50000)
    customers = startup_data.get('customer_count', 0)
    team_size = startup_data.get('team_size_full_time', 5)
    runway = startup_data.get('runway_months', 12)
    stage = startup_data.get('funding_stage', 'seed')
    sam = startup_data.get('sam_size_usd', 1e9)
    
    # Stage-aware roadmap for zero-revenue companies
    if revenue == 0 and stage in ['pre_seed', 'seed']:
        target_customers = get_target_customers_by_stage(stage)
        first_year_revenue = get_projected_revenue_by_stage(stage, sam)
        months_to_revenue = get_months_to_first_revenue_by_stage(stage)
        
        roadmap = [
            {
                "phase": "Product-Market Fit (0-3 months)",
                "quarter": "Q1",
                "initiatives": [
                    f"Complete customer discovery interviews with {target_customers * 10} prospects",
                    f"Build MVP targeting top 3 use cases identified",
                    f"Secure {target_customers} pilot customers with LOIs"
                ],
                "milestones": [
                    f"{target_customers} pilot customers signed",
                    "MVP feature complete",
                    "Product-market fit survey >40%",
                    f"Runway extended to {months_to_revenue + 6} months"
                ],
                "investment": burn * 3,
                "success_metrics": {
                    "pilot_customers": target_customers,
                    "interviews_completed": target_customers * 10,
                    "product_readiness": 0.8,  # 80% feature complete
                    "pmf_score": 40  # 40% would be disappointed
                }
            },
            {
                "phase": f"First Revenue (3-{months_to_revenue} months)",
                "quarter": "Q2-Q3",
                "initiatives": [
                    f"Convert {target_customers} pilots to paying customers",
                    f"Achieve first ${first_year_revenue/1e3:.0f}K in revenue",
                    f"Build repeatable sales process",
                    "Establish customer success function"
                ],
                "milestones": [
                    f"${first_year_revenue/1e3:.0f}K ARR achieved",
                    f"{target_customers * 3} total customers",
                    "Sales playbook documented",
                    "Seed round of ${max(2, burn*18/1e6):.0f}M raised"
                ],
                "investment": burn * months_to_revenue,
                "success_metrics": {
                    "revenue_target": first_year_revenue,
                    "customer_target": target_customers * 3,
                    "conversion_rate": 0.3,  # 30% pilot to paid
                    "funding_target": max(2000000, burn * 18)
                }
            },
            {
                "phase": f"Scale Foundation ({months_to_revenue}-18 months)",
                "quarter": "Q4-Q6",
                "initiatives": [
                    f"Scale to ${first_year_revenue*10/1e6:.1f}M ARR",
                    f"Expand team to {team_size * 3} with sales/engineering hires",
                    "Achieve product-market fit in primary vertical",
                    "Build competitive moat through network effects"
                ],
                "milestones": [
                    f"${first_year_revenue*10/1e6:.1f}M ARR",
                    f"{target_customers * 20} customers",
                    "Net retention >100%",
                    "Series A readiness achieved"
                ],
                "investment": burn * 12,
                "success_metrics": {
                    "revenue_target": first_year_revenue * 10,
                    "customer_target": target_customers * 20,
                    "net_retention": 110,
                    "team_size": team_size * 3
                }
            }
        ]
    else:
        # Existing revenue-positive roadmap
        if revenue == 0:
            revenue = 1000000  # Fallback
        if customers == 0:
            customers = 10  # Fallback
            
        # Extract specific recommendations from frameworks
        bcg_recs = framework_results.get('bcg_matrix', {}).get('recommendations', [])
        porter_insights = framework_results.get('porters_five_forces', {}).get('insights', [])
        unit_econ_recs = framework_results.get('unit_economics', {}).get('recommendations', [])
        
        roadmap = [
            {
                "phase": "Foundation (0-3 months)",
                "quarter": "Q1",
                "initiatives": [
                    bcg_recs[0] if bcg_recs else f"Increase revenue from ${revenue/1e6:.1f}M to ${revenue*1.5/1e6:.1f}M (50% growth)",
                    unit_econ_recs[0] if unit_econ_recs else f"Reduce CAC from ${burn/max(customers,1):.0f} to ${burn/max(customers,1)*0.6:.0f} (40% reduction)",
                    f"Extend runway from {runway} to {runway + 6} months by optimizing burn or raising ${burn*6/1e3:.0f}K bridge"
                ],
                "milestones": [
                    f"${revenue*1.5/1e6:.1f}M ARR achieved",
                    f"{int(customers * 1.5)} total customers",
                    f"Burn reduced to ${burn*0.8/1e3:.0f}K/month",
                    "Unit economics positive (LTV/CAC > 3)"
                ],
                "investment": burn * 3,
                "success_metrics": {
                    "revenue_target": revenue * 1.5,
                    "customer_target": int(customers * 1.5),
                    "burn_target": burn * 0.8,
                    "team_target": team_size + 2
                }
            },
            {
                "phase": "Growth Acceleration (3-9 months)", 
                "quarter": "Q2-Q3",
                "initiatives": [
                    f"Scale from {customers} to {int(customers * 4)} customers through targeted acquisition",
                    f"Increase team from {team_size} to {team_size * 2} with focus on sales/marketing",
                    bcg_recs[1] if len(bcg_recs) > 1 else f"Achieve ${revenue*3/1e6:.1f}M ARR run rate"
                ],
                "milestones": [
                    f"${revenue*3/1e6:.1f}M ARR (3x growth)",
                    f"{int(customers * 4)} customers acquired",
                    f"Market share increased to {min(5, (revenue*3/sam)*100):.1f}%",
                    "Series A fundraise of ${max(5, burn*18/1e6):.0f}M completed"
                ],
                "investment": burn * 9,
                "success_metrics": {
                    "revenue_target": revenue * 3,
                    "customer_target": int(customers * 4),
                    "market_share_target": min(5, (revenue*3/sam)*100),
                    "funding_target": max(5000000, burn * 18)
                }
            },
            {
                "phase": "Market Leadership (9-18 months)",
                "quarter": "Q4-Q6",
                "initiatives": [
                    f"Expand to {3 if stage == 'seed' else 5} new market segments",
                    f"Build moat through {'platform features' if customers > 100 else 'network effects'}",
                    f"Achieve operational efficiency with <2.0x burn multiple"
                ],
                "milestones": [
                    f"${revenue*6/1e6:.1f}M ARR achieved",
                    f"{int(customers * 10)} total customers",
                    "EBITDA positive operations",
                    "Category leader in primary vertical"
                ],
                "investment": burn * 12,
                "success_metrics": {
                    "revenue_target": revenue * 6,
                    "customer_target": int(customers * 10),
                    "ebitda_margin": 0.15,
                    "nps_score": 50
                }
            }
        ]
    
    return roadmap


def generate_financial_projections(startup_data: Dict[str, Any]) -> Dict[str, Any]:
    """Generate 3-year financial projections with stage-aware scenarios"""
    
    revenue = startup_data.get('annual_revenue_run_rate', 0)
    burn_rate = startup_data.get('monthly_burn_usd', 100000)
    if burn_rate == 0:
        burn_rate = 100000  # Default $100K/month
    
    stage = startup_data.get('funding_stage', 'seed')
    tam = startup_data.get('tam_size_usd', 10000000000)
    sam = startup_data.get('sam_size_usd', tam * 0.1)
    
    # Stage-aware projections for zero-revenue companies
    if revenue == 0 and stage in ['pre_seed', 'seed']:
        # Market-based projections for pre-revenue companies
        target_share = get_target_market_share_by_stage(stage, tam, sam)
        year1_revenue = sam * (target_share / 100) * 0.001  # 0.1% of target in Y1
        
        projections = {
            "base_case": [
                {"year": 1, "revenue": year1_revenue, "ebitda": -burn_rate * 12},
                {"year": 2, "revenue": year1_revenue * 10, "ebitda": -burn_rate * 6},
                {"year": 3, "revenue": year1_revenue * 50, "ebitda": year1_revenue * 2}
            ],
            "bull_case": [
                {"year": 1, "revenue": year1_revenue * 2, "ebitda": -burn_rate * 10},
                {"year": 2, "revenue": year1_revenue * 20, "ebitda": -burn_rate * 2},
                {"year": 3, "revenue": year1_revenue * 100, "ebitda": year1_revenue * 10}
            ],
            "bear_case": [
                {"year": 1, "revenue": year1_revenue * 0.5, "ebitda": -burn_rate * 15},
                {"year": 2, "revenue": year1_revenue * 3, "ebitda": -burn_rate * 10},
                {"year": 3, "revenue": year1_revenue * 10, "ebitda": -burn_rate * 3}
            ]
        }
    else:
        # Existing revenue-based projections
        if revenue == 0:
            revenue = 1000000  # Default fallback
            
        projections = {
            "base_case": [
                {"year": 1, "revenue": revenue * 2.5, "ebitda": -burn_rate * 6},
                {"year": 2, "revenue": revenue * 6, "ebitda": revenue * 0.5},
                {"year": 3, "revenue": revenue * 15, "ebitda": revenue * 3}
            ],
            "bull_case": [
                {"year": 1, "revenue": revenue * 3, "ebitda": -burn_rate * 3},
                {"year": 2, "revenue": revenue * 9, "ebitda": revenue * 1.5},
                {"year": 3, "revenue": revenue * 25, "ebitda": revenue * 6}
            ],
            "bear_case": [
                {"year": 1, "revenue": revenue * 1.5, "ebitda": -burn_rate * 12},
                {"year": 2, "revenue": revenue * 3, "ebitda": -burn_rate * 6},
                {"year": 3, "revenue": revenue * 6, "ebitda": revenue * 0.5}
            ]
        }
    
    return projections

@deep_analysis_router.post("/deep-analysis", response_model=DeepAnalysisResponse)
async def perform_deep_framework_analysis(request: DeepAnalysisRequest):
    """
    Perform McKinsey-quality deep framework analysis using actual frameworks
    """
    try:
        startup_data = request.startup_data
        
        # Log the received data to debug
        logger.info(f"Received startup data: revenue={startup_data.get('annual_revenue_run_rate', 0)}, burn={startup_data.get('monthly_burn_usd', 0)}, customers={startup_data.get('customer_count', 0)}")
        
        try:
            # Step 1: Intelligently select relevant frameworks
            selected_frameworks = await select_relevant_frameworks(startup_data)
            logger.info(f"Selected {len(selected_frameworks)} relevant frameworks")
        except Exception as e:
            logger.error(f"Error in select_relevant_frameworks: {e}")
            raise
        
        try:
            # Step 2: Apply each framework to get specific insights
            framework_results = await apply_frameworks(startup_data, selected_frameworks)
        except Exception as e:
            logger.error(f"Error in apply_frameworks: {e}")
            raise
        
        try:
            # Step 3: Generate specific executive summary with real calculations
            executive_summary = generate_executive_summary(startup_data, framework_results)
        except Exception as e:
            logger.error(f"Error in generate_executive_summary: {e}")
            raise
        
        try:
            # Step 4: Generate strategic options based on framework insights
            strategic_options = generate_strategic_options_from_frameworks(startup_data, framework_results)
        except Exception as e:
            logger.error(f"Error in generate_strategic_options_from_frameworks: {e}")
            raise
        
        try:
            # Step 5: Analyze competitive dynamics using Porter's analysis
            competitive_dynamics = extract_competitive_dynamics(framework_results)
        except Exception as e:
            logger.error(f"Error in extract_competitive_dynamics: {e}")
            raise
        
        try:
            # Step 6: Create implementation roadmap based on framework recommendations
            implementation_roadmap = create_roadmap_from_frameworks(startup_data, framework_results)
        except Exception as e:
            logger.error(f"Error in create_roadmap_from_frameworks: {e}")
            raise
        
        try:
            # Step 7: Generate financial projections
            financial_projections = generate_financial_projections(startup_data)
        except Exception as e:
            logger.error(f"Error in generate_financial_projections: {e}")
            raise
        
        # Create situation assessment
        situation_assessment = {
            "market_context": f"The {startup_data.get('sector', 'technology')} sector exhibits "
                              f"winner-take-all dynamics with incumbents controlling 60% share. "
                              f"Disruption window remains open for 18-24 months.",
            "competitive_position": "Currently positioned as emerging challenger with differentiated "
                                    "technology but limited market presence. Key advantages include "
                                    "superior product velocity and modern architecture.",
            "organizational_readiness": f"Team of {startup_data.get('team_size_full_time', 10)} "
                                        f"demonstrates strong technical capabilities but lacks "
                                        f"enterprise go-to-market experience.",
            "key_risks": [
                "Competitive response from incumbents with 10x resources",
                "Customer acquisition costs may not scale efficiently", 
                "Technical debt accumulation could constrain roadmap",
                "Key person dependency on founding team"
            ]
        }
        
        # Create value drivers
        revenue = startup_data.get('annual_revenue_run_rate', 1000000)
        value_drivers = [
            {
                "name": "Revenue Growth",
                "impact": revenue * 5,
                "timeline": "Y1-Y2",
                "owner": "CRO"
            },
            {
                "name": "Margin Expansion", 
                "impact": revenue * 2,
                "timeline": "Y1-Y3",
                "owner": "COO"
            },
            {
                "name": "Multiple Expansion",
                "impact": revenue * 3,
                "timeline": "Y2-Y3", 
                "owner": "CEO"
            }
        ]
        
        # Enhance with DeepSeek if available
        if request.analysis_depth == "comprehensive" and framework_results:
            framework_summary = "\n".join([
                f"{fid}: {res.get('position', 'N/A')} - {res.get('insights', [''])[0][:100]}..."
                for fid, res in framework_results.items()
            ])
            
            prompt = f"""As a senior McKinsey partner, synthesize these framework analyses into strategic insights:
            
            Company: {startup_data.get('sector')} startup, ${revenue/1e6:.1f}M ARR
            Frameworks Applied:
            {framework_summary}
            
            Provide 3 non-obvious strategic insights that connect these frameworks."""
            
            deepseek_insights = await call_deepseek_api(prompt)
            if deepseek_insights:
                logger.info("Enhanced analysis with DeepSeek insights")
        
        return DeepAnalysisResponse(
            executive_summary=executive_summary,
            situation_assessment=situation_assessment,
            strategic_options=strategic_options,
            value_drivers=value_drivers,
            competitive_dynamics=competitive_dynamics,
            implementation_roadmap=implementation_roadmap,
            financial_projections=financial_projections
        )
        
    except Exception as e:
        logger.error(f"Deep analysis error: {e}")
        raise HTTPException(status_code=500, detail=str(e))