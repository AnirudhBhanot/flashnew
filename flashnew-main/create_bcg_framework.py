#!/usr/bin/env python3
"""
Add BCG Matrix to framework database
"""

import sys
sys.path.insert(0, '/Users/sf/Desktop/FLASH')

from framework_intelligence.framework_database import Framework, FrameworkCategory, ComplexityLevel, FRAMEWORKS

# Define BCG Matrix framework
bcg_matrix = Framework(
    id="bcg_matrix",
    name="BCG Growth-Share Matrix",
    description="Strategic portfolio management tool that classifies business units based on market growth and relative market share",
    category=FrameworkCategory.STRATEGY,
    subcategory="Portfolio Management",
    when_to_use=[
        "Evaluating product/business portfolio",
        "Resource allocation decisions",
        "Strategic positioning analysis",
        "Growth strategy planning",
        "Investment prioritization"
    ],
    key_components=[
        "Market Growth Rate (vertical axis)",
        "Relative Market Share (horizontal axis)",
        "Four Quadrants: Stars, Cash Cows, Question Marks, Dogs",
        "Strategic implications for each quadrant"
    ],
    application_steps=[
        "Calculate market growth rate for each business unit/product",
        "Determine relative market share (your share / largest competitor's share)",
        "Plot each unit on the matrix",
        "Classify into quadrants",
        "Develop strategies for each quadrant",
        "Allocate resources based on classification"
    ],
    expected_outcomes=[
        "Clear portfolio visualization",
        "Resource allocation strategy",
        "Investment priorities",
        "Divestment candidates identified"
    ],
    complexity=ComplexityLevel.BASIC,
    industry_relevance=["all"],
    prerequisites=["Market share data", "Growth rate data", "Competitive intelligence"],
    complementary_frameworks=["ansoff_matrix", "porters_generic_strategies", "ge_mckinsey_matrix"],
    time_to_implement="1-2 weeks",
    resources_required=["Market data", "Financial data", "Competitive analysis"],
    common_pitfalls=[
        "Over-simplifying complex businesses",
        "Ignoring synergies between units",
        "Using only historical data"
    ],
    success_metrics=[
        "Portfolio balance",
        "ROI by quadrant",
        "Resource allocation efficiency"
    ]
)

# Add to FRAMEWORKS
FRAMEWORKS["bcg_matrix"] = bcg_matrix

# Verify it was added
if "bcg_matrix" in FRAMEWORKS:
    print("✓ BCG Matrix successfully added to framework database")
    print(f"  Name: {FRAMEWORKS['bcg_matrix'].name}")
    print(f"  Category: {FRAMEWORKS['bcg_matrix'].category.value}")
    print(f"  Industry Relevance: {FRAMEWORKS['bcg_matrix'].industry_relevance}")
else:
    print("✗ Failed to add BCG Matrix")

# Also add Porter's Five Forces if missing
if "porters_five_forces" not in FRAMEWORKS:
    porters = Framework(
        id="porters_five_forces",
        name="Porter's Five Forces",
        description="Industry analysis framework that examines competitive forces shaping an industry",
        category=FrameworkCategory.STRATEGY,
        subcategory="Competitive Analysis",
        when_to_use=[
            "Industry attractiveness analysis",
            "Competitive strategy development",
            "Market entry decisions",
            "Investment evaluation"
        ],
        key_components=[
            "Competitive Rivalry",
            "Threat of New Entrants",
            "Bargaining Power of Suppliers",
            "Bargaining Power of Buyers",
            "Threat of Substitutes"
        ],
        application_steps=[
            "Identify key players in each force",
            "Assess strength of each force (Low/Medium/High)",
            "Analyze collective impact on profitability",
            "Identify strategic opportunities and threats",
            "Develop strategies to improve position"
        ],
        expected_outcomes=[
            "Industry attractiveness assessment",
            "Competitive positioning insights",
            "Strategic opportunities identified",
            "Risk factors understood"
        ],
        complexity=ComplexityLevel.INTERMEDIATE,
        industry_relevance=["all"],
        prerequisites=["Industry knowledge", "Competitive data"],
        complementary_frameworks=["swot_analysis", "vrio_framework", "pestle_analysis"],
        time_to_implement="2-3 weeks",
        resources_required=["Industry research", "Competitive intelligence", "Market data"],
        success_metrics=[
            "Profit margin trends",
            "Market share stability",
            "Competitive advantages sustained"
        ]
    )
    FRAMEWORKS["porters_five_forces"] = porters
    print("\n✓ Porter's Five Forces also added")

print(f"\nTotal frameworks in database: {len(FRAMEWORKS)}")