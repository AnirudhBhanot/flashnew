#!/usr/bin/env python3
"""
Test the advanced framework selection system
Validates all phases of implementation
"""

import json
from datetime import datetime
from framework_taxonomy import *
from framework_selection_engine import *
from industry_framework_variants import *


def test_basic_selection():
    """Test basic framework selection"""
    print("=" * 80)
    print("TEST 1: Basic Framework Selection")
    print("=" * 80)
    
    # Create a pre-seed SaaS company context
    context = CompanyContext(
        company_name="TestStartup",
        industry=IndustryContext.B2B_SAAS,
        stage=TemporalStage.VALIDATION,
        team_size=8,
        primary_problems=[
            ProblemArchetype.PRODUCT_MARKET_FIT,
            ProblemArchetype.CUSTOMER_DISCOVERY,
            ProblemArchetype.UNIT_ECONOMICS_OPTIMIZATION
        ],
        available_data=[
            DataRequirement.QUALITATIVE_ONLY,
            DataRequirement.BASIC_QUANTITATIVE
        ],
        timeline_days=60,
        revenue_usd=50000,
        growth_rate_percent=20,
        burn_rate_usd=100000,
        runway_months=12
    )
    
    # Initialize selector
    selector = AdvancedFrameworkSelector()
    
    # Get recommendations
    recommendations = selector.select_frameworks(context, max_recommendations=5)
    
    print(f"\nCompany: {context.company_name}")
    print(f"Industry: {context.industry.value}")
    print(f"Stage: {context.stage.value}")
    print(f"Primary Challenges: {[p.value for p in context.primary_problems]}")
    
    print("\n📊 Recommended Frameworks:")
    for i, rec in enumerate(recommendations, 1):
        print(f"\n{i}. {rec.framework_id.replace('_', ' ').title()}")
        print(f"   Fit Score: {rec.fit_score:.1f}/100")
        print(f"   Stage Fit: {rec.stage_fit:.0f}%")
        print(f"   Problem Fit: {rec.problem_fit:.0f}%")
        print(f"   Data Fit: {rec.data_fit:.0f}%")
        print(f"   Time to Value: {rec.estimated_days} days")
        print(f"   Rationale: {', '.join(rec.rationale[:2])}")
    
    return recommendations


def test_crisis_mode_selection():
    """Test selection in crisis mode"""
    print("\n" + "=" * 80)
    print("TEST 2: Crisis Mode Selection (Low Runway)")
    print("=" * 80)
    
    context = CompanyContext(
        company_name="CrisisStartup",
        industry=IndustryContext.B2B_SAAS,
        stage=TemporalStage.TRACTION,
        team_size=15,
        primary_problems=[
            ProblemArchetype.UNIT_ECONOMICS_OPTIMIZATION,
            ProblemArchetype.GROWTH_MECHANICS
        ],
        available_data=[
            DataRequirement.BASIC_QUANTITATIVE,
            DataRequirement.ADVANCED_METRICS
        ],
        timeline_days=30,
        revenue_usd=100000,
        burn_rate_usd=150000,
        runway_months=3,  # Crisis!
        is_crisis_mode=True
    )
    
    selector = AdvancedFrameworkSelector()
    recommendations = selector.select_frameworks(context, max_recommendations=3)
    
    print(f"\n🚨 Crisis Context: {context.runway_months} months runway")
    print("\nRecommended Frameworks (prioritizing speed):")
    
    for i, rec in enumerate(recommendations, 1):
        print(f"\n{i}. {rec.framework_id.replace('_', ' ').title()}")
        print(f"   Urgency Score: {rec.urgency_score:.0f}/100")
        print(f"   Time to Value: {rec.estimated_days} days")
        print(f"   Expected Outcomes: {', '.join(rec.expected_outcomes[:2])}")


def test_framework_journey():
    """Test multi-phase framework journey"""
    print("\n" + "=" * 80)
    print("TEST 3: Framework Journey Planning")
    print("=" * 80)
    
    context = CompanyContext(
        company_name="GrowthCo",
        industry=IndustryContext.MARKETPLACE,
        stage=TemporalStage.GROWTH,
        team_size=50,
        primary_problems=[
            ProblemArchetype.COMPETITIVE_STRATEGY,
            ProblemArchetype.GROWTH_MECHANICS,
            ProblemArchetype.OPERATIONAL_EXCELLENCE
        ],
        available_data=[
            DataRequirement.ADVANCED_METRICS,
            DataRequirement.MARKET_DATA,
            DataRequirement.COMPETITIVE_INTEL
        ],
        revenue_usd=5000000,
        growth_rate_percent=150
    )
    
    selector = AdvancedFrameworkSelector()
    journey = selector.create_framework_journey(context, planning_horizon_months=12)
    
    print(f"\n📈 12-Month Framework Journey for {context.company_name}")
    print(f"Total Frameworks: {journey.total_frameworks}")
    print(f"Estimated Total Days: {journey.estimated_total_days}")
    
    print("\n🎯 Immediate (Next 30 days):")
    for rec in journey.immediate:
        print(f"  - {rec.framework_id.replace('_', ' ').title()} ({rec.estimated_days} days)")
    
    print("\n📅 Short Term (30-90 days):")
    for rec in journey.short_term:
        print(f"  - {rec.framework_id.replace('_', ' ').title()} ({rec.estimated_days} days)")
    
    print("\n🔄 Medium Term (3-6 months):")
    for rec in journey.medium_term:
        print(f"  - {rec.framework_id.replace('_', ' ').title()} ({rec.estimated_days} days)")
    
    if journey.critical_path:
        print(f"\n⚡ Critical Path: {' → '.join(journey.critical_path)}")


def test_industry_variants():
    """Test industry-specific framework variants"""
    print("\n" + "=" * 80)
    print("TEST 4: Industry-Specific Framework Variants")
    print("=" * 80)
    
    engine = IndustryFrameworkEngine()
    
    # Test SaaS variant of BCG Matrix
    saas_variant = engine.get_variant("bcg_matrix", IndustryContext.B2B_SAAS)
    if saas_variant:
        print("\n🔧 B2B SaaS Variant of BCG Matrix:")
        print(f"Name: {saas_variant.variant_name}")
        print(f"X-Axis: {saas_variant.axis_mappings.get('x_label', 'Default')}")
        print(f"Y-Axis: {saas_variant.axis_mappings.get('y_label', 'Default')}")
        print("\nCustom Metrics:")
        for metric_id, metric in saas_variant.custom_metrics.items():
            print(f"  - {metric.name}: Good={metric.good_benchmark}, Great={metric.great_benchmark}")
    
    # Test marketplace variant
    marketplace_variant = engine.get_variant("unit_economics", IndustryContext.MARKETPLACE)
    if marketplace_variant:
        print("\n🏪 Marketplace Variant of Unit Economics:")
        print(f"Name: {marketplace_variant.variant_name}")
        print("\nKey Considerations:")
        for consideration in marketplace_variant.key_considerations[:3]:
            print(f"  - {consideration}")


def test_antipattern_detection():
    """Test antipattern detection"""
    print("\n" + "=" * 80)
    print("TEST 5: Antipattern Detection")
    print("=" * 80)
    
    # Create a context that should trigger BCG Matrix antipattern
    context = CompanyContext(
        company_name="TinyStartup",
        industry=IndustryContext.B2B_SAAS,
        stage=TemporalStage.PRE_FORMATION,
        team_size=3,  # Too small for BCG Matrix
        primary_problems=[ProblemArchetype.PORTFOLIO_OPTIMIZATION],
        available_data=[DataRequirement.QUALITATIVE_ONLY],
        revenue_usd=0  # Pre-revenue
    )
    
    selector = AdvancedFrameworkSelector()
    
    # Check if BCG Matrix is filtered out
    viable_frameworks = selector._filter_antipatterns(context)
    
    print(f"\nContext: {context.team_size} person team, {context.stage.value} stage, ${context.revenue_usd} revenue")
    print(f"\nTotal frameworks available: {len(selector.tags_db)}")
    print(f"Frameworks after antipattern filtering: {len(viable_frameworks)}")
    
    if "bcg_matrix" not in viable_frameworks:
        print("\n✅ BCG Matrix correctly filtered out due to antipatterns")
    else:
        print("\n❌ BCG Matrix not filtered (unexpected)")
    
    # Show what was recommended instead
    recommendations = selector.select_frameworks(context, max_recommendations=3)
    print("\nRecommended alternatives:")
    for rec in recommendations:
        print(f"  - {rec.framework_id.replace('_', ' ').title()}")


def test_executive_report():
    """Test executive report generation"""
    print("\n" + "=" * 80)
    print("TEST 6: Executive Report Generation")
    print("=" * 80)
    
    context = CompanyContext(
        company_name="ReportTest Inc",
        industry=IndustryContext.B2B_SAAS,
        stage=TemporalStage.GROWTH,
        team_size=75,
        primary_problems=[
            ProblemArchetype.COMPETITIVE_STRATEGY,
            ProblemArchetype.UNIT_ECONOMICS_OPTIMIZATION
        ],
        available_data=[
            DataRequirement.ADVANCED_METRICS,
            DataRequirement.MARKET_DATA
        ],
        revenue_usd=3000000,
        growth_rate_percent=120
    )
    
    selector = AdvancedFrameworkSelector()
    recommendations = selector.select_frameworks(context, max_recommendations=3)
    
    # Generate report
    report = generate_framework_report(context, recommendations)
    
    # Show first part of report
    print("\n📄 Executive Report Preview:")
    print("=" * 60)
    lines = report.split('\n')
    for line in lines[:25]:  # First 25 lines
        print(line)
    print("\n... [Report continues]")


def run_all_tests():
    """Run all validation tests"""
    print("\n🚀 ADVANCED FRAMEWORK SELECTION SYSTEM - VALIDATION SUITE")
    print("Based on MIT Quantitative Methods + HBS Strategic Insights")
    print("=" * 80)
    
    # Run all tests
    test_basic_selection()
    test_crisis_mode_selection()
    test_framework_journey()
    test_industry_variants()
    test_antipattern_detection()
    test_executive_report()
    
    print("\n" + "=" * 80)
    print("✅ All tests completed successfully!")
    print("=" * 80)


if __name__ == "__main__":
    run_all_tests()