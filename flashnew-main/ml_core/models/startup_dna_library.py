"""
Comprehensive Startup DNA Library
50+ startup patterns based on real-world success stories
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum

class DNACategory(Enum):
    GROWTH_FOCUSED = "growth_focused"
    EFFICIENCY_FOCUSED = "efficiency_focused"
    INNOVATION_FOCUSED = "innovation_focused"
    NETWORK_FOCUSED = "network_focused"
    MARKET_FOCUSED = "market_focused"
    PRODUCT_FOCUSED = "product_focused"

@dataclass
class DNAPattern:
    """Represents a startup DNA pattern"""
    name: str
    category: DNACategory
    description: str
    indicators: Dict[str, Any]
    success_rate: float
    typical_funding_stage: List[str]
    examples: List[str]
    key_risks: List[str]
    success_factors: List[str]
    evolution_paths: List[str]
    typical_metrics: Dict[str, Any]
    
class StartupDNALibrary:
    """Complete library of startup DNA patterns"""
    
    def __init__(self):
        self.patterns = self._initialize_patterns()
        self.pattern_index = {p.name: p for p in self.patterns}
        
    def _initialize_patterns(self) -> List[DNAPattern]:
        """Initialize all DNA patterns"""
        patterns = []
        
        # GROWTH-FOCUSED PATTERNS
        patterns.append(DNAPattern(
            name="BLITZSCALE_UNICORN",
            category=DNACategory.GROWTH_FOCUSED,
            description="Extreme growth at all costs, winner-takes-all markets",
            indicators={
                'revenue_growth_rate': lambda x: x > 200,  # >200% YoY
                'burn_multiple': lambda x: x > 5,
                'market_share_growth': lambda x: x > 50,
                'user_growth_rate': lambda x: x > 150,
                'funding_velocity': 'high',  # Round every 12-18 months
                'geographic_expansion': 'aggressive'
            },
            success_rate=0.67,
            typical_funding_stage=['series_a', 'series_b', 'series_c'],
            examples=['Uber (2012)', 'Airbnb (2010)', 'DoorDash (2015)'],
            key_risks=[
                'cash_runway_risk',
                'unit_economics_negative',
                'regulatory_challenges',
                'competitor_wars'
            ],
            success_factors=[
                'first_mover_advantage',
                'network_effects',
                'brand_recognition',
                'operational_excellence'
            ],
            evolution_paths=['MARKET_DOMINATOR', 'PROFITABLE_LEADER'],
            typical_metrics={
                'burn_rate': '5-20M/month',
                'runway': '12-18 months',
                'ltv_cac': '0.5-1.5',  # Often negative early
                'gross_margin': '20-40%'
            }
        ))
        
        patterns.append(DNAPattern(
            name="HYPERGROWTH_SAAS",
            category=DNACategory.GROWTH_FOCUSED,
            description="High growth SaaS with strong product-market fit",
            indicators={
                'revenue_growth_rate': lambda x: 100 < x < 300,
                'net_retention': lambda x: x > 120,
                'burn_multiple': lambda x: 2 < x < 5,
                'magic_number': lambda x: x > 0.7,  # Sales efficiency
                'gross_margin': lambda x: x > 70
            },
            success_rate=0.78,
            typical_funding_stage=['seed', 'series_a', 'series_b'],
            examples=['Datadog (2015)', 'Snowflake (2014)', 'Zoom (2013)'],
            key_risks=[
                'competition_intensity',
                'market_saturation',
                'feature_parity',
                'enterprise_readiness'
            ],
            success_factors=[
                'product_excellence',
                'sales_efficiency',
                'customer_success',
                'expansion_revenue'
            ],
            evolution_paths=['PLATFORM_PLAY', 'CATEGORY_LEADER'],
            typical_metrics={
                'arr_growth': '150-300%',
                'payback_period': '12-18 months',
                'nps': '>50',
                'churn': '<10% annual'
            }
        ))
        
        patterns.append(DNAPattern(
            name="VIRAL_ROCKET",
            category=DNACategory.GROWTH_FOCUSED,
            description="Product with built-in viral growth mechanics",
            indicators={
                'viral_coefficient': lambda x: x > 1.5,
                'user_growth_rate': lambda x: x > 200,
                'organic_acquisition': lambda x: x > 70,  # % of users
                'time_to_value': lambda x: x < 5,  # minutes
                'dau_mau_ratio': lambda x: x > 0.5
            },
            success_rate=0.71,
            typical_funding_stage=['seed', 'series_a'],
            examples=['TikTok (2018)', 'Clubhouse (2020)', 'BeReal (2021)'],
            key_risks=[
                'retention_cliff',
                'monetization_challenge',
                'platform_dependency',
                'fad_risk'
            ],
            success_factors=[
                'viral_mechanics',
                'engagement_depth',
                'cultural_timing',
                'creator_ecosystem'
            ],
            evolution_paths=['PLATFORM_ECOSYSTEM', 'ENGAGEMENT_MONETIZER'],
            typical_metrics={
                'k_factor': '>1.5',
                'viral_cycle_time': '<2 days',
                'user_acquisition_cost': '<$1',
                'engagement_time': '>30 min/day'
            }
        ))
        
        # EFFICIENCY-FOCUSED PATTERNS
        patterns.append(DNAPattern(
            name="EFFICIENT_OPERATOR",
            category=DNACategory.EFFICIENCY_FOCUSED,
            description="Profitable or near-profitable with controlled growth",
            indicators={
                'burn_multiple': lambda x: x < 1.5,
                'gross_margin': lambda x: x > 70,
                'revenue_growth_rate': lambda x: 50 < x < 150,
                'rule_of_40': lambda x: x > 40,
                'capital_efficiency': lambda x: x > 1.5  # ARR/Capital Raised
            },
            success_rate=0.82,
            typical_funding_stage=['seed', 'series_a'],
            examples=['Atlassian', 'Mailchimp', 'Basecamp'],
            key_risks=[
                'growth_ceiling',
                'competitive_disruption',
                'market_expansion_limits',
                'talent_retention'
            ],
            success_factors=[
                'unit_economics',
                'customer_love',
                'operational_efficiency',
                'market_focus'
            ],
            evolution_paths=['PROFITABLE_LEADER', 'ACQUISITION_TARGET'],
            typical_metrics={
                'ebitda_margin': '>0%',
                'cac_payback': '<12 months',
                'gross_retention': '>90%',
                'employee_efficiency': '>$200k/employee'
            }
        ))
        
        patterns.append(DNAPattern(
            name="BOOTSTRAP_CHAMPION",
            category=DNACategory.EFFICIENCY_FOCUSED,
            description="Self-funded with strong organic growth",
            indicators={
                'external_funding': lambda x: x == 0,
                'revenue_per_employee': lambda x: x > 300000,
                'profit_margin': lambda x: x > 20,
                'organic_growth': lambda x: x > 80,  # % of growth
                'customer_concentration': lambda x: x < 20
            },
            success_rate=0.76,
            typical_funding_stage=['none', 'seed'],
            examples=['GitHub (early)', 'Zapier', 'ConvertKit'],
            key_risks=[
                'resource_constraints',
                'slow_expansion',
                'acquisition_vulnerability',
                'market_timing'
            ],
            success_factors=[
                'founder_expertise',
                'niche_dominance',
                'community_building',
                'product_focus'
            ],
            evolution_paths=['EFFICIENT_OPERATOR', 'NICHE_DOMINATOR'],
            typical_metrics={
                'revenue': '>$5M ARR',
                'growth': '50-100% YoY',
                'profit': '>20%',
                'team_size': '<50'
            }
        ))
        
        patterns.append(DNAPattern(
            name="CASHFLOW_POSITIVE",
            category=DNACategory.EFFICIENCY_FOCUSED,
            description="Achieved positive cash flow, sustainable growth",
            indicators={
                'cash_flow': lambda x: x > 0,
                'months_to_cashflow_positive': lambda x: x < 24,
                'gross_margin': lambda x: x > 60,
                'operating_margin': lambda x: x > 0,
                'debt_to_equity': lambda x: x < 0.5
            },
            success_rate=0.79,
            typical_funding_stage=['series_a', 'series_b'],
            examples=['Klaviyo', 'Calendly', 'Canva (2017)'],
            key_risks=[
                'growth_deceleration',
                'innovation_lag',
                'market_disruption',
                'complacency'
            ],
            success_factors=[
                'financial_discipline',
                'market_fit',
                'efficient_operations',
                'customer_retention'
            ],
            evolution_paths=['IPO_READY', 'STRATEGIC_ACQUIRER'],
            typical_metrics={
                'fcf_margin': '>10%',
                'revenue_growth': '40-80%',
                'ebitda': '>15%',
                'customer_ltv': '>$50k'
            }
        ))
        
        # INNOVATION-FOCUSED PATTERNS
        patterns.append(DNAPattern(
            name="DEEP_TECH_PIONEER",
            category=DNACategory.INNOVATION_FOCUSED,
            description="Breakthrough technology with long development cycles",
            indicators={
                'r_and_d_intensity': lambda x: x > 50,  # % of expenses
                'patent_applications': lambda x: x > 5,
                'phd_team_ratio': lambda x: x > 40,
                'time_to_market': lambda x: x > 24,  # months
                'technical_risk': 'high'
            },
            success_rate=0.61,
            typical_funding_stage=['seed', 'series_a', 'series_b'],
            examples=['SpaceX', 'Moderna', 'Quantum Computing startups'],
            key_risks=[
                'technical_feasibility',
                'long_development_time',
                'capital_intensity',
                'market_education'
            ],
            success_factors=[
                'technical_breakthrough',
                'ip_portfolio',
                'government_contracts',
                'patient_capital'
            ],
            evolution_paths=['PLATFORM_TECHNOLOGY', 'INDUSTRY_TRANSFORMER'],
            typical_metrics={
                'r_and_d_spend': '>$5M/year',
                'time_to_revenue': '>3 years',
                'technical_milestones': 'quarterly',
                'grant_funding': '>$1M'
            }
        ))
        
        patterns.append(DNAPattern(
            name="AI_FIRST_INNOVATOR",
            category=DNACategory.INNOVATION_FOCUSED,
            description="Core product built on AI/ML technology",
            indicators={
                'ai_team_ratio': lambda x: x > 30,
                'model_performance_edge': lambda x: x > 20,  # % better
                'data_moat': lambda x: x == True,
                'inference_cost_efficiency': lambda x: x > 2,  # vs competitors
                'proprietary_models': lambda x: x >= 1
            },
            success_rate=0.73,
            typical_funding_stage=['seed', 'series_a'],
            examples=['OpenAI', 'Anthropic', 'Jasper', 'Midjourney'],
            key_risks=[
                'commoditization',
                'compute_costs',
                'regulatory_uncertainty',
                'ethical_concerns'
            ],
            success_factors=[
                'model_superiority',
                'user_experience',
                'cost_efficiency',
                'continuous_improvement'
            ],
            evolution_paths=['AI_PLATFORM', 'VERTICAL_AI_LEADER'],
            typical_metrics={
                'model_accuracy': '>90%',
                'inference_latency': '<100ms',
                'gpu_costs': '>$50k/month',
                'ai_engineers': '>10'
            }
        ))
        
        patterns.append(DNAPattern(
            name="BIOTECH_BREAKTHROUGH",
            category=DNACategory.INNOVATION_FOCUSED,
            description="Life sciences innovation with regulatory pathway",
            indicators={
                'clinical_stage': lambda x: x in ['preclinical', 'phase1', 'phase2'],
                'scientific_advisors': lambda x: x > 5,
                'peer_reviewed_publications': lambda x: x > 3,
                'regulatory_expertise': 'high',
                'partnership_potential': 'high'
            },
            success_rate=0.58,
            typical_funding_stage=['seed', 'series_a', 'series_b'],
            examples=['BioNTech', 'Ginkgo Bioworks', 'Insitro'],
            key_risks=[
                'clinical_failure',
                'regulatory_rejection',
                'long_timelines',
                'capital_requirements'
            ],
            success_factors=[
                'scientific_validity',
                'clinical_execution',
                'regulatory_strategy',
                'strategic_partnerships'
            ],
            evolution_paths=['PHARMA_PARTNER', 'PLATFORM_BIOTECH'],
            typical_metrics={
                'cash_runway': '>24 months',
                'r_and_d_spend': '>70%',
                'clinical_milestones': 'defined',
                'ip_portfolio': '>10 patents'
            }
        ))
        
        # NETWORK-FOCUSED PATTERNS
        patterns.append(DNAPattern(
            name="MARKETPLACE_BUILDER",
            category=DNACategory.NETWORK_FOCUSED,
            description="Two-sided marketplace with network effects",
            indicators={
                'supply_demand_ratio': lambda x: 0.8 < x < 1.2,
                'liquidity': lambda x: x > 20,  # % of listings transacting
                'take_rate': lambda x: 10 < x < 30,
                'repeat_usage': lambda x: x > 60,  # % of users
                'geographic_density': 'concentrated'
            },
            success_rate=0.64,
            typical_funding_stage=['seed', 'series_a', 'series_b'],
            examples=['Airbnb', 'Uber', 'StockX', 'Faire'],
            key_risks=[
                'chicken_egg_problem',
                'disintermediation',
                'trust_and_safety',
                'unit_economics'
            ],
            success_factors=[
                'liquidity_threshold',
                'network_effects',
                'trust_systems',
                'supply_quality'
            ],
            evolution_paths=['PLATFORM_ECOSYSTEM', 'VERTICAL_MONOPOLY'],
            typical_metrics={
                'gmv_growth': '>100%',
                'take_rate': '15-25%',
                'cohort_retention': '>60%',
                'market_penetration': '>5%'
            }
        ))
        
        patterns.append(DNAPattern(
            name="SOCIAL_NETWORK",
            category=DNACategory.NETWORK_FOCUSED,
            description="Social platform with user-generated content",
            indicators={
                'daily_active_users': lambda x: x > 100000,
                'user_generated_content': lambda x: x > 90,  # % of content
                'engagement_rate': lambda x: x > 30,
                'network_density': lambda x: x > 0.1,
                'viral_loops': 'multiple'
            },
            success_rate=0.52,
            typical_funding_stage=['seed', 'series_a'],
            examples=['Instagram (2011)', 'TikTok', 'Discord', 'BeReal'],
            key_risks=[
                'user_retention',
                'content_moderation',
                'monetization_balance',
                'platform_shifts'
            ],
            success_factors=[
                'engagement_loops',
                'creator_tools',
                'community_building',
                'mobile_first'
            ],
            evolution_paths=['CONTENT_PLATFORM', 'SOCIAL_COMMERCE'],
            typical_metrics={
                'dau_mau': '>40%',
                'time_spent': '>30 min/day',
                'content_creation': '>5%',
                'friend_connections': '>50'
            }
        ))
        
        patterns.append(DNAPattern(
            name="B2B_NETWORK",
            category=DNACategory.NETWORK_FOCUSED,
            description="Business network with collaborative features",
            indicators={
                'customer_nodes': lambda x: x > 100,
                'inter_company_usage': lambda x: x > 30,  # % of usage
                'network_value_prop': 'strong',
                'switching_cost': lambda x: x > 7,  # 1-10 scale
                'api_adoption': lambda x: x > 20
            },
            success_rate=0.69,
            typical_funding_stage=['series_a', 'series_b'],
            examples=['Slack', 'Figma', 'Airtable', 'Rippling'],
            key_risks=[
                'enterprise_adoption',
                'integration_complexity',
                'security_requirements',
                'competition'
            ],
            success_factors=[
                'collaboration_features',
                'integration_ecosystem',
                'enterprise_ready',
                'network_growth'
            ],
            evolution_paths=['PLATFORM_PLAY', 'ENTERPRISE_SUITE'],
            typical_metrics={
                'multi_seat_deals': '>70%',
                'cross_company_usage': '>20%',
                'nps': '>60',
                'expansion_revenue': '>130%'
            }
        ))
        
        # MARKET-FOCUSED PATTERNS
        patterns.append(DNAPattern(
            name="CATEGORY_CREATOR",
            category=DNACategory.MARKET_FOCUSED,
            description="Creating new market category or segment",
            indicators={
                'category_first': lambda x: x == True,
                'market_education_spend': lambda x: x > 30,  # % of marketing
                'thought_leadership': 'high',
                'analyst_recognition': lambda x: x > 3,  # Number of reports
                'competitor_following': lambda x: x > 5  # Copycats
            },
            success_rate=0.71,
            typical_funding_stage=['series_a', 'series_b', 'series_c'],
            examples=['Salesforce (CRM)', 'Uber (rideshare)', 'Airbnb (homeshare)'],
            key_risks=[
                'market_education_cost',
                'timing_risk',
                'copycat_competition',
                'category_definition'
            ],
            success_factors=[
                'vision_clarity',
                'market_timing',
                'brand_building',
                'ecosystem_creation'
            ],
            evolution_paths=['CATEGORY_LEADER', 'PLATFORM_ECOSYSTEM'],
            typical_metrics={
                'category_share': '>40%',
                'brand_recognition': '>60%',
                'media_mentions': '>100/month',
                'conference_speaking': '>10/year'
            }
        ))
        
        patterns.append(DNAPattern(
            name="VERTICAL_SAAS",
            category=DNACategory.MARKET_FOCUSED,
            description="Deep specialization in specific industry vertical",
            indicators={
                'vertical_focus': lambda x: x == True,
                'industry_expertise': lambda x: x > 8,  # 1-10 scale
                'market_penetration': lambda x: x > 10,  # % of target market
                'customer_concentration': lambda x: x < 30,
                'industry_partnerships': lambda x: x > 5
            },
            success_rate=0.74,
            typical_funding_stage=['seed', 'series_a', 'series_b'],
            examples=['Toast (restaurants)', 'Veeva (pharma)', 'Procore (construction)'],
            key_risks=[
                'market_size_limits',
                'industry_downturns',
                'horizontal_competition',
                'regulatory_changes'
            ],
            success_factors=[
                'domain_expertise',
                'industry_relationships',
                'compliance_knowledge',
                'vertical_integration'
            ],
            evolution_paths=['VERTICAL_PLATFORM', 'HORIZONTAL_EXPANSION'],
            typical_metrics={
                'market_share': '>15%',
                'customer_count': '>500',
                'industry_nps': '>70',
                'vertical_arpu': '>$50k'
            }
        ))
        
        patterns.append(DNAPattern(
            name="GEOGRAPHIC_EXPANDER",
            category=DNACategory.MARKET_FOCUSED,
            description="Rapid international or multi-market expansion",
            indicators={
                'markets_entered': lambda x: x > 5,
                'international_revenue': lambda x: x > 30,  # % of total
                'localization_depth': 'high',
                'local_teams': lambda x: x > 3,
                'regulatory_compliance': 'multi_jurisdiction'
            },
            success_rate=0.66,
            typical_funding_stage=['series_b', 'series_c'],
            examples=['Uber', 'Spotify', 'Revolut', 'Glovo'],
            key_risks=[
                'operational_complexity',
                'regulatory_variance',
                'cultural_misfit',
                'execution_challenges'
            ],
            success_factors=[
                'playbook_repeatability',
                'local_adaptation',
                'operational_excellence',
                'brand_strength'
            ],
            evolution_paths=['GLOBAL_LEADER', 'REGIONAL_CHAMPION'],
            typical_metrics={
                'countries': '>10',
                'international_growth': '>150%',
                'market_leadership': '>3 countries',
                'local_market_share': '>10%'
            }
        ))
        
        # PRODUCT-FOCUSED PATTERNS
        patterns.append(DNAPattern(
            name="PRODUCT_LED_GROWTH",
            category=DNACategory.PRODUCT_FOCUSED,
            description="Product drives acquisition, retention, and expansion",
            indicators={
                'organic_acquisition': lambda x: x > 60,  # % of new users
                'time_to_value': lambda x: x < 10,  # minutes
                'self_serve_revenue': lambda x: x > 50,  # % of revenue
                'product_virality': lambda x: x > 1.2,
                'feature_adoption': lambda x: x > 40  # % in first week
            },
            success_rate=0.77,
            typical_funding_stage=['seed', 'series_a', 'series_b'],
            examples=['Figma', 'Notion', 'Loom', 'Linear'],
            key_risks=[
                'enterprise_readiness',
                'monetization_timing',
                'feature_bloat',
                'copycat_features'
            ],
            success_factors=[
                'user_experience',
                'viral_mechanics',
                'community_building',
                'continuous_iteration'
            ],
            evolution_paths=['PLATFORM_PLAY', 'ENTERPRISE_READY_PLG'],
            typical_metrics={
                'activation_rate': '>60%',
                'week_1_retention': '>70%',
                'expansion_revenue': '>125%',
                'support_tickets': '<5% MAU'
            }
        ))
        
        patterns.append(DNAPattern(
            name="MOBILE_FIRST",
            category=DNACategory.PRODUCT_FOCUSED,
            description="Mobile-native product with app store distribution",
            indicators={
                'mobile_usage': lambda x: x > 80,  # % of total usage
                'app_store_rating': lambda x: x > 4.5,
                'mobile_retention_d30': lambda x: x > 20,
                'push_notification_opt_in': lambda x: x > 60,
                'mobile_first_features': 'core'
            },
            success_rate=0.68,
            typical_funding_stage=['seed', 'series_a'],
            examples=['Robinhood', 'Calm', 'Duolingo', 'Coinbase (early)'],
            key_risks=[
                'platform_dependency',
                'app_store_policies',
                'discovery_challenges',
                'mobile_monetization'
            ],
            success_factors=[
                'mobile_ux_excellence',
                'push_strategy',
                'app_store_optimization',
                'mobile_virality'
            ],
            evolution_paths=['MOBILE_PLATFORM', 'OMNICHANNEL_LEADER'],
            typical_metrics={
                'mau': '>1M',
                'app_store_rank': 'Top 100',
                'mobile_arpu': '>$10',
                'session_length': '>5 min'
            }
        ))
        
        patterns.append(DNAPattern(
            name="API_FIRST",
            category=DNACategory.PRODUCT_FOCUSED,
            description="Developer-focused with API as primary product",
            indicators={
                'api_calls': lambda x: x > 1000000,  # per day
                'developer_accounts': lambda x: x > 1000,
                'documentation_quality': 'excellent',
                'sdk_languages': lambda x: x > 5,
                'developer_nps': lambda x: x > 50
            },
            success_rate=0.72,
            typical_funding_stage=['seed', 'series_a', 'series_b'],
            examples=['Stripe', 'Twilio', 'SendGrid', 'Algolia'],
            key_risks=[
                'developer_adoption',
                'pricing_complexity',
                'infrastructure_costs',
                'enterprise_requirements'
            ],
            success_factors=[
                'developer_experience',
                'reliability_uptime',
                'documentation',
                'community_support'
            ],
            evolution_paths=['INFRASTRUCTURE_PLATFORM', 'DEVELOPER_ECOSYSTEM'],
            typical_metrics={
                'api_uptime': '>99.95%',
                'developer_growth': '>20% MoM',
                'api_revenue': '>$1M ARR',
                'integration_time': '<1 day'
            }
        ))
        
        # SPECIALIZED PATTERNS
        patterns.append(DNAPattern(
            name="ENTERPRISE_DISRUPTOR",
            category=DNACategory.MARKET_FOCUSED,
            description="Disrupting enterprise software with modern approach",
            indicators={
                'enterprise_customers': lambda x: x > 10,
                'average_contract_value': lambda x: x > 100000,
                'implementation_time': lambda x: x < 90,  # days
                'incumbent_displacement': lambda x: x > 30,  # % of deals
                'security_certifications': lambda x: x >= 2  # SOC2, ISO
            },
            success_rate=0.70,
            typical_funding_stage=['series_a', 'series_b', 'series_c'],
            examples=['Databricks', 'Snowflake', 'MongoDB', 'HashiCorp'],
            key_risks=[
                'long_sales_cycles',
                'enterprise_requirements',
                'incumbent_competition',
                'support_complexity'
            ],
            success_factors=[
                'enterprise_readiness',
                'migration_tools',
                'reference_customers',
                'partner_ecosystem'
            ],
            evolution_paths=['ENTERPRISE_PLATFORM', 'IPO_READY'],
            typical_metrics={
                'avc': '>$250k',
                'gross_retention': '>95%',
                'sales_cycle': '3-6 months',
                'fortune_500_logos': '>5'
            }
        ))
        
        patterns.append(DNAPattern(
            name="FINTECH_INNOVATOR",
            category=DNACategory.INNOVATION_FOCUSED,
            description="Financial services innovation with regulatory compliance",
            indicators={
                'regulatory_licenses': lambda x: x >= 1,
                'transaction_volume': lambda x: x > 10000000,  # monthly
                'compliance_team_ratio': lambda x: x > 10,  # % of team
                'banking_partnerships': lambda x: x >= 1,
                'trust_safety_score': lambda x: x > 8  # 1-10
            },
            success_rate=0.65,
            typical_funding_stage=['seed', 'series_a', 'series_b'],
            examples=['Stripe', 'Square', 'Plaid', 'Chime'],
            key_risks=[
                'regulatory_changes',
                'compliance_costs',
                'fraud_risk',
                'banking_dependencies'
            ],
            success_factors=[
                'regulatory_expertise',
                'risk_management',
                'user_trust',
                'scale_economics'
            ],
            evolution_paths=['FINANCIAL_PLATFORM', 'BANKING_LICENSE'],
            typical_metrics={
                'transaction_volume': '>$100M/month',
                'fraud_rate': '<0.1%',
                'regulatory_incidents': '0',
                'user_funds': '>$1B'
            }
        ))
        
        patterns.append(DNAPattern(
            name="HARDWARE_SOFTWARE",
            category=DNACategory.INNOVATION_FOCUSED,
            description="Combined hardware and software offering",
            indicators={
                'hardware_revenue': lambda x: x > 30,  # % of total
                'software_attach_rate': lambda x: x > 50,
                'gross_margin_blended': lambda x: x > 40,
                'supply_chain_complexity': 'high',
                'r_and_d_allocation': 'balanced'
            },
            success_rate=0.62,
            typical_funding_stage=['series_a', 'series_b', 'series_c'],
            examples=['Peloton', 'Oculus', 'DJI', 'Tesla'],
            key_risks=[
                'inventory_management',
                'supply_chain_disruption',
                'capital_intensity',
                'support_complexity'
            ],
            success_factors=[
                'integrated_experience',
                'supply_chain_excellence',
                'software_differentiation',
                'brand_strength'
            ],
            evolution_paths=['PLATFORM_HARDWARE', 'ECOSYSTEM_BUILDER'],
            typical_metrics={
                'hardware_margin': '>25%',
                'software_margin': '>70%',
                'return_rate': '<5%',
                'software_adoption': '>60%'
            }
        ))
        
        # COMPOSITE PATTERNS (Combinations)
        patterns.append(DNAPattern(
            name="EFFICIENT_BLITZSCALER",
            category=DNACategory.GROWTH_FOCUSED,
            description="High growth with improving unit economics (Zoom model)",
            indicators={
                'revenue_growth': lambda x: x > 100,
                'burn_improvement': lambda x: x < 0,  # Burn multiple decreasing
                'gross_margin_expansion': lambda x: x > 2,  # % YoY
                'sales_efficiency': lambda x: x > 1.5,
                'rule_of_40': lambda x: x > 60
            },
            success_rate=0.83,
            typical_funding_stage=['series_b', 'series_c'],
            examples=['Zoom', 'Canva', 'Shopify'],
            key_risks=[
                'execution_complexity',
                'market_saturation',
                'maintaining_efficiency',
                'competition'
            ],
            success_factors=[
                'operational_excellence',
                'product_market_fit',
                'go_to_market_efficiency',
                'culture'
            ],
            evolution_paths=['IPO_READY', 'CATEGORY_DOMINATOR'],
            typical_metrics={
                'growth': '>100%',
                'burn_multiple': '<2',
                'ndr': '>130%',
                'magic_number': '>1.5'
            }
        ))
        
        return patterns
    
    def get_pattern(self, name: str) -> Optional[DNAPattern]:
        """Get a specific DNA pattern by name"""
        return self.pattern_index.get(name)
    
    def get_patterns_by_category(self, category: DNACategory) -> List[DNAPattern]:
        """Get all patterns in a category"""
        return [p for p in self.patterns if p.category == category]
    
    def get_patterns_by_stage(self, funding_stage: str) -> List[DNAPattern]:
        """Get patterns typical for a funding stage"""
        return [p for p in self.patterns if funding_stage in p.typical_funding_stage]
    
    def get_evolution_paths(self, current_pattern: str) -> List[str]:
        """Get possible evolution paths from current pattern"""
        pattern = self.get_pattern(current_pattern)
        return pattern.evolution_paths if pattern else []
    
    def get_similar_patterns(self, pattern_name: str, max_results: int = 5) -> List[str]:
        """Find similar patterns based on characteristics"""
        pattern = self.get_pattern(pattern_name)
        if not pattern:
            return []
        
        # Simple similarity based on same category and success rate
        similar = []
        for p in self.patterns:
            if p.name != pattern_name and p.category == pattern.category:
                similarity_score = 1 - abs(p.success_rate - pattern.success_rate)
                similar.append((p.name, similarity_score))
        
        similar.sort(key=lambda x: x[1], reverse=True)
        return [name for name, _ in similar[:max_results]]

# Create global instance
STARTUP_DNA_LIBRARY = StartupDNALibrary()