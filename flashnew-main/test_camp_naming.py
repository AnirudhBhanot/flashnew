#!/usr/bin/env python3
"""Test CAMP naming consistency in frontend components"""

import os
import re

def check_camp_naming():
    """Check that CAMP names are used consistently"""
    
    # Components to check
    components = [
        "flash-frontend/src/components/v3/WeightageExplanation.tsx",
        "flash-frontend/src/components/v3/WorldClassResults.tsx",
        "flash-frontend/src/components/v3/FullAnalysisView.tsx"
    ]
    
    # Business terms we're replacing
    old_terms = {
        "Capital Efficiency": "Capital",
        "Competitive Advantage": "Advantage", 
        "Market Opportunity": "Market",
        "Team Quality": "People"
    }
    
    print("Checking CAMP naming consistency...\n")
    
    for component in components:
        if os.path.exists(component):
            with open(component, 'r') as f:
                content = f.read()
                
            print(f"Checking {os.path.basename(component)}:")
            
            # Check for old business terms
            found_old = False
            for old_term, new_term in old_terms.items():
                if old_term in content:
                    print(f"  ❌ Found '{old_term}' - should be '{new_term}'")
                    found_old = True
            
            # Check for new CAMP terms with subtitles
            if "subtitle:" in content:
                print(f"  ✅ Using subtitle pattern for business-friendly descriptions")
            
            if not found_old:
                print(f"  ✅ No old business terms found")
                
            print()

if __name__ == "__main__":
    check_camp_naming()