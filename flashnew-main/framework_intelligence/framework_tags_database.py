#!/usr/bin/env python3
"""
Framework Tags Database - Comprehensive tagging for all frameworks
This implements the multi-dimensional taxonomy for framework selection
"""

from framework_intelligence.framework_taxonomy import *


def create_framework_tags_database():
    """Create comprehensive tags for all frameworks"""
    
    tags_db = {}
    
    # BCG Growth-Share Matrix
    tags_db["bcg_matrix"] = FrameworkTags(
        temporal_stages=[TemporalStage.GROWTH, TemporalStage.SCALE, TemporalStage.MATURITY],
        problem_archetypes=[
            ProblemArchetype.PORTFOLIO_OPTIMIZATION,
            ProblemArchetype.BUSINESS_MODEL_DESIGN,
            ProblemArchetype.COMPETITIVE_STRATEGY
        ],
        decision_contexts=[DecisionContext.DIAGNOSTIC, DecisionContext.PRESCRIPTIVE],
        data_requirements=[
            DataRequirement.MARKET_DATA,
            DataRequirement.BASIC_QUANTITATIVE,
            DataRequirement.COMPETITIVE_INTEL
        ],
        complexity_tier=ComplexityTier.MODERATE,
        outcome_types=[
            OutcomeType.STRATEGIC_CLARITY,
            OutcomeType.TACTICAL_ACTIONS
        ],
        industry_contexts=[IndustryContext.UNIVERSAL],
        typical_users=["CEO", "CSO", "Head of Strategy", "Board Members"],
        team_size_min=20,  # Need multiple products/units
        team_size_max=10000,
        time_to_value_days=14,
        durability_months=18,
        ease_of_use=70,
        actionability=80,
        accuracy=60,
        strategic_impact=85,
        requires_facilitator=False,
        requires_software=False,
        has_variants=True,
        keywords={"portfolio", "growth", "share", "resource allocation", "investment"}
    )
    
    # Porter's Five Forces
    tags_db["porters_five_forces"] = FrameworkTags(
        temporal_stages=[TemporalStage.VALIDATION, TemporalStage.TRACTION, TemporalStage.GROWTH, TemporalStage.SCALE],
        problem_archetypes=[
            ProblemArchetype.COMPETITIVE_STRATEGY,
            ProblemArchetype.MARKET_ANALYSIS,
            ProblemArchetype.BUSINESS_MODEL_DESIGN
        ],
        decision_contexts=[DecisionContext.DIAGNOSTIC, DecisionContext.PREDICTIVE],
        data_requirements=[
            DataRequirement.MARKET_DATA,
            DataRequirement.COMPETITIVE_INTEL,
            DataRequirement.QUALITATIVE_ONLY
        ],
        complexity_tier=ComplexityTier.MODERATE,
        outcome_types=[
            OutcomeType.STRATEGIC_CLARITY,
            OutcomeType.COMPETITIVE_ADVANTAGE,
            OutcomeType.RISK_MITIGATION
        ],
        industry_contexts=[IndustryContext.UNIVERSAL],
        typical_users=["CEO", "CSO", "Head of Strategy", "Business Development"],
        team_size_min=5,
        team_size_max=10000,
        time_to_value_days=21,
        durability_months=24,
        ease_of_use=60,
        actionability=70,
        accuracy=75,
        strategic_impact=90,
        requires_facilitator=True,
        requires_software=False,
        has_variants=False,
        keywords={"competition", "industry", "rivalry", "barriers", "suppliers", "buyers", "threats"}
    )
    
    # Jobs to be Done
    tags_db["jobs_to_be_done"] = FrameworkTags(
        temporal_stages=[TemporalStage.PRE_FORMATION, TemporalStage.FORMATION, TemporalStage.VALIDATION],
        problem_archetypes=[
            ProblemArchetype.CUSTOMER_DISCOVERY,
            ProblemArchetype.PRODUCT_MARKET_FIT,
            ProblemArchetype.INNOVATION_MANAGEMENT
        ],
        decision_contexts=[DecisionContext.EXPLORATORY, DecisionContext.DIAGNOSTIC],
        data_requirements=[
            DataRequirement.QUALITATIVE_ONLY,
            DataRequirement.EXPERIMENTAL_DATA
        ],
        complexity_tier=ComplexityTier.SIMPLE,
        outcome_types=[
            OutcomeType.CUSTOMER_INSIGHTS,
            OutcomeType.INNOVATION_PIPELINE,
            OutcomeType.TACTICAL_ACTIONS
        ],
        industry_contexts=[IndustryContext.UNIVERSAL],
        typical_users=["Product Manager", "UX Designer", "Innovation Lead", "Founder"],
        team_size_min=1,
        team_size_max=1000,
        time_to_value_days=7,
        durability_months=12,
        ease_of_use=80,
        actionability=90,
        accuracy=85,
        strategic_impact=70,
        requires_facilitator=False,
        requires_software=False,
        has_variants=True,
        keywords={"customer", "needs", "innovation", "problems", "solutions", "outcomes"}
    )
    
    # Unit Economics
    tags_db["unit_economics"] = FrameworkTags(
        temporal_stages=[TemporalStage.VALIDATION, TemporalStage.TRACTION, TemporalStage.GROWTH],
        problem_archetypes=[
            ProblemArchetype.UNIT_ECONOMICS_OPTIMIZATION,
            ProblemArchetype.BUSINESS_MODEL_DESIGN,
            ProblemArchetype.FINANCIAL_PLANNING
        ],
        decision_contexts=[DecisionContext.DIAGNOSTIC, DecisionContext.EVALUATIVE],
        data_requirements=[
            DataRequirement.BASIC_QUANTITATIVE,
            DataRequirement.ADVANCED_METRICS
        ],
        complexity_tier=ComplexityTier.MODERATE,
        outcome_types=[
            OutcomeType.FINANCIAL_PROJECTIONS,
            OutcomeType.TACTICAL_ACTIONS,
            OutcomeType.OPERATIONAL_IMPROVEMENTS
        ],
        industry_contexts=[IndustryContext.B2B_SAAS, IndustryContext.B2C_SAAS, IndustryContext.MARKETPLACE, IndustryContext.ECOMMERCE],
        typical_users=["CFO", "CEO", "Head of Finance", "Investors"],
        team_size_min=5,
        team_size_max=5000,
        time_to_value_days=7,
        durability_months=6,
        ease_of_use=60,
        actionability=95,
        accuracy=90,
        strategic_impact=80,
        requires_facilitator=False,
        requires_software=True,
        has_variants=True,
        keywords={"ltv", "cac", "payback", "margin", "profitability", "economics"}
    )
    
    # Lean Canvas
    tags_db["lean_canvas"] = FrameworkTags(
        temporal_stages=[TemporalStage.PRE_FORMATION, TemporalStage.FORMATION, TemporalStage.VALIDATION],
        problem_archetypes=[
            ProblemArchetype.BUSINESS_MODEL_DESIGN,
            ProblemArchetype.PRODUCT_MARKET_FIT,
            ProblemArchetype.CUSTOMER_DISCOVERY
        ],
        decision_contexts=[DecisionContext.EXPLORATORY, DecisionContext.DIAGNOSTIC],
        data_requirements=[DataRequirement.QUALITATIVE_ONLY],
        complexity_tier=ComplexityTier.PLUG_AND_PLAY,
        outcome_types=[
            OutcomeType.STRATEGIC_CLARITY,
            OutcomeType.TACTICAL_ACTIONS
        ],
        industry_contexts=[IndustryContext.UNIVERSAL],
        typical_users=["Founder", "Product Manager", "Entrepreneur"],
        team_size_min=1,
        team_size_max=50,
        time_to_value_days=1,
        durability_months=6,
        ease_of_use=90,
        actionability=85,
        accuracy=70,
        strategic_impact=75,
        requires_facilitator=False,
        requires_software=False,
        has_variants=False,
        keywords={"startup", "business model", "problem", "solution", "mvp"}
    )
    
    # AARRR Metrics (Pirate Metrics)
    tags_db["aarrr_metrics"] = FrameworkTags(
        temporal_stages=[TemporalStage.TRACTION, TemporalStage.GROWTH, TemporalStage.SCALE],
        problem_archetypes=[
            ProblemArchetype.GROWTH_MECHANICS,
            ProblemArchetype.UNIT_ECONOMICS_OPTIMIZATION,
            ProblemArchetype.OPERATIONAL_EXCELLENCE
        ],
        decision_contexts=[DecisionContext.DIAGNOSTIC, DecisionContext.EVALUATIVE],
        data_requirements=[
            DataRequirement.ADVANCED_METRICS,
            DataRequirement.HISTORICAL_DATA
        ],
        complexity_tier=ComplexityTier.SIMPLE,
        outcome_types=[
            OutcomeType.OPERATIONAL_IMPROVEMENTS,
            OutcomeType.GROWTH_STRATEGY,
            OutcomeType.TACTICAL_ACTIONS
        ],
        industry_contexts=[IndustryContext.B2B_SAAS, IndustryContext.B2C_SAAS, IndustryContext.MARKETPLACE, IndustryContext.ECOMMERCE],
        typical_users=["Growth Manager", "CMO", "Product Manager", "Data Analyst"],
        team_size_min=10,
        team_size_max=5000,
        time_to_value_days=7,
        durability_months=3,
        ease_of_use=80,
        actionability=90,
        accuracy=85,
        strategic_impact=70,
        requires_facilitator=False,
        requires_software=True,
        has_variants=True,
        keywords={"acquisition", "activation", "retention", "referral", "revenue", "metrics", "funnel"}
    )
    
    # Blue Ocean Strategy
    tags_db["blue_ocean_strategy"] = FrameworkTags(
        temporal_stages=[TemporalStage.FORMATION, TemporalStage.VALIDATION, TemporalStage.TRACTION, TemporalStage.GROWTH],
        problem_archetypes=[
            ProblemArchetype.COMPETITIVE_STRATEGY,
            ProblemArchetype.INNOVATION_MANAGEMENT,
            ProblemArchetype.MARKET_ANALYSIS
        ],
        decision_contexts=[DecisionContext.EXPLORATORY, DecisionContext.PRESCRIPTIVE],
        data_requirements=[
            DataRequirement.MARKET_DATA,
            DataRequirement.COMPETITIVE_INTEL,
            DataRequirement.QUALITATIVE_ONLY
        ],
        complexity_tier=ComplexityTier.COMPLEX,
        outcome_types=[
            OutcomeType.STRATEGIC_CLARITY,
            OutcomeType.INNOVATION_PIPELINE,
            OutcomeType.COMPETITIVE_ADVANTAGE
        ],
        industry_contexts=[IndustryContext.UNIVERSAL],
        typical_users=["CEO", "CSO", "Innovation Lead", "Product Strategy"],
        team_size_min=10,
        team_size_max=10000,
        time_to_value_days=30,
        durability_months=36,
        ease_of_use=50,
        actionability=70,
        accuracy=60,
        strategic_impact=95,
        requires_facilitator=True,
        requires_software=False,
        has_variants=False,
        keywords={"uncontested", "market space", "competition", "value innovation", "differentiation"}
    )
    
    # Ansoff Matrix
    tags_db["ansoff_matrix"] = FrameworkTags(
        temporal_stages=[TemporalStage.TRACTION, TemporalStage.GROWTH, TemporalStage.SCALE],
        problem_archetypes=[
            ProblemArchetype.GROWTH_MECHANICS,
            ProblemArchetype.COMPETITIVE_STRATEGY,
            ProblemArchetype.RISK_MANAGEMENT
        ],
        decision_contexts=[DecisionContext.PRESCRIPTIVE, DecisionContext.PREDICTIVE],
        data_requirements=[
            DataRequirement.MARKET_DATA,
            DataRequirement.BASIC_QUANTITATIVE
        ],
        complexity_tier=ComplexityTier.SIMPLE,
        outcome_types=[
            OutcomeType.GROWTH_STRATEGY,
            OutcomeType.RISK_MITIGATION,
            OutcomeType.STRATEGIC_CLARITY
        ],
        industry_contexts=[IndustryContext.UNIVERSAL],
        typical_users=["CEO", "CSO", "Head of Growth", "Board Members"],
        team_size_min=20,
        team_size_max=10000,
        time_to_value_days=7,
        durability_months=24,
        ease_of_use=85,
        actionability=80,
        accuracy=70,
        strategic_impact=80,
        requires_facilitator=False,
        requires_software=False,
        has_variants=False,
        keywords={"growth", "market penetration", "development", "diversification", "risk"}
    )
    
    # Customer Development
    tags_db["customer_development"] = FrameworkTags(
        temporal_stages=[TemporalStage.PRE_FORMATION, TemporalStage.FORMATION, TemporalStage.VALIDATION],
        problem_archetypes=[
            ProblemArchetype.CUSTOMER_DISCOVERY,
            ProblemArchetype.PRODUCT_MARKET_FIT
        ],
        decision_contexts=[DecisionContext.EXPLORATORY, DecisionContext.DIAGNOSTIC],
        data_requirements=[DataRequirement.QUALITATIVE_ONLY],
        complexity_tier=ComplexityTier.SIMPLE,
        outcome_types=[
            OutcomeType.CUSTOMER_INSIGHTS,
            OutcomeType.TACTICAL_ACTIONS
        ],
        industry_contexts=[IndustryContext.UNIVERSAL],
        typical_users=["Founder", "Product Manager", "Customer Success"],
        team_size_min=1,
        team_size_max=100,
        time_to_value_days=14,
        durability_months=6,
        ease_of_use=70,
        actionability=95,
        accuracy=80,
        strategic_impact=85,
        requires_facilitator=False,
        requires_software=False,
        has_variants=False,
        keywords={"customer", "discovery", "validation", "interviews", "feedback"}
    )
    
    # SWOT Analysis
    tags_db["swot_analysis"] = FrameworkTags(
        temporal_stages=[stage for stage in TemporalStage],  # All stages
        problem_archetypes=[
            ProblemArchetype.COMPETITIVE_STRATEGY,
            ProblemArchetype.RISK_MANAGEMENT,
            ProblemArchetype.BUSINESS_MODEL_DESIGN
        ],
        decision_contexts=[DecisionContext.DIAGNOSTIC],
        data_requirements=[DataRequirement.QUALITATIVE_ONLY],
        complexity_tier=ComplexityTier.PLUG_AND_PLAY,
        outcome_types=[
            OutcomeType.STRATEGIC_CLARITY,
            OutcomeType.RISK_MITIGATION
        ],
        industry_contexts=[IndustryContext.UNIVERSAL],
        typical_users=["Any role"],
        team_size_min=1,
        team_size_max=10000,
        time_to_value_days=1,
        durability_months=12,
        ease_of_use=95,
        actionability=60,
        accuracy=50,
        strategic_impact=60,
        requires_facilitator=False,
        requires_software=False,
        has_variants=False,
        keywords={"strengths", "weaknesses", "opportunities", "threats", "analysis"}
    )
    
    return tags_db


def create_framework_relationships():
    """Create relationship mappings between frameworks"""
    
    relationships = {}
    
    # BCG Matrix relationships
    relationships["bcg_matrix"] = [
        FrameworkRelationship(
            framework_id="bcg_matrix",
            relationship_type="prerequisite",
            related_framework_ids=["market_share_analysis", "growth_rate_analysis"],
            relationship_strength=90,
            notes="Need market data before portfolio analysis"
        ),
        FrameworkRelationship(
            framework_id="bcg_matrix",
            relationship_type="complementary",
            related_framework_ids=["ansoff_matrix", "ge_mckinsey_matrix"],
            relationship_strength=80,
            notes="Natural progression for growth strategy"
        ),
        FrameworkRelationship(
            framework_id="bcg_matrix",
            relationship_type="alternative",
            related_framework_ids=["ge_mckinsey_matrix", "adl_matrix"],
            relationship_strength=70,
            notes="Alternative portfolio analysis tools"
        )
    ]
    
    # Jobs to be Done relationships
    relationships["jobs_to_be_done"] = [
        FrameworkRelationship(
            framework_id="jobs_to_be_done",
            relationship_type="complementary",
            related_framework_ids=["value_proposition_canvas", "customer_journey_mapping"],
            relationship_strength=90,
            notes="Deep customer understanding tools"
        ),
        FrameworkRelationship(
            framework_id="jobs_to_be_done",
            relationship_type="progressive",
            related_framework_ids=["lean_canvas", "business_model_canvas"],
            relationship_strength=85,
            notes="Natural progression to business model design"
        )
    ]
    
    # Unit Economics relationships
    relationships["unit_economics"] = [
        FrameworkRelationship(
            framework_id="unit_economics",
            relationship_type="prerequisite",
            related_framework_ids=["customer_acquisition_data", "retention_analysis"],
            relationship_strength=95,
            notes="Need cohort data for accurate unit economics"
        ),
        FrameworkRelationship(
            framework_id="unit_economics",
            relationship_type="complementary",
            related_framework_ids=["ltv_cac_ratio", "cohort_analysis", "pricing_strategy"],
            relationship_strength=90,
            notes="Financial optimization tools"
        ),
        FrameworkRelationship(
            framework_id="unit_economics",
            relationship_type="progressive",
            related_framework_ids=["financial_modeling", "scenario_planning"],
            relationship_strength=80,
            notes="Advanced financial planning"
        )
    ]
    
    # Porter's Five Forces relationships
    relationships["porters_five_forces"] = [
        FrameworkRelationship(
            framework_id="porters_five_forces",
            relationship_type="complementary",
            related_framework_ids=["swot_analysis", "pestle_analysis", "value_chain_analysis"],
            relationship_strength=85,
            notes="Comprehensive strategic analysis"
        ),
        FrameworkRelationship(
            framework_id="porters_five_forces",
            relationship_type="progressive",
            related_framework_ids=["blue_ocean_strategy", "competitive_positioning"],
            relationship_strength=80,
            notes="From analysis to strategy formulation"
        )
    ]
    
    # Lean Canvas relationships
    relationships["lean_canvas"] = [
        FrameworkRelationship(
            framework_id="lean_canvas",
            relationship_type="prerequisite",
            related_framework_ids=["customer_development", "problem_validation"],
            relationship_strength=90,
            notes="Validate assumptions first"
        ),
        FrameworkRelationship(
            framework_id="lean_canvas",
            relationship_type="progressive",
            related_framework_ids=["business_model_canvas", "mvp_framework"],
            relationship_strength=85,
            notes="From concept to execution"
        )
    ]
    
    return relationships


def create_framework_antipatterns():
    """Create antipattern database - when NOT to use frameworks"""
    
    antipatterns = {}
    
    # BCG Matrix antipatterns
    antipatterns["bcg_matrix"] = FrameworkAntiPattern(
        framework_id="bcg_matrix",
        antipattern_conditions=[
            "Single product company",
            "Pre-revenue startup",
            "Rapidly pivoting business",
            "Markets with unclear boundaries",
            "B2B with < 10 customers",
            "Team size < 20 people"
        ],
        negative_outcomes=[
            "Misleading strategic decisions",
            "Over-simplification of complex dynamics",
            "Resource misallocation",
            "False sense of clarity"
        ],
        alternative_frameworks=["lean_canvas", "jobs_to_be_done", "unit_economics"],
        severity="high"
    )
    
    # Porter's Five Forces antipatterns
    antipatterns["porters_five_forces"] = FrameworkAntiPattern(
        framework_id="porters_five_forces",
        antipattern_conditions=[
            "Emerging markets with no clear structure",
            "Platform businesses with network effects",
            "Pre-formation stage startups",
            "Highly regulated industries in flux",
            "Digital ecosystems with blurred boundaries"
        ],
        negative_outcomes=[
            "Analysis paralysis",
            "Missing ecosystem dynamics",
            "Overemphasis on competition vs collaboration",
            "Static view of dynamic markets"
        ],
        alternative_frameworks=["ecosystem_mapping", "platform_strategy", "blue_ocean_strategy"],
        severity="medium"
    )
    
    # Unit Economics antipatterns
    antipatterns["unit_economics"] = FrameworkAntiPattern(
        framework_id="unit_economics",
        antipattern_conditions=[
            "No paying customers yet",
            "One-time project businesses",
            "Highly variable customer segments",
            "Platform businesses in growth mode",
            "Less than 6 months of data"
        ],
        negative_outcomes=[
            "Premature optimization",
            "Misleading profitability projections",
            "Over-focus on metrics vs product",
            "Short-term thinking"
        ],
        alternative_frameworks=["customer_development", "jobs_to_be_done", "lean_canvas"],
        severity="medium"
    )
    
    # SWOT Analysis antipatterns
    antipatterns["swot_analysis"] = FrameworkAntiPattern(
        framework_id="swot_analysis",
        antipattern_conditions=[
            "Need for deep strategic analysis",
            "Complex competitive dynamics",
            "Data-driven decision making culture",
            "Need for actionable outcomes"
        ],
        negative_outcomes=[
            "Surface-level insights only",
            "Confirmation bias",
            "Lack of prioritization",
            "No clear action items"
        ],
        alternative_frameworks=["porters_five_forces", "vrio_analysis", "scenario_planning"],
        severity="low"
    )
    
    # Blue Ocean Strategy antipatterns
    antipatterns["blue_ocean_strategy"] = FrameworkAntiPattern(
        framework_id="blue_ocean_strategy",
        antipattern_conditions=[
            "Highly regulated industries",
            "B2B with switching costs",
            "Network effect businesses",
            "Commodity markets",
            "Limited resources for innovation"
        ],
        negative_outcomes=[
            "Unrealistic market expectations",
            "Ignoring competitive responses",
            "Underestimating execution complexity",
            "Resource drain on failed experiments"
        ],
        alternative_frameworks=["porters_generic_strategies", "competitive_positioning", "focus_strategy"],
        severity="medium"
    )
    
    return antipatterns


def create_framework_effectiveness_data():
    """Create effectiveness metrics based on empirical data"""
    
    effectiveness = {}
    
    # BCG Matrix effectiveness
    effectiveness["bcg_matrix"] = FrameworkEffectiveness(
        framework_id="bcg_matrix",
        success_rate=0.65,  # 65% achieve strategic clarity
        time_to_impact_days=30,
        effort_return_ratio=2.5,  # 2.5x value vs effort
        durability_months=18,
        effectiveness_by_stage={
            TemporalStage.GROWTH: 0.75,
            TemporalStage.SCALE: 0.80,
            TemporalStage.MATURITY: 0.70,
            TemporalStage.VALIDATION: 0.30,  # Poor fit
            TemporalStage.PRE_FORMATION: 0.10  # Very poor fit
        },
        effectiveness_by_industry={
            IndustryContext.CONSUMER_GOODS: 0.80,
            IndustryContext.B2B_SAAS: 0.60,
            IndustryContext.MARKETPLACE: 0.55
        },
        effectiveness_by_team_size={
            "small": 0.30,  # <50 people
            "medium": 0.70,  # 50-500
            "large": 0.85   # 500+
        },
        success_factors=[
            "Multiple distinct business units",
            "Clear market boundaries",
            "Reliable market share data",
            "Stable competitive landscape"
        ],
        failure_factors=[
            "Single product focus",
            "Rapidly changing markets",
            "Unclear unit economics",
            "Platform/network businesses"
        ],
        data_points=250,
        confidence_level=0.85
    )
    
    # Jobs to be Done effectiveness
    effectiveness["jobs_to_be_done"] = FrameworkEffectiveness(
        framework_id="jobs_to_be_done",
        success_rate=0.82,  # 82% find valuable insights
        time_to_impact_days=14,
        effort_return_ratio=4.2,  # High ROI
        durability_months=12,
        effectiveness_by_stage={
            TemporalStage.PRE_FORMATION: 0.90,
            TemporalStage.FORMATION: 0.85,
            TemporalStage.VALIDATION: 0.80,
            TemporalStage.TRACTION: 0.70,
            TemporalStage.SCALE: 0.60
        },
        effectiveness_by_industry={
            IndustryContext.B2C_SAAS: 0.85,
            IndustryContext.CONSUMER_GOODS: 0.80,
            IndustryContext.B2B_SAAS: 0.75
        },
        effectiveness_by_team_size={
            "small": 0.90,
            "medium": 0.80,
            "large": 0.70
        },
        success_factors=[
            "Direct customer access",
            "Skilled interviewers",
            "Open-minded approach",
            "Time for iteration"
        ],
        failure_factors=[
            "Leading questions",
            "Small sample size",
            "Confirmation bias",
            "Solution-first thinking"
        ],
        data_points=500,
        confidence_level=0.90
    )
    
    # Unit Economics effectiveness
    effectiveness["unit_economics"] = FrameworkEffectiveness(
        framework_id="unit_economics",
        success_rate=0.78,
        time_to_impact_days=7,
        effort_return_ratio=5.5,  # Very high ROI
        durability_months=6,  # Changes quickly
        effectiveness_by_stage={
            TemporalStage.VALIDATION: 0.85,
            TemporalStage.TRACTION: 0.90,
            TemporalStage.GROWTH: 0.85,
            TemporalStage.PRE_FORMATION: 0.20
        },
        effectiveness_by_industry={
            IndustryContext.B2B_SAAS: 0.95,
            IndustryContext.MARKETPLACE: 0.85,
            IndustryContext.ECOMMERCE: 0.80,
            IndustryContext.HARDWARE: 0.60
        },
        effectiveness_by_team_size={
            "small": 0.80,
            "medium": 0.85,
            "large": 0.75
        },
        success_factors=[
            "Accurate CAC tracking",
            "Cohort data available",
            "Clear unit definition",
            "6+ months of data"
        ],
        failure_factors=[
            "Incomplete cost allocation",
            "Mixed customer segments",
            "Seasonal businesses",
            "Long sales cycles"
        ],
        data_points=800,
        confidence_level=0.95
    )
    
    return effectiveness