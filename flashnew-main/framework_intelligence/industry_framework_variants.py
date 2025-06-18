#!/usr/bin/env python3
"""
Industry-Specific Framework Variants
Deep customization of frameworks for different verticals
Based on empirical research and best practices
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from framework_intelligence.framework_taxonomy import IndustryContext


@dataclass
class MetricDefinition:
    """Define a metric with industry context"""
    name: str
    description: str
    formula: str
    good_benchmark: float
    great_benchmark: float
    unit: str = ""
    frequency: str = "monthly"


@dataclass
class FrameworkVariant:
    """Industry-specific variant of a framework"""
    base_framework_id: str
    industry: IndustryContext
    variant_name: str
    
    # Customizations
    custom_metrics: Dict[str, MetricDefinition] = field(default_factory=dict)
    axis_mappings: Dict[str, str] = field(default_factory=dict)  # For matrix frameworks
    custom_categories: Dict[str, List[str]] = field(default_factory=dict)
    thresholds: Dict[str, float] = field(default_factory=dict)
    
    # Industry-specific guidance
    key_considerations: List[str] = field(default_factory=list)
    common_pitfalls: List[str] = field(default_factory=list)
    success_patterns: List[str] = field(default_factory=list)
    
    # Benchmarks
    industry_benchmarks: Dict[str, Any] = field(default_factory=dict)
    
    # Implementation differences
    modified_steps: Dict[int, str] = field(default_factory=dict)  # Step number -> new instruction
    additional_steps: List[str] = field(default_factory=list)
    tools_required: List[str] = field(default_factory=list)


class IndustryFrameworkEngine:
    """Engine for managing industry-specific framework variants"""
    
    def __init__(self):
        self.variants = self._initialize_variants()
        
    def _initialize_variants(self) -> Dict[str, List[FrameworkVariant]]:
        """Initialize all industry variants"""
        variants = {}
        
        # BCG Matrix Variants
        variants["bcg_matrix"] = [
            # B2B SaaS Variant
            FrameworkVariant(
                base_framework_id="bcg_matrix",
                industry=IndustryContext.B2B_SAAS,
                variant_name="SaaS Growth-Share Matrix",
                axis_mappings={
                    "x_axis": "net_revenue_retention",
                    "y_axis": "arr_growth_rate",
                    "x_label": "Net Revenue Retention (%)",
                    "y_label": "ARR Growth Rate (%)"
                },
                custom_metrics={
                    "net_revenue_retention": MetricDefinition(
                        name="Net Revenue Retention",
                        description="Revenue retained from existing customers including expansion",
                        formula="(Starting ARR - Churn + Expansion) / Starting ARR * 100",
                        good_benchmark=110,
                        great_benchmark=130,
                        unit="%"
                    ),
                    "arr_growth_rate": MetricDefinition(
                        name="ARR Growth Rate",
                        description="Year-over-year Annual Recurring Revenue growth",
                        formula="(Current ARR - Prior Year ARR) / Prior Year ARR * 100",
                        good_benchmark=100,
                        great_benchmark=200,
                        unit="%"
                    )
                },
                thresholds={
                    "high_retention": 110,
                    "high_growth": 100,
                    "star_minimum_arr": 1000000,  # $1M ARR minimum for star
                },
                custom_categories={
                    "star": ["High growth (>100% YoY)", "High retention (>110% NRR)", "ARR > $1M"],
                    "cash_cow": ["Moderate growth (<50% YoY)", "High retention (>110% NRR)", "Profitable"],
                    "question_mark": ["High growth (>100% YoY)", "Low retention (<100% NRR)", "High CAC"],
                    "dog": ["Low growth (<30% YoY)", "Low retention (<90% NRR)", "Consider sunset"]
                },
                key_considerations=[
                    "SaaS businesses should prioritize NRR over new customer acquisition",
                    "Stars in SaaS often have negative cash flow due to growth investments",
                    "Cash cows in SaaS are rare but extremely valuable (e.g., Salesforce CRM)",
                    "Dogs might be feature products that should be bundled, not killed"
                ],
                common_pitfalls=[
                    "Using revenue instead of ARR for calculations",
                    "Ignoring cohort effects in retention calculations",
                    "Not accounting for customer segmentation differences",
                    "Treating all products equally regardless of strategic importance"
                ],
                success_patterns=[
                    "Move question marks to stars by improving product-market fit",
                    "Use cash cows to fund customer success for question marks",
                    "Bundle dogs with stars to increase overall retention"
                ],
                industry_benchmarks={
                    "median_nrr": 106,
                    "top_quartile_nrr": 115,
                    "median_growth": 65,
                    "top_quartile_growth": 125,
                    "rule_of_40_target": 40  # Growth % + Profit Margin %
                }
            ),
            
            # Marketplace Variant
            FrameworkVariant(
                base_framework_id="bcg_matrix",
                industry=IndustryContext.MARKETPLACE,
                variant_name="Marketplace Dynamics Matrix",
                axis_mappings={
                    "x_axis": "take_rate",
                    "y_axis": "gmv_growth",
                    "x_label": "Take Rate (%)",
                    "y_label": "GMV Growth Rate (%)"
                },
                custom_metrics={
                    "take_rate": MetricDefinition(
                        name="Take Rate",
                        description="Percentage of GMV captured as revenue",
                        formula="Net Revenue / GMV * 100",
                        good_benchmark=15,
                        great_benchmark=25,
                        unit="%"
                    ),
                    "gmv_growth": MetricDefinition(
                        name="GMV Growth Rate",
                        description="Gross Merchandise Volume growth year-over-year",
                        formula="(Current GMV - Prior Year GMV) / Prior Year GMV * 100",
                        good_benchmark=100,
                        great_benchmark=200,
                        unit="%"
                    ),
                    "liquidity": MetricDefinition(
                        name="Marketplace Liquidity",
                        description="Percentage of listings that result in transactions",
                        formula="Successful Transactions / Total Listings * 100",
                        good_benchmark=20,
                        great_benchmark=35,
                        unit="%"
                    )
                },
                thresholds={
                    "high_take_rate": 15,
                    "high_growth": 150,
                    "minimum_liquidity": 10  # Below this, marketplace doesn't work
                },
                custom_categories={
                    "star": ["High GMV growth (>150%)", "Strong take rate (>15%)", "High liquidity"],
                    "cash_cow": ["Mature categories", "High take rate", "Stable supply/demand"],
                    "question_mark": ["New categories", "Low take rate", "Supply constrained"],
                    "dog": ["Low liquidity (<10%)", "Declining GMV", "High operational cost"]
                },
                key_considerations=[
                    "Network effects make it hard to kill 'dog' categories",
                    "Take rate must balance marketplace health with profitability",
                    "Geographic expansion often creates new 'question marks'",
                    "Supply-side subsidies may be needed for question marks"
                ],
                industry_benchmarks={
                    "median_take_rate": 12,
                    "top_quartile_take_rate": 20,
                    "median_gmv_growth": 85,
                    "top_quartile_gmv_growth": 180
                }
            ),
            
            # FinTech Variant
            FrameworkVariant(
                base_framework_id="bcg_matrix",
                industry=IndustryContext.FINTECH,
                variant_name="FinTech Portfolio Matrix",
                axis_mappings={
                    "x_axis": "revenue_per_user",
                    "y_axis": "user_growth_rate",
                    "x_label": "Revenue per User ($)",
                    "y_label": "User Growth Rate (%)"
                },
                custom_metrics={
                    "revenue_per_user": MetricDefinition(
                        name="Average Revenue Per User",
                        description="Total revenue divided by active users",
                        formula="Total Revenue / Monthly Active Users",
                        good_benchmark=50,
                        great_benchmark=200,
                        unit="$"
                    ),
                    "regulatory_risk_score": MetricDefinition(
                        name="Regulatory Risk Score",
                        description="Composite score of compliance complexity and risk",
                        formula="Custom scoring based on licenses, jurisdictions, products",
                        good_benchmark=30,  # Lower is better
                        great_benchmark=10,
                        unit="points"
                    )
                },
                thresholds={
                    "high_revenue_per_user": 100,
                    "high_growth": 100,
                    "max_regulatory_risk": 50
                },
                key_considerations=[
                    "Regulatory compliance can quickly turn stars into dogs",
                    "Revenue per user often limited by regulations (e.g., interchange caps)",
                    "Customer acquisition costs are high due to trust requirements",
                    "Cross-selling is critical for moving from question mark to star"
                ],
                industry_benchmarks={
                    "median_arpu": 45,
                    "top_quartile_arpu": 150,
                    "median_cac_payback_months": 18,
                    "compliance_cost_percentage": 15  # % of revenue
                }
            )
        ]
        
        # Unit Economics Variants
        variants["unit_economics"] = [
            # B2B SaaS Variant
            FrameworkVariant(
                base_framework_id="unit_economics",
                industry=IndustryContext.B2B_SAAS,
                variant_name="SaaS Unit Economics",
                custom_metrics={
                    "ltv_cac_ratio": MetricDefinition(
                        name="LTV/CAC Ratio",
                        description="Lifetime value to customer acquisition cost ratio",
                        formula="(ARPU * Gross Margin % * Avg Customer Lifetime) / CAC",
                        good_benchmark=3.0,
                        great_benchmark=5.0,
                        unit="x"
                    ),
                    "magic_number": MetricDefinition(
                        name="SaaS Magic Number",
                        description="Efficiency of sales and marketing spend",
                        formula="(Current Quarter ARR - Prior Quarter ARR) * 4 / Prior Quarter S&M Spend",
                        good_benchmark=0.75,
                        great_benchmark=1.5,
                        unit=""
                    ),
                    "quick_ratio": MetricDefinition(
                        name="SaaS Quick Ratio",
                        description="Growth efficiency accounting for churn",
                        formula="(New MRR + Expansion MRR) / (Churned MRR + Contraction MRR)",
                        good_benchmark=2.0,
                        great_benchmark=4.0,
                        unit="x"
                    ),
                    "burn_multiple": MetricDefinition(
                        name="Burn Multiple",
                        description="Capital efficiency metric",
                        formula="Net Burn / Net New ARR",
                        good_benchmark=2.0,  # Lower is better
                        great_benchmark=1.0,
                        unit="x"
                    )
                },
                key_considerations=[
                    "CAC should be fully loaded (include salaries, tools, overhead)",
                    "LTV calculations should use gross margin, not revenue",
                    "Segmentation by customer size often reveals different unit economics",
                    "Payback period more important than LTV/CAC for capital efficiency"
                ],
                modified_steps={
                    3: "Calculate gross margin excluding customer success costs",
                    5: "Segment CAC by channel and customer segment",
                    7: "Add expansion revenue to LTV calculations"
                },
                industry_benchmarks={
                    "median_ltv_cac": 2.8,
                    "top_quartile_ltv_cac": 4.5,
                    "median_payback_months": 15,
                    "top_quartile_payback_months": 8,
                    "median_gross_margin": 75,
                    "median_magic_number": 0.8
                }
            ),
            
            # Marketplace Variant
            FrameworkVariant(
                base_framework_id="unit_economics",
                industry=IndustryContext.MARKETPLACE,
                variant_name="Marketplace Unit Economics",
                custom_metrics={
                    "contribution_margin": MetricDefinition(
                        name="Contribution Margin per Transaction",
                        description="Profit per transaction after variable costs",
                        formula="Take Rate - Payment Processing - Support Costs - Insurance/Fraud",
                        good_benchmark=60,
                        great_benchmark=80,
                        unit="%"
                    ),
                    "seller_ltv": MetricDefinition(
                        name="Seller Lifetime Value",
                        description="Total contribution from a seller over lifetime",
                        formula="Avg Monthly GMV * Take Rate * Gross Margin * Seller Lifetime",
                        good_benchmark=10000,
                        great_benchmark=50000,
                        unit="$"
                    ),
                    "buyer_ltv": MetricDefinition(
                        name="Buyer Lifetime Value",
                        description="Total contribution from a buyer over lifetime",
                        formula="Avg Order Value * Orders per Year * Years Active * Contribution Margin",
                        good_benchmark=500,
                        great_benchmark=2000,
                        unit="$"
                    ),
                    "cohort_retention": MetricDefinition(
                        name="12-Month Cohort Retention",
                        description="Percentage of users active after 12 months",
                        formula="Month 12 Active Users / Month 0 Cohort Size * 100",
                        good_benchmark=20,
                        great_benchmark=40,
                        unit="%"
                    )
                },
                key_considerations=[
                    "Must track both supply and demand side economics",
                    "Network effects mean losing money on one side might be optimal",
                    "Geographic expansion resets unit economics",
                    "Category expansion often has different economics"
                ],
                additional_steps=[
                    "Calculate supply-side acquisition costs separately",
                    "Analyze cross-side network effects on retention",
                    "Model geographic expansion economics"
                ],
                industry_benchmarks={
                    "median_take_rate": 15,
                    "median_contribution_margin": 65,
                    "supply_side_cac_multiple": 3,  # vs demand side
                    "year_2_retention": 35
                }
            ),
            
            # Hardware Variant
            FrameworkVariant(
                base_framework_id="unit_economics",
                industry=IndustryContext.HARDWARE,
                variant_name="Hardware Unit Economics",
                custom_metrics={
                    "gross_margin": MetricDefinition(
                        name="Hardware Gross Margin",
                        description="Margin after COGS including logistics",
                        formula="(Revenue - COGS - Logistics - Warranty) / Revenue * 100",
                        good_benchmark=35,
                        great_benchmark=50,
                        unit="%"
                    ),
                    "inventory_turns": MetricDefinition(
                        name="Inventory Turnover",
                        description="How often inventory is sold and replaced",
                        formula="Annual COGS / Average Inventory Value",
                        good_benchmark=6,
                        great_benchmark=12,
                        unit="x/year"
                    ),
                    "warranty_reserve": MetricDefinition(
                        name="Warranty Reserve Rate",
                        description="Percentage of revenue reserved for warranty claims",
                        formula="Warranty Reserve / Revenue * 100",
                        good_benchmark=3,  # Lower is better
                        great_benchmark=1,
                        unit="%"
                    ),
                    "nre_recovery": MetricDefinition(
                        name="NRE Recovery Rate",
                        description="Non-recurring engineering cost recovery",
                        formula="Gross Profit per Unit * Units Sold / Total NRE Investment",
                        good_benchmark=1.0,  # Breakeven
                        great_benchmark=3.0,
                        unit="x"
                    )
                },
                key_considerations=[
                    "Working capital requirements often dominate economics",
                    "Scale effects on COGS are non-linear",
                    "Software/services attachment critical for margins",
                    "Supply chain risks can destroy unit economics overnight"
                ],
                modified_steps={
                    2: "Include landed cost (tariffs, logistics) in COGS",
                    4: "Add warranty reserve to unit costs",
                    6: "Calculate breakeven including NRE amortization"
                },
                industry_benchmarks={
                    "median_gross_margin": 32,
                    "top_quartile_gross_margin": 45,
                    "median_inventory_turns": 5,
                    "warranty_claim_rate": 2.5
                }
            )
        ]
        
        # Porter's Five Forces Variants
        variants["porters_five_forces"] = [
            # B2B SaaS Variant
            FrameworkVariant(
                base_framework_id="porters_five_forces",
                industry=IndustryContext.B2B_SAAS,
                variant_name="SaaS Competitive Forces",
                custom_categories={
                    "threat_of_new_entrants": [
                        "Low technical barriers (no-code/low-code platforms)",
                        "Decreasing customer acquisition costs",
                        "Open source alternatives",
                        "Platform players entering verticals (e.g., Salesforce, Microsoft)"
                    ],
                    "bargaining_power_of_buyers": [
                        "Low switching costs without data lock-in",
                        "Increasing price transparency",
                        "Procurement sophistication for SaaS",
                        "Multi-year contract negotiations"
                    ],
                    "threat_of_substitutes": [
                        "In-house development becoming easier",
                        "Horizontal platforms adding vertical features",
                        "AI/automation replacing software categories",
                        "Open source alternatives"
                    ],
                    "bargaining_power_of_suppliers": [
                        "Cloud infrastructure oligopoly (AWS, Azure, GCP)",
                        "Developer talent scarcity",
                        "Third-party API dependencies",
                        "Data provider concentration"
                    ],
                    "competitive_rivalry": [
                        "Feature parity achieved quickly",
                        "Price wars in commoditized categories",
                        "Platform ecosystem competition",
                        "Geographic expansion battles"
                    ]
                },
                key_considerations=[
                    "Network effects and data moats more important than traditional barriers",
                    "Switching costs created through integrations and workflows",
                    "Category creation can avoid direct competition",
                    "Vertical SaaS has different dynamics than horizontal"
                ],
                success_patterns=[
                    "Build switching costs through integrations",
                    "Create category before competitors emerge",
                    "Focus on workflow lock-in vs feature differentiation",
                    "Partner with potential substitutes"
                ]
            ),
            
            # Marketplace Variant
            FrameworkVariant(
                base_framework_id="porters_five_forces",
                industry=IndustryContext.MARKETPLACE,
                variant_name="Marketplace Competitive Dynamics",
                custom_categories={
                    "threat_of_new_entrants": [
                        "Geographic copycats with local advantage",
                        "Vertical marketplace unbundling",
                        "Super apps adding marketplace features",
                        "Social commerce platforms"
                    ],
                    "bargaining_power_of_suppliers": [
                        "Multi-homing by sellers",
                        "Direct-to-consumer alternatives",
                        "Supplier concentration in key categories",
                        "Inventory/fulfillment requirements"
                    ],
                    "bargaining_power_of_buyers": [
                        "Price comparison ease",
                        "Low platform loyalty",
                        "Mobile app switching",
                        "Social proof requirements"
                    ],
                    "network_effects": [  # Additional force for platforms
                        "Cross-side network effects strength",
                        "Local vs global network effects",
                        "Data network effects",
                        "Social network effects"
                    ]
                },
                key_considerations=[
                    "Two-sided dynamics require analyzing both sides",
                    "Local network effects create geographic moats",
                    "Liquidity more important than features",
                    "Winner-take-all dynamics in many categories"
                ]
            )
        ]
        
        # Jobs to be Done Variants
        variants["jobs_to_be_done"] = [
            # B2B SaaS Variant
            FrameworkVariant(
                base_framework_id="jobs_to_be_done",
                industry=IndustryContext.B2B_SAAS,
                variant_name="B2B Software Jobs",
                custom_categories={
                    "functional_jobs": [
                        "Reduce operational costs",
                        "Increase team productivity", 
                        "Ensure compliance",
                        "Scale operations",
                        "Integrate systems"
                    ],
                    "emotional_jobs": [
                        "Look good to boss/board",
                        "Reduce stress/anxiety",
                        "Feel in control",
                        "Appear innovative",
                        "Avoid blame for failures"
                    ],
                    "social_jobs": [
                        "Build political capital",
                        "Justify headcount/budget",
                        "Show leadership",
                        "Enable team success",
                        "Industry recognition"
                    ]
                },
                key_considerations=[
                    "B2B purchases involve multiple stakeholders with different jobs",
                    "Emotional and social jobs often trump functional in enterprise",
                    "Job importance varies by company stage and industry",
                    "Integration jobs become critical as stack grows"
                ],
                modified_steps={
                    2: "Map stakeholder roles (user, buyer, influencer, decision maker)",
                    3: "Identify jobs for each stakeholder type",
                    5: "Analyze competitive solutions by stakeholder"
                },
                tools_required=[
                    "Stakeholder mapping template",
                    "B2B interview guide",
                    "ROI calculator template"
                ]
            )
        ]
        
        return variants
    
    def get_variant(
        self,
        framework_id: str,
        industry: IndustryContext
    ) -> Optional[FrameworkVariant]:
        """Get specific variant for framework and industry"""
        
        if framework_id in self.variants:
            for variant in self.variants[framework_id]:
                if variant.industry == industry:
                    return variant
        return None
    
    def get_all_variants_for_framework(
        self,
        framework_id: str
    ) -> List[FrameworkVariant]:
        """Get all industry variants for a framework"""
        
        return self.variants.get(framework_id, [])
    
    def get_custom_implementation(
        self,
        framework_id: str,
        industry: IndustryContext,
        base_steps: List[str]
    ) -> List[str]:
        """Get customized implementation steps for industry"""
        
        variant = self.get_variant(framework_id, industry)
        if not variant:
            return base_steps
            
        # Apply modifications
        custom_steps = base_steps.copy()
        
        # Modify existing steps
        for step_num, new_instruction in variant.modified_steps.items():
            if 0 <= step_num - 1 < len(custom_steps):
                custom_steps[step_num - 1] = new_instruction
                
        # Add additional steps
        custom_steps.extend(variant.additional_steps)
        
        return custom_steps
    
    def get_industry_benchmarks(
        self,
        framework_id: str,
        industry: IndustryContext,
        metric: str
    ) -> Dict[str, float]:
        """Get industry-specific benchmarks for a metric"""
        
        variant = self.get_variant(framework_id, industry)
        if not variant:
            return {}
            
        if metric in variant.custom_metrics:
            metric_def = variant.custom_metrics[metric]
            return {
                "good": metric_def.good_benchmark,
                "great": metric_def.great_benchmark,
                "industry_median": variant.industry_benchmarks.get(f"median_{metric}", None),
                "industry_top_quartile": variant.industry_benchmarks.get(f"top_quartile_{metric}", None)
            }
            
        return variant.industry_benchmarks
    
    def generate_industry_specific_report(
        self,
        framework_id: str,
        industry: IndustryContext,
        company_data: Dict[str, Any]
    ) -> str:
        """Generate industry-specific insights report"""
        
        variant = self.get_variant(framework_id, industry)
        if not variant:
            return "No industry-specific variant available."
            
        report = f"""
# {variant.variant_name} Analysis
## Industry: {industry.value}

### Key Metrics for Your Industry
"""
        
        for metric_id, metric_def in variant.custom_metrics.items():
            company_value = company_data.get(metric_id, "Not available")
            
            report += f"""
**{metric_def.name}**
- Your value: {company_value} {metric_def.unit}
- Good benchmark: {metric_def.good_benchmark} {metric_def.unit}
- Great benchmark: {metric_def.great_benchmark} {metric_def.unit}
- Formula: {metric_def.formula}
"""
            
        report += """
### Industry-Specific Considerations
"""
        for consideration in variant.key_considerations:
            report += f"- {consideration}\n"
            
        if company_value and isinstance(company_value, (int, float)):
            # Provide specific guidance based on performance
            if metric_id in variant.custom_metrics:
                if company_value >= metric_def.great_benchmark:
                    report += f"\n✅ Your {metric_def.name} is excellent!\n"
                elif company_value >= metric_def.good_benchmark:
                    report += f"\n👍 Your {metric_def.name} is good but has room for improvement.\n"
                else:
                    report += f"\n⚠️ Your {metric_def.name} needs attention.\n"
                    
        return report