#!/usr/bin/env python3
"""
Enhanced Framework Analysis API Endpoints with Intelligent LLM-based Selection
"""

import os
import sys
import logging
import json
import asyncio
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, Field
import aiohttp
from tenacity import retry, stop_after_attempt, wait_exponential

# Setup logging
logger = logging.getLogger(__name__)

# Add framework_intelligence to path
current_dir = os.path.dirname(os.path.abspath(__file__))

try:
    from framework_intelligence.framework_selector import FrameworkSelector, StartupContext, BusinessStage, IndustryType, ChallengeType
    from framework_intelligence.framework_database import FRAMEWORKS as FRAMEWORK_DATABASE, ComplexityLevel, FrameworkCategory
    from llm_analysis import LLMAnalysisEngine, get_fallback_recommendations
    from api_llm_helpers import get_engine
except ImportError as e:
    logger.error(f"Failed to import required modules: {e}")
    raise

# Create router
framework_analysis_router = APIRouter(prefix="/api/frameworks", tags=["Framework Analysis"])

# Initialize components
framework_selector = FrameworkSelector()
llm_engine = None

def get_llm_engine():
    """Get or create LLM engine instance"""
    global llm_engine
    if llm_engine is None:
        llm_engine = LLMAnalysisEngine()
    return llm_engine

# Request/Response Models
class StartupAnalysisRequest(BaseModel):
    """Enhanced startup data for intelligent framework selection"""
    # Company basics
    company_name: Optional[str] = Field(None, description="Company name")
    company_stage: str = Field(..., description="Current stage (pre-seed, seed, series-a, etc.)")
    funding_stage: str = Field(..., description="Funding stage")
    industry: str = Field(..., description="Industry or sector")
    sector: Optional[str] = Field(None, description="Specific sector")
    
    # Team and resources
    team_size_full_time: int = Field(..., ge=0, description="Full-time team size")
    technical_team_percent: Optional[float] = Field(0, description="Percentage of technical team")
    founders_experience_years: Optional[int] = Field(0, description="Founders' experience in years")
    
    # Financial metrics
    annual_revenue_run_rate: Optional[float] = Field(0, description="Annual revenue run rate")
    revenue_growth_rate_percent: Optional[float] = Field(0, description="Revenue growth rate %")
    monthly_burn_usd: Optional[float] = Field(0, description="Monthly burn rate in USD")
    runway_months: Optional[float] = Field(0, description="Runway in months")
    burn_multiple: Optional[float] = Field(0, description="Burn multiple")
    
    # Business metrics
    customer_count: Optional[int] = Field(0, description="Number of customers")
    customer_acquisition_cost_usd: Optional[float] = Field(0, description="CAC in USD")
    customer_lifetime_value_usd: Optional[float] = Field(0, description="LTV in USD")
    net_dollar_retention_percent: Optional[float] = Field(0, description="NDR %")
    
    # Challenges and goals
    primary_challenges: List[str] = Field(default_factory=list, description="Main challenges")
    goals: List[str] = Field(default_factory=list, description="Business goals")
    pain_points: List[str] = Field(default_factory=list, description="Specific pain points")
    
    # Additional context
    business_model: Optional[str] = Field(None, description="Business model (B2B, B2C, etc.)")
    target_market: Optional[str] = Field(None, description="Target market")
    competitive_landscape: Optional[str] = Field(None, description="Competitive landscape description")
    unique_value_proposition: Optional[str] = Field(None, description="UVP")


class IntelligentFrameworkRecommendation(BaseModel):
    """Framework recommendation with intelligent insights"""
    framework_id: str
    framework_name: str
    category: str
    relevance_score: float = Field(..., ge=0, le=1)
    why_selected: str
    expected_impact: str
    implementation_priority: int
    time_to_value: str
    specific_benefits: List[str]
    implementation_tips: List[str]
    success_metrics: List[str]
    risk_factors: List[str]
    
    
class FrameworkAnalysisResponse(BaseModel):
    """Complete framework analysis response"""
    recommendations: List[IntelligentFrameworkRecommendation]
    situation_analysis: str
    strategic_priorities: List[str]
    implementation_roadmap: Dict[str, Any]
    success_factors: List[str]
    total_frameworks_analyzed: int
    selection_rationale: str
    

async def analyze_startup_situation_with_llm(startup_data: StartupAnalysisRequest) -> Dict[str, Any]:
    """Use LLM to analyze startup situation and identify key needs"""
    engine = get_llm_engine()
    
    # Create a comprehensive prompt for situation analysis
    prompt = f"""Analyze this startup's situation and identify the most relevant business frameworks from our database of 554 frameworks.

Company Profile:
- Stage: {startup_data.company_stage} ({startup_data.funding_stage})
- Industry: {startup_data.industry} {f'({startup_data.sector})' if startup_data.sector else ''}
- Team Size: {startup_data.team_size_full_time} (Technical: {startup_data.technical_team_percent}%)
- Business Model: {startup_data.business_model or 'Not specified'}

Financial Health:
- Annual Revenue: ${startup_data.annual_revenue_run_rate:,.0f}
- Growth Rate: {startup_data.revenue_growth_rate_percent}%
- Monthly Burn: ${startup_data.monthly_burn_usd:,.0f}
- Runway: {startup_data.runway_months} months
- Burn Multiple: {startup_data.burn_multiple}x

Business Metrics:
- Customers: {startup_data.customer_count}
- CAC: ${startup_data.customer_acquisition_cost_usd:,.0f}
- LTV: ${startup_data.customer_lifetime_value_usd:,.0f}
- NDR: {startup_data.net_dollar_retention_percent}%

Challenges: {', '.join(startup_data.primary_challenges) if startup_data.primary_challenges else 'Not specified'}
Goals: {', '.join(startup_data.goals) if startup_data.goals else 'Not specified'}
Pain Points: {', '.join(startup_data.pain_points) if startup_data.pain_points else 'Not specified'}

Based on this analysis, identify:
1. The startup's most critical needs (prioritize top 3-5)
2. Framework categories that would be most beneficial
3. Specific framework characteristics needed (complexity level, implementation time, etc.)
4. Strategic priorities for the next 6-12 months

Provide structured JSON output with:
- critical_needs: List of top needs
- recommended_categories: List of framework categories (Strategy, Growth, Product, etc.)
- complexity_preference: Basic/Intermediate/Advanced
- implementation_timeline: Immediate/Short-term/Long-term
- strategic_priorities: List of priorities
"""

    try:
        # Call LLM for analysis
        if engine.fallback_mode:
            # Use fallback analysis
            return await fallback_situation_analysis(startup_data)
        
        messages = [
            {"role": "system", "content": "You are an expert startup advisor with deep knowledge of business frameworks and methodologies."},
            {"role": "user", "content": prompt}
        ]
        
        response = await engine._call_deepseek(messages)
        
        # Parse JSON from response
        json_match = re.search(r'\{.*\}', response, re.DOTALL)
        if json_match:
            return json.loads(json_match.group())
        else:
            # Try to extract structured data from text
            return parse_text_response(response)
            
    except Exception as e:
        logger.error(f"LLM analysis failed: {e}")
        return await fallback_situation_analysis(startup_data)


async def fallback_situation_analysis(startup_data: StartupAnalysisRequest) -> Dict[str, Any]:
    """Fallback analysis when LLM is not available"""
    # Determine critical needs based on data
    critical_needs = []
    recommended_categories = []
    
    # Analyze based on stage
    if startup_data.company_stage in ["pre-seed", "seed"]:
        critical_needs.extend(["Product-market fit", "Customer validation", "MVP development"])
        recommended_categories.extend(["Product", "Innovation", "Customer"])
    elif startup_data.company_stage in ["series-a", "series-b"]:
        critical_needs.extend(["Scaling operations", "Growth optimization", "Team building"])
        recommended_categories.extend(["Growth", "Operations", "Leadership"])
    else:
        critical_needs.extend(["Market expansion", "Operational efficiency", "Innovation"])
        recommended_categories.extend(["Strategy", "Operations", "Innovation"])
    
    # Analyze based on metrics
    if startup_data.runway_months and startup_data.runway_months < 12:
        critical_needs.append("Fundraising and capital efficiency")
        recommended_categories.append("Financial")
    
    if startup_data.revenue_growth_rate_percent and startup_data.revenue_growth_rate_percent < 100:
        critical_needs.append("Revenue growth acceleration")
        recommended_categories.append("Growth")
    
    if startup_data.customer_acquisition_cost_usd and startup_data.customer_lifetime_value_usd:
        ltv_cac_ratio = startup_data.customer_lifetime_value_usd / startup_data.customer_acquisition_cost_usd
        if ltv_cac_ratio < 3:
            critical_needs.append("Unit economics optimization")
            recommended_categories.append("Financial")
    
    # Add from explicit challenges
    if startup_data.primary_challenges:
        critical_needs.extend(startup_data.primary_challenges[:2])
    
    # Determine complexity based on team size and stage
    complexity = "Basic" if startup_data.team_size_full_time < 10 else "Intermediate"
    if startup_data.team_size_full_time > 50 or startup_data.company_stage in ["series-b", "series-c"]:
        complexity = "Advanced"
    
    return {
        "critical_needs": critical_needs[:5],
        "recommended_categories": list(set(recommended_categories))[:4],
        "complexity_preference": complexity,
        "implementation_timeline": "Short-term" if startup_data.runway_months < 12 else "Medium-term",
        "strategic_priorities": [
            f"Address {critical_needs[0]}" if critical_needs else "Establish foundation",
            "Build sustainable growth engine",
            "Strengthen competitive position"
        ]
    }


def parse_text_response(response: str) -> Dict[str, Any]:
    """Parse structured data from text response"""
    # Simple parsing logic - can be enhanced
    result = {
        "critical_needs": [],
        "recommended_categories": [],
        "complexity_preference": "Intermediate",
        "implementation_timeline": "Short-term",
        "strategic_priorities": []
    }
    
    lines = response.split('\n')
    current_section = None
    
    for line in lines:
        line = line.strip()
        if 'critical needs' in line.lower() or 'needs:' in line.lower():
            current_section = 'needs'
        elif 'categories' in line.lower():
            current_section = 'categories'
        elif 'priorities' in line.lower():
            current_section = 'priorities'
        elif line.startswith('-') or line.startswith('•'):
            item = line.lstrip('-•').strip()
            if current_section == 'needs' and len(result['critical_needs']) < 5:
                result['critical_needs'].append(item)
            elif current_section == 'categories' and len(result['recommended_categories']) < 4:
                result['recommended_categories'].append(item)
            elif current_section == 'priorities' and len(result['strategic_priorities']) < 5:
                result['strategic_priorities'].append(item)
    
    return result


async def select_frameworks_intelligently(
    startup_data: StartupAnalysisRequest,
    situation_analysis: Dict[str, Any]
) -> List[Tuple[str, float, str]]:
    """Select frameworks based on situation analysis"""
    
    selected_frameworks = []
    
    # Map situation to framework selection
    critical_needs = situation_analysis.get("critical_needs", [])
    recommended_categories = situation_analysis.get("recommended_categories", [])
    complexity_pref = situation_analysis.get("complexity_preference", "Intermediate")
    
    # Convert text complexity to enum
    complexity_map = {
        "Basic": ComplexityLevel.BASIC,
        "Intermediate": ComplexityLevel.INTERMEDIATE,
        "Advanced": ComplexityLevel.ADVANCED,
        "Expert": ComplexityLevel.EXPERT
    }
    target_complexity = complexity_map.get(complexity_pref, ComplexityLevel.INTERMEDIATE)
    
    # Score each framework based on relevance
    framework_scores = {}
    
    for framework_id, framework in FRAMEWORK_DATABASE.items():
        score = 0.0
        reasons = []
        
        # Category match
        if hasattr(framework.category, 'value'):
            category_name = framework.category.value
        else:
            category_name = str(framework.category)
            
        if category_name in recommended_categories:
            score += 0.3
            reasons.append(f"Matches recommended category: {category_name}")
        
        # Complexity match
        if framework.complexity == target_complexity:
            score += 0.2
            reasons.append(f"Appropriate complexity level")
        elif abs(framework.complexity.value - target_complexity.value) == 1:
            score += 0.1
            reasons.append(f"Close to target complexity")
        
        # Need matching (check descriptions and use cases)
        framework_text = f"{framework.description} {' '.join(framework.when_to_use)}".lower()
        for need in critical_needs:
            need_keywords = need.lower().split()
            matches = sum(1 for keyword in need_keywords if keyword in framework_text)
            if matches >= len(need_keywords) * 0.5:  # At least 50% keyword match
                score += 0.3 / len(critical_needs)
                reasons.append(f"Addresses: {need}")
        
        # Industry relevance
        if hasattr(framework, 'industry_relevance') and startup_data.industry:
            if any(ind.lower() in startup_data.industry.lower() or 
                   startup_data.industry.lower() in ind.lower() 
                   for ind in framework.industry_relevance):
                score += 0.1
                reasons.append(f"Industry relevant")
        
        # Stage relevance
        stage_keywords = {
            "pre-seed": ["idea", "validation", "mvp"],
            "seed": ["product-market fit", "early", "customer"],
            "series-a": ["growth", "scaling", "expansion"],
            "series-b": ["scale", "optimization", "efficiency"],
            "series-c": ["mature", "transformation", "innovation"]
        }
        
        if startup_data.company_stage in stage_keywords:
            keywords = stage_keywords[startup_data.company_stage]
            if any(kw in framework_text for kw in keywords):
                score += 0.1
                reasons.append(f"Stage appropriate")
        
        if score > 0.3:  # Minimum threshold
            framework_scores[framework_id] = (score, " | ".join(reasons))
    
    # Sort by score and select top frameworks
    sorted_frameworks = sorted(
        framework_scores.items(), 
        key=lambda x: x[1][0], 
        reverse=True
    )
    
    # Select top 10-15 frameworks, ensuring diversity
    selected_categories = set()
    for framework_id, (score, reason) in sorted_frameworks:
        framework = FRAMEWORK_DATABASE[framework_id]
        category = framework.category.value if hasattr(framework.category, 'value') else str(framework.category)
        
        # Ensure category diversity
        category_count = sum(1 for _, _, _ in selected_frameworks if _[2] == category)
        if category_count < 3:  # Max 3 per category
            selected_frameworks.append((framework_id, score, reason))
            selected_categories.add(category)
        
        if len(selected_frameworks) >= 15:
            break
    
    # Ensure we have at least 8 frameworks
    if len(selected_frameworks) < 8:
        # Add more from priority categories
        for framework_id, framework in FRAMEWORK_DATABASE.items():
            if framework_id not in [f[0] for f in selected_frameworks]:
                category = framework.category.value if hasattr(framework.category, 'value') else str(framework.category)
                if category in recommended_categories:
                    score = 0.5  # Default relevance
                    reason = f"Additional {category} framework"
                    selected_frameworks.append((framework_id, score, reason))
                    if len(selected_frameworks) >= 10:
                        break
    
    return selected_frameworks[:12]  # Return top 12


def create_framework_recommendation(
    framework_id: str,
    framework,
    score: float,
    reason: str,
    priority: int,
    startup_data: StartupAnalysisRequest
) -> IntelligentFrameworkRecommendation:
    """Create detailed framework recommendation"""
    
    # Determine expected impact based on score and startup needs
    if score > 0.8:
        expected_impact = "High - Critical for addressing your primary challenges"
    elif score > 0.6:
        expected_impact = "Medium-High - Significant benefits expected"
    elif score > 0.4:
        expected_impact = "Medium - Valuable supporting framework"
    else:
        expected_impact = "Low-Medium - Complementary benefits"
    
    # Time to value based on complexity
    time_to_value_map = {
        ComplexityLevel.BASIC: "2-4 weeks",
        ComplexityLevel.INTERMEDIATE: "1-3 months",
        ComplexityLevel.ADVANCED: "3-6 months",
        ComplexityLevel.EXPERT: "6-12 months"
    }
    time_to_value = time_to_value_map.get(framework.complexity, "2-3 months")
    
    # Specific benefits based on startup situation
    specific_benefits = []
    if startup_data.runway_months and startup_data.runway_months < 12:
        if "financial" in framework.name.lower() or "efficiency" in reason.lower():
            specific_benefits.append("Extend runway through improved capital efficiency")
    
    if startup_data.revenue_growth_rate_percent and startup_data.revenue_growth_rate_percent < 100:
        if "growth" in framework.name.lower() or "customer" in reason.lower():
            specific_benefits.append("Accelerate revenue growth through systematic approach")
    
    # Add framework's expected outcomes
    specific_benefits.extend(framework.expected_outcomes[:2])
    
    # Risk factors
    risk_factors = []
    if framework.complexity.value >= ComplexityLevel.ADVANCED.value:
        risk_factors.append("Requires significant time and expertise to implement effectively")
    if startup_data.team_size_full_time < 10 and framework.complexity.value > ComplexityLevel.BASIC.value:
        risk_factors.append("May strain limited team resources")
    if framework.common_pitfalls:
        risk_factors.append(framework.common_pitfalls[0])
    
    return IntelligentFrameworkRecommendation(
        framework_id=framework_id,
        framework_name=framework.name,
        category=framework.category.value if hasattr(framework.category, 'value') else str(framework.category),
        relevance_score=round(score, 2),
        why_selected=reason,
        expected_impact=expected_impact,
        implementation_priority=priority,
        time_to_value=time_to_value,
        specific_benefits=specific_benefits[:3],
        implementation_tips=framework.application_steps[:3] if hasattr(framework, 'application_steps') else [],
        success_metrics=framework.success_metrics[:3] if framework.success_metrics else [],
        risk_factors=risk_factors[:2] if risk_factors else ["Standard implementation risks apply"]
    )


def create_implementation_roadmap(
    recommendations: List[IntelligentFrameworkRecommendation],
    situation_analysis: Dict[str, Any]
) -> Dict[str, Any]:
    """Create phased implementation roadmap"""
    
    # Group by priority
    immediate = [r for r in recommendations if r.implementation_priority <= 3]
    short_term = [r for r in recommendations if 4 <= r.implementation_priority <= 7]
    long_term = [r for r in recommendations if r.implementation_priority > 7]
    
    roadmap = {
        "phase_1": {
            "name": "Foundation (0-3 months)",
            "frameworks": [r.framework_name for r in immediate],
            "objectives": [
                "Establish core measurement systems",
                "Address most critical pain points",
                "Quick wins for team morale"
            ],
            "expected_outcomes": [
                "Improved visibility into key metrics",
                "Initial process improvements",
                "Team alignment on priorities"
            ]
        },
        "phase_2": {
            "name": "Growth (3-6 months)",
            "frameworks": [r.framework_name for r in short_term],
            "objectives": [
                "Scale successful initiatives",
                "Optimize core operations",
                "Build competitive advantages"
            ],
            "expected_outcomes": [
                "Accelerated growth metrics",
                "Improved operational efficiency",
                "Stronger market position"
            ]
        },
        "phase_3": {
            "name": "Excellence (6-12 months)",
            "frameworks": [r.framework_name for r in long_term],
            "objectives": [
                "Achieve operational excellence",
                "Develop innovation capabilities",
                "Prepare for next growth stage"
            ],
            "expected_outcomes": [
                "Industry-leading performance",
                "Sustainable competitive advantages",
                "Platform for future expansion"
            ]
        }
    }
    
    return roadmap


# Main endpoint
@framework_analysis_router.post("/recommend")
async def get_intelligent_framework_recommendations(
    request: StartupAnalysisRequest
) -> FrameworkAnalysisResponse:
    """
    Get AI-powered framework recommendations based on comprehensive startup analysis
    
    This endpoint:
    1. Analyzes the startup's situation using LLM
    2. Identifies critical needs and priorities
    3. Selects most relevant frameworks from 554 available
    4. Provides detailed implementation guidance
    """
    try:
        logger.info(f"Analyzing startup: {request.company_stage} {request.industry} company")
        
        # Step 1: Analyze situation with LLM
        situation_analysis = await analyze_startup_situation_with_llm(request)
        logger.info(f"Situation analysis complete: {len(situation_analysis.get('critical_needs', []))} critical needs identified")
        
        # Step 2: Select frameworks intelligently
        selected_frameworks = await select_frameworks_intelligently(request, situation_analysis)
        logger.info(f"Selected {len(selected_frameworks)} relevant frameworks")
        
        # Step 3: Create detailed recommendations
        recommendations = []
        for i, (framework_id, score, reason) in enumerate(selected_frameworks):
            framework = FRAMEWORK_DATABASE.get(framework_id)
            if framework:
                recommendation = create_framework_recommendation(
                    framework_id=framework_id,
                    framework=framework,
                    score=score,
                    reason=reason,
                    priority=i + 1,
                    startup_data=request
                )
                recommendations.append(recommendation)
        
        # Step 4: Create implementation roadmap
        roadmap = create_implementation_roadmap(recommendations, situation_analysis)
        
        # Step 5: Generate situation summary
        situation_summary = f"""
Based on analysis of your {request.company_stage} {request.industry} company with {request.team_size_full_time} employees:

Key Findings:
- Current challenges: {', '.join(situation_analysis.get('critical_needs', [])[:3])}
- Recommended focus areas: {', '.join(situation_analysis.get('recommended_categories', []))}
- Implementation approach: {situation_analysis.get('implementation_timeline', 'Phased')} with {situation_analysis.get('complexity_preference', 'Intermediate')} complexity

Your startup would benefit most from frameworks that address {situation_analysis.get('critical_needs', ['your key challenges'])[0].lower()} 
while building foundations for sustainable growth.
        """.strip()
        
        # Success factors based on analysis
        success_factors = [
            "Executive commitment to framework implementation",
            "Dedicated resources for change management",
            "Regular progress tracking and adaptation",
            f"Focus on {situation_analysis.get('strategic_priorities', ['quick wins'])[0].lower()}",
            "Cross-functional collaboration and buy-in"
        ]
        
        return FrameworkAnalysisResponse(
            recommendations=recommendations[:10],  # Top 10 most relevant
            situation_analysis=situation_summary,
            strategic_priorities=situation_analysis.get('strategic_priorities', []),
            implementation_roadmap=roadmap,
            success_factors=success_factors,
            total_frameworks_analyzed=len(FRAMEWORK_DATABASE),
            selection_rationale=f"Frameworks selected based on {request.company_stage} stage needs, {request.industry} industry best practices, and your specific challenges"
        )
        
    except Exception as e:
        logger.error(f"Framework recommendation error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Framework analysis failed: {str(e)}")


@framework_analysis_router.post("/analyze-with-frameworks")
async def analyze_startup_with_frameworks(request: StartupAnalysisRequest) -> Dict[str, Any]:
    """
    Complete startup analysis using selected frameworks
    
    This endpoint:
    1. Gets framework recommendations
    2. Applies relevant frameworks to analyze the startup
    3. Provides actionable insights and next steps
    """
    try:
        # First get framework recommendations
        recommendations_response = await get_intelligent_framework_recommendations(request)
        
        # Select top frameworks for analysis
        top_frameworks = recommendations_response.recommendations[:5]
        
        # Apply each framework to generate insights
        framework_insights = []
        
        for rec in top_frameworks:
            framework = FRAMEWORK_DATABASE.get(rec.framework_id)
            if framework:
                insight = {
                    "framework": rec.framework_name,
                    "category": rec.category,
                    "analysis": f"Applying {framework.name} to your situation reveals opportunities in {rec.why_selected.lower()}",
                    "key_findings": rec.specific_benefits,
                    "action_items": framework.application_steps[:3] if hasattr(framework, 'application_steps') else [],
                    "expected_impact": rec.expected_impact,
                    "implementation_timeline": rec.time_to_value
                }
                framework_insights.append(insight)
        
        # Generate overall analysis
        overall_analysis = {
            "executive_summary": recommendations_response.situation_analysis,
            "framework_insights": framework_insights,
            "strategic_priorities": recommendations_response.strategic_priorities,
            "implementation_roadmap": recommendations_response.implementation_roadmap,
            "next_steps": [
                f"Begin with {top_frameworks[0].framework_name} to address {recommendations_response.strategic_priorities[0] if recommendations_response.strategic_priorities else 'immediate needs'}",
                "Establish baseline metrics for tracking progress",
                "Assign framework champions for each priority area",
                "Schedule weekly reviews to track implementation progress"
            ],
            "success_metrics": [
                "Framework adoption rate across teams",
                "Improvement in key business metrics",
                "Time to achieve quick wins",
                "Team satisfaction with new processes"
            ]
        }
        
        return overall_analysis
        
    except Exception as e:
        logger.error(f"Framework analysis error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


@framework_analysis_router.get("/categories-with-relevance")
async def get_framework_categories_with_relevance(
    stage: Optional[str] = None,
    industry: Optional[str] = None,
    challenge: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get framework categories with relevance scores based on filters
    """
    categories_relevance = {}
    
    # Define relevance mappings
    stage_category_relevance = {
        "pre-seed": ["Innovation", "Product", "Customer", "Startup"],
        "seed": ["Product", "Growth", "Customer", "Marketing"],
        "series-a": ["Growth", "Sales", "Operations", "Financial"],
        "series-b": ["Operations", "Leadership", "Organizational", "Growth"],
        "series-c": ["Strategy", "Organizational", "Digital", "Risk"]
    }
    
    industry_category_relevance = {
        "saas": ["Product", "Growth", "Customer", "Financial"],
        "ecommerce": ["Marketing", "Operations", "Customer", "Digital"],
        "fintech": ["Risk", "Financial", "Technology", "Compliance"],
        "healthtech": ["Quality", "Risk", "Innovation", "Operations"],
        "b2b": ["Sales", "Customer", "Strategy", "Growth"],
        "b2c": ["Marketing", "Customer", "Digital", "Growth"]
    }
    
    # Calculate relevance for each category
    for category in FrameworkCategory:
        relevance_score = 0.5  # Base relevance
        category_name = category.value
        
        # Stage relevance
        if stage and stage in stage_category_relevance:
            if category_name in stage_category_relevance[stage]:
                relevance_score += 0.2
        
        # Industry relevance
        if industry and industry.lower() in industry_category_relevance:
            if category_name in industry_category_relevance[industry.lower()]:
                relevance_score += 0.2
        
        # Challenge relevance
        if challenge:
            challenge_lower = challenge.lower()
            if any(word in challenge_lower for word in category_name.lower().split()):
                relevance_score += 0.1
        
        # Count frameworks in category
        framework_count = sum(1 for f in FRAMEWORK_DATABASE.values() 
                            if f.category == category)
        
        categories_relevance[category_name] = {
            "relevance_score": round(min(relevance_score, 1.0), 2),
            "framework_count": framework_count,
            "description": get_category_description(category),
            "typical_use_cases": get_category_use_cases(category)
        }
    
    # Sort by relevance
    sorted_categories = dict(
        sorted(categories_relevance.items(), 
               key=lambda x: x[1]["relevance_score"], 
               reverse=True)
    )
    
    return {
        "categories": sorted_categories,
        "filters_applied": {
            "stage": stage,
            "industry": industry,
            "challenge": challenge
        },
        "total_frameworks": len(FRAMEWORK_DATABASE)
    }


def get_category_description(category: FrameworkCategory) -> str:
    """Get description for framework category"""
    descriptions = {
        FrameworkCategory.STRATEGY: "Strategic planning and competitive positioning frameworks",
        FrameworkCategory.INNOVATION: "Innovation methodologies and creative problem-solving approaches",
        FrameworkCategory.GROWTH: "Growth hacking and scaling frameworks",
        FrameworkCategory.FINANCIAL: "Financial analysis and unit economics frameworks",
        FrameworkCategory.OPERATIONS: "Operational efficiency and process optimization",
        FrameworkCategory.MARKETING: "Marketing strategy and customer acquisition frameworks",
        FrameworkCategory.PRODUCT: "Product development and management methodologies",
        FrameworkCategory.LEADERSHIP: "Leadership development and management frameworks",
        FrameworkCategory.ORGANIZATIONAL: "Organizational design and culture frameworks",
        FrameworkCategory.ANALYTICS: "Data analysis and decision-making frameworks",
        FrameworkCategory.CUSTOMER: "Customer experience and satisfaction frameworks",
        FrameworkCategory.TECHNOLOGY: "Technology adoption and digital transformation",
        FrameworkCategory.RISK: "Risk management and mitigation strategies",
        FrameworkCategory.CHANGE: "Change management and transformation frameworks",
        FrameworkCategory.QUALITY: "Quality assurance and continuous improvement",
        FrameworkCategory.SALES: "Sales methodologies and revenue optimization",
        FrameworkCategory.HR: "Human resources and talent management",
        FrameworkCategory.SUSTAINABILITY: "Sustainable business and ESG frameworks",
        FrameworkCategory.DIGITAL: "Digital transformation and innovation frameworks",
        FrameworkCategory.STARTUP: "Startup-specific methodologies and frameworks"
    }
    return descriptions.get(category, "Business frameworks for this category")


def get_category_use_cases(category: FrameworkCategory) -> List[str]:
    """Get typical use cases for framework category"""
    use_cases = {
        FrameworkCategory.STRATEGY: [
            "Entering new markets",
            "Competitive analysis",
            "Long-term planning",
            "Strategic pivots"
        ],
        FrameworkCategory.GROWTH: [
            "Scaling customer acquisition",
            "Improving retention",
            "Expanding revenue streams",
            "Geographic expansion"
        ],
        FrameworkCategory.PRODUCT: [
            "Feature prioritization",
            "Product-market fit",
            "User experience design",
            "Product lifecycle management"
        ],
        FrameworkCategory.FINANCIAL: [
            "Improving unit economics",
            "Fundraising preparation",
            "Cash flow optimization",
            "Financial modeling"
        ]
    }
    return use_cases.get(category, ["General business improvement", "Process optimization"])


# Export router
__all__ = ['framework_analysis_router']