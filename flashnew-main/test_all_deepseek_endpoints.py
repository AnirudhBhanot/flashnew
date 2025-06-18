#!/usr/bin/env python3
"""
Comprehensive test for all DeepSeek API endpoints in FLASH platform
Tests each endpoint and reports on DeepSeek usage vs fallback
"""

import requests
import json
import time
from datetime import datetime
from typing import Dict, Any, List

# API base URL
BASE_URL = "http://localhost:8001"

# Sample startup data for testing
SAMPLE_STARTUP_DATA = {
    "company_name": "TechVision AI",
    "funding_stage": "seed",
    "sector": "saas",
    "annual_revenue_run_rate": 500000,
    "revenue_growth_rate_percent": 150,
    "monthly_burn_usd": 50000,
    "runway_months": 12,
    "team_size_full_time": 8,
    "customer_count": 25,
    "net_dollar_retention_percent": 110,
    "years_experience_avg": 7,
    "total_capital_raised_usd": 1500000,
    "tam_size_usd": 10000000000,
    "burn_multiple": 2.5,
    "has_technical_cofounder": True,
    "has_repeat_founders": False,
    "ip_patents": 0,
    "nps_score": 45,
    "customer_acquisition_cost": 5000,
    "average_contract_value": 20000,
    "time_to_product_market_fit": 18,
    "github_stars": 150,
    "web_traffic_monthly": 10000,
    "competition_level": "high",
    "has_advisors": True,
    "customer_growth_mom": 15,
    "gross_margin_percent": 75,
    "sales_cycle_days": 45,
    "funding_rounds_count": 1,
    "ai_automation_level": "medium",
    "data_moat_score": 6,
    "brand_recognition_score": 4,
    "viral_coefficient": 0.8,
    "market_timing_score": 7,
    "pivot_history": 0,
    "technical_debt_score": 3,
    "has_regulatory_approval": False,
    "international_presence": False,
    "mobile_app_rating": 0,
    "has_api": True,
    "integration_partners": 5,
    "proprietary_tech": True,
    "open_source_contributions": 200,
    "media_coverage_score": 3,
    "competitive_advantage": "AI technology",
    "lean_startup_score": 8,
    "scalability_score": 7,
    "churn_rate_monthly": 5
}

# Sample CAMP scores
SAMPLE_SCORES = {
    "capital": 0.65,
    "advantage": 0.72,
    "market": 0.80,
    "people": 0.68,
    "success_probability": 0.71
}

def test_endpoint(endpoint: str, method: str, data: Dict[str, Any] = None) -> Dict[str, Any]:
    """Test a single endpoint and return results"""
    url = f"{BASE_URL}{endpoint}"
    start_time = time.time()
    
    try:
        if method == "GET":
            response = requests.get(url, params=data)
        else:
            response = requests.post(url, json=data)
        
        response_time = (time.time() - start_time) * 1000  # Convert to milliseconds
        
        result = {
            "endpoint": endpoint,
            "status_code": response.status_code,
            "response_time_ms": round(response_time, 2),
            "success": response.status_code == 200,
            "error": None,
            "data": None,
            "uses_deepseek": False,
            "is_fallback": False
        }
        
        if response.status_code == 200:
            try:
                response_data = response.json()
                result["data"] = response_data
                
                # Check for DeepSeek usage indicators
                if isinstance(response_data, dict):
                    # Check for signs of LLM-generated content
                    if "recommendations" in response_data:
                        recs = response_data["recommendations"]
                        if recs and len(recs) > 0:
                            # Check if recommendations have the expected structure
                            first_rec = recs[0]
                            if all(key in first_rec for key in ["title", "why", "how", "timeline", "impact"]):
                                result["uses_deepseek"] = True
                            else:
                                result["is_fallback"] = True
                    
                    elif "analysis" in response_data:
                        # Deep framework analysis
                        analysis = response_data.get("analysis", {})
                        if "insights" in analysis and isinstance(analysis["insights"], list):
                            if analysis["insights"] and len(analysis["insights"][0]) > 100:
                                result["uses_deepseek"] = True
                            else:
                                result["is_fallback"] = True
                    
                    elif "scenarios" in response_data:
                        # What-if analysis
                        scenarios = response_data.get("scenarios", [])
                        if scenarios and "narrative" in scenarios[0]:
                            result["uses_deepseek"] = True
                        else:
                            result["is_fallback"] = True
                    
                    elif "insights" in response_data:
                        # Market insights
                        insights = response_data.get("insights", {})
                        if insights and "market_trends" in insights:
                            result["uses_deepseek"] = True
                        else:
                            result["is_fallback"] = True
                    
                    elif "competitors" in response_data:
                        # Competitor analysis
                        competitors = response_data.get("competitors", [])
                        if competitors and any("description" in c for c in competitors):
                            result["uses_deepseek"] = True
                        else:
                            result["is_fallback"] = True
                
            except json.JSONDecodeError:
                result["error"] = "Invalid JSON response"
        else:
            result["error"] = response.text[:200]
        
        return result
        
    except requests.exceptions.ConnectionError:
        return {
            "endpoint": endpoint,
            "status_code": 0,
            "response_time_ms": 0,
            "success": False,
            "error": "Connection refused - is the API server running?",
            "data": None,
            "uses_deepseek": False,
            "is_fallback": False
        }
    except Exception as e:
        return {
            "endpoint": endpoint,
            "status_code": 0,
            "response_time_ms": 0,
            "success": False,
            "error": str(e),
            "data": None,
            "uses_deepseek": False,
            "is_fallback": False
        }

def main():
    """Test all DeepSeek API endpoints"""
    print("=" * 80)
    print("FLASH Platform - DeepSeek API Endpoint Testing")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)
    print()
    
    # Define endpoints to test
    endpoints_to_test = [
        {
            "name": "Dynamic Recommendations",
            "endpoint": "/api/analysis/recommendations/dynamic",
            "method": "POST",
            "data": {
                "startup_data": SAMPLE_STARTUP_DATA,
                "scores": SAMPLE_SCORES,
                "verdict": "promising"
            }
        },
        {
            "name": "Deep Framework Analysis",
            "endpoint": "/api/frameworks/deep-analysis",
            "method": "POST",
            "data": SAMPLE_STARTUP_DATA
        },
        {
            "name": "What-If Analysis",
            "endpoint": "/api/analysis/whatif/dynamic",
            "method": "POST",
            "data": {
                "startup_data": SAMPLE_STARTUP_DATA,
                "current_scores": SAMPLE_SCORES,
                "improvements": [
                    {"description": "Increase revenue by 50%", "metric": "revenue", "change": 50},
                    {"description": "Reduce burn by 20%", "metric": "burn", "change": -20}
                ]
            }
        },
        {
            "name": "Market Insights",
            "endpoint": "/api/analysis/insights/market",
            "method": "POST",
            "data": {
                "industry": SAMPLE_STARTUP_DATA["sector"],
                "stage": SAMPLE_STARTUP_DATA["funding_stage"],
                "metrics": {
                    "revenue": SAMPLE_STARTUP_DATA["annual_revenue_run_rate"],
                    "growth_rate": SAMPLE_STARTUP_DATA["revenue_growth_rate_percent"]
                }
            }
        },
        {
            "name": "Competitor Analysis",
            "endpoint": "/api/analysis/competitors/analyze",
            "method": "POST",
            "data": {
                "startup_data": SAMPLE_STARTUP_DATA,
                "market_position": {
                    "revenue_percentile": 65,
                    "growth_percentile": 80,
                    "market_share": 0.5
                }
            }
        }
    ]
    
    # Test each endpoint
    results = []
    for test in endpoints_to_test:
        print(f"\nTesting: {test['name']}")
        print(f"Endpoint: {test['endpoint']}")
        print("-" * 60)
        
        result = test_endpoint(test["endpoint"], test["method"], test.get("data"))
        results.append(result)
        
        # Print result summary
        if result["success"]:
            print(f"✅ Status: {result['status_code']} OK")
            print(f"⏱️  Response Time: {result['response_time_ms']}ms")
            
            if result["uses_deepseek"]:
                print("🤖 Using: DeepSeek API")
            elif result["is_fallback"]:
                print("⚠️  Using: Fallback Mode")
            else:
                print("❓ Using: Unknown")
            
            # Show sample of response
            if result["data"]:
                print("\nSample Response:")
                response_str = json.dumps(result["data"], indent=2)
                if len(response_str) > 500:
                    print(response_str[:500] + "...")
                else:
                    print(response_str)
        else:
            print(f"❌ Status: {result['status_code']} - Error")
            print(f"Error: {result['error']}")
    
    # Summary
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    
    successful = sum(1 for r in results if r["success"])
    failed = len(results) - successful
    using_deepseek = sum(1 for r in results if r["uses_deepseek"])
    using_fallback = sum(1 for r in results if r["is_fallback"])
    
    print(f"\nTotal Endpoints Tested: {len(results)}")
    print(f"✅ Successful: {successful}")
    print(f"❌ Failed: {failed}")
    print(f"🤖 Using DeepSeek API: {using_deepseek}")
    print(f"⚠️  Using Fallback: {using_fallback}")
    
    # Average response time for successful requests
    successful_times = [r["response_time_ms"] for r in results if r["success"]]
    if successful_times:
        avg_time = sum(successful_times) / len(successful_times)
        print(f"\n⏱️  Average Response Time: {avg_time:.2f}ms")
    
    # Check backend.log for DeepSeek errors
    print("\n" + "=" * 80)
    print("CHECKING BACKEND LOG FOR DEEPSEEK ERRORS")
    print("=" * 80)
    
    try:
        import subprocess
        log_check = subprocess.run(
            ["tail", "-n", "100", "backend.log"],
            capture_output=True,
            text=True,
            cwd="/Users/sf/Desktop/FLASH"
        )
        
        if log_check.returncode == 0:
            log_lines = log_check.stdout.split('\n')
            deepseek_errors = [line for line in log_lines if 'deepseek' in line.lower() and ('error' in line.lower() or 'warning' in line.lower())]
            
            if deepseek_errors:
                print("\nRecent DeepSeek-related errors/warnings:")
                for error in deepseek_errors[-5:]:  # Show last 5 errors
                    print(f"  - {error}")
            else:
                print("\n✅ No recent DeepSeek errors found in backend.log")
        else:
            print("\n⚠️  Could not read backend.log")
    except Exception as e:
        print(f"\n⚠️  Error checking backend.log: {e}")
    
    # Save detailed results
    output_file = f"deepseek_test_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(output_file, 'w') as f:
        json.dump({
            "timestamp": datetime.now().isoformat(),
            "summary": {
                "total_tested": len(results),
                "successful": successful,
                "failed": failed,
                "using_deepseek": using_deepseek,
                "using_fallback": using_fallback,
                "avg_response_time_ms": avg_time if successful_times else 0
            },
            "detailed_results": results
        }, f, indent=2)
    
    print(f"\n💾 Detailed results saved to: {output_file}")

if __name__ == "__main__":
    main()