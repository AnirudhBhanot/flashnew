"""
Framework Intelligence Engine

A comprehensive system for intelligently selecting and recommending
business frameworks based on startup context and needs.
"""

from .framework_database import (
    Framework,
    FrameworkCategory,
    ComplexityLevel,
    get_framework_by_id,
    get_frameworks_by_category,
    get_frameworks_by_complexity,
    search_frameworks,
    get_complementary_frameworks,
    get_frameworks_for_industry,
    get_framework_statistics,
    FRAMEWORKS
)

from .framework_selector import (
    BusinessStage,
    IndustryType,
    ChallengeType,
    StartupContext,
    FrameworkRecommendation,
    FrameworkSelector,
    recommend_frameworks_for_startup,
    get_implementation_roadmap,
    get_framework_combinations,
    get_detailed_implementation_guide
)

__version__ = "1.0.0"
__author__ = "Framework Intelligence Engine"

__all__ = [
    # Database exports
    "Framework",
    "FrameworkCategory",
    "ComplexityLevel",
    "get_framework_by_id",
    "get_frameworks_by_category",
    "get_frameworks_by_complexity",
    "search_frameworks",
    "get_complementary_frameworks",
    "get_frameworks_for_industry",
    "get_framework_statistics",
    "FRAMEWORKS",
    
    # Selector exports
    "BusinessStage",
    "IndustryType",
    "ChallengeType",
    "StartupContext",
    "FrameworkRecommendation",
    "FrameworkSelector",
    "recommend_frameworks_for_startup",
    "get_implementation_roadmap",
    "get_framework_combinations",
    "get_detailed_implementation_guide"
]