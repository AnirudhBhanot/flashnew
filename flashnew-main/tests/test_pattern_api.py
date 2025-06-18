#!/usr/bin/env python3
"""
Test Pattern API End-to-End
"""

import requests
import json

# Test data for a typical Series A B2B SaaS startup
test_startup = {
    # Capital metrics
    "funding_stage": "series_a",  # Use API validation format
    "total_capital_raised_usd": 15000000,
    "cash_on_hand_usd": 10000000,
    "monthly_burn_usd": 400000,
    "runway_months": 25,
    "annual_revenue_run_rate": 5000000,
    "revenue_growth_rate_percent": 150,
    "gross_margin_percent": 75,
    "burn_multiple": 1.5,
    "ltv_cac_ratio": 3.5,
    "investor_tier_primary": "tier_1",
    "has_debt": False,
    
    # Advantage metrics
    "patent_count": 2,
    "network_effects_present": True,
    "has_data_moat": True,
    "regulatory_advantage_present": False,
    "tech_differentiation_score": 4,
    "switching_cost_score": 3,  # Added - required field
    "brand_strength_score": 3.5,  # Added - required field
    "scalability_score": 4,
    "product_stage": "growth",
    "product_retention_30d": 0.85,
    "product_retention_90d": 0.75,  # Added - required field
    
    # Market metrics
    "sector": "SaaS",  # Added - required field
    "tam_size_usd": 5000000000,  # Changed from tam_usd
    "sam_size_usd": 500000000,  # Added - required field
    "som_size_usd": 50000000,  # Added - required field
    "market_growth_rate_percent": 25,
    "customer_count": 120,  # Added - required field
    "customer_concentration_percent": 15,
    "user_growth_rate_percent": 180,  # Added - required field
    "net_dollar_retention_percent": 115,
    "competition_intensity": 3,  # Added - required field
    "competitors_named_count": 15,  # Added - required field
    "dau_mau_ratio": 0.65,  # Added - required field
    
    # People metrics
    "founders_count": 2,  # Added - required field
    "team_size_full_time": 35,
    "years_experience_avg": 12,  # Added - required field
    "domain_expertise_years_avg": 8,  # Added - required field
    "prior_startup_experience_count": 3,  # Added - required field
    "prior_successful_exits_count": 1,
    "board_advisor_experience_score": 3.5,  # Changed from advisor_tier_score
    "advisors_count": 5,  # Added - required field
    "team_diversity_percent": 40,
    "key_person_dependency": False  # Added - required field
}

def test_pattern_api():
    """Test the pattern-enhanced API endpoint"""
    
    base_url = "http://localhost:8001"
    
    # 1. Test health endpoint
    print("1. Testing health endpoint...")
    response = requests.get(f"{base_url}/health")
    health = response.json()
    print(f"   - Status: {health['status']}")
    print(f"   - Pattern support: {health['pattern_support']}")
    print(f"   - Pattern models loaded: {health['pattern_models_loaded']}")
    
    # 2. Test patterns list endpoint
    print("\n2. Testing patterns endpoint...")
    response = requests.get(f"{base_url}/patterns")
    patterns = response.json()
    print(f"   - Total patterns: {patterns['total_patterns']}")
    print(f"   - Pattern models loaded: {patterns['pattern_models_loaded']}")
    print(f"   - First 3 patterns: {[p['name'] for p in patterns['patterns'][:3]]}")
    
    # Test standard prediction first
    print("\n2.5. Testing standard prediction...")
    response = requests.post(
        f"{base_url}/predict",
        json=test_startup,
        headers={"Content-Type": "application/json"}
    )
    
    if response.status_code == 200:
        result = response.json()
        print(f"   - Success probability: {result['success_probability']:.2%}")
        print(f"   - Risk level: {result['risk_level']}")
        print(f"   - Verdict: {result['verdict']}")
    else:
        print(f"   - Error: {response.status_code}")
        print(f"   - Details: {response.text}")
    
    # 3. Test pattern-enhanced prediction
    print("\n3. Testing pattern-enhanced prediction...")
    response = requests.post(
        f"{base_url}/predict_enhanced",
        json=test_startup,
        headers={"Content-Type": "application/json"}
    )
    
    if response.status_code == 200:
        result = response.json()
        
        print(f"   - Success probability: {result['success_probability']:.2%}")
        print(f"   - Pattern-adjusted probability: {result.get('pattern_adjusted_probability', 'N/A')}")
        print(f"   - Risk level: {result['risk_level']}")
        print(f"   - Verdict: {result['verdict']}")
        
        if 'pattern_analysis' in result:
            pattern = result['pattern_analysis']['primary_pattern']
            print(f"\n   Pattern Analysis:")
            print(f"   - Primary pattern: {pattern['name']}")
            print(f"   - Confidence: {pattern['confidence']:.2%}")
            print(f"   - Expected success rate: {pattern['expected_success_rate']:.2%}")
            print(f"   - Similar companies: {', '.join(pattern['similar_companies'][:3])}")
            
            if pattern['recommendations']:
                print(f"\n   Recommendations:")
                for i, rec in enumerate(pattern['recommendations'][:3], 1):
                    print(f"   {i}. {rec}")
        else:
            print("   - No pattern analysis in response")
    else:
        print(f"   - Error: {response.status_code}")
        print(f"   - Details: {response.text}")
    
    # 4. Test pattern analysis endpoint
    print("\n4. Testing pattern analysis endpoint...")
    response = requests.post(
        f"{base_url}/analyze_pattern",
        json=test_startup,
        headers={"Content-Type": "application/json"}
    )
    
    if response.status_code == 200:
        analysis = response.json()
        print(f"   - Primary pattern: {analysis['primary_pattern']['name']}")
        print(f"   - Pattern confidence: {analysis['primary_pattern']['confidence']:.2%}")
        print(f"   - Tags: {', '.join(analysis['tags'][:5])}")
    else:
        print(f"   - Error: {response.status_code}")
        print(f"   - Details: {response.text}")

if __name__ == "__main__":
    test_pattern_api()