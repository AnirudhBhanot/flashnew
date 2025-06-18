"""
Enhanced Framework Intelligence Engine - Next Generation Framework Selection

This module implements ML-driven framework selection with real-time adaptation,
competitive intelligence integration, and outcome-based learning.
"""

import json
import numpy as np
from typing import List, Dict, Optional, Tuple, Set, Any
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timedelta
import re
from collections import defaultdict, Counter
import asyncio
from concurrent.futures import ThreadPoolExecutor

from .framework_database import (
    Framework, FrameworkCategory, ComplexityLevel,
    get_framework_by_id, get_frameworks_by_category,
    FRAMEWORKS
)
from .framework_selector import BusinessStage, IndustryType, ChallengeType, StartupContext


@dataclass
class MarketIntelligence:
    """Real-time market intelligence data"""
    competitor_moves: List[Dict[str, Any]]
    industry_trends: List[Dict[str, Any]]
    regulatory_changes: List[Dict[str, Any]]
    funding_rounds: List[Dict[str, Any]]
    market_signals: Dict[str, float]
    technology_shifts: List[str]
    customer_sentiment: Dict[str, float]
    
    
@dataclass
class CompanyDNA:
    """Deep company profile beyond basic metrics"""
    culture_indicators: Dict[str, float]
    innovation_velocity: float
    execution_capability: float
    market_timing_score: float
    founder_profiles: List[Dict[str, Any]]
    tech_stack_sophistication: float
    customer_love_score: float
    competitive_moat_strength: float
    

@dataclass
class FrameworkOutcome:
    """Historical outcome data for framework effectiveness"""
    framework_id: str
    company_stage: str
    industry: str
    success_metrics: Dict[str, float]
    implementation_time: int  # days
    roi_achieved: float
    challenges_encountered: List[str]
    modifications_made: List[str]
    

@dataclass
class EnhancedRecommendation:
    """Enhanced framework recommendation with intelligence"""
    framework: Framework
    relevance_score: float
    confidence_level: float
    synergy_score: float  # How well it works with other selected frameworks
    timing_score: float  # How appropriate for current market conditions
    customizations: List[str]  # Specific adaptations for this company
    success_probability: float
    risk_factors: List[str]
    quick_wins: List[str]  # Early victories possible
    integration_plan: Dict[str, Any]
    

class IntelligenceSource(Enum):
    """Data sources for market intelligence"""
    CRUNCHBASE = "crunchbase"
    PITCHBOOK = "pitchbook"
    GARTNER = "gartner"
    FORRESTER = "forrester"
    TECHCRUNCH = "techcrunch"
    INDUSTRY_REPORTS = "industry_reports"
    PATENT_FILINGS = "patent_filings"
    SOCIAL_SIGNALS = "social_signals"
    

class EnhancedFrameworkSelector:
    """Next-generation framework selector with ML and real-time intelligence"""
    
    def __init__(self):
        self.framework_patterns = self._initialize_enhanced_patterns()
        self.outcome_database = self._load_outcome_database()
        self.market_intelligence_cache = {}
        self.ml_model = self._initialize_ml_model()
        self.synergy_matrix = self._build_synergy_matrix()
        # Add stage and challenge mappings from original selector
        self.stage_frameworks = self._initialize_stage_mappings()
        self.challenge_frameworks = self._initialize_challenge_mappings()
        
    def _initialize_enhanced_patterns(self) -> Dict[str, Any]:
        """Initialize enhanced pattern matching with ML weights"""
        return {
            "growth_velocity_patterns": {
                "hypergrowth": {
                    "indicators": ["mrr_growth > 20%", "user_growth > 15%", "market_expansion"],
                    "frameworks": ["blitzscaling", "growth_loops", "viral_coefficient", "land_and_expand"],
                    "weight": 0.85
                },
                "steady_growth": {
                    "indicators": ["mrr_growth 5-20%", "user_growth 5-15%", "market_penetration"],
                    "frameworks": ["aarrr_metrics", "growth_hacking", "product_led_growth"],
                    "weight": 0.75
                },
                "stagnant": {
                    "indicators": ["mrr_growth < 5%", "user_growth < 5%", "high_churn"],
                    "frameworks": ["turnaround_strategy", "pivot_framework", "jobs_to_be_done"],
                    "weight": 0.90
                }
            },
            "market_dynamics_patterns": {
                "winner_take_all": {
                    "indicators": ["network_effects", "high_switching_costs", "platform_dynamics"],
                    "frameworks": ["platform_strategy", "network_orchestration", "ecosystem_play"],
                    "weight": 0.88
                },
                "fragmented": {
                    "indicators": ["low_barriers", "many_competitors", "regional_differences"],
                    "frameworks": ["niche_domination", "vertical_integration", "roll_up_strategy"],
                    "weight": 0.82
                },
                "disruption_imminent": {
                    "indicators": ["new_technology", "changing_regulations", "shifting_demographics"],
                    "frameworks": ["disruption_defense", "innovation_portfolio", "scenario_planning"],
                    "weight": 0.92
                }
            },
            "organizational_maturity_patterns": {
                "founder_led": {
                    "indicators": ["team < 20", "founder_ceo", "informal_processes"],
                    "frameworks": ["founder_scaling", "delegation_framework", "culture_codification"],
                    "weight": 0.80
                },
                "scaling_chaos": {
                    "indicators": ["team 20-100", "process_gaps", "communication_breakdown"],
                    "frameworks": ["spans_and_layers", "okr_implementation", "agile_at_scale"],
                    "weight": 0.85
                },
                "enterprise_transition": {
                    "indicators": ["team > 100", "multiple_products", "global_presence"],
                    "frameworks": ["matrix_organization", "innovation_labs", "corporate_venture"],
                    "weight": 0.78
                }
            }
        }
        
    def _load_outcome_database(self) -> List[FrameworkOutcome]:
        """Load historical framework outcomes (would connect to real database)"""
        # Simulated data - in production, this would query actual outcome database
        return []
        
    def _initialize_ml_model(self) -> Any:
        """Initialize ML model for framework scoring"""
        # Placeholder for actual ML model (would use TensorFlow/PyTorch)
        class MLModel:
            def predict_success(self, features: Dict[str, float]) -> float:
                # More nuanced scoring based on feature alignment
                base_score = 0.4  # Start lower to allow more variation
                
                # Stage match is critical
                stage_match = features.get("stage_match", 0)
                base_score += stage_match * 0.25
                
                # Challenge alignment is important
                challenge_align = features.get("challenge_alignment", 0)
                base_score += challenge_align * 0.20
                
                # Resource fit matters
                resource_fit = features.get("resource_fit", 0)
                base_score += resource_fit * 0.15
                
                # Culture and execution readiness
                culture_align = features.get("culture_alignment", 0.5)
                base_score += culture_align * 0.10
                
                execution_ready = features.get("execution_readiness", 0.5)
                base_score += execution_ready * 0.10
                
                # Add some randomness to avoid always selecting the same
                import random
                base_score += random.uniform(-0.05, 0.05)
                
                return max(0.1, min(base_score, 0.95))
                
        return MLModel()
        
    def _build_synergy_matrix(self) -> Dict[Tuple[str, str], float]:
        """Build framework synergy scores"""
        synergies = {}
        
        # High synergy combinations
        synergies[("okr_framework", "balanced_scorecard")] = 0.85
        synergies[("design_thinking", "lean_startup")] = 0.90
        synergies[("blue_ocean_strategy", "jobs_to_be_done")] = 0.88
        synergies[("porters_five_forces", "swot_analysis")] = 0.82
        synergies[("growth_loops", "aarrr_metrics")] = 0.87
        synergies[("bcg_matrix", "ansoff_matrix")] = 0.83
        
        # Conflicting frameworks (negative synergy)
        synergies[("waterfall_methodology", "agile_methodology")] = -0.5
        synergies[("cost_leadership", "differentiation_strategy")] = -0.3
        
        # Make synergy matrix symmetric
        synergy_copy = synergies.copy()
        for (f1, f2), score in synergy_copy.items():
            synergies[(f2, f1)] = score
            
        return synergies
        
    def _initialize_stage_mappings(self) -> Dict[BusinessStage, List[str]]:
        """Map business stages to relevant frameworks"""
        return {
            BusinessStage.IDEA: [
                "design_thinking", "jobs_to_be_done", "lean_startup", "mvp_framework",
                "customer_development", "value_proposition_canvas"
            ],
            BusinessStage.MVP: [
                "lean_startup", "mvp_framework", "product_market_fit", "unit_economics",
                "customer_journey_mapping", "agile_methodology"
            ],
            BusinessStage.PRODUCT_MARKET_FIT: [
                "product_market_fit", "aarrr_metrics", "unit_economics", "ltv_cac_ratio",
                "growth_loops", "content_marketing_framework"
            ],
            BusinessStage.GROWTH: [
                "growth_loops", "product_led_growth", "viral_coefficient", "land_and_expand",
                "saas_metrics", "okr_framework", "scaling_framework"
            ],
            BusinessStage.SCALE: [
                "organizational_culture", "leadership_pipeline", "balanced_scorecard",
                "operational_excellence", "supply_chain_optimization", "mckinsey_7s"
            ],
            BusinessStage.MATURE: [
                "blue_ocean_strategy", "innovation_ecosystem", "digital_transformation",
                "porters_five_forces", "bcg_matrix", "transformation_framework"
            ]
        }
        
    def _initialize_challenge_mappings(self) -> Dict[ChallengeType, List[str]]:
        """Map challenges to relevant frameworks"""
        return {
            ChallengeType.CUSTOMER_ACQUISITION: [
                "aarrr_metrics", "growth_loops", "content_marketing_framework",
                "viral_coefficient", "stp_marketing", "marketing_mix_4ps"
            ],
            ChallengeType.RETENTION: [
                "customer_journey_mapping", "jobs_to_be_done", "kano_model",
                "nps_framework", "customer_success", "cohort_analysis"
            ],
            ChallengeType.PRODUCT_DEVELOPMENT: [
                "design_thinking", "agile_methodology", "lean_startup",
                "stage_gate_process", "mvp_framework", "rice_prioritization"
            ],
            ChallengeType.MARKET_ENTRY: [
                "porters_five_forces", "swot_analysis", "ansoff_matrix",
                "market_entry_strategy", "competitive_analysis", "blue_ocean_strategy"
            ],
            ChallengeType.COMPETITIVE_PRESSURE: [
                "porters_five_forces", "blue_ocean_strategy", "value_chain_analysis",
                "competitive_advantage", "differentiation_strategy", "brand_positioning_framework"
            ],
            ChallengeType.SCALING: [
                "scaling_framework", "operational_excellence", "spans_and_layers",
                "leadership_pipeline", "organizational_design", "process_optimization"
            ],
            ChallengeType.FUNDING: [
                "unit_economics", "ltv_cac_ratio", "burn_rate_runway",
                "financial_modeling", "investor_pitch", "saas_metrics"
            ],
            ChallengeType.TEAM_BUILDING: [
                "hiring_framework", "team_effectiveness", "culture_framework",
                "performance_management", "leadership_development", "talent_management"
            ],
            ChallengeType.CULTURE: [
                "organizational_culture", "servant_leadership", "values_framework",
                "employee_engagement", "change_management", "cultural_transformation"
            ],
            ChallengeType.INNOVATION: [
                "design_thinking", "open_innovation", "innovation_ecosystem",
                "stage_gate_process", "lean_startup", "disruptive_innovation"
            ],
            ChallengeType.COST_OPTIMIZATION: [
                "lean_methodology", "value_chain_analysis", "activity_based_costing",
                "zero_based_budgeting", "process_optimization", "automation_framework"
            ],
            ChallengeType.STRATEGIC_PLANNING: [
                "swot_analysis", "scenario_planning", "balanced_scorecard",
                "blue_ocean_strategy", "mckinsey_7s", "strategic_planning_process"
            ],
            ChallengeType.DIGITAL_TRANSFORMATION: [
                "digital_maturity", "agile_methodology", "platform_strategy",
                "api_economy", "data_strategy", "customer_experience_design"
            ],
            ChallengeType.QUALITY_ISSUES: [
                "six_sigma", "total_quality_management", "root_cause_analysis",
                "continuous_improvement", "quality_circles", "iso_framework"
            ],
            ChallengeType.OPERATIONAL_EFFICIENCY: [
                "lean_methodology", "six_sigma", "process_mapping",
                "automation_framework", "supply_chain_optimization", "operational_excellence"
            ]
        }
        
    async def get_market_intelligence(
        self,
        context: StartupContext
    ) -> MarketIntelligence:
        """Fetch real-time market intelligence"""
        # In production, this would aggregate data from multiple sources
        # For now, return intelligent mock data based on context
        
        competitor_moves = []
        if context.industry == IndustryType.B2B_SAAS:
            competitor_moves = [
                {"company": "Competitor A", "action": "raised_series_b", "amount": 50000000, "date": "2024-01-15"},
                {"company": "Competitor B", "action": "acquired_startup", "target": "AI Tool Co", "date": "2024-02-01"},
                {"company": "Competitor C", "action": "launched_feature", "feature": "AI Assistant", "date": "2024-02-15"}
            ]
            
        industry_trends = []
        if "AI" in str(context.goals) or "automation" in str(context.goals):
            industry_trends = [
                {"trend": "ai_adoption", "growth_rate": 0.35, "adoption_stage": "early_majority"},
                {"trend": "automation_first", "growth_rate": 0.28, "adoption_stage": "early_adopters"},
                {"trend": "no_code_tools", "growth_rate": 0.42, "adoption_stage": "innovators"}
            ]
            
        market_signals = {
            "investor_interest": 0.75 if context.stage in [BusinessStage.MVP, BusinessStage.GROWTH] else 0.5,
            "talent_availability": 0.6 if context.industry in [IndustryType.B2B_SAAS, IndustryType.FINTECH] else 0.8,
            "customer_demand": 0.85 if context.stage == BusinessStage.PRODUCT_MARKET_FIT else 0.65,
            "competitive_intensity": min(0.9, 0.3 + (len(competitor_moves) * 0.1)),
            "regulatory_risk": 0.7 if context.industry == IndustryType.FINTECH else 0.3
        }
        
        return MarketIntelligence(
            competitor_moves=competitor_moves,
            industry_trends=industry_trends,
            regulatory_changes=[],
            funding_rounds=competitor_moves,  # Simplified
            market_signals=market_signals,
            technology_shifts=["ai_transformation", "api_economy", "sustainability_focus"],
            customer_sentiment={"satisfaction": 0.72, "loyalty": 0.65, "advocacy": 0.58}
        )
        
    def analyze_company_dna(
        self,
        context: StartupContext,
        assessment_data: Dict[str, Any]
    ) -> CompanyDNA:
        """Deep analysis of company's unique characteristics"""
        
        # Culture indicators based on team and goals
        culture_indicators = {
            "innovation_focus": 0.8 if "innovation" in str(context.goals).lower() else 0.5,
            "customer_centricity": 0.85 if ChallengeType.RETENTION in context.primary_challenges else 0.6,
            "data_driven": 0.9 if "analytics" in str(context.existing_frameworks) else 0.4,
            "agility": 0.8 if context.team_size < 50 else 0.5,
            "risk_appetite": 0.7 if context.stage in [BusinessStage.IDEA, BusinessStage.MVP] else 0.4
        }
        
        # Innovation velocity based on product stage and timeline
        innovation_velocity = 0.8 if context.stage == BusinessStage.MVP else 0.6
        
        # Execution capability based on team size and experience
        execution_capability = min(0.9, 0.5 + (context.team_size / 100))
        
        # Market timing score
        market_timing_score = 0.75  # Would be calculated from market intelligence
        
        # Competitive moat strength
        moat_indicators = assessment_data.get("advantage", {})
        competitive_moat_strength = 0.3
        if moat_indicators.get("proprietaryTech"):
            competitive_moat_strength += 0.2
        if moat_indicators.get("networkEffects"):
            competitive_moat_strength += 0.2
        if moat_indicators.get("patentsFiled", 0) > 0:
            competitive_moat_strength += 0.1
        if moat_indicators.get("exclusivePartnerships"):
            competitive_moat_strength += 0.2
            
        return CompanyDNA(
            culture_indicators=culture_indicators,
            innovation_velocity=innovation_velocity,
            execution_capability=execution_capability,
            market_timing_score=market_timing_score,
            founder_profiles=[],  # Would be enriched from LinkedIn/other sources
            tech_stack_sophistication=0.7,  # Would analyze actual tech stack
            customer_love_score=0.75,  # Would be from NPS/reviews
            competitive_moat_strength=competitive_moat_strength
        )
        
    def calculate_framework_timing_score(
        self,
        framework: Framework,
        market_intel: MarketIntelligence,
        company_dna: CompanyDNA
    ) -> float:
        """Calculate how timely a framework is given current conditions"""
        score = 0.5  # Base score
        
        # Market momentum alignment
        if framework.category == FrameworkCategory.GROWTH:
            if market_intel.market_signals.get("customer_demand", 0) > 0.7:
                score += 0.2
                
        # Competitive pressure alignment
        if framework.category == FrameworkCategory.STRATEGY:
            if market_intel.market_signals.get("competitive_intensity", 0) > 0.7:
                score += 0.15
                
        # Innovation timing
        if framework.category == FrameworkCategory.INNOVATION:
            if company_dna.market_timing_score > 0.7:
                score += 0.25
                
        # Resource availability
        if framework.complexity == ComplexityLevel.ADVANCED:
            if company_dna.execution_capability < 0.5:
                score -= 0.2
                
        return max(0.1, min(1.0, score))
        
    def generate_framework_customizations(
        self,
        framework: Framework,
        context: StartupContext,
        company_dna: CompanyDNA,
        market_intel: MarketIntelligence
    ) -> List[str]:
        """Generate specific customizations for framework application"""
        customizations = []
        
        # Stage-specific customizations
        if context.stage == BusinessStage.MVP:
            if framework.id == "lean_startup":
                customizations.append("Focus on single core hypothesis validation before expanding")
                customizations.append("Set 2-week experiment cycles with clear kill criteria")
                
        # Industry-specific customizations
        if context.industry == IndustryType.B2B_SAAS:
            if framework.id == "aarrr_metrics":
                customizations.append("Emphasize activation rate given B2B complexity")
                customizations.append("Track feature adoption as proxy for retention")
                
        # Culture-specific customizations
        if company_dna.culture_indicators.get("data_driven", 0) < 0.5:
            customizations.append("Start with qualitative insights before quantitative metrics")
            customizations.append("Build data culture alongside framework implementation")
            
        # Market condition customizations
        if market_intel.market_signals.get("competitive_intensity", 0) > 0.8:
            if framework.category == FrameworkCategory.STRATEGY:
                customizations.append("Accelerate implementation timeline by 30%")
                customizations.append("Focus on differentiation over cost optimization")
                
        # Resource constraint customizations
        if context.team_size < 10:
            customizations.append("Combine roles where possible (e.g., PM also does analysis)")
            customizations.append("Use lightweight tools and automation")
            
        return customizations
        
    async def recommend_frameworks_enhanced(
        self,
        context: StartupContext,
        assessment_data: Dict[str, Any],
        max_recommendations: int = 10
    ) -> List[EnhancedRecommendation]:
        """Enhanced framework recommendation with intelligence layers"""
        
        # Gather intelligence concurrently
        market_intel_task = asyncio.create_task(self.get_market_intelligence(context))
        company_dna = self.analyze_company_dna(context, assessment_data)
        market_intel = await market_intel_task
        
        # Score all frameworks with enhanced algorithm
        framework_scores = {}
        
        for framework_id, framework in FRAMEWORKS.items():
            # Base scoring (similar to original)
            base_score = self._calculate_base_score(framework, context)
            
            # ML-enhanced scoring
            ml_features = self._extract_ml_features(framework, context, company_dna)
            ml_score = self.ml_model.predict_success(ml_features)
            
            # Timing score
            timing_score = self.calculate_framework_timing_score(
                framework, market_intel, company_dna
            )
            
            # Combined score with weights
            combined_score = (
                base_score * 0.3 +
                ml_score * 0.4 +
                timing_score * 0.3
            )
            
            framework_scores[framework_id] = {
                "score": combined_score,
                "base": base_score,
                "ml": ml_score,
                "timing": timing_score
            }
            
        # Sort and get top candidates
        sorted_frameworks = sorted(
            framework_scores.items(),
            key=lambda x: x[1]["score"],
            reverse=True
        )
        
        # Filter out duplicate framework patterns (e.g., multiple Innovation Pipelines)
        seen_patterns = set()
        filtered_frameworks = []
        
        for framework_id, scores in sorted_frameworks:
            framework = get_framework_by_id(framework_id)
            # Create a pattern key from the base name (remove industry suffixes)
            base_name = framework.name.split('(')[0].strip()
            pattern_key = (base_name, framework.category)
            
            # Only keep the first occurrence of each pattern
            if pattern_key not in seen_patterns:
                seen_patterns.add(pattern_key)
                filtered_frameworks.append((framework_id, scores))
                
            if len(filtered_frameworks) >= max_recommendations * 2:
                break
        
        sorted_frameworks = filtered_frameworks
        
        # Ensure category diversity before synergy optimization
        category_balanced = self._ensure_category_diversity(
            sorted_frameworks, max_recommendations
        )
        
        # Optimize for synergies
        optimized_set = self._optimize_framework_synergies(
            category_balanced, max_recommendations
        )
        
        # Create enhanced recommendations
        recommendations = []
        for framework_id, scores in optimized_set:
            framework = get_framework_by_id(framework_id)
            
            # Calculate synergy with other selected frameworks
            synergy_score = self._calculate_synergy_score(
                framework_id, [f[0] for f in optimized_set if f[0] != framework_id]
            )
            
            # Generate customizations
            customizations = self.generate_framework_customizations(
                framework, context, company_dna, market_intel
            )
            
            # Identify quick wins
            quick_wins = self._identify_quick_wins(framework, context, company_dna)
            
            # Create integration plan
            integration_plan = self._create_integration_plan(
                framework, context, [f[0] for f in optimized_set]
            )
            
            recommendation = EnhancedRecommendation(
                framework=framework,
                relevance_score=scores["score"],
                confidence_level=self._calculate_confidence(scores),
                synergy_score=synergy_score,
                timing_score=scores["timing"],
                customizations=customizations,
                success_probability=scores["ml"],
                risk_factors=self._identify_risks(framework, context, market_intel),
                quick_wins=quick_wins,
                integration_plan=integration_plan
            )
            
            recommendations.append(recommendation)
            
        return recommendations
        
    def _calculate_base_score(
        self,
        framework: Framework,
        context: StartupContext
    ) -> float:
        """Calculate base relevance score (original algorithm)"""
        score = 0.0
        
        # Stage relevance (25% weight)
        if framework.id in self.stage_frameworks.get(context.stage, []):
            score += 0.25
            
        # Challenge relevance (30% weight)
        challenge_matches = 0
        for challenge in context.primary_challenges:
            if framework.id in self.challenge_frameworks.get(challenge, []):
                challenge_matches += 1
        if challenge_matches > 0:
            score += 0.30 * (challenge_matches / len(context.primary_challenges))
            
        # Industry relevance (15% weight)
        industry_keywords = context.industry.value.lower().split()
        for keyword in industry_keywords:
            for relevance in framework.industry_relevance:
                if keyword in relevance.lower() or "all industries" in relevance.lower():
                    score += 0.15
                    break
                    
        # Complexity match (10% weight)
        complexity_diff = abs(framework.complexity.value - context.complexity_preference.value)
        complexity_score = 0.10 * (1 - complexity_diff / 3)
        score += complexity_score
            
        # Goal alignment (10% weight)
        goal_matches = 0
        for goal in context.goals:
            goal_lower = goal.lower()
            if (goal_lower in framework.description.lower() or
                any(goal_lower in outcome.lower() for outcome in framework.expected_outcomes)):
                goal_matches += 1
                
        if goal_matches > 0:
            score += 0.10 * (goal_matches / len(context.goals))
            
        # Time constraint match (5% weight)
        if framework.time_to_implement and hasattr(context, 'time_constraint'):
            time_constraint = getattr(context, 'time_constraint', '3-6 months')
            if self._time_fits_constraint(framework.time_to_implement, time_constraint):
                score += 0.05
                
        # Complementary to existing frameworks (5% weight)
        if context.existing_frameworks:
            for existing_id in context.existing_frameworks:
                existing = get_framework_by_id(existing_id)
                if existing and framework.id in (existing.complementary_frameworks or []):
                    score += 0.05
                    break
                    
        return score
        
    def _extract_ml_features(
        self,
        framework: Framework,
        context: StartupContext,
        company_dna: CompanyDNA
    ) -> Dict[str, float]:
        """Extract features for ML model"""
        # Map stage to complexity level for comparison
        stage_complexity_map = {
            BusinessStage.IDEA: 1,
            BusinessStage.MVP: 2,
            BusinessStage.PRODUCT_MARKET_FIT: 2,
            BusinessStage.GROWTH: 3,
            BusinessStage.SCALE: 3,
            BusinessStage.MATURE: 4
        }
        
        features = {
            "stage_match": 1.0 if framework.complexity.value <= stage_complexity_map.get(context.stage, 2) else 0.5,
            "challenge_alignment": len(set(framework.when_to_use) & set(str(c) for c in context.primary_challenges)) / max(len(context.primary_challenges), 1),
            "resource_fit": 1.0 if context.team_size >= 10 or framework.complexity == ComplexityLevel.BASIC else 0.5,
            "culture_alignment": company_dna.culture_indicators.get("innovation_focus", 0.5) if framework.category == FrameworkCategory.INNOVATION else 0.7,
            "execution_readiness": company_dna.execution_capability,
            "timing_fit": company_dna.market_timing_score
        }
        return features
        
    def _optimize_framework_synergies(
        self,
        candidates: List[Tuple[str, Dict[str, float]]],
        max_count: int
    ) -> List[Tuple[str, Dict[str, float]]]:
        """Optimize framework selection for maximum synergy"""
        if len(candidates) <= max_count:
            return candidates
            
        # Dynamic programming approach to find optimal combination
        selected = [candidates[0]]  # Start with highest scored
        
        while len(selected) < max_count and len(candidates) > len(selected):
            best_addition = None
            best_synergy = -float('inf')
            
            for candidate in candidates:
                if candidate in selected:
                    continue
                    
                total_synergy = sum(
                    self.synergy_matrix.get((candidate[0], s[0]), 0)
                    for s in selected
                )
                
                if total_synergy > best_synergy:
                    best_synergy = total_synergy
                    best_addition = candidate
                    
            if best_addition:
                selected.append(best_addition)
            else:
                # No positive synergy found, add by score
                for candidate in candidates:
                    if candidate not in selected:
                        selected.append(candidate)
                        break
                        
        return selected[:max_count]
        
    def _calculate_synergy_score(
        self,
        framework_id: str,
        other_framework_ids: List[str]
    ) -> float:
        """Calculate total synergy score with other frameworks"""
        if not other_framework_ids:
            return 0.5
            
        total_synergy = sum(
            self.synergy_matrix.get((framework_id, other_id), 0)
            for other_id in other_framework_ids
        )
        
        # Normalize to 0-1 range
        max_possible = len(other_framework_ids)
        return (total_synergy + max_possible) / (2 * max_possible)
        
    def _calculate_confidence(self, scores: Dict[str, float]) -> float:
        """Calculate confidence level in recommendation"""
        # High confidence if all scores align
        score_variance = np.var([scores["base"], scores["ml"], scores["timing"]])
        base_confidence = 1.0 - min(score_variance * 2, 0.5)
        
        # Boost confidence if score is very high
        if scores["score"] > 0.8:
            base_confidence = min(base_confidence + 0.1, 0.95)
            
        return base_confidence
        
    def _identify_quick_wins(
        self,
        framework: Framework,
        context: StartupContext,
        company_dna: CompanyDNA
    ) -> List[str]:
        """Identify quick wins possible with this framework"""
        quick_wins = []
        
        if framework.id == "okr_framework":
            quick_wins.append("Align team on top 3 objectives within 1 week")
            quick_wins.append("Improve focus by dropping 50% of current initiatives")
            
        elif framework.id == "aarrr_metrics":
            quick_wins.append("Identify biggest drop-off in funnel within 3 days")
            quick_wins.append("Implement one retention experiment in week 1")
            
        elif framework.id == "jobs_to_be_done":
            quick_wins.append("Interview 5 customers this week for job insights")
            quick_wins.append("Identify one underserved job to prototype")
            
        # Add context-specific quick wins
        if context.stage == BusinessStage.MVP:
            quick_wins.append("Validate core assumption with 20 users")
            
        return quick_wins[:3]  # Limit to top 3
        
    def _identify_risks(
        self,
        framework: Framework,
        context: StartupContext,
        market_intel: MarketIntelligence
    ) -> List[str]:
        """Identify implementation risks"""
        risks = []
        
        # Complexity risks
        if framework.complexity.value > context.complexity_preference.value:
            risks.append(f"Framework complexity exceeds team's current capability")
            
        # Timing risks
        if market_intel.market_signals.get("competitive_intensity", 0) > 0.8:
            if framework.time_to_implement and "months" in framework.time_to_implement:
                risks.append("Long implementation time in fast-moving market")
                
        # Resource risks
        if context.team_size < 10 and framework.complexity == ComplexityLevel.ADVANCED:
            risks.append("Insufficient team size for proper implementation")
            
        # Market risks
        if framework.category == FrameworkCategory.GROWTH:
            if market_intel.market_signals.get("customer_demand", 0) < 0.5:
                risks.append("Growth framework in low-demand market")
                
        return risks
        
    def _create_integration_plan(
        self,
        framework: Framework,
        context: StartupContext,
        other_frameworks: List[str]
    ) -> Dict[str, Any]:
        """Create integration plan with other frameworks"""
        plan = {
            "sequence": 1,  # Default
            "dependencies": [],
            "parallel_frameworks": [],
            "integration_points": [],
            "resource_allocation": {}
        }
        
        # Determine sequencing
        if framework.category == FrameworkCategory.STRATEGY:
            plan["sequence"] = 1  # Strategy first
        elif framework.category == FrameworkCategory.OPERATIONS:
            plan["sequence"] = 3  # Operations after strategy
            
        # Identify dependencies
        if framework.id == "balanced_scorecard":
            if "okr_framework" in other_frameworks:
                plan["dependencies"].append("okr_framework")
                plan["integration_points"].append(
                    "Use OKRs as input for balanced scorecard perspectives"
                )
                
        # Identify parallel opportunities
        if framework.category == FrameworkCategory.GROWTH:
            for other in other_frameworks:
                other_framework = get_framework_by_id(other)
                if other_framework and other_framework.category == FrameworkCategory.MARKETING:
                    plan["parallel_frameworks"].append(other)
                    
        # Resource allocation
        total_resources = 100
        framework_count = len(other_frameworks) + 1
        base_allocation = total_resources / framework_count
        
        # Adjust based on complexity
        if framework.complexity == ComplexityLevel.ADVANCED:
            plan["resource_allocation"]["percentage"] = base_allocation * 1.5
        else:
            plan["resource_allocation"]["percentage"] = base_allocation
            
        plan["resource_allocation"]["team_members"] = max(
            1, int(context.team_size * plan["resource_allocation"]["percentage"] / 100)
        )
        
        return plan
        
    def _time_fits_constraint(self, framework_time: str, constraint_time: str) -> bool:
        """Check if framework implementation time fits within constraints"""
        framework_months = self._extract_months(framework_time)
        constraint_months = self._extract_months(constraint_time)
        
        return framework_months <= constraint_months
        
    def _extract_months(self, time_string: str) -> int:
        """Extract number of months from time string"""
        import re
        
        # Try range pattern first
        range_match = re.search(r'(\d+)-(\d+)\s*months?', time_string.lower())
        if range_match:
            return int(range_match.group(2))  # Return upper bound
            
        # Try single number pattern
        single_match = re.search(r'(\d+)\s*months?', time_string.lower())
        if single_match:
            return int(single_match.group(1))
            
        # Try weeks pattern and convert
        weeks_match = re.search(r'(\d+)\s*weeks?', time_string.lower())
        if weeks_match:
            return int(weeks_match.group(1)) // 4
            
        # Default to 3 months if can't parse
        return 3
        
    def find_framework_combinations(
        self,
        context: StartupContext,
        max_combinations: int = 5
    ) -> List[List[Framework]]:
        """Find synergistic framework combinations"""
        from collections import defaultdict
        
        recommendations = asyncio.run(self.recommend_frameworks_enhanced(context, {}, max_recommendations=20))
        
        combinations = []
        
        # Method 1: Complementary frameworks
        for rec in recommendations[:10]:
            if rec.framework.complementary_frameworks:
                combo = [rec.framework]
                for comp_id in rec.framework.complementary_frameworks[:2]:
                    comp_framework = get_framework_by_id(comp_id)
                    if comp_framework:
                        combo.append(comp_framework)
                if len(combo) > 1:
                    combinations.append(combo)
                    
        # Method 2: Category-based combinations
        category_groups = defaultdict(list)
        for rec in recommendations[:15]:
            category_groups[rec.framework.category].append(rec.framework)
            
        # Create cross-category combinations
        priority_categories = [
            FrameworkCategory.STRATEGY,
            FrameworkCategory.GROWTH,
            FrameworkCategory.PRODUCT,
            FrameworkCategory.OPERATIONS
        ]
        
        for i, cat1 in enumerate(priority_categories):
            for cat2 in priority_categories[i+1:]:
                if cat1 in category_groups and cat2 in category_groups:
                    combo = [
                        category_groups[cat1][0],
                        category_groups[cat2][0]
                    ]
                    combinations.append(combo)
                    
        # Remove duplicates and limit
        unique_combos = []
        seen = set()
        
        for combo in combinations:
            combo_ids = tuple(sorted(f.id for f in combo))
            if combo_ids not in seen:
                seen.add(combo_ids)
                unique_combos.append(combo)
                
        return unique_combos[:max_combinations]
        
    def _ensure_category_diversity(
        self,
        sorted_frameworks: List[Tuple[str, Dict[str, float]]],
        max_count: int
    ) -> List[Tuple[str, Dict[str, float]]]:
        """Ensure diverse representation of framework categories"""
        # Priority categories for balanced recommendations
        priority_categories = [
            FrameworkCategory.STRATEGY,
            FrameworkCategory.GROWTH,
            FrameworkCategory.PRODUCT,
            FrameworkCategory.OPERATIONS,
            FrameworkCategory.MARKETING,
            FrameworkCategory.INNOVATION,
            FrameworkCategory.ORGANIZATIONAL,
            FrameworkCategory.FINANCIAL
        ]
        
        # Track selections per category
        category_selections = defaultdict(list)
        selected = []
        
        # First pass: Take top framework from each priority category
        for category in priority_categories:
            for framework_id, scores in sorted_frameworks:
                if (framework_id, scores) not in selected:
                    framework = get_framework_by_id(framework_id)
                    if framework and framework.category == category:
                        selected.append((framework_id, scores))
                        category_selections[category].append((framework_id, scores))
                        break
            
            if len(selected) >= max_count:
                break
        
        # Second pass: Fill remaining slots with highest scoring frameworks
        if len(selected) < max_count:
            for framework_id, scores in sorted_frameworks:
                if (framework_id, scores) not in selected:
                    framework = get_framework_by_id(framework_id)
                    # Limit to 2 per category to maintain diversity
                    if len(category_selections[framework.category]) < 2:
                        selected.append((framework_id, scores))
                        category_selections[framework.category].append((framework_id, scores))
                        
                        if len(selected) >= max_count:
                            break
        
        return selected[:max_count]


# Public API functions

async def get_intelligent_recommendations(
    stage: str,
    industry: str,
    team_size: int,
    funding_stage: str,
    challenges: List[str],
    goals: List[str],
    assessment_data: Dict[str, Any],
    existing_frameworks: List[str] = None
) -> List[Dict[str, Any]]:
    """
    Get intelligent framework recommendations with ML and market intelligence
    """
    # Convert inputs to enums
    business_stage = BusinessStage[stage.upper().replace(" ", "_")]
    industry_type = IndustryType[industry.upper().replace(" ", "_")]
    challenge_types = [ChallengeType[c.upper().replace(" ", "_")] for c in challenges]
    
    # Create context
    context = StartupContext(
        stage=business_stage,
        industry=industry_type,
        team_size=team_size,
        funding_stage=funding_stage,
        primary_challenges=challenge_types,
        goals=goals,
        constraints=[],
        existing_frameworks=existing_frameworks
    )
    
    # Get enhanced recommendations
    selector = EnhancedFrameworkSelector()
    recommendations = await selector.recommend_frameworks_enhanced(
        context, assessment_data
    )
    
    # Convert to API format
    results = []
    for i, rec in enumerate(recommendations):
        results.append({
            "framework_name": rec.framework.name,
            "framework_id": rec.framework.id,
            "category": rec.framework.category.value,
            "relevance_score": round(rec.relevance_score, 3),
            "confidence_level": round(rec.confidence_level, 2),
            "synergy_score": round(rec.synergy_score, 2),
            "timing_score": round(rec.timing_score, 2),
            "success_probability": round(rec.success_probability, 2),
            "customizations": rec.customizations,
            "quick_wins": rec.quick_wins,
            "risk_factors": rec.risk_factors,
            "integration_plan": rec.integration_plan,
            "implementation_order": i + 1,
            "complexity": rec.framework.complexity.name,
            "time_to_implement": rec.framework.time_to_implement,
            "description": rec.framework.description,
            "key_components": rec.framework.key_components,
            "expected_outcomes": rec.framework.expected_outcomes
        })
        
    return results


def get_framework_combination_insights(
    framework_ids: List[str]
) -> Dict[str, Any]:
    """
    Get insights on how frameworks work together
    """
    selector = EnhancedFrameworkSelector()
    insights = {
        "total_synergy": 0,
        "conflicts": [],
        "reinforcements": [],
        "implementation_order": [],
        "resource_optimization": {}
    }
    
    # Calculate pairwise synergies
    for i, f1 in enumerate(framework_ids):
        for f2 in framework_ids[i+1:]:
            synergy = selector.synergy_matrix.get((f1, f2), 0)
            insights["total_synergy"] += synergy
            
            if synergy < -0.2:
                insights["conflicts"].append({
                    "framework1": f1,
                    "framework2": f2,
                    "reason": "Conflicting methodologies",
                    "resolution": "Choose one as primary, other as secondary"
                })
            elif synergy > 0.7:
                insights["reinforcements"].append({
                    "framework1": f1,
                    "framework2": f2,
                    "benefit": "Strong complementary effects",
                    "integration": "Implement in parallel for maximum benefit"
                })
                
    # Determine optimal implementation order
    strategy_frameworks = [f for f in framework_ids if "strategy" in f or "swot" in f]
    operational_frameworks = [f for f in framework_ids if "operations" in f or "process" in f]
    growth_frameworks = [f for f in framework_ids if "growth" in f or "marketing" in f]
    
    insights["implementation_order"] = (
        strategy_frameworks + 
        operational_frameworks + 
        growth_frameworks +
        [f for f in framework_ids if f not in strategy_frameworks + operational_frameworks + growth_frameworks]
    )
    
    return insights