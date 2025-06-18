#!/usr/bin/env python3
"""
Improved JSON parser for DeepSeek responses
"""

import re
import json
import logging

logger = logging.getLogger(__name__)

def extract_and_parse_json(response_text: str) -> dict:
    """Extract and parse JSON from LLM response with advanced error recovery"""
    
    if not response_text:
        raise ValueError("Empty response from LLM")
    
    # Step 1: Extract JSON content
    json_str = response_text
    
    # Try to find JSON wrapped in markdown
    json_match = re.search(r'```(?:json)?\s*(.*?)\s*```', response_text, re.DOTALL)
    if json_match:
        json_str = json_match.group(1)
    else:
        # Try to find JSON by looking for opening and closing braces
        json_match = re.search(r'\{[\s\S]*\}', response_text)
        if json_match:
            json_str = json_match.group(0)
    
    # Step 2: Clean up the JSON string
    json_str = json_str.strip()
    
    # Fix triple quotes to single quotes
    json_str = json_str.replace('"""', '"')
    
    # Fix unquoted property names (word followed by colon)
    # This is more aggressive - it will quote any unquoted word before a colon
    json_str = re.sub(r'(\w+)(\s*:\s*)', r'"\1"\2', json_str)
    
    # Fix already quoted property names (avoid double quoting)
    json_str = re.sub(r'"+"', '"', json_str)
    
    # Fix unquoted string values after colons
    # Match : followed by unquoted text that's not a number, boolean, null, or already quoted
    json_str = re.sub(
        r':\s*([A-Za-z][A-Za-z0-9\s\-_]*?)(?=\s*[,}])',
        r': "\1"',
        json_str
    )
    
    # Remove trailing commas
    json_str = re.sub(r',\s*}', '}', json_str)
    json_str = re.sub(r',\s*]', ']', json_str)
    
    # Fix newlines within strings (simplified approach)
    # This is a basic approach - replace newlines that appear to be within strings
    lines = json_str.split('\n')
    fixed_lines = []
    in_string = False
    for line in lines:
        # Count quotes to track if we're in a string
        quote_count = line.count('"') - line.count('\\"')
        if quote_count % 2 == 1:
            in_string = not in_string
        
        if in_string and fixed_lines:
            # Append to previous line instead of new line
            fixed_lines[-1] += ' ' + line.strip()
        else:
            fixed_lines.append(line)
    
    json_str = '\n'.join(fixed_lines)
    
    # Step 3: Try to parse
    try:
        return json.loads(json_str)
    except json.JSONDecodeError as e:
        logger.error(f"Initial parse failed: {e}")
        
        # Step 4: Advanced recovery techniques
        
        # Try to fix specific patterns seen in logs
        # Fix incomplete analysis patterns
        if '"analysis":' in json_str and not re.search(r'"analysis"\s*:\s*"[^"]*"', json_str):
            # Find incomplete analysis fields and close them
            json_str = re.sub(
                r'("analysis"\s*:\s*")([^"]*?)(?=\s*[,}])',
                r'\1\2"',
                json_str
            )
        
        # Fix truncated strings at specific character limits
        if len(json_str) > 3000:
            # Check if we're in the middle of a string
            last_quote_pos = json_str.rfind('"')
            last_comma_pos = json_str.rfind(',')
            last_brace_pos = max(json_str.rfind('}'), json_str.rfind(']'))
            
            if last_quote_pos > max(last_comma_pos, last_brace_pos):
                # We're likely in a string that got cut off
                json_str = json_str[:last_quote_pos + 1]
        
        # Count and balance braces/brackets
        open_braces = json_str.count('{')
        close_braces = json_str.count('}')
        open_brackets = json_str.count('[')
        close_brackets = json_str.count(']')
        
        # Remove any trailing incomplete structures
        if open_braces > close_braces or open_brackets > close_brackets:
            # Find the last complete structure
            last_complete = -1
            brace_count = 0
            bracket_count = 0
            in_string = False
            escape_next = False
            
            for i, char in enumerate(json_str):
                if escape_next:
                    escape_next = False
                    continue
                    
                if char == '\\':
                    escape_next = True
                    continue
                    
                if char == '"' and not escape_next:
                    in_string = not in_string
                    continue
                
                if not in_string:
                    if char == '{':
                        brace_count += 1
                    elif char == '}':
                        brace_count -= 1
                    elif char == '[':
                        bracket_count += 1
                    elif char == ']':
                        bracket_count -= 1
                    
                    if brace_count == 0 and bracket_count == 0 and i > 0:
                        last_complete = i
            
            if last_complete > 0 and last_complete < len(json_str) - 1:
                # Truncate to last complete structure
                json_str = json_str[:last_complete + 1]
            else:
                # Add missing closing characters
                json_str = json_str.rstrip(',')
                json_str += ']' * (open_brackets - close_brackets)
                json_str += '}' * (open_braces - close_braces)
        
        # Final parse attempt
        try:
            return json.loads(json_str)
        except json.JSONDecodeError as e:
            logger.error(f"Advanced recovery failed: {e}")
            logger.error(f"Problematic section: {json_str[max(0, e.pos-50):e.pos+50]}")
            
            # Return a structured error response
            return {
                "error": "JSON_PARSE_FAILED",
                "raw_response": response_text[:1000],
                "attempted_json": json_str[:1000],
                "parse_error": str(e)
            }


# Test with problematic responses from logs
if __name__ == "__main__":
    test_cases = [
        # Case 1: Truncated response
        '''```json
{
  "bcg_matrix_analysis": {
    "position": "Question Mark",
    "market_growth_rate": "High",
    "relative_market_share": "Low",
    "strategic_implications": "The company needs significant investment to capture market share and transition into a Star. Given the strong LTV:CAC ratio, scaling customer acquisition efficiently could drive this transition."
  },
  "porters_five_forces": {
    "threat_of_new_entrants": {
      "level": "Medium",
      "analysis": "Moderate barriers due to proprietary tech and brand differentiation, but the large market attracts new players."
    },
    "supplier_power": {
      "level": "Low",
      "analysis": "Sustainable fashion suppliers are fragmented, giving EcoThread negotiating leverage."
    },
    "buyer_power": {
      "level": "Medium",
      "analysi''',
      
        # Case 2: Unquoted property names
        '''{
    bcg_matrix_analysis: {
        position: "Star",
        market_growth_rate: High,
        relative_market_share: Low,
        strategic_implications: "Company is well positioned"
    }
}''',

        # Case 3: Mixed quotes and truncation
        '''```json
{
  "strategic_options_overview": "Multiple paths available",
  "ansoff_matrix_analysis": {
    "market_penetration": {
      "initiatives": ["Launch targeted digital marketing campaigns", "Introduce loyalty program"],
      "feasibility": "High",
      "expected_impact": "15% growth",
      "timeline": "6-12 months"
    },
    "market_development": {
      "initiatives":[  
         [  
            ",
            "
         ]
   ],
   ",
   ",
   ",
   "
}
]
}'''
    ]
    
    for i, test in enumerate(test_cases):
        print(f"\n=== Test Case {i+1} ===")
        result = extract_and_parse_json(test)
        if "error" in result:
            print(f"Failed to parse: {result['error']}")
        else:
            print(f"Successfully parsed!")
            print(json.dumps(result, indent=2)[:200] + "...")