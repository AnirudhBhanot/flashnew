#!/usr/bin/env python3
"""
Fix DeepSeek integration and add retry mechanism
"""

import os
import re

def fix_deepseek_integration():
    """Add retry mechanism to DeepSeek calls"""
    
    fixes_applied = []
    
    # Fix 1: Update api_framework_intelligent.py
    intelligent_file = "/Users/sf/Desktop/FLASH/api_framework_intelligent.py"
    
    print(f"Fixing {intelligent_file}...")
    
    with open(intelligent_file, 'r') as f:
        content = f.read()
    
    # Add tenacity import if not present
    if 'from tenacity import' not in content:
        # Add after other imports
        import_pos = content.find('import os\n') + len('import os\n')
        new_imports = '''from tenacity import retry, stop_after_attempt, wait_exponential
'''
        content = content[:import_pos] + new_imports + content[import_pos:]
        fixes_applied.append("Added tenacity imports")
    
    # Replace the call_deepseek function with retry logic
    old_function = '''async def call_deepseek(prompt: str, max_tokens: int = 1000) -> str:
    """Call DeepSeek API for framework analysis"""
    try:
        timeout = aiohttp.ClientTimeout(total=30)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            payload = {
                "model": "deepseek-chat",
                "messages": [
                    {
                        "role": "system",
                        "content": "You are a McKinsey senior consultant specializing in business frameworks and strategic analysis."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "temperature": 0.3,
                "max_tokens": max_tokens
            }
            
            headers = {
                "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
                "Content-Type": "application/json"
            }
            
            async with session.post(
                f"{DEEPSEEK_BASE_URL}/chat/completions",
                json=payload,
                headers=headers
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    return data['choices'][0]['message']['content'].strip()
                else:
                    logger.error(f"DeepSeek API error: {response.status}")
                    return None
    except Exception as e:
        logger.error(f"DeepSeek API call failed: {e}")
        return None'''
    
    new_function = '''@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10),
    reraise=True
)
async def call_deepseek(prompt: str, max_tokens: int = 1000) -> str:
    """Call DeepSeek API for framework analysis with retry logic"""
    timeout = aiohttp.ClientTimeout(total=30)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        payload = {
            "model": "deepseek-chat",
            "messages": [
                {
                    "role": "system",
                    "content": "You are a McKinsey senior consultant specializing in business frameworks and strategic analysis."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.3,
            "max_tokens": max_tokens
        }
        
        headers = {
            "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
            "Content-Type": "application/json"
        }
        
        async with session.post(
            f"{DEEPSEEK_BASE_URL}/chat/completions",
            json=payload,
            headers=headers
        ) as response:
            if response.status == 200:
                data = await response.json()
                return data['choices'][0]['message']['content'].strip()
            elif response.status == 429:
                # Rate limit - let retry handle it
                error_data = await response.text()
                logger.warning(f"DeepSeek rate limit: {error_data}")
                raise Exception("Rate limited")
            elif response.status == 401:
                # Auth error - don't retry
                logger.error("DeepSeek authentication failed")
                return None
            else:
                # Other errors - let retry handle
                error_data = await response.text()
                logger.error(f"DeepSeek API error {response.status}: {error_data}")
                raise Exception(f"API error: {response.status}")'''
    
    if old_function in content:
        content = content.replace(old_function, new_function)
        fixes_applied.append("Added retry decorator to call_deepseek")
    
    # Add wrapper function for better error handling
    wrapper_function = '''
async def call_deepseek_safe(prompt: str, max_tokens: int = 1000) -> Optional[str]:
    """Safe wrapper for DeepSeek calls with fallback"""
    try:
        return await call_deepseek(prompt, max_tokens)
    except Exception as e:
        logger.error(f"DeepSeek call failed after retries: {e}")
        return None
'''
    
    if 'call_deepseek_safe' not in content:
        # Add after call_deepseek function
        insert_pos = content.find('async def generate_dynamic_framework_analysis(')
        content = content[:insert_pos] + wrapper_function + '\n' + content[insert_pos:]
        fixes_applied.append("Added call_deepseek_safe wrapper")
    
    # Update calls to use the safe wrapper
    content = content.replace('await call_deepseek(', 'await call_deepseek_safe(')
    
    # Write updated content
    with open(intelligent_file, 'w') as f:
        f.write(content)
    
    print(f"✅ Fixed {len(fixes_applied)} issues in api_framework_intelligent.py")
    
    # Fix 2: Update api_framework_intelligent_enhanced.py
    enhanced_file = "/Users/sf/Desktop/FLASH/api_framework_intelligent_enhanced.py"
    if os.path.exists(enhanced_file):
        print(f"\nFixing {enhanced_file}...")
        
        with open(enhanced_file, 'r') as f:
            enhanced_content = f.read()
        
        # Apply similar fixes
        if 'from tenacity import' not in enhanced_content:
            import_pos = enhanced_content.find('import os\n')
            if import_pos > -1:
                import_pos += len('import os\n')
                enhanced_content = enhanced_content[:import_pos] + new_imports + enhanced_content[import_pos:]
        
        # Update DeepSeek calls to use safe wrapper
        enhanced_content = enhanced_content.replace('await call_deepseek(', 'await call_deepseek_safe(')
        
        with open(enhanced_file, 'w') as f:
            f.write(enhanced_content)
        
        print("✅ Fixed api_framework_intelligent_enhanced.py")
    
    # Fix 3: Add better JSON parsing for DeepSeek responses
    print("\nAdding robust JSON parsing...")
    
    json_parse_function = '''
def parse_deepseek_json(response: str) -> Optional[Dict[str, Any]]:
    """Parse JSON from DeepSeek response with error handling"""
    if not response:
        return None
    
    try:
        # Try direct JSON parsing
        return json.loads(response)
    except json.JSONDecodeError:
        # Try to extract JSON from markdown code blocks
        json_match = re.search(r'```json\s*(.*?)\s*```', response, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group(1))
            except json.JSONDecodeError:
                pass
        
        # Try to find JSON-like structure
        json_match = re.search(r'\{.*\}', response, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group(0))
            except json.JSONDecodeError:
                pass
    
    logger.warning("Could not parse JSON from DeepSeek response")
    return None
'''
    
    # Add this function to api_framework_intelligent.py
    with open(intelligent_file, 'r') as f:
        content = f.read()
    
    if 'parse_deepseek_json' not in content:
        # Add after imports
        insert_pos = content.find('# Router for framework intelligence endpoints')
        content = content[:insert_pos] + json_parse_function + '\n' + content[insert_pos:]
        
        with open(intelligent_file, 'w') as f:
            f.write(content)
        
        print("✅ Added parse_deepseek_json function")
    
    return fixes_applied

if __name__ == "__main__":
    fixed = fix_deepseek_integration()
    print(f"\n🎉 DeepSeek integration fixes complete!")
    print("Improvements added:")
    print("- Retry logic with exponential backoff")
    print("- Rate limit handling")
    print("- Safe wrapper function")
    print("- Robust JSON parsing")