#!/usr/bin/env python3
"""
Simple API test with proper field mapping
"""

import requests
import json

def test_api():
    """Test API with properly mapped fields"""
    
    # Frontend-style data (what the UI sends)
    frontend_data = {
        "funding_stage": "Series A",
        "total_capital_raised_usd": 5000000,
        "cash_on_hand_usd": 3000000,
        "monthly_burn_usd": 150000,
        "annual_revenue_run_rate": 1200000,
        "revenue_growth_rate_yoy": 150,
        "gross_margin": 75,
        "r_and_d_spend_percentage": 25,
        "sales_marketing_efficiency": 1.2,
        "customer_acquisition_cost": 5000,
        "lifetime_value": 25000,
        "months_to_profitability": 18,
        "investor_tier_primary": "Tier 1",
        "investor_experience_score": 85,
        "board_diversity_score": 70,
        "scalability_score": 4,
        "innovation_index": 80,
        "competitive_moat_score": 75,
        "technical_debt_ratio": 20,
        "team_size": 25,
        "engineering_ratio": 60,
        "founder_experience_years": 12,
        "repeat_founder": True,
        "team_completeness_score": 90,
        "advisory_board_strength": 85,
        "company_age_months": 24,
        "pivot_count": 1,
        "partnership_score": 70,
        "customer_concentration": 15,
        "international_presence": False,
        "esg_score": 65,
        "market_size_billions": 10,
        "market_growth_rate": 25,
        "market_competition_level": "medium",
        "regulatory_risk_score": 30,
        "technology_risk_score": 25,
        "ip_portfolio_strength": 70,
        "product_market_fit_score": 80,
        "viral_coefficient": 1.2,
        "weekly_active_users_growth": 10,
        "feature_adoption_rate": 65,
        "tech_stack_modernity": 85,
        "cybersecurity_score": 80,
        "data_privacy_compliance": 90,
        "platform_risk_score": 20,
        
        # Add missing fields with defaults
        "founding_year": 2023,
        "total_funding": 5000000,
        "num_funding_rounds": 2,
        "burn_rate": 150000,
        "runway": 20,
        "investor_count": 5,
        "investor_concentration": 20,
        "has_debt": False,
        "debt_to_equity": 0
    }
    
    print("🧪 Testing API with frontend data format...")
    print(f"📊 Sending {len(frontend_data)} fields")
    
    try:
        response = requests.post("http://localhost:8001/predict", json=frontend_data)
        
        if response.status_code == 200:
            result = response.json()
            print("\n✅ Prediction successful!")
            print(f"Success Probability: {result.get('success_probability', 0):.1%}")
            print(f"Verdict: {result.get('verdict', 'N/A')}")
            
            # Show CAMP scores
            camp_scores = result.get('camp_scores', {})
            if camp_scores:
                print("\nCAMP Scores:")
                for pillar, score in camp_scores.items():
                    print(f"  {pillar}: {score:.2f}")
            
            # Show model predictions
            model_predictions = result.get('model_predictions', {})
            if model_predictions:
                print("\nModel Predictions:")
                for model, pred in model_predictions.items():
                    print(f"  {model}: {pred:.3f}")
                    
            return True
        else:
            print(f"\n❌ Prediction failed: {response.status_code}")
            error_detail = response.json()
            if "detail" in error_detail:
                print("\nMissing fields:")
                for error in error_detail["detail"][:5]:  # Show first 5 errors
                    if error["type"] == "missing":
                        print(f"  - {error['loc'][1]}")
            return False
            
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        return False

if __name__ == "__main__":
    test_api()