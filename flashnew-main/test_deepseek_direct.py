#!/usr/bin/env python3
"""
Direct test of DeepSeek API to diagnose issues
"""

import asyncio
import aiohttp
import json

DEEPSEEK_API_KEY = "sk-f68b7148243e4663a31386a5ea6093cf"
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"

async def test_deepseek():
    """Test DeepSeek API directly"""
    
    print("Testing DeepSeek API...")
    print(f"API Key: {DEEPSEEK_API_KEY[:10]}...{DEEPSEEK_API_KEY[-4:]}")
    
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }
    
    # Simple test prompt
    payload = {
        "model": "deepseek-chat",
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful assistant. Always respond with valid JSON."
            },
            {
                "role": "user", 
                "content": 'Please respond with a JSON object containing a greeting. Format: {"greeting": "your message here"}'
            }
        ],
        "temperature": 0.7,
        "max_tokens": 100
    }
    
    async with aiohttp.ClientSession() as session:
        try:
            print("\nSending request to DeepSeek API...")
            async with session.post(DEEPSEEK_API_URL, json=payload, headers=headers, timeout=30) as response:
                print(f"Response status: {response.status}")
                
                response_text = await response.text()
                print(f"Response text: {response_text[:500]}...")
                
                if response.status == 200:
                    result = await response.json()
                    if 'choices' in result and len(result['choices']) > 0:
                        content = result['choices'][0]['message']['content']
                        print(f"\n✅ Success! DeepSeek returned: {content}")
                        
                        # Try to parse as JSON
                        try:
                            parsed = json.loads(content)
                            print(f"✅ Valid JSON: {parsed}")
                        except:
                            print("⚠️  Response is not valid JSON")
                    else:
                        print("❌ No choices in response")
                else:
                    print(f"❌ API Error: {response_text}")
                    
        except asyncio.TimeoutError:
            print("❌ Request timed out")
        except Exception as e:
            print(f"❌ Error: {type(e).__name__}: {e}")

if __name__ == "__main__":
    asyncio.run(test_deepseek())