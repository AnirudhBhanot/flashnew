#!/usr/bin/env python3
import json
import requests
import time

# Test data for Framework Intelligence
startup_context = {
    "company_name": "FLASH Analytics",
    "industry": "AI/ML",
    "stage": "Seed",
    "team_size": 18,
    "challenges": [
        "Low market awareness",
        "Limited sales resources",
        "Scaling technical infrastructure",
        "Competitive differentiation"
    ],
    "goals": [
        "Achieve product-market fit",
        "Scale to $10M ARR",
        "Build strong company culture",
        "Establish market leadership"
    ],
    "resources": {
        "budget": "limited",
        "time_horizon": "12-18 months",
        "expertise": ["technical", "product"]
    }
}

print('🧠 Testing Framework Intelligence Engine')
print('='*60)

# 1. Test Framework Recommendations
print('\n📚 1. Framework Recommendations')
print('-'*40)
try:
    response = requests.post(
        'http://localhost:8001/api/frameworks/recommend',
        json={
            "context": startup_context,
            "top_n": 5
        }
    )
    if response.status_code == 200:
        result = response.json()
        recommendations = result.get('recommendations', [])
        print(f"✓ Received {len(recommendations)} framework recommendations")
        
        for i, rec in enumerate(recommendations[:3], 1):
            print(f"\n{i}. {rec['name']}")
            print(f"   Category: {rec['category']}")
            print(f"   Relevance Score: {rec['relevance_score']:.2f}")
            print(f"   Why: {rec['reasoning']}")
    else:
        print(f"✗ Error: {response.status_code}")
        print(f"Response: {response.text}")
except Exception as e:
    print(f"✗ Error: {e}")

# 2. Test Implementation Roadmap
print('\n\n📋 2. Implementation Roadmap')
print('-'*40)
try:
    selected_frameworks = [
        "jobs_to_be_done",
        "okr",
        "lean_startup",
        "pirate_metrics"
    ]
    
    response = requests.post(
        'http://localhost:8001/api/frameworks/roadmap',
        json={
            "selected_frameworks": selected_frameworks,
            "context": startup_context,
            "timeline_months": 6
        }
    )
    if response.status_code == 200:
        result = response.json()
        roadmap = result.get('roadmap', {})
        phases = roadmap.get('phases', [])
        print(f"✓ Generated {len(phases)}-phase implementation roadmap")
        
        for phase in phases[:2]:
            print(f"\nPhase {phase['phase']}: {phase['name']} ({phase['duration']})")
            print(f"Frameworks: {', '.join(phase['frameworks'])}")
            print(f"Key Activities: {len(phase.get('key_activities', []))} items")
    else:
        print(f"✗ Error: {response.status_code}")
        print(f"Response: {response.text}")
except Exception as e:
    print(f"✗ Error: {e}")

# 3. Test Framework Combinations
print('\n\n🔗 3. Framework Combinations')
print('-'*40)
try:
    response = requests.post(
        'http://localhost:8001/api/frameworks/combinations',
        json={
            "primary_framework": "lean_startup",
            "context": startup_context,
            "combination_count": 3
        }
    )
    if response.status_code == 200:
        result = response.json()
        combinations = result.get('combinations', [])
        print(f"✓ Found {len(combinations)} synergistic combinations")
        
        for combo in combinations:
            print(f"\n• {combo['primary']} + {combo['complementary']}")
            print(f"  Synergy Score: {combo['synergy_score']:.2f}")
            print(f"  Benefits: {combo['benefits'][0] if combo.get('benefits') else 'N/A'}")
    else:
        print(f"✗ Error: {response.status_code}")
        print(f"Response: {response.text}")
except Exception as e:
    print(f"✗ Error: {e}")

# 4. Test Categories Listing
print('\n\n📁 4. Framework Categories')
print('-'*40)
try:
    response = requests.get('http://localhost:8001/api/frameworks/categories')
    if response.status_code == 200:
        result = response.json()
        categories = result.get('categories', [])
        print(f"✓ Available categories: {len(categories)}")
        
        for cat in categories[:5]:
            info = cat.get('info', {})
            print(f"\n• {cat['name']}: {info.get('framework_count', 0)} frameworks")
            print(f"  Focus: {info.get('description', 'N/A')[:60]}...")
    else:
        print(f"✗ Error: {response.status_code}")
except Exception as e:
    print(f"✗ Error: {e}")

# 5. Test Framework Details
print('\n\n📖 5. Framework Details')
print('-'*40)
try:
    framework_name = "business_model_canvas"
    response = requests.get(f'http://localhost:8001/api/frameworks/framework/{framework_name}')
    if response.status_code == 200:
        framework = response.json()
        print(f"✓ Framework: {framework.get('display_name', 'N/A')}")
        print(f"  Category: {framework.get('category', 'N/A')}")
        print(f"  Complexity: {framework.get('implementation_complexity', 'N/A')}")
        print(f"  Time to implement: {framework.get('typical_timeline', 'N/A')}")
        print(f"  Key components: {len(framework.get('key_components', []))}")
    else:
        print(f"✗ Error: {response.status_code}")
except Exception as e:
    print(f"✗ Error: {e}")

# 6. Test Implementation Guide
print('\n\n📘 6. Custom Implementation Guide')
print('-'*40)
try:
    response = requests.post(
        'http://localhost:8001/api/frameworks/implementation-guide',
        json={
            "framework": "okr",
            "context": startup_context,
            "specific_challenges": ["alignment between teams", "measuring success"],
            "detail_level": "detailed"
        }
    )
    if response.status_code == 200:
        result = response.json()
        guide = result.get('guide', {})
        print(f"✓ Generated implementation guide for OKRs")
        print(f"  Preparation steps: {len(guide.get('preparation', []))}")
        print(f"  Implementation phases: {len(guide.get('implementation_steps', []))}")
        print(f"  Success metrics: {len(guide.get('success_metrics', []))}")
        print(f"  Common pitfalls: {len(guide.get('common_pitfalls', []))}")
    else:
        print(f"✗ Error: {response.status_code}")
        print(f"Response: {response.text}")
except Exception as e:
    print(f"✗ Error: {e}")

# 7. Test Framework Search
print('\n\n🔍 7. Framework Search')
print('-'*40)
try:
    response = requests.get(
        'http://localhost:8001/api/frameworks/search',
        params={
            "query": "customer",
            "category": "marketing"
        }
    )
    if response.status_code == 200:
        result = response.json()
        results = result.get('results', [])
        print(f"✓ Found {len(results)} frameworks matching 'customer' in marketing")
        
        for framework in results[:3]:
            print(f"\n• {framework['display_name']}")
            print(f"  Relevance: {framework.get('search_relevance', 0):.2f}")
    else:
        print(f"✗ Error: {response.status_code}")
except Exception as e:
    print(f"✗ Error: {e}")

print('\n' + '='*60)
print('✅ Framework Intelligence testing completed!')