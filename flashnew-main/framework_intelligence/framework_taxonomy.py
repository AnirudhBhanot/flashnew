#!/usr/bin/env python3
"""
Framework Taxonomy System - Multi-dimensional classification for 500+ business frameworks
Based on MIT Systems Design and HBS Strategic Management principles
"""

from enum import Enum
from typing import List, Dict, Set, Optional
from dataclasses import dataclass, field


class TemporalStage(Enum):
    """Company lifecycle stages for framework applicability"""
    PRE_FORMATION = "pre_formation"  # Idea stage, no company yet
    FORMATION = "formation"  # 0-6 months, company forming
    VALIDATION = "validation"  # 6-18 months, seeking PMF
    TRACTION = "traction"  # 18-36 months, early revenue
    GROWTH = "growth"  # 3-5 years, scaling
    SCALE = "scale"  # 5-10 years, expansion
    MATURITY = "maturity"  # 10+ years, optimization


class ProblemArchetype(Enum):
    """Core problem types that frameworks address"""
    CUSTOMER_DISCOVERY = "customer_discovery"
    PRODUCT_MARKET_FIT = "product_market_fit"
    BUSINESS_MODEL_DESIGN = "business_model_design"
    UNIT_ECONOMICS_OPTIMIZATION = "unit_economics_optimization"
    GROWTH_MECHANICS = "growth_mechanics"
    COMPETITIVE_STRATEGY = "competitive_strategy"
    ORGANIZATIONAL_DESIGN = "organizational_design"
    INNOVATION_MANAGEMENT = "innovation_management"
    RISK_MANAGEMENT = "risk_management"
    PORTFOLIO_OPTIMIZATION = "portfolio_optimization"
    OPERATIONAL_EXCELLENCE = "operational_excellence"
    MARKET_ANALYSIS = "market_analysis"
    FINANCIAL_PLANNING = "financial_planning"
    TALENT_MANAGEMENT = "talent_management"
    DIGITAL_TRANSFORMATION = "digital_transformation"


class DecisionContext(Enum):
    """Type of decision the framework supports"""
    DIAGNOSTIC = "diagnostic"  # Understand current state
    PREDICTIVE = "predictive"  # Forecast future outcomes
    PRESCRIPTIVE = "prescriptive"  # Recommend specific actions
    EVALUATIVE = "evaluative"  # Assess performance/results
    EXPLORATORY = "exploratory"  # Discover new opportunities


class DataRequirement(Enum):
    """Level of data sophistication needed"""
    QUALITATIVE_ONLY = "qualitative_only"  # Interviews, observations
    BASIC_QUANTITATIVE = "basic_quantitative"  # Revenue, costs, counts
    ADVANCED_METRICS = "advanced_metrics"  # Cohorts, LTV, CAC
    MARKET_DATA = "market_data"  # Industry research required
    COMPETITIVE_INTEL = "competitive_intel"  # Competitor data required
    HISTORICAL_DATA = "historical_data"  # Time series required
    EXPERIMENTAL_DATA = "experimental_data"  # A/B test results


class ComplexityTier(Enum):
    """Implementation complexity and time requirement"""
    PLUG_AND_PLAY = "plug_and_play"  # < 1 day
    SIMPLE = "simple"  # 1-3 days
    MODERATE = "moderate"  # 1-2 weeks
    COMPLEX = "complex"  # 2-4 weeks
    ENTERPRISE = "enterprise"  # 1+ months


class OutcomeType(Enum):
    """Primary outcome delivered by the framework"""
    STRATEGIC_CLARITY = "strategic_clarity"
    TACTICAL_ACTIONS = "tactical_actions"
    FINANCIAL_PROJECTIONS = "financial_projections"
    ORGANIZATIONAL_DESIGN = "organizational_design"
    RISK_MITIGATION = "risk_mitigation"
    INNOVATION_PIPELINE = "innovation_pipeline"
    OPERATIONAL_IMPROVEMENTS = "operational_improvements"
    CUSTOMER_INSIGHTS = "customer_insights"
    COMPETITIVE_ADVANTAGE = "competitive_advantage"
    GROWTH_STRATEGY = "growth_strategy"


class IndustryContext(Enum):
    """Industry-specific applicability"""
    UNIVERSAL = "universal"
    B2B_SAAS = "b2b_saas"
    B2C_SAAS = "b2c_saas"
    MARKETPLACE = "marketplace"
    ECOMMERCE = "ecommerce"
    HARDWARE = "hardware"
    CONSUMER_GOODS = "consumer_goods"
    ENTERPRISE_SOFTWARE = "enterprise_software"
    FINTECH = "fintech"
    HEALTHTECH = "healthtech"
    EDTECH = "edtech"
    CLEANTECH = "cleantech"
    BIOTECH = "biotech"
    RETAIL = "retail"
    MANUFACTURING = "manufacturing"
    SERVICES = "services"


@dataclass
class FrameworkTags:
    """Complete tagging system for a framework"""
    # Primary dimensions
    temporal_stages: List[TemporalStage] = field(default_factory=list)
    problem_archetypes: List[ProblemArchetype] = field(default_factory=list)
    decision_contexts: List[DecisionContext] = field(default_factory=list)
    data_requirements: List[DataRequirement] = field(default_factory=list)
    complexity_tier: ComplexityTier = ComplexityTier.MODERATE
    outcome_types: List[OutcomeType] = field(default_factory=list)
    industry_contexts: List[IndustryContext] = field(default_factory=list)
    
    # Additional metadata
    typical_users: List[str] = field(default_factory=list)  # CEO, CFO, Product Manager
    team_size_min: int = 1
    team_size_max: int = 1000
    time_to_value_days: int = 7  # How long until first insights
    durability_months: int = 12  # How long insights remain relevant
    
    # Effectiveness metrics (0-100)
    ease_of_use: int = 50
    actionability: int = 50
    accuracy: int = 50
    strategic_impact: int = 50
    
    # Special flags
    requires_facilitator: bool = False
    requires_software: bool = False
    requires_certification: bool = False
    is_proprietary: bool = False
    has_variants: bool = False
    
    # Keywords for search
    keywords: Set[str] = field(default_factory=set)
    
    def is_suitable_for_stage(self, stage: TemporalStage) -> bool:
        """Check if framework is suitable for a given company stage"""
        return stage in self.temporal_stages
    
    def matches_problem(self, problem: ProblemArchetype) -> bool:
        """Check if framework addresses a specific problem type"""
        return problem in self.problem_archetypes
    
    def complexity_score(self) -> int:
        """Return numerical complexity score"""
        complexity_map = {
            ComplexityTier.PLUG_AND_PLAY: 1,
            ComplexityTier.SIMPLE: 2,
            ComplexityTier.MODERATE: 3,
            ComplexityTier.COMPLEX: 4,
            ComplexityTier.ENTERPRISE: 5
        }
        return complexity_map.get(self.complexity_tier, 3)
    
    def effectiveness_score(self) -> float:
        """Calculate overall effectiveness score"""
        return (self.ease_of_use + self.actionability + 
                self.accuracy + self.strategic_impact) / 4.0
    
    def get_implementation_time(self) -> str:
        """Get human-readable implementation time"""
        time_map = {
            ComplexityTier.PLUG_AND_PLAY: "< 1 day",
            ComplexityTier.SIMPLE: "1-3 days",
            ComplexityTier.MODERATE: "1-2 weeks",
            ComplexityTier.COMPLEX: "2-4 weeks",
            ComplexityTier.ENTERPRISE: "1+ months"
        }
        return time_map.get(self.complexity_tier, "1-2 weeks")


@dataclass
class FrameworkRelationship:
    """Defines relationships between frameworks"""
    framework_id: str
    relationship_type: str  # prerequisite, complementary, alternative, progressive
    related_framework_ids: List[str] = field(default_factory=list)
    relationship_strength: int = 50  # 0-100, how strong the relationship
    notes: str = ""


@dataclass
class FrameworkEffectiveness:
    """Empirical effectiveness data for a framework"""
    framework_id: str
    success_rate: float = 0.0  # % of implementations that achieved goals
    time_to_impact_days: int = 30  # How quickly results appear
    effort_return_ratio: float = 1.0  # Value created / effort required
    durability_months: int = 12  # How long insights remain relevant
    
    # Context-specific effectiveness
    effectiveness_by_stage: Dict[TemporalStage, float] = field(default_factory=dict)
    effectiveness_by_industry: Dict[IndustryContext, float] = field(default_factory=dict)
    effectiveness_by_team_size: Dict[str, float] = field(default_factory=dict)  # small/medium/large
    
    # Common success factors
    success_factors: List[str] = field(default_factory=list)
    failure_factors: List[str] = field(default_factory=list)
    
    # Sample size for confidence
    data_points: int = 0
    confidence_level: float = 0.0  # 0-100%


@dataclass
class FrameworkAntiPattern:
    """When NOT to use a framework"""
    framework_id: str
    antipattern_conditions: List[str] = field(default_factory=list)
    negative_outcomes: List[str] = field(default_factory=list)
    alternative_frameworks: List[str] = field(default_factory=list)
    severity: str = "medium"  # low, medium, high
    
    def check_antipattern_match(self, company_context: Dict) -> bool:
        """Check if company matches any antipattern conditions"""
        # This would be implemented with actual matching logic
        return False


class FrameworkTaxonomyEngine:
    """Engine for managing framework taxonomy and relationships"""
    
    def __init__(self):
        self.framework_tags: Dict[str, FrameworkTags] = {}
        self.relationships: Dict[str, List[FrameworkRelationship]] = {}
        self.effectiveness_data: Dict[str, FrameworkEffectiveness] = {}
        self.antipatterns: Dict[str, FrameworkAntiPattern] = {}
        
    def add_framework_tags(self, framework_id: str, tags: FrameworkTags):
        """Add taxonomy tags for a framework"""
        self.framework_tags[framework_id] = tags
        
    def add_relationship(self, relationship: FrameworkRelationship):
        """Add a relationship between frameworks"""
        if relationship.framework_id not in self.relationships:
            self.relationships[relationship.framework_id] = []
        self.relationships[relationship.framework_id].append(relationship)
        
    def add_effectiveness_data(self, framework_id: str, data: FrameworkEffectiveness):
        """Add effectiveness data for a framework"""
        self.effectiveness_data[framework_id] = data
        
    def add_antipattern(self, framework_id: str, antipattern: FrameworkAntiPattern):
        """Add antipattern for a framework"""
        self.antipatterns[framework_id] = antipattern
        
    def find_frameworks_by_stage(self, stage: TemporalStage) -> List[str]:
        """Find all frameworks suitable for a given stage"""
        suitable = []
        for fid, tags in self.framework_tags.items():
            if tags.is_suitable_for_stage(stage):
                suitable.append(fid)
        return suitable
        
    def find_frameworks_by_problem(self, problem: ProblemArchetype) -> List[str]:
        """Find all frameworks that address a specific problem"""
        suitable = []
        for fid, tags in self.framework_tags.items():
            if tags.matches_problem(problem):
                suitable.append(fid)
        return suitable
        
    def get_complementary_frameworks(self, framework_id: str) -> List[str]:
        """Get frameworks that work well together"""
        complementary = []
        if framework_id in self.relationships:
            for rel in self.relationships[framework_id]:
                if rel.relationship_type == "complementary":
                    complementary.extend(rel.related_framework_ids)
        return complementary
        
    def get_prerequisite_frameworks(self, framework_id: str) -> List[str]:
        """Get frameworks that should be completed first"""
        prerequisites = []
        if framework_id in self.relationships:
            for rel in self.relationships[framework_id]:
                if rel.relationship_type == "prerequisite":
                    prerequisites.extend(rel.related_framework_ids)
        return prerequisites
        
    def calculate_framework_fit_score(self, framework_id: str, company_context: Dict) -> float:
        """Calculate how well a framework fits a company's context"""
        if framework_id not in self.framework_tags:
            return 0.0
            
        tags = self.framework_tags[framework_id]
        score = 0.0
        weights = {
            'stage_match': 0.25,
            'problem_match': 0.30,
            'complexity_fit': 0.15,
            'data_availability': 0.15,
            'team_fit': 0.15
        }
        
        # Stage match
        company_stage = company_context.get('stage')
        if company_stage and any(stage.value == company_stage for stage in tags.temporal_stages):
            score += weights['stage_match'] * 100
            
        # Problem match
        company_problems = company_context.get('problems', [])
        problem_matches = sum(1 for p in tags.problem_archetypes if p.value in company_problems)
        if company_problems:
            score += weights['problem_match'] * (problem_matches / len(company_problems)) * 100
            
        # Complexity fit
        team_size = company_context.get('team_size', 10)
        if tags.team_size_min <= team_size <= tags.team_size_max:
            complexity_penalty = abs(tags.complexity_score() - 3) * 10  # Prefer moderate complexity
            score += weights['complexity_fit'] * (100 - complexity_penalty)
            
        # Data availability
        available_data = company_context.get('available_data', [])
        required_data = [d.value for d in tags.data_requirements]
        if required_data:
            data_match = sum(1 for d in required_data if d in available_data) / len(required_data)
            score += weights['data_availability'] * data_match * 100
            
        # Team fit
        if team_size >= tags.team_size_min:
            score += weights['team_fit'] * 100
            
        return score