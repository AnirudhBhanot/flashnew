#!/usr/bin/env python3
import asyncio
import aiohttp
import json
import os

async def test_direct_api():
    url = "https://api.deepseek.com/v1/chat/completions"
    api_key = os.getenv("DEEPSEEK_API_KEY", "sk-f68b7148243e4663a31386a5ea6093cf")
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    prompt = """Analyze the competitive position. Return ONLY valid JSON:
{
  "position_assessment": {
    "overall_rating": "Strong/Moderate/Weak",
    "summary": "Brief summary"
  }
}"""
    
    payload = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": "You are a strategic analyst."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 2000
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload, headers=headers) as response:
            result = await response.json()
            content = result['choices'][0]['message']['content']
            print("Response content:")
            print(content)
            print("\nLength:", len(content))

if __name__ == "__main__":
    asyncio.run(test_direct_api())