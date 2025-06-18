"""
Enhanced Framework Intelligence API with DeepSeek Integration
Generates dynamic, context-specific framework analysis using AI
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
import logging
import json
import aiohttp
import asyncio
from datetime import datetime
import os
from tenacity import retry, stop_after_attempt, wait_exponential

# Framework intelligence modules
from framework_intelligence.enhanced_framework_selector import EnhancedFrameworkSelector
from framework_intelligence.framework_database import FrameworkDatabase


def get_framework_attr(framework, attr_name, default=None):
    """Safely get attribute from framework object or dict"""
    if hasattr(framework, attr_name):
        return getattr(framework, attr_name)
    elif isinstance(framework, dict):
        return framework.get(attr_name, default)
    return default

logger = logging.getLogger(__name__)

# DeepSeek configuration
DEEPSEEK_API_KEY = os.environ.get("DEEPSEEK_API_KEY", "sk-c57ed3d5cf5a450e81b0e9f2ad25773d")
DEEPSEEK_BASE_URL = "https://api.deepseek.com/v1"

# Router for framework intelligence endpoints
router = APIRouter(prefix="/api/frameworks", tags=["framework-intelligence"])

# Initialize framework components
db = FrameworkDatabase()
enhanced_selector = EnhancedFrameworkSelector(db)

class FrameworkRequest(BaseModel):
    company_name: str
    industry: str
    stage: str
    challenges: List[str]
    assessment_data: Optional[Dict[str, Any]] = None

class FrameworkRecommendation(BaseModel):
    framework_id: str
    framework_name: str
    relevance_score: float
    why_relevant: str
    category: str
    complexity: str
    typical_timeline: str

class FrameworkAnalysis(BaseModel):
    framework_id: str
    framework_name: str
    analysis: Dict[str, Any]
    implementation_guide: Dict[str, Any]
    expected_outcomes: List[str]
    success_metrics: List[str]

async def call_deepseek(prompt: str, max_tokens: int = 1000) -> str:
    """Call DeepSeek API for framework analysis"""
    try:
        timeout = aiohttp.ClientTimeout(total=30)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            payload = {
                "model": "deepseek-chat",
                "messages": [
                    {
                        "role": "system",
                        "content": "You are a McKinsey senior consultant specializing in business frameworks and strategic analysis."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "temperature": 0.3,
                "max_tokens": max_tokens
            }
            
            headers = {
                "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
                "Content-Type": "application/json"
            }
            
            async with session.post(
                f"{DEEPSEEK_BASE_URL}/chat/completions",
                json=payload,
                headers=headers
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    return data['choices'][0]['message']['content'].strip()
                else:
                    logger.error(f"DeepSeek API error: {response.status}")
                    return None
    except Exception as e:
        logger.error(f"DeepSeek API call failed: {e}")
        return None

async def generate_dynamic_framework_analysis(
    framework_id: str,
    framework_name: str,
    company_data: Dict[str, Any]
) -> Dict[str, Any]:
    """Generate dynamic framework analysis using DeepSeek"""
    
    # Get framework details from database
    framework = db.get_framework(framework_id)
    if not framework:
        logger.warning(f"Framework {framework_id} not found, using generic analysis")
        return generate_fallback_analysis(framework_id, framework_name, company_data)
    
    # Create a detailed prompt for DeepSeek
    prompt = f"""
    Apply the {framework_name} framework to analyze {company_data.get('company_name', 'this startup')}.

    Company Context:
    - Industry: {company_data.get('industry', 'technology')}
    - Stage: {company_data.get('stage', 'growth').replace('_', ' ').title()}
    - Funding: ${company_data.get('total_funding', 5000000):,}
    - Team Size: {company_data.get('team_size', 20)}
    - Key Challenges: {', '.join(company_data.get('challenges', ['scaling', 'competition']))}

    Framework Description: {framework.get('description', '')}
    Framework Components: {', '.join(framework.get('components', []))}

    Please provide:
    1. Current State Analysis using this framework
    2. Key Insights and Findings
    3. Strategic Recommendations
    4. Action Items

    Format the response as structured sections, not JSON.
    """
    
    # Call DeepSeek
    analysis_text = await call_deepseek_safe(prompt)
    
    if not analysis_text:
        logger.warning(f"DeepSeek failed for {framework_id}, using fallback")
        return generate_fallback_analysis(framework_id, framework_name, company_data)
    
    # Parse the text response into structured format
    analysis = parse_framework_analysis(analysis_text, framework_id, framework_name)
    
    # Add company-specific metrics
    analysis['company_context'] = {
        'name': company_data.get('company_name', 'Company'),
        'industry': company_data.get('industry', 'technology'),
        'stage': company_data.get('stage', 'growth'),
        'primary_challenge': company_data.get('challenges', ['growth'])[0] if company_data.get('challenges') else 'growth'
    }
    
    return analysis

def parse_framework_analysis(text: str, framework_id: str, framework_name: str) -> Dict[str, Any]:
    """Parse DeepSeek text response into structured analysis"""
    
    # Split text into sections
    sections = text.split('\n\n')
    
    analysis = {
        'framework_id': framework_id,
        'framework_name': framework_name,
        'current_state': '',
        'key_insights': [],
        'recommendations': [],
        'action_items': [],
        'summary': ''
    }
    
    current_section = None
    
    for section in sections:
        section_lower = section.lower()
        
        if 'current state' in section_lower or 'analysis' in section_lower:
            current_section = 'current_state'
            analysis['current_state'] = section
        elif 'insight' in section_lower or 'finding' in section_lower:
            current_section = 'insights'
            # Extract bullet points or numbered items
            lines = section.split('\n')
            for line in lines:
                line = line.strip()
                if line and (line[0].isdigit() or line.startswith('-') or line.startswith('•')):
                    analysis['key_insights'].append(line.lstrip('0123456789.-• '))
        elif 'recommend' in section_lower:
            current_section = 'recommendations'
            lines = section.split('\n')
            for line in lines:
                line = line.strip()
                if line and (line[0].isdigit() or line.startswith('-') or line.startswith('•')):
                    analysis['recommendations'].append(line.lstrip('0123456789.-• '))
        elif 'action' in section_lower or 'next step' in section_lower:
            current_section = 'actions'
            lines = section.split('\n')
            for line in lines:
                line = line.strip()
                if line and (line[0].isdigit() or line.startswith('-') or line.startswith('•')):
                    analysis['action_items'].append(line.lstrip('0123456789.-• '))
        elif current_section == 'current_state':
            analysis['current_state'] += '\n\n' + section
        
    # Generate summary if not present
    if not analysis['summary']:
        if analysis['key_insights']:
            analysis['summary'] = f"Analysis using {framework_name} reveals {len(analysis['key_insights'])} key insights and {len(analysis['recommendations'])} strategic recommendations."
        else:
            analysis['summary'] = f"{framework_name} analysis completed for strategic planning."
    
    return analysis

def generate_fallback_analysis(framework_id: str, framework_name: str, company_data: Dict[str, Any]) -> Dict[str, Any]:
    """Generate fallback analysis when DeepSeek is unavailable"""
    
    # Framework-specific fallback analyses
    fallback_analyses = {
        'ansoff_matrix': {
            'current_state': f"{company_data.get('company_name', 'The company')} is currently in the {company_data.get('stage', 'growth')} stage, focusing on {company_data.get('industry', 'technology')} market.",
            'key_insights': [
                f"Market Penetration: Strong potential to increase share in current {company_data.get('industry', 'technology')} market",
                "Product Development: Opportunity to expand product line based on customer feedback",
                "Market Development: Adjacent markets show promise for expansion",
                "Diversification: Should be considered only after exhausting other growth options"
            ],
            'recommendations': [
                "Focus on market penetration strategies for next 6-12 months",
                "Invest in product development to address unmet customer needs",
                "Explore geographic expansion as secondary growth driver",
                "Build capabilities for future market development"
            ],
            'action_items': [
                "Conduct market share analysis in current segments",
                "Survey customers for product enhancement ideas",
                "Research adjacent market opportunities",
                "Develop growth scenario planning"
            ]
        },
        'bcg_matrix': {
            'current_state': f"Portfolio analysis for {company_data.get('company_name', 'the company')} shows mixed positioning across business units.",
            'key_insights': [
                "Star Products: High growth offerings requiring continued investment",
                "Cash Cows: Established products generating steady revenue",
                "Question Marks: New initiatives with uncertain potential",
                "Dogs: Legacy offerings with declining relevance"
            ],
            'recommendations': [
                "Invest heavily in Star products to maintain market leadership",
                "Optimize Cash Cows for maximum profitability",
                "Make decisive choices on Question Marks - invest or divest",
                "Phase out Dogs strategically to free up resources"
            ],
            'action_items': [
                "Map all products/services to BCG quadrants",
                "Allocate resources based on portfolio position",
                "Set clear metrics for Question Mark evaluation",
                "Create sunset plan for Dog products"
            ]
        },
        'porters_five_forces': {
            'current_state': f"Competitive analysis reveals {company_data.get('industry', 'technology')} industry dynamics affecting {company_data.get('company_name', 'the company')}.",
            'key_insights': [
                "Competitive Rivalry: Intense competition from established players",
                "Buyer Power: Increasing as customers have more choices",
                "Supplier Power: Moderate with multiple vendor options",
                "Threat of Substitutes: Growing from alternative solutions",
                "Barriers to Entry: Moderately high due to technical requirements"
            ],
            'recommendations': [
                "Differentiate through unique value proposition",
                "Build switching costs to reduce buyer power",
                "Diversify supplier base to reduce dependency",
                "Monitor emerging substitutes closely",
                "Strengthen competitive moats"
            ],
            'action_items': [
                "Conduct competitor analysis quarterly",
                "Implement customer loyalty programs",
                "Negotiate long-term supplier agreements",
                "Track technology trends for disruption signals",
                "Patent key innovations"
            ]
        }
    }
    
    # Use specific analysis if available, otherwise generate generic
    if framework_id in fallback_analyses:
        analysis = fallback_analyses[framework_id]
    else:
        # Generic fallback
        analysis = {
            'current_state': f"Applying {framework_name} to analyze {company_data.get('company_name', 'the company')}'s strategic position.",
            'key_insights': [
                f"Current {company_data.get('stage', 'growth')} stage requires focused strategy",
                f"{company_data.get('industry', 'Technology')} market dynamics are evolving rapidly",
                "Resource constraints necessitate strategic prioritization",
                "Competitive landscape demands clear differentiation"
            ],
            'recommendations': [
                "Prioritize initiatives based on strategic fit",
                "Allocate resources to highest-impact areas",
                "Build capabilities for long-term success",
                "Monitor and adapt to market changes"
            ],
            'action_items': [
                f"Apply {framework_name} principles to current challenges",
                "Develop implementation roadmap",
                "Set measurable success metrics",
                "Review and adjust quarterly"
            ]
        }
    
    analysis['framework_id'] = framework_id
    analysis['framework_name'] = framework_name
    analysis['company_context'] = {
        'name': company_data.get('company_name', 'Company'),
        'industry': company_data.get('industry', 'technology'),
        'stage': company_data.get('stage', 'growth')
    }
    
    return analysis

def extract_context_from_assessment(assessment_data: Dict[str, Any]) -> Dict[str, Any]:
    """Extract business context from assessment data"""
    
    # Map funding stage to business stage
    funding_to_stage = {
        'pre_seed': 'startup',
        'seed': 'startup',
        'series_a': 'growth',
        'series_b': 'growth',
        'series_c': 'expansion',
        'series_d': 'expansion',
        'growth': 'mature'
    }
    
    # Extract challenges based on metrics
    challenges = []
    
    # Revenue/growth challenges
    revenue_growth = assessment_data.get('revenue_growth_rate_percent', 0)
    if revenue_growth < 20:
        challenges.append('growth')
        challenges.append('revenue_scaling')
    
    # Burn rate challenges
    burn_multiple = assessment_data.get('burn_multiple', 1)
    if burn_multiple > 2:
        challenges.append('cash_management')
        challenges.append('unit_economics')
    
    # Market challenges
    competition = assessment_data.get('competition_intensity', 3)
    if competition >= 4:
        challenges.append('competition')
        challenges.append('differentiation')
    
    # Team challenges
    team_size = assessment_data.get('team_size_full_time', 10)
    if team_size < 10:
        challenges.append('talent_acquisition')
    elif team_size > 50:
        challenges.append('organizational_scaling')
    
    # Customer challenges
    customer_concentration = assessment_data.get('customer_concentration_percent', 0)
    if customer_concentration > 30:
        challenges.append('customer_diversification')
    
    # Product challenges
    product_stage = assessment_data.get('product_stage', 'mvp')
    if product_stage in ['idea', 'prototype', 'mvp']:
        challenges.append('product_development')
        challenges.append('product_market_fit')
    
    # Default challenges if none identified
    if not challenges:
        challenges = ['growth', 'scaling', 'competition']
    
    return {
        'company_name': assessment_data.get('company_name', assessment_data.get('startup_name', 'Company')),
        'industry': assessment_data.get('sector', assessment_data.get('industry', 'technology')),
        'stage': funding_to_stage.get(
            assessment_data.get('funding_stage', 'series_a'), 
            'growth'
        ),
        'challenges': list(set(challenges))[:5],  # Top 5 unique challenges
        'team_size': assessment_data.get('team_size_full_time', 20),
        'total_funding': assessment_data.get('total_capital_raised_usd', 5000000),
        'revenue': assessment_data.get('annual_revenue_run_rate', 1000000),
        'growth_rate': assessment_data.get('revenue_growth_rate_percent', 20)
    }

@router.post("/recommend/dynamic", response_model=List[FrameworkRecommendation])
async def recommend_frameworks_dynamic(request: FrameworkRequest):
    """Get framework recommendations with dynamic analysis"""
    try:
        # Extract context from assessment data if provided
        if request.assessment_data:
            context = extract_context_from_assessment(request.assessment_data)
            # Override with explicit values if provided
            context['company_name'] = request.company_name or context.get('company_name', 'Company')
            context['industry'] = request.industry or context.get('industry', 'technology')
            context['stage'] = request.stage or context.get('stage', 'growth')
            if request.challenges:
                context['challenges'] = request.challenges
        else:
            context = {
                'company_name': request.company_name,
                'industry': request.industry,
                'stage': request.stage,
                'challenges': request.challenges
            }
        
        # Get enhanced recommendations
        recommendations = enhanced_selector.recommend_frameworks_enhanced(
            business_stage=context['stage'],
            industry=context['industry'],
            primary_challenge=context['challenges'][0] if context['challenges'] else 'growth',
            company_size=context.get('team_size', 20),
            budget_level='medium',
            time_horizon='medium',
            strategic_goals=context['challenges'],
            top_k=6
        )
        
        # Convert to response format
        formatted_recommendations = []
        for rec in recommendations:
            framework = db.get_framework(rec['id'])
            if framework:
                formatted_recommendations.append(
                    FrameworkRecommendation(
                        framework_id=rec['id'],
                        framework_name=rec['name'],
                        relevance_score=rec['score'],
                        why_relevant=rec['reason'],
                        category=framework.get('category', 'Strategy'),
                        complexity=framework.get('complexity', 'Medium'),
                        typical_timeline=framework.get('typical_timeline', '2-4 weeks')
                    )
                )
        
        return formatted_recommendations
        
    except Exception as e:
        logger.error(f"Error in framework recommendation: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/analyze/{framework_id}", response_model=FrameworkAnalysis)
async def analyze_with_framework(
    framework_id: str,
    assessment_data: Dict[str, Any]
):
    """Apply a specific framework to analyze the startup with dynamic content"""
    try:
        # Get framework details
        framework = db.get_framework(framework_id)
        if not framework:
            raise HTTPException(status_code=404, detail=f"Framework {framework_id} not found")
        
        # Extract context
        context = extract_context_from_assessment(assessment_data)
        
        # Generate dynamic analysis using DeepSeek
        analysis = await generate_dynamic_framework_analysis(
            framework_id,
            framework.name if hasattr(framework, 'name') else framework.get('name', ''),
            context
        )
        
        # Generate implementation guide
        implementation_guide = {
            'phases': [
                {
                    'phase': 'Preparation',
                    'duration': '1 week',
                    'activities': ['Gather data', 'Align stakeholders', 'Set objectives']
                },
                {
                    'phase': 'Analysis',
                    'duration': '2 weeks',
                    'activities': analysis.get('action_items', ['Apply framework', 'Document findings'])[:3]
                },
                {
                    'phase': 'Implementation',
                    'duration': '4-8 weeks',
                    'activities': analysis.get('recommendations', ['Execute recommendations', 'Monitor progress'])[:3]
                }
            ],
            'resources_needed': ['Strategic planning team', 'Data analyst', 'Domain experts'],
            'key_stakeholders': ['CEO', 'Department heads', 'Board members']
        }
        
        # Extract expected outcomes from analysis
        expected_outcomes = []
        if analysis.get('recommendations'):
            for rec in analysis['recommendations'][:3]:
                expected_outcomes.append(f"Achieved: {rec}")
        else:
            expected_outcomes = [
                'Clear strategic direction established',
                'Actionable roadmap developed',
                'Team alignment achieved'
            ]
        
        # Define success metrics
        success_metrics = [
            'Strategic objectives defined and measured',
            'Implementation milestones tracked',
            'ROI on strategic initiatives',
            'Team engagement scores'
        ]
        
        return FrameworkAnalysis(
            framework_id=framework_id,
            framework_name=framework.name if hasattr(framework, 'name') else framework.get('name', ''),
            analysis=analysis,
            implementation_guide=implementation_guide,
            expected_outcomes=expected_outcomes,
            success_metrics=success_metrics
        )
        
    except Exception as e:
        logger.error(f"Error in framework analysis: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/test/{framework_id}")
async def test_framework_analysis(framework_id: str):
    """Test endpoint to debug framework analysis"""
    try:
        # Test data
        test_company = {
            'company_name': 'TechStartup AI',
            'industry': 'artificial_intelligence',
            'stage': 'series_a',
            'challenges': ['scaling', 'competition', 'talent_acquisition'],
            'team_size': 25,
            'total_funding': 10000000
        }
        
        # Get framework
        framework = db.get_framework(framework_id)
        if not framework:
            return {"error": f"Framework {framework_id} not found"}
        
        # Generate analysis
        analysis = await generate_dynamic_framework_analysis(
            framework_id,
            framework.name if hasattr(framework, 'name') else framework.get('name', ''),
            test_company
        )
        
        return {
            "framework": framework,
            "test_company": test_company,
            "analysis": analysis
        }
        
    except Exception as e:
        logger.error(f"Test error: {str(e)}")
        return {"error": str(e)}

# Include these routes in the main app
def include_intelligent_routes(app):
    """Include the framework intelligence routes in the FastAPI app"""
    app.include_router(router)
    logger.info("Framework Intelligence routes with DeepSeek integration included")
