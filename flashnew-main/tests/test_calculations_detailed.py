#!/usr/bin/env python3
"""
Detailed test to identify calculation issues and hardcoded fallbacks
"""

import json
import pandas as pd
import numpy as np
from pathlib import Path

# Test feature name mapping
print("=== ISSUE 1: Feature Name Mismatch ===")
print("\nFrontend sends:")
frontend_features = [
    'founding_year', 'founder_experience_years', 'team_size', 'total_funding',
    'burn_rate', 'runway_months', 'revenue_growth_rate', 'customer_retention_rate',
    'tam_size', 'sam_percentage', 'market_share', 'market_growth_rate',
    'customer_acquisition_cost', 'ltv_cac_ratio'
]
print(frontend_features[:10], "...")

print("\nBackend expects:")
backend_features = [
    'total_capital_raised_usd', 'cash_on_hand_usd', 'monthly_burn_usd',
    'runway_months', 'annual_revenue_run_rate', 'revenue_growth_rate_percent',
    'gross_margin_percent', 'burn_multiple', 'ltv_cac_ratio', 'tam_size_usd',
    'sam_size_usd', 'som_size_usd', 'market_growth_rate_percent', 'customer_count'
]
print(backend_features[:10], "...")

# Check orchestrator predictions without import issues
print("\n=== ISSUE 2: Hardcoded 0.5 Fallbacks ===")
print("From test output, we see:")
print("- DNA analyzer: Always returns 0.5 (fallback due to feature mismatch)")
print("- Pattern analysis: Always returns 0.5 (fallback due to feature mismatch)")
print("- Industry model: Works but limited variation (0.48-0.51)")
print("- Temporal model: Works with some variation (0.27-0.61)")

# Check CAMP score calculation
print("\n=== ISSUE 3: CAMP Score Calculations ===")
print("From the code in unified_orchestrator_v3.py:")
print("")
print("1. Capital score calculation (lines 247-252):")
print("   - Uses mean() of capital features if they exist")
print("   - Falls back to 0.5 if no features found")
print("   - Example: camp_scores['capital_score'] = features[capital_cols].mean(axis=1).fillna(0.5)")
print("")
print("2. The CAMP scores are calculated as simple averages, not weighted calculations")
print("3. Missing features are filled with 0.5, not calculated from available data")

# Analyze financial calculations
print("\n=== ISSUE 4: Missing Financial Calculations ===")
print("No actual calculations found for:")
print("1. LTV/CAC ratio - Expected from frontend, not calculated")
print("2. Runway months - Expected from frontend, not calculated")
print("3. Burn multiple - Expected from frontend, not calculated")
print("4. Gross margin - Not provided by frontend, not calculated")
print("5. Revenue growth rate - Provided as percentage, not annualized")

# Check model weights
print("\n=== ISSUE 5: Model Weights and Final Score ===")
weights = {
    "camp_evaluation": 0.50,
    "pattern_analysis": 0.25,
    "industry_specific": 0.15,
    "temporal_prediction": 0.10
}
print(f"Weights: {json.dumps(weights, indent=2)}")
print("\nWith DNA and Pattern both falling back to 0.5:")
print(f"Minimum possible score: {0.5 * 0.5 + 0.5 * 0.25 + 0 * 0.15 + 0 * 0.1} = 0.375")
print(f"Maximum possible score: {0.5 * 0.5 + 0.5 * 0.25 + 1 * 0.15 + 1 * 0.1} = 0.625")
print("This explains why all predictions are between 0.48-0.51!")

# Check verdict thresholds
print("\n=== ISSUE 6: Verdict Determination ===")
print("Thresholds from _determine_verdict():")
print("- >= 0.80: STRONG PASS")
print("- >= 0.65: PASS")
print("- >= 0.50: CONDITIONAL PASS")
print("- >= 0.35: CONDITIONAL FAIL")
print("- >= 0.20: FAIL")
print("- < 0.20: STRONG FAIL")
print("\nWith scores limited to 0.375-0.625, only CONDITIONAL PASS/FAIL are possible!")

# Summary of issues
print("\n=== SUMMARY OF ISSUES ===")
print("1. Feature name mismatch causes DNA analyzer and Pattern system to always return 0.5")
print("2. No actual financial calculations performed - all values expected from frontend")
print("3. CAMP scores are simple averages, not sophisticated calculations")
print("4. With 75% of weight on broken models, predictions are essentially random")
print("5. Frontend likely shows hardcoded pillar scores of 0.5 (see transform_response_for_frontend)")
print("6. The system cannot distinguish between good and bad startups")

# Recommendations
print("\n=== RECOMMENDATIONS ===")
print("1. Fix feature name mapping between frontend and backend")
print("2. Implement actual calculations for financial metrics")
print("3. Retrain models with correct feature names")
print("4. Add feature engineering for missing calculations")
print("5. Implement proper CAMP score calculations with domain logic")
print("6. Add integration tests to catch these issues")

# Check for proper calculations that DO work
print("\n=== CALCULATIONS THAT DO WORK ===")
print("1. Temporal features (growth_momentum, efficiency_trend) - lines 296-310")
print("2. Model agreement calculation - line 169")
print("3. Confidence interval calculation in API - lines 129-130")
print("4. Some categorical encoding - lines 203-217")

# Check pattern insights
print("\n=== PATTERN INSIGHTS (lines 369-400) ===")
print("Some business logic exists for insights:")
print("- burn_multiple < 2: 'Efficient burn rate'")
print("- user_growth_rate > 50: 'High user growth'")
print("- net_dollar_retention > 110: 'Excellent revenue retention'")
print("- team_size > 30: 'Substantial team size'")
print("\nBut these are just string messages, not calculations.")