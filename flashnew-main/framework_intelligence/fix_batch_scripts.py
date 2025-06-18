#!/usr/bin/env python3
"""Fix batch scripts to use correct Framework object syntax"""

import re

def fix_batch_file(filename):
    """Fix a batch file to use Framework objects correctly"""
    with open(filename, 'r') as f:
        content = f.read()
    
    # Replace add_framework( with add_framework(Framework(
    content = re.sub(r'expander\.add_framework\(\s*\n\s*id=', 
                     'expander.add_framework(Framework(\n        id=', 
                     content)
    
    # Add industry_relevance to all frameworks and close with ))
    # This is a bit complex, so let's do it step by step
    
    # First, find all complexity=ComplexityLevel.* patterns followed by )
    pattern = r'(complexity=ComplexityLevel\.[A-Z]+)\s*\n\s*\)'
    
    def add_industry_relevance(match):
        complexity_line = match.group(1)
        # Determine industry relevance based on context
        return f'{complexity_line},\n        industry_relevance=["All industries"]\n    ))'
    
    content = re.sub(pattern, add_industry_relevance, content)
    
    # Write the fixed content
    with open(filename, 'w') as f:
        f.write(content)
    
    print(f"Fixed {filename}")

# Fix batch 4 and 5
fix_batch_file('/Users/sf/Desktop/FLASH/framework_intelligence/expand_frameworks_batch4.py')
fix_batch_file('/Users/sf/Desktop/FLASH/framework_intelligence/expand_frameworks_batch5.py')