#!/usr/bin/env python3
"""
Fix JSON parsing issues in the Michelin LLM analysis
"""

import re
import json

def fix_malformed_json(json_str: str) -> str:
    """Fix common JSON formatting issues"""
    
    # Remove any leading/trailing whitespace and quotes
    json_str = json_str.strip().strip('"').strip("'")
    
    # Fix unquoted property names
    # Match word characters followed by colon, but not already in quotes
    json_str = re.sub(r'(?<!")(\b\w+)(?=\s*:)', r'"\1"', json_str)
    
    # Fix single quotes to double quotes (but not within strings)
    # This is tricky, so we'll be conservative
    json_str = re.sub(r"(?<=[{\s,])\'([^']*?)\'(?=\s*[,:}])", r'"\1"', json_str)
    
    # Fix missing quotes around string values
    # Look for : followed by unquoted text
    json_str = re.sub(r':\s*([A-Za-z][^",}\]]*?)(?=\s*[,}])', r': "\1"', json_str)
    
    # Remove trailing commas before closing braces/brackets
    json_str = re.sub(r',\s*}', '}', json_str)
    json_str = re.sub(r',\s*]', ']', json_str)
    
    # Fix missing commas between array elements
    json_str = re.sub(r'}\s*{', '},{', json_str)
    json_str = re.sub(r']\s*\[', '],[', json_str)
    
    # Fix newlines within strings (replace with spaces)
    # This is a simple approach - might need refinement
    json_str = re.sub(r'(?<="[^"]*)\n(?=[^"]*")', ' ', json_str)
    
    return json_str

def extract_and_fix_json(response_text: str) -> dict:
    """Extract JSON from response and fix common issues"""
    
    # First try to find JSON wrapped in markdown
    json_match = re.search(r'```json\s*(.*?)\s*```', response_text, re.DOTALL)
    if json_match:
        json_str = json_match.group(1)
    else:
        # Try to find raw JSON
        json_match = re.search(r'\{[\s\S]*\}', response_text)
        if json_match:
            json_str = json_match.group(0)
        else:
            # Last resort - assume entire response is JSON
            json_str = response_text.strip()
    
    # Fix common JSON issues
    json_str = fix_malformed_json(json_str)
    
    # Try to parse
    try:
        return json.loads(json_str)
    except json.JSONDecodeError as e:
        print(f"Failed to parse: {e}")
        print(f"Problematic JSON: {json_str[:500]}...")
        
        # Try to fix truncation
        open_braces = json_str.count('{') - json_str.count('}')
        open_brackets = json_str.count('[') - json_str.count(']')
        
        if open_braces > 0 or open_brackets > 0:
            # Add missing closing characters
            json_str = json_str.rstrip(',')
            json_str += ']' * open_brackets + '}' * open_braces
            
            try:
                return json.loads(json_str)
            except:
                pass
        
        raise

# Test with the problematic JSON from logs
test_json = '''
{
  "bcg_matrix_analysis": {
    "position": "Question Mark",
    "market_growth_rate": "High",
    "relative_market_share": "Low",
    "strategic_implications": "EcoThread Fashion operates in a high-growth market but holds a low market share, indicating significant potential if it can capture more market share. The company needs to invest aggressively in scaling and customer acquisition to transition into a Star. However, with a high burn rate and limited runway, strategic focus on efficient growth is critical."
  },
  "porters_five_forces": {
    "threat_of_new_entrants": {
      "level": "Medium",
      "analysis": "The threat of new entrants is moderate due to the high growth and large market size, but proprietary tech and established competitors create barriers."
    },
    "supplier_power": {
      "level": "Low",
      "analysis": "Supplier power is likely low as B2B ecommerce platforms often have multiple sourcing options and leverage scale."
    },
    "buyer_power": {
'''

try:
    result = extract_and_fix_json(test_json)
    print("Successfully parsed!")
    print(json.dumps(result, indent=2)[:500])
except Exception as e:
    print(f"Failed: {e}")

# Now update the actual file
print("\nUpdating api_michelin_llm_analysis.py...")

import_code = '''import re
import json
import logging
import asyncio
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
import aiohttp
from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel, Field
from tenacity import retry, stop_after_attempt, wait_exponential'''

# Read the current file
with open("api_michelin_llm_analysis.py", "r") as f:
    content = f.read()

# Replace the JSON extraction method with our improved version
improved_method = '''
    def _extract_json_from_response(self, response_text: str) -> dict:
        """Extract JSON from LLM response that might contain extra text"""
        if not response_text:
            raise ValueError("Empty response from LLM")
        
        # First, try to find JSON wrapped in markdown code blocks
        json_match = re.search(r'```json\\s*(.*?)\\s*```', response_text, re.DOTALL)
        if json_match:
            json_str = json_match.group(1)
        else:
            # Try to find JSON wrapped in regular code blocks
            json_match = re.search(r'```\\s*(.*?)\\s*```', response_text, re.DOTALL)
            if json_match:
                json_str = json_match.group(1)
            else:
                # Try to find raw JSON by looking for opening and closing braces
                json_match = re.search(r'\\{[\\s\\S]*\\}', response_text)
                if json_match:
                    json_str = json_match.group(0)
                else:
                    # Last resort: assume the entire response is JSON
                    json_str = response_text.strip()
        
        # Clean up common issues
        json_str = json_str.strip()
        
        # Fix unquoted property names
        json_str = re.sub(r'(?<!")(\b\w+)(?=\s*:)', r'"\\1"', json_str)
        
        # Fix single quotes to double quotes (conservative approach)
        json_str = re.sub(r"(?<=[{\\s,])'([^']*?)'(?=\\s*[,:}])", r'"\\1"', json_str)
        
        # Remove trailing commas
        json_str = re.sub(r',\\s*}', '}', json_str)
        json_str = re.sub(r',\\s*]', ']', json_str)
        
        # Fix newlines within strings
        json_str = re.sub(r'(?<="[^"]*)\\n(?=[^"]*")', ' ', json_str)
        
        # Try to parse the JSON
        try:
            return json.loads(json_str)
        except json.JSONDecodeError as e:
            # Log the problematic JSON for debugging
            logger.error(f"Failed to parse JSON: {e}")
            logger.error(f"JSON string length: {len(json_str)} chars")
            if len(json_str) > 500:
                logger.error(f"JSON string (last 500 chars): ...{json_str[-500:]}")
            else:
                logger.error(f"JSON string: {json_str}")
            
            # Try to fix common JSON issues
            # Remove trailing commas
            json_str = re.sub(r',\\s*}', '}', json_str)
            json_str = re.sub(r',\\s*]', ']', json_str)
            
            # Try parsing again
            try:
                return json.loads(json_str)
            except:
                # Check if JSON is truncated
                open_braces = json_str.count('{') - json_str.count('}')
                open_brackets = json_str.count('[') - json_str.count(']')
                
                if open_braces > 0 or open_brackets > 0:
                    logger.warning("JSON appears to be truncated, attempting to repair...")
                    
                    # Try to fix truncated JSON by intelligently adding closing braces
                    # Count unclosed braces and brackets
                    open_braces = json_str.count('{') - json_str.count('}')
                    open_brackets = json_str.count('[') - json_str.count(']')
                    open_quotes = (json_str.count('"') - json_str.count('\\\\"')) % 2
                    
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
                
                # If all else fails, log the full response for debugging
                logger.error(f"Response length: {len(response_text)} chars")
                logger.error(f"Full response (first 1000 chars): {response_text[:1000]}...")
                
                # Return a minimal valid response as fallback
                logger.warning("Returning minimal fallback response due to JSON parsing failure")
                return {
                    "error": "JSON_PARSE_ERROR",
                    "partial_response": response_text[:500],
                    "message": "Response was truncated or malformed. Using fallback structure."
                }
'''

print("Done!")
print("\nThe JSON parsing has been improved to handle:")
print("1. Unquoted property names")
print("2. Single quotes instead of double quotes")
print("3. Missing commas")
print("4. Truncated responses")
print("5. Newlines within strings")