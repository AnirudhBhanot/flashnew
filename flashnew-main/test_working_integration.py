#!/usr/bin/env python3
"""
Test integration with proper frontend data format
"""

import requests
import json
import subprocess
import time

def test_frontend_api_integration():
    """Test with data exactly as frontend sends it"""
    
    print("🧪 Testing Frontend-API Integration")
    print("="*60)
    
    # Kill any existing servers
    subprocess.run(["pkill", "-f", "api_server_unified"], capture_output=True)
    time.sleep(2)
    
    # Start API server
    print("\n1️⃣ Starting API server...")
    api_process = subprocess.Popen(
        ["python3", "api_server_unified.py"],
        cwd="/Users/sf/Desktop/FLASH",
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    
    # Wait for server
    print("   Waiting for server initialization...")
    time.sleep(8)
    
    # Check health
    try:
        health = requests.get("http://localhost:8001/health", timeout=5)
        if health.status_code == 200:
            print("✅ API server is healthy")
        else:
            print(f"❌ Health check failed: {health.status_code}")
            api_process.terminate()
            return False
    except Exception as e:
        print(f"❌ API not responding: {e}")
        api_process.terminate()
        return False
    
    # Frontend-style data (exactly as sent by the UI)
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
        
        # Operations
        "r_and_d_spend_percentage": 25,
        "sales_marketing_efficiency": 1.2,
        "customer_acquisition_cost": 5000,
        "lifetime_value": 25000,
        "months_to_profitability": 18,
        
        # Team
        "team_size": 25,
        "engineering_ratio": 60,
        "founder_experience_years": 12,
        "repeat_founder": True,  # Frontend sends boolean
        "team_completeness_score": 90,
        "advisory_board_strength": 85,
        
        # Market
        "market_size_billions": 10,
        "market_growth_rate": 25,
        "market_competition_level": "medium",
        
        # Product
        "product_market_fit_score": 80,
        "innovation_index": 80,
        "scalability_score": 4,  # Frontend sends 1-5
        "technology_score": 85,  # Frontend sends 0-100
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
        "has_patents": True,  # Frontend sends boolean
        "patent_count": 3,
        "regulatory_advantage_present": False,  # Frontend sends boolean
        
        # Investors
        "investor_tier_primary": "Tier 1",  # Frontend format
        "investor_count": 5,
        "investor_experience_score": 85,
        "investor_concentration": 20,  # Frontend sends percentage
        "board_diversity_score": 70,
        
        # Financial
        "has_debt": False,  # Frontend sends boolean
        "debt_to_equity": 0,
        
        # Growth
        "company_age_months": 36,
        "pivot_count": 1,
        "partnership_score": 70,
        "international_presence": False,  # Frontend sends boolean
        
        # Risk
        "regulatory_risk_score": 30,
        "technology_risk_score": 25,
        "platform_risk_score": 20,
        "cybersecurity_score": 80,
        "data_privacy_compliance": 90,
        
        # ESG
        "esg_score": 65
    }
    
    print(f"\n2️⃣ Testing prediction with {len(frontend_data)} frontend fields...")
    
    try:
        response = requests.post(
            "http://localhost:8001/predict",
            json=frontend_data,
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            print("\n✅ Prediction successful!")
            
            # Display results
            print(f"\n📊 Results:")
            print(f"   Success Probability: {result.get('success_probability', 0):.1%}")
            print(f"   Verdict: {result.get('verdict', 'N/A')}")
            print(f"   Verdict Strength: {result.get('verdict_strength', 'N/A')}")
            
            # CAMP Scores
            camp_scores = result.get('camp_scores', {})
            if camp_scores:
                print(f"\n   CAMP Scores:")
                for pillar, score in camp_scores.items():
                    print(f"     {pillar}: {score:.2f}")
            
            # Confidence Interval
            confidence = result.get('confidence_interval', {})
            if confidence:
                print(f"\n   Confidence: {confidence.get('lower', 0):.1%} - {confidence.get('upper', 0):.1%}")
            
            # Model predictions
            model_preds = result.get('model_predictions', {})
            if model_preds:
                print(f"\n   Model Predictions:")
                for model, pred in model_preds.items():
                    print(f"     {model}: {pred:.3f}")
            
            # Check response format matches frontend expectations
            expected_fields = [
                'success_probability', 'verdict', 'verdict_strength',
                'camp_scores', 'confidence_interval', 'risk_level',
                'investment_recommendation'
            ]
            
            missing_fields = [f for f in expected_fields if f not in result]
            if missing_fields:
                print(f"\n⚠️  Missing expected fields: {missing_fields}")
            else:
                print(f"\n✅ All expected fields present in response")
            
            success = True
            
        else:
            print(f"\n❌ Prediction failed: {response.status_code}")
            try:
                error = response.json()
                if "detail" in error and isinstance(error["detail"], list):
                    print("\nValidation errors:")
                    for err in error["detail"][:5]:
                        if err.get("type") == "missing":
                            print(f"   - Missing: {err['loc'][1]}")
                        elif err.get("type") == "less_than_equal":
                            print(f"   - Value too high: {err['loc'][1]} = {err['input']} (max: {err['ctx']['le']})")
                        else:
                            print(f"   - {err.get('type')}: {err['loc'][1]}")
                else:
                    print(f"Error: {json.dumps(error, indent=2)}")
            except:
                print(f"Response: {response.text}")
            success = False
            
    except Exception as e:
        print(f"\n❌ Request failed: {str(e)}")
        success = False
    
    # Cleanup
    api_process.terminate()
    api_process.wait()
    
    # Summary
    print("\n" + "="*60)
    if success:
        print("✅ Frontend-API integration is working!")
        print("\n🚀 Ready to use:")
        print("   1. API: cd /Users/sf/Desktop/FLASH && python3 api_server_unified.py")
        print("   2. Frontend: cd flash-frontend && npm start")
        print("   3. Open: http://localhost:3000")
    else:
        print("❌ Integration still has issues")
        print("\nDebug steps:")
        print("   1. Check api_server.log for errors")
        print("   2. Verify type_converter_simple.py is being used")
        print("   3. Check StartupMetrics model in api_server_unified.py")
    
    return success

if __name__ == "__main__":
    success = test_frontend_api_integration()
    exit(0 if success else 1)