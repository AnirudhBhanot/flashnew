#!/usr/bin/env python3
"""
Test why BCG Matrix isn't being selected for Series A companies
"""

import asyncio
import logging
from framework_intelligence.framework_selection_engine import AdvancedFrameworkSelector, CompanyContext
from framework_intelligence.framework_taxonomy import *
from framework_intelligence.framework_tags_database import create_framework_tags_database

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_bcg_selection():
    """Test BCG Matrix selection for Series A company"""
    
    # Create selector
    selector = AdvancedFrameworkSelector()
    
    # Create Series A context
    context = CompanyContext(
        company_name="SeriesATest",
        industry=IndustryContext.B2B_SAAS,
        stage=TemporalStage.GROWTH,  # Series A = Growth stage
        team_size=25,  # Above BCG minimum of 20
        primary_problems=[
            ProblemArchetype.COMPETITIVE_STRATEGY,
            ProblemArchetype.PORTFOLIO_OPTIMIZATION,
            ProblemArchetype.GROWTH_MECHANICS
        ],
        available_data=[
            DataRequirement.MARKET_DATA,
            DataRequirement.BASIC_QUANTITATIVE,
            DataRequirement.COMPETITIVE_INTEL
        ],
        revenue_usd=5000000,  # $5M ARR
        growth_rate_percent=150,
        burn_rate_usd=500000,
        runway_months=12,
        is_crisis_mode=False,
        is_fundraising=True
    )
    
    # Get recommendations
    recommendations = selector.select_frameworks(context, max_recommendations=5)
    
    # Log results
    logger.info(f"\nContext: {context.company_name}")
    logger.info(f"Stage: {context.stage.value}")
    logger.info(f"Team Size: {context.team_size}")
    logger.info(f"Problems: {[p.value for p in context.primary_problems]}")
    
    logger.info("\nRecommended Frameworks:")
    for i, rec in enumerate(recommendations, 1):
        logger.info(f"{i}. {rec.framework_id}")
        logger.info(f"   Fit Score: {rec.fit_score:.1f}")
        logger.info(f"   Rationale: {rec.rationale}")
        logger.info(f"   Stage Fit: {rec.stage_fit}")
        logger.info(f"   Problem Fit: {rec.problem_fit}")
        logger.info(f"   Team Fit: {rec.team_fit}")
    
    # Check if BCG Matrix was considered
    bcg_score = selector._score_framework("bcg_matrix", context)
    logger.info(f"\nBCG Matrix Analysis:")
    logger.info(f"Fit Score: {bcg_score.fit_score:.1f}")
    logger.info(f"Stage Fit: {bcg_score.stage_fit}")
    logger.info(f"Problem Fit: {bcg_score.problem_fit}")
    logger.info(f"Team Fit: {bcg_score.team_fit}")
    logger.info(f"Rationale: {bcg_score.rationale}")
    logger.info(f"Risks: {bcg_score.risks}")
    
    # Check tags
    tags_db = create_framework_tags_database()
    bcg_tags = tags_db.get("bcg_matrix")
    if bcg_tags:
        logger.info(f"\nBCG Matrix Tags:")
        logger.info(f"Stages: {[s.value for s in bcg_tags.temporal_stages]}")
        logger.info(f"Problems: {[p.value for p in bcg_tags.problem_archetypes]}")
        logger.info(f"Team Size: {bcg_tags.team_size_min} - {bcg_tags.team_size_max}")

if __name__ == "__main__":
    asyncio.run(test_bcg_selection())