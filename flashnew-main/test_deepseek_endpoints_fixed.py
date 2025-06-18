#!/usr/bin/env python3
"""
Fixed test for all DeepSeek API endpoints with correct request formats
"""

import requests
import json
import time
from datetime import datetime
from typing import Dict, Any, List
import uuid

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

def test_endpoint(endpoint: str, method: str, data: Dict[str, Any] = None, name: str = "") -> Dict[str, Any]:
    """Test a single endpoint and return results"""
    url = f"{BASE_URL}{endpoint}"
    start_time = time.time()
    
    try:
        headers = {"Content-Type": "application/json"}
        
        if method == "GET":
            response = requests.get(url, params=data, headers=headers)
        else:
            response = requests.post(url, json=data, headers=headers)
        
        response_time = (time.time() - start_time) * 1000  # Convert to milliseconds
        
        result = {
            "name": name,
            "endpoint": endpoint,
            "status_code": response.status_code,
            "response_time_ms": round(response_time, 2),
            "success": response.status_code == 200,
            "error": None,
            "data": None,
            "uses_deepseek": False,
            "is_fallback": False,
            "response_size": len(response.text)
        }
        
        if response.status_code == 200:
            try:
                response_data = response.json()
                result["data"] = response_data
                
                # Analyze response to determine if DeepSeek was used
                response_str = json.dumps(response_data)
                
                # Check for indicators of AI-generated content
                ai_indicators = [
                    len(response_str) > 1000,  # Substantial response
                    "insights" in response_str.lower(),
                    "recommend" in response_str.lower(),
                    "analysis" in response_str.lower(),
                    "strategic" in response_str.lower(),
                    "narrative" in response_str.lower()
                ]
                
                # Check for specific patterns in each endpoint type
                if "recommendations" in endpoint:
                    if isinstance(response_data.get("recommendations"), list):
                        recs = response_data["recommendations"]
                        if recs and isinstance(recs[0], dict):
                            # Check for AI-generated structure
                            if "how" in recs[0] and isinstance(recs[0]["how"], list):
                                result["uses_deepseek"] = True
                            elif "category" in recs[0]:  # Fallback structure
                                result["is_fallback"] = True
                
                elif "deep-analysis" in endpoint:
                    analysis = response_data.get("analysis", {})
                    if "insights" in analysis and len(str(analysis["insights"])) > 500:
                        result["uses_deepseek"] = True
                    else:
                        result["is_fallback"] = True
                
                elif "whatif" in endpoint:
                    scenarios = response_data.get("scenarios", [])
                    if scenarios and "narrative" in scenarios[0]:
                        result["uses_deepseek"] = True
                    else:
                        result["is_fallback"] = True
                
                elif "market" in endpoint:
                    insights = response_data.get("insights", {})
                    if insights and sum(ai_indicators) >= 3:
                        result["uses_deepseek"] = True
                    else:
                        result["is_fallback"] = True
                
                elif "competitors" in endpoint:
                    competitors = response_data.get("competitors", [])
                    if competitors and len(response_str) > 1000:
                        result["uses_deepseek"] = True
                    else:
                        result["is_fallback"] = True
                
            except json.JSONDecodeError:
                result["error"] = "Invalid JSON response"
        else:
            try:
                error_data = response.json()
                result["error"] = json.dumps(error_data)
            except:
                result["error"] = response.text[:500]
        
        return result
        
    except requests.exceptions.ConnectionError:
        return {
            "name": name,
            "endpoint": endpoint,
            "status_code": 0,
            "response_time_ms": 0,
            "success": False,
            "error": "Connection refused - is the API server running on port 8001?",
            "data": None,
            "uses_deepseek": False,
            "is_fallback": False,
            "response_size": 0
        }
    except Exception as e:
        return {
            "name": name,
            "endpoint": endpoint,
            "status_code": 0,
            "response_time_ms": 0,
            "success": False,
            "error": str(e),
            "data": None,
            "uses_deepseek": False,
            "is_fallback": False,
            "response_size": 0
        }

def main():
    """Test all DeepSeek API endpoints"""
    print("=" * 80)
    print("FLASH Platform - DeepSeek API Endpoint Testing (Fixed)")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)
    print()
    
    # Define endpoints to test with correct request formats
    endpoints_to_test = [
        {
            "name": "1. Dynamic Recommendations",
            "endpoint": "/api/analysis/recommendations/dynamic",
            "method": "POST",
            "data": {
                "startup_data": SAMPLE_STARTUP_DATA,
                "scores": SAMPLE_SCORES,
                "verdict": "promising"
            }
        },
        {
            "name": "2. Deep Framework Analysis",
            "endpoint": "/api/frameworks/deep-analysis",
            "method": "POST",
            "data": {
                "startup_data": SAMPLE_STARTUP_DATA,
                "analysis_depth": "comprehensive"
            }
        },
        {
            "name": "3. What-If Analysis",
            "endpoint": "/api/analysis/whatif/dynamic",
            "method": "POST",
            "data": {
                "startup_data": SAMPLE_STARTUP_DATA,
                "current_scores": SAMPLE_SCORES,
                "improvements": [
                    {
                        "id": str(uuid.uuid4()),
                        "description": "Increase revenue by 50%",
                        "camp_area": "market"
                    },
                    {
                        "id": str(uuid.uuid4()),
                        "description": "Reduce burn by 20%",
                        "camp_area": "capital"
                    }
                ]
            }
        },
        {
            "name": "4. Market Insights",
            "endpoint": "/api/analysis/insights/market",
            "method": "POST",
            "data": {
                "startup_data": SAMPLE_STARTUP_DATA
            }
        },
        {
            "name": "5. Competitor Analysis",
            "endpoint": "/api/analysis/competitors/analyze",
            "method": "POST",
            "data": {
                "startup_data": SAMPLE_STARTUP_DATA,
                "top_n": 5
            }
        }
    ]
    
    # Test each endpoint
    results = []
    deepseek_times = []
    fallback_times = []
    
    for test in endpoints_to_test:
        print(f"\nTesting: {test['name']}")
        print(f"Endpoint: {test['endpoint']}")
        print("-" * 60)
        
        result = test_endpoint(test["endpoint"], test["method"], test.get("data"), test["name"])
        results.append(result)
        
        # Print result summary
        if result["success"]:
            print(f"✅ Status: {result['status_code']} OK")
            print(f"⏱️  Response Time: {result['response_time_ms']}ms")
            print(f"📦 Response Size: {result['response_size']} bytes")
            
            if result["uses_deepseek"]:
                print("🤖 Using: DeepSeek API (AI-generated content)")
                deepseek_times.append(result['response_time_ms'])
            elif result["is_fallback"]:
                print("⚠️  Using: Fallback Mode (pre-defined responses)")
                fallback_times.append(result['response_time_ms'])
            else:
                print("❓ Using: Unknown mode")
            
            # Show sample of response
            if result["data"]:
                print("\nSample Response:")
                response_str = json.dumps(result["data"], indent=2)
                if len(response_str) > 400:
                    print(response_str[:400] + "\n... (truncated)")
                else:
                    print(response_str)
        else:
            print(f"❌ Status: {result['status_code']} - Error")
            print(f"Error: {result['error'][:200]}")
    
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
    
    # Performance analysis
    print("\n" + "-" * 40)
    print("PERFORMANCE ANALYSIS")
    print("-" * 40)
    
    if deepseek_times:
        avg_deepseek = sum(deepseek_times) / len(deepseek_times)
        print(f"🤖 DeepSeek Average Response Time: {avg_deepseek:.2f}ms")
        print(f"   Min: {min(deepseek_times):.2f}ms, Max: {max(deepseek_times):.2f}ms")
    
    if fallback_times:
        avg_fallback = sum(fallback_times) / len(fallback_times)
        print(f"⚠️  Fallback Average Response Time: {avg_fallback:.2f}ms")
        print(f"   Min: {min(fallback_times):.2f}ms, Max: {max(fallback_times):.2f}ms")
    
    # Check backend.log for recent DeepSeek activity
    print("\n" + "=" * 80)
    print("RECENT DEEPSEEK API ACTIVITY (from backend.log)")
    print("=" * 80)
    
    try:
        import subprocess
        log_check = subprocess.run(
            ["tail", "-n", "50", "backend.log"],
            capture_output=True,
            text=True,
            cwd="/Users/sf/Desktop/FLASH"
        )
        
        if log_check.returncode == 0:
            log_lines = log_check.stdout.split('\n')
            deepseek_logs = [line for line in log_lines if 'deepseek' in line.lower() or 'DeepSeek' in line]
            
            if deepseek_logs:
                print("\nRecent DeepSeek API calls:")
                for log in deepseek_logs[-10:]:  # Show last 10
                    if len(log) > 120:
                        print(f"  {log[:120]}...")
                    else:
                        print(f"  {log}")
            else:
                print("\n⚠️  No recent DeepSeek activity found in logs")
        else:
            print("\n⚠️  Could not read backend.log")
    except Exception as e:
        print(f"\n⚠️  Error checking backend.log: {e}")
    
    # Detailed results table
    print("\n" + "=" * 80)
    print("DETAILED RESULTS TABLE")
    print("=" * 80)
    print(f"\n{'Endpoint':<30} {'Status':<10} {'Time (ms)':<12} {'Mode':<15} {'Size':<10}")
    print("-" * 80)
    
    for r in results:
        mode = "DeepSeek" if r["uses_deepseek"] else ("Fallback" if r["is_fallback"] else "Unknown")
        status = "✅ OK" if r["success"] else "❌ Error"
        print(f"{r['name']:<30} {status:<10} {r['response_time_ms']:<12.2f} {mode:<15} {r['response_size']:<10}")
    
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
                "avg_deepseek_time_ms": avg_deepseek if deepseek_times else 0,
                "avg_fallback_time_ms": avg_fallback if fallback_times else 0
            },
            "detailed_results": results
        }, f, indent=2)
    
    print(f"\n💾 Detailed results saved to: {output_file}")
    
    # Final recommendation
    print("\n" + "=" * 80)
    print("RECOMMENDATIONS")
    print("=" * 80)
    
    if using_deepseek < len(results) / 2:
        print("\n⚠️  WARNING: Less than half of the endpoints are using DeepSeek API!")
        print("   This may indicate:")
        print("   - API key issues")
        print("   - Rate limiting")
        print("   - Fallback mode being triggered too often")
        print("\n   Check the backend.log for errors and ensure DEEPSEEK_API_KEY is set correctly.")
    else:
        print("\n✅ DeepSeek API integration appears to be working correctly!")
        print(f"   - {using_deepseek}/{len(results)} endpoints are using AI-generated responses")
        print(f"   - Average response time: {avg_deepseek:.2f}ms")

if __name__ == "__main__":
    main()