"""
Async version of framework wrapper for use in async contexts
"""

from typing import Dict, Any, List
from framework_intelligence.enhanced_framework_selector import (
    EnhancedFrameworkSelector, StartupContext, BusinessStage, 
    IndustryType, ChallengeType
)
from framework_intelligence import framework_database

class AsyncFrameworkSystemWrapper:
    """Async wrapper for framework system"""
    
    def __init__(self):
        self.selector = EnhancedFrameworkSelector()
        
    async def recommend_frameworks_async(
        self,
        company_name: str,
        industry: str,
        stage: str,
        challenges: List[str],
        team_size: int = 20,
        top_k: int = 6
    ) -> List[Dict[str, Any]]:
        """Async version of framework recommendations"""
        
        # Map stage to BusinessStage enum
        stage_map = {
            'pre_seed': BusinessStage.IDEA,
            'pre-seed': BusinessStage.IDEA,
            'seed': BusinessStage.MVP,
            'series_a': BusinessStage.GROWTH,
            'series-a': BusinessStage.GROWTH,
            'series_b': BusinessStage.GROWTH,
            'series-b': BusinessStage.GROWTH,
            'series_c': BusinessStage.SCALE,
            'series-c': BusinessStage.SCALE,
            'idea': BusinessStage.IDEA,
            'mvp': BusinessStage.MVP,
            'product_market_fit': BusinessStage.PRODUCT_MARKET_FIT,
            'growth': BusinessStage.GROWTH,
            'scale': BusinessStage.SCALE,
            'mature': BusinessStage.MATURE,
            'startup': BusinessStage.MVP,
            'expansion': BusinessStage.SCALE
        }
        
        # Map industry
        industry_map = {
            'artificial_intelligence': IndustryType.DEEPTECH,
            'ai': IndustryType.DEEPTECH,
            'fintech': IndustryType.FINTECH,
            'ecommerce': IndustryType.ECOMMERCE,
            'saas': IndustryType.B2B_SAAS,
            'healthcare': IndustryType.HEALTHTECH,
            'technology': IndustryType.TECHNOLOGY
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
        
        # Get recommendations (already async)
        recommendations = await self.selector.recommend_frameworks_enhanced(
            context=context,
            assessment_data=assessment_data,
            max_recommendations=top_k
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

# Global async instance
async_framework_system = AsyncFrameworkSystemWrapper()
