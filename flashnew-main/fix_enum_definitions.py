#!/usr/bin/env python3
"""
Fix missing enum definitions in framework_selector.py
"""

import os
import re

def fix_enum_definitions():
    """Add missing enum values to framework_selector.py"""
    
    selector_file = "/Users/sf/Desktop/FLASH/framework_intelligence/framework_selector.py"
    
    print(f"Fixing enum definitions in {selector_file}...")
    
    with open(selector_file, 'r') as f:
        content = f.read()
    
    original_content = content
    
    # Fix 1: Add missing IndustryType values
    industry_enum_pattern = r'(class IndustryType\(Enum\):[^}]+?OTHER = "Other")'
    match = re.search(industry_enum_pattern, content, re.DOTALL)
    
    if match:
        # Insert new industry types before OTHER
        new_industries = '''    TECHNOLOGY = "Technology"
    REAL_ESTATE = "Real Estate"
    LOGISTICS = "Logistics & Transportation"
    CLEANTECH = "Clean Technology"
    OTHER = "Other"'''
        
        # Replace just the OTHER line with new industries + OTHER
        content = content.replace('    OTHER = "Other"', new_industries)
        print("✅ Added missing IndustryType values")
    
    # Fix 2: Add missing ChallengeType values
    challenge_enum_end = 'OPERATIONAL_EFFICIENCY = "Operational Efficiency"'
    if challenge_enum_end in content:
        # Add new challenge types after OPERATIONAL_EFFICIENCY
        new_challenges = '''    OPERATIONAL_EFFICIENCY = "Operational Efficiency"
    MARKET_PENETRATION = "Market Penetration"
    COMPETITION = "Competition"
    TALENT_ACQUISITION = "Talent Acquisition"
    REGULATORY_COMPLIANCE = "Regulatory Compliance"'''
        
        content = content.replace(
            '    OPERATIONAL_EFFICIENCY = "Operational Efficiency"',
            new_challenges
        )
        print("✅ Added missing ChallengeType values")
    
    # Fix 3: Update challenge mappings to include new values
    challenge_mapping_pattern = r'(def _initialize_challenge_mappings\(self\)[^}]+?return \{[^}]+?\})'
    match = re.search(challenge_mapping_pattern, content, re.DOTALL)
    
    if match:
        # Find the return statement and add new mappings
        mapping_start = content.find('def _initialize_challenge_mappings(self)')
        mapping_end = content.find('def ', mapping_start + 1)
        
        if mapping_start > -1:
            mapping_section = content[mapping_start:mapping_end]
            
            # Check if new challenge types are missing from mappings
            if 'ChallengeType.MARKET_PENETRATION' not in mapping_section:
                # Add new challenge mappings before the closing brace
                insert_pos = mapping_section.rfind('}')
                new_mappings = ''',
            ChallengeType.MARKET_PENETRATION: [
                "ansoff_matrix", "blue_ocean_strategy", "market_segmentation",
                "go_to_market_strategy", "beachhead_strategy"
            ],
            ChallengeType.COMPETITION: [
                "porters_five_forces", "competitive_positioning", "blue_ocean_strategy",
                "differentiation_strategy", "swot_analysis"
            ],
            ChallengeType.TALENT_ACQUISITION: [
                "employer_branding", "talent_pipeline", "recruitment_funnel",
                "competency_framework", "organizational_culture"
            ],
            ChallengeType.REGULATORY_COMPLIANCE: [
                "compliance_framework", "risk_management_framework", "governance_framework",
                "regulatory_mapping", "audit_framework"
            ]
        }'''
                
                new_mapping_section = mapping_section[:insert_pos] + new_mappings + mapping_section[insert_pos:]
                content = content[:mapping_start] + new_mapping_section + content[mapping_end:]
                print("✅ Added challenge mappings for new ChallengeType values")
    
    # Write the updated content
    if content != original_content:
        with open(selector_file, 'w') as f:
            f.write(content)
        print("✅ Enum definitions updated successfully")
    else:
        print("ℹ️  No changes needed")
    
    # Verify the changes
    print("\nVerifying changes...")
    with open(selector_file, 'r') as f:
        updated_content = f.read()
    
    # Check if all required enums are present
    missing = []
    
    # Check IndustryType
    for industry in ["TECHNOLOGY", "REAL_ESTATE", "LOGISTICS", "CLEANTECH"]:
        if f'{industry} = ' not in updated_content:
            missing.append(f"IndustryType.{industry}")
    
    # Check ChallengeType
    for challenge in ["MARKET_PENETRATION", "COMPETITION", "TALENT_ACQUISITION", "REGULATORY_COMPLIANCE"]:
        if f'{challenge} = ' not in updated_content:
            missing.append(f"ChallengeType.{challenge}")
    
    if missing:
        print(f"⚠️  Still missing: {', '.join(missing)}")
    else:
        print("✅ All required enum values are now defined")

if __name__ == "__main__":
    fix_enum_definitions()
    print("\n🎉 Enum definition fixes complete!")