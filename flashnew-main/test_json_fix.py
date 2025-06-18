#!/usr/bin/env python3
import json
import re

# The problematic JSON from the logs
test_json = '''{
  "position_assessment": {
    "overall_rating": "Moderate",
    "summary": "The company has a moderate competitive position due to high buyer power and competitive rivalry, balanced by low threat of new entry and a strong team. However, limited marketing and economic uncertainty pose risks.",
    "key_strengths": ["Strong team", "Low threat of new entry"],
    "key_vulnerabilities": ["High buyer power", "Limited marketing", "Economic uncertainty"]
  },
  "gaps": [
    {"gap": "Limited marketing and brand awareness", "impact": "High", "urgency": "High"},
    {"gap": "High buyer power reducing pricing flexibility", "impact": "High", "urgency": "Medium"},
    {"gap": "Intense competitive rivalry", "impact": "High", "urgency": "High"}
  ],
  "opportunities": [
    {"opportunity": "Growing market", "potential_impact": "Increased revenue and market share", "time_horizon": "Medium"},
    {"opportunity": "Leverage strong team for innovation", "potential_impact": "Differentiation from competitors", "time_horizon": "Short"},
    {"opportunity": "Explore new customer segments less sensitive to price", "potential_impact": "Reduced buyer power impact", "time_horizon": "Medium"}
  ],
  "threats": [
    {"threat": "Economic uncertainty", "likelihood": "High", "severity": "High"},
    {"threat": "Many alternatives available to buyers", "likelihood": "High", "severity": "High"},
    {"threat": "Intense competition from many players", "likelihood": "High", "severity": "Medium"}
  ],
  recommendations: [
    {action: Invest in marketing to differentiate from competitors, priority: High, expected_outcome: Increased brand awareness and customer loyalty},
    {action: Diversify supplier base to reduce dependency, priority: Medium, expected_outcome: Reduced supply chain risk},
    {action: Leverage strong team to innovate and create unique value propositions, priority: High, expected_outcome: Enhanced competitive advantage and market differentiation}
  ]
}'''

def fix_json_string(json_str):
    """Fix common JSON formatting issues"""
    # First, let's identify the problematic part - it's the recommendations array
    # Split at the recommendations line
    parts = json_str.split('recommendations:')
    if len(parts) == 2:
        before_recs = parts[0]
        recs_part = parts[1]
        
        # Fix the recommendations part
        # Add quotes around 'recommendations'
        fixed = before_recs + '"recommendations":'
        
        # Fix the array items - they have unquoted keys and values
        # Pattern to match the objects in the array
        recs_part = recs_part.strip()
        
        # Replace unquoted property names and values
        # This is a bit hacky but works for this specific case
        recs_part = recs_part.replace('action:', '"action":')
        recs_part = recs_part.replace('priority:', '"priority":')
        recs_part = recs_part.replace('expected_outcome:', '"expected_outcome":')
        recs_part = recs_part.replace('High', '"High"')
        recs_part = recs_part.replace('Medium', '"Medium"')
        
        # Now we need to quote the string values
        # Look for patterns like: "action": text without quotes, 
        lines = recs_part.split('\n')
        fixed_lines = []
        for line in lines:
            if '"action":' in line and not line.strip().startswith('"action": "'):
                # Extract the value part
                match = re.search(r'"action":\s*([^,]+),', line)
                if match:
                    value = match.group(1).strip()
                    line = line.replace(f'"action": {value}', f'"action": "{value}"')
            
            if '"expected_outcome":' in line and not line.strip().endswith('"}'):
                # Extract the value part
                match = re.search(r'"expected_outcome":\s*([^}]+)}', line)
                if match:
                    value = match.group(1).strip()
                    line = line.replace(f'"expected_outcome": {value}', f'"expected_outcome": "{value}"')
            
            fixed_lines.append(line)
        
        return fixed + '\n'.join(fixed_lines)
    
    return json_str

# Test the fix
print("Original JSON (with errors):")
print(test_json[-500:])
print("\n" + "="*50 + "\n")

try:
    json.loads(test_json)
    print("✓ Original JSON is valid (unexpected!)")
except json.JSONDecodeError as e:
    print(f"✗ Original JSON error: {e}")
    print(f"   Error position: {e.pos}")
    print(f"   Context: ...{test_json[max(0, e.pos-50):e.pos+50]}...")

print("\n" + "="*50 + "\n")

fixed_json = fix_json_string(test_json)
print("Fixed JSON:")
print(fixed_json[-500:])

print("\n" + "="*50 + "\n")

try:
    result = json.loads(fixed_json)
    print("✓ Fixed JSON is valid!")
    print(f"  - Recommendations count: {len(result.get('recommendations', []))}")
except json.JSONDecodeError as e:
    print(f"✗ Fixed JSON still has error: {e}")
    print(f"   Error position: {e.pos}")
    print(f"   Context: ...{fixed_json[max(0, e.pos-50):e.pos+50]}...")