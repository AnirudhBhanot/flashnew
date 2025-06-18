#!/usr/bin/env python3
"""
Complete integration test simulating frontend submission
"""

import requests
import json
import subprocess
import time
import os
import signal

def create_complete_frontend_data():
    """Create complete data as sent by frontend form"""
    return {
        # Company Information
        "startup_name": "TechCorp AI",
        "founding_year": 2021,
        "hq_location": "San Francisco",
        
        # Funding Information
        "funding_stage": "Series A",
        "total_funding": 5000000,
        "total_capital_raised_usd": 5000000,
        "num_funding_rounds": 2,
        "cash_on_hand_usd": 3000000,
        "burn_rate": 150000,
        "monthly_burn_usd": 150000,
        "runway": 20,
        "runway_months": 20,
        
        # Revenue Metrics
        "annual_revenue_run_rate": 1200000,
        "revenue_growth_rate_yoy": 150,
        "gross_margin": 75,
        
        # Business Metrics
        "r_and_d_spend_percentage": 25,
        "sales_marketing_efficiency": 1.2,
        "customer_acquisition_cost": 5000,
        "lifetime_value": 25000,
        "months_to_profitability": 18,
        
        # Team Information
        "team_size": 25,
        "engineering_ratio": 60,
        "founder_experience_years": 12,
        "repeat_founder": True,
        "team_completeness_score": 90,
        "advisory_board_strength": 85,
        
        # Market & Competition
        "market_size_billions": 10,
        "market_growth_rate": 25,
        "market_competition_level": "medium",
        "vertical": "AI/ML",
        
        # Product & Technology
        "product_market_fit_score": 80,
        "innovation_index": 80,
        "scalability_score": 4,
        "technology_score": 85,
        "tech_stack_modernity": 85,
        "technical_debt_ratio": 20,
        
        # Customer Metrics
        "customer_concentration": 15,
        "viral_coefficient": 1.2,
        "weekly_active_users_growth": 10,
        "feature_adoption_rate": 65,
        
        # Competitive Advantage
        "competitive_moat_score": 75,
        "ip_portfolio_strength": 70,
        "has_patents": True,
        "patent_count": 3,
        "regulatory_advantage_present": False,
        
        # Investor Information
        "investor_tier_primary": "Tier 1",
        "investor_count": 5,
        "investor_experience_score": 85,
        "investor_concentration": 20,
        "board_diversity_score": 70,
        
        # Financial Health
        "has_debt": False,
        "debt_to_equity": 0,
        
        # Growth & Operations
        "company_age_months": 36,
        "pivot_count": 1,
        "partnership_score": 70,
        "international_presence": False,
        
        # Risk Factors
        "regulatory_risk_score": 30,
        "technology_risk_score": 25,
        "platform_risk_score": 20,
        "cybersecurity_score": 80,
        "data_privacy_compliance": 90,
        
        # ESG
        "esg_score": 65,
        
        # Additional fields that might be needed
        "burn_multiple": 2.0,
        "network_effects_present": True,
        "has_data_moat": True,
        "key_person_dependency": False,
        "switching_cost_score": 70,
        "brand_strength_score": 65,
        "sector": "technology",
        "tam_size_usd": 10000000000,
        "sam_size_usd": 1000000000,
        "som_size_usd": 100000000,
        "market_growth_rate_percent": 25,
        "customer_count": 100,
        "customer_concentration_percent": 15,
        "user_growth_rate_percent": 120,
        "net_dollar_retention_percent": 115,
        "competition_intensity": "medium",
        "competitors_named_count": 5,
        "founders_count": 2,
        "team_size_full_time": 25,
        "years_experience_avg": 8,
        "domain_expertise_years_avg": 6,
        "prior_startup_experience_count": 3,
        "prior_successful_exits_count": 1,
        "board_advisor_experience_score": 85,
        "c_suite_completeness_percent": 80,
        "revenue_per_employee": 48000,
        "product_stage": "growth",
        "mvp_months_to_market": 6,
        "feature_completeness_percent": 85,
        "technical_complexity_score": 80,
        "api_integration_count": 15,
        "platform_dependency_score": 30,
        "code_quality_score": 85
    }

def test_full_integration():
    """Test complete frontend-backend integration"""
    
    print("🧪 Full Integration Test")
    print("="*60)
    
    # Start API server
    print("\n1️⃣ Starting API server...")
    api_process = subprocess.Popen(
        ["python3", "api_server_unified.py"],
        cwd="/Users/sf/Desktop/FLASH",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    # Wait for server to start
    print("   Waiting for server to initialize...")
    time.sleep(8)
    
    # Check health
    try:
        health_response = requests.get("http://localhost:8001/health")
        if health_response.status_code == 200:
            print("✅ API server is healthy")
        else:
            print("❌ API server health check failed")
            api_process.terminate()
            return False
    except:
        print("❌ API server not responding")
        api_process.terminate()
        return False
    
    # Test prediction with complete data
    print("\n2️⃣ Testing prediction with complete frontend data...")
    frontend_data = create_complete_frontend_data()
    print(f"   Sending {len(frontend_data)} fields")
    
    try:
        response = requests.post("http://localhost:8001/predict", json=frontend_data)
        
        if response.status_code == 200:
            result = response.json()
            print("\n✅ Prediction successful!")
            print(f"   Success Probability: {result.get('success_probability', 0):.1%}")
            print(f"   Verdict: {result.get('verdict', 'N/A')}")
            print(f"   Verdict Strength: {result.get('verdict_strength', 'N/A')}")
            
            # Show CAMP scores
            camp_scores = result.get('camp_scores', {})
            if camp_scores:
                print("\n   CAMP Scores:")
                for pillar, score in camp_scores.items():
                    print(f"     {pillar}: {score:.2f}")
            
            # Show confidence interval
            confidence = result.get('confidence_interval', {})
            if confidence:
                print(f"\n   Confidence Interval: {confidence.get('lower', 0):.1%} - {confidence.get('upper', 0):.1%}")
            
            # Check frontend
            print("\n3️⃣ Checking frontend availability...")
            try:
                frontend_response = requests.get("http://localhost:3000")
                if frontend_response.status_code == 200:
                    print("✅ Frontend is running")
                else:
                    print("❌ Frontend not responding properly")
            except:
                print("⚠️  Frontend not running (start with: cd flash-frontend && npm start)")
            
            api_process.terminate()
            return True
            
        else:
            print(f"\n❌ Prediction failed: {response.status_code}")
            error_detail = response.json()
            if "detail" in error_detail:
                print("\nError details:")
                if isinstance(error_detail["detail"], list):
                    # Show first 5 validation errors
                    for error in error_detail["detail"][:5]:
                        if error.get("type") == "missing":
                            print(f"   Missing field: {error['loc'][1]}")
                        else:
                            print(f"   {error.get('type', 'error')}: {error.get('msg', 'unknown')}")
                else:
                    print(f"   {error_detail['detail']}")
            api_process.terminate()
            return False
            
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        api_process.terminate()
        return False

def main():
    """Run integration test"""
    success = test_full_integration()
    
    print("\n" + "="*60)
    if success:
        print("✅ Integration test PASSED!")
        print("\n🚀 System is ready. To use:")
        print("   1. Start API: cd /Users/sf/Desktop/FLASH && python3 api_server_unified.py")
        print("   2. Start Frontend: cd flash-frontend && npm start")
        print("   3. Open browser to http://localhost:3000")
    else:
        print("❌ Integration test FAILED")
        print("\nCheck:")
        print("   - API server logs: tail -f api_server.log")
        print("   - Missing imports after cleanup")
        print("   - Field mapping in type_converter_simple.py")
    
    return success

if __name__ == "__main__":
    exit(0 if main() else 1)