"""
API endpoints for Michelin-format framework implementation
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Dict, List, Any, Optional
import logging
from datetime import datetime

from framework_intelligence.framework_implementation import (
    FrameworkImplementation,
    FrameworkPosition,
    FrameworkInsight,
    FrameworkAction
)
from framework_intelligence.framework_database import FRAMEWORKS
from llm_analysis import LLMAnalyzer

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create router
implementation_router = APIRouter(prefix="/api/framework-implementation", tags=["framework-implementation"])

# Initialize services
framework_impl = FrameworkImplementation()
llm_analyzer = LLMAnalyzer()

class CompanyData(BaseModel):
    """Company data for framework analysis"""
    company_info: Dict[str, Any]
    capital: Dict[str, Any]
    advantage: Dict[str, Any]
    market: Dict[str, Any]
    people: Dict[str, Any]
    
class FrameworkAnalysisRequest(BaseModel):
    """Request for single framework analysis"""
    framework_id: str = Field(..., description="ID of the framework to apply")
    company_data: CompanyData = Field(..., description="Company data from assessment")
    include_visualization: bool = Field(True, description="Include visualization data")
    
class MultiFrameworkRequest(BaseModel):
    """Request for multiple framework analysis"""
    framework_ids: List[str] = Field(..., description="List of framework IDs to apply")
    company_data: CompanyData = Field(..., description="Company data from assessment")
    max_frameworks: int = Field(5, description="Maximum number of frameworks to apply")
    
class InsightGenerationRequest(BaseModel):
    """Request for deep insight generation"""
    framework_id: str
    position: Dict[str, Any]
    company_data: CompanyData
    focus_areas: Optional[List[str]] = Field(None, description="Specific areas to focus on")

@implementation_router.post("/apply-framework")
async def apply_framework(request: FrameworkAnalysisRequest):
    """
    Apply a specific framework to company data and return Michelin-format analysis
    """
    try:
        logger.info(f"Applying framework {request.framework_id} to company {request.company_data.company_info.get('name', 'Unknown')}")
        
        # Convert Pydantic model to dict
        company_data_dict = request.company_data.dict()
        
        # Apply framework
        result = framework_impl.apply_framework(request.framework_id, company_data_dict)
        
        # Enhance with LLM insights if framework is complex
        if result.get('status') != 'partial_implementation':
            enhanced_insights = await enhance_insights_with_llm(result, company_data_dict)
            result['enhanced_insights'] = enhanced_insights
        
        # Add metadata
        result['api_version'] = '2.0'
        result['analysis_timestamp'] = datetime.now().isoformat()
        
        return {
            'success': True,
            'framework_analysis': result,
            'framework_info': get_framework_info(request.framework_id)
        }
        
    except Exception as e:
        logger.error(f"Error applying framework: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@implementation_router.post("/apply-multiple-frameworks")
async def apply_multiple_frameworks(request: MultiFrameworkRequest):
    """
    Apply multiple frameworks and synthesize insights
    """
    try:
        results = []
        company_data_dict = request.company_data.dict()
        
        # Apply each framework
        for framework_id in request.framework_ids[:request.max_frameworks]:
            try:
                result = framework_impl.apply_framework(framework_id, company_data_dict)
                results.append(result)
            except Exception as e:
                logger.warning(f"Failed to apply framework {framework_id}: {str(e)}")
                continue
        
        # Generate executive summary
        if results:
            summary = framework_impl.generate_executive_summary(results)
        else:
            summary = {'error': 'No frameworks could be applied'}
        
        return {
            'success': True,
            'framework_results': results,
            'executive_summary': summary,
            'frameworks_applied': len(results)
        }
        
    except Exception as e:
        logger.error(f"Error applying multiple frameworks: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@implementation_router.post("/bcg-matrix")
async def apply_bcg_matrix(request: FrameworkAnalysisRequest):
    """
    Specialized endpoint for BCG Matrix with enhanced visualization
    """
    try:
        company_data_dict = request.company_data.dict()
        
        # Apply BCG Matrix
        result = framework_impl._implement_bcg_matrix(company_data_dict)
        
        # Enhance with competitive analysis
        if company_data_dict.get('market', {}).get('competitors'):
            result['competitive_landscape'] = analyze_competitive_position(
                company_data_dict,
                result['position']
            )
        
        return {
            'success': True,
            'bcg_analysis': result,
            'strategic_options': generate_bcg_strategies(result['position'].position)
        }
        
    except Exception as e:
        logger.error(f"Error in BCG Matrix analysis: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@implementation_router.post("/ansoff-matrix")
async def apply_ansoff_matrix(request: FrameworkAnalysisRequest):
    """
    Specialized endpoint for Ansoff Matrix with growth strategies
    """
    try:
        company_data_dict = request.company_data.dict()
        
        # Apply Ansoff Matrix
        result = framework_impl._implement_ansoff_matrix(company_data_dict)
        
        # Generate specific growth tactics
        result['growth_tactics'] = generate_growth_tactics(
            result['strategy_scores'],
            company_data_dict
        )
        
        return {
            'success': True,
            'ansoff_analysis': result,
            'recommended_strategy': result['position'].position,
            'implementation_timeline': generate_growth_timeline(result['position'].position)
        }
        
    except Exception as e:
        logger.error(f"Error in Ansoff Matrix analysis: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@implementation_router.post("/porters-five-forces")
async def apply_porters_five_forces(request: FrameworkAnalysisRequest):
    """
    Specialized endpoint for Porter's Five Forces with competitive dynamics
    """
    try:
        company_data_dict = request.company_data.dict()
        
        # Apply Porter's Five Forces
        result = framework_impl._implement_porters_five_forces(company_data_dict)
        
        # Add industry benchmarks
        result['industry_benchmarks'] = get_industry_benchmarks(
            company_data_dict.get('company_info', {}).get('sector')
        )
        
        # Generate competitive strategies
        result['competitive_strategies'] = generate_competitive_strategies(
            result['force_analysis'],
            company_data_dict
        )
        
        return {
            'success': True,
            'five_forces_analysis': result,
            'industry_attractiveness': result['position'].position,
            'strategic_implications': analyze_strategic_implications(result['force_analysis'])
        }
        
    except Exception as e:
        logger.error(f"Error in Porter's Five Forces analysis: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@implementation_router.post("/lean-canvas")
async def apply_lean_canvas(request: FrameworkAnalysisRequest):
    """
    Specialized endpoint for Lean Canvas with startup focus
    """
    try:
        company_data_dict = request.company_data.dict()
        
        # Apply Lean Canvas
        result = framework_impl._implement_lean_canvas(company_data_dict)
        
        # Add validation metrics
        result['validation_metrics'] = generate_validation_metrics(
            result['canvas_data'],
            company_data_dict
        )
        
        # Generate experiment suggestions
        result['experiments'] = suggest_validation_experiments(
            result['canvas_data'],
            company_data_dict
        )
        
        return {
            'success': True,
            'lean_canvas_analysis': result,
            'canvas_strength': result['position'].score,
            'next_steps': generate_lean_next_steps(result['canvas_data'])
        }
        
    except Exception as e:
        logger.error(f"Error in Lean Canvas analysis: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@implementation_router.get("/available-frameworks")
async def get_available_frameworks():
    """
    Get list of frameworks available for implementation
    """
    implemented_frameworks = list(framework_impl.framework_implementations.keys())
    
    frameworks = []
    for fw_id in implemented_frameworks:
        if fw_id in FRAMEWORKS:
            fw = FRAMEWORKS[fw_id]
            frameworks.append({
                'id': fw_id,
                'name': fw.name,
                'category': fw.category.value,
                'description': fw.description,
                'implementation_status': 'full'
            })
    
    # Add partially implemented frameworks
    for fw_id, fw in FRAMEWORKS.items():
        if fw_id not in implemented_frameworks:
            frameworks.append({
                'id': fw_id,
                'name': fw.name,
                'category': fw.category.value,
                'description': fw.description,
                'implementation_status': 'partial'
            })
    
    return {
        'success': True,
        'total_frameworks': len(frameworks),
        'fully_implemented': len(implemented_frameworks),
        'frameworks': frameworks
    }

@implementation_router.post("/generate-insights")
async def generate_deep_insights(request: InsightGenerationRequest):
    """
    Generate deep, contextual insights for a framework position
    """
    try:
        company_data_dict = request.company_data.dict()
        
        # Use LLM to generate deeper insights
        prompt = f"""
        Company: {company_data_dict.get('company_info', {}).get('name')}
        Framework: {request.framework_id}
        Position: {request.position}
        
        Key metrics:
        - Revenue: ${company_data_dict.get('capital', {}).get('monthly_revenue', 0):,}/month
        - Runway: {company_data_dict.get('capital', {}).get('runway', 0):.1f} months
        - Market share: {company_data_dict.get('market', {}).get('market_share', 0):.1f}%
        - Team size: {company_data_dict.get('people', {}).get('team_size', 0)}
        
        Generate 3 specific, actionable insights based on this framework position.
        """
        
        insights = await llm_analyzer.analyze(prompt, "framework_insights")
        
        return {
            'success': True,
            'framework_id': request.framework_id,
            'deep_insights': insights,
            'focus_areas': request.focus_areas or ['general']
        }
        
    except Exception as e:
        logger.error(f"Error generating insights: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Helper functions

def get_framework_info(framework_id: str) -> Dict[str, Any]:
    """Get framework information"""
    if framework_id in FRAMEWORKS:
        fw = FRAMEWORKS[framework_id]
        return {
            'name': fw.name,
            'category': fw.category.value,
            'description': fw.description,
            'typical_use_cases': fw.typical_use_cases
        }
    return {'name': framework_id, 'category': 'unknown'}

async def enhance_insights_with_llm(result: Dict[str, Any], company_data: Dict[str, Any]) -> List[str]:
    """Enhance framework insights with LLM analysis"""
    try:
        prompt = f"""
        Framework: {result['framework_name']}
        Company Position: {result['position'].position if hasattr(result['position'], 'position') else result['position']}
        
        Based on this analysis, provide 2 additional strategic insights specific to this company's situation.
        """
        
        enhanced = await llm_analyzer.analyze(prompt, "insight_enhancement")
        return enhanced.get('insights', [])
    except:
        return []

def analyze_competitive_position(company_data: Dict[str, Any], position: FrameworkPosition) -> Dict[str, Any]:
    """Analyze competitive position for BCG Matrix"""
    return {
        'market_leader': position.position in ['Star', 'Cash Cow'],
        'growth_potential': position.position in ['Star', 'Question Mark'],
        'resource_requirements': 'High' if position.position in ['Star', 'Question Mark'] else 'Low',
        'competitive_threats': identify_competitive_threats(company_data)
    }

def identify_competitive_threats(company_data: Dict[str, Any]) -> List[str]:
    """Identify competitive threats"""
    threats = []
    
    if company_data.get('market', {}).get('competitor_count', 0) > 10:
        threats.append("High number of competitors")
    
    if company_data.get('advantage', {}).get('differentiation_score', 0) < 3:
        threats.append("Low differentiation")
    
    if company_data.get('market', {}).get('market_share', 0) < 5:
        threats.append("Small market share vulnerable to competition")
    
    return threats

def generate_bcg_strategies(position: str) -> List[Dict[str, str]]:
    """Generate strategies based on BCG position"""
    strategies = {
        'Star': [
            {'strategy': 'Invest for growth', 'priority': 'High'},
            {'strategy': 'Defend market share', 'priority': 'High'},
            {'strategy': 'Build barriers to entry', 'priority': 'Medium'}
        ],
        'Question Mark': [
            {'strategy': 'Selective investment', 'priority': 'High'},
            {'strategy': 'Find defensible niche', 'priority': 'High'},
            {'strategy': 'Consider pivot or exit', 'priority': 'Medium'}
        ],
        'Cash Cow': [
            {'strategy': 'Maximize cash generation', 'priority': 'High'},
            {'strategy': 'Maintain position efficiently', 'priority': 'Medium'},
            {'strategy': 'Fund new ventures', 'priority': 'Medium'}
        ],
        'Dog': [
            {'strategy': 'Minimize investment', 'priority': 'High'},
            {'strategy': 'Consider divestment', 'priority': 'High'},
            {'strategy': 'Find niche or exit', 'priority': 'High'}
        ]
    }
    
    return strategies.get(position, [])

def generate_growth_tactics(strategy_scores: Dict[str, float], company_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Generate specific growth tactics based on Ansoff Matrix"""
    tactics = []
    
    # Get top strategy
    top_strategy = max(strategy_scores, key=strategy_scores.get)
    
    if top_strategy == 'market_penetration':
        tactics.extend([
            {
                'tactic': 'Increase usage frequency',
                'how': f"Target current {company_data.get('market', {}).get('customer_count', 0)} customers with engagement campaigns",
                'expected_impact': '20-30% revenue increase'
            },
            {
                'tactic': 'Win competitor customers',
                'how': 'Competitive switching campaigns with incentives',
                'expected_impact': '15% market share gain'
            }
        ])
    
    return tactics

def generate_growth_timeline(strategy: str) -> Dict[str, List[str]]:
    """Generate implementation timeline for growth strategy"""
    timelines = {
        'Market Penetration': {
            '0-3 months': ['Customer segmentation', 'Usage analysis', 'Retention programs'],
            '3-6 months': ['Upsell campaigns', 'Referral programs', 'Price optimization'],
            '6-12 months': ['Market consolidation', 'Category leadership', 'Expansion prep']
        },
        'Market Development': {
            '0-3 months': ['Market research', 'Localization', 'Channel partners'],
            '3-6 months': ['Pilot launch', 'Local team hiring', 'Marketing adaptation'],
            '6-12 months': ['Full market entry', 'Scale operations', 'Next market prep']
        }
    }
    
    return timelines.get(strategy, {})

def get_industry_benchmarks(sector: str) -> Dict[str, Any]:
    """Get industry benchmarks for Five Forces"""
    # Simplified benchmarks by sector
    benchmarks = {
        'saas': {
            'avg_competitive_rivalry': 4.2,
            'avg_buyer_power': 3.5,
            'avg_supplier_power': 2.1,
            'typical_margins': '70-80%',
            'market_concentration': 'Fragmented'
        },
        'fintech': {
            'avg_competitive_rivalry': 4.5,
            'avg_buyer_power': 3.8,
            'avg_supplier_power': 2.5,
            'typical_margins': '60-70%',
            'market_concentration': 'Consolidating'
        }
    }
    
    return benchmarks.get(sector, benchmarks['saas'])

def generate_competitive_strategies(forces: Dict[str, float], company_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Generate strategies based on Five Forces analysis"""
    strategies = []
    
    # Find strongest force
    strongest_force = max(forces, key=forces.get)
    
    if strongest_force == 'competitive_rivalry':
        strategies.append({
            'strategy': 'Differentiation',
            'tactics': ['Build unique features', 'Create switching costs', 'Focus on niche'],
            'timeline': '6-12 months'
        })
    elif strongest_force == 'buyer_power':
        strategies.append({
            'strategy': 'Reduce buyer power',
            'tactics': ['Diversify customer base', 'Increase switching costs', 'Build brand loyalty'],
            'timeline': '12-18 months'
        })
    
    return strategies

def analyze_strategic_implications(forces: Dict[str, float]) -> Dict[str, Any]:
    """Analyze strategic implications of Five Forces"""
    avg_force = sum(forces.values()) / len(forces)
    
    return {
        'industry_attractiveness': 'Low' if avg_force > 3.5 else 'Medium' if avg_force > 2.5 else 'High',
        'profit_potential': 'Challenging' if avg_force > 3.5 else 'Moderate' if avg_force > 2.5 else 'Strong',
        'strategic_focus': determine_strategic_focus(forces),
        'time_horizon': '12-24 months' if avg_force > 3.5 else '24-36 months'
    }

def determine_strategic_focus(forces: Dict[str, float]) -> str:
    """Determine strategic focus based on forces"""
    if forces['competitive_rivalry'] > 4:
        return 'Differentiation and niche focus'
    elif forces['buyer_power'] > 4:
        return 'Customer diversification and value creation'
    elif forces['threat_of_new_entrants'] > 4:
        return 'Build barriers to entry'
    else:
        return 'Balanced growth strategy'

def generate_validation_metrics(canvas_data: Dict[str, Any], company_data: Dict[str, Any]) -> Dict[str, Any]:
    """Generate validation metrics for Lean Canvas"""
    return {
        'problem_validation': {
            'score': canvas_data['problem']['score'],
            'metrics': ['Customer interviews', 'Problem severity ratings', 'Willingness to pay'],
            'target': 'Talk to 100 customers'
        },
        'solution_validation': {
            'score': canvas_data['solution']['score'],
            'metrics': ['MVP usage', 'Feature requests', 'Time to value'],
            'target': '40% activation rate'
        },
        'channel_validation': {
            'score': canvas_data['channels']['score'],
            'metrics': ['CAC by channel', 'Conversion rates', 'Channel scalability'],
            'target': 'CAC < $100'
        }
    }

def suggest_validation_experiments(canvas_data: Dict[str, Any], company_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Suggest experiments to validate Lean Canvas assumptions"""
    experiments = []
    
    # Find weakest areas
    weak_areas = [(k, v) for k, v in canvas_data.items() if v['score'] < 3]
    
    for area, data in weak_areas[:3]:  # Top 3 weak areas
        if area == 'problem':
            experiments.append({
                'area': 'Problem Validation',
                'experiment': 'Customer Discovery Interviews',
                'hypothesis': 'Target customers experience this problem severely enough to pay for a solution',
                'success_criteria': '70% of interviewees rate problem severity 4+ out of 5',
                'duration': '2 weeks'
            })
        elif area == 'channels':
            experiments.append({
                'area': 'Channel Testing',
                'experiment': 'Multi-channel CAC Test',
                'hypothesis': 'We can acquire customers for less than $100 through digital channels',
                'success_criteria': 'At least one channel shows CAC < $100',
                'duration': '4 weeks'
            })
    
    return experiments

def generate_lean_next_steps(canvas_data: Dict[str, Any]) -> List[str]:
    """Generate next steps based on Lean Canvas analysis"""
    next_steps = []
    
    # Check completion
    completion = sum(1 for block in canvas_data.values() if block['score'] > 2) / len(canvas_data)
    
    if completion < 0.5:
        next_steps.append("Complete customer discovery - talk to 50+ potential customers")
    
    if canvas_data['problem']['score'] < 3:
        next_steps.append("Validate problem severity through surveys and interviews")
    
    if canvas_data['channels']['score'] < 3:
        next_steps.append("Test 3 different acquisition channels with $1000 budget each")
    
    if canvas_data['revenue_streams']['score'] < 3:
        next_steps.append("Test pricing with 10 potential customers")
    
    return next_steps[:3]  # Top 3 priorities