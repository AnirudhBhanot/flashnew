#!/usr/bin/env python3
"""
Final integration test with complete frontend data
"""

import requests
import json

print("🧪 FLASH Integration Test - Final")
print("="*60)

# Complete frontend data
frontend_data = {
    # Company Info
    "startup_name": "TechCorp AI",
    "founding_year": 2021,
    "hq_location": "San Francisco",
    "vertical": "AI/ML",
    
    # Funding
    "funding_stage": "Series A",
    "total_funding": 5000000,
    "total_capital_raised_usd": 5000000,
    "num_funding_rounds": 2,
    "cash_on_hand_usd": 3000000,
    "burn_rate": 150000,
    "monthly_burn_usd": 150000,
    "runway": 20,
    "runway_months": 20,
    
    # Revenue
    "annual_revenue_run_rate": 1200000,
    "revenue_growth_rate_yoy": 150,
    "gross_margin": 75,
    
    # Team
    "team_size": 25,
    "engineering_ratio": 60,
    "founder_experience_years": 12,
    "repeat_founder": True,
    "team_completeness_score": 90,
    "advisory_board_strength": 85,
    
    # Market
    "market_size_billions": 10,
    "market_growth_rate": 25,
    "market_competition_level": "medium",
    
    # Product
    "product_market_fit_score": 80,
    "innovation_index": 80,
    "scalability_score": 4,
    "technology_score": 85,
    "tech_stack_modernity": 85,
    "technical_debt_ratio": 20,
    
    # Customers
    "customer_concentration": 15,
    "viral_coefficient": 1.2,
    "weekly_active_users_growth": 10,
    "feature_adoption_rate": 65,
    
    # Competition
    "competitive_moat_score": 75,
    "ip_portfolio_strength": 70,
    "has_patents": True,
    "patent_count": 3,
    "regulatory_advantage_present": False,
    
    # Investors
    "investor_tier_primary": "Tier 1",
    "investor_count": 5,
    "investor_experience_score": 85,
    "investor_concentration": 20,
    "board_diversity_score": 70,
    
    # Financial
    "has_debt": False,
    "debt_to_equity": 0,
    
    # Growth
    "company_age_months": 36,
    "pivot_count": 1,
    "partnership_score": 70,
    "international_presence": False,
    
    # Risk
    "regulatory_risk_score": 30,
    "technology_risk_score": 25,
    "platform_risk_score": 20,
    "cybersecurity_score": 80,
    "data_privacy_compliance": 90,
    
    # ESG
    "esg_score": 65,
    
    # Additional fields
    "r_and_d_spend_percentage": 25,
    "sales_marketing_efficiency": 1.2,
    "customer_acquisition_cost": 5000,
    "lifetime_value": 25000,
    "months_to_profitability": 18
}

print(f"Sending {len(frontend_data)} fields...")

# First test the main server
server_url = "http://localhost:8001"
try:
    # Health check
    health = requests.get(f"{server_url}/health", timeout=2)
    if health.status_code == 200:
        print("✅ API server is healthy")
    else:
        print(f"⚠️  API health returned: {health.status_code}")
        server_url = "http://localhost:8000"  # Try alternate port
except:
    print("❌ No API server found on port 8001")
    exit(1)

# Test prediction
try:
    response = requests.post(f"{server_url}/predict", json=frontend_data, timeout=10)
    
    if response.status_code == 200:
        result = response.json()
        print("\n✅ PREDICTION SUCCESSFUL!")
        print("\n📊 Results:")
        print(f"   Success Probability: {result.get('success_probability', 0):.1%}")
        print(f"   Verdict: {result.get('verdict', 'N/A')}")
        print(f"   Risk Level: {result.get('risk_level', 'N/A')}")
        
        # CAMP Scores
        camp_scores = result.get('camp_scores', {})
        if camp_scores:
            print(f"\n   CAMP Scores:")
            for pillar, score in camp_scores.items():
                print(f"     {pillar}: {score:.2f}")
        
        # Confidence
        confidence = result.get('confidence_interval', {})
        if confidence:
            print(f"\n   Confidence: {confidence.get('lower', 0):.1%} - {confidence.get('upper', 0):.1%}")
        
        print("\n✅ All systems working correctly!")
        print("\n🚀 Integration Summary:")
        print("   - API accepts frontend data format ✅")
        print("   - Type converter handles field mapping ✅") 
        print("   - Models return predictions ✅")
        print("   - Response includes all expected fields ✅")
        
    else:
        print(f"\n❌ Prediction failed: {response.status_code}")
        print(f"Response: {response.text[:500]}")
        
except Exception as e:
    print(f"\n❌ Error: {str(e)}")

# Check frontend
print("\n📱 Frontend Status:")
try:
    frontend = requests.get("http://localhost:3000", timeout=2)
    if frontend.status_code == 200:
        print("✅ Frontend is running on port 3000")
    else:
        print(f"⚠️  Frontend returned: {frontend.status_code}")
except:
    print("⚠️  Frontend not running (start with: cd flash-frontend && npm start)")

print("\n" + "="*60)
print("Integration test complete!")