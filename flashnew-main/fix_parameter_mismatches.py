#!/usr/bin/env python3
"""
Fix parameter mismatches between frontend and backend
"""

import os
import re

def fix_parameter_mismatches():
    """Fix all parameter mismatches in framework API files"""
    
    fixes_applied = []
    
    # Fix 1: Update challenge mappings in api_framework_endpoints.py
    endpoint_file = "/Users/sf/Desktop/FLASH/api_framework_endpoints.py"
    
    print(f"Fixing {endpoint_file}...")
    
    with open(endpoint_file, 'r') as f:
        content = f.read()
    
    # Find the challenge_map section
    challenge_map_pattern = r'challenge_map = \{([^}]+)\}'
    match = re.search(challenge_map_pattern, content, re.DOTALL)
    
    if match:
        # Replace with comprehensive mapping
        new_challenge_map = '''challenge_map = {
        # Frontend values
        "finding_product_market_fit": ChallengeType.PRODUCT_DEVELOPMENT,
        "fundraising": ChallengeType.FUNDING,
        "accelerating_growth": ChallengeType.SCALING,
        "scaling_operations": ChallengeType.SCALING,
        # Original values
        "raising_funding": ChallengeType.FUNDING,
        "customer_acquisition": ChallengeType.CUSTOMER_ACQUISITION,
        "team_building": ChallengeType.TEAM_BUILDING,
        "revenue_growth": ChallengeType.SCALING,
        "operational_efficiency": ChallengeType.OPERATIONAL_EFFICIENCY,
        # Additional common values
        "product_development": ChallengeType.PRODUCT_DEVELOPMENT,
        "market_expansion": ChallengeType.MARKET_PENETRATION,
        "competition": ChallengeType.COMPETITION,
        "talent_acquisition": ChallengeType.TALENT_ACQUISITION,
        "regulatory": ChallengeType.REGULATORY_COMPLIANCE
    }'''
        
        content = content[:match.start()] + new_challenge_map + content[match.end():]
        fixes_applied.append("challenge_map")
    
    # Fix 2: Update industry mappings
    industry_map_pattern = r'industry_map = \{([^}]+)\}'
    match = re.search(industry_map_pattern, content, re.DOTALL)
    
    if match:
        # Replace with comprehensive mapping
        new_industry_map = '''industry_map = {
        # Frontend values
        "tech": IndustryType.TECHNOLOGY,
        "technology": IndustryType.TECHNOLOGY,
        "artificial_intelligence": IndustryType.DEEPTECH,
        "ai": IndustryType.DEEPTECH,
        "ai-ml": IndustryType.DEEPTECH,
        "machine-learning": IndustryType.DEEPTECH,
        # Original values
        "b2b_saas": IndustryType.B2B_SAAS,
        "b2c_saas": IndustryType.B2C_SAAS,
        "saas": IndustryType.B2B_SAAS,
        "ecommerce": IndustryType.ECOMMERCE,
        "marketplace": IndustryType.MARKETPLACE,
        "fintech": IndustryType.FINTECH,
        "healthtech": IndustryType.HEALTHTECH,
        "healthcare": IndustryType.HEALTHTECH,
        "edtech": IndustryType.EDTECH,
        "enterprise": IndustryType.ENTERPRISE,
        "consumer": IndustryType.CONSUMER,
        "hardware": IndustryType.HARDWARE,
        "deeptech": IndustryType.DEEPTECH,
        "services": IndustryType.SERVICES,
        "retail": IndustryType.RETAIL,
        "manufacturing": IndustryType.MANUFACTURING,
        # Additional values
        "blockchain": IndustryType.FINTECH,
        "crypto": IndustryType.FINTECH,
        "real-estate": IndustryType.REAL_ESTATE,
        "transportation": IndustryType.LOGISTICS,
        "clean-tech": IndustryType.CLEANTECH,
        "deep-tech": IndustryType.DEEPTECH
    }'''
        
        content = content[:match.start()] + new_industry_map + content[match.end():]
        fixes_applied.append("industry_map")
    
    # Fix 3: Update stage mappings
    stage_map_pattern = r'stage_map = \{([^}]+)\}'
    match = re.search(stage_map_pattern, content, re.DOTALL)
    
    if match:
        # Replace with comprehensive mapping
        new_stage_map = '''stage_map = {
        # Frontend values
        "pre_seed": BusinessStage.IDEA,
        "pre-seed": BusinessStage.IDEA,
        "seed": BusinessStage.MVP,
        "series_a": BusinessStage.GROWTH,
        "series-a": BusinessStage.GROWTH,
        "series_b": BusinessStage.GROWTH,
        "series-b": BusinessStage.GROWTH,
        "series_c": BusinessStage.SCALE,
        "series-c": BusinessStage.SCALE,
        # Original values
        "idea": BusinessStage.IDEA,
        "mvp": BusinessStage.MVP,
        "product_market_fit": BusinessStage.PRODUCT_MARKET_FIT,
        "growth": BusinessStage.GROWTH,
        "scale": BusinessStage.SCALE,
        "mature": BusinessStage.MATURE,
        # Additional values
        "startup": BusinessStage.MVP,
        "expansion": BusinessStage.SCALE
    }'''
        
        content = content[:match.start()] + new_stage_map + content[match.end():]
        fixes_applied.append("stage_map")
    
    # Write the updated content
    with open(endpoint_file, 'w') as f:
        f.write(content)
    
    print(f"✅ Fixed {len(fixes_applied)} parameter mappings in api_framework_endpoints.py")
    print(f"   Fixed: {', '.join(fixes_applied)}")
    
    # Fix 4: Check if ChallengeType enum needs updating
    selector_file = "/Users/sf/Desktop/FLASH/framework_intelligence/framework_selector.py"
    if os.path.exists(selector_file):
        print(f"\nChecking {selector_file} for enum definitions...")
        
        with open(selector_file, 'r') as f:
            selector_content = f.read()
        
        # Check if all challenge types exist
        missing_challenges = []
        challenges_to_check = [
            "PRODUCT_DEVELOPMENT",
            "FUNDING", 
            "SCALING",
            "CUSTOMER_ACQUISITION",
            "TEAM_BUILDING",
            "OPERATIONAL_EFFICIENCY",
            "MARKET_PENETRATION",
            "COMPETITION",
            "TALENT_ACQUISITION",
            "REGULATORY_COMPLIANCE"
        ]
        
        for challenge in challenges_to_check:
            if challenge not in selector_content:
                missing_challenges.append(challenge)
        
        if missing_challenges:
            print(f"⚠️  Missing challenge types in enum: {', '.join(missing_challenges)}")
            print("   These need to be added to ChallengeType enum")
        else:
            print("✅ All challenge types are defined in enum")
        
        # Check IndustryType enum
        missing_industries = []
        industries_to_check = [
            "TECHNOLOGY",
            "DEEPTECH",
            "REAL_ESTATE",
            "LOGISTICS", 
            "CLEANTECH"
        ]
        
        for industry in industries_to_check:
            if f"IndustryType.{industry}" not in selector_content and f"{industry} =" not in selector_content:
                missing_industries.append(industry)
        
        if missing_industries:
            print(f"⚠️  Missing industry types in enum: {', '.join(missing_industries)}")
            print("   These need to be added to IndustryType enum")
        else:
            print("✅ All industry types are defined in enum")
    
    return fixes_applied

if __name__ == "__main__":
    fixed = fix_parameter_mismatches()
    print(f"\n🎉 Parameter mismatch fixes complete!")
    print("Note: You may need to update the enum definitions if warnings were shown above.")