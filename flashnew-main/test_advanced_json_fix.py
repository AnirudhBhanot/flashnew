#!/usr/bin/env python3
import json
import re

# The exact problematic JSON from the error
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

def advanced_fix_json(json_str):
    """More advanced JSON fixing that handles the specific DeepSeek output patterns"""
    # First, handle the recommendations array specifically
    # Look for patterns like "word: [" without quotes
    json_str = re.sub(r'\b(\w+):\s*\[', r'"\1": [', json_str)
    
    # Now handle object properties without quotes
    # Look for patterns like "{word:" at the start of objects
    json_str = re.sub(r'{\s*(\w+):', r'{"\1":', json_str)
    
    # Handle subsequent properties in objects ", word:"
    json_str = re.sub(r',\s*(\w+):', r', "\1":', json_str)
    
    # Now we need to quote string values
    # This is tricky because we need to identify what's a string vs number/boolean
    
    # Split into lines for easier processing
    lines = json_str.split('\n')
    fixed_lines = []
    
    for line in lines:
        # Skip lines that don't have colons (not property lines)
        if ':' not in line:
            fixed_lines.append(line)
            continue
            
        # Check if this line has an unquoted string value
        # Pattern: "key": value_without_quotes
        match = re.search(r'"(\w+)":\s*([^",\[\]{}]+?)(?=[,}\]])', line)
        if match:
            key, value = match.groups()
            value = value.strip()
            
            # Check if value needs quotes
            if value and not value.startswith('"'):
                # Check if it's not a number, boolean, or null
                if value not in ['true', 'false', 'null']:
                    try:
                        float(value)
                    except ValueError:
                        # It's a string, add quotes
                        line = line.replace(f'"{key}": {value}', f'"{key}": "{value}"')
        
        fixed_lines.append(line)
    
    return '\n'.join(fixed_lines)

print("Testing advanced JSON fix...")
print("Original JSON has error at line 19 column 62")
print("\n" + "="*50 + "\n")

try:
    json.loads(test_json)
    print("✓ Original JSON is valid (unexpected!)")
except json.JSONDecodeError as e:
    print(f"✗ Original JSON error: {e}")
    print(f"   Line {e.lineno}, Column {e.colno}, Position {e.pos}")
    # Show the problematic line
    lines = test_json.split('\n')
    if e.lineno <= len(lines):
        print(f"   Problematic line: {lines[e.lineno-1]}")
        print(f"   Error at: {' ' * (e.colno-1)}^")

print("\n" + "="*50 + "\n")

fixed_json = advanced_fix_json(test_json)
print("Fixed JSON:")

try:
    result = json.loads(fixed_json)
    print("✓ Fixed JSON is valid!")
    print(f"  - Recommendations count: {len(result.get('recommendations', []))}")
    print(f"  - First recommendation: {result['recommendations'][0]['action'][:50]}...")
except json.JSONDecodeError as e:
    print(f"✗ Fixed JSON still has error: {e}")
    print(f"   Line {e.lineno}, Column {e.colno}, Position {e.pos}")
    lines = fixed_json.split('\n')
    if e.lineno <= len(lines):
        print(f"   Problematic line: {lines[e.lineno-1]}")
        print(f"   Error at: {' ' * (e.colno-1)}^")
    
    # Show a few lines around the error
    print("\nContext around error:")
    start = max(0, e.lineno - 3)
    end = min(len(lines), e.lineno + 2)
    for i in range(start, end):
        marker = " -> " if i == e.lineno - 1 else "    "
        print(f"{marker}{i+1}: {lines[i]}")