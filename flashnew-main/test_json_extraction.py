#!/usr/bin/env python3
import json
import re
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def _extract_json_from_response(response: str) -> dict:
    """Extract JSON from a response that might contain markdown or extra text"""
    # Try direct JSON parsing first
    try:
        return json.loads(response)
    except json.JSONDecodeError:
        pass
    
    # Try to extract JSON from markdown code blocks
    import re
    
    # Pattern for ```json ... ``` blocks
    json_pattern = r'```json\s*(.*?)\s*```'
    matches = re.findall(json_pattern, response, re.DOTALL | re.MULTILINE)
    if matches:
        try:
            logger.debug(f"Found JSON in markdown block, attempting to parse {len(matches[0])} chars")
            # Strip any extra whitespace
            json_str = matches[0].strip()
            return json.loads(json_str)
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON from markdown: {e}")
            logger.error(f"JSON string: {matches[0][:200]}...")
            pass
    
    # Pattern for ``` ... ``` blocks without json marker
    code_pattern = r'```\s*(.*?)\s*```'
    matches = re.findall(code_pattern, response, re.DOTALL | re.MULTILINE)
    if matches:
        try:
            return json.loads(matches[0])
        except json.JSONDecodeError:
            pass
    
    # Try to find JSON object in the response
    json_start = response.find('{')
    json_end = response.rfind('}')
    if json_start != -1 and json_end > json_start:
        try:
            return json.loads(response[json_start:json_end + 1])
        except json.JSONDecodeError:
            pass
    
    # If all else fails, raise an error
    logger.error(f"Could not extract JSON from response: {response[:200]}...")
    raise ValueError("Could not parse JSON from response")

# Test with the actual response from the logs
test_response = '''```json
{
  "position_assessment": {
    "overall_rating": "Moderate",
    "summary": "The company has a moderate competitive position due to high buyer power and competitive rivalry, balanced by low threat of new entry and medium supplier power.",
    "key_strengths": ["Strong team capabilities", "High barriers to entry protecting market position"],
    "key_vulnerabilities": ["Limited marketing reach", "High buyer bargaining power"]
  },
  "gaps": [
    {"gap": "Marketing and brand awareness", "impact": "High", "urgency": "High"},
    {"gap": "Customer retention strategies", "impact": "High", "urgency": "Medium"},
    {"gap": "Competitive differentiation", "impact": "Medium", "urgency": "High"}
  ],
  "opportunities": [
    {"opportunity": "Expanding into growing market segments", "potential_impact": "Significant revenue growth", "time_horizon": "Medium"},
    {"opportunity": "Leveraging team strengths for innovation", "potential_impact": "Enhanced competitive advantage", "time_horizon": "Short"},
    {"opportunity": "Building strategic partnerships", "potential_impact": "Market expansion and resource sharing", "time_horizon": "Medium"}
  ],
  "threats": [
    {"threat": "Economic uncertainty affecting buyer behavior", "likelihood": "High", "severity": "Medium"},
    {"threat": "Intense competitive rivalry", "likelihood": "High", "severity": "High"},
    {"threat": "Customer switching to alternatives", "likelihood": "Medium", "severity": "High"}
  ],
  "recommendations": [
    {"action": "Develop comprehensive marketing strategy", "priority": "High", "expected_outcome": "Increased brand awareness and customer acquisition"},
    {"action": "Implement customer loyalty programs", "priority": "High", "expected_outcome": "Reduced customer churn and increased lifetime value"},
    {"action": "Differentiate through unique value propositions", "priority": "Medium", "expected_outcome": "Stronger competitive position"}
  ]
}
```'''

print("Testing JSON extraction with actual response...")
try:
    result = _extract_json_from_response(test_response)
    print("✓ Successfully extracted JSON!")
    print(f"  - Overall rating: {result['position_assessment']['overall_rating']}")
    print(f"  - Number of gaps: {len(result['gaps'])}")
    print(f"  - Number of recommendations: {len(result['recommendations'])}")
except Exception as e:
    print(f"✗ Failed to extract JSON: {e}")
    print(f"  - Error type: {type(e).__name__}")