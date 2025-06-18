#!/usr/bin/env python3
"""
Fix API endpoint issues for Deep Dive and Framework Intelligence
"""

import os
import sys
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def fix_framework_endpoints():
    """Fix the Framework Intelligence endpoint issues"""
    
    # Read the current api_framework_endpoints.py
    with open('api_framework_endpoints.py', 'r') as f:
        content = f.read()
    
    # Fix 1: Update the roadmap endpoint to handle framework.category correctly
    # Find the line with framework.category
    old_line = '"category": framework.category.value,'
    new_line = '"category": framework.category.value if hasattr(framework.category, "value") else str(framework.category),'
    
    if old_line in content:
        content = content.replace(old_line, new_line)
        logger.info("Fixed framework.category access in api_framework_endpoints.py")
    
    # Fix 2: Add proper error handling for framework attributes
    fixes = [
        (
            'framework = rec.framework',
            '''framework = rec.framework
            # Ensure framework is properly loaded
            if isinstance(framework, str):
                logger.warning(f"Framework {framework} is string, not object")
                continue'''
        ),
        (
            '"category": framework.category.value if hasattr(framework.category, "value") else str(framework.category),',
            '"category": getattr(framework.category, "value", str(framework.category)) if hasattr(framework, "category") else "Unknown",'
        )
    ]
    
    for old, new in fixes:
        if old in content and new not in content:
            content = content.replace(old, new)
    
    # Write the fixed content back
    with open('api_framework_endpoints.py', 'w') as f:
        f.write(content)
    
    logger.info("Framework endpoints fixed")

def fix_deepdive_endpoint_registration():
    """Ensure Deep Dive endpoints are properly registered"""
    
    # Check if the endpoints exist in api_llm_endpoints.py
    with open('api_llm_endpoints.py', 'r') as f:
        llm_content = f.read()
    
    # Verify the deep dive endpoints are defined
    deepdive_endpoints = [
        '/deepdive/phase1/analysis',
        '/deepdive/phase2/vision-reality',
        '/deepdive/phase3/organizational',
        '/deepdive/phase4/scenarios',
        '/deepdive/synthesis'
    ]
    
    missing_endpoints = []
    for endpoint in deepdive_endpoints:
        if endpoint not in llm_content:
            missing_endpoints.append(endpoint)
    
    if missing_endpoints:
        logger.warning(f"Missing deep dive endpoints: {missing_endpoints}")
    else:
        logger.info("All deep dive endpoints are defined in api_llm_endpoints.py")
    
    # Check if llm_router is properly included in api_server_unified.py
    with open('api_server_unified.py', 'r') as f:
        server_content = f.read()
    
    if 'app.include_router(llm_router)' in server_content:
        logger.info("LLM router is properly included in API server")
    else:
        logger.error("LLM router is NOT included in API server!")
        # Add the include statement if missing
        # Find the right place to add it (after auth router)
        if 'app.include_router(auth_router)' in server_content:
            insertion_point = server_content.find('app.include_router(auth_router)') + len('app.include_router(auth_router)')
            new_content = server_content[:insertion_point] + '''

# Include LLM endpoints if available
if LLM_ENDPOINTS_AVAILABLE:
    app.include_router(llm_router)
    logger.info("LLM endpoints enabled")''' + server_content[insertion_point:]
            
            with open('api_server_unified.py', 'w') as f:
                f.write(new_content)
            logger.info("Added LLM router inclusion to API server")

def fix_validation_errors():
    """Fix validation errors in request models"""
    
    # Read api_llm_endpoints.py
    with open('api_llm_endpoints.py', 'r') as f:
        content = f.read()
    
    # Fix 1: Ensure all request models have proper field_validator instead of validator
    if '@validator(' in content:
        content = content.replace('@validator(', '@field_validator(')
        logger.info("Updated validators to field_validators")
    
    # Fix 2: Add missing imports if needed
    if 'from pydantic import BaseModel, Field, field_validator' not in content:
        # Update the import
        old_import = 'from pydantic import BaseModel, Field, field_validator, validator'
        new_import = 'from pydantic import BaseModel, Field, field_validator'
        content = content.replace(old_import, new_import)
        logger.info("Fixed pydantic imports")
    
    # Write back the fixed content
    with open('api_llm_endpoints.py', 'w') as f:
        f.write(content)
    
    logger.info("Fixed validation errors in LLM endpoints")

def create_test_script():
    """Create a test script to verify the fixes"""
    
    test_script = '''#!/usr/bin/env python3
"""
Test script to verify Deep Dive and Framework Intelligence endpoints
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_framework_endpoints():
    """Test Framework Intelligence endpoints"""
    print("\\n=== Testing Framework Intelligence Endpoints ===")
    
    # Test recommendation endpoint
    print("\\n1. Testing /api/frameworks/recommend")
    request_data = {
        "company_stage": "mvp",
        "industry": "saas",
        "primary_challenge": "customer_acquisition",
        "team_size": 10,
        "resources": "limited",
        "timeline": "3 months",
        "goals": ["increase revenue", "improve retention"],
        "current_frameworks": []
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/frameworks/recommend", json=request_data)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print("✓ Framework recommendations working")
            print(f"Recommendations: {len(response.json().get('recommendations', []))}")
        else:
            print(f"✗ Error: {response.text}")
    except Exception as e:
        print(f"✗ Request failed: {e}")
    
    # Test roadmap endpoint
    print("\\n2. Testing /api/frameworks/roadmap")
    try:
        response = requests.post(f"{BASE_URL}/api/frameworks/roadmap", json=request_data)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print("✓ Framework roadmap working")
        else:
            print(f"✗ Error: {response.text}")
    except Exception as e:
        print(f"✗ Request failed: {e}")

def test_deepdive_endpoints():
    """Test Progressive Deep Dive endpoints"""
    print("\\n=== Testing Progressive Deep Dive Endpoints ===")
    
    # Test Phase 1
    print("\\n1. Testing Phase 1 - Competitive Analysis")
    phase1_data = {
        "porters_five_forces": {
            "supplier_power": {"rating": "Medium", "factors": ["Limited suppliers"], "score": 6.5},
            "buyer_power": {"rating": "High", "factors": ["Many alternatives"], "score": 7.8},
            "competitive_rivalry": {"rating": "High", "factors": ["Many competitors"], "score": 8.2},
            "threat_of_substitution": {"rating": "Medium", "factors": ["Some alternatives"], "score": 5.5},
            "threat_of_new_entry": {"rating": "Low", "factors": ["High barriers"], "score": 3.2}
        },
        "internal_audit": {
            "strengths": ["Strong tech team", "Innovative product"],
            "weaknesses": ["Limited marketing", "Cash constraints"],
            "opportunities": ["Growing market", "Partnerships"],
            "threats": ["Economic uncertainty", "Regulation"]
        }
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/analysis/deepdive/phase1/analysis", json=phase1_data)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print("✓ Phase 1 analysis working")
        else:
            print(f"✗ Error: {response.text}")
    except Exception as e:
        print(f"✗ Request failed: {e}")
    
    # Test Phase 2
    print("\\n2. Testing Phase 2 - Vision-Reality Analysis")
    phase2_data = {
        "vision_statement": "To become the leading SaaS platform by 2027",
        "current_reality": {
            "market_share": "5%",
            "revenue": "$10M ARR",
            "customer_base": "50 clients"
        },
        "ansoff_matrix_position": "market_penetration"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/analysis/deepdive/phase2/vision-reality", json=phase2_data)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print("✓ Phase 2 analysis working")
        else:
            print(f"✗ Error: {response.text}")
    except Exception as e:
        print(f"✗ Request failed: {e}")

if __name__ == "__main__":
    print("Testing API Endpoints...")
    print("Make sure the API server is running on http://localhost:8000")
    print("=" * 50)
    
    # Wait for user confirmation
    input("Press Enter to start tests...")
    
    test_framework_endpoints()
    test_deepdive_endpoints()
    
    print("\\n" + "=" * 50)
    print("Testing completed!")
'''
    
    with open('test_api_fixes.py', 'w') as f:
        f.write(test_script)
    
    os.chmod('test_api_fixes.py', 0o755)
    logger.info("Created test script: test_api_fixes.py")

def main():
    """Main function to apply all fixes"""
    print("Fixing API Endpoint Issues...")
    print("=" * 50)
    
    try:
        # Fix Framework Intelligence issues
        print("\n1. Fixing Framework Intelligence endpoints...")
        fix_framework_endpoints()
        
        # Fix Deep Dive endpoint registration
        print("\n2. Fixing Deep Dive endpoint registration...")
        fix_deepdive_endpoint_registration()
        
        # Fix validation errors
        print("\n3. Fixing validation errors...")
        fix_validation_errors()
        
        # Create test script
        print("\n4. Creating test script...")
        create_test_script()
        
        print("\n" + "=" * 50)
        print("✓ All fixes applied successfully!")
        print("\nNext steps:")
        print("1. Restart the API server: ./start_fixed_system.sh")
        print("2. Run the test script: python test_api_fixes.py")
        
    except Exception as e:
        logger.error(f"Error applying fixes: {e}")
        raise

if __name__ == "__main__":
    main()