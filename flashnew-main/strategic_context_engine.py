#!/usr/bin/env python3
"""
Strategic Context Engine - Build rich company context for McKinsey-grade analysis
"""

import json
import logging
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import numpy as np

logger = logging.getLogger(__name__)


class StrategicInflection(Enum):
    """Key strategic inflection points"""
    PRE_PMF = "pre_product_market_fit"
    ACHIEVING_PMF = "achieving_product_market_fit"
    SCALING_GROWTH = "scaling_growth"
    MARKET_EXPANSION = "market_expansion"
    CATEGORY_CREATION = "category_creation"
    PLATFORM_SHIFT = "platform_shift"
    PROFITABILITY_TRANSITION = "profitability_transition"
    MARKET_LEADERSHIP = "market_leadership"
    DISRUPTION_THREAT = "disruption_threat"


@dataclass
class IndustryBenchmarks:
    """Industry-specific benchmarks"""
    industry: str
    top_quartile_growth: float
    median_growth: float
    top_quartile_nrr: float
    median_burn_multiple: float
    top_quartile_ltv_cac: float
    median_cac_payback_months: int
    time_to_pmf_months: int
    time_to_unicorn_years: float
    typical_gross_margin: float
    typical_ebitda_margin: float
    market_concentration: str  # fragmented, concentrated, oligopoly
    disruption_risk: str  # low, medium, high


@dataclass
class CompetitiveDynamics:
    """Competitive landscape analysis"""
    direct_competitors: List[Dict[str, Any]]
    indirect_competitors: List[Dict[str, Any]]
    market_leader: Dict[str, Any]
    our_relative_position: int  # 1 = leader, 2+ = follower
    differentiation_factors: List[str]
    competitive_advantages: List[str]
    competitive_threats: List[str]
    market_dynamics: str  # stable, consolidating, disrupting, emerging
    

@dataclass
class StrategicPattern:
    """Successful pattern from similar companies"""
    pattern_name: str
    applicable_stage: str
    industry: str
    key_metrics: Dict[str, float]
    frameworks_used: List[str]
    outcome: str
    timeframe_months: int
    critical_success_factors: List[str]


@dataclass
class HypothesisNode:
    """Node in hypothesis tree"""
    question: str
    hypothesis: str
    supporting_data: List[str]
    contradicting_data: List[str]
    sub_hypotheses: List['HypothesisNode'] = field(default_factory=list)
    confidence: float = 0.5
    impact: str = "medium"  # low, medium, high


@dataclass
class CompanyContext:
    """Rich context for strategic analysis"""
    # Basic info
    company_name: str
    industry: str
    sub_industry: str
    stage: str
    founding_date: datetime
    
    # Strategic narrative
    strategic_narrative: str
    founding_story: str
    unique_insights: List[str]
    strategic_assets: List[str]
    key_partnerships: List[str]
    
    # Current situation
    current_inflection: StrategicInflection
    key_challenges: List[str]
    strategic_opportunities: List[str]
    critical_constraints: List[str]
    
    # Metrics and performance
    key_metrics: Dict[str, float]
    metric_trends: Dict[str, List[float]]
    cohort_data: Dict[str, Any]
    
    # External context
    industry_benchmarks: IndustryBenchmarks
    competitive_dynamics: CompetitiveDynamics
    market_trends: List[str]
    regulatory_factors: List[str]
    
    # Pattern matching
    similar_success_patterns: List[StrategicPattern]
    similar_failure_patterns: List[StrategicPattern]
    
    # Strategic questions
    primary_strategic_question: str
    hypothesis_tree: HypothesisNode
    key_uncertainties: List[str]
    strategic_options: List[str]


class StrategicContextEngine:
    """Build rich strategic context for companies"""
    
    def __init__(self):
        self.industry_benchmarks = self._load_industry_benchmarks()
        self.pattern_library = self._load_successful_patterns()
        self.competitive_data = {}
        
    def _load_industry_benchmarks(self) -> Dict[str, IndustryBenchmarks]:
        """Load industry-specific benchmarks"""
        # In production, this would load from a database
        # For now, using representative benchmarks
        return {
            "saas_b2b": IndustryBenchmarks(
                industry="saas_b2b",
                top_quartile_growth=150,  # 150% YoY
                median_growth=80,
                top_quartile_nrr=120,
                median_burn_multiple=1.5,
                top_quartile_ltv_cac=4.0,
                median_cac_payback_months=14,
                time_to_pmf_months=18,
                time_to_unicorn_years=7,
                typical_gross_margin=80,
                typical_ebitda_margin=20,
                market_concentration="fragmented",
                disruption_risk="medium"
            ),
            "marketplace": IndustryBenchmarks(
                industry="marketplace",
                top_quartile_growth=200,
                median_growth=100,
                top_quartile_nrr=115,
                median_burn_multiple=2.0,
                top_quartile_ltv_cac=3.0,
                median_cac_payback_months=18,
                time_to_pmf_months=24,
                time_to_unicorn_years=6,
                typical_gross_margin=70,
                typical_ebitda_margin=15,
                market_concentration="concentrated",
                disruption_risk="high"
            ),
            "fintech": IndustryBenchmarks(
                industry="fintech",
                top_quartile_growth=120,
                median_growth=70,
                top_quartile_nrr=110,
                median_burn_multiple=2.5,
                top_quartile_ltv_cac=3.5,
                median_cac_payback_months=20,
                time_to_pmf_months=30,
                time_to_unicorn_years=8,
                typical_gross_margin=60,
                typical_ebitda_margin=10,
                market_concentration="oligopoly",
                disruption_risk="high"
            ),
            "healthtech": IndustryBenchmarks(
                industry="healthtech",
                top_quartile_growth=100,
                median_growth=60,
                top_quartile_nrr=105,
                median_burn_multiple=3.0,
                top_quartile_ltv_cac=3.0,
                median_cac_payback_months=24,
                time_to_pmf_months=36,
                time_to_unicorn_years=10,
                typical_gross_margin=65,
                typical_ebitda_margin=5,
                market_concentration="fragmented",
                disruption_risk="medium"
            )
        }
        
    def _load_successful_patterns(self) -> List[StrategicPattern]:
        """Load patterns from successful companies"""
        return [
            StrategicPattern(
                pattern_name="PLG_to_Enterprise",
                applicable_stage="growth",
                industry="saas_b2b",
                key_metrics={"nrr": 120, "growth": 100, "ltv_cac": 4},
                frameworks_used=["product_led_growth", "enterprise_sales", "land_and_expand"],
                outcome="Successful upmarket transition",
                timeframe_months=18,
                critical_success_factors=["Strong product", "Sales team", "Enterprise features"]
            ),
            StrategicPattern(
                pattern_name="Geographic_Expansion",
                applicable_stage="scale",
                industry="marketplace",
                key_metrics={"market_share": 15, "unit_economics": 2.5},
                frameworks_used=["market_entry", "localization", "partnership_strategy"],
                outcome="International growth",
                timeframe_months=24,
                critical_success_factors=["Local partnerships", "Adapted product", "Capital"]
            ),
            StrategicPattern(
                pattern_name="Vertical_Integration",
                applicable_stage="mature",
                industry="fintech",
                key_metrics={"gross_margin": 70, "market_position": 1},
                frameworks_used=["value_chain", "build_vs_buy", "integration_strategy"],
                outcome="Margin expansion",
                timeframe_months=36,
                critical_success_factors=["Technical capability", "Regulatory approval", "Capital"]
            )
        ]
        
    async def build_company_context(self, startup_data: Dict[str, Any]) -> CompanyContext:
        """Build comprehensive company context"""
        
        # Determine industry and sub-industry
        industry, sub_industry = self._categorize_industry(startup_data)
        
        # Get industry benchmarks
        benchmarks = self._get_industry_benchmarks(industry)
        
        # Analyze competitive dynamics
        competitive_dynamics = await self._analyze_competitive_landscape(
            startup_data, industry
        )
        
        # Identify strategic inflection point
        inflection = self._identify_inflection_point(startup_data, benchmarks)
        
        # Build strategic narrative
        narrative = self._build_strategic_narrative(startup_data, inflection)
        
        # Find similar patterns
        success_patterns = self._find_similar_patterns(
            startup_data, industry, "success"
        )
        failure_patterns = self._find_similar_patterns(
            startup_data, industry, "failure"
        )
        
        # Generate hypothesis tree
        primary_question = self._generate_primary_strategic_question(
            startup_data, inflection, competitive_dynamics
        )
        hypothesis_tree = self._build_hypothesis_tree(
            primary_question, startup_data, benchmarks
        )
        
        # Extract key metrics and trends
        metrics, trends = self._extract_metrics_and_trends(startup_data)
        
        return CompanyContext(
            company_name=startup_data.get("startup_name", "Company"),
            industry=industry,
            sub_industry=sub_industry,
            stage=startup_data.get("funding_stage", "seed"),
            founding_date=datetime.now(),  # Would extract from data
            strategic_narrative=narrative,
            founding_story=self._extract_founding_story(startup_data),
            unique_insights=self._extract_unique_insights(startup_data),
            strategic_assets=self._identify_strategic_assets(startup_data),
            key_partnerships=self._extract_partnerships(startup_data),
            current_inflection=inflection,
            key_challenges=self._identify_key_challenges(startup_data, benchmarks),
            strategic_opportunities=self._identify_opportunities(
                startup_data, benchmarks, competitive_dynamics
            ),
            critical_constraints=self._identify_constraints(startup_data),
            key_metrics=metrics,
            metric_trends=trends,
            cohort_data=self._extract_cohort_data(startup_data),
            industry_benchmarks=benchmarks,
            competitive_dynamics=competitive_dynamics,
            market_trends=self._identify_market_trends(industry),
            regulatory_factors=self._identify_regulatory_factors(industry),
            similar_success_patterns=success_patterns,
            similar_failure_patterns=failure_patterns,
            primary_strategic_question=primary_question,
            hypothesis_tree=hypothesis_tree,
            key_uncertainties=self._identify_uncertainties(
                startup_data, industry
            ),
            strategic_options=self._generate_strategic_options(
                inflection, benchmarks, competitive_dynamics
            )
        )
        
    def _categorize_industry(self, data: Dict[str, Any]) -> Tuple[str, str]:
        """Categorize company into industry and sub-industry"""
        sector = data.get("sector", "").lower()
        b2b_b2c = data.get("b2b_or_b2c", "b2b").lower()
        
        # Map to our industry categories
        industry_map = {
            "saas": "saas_b2b" if b2b_b2c == "b2b" else "saas_b2c",
            "software": "saas_b2b" if b2b_b2c == "b2b" else "saas_b2c",
            "fintech": "fintech",
            "finance": "fintech",
            "healthcare": "healthtech",
            "health": "healthtech",
            "ecommerce": "marketplace",
            "marketplace": "marketplace"
        }
        
        for key, value in industry_map.items():
            if key in sector:
                return value, sector
                
        return "saas_b2b", sector  # Default
        
    def _get_industry_benchmarks(self, industry: str) -> IndustryBenchmarks:
        """Get industry-specific benchmarks"""
        return self.industry_benchmarks.get(
            industry,
            self.industry_benchmarks["saas_b2b"]  # Default
        )
        
    async def _analyze_competitive_landscape(
        self, data: Dict[str, Any], industry: str
    ) -> CompetitiveDynamics:
        """Analyze competitive dynamics"""
        # In production, this would call external APIs for competitor data
        # For now, using data from the startup
        
        competitor_count = data.get("competitor_count", 10)
        market_share = data.get("market_share_percentage", 1.0)
        
        # Determine position
        if market_share > 20:
            position = 1
        elif market_share > 10:
            position = 2
        elif market_share > 5:
            position = 3
        else:
            position = competitor_count // 2
            
        # Determine market dynamics
        growth = data.get("market_growth_rate_percent", 20)
        if growth > 50:
            dynamics = "emerging"
        elif growth > 20:
            dynamics = "disrupting"
        elif competitor_count < 5:
            dynamics = "consolidating"
        else:
            dynamics = "stable"
            
        return CompetitiveDynamics(
            direct_competitors=[
                {"name": f"Competitor {i+1}", "market_share": 15 - i}
                for i in range(min(5, competitor_count))
            ],
            indirect_competitors=[],
            market_leader={"name": "Market Leader", "market_share": 30},
            our_relative_position=position,
            differentiation_factors=self._extract_differentiation(data),
            competitive_advantages=self._extract_advantages(data),
            competitive_threats=self._identify_threats(data),
            market_dynamics=dynamics
        )
        
    def _identify_inflection_point(
        self, data: Dict[str, Any], benchmarks: IndustryBenchmarks
    ) -> StrategicInflection:
        """Identify current strategic inflection point"""
        revenue = data.get("annual_revenue_usd", 0)
        growth = data.get("revenue_growth_rate_percent", 0)
        users = data.get("monthly_active_users", 0)
        nrr = data.get("net_dollar_retention", 100)
        stage = data.get("funding_stage", "seed")
        
        if revenue == 0:
            return StrategicInflection.PRE_PMF
        elif revenue < 1000000 and growth > 20:
            return StrategicInflection.ACHIEVING_PMF
        elif growth > benchmarks.top_quartile_growth:
            return StrategicInflection.SCALING_GROWTH
        elif stage in ["series_b", "series_c"] and nrr > 110:
            return StrategicInflection.MARKET_EXPANSION
        elif data.get("market_share_percentage", 0) > 15:
            return StrategicInflection.MARKET_LEADERSHIP
        else:
            return StrategicInflection.SCALING_GROWTH
            
    def _build_strategic_narrative(
        self, data: Dict[str, Any], inflection: StrategicInflection
    ) -> str:
        """Build strategic narrative"""
        narratives = {
            StrategicInflection.PRE_PMF: (
                f"{data.get('startup_name')} is seeking product-market fit in the "
                f"{data.get('sector')} space, with {data.get('monthly_active_users', 0)} "
                f"early users and {data.get('runway_months', 12)} months runway to prove "
                f"the concept."
            ),
            StrategicInflection.ACHIEVING_PMF: (
                f"{data.get('startup_name')} is showing early signs of product-market fit "
                f"with ${data.get('annual_revenue_usd', 0):,.0f} in revenue and "
                f"{data.get('revenue_growth_rate_percent', 0)}% growth, positioning for "
                f"rapid scaling."
            ),
            StrategicInflection.SCALING_GROWTH: (
                f"{data.get('startup_name')} is in hypergrowth mode with "
                f"{data.get('revenue_growth_rate_percent', 0)}% annual growth, focusing on "
                f"scaling efficiently while maintaining unit economics."
            )
        }
        
        return narratives.get(
            inflection,
            f"{data.get('startup_name')} is navigating {inflection.value}"
        )
        
    def _find_similar_patterns(
        self, data: Dict[str, Any], industry: str, pattern_type: str
    ) -> List[StrategicPattern]:
        """Find similar success or failure patterns"""
        relevant_patterns = []
        
        for pattern in self.pattern_library:
            if pattern.industry == industry:
                # Check if metrics are similar
                similarity = self._calculate_pattern_similarity(data, pattern)
                if similarity > 0.7:
                    relevant_patterns.append(pattern)
                    
        return relevant_patterns[:3]  # Top 3 most relevant
        
    def _calculate_pattern_similarity(
        self, data: Dict[str, Any], pattern: StrategicPattern
    ) -> float:
        """Calculate similarity to a pattern"""
        similarity_scores = []
        
        for metric, value in pattern.key_metrics.items():
            if metric in ["nrr", "growth", "ltv_cac"]:
                actual = data.get(f"{metric}_percent", data.get(metric, 0))
                if actual > 0 and value > 0:
                    try:
                        similarity = 1 - abs(actual - value) / value
                        similarity_scores.append(max(0, similarity))
                    except ZeroDivisionError:
                        logger.warning(f"Division by zero in pattern matching: value={value}")
                        continue
                    
        try:
            return np.mean(similarity_scores) if similarity_scores else 0
        except Exception as e:
            logger.error(f"Error calculating similarity scores: {e}")
            return 0
        
    def _generate_primary_strategic_question(
        self, data: Dict[str, Any], 
        inflection: StrategicInflection,
        competitive: CompetitiveDynamics
    ) -> str:
        """Generate the primary strategic question"""
        questions = {
            StrategicInflection.PRE_PMF: (
                f"How can {data.get('startup_name')} achieve product-market fit "
                f"within {data.get('runway_months', 12)} months while competing against "
                f"{competitive.direct_competitors[0]['name'] if competitive.direct_competitors else 'established players'}?"
            ),
            StrategicInflection.SCALING_GROWTH: (
                f"How should {data.get('startup_name')} scale from "
                f"${data.get('annual_revenue_usd', 0)/1e6:.1f}M to "
                f"${data.get('annual_revenue_usd', 0)*5/1e6:.0f}M while maintaining "
                f"unit economics and competitive differentiation?"
            )
        }
        
        return questions.get(
            inflection,
            f"What is the optimal growth strategy for {data.get('startup_name')}?"
        )
        
    def _build_hypothesis_tree(
        self, primary_question: str, 
        data: Dict[str, Any],
        benchmarks: IndustryBenchmarks
    ) -> HypothesisNode:
        """Build McKinsey-style hypothesis tree"""
        root = HypothesisNode(
            question=primary_question,
            hypothesis=f"{data.get('startup_name')} can achieve sustainable growth through focused execution",
            supporting_data=[],
            contradicting_data=[]
        )
        
        # Add sub-hypotheses based on data
        if data.get("annual_revenue_usd", 0) == 0:
            root.sub_hypotheses.append(
                HypothesisNode(
                    question="Is there sufficient market demand?",
                    hypothesis="The TAM supports a venture-scale business",
                    supporting_data=[f"TAM: ${data.get('market_size_usd', 0)/1e9:.1f}B"],
                    contradicting_data=[],
                    impact="high"
                )
            )
            
        if data.get("ltv_cac_ratio", 0) < 3:
            root.sub_hypotheses.append(
                HypothesisNode(
                    question="Can unit economics be fixed?",
                    hypothesis="CAC can be reduced through product improvements",
                    supporting_data=[],
                    contradicting_data=[f"Current LTV/CAC: {data.get('ltv_cac_ratio', 1):.1f}"],
                    impact="high"
                )
            )
            
        return root
        
    def _extract_metrics_and_trends(
        self, data: Dict[str, Any]
    ) -> Tuple[Dict[str, float], Dict[str, List[float]]]:
        """Extract key metrics and trends"""
        metrics = {
            "revenue": data.get("annual_revenue_usd", 0),
            "growth_rate": data.get("revenue_growth_rate_percent", 0),
            "burn_rate": data.get("monthly_burn_usd", 0),
            "runway": data.get("runway_months", 0),
            "ltv_cac": data.get("ltv_cac_ratio", 0),
            "nrr": data.get("net_dollar_retention", 100),
            "users": data.get("monthly_active_users", 0),
            "market_share": data.get("market_share_percentage", 0)
        }
        
        # In production, would have historical data
        # For now, creating synthetic trends
        trends = {
            "revenue": [metrics["revenue"] * 0.5, metrics["revenue"] * 0.7, metrics["revenue"]],
            "users": [metrics["users"] * 0.6, metrics["users"] * 0.8, metrics["users"]],
            "ltv_cac": [2.0, 2.5, metrics["ltv_cac"]]
        }
        
        return metrics, trends
        
    def _extract_founding_story(self, data: Dict[str, Any]) -> str:
        """Extract or generate founding story"""
        return (
            f"Founded to solve {data.get('sector', 'industry')} challenges with "
            f"{data.get('key_differentiators', 'innovative technology')}"
        )
        
    def _extract_unique_insights(self, data: Dict[str, Any]) -> List[str]:
        """Extract unique insights"""
        insights = []
        
        if data.get("proprietary_tech"):
            insights.append("Proprietary technology platform")
        if data.get("network_effects"):
            insights.append("Strong network effects")
        if data.get("patents_filed", 0) > 0:
            insights.append(f"{data.get('patents_filed')} patents filed")
            
        return insights
        
    def _identify_strategic_assets(self, data: Dict[str, Any]) -> List[str]:
        """Identify strategic assets"""
        assets = []
        
        if data.get("brand_strength_score", 0) > 7:
            assets.append("Strong brand recognition")
        if data.get("customer_count", 0) > 1000:
            assets.append(f"{data.get('customer_count'):,} customers")
        if data.get("data_moat"):
            assets.append("Proprietary data assets")
            
        return assets
        
    def _extract_partnerships(self, data: Dict[str, Any]) -> List[str]:
        """Extract key partnerships"""
        # In production, would extract from data
        return ["Strategic partners in distribution"]
        
    def _identify_key_challenges(
        self, data: Dict[str, Any], benchmarks: IndustryBenchmarks
    ) -> List[str]:
        """Identify key challenges based on data"""
        challenges = []
        
        if data.get("runway_months", 0) < 12:
            challenges.append("Limited runway requiring immediate funding")
            
        if data.get("ltv_cac_ratio", 0) < benchmarks.top_quartile_ltv_cac * 0.5:
            challenges.append("Unit economics below industry benchmarks")
            
        if data.get("revenue_growth_rate_percent", 0) < benchmarks.median_growth:
            challenges.append("Growth rate below industry median")
            
        if data.get("competitor_count", 0) > 50:
            challenges.append("Highly competitive market")
            
        return challenges
        
    def _identify_opportunities(
        self, data: Dict[str, Any], 
        benchmarks: IndustryBenchmarks,
        competitive: CompetitiveDynamics
    ) -> List[str]:
        """Identify strategic opportunities"""
        opportunities = []
        
        if data.get("market_growth_rate_percent", 0) > 30:
            opportunities.append("Rapidly growing market")
            
        if competitive.our_relative_position > 3:
            opportunities.append("Opportunity to gain market share")
            
        if data.get("net_dollar_retention", 100) > benchmarks.top_quartile_nrr:
            opportunities.append("Strong expansion revenue potential")
            
        return opportunities
        
    def _identify_constraints(self, data: Dict[str, Any]) -> List[str]:
        """Identify critical constraints"""
        constraints = []
        
        if data.get("cash_on_hand_usd", 0) < data.get("monthly_burn_usd", 0) * 6:
            constraints.append("Capital constraints")
            
        if data.get("team_size_full_time", 0) < 10:
            constraints.append("Limited team capacity")
            
        if data.get("regulatory_advantage", False):
            constraints.append("Regulatory requirements")
            
        return constraints
        
    def _extract_cohort_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract cohort retention data"""
        return {
            "d1_retention": data.get("product_retention_1d", 100),
            "d7_retention": data.get("product_retention_7d", 80),
            "d30_retention": data.get("product_retention_30d", 60),
            "d90_retention": data.get("product_retention_90d", 40)
        }
        
    def _extract_differentiation(self, data: Dict[str, Any]) -> List[str]:
        """Extract differentiation factors"""
        factors = []
        
        if data.get("proprietary_tech"):
            factors.append("Proprietary technology")
        if data.get("network_effects"):
            factors.append("Network effects")
        if data.get("brand_strength_score", 0) > 7:
            factors.append("Brand strength")
            
        return factors
        
    def _extract_advantages(self, data: Dict[str, Any]) -> List[str]:
        """Extract competitive advantages"""
        advantages = []
        
        if data.get("switching_cost_score", 0) > 7:
            advantages.append("High switching costs")
        if data.get("scalability_score", 0) > 8:
            advantages.append("Superior scalability")
        if data.get("domain_expertise_years", 0) > 10:
            advantages.append("Deep domain expertise")
            
        return advantages
        
    def _identify_threats(self, data: Dict[str, Any]) -> List[str]:
        """Identify competitive threats"""
        threats = []
        
        if data.get("competitor_count", 0) > 50:
            threats.append("New entrants")
        if not data.get("proprietary_tech"):
            threats.append("Easy to replicate")
        if data.get("customer_concentration", 0) > 30:
            threats.append("Customer concentration risk")
            
        return threats
        
    def _identify_market_trends(self, industry: str) -> List[str]:
        """Identify relevant market trends"""
        trends_map = {
            "saas_b2b": [
                "Shift to usage-based pricing",
                "AI/ML integration expectations",
                "Consolidation of point solutions"
            ],
            "fintech": [
                "Embedded finance growth",
                "Regulatory scrutiny increasing",
                "Open banking adoption"
            ],
            "healthtech": [
                "Value-based care transition",
                "AI diagnostics adoption",
                "Patient data portability"
            ],
            "marketplace": [
                "Creator economy expansion",
                "Social commerce integration",
                "Sustainability focus"
            ]
        }
        
        return trends_map.get(industry, ["Digital transformation", "AI adoption"])
        
    def _identify_regulatory_factors(self, industry: str) -> List[str]:
        """Identify regulatory factors"""
        regulatory_map = {
            "fintech": ["Banking regulations", "KYC/AML requirements", "Data privacy"],
            "healthtech": ["HIPAA compliance", "FDA approvals", "Medical licensing"],
            "marketplace": ["Tax collection", "Labor classification", "Consumer protection"]
        }
        
        return regulatory_map.get(industry, ["Data privacy", "General compliance"])
        
    def _identify_uncertainties(
        self, data: Dict[str, Any], industry: str
    ) -> List[str]:
        """Identify key uncertainties"""
        uncertainties = []
        
        if data.get("annual_revenue_usd", 0) == 0:
            uncertainties.append("Time to first revenue")
            
        if data.get("funding_stage") in ["pre_seed", "seed"]:
            uncertainties.append("Product-market fit achievement")
            
        uncertainties.extend([
            "Competitive response to growth",
            "Market growth sustainability",
            "Regulatory changes"
        ])
        
        return uncertainties
        
    def _generate_strategic_options(
        self, inflection: StrategicInflection,
        benchmarks: IndustryBenchmarks,
        competitive: CompetitiveDynamics
    ) -> List[str]:
        """Generate strategic options"""
        options_map = {
            StrategicInflection.PRE_PMF: [
                "Narrow focus to specific customer segment",
                "Pivot to adjacent market opportunity",
                "Partner for distribution"
            ],
            StrategicInflection.SCALING_GROWTH: [
                "Aggressive geographic expansion",
                "Upmarket enterprise focus",
                "Platform strategy with APIs",
                "Strategic acquisitions"
            ],
            StrategicInflection.MARKET_LEADERSHIP: [
                "Category expansion",
                "International markets",
                "M&A consolidation"
            ]
        }
        
        return options_map.get(
            inflection,
            ["Organic growth", "Strategic partnerships", "Market expansion"]
        )