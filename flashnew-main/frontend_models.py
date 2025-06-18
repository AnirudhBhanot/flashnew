"""
Frontend data models that match what the UI sends
"""

from pydantic import BaseModel, Field
from typing import Optional, Any, Dict


class FrontendStartupData(BaseModel):
    """Input model that matches frontend data format exactly"""
    
    # Company Information
    startup_name: Optional[str] = None
    founding_year: Optional[int] = None
    hq_location: Optional[str] = None
    vertical: Optional[str] = None
    
    # Funding Information  
    funding_stage: Optional[str] = None
    total_funding: Optional[float] = None
    total_capital_raised_usd: Optional[float] = None
    num_funding_rounds: Optional[int] = None
    cash_on_hand_usd: Optional[float] = None
    burn_rate: Optional[float] = None
    monthly_burn_usd: Optional[float] = None
    runway: Optional[float] = None
    runway_months: Optional[float] = None
    burn_multiple: Optional[float] = None
    
    # Revenue Metrics
    annual_revenue_run_rate: Optional[float] = None
    revenue_growth_rate_yoy: Optional[float] = None
    gross_margin: Optional[float] = None
    
    # Business Metrics
    r_and_d_spend_percentage: Optional[float] = None
    r_and_d_intensity: Optional[float] = None
    sales_marketing_efficiency: Optional[float] = None
    customer_acquisition_cost: Optional[float] = None
    lifetime_value: Optional[float] = None
    months_to_profitability: Optional[float] = None
    
    # Team Information
    team_size: Optional[int] = None
    team_size_full_time: Optional[int] = None
    engineering_ratio: Optional[float] = None
    founder_experience_years: Optional[float] = None
    repeat_founder: Optional[bool] = None
    team_completeness_score: Optional[float] = None
    advisory_board_strength: Optional[float] = None
    
    # Market & Competition
    market_size_billions: Optional[float] = None
    market_growth_rate: Optional[float] = None
    market_competition_level: Optional[str] = None
    tam_size: Optional[float] = None
    tam_size_usd: Optional[float] = None
    sam_size_usd: Optional[float] = None
    sam_percentage: Optional[float] = None
    som_size_usd: Optional[float] = None
    market_share: Optional[float] = None
    
    # Product & Technology
    product_market_fit_score: Optional[float] = None
    innovation_index: Optional[float] = None
    scalability_score: Optional[float] = None  # Frontend sends 1-5
    technology_score: Optional[float] = None  # Frontend sends 0-100
    tech_stack_modernity: Optional[float] = None
    technical_debt_ratio: Optional[float] = None
    
    # Customer Metrics
    customer_concentration: Optional[float] = None
    customer_concentration_percent: Optional[float] = None
    viral_coefficient: Optional[float] = None
    weekly_active_users_growth: Optional[float] = None
    feature_adoption_rate: Optional[float] = None
    
    # Competitive Advantage
    competitive_moat_score: Optional[float] = None
    ip_portfolio_strength: Optional[float] = None
    has_patents: Optional[bool] = None
    patent_count: Optional[int] = None
    regulatory_advantage_present: Optional[bool] = None
    network_effects_present: Optional[bool] = None
    has_data_moat: Optional[bool] = None
    
    # Investor Information
    investor_tier_primary: Optional[str] = None
    investor_count: Optional[int] = None
    investor_experience_score: Optional[float] = None
    investor_concentration: Optional[float] = None  # Frontend sends percentage
    board_diversity_score: Optional[float] = None
    
    # Financial Health
    has_debt: Optional[bool] = None
    debt_to_equity: Optional[float] = None
    
    # Growth & Operations
    company_age_months: Optional[int] = None
    pivot_count: Optional[int] = None
    partnership_score: Optional[float] = None
    international_presence: Optional[bool] = None
    
    # Risk Factors
    regulatory_risk_score: Optional[float] = None
    technology_risk_score: Optional[float] = None
    platform_risk_score: Optional[float] = None
    cybersecurity_score: Optional[float] = None
    data_privacy_compliance: Optional[float] = None
    key_person_dependency: Optional[bool] = None
    
    # ESG
    esg_score: Optional[float] = None
    
    # Additional fields that might come from frontend
    switching_cost_score: Optional[float] = None
    brand_strength_score: Optional[float] = None
    sector: Optional[str] = None
    market_growth_rate_percent: Optional[float] = None
    customer_count: Optional[int] = None
    user_growth_rate_percent: Optional[float] = None
    net_dollar_retention_percent: Optional[float] = None
    competition_intensity: Optional[Any] = None  # Can be string or number from frontend
    competitors_named_count: Optional[int] = None
    founders_count: Optional[int] = None
    years_experience_avg: Optional[float] = None
    domain_expertise_years_avg: Optional[float] = None
    prior_startup_experience_count: Optional[int] = None
    prior_successful_exits_count: Optional[int] = None
    board_advisor_experience_score: Optional[float] = None
    c_suite_completeness_percent: Optional[float] = None
    revenue_per_employee: Optional[float] = None
    product_stage: Optional[str] = None
    mvp_months_to_market: Optional[float] = None
    feature_completeness_percent: Optional[float] = None
    technical_complexity_score: Optional[float] = None
    api_integration_count: Optional[int] = None
    platform_dependency_score: Optional[float] = None
    code_quality_score: Optional[float] = None
    
    class Config:
        """Allow any extra fields from frontend"""
        extra = 'allow'
        validate_assignment = False  # Don't validate on assignment