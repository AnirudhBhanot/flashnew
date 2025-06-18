#!/usr/bin/env python3
"""Debug the Michelin API error"""

import sys
sys.path.append('.')

from api_michelin_llm_analysis import StartupData, MichelinAnalysisEngine

# Create test data
test_data = StartupData(
    startup_name="TestStartup",
    sector="technology",
    funding_stage="seed",
    total_capital_raised_usd=1000000,
    cash_on_hand_usd=800000,
    monthly_burn_usd=50000,
    runway_months=16,
    team_size_full_time=5,
    market_size_usd=10000000000,
    market_growth_rate_annual=25,
    competitor_count=150,
    market_share_percentage=0.1,
    customer_acquisition_cost_usd=1000,
    lifetime_value_usd=10000,
    monthly_active_users=100000,
    product_stage="beta",
    proprietary_tech=False,
    patents_filed=0,
    founders_industry_experience_years=10,
    b2b_or_b2c="b2b",
    burn_rate_usd=50000,
    investor_tier_primary="tier_2",
    customer_count=0
)

# Try to create the prompt
engine = MichelinAnalysisEngine()
try:
    prompt = engine._create_phase1_prompt(test_data)
    print("Prompt created successfully!")
    print("First 500 chars of prompt:")
    print(prompt[:500])
except Exception as e:
    print(f"Error creating prompt: {e}")
    import traceback
    traceback.print_exc()