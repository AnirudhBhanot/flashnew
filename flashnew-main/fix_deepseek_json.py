#!/usr/bin/env python3
import json
import re

def fix_deepseek_json(json_str):
    """Fix DeepSeek's malformed JSON output"""
    
    # Step 1: Fix unquoted property names
    # Pattern: word followed by colon (not already quoted)
    json_str = re.sub(r'\b(\w+):\s*\[', r'"\1": [', json_str)  # Arrays
    json_str = re.sub(r'{\s*(\w+):', r'{"\1":', json_str)      # Start of objects
    json_str = re.sub(r',\s*(\w+):', r', "\1":', json_str)     # Middle of objects
    
    # Step 2: Fix known unquoted values
    # Replace common unquoted values that should be strings
    json_str = re.sub(r':\s*High(?=[,}\]])', r': "High"', json_str)
    json_str = re.sub(r':\s*Medium(?=[,}\]])', r': "Medium"', json_str)
    json_str = re.sub(r':\s*Low(?=[,}\]])', r': "Low"', json_str)
    json_str = re.sub(r':\s*Short(?=[,}\]])', r': "Short"', json_str)
    json_str = re.sub(r':\s*Long(?=[,}\]])', r': "Long"', json_str)
    
    # Step 3: Fix unquoted string values after colons
    # This is the trickiest part - we need to identify strings that aren't quoted
    
    # Process line by line for more control
    lines = json_str.split('\n')
    fixed_lines = []
    
    for line in lines:
        # Look for patterns like: "key": unquoted string value
        # We need to be careful not to break already-quoted values or arrays/objects
        
        # Pattern to match: "key": value_that_needs_quotes
        # Where value_that_needs_quotes doesn't start with ", [, {, number, true, false, null
        match = re.search(r'"([^"]+)":\s*([^",\[\]{}0-9\-].*?)(?=\s*[,}\]])', line)
        if match:
            key = match.group(1)
            value = match.group(2).strip()
            
            # Check if this value is not already handled and not a boolean/null
            if value not in ['true', 'false', 'null'] and not value.startswith('"'):
                # Quote the entire value
                old_pattern = f'"{key}": {value}'
                new_pattern = f'"{key}": "{value}"'
                line = line.replace(old_pattern, new_pattern)
        
        fixed_lines.append(line)
    
    return '\n'.join(fixed_lines)

# Test with the exact problematic JSON
test_json = '''{
  "position_assessment": {
    "overall_rating": "Moderate",
    "summary": "The company has a moderate competitive position due to high buyer power and competitive rivalry, balanced by low threat of new entry and a strong team. However, limited marketing and economic uncertainty pose risks.",
    "key_strengths": ["Strong team", "Low threat of new entry"],
    "key_vulnerabilities": ["High buyer power", "Limited marketing"]
  },
  "gaps": [
    {"gap": "Limited marketing presence", "impact": "High", "urgency": "High"},
    {"gap": "High buyer power reducing pricing flexibility", "impact": "High", "urgency": "Medium"},
    {"gap": "Intense competitive rivalry", "impact": "High", "urgency": "High"}
  ],
  "opportunities": [
    {"opportunity": "Growing market potential", "potential_impact": "Increased revenue and market share", "time_horizon": "Medium"},
    {"opportunity": "Leverage strong team for innovation", "potential_impact": "Differentiation from competitors", "time_horizon": "Short"},
    {"opportunity": "Explore new customer segments", "potential_impact": "Reduced buyer power impact", "time_horizon": "Medium"}
  ],
  "threats": [
    {"threat": "Economic uncertainty affecting demand", "likelihood": "High", "severity": "High"},
    {"threat": "Buyers have many alternatives", "likelihood": "High", "severity": "High"},
    {"threat": "Intense competition from existing players", "likelihood": "High", "severity": "Medium"}
  ],
  recommendations: [
    {action: Invest in marketing to enhance brand visibility, priority: High, expected_outcome: Increased customer acquisition and retention},
    {action: Diversify supplier base to mitigate risks, priority: Medium, expected_outcome: Reduced supplier dependency and improved negotiation power},
    {action: Focus on product innovation to differentiate from competitors, priority: High, expected_outcome: Enhanced competitive advantage and market positioning}
  ]
}'''

print("Testing comprehensive JSON fix...")

try:
    json.loads(test_json)
    print("✓ Original JSON is valid (unexpected!)")
except json.JSONDecodeError as e:
    print(f"✗ Original JSON error: {e}")

print("\n" + "="*50 + "\n")

fixed_json = fix_deepseek_json(test_json)

try:
    result = json.loads(fixed_json)
    print("✓ Fixed JSON is valid!")
    print(f"\nExtracted data:")
    print(f"  - Overall rating: {result['position_assessment']['overall_rating']}")
    print(f"  - Number of gaps: {len(result['gaps'])}")
    print(f"  - Number of opportunities: {len(result['opportunities'])}")
    print(f"  - Number of threats: {len(result['threats'])}")
    print(f"  - Number of recommendations: {len(result['recommendations'])}")
    print(f"\nFirst recommendation:")
    print(f"  - Action: {result['recommendations'][0]['action']}")
    print(f"  - Priority: {result['recommendations'][0]['priority']}")
    print(f"  - Expected outcome: {result['recommendations'][0]['expected_outcome']}")
except json.JSONDecodeError as e:
    print(f"✗ Fixed JSON still has error: {e}")
    print(f"\nDebugging - show the recommendations section:")
    lines = fixed_json.split('\n')
    for i, line in enumerate(lines):
        if 'recommendations' in line:
            for j in range(max(0, i-1), min(len(lines), i+8)):
                print(f"{j+1}: {lines[j]}")