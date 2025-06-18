#!/usr/bin/env python3
"""
Final comprehensive test for DeepSeek API endpoints with accurate detection
"""

import requests
import json
import time
from datetime import datetime
from typing import Dict, Any, List
import uuid
import sys

# API base URL
BASE_URL = "http://localhost:8001"

# Sample startup data for testing
SAMPLE_STARTUP_DATA = {
    "company_name": "TestStartup AI",
    "funding_stage": "seed",
    "sector": "saas",
    "annual_revenue_run_rate": 750000,
    "revenue_growth_rate_percent": 200,
    "monthly_burn_usd": 60000,
    "runway_months": 15,
    "team_size_full_time": 12,
    "customer_count": 40,
    "net_dollar_retention_percent": 120,
    "years_experience_avg": 8,
    "total_capital_raised_usd": 2000000,
    "tam_size_usd": 15000000000,
    "burn_multiple": 2.0,
    "has_technical_cofounder": True,
    "has_repeat_founders": True,
    "ip_patents": 2,
    "nps_score": 60,
    "customer_acquisition_cost": 4000,
    "average_contract_value": 25000,
    "time_to_product_market_fit": 12,
    "github_stars": 500,
    "web_traffic_monthly": 25000,
    "competition_level": "medium",
    "has_advisors": True,
    "customer_growth_mom": 20,
    "gross_margin_percent": 80,
    "sales_cycle_days": 30,
    "funding_rounds_count": 2,
    "ai_automation_level": "high",
    "data_moat_score": 8,
    "brand_recognition_score": 6,
    "viral_coefficient": 1.2,
    "market_timing_score": 8,
    "pivot_history": 1,
    "technical_debt_score": 2,
    "has_regulatory_approval": True,
    "international_presence": True,
    "mobile_app_rating": 4.5,
    "has_api": True,
    "integration_partners": 10,
    "proprietary_tech": True,
    "open_source_contributions": 500,
    "media_coverage_score": 5,
    "competitive_advantage": "AI-powered automation",
    "lean_startup_score": 9,
    "scalability_score": 9,
    "churn_rate_monthly": 3
}

# Sample CAMP scores
SAMPLE_SCORES = {
    "capital": 0.75,
    "advantage": 0.82,
    "market": 0.78,
    "people": 0.80,
    "success_probability": 0.79
}

def analyze_deepseek_usage(endpoint: str, response_data: dict, response_time: float) -> tuple[bool, bool, str]:
    """
    Analyze if response is from DeepSeek or fallback
    Returns: (uses_deepseek, is_fallback, reason)
    """
    
    # Check response time - DeepSeek calls typically take 5-30 seconds
    if response_time > 5000:  # > 5 seconds suggests API call
        time_suggests_api = True
    else:
        time_suggests_api = False
    
    # Endpoint-specific analysis
    if "recommendations" in endpoint:
        recs = response_data.get("recommendations", [])
        if recs and isinstance(recs[0], dict):
            # DeepSeek structure has detailed fields
            if all(key in recs[0] for key in ["title", "why", "how", "timeline", "impact", "camp_area"]):
                return True, False, "DeepSeek structure with all expected fields"
            # Fallback structure has different fields
            elif "category" in recs[0] and "priority" in recs[0]:
                return False, True, "Fallback structure with category/priority"
    
    elif "deep-analysis" in endpoint:
        # Check if we have the DeepSeek enhanced insights
        analysis = response_data.get("analysis", {})
        insights = analysis.get("insights", [])
        
        # DeepSeek responses have detailed strategic insights
        if insights and len(insights) > 0:
            # DeepSeek insights are typically longer and more detailed
            first_insight = str(insights[0])
            if len(first_insight) > 200:
                return True, False, "DeepSeek-generated detailed insights"
        
        # But also check for the executive summary which indicates processing
        if "executive_summary" in response_data and time_suggests_api:
            exec_summary = response_data["executive_summary"]
            if "key_insights" in exec_summary and len(exec_summary.get("situation", "")) > 50:
                return True, False, "DeepSeek-enhanced executive summary"
    
    elif "whatif" in endpoint:
        scenarios = response_data.get("scenarios", [])
        if scenarios and len(scenarios) > 0:
            # DeepSeek creates narrative scenarios
            if "narrative" in scenarios[0] and len(scenarios[0]["narrative"]) > 100:
                return True, False, "DeepSeek-generated narrative scenarios"
        
        # Check for analysis field as well
        if "analysis" in response_data and isinstance(response_data["analysis"], str):
            if len(response_data["analysis"]) > 200:
                return True, False, "DeepSeek-generated analysis text"
    
    elif "market" in endpoint:
        insights = response_data.get("insights", {})
        
        # DeepSeek market insights are comprehensive
        if insights:
            # Check content depth
            content_length = len(json.dumps(insights))
            if content_length > 500 and time_suggests_api:
                return True, False, "DeepSeek-generated market insights"
        
        # Fallback has simpler structure
        if "market_trends" in response_data and isinstance(response_data["market_trends"], list):
            if time_suggests_api:
                return True, False, "DeepSeek-enhanced market trends"
            else:
                return False, True, "Fallback market trends"
    
    elif "competitors" in endpoint:
        competitors = response_data.get("competitors", [])
        
        # Enhanced fallback is being used for this endpoint
        if competitors and "description" in competitors[0]:
            if time_suggests_api:
                return True, False, "DeepSeek competitor analysis"
            else:
                return False, True, "Enhanced fallback competitor analysis"
    
    # Default fallback detection
    if time_suggests_api:
        return True, False, "Long response time suggests API call"
    else:
        return False, True, "Quick response suggests fallback"

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
            "detection_reason": "",
            "response_size": len(response.text)
        }
        
        if response.status_code == 200:
            try:
                response_data = response.json()
                result["data"] = response_data
                
                # Analyze DeepSeek usage
                uses_deepseek, is_fallback, reason = analyze_deepseek_usage(
                    endpoint, response_data, response_time
                )
                result["uses_deepseek"] = uses_deepseek
                result["is_fallback"] = is_fallback
                result["detection_reason"] = reason
                
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
            "detection_reason": "Connection error",
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
            "detection_reason": "Exception",
            "response_size": 0
        }

def check_backend_logs():
    """Check backend logs for DeepSeek API activity"""
    try:
        import subprocess
        
        # Get last 100 lines of backend.log
        result = subprocess.run(
            ["tail", "-n", "100", "/Users/sf/Desktop/FLASH/backend.log"],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            log_lines = result.stdout.split('\n')
            
            # Analyze DeepSeek activity
            deepseek_calls = []
            deepseek_errors = []
            cache_hits = []
            fallback_uses = []
            
            for line in log_lines:
                if 'Calling DeepSeek API' in line:
                    deepseek_calls.append(line)
                elif 'DeepSeek API response status: 200' in line:
                    deepseek_calls.append(line)
                elif 'DeepSeek' in line and ('error' in line.lower() or 'failed' in line.lower()):
                    deepseek_errors.append(line)
                elif 'Cache hit for llm:' in line:
                    cache_hits.append(line)
                elif 'Using enhanced fallback' in line or 'fallback mode' in line.lower():
                    fallback_uses.append(line)
            
            return {
                "success": True,
                "deepseek_calls": deepseek_calls[-5:],  # Last 5
                "deepseek_errors": deepseek_errors[-3:],  # Last 3
                "cache_hits": cache_hits[-3:],  # Last 3
                "fallback_uses": fallback_uses[-3:]  # Last 3
            }
        else:
            return {"success": False, "error": "Could not read backend.log"}
    except Exception as e:
        return {"success": False, "error": str(e)}

def main():
    """Test all DeepSeek API endpoints"""
    print("=" * 80)
    print("FLASH Platform - DeepSeek API Endpoint Testing (Final)")
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
                "verdict": "strong"
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
                        "description": "Increase revenue by 100% through new product launch",
                        "camp_area": "market"
                    },
                    {
                        "id": str(uuid.uuid4()),
                        "description": "Reduce burn rate by 30% through automation",
                        "camp_area": "capital"
                    },
                    {
                        "id": str(uuid.uuid4()),
                        "description": "Add 2 senior engineers with AI expertise",
                        "camp_area": "people"
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
    
    for i, test in enumerate(endpoints_to_test):
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
                print(f"🤖 Using: DeepSeek API - {result['detection_reason']}")
                deepseek_times.append(result['response_time_ms'])
            elif result["is_fallback"]:
                print(f"⚠️  Using: Fallback Mode - {result['detection_reason']}")
                fallback_times.append(result['response_time_ms'])
            else:
                print("❓ Using: Unknown mode")
            
            # Show key response details
            if result["data"]:
                print("\nKey Response Details:")
                data = result["data"]
                
                if "recommendations" in data:
                    print(f"  - Recommendations: {len(data['recommendations'])} items")
                    if data['recommendations']:
                        first_rec = data['recommendations'][0]
                        print(f"  - Structure: {list(first_rec.keys())[:5]}...")
                
                elif "executive_summary" in data:
                    summary = data["executive_summary"]
                    print(f"  - Executive Summary: {len(summary.get('situation', ''))} chars")
                    print(f"  - Key Insights: {len(summary.get('key_insights', []))} items")
                    print(f"  - Confidence Level: {summary.get('confidence_level', 0)}%")
                
                elif "scenarios" in data:
                    print(f"  - Scenarios: {len(data['scenarios'])} items")
                    if data.get('analysis'):
                        print(f"  - Analysis Length: {len(data['analysis'])} chars")
                
                elif "insights" in data:
                    print(f"  - Insights: {type(data['insights']).__name__}")
                    print(f"  - Content Size: {len(str(data['insights']))} chars")
                
                elif "competitors" in data:
                    print(f"  - Competitors: {len(data['competitors'])} items")
                    
        else:
            print(f"❌ Status: {result['status_code']} - Error")
            print(f"Error: {result['error'][:200]}")
        
        # Add small delay between tests to avoid overwhelming the API
        if i < len(endpoints_to_test) - 1:
            time.sleep(1)
    
    # Check backend logs
    print("\n" + "=" * 80)
    print("BACKEND LOG ANALYSIS")
    print("=" * 80)
    
    log_analysis = check_backend_logs()
    if log_analysis["success"]:
        if log_analysis["deepseek_calls"]:
            print("\n🤖 Recent DeepSeek API Calls:")
            for call in log_analysis["deepseek_calls"]:
                print(f"  {call[:120]}")
        
        if log_analysis["cache_hits"]:
            print("\n💾 Recent Cache Hits:")
            for hit in log_analysis["cache_hits"]:
                print(f"  {hit[:120]}")
        
        if log_analysis["fallback_uses"]:
            print("\n⚠️  Recent Fallback Uses:")
            for fallback in log_analysis["fallback_uses"]:
                print(f"  {fallback[:120]}")
        
        if log_analysis["deepseek_errors"]:
            print("\n❌ Recent DeepSeek Errors:")
            for error in log_analysis["deepseek_errors"]:
                print(f"  {error[:120]}")
    else:
        print(f"\n⚠️  Could not analyze backend logs: {log_analysis['error']}")
    
    # Summary
    print("\n" + "=" * 80)
    print("FINAL SUMMARY")
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
    
    # Detailed results table
    print("\n" + "=" * 80)
    print("DETAILED RESULTS TABLE")
    print("=" * 80)
    print(f"\n{'Endpoint':<30} {'Status':<10} {'Time (ms)':<12} {'Mode':<15} {'Detection Reason':<40}")
    print("-" * 110)
    
    for r in results:
        mode = "DeepSeek" if r["uses_deepseek"] else ("Fallback" if r["is_fallback"] else "Unknown")
        status = "✅" if r["success"] else "❌"
        reason = r["detection_reason"][:40] if r["detection_reason"] else "N/A"
        print(f"{r['name']:<30} {status:<10} {r['response_time_ms']:<12.2f} {mode:<15} {reason:<40}")
    
    # Final assessment
    print("\n" + "=" * 80)
    print("FINAL ASSESSMENT")
    print("=" * 80)
    
    deepseek_percentage = (using_deepseek / successful * 100) if successful > 0 else 0
    
    if deepseek_percentage >= 80:
        print("\n✅ EXCELLENT: DeepSeek API integration is working very well!")
        print(f"   {using_deepseek}/{successful} endpoints are using AI-generated responses ({deepseek_percentage:.0f}%)")
    elif deepseek_percentage >= 60:
        print("\n🟡 GOOD: DeepSeek API integration is mostly working")
        print(f"   {using_deepseek}/{successful} endpoints are using AI-generated responses ({deepseek_percentage:.0f}%)")
    elif deepseek_percentage >= 40:
        print("\n⚠️  FAIR: DeepSeek API integration needs attention")
        print(f"   Only {using_deepseek}/{successful} endpoints are using AI-generated responses ({deepseek_percentage:.0f}%)")
    else:
        print("\n❌ POOR: DeepSeek API integration has issues")
        print(f"   Only {using_deepseek}/{successful} endpoints are using AI-generated responses ({deepseek_percentage:.0f}%)")
    
    # Specific observations
    print("\nSpecific Observations:")
    for r in results:
        if r["success"]:
            if r["uses_deepseek"]:
                print(f"  ✅ {r['name']}: Working correctly with DeepSeek")
            elif r["is_fallback"]:
                print(f"  ⚠️  {r['name']}: Using fallback (check caching or API issues)")
        else:
            print(f"  ❌ {r['name']}: Failed with error")

if __name__ == "__main__":
    main()