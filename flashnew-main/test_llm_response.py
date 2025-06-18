#!/usr/bin/env python3
import asyncio
import aiohttp
import json
import os

async def test_deepseek_directly():
    """Test DeepSeek API directly to see the raw response"""
    
    url = "https://api.deepseek.com/v1/chat/completions"
    api_key = os.getenv("DEEPSEEK_API_KEY", "sk-f68b7148243e4663a31386a5ea6093cf")
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # Use a simpler prompt that should produce clean JSON
    prompt = """Return a JSON object with this exact structure:
{
  "recommendations": [
    {"action": "Action 1", "priority": "High", "expected_outcome": "Outcome 1"},
    {"action": "Action 2", "priority": "Medium", "expected_outcome": "Outcome 2"}
  ]
}

Make sure all property names and string values are in double quotes."""
    
    payload = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": "You are a JSON generator. Always return valid JSON with all property names and values properly quoted."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.3,  # Lower temperature for more consistent output
        "max_tokens": 500
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload, headers=headers) as response:
            result = await response.json()
            content = result['choices'][0]['message']['content']
            
            print("Raw response from DeepSeek:")
            print(content)
            print("\n" + "="*50 + "\n")
            
            # Try to parse it
            try:
                # Remove markdown if present
                if content.strip().startswith('```'):
                    content = content.strip()
                    if content.startswith('```json'):
                        content = content[7:]
                    else:
                        content = content[3:]
                    if content.endswith('```'):
                        content = content[:-3]
                    content = content.strip()
                
                parsed = json.loads(content)
                print("✓ Successfully parsed JSON!")
                print(json.dumps(parsed, indent=2))
            except json.JSONDecodeError as e:
                print(f"✗ Failed to parse: {e}")
                print(f"Content that failed: {content}")

if __name__ == "__main__":
    asyncio.run(test_deepseek_directly())