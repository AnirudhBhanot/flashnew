"""
Wrapper to make the framework system work with the API
"""

from typing import Dict, Any, List
import asyncio
from framework_intelligence.enhanced_framework_selector import (
    EnhancedFrameworkSelector, StartupContext, BusinessStage, 
    IndustryType, ChallengeType
)
from framework_intelligence import framework_database

class FrameworkSystemWrapper:
    """Wrapper to simplify framework system usage"""
    
    def __init__(self):
        self.selector = EnhancedFrameworkSelector()
        
    def recommend_frameworks_simple(
        self,
        company_name: str,
        industry: str,
        stage: str,
        challenges: List[str],
        team_size: int = 20,
        top_k: int = 6
    ) -> List[Dict[str, Any]]:
        """Simple synchronous wrapper for framework recommendations"""
        
        # Map stage to BusinessStage enum
        stage_map = {
            'pre_seed': BusinessStage.IDEA,
            'seed': BusinessStage.MVP,
            'series_a': BusinessStage.GROWTH,
            'series_b': BusinessStage.GROWTH,
            'series_c': BusinessStage.SCALE,
            'growth': BusinessStage.MATURE,
            'startup': BusinessStage.MVP,
            'expansion': BusinessStage.SCALE,
            'mature': BusinessStage.MATURE
        }
        
        # Map industry
        industry_map = {
            'artificial_intelligence': IndustryType.DEEPTECH,
            'ai': IndustryType.DEEPTECH,
            'fintech': IndustryType.FINTECH,
            'ecommerce': IndustryType.ECOMMERCE,
            'saas': IndustryType.B2B_SAAS,
            'healthcare': IndustryType.HEALTHTECH,
            'technology': IndustryType.ENTERPRISE
        }
        
        # Map challenges
        challenge_map = {
            'scaling': ChallengeType.SCALING,
            'competition': ChallengeType.COMPETITION,
            'talent_acquisition': ChallengeType.TALENT_ACQUISITION,
            'product_development': ChallengeType.PRODUCT_MARKET_FIT,
            'funding': ChallengeType.FUNDRAISING,
            'market_expansion': ChallengeType.MARKET_PENETRATION
        }
        
        # Create context
        context = StartupContext(
            stage=stage_map.get(stage.lower(), BusinessStage.GROWTH),
            industry=industry_map.get(industry.lower(), IndustryType.TECHNOLOGY),
            size=team_size,
            primary_challenge=challenge_map.get(
                challenges[0].lower() if challenges else 'scaling',
                ChallengeType.SCALING
            ),
            budget_constraint='medium',
            time_constraint='medium',
            strategic_goals=challenges[:3] if challenges else ['growth']
        )
        
        # Create minimal assessment data
        assessment_data = {
            'company_name': company_name,
            'team_size': team_size,
            'industry': industry,
            'stage': stage
        }
        
        # Run async method in sync context safely
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                # We're already in an async context, use asyncio.create_task
                import nest_asyncio
                nest_asyncio.apply()
        except RuntimeError:
            # No event loop, create one
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        
        try:
            recommendations = loop.run_until_complete(
                self.selector.recommend_frameworks_enhanced(
                    context=context,
                    assessment_data=assessment_data,
                    max_recommendations=top_k
                )
            )
            
            # Convert to simple format
            simple_recs = []
            for rec in recommendations:
                framework = framework_database.get_framework_by_id(rec.framework_id)
                if framework:
                    simple_recs.append({
                        'id': rec.framework_id,
                        'name': framework.name,
                        'score': rec.relevance_score,
                        'reason': rec.ai_reasoning or rec.reasoning,
                        'category': framework.category.value if hasattr(framework.category, 'value') else str(framework.category),
                        'description': framework.description
                    })
            
            return simple_recs
            
        finally:
            # Only close if we created the loop
            try:
                if not loop.is_running():
                    loop.close()
            except:
                pass
    
    def get_framework_analysis(
        self,
        framework_id: str,
        company_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Get analysis for a specific framework"""
        
        framework = framework_database.get_framework_by_id(framework_id)
        if not framework:
            return {
                'error': f'Framework {framework_id} not found',
                'available_frameworks': list(framework_database.FRAMEWORKS.keys())[:10]
            }
        
        # Generate analysis based on framework data
        analysis = {
            'framework_id': framework_id,
            'framework_name': framework.name,
            'description': framework.description,
            'category': framework.category.value if hasattr(framework.category, 'value') else str(framework.category),
            'when_to_use': framework.when_to_use,
            'key_components': framework.key_components,
            'application_steps': framework.application_steps,
            'expected_outcomes': framework.expected_outcomes,
            'company_specific': {
                'relevance': f"Highly relevant for {company_data.get('company_name', 'your company')} given your {company_data.get('stage', 'growth')} stage",
                'priority_components': framework.key_components[:3] if framework.key_components else [],
                'quick_wins': framework.application_steps[:2] if framework.application_steps else [],
                'timeline': framework.time_to_implement or '4-8 weeks'
            }
        }
        
        return analysis

# Global instance
framework_system = FrameworkSystemWrapper()