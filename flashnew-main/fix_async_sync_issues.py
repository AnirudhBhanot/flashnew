#!/usr/bin/env python3
"""
Fix async/sync mismatch issues in framework system
"""

import os
import re

def fix_async_sync_issues():
    """Fix all async/sync mismatch issues"""
    
    fixes_applied = []
    
    # Fix 1: Update framework_wrapper.py to handle async better
    wrapper_file = "/Users/sf/Desktop/FLASH/framework_wrapper.py"
    
    print(f"Fixing {wrapper_file}...")
    
    with open(wrapper_file, 'r') as f:
        content = f.read()
    
    # Replace the problematic event loop creation
    old_pattern = '''        # Run async method in sync context
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            recommendations = loop.run_until_complete(
                self.selector.recommend_frameworks_enhanced(
                    context=context,
                    assessment_data=assessment_data,
                    max_recommendations=top_k
                )
            )'''
    
    new_pattern = '''        # Run async method in sync context safely
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
            )'''
    
    if old_pattern in content:
        content = content.replace(old_pattern, new_pattern)
        fixes_applied.append("Fixed event loop handling in recommend_frameworks_simple")
    
    # Add nest_asyncio import if not present
    if 'import nest_asyncio' not in content and 'nest_asyncio' in content:
        # Add import after asyncio import
        import_pos = content.find('import asyncio')
        if import_pos > -1:
            import_end = content.find('\n', import_pos)
            content = content[:import_end] + '\nimport nest_asyncio' + content[import_end:]
            fixes_applied.append("Added nest_asyncio import")
    
    # Fix the finally block
    old_finally = '''        finally:
            loop.close()'''
    
    new_finally = '''        finally:
            # Only close if we created the loop
            try:
                if not loop.is_running():
                    loop.close()
            except:
                pass'''
    
    if old_finally in content:
        content = content.replace(old_finally, new_finally)
        fixes_applied.append("Fixed loop.close() handling")
    
    # Write updated content
    with open(wrapper_file, 'w') as f:
        f.write(content)
    
    print(f"✅ Fixed {len(fixes_applied)} issues in framework_wrapper.py")
    
    # Fix 2: Create async wrapper version
    async_wrapper_content = '''"""
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
'''
    
    async_wrapper_file = "/Users/sf/Desktop/FLASH/framework_wrapper_async.py"
    with open(async_wrapper_file, 'w') as f:
        f.write(async_wrapper_content)
    
    print(f"✅ Created async wrapper: {async_wrapper_file}")
    
    # Fix 3: Update api_framework_intelligent.py to use async wrapper when appropriate
    intelligent_file = "/Users/sf/Desktop/FLASH/api_framework_intelligent.py"
    
    print(f"\nChecking {intelligent_file}...")
    
    with open(intelligent_file, 'r') as f:
        intelligent_content = f.read()
    
    # Check if it's using the sync wrapper in async context
    if 'framework_system.recommend_frameworks_simple(' in intelligent_content:
        print("⚠️  Found sync wrapper usage in async context")
        # Add import for async wrapper
        if 'from framework_wrapper_async import' not in intelligent_content:
            import_pos = intelligent_content.find('from framework_wrapper import')
            if import_pos > -1:
                import_end = intelligent_content.find('\n', import_pos)
                intelligent_content = intelligent_content[:import_end] + '\nfrom framework_wrapper_async import async_framework_system' + intelligent_content[import_end:]
                
                # Replace sync call with async call
                intelligent_content = intelligent_content.replace(
                    'framework_system.recommend_frameworks_simple(',
                    'await async_framework_system.recommend_frameworks_async('
                )
                
                with open(intelligent_file, 'w') as f:
                    f.write(intelligent_content)
                
                print("✅ Updated to use async wrapper")
    
    return fixes_applied

if __name__ == "__main__":
    fixed = fix_async_sync_issues()
    
    print(f"\n🎉 Async/sync fixes complete!")
    print("Improvements:")
    print("- Better event loop handling")
    print("- Created async wrapper for async contexts")
    print("- Fixed potential loop closing issues")