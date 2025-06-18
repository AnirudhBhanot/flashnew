#!/usr/bin/env python3
"""Test the improved JSON parsing logic"""

import json
import re
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def extract_json_from_response(response_text: str) -> dict:
    """Extract JSON from LLM response that might contain extra text"""
    if not response_text:
        raise ValueError("Empty response from LLM")
    
    # First, try to find JSON wrapped in markdown code blocks
    json_match = re.search(r'```json\s*(.*?)\s*```', response_text, re.DOTALL)
    if json_match:
        json_str = json_match.group(1)
    else:
        # Try to find JSON wrapped in regular code blocks
        json_match = re.search(r'```\s*(.*?)\s*```', response_text, re.DOTALL)
        if json_match:
            json_str = json_match.group(1)
        else:
            # Try to find raw JSON by looking for opening and closing braces
            json_match = re.search(r'\{[\s\S]*\}', response_text)
            if json_match:
                json_str = json_match.group(0)
            else:
                # Last resort: assume the entire response is JSON
                json_str = response_text.strip()
    
    # Clean up common issues
    json_str = json_str.strip()
    
    # Try to parse the JSON
    try:
        return json.loads(json_str)
    except json.JSONDecodeError as e:
        # Log the problematic JSON for debugging
        logger.error(f"Failed to parse JSON: {e}")
        logger.error(f"JSON string length: {len(json_str)} chars")
        logger.error(f"JSON string (last 500 chars): ...{json_str[-500:]}")
        
        # Try to fix common JSON issues
        # Remove trailing commas
        json_str = re.sub(r',\s*}', '}', json_str)
        json_str = re.sub(r',\s*]', ']', json_str)
        
        # Try parsing again
        try:
            return json.loads(json_str)
        except:
            # Check if JSON was truncated
            if len(json_str) > 2000 and not json_str.rstrip().endswith('}'):
                logger.warning("JSON appears to be truncated, attempting to repair...")
                
                # Try to fix truncated JSON by intelligently adding closing braces
                # Count unclosed braces and brackets
                open_braces = json_str.count('{') - json_str.count('}')
                open_brackets = json_str.count('[') - json_str.count(']')
                open_quotes = (json_str.count('"') - json_str.count('\\"')) % 2
                
                # If we have an odd number of quotes, close the string first
                if open_quotes == 1:
                    json_str += '"'
                
                # Close any incomplete array or object
                if json_str.rstrip().endswith(','):
                    json_str = json_str.rstrip()[:-1]  # Remove trailing comma
                
                # Add missing closing brackets and braces
                json_str += ']' * open_brackets + '}' * open_braces
                
                try:
                    logger.info("Successfully repaired truncated JSON")
                    return json.loads(json_str)
                except Exception as repair_error:
                    logger.error(f"Failed to repair JSON: {repair_error}")
            
            # If all else fails, return a minimal valid response as fallback
            logger.warning("Returning minimal fallback response due to JSON parsing failure")
            return {
                "error": "JSON_PARSE_ERROR",
                "partial_response": json_str[:500],
                "message": "Response was truncated or malformed. Using fallback structure."
            }

# Test cases
test_cases = [
    # Case 1: Properly formatted JSON
    ('{"key": "value", "number": 123}', "properly formatted"),
    
    # Case 2: JSON in markdown code block
    ('```json\n{"key": "value", "number": 123}\n```', "markdown code block"),
    
    # Case 3: Truncated JSON
    ('{"bcg_matrix_analysis": {"position": "Star", "market_growth_rate": "High", "relative_market_share": "High", "strategic_implications": "The company is well-positioned"', "truncated JSON"),
    
    # Case 4: JSON with trailing comma
    ('{"key": "value", "items": [1, 2, 3,], "last": true,}', "trailing commas"),
    
    # Case 5: Severely truncated with nested structures
    ('{"phase1": {"analysis": {"strengths": ["Strong team", "Good product", "Market fit"], "weaknesses": ["Limited resources", "Small market share"', "severely truncated"),
]

print("Testing JSON parsing improvements")
print("=" * 50)

for test_input, description in test_cases:
    print(f"\nTest: {description}")
    print(f"Input length: {len(test_input)} chars")
    try:
        result = extract_json_from_response(test_input)
        if result.get('error') == 'JSON_PARSE_ERROR':
            print("❌ Parsing failed - returned fallback structure")
        else:
            print("✅ Successfully parsed!")
            print(f"Result: {json.dumps(result, indent=2)[:200]}...")
    except Exception as e:
        print(f"❌ Error: {e}")

print("\n" + "=" * 50)
print("Test complete!")