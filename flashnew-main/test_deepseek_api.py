#!/usr/bin/env python3
"""
Simple test for DeepSeek API
"""

import aiohttp
import asyncio
import json
import os

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "sk-f68b7148243e4663a31386a5ea6093cf")
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"

async def test_api():
    """Test basic API call"""
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Say 'Hello, API is working!' and nothing else."}
        ],
        "temperature": 0.7,
        "max_tokens": 50
    }
    
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(DEEPSEEK_API_URL, json=payload, headers=headers) as response:
                print(f"Status: {response.status}")
                print(f"Headers: {dict(response.headers)}")
                
                response_text = await response.text()
                print(f"Response: {response_text}")
                
                if response.status == 200:
                    result = json.loads(response_text)
                    content = result['choices'][0]['message']['content']
                    print(f"\n✅ Success! Response: {content}")
                else:
                    print(f"\n❌ Error: {response.status}")
                    
        except Exception as e:
            print(f"\n❌ Exception: {type(e).__name__}: {e}")

if __name__ == "__main__":
    print("Testing DeepSeek API...")
    print(f"API Key: {DEEPSEEK_API_KEY[:10]}...{DEEPSEEK_API_KEY[-4:]}")
    print(f"URL: {DEEPSEEK_API_URL}\n")
    
    asyncio.run(test_api())