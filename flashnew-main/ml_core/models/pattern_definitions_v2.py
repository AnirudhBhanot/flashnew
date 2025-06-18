"""
FLASH Pattern System V2 - 45 Pattern Definitions
Hierarchical pattern structure with 8 master categories
"""

from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional, Set
from enum import Enum
import numpy as np


class MasterCategory(Enum):
    """Top-level pattern categories"""
    GROWTH_DYNAMICS = "growth_dynamics"
    BUSINESS_MODEL = "business_model"
    TECHNOLOGY_DEPTH = "technology_depth"
    MARKET_APPROACH = "market_approach"
    INDUSTRY_VERTICAL = "industry_vertical"
    OPERATIONAL_MODEL = "operational_model"
    FUNDING_PROFILE = "funding_profile"
    MATURITY_STAGE = "maturity_stage"


@dataclass
class PatternDefinition:
    """Complete pattern definition with all attributes"""
    # Basic info
    name: str
    master_category: MasterCategory
    description: str
    
    # Identification criteria
    required_conditions: Dict[str, any]  # Must meet ALL
    optional_conditions: Dict[str, any]  # Should meet SOME
    exclusion_conditions: Dict[str, any]  # Must NOT meet
    
    # Pattern characteristics
    typical_success_rate: Tuple[float, float]  # (min, max)
    typical_funding_stages: List[str]
    typical_team_size: Tuple[int, int]  # (min, max)
    
    # Business metrics
    typical_burn_multiple: Tuple[float, float]
    typical_growth_rate: Tuple[float, float]
    typical_gross_margin: Tuple[float, float]
    
    # Examples and evolution
    example_companies: List[str]
    evolution_paths: List[str]  # What patterns they typically evolve to
    compatible_patterns: List[str]  # Can coexist
    incompatible_patterns: List[str]  # Mutually exclusive
    
    # Strategic insights
    key_success_factors: List[str]
    common_failure_modes: List[str]
    strategic_recommendations: List[str]


# Pattern Definitions - 45 Total

# ==========================================
# 1. GROWTH DYNAMICS PATTERNS (7)
# ==========================================

VIRAL_CONSUMER_GROWTH = PatternDefinition(
    name="VIRAL_CONSUMER_GROWTH",
    master_category=MasterCategory.GROWTH_DYNAMICS,
    description="Consumer products with viral/exponential user growth",
    required_conditions={
        "user_growth_rate_percent": lambda x: x > 200,
        "dau_mau_ratio": lambda x: x > 0.4,
        "customer_count": lambda x: x > 1000
    },
    optional_conditions={
        "network_effects_present": lambda x: x == 1,
        "brand_strength_score": lambda x: x >= 4
    },
    exclusion_conditions={
        "customer_concentration_percent": lambda x: x > 50
    },
    typical_success_rate=(0.35, 0.65),
    typical_funding_stages=["seed", "series_a", "series_b"],
    typical_team_size=(10, 50),
    typical_burn_multiple=(3.0, 10.0),
    typical_growth_rate=(200, 500),
    typical_gross_margin=(20, 60),
    example_companies=["TikTok", "Snapchat", "BeReal", "Clubhouse"],
    evolution_paths=["PLATFORM_NETWORK_EFFECTS", "MARKET_LEADER"],
    compatible_patterns=["CONSUMER_MASS_MARKET", "AI_ML_CORE"],
    incompatible_patterns=["B2B_ENTERPRISE", "BOOTSTRAP_PROFITABLE"],
    key_success_factors=[
        "Product-market fit with strong retention",
        "Viral coefficient > 1.0",
        "Low customer acquisition cost"
    ],
    common_failure_modes=[
        "Unable to monetize user base",
        "High churn after initial growth",
        "Platform risk (app store, social media)"
    ],
    strategic_recommendations=[
        "Focus on retention before monetization",
        "Build strong community features",
        "Plan for international expansion early"
    ]
)

ENTERPRISE_LAND_EXPAND = PatternDefinition(
    name="ENTERPRISE_LAND_EXPAND",
    master_category=MasterCategory.GROWTH_DYNAMICS,
    description="B2B companies that start small and expand within accounts",
    required_conditions={
        "net_dollar_retention_percent": lambda x: x > 120,
        "ltv_cac_ratio": lambda x: x > 3,
        "customer_concentration_percent": lambda x: x > 20
    },
    optional_conditions={
        "annual_revenue_run_rate": lambda x: x > 1000000,
        "gross_margin_percent": lambda x: x > 70
    },
    exclusion_conditions={
        "customer_count": lambda x: x > 10000  # Not mass market
    },
    typical_success_rate=(0.60, 0.80),
    typical_funding_stages=["series_a", "series_b", "series_c"],
    typical_team_size=(50, 200),
    typical_burn_multiple=(1.5, 3.0),
    typical_growth_rate=(80, 150),
    typical_gross_margin=(70, 85),
    example_companies=["Datadog", "Snowflake", "MongoDB", "HashiCorp"],
    evolution_paths=["MARKET_LEADER", "PLATFORM_INFRASTRUCTURE"],
    compatible_patterns=["B2B_ENTERPRISE", "PURE_SOFTWARE"],
    incompatible_patterns=["VIRAL_CONSUMER_GROWTH", "BOOTSTRAP_PROFITABLE"],
    key_success_factors=[
        "Strong product expansion capabilities",
        "Enterprise-grade security and compliance",
        "Customer success focus"
    ],
    common_failure_modes=[
        "Inability to move upmarket",
        "High churn in smaller accounts",
        "Sales efficiency decline"
    ],
    strategic_recommendations=[
        "Invest heavily in customer success",
        "Build platform capabilities for expansion",
        "Focus on logo retention first, then expansion"
    ]
)

PLG_BOTTOM_UP = PatternDefinition(
    name="PLG_BOTTOM_UP",
    master_category=MasterCategory.GROWTH_DYNAMICS,
    description="Product-led growth with bottom-up adoption in organizations",
    required_conditions={
        "product_retention_30d": lambda x: x > 0.6,
        "ltv_cac_ratio": lambda x: x > 3,
        "user_growth_rate_percent": lambda x: x > 100
    },
    optional_conditions={
        "dau_mau_ratio": lambda x: x > 0.3,
        "tech_differentiation_score": lambda x: x >= 4
    },
    exclusion_conditions={
        "customer_concentration_percent": lambda x: x > 40
    },
    typical_success_rate=(0.55, 0.75),
    typical_funding_stages=["seed", "series_a", "series_b"],
    typical_team_size=(20, 100),
    typical_burn_multiple=(1.0, 2.5),
    typical_growth_rate=(100, 200),
    typical_gross_margin=(60, 80),
    example_companies=["Figma", "Notion", "Linear", "Airtable"],
    evolution_paths=["ENTERPRISE_LAND_EXPAND", "PLATFORM_PLAY"],
    compatible_patterns=["PURE_SOFTWARE", "FREEMIUM_CONVERSION"],
    incompatible_patterns=["SALES_LED_GROWTH", "ASSET_HEAVY_OPERATIONS"],
    key_success_factors=[
        "Exceptional user experience",
        "Viral loops within organizations",
        "Self-serve onboarding"
    ],
    common_failure_modes=[
        "Inability to monetize free users",
        "Enterprise features lag",
        "Security/compliance gaps"
    ],
    strategic_recommendations=[
        "Focus on time-to-value metrics",
        "Build collaboration features",
        "Layer in enterprise capabilities gradually"
    ]
)

SALES_LED_GROWTH = PatternDefinition(
    name="SALES_LED_GROWTH",
    master_category=MasterCategory.GROWTH_DYNAMICS,
    description="Traditional enterprise sales motion with direct sales teams",
    required_conditions={
        "ltv_cac_ratio": lambda x: x > 2,
        "annual_revenue_run_rate": lambda x: x > 500000,
        "team_size_full_time": lambda x: x > 20
    },
    optional_conditions={
        "board_advisor_experience_score": lambda x: x >= 4,
        "prior_successful_exits_count": lambda x: x > 0
    },
    exclusion_conditions={
        "product_retention_30d": lambda x: x > 0.8  # Not product-led
    },
    typical_success_rate=(0.50, 0.70),
    typical_funding_stages=["series_a", "series_b", "series_c"],
    typical_team_size=(50, 500),
    typical_burn_multiple=(2.0, 4.0),
    typical_growth_rate=(50, 100),
    typical_gross_margin=(60, 80),
    example_companies=["Salesforce", "Workday", "ServiceNow", "Veeva"],
    evolution_paths=["MARKET_LEADER", "VERTICAL_SAAS_LEADER"],
    compatible_patterns=["B2B_ENTERPRISE", "VERTICAL_SPECIFIC"],
    incompatible_patterns=["PLG_BOTTOM_UP", "VIRAL_CONSUMER_GROWTH"],
    key_success_factors=[
        "Experienced sales leadership",
        "Clear ROI proposition",
        "Strong implementation services"
    ],
    common_failure_modes=[
        "High sales costs",
        "Long sales cycles",
        "Inability to scale sales team"
    ],
    strategic_recommendations=[
        "Invest in sales enablement",
        "Focus on repeatability",
        "Build strong partnerships"
    ]
)

COMMUNITY_DRIVEN_GROWTH = PatternDefinition(
    name="COMMUNITY_DRIVEN_GROWTH",
    master_category=MasterCategory.GROWTH_DYNAMICS,
    description="Growth through community building and user-generated content",
    required_conditions={
        "user_growth_rate_percent": lambda x: x > 80,
        "dau_mau_ratio": lambda x: x > 0.25,
        "network_effects_present": lambda x: x == 1
    },
    optional_conditions={
        "brand_strength_score": lambda x: x >= 4,
        "customer_count": lambda x: x > 5000
    },
    exclusion_conditions={},
    typical_success_rate=(0.45, 0.70),
    typical_funding_stages=["seed", "series_a"],
    typical_team_size=(10, 50),
    typical_burn_multiple=(1.5, 3.0),
    typical_growth_rate=(80, 150),
    typical_gross_margin=(30, 70),
    example_companies=["Discord", "Reddit", "Twitch", "GitHub"],
    evolution_paths=["PLATFORM_NETWORK_EFFECTS", "DATA_MONETIZATION"],
    compatible_patterns=["FREEMIUM_CONVERSION", "PLATFORM_TECH"],
    incompatible_patterns=["SALES_LED_GROWTH", "B2B_ENTERPRISE"],
    key_success_factors=[
        "Strong community moderation",
        "User-generated content",
        "Network effects"
    ],
    common_failure_modes=[
        "Community toxicity",
        "Monetization challenges",
        "Platform maintenance costs"
    ],
    strategic_recommendations=[
        "Invest in community tools",
        "Create creator economy",
        "Build trust and safety features"
    ]
)

PLATFORM_NETWORK_EFFECTS = PatternDefinition(
    name="PLATFORM_NETWORK_EFFECTS",
    master_category=MasterCategory.GROWTH_DYNAMICS,
    description="Platforms with strong network effects driving growth",
    required_conditions={
        "network_effects_present": lambda x: x == 1,
        "scalability_score": lambda x: x >= 4,
        "user_growth_rate_percent": lambda x: x > 100
    },
    optional_conditions={
        "dau_mau_ratio": lambda x: x > 0.3,
        "gross_margin_percent": lambda x: x > 60
    },
    exclusion_conditions={},
    typical_success_rate=(0.40, 0.80),
    typical_funding_stages=["series_a", "series_b", "series_c"],
    typical_team_size=(50, 500),
    typical_burn_multiple=(2.0, 5.0),
    typical_growth_rate=(100, 300),
    typical_gross_margin=(40, 80),
    example_companies=["Uber", "Airbnb", "DoorDash", "Stripe"],
    evolution_paths=["MARKET_LEADER", "PLATFORM_INFRASTRUCTURE"],
    compatible_patterns=["TRANSACTIONAL_MARKETPLACE", "API_PLATFORM"],
    incompatible_patterns=["BOOTSTRAP_PROFITABLE", "LINEAR_SERVICES"],
    key_success_factors=[
        "Liquidity on both sides",
        "Trust and safety",
        "Platform governance"
    ],
    common_failure_modes=[
        "Chicken-and-egg problem",
        "Disintermediation",
        "Regulatory challenges"
    ],
    strategic_recommendations=[
        "Focus on supply first",
        "Build trust mechanisms",
        "Plan for global expansion"
    ]
)

GEOGRAPHIC_EXPANSION = PatternDefinition(
    name="GEOGRAPHIC_EXPANSION",
    master_category=MasterCategory.GROWTH_DYNAMICS,
    description="Growth through systematic geographic market expansion",
    required_conditions={
        "revenue_growth_rate_percent": lambda x: x > 100,
        "team_size_full_time": lambda x: x > 50,
        "scalability_score": lambda x: x >= 3
    },
    optional_conditions={
        "total_capital_raised_usd": lambda x: x > 10000000,
        "market_growth_rate_percent": lambda x: x > 20
    },
    exclusion_conditions={},
    typical_success_rate=(0.45, 0.65),
    typical_funding_stages=["series_a", "series_b", "series_c"],
    typical_team_size=(100, 1000),
    typical_burn_multiple=(2.5, 5.0),
    typical_growth_rate=(80, 150),
    typical_gross_margin=(20, 50),
    example_companies=["Uber", "Lime", "Deliveroo", "Grab"],
    evolution_paths=["MARKET_LEADER", "REGIONAL_CHAMPION"],
    compatible_patterns=["ASSET_HEAVY_OPERATIONS", "LOCALIZED_PLAYBOOK"],
    incompatible_patterns=["BOOTSTRAP_PROFITABLE", "PURE_SOFTWARE"],
    key_success_factors=[
        "Localization capabilities",
        "Operational excellence",
        "Local partnerships"
    ],
    common_failure_modes=[
        "Underestimating local competition",
        "Regulatory challenges",
        "Unit economics deterioration"
    ],
    strategic_recommendations=[
        "Perfect playbook in home market",
        "Hire local leadership",
        "Adapt to local preferences"
    ]
)

# ==========================================
# 2. BUSINESS MODEL PATTERNS (6)
# ==========================================

SUBSCRIPTION_RECURRING = PatternDefinition(
    name="SUBSCRIPTION_RECURRING",
    master_category=MasterCategory.BUSINESS_MODEL,
    description="Subscription-based recurring revenue model",
    required_conditions={
        "net_dollar_retention_percent": lambda x: x > 90,
        "ltv_cac_ratio": lambda x: x > 2,
        "gross_margin_percent": lambda x: x > 60
    },
    optional_conditions={
        "annual_revenue_run_rate": lambda x: x > 1000000,
        "product_retention_30d": lambda x: x > 0.7
    },
    exclusion_conditions={},
    typical_success_rate=(0.55, 0.75),
    typical_funding_stages=["seed", "series_a", "series_b"],
    typical_team_size=(20, 200),
    typical_burn_multiple=(1.5, 3.0),
    typical_growth_rate=(60, 150),
    typical_gross_margin=(70, 85),
    example_companies=["Netflix", "Spotify", "Zoom", "Slack"],
    evolution_paths=["USAGE_BASED_PRICING", "PLATFORM_PLAY"],
    compatible_patterns=["PURE_SOFTWARE", "PLG_BOTTOM_UP"],
    incompatible_patterns=["TRANSACTIONAL_ONE_TIME", "PROJECT_BASED"],
    key_success_factors=[
        "Low churn rates",
        "Expansion revenue",
        "Predictable revenue"
    ],
    common_failure_modes=[
        "High churn",
        "Feature fatigue",
        "Price sensitivity"
    ],
    strategic_recommendations=[
        "Focus on annual contracts",
        "Build switching costs",
        "Optimize for NRR > 110%"
    ]
)

TRANSACTIONAL_MARKETPLACE = PatternDefinition(
    name="TRANSACTIONAL_MARKETPLACE",
    master_category=MasterCategory.BUSINESS_MODEL,
    description="Two-sided marketplace with transaction-based revenue",
    required_conditions={
        "network_effects_present": lambda x: x == 1,
        "gross_margin_percent": lambda x: x < 50,
        "customer_count": lambda x: x > 1000
    },
    optional_conditions={
        "user_growth_rate_percent": lambda x: x > 100,
        "brand_strength_score": lambda x: x >= 3
    },
    exclusion_conditions={
        "ltv_cac_ratio": lambda x: x > 10  # Not subscription-like
    },
    typical_success_rate=(0.35, 0.60),
    typical_funding_stages=["seed", "series_a", "series_b", "series_c"],
    typical_team_size=(50, 500),
    typical_burn_multiple=(3.0, 8.0),
    typical_growth_rate=(100, 300),
    typical_gross_margin=(15, 40),
    example_companies=["eBay", "Etsy", "StockX", "Mercari"],
    evolution_paths=["PLATFORM_NETWORK_EFFECTS", "FINTECH_EMBEDDED"],
    compatible_patterns=["PLATFORM_TECH", "COMMUNITY_DRIVEN_GROWTH"],
    incompatible_patterns=["SUBSCRIPTION_RECURRING", "HARDWARE_AS_SERVICE"],
    key_success_factors=[
        "Liquidity on both sides",
        "Trust and safety",
        "Competitive take rates"
    ],
    common_failure_modes=[
        "Disintermediation",
        "Supply/demand imbalance",
        "Take rate pressure"
    ],
    strategic_recommendations=[
        "Focus on transaction velocity",
        "Build trust systems",
        "Expand payment services"
    ]
)

FREEMIUM_CONVERSION = PatternDefinition(
    name="FREEMIUM_CONVERSION",
    master_category=MasterCategory.BUSINESS_MODEL,
    description="Free tier with conversion to paid subscriptions",
    required_conditions={
        "product_retention_30d": lambda x: x > 0.5,
        "customer_count": lambda x: x > 5000,
        "ltv_cac_ratio": lambda x: x > 2
    },
    optional_conditions={
        "dau_mau_ratio": lambda x: x > 0.25,
        "user_growth_rate_percent": lambda x: x > 100
    },
    exclusion_conditions={},
    typical_success_rate=(0.45, 0.70),
    typical_funding_stages=["seed", "series_a"],
    typical_team_size=(20, 100),
    typical_burn_multiple=(1.5, 3.0),
    typical_growth_rate=(80, 200),
    typical_gross_margin=(60, 80),
    example_companies=["Dropbox", "Evernote", "Canva", "Grammarly"],
    evolution_paths=["SUBSCRIPTION_RECURRING", "PLG_BOTTOM_UP"],
    compatible_patterns=["PURE_SOFTWARE", "VIRAL_CONSUMER_GROWTH"],
    incompatible_patterns=["SALES_LED_GROWTH", "HARDWARE_AS_SERVICE"],
    key_success_factors=[
        "Clear upgrade path",
        "Feature gating strategy",
        "Low marginal costs"
    ],
    common_failure_modes=[
        "Low conversion rates",
        "Free tier too generous",
        "High support costs"
    ],
    strategic_recommendations=[
        "Optimize conversion funnel",
        "Create usage limits",
        "Build team features"
    ]
)

USAGE_BASED_PRICING = PatternDefinition(
    name="USAGE_BASED_PRICING",
    master_category=MasterCategory.BUSINESS_MODEL,
    description="Revenue scales with customer usage",
    required_conditions={
        "net_dollar_retention_percent": lambda x: x > 110,
        "scalability_score": lambda x: x >= 4,
        "gross_margin_percent": lambda x: x > 50
    },
    optional_conditions={
        "tech_differentiation_score": lambda x: x >= 4,
        "annual_revenue_run_rate": lambda x: x > 1000000
    },
    exclusion_conditions={},
    typical_success_rate=(0.60, 0.80),
    typical_funding_stages=["series_a", "series_b"],
    typical_team_size=(50, 200),
    typical_burn_multiple=(1.5, 2.5),
    typical_growth_rate=(100, 200),
    typical_gross_margin=(60, 80),
    example_companies=["Twilio", "SendGrid", "AWS", "Datadog"],
    evolution_paths=["PLATFORM_INFRASTRUCTURE", "MARKET_LEADER"],
    compatible_patterns=["API_PLATFORM", "DEVELOPER_TOOLS"],
    incompatible_patterns=["FIXED_PRICE_ENTERPRISE", "ONE_TIME_LICENSE"],
    key_success_factors=[
        "Usage naturally grows",
        "Transparent pricing",
        "Cost optimization tools"
    ],
    common_failure_modes=[
        "Unpredictable revenue",
        "Customer bill shock",
        "Complex pricing"
    ],
    strategic_recommendations=[
        "Build usage dashboards",
        "Offer committed use discounts",
        "Focus on customer success"
    ]
)

HARDWARE_AS_SERVICE = PatternDefinition(
    name="HARDWARE_AS_SERVICE",
    master_category=MasterCategory.BUSINESS_MODEL,
    description="Hardware with recurring service revenue",
    required_conditions={
        "gross_margin_percent": lambda x: 30 <= x <= 60,
        "patent_count": lambda x: x > 0,
        "has_debt": lambda x: x == 1  # Often needs debt financing
    },
    optional_conditions={
        "regulatory_advantage_present": lambda x: x == 1,
        "tech_differentiation_score": lambda x: x >= 4
    },
    exclusion_conditions={
        "scalability_score": lambda x: x > 4  # Not infinitely scalable
    },
    typical_success_rate=(0.40, 0.65),
    typical_funding_stages=["series_a", "series_b", "series_c"],
    typical_team_size=(50, 500),
    typical_burn_multiple=(2.0, 5.0),
    typical_growth_rate=(50, 150),
    typical_gross_margin=(30, 50),
    example_companies=["Peloton", "Tesla", "Whoop", "Eight Sleep"],
    evolution_paths=["PLATFORM_ECOSYSTEM", "VERTICAL_INTEGRATION"],
    compatible_patterns=["SUBSCRIPTION_RECURRING", "DIRECT_TO_CONSUMER"],
    incompatible_patterns=["PURE_SOFTWARE", "ASSET_LIGHT_DIGITAL"],
    key_success_factors=[
        "Strong brand",
        "Service attachment",
        "Supply chain excellence"
    ],
    common_failure_modes=[
        "Inventory management",
        "High capital requirements",
        "Service scaling challenges"
    ],
    strategic_recommendations=[
        "Focus on subscription attach rate",
        "Build community features",
        "Manage working capital carefully"
    ]
)

DATA_MONETIZATION = PatternDefinition(
    name="DATA_MONETIZATION",
    master_category=MasterCategory.BUSINESS_MODEL,
    description="Monetizing aggregated data or insights",
    required_conditions={
        "has_data_moat": lambda x: x == 1,
        "customer_count": lambda x: x > 10000,
        "tech_differentiation_score": lambda x: x >= 3
    },
    optional_conditions={
        "network_effects_present": lambda x: x == 1,
        "regulatory_advantage_present": lambda x: x == 1
    },
    exclusion_conditions={},
    typical_success_rate=(0.50, 0.75),
    typical_funding_stages=["series_a", "series_b"],
    typical_team_size=(30, 150),
    typical_burn_multiple=(1.5, 3.0),
    typical_growth_rate=(80, 150),
    typical_gross_margin=(70, 90),
    example_companies=["Palantir", "Bloomberg", "CoStar", "ZoomInfo"],
    evolution_paths=["AI_ML_CORE", "PLATFORM_INFRASTRUCTURE"],
    compatible_patterns=["NETWORK_EFFECTS", "B2B_ENTERPRISE"],
    incompatible_patterns=["HARDWARE_AS_SERVICE", "LINEAR_SERVICES"],
    key_success_factors=[
        "Data network effects",
        "Unique data sources",
        "Privacy compliance"
    ],
    common_failure_modes=[
        "Privacy concerns",
        "Data quality issues",
        "Commoditization"
    ],
    strategic_recommendations=[
        "Build data moats",
        "Ensure compliance",
        "Create insights layers"
    ]
)

# ==========================================
# 3. TECHNOLOGY DEPTH PATTERNS (6)
# ==========================================

AI_ML_CORE = PatternDefinition(
    name="AI_ML_CORE",
    master_category=MasterCategory.TECHNOLOGY_DEPTH,
    description="AI/ML as core technology differentiator",
    required_conditions={
        "tech_differentiation_score": lambda x: x >= 4,
        "has_data_moat": lambda x: x == 1,
        "domain_expertise_years_avg": lambda x: x > 5
    },
    optional_conditions={
        "patent_count": lambda x: x > 0,
        "prior_successful_exits_count": lambda x: x > 0
    },
    exclusion_conditions={},
    typical_success_rate=(0.50, 0.75),
    typical_funding_stages=["seed", "series_a", "series_b"],
    typical_team_size=(20, 100),
    typical_burn_multiple=(2.0, 4.0),
    typical_growth_rate=(100, 300),
    typical_gross_margin=(60, 85),
    example_companies=["OpenAI", "Anthropic", "Cohere", "Stability AI"],
    evolution_paths=["PLATFORM_INFRASTRUCTURE", "VERTICAL_AI_SOLUTION"],
    compatible_patterns=["DATA_MONETIZATION", "API_PLATFORM"],
    incompatible_patterns=["LOW_TECH_SERVICES", "TRADITIONAL_RETAIL"],
    key_success_factors=[
        "Proprietary models",
        "Data advantages",
        "Top AI talent"
    ],
    common_failure_modes=[
        "Commoditization",
        "High compute costs",
        "Talent retention"
    ],
    strategic_recommendations=[
        "Build proprietary datasets",
        "Focus on specific use cases",
        "Create platform effects"
    ]
)

BLOCKCHAIN_WEB3 = PatternDefinition(
    name="BLOCKCHAIN_WEB3",
    master_category=MasterCategory.TECHNOLOGY_DEPTH,
    description="Blockchain/crypto native business model",
    required_conditions={
        "tech_differentiation_score": lambda x: x >= 4,
        "network_effects_present": lambda x: x == 1,
        "regulatory_advantage_present": lambda x: x == 1
    },
    optional_conditions={
        "community_driven": lambda x: x == 1,
        "has_token": lambda x: x == 1
    },
    exclusion_conditions={},
    typical_success_rate=(0.30, 0.60),
    typical_funding_stages=["seed", "token_sale"],
    typical_team_size=(10, 50),
    typical_burn_multiple=(1.0, 3.0),
    typical_growth_rate=(100, 1000),
    typical_gross_margin=(50, 90),
    example_companies=["Uniswap", "OpenSea", "Chainlink", "Polygon"],
    evolution_paths=["DEFI_PROTOCOL", "WEB3_INFRASTRUCTURE"],
    compatible_patterns=["COMMUNITY_DRIVEN_GROWTH", "OPEN_SOURCE"],
    incompatible_patterns=["TRADITIONAL_FINANCE", "CENTRALIZED_CONTROL"],
    key_success_factors=[
        "Strong community",
        "Token economics",
        "Technical innovation"
    ],
    common_failure_modes=[
        "Regulatory crackdown",
        "Security breaches",
        "Token volatility"
    ],
    strategic_recommendations=[
        "Focus on utility",
        "Build for compliance",
        "Prioritize security"
    ]
)

BIOTECH_LIFESCIENCES = PatternDefinition(
    name="BIOTECH_LIFESCIENCES",
    master_category=MasterCategory.TECHNOLOGY_DEPTH,
    description="Deep biotech with long R&D cycles",
    required_conditions={
        "patent_count": lambda x: x > 5,
        "regulatory_advantage_present": lambda x: x == 1,
        "domain_expertise_years_avg": lambda x: x > 10
    },
    optional_conditions={
        "board_advisor_experience_score": lambda x: x >= 4,
        "total_capital_raised_usd": lambda x: x > 10000000
    },
    exclusion_conditions={
        "revenue_growth_rate_percent": lambda x: x > 200  # Not hypergrowth
    },
    typical_success_rate=(0.35, 0.60),
    typical_funding_stages=["seed", "series_a", "series_b", "series_c"],
    typical_team_size=(20, 200),
    typical_burn_multiple=(5.0, 20.0),
    typical_growth_rate=(0, 100),
    typical_gross_margin=(60, 90),
    example_companies=["Moderna", "BioNTech", "Ginkgo Bioworks", "23andMe"],
    evolution_paths=["PHARMA_PLATFORM", "DIAGNOSTIC_LEADER"],
    compatible_patterns=["GRANT_RESEARCH_FUNDED", "STRATEGIC_PARTNERSHIPS"],
    incompatible_patterns=["BOOTSTRAP_PROFITABLE", "QUICK_FLIP"],
    key_success_factors=[
        "Strong IP portfolio",
        "Clinical validation",
        "Regulatory expertise"
    ],
    common_failure_modes=[
        "Clinical trial failures",
        "Regulatory delays",
        "Funding gaps"
    ],
    strategic_recommendations=[
        "Build platform capabilities",
        "Partner with pharma early",
        "Manage cash carefully"
    ]
)

HARDWARE_ROBOTICS = PatternDefinition(
    name="HARDWARE_ROBOTICS",
    master_category=MasterCategory.TECHNOLOGY_DEPTH,
    description="Hardware/robotics with software integration",
    required_conditions={
        "patent_count": lambda x: x > 0,
        "tech_differentiation_score": lambda x: x >= 4,
        "gross_margin_percent": lambda x: x < 60
    },
    optional_conditions={
        "regulatory_advantage_present": lambda x: x == 1,
        "has_debt": lambda x: x == 1
    },
    exclusion_conditions={},
    typical_success_rate=(0.40, 0.65),
    typical_funding_stages=["series_a", "series_b", "series_c"],
    typical_team_size=(50, 300),
    typical_burn_multiple=(2.5, 5.0),
    typical_growth_rate=(50, 150),
    typical_gross_margin=(25, 50),
    example_companies=["Boston Dynamics", "Zipline", "Nuro", "Cruise"],
    evolution_paths=["AUTONOMOUS_SYSTEMS", "INDUSTRIAL_IOT"],
    compatible_patterns=["AI_ML_CORE", "HARDWARE_AS_SERVICE"],
    incompatible_patterns=["PURE_SOFTWARE", "ASSET_LIGHT_DIGITAL"],
    key_success_factors=[
        "Technical breakthroughs",
        "Manufacturing excellence",
        "Software integration"
    ],
    common_failure_modes=[
        "Hardware complexity",
        "Long development cycles",
        "High capital needs"
    ],
    strategic_recommendations=[
        "Start with narrow use case",
        "Build software moat",
        "Partner for manufacturing"
    ]
)

QUANTUM_COMPUTING = PatternDefinition(
    name="QUANTUM_COMPUTING",
    master_category=MasterCategory.TECHNOLOGY_DEPTH,
    description="Quantum computing hardware or software",
    required_conditions={
        "tech_differentiation_score": lambda x: x == 5,
        "patent_count": lambda x: x > 10,
        "domain_expertise_years_avg": lambda x: x > 15
    },
    optional_conditions={
        "total_capital_raised_usd": lambda x: x > 50000000,
        "board_advisor_experience_score": lambda x: x == 5
    },
    exclusion_conditions={
        "annual_revenue_run_rate": lambda x: x > 10000000  # Pre-revenue
    },
    typical_success_rate=(0.30, 0.60),
    typical_funding_stages=["series_a", "series_b", "series_c", "series_d"],
    typical_team_size=(50, 200),
    typical_burn_multiple=(10.0, 50.0),
    typical_growth_rate=(0, 50),
    typical_gross_margin=(0, 50),
    example_companies=["Rigetti", "IonQ", "PsiQuantum", "Atom Computing"],
    evolution_paths=["QUANTUM_CLOUD", "QUANTUM_APPLICATIONS"],
    compatible_patterns=["GRANT_RESEARCH_FUNDED", "DEEP_TECH_CONSORTIUM"],
    incompatible_patterns=["BOOTSTRAP_PROFITABLE", "QUICK_EXIT"],
    key_success_factors=[
        "Scientific breakthroughs",
        "Patient capital",
        "Government contracts"
    ],
    common_failure_modes=[
        "Technical barriers",
        "Funding exhaustion",
        "Talent competition"
    ],
    strategic_recommendations=[
        "Focus on near-term applications",
        "Build ecosystem partnerships",
        "Secure government funding"
    ]
)

PLATFORM_INFRASTRUCTURE = PatternDefinition(
    name="PLATFORM_INFRASTRUCTURE",
    master_category=MasterCategory.TECHNOLOGY_DEPTH,
    description="Infrastructure platform for developers/enterprises",
    required_conditions={
        "scalability_score": lambda x: x >= 4,
        "tech_differentiation_score": lambda x: x >= 4,
        "gross_margin_percent": lambda x: x > 60
    },
    optional_conditions={
        "network_effects_present": lambda x: x == 1,
        "developer_adoption": lambda x: x > 1000
    },
    exclusion_conditions={},
    typical_success_rate=(0.55, 0.80),
    typical_funding_stages=["series_a", "series_b", "series_c"],
    typical_team_size=(50, 500),
    typical_burn_multiple=(2.0, 4.0),
    typical_growth_rate=(100, 200),
    typical_gross_margin=(70, 85),
    example_companies=["Stripe", "Twilio", "Snowflake", "Databricks"],
    evolution_paths=["MARKET_LEADER", "PLATFORM_ECOSYSTEM"],
    compatible_patterns=["USAGE_BASED_PRICING", "DEVELOPER_FIRST"],
    incompatible_patterns=["CONSUMER_APPS", "LOCAL_SERVICES"],
    key_success_factors=[
        "Developer experience",
        "Reliability at scale",
        "Ecosystem building"
    ],
    common_failure_modes=[
        "Complexity creep",
        "Competition from cloud giants",
        "Migration difficulties"
    ],
    strategic_recommendations=[
        "Focus on developer love",
        "Build network effects",
        "Expand use cases gradually"
    ]
)

# ==========================================
# 4. MARKET APPROACH PATTERNS (5)
# ==========================================

B2B_ENTERPRISE = PatternDefinition(
    name="B2B_ENTERPRISE",
    master_category=MasterCategory.MARKET_APPROACH,
    description="Selling to large enterprises (Fortune 5000)",
    required_conditions={
        "ltv_cac_ratio": lambda x: x > 3,
        "annual_revenue_run_rate": lambda x: x > 1000000,
        "customer_concentration_percent": lambda x: x > 15
    },
    optional_conditions={
        "board_advisor_experience_score": lambda x: x >= 4,
        "gross_margin_percent": lambda x: x > 70
    },
    exclusion_conditions={
        "customer_count": lambda x: x > 10000  # Not mass market
    },
    typical_success_rate=(0.55, 0.75),
    typical_funding_stages=["series_a", "series_b", "series_c"],
    typical_team_size=(50, 500),
    typical_burn_multiple=(2.0, 4.0),
    typical_growth_rate=(50, 100),
    typical_gross_margin=(70, 85),
    example_companies=["Salesforce", "Workday", "ServiceNow", "Palantir"],
    evolution_paths=["MARKET_LEADER", "PLATFORM_PLAY"],
    compatible_patterns=["SALES_LED_GROWTH", "ENTERPRISE_LAND_EXPAND"],
    incompatible_patterns=["B2C_MASS_MARKET", "VIRAL_CONSUMER_GROWTH"],
    key_success_factors=[
        "Enterprise features",
        "Security/compliance",
        "Professional services"
    ],
    common_failure_modes=[
        "Long sales cycles",
        "High acquisition costs",
        "Complex implementations"
    ],
    strategic_recommendations=[
        "Build for Fortune 500 needs",
        "Invest in customer success",
        "Create partner ecosystem"
    ]
)

B2B_SMB_FOCUSED = PatternDefinition(
    name="B2B_SMB_FOCUSED",
    master_category=MasterCategory.MARKET_APPROACH,
    description="Targeting small and medium businesses",
    required_conditions={
        "customer_count": lambda x: x > 1000,
        "customer_concentration_percent": lambda x: x < 20,
        "ltv_cac_ratio": lambda x: x > 2
    },
    optional_conditions={
        "product_retention_30d": lambda x: x > 0.6,
        "gross_margin_percent": lambda x: x > 60
    },
    exclusion_conditions={
        "annual_revenue_run_rate": lambda x: x < 100000  # Some traction
    },
    typical_success_rate=(0.45, 0.65),
    typical_funding_stages=["seed", "series_a", "series_b"],
    typical_team_size=(20, 200),
    typical_burn_multiple=(1.5, 3.0),
    typical_growth_rate=(80, 150),
    typical_gross_margin=(60, 80),
    example_companies=["Square", "Gusto", "Shopify", "HubSpot"],
    evolution_paths=["B2B_ENTERPRISE", "PLATFORM_ECOSYSTEM"],
    compatible_patterns=["PLG_BOTTOM_UP", "FREEMIUM_CONVERSION"],
    incompatible_patterns=["ENTERPRISE_ONLY", "HIGH_TOUCH_SALES"],
    key_success_factors=[
        "Self-serve onboarding",
        "Simple pricing",
        "Low touch sales"
    ],
    common_failure_modes=[
        "High churn",
        "Limited expansion",
        "Price sensitivity"
    ],
    strategic_recommendations=[
        "Automate everything",
        "Build for simplicity",
        "Focus on retention"
    ]
)

B2C_MASS_MARKET = PatternDefinition(
    name="B2C_MASS_MARKET",
    master_category=MasterCategory.MARKET_APPROACH,
    description="Direct to consumer mass market",
    required_conditions={
        "customer_count": lambda x: x > 10000,
        "dau_mau_ratio": lambda x: x > 0.2,
        "user_growth_rate_percent": lambda x: x > 50
    },
    optional_conditions={
        "brand_strength_score": lambda x: x >= 4,
        "network_effects_present": lambda x: x == 1
    },
    exclusion_conditions={
        "customer_concentration_percent": lambda x: x > 30
    },
    typical_success_rate=(0.35, 0.60),
    typical_funding_stages=["seed", "series_a", "series_b"],
    typical_team_size=(20, 200),
    typical_burn_multiple=(2.0, 5.0),
    typical_growth_rate=(100, 300),
    typical_gross_margin=(30, 70),
    example_companies=["Netflix", "Spotify", "Duolingo", "Calm"],
    evolution_paths=["PLATFORM_PLAY", "INTERNATIONAL_EXPANSION"],
    compatible_patterns=["VIRAL_CONSUMER_GROWTH", "FREEMIUM_CONVERSION"],
    incompatible_patterns=["B2B_ENTERPRISE", "HIGH_TOUCH_SALES"],
    key_success_factors=[
        "Product virality",
        "Brand building",
        "User engagement"
    ],
    common_failure_modes=[
        "High acquisition costs",
        "Platform dependence",
        "Monetization challenges"
    ],
    strategic_recommendations=[
        "Focus on organic growth",
        "Build direct relationships",
        "Optimize for engagement"
    ]
)

B2B2C_EMBEDDED = PatternDefinition(
    name="B2B2C_EMBEDDED",
    master_category=MasterCategory.MARKET_APPROACH,
    description="Reaching consumers through business partners",
    required_conditions={
        "customer_concentration_percent": lambda x: x > 30,
        "ltv_cac_ratio": lambda x: x > 3,
        "gross_margin_percent": lambda x: x > 50
    },
    optional_conditions={
        "network_effects_present": lambda x: x == 1,
        "regulatory_advantage_present": lambda x: x == 1
    },
    exclusion_conditions={},
    typical_success_rate=(0.50, 0.70),
    typical_funding_stages=["series_a", "series_b"],
    typical_team_size=(30, 150),
    typical_burn_multiple=(1.5, 3.0),
    typical_growth_rate=(80, 150),
    typical_gross_margin=(60, 80),
    example_companies=["Affirm", "Plaid", "Marqeta", "Checkr"],
    evolution_paths=["PLATFORM_INFRASTRUCTURE", "DIRECT_TO_CONSUMER"],
    compatible_patterns=["API_PLATFORM", "WHITE_LABEL"],
    incompatible_patterns=["DIRECT_CONSUMER_BRAND", "B2C_MASS_MARKET"],
    key_success_factors=[
        "Partner integration",
        "White label capabilities",
        "API excellence"
    ],
    common_failure_modes=[
        "Partner concentration",
        "Channel conflict",
        "Limited brand value"
    ],
    strategic_recommendations=[
        "Diversify partners",
        "Build switching costs",
        "Consider direct channel"
    ]
)

B2G_GOVERNMENT = PatternDefinition(
    name="B2G_GOVERNMENT",
    master_category=MasterCategory.MARKET_APPROACH,
    description="Selling to government agencies",
    required_conditions={
        "regulatory_advantage_present": lambda x: x == 1,
        "board_advisor_experience_score": lambda x: x >= 4,
        "years_experience_avg": lambda x: x > 10
    },
    optional_conditions={
        "prior_successful_exits_count": lambda x: x > 0,
        "team_diversity_percent": lambda x: x > 30
    },
    exclusion_conditions={},
    typical_success_rate=(0.45, 0.65),
    typical_funding_stages=["series_a", "series_b", "series_c"],
    typical_team_size=(50, 300),
    typical_burn_multiple=(2.0, 4.0),
    typical_growth_rate=(30, 80),
    typical_gross_margin=(50, 80),
    example_companies=["Palantir", "Anduril", "SpaceX", "Scale AI"],
    evolution_paths=["DEFENSE_CONTRACTOR", "CIVIC_TECH_LEADER"],
    compatible_patterns=["HIGH_SECURITY", "MISSION_CRITICAL"],
    incompatible_patterns=["CONSUMER_SOCIAL", "QUICK_FLIP"],
    key_success_factors=[
        "Security clearances",
        "Compliance expertise",
        "Long-term contracts"
    ],
    common_failure_modes=[
        "Long sales cycles",
        "Political risk",
        "Procurement complexity"
    ],
    strategic_recommendations=[
        "Hire government expertise",
        "Start with pilots",
        "Build for compliance"
    ]
)

# ==========================================
# 5. INDUSTRY VERTICAL PATTERNS (8)
# ==========================================

FINTECH_PAYMENTS = PatternDefinition(
    name="FINTECH_PAYMENTS",
    master_category=MasterCategory.INDUSTRY_VERTICAL,
    description="Financial technology focused on payments/banking",
    required_conditions={
        "regulatory_advantage_present": lambda x: x == 1,
        "gross_margin_percent": lambda x: x > 40,
        "customer_count": lambda x: x > 1000
    },
    optional_conditions={
        "network_effects_present": lambda x: x == 1,
        "has_licenses": lambda x: x == 1
    },
    exclusion_conditions={},
    typical_success_rate=(0.45, 0.70),
    typical_funding_stages=["series_a", "series_b", "series_c"],
    typical_team_size=(50, 300),
    typical_burn_multiple=(2.0, 4.0),
    typical_growth_rate=(80, 200),
    typical_gross_margin=(40, 70),
    example_companies=["Stripe", "Square", "Adyen", "Marqeta"],
    evolution_paths=["BANKING_AS_SERVICE", "SUPER_APP"],
    compatible_patterns=["API_PLATFORM", "B2B2C_EMBEDDED"],
    incompatible_patterns=["UNREGULATED", "MOVE_FAST_BREAK"],
    key_success_factors=[
        "Regulatory compliance",
        "Fraud prevention",
        "Scale economics"
    ],
    common_failure_modes=[
        "Regulatory issues",
        "Fraud losses",
        "Commoditization"
    ],
    strategic_recommendations=[
        "Build compliance early",
        "Focus on developer experience",
        "Expand payment types"
    ]
)

HEALTHTECH_DIGITAL = PatternDefinition(
    name="HEALTHTECH_DIGITAL",
    master_category=MasterCategory.INDUSTRY_VERTICAL,
    description="Digital health and medical technology",
    required_conditions={
        "regulatory_advantage_present": lambda x: x == 1,
        "domain_expertise_years_avg": lambda x: x > 8,
        "gross_margin_percent": lambda x: x > 50
    },
    optional_conditions={
        "has_clinical_validation": lambda x: x == 1,
        "patent_count": lambda x: x > 0
    },
    exclusion_conditions={},
    typical_success_rate=(0.40, 0.65),
    typical_funding_stages=["series_a", "series_b", "series_c"],
    typical_team_size=(30, 200),
    typical_burn_multiple=(2.0, 5.0),
    typical_growth_rate=(50, 150),
    typical_gross_margin=(50, 80),
    example_companies=["Teladoc", "Oscar Health", "Ro", "Hims"],
    evolution_paths=["INTEGRATED_CARE", "PHARMA_PLATFORM"],
    compatible_patterns=["B2B2C_EMBEDDED", "SUBSCRIPTION_RECURRING"],
    incompatible_patterns=["MOVE_FAST", "UNREGULATED"],
    key_success_factors=[
        "Clinical validation",
        "Regulatory approval",
        "Provider adoption"
    ],
    common_failure_modes=[
        "Regulatory delays",
        "Reimbursement challenges",
        "Slow adoption"
    ],
    strategic_recommendations=[
        "Partner with providers",
        "Focus on outcomes",
        "Build for compliance"
    ]
)

EDTECH_LEARNING = PatternDefinition(
    name="EDTECH_LEARNING",
    master_category=MasterCategory.INDUSTRY_VERTICAL,
    description="Education technology and online learning",
    required_conditions={
        "customer_count": lambda x: x > 5000,
        "product_retention_30d": lambda x: x > 0.5,
        "gross_margin_percent": lambda x: x > 60
    },
    optional_conditions={
        "dau_mau_ratio": lambda x: x > 0.3,
        "has_content_library": lambda x: x == 1
    },
    exclusion_conditions={},
    typical_success_rate=(0.40, 0.60),
    typical_funding_stages=["seed", "series_a", "series_b"],
    typical_team_size=(20, 150),
    typical_burn_multiple=(1.5, 3.5),
    typical_growth_rate=(60, 150),
    typical_gross_margin=(60, 80),
    example_companies=["Coursera", "Duolingo", "MasterClass", "Khan Academy"],
    evolution_paths=["CREDENTIALING_PLATFORM", "CORPORATE_TRAINING"],
    compatible_patterns=["FREEMIUM_CONVERSION", "SUBSCRIPTION_RECURRING"],
    incompatible_patterns=["HIGH_TOUCH_SALES", "HARDWARE_HEAVY"],
    key_success_factors=[
        "Engaging content",
        "Learning outcomes",
        "Completion rates"
    ],
    common_failure_modes=[
        "Low engagement",
        "Content costs",
        "Seasonal usage"
    ],
    strategic_recommendations=[
        "Focus on outcomes",
        "Build community",
        "Gamify experience"
    ]
)

PROPTECH_REAL_ESTATE = PatternDefinition(
    name="PROPTECH_REAL_ESTATE",
    master_category=MasterCategory.INDUSTRY_VERTICAL,
    description="Property technology and real estate innovation",
    required_conditions={
        "gross_margin_percent": lambda x: x > 30,
        "market_growth_rate_percent": lambda x: x > 10,
        "total_capital_raised_usd": lambda x: x > 5000000
    },
    optional_conditions={
        "has_marketplace": lambda x: x == 1,
        "regulatory_advantage_present": lambda x: x == 1
    },
    exclusion_conditions={},
    typical_success_rate=(0.40, 0.65),
    typical_funding_stages=["series_a", "series_b", "series_c"],
    typical_team_size=(30, 300),
    typical_burn_multiple=(2.0, 5.0),
    typical_growth_rate=(50, 150),
    typical_gross_margin=(30, 60),
    example_companies=["Opendoor", "Compass", "Zillow", "Airbnb"],
    evolution_paths=["IBUYING_PLATFORM", "PROPERTY_MANAGEMENT"],
    compatible_patterns=["MARKETPLACE", "ASSET_HEAVY"],
    incompatible_patterns=["PURE_SOFTWARE", "QUICK_SCALE"],
    key_success_factors=[
        "Local market knowledge",
        "Capital efficiency",
        "Technology leverage"
    ],
    common_failure_modes=[
        "Capital intensity",
        "Market timing",
        "Regulatory issues"
    ],
    strategic_recommendations=[
        "Start in one market",
        "Build data advantages",
        "Partner with incumbents"
    ]
)

AGTECH_FOOD = PatternDefinition(
    name="AGTECH_FOOD",
    master_category=MasterCategory.INDUSTRY_VERTICAL,
    description="Agriculture technology and food innovation",
    required_conditions={
        "domain_expertise_years_avg": lambda x: x > 5,
        "gross_margin_percent": lambda x: x > 20,
        "has_sustainability_focus": lambda x: x == 1
    },
    optional_conditions={
        "patent_count": lambda x: x > 0,
        "regulatory_advantage_present": lambda x: x == 1
    },
    exclusion_conditions={},
    typical_success_rate=(0.35, 0.60),
    typical_funding_stages=["seed", "series_a", "series_b"],
    typical_team_size=(20, 150),
    typical_burn_multiple=(2.0, 5.0),
    typical_growth_rate=(50, 150),
    typical_gross_margin=(20, 60),
    example_companies=["Impossible Foods", "Beyond Meat", "Indigo Ag", "Plenty"],
    evolution_paths=["SUSTAINABLE_FOOD", "SUPPLY_CHAIN_TECH"],
    compatible_patterns=["BIOTECH", "HARDWARE_ROBOTICS"],
    incompatible_patterns=["PURE_DIGITAL", "QUICK_RETURNS"],
    key_success_factors=[
        "Scientific validation",
        "Scale manufacturing",
        "Distribution partnerships"
    ],
    common_failure_modes=[
        "Long development cycles",
        "Scaling challenges",
        "Market education"
    ],
    strategic_recommendations=[
        "Partner with industry",
        "Focus on ROI",
        "Build for farmers"
    ]
)

CLIMATE_SUSTAINABILITY = PatternDefinition(
    name="CLIMATE_SUSTAINABILITY",
    master_category=MasterCategory.INDUSTRY_VERTICAL,
    description="Climate tech and sustainability solutions",
    required_conditions={
        "has_sustainability_metrics": lambda x: x == 1,
        "tech_differentiation_score": lambda x: x >= 3,
        "domain_expertise_years_avg": lambda x: x > 5
    },
    optional_conditions={
        "regulatory_advantage_present": lambda x: x == 1,
        "grant_funding": lambda x: x > 0
    },
    exclusion_conditions={},
    typical_success_rate=(0.40, 0.65),
    typical_funding_stages=["seed", "series_a", "series_b"],
    typical_team_size=(20, 200),
    typical_burn_multiple=(2.0, 5.0),
    typical_growth_rate=(50, 200),
    typical_gross_margin=(30, 70),
    example_companies=["Tesla", "Rivian", "Northvolt", "Carbon Engineering"],
    evolution_paths=["INFRASTRUCTURE_PLAY", "CARBON_MARKETS"],
    compatible_patterns=["DEEP_TECH", "GRANT_FUNDED"],
    incompatible_patterns=["QUICK_PROFIT", "HIGH_EMISSIONS"],
    key_success_factors=[
        "Technology breakthrough",
        "Policy tailwinds",
        "Cost competitiveness"
    ],
    common_failure_modes=[
        "Technology risk",
        "Policy changes",
        "Long payback periods"
    ],
    strategic_recommendations=[
        "Align with policy",
        "Focus on economics",
        "Build coalitions"
    ]
)

RETAIL_COMMERCE = PatternDefinition(
    name="RETAIL_COMMERCE",
    master_category=MasterCategory.INDUSTRY_VERTICAL,
    description="Retail technology and e-commerce innovation",
    required_conditions={
        "customer_count": lambda x: x > 10000,
        "gross_margin_percent": lambda x: x > 20,
        "brand_strength_score": lambda x: x >= 3
    },
    optional_conditions={
        "has_physical_stores": lambda x: x == 1,
        "has_private_label": lambda x: x == 1
    },
    exclusion_conditions={},
    typical_success_rate=(0.35, 0.60),
    typical_funding_stages=["seed", "series_a", "series_b"],
    typical_team_size=(30, 300),
    typical_burn_multiple=(2.0, 5.0),
    typical_growth_rate=(50, 200),
    typical_gross_margin=(20, 50),
    example_companies=["Warby Parker", "Allbirds", "Glossier", "Faire"],
    evolution_paths=["OMNICHANNEL", "BRAND_PLATFORM"],
    compatible_patterns=["D2C_BRAND", "MARKETPLACE"],
    incompatible_patterns=["B2B_ONLY", "HIGH_MARGIN_SOFTWARE"],
    key_success_factors=[
        "Brand building",
        "Supply chain efficiency",
        "Customer acquisition"
    ],
    common_failure_modes=[
        "CAC/LTV imbalance",
        "Inventory management",
        "Competition"
    ],
    strategic_recommendations=[
        "Build brand moat",
        "Optimize supply chain",
        "Focus on retention"
    ]
)

MOBILITY_TRANSPORT = PatternDefinition(
    name="MOBILITY_TRANSPORT",
    master_category=MasterCategory.INDUSTRY_VERTICAL,
    description="Transportation and mobility solutions",
    required_conditions={
        "scalability_score": lambda x: x >= 3,
        "user_growth_rate_percent": lambda x: x > 50,
        "has_ops_excellence": lambda x: x == 1
    },
    optional_conditions={
        "has_fleet": lambda x: x == 1,
        "regulatory_advantage_present": lambda x: x == 1
    },
    exclusion_conditions={},
    typical_success_rate=(0.35, 0.60),
    typical_funding_stages=["series_a", "series_b", "series_c"],
    typical_team_size=(50, 1000),
    typical_burn_multiple=(3.0, 10.0),
    typical_growth_rate=(100, 300),
    typical_gross_margin=(10, 40),
    example_companies=["Uber", "Lyft", "Lime", "Bird"],
    evolution_paths=["AUTONOMOUS_VEHICLES", "LOGISTICS_PLATFORM"],
    compatible_patterns=["GEOGRAPHIC_EXPANSION", "PLATFORM_NETWORK_EFFECTS"],
    incompatible_patterns=["ASSET_LIGHT", "HIGH_MARGIN"],
    key_success_factors=[
        "Operational excellence",
        "Network density",
        "Regulatory navigation"
    ],
    common_failure_modes=[
        "Unit economics",
        "Regulatory backlash",
        "Competition"
    ],
    strategic_recommendations=[
        "Focus on unit economics",
        "Build regulatory relationships",
        "Expand to adjacencies"
    ]
)

# ==========================================
# 6. OPERATIONAL MODEL PATTERNS (5)
# ==========================================

ASSET_LIGHT_DIGITAL = PatternDefinition(
    name="ASSET_LIGHT_DIGITAL",
    master_category=MasterCategory.OPERATIONAL_MODEL,
    description="Pure digital business with minimal physical assets",
    required_conditions={
        "gross_margin_percent": lambda x: x > 70,
        "scalability_score": lambda x: x >= 4,
        "has_physical_assets": lambda x: x == 0
    },
    optional_conditions={
        "network_effects_present": lambda x: x == 1,
        "product_stage": lambda x: x in ["growth", "mature"]
    },
    exclusion_conditions={
        "has_inventory": lambda x: x == 1
    },
    typical_success_rate=(0.50, 0.75),
    typical_funding_stages=["seed", "series_a", "series_b"],
    typical_team_size=(10, 200),
    typical_burn_multiple=(1.0, 3.0),
    typical_growth_rate=(100, 300),
    typical_gross_margin=(70, 90),
    example_companies=["Zoom", "Slack", "Dropbox", "GitHub"],
    evolution_paths=["PLATFORM_PLAY", "MARKET_LEADER"],
    compatible_patterns=["PURE_SOFTWARE", "SUBSCRIPTION_RECURRING"],
    incompatible_patterns=["ASSET_HEAVY_OPERATIONS", "HARDWARE_PRODUCT"],
    key_success_factors=[
        "Scalable infrastructure",
        "Low marginal costs",
        "Global reach"
    ],
    common_failure_modes=[
        "Competition",
        "Platform risk",
        "Feature commoditization"
    ],
    strategic_recommendations=[
        "Build switching costs",
        "Expand globally fast",
        "Focus on product"
    ]
)

ASSET_HEAVY_OPERATIONS = PatternDefinition(
    name="ASSET_HEAVY_OPERATIONS",
    master_category=MasterCategory.OPERATIONAL_MODEL,
    description="Significant physical assets or operations",
    required_conditions={
        "gross_margin_percent": lambda x: x < 50,
        "has_physical_assets": lambda x: x == 1,
        "has_debt": lambda x: x == 1
    },
    optional_conditions={
        "team_size_full_time": lambda x: x > 100,
        "has_fleet_or_inventory": lambda x: x == 1
    },
    exclusion_conditions={
        "scalability_score": lambda x: x > 4
    },
    typical_success_rate=(0.35, 0.60),
    typical_funding_stages=["series_a", "series_b", "series_c", "debt"],
    typical_team_size=(100, 5000),
    typical_burn_multiple=(2.0, 8.0),
    typical_growth_rate=(50, 150),
    typical_gross_margin=(15, 40),
    example_companies=["WeWork", "Opendoor", "Carvana", "Sweetgreen"],
    evolution_paths=["OPERATIONAL_EXCELLENCE", "TECH_ENABLED_TRADITIONAL"],
    compatible_patterns=["GEOGRAPHIC_EXPANSION", "VERTICAL_INTEGRATION"],
    incompatible_patterns=["ASSET_LIGHT_DIGITAL", "PURE_SOFTWARE"],
    key_success_factors=[
        "Operational efficiency",
        "Capital management",
        "Technology leverage"
    ],
    common_failure_modes=[
        "Capital intensity",
        "Scaling challenges",
        "Low margins"
    ],
    strategic_recommendations=[
        "Focus on unit economics",
        "Use debt wisely",
        "Build tech advantages"
    ]
)

HYBRID_DIGITAL_PHYSICAL = PatternDefinition(
    name="HYBRID_DIGITAL_PHYSICAL",
    master_category=MasterCategory.OPERATIONAL_MODEL,
    description="Combination of digital platform and physical operations",
    required_conditions={
        "gross_margin_percent": lambda x: 30 <= x <= 70,
        "has_digital_platform": lambda x: x == 1,
        "has_physical_component": lambda x: x == 1
    },
    optional_conditions={
        "network_effects_present": lambda x: x == 1,
        "brand_strength_score": lambda x: x >= 3
    },
    exclusion_conditions={},
    typical_success_rate=(0.45, 0.70),
    typical_funding_stages=["series_a", "series_b", "series_c"],
    typical_team_size=(50, 1000),
    typical_burn_multiple=(2.0, 5.0),
    typical_growth_rate=(80, 200),
    typical_gross_margin=(30, 60),
    example_companies=["Peloton", "Warby Parker", "Casper", "Sweetgreen"],
    evolution_paths=["OMNICHANNEL_LEADER", "PLATFORM_EXPANSION"],
    compatible_patterns=["D2C_BRAND", "SUBSCRIPTION_RECURRING"],
    incompatible_patterns=["PURE_DIGITAL", "PURE_PHYSICAL"],
    key_success_factors=[
        "Seamless integration",
        "Brand strength",
        "Operational efficiency"
    ],
    common_failure_modes=[
        "Complexity management",
        "Channel conflict",
        "Margin pressure"
    ],
    strategic_recommendations=[
        "Integrate channels",
        "Leverage data",
        "Build unified experience"
    ]
)

PURE_SOFTWARE = PatternDefinition(
    name="PURE_SOFTWARE",
    master_category=MasterCategory.OPERATIONAL_MODEL,
    description="Software-only business model",
    required_conditions={
        "gross_margin_percent": lambda x: x > 80,
        "scalability_score": lambda x: x >= 4,
        "tech_differentiation_score": lambda x: x >= 3
    },
    optional_conditions={
        "product_retention_30d": lambda x: x > 0.7,
        "ltv_cac_ratio": lambda x: x > 3
    },
    exclusion_conditions={
        "has_hardware_component": lambda x: x == 1
    },
    typical_success_rate=(0.55, 0.80),
    typical_funding_stages=["seed", "series_a", "series_b"],
    typical_team_size=(10, 500),
    typical_burn_multiple=(1.0, 3.0),
    typical_growth_rate=(100, 300),
    typical_gross_margin=(80, 95),
    example_companies=["Salesforce", "Adobe", "Atlassian", "Shopify"],
    evolution_paths=["PLATFORM_PLAY", "MARKET_LEADER"],
    compatible_patterns=["SUBSCRIPTION_RECURRING", "PLG_BOTTOM_UP"],
    incompatible_patterns=["HARDWARE_PRODUCT", "SERVICE_HEAVY"],
    key_success_factors=[
        "Product excellence",
        "Low acquisition costs",
        "High retention"
    ],
    common_failure_modes=[
        "Feature competition",
        "Open source disruption",
        "Platform shifts"
    ],
    strategic_recommendations=[
        "Build moats",
        "Expand use cases",
        "Focus on stickiness"
    ]
)

SERVICE_ENABLED_TECH = PatternDefinition(
    name="SERVICE_ENABLED_TECH",
    master_category=MasterCategory.OPERATIONAL_MODEL,
    description="Technology with significant service component",
    required_conditions={
        "gross_margin_percent": lambda x: 40 <= x <= 70,
        "has_services_revenue": lambda x: x == 1,
        "team_size_full_time": lambda x: x > 50
    },
    optional_conditions={
        "has_implementation_team": lambda x: x == 1,
        "enterprise_focused": lambda x: x == 1
    },
    exclusion_conditions={},
    typical_success_rate=(0.45, 0.65),
    typical_funding_stages=["series_a", "series_b", "series_c"],
    typical_team_size=(100, 1000),
    typical_burn_multiple=(2.0, 4.0),
    typical_growth_rate=(50, 100),
    typical_gross_margin=(40, 65),
    example_companies=["Palantir", "Thoughtworks", "EPAM", "Globant"],
    evolution_paths=["PURE_SOFTWARE", "CONSULTING_SCALE"],
    compatible_patterns=["B2B_ENTERPRISE", "COMPLEX_IMPLEMENTATION"],
    incompatible_patterns=["PURE_PRODUCT", "SELF_SERVE"],
    key_success_factors=[
        "Service efficiency",
        "Productization",
        "Customer success"
    ],
    common_failure_modes=[
        "Service scaling",
        "Margin pressure",
        "Talent costs"
    ],
    strategic_recommendations=[
        "Productize services",
        "Build playbooks",
        "Focus on repeatability"
    ]
)

# ==========================================
# 7. FUNDING PROFILE PATTERNS (4)
# ==========================================

VC_HYPERGROWTH = PatternDefinition(
    name="VC_HYPERGROWTH",
    master_category=MasterCategory.FUNDING_PROFILE,
    description="Venture-backed with aggressive growth targets",
    required_conditions={
        "total_capital_raised_usd": lambda x: x > 10000000,
        "revenue_growth_rate_percent": lambda x: x > 100,
        "burn_multiple": lambda x: x > 2
    },
    optional_conditions={
        "investor_tier_primary": lambda x: x in ["tier_1", "tier_2"],
        "prior_successful_exits_count": lambda x: x > 0
    },
    exclusion_conditions={
        "profitable": lambda x: x == 1
    },
    typical_success_rate=(0.40, 0.70),
    typical_funding_stages=["series_a", "series_b", "series_c"],
    typical_team_size=(50, 500),
    typical_burn_multiple=(2.5, 10.0),
    typical_growth_rate=(150, 500),
    typical_gross_margin=(50, 85),
    example_companies=["Uber", "WeWork", "DoorDash", "Instacart"],
    evolution_paths=["IPO_TRACK", "ACQUISITION_TARGET"],
    compatible_patterns=["BLITZSCALE", "WINNER_TAKES_ALL"],
    incompatible_patterns=["BOOTSTRAP_PROFITABLE", "LIFESTYLE_BUSINESS"],
    key_success_factors=[
        "Market leadership",
        "Fundraising ability",
        "Execution speed"
    ],
    common_failure_modes=[
        "Cash burn",
        "Growth at all costs",
        "Valuation pressure"
    ],
    strategic_recommendations=[
        "Focus on market share",
        "Build barriers fast",
        "Plan next funding early"
    ]
)

BOOTSTRAP_PROFITABLE = PatternDefinition(
    name="BOOTSTRAP_PROFITABLE",
    master_category=MasterCategory.FUNDING_PROFILE,
    description="Self-funded with focus on profitability",
    required_conditions={
        "burn_multiple": lambda x: x < 1,
        "gross_margin_percent": lambda x: x > 60,
        "profitable": lambda x: x == 1
    },
    optional_conditions={
        "total_capital_raised_usd": lambda x: x < 1000000,
        "founders_control": lambda x: x > 80
    },
    exclusion_conditions={
        "investor_tier_primary": lambda x: x in ["tier_1", "tier_2"]
    },
    typical_success_rate=(0.60, 0.80),
    typical_funding_stages=["bootstrapped", "seed"],
    typical_team_size=(5, 50),
    typical_burn_multiple=(0.5, 1.0),
    typical_growth_rate=(30, 100),
    typical_gross_margin=(70, 90),
    example_companies=["Mailchimp", "Basecamp", "ConvertKit", "Plenty of Fish"],
    evolution_paths=["LIFESTYLE_BUSINESS", "LATE_STAGE_FUNDING"],
    compatible_patterns=["EFFICIENT_GROWTH", "NICHE_DOMINATION"],
    incompatible_patterns=["VC_HYPERGROWTH", "BLITZSCALE"],
    key_success_factors=[
        "Capital efficiency",
        "Customer focus",
        "Sustainable growth"
    ],
    common_failure_modes=[
        "Slow growth",
        "Limited resources",
        "Competitive pressure"
    ],
    strategic_recommendations=[
        "Focus on profits",
        "Grow organically",
        "Maintain control"
    ]
)

GRANT_RESEARCH_FUNDED = PatternDefinition(
    name="GRANT_RESEARCH_FUNDED",
    master_category=MasterCategory.FUNDING_PROFILE,
    description="Grant or research funding driven",
    required_conditions={
        "has_grant_funding": lambda x: x == 1,
        "domain_expertise_years_avg": lambda x: x > 10,
        "patent_count": lambda x: x > 0
    },
    optional_conditions={
        "university_affiliated": lambda x: x == 1,
        "regulatory_advantage_present": lambda x: x == 1
    },
    exclusion_conditions={
        "revenue_growth_rate_percent": lambda x: x > 200
    },
    typical_success_rate=(0.35, 0.60),
    typical_funding_stages=["grant", "seed", "series_a"],
    typical_team_size=(10, 100),
    typical_burn_multiple=(2.0, 10.0),
    typical_growth_rate=(0, 100),
    typical_gross_margin=(0, 80),
    example_companies=["Moderna", "Boston Dynamics", "Magic Leap", "Quantum startups"],
    evolution_paths=["VC_BACKED", "ACQUISITION"],
    compatible_patterns=["DEEP_TECH", "LONG_R&D"],
    incompatible_patterns=["QUICK_FLIP", "CONSUMER_VIRAL"],
    key_success_factors=[
        "Technical milestones",
        "Grant writing",
        "Research excellence"
    ],
    common_failure_modes=[
        "Commercialization gap",
        "Funding dependency",
        "Long timelines"
    ],
    strategic_recommendations=[
        "Bridge to commercial",
        "Diversify funding",
        "Build IP portfolio"
    ]
)

REVENUE_BASED_FUNDING = PatternDefinition(
    name="REVENUE_BASED_FUNDING",
    master_category=MasterCategory.FUNDING_PROFILE,
    description="Alternative funding tied to revenue",
    required_conditions={
        "annual_revenue_run_rate": lambda x: x > 1000000,
        "gross_margin_percent": lambda x: x > 50,
        "revenue_predictability": lambda x: x > 0.8
    },
    optional_conditions={
        "net_dollar_retention_percent": lambda x: x > 100,
        "has_recurring_revenue": lambda x: x == 1
    },
    exclusion_conditions={
        "pre_revenue": lambda x: x == 1
    },
    typical_success_rate=(0.50, 0.70),
    typical_funding_stages=["revenue_based", "series_a"],
    typical_team_size=(20, 200),
    typical_burn_multiple=(1.0, 2.5),
    typical_growth_rate=(50, 150),
    typical_gross_margin=(60, 80),
    example_companies=["Clearbanc portfolio", "Pipe customers", "Capchase users"],
    evolution_paths=["VC_FUNDING", "PROFITABLE_GROWTH"],
    compatible_patterns=["SUBSCRIPTION_RECURRING", "STEADY_GROWTH"],
    incompatible_patterns=["PRE_REVENUE", "HYPERGROWTH"],
    key_success_factors=[
        "Predictable revenue",
        "Strong unit economics",
        "Growth efficiency"
    ],
    common_failure_modes=[
        "Revenue volatility",
        "Growth constraints",
        "Debt burden"
    ],
    strategic_recommendations=[
        "Optimize CAC/LTV",
        "Build predictability",
        "Manage debt levels"
    ]
)

# ==========================================
# 8. MATURITY STAGE PATTERNS (4)
# ==========================================

IDEA_VALIDATION = PatternDefinition(
    name="IDEA_VALIDATION",
    master_category=MasterCategory.MATURITY_STAGE,
    description="Pre-product market fit, validating concept",
    required_conditions={
        "product_stage": lambda x: x in ["concept", "mvp"],
        "customer_count": lambda x: x < 100,
        "annual_revenue_run_rate": lambda x: x < 100000
    },
    optional_conditions={
        "founders_working_fulltime": lambda x: x >= 1,
        "has_mvp": lambda x: x == 1
    },
    exclusion_conditions={
        "series_a_raised": lambda x: x == 1
    },
    typical_success_rate=(0.20, 0.40),
    typical_funding_stages=["pre_seed", "seed"],
    typical_team_size=(1, 10),
    typical_burn_multiple=(5.0, 50.0),
    typical_growth_rate=(0, 1000),
    typical_gross_margin=(0, 80),
    example_companies=["Most early startups", "YC batch companies"],
    evolution_paths=["PRODUCT_MARKET_FIT", "PIVOT", "SHUTDOWN"],
    compatible_patterns=["LEAN_STARTUP", "CUSTOMER_DEVELOPMENT"],
    incompatible_patterns=["SCALING_GROWTH", "MARKET_LEADER"],
    key_success_factors=[
        "Customer discovery",
        "Rapid iteration",
        "Founder commitment"
    ],
    common_failure_modes=[
        "No market need",
        "Running out of cash",
        "Team issues"
    ],
    strategic_recommendations=[
        "Talk to customers",
        "Build MVP fast",
        "Find early adopters"
    ]
)

PRODUCT_MARKET_FIT = PatternDefinition(
    name="PRODUCT_MARKET_FIT",
    master_category=MasterCategory.MATURITY_STAGE,
    description="Found product-market fit, early traction",
    required_conditions={
        "product_retention_30d": lambda x: x > 0.4,
        "customer_count": lambda x: 100 <= x <= 10000,
        "revenue_growth_rate_percent": lambda x: x > 50
    },
    optional_conditions={
        "net_promoter_score": lambda x: x > 30,
        "organic_growth_percent": lambda x: x > 50
    },
    exclusion_conditions={},
    typical_success_rate=(0.40, 0.65),
    typical_funding_stages=["seed", "series_a"],
    typical_team_size=(10, 50),
    typical_burn_multiple=(2.0, 5.0),
    typical_growth_rate=(100, 300),
    typical_gross_margin=(40, 80),
    example_companies=["Airbnb 2009", "Uber 2011", "Slack 2014"],
    evolution_paths=["SCALING_GROWTH", "NICHE_LEADER"],
    compatible_patterns=["EFFICIENT_GROWTH", "PLG_BOTTOM_UP"],
    incompatible_patterns=["IDEA_VALIDATION", "STRUGGLING"],
    key_success_factors=[
        "Strong retention",
        "Word of mouth",
        "Clear value prop"
    ],
    common_failure_modes=[
        "Premature scaling",
        "Competition",
        "Execution issues"
    ],
    strategic_recommendations=[
        "Double down on what works",
        "Hire carefully",
        "Maintain product quality"
    ]
)

SCALING_GROWTH = PatternDefinition(
    name="SCALING_GROWTH",
    master_category=MasterCategory.MATURITY_STAGE,
    description="Scaling rapidly with established playbook",
    required_conditions={
        "revenue_growth_rate_percent": lambda x: x > 100,
        "team_size_full_time": lambda x: x > 50,
        "annual_revenue_run_rate": lambda x: x > 10000000
    },
    optional_conditions={
        "net_dollar_retention_percent": lambda x: x > 110,
        "ltv_cac_ratio": lambda x: x > 3
    },
    exclusion_conditions={},
    typical_success_rate=(0.50, 0.75),
    typical_funding_stages=["series_a", "series_b", "series_c"],
    typical_team_size=(50, 500),
    typical_burn_multiple=(1.5, 4.0),
    typical_growth_rate=(100, 200),
    typical_gross_margin=(50, 80),
    example_companies=["Stripe 2015", "Zoom 2017", "Canva 2018"],
    evolution_paths=["MARKET_LEADER", "IPO_TRACK"],
    compatible_patterns=["HYPERGROWTH", "GEOGRAPHIC_EXPANSION"],
    incompatible_patterns=["IDEA_VALIDATION", "STRUGGLING"],
    key_success_factors=[
        "Execution excellence",
        "Talent density",
        "Market timing"
    ],
    common_failure_modes=[
        "Culture dilution",
        "Operational chaos",
        "Competition"
    ],
    strategic_recommendations=[
        "Hire ahead of growth",
        "Build scalable systems",
        "Maintain culture"
    ]
)

MARKET_LEADER = PatternDefinition(
    name="MARKET_LEADER",
    master_category=MasterCategory.MATURITY_STAGE,
    description="Dominant position in market segment",
    required_conditions={
        "market_share": lambda x: x > 30,
        "annual_revenue_run_rate": lambda x: x > 100000000,
        "brand_strength_score": lambda x: x >= 4
    },
    optional_conditions={
        "net_dollar_retention_percent": lambda x: x > 120,
        "international_presence": lambda x: x == 1
    },
    exclusion_conditions={},
    typical_success_rate=(0.70, 0.90),
    typical_funding_stages=["series_c", "series_d", "pre_ipo"],
    typical_team_size=(500, 10000),
    typical_burn_multiple=(0.5, 2.0),
    typical_growth_rate=(30, 100),
    typical_gross_margin=(60, 85),
    example_companies=["Salesforce", "Shopify", "Datadog", "MongoDB"],
    evolution_paths=["IPO", "PLATFORM_ECOSYSTEM"],
    compatible_patterns=["CATEGORY_CREATOR", "ACQUISITION_MACHINE"],
    incompatible_patterns=["STARTUP_MODE", "PIVOT_NEEDED"],
    key_success_factors=[
        "Market dominance",
        "Innovation continuity",
        "Operational excellence"
    ],
    common_failure_modes=[
        "Disruption",
        "Complacency",
        "Regulatory issues"
    ],
    strategic_recommendations=[
        "Expand TAM",
        "Build ecosystem",
        "Acquire innovation"
    ]
)


# Pattern Collection
ALL_PATTERNS = [
    # Growth Dynamics
    VIRAL_CONSUMER_GROWTH,
    ENTERPRISE_LAND_EXPAND,
    PLG_BOTTOM_UP,
    SALES_LED_GROWTH,
    COMMUNITY_DRIVEN_GROWTH,
    PLATFORM_NETWORK_EFFECTS,
    GEOGRAPHIC_EXPANSION,
    
    # Business Model
    SUBSCRIPTION_RECURRING,
    TRANSACTIONAL_MARKETPLACE,
    FREEMIUM_CONVERSION,
    USAGE_BASED_PRICING,
    HARDWARE_AS_SERVICE,
    DATA_MONETIZATION,
    
    # Technology Depth
    AI_ML_CORE,
    BLOCKCHAIN_WEB3,
    BIOTECH_LIFESCIENCES,
    HARDWARE_ROBOTICS,
    QUANTUM_COMPUTING,
    PLATFORM_INFRASTRUCTURE,
    
    # Market Approach
    B2B_ENTERPRISE,
    B2B_SMB_FOCUSED,
    B2C_MASS_MARKET,
    B2B2C_EMBEDDED,
    B2G_GOVERNMENT,
    
    # Industry Vertical
    FINTECH_PAYMENTS,
    HEALTHTECH_DIGITAL,
    EDTECH_LEARNING,
    PROPTECH_REAL_ESTATE,
    AGTECH_FOOD,
    CLIMATE_SUSTAINABILITY,
    RETAIL_COMMERCE,
    MOBILITY_TRANSPORT,
    
    # Operational Model
    ASSET_LIGHT_DIGITAL,
    ASSET_HEAVY_OPERATIONS,
    HYBRID_DIGITAL_PHYSICAL,
    PURE_SOFTWARE,
    SERVICE_ENABLED_TECH,
    
    # Funding Profile
    VC_HYPERGROWTH,
    BOOTSTRAP_PROFITABLE,
    GRANT_RESEARCH_FUNDED,
    REVENUE_BASED_FUNDING,
    
    # Maturity Stage
    IDEA_VALIDATION,
    PRODUCT_MARKET_FIT,
    SCALING_GROWTH,
    MARKET_LEADER
]

# Create pattern lookup dictionary
PATTERN_LOOKUP = {pattern.name: pattern for pattern in ALL_PATTERNS}

# Pattern compatibility matrix
PATTERN_COMPATIBILITY_MATRIX = {
    pattern.name: {
        'compatible': pattern.compatible_patterns,
        'incompatible': pattern.incompatible_patterns
    }
    for pattern in ALL_PATTERNS
}

# Pattern evolution graph
PATTERN_EVOLUTION_GRAPH = {
    pattern.name: pattern.evolution_paths
    for pattern in ALL_PATTERNS
}