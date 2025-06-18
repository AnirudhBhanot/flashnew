"""
Framework Selector - AI-powered framework recommendation engine

This module provides intelligent framework selection based on startup context,
business challenges, and strategic goals.
"""

import json
from typing import List, Dict, Optional, Tuple, Set
from dataclasses import dataclass
from enum import Enum
import re
from collections import defaultdict

from .framework_database import (
    Framework, FrameworkCategory, ComplexityLevel,
    get_framework_by_id, get_frameworks_by_category,
    search_frameworks, get_complementary_frameworks,
    FRAMEWORKS
)


class BusinessStage(Enum):
    """Startup/Business development stages"""
    IDEA = "Idea Stage"
    MVP = "MVP Stage"
    PRODUCT_MARKET_FIT = "Product-Market Fit"
    GROWTH = "Growth Stage"
    SCALE = "Scale Stage"
    MATURE = "Mature Stage"


class IndustryType(Enum):
    """Industry classifications"""
    B2B_SAAS = "B2B SaaS"
    B2C_SAAS = "B2C SaaS"
    ECOMMERCE = "E-commerce"
    MARKETPLACE = "Marketplace"
    FINTECH = "FinTech"
    HEALTHTECH = "HealthTech"
    EDTECH = "EdTech"
    ENTERPRISE = "Enterprise Software"
    CONSUMER = "Consumer Products"
    HARDWARE = "Hardware"
    DEEPTECH = "Deep Tech"
    SERVICES = "Professional Services"
    RETAIL = "Retail"
    MANUFACTURING = "Manufacturing"
    TECHNOLOGY = "Technology"
    REAL_ESTATE = "Real Estate"
    LOGISTICS = "Logistics & Transportation"
    CLEANTECH = "Clean Technology"
    OTHER = "Other"


class ChallengeType(Enum):
    """Common business challenges"""
    CUSTOMER_ACQUISITION = "Customer Acquisition"
    RETENTION = "Customer Retention"
    PRODUCT_DEVELOPMENT = "Product Development"
    MARKET_ENTRY = "Market Entry"
    COMPETITIVE_PRESSURE = "Competitive Pressure"
    SCALING = "Scaling Operations"
    FUNDING = "Fundraising"
    TEAM_BUILDING = "Team Building"
    CULTURE = "Culture Development"
    INNOVATION = "Innovation"
    COST_OPTIMIZATION = "Cost Optimization"
    STRATEGIC_PLANNING = "Strategic Planning"
    DIGITAL_TRANSFORMATION = "Digital Transformation"
    QUALITY_ISSUES = "Quality Issues"
    OPERATIONAL_EFFICIENCY = "Operational Efficiency"
    MARKET_PENETRATION = "Market Penetration"
    COMPETITION = "Competition"
    TALENT_ACQUISITION = "Talent Acquisition"
    REGULATORY_COMPLIANCE = "Regulatory Compliance"


@dataclass
class StartupContext:
    """Context information about the startup"""
    stage: BusinessStage
    industry: IndustryType
    team_size: int
    funding_stage: str
    primary_challenges: List[ChallengeType]
    goals: List[str]
    constraints: List[str]
    existing_frameworks: List[str] = None
    complexity_preference: ComplexityLevel = ComplexityLevel.INTERMEDIATE
    time_constraint: str = "3-6 months"
    

@dataclass
class FrameworkRecommendation:
    """Framework recommendation with rationale"""
    framework: Framework
    relevance_score: float
    rationale: List[str]
    implementation_order: int
    prerequisites_met: bool
    estimated_impact: str
    risk_level: str
    

class FrameworkSelector:
    """Intelligent framework selector and recommender"""
    
    def __init__(self):
        self.framework_patterns = self._initialize_patterns()
        self.stage_frameworks = self._initialize_stage_mappings()
        self.challenge_frameworks = self._initialize_challenge_mappings()
        
    def _initialize_patterns(self) -> Dict[str, List[str]]:
        """Initialize keyword patterns for framework matching"""
        return {
            "growth": ["aarrr_metrics", "growth_loops", "product_led_growth", "viral_coefficient"],
            "strategy": ["swot_analysis", "porters_five_forces", "blue_ocean_strategy", "ansoff_matrix"],
            "innovation": ["design_thinking", "lean_startup", "jobs_to_be_done", "open_innovation"],
            "operations": ["lean_methodology", "six_sigma", "agile_methodology", "supply_chain_optimization"],
            "financial": ["unit_economics", "ltv_cac_ratio", "burn_rate_runway", "saas_metrics"],
            "marketing": ["marketing_mix_4ps", "stp_marketing", "customer_journey_mapping", "content_marketing_framework"],
            "product": ["kano_model", "rice_prioritization", "product_market_fit", "mvp_framework"],
            "leadership": ["situational_leadership", "transformational_leadership", "servant_leadership"],
            "organizational": ["mckinsey_7s", "organizational_culture", "balanced_scorecard", "okr_framework"]
        }
        
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
        ,
            ChallengeType.MARKET_PENETRATION: [
                "ansoff_matrix", "blue_ocean_strategy", "market_segmentation",
                "go_to_market_strategy", "beachhead_strategy"
            ],
            ChallengeType.COMPETITION: [
                "porters_five_forces", "competitive_positioning", "blue_ocean_strategy",
                "differentiation_strategy", "swot_analysis"
            ],
            ChallengeType.TALENT_ACQUISITION: [
                "employer_branding", "talent_pipeline", "recruitment_funnel",
                "competency_framework", "organizational_culture"
            ],
            ChallengeType.REGULATORY_COMPLIANCE: [
                "compliance_framework", "risk_management_framework", "governance_framework",
                "regulatory_mapping", "audit_framework"
            ]
        }
        
    def recommend_frameworks(
        self,
        context: StartupContext,
        max_recommendations: int = 10
    ) -> List[FrameworkRecommendation]:
        """Recommend frameworks based on startup context"""
        
        # Score all frameworks
        framework_scores = {}
        framework_rationales = {}
        
        for framework_id, framework in FRAMEWORKS.items():
            score, rationale = self._score_framework(framework, context)
            framework_scores[framework_id] = score
            framework_rationales[framework_id] = rationale
            
        # Sort by score and get top recommendations
        sorted_frameworks = sorted(
            framework_scores.items(),
            key=lambda x: x[1],
            reverse=True
        )[:max_recommendations]
        
        # Create recommendations
        recommendations = []
        for i, (framework_id, score) in enumerate(sorted_frameworks):
            if score > 0:  # Only include relevant frameworks
                framework = get_framework_by_id(framework_id)
                recommendation = FrameworkRecommendation(
                    framework=framework,
                    relevance_score=score,
                    rationale=framework_rationales[framework_id],
                    implementation_order=i + 1,
                    prerequisites_met=self._check_prerequisites(framework, context),
                    estimated_impact=self._estimate_impact(framework, context),
                    risk_level=self._assess_risk(framework, context)
                )
                recommendations.append(recommendation)
                
        return recommendations
        
    def _score_framework(
        self,
        framework: Framework,
        context: StartupContext
    ) -> Tuple[float, List[str]]:
        """Score a framework's relevance to the context"""
        score = 0.0
        rationale = []
        
        # Stage relevance (25% weight)
        if framework.id in self.stage_frameworks.get(context.stage, []):
            score += 0.25
            rationale.append(f"Highly relevant for {context.stage.value}")
            
        # Challenge relevance (30% weight)
        challenge_matches = 0
        for challenge in context.primary_challenges:
            if framework.id in self.challenge_frameworks.get(challenge, []):
                challenge_matches += 1
                rationale.append(f"Addresses {challenge.value}")
        if challenge_matches > 0:
            score += 0.30 * (challenge_matches / len(context.primary_challenges))
            
        # Industry relevance (15% weight)
        industry_keywords = context.industry.value.lower().split()
        for keyword in industry_keywords:
            for relevance in framework.industry_relevance:
                if keyword in relevance.lower() or "all industries" in relevance.lower():
                    score += 0.15
                    rationale.append(f"Applicable to {context.industry.value}")
                    break
                    
        # Complexity match (10% weight)
        complexity_diff = abs(framework.complexity.value - context.complexity_preference.value)
        complexity_score = 0.10 * (1 - complexity_diff / 3)
        score += complexity_score
        if complexity_score > 0.05:
            rationale.append(f"Appropriate complexity level")
            
        # Goal alignment (10% weight)
        goal_matches = 0
        for goal in context.goals:
            goal_lower = goal.lower()
            if (goal_lower in framework.description.lower() or
                any(goal_lower in outcome.lower() for outcome in framework.expected_outcomes)):
                goal_matches += 1
                
        if goal_matches > 0:
            score += 0.10 * (goal_matches / len(context.goals))
            rationale.append(f"Aligns with {goal_matches} stated goal(s)")
            
        # Time constraint match (5% weight)
        if framework.time_to_implement:
            if self._time_fits_constraint(framework.time_to_implement, context.time_constraint):
                score += 0.05
                rationale.append("Fits within time constraints")
                
        # Complementary to existing frameworks (5% weight)
        if context.existing_frameworks:
            for existing_id in context.existing_frameworks:
                existing = get_framework_by_id(existing_id)
                if existing and framework.id in (existing.complementary_frameworks or []):
                    score += 0.05
                    rationale.append(f"Complements {existing.name}")
                    break
                    
        return score, rationale
        
    def _check_prerequisites(self, framework: Framework, context: StartupContext) -> bool:
        """Check if prerequisites are likely met"""
        if not framework.prerequisites:
            return True
            
        # Simple heuristic checks
        prerequisites_met = 0
        total_prerequisites = len(framework.prerequisites)
        
        for prereq in framework.prerequisites:
            prereq_lower = prereq.lower()
            
            # Check team size requirements
            if "team" in prereq_lower:
                if context.team_size > 5:
                    prerequisites_met += 1
                    
            # Check funding/resources
            elif "resources" in prereq_lower or "budget" in prereq_lower:
                if context.funding_stage not in ["Pre-seed", "Bootstrapped"]:
                    prerequisites_met += 1
                    
            # Check data/analytics
            elif "data" in prereq_lower or "analytics" in prereq_lower:
                if context.stage.value not in [BusinessStage.IDEA.value, BusinessStage.MVP.value]:
                    prerequisites_met += 1
                    
            # Default: assume 70% chance of meeting unknown prerequisites
            else:
                prerequisites_met += 0.7
                
        return prerequisites_met / total_prerequisites >= 0.7
        
    def _estimate_impact(self, framework: Framework, context: StartupContext) -> str:
        """Estimate potential impact of framework"""
        # Calculate impact based on challenge severity and framework effectiveness
        impact_score = 0
        
        # Check if framework addresses primary challenges
        for challenge in context.primary_challenges:
            if framework.id in self.challenge_frameworks.get(challenge, []):
                impact_score += 2
                
        # Consider business stage alignment
        if framework.id in self.stage_frameworks.get(context.stage, []):
            impact_score += 1
            
        # Factor in expected outcomes
        if len(framework.expected_outcomes) >= 5:
            impact_score += 1
            
        # Categorize impact
        if impact_score >= 4:
            return "High"
        elif impact_score >= 2:
            return "Medium"
        else:
            return "Low"
            
    def _assess_risk(self, framework: Framework, context: StartupContext) -> str:
        """Assess implementation risk"""
        risk_score = 0
        
        # Complexity risk
        if framework.complexity.value > context.complexity_preference.value:
            risk_score += 2
            
        # Resource risk
        if context.team_size < 10 and framework.complexity == ComplexityLevel.ADVANCED:
            risk_score += 1
            
        # Time risk
        if framework.time_to_implement:
            if "months" in framework.time_to_implement:
                months = self._extract_months(framework.time_to_implement)
                if months > 6:
                    risk_score += 1
                    
        # Prerequisites risk
        if not self._check_prerequisites(framework, context):
            risk_score += 2
            
        # Categorize risk
        if risk_score >= 4:
            return "High"
        elif risk_score >= 2:
            return "Medium"
        else:
            return "Low"
            
    def _time_fits_constraint(self, framework_time: str, constraint_time: str) -> bool:
        """Check if framework implementation time fits within constraints"""
        framework_months = self._extract_months(framework_time)
        constraint_months = self._extract_months(constraint_time)
        
        return framework_months <= constraint_months
        
    def _extract_months(self, time_string: str) -> int:
        """Extract number of months from time string"""
        # Look for patterns like "3-6 months", "12 months", etc.
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
        
    def create_implementation_roadmap(
        self,
        recommendations: List[FrameworkRecommendation]
    ) -> Dict[str, List[FrameworkRecommendation]]:
        """Create phased implementation roadmap"""
        roadmap = {
            "Phase 1 (0-3 months)": [],
            "Phase 2 (3-6 months)": [],
            "Phase 3 (6-12 months)": [],
            "Phase 4 (12+ months)": []
        }
        
        # Sort by implementation order and complexity
        sorted_recs = sorted(
            recommendations,
            key=lambda x: (x.implementation_order, x.framework.complexity.value)
        )
        
        # Assign to phases based on complexity and dependencies
        for rec in sorted_recs:
            if rec.framework.complexity == ComplexityLevel.BASIC:
                if len(roadmap["Phase 1 (0-3 months)"]) < 3:
                    roadmap["Phase 1 (0-3 months)"].append(rec)
                else:
                    roadmap["Phase 2 (3-6 months)"].append(rec)
            elif rec.framework.complexity == ComplexityLevel.INTERMEDIATE:
                if rec.prerequisites_met and len(roadmap["Phase 2 (3-6 months)"]) < 3:
                    roadmap["Phase 2 (3-6 months)"].append(rec)
                else:
                    roadmap["Phase 3 (6-12 months)"].append(rec)
            else:  # ADVANCED or EXPERT
                if rec.prerequisites_met:
                    roadmap["Phase 3 (6-12 months)"].append(rec)
                else:
                    roadmap["Phase 4 (12+ months)"].append(rec)
                    
        return roadmap
        
    def find_framework_combinations(
        self,
        context: StartupContext,
        max_combinations: int = 5
    ) -> List[List[Framework]]:
        """Find synergistic framework combinations"""
        recommendations = self.recommend_frameworks(context, max_recommendations=20)
        
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
        
    def generate_implementation_guide(
        self,
        framework: Framework,
        context: StartupContext
    ) -> Dict[str, any]:
        """Generate detailed implementation guide for a framework"""
        guide = {
            "framework": framework.name,
            "estimated_duration": framework.time_to_implement or "2-3 months",
            "team_requirements": self._estimate_team_requirements(framework, context),
            "preparation_steps": self._generate_preparation_steps(framework, context),
            "implementation_phases": self._generate_implementation_phases(framework),
            "success_criteria": framework.success_metrics or ["Define based on goals"],
            "common_challenges": framework.common_pitfalls or ["Monitor implementation closely"],
            "resources": self._recommend_resources(framework),
            "customization_notes": self._generate_customization_notes(framework, context)
        }
        
        return guide
        
    def _estimate_team_requirements(
        self,
        framework: Framework,
        context: StartupContext
    ) -> Dict[str, any]:
        """Estimate team requirements for framework implementation"""
        requirements = {
            "minimum_team_size": 1,
            "recommended_team_size": 3,
            "key_roles": [],
            "time_commitment": "Part-time",
            "skills_needed": []
        }
        
        # Adjust based on complexity
        if framework.complexity == ComplexityLevel.ADVANCED:
            requirements["minimum_team_size"] = 3
            requirements["recommended_team_size"] = 5
            requirements["time_commitment"] = "Full-time lead, part-time team"
        elif framework.complexity == ComplexityLevel.INTERMEDIATE:
            requirements["minimum_team_size"] = 2
            requirements["recommended_team_size"] = 4
            
        # Determine key roles based on category
        if framework.category == FrameworkCategory.STRATEGY:
            requirements["key_roles"] = ["Strategy Lead", "Business Analyst", "Executive Sponsor"]
        elif framework.category == FrameworkCategory.PRODUCT:
            requirements["key_roles"] = ["Product Manager", "Designer", "Engineer"]
        elif framework.category == FrameworkCategory.GROWTH:
            requirements["key_roles"] = ["Growth Lead", "Data Analyst", "Marketing"]
        elif framework.category == FrameworkCategory.OPERATIONS:
            requirements["key_roles"] = ["Operations Manager", "Process Expert", "Team Members"]
            
        # Extract skills from prerequisites
        if framework.prerequisites:
            requirements["skills_needed"] = framework.prerequisites
            
        return requirements
        
    def _generate_preparation_steps(
        self,
        framework: Framework,
        context: StartupContext
    ) -> List[str]:
        """Generate preparation steps for framework implementation"""
        steps = []
        
        # Standard preparation
        steps.append(f"Review {framework.name} methodology and best practices")
        steps.append("Secure executive sponsorship and team commitment")
        
        # Data preparation
        if "data" in str(framework.prerequisites).lower():
            steps.append("Gather and organize relevant data and metrics")
            
        # Team preparation
        if framework.complexity.value >= ComplexityLevel.INTERMEDIATE.value:
            steps.append("Conduct team training on framework concepts")
            
        # Tool preparation
        if framework.resources_required:
            steps.append(f"Set up required tools: {', '.join(framework.resources_required[:3])}")
            
        # Stakeholder preparation
        if framework.category in [FrameworkCategory.STRATEGY, FrameworkCategory.ORGANIZATIONAL]:
            steps.append("Align stakeholders on objectives and approach")
            
        return steps
        
    def _generate_implementation_phases(self, framework: Framework) -> List[Dict[str, str]]:
        """Generate implementation phases based on framework steps"""
        phases = []
        
        # Group application steps into phases
        total_steps = len(framework.application_steps)
        
        if total_steps <= 4:
            # Single phase
            phases.append({
                "phase": "Implementation",
                "duration": framework.time_to_implement or "2-4 weeks",
                "activities": framework.application_steps
            })
        else:
            # Multiple phases
            steps_per_phase = max(2, total_steps // 3)
            
            # Phase 1: Setup/Analysis
            phases.append({
                "phase": "Setup & Analysis",
                "duration": "1-2 weeks",
                "activities": framework.application_steps[:steps_per_phase]
            })
            
            # Phase 2: Implementation
            phases.append({
                "phase": "Core Implementation",
                "duration": "2-4 weeks",
                "activities": framework.application_steps[steps_per_phase:steps_per_phase*2]
            })
            
            # Phase 3: Optimization
            phases.append({
                "phase": "Optimization & Rollout",
                "duration": "1-2 weeks",
                "activities": framework.application_steps[steps_per_phase*2:]
            })
            
        return phases
        
    def _recommend_resources(self, framework: Framework) -> Dict[str, List[str]]:
        """Recommend resources for framework implementation"""
        resources = {
            "tools": [],
            "templates": [],
            "training": [],
            "reading": []
        }
        
        # Extract from framework data
        if framework.resources_required:
            resources["tools"] = framework.resources_required
            
        if framework.tools_templates:
            resources["templates"] = framework.tools_templates
            
        # Add category-specific resources
        if framework.category == FrameworkCategory.STRATEGY:
            resources["templates"].append(f"{framework.name} Canvas Template")
            resources["reading"].append(f"Harvard Business Review: {framework.name} Guide")
            
        elif framework.category == FrameworkCategory.GROWTH:
            resources["tools"].append("Analytics Platform (Google Analytics, Mixpanel)")
            resources["templates"].append("Growth Experiment Template")
            
        elif framework.category == FrameworkCategory.PRODUCT:
            resources["tools"].append("Product Management Platform (Jira, Asana)")
            resources["templates"].append("Product Roadmap Template")
            
        # Training recommendations
        resources["training"].append(f"Online Course: Mastering {framework.name}")
        resources["training"].append(f"Workshop: {framework.category.value} Excellence")
        
        return resources
        
    def _generate_customization_notes(
        self,
        framework: Framework,
        context: StartupContext
    ) -> List[str]:
        """Generate customization notes based on context"""
        notes = []
        
        # Stage-specific customization
        if context.stage == BusinessStage.IDEA:
            notes.append("Focus on validation and learning rather than perfection")
        elif context.stage == BusinessStage.GROWTH:
            notes.append("Emphasize scalability and repeatability in implementation")
        elif context.stage == BusinessStage.MATURE:
            notes.append("Consider change management and organizational inertia")
            
        # Industry-specific customization
        if context.industry == IndustryType.B2B_SAAS:
            notes.append("Adapt for longer sales cycles and enterprise requirements")
        elif context.industry == IndustryType.ECOMMERCE:
            notes.append("Focus on customer experience and conversion optimization")
            
        # Team size customization
        if context.team_size < 10:
            notes.append("Simplify processes and combine roles where possible")
        elif context.team_size > 50:
            notes.append("Ensure clear communication and change management processes")
            
        # Challenge-specific customization
        if ChallengeType.FUNDING in context.primary_challenges:
            notes.append("Document results and metrics for investor communications")
        if ChallengeType.SCALING in context.primary_challenges:
            notes.append("Build for 10x growth from the start")
            
        return notes


# Utility functions for external use

def recommend_frameworks_for_startup(
    stage: str,
    industry: str,
    team_size: int,
    funding_stage: str,
    challenges: List[str],
    goals: List[str],
    constraints: List[str] = None,
    existing_frameworks: List[str] = None
) -> List[Dict[str, any]]:
    """
    Main function to get framework recommendations for a startup
    
    Returns list of framework recommendations with implementation guidance
    """
    
    # Convert string inputs to enums
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
        constraints=constraints or [],
        existing_frameworks=existing_frameworks
    )
    
    # Get recommendations
    selector = FrameworkSelector()
    recommendations = selector.recommend_frameworks(context)
    
    # Convert to dictionary format
    results = []
    for rec in recommendations:
        results.append({
            "framework_name": rec.framework.name,
            "framework_id": rec.framework.id,
            "category": rec.framework.category.value,
            "relevance_score": round(rec.relevance_score, 2),
            "rationale": rec.rationale,
            "implementation_order": rec.implementation_order,
            "complexity": rec.framework.complexity.name,
            "time_to_implement": rec.framework.time_to_implement,
            "estimated_impact": rec.estimated_impact,
            "risk_level": rec.risk_level,
            "prerequisites_met": rec.prerequisites_met,
            "description": rec.framework.description,
            "key_components": rec.framework.key_components,
            "expected_outcomes": rec.framework.expected_outcomes
        })
        
    return results


def get_implementation_roadmap(
    recommendations: List[Dict[str, any]]
) -> Dict[str, List[Dict[str, any]]]:
    """
    Create a phased implementation roadmap from recommendations
    """
    selector = FrameworkSelector()
    
    # Convert back to FrameworkRecommendation objects
    rec_objects = []
    for rec_dict in recommendations:
        framework = get_framework_by_id(rec_dict["framework_id"])
        if framework:
            rec = FrameworkRecommendation(
                framework=framework,
                relevance_score=rec_dict["relevance_score"],
                rationale=rec_dict["rationale"],
                implementation_order=rec_dict["implementation_order"],
                prerequisites_met=rec_dict["prerequisites_met"],
                estimated_impact=rec_dict["estimated_impact"],
                risk_level=rec_dict["risk_level"]
            )
            rec_objects.append(rec)
            
    roadmap = selector.create_implementation_roadmap(rec_objects)
    
    # Convert to dictionary format
    roadmap_dict = {}
    for phase, recs in roadmap.items():
        roadmap_dict[phase] = [
            {
                "framework_name": rec.framework.name,
                "framework_id": rec.framework.id,
                "complexity": rec.framework.complexity.name,
                "estimated_impact": rec.estimated_impact,
                "risk_level": rec.risk_level
            }
            for rec in recs
        ]
        
    return roadmap_dict


def get_framework_combinations(
    stage: str,
    industry: str,
    challenges: List[str],
    goals: List[str]
) -> List[List[Dict[str, str]]]:
    """
    Get synergistic framework combinations
    """
    # Create minimal context for combination finding
    context = StartupContext(
        stage=BusinessStage[stage.upper().replace(" ", "_")],
        industry=IndustryType[industry.upper().replace(" ", "_")],
        team_size=10,  # Default
        funding_stage="Series A",  # Default
        primary_challenges=[ChallengeType[c.upper().replace(" ", "_")] for c in challenges],
        goals=goals,
        constraints=[]  # Default empty constraints
    )
    
    selector = FrameworkSelector()
    combinations = selector.find_framework_combinations(context)
    
    # Convert to dictionary format
    combo_list = []
    for combo in combinations:
        combo_dict = [
            {
                "framework_name": f.name,
                "framework_id": f.id,
                "category": f.category.value
            }
            for f in combo
        ]
        combo_list.append(combo_dict)
        
    return combo_list


def get_detailed_implementation_guide(
    framework_id: str,
    stage: str,
    industry: str,
    team_size: int
) -> Dict[str, any]:
    """
    Get detailed implementation guide for a specific framework
    """
    framework = get_framework_by_id(framework_id)
    if not framework:
        return {"error": "Framework not found"}
        
    # Create context
    context = StartupContext(
        stage=BusinessStage[stage.upper().replace(" ", "_")],
        industry=IndustryType[industry.upper().replace(" ", "_")],
        team_size=team_size,
        funding_stage="Series A",  # Default
        primary_challenges=[],
        goals=[],
        constraints=[]  # Default empty constraints
    )
    
    selector = FrameworkSelector()
    guide = selector.generate_implementation_guide(framework, context)
    
    return guide